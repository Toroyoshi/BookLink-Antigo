import os
import httpx

LOAN_SERVICE_URL = os.getenv("LOAN_SERVICE_URL", "http://localhost:8003")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "internal-dev-token")

async def mark_fine_paid(fine_id: int):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            f"{LOAN_SERVICE_URL}/internal/fines/{fine_id}/mark-paid",
            headers={"X-Internal-Token": INTERNAL_SERVICE_TOKEN},
        )
        return r
