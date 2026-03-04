from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup
import re

app = FastAPI(title="StockX Release Date API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def extract_release_date(html: str) -> str | None:
    """
    Try multiple strategies to extract the release date from StockX product HTML.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Strategy 1: Look for a label "Release Date" and grab sibling/child <p>
    for label in soup.find_all(string=re.compile(r"Release Date", re.I)):
        parent = label.find_parent()
        if parent:
            p = parent.find("p")
            if p:
                return p.get_text(strip=True)
            # Try next sibling text
            sibling = label.find_next_sibling()
            if sibling:
                return sibling.get_text(strip=True)

    # Strategy 2: JSON-LD structured data
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string or "")
            if isinstance(data, dict):
                for key in ("releaseDate", "release_date", "datePublished"):
                    if key in data:
                        return data[key]
        except Exception:
            pass

    # Strategy 3: meta tag
    meta = soup.find("meta", {"name": re.compile(r"release", re.I)})
    if meta and meta.get("content"):
        return meta["content"]

    return None


@app.get("/")
def root():
    return {"message": "StockX Release Date API. Use /release-date?sku=YOUR_SKU"}


@app.get("/release-date")
async def get_release_date(sku: str):
    """
    Fetch the release date for a StockX product by SKU or slug.
    Example: /release-date?sku=nike-air-max-1-anniversary-red
    """
    # Support both slugs and search — try direct URL first
    url = f"https://stockx.com/{sku}" if not sku.startswith("http") else sku

    async with httpx.AsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        timeout=20.0,
    ) as client:
        try:
            response = await client.get(url)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Request failed: {e}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"StockX returned HTTP {response.status_code}",
        )

    release_date = extract_release_date(response.text)

    if not release_date:
        raise HTTPException(
            status_code=404,
            detail="Release date not found on page. StockX may require JS rendering.",
        )

    return {
        "sku": sku,
        "url": str(response.url),
        "release_date": release_date,
    }


@app.get("/release-date/batch")
async def get_release_dates_batch(skus: str):
    """
    Fetch release dates for multiple SKUs.
    Example: /release-date/batch?skus=slug-one,slug-two,slug-three
    """
    sku_list = [s.strip() for s in skus.split(",") if s.strip()]
    if not sku_list:
        raise HTTPException(status_code=400, detail="Provide at least one SKU.")
    if len(sku_list) > 20:
        raise HTTPException(status_code=400, detail="Max 20 SKUs per batch request.")

    results = []
    async with httpx.AsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        timeout=20.0,
    ) as client:
        for sku in sku_list:
            url = f"https://stockx.com/{sku}"
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    date = extract_release_date(response.text)
                    results.append({
                        "sku": sku,
                        "release_date": date,
                        "error": None if date else "Release date not found",
                    })
                else:
                    results.append({
                        "sku": sku,
                        "release_date": None,
                        "error": f"HTTP {response.status_code}",
                    })
            except Exception as e:
                results.append({"sku": sku, "release_date": None, "error": str(e)})

    return {"results": results}
