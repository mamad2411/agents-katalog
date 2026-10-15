---
name: ai-system-design-guide
description: Comprehensive guide for designing production AI systems, RAG architectures, LLM engineering, agentic AI, and interview preparation
triggers:
  - design an AI system for production
  - build a RAG pipeline with best practices
  - prepare for AI engineer interview
  - choose the right LLM model for my use case
  - implement agentic workflows with MCP
  - evaluate and monitor AI system performance
  - design multi-tenant AI architecture
  - implement tool-use and computer agents
---

# ai-system-design-guide

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What This Project Does

The **ai-system-design-guide** is a living, continuously updated reference for building production AI systems. It covers:

- **110+ interview questions** with staff-level answers and frameworks
- **RAG architectures**: chunking, vector databases, reranking, contextual retrieval, ColBERT
- **Model selection**: Claude Opus 4.7, GPT-5.5, Gemini 3.1 Pro, DeepSeek V4 Pro, Llama 4, and more (May 2026)
- **Agentic systems**: MCP 2.0, A2A protocols, tool-use, computer agents (OpenClaw)
- **Production patterns**: multi-tenant isolation, eval pipelines, LLMOps, security
- **Real case studies**: 20+ production architectures with diagrams and tradeoffs

This is NOT a tutorial for ML basics—it's a reference for engineers building production AI systems and preparing for staff+ interviews.

## Installation

This is a documentation repository. Clone it locally for offline reference:

```bash
git clone https://github.com/ombharatiya/ai-system-design-guide.git
cd ai-system-design-guide
```

## Repository Structure

```
ai-system-design-guide/
├── 00-interview-prep/           # 110 questions, answer frameworks, job trends
├── 01-foundations/              # LLM internals, transformers, attention
├── 02-model-landscape/          # Model taxonomy, pricing (May 2026)
├── 03-training-and-adaptation/  # Fine-tuning, LoRA, DPO, distillation
├── 04-inference-optimization/   # KV cache, vLLM, PagedAttention
├── 05-prompting-and-context/    # Prompt engineering, CoT, DSPy
├── 06-retrieval-systems/        # RAG, chunking, vector DBs, reranking
├── 07-agentic-systems/          # MCP, A2A, multi-agent, computer-use
├── 08-memory-and-state/         # L1-L3 memory, Mem0, caching
├── 09-frameworks-and-tools/     # LangGraph, DSPy, LlamaIndex, Claude Code
├── 10-document-processing/      # Vision-LLM OCR, multimodal parsing
├── 11-infrastructure-and-mlops/ # GPU clusters, LLMOps, cost
├── 12-security-and-access/      # RBAC, ABAC, multi-tenant isolation
├── 13-reliability-and-safety/   # Guardrails, red-teaming
├── 14-evaluation-and-observability/ # RAGAS, LangSmith, Phoenix
├── 15-ai-design-patterns/       # Pattern catalog, anti-patterns
├── 16-case-studies/             # 20+ real architectures
├── 17-tool-use-and-computer-agents/ # OpenClaw, Computer Use, safety
├── GLOSSARY.md                  # Every term defined
├── COURSES.md                   # Learning paths
└── TRANSITION_GUIDE.md          # Role transitions to AI
```

## Key Navigation Patterns

### Quick Lookup by Goal

```bash
# Interview prep
cat 00-interview-prep/01-question-bank.md
cat 00-interview-prep/02-answer-frameworks.md
cat 00-interview-prep/06-job-market-trends-2026.md

# Build RAG
cat 06-retrieval-systems/01-rag-fundamentals.md
cat 06-retrieval-systems/02-chunking-strategies.md
cat 06-retrieval-systems/04-vector-databases.md
cat 06-retrieval-systems/14-production-rag-at-scale.md

# Build agents
cat 07-agentic-systems/01-agent-fundamentals.md
cat 07-agentic-systems/03-tool-use-and-mcp.md
cat 09-frameworks-and-tools/02-langgraph-orchestration.md

# Pick a model
cat 02-model-landscape/01-model-taxonomy.md
cat 02-model-landscape/03-pricing-and-costs.md

# Evaluate AI
cat ai_evals_comprehensive_study_guide.md
cat ai_evals_complete_guide_langwatch_langfuse.md

# Multi-tenant systems
cat 12-security-and-access/04-multi-tenant-rag-isolation.md
cat 16-case-studies/08-multi-tenant-saas.md

# Tool-use and computer agents
cat 17-tool-use-and-computer-agents/01-tool-use-landscape.md
cat 17-tool-use-and-computer-agents/03-openclaw-deep-dive.md
cat 16-case-studies/16-computer-use-agent-production.md
```

### Model Selection (May 2026)

| Use Case | Recommended Model | File |
|----------|-------------------|------|
| General production | GPT-5.5 | `02-model-landscape/01-model-taxonomy.md` |
| Long-context reasoning | Claude Opus 4.7 | Same |
| Multimodal | Gemini 3.1 Pro | Same |
| Self-hosted (open) | DeepSeek V4 Pro, Llama 4 | Same |
| Cost-optimized | Gemini 3.1 Flash | `02-model-landscape/03-pricing-and-costs.md` |

## Common Patterns

### Pattern 1: Design a RAG System (Interview Question)

```markdown
# From 00-interview-prep/02-answer-frameworks.md

## Framework: RAG System Design

1. **Clarify requirements**
   - Query types (factual, multi-hop, temporal)
   - Latency budget (200ms? 2s?)
   - Scale (queries/sec, corpus size)
   - Accuracy requirements (precision@5, MRR)

2. **Document ingestion**
   - Parsing: Use Vision-LLM for PDFs (06-retrieval-systems/02-chunking-strategies.md)
   - Chunking: 512-token semantic chunks with 50-token overlap
   - Embeddings: text-embedding-3-large or Cohere embed-v3
   - Storage: Pinecone (managed) or Qdrant (self-hosted)

3. **Retrieval strategy**
   - Hybrid search: BM25 + vector (0.3/0.7 weight)
   - Rerank top-20 with Cohere rerank-3.5 or local BGE-reranker
   - Query expansion for multi-hop (HyDE or LLM rephrase)

4. **Generation**
   - Model: Claude Opus 4.7 for 200K context, GPT-5.5 for speed
   - Prompt: Include retrieved chunks + instruction to cite sources
   - Streaming: Server-Sent Events for <3s TTFT

5. **Evaluation**
   - Offline: RAGAS (context_precision, faithfulness, answer_relevancy)
   - Online: User thumbs up/down, response latency, hallucination rate

6. **Production concerns**
   - Cache: Redis for frequent queries (Mem0 pattern, 08-memory-and-state)
   - Monitoring: LangSmith or Phoenix for trace/eval
   - Guardrails: Check PII leakage, prompt injection
```

**Implementation reference**: `06-retrieval-systems/14-production-rag-at-scale.md`

### Pattern 2: Build an MCP Agent

```python
# From 07-agentic-systems/03-tool-use-and-mcp.md

# Example: MCP-enabled agent with Claude

import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define MCP tool schema (MCP 2.0)
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_docs",
        "description": "Search internal knowledge base",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]

# Tool execution stubs
def execute_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        # Call weather API
        return f"Weather in {tool_input['city']}: 72°F, sunny"
    elif tool_name == "search_docs":
        # Call vector search
        return "Documentation: Use the --verbose flag for detailed output"
    return "Tool not found"

# Agent loop with tool use
messages = [{"role": "user", "content": "What's the weather in SF and how do I enable verbose mode?"}]

while True:
    response = client.messages.create(
        model="claude-opus-4.7",  # May 2026 model
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    
    if response.stop_reason == "end_turn":
        # Final answer
        print(response.content[0].text)
        break
    
    elif response.stop_reason == "tool_use":
        # Execute tools
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        
        messages.append({"role": "user", "content": tool_results})
```

**Full details**: `07-agentic-systems/03-tool-use-and-mcp.md`, `09-frameworks-and-tools/02-langgraph-orchestration.md`

### Pattern 3: Multi-Tenant RAG with Isolation

```python
# From 12-security-and-access/04-multi-tenant-rag-isolation.md

# Defense-in-depth: L1 (query filter) + L2 (retrieval filter) + L3 (post-filter)

import qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = qdrant_client.QdrantClient(url=os.environ.get("QDRANT_URL"))

def search_multi_tenant(user_id: str, tenant_id: str, query: str, top_k: int = 5):
    """
    L1: Check user has access to tenant (before query)
    L2: Filter vector search by tenant_id
    L3: Post-filter results by document-level ACL
    """
    # L1: Authorization check
    if not user_has_tenant_access(user_id, tenant_id):
        raise PermissionError(f"User {user_id} cannot access tenant {tenant_id}")
    
    # Embed query
    query_vector = embed(query)  # e.g., text-embedding-3-large
    
    # L2: Retrieval-time filter (mandatory tenant_id match)
    results = client.search(
        collection_name="documents",
        query_vector=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))
            ]
        ),
        limit=top_k * 2  # Over-retrieve for L3 filtering
    )
    
    # L3: Post-retrieval ACL check (document-level permissions)
    filtered = []
    for hit in results:
        doc_acl = hit.payload.get("allowed_users", [])
        if user_id in doc_acl or hit.payload.get("public", False):
            filtered.append(hit)
        if len(filtered) == top_k:
            break
    
    return filtered

def user_has_tenant_access(user_id: str, tenant_id: str) -> bool:
    # Check user-tenant mapping in auth DB
    # For multi-tenant SaaS: each user belongs to one tenant
    # For enterprise: RBAC with tenant scopes
    return True  # Stub: implement with your auth layer
```

**Full case study**: `16-case-studies/08-multi-tenant-saas.md`

### Pattern 4: Eval-Gated CI/CD

```python
# From 16-case-studies/18-eval-gated-cicd.md

# Block PRs if AI quality regresses below threshold

import langfuse
import openai
import os

langfuse_client = langfuse.Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY")
)

def run_eval_suite(model_name: str, golden_set: list) -> dict:
    """
    Run golden-set eval with LLM judge (GPT-5.5 as judge)
    Returns: {"accuracy": 0.92, "faithfulness": 0.88, "latency_p95": 1200}
    """
    results = []
    for example in golden_set:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": example["input"]}]
        )
        
        # LLM judge: compare response to expected output
        judge_prompt = f"""
        Expected: {example["expected_output"]}
        Actual: {response.choices[0].message.content}
        Rate accuracy (0-1) and faithfulness (0-1).
        Return JSON: {{"accuracy": 0.9, "faithfulness": 0.85}}
        """
        judge_response = openai.ChatCompletion.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": judge_prompt}]
        )
        scores = eval(judge_response.choices[0].message.content)
        results.append(scores)
        
        # Log to Langfuse for tracing
        langfuse_client.trace(
            name=f"eval_{example['id']}",
            input=example["input"],
            output=response.choices[0].message.content,
            metadata={"model": model_name, "judge_scores": scores}
        )
    
    # Aggregate
    avg_accuracy = sum(r["accuracy"] for r in results) / len(results)
    avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
    
    return {
        "accuracy": avg_accuracy,
        "faithfulness": avg_faithfulness,
        "latency_p95": 1200  # Stub: measure in prod
    }

def ci_check(pr_model: str, baseline_model: str, golden_set: list):
    """
    Run in CI: compare PR model vs baseline
    Fail PR if accuracy drops >2% or faithfulness drops >3%
    """
    pr_metrics = run_eval_suite(pr_model, golden_set)
    baseline_metrics = run_eval_suite(baseline_model, golden_set)
    
    accuracy_delta = pr_metrics["accuracy"] - baseline_metrics["accuracy"]
    faithfulness_delta = pr_metrics["faithfulness"] - baseline_metrics["faithfulness"]
    
    if accuracy_delta < -0.02:
        raise Exception(f"Accuracy regression: {accuracy_delta:.2%}")
    if faithfulness_delta < -0.03:
        raise Exception(f"Faithfulness regression: {faithfulness_delta:.2%}")
    
    print(f"✅ Eval passed: accuracy {pr_metrics['accuracy']:.2%}, faithfulness {pr_metrics['faithfulness']:.2%}")
```

**Full pipeline**: `16-case-studies/18-eval-gated-cicd.md`, `ai_evals_comprehensive_study_guide.md`

## Configuration

This is a documentation repository with no runtime configuration. For the frameworks and tools referenced in the guide, see:

- **LangGraph**: `09-frameworks-and-tools/02-langgraph-orchestration.md`
- **DSPy**: `09-frameworks-and-tools/03-dspy-prompt-optimization.md`
- **LangSmith**: `14-evaluation-and-observability/02-langsmith-tracing.md`
- **Phoenix/Langfuse**: `ai_evals_comprehensive_study_guide.md`

## Real Code Examples

### Example 1: Production RAG with Reranking

```python
# From 06-retrieval-systems/06-reranking-strategies.md

import cohere
import qdrant_client
import os

cohere_client = cohere.Client(os.environ.get("COHERE_API_KEY"))
qdrant = qdrant_client.QdrantClient(url=os.environ.get("QDRANT_URL"))

def rag_with_reranking(query: str, top_k: int = 5) -> list:
    """
    1. Vector search (retrieve top-20)
    2. Rerank with Cohere rerank-3.5
    3. Return top-5 after reranking
    """
    # Step 1: Vector search
    query_vector = embed(query)  # e.g., OpenAI text-embedding-3-large
    vector_results = qdrant.search(
        collection_name="knowledge_base",
        query_vector=query_vector,
        limit=20  # Over-retrieve for reranking
    )
    
    # Step 2: Rerank
    docs = [hit.payload["text"] for hit in vector_results]
    rerank_response = cohere_client.rerank(
        model="rerank-3.5",  # May 2026 model
        query=query,
        documents=docs,
        top_n=top_k
    )
    
    # Step 3: Return top-k with rerank scores
    reranked = []
    for result in rerank_response.results:
        original_hit = vector_results[result.index]
        reranked.append({
            "text": original_hit.payload["text"],
            "metadata": original_hit.payload["metadata"],
            "rerank_score": result.relevance_score,
            "vector_score": original_hit.score
        })
    
    return reranked

def embed(text: str):
    # Stub: use OpenAI or Cohere embedding API
    import openai
    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding
```

### Example 2: Agentic RAG with LangGraph

```python
# From 06-retrieval-systems/13-agentic-rag.md

from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    plan: str
    retrieved_docs: list
    answer: str

def plan_step(state: AgentState) -> AgentState:
    """Decompose query into sub-questions"""
    state["plan"] = llm_call(f"Break down this query: {state['query']}")
    return state

def retrieve_step(state: AgentState) -> AgentState:
    """Multi-step retrieval based on plan"""
    sub_queries = state["plan"].split("\n")
    all_docs = []
    for sub_q in sub_queries:
        docs = rag_with_reranking(sub_q, top_k=3)
        all_docs.extend(docs)
    state["retrieved_docs"] = all_docs
    return state

def synthesize_step(state: AgentState) -> AgentState:
    """Generate final answer from all retrieved docs"""
    context = "\n".join([d["text"] for d in state["retrieved_docs"]])
    state["answer"] = llm_call(f"Answer: {state['query']}\nContext: {context}")
    return state

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("plan", plan_step)
workflow.add_node("retrieve", retrieve_step)
workflow.add_node("synthesize", synthesize_step)
workflow.add_edge("plan", "retrieve")
workflow.add_edge("retrieve", "synthesize")
workflow.add_edge("synthesize", END)
workflow.set_entry_point("plan")

app = workflow.compile()

# Run agentic RAG
result = app.invoke({"query": "What are the multi-hop causes of the 2008 financial crisis?"})
print(result["answer"])
```

**Full details**: `06-retrieval-systems/13-agentic-rag.md`, `09-frameworks-and-tools/02-langgraph-orchestration.md`

### Example 3: Computer-Use Agent with Safety Gates

```python
# From 17-tool-use-and-computer-agents/03-openclaw-deep-dive.md
# and 16-case-studies/16-computer-use-agent-production.md

import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Action gate: block destructive actions
BLOCKED_ACTIONS = ["delete", "rm -rf", "DROP TABLE", "sudo"]

def action_gate(action: str) -> bool:
    """L1 defense: block obviously destructive actions"""
    return not any(keyword in action.lower() for keyword in BLOCKED_ACTIONS)

def run_computer_use_agent(task: str, sandbox_url: str):
    """
    Computer-use agent with Firecracker VM sandbox + action gate
    """
    messages = [{"role": "user", "content": task}]
    
    while True:
        response = client.messages.create(
            model="claude-opus-4.7",
            max_tokens=8192,
            tools=[
                {
                    "type": "computer_20241022",
                    "name": "computer",
                    "display_width_px": 1920,
                    "display_height_px": 1080
                }
            ],
            messages=messages
        )
        
        if response.stop_reason == "end_turn":
            print(f"Task complete: {response.content[0].text}")
            break
        
        elif response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use" and block.name == "computer":
                    action = block.input.get("action")
                    
                    # Action gate check
                    if not action_gate(str(block.input)):
                        result = "BLOCKED: Action violates safety policy"
                    else:
                        # Execute in sandbox (Firecracker VM)
                        result = execute_in_sandbox(sandbox_url, block.input)
                    
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        }]
                    })

def execute_in_sandbox(sandbox_url: str, action: dict) -> str:
    """
    Send action to isolated Firecracker VM
    VM has network egress blocked, no access to prod data
    """
    import requests
    response = requests.post(
        f"{sandbox_url}/execute",
        json=action,
        headers={"X-Sandbox-Token": os.environ.get("SANDBOX_TOKEN")}
    )
    return response.json()["output"]
```

**Full production setup**: `16-case-studies/16-computer-use-agent-production.md`, `17-tool-use-and-computer-agents/07-safety-and-governance.md`

## Troubleshooting

### Issue: "Which model should I use?"

**Solution**: Check `02-model-landscape/01-model-taxonomy.md` for decision matrix. Quick picks:
- **General**: GPT-5.5
- **Long-context/tool-use**: Claude Opus 4.7
- **Multimodal**: Gemini 3.1 Pro
- **Self-hosted**: DeepSeek V4 Pro, Llama 4

### Issue: "RAG is returning irrelevant results"

**Solution**: Checklist from `06-retrieval-systems/14-production-rag-at-scale.md`:
1. Check chunking strategy (semantic vs fixed-size)
2. Add reranking layer (Cohere rerank-3.5)
3. Use hybrid search (BM25 + vector)
4. Try query expansion (HyDE or LLM rephrase)
5. Eval with RAGAS: if `context_precision < 0.7`, fix retrieval; if `faithfulness < 0.8`, fix generation

### Issue: "Agent is looping or hallucinating tool calls"

**Solution**: From `07-agentic-systems/01-agent-fundamentals.md`:
1. Add max iteration limit (e.g., 5 loops)
2. Use structured output with strict JSON schema
3. Add self-critique step: ask LLM "Is this tool call necessary?"
4. Log all tool calls to LangSmith for debugging

### Issue: "How do I isolate tenants in multi-tenant RAG?"

**Solution**: Defense-in-depth pattern from `12-security-and-access/04-multi-tenant-rag-isolation.md`:
- **L1**: Authorization check before query
- **L2**: Filter vector search by `tenant_id` (mandatory)
- **L3**: Post-filter by document-level ACL

### Issue: "Eval metrics are failing in CI"

**Solution**: From `16-case-studies/18-eval-gated-cicd.md`:
1. Use golden-set with at least 50 examples per use case
2. LLM judge with GPT-5.5 (more reliable than GPT-4o)
3. Statistical correction: require >5% delta to flag regression (avoid noise)
4. Log all eval runs to Langfuse for debugging judge decisions

### Issue: "How do I prepare for an AI engineer interview?"

**Solution**: Start with `00-interview-prep/01-question-bank.md` (110 questions) and `00-interview-prep/02-answer-frameworks.md`. Practice whiteboard exercises in `00-interview-prep/03-whiteboard-exercises.md`. Check `00-interview-prep/06-job-market-trends-2026.md` for May 2026 hiring landscape.

## Advanced Patterns

### Pattern: ColBERT Late Interaction

```python
# From 06-retrieval-systems/11-late-interaction-colbert.md

from colbert import Searcher
from colbert.infra import Run, RunConfig

# Initialize ColBERT searcher
with Run().context(RunConfig(nranks=1, experiment="my_index")):
    searcher = Searcher(index="my_colbert_index")

def colbert_search(query: str, top_k: int = 5):
    """
    ColBERT: token-level similarity (not sentence embedding)
    Better for multi-aspect queries and long documents
    """
    results = searcher.search(query, k=top_k)
    
    return [
        {
            "doc_id": doc_id,
            "score": score,
            "text": searcher.collection[doc_id]
        }
        for doc_id, score in zip(results[0], results[1])
    ]
```

**When to use**: Multi-hop queries, long documents (>2K tokens), academic search. See full comparison in `06-retrieval-systems/11-late-interaction-colbert.md`.

### Pattern: Distillation Pipeline

```python
# From 16-case-studies/19-customer-distillation-pipeline.md

import openai
import os

def distill_from_traces(teacher_model: str, student_model: str, traces: list):
    """
    Distill student model from teacher traces
    1. Collect teacher responses (e.g., Claude Opus 4.7)
    2. Fine-tune student (e.g., Llama 4 8B) on (input, teacher_output) pairs
    3. Eval on holdout set
    """
    training_data = []
    for trace in traces:
        # Generate teacher response
        teacher_response = openai.ChatCompletion.create(
            model=teacher_model,
            messages=[{"role": "user", "content": trace["input"]}]
        )
        training_data.append({
            "messages": [
                {"role": "user", "content": trace["input"]},
                {"role": "assistant", "content": teacher_response.choices[0].message.content}
            ]
        })
    
    # Fine-tune student (OpenAI fine-tuning API or local LoRA)
    fine_tune_job = openai.FineTuningJob.create(
        training_file=upload_jsonl(training_data),
        model=student_model,
        suffix="distilled_from_opus"
    )
    
    return fine_tune_job.id
```

**ROI**: Cut $50K/mo frontier model spend to $6K with 3-month payback. Full case study: `16-case-studies/19-customer-distillation-pipeline.md`.

## Contributing to the Guide

The guide welcomes PRs for:
- New case studies with production tradeoffs
- Updated model pricing (verify with API docs)
- New patterns (MCP tools, eval techniques)
- Interview questions from real staff+ interviews

See `CONTRIBUTING.md` in the repo for guidelines.

## Quick Reference: Interview Question Types

From `00-interview-prep/01-question-bank.md`:

| Category | Example Question | File |
|----------|------------------|------|
| System design | "Design a multi-tenant RAG for 1M users" | Case study 08 |
| Model selection | "When to use Claude vs GPT vs Gemini?" | `02-model-landscape/01-model-taxonomy.md` |
| RAG optimization | "How to reduce hallucination in RAG?" | `06-retrieval-systems/14-production-rag-at-scale.md` |
| Agents | "Design a coding agent with tool use" | `16-case-studies/07-autonomous-coding-agent.md` |
| Evaluation | "How to eval a chatbot in production?" | `ai_evals_comprehensive_study_guide.md` |
| Tradeoffs | "Latency vs accuracy for search?" | `16-case-studies/06-real-time-search.md` |

## Related Resources

- **Glossary**: `GLOSSARY.md` — every term defined
- **Courses**: `COURSES.md` — learning paths for AI engineers
- **Transitions**: `TRANSITION_GUIDE.md` — move from backend
