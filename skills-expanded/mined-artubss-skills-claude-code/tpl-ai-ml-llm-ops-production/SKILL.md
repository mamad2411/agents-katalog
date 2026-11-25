---
name: tpl-ai-ml-llm-ops-production
description: Template do pack (ai-ml/06-llm-ops-production.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/06-llm-ops-production.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: LLMOps Production (LangSmith + Langfuse + Model Routing + Prompt Management)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/06-llm-ops-production.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Observability:** Langfuse (self-hosted or cloud) + LangSmith (tracing)
- **Prompt Management:** Langfuse Prompt Registry / LangChain Hub
- **Model Router:** Custom router — OpenAI GPT-5.4 / Anthropic Claude Sonnet 4.6 / local Ollama
- **API:** FastAPI + async
- **Cost Tracking:** Per-feature budget tracking in PostgreSQL
- **A/B Testing:** Prompt variant routing with statistical significance
- **Evaluation:** LLM-as-Judge (automated) + human annotation workflow

---

## ARCHITECTURE RULES
1. **Every LLM call is traced** — no blind calls; every trace has: run_name, feature tag, user_id, session_id.
2. **Prompts are versioned in registry** — never hardcode prompts in code; pull from Langfuse/LangChain Hub; version = commit.
3. **Model routing is explicit** — define routing logic in config, not scattered in code; change models without code deploys.
4. **Cost budget per feature** — define monthly budget per feature; block calls when budget exceeded.
5. **Latency SLO defined and measured** — P99 < 3s for interactive, P99 < 30s for batch; alert on breach.
6. **Evaluation pipelines run automatically** — on every prompt change, evaluation pipeline triggers; no manual testing.
7. **Fallback chain is mandatory** — OpenAI down → Anthropic → local; never single point of failure.
8. **Prompt A/B testing requires sample size** — minimum 200 samples per variant before declaring winner.

---

## LANGFUSE TRACING SETUP

```python
# app/tracing.py
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe
import os

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

# Usage: decorate any LLM function
@observe(name="SummarizeChain")
async def summarize_document(text: str, user_id: str) -> str:
    langfuse_context.update_current_trace(
        user_id=user_id,
        tags=["summarize", "v1"],
        metadata={"text_length": len(text)},
    )

    # LLM call happens here — automatically traced
    result = await llm_chain.ainvoke({"text": text})

    # Score the output (for automated eval tracking)
    langfuse_context.score_current_observation(
        name="output_length",
        value=len(result),
    )

    return result
```

---

## MODEL ROUTER

```python
# app/routing/model_router.py
from dataclasses import dataclass
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os

class ModelTier(Enum):
    FAST    = "fast"      # gpt-5.4-mini / claude-haiku — cheap, fast
    SMART   = "smart"     # gpt-5.4 / claude-sonnet-4-6 — high quality
    LOCAL   = "local"     # Ollama — free, private

@dataclass
class RoutingConfig:
    """Define per-feature model routing in one place."""
    feature: str
    tier: ModelTier
    max_tokens: int
    temperature: float = 0.0
    monthly_budget_usd: float = 50.0

# Central routing table — change models here without touching feature code
ROUTING_TABLE: dict[str, RoutingConfig] = {
    "chat":           RoutingConfig("chat",          ModelTier.SMART, 2048, 0.7, 500.0),
    "summarize":      RoutingConfig("summarize",     ModelTier.FAST,  1024, 0.0, 100.0),
    "classify":       RoutingConfig("classify",      ModelTier.FAST,   256, 0.0,  50.0),
    "code_review":    RoutingConfig("code_review",   ModelTier.SMART, 4096, 0.0, 200.0),
    "extraction":     RoutingConfig("extraction",    ModelTier.FAST,   512, 0.0,  50.0),
    "batch_process":  RoutingConfig("batch_process", ModelTier.LOCAL, 2048, 0.0,   0.0),
}

def get_llm_for_feature(feature: str):
    config = ROUTING_TABLE.get(feature)
    if not config:
        raise ValueError(f"Unknown feature: {feature}. Add to ROUTING_TABLE.")

    if config.tier == ModelTier.FAST:
        return ChatOpenAI(model="gpt-5.4-mini", temperature=config.temperature,
                          max_tokens=config.max_tokens)

    elif config.tier == ModelTier.SMART:
        primary = ChatOpenAI(model="gpt-5.4", temperature=config.temperature,
                             max_tokens=config.max_tokens)
        fallback = ChatAnthropic(model="claude-sonnet-4-6",
                                 temperature=config.temperature,
                                 max_tokens=config.max_tokens)
        return primary.with_fallbacks([fallback])

    elif config.tier == ModelTier.LOCAL:
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model="llama3:8b", temperature=config.temperature)
```

---

## PROMPT VERSIONING (LANGFUSE REGISTRY)

```python
# app/prompts/registry.py
from langfuse import Langfuse
from langchain_core.prompts import ChatPromptTemplate

langfuse = Langfuse()

def get_prompt(prompt_name: str, version: int | None = None) -> ChatPromptTemplate:
    """
    Fetch prompt from Langfuse registry.
    version=None → uses 'production' label (latest approved)
    version=N    → specific version for A/B testing
    """
    lf_prompt = langfuse.get_prompt(
        name=prompt_name,
        version=version,
        label="production" if version is None else None,
        type="chat",
    )

    return lf_prompt.get_langchain_prompt()

# Usage:
# prompt = get_prompt("summarize-document")   # Always fetches production version
# prompt = get_prompt("summarize-document", version=12)   # A/B test variant
```

---

## COST TRACKING PER FEATURE

```python
# app/cost/tracker.py
import asyncpg
import os
from datetime import datetime, timezone
from app.routing.model_router import ROUTING_TABLE

COST_PER_1K = {
    "gpt-5.4":             {"input": 0.005,  "output": 0.015},
    "gpt-5.4-mini":        {"input": 0.00015,"output": 0.0006},
    "claude-sonnet-4-6":   {"input": 0.003,  "output": 0.015},
}

async def log_and_check_budget(
    feature: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    db_pool: asyncpg.Pool,
) -> None:
    rates = COST_PER_1K.get(model, COST_PER_1K["gpt-5.4"])
    cost = (input_tokens / 1000 * rates["input"]) + \
           (output_tokens / 1000 * rates["output"])

    async with db_pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO llm_cost_log (feature, model, input_tokens, output_tokens, cost_usd, created_at)
               VALUES ($1, $2, $3, $4, $5, $6)""",
            feature, model, input_tokens, output_tokens, cost, datetime.now(timezone.utc)
        )

        # Check monthly budget
        monthly_spend = await conn.fetchval(
            """SELECT COALESCE(SUM(cost_usd), 0) FROM llm_cost_log
               WHERE feature = $1 AND date_trunc('month', created_at) = date_trunc('month', NOW())""",
            feature
        )

    budget = ROUTING_TABLE[feature].monthly_budget_usd
    if monthly_spend > budget * 0.95:
        # Alert at 95% — don't hard-block, just alert
        logger.warning({
            "event": "budget_alert",
            "feature": feature,
            "spent_usd": monthly_spend,
            "budget_usd": budget,
            "pct_used": round(monthly_spend / budget * 100, 1),
        })
```

---

## LLM-AS-JUDGE EVALUATION PIPELINE

```python
# app/evaluation/judge.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class JudgeScore(BaseModel):
    score: int = Field(ge=1, le=10, description="Quality score 1-10")
    reasoning: str = Field(description="Brief explanation of the score")
    passed: bool = Field(description="Whether it meets production bar (score >= 7)")

JUDGE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert evaluator assessing LLM output quality.
Score the response on a scale of 1-10 on these criteria:
- Accuracy: Is the information correct and grounded in the context?
- Completeness: Does it fully address the user's question?
- Clarity: Is it clear and well-structured?
Score >= 7 = production quality. Score < 7 = needs improvement."""),
    ("human", """Question: {question}

Context: {context}

Response to evaluate: {response}

Provide your evaluation.""")
])

judge_llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)

async def evaluate_with_judge(
    question: str,
    context: str,
    response: str,
) -> JudgeScore:
    chain = JUDGE_PROMPT | judge_llm.with_structured_output(JudgeScore)
    return await chain.ainvoke({
        "question": question,
        "context": context,
        "response": response,
    })
```

---

## LATENCY SLOs

```yaml
# SLO definitions — enforce with Prometheus alerts
SLOs:
  interactive:
    features: [chat, classify, extraction]
    p50_target_ms: 800
    p95_target_ms: 2000
    p99_target_ms: 3000
    error_budget_monthly_pct: 0.1%  # 99.9% success rate

  async_batch:
    features: [summarize, code_review, batch_process]
    p95_target_ms: 15000
    p99_target_ms: 30000
    error_budget_monthly_pct: 1%
```

---

## FALLBACK CHAIN PATTERN

```python
# app/routing/fallback.py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableWithFallbacks
import openai, anthropic

def build_resilient_chain():
    """3-level fallback: OpenAI → Anthropic → Local Ollama"""
    primary  = ChatOpenAI(model="gpt-5.4", timeout=10)
    backup   = ChatAnthropic(model="claude-sonnet-4-6", timeout=15)
    local    = ChatOllama(model="llama3:8b", timeout=60)

    return primary.with_fallbacks(
        [backup, local],
        exceptions_to_handle=(
            openai.RateLimitError,
            openai.APIConnectionError,
            openai.APIStatusError,
        ),
    )
```

---

## PROMPT A/B TEST FRAMEWORK

```python
# app/ab_testing/prompt_ab.py
import random
from app.tracing import langfuse

def get_ab_prompt(prompt_name: str, user_id: str) -> tuple[object, str]:
    """Returns (prompt, variant_label) for consistent per-user assignment."""
    # Consistent hashing: same user always gets same variant
    variant = "control" if hash(user_id) % 100 < 70 else "treatment"

    version_map = {
        "control":   None,    # Production label
        "treatment": 15,      # Specific version being tested
    }

    prompt = langfuse.get_prompt(
        name=prompt_name,
        version=version_map[variant],
        label="production" if version_map[variant] is None else None,
    )

    # Tag trace with variant for analysis
    langfuse_context.update_current_trace(
        metadata={"ab_variant": variant, "prompt_version": version_map[variant]},
    )

    return prompt.get_langchain_prompt(), variant

# Analyze A/B results:
# SELECT variant, AVG(score), COUNT(*) FROM evaluation_results
# WHERE prompt_name = 'summarize-document'
# GROUP BY variant HAVING COUNT(*) >= 200;
```
