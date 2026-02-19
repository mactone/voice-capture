import os
from abc import ABC, abstractmethod
import httpx

SYSTEM_PROMPT = (
    "You are a text polisher. The user will give you a raw voice transcript. "
    "Clean it up into clear, well-structured text while preserving the original "
    "meaning and ideas. Fix grammar, remove filler words, and organize the thoughts. "
    "Output ONLY the polished text, nothing else."
)


class AIProvider(ABC):
    @abstractmethod
    async def polish(self, raw_text: str) -> str: ...


class OpenAICompatibleProvider(AIProvider):
    """Works with any OpenAI-compatible API (DeepSeek, MiniMax, z.ai, etc.)."""

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def polish(self, raw_text: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text},
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()


# --- Provider registry ---

PROVIDERS: dict[str, callable] = {}


def register(name: str):
    def decorator(factory):
        PROVIDERS[name] = factory
        return factory
    return decorator


@register("deepseek")
def _deepseek():
    return OpenAICompatibleProvider(
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    )


@register("zai")
def _zai():
    return OpenAICompatibleProvider(
        base_url=os.getenv("ZAI_BASE_URL", "https://api.z.ai/v1"),
        api_key=os.getenv("ZAI_API_KEY", ""),
        model=os.getenv("ZAI_MODEL", "z1-mini"),
    )


@register("minimax")
def _minimax():
    return OpenAICompatibleProvider(
        base_url=os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
        api_key=os.getenv("MINIMAX_API_KEY", ""),
        model=os.getenv("MINIMAX_MODEL", "MiniMax-Text-01"),
    )


@register("openai")
def _openai():
    return OpenAICompatibleProvider(
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )


@register("custom")
def _custom():
    return OpenAICompatibleProvider(
        base_url=os.getenv("CUSTOM_BASE_URL", ""),
        api_key=os.getenv("CUSTOM_API_KEY", ""),
        model=os.getenv("CUSTOM_MODEL", ""),
    )


def get_provider(name: str) -> AIProvider:
    factory = PROVIDERS.get(name)
    if not factory:
        available = ", ".join(PROVIDERS.keys())
        raise ValueError(f"Unknown provider '{name}'. Available: {available}")
    return factory()
