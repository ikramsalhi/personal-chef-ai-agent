# Personal Chef AI Agent 🍳

A LangChain agent built during the Thirduni AI Agents programme.

It demonstrates a simple tool-using agent with:

- Gemini 3.1 Flash-Lite
- Tavily web search
- a custom serving-size tool
- LangGraph conversation memory
- tool calling

## Architecture

User → Agent → Tool (when needed) → Tool result → Agent response

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your keys.

```bash
python src/agent.py
```

## Example

Ask:

```text
I have chicken, rice, tomatoes and yogurt. Give me a dinner idea for 3 people.
```

Then continue in the same conversation:

```text
Make it for 5 people instead.
```

The checkpointer keeps the thread memory while the program is running.

## Security

Never commit `.env` or real API keys.
