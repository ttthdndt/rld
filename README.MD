# SKU Scan — StockX Lookup Tool

A web app to look up StockX product data by SKU. Built with FastAPI (backend) + HTML/CSS/JS (frontend).

## Project Structure

```
stockx-lookup/
├── backend/
│   ├── main.py           # FastAPI app
│   └── requirements.txt
├── frontend/
│   └── index.html        # Single-file frontend
├── vercel.json           # Backend deployment config
└── README.md
```

---

## 🚀 Deployment Guide

### Step 1 — Push to GitHub

1. Create a new repo on GitHub (e.g. `stockx-lookup`)
2. Push this project:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/stockx-lookup.git
git push -u origin main
```

---

### Step 2 — Deploy Backend on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import your GitHub repo
3. Add Environment Variable:
   - Key: `RAPIDAPI_KEY`
   - Value: `c71d279a4emshe0f0dd7410b3dfdp1a9229jsn93f17eae361b`
4. Deploy → copy the URL (e.g. `https://stockx-lookup.vercel.app`)

---

### Step 3 — Update Frontend

Open `frontend/index.html` and find this line:

```js
: 'https://YOUR-BACKEND.vercel.app'; // ← update after deploying
```

Replace it with your actual Vercel backend URL.

---

### Step 4 — Deploy Frontend on Vercel (or GitHub Pages)

**Option A — GitHub Pages (easiest):**
1. Move `frontend/index.html` to repo root as `index.html`
2. Go to GitHub repo → Settings → Pages → Deploy from branch `main`

**Option B — Vercel second project:**
1. Create another Vercel project pointing to the `frontend/` folder

---

## 💡 Usage

1. Open the frontend URL
2. Paste SKUs one per line (e.g. `DV1031-030`)
3. Click **LOOK UP** or press `Ctrl+Enter`
4. View results table with Name, SKU, Release Date, Retail Price, Last Sale

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `RAPIDAPI_KEY` | Your RapidAPI key for StockX API |
