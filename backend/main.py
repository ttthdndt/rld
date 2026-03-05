from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import http.client
import json
import os

app = FastAPI(title="StockX SKU Lookup")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "c71d279a4emshe0f0dd7410b3dfdp1a9229jsn93f17eae361b")
RAPIDAPI_HOST = "stockx1.p.rapidapi.com"


class SKURequest(BaseModel):
    skus: list[str]


def fetch_product(sku: str) -> dict:
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    conn.request("GET", f"/v2/stockx/product?query={sku}", headers=headers)
    res = conn.getresponse()
    raw = res.read().decode("utf-8")
    conn.close()
    return json.loads(raw)


@app.post("/lookup")
async def lookup_skus(request: SKURequest):
    results = []
    for sku in request.skus:
        sku = sku.strip()
        if not sku:
            continue
        try:
            data = fetch_product(sku)
            traits = {t["name"]: t["value"] for t in data.get("traits", [])}
            results.append({
                "sku": data.get("sku", sku),
                "name": data.get("name", "N/A"),
                "release_date": traits.get("Release Date", "N/A"),
                "retail_price": traits.get("Retail Price", "N/A"),
                "colorway": traits.get("Colorway", "N/A"),
                "brand": data.get("brand", "N/A"),
                "image": data.get("thumb_image", ""),
                "lowest_ask": data.get("market", {}).get("bids", {}).get("lowest_ask"),
                "last_sale": data.get("market", {}).get("sales", {}).get("last_sale"),
                "status": "success",
            })
        except Exception as e:
            results.append({
                "sku": sku,
                "name": "Error",
                "release_date": "N/A",
                "retail_price": "N/A",
                "colorway": "N/A",
                "brand": "N/A",
                "image": "",
                "lowest_ask": None,
                "last_sale": None,
                "status": "error",
                "error": str(e),
            })
    return {"results": results}


@app.get("/health")
async def health():
    return {"status": "ok"}
