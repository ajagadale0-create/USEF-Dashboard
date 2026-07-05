# Publish USEF Dashboard on Streamlit Cloud

Follow these steps to get a public URL like `https://your-app.streamlit.app`.

---

## Step 1 — Create a GitHub account & repository

1. Go to [github.com](https://github.com) and sign in (or create account).
2. Click **New repository**.
3. Name it e.g. `usef-sales-dashboard`.
4. Keep it **Public** (required for free Streamlit Cloud).
5. Do **not** add README (we already have files).

---

## Step 2 — Upload these files to GitHub

Upload **only these files/folders** to the repo root:

```
streamlit_app.py                    ← main entry (required)
usef_sales_excellence_dashboard.py  ← dashboard logic
requirements.txt                    ← Python packages
.streamlit/config.toml              ← theme
Data/                               ← pre-built CSV data (fast startup)
  employee.csv
  customer.csv
  product.csv
  sales.csv
  collection.csv
  activity.csv
  target.csv
  forecast.csv
  training.csv
  opportunity.csv
  incentive_config.csv
```

**GitHub web upload:** Repo → **Add file** → **Upload files** → drag all files above.

---

## Step 3 — Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**.
2. Sign in with **GitHub**.
3. Click **New app**.
4. Fill in:
   - **Repository:** `your-username/usef-sales-dashboard`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **Deploy**.

First deploy takes 2–5 minutes. You will get a live URL to share in your interview.

---

## Step 4 — Optional: install Git on your PC (for future updates)

If Git is not installed:

1. Download from [git-scm.com/download/win](https://git-scm.com/download/win)
2. Install with default options.
3. Then in `C:\Python`:

```powershell
cd C:\Python
git init
git add streamlit_app.py usef_sales_excellence_dashboard.py requirements.txt .streamlit/config.toml Data/*.csv
git commit -m "USEF sales excellence dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/usef-sales-dashboard.git
git push -u origin main
```

After that, every `git push` auto-redeploys on Streamlit Cloud.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| App crashes on startup | Check **Manage app → Logs** on Streamlit Cloud |
| Missing module | Add package to `requirements.txt` |
| Slow first load | Ensure `Data/*.csv` files are in the repo |
| Wrong page shown | Main file must be `streamlit_app.py` |

---

## Share in interview

> "I built a universal sales excellence dashboard in Python + Streamlit with 10 pages — command center, employee/customer scorecards, pipeline, forecast, and incentive calculator. It's live at [your-url].streamlit.app and works for any industry by swapping the CSV data source."
