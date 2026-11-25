---
name: tpl-ai-ml-langchain-python-agent
description: Template do pack (ai-ml/01-langchain-python-agent.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/01-langchain-python-agent.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: LangChain Python Agent (FastAPI + OpenAI/Anthropic + Chroma + LangSmith)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/01-langchain-python-agent.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Python 3.12
- **Framework:** LangChain 0.2+ (langchain, langchain-openai, langchain-anthropic)
- **LLM Providers:** OpenAI GPT-5.4 / Anthropic Claude Sonnet 4.6
- **Vector Store:** Chroma (local dev) / Pinecone (prod)
- **API Layer:** FastAPI + Pydantic v2
- **Tracing:** LangSmith (langsmith SDK)
- **Memory:** Redis (cross-session) / InMemoryChatMessageHistory (single session)

---

## PROJECT STRUCTURE
```
app/
├── main.py                    # FastAPI entry point
├── agents/
│   ├── __init__.py
│   ├── base.py                # Base agent factory
│   ├── research_agent.py      # ReAct agent with tools
│   └── rag_agent.py           # RAG chain
├── chains/
│   ├── summarize.py
│   └── extraction.py
├── tools/
│   ├── web_search.py          # Tavily / SerpAPI
│   ├── calculator.py
│   └── document_reader.py
├── memory/
│   └── redis_history.py
├── prompts/
│   └── templates.py           # Centralized prompt management
├── callbacks/
│   └── cost_tracker.py        # Token usage + cost tracking
└── config.py                  # Settings via pydantic-settings
```

---

## ARCHITECTURE RULES
1. **Agent vs Chain decision** — use Agent when the system needs to decide *which* tool to call; use Chain when the flow is deterministic.
2. **Always trace with LangSmith** — every chain/agent run must have a `run_name` and project tag; never debug blind.
3. **Prompt templates in hub or templates.py** — never inline f-string prompts in business logic.
4. **Cost tracking on every LLM call** — `CostCallbackHandler` always attached; log token usage per request.
5. **Retry with exponential backoff** — wrap all LLM calls with `tenacity`; handle rate limits gracefully.
6. **Async throughout** — `ainvoke`, `astream`; block the event loop = timeout under load.
7. **Structured output for data extraction** — use `with_structured_output(ZodSchema)` instead of parsing output manually.
8. **Memory scope** — session memory in Redis; user-level context in vector store, not in message history.

---

## AGENT VS CHAIN DECISION TABLE
```
Use AGENT when:
  ✅ Need to choose between multiple tools dynamically
  ✅ Number of reasoning steps is unknown
  ✅ Task requires multi-hop research
  ✅ Self-correction needed ("I was wrong, let me retry")

Use CHAIN when:
  ✅ Flow is deterministic (always: classify → extract → format)
  ✅ Speed and cost matter (every agent step = one LLM call)
  ✅ Easier to test and reproduce
  ✅ Output format must be guaranteed

Use RAG CHAIN specifically when:
  ✅ Answering questions from a known document corpus
  ✅ No external tool calls needed
```

---

## CONFIGURATION

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: SecretStr
    anthropic_api_key: SecretStr
    langsmith_api_key: SecretStr
    langsmith_project: str = "my-app"

    # LLM defaults
    default_model: str = "gpt-5.4"
    temperature: float = 0.0          # Deterministic by default
    max_tokens: int = 4096
    max_retries: int = 3

    # Vector store
    chroma_persist_dir: str = "./chroma_db"

    # Redis
    redis_url: str = "redis://localhost:6379"

settings = Settings()

# Enable LangSmith tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key.get_secret_value()
```

---

## COST TRACKING CALLBACK

```python
# app/callbacks/cost_tracker.py
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
import logging

# GPT-5.4 / Claude Sonnet 4.6 pricing (per 1K tokens, USD) — update when pricing changes
COST_TABLE = {
    "gpt-5.4":              {"input": 0.005,  "output": 0.015},
    "gpt-5.4-mini":         {"input": 0.00015,"output": 0.0006},
    "claude-sonnet-4-6":    {"input": 0.003,  "output": 0.015},
}

logger = logging.getLogger(__name__)

class CostCallbackHandler(BaseCallbackHandler):
    def __init__(self, feature: str):
        self.feature = feature
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0

    def on_llm_end(self, response: LLMResult, **kwargs):
        usage = response.llm_output.get("token_usage", {})
        model = response.llm_output.get("model_name", "gpt-5.4")

        input_tokens  = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        rates = COST_TABLE.get(model, COST_TABLE["gpt-5.4"])
        cost = (input_tokens / 1000 * rates["input"]) + \
               (output_tokens / 1000 * rates["output"])

        self.total_input_tokens  += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd      += cost

        logger.info({
            "event":          "llm_call_complete",
            "feature":        self.feature,
            "model":          model,
            "input_tokens":   input_tokens,
            "output_tokens":  output_tokens,
            "cost_usd":       round(cost, 6),
        })
```

---

## REACT AGENT WITH TOOLS

```python
# app/agents/research_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain import hub
from app.callbacks.cost_tracker import CostCallbackHandler
from app.config import settings

def build_research_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        model=settings.default_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        api_key=settings.openai_api_key,
    )

    tools = [
        TavilySearchResults(max_results=5, include_raw_content=False),
    ]

    prompt = hub.pull("hwchase17/react")   # Standard ReAct prompt from hub

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=6,          # Prevent infinite loops
        max_execution_time=30,     # 30s hard timeout
        early_stopping_method="generate",
        handle_parsing_errors=True,
        verbose=False,             # Use LangSmith tracing, not stdout verbosity
    )

# Usage in endpoint:
# agent = build_research_agent()
# cost_cb = CostCallbackHandler(feature="research")
# result = await agent.ainvoke(
#     {"input": user_query},
#     config={"callbacks": [cost_cb], "run_name": "ResearchAgent"},
# )
```

---

## MEMORY — REDIS CROSS-SESSION

```python
# app/memory/redis_history.py
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

def build_conversational_chain(session_id: str):
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    def get_history(session_id: str):
        return RedisChatMessageHistory(
            session_id=session_id,
            url="redis://localhost:6379",
            ttl=3600,   # 1 hour session expiry
        )

    return RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="input",
        history_messages_key="history",
    )
```

---

## RETRY + FALLBACK PATTERN

```python
# app/agents/base.py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import RunnableWithFallbacks

def build_llm_with_fallback():
    primary = ChatOpenAI(model="gpt-5.4", temperature=0)
    fallback = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

    # If primary raises RateLimitError, fall back to Anthropic
    return primary.with_fallbacks(
        [fallback],
        exceptions_to_handle=(Exception,),
    )

# Retry with tenacity for transient errors
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import openai

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError)),
    reraise=True,
)
async def call_with_retry(chain, inputs: dict):
    return await chain.ainvoke(inputs)
```

---

## FASTAPI ENDPOINT

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.research_agent import build_research_agent
from app.callbacks.cost_tracker import CostCallbackHandler

app = FastAPI()
agent = build_research_agent()   # Singleton

class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None

class QueryResponse(BaseModel):
    answer: str
    cost_usd: float
    tokens_used: int

@app.post("/v1/research", response_model=QueryResponse)
async def research(body: QueryRequest):
    cost_cb = CostCallbackHandler(feature="research_endpoint")
    try:
        result = await agent.ainvoke(
            {"input": body.query},
            config={"callbacks": [cost_cb], "run_name": "ResearchQuery"},
        )
        return QueryResponse(
            answer=result["output"],
            cost_usd=round(cost_cb.total_cost_usd, 6),
            tokens_used=cost_cb.total_input_tokens + cost_cb.total_output_tokens,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## MEMORY TYPES DECISION TABLE
```
InMemoryChatMessageHistory  → Single request/test; resets per process restart
RedisChatMessageHistory     → Multi-turn chat within a session (web app)
PostgresChatMessageHistory  → Long-term, auditable conversation store
VectorStore (Chroma)        → Semantic search over past conversations (>100 turns)
ConversationSummaryMemory   → Compress long histories to stay within context window
  → Use when: conversation > 10 turns AND model context < 32K tokens
```
