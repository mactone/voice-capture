import os
import time
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from ai_providers import get_provider

load_dotenv()

app = FastAPI(title="Voice Capture → Discord")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


class CaptureRequest(BaseModel):
    text: str
    provider: Optional[str] = None  # override default provider per-request


class CaptureResponse(BaseModel):
    original: str
    polished: str
    provider_used: str
    elapsed_ms: int


@app.post("/capture", response_model=CaptureResponse)
async def capture(req: CaptureRequest):
    if not req.text.strip():
        raise HTTPException(400, "Empty text")
    if not DISCORD_WEBHOOK_URL:
        raise HTTPException(500, "DISCORD_WEBHOOK_URL not configured")

    start = time.time()

    provider_name = req.provider or os.getenv("AI_PROVIDER", "deepseek")
    provider = get_provider(provider_name)
    polished = await provider.polish(req.text)

    await send_to_discord(polished)

    elapsed = int((time.time() - start) * 1000)
    return CaptureResponse(
        original=req.text,
        polished=polished,
        provider_used=provider_name,
        elapsed_ms=elapsed,
    )


async def send_to_discord(text: str):
    payload = {"content": text}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(DISCORD_WEBHOOK_URL, json=payload)
        if resp.status_code not in (200, 204):
            raise HTTPException(502, f"Discord webhook failed: {resp.status_code}")


@app.get("/health")
async def health():
    return {"status": "ok"}
