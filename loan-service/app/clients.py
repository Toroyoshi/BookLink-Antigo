import os
import httpx
from fastapi import HTTPException

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8002")

async def claim_copy(copy_id: int):
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.post(f"{CATALOG_SERVICE_URL}/copies/{copy_id}/claim", params={"purpose":"LOAN"})
            return r
        
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Catalog Service is unavailable")
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error from Catalog Service")
        
async def release_copy(copy_id: int):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{CATALOG_SERVICE_URL}/copies/{copy_id}/release")
        return r
