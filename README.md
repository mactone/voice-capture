# Voice Capture → Discord

One-tap voice recording on iPhone → AI polishes your speech → sends to Discord channel.

Capture fleeting ideas instantly before they disappear.

## How It Works

```
iPhone Shortcut (Dictate) → POST /capture → AI Polish → Discord Webhook
```

1. Tap the shortcut on your iPhone home screen
2. Speak your idea
3. Speech is converted to text (Apple's built-in dictation)
4. Text is sent to your server, where AI cleans it up (fixes grammar, removes filler words, organizes thoughts)
5. Polished text is posted to your Discord channel

## Features

- **Instant capture** — one tap from home screen, speak, done
- **AI polishing** — raw voice transcripts become clean, readable text
- **Multi-provider** — supports DeepSeek, OpenRouter, OpenAI, MiniMax, z.ai, or any OpenAI-compatible API
- **Per-request override** — switch AI providers on the fly
- **Fast** — typically under 3 seconds end-to-end
- **Free to run** — Fly.io free tier + your own API key

## Quick Start

See [SETUP.md](SETUP.md) for full deployment and iOS Shortcut setup instructions.

```bash
git clone https://github.com/mactone/voice-capture.git
cd voice-capture/server
fly launch
fly secrets set DISCORD_WEBHOOK_URL="..." AI_PROVIDER="openai" OPENAI_API_KEY="..."
fly deploy
```

Then create an iOS Shortcut with two actions: **Dictate Text** → **Get Contents of URL** (POST to your server).

## Tech Stack

- **Backend**: Python, FastAPI, httpx
- **AI**: Any OpenAI-compatible API
- **Deployment**: Fly.io (Docker)
- **Client**: iOS Shortcuts

## License

MIT

---

# Voice Capture → Discord（語音捕捉）

iPhone 一鍵錄音 → AI 潤飾語音內容 → 發送到 Discord 頻道。

在靈感消失之前，即時捕捉你的想法。

## 運作原理

```
iPhone 捷徑（聽寫）→ POST /capture → AI 潤飾 → Discord Webhook
```

1. 點擊 iPhone 主畫面上的捷徑
2. 說出你的想法
3. 語音透過 Apple 內建聽寫功能轉為文字
4. 文字傳送至伺服器，AI 自動潤飾（修正文法、刪除贅字、整理思路）
5. 潤飾後的文字發送到你的 Discord 頻道

## 功能特色

- **即時捕捉** — 主畫面一鍵啟動，說完即送
- **AI 潤飾** — 語音逐字稿自動變成清晰、易讀的文字
- **多模型支援** — 支援 DeepSeek、OpenRouter、OpenAI、MiniMax、z.ai，或任何 OpenAI 相容 API
- **逐次切換** — 每次請求可指定不同的 AI 模型
- **快速** — 端到端通常不到 3 秒
- **免費運行** — Fly.io 免費方案 + 你自己的 API 金鑰

## 快速開始

完整部署及 iOS 捷徑設定請參考 [SETUP.md](SETUP.md)。

```bash
git clone https://github.com/mactone/voice-capture.git
cd voice-capture/server
fly launch
fly secrets set DISCORD_WEBHOOK_URL="..." AI_PROVIDER="openai" OPENAI_API_KEY="..."
fly deploy
```

然後在 iPhone 建立一個捷徑，包含兩個動作：**聽寫文字** → **取得 URL 的內容**（POST 到你的伺服器）。

## 技術架構

- **後端**：Python、FastAPI、httpx
- **AI**：任何 OpenAI 相容 API
- **部署**：Fly.io（Docker）
- **客戶端**：iOS 捷徑

## 授權條款

MIT
