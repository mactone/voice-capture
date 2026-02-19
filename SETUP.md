# Voice Capture → Discord

One-tap voice recording on iPhone → AI polishes your speech → sends to Discord channel.

Capture fleeting ideas instantly before they disappear.

## Architecture

```
iPhone Shortcut (Dictate) → POST /capture → AI Polish → Discord Webhook
```

## Setup

### 1. Discord Webhook

1. Open Discord → go to your target channel
2. Click the gear icon (Edit Channel) → **Integrations** → **Webhooks**
3. Click **New Webhook** → name it (e.g. "Idea Capture")
4. Click **Copy Webhook URL** → save it

### 2. Get an AI API Key

Any OpenAI-compatible API works. Supported providers:

| Provider | Env Prefix | Notes |
|----------|-----------|-------|
| DeepSeek | `DEEPSEEK_` | Default base URL: `https://api.deepseek.com/v1` |
| OpenRouter | `OPENAI_` | Base URL: `https://openrouter.ai/api/v1`, access many models |
| OpenAI | `OPENAI_` | Base URL: `https://api.openai.com/v1` |
| z.ai | `ZAI_` | Base URL: `https://api.z.ai/v1` |
| MiniMax | `MINIMAX_` | Base URL: `https://api.minimax.io/v1` |
| Custom | `CUSTOM_` | Any OpenAI-compatible endpoint |

### 3. Deploy to Fly.io

```bash
# Install Fly CLI (if not already)
brew install flyctl
# or: curl -L https://fly.io/install.sh | sh

# Login / sign up
fly auth login

# Clone and enter the project
git clone https://github.com/YOUR_USERNAME/voice-capture.git
cd voice-capture/server

# Launch the app
fly launch

# Set your secrets (example with OpenRouter)
fly secrets set \
  DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN" \
  AI_PROVIDER="openai" \
  OPENAI_API_KEY="your-api-key" \
  OPENAI_BASE_URL="https://openrouter.ai/api/v1" \
  OPENAI_MODEL="openai/gpt-4o-mini"

# Deploy
fly deploy
```

Your server will be live at `https://YOUR_APP_NAME.fly.dev`.

### 4. Run Locally (Alternative)

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your keys

# Run
uvicorn main:app --port 8080
```

Test:
```bash
curl -X POST http://localhost:8080/capture \
  -H "Content-Type: application/json" \
  -d '{"text": "so um I was thinking we should try a different approach to this problem"}'
```

### 5. iOS Shortcut Setup

1. Open **Shortcuts** app → tap **+**

2. **Action 1** — Search and add「**Dictate Text**」(聽寫文字)
   - Set "Stop Listening" to "After Pause"（暫停後）

3. **Action 2** — Search and add「**Get Contents of URL**」(取得 URL 的內容)
   - The URL field will auto-fill with "Dictated Text" — **tap the blue tag and delete it**
   - Type your server URL: `https://YOUR_APP_NAME.fly.dev/capture`
   - Tap "**Show More**"（顯示更多）
   - Method: **POST**
   - Request Body: **JSON**
   - Tap "**Add New Field**"（加入新欄位）→ select "**Text**"（文字）
   - Left side (Key): type `text`
   - Right side (Value): tap and select the blue「**Dictated Text**」(聽寫的文字) variable

4. Name the shortcut → tap **ⓘ** → **Add to Home Screen**

Now you have a one-tap idea capture button on your iPhone!

## Switching AI Providers

Change `AI_PROVIDER` in your Fly secrets:

```bash
# Switch to DeepSeek
fly secrets set AI_PROVIDER="deepseek" DEEPSEEK_API_KEY="your-key"

# Switch to MiniMax
fly secrets set AI_PROVIDER="minimax" MINIMAX_API_KEY="your-key"
```

Or override per-request:
```json
{"text": "your voice text", "provider": "deepseek"}
```

## API

### POST /capture

Request:
```json
{
  "text": "raw voice transcript",
  "provider": "openai"  // optional, overrides default
}
```

Response:
```json
{
  "original": "raw voice transcript",
  "polished": "Polished voice transcript.",
  "provider_used": "openai",
  "elapsed_ms": 2253
}
```

### GET /health

Returns `{"status": "ok"}` — used for health checks.

## License

MIT
