import os
import httpx

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8002")

async def claim_copy(copy_id: int):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{CATALOG_SERVICE_URL}/copies/{copy_id}/claim", params={"purpose":"LOAN"})
        return r

async def release_copy(copy_id: int):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{CATALOG_SERVICE_URL}/copies/{copy_id}/release")
        return r
