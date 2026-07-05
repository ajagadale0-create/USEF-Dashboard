"""Push dashboard files to GitHub via REST API (no local git required)."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import requests

BASE_DIR = Path(__file__).resolve().parent

DEPLOY_FILES = [
    "streamlit_app.py",
    "usef_sales_excellence_dashboard.py",
    "github_publish.py",
    "requirements.txt",
    "DEPLOY_STREAMLIT.md",
    ".streamlit/config.toml",
    ".gitignore",
]

DATA_FILES = [
    "Data/employee.csv",
    "Data/customer.csv",
    "Data/product.csv",
    "Data/sales.csv",
    "Data/collection.csv",
    "Data/activity.csv",
    "Data/target.csv",
    "Data/forecast.csv",
    "Data/training.csv",
    "Data/opportunity.csv",
    "Data/incentive_config.csv",
]


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def verify_github_token(token: str) -> tuple[bool, str, dict[str, Any] | None]:
    """Return (ok, message, user_json)."""
    if not token or not token.strip():
        return False, "Token is empty.", None
    try:
        resp = requests.get(
            "https://api.github.com/user",
            headers=_headers(token.strip()),
            timeout=30,
        )
    except requests.RequestException as exc:
        return False, f"Network error: {exc}", None
    if resp.status_code == 401:
        return False, "Invalid token. Create a new Personal Access Token on GitHub.", None
    if resp.status_code != 200:
        return False, f"GitHub API error ({resp.status_code}): {resp.text[:200]}", None
    user = resp.json()
    login = user.get("login", "unknown")
    return True, f"Connected as @{login}", user


def repo_exists(token: str, owner: str, repo: str) -> tuple[bool, str]:
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=_headers(token),
            timeout=30,
        )
    except requests.RequestException as exc:
        return False, str(exc)
    if resp.status_code == 200:
        return True, "Repository found."
    if resp.status_code == 404:
        return False, f"Repository '{owner}/{repo}' not found. Create it on GitHub first (public repo)."
    return False, f"GitHub error ({resp.status_code}): {resp.text[:200]}"


def _get_file_sha(token: str, owner: str, repo: str, path: str, branch: str) -> str | None:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=_headers(token), params={"ref": branch}, timeout=30)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def upload_file(
    token: str,
    owner: str,
    repo: str,
    branch: str,
    repo_path: str,
    local_path: Path,
    message: str,
) -> tuple[bool, str]:
    if not local_path.is_file():
        return False, f"Missing local file: {local_path}"
    content = local_path.read_bytes()
    payload: dict[str, Any] = {
        "message": message,
        "content": base64.b64encode(content).decode("ascii"),
        "branch": branch,
    }
    sha = _get_file_sha(token, owner, repo, repo_path.replace("\\", "/"), branch)
    if sha:
        payload["sha"] = sha
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{repo_path.replace(chr(92), '/')}"
    try:
        resp = requests.put(url, headers=_headers(token), json=payload, timeout=60)
    except requests.RequestException as exc:
        return False, str(exc)
    if resp.status_code in (200, 201):
        return True, "OK"
    return False, f"{resp.status_code}: {resp.text[:300]}"


def push_dashboard_to_github(
    token: str,
    owner: str,
    repo: str,
    branch: str = "main",
    commit_message: str = "Update USEF dashboard",
    include_data: bool = True,
) -> tuple[list[str], list[str]]:
    """Upload deploy files. Returns (success_paths, error_messages)."""
    files = list(DEPLOY_FILES)
    if include_data:
        files.extend(DATA_FILES)
    ok_paths: list[str] = []
    errors: list[str] = []
    for rel in files:
        local = BASE_DIR / rel
        success, detail = upload_file(
            token, owner, repo, branch, rel, local, f"{commit_message} — {rel}"
        )
        if success:
            ok_paths.append(rel)
        else:
            errors.append(f"{rel}: {detail}")
    return ok_paths, errors
