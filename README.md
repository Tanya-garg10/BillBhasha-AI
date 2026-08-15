# BillBhasha AI — Voice Assistant for Local Commerce

A voice-first AI assistant that helps users understand bills, GST, invoices, charges, payments, returns, and refunds in simple Hindi/Hinglish. Built as part of the **10 Days of AI Voice Agents — #VoiceForBharat** challenge.

**Features:**
- 🎙️ Natural Hindi/Hinglish voice conversations
- 📊 GST and billing explanations in simple language
- 🧑‍💼 Specialist handoff for return/refund issues
- 💾 Caller memory and personalization
- 📈 Call analytics dashboard
- 🎨 Premium modern UI/UX
- 🆘 Human escalation with support tickets

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Murf Falcon](https://img.shields.io/badge/TTS-Murf%20Falcon-6366F1)](https://murf.ai/api/docs/text-to-speech/streaming) [![LiveKit](https://img.shields.io/badge/Transport-LiveKit-002cf2)](https://docs.livekit.io) [![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/) [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

## Why Murf Falcon

- **55ms model latency** - fastest production TTS
- **130ms time-to-first-audio** across 10+ global regions
- **$0.01/1000 characters** - up to 10x cheaper than alternatives
- **150+ voices** across 35+ languages
- **99.38% pronunciation accuracy**

## Project Overview

BillBhasha AI is a 10-day project building a production-ready voice assistant for Indian local commerce. Each day added new capabilities:

- **Day 1**: Voice AI pipeline setup with Murf Falcon TTS
- **Day 2**: System prompts for billing/GST assistance
- **Day 3**: Frontend UI/UX redesign
- **Day 4**: Caller memory and personalization
- **Day 5**: Tools and catalogue integration
- **Day 6**: Outbound calling capability
- **Day 7**: Human escalation with support tickets
- **Day 8**: Call analytics dashboard
- **Day 9**: Specialist handoff for returns/refunds
- **Day 10**: Final polish and deployment

## Architecture

```mermaid
flowchart LR
    A[🎙️ User speaks] -->|audio| B[Deepgram STT]
    B -->|text| C[LLM]
    C -->|response text| D[Murf Falcon TTS]
    D -->|audio| E[LiveKit]
    E -->|stream| F[🔊 User hears]

    style A fill:#444441,stroke:#888780,color:#fff
    style B fill:#185FA5,stroke:#85B7EB,color:#fff
    style C fill:#534AB7,stroke:#AFA9EC,color:#fff
    style D fill:#0F6E56,stroke:#5DCAA5,color:#fff
    style E fill:#D85A30,stroke:#F0997B,color:#fff
    style F fill:#444441,stroke:#888780,color:#fff
```

## Quickstart

### Prerequisites

- **Python** 3.10+
- **[uv](https://docs.astral.sh/uv/)** - fast Python package manager
  ```bash
  # macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Node.js** 18+
- **pnpm** — fast Node package manager
  ```bash
  npm install -g pnpm
  ```
- A [LiveKit](https://cloud.livekit.io/) project (free tier available)

### Step 1: Clone the repo

```bash
git clone https://github.com/Tanya-garg10/BillBhasha-AI.git
cd BillBhasha-AI
```

### Step 2: Set up environment variables

Create `.env.local` in both `backend/` and `frontend/` (copy from `.env.example` in each). You need:

| Variable                               | Where to get it                                        | Required |
| -------------------------------------- | ------------------------------------------------------ | -------- |
| `LIVEKIT_URL`                          | LiveKit Cloud dashboard                                | Yes      |
| `LIVEKIT_API_KEY`                      | LiveKit Cloud dashboard                                | Yes      |
| `LIVEKIT_API_SECRET`                   | LiveKit Cloud dashboard                                | Yes      |
| `MURF_API_KEY`                         | [murf.ai/api/dashboard](https://murf.ai/api/dashboard) | Yes      |
| `DEEPGRAM_API_KEY`                     | [deepgram.com](https://deepgram.com)                   | Yes      |
| `GOOGLE_API_KEY` (or `OPENAI_API_KEY`) | Depends on LLM choice                                  | Yes      |

### Step 3: Install backend dependencies

```bash
cd backend
uv sync
uv run python src/agent.py download-files
```

### Step 4: Install frontend dependencies

```bash
cd frontend
pnpm install
```

### Step 5: Run it

**Option A - All-in-one (from repo root):**

```bash
# macOS/Linux
chmod +x start_app.sh
./start_app.sh

# Windows (PowerShell)
.\start_app.ps1
```

**Option B - Separate terminals:**

```bash
# Terminal 1 — LiveKit Server
livekit-server --dev

# Terminal 2 — Backend agent
cd backend && uv run python src/agent.py dev

# Terminal 3 — Frontend
cd frontend && pnpm dev
```

Then open **http://localhost:3000** in your browser.

You should now see the voice agent UI. Click **Start talking**, allow microphone access, and speak — the agent will respond with Murf Falcon TTS. Ensure your backend and (if using Option B) LiveKit server are running.

## Deploy

Want to deploy this beyond localhost? You'll need to deploy **two services**: the backend agent and the frontend. Both must use the same LiveKit project.

> This is a two-service app — the backend agent and the frontend UI deploy separately. You'll need both running and connected to the same LiveKit project.

### Backend (Python agent) — Deploy to Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template?template=https%3A%2F%2Fgithub.com%2FTanya-garg10%2FBillBhasha-AI)

Set these environment variables in Railway:

- `MURF_API_KEY`
- `DEEPGRAM_API_KEY`
- `GOOGLE_API_KEY` or `OPENAI_API_KEY`
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

The backend runs as a long-lived Python process that connects to LiveKit as an agent. Railway handles this well.

### Frontend (Next.js) — Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Tanya-garg10/BillBhasha-AI&root-directory=frontend&env=LIVEKIT_URL,LIVEKIT_API_KEY,LIVEKIT_API_SECRET&project-name=billbhasha-ai&repository-name=billbhasha-ai)

Set these environment variables in Vercel:

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `AGENT_NAME` (optional — for explicit agent dispatch)

The frontend is a standard Next.js app. Point it at the same LiveKit instance your backend agent is connected to.

### Connecting them

The frontend and backend don't call each other directly — they both connect to **LiveKit**, which handles the real-time audio transport.

1. Use the **same** `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` on both Railway and Vercel
2. Set `AGENT_NAME=my-agent` on Vercel — this matches the `agent_name="my-agent"` registered in `backend/src/agent.py`
3. Verify: Railway logs should show the agent connected to LiveKit. Open your Vercel URL, click **Start talking** — the agent should respond

If the agent doesn't connect, double-check that both services point to the same LiveKit project and that the backend is running (check Railway logs).

## BillBhasha AI Use Case

BillBhasha AI is specifically designed for local commerce and billing assistance in India. The default system prompt makes it a **billing and GST assistant** that helps users understand:

- GST calculations and rates
- Invoice breakdowns
- Payment processing fees
- Return and refund processes
- Product catalogue and pricing
- Order tracking and delivery

**Where the prompt lives:** `backend/src/agent.py`- the `SYSTEM_PROMPT` constant (near the top of the file, after the imports). Change that string to change what your voice agent does.

### Specialized Features

BillBhasha AI includes specialized features for local commerce:

- **Specialist Handoff**: Automatically routes return/refund issues to a dedicated Returns & Refunds Specialist
- **Caller Memory**: Remembers user preferences and past conversations
- **Support Tickets**: Creates structured support tickets for complex issues
- **Call Analytics**: Tracks call outcomes and provides dashboard insights
- **Hindi/Hinglish Support**: Natural conversations in mixed Hindi-English

### Customizing for Your Use Case

To adapt BillBhasha AI for your specific local commerce use case, modify the `SYSTEM_PROMPT` to include:

- Your specific business context
- Product/service information
- Policies and procedures
- Language preferences
- Specialist agent needs

See the Configuration section below for voice, STT, and LLM options.

## Configuration

### Murf voice

Edit the `tts=murf.TTS(...)` call in `backend/src/agent.py`. Set the `voice` argument to any Murf voice ID. Examples:

- `Anisha` — Indian English (female, default in this starter)
- `Pooja` — Indian English (female)
- `Samar` — Indian English (male)
- `Amara` — US English (female)
- `Gordon` — US English (male)
- `Hazel` — UK English (female)
- `Bertie` — UK English (male)

Browse all voices: [Murf Voice Library](https://murf.ai/api/docs/voices-styles/voice-library).

### STT provider

STT is configured in `backend/src/agent.py` in the `AgentSession(stt=...)` call. The default is Deepgram (`deepgram.STT(model="nova-3")`). You can swap to another LiveKit-compatible STT plugin if needed.

### LLM (Gemini vs OpenAI)

- **Gemini (default):** Set `GOOGLE_API_KEY` and use `llm=google.LLM(model="gemini-3.5-flash-lite")` in `agent.py`.
- **OpenAI:** Set `OPENAI_API_KEY`, add the OpenAI plugin, and use the corresponding `llm=openai.LLM(...)` in `agent.py`.

### Audio format

Murf Falcon and LiveKit handle audio format internally. For advanced options, see [Murf API docs](https://murf.ai/api/docs) and [LiveKit docs](https://docs.livekit.io).

## Project Structure

```
BillBhasha-AI/
├── backend/                 # Python voice agent (LiveKit Agents + Murf Falcon)
│   ├── src/
│   │   ├── agent.py         # Agent entrypoint, pipeline (STT/LLM/TTS), system prompt
│   │   ├── memory.py        # Caller memory and analytics database
│   │   ├── catalogue.py     # Product catalogue and pricing
│   │   ├── support_tickets.py # Support ticket management
│   │   ├── refund_specialist.py # Returns & Refunds specialist tools
│   │   └── analytics_api.py # Analytics API server
│   ├── tests/               # Agent tests
│   ├── .env.example         # Backend env template
│   ├── pyproject.toml       # Python deps (uv)
│   └── railway.toml         # Railway deploy config
├── frontend/                # Next.js UI for voice sessions
│   ├── app/
│   │   ├── page.tsx         # Main page
│   │   ├── dashboard/       # Analytics dashboard
│   │   └── api/token/       # LiveKit token endpoint (dev)
│   ├── components/
│   │   ├── app/             # Custom BillBhasha components
│   │   │   ├── welcome-view.tsx  # Premium hero section
│   │   │   ├── voice-orb.tsx     # Animated voice orb
│   │   │   ├── dashboard.tsx     # Analytics dashboard
│   │   │   ├── navigation.tsx   # Desktop navigation
│   │   │   └── mobile-navigation.tsx # Mobile navigation
│   │   └── agents-ui/       # LiveKit Agents UI components
│   ├── app-config.ts        # Branding, title, button text, accent
│   ├── .env.example         # Frontend env template
│   └── package.json         # Node deps (pnpm)
├── start_app.sh             # Start LiveKit + backend + frontend (macOS/Linux)
├── start_app.ps1            # Start LiveKit + backend + frontend (Windows)
├── README.md                # This file
└── AGENTS.md                # Agent development guidelines
```

For deeper documentation on each part, see:

- [Backend Documentation](./backend/README.md) — agent pipeline, voice/LLM/STT configuration, testing, deployment
- [Frontend Documentation](./frontend/README.md) — UI customization, visualizers, theming, component architecture

## Links

- [Murf API Docs](https://murf.ai/api/docs)
- [Murf Voice Library](https://murf.ai/api/docs/voices-styles/voice-library)
- [LiveKit Docs](https://docs.livekit.io)
- [Deepgram Docs](https://developers.deepgram.com)
- [Murf Falcon Benchmarks](https://murf.ai/falcon/benchmarks)
- [TTS Latency Benchmarker](https://github.com/sahilsgupta/tts-latency-benchmarker) — run your own p50/p95 tests across providers
- [Murf Discord](https://discord.gg/FbKAy96Sz7)
- [Murf Startup Incubator](https://murf.ai/api) — 50M free characters for startups
- [10 Days of AI Voice Agents — #VoiceForBharat](https://twitter.com/search?q=%23VoiceForBharat) — Daily voice AI builds

## Acknowledgments

Built as part of the **10 Days of AI Voice Agents — #VoiceForBharat** challenge by Tanya Garg.

Powered by:
- **Murf Falcon** — The fastest production TTS
- **LiveKit Agents** — Real-time voice AI framework
- **Google Gemini** — Large Language Model
- **Deepgram** — Speech-to-Text

## License

MIT License — Copyright (c) 2026 Tanya Garg

## License

MIT
