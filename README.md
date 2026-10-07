# Multi-Persona Financial Assistant

A Gradio web application where three different AI financial advisors answer your questions simultaneously — each with a completely different personality, expertise level, and communication style. Same model. Same question. Three expert perspectives.

> Built to make **prompt engineering visible and tangible**. The entire difference between the three advisors is 100 lines of system prompt text.

---

## What It Does

Generic financial chatbots give identical advice to everyone. This app doesn't.

When you ask *"Should I invest in mutual funds?"*, the answer depends entirely on who you are:

| Who You Are | What You Need |
|---|---|
| 22-year-old with ₹5,000 savings | "Start a ₹500/month SIP in an index fund today." |
| 40-year-old with ₹50L invested | "Consider portfolio rebalancing and tax harvesting." |
| Someone with dependents and no insurance | "Get term insurance first. Then talk investments." |

Pick the tab that matches your situation and get the right answer for you.

---

## The Three Personas

### Beginner Investor
**Target:** Ages 22–28, earning ₹25,000–50,000/month, zero investment experience  
**Style:** Patient, encouraging, jargon-free. Every term defined. Ends every response with one concrete next step.  
**Example question:** *"How do I start investing with ₹1,000/month?"*

### Experienced Trader
**Target:** ₹10L+ invested, reads financial news daily, understands valuations  
**Style:** Peer-to-peer. Opinionated. Technical. References P/E ratios, FII/DII flows, macro context. No hand-holding.  
**Example question:** *"What's your view on IT sector valuations right now?"*

### Insurance Advisor
**Target:** Anyone with dependents or liabilities wanting protection-first thinking  
**Style:** Diagnoses before prescribing. Asks about dependents first. Brutally honest about bad products (ULIPs, endowments).  
**Example question:** *"My agent is recommending an endowment plan — should I buy it?"*

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web UI | Gradio 6 |
| LLM API | OpenAI SDK (`gpt-4o-mini` by default) |
| Package Manager | uv |
| Config | python-dotenv |

---

## Project Structure

```
Multi Persona Financial Assistant/
├── app.py                          # Entry point — launches Gradio
├── config.py                       # Model, temperature, pricing constants
├── .env                            # Your secrets (not committed)
├── .env.example                    # Template to copy from
│
├── src/
│   ├── personas/
│   │   ├── base.py                 # build_messages() and stream_response() functions
│   │   ├── beginner.py             # Beginner system prompt
│   │   ├── trader.py               # Trader system prompt
│   │   ├── insurance.py            # Insurance system prompt
│   │   └── __init__.py             # PERSONAS dict — maps name → prompt
│   │
│   ├── llm/
│   │   ├── client.py               # Lazy OpenAI client singleton
│   │   └── streamer.py             # Streaming + token cost calculation
│   │
│   ├── storage/
│   │   └── conversation_logger.py  # Saves every exchange to JSON
│   │
│   └── ui/
│       └── interface.py            # Gradio Blocks layout — 3 tabs
│
└── data/
    └── conversation_log.json       # Auto-created on first chat
```

---

## Setup

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/getting-started/installation/)

```powershell
# 1. Install dependencies
uv sync

# 2. Create your .env file
Copy-Item .env.example .env

# 3. Add your OpenAI API key to .env
notepad .env
```

Your `.env` should look like:
```
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.7
```

---

## Running the App

```powershell
uv run python app.py
```

Open your browser at **http://127.0.0.1:7860**

The app includes a **Toggle Dark Mode** button in the header.

---

## How It Works

### The Core Insight

All three personas use the **exact same model** (`gpt-4o-mini`), the **same temperature**, and the **same API call structure**. The only difference is the system prompt prepended to every conversation.

```python
# Every chat call builds messages like this:
[
  {"role": "system", "content": PERSONAS["beginner"]},  # ← this is everything
  {"role": "user",   "content": "How do I start investing?"}
]
```

### Streaming

Responses stream word-by-word using OpenAI's `stream=True`. Every chunk yields a partial string to Gradio, which re-renders the UI in real time — exactly like ChatGPT.

### Conversation Logging

Every exchange is automatically saved to `data/conversation_log.json`:

```json
{
  "timestamp": "2026-05-22T10:30:00",
  "persona": "beginner",
  "user_message": "How do I start investing?",
  "ai_response": "Great question...",
  "input_tokens": 120,
  "output_tokens": 80,
  "total_tokens": 200
}
```

This JSON log is your first **data asset** — ready for RAG or analytics later.

---

## Adding a Fourth Persona

1. Create `src/personas/tax.py` with a `SYSTEM_PROMPT` string
2. Add one line to `src/personas/__init__.py`:
   ```python
   PERSONAS["tax"] = tax.SYSTEM_PROMPT
   ```
3. Add a new tab in `src/ui/interface.py`

Takes ~15 minutes.

---

## Changing the Model

Edit `.env`:
```
MODEL_NAME=gpt-4o        # More capable, ~10x more expensive
MODEL_NAME=gpt-4o-mini   # Default — fast and cheap
```

---

## What This Project Teaches

- **Prompt engineering is the product** — same model, completely different behavior
- **Streaming is non-negotiable for UX** — 8-second wait vs words appearing live
- **Token costs compound** — watch the log grow as conversation history is re-sent each turn
- **Modular architecture** — adding a persona takes 15 minutes, not a refactor
