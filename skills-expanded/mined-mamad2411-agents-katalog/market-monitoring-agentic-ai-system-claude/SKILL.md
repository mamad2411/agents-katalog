# CLAUDE.md — monitoring_agents

## Project overview

**Agentic AI Local Market Monitor** — a multi-agent smart city system that monitors Karachi bazaar health in real time. Six specialized LangGraph agents run sequentially, each reading shared state and writing findings back. A final synthesis node produces an executive report.

Stack: LangGraph · Groq API (Llama 3.3 / Llama 4) · Qdrant (in-memory vector DB) · Redis (with graceful in-memory fallback) · Streamlit · FastAPI · sentence-transformers

---

## How to run

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install deps (first time)
pip install -r requirements.txt

# Dashboard (primary UI)
streamlit run dashboard.py

# CLI pipeline run
python orchestrator.py

# Preview mock data
python data/mock_iot_data.py
```

Requires `GROQ_API_KEY` in `.env` (free key at https://console.groq.com). Set `LLM_MODEL_ID` to switch models. No local model download needed — all inference runs on Groq's cloud.

Redis and Qdrant are **optional** — both fall back gracefully to in-memory alternatives with no code changes required.

---

## Architecture

```
orchestrator_node  (loads feeds, seeds RAG knowledge base)
     ↓
inventory_agent  →  customer_agent  →  security_agent
                                            ↓
                           CRITICAL alerts? → emergency_synthesis → END
                                            ↓ (no CRITICAL)
                         supply_agent → pricing_agent → demand_agent
                                            ↓
                                      synthesis_node → END
```

### Key files

| File | Role |
|---|---|
| `orchestrator.py` | LangGraph graph definition, conditional routing, synthesis nodes |
| `state.py` | `MarketState` TypedDict — the single shared state schema |
| `llm_config.py` | LLM singleton (`ChatGroq` via `langchain-groq`); `get_llm()` returns a `str → str` callable |
| `data/mock_iot_data.py` | All mock sensor/POS/camera/audio/weather data |
| `tools/alert_tool.py` | `emit_alert()` — creates + persists alerts to Redis; `format_state_alerts()` / `format_history_context()` for prompt injection |
| `tools/rag_tool.py` | Qdrant in-memory RAG; `seed_market_knowledge()` + `retrieve_context()` |
| `tools/chart_tool.py` | matplotlib chart generators — each returns a `.png` path under `./charts/` |
| `memory/redis_store.py` | Redis key-value store with in-memory fallback |
| `memory/vector_store.py` | (stub) secondary vector store |
| `dashboard.py` | Streamlit UI |
| `agents/*.py` | One file per agent |

### Agent pattern (all 6 follow this)

Every agent:
1. Reads its relevant slices of `state` (raw feed data)
2. Runs **rule-based logic** to compute counts, flags, structured outputs — this is the source of truth
3. Generates charts via `tools/chart_tool.py`
4. Injects context into the LLM prompt:
   - `format_state_alerts(state["alerts"], exclude_agent=self)` — upstream agent alerts from this run
   - `format_history_context()` — prior-run alerts from Redis
   - `retrieve_context(query)` — RAG snippets (security and demand agents only)
5. Calls `llm(prompt)` for **natural language narration only** — LLM never sets counts or flags
6. Creates alerts via `emit_alert()` — persists to Redis, returns dict for `state["alerts"]`
7. Returns updated state

---

## Core invariants — never break these

**Hallucination prevention**: Rule-based Python code is always the source of truth. The LLM never sets alert counts, severity levels, or structured fields. It only narrates pre-computed facts.

**Alert accumulation**: `state["alerts"]` uses `Annotated[list, operator.add]` — agents append, never overwrite. Always return `"alerts": alerts` (the new slice only). Synthesis and utility nodes that generate no alerts must return only their changed fields (e.g. `{"final_report": ...}`), never `{**state, ...}` — spreading state re-injects the accumulated alerts list and the reducer doubles them.

**LLM singleton**: `get_llm()` returns a cached callable. `ChatGroq` is instantiated once via `lru_cache`. Never instantiate `ChatGroq` directly in agents — always call `get_llm()`.

**LLM response cache**: `llm_config.py` calls `set_llm_cache()` at import time. Responses are keyed by prompt hash + model params. Redis available → `RedisCache`. Redis down → `SQLiteCache` (`.llm_cache.db`). Set `LLM_CACHE=false` in `.env` to disable. Cache hits return in <5ms. Benefit is most visible in the Streamlit dashboard (persistent process) — subsequent pipeline runs after the first are near-instant. Clear the cache: `del .llm_cache.db` or `redis-cli FLUSHDB`.

**Graceful degradation**: Redis down → in-memory fallback. Qdrant down → keyword search fallback. sentence-transformers unavailable → keyword fallback. No agent should crash if external services are absent.

---

## Adding a new agent

1. Create `agents/my_agent.py` following the pattern above
2. Add the output key to `MarketState` in `state.py`
3. Register in `orchestrator.py`: `graph.add_node("my_agent", my_agent)` and wire edges
4. Add a tab in `dashboard.py` under "Agent Outputs"

## Adding new RAG knowledge

```python
from tools.rag_tool import index_text
index_text("your market pattern text", {"type": "pattern_type", "source": "manual"})
```

Or add to the `MARKET_KNOWLEDGE` list in `tools/rag_tool.py` for permanent baseline knowledge.

---

## Environment variables (`.env`)

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | *(required)* | Groq API key — get free at https://console.groq.com |
| `LLM_MODEL_ID` | `llama-3.3-70b-versatile` | Groq model ID (see model guide below) |
| `LLM_MAX_NEW_TOKENS` | `512` | Max tokens per LLM call |
| `LLM_CACHE` | `true` | Set to `false` to disable response caching |
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `QDRANT_HOST` | `localhost` | Qdrant server host (falls back to in-memory) |
| `QDRANT_PORT` | `6333` | Qdrant server port |

---

## Data sources (all mock)

`data/mock_iot_data.py` — `random.seed(42)`, reproducible. Five shops (`SHOP_001`–`SHOP_005`), eight SKUs (staples: rice, oil, flour, sugar, milk, eggs, bread, tomatoes). Deliberately includes low-stock items, anomalous POS transactions, camera events including a CRITICAL altercation, cartel pricing signals, and supply disruptions to ensure agents always have something to flag.

Do not randomize `BASE_TIME` or remove `random.seed(42)` — tests and demos depend on deterministic output.

---

## Model guide (Groq)

All inference runs on Groq's cloud. No local GPU or RAM required.
Llama 3.2 preview models are **decommissioned** — do not use them.

| Model ID | Quality | Speed | Use case |
|---|---|---|---|
| `llama-3.3-70b-versatile` | Best | ~300ms/call | Default — production quality |
| `llama-3.1-8b-instant` | Good | ~150ms/call | Fast dev / high-volume runs |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Best + next-gen | ~250ms/call | Llama 4, balanced |

Pipeline makes 4–8 LLM calls total depending on routing: emergency path runs 4 calls (inventory + customer + security + emergency_synthesis), normal path runs 8 (all 6 agents + synthesis). End-to-end: ~1–3s on emergency path, ~3–5s on normal path.
