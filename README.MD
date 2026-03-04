# StockX Release Date API

A FastAPI service that extracts the **release date** from a StockX product page.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/release-date?sku=SLUG` | Single SKU lookup |
| GET | `/release-date/batch?skus=SLUG1,SLUG2` | Batch lookup (max 20) |

### Example requests

```
GET /release-date?sku=nike-air-max-1-anniversary-red
GET /release-date/batch?skus=nike-air-max-1-anniversary-red,adidas-yeezy-boost-350-v2-zebra
```

### Example response

```json
{
  "sku": "nike-air-max-1-anniversary-red",
  "url": "https://stockx.com/nike-air-max-1-anniversary-red",
  "release_date": "04/21/2017"
}
```

---

## Local development

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
# → http://localhost:8000
```

---

## Deploy to Vercel (via GitHub)

1. **Push this repo to GitHub**

2. **Go to [vercel.com](https://vercel.com)** → New Project → Import your GitHub repo

3. Vercel auto-detects Python. No build settings needed — `vercel.json` handles routing.

4. Click **Deploy** ✓

### Notes
- StockX heavily uses JavaScript rendering. If release dates are missing,
  you may need to add a headless browser layer (e.g. Playwright via a separate
  service) since Vercel serverless functions cannot run Chromium easily.
- The scraper uses 3 fallback strategies: DOM parsing, JSON-LD, and meta tags.
