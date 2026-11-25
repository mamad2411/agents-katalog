---
name: llm-toolkit
description: Consolidated toolkit for llm. Covers llm-app-patterns, llm-application-dev-prompt-optimize, llm-application-dev-ai-assistant, llm-application-dev-langchain-agent, llm-evaluation
---
# Llm Toolkit

## Use this skill when
- Building confidence in production systems
- Comparing different models or prompts
- Debugging unexpected model behavior
- Detecting performance regressions before deployment
- Establishing baselines and tracking progress over time
- Measuring LLM application performance systematically
- Needing guidance, best practices, or checklists for ai assistant development
- Needing guidance, best practices, or checklists for langchain/langgraph agent development expert
- Needing guidance, best practices, or checklists for prompt optimization
- Validating improvements from prompt changes
- Working on ai assistant development tasks or workflows
- Working on langchain/langgraph agent development expert tasks or workflows
- Working on prompt optimization tasks or workflows

## Do not use this skill when
- The task is unrelated to ai assistant development
- The task is unrelated to langchain/langgraph agent development expert
- The task is unrelated to llm evaluation
- The task is unrelated to prompt optimization
- You need a different domain or tool outside this scope

## Core Capabilities
# Llm Toolkit

# 🤖 LLM Application Patterns

> Production-ready patterns for building LLM applications, inspired by [Dify](https://github.com/langgenius/dify) and industry best practices.

## When to Use This Skill

Use this skill when:

- Designing LLM-powered applications
- Implementing RAG (Retrieval-Augmented Generation)
- Building AI agents with tools
- Setting up LLMOps monitoring
- Choosing between agent architectures

---

## 1. RAG Pipeline Architecture

### Overview

RAG (Retrieval-Augmented Generation) grounds LLM responses in your data.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Ingest    │────▶│   Retrieve  │────▶│   Generate  │
│  Documents  │     │   Context   │     │   Response  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
 ┌─────────┐       ┌───────────┐       ┌───────────┐
 │ Chunking│       │  Vector   │       │    LLM    │
 │Embedding│       │  Search   │       │  + Context│
 └─────────┘       └───────────┘       └───────────┘
```

### 1.1 Document Ingestion

```python
# Chunking strategies
class ChunkingStrategy:
    # Fixed-size chunks (simple but may break context)
    FIXED_SIZE = "fixed_size"  # e.g., 512 tokens

    # Semantic chunking (preserves meaning)
    SEMANTIC = "semantic"      # Split on paragraphs/sections

    # Recursive splitting (tries multiple separators)
    RECURSIVE = "recursive"    # ["\n\n", "\n", " ", ""]

    # Document-aware (respects structure)
    DOCUMENT_AWARE = "document_aware"  # Headers, lists, etc.

# Recommended settings
CHUNK_CONFIG = {
    "chunk_size": 512,       # tokens
    "chunk_overlap": 50,     # token overlap between chunks
    "separators": ["\n\n", "\n", ". ", " "],
}
```

### 1.2 Embedding & Storage

```python
# Vector database selection
VECTOR_DB_OPTIONS = {
    "pinecone": {
        "use_case": "Production, managed service",
        "scale": "Billions of vectors",
        "features": ["Hybrid search", "Metadata filtering"]
    },
    "weaviate": {
        "use_case": "Self-hosted, multi-modal",
        "scale": "Millions of vectors",
        "features": ["GraphQL API", "Modules"]
    },
    "chromadb": {
        "use_case": "Development, prototyping",
        "scale": "Thousands of vectors",
        "features": ["Simple API", "In-memory option"]
    },
    "pgvector": {
        "use_case": "Existing Postgres infrastructure",
        "scale": "Millions of vectors",
        "features": ["SQL integration", "ACID compliance"]
    }
}

# Embedding model selection
EMBEDDING_MODELS = {
    "openai/text-embedding-3-small": {
        "dimensions": 1536,
        "cost": "$0.02/1M tokens",
        "quality": "Good for most use cases"
    },
    "openai/text-embedding-3-large": {
        "dimensions": 3072,
        "cost": "$0.13/1M tokens",
        "quality": "Best for complex queries"
    },
    "local/bge-large": {
        "dimensions": 1024,
        "cost": "Free (compute only)",
        "quality": "Comparable to OpenAI small"
    }
}
```

### 1.3 Retrieval Strategies

```python
# Basic semantic search
def semantic_search(query: str, top_k: int = 5):
    query_embedding = embed(query)
    results = vector_db.similarity_search(
        query_embedding,
        top_k=top_k
    )
    return results

# Hybrid search (semantic + keyword)
def hybrid_search(query: str, top_k: int = 5, alpha: float = 0.5):
    """
    alpha=1.0: Pure semantic
    alpha=0.0: Pure keyword (BM25)
    alpha=0.5: Balanced
    """
    semantic_results = vector_db.similarity_search(query)
    keyword_results = bm25_search(query)

    # Reciprocal Rank Fusion
    return rrf_merge(semantic_results, keyword_results, alpha)

# Multi-query retrieval
def multi_query_retrieval(query: str):
    """Generate multiple query variations for better recall"""
    queries = llm.generate_query_variations(query, n=3)
    all_results = []
    for q in queries:
        all_results.extend(semantic_search(q))
    return deduplicate(all_results)

# Contextual compression
def compressed_retrieval(query: str):
    """Retrieve then compress to relevant parts only"""
    docs = semantic_search(query, top_k=10)
    compressed = llm.extract_relevant_parts(docs, query)
    return compressed
```

### 1.4 Generation with Context

```python
RAG_PROMPT_TEMPLATE = """
Answer the user's question based ONLY on the following context.
If the context doesn't contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""

def generate_with_rag(question: str):
    # Retrieve
    context_docs = hybrid_search(question, top_k=5)
    context = "\n\n".join([doc.content for doc in context_docs])

    # Generate
    prompt = RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    response = llm.generate(prompt)

    # Return with citations
    return {
        "answer": response,
        "sources": [doc.metadata for doc in context_docs]
    }
```

---

## 2. Agent Architectures

### 2.1 ReAct Pattern (Reasoning + Acting)

```
Thought: I need to search for information about X
Action: search("X")
Observation: [search results]
Thought: Based on the results, I should...
Action: calculate(...)
Observation: [calculation result]
Thought: I now have enough information
Action: final_answer("The answer is...")
```

```python
REACT_PROMPT = """
You are an AI assistant that can use tools to answer questions.

Available tools:
{tools_description}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(arguments)]
Observation: [tool result - this will be filled in]
... (repeat Thought/Action/Observation as needed)
Thought: I have enough information to answer
Final Answer: [your final response]

Question: {question}
"""

class ReActAgent:
    def __init__(self, tools: list, llm):
        self.tools = {t.name: t for t in tools}
        self.llm = llm
        self.max_iterations = 10

    def run(self, question: str) -> str:
        prompt = REACT_PROMPT.format(
            tools_description=self._format_tools(),
            question=question
        )

        for _ in range(self.max_iterations):
            response = self.llm.generate(prompt)

            if "Final Answer:" in response:
                return self._extract_final_answer(response)

            action = self._parse_action(response)
            observation = self._execute_tool(action)
            prompt += f"\nObservation: {observation}\n"

        return "Max iterations reached"
```

### 2.2 Function Calling Pattern

```python
# Define tools as functions with schemas
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }
]

class FunctionCallingAgent:
    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]

        while True:
            response = self.llm.chat(
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(
                        tool_call.name,
                        tool_call.arguments
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                return response.content
```

### 2.3 Plan-and-Execute Pattern

```python
class PlanAndExecuteAgent:
    """
    1. Create a plan (list of steps)
    2. Execute each step
    3. Replan if needed
    """

    def run(self, task: str) -> str:
        # Planning phase
        plan = self.planner.create_plan(task)
        # Returns: ["Step 1: ...", "Step 2: ...", ...]

        results = []
        for step in plan:
            # Execute each step
            result = self.executor.execute(step, context=results)
            results.append(result)

            # Check if replan needed
            if self._needs_replan(task, results):
                new_plan = self.planner.replan(
                    task,
                    completed=results,
                    remaining=plan[len(results):]
                )
                plan = new_plan

        # Synthesize final answer
        return self.synthesizer.summarize(task, results)
```

### 2.4 Multi-Agent Collaboration

```python
class AgentTeam:
    """
    Specialized agents collaborating on complex tasks
    """

    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
            "critic": CriticAgent()
        }
        self.coordinator = CoordinatorAgent()

    def solve(self, task: str) -> str:
        # Coordinator assigns subtasks
        assignments = self.coordinator.decompose(task)

        results = {}
        for assignment in assignments:
            agent = self.agents[assignment.agent]
            result = agent.execute(
                assignment.subtask,
                context=results
            )
            results[assignment.id] = result

        # Critic reviews
        critique = self.agents["critic"].review(results)

        if critique.needs_revision:
            # Iterate with feedback
            return self.solve_with_feedback(task, results, critique)

        return self.coordinator.synthesize(results)
```

---

## 3. Prompt IDE Patterns

### 3.1 Prompt Templates with Variables

```python
class PromptTemplate:
    def __init__(self, template: str, variables: list[str]):
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        # Validate all variables provided
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")

        return self.template.format(**kwargs)

    def with_examples(self, examples: list[dict]) -> str:
        """Add few-shot examples"""
        example_text = "\n\n".join([
            f"Input: {ex['input']}\nOutput: {ex['output']}"
            for ex in examples
        ])
        return f"{example_text}\n\n{self.template}"

# Usage
summarizer = PromptTemplate(
    template="Summarize the following text in {style} style:\n\n{text}",
    variables=["style", "text"]
)

prompt = summarizer.format(
    style="professional",
    text="Long article content..."
)
```

### 3.2 Prompt Versioning & A/B Testing

```python
class PromptRegistry:
    def __init__(self, db):
        self.db = db

    def register(self, name: str, template: str, version: str):
        """Store prompt with version"""
        self.db.save({
            "name": name,
            "template": template,
            "version": version,
            "created_at": datetime.now(),
            "metrics": {}
        })

    def get(self, name: str, version: str = "latest") -> str:
        """Retrieve specific version"""
        return self.db.get(name, version)

    def ab_test(self, name: str, user_id: str) -> str:
        """Return variant based on user bucket"""
        variants = self.db.get_all_versions(name)
        bucket = hash(user_id) % len(variants)
        return variants[bucket]

    def record_outcome(self, prompt_id: str, outcome: dict):
        """Track prompt performance"""
        self.db.update_metrics(prompt_id, outcome)
```

### 3.3 Prompt Chaining

```python
class PromptChain:
    """
    Chain prompts together, passing output as input to next
    """

    def __init__(self, steps: list[dict]):
        self.steps = steps

    def run(self, initial_input: str) -> dict:
        context = {"input": initial_input}
        results = []

        for step in self.steps:
            prompt = step["prompt"].format(**context)
            output = llm.generate(prompt)

            # Parse output if needed
            if step.get("parser"):
                output = step["parser"](output)

            context[step["output_key"]] = output
            results.append({
                "step": step["name"],
                "output": output
            })

        return {
            "final_output": context[self.steps[-1]["output_key"]],
            "intermediate_results": results
        }

# Example: Research → Analyze → Summarize
chain = PromptChain([
    {
        "name": "research",
        "prompt": "Research the topic: {input}",
        "output_key": "research"
    },
    {
        "name": "analyze",
        "prompt": "Analyze these findings:\n{research}",
        "output_key": "analysis"
    },
    {
        "name": "summarize",
        "prompt": "Summarize this analysis in 3 bullet points:\n{analysis}",
        "output_key": "summary"
    }
])
```

---

## 4. LLMOps & Observability

### 4.1 Metrics to Track

```python
LLM_METRICS = {
    # Performance
    "latency_p50": "50th percentile response time",
    "latency_p99": "99th percentile response time",
    "tokens_per_second": "Generation speed",

    # Quality
    "user_satisfaction": "Thumbs up/down ratio",
    "task_completion": "% tasks completed successfully",
    "hallucination_rate": "% responses with factual errors",

    # Cost
    "cost_per_request": "Average $ per API call",
    "tokens_per_request": "Average tokens used",
    "cache_hit_rate": "% requests served from cache",

    # Reliability
    "error_rate": "% failed requests",
    "timeout_rate": "% requests that timed out",
    "retry_rate": "% requests needing retry"
}
```

### 4.2 Logging & Tracing

```python
import logging
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class LLMLogger:
    def log_request(self, request_id: str, data: dict):
        """Log LLM request for debugging and analysis"""
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "model": data["model"],
            "prompt": data["prompt"][:500],  # Truncate for storage
            "prompt_tokens": data["prompt_tokens"],
            "temperature": data.get("temperature", 1.0),
            "user_id": data.get("user_id"),
        }
        logging.info(f"LLM_REQUEST: {json.dumps(log_entry)}")

    def log_response(self, request_id: str, data: dict):
        """Log LLM response"""
        log_entry = {
            "request_id": request_id,
            "completion_tokens": data["completion_tokens"],
            "total_tokens": data["total_tokens"],
            "latency_ms": data["latency_ms"],
            "finish_reason": data["finish_reason"],
            "cost_usd": self._calculate_cost(data),
        }
        logging.info(f"LLM_RESPONSE: {json.dumps(log_entry)}")

# Distributed tracing
@tracer.start_as_current_span("llm_call")
def call_llm(prompt: str) -> str:
    span = trace.get_current_span()
    span.set_attribute("prompt.length", len(prompt))

    response = llm.generate(prompt)

    span.set_attribute("response.length", len(response))
    span.set_attribute("tokens.total", response.usage.total_tokens)

    return response.content
```

### 4.3 Evaluation Framework

```python
class LLMEvaluator:
    """
    Evaluate LLM outputs for quality
    """

    def evaluate_response(self,
                          question: str,
                          response: str,
                          ground_truth: str = None) -> dict:
        scores = {}

        # Relevance: Does it answer the question?
        scores["relevance"] = self._score_relevance(question, response)

        # Coherence: Is it well-structured?
        scores["coherence"] = self._score_coherence(response)

        # Groundedness: Is it based on provided context?
        scores["groundedness"] = self._score_groundedness(response)

        # Accuracy: Does it match ground truth?
        if ground_truth:
            scores["accuracy"] = self._score_accuracy(response, ground_truth)

        # Harmfulness: Is it safe?
        scores["safety"] = self._score_safety(response)

        return scores

    def run_benchmark(self, test_cases: list[dict]) -> dict:
        """Run evaluation on test set"""
        results = []
        for case in test_cases:
            response = llm.generate(case["prompt"])
            scores = self.evaluate_response(
                question=case["prompt"],
                response=response,
                ground_truth=case.get("expected")
            )
            results.append(scores)

        return self._aggregate_scores(results)
```

---

## 5. Production Patterns

### 5.1 Caching Strategy

```python
import hashlib
from functools import lru_cache

class LLMCache:
    def __init__(self, redis_client, ttl_seconds=3600):
        self.redis = redis_client
        self.ttl = ttl_seconds

    def _cache_key(self, prompt: str, model: str, **kwargs) -> str:
        """Generate deterministic cache key"""
        content = f"{model}:{prompt}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get_or_generate(self, prompt: str, model: str, **kwargs) -> str:
        key = self._cache_key(prompt, model, **kwargs)

        # Check cache
        cached = self.redis.get(key)
        if cached:
            return cached.decode()

        # Generate
        response = llm.generate(prompt, model=model, **kwargs)

        # Cache (only cache deterministic outputs)
        if kwargs.get("temperature", 1.0) == 0:
            self.redis.setex(key, self.ttl, response)

        return response
```

### 5.2 Rate Limiting & Retry

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.timestamps = []

    def acquire(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()

        # Remove old timestamps
        self.timestamps = [t for t in self.timestamps if now - t < 60]

        if len(self.timestamps) >= self.rpm:
            sleep_time = 60 - (now - self.timestamps[0])
            time.sleep(sleep_time)

        self.timestamps.append(time.time())

# Retry with exponential backoff
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
def call_llm_with_retry(prompt: str) -> str:
    try:
        return llm.generate(prompt)
    except RateLimitError:
        raise  # Will trigger retry
    except APIError as e:
        if e.status_code >= 500:
            raise  # Retry server errors
        raise  # Don't retry client errors
```

### 5.3 Fallback Strategy

```python
class LLMWithFallback:
    def __init__(self, primary: str, fallbacks: list[str]):
        self.primary = primary
        self.fallbacks = fallbacks

    def generate(self, prompt: str, **kwargs) -> str:
        models = [self.primary] + self.fallbacks

        for model in models:
            try:
                return llm.generate(prompt, model=model, **kwargs)
            except (RateLimitError, APIError) as e:
                logging.warning(f"Model {model} failed: {e}")
                continue

        raise AllModelsFailedError("All models exhausted")

# Usage
llm_client = LLMWithFallback(
    primary="gpt-4-turbo",
    fallbacks=["gpt-3.5-turbo", "claude-3-sonnet"]
)
```

---

## Architecture Decision Matrix

| Pattern              | Use When         | Complexity | Cost      |
| :------------------- | :--------------- | :--------- | :-------- |
| **Simple RAG**       | FAQ, docs search | Low        | Low       |
| **Hybrid RAG**       | Mixed queries    | Medium     | Medium    |
| **ReAct Agent**      | Multi-step tasks | Medium     | Medium    |
| **Function Calling** | Structured tools | Low        | Low       |
| **Plan-Execute**     | Complex tasks    | High       | High      |
| **Multi-Agent**      | Research tasks   | Very High  | Very High |

---

## Resources

- [Dify Platform](https://github.com/langgenius/dify)
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

# Prompt Optimization

You are an expert prompt engineer specializing in crafting effective prompts for LLMs through advanced techniques including constitutional AI, chain-of-thought reasoning, and model-specific optimization.

## Context

Transform basic instructions into production-ready prompts. Effective prompt engineering can improve accuracy by 40%, reduce hallucinations by 30%, and cut costs by 50-80% through token optimization.

## Requirements

$ARGUMENTS

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

# AI Assistant Development

You are an AI assistant development expert specializing in creating intelligent conversational interfaces, chatbots, and AI-powered applications. Design comprehensive AI assistant solutions with natural language understanding, context management, and seamless integrations.

## Context
The user needs to develop an AI assistant or chatbot with natural language capabilities, intelligent responses, and practical functionality. Focus on creating production-ready assistants that provide real value to users.

## Requirements
$ARGUMENTS

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

# LangChain/LangGraph Agent Development Expert

You are an expert LangChain agent developer specializing in production-grade AI systems using LangChain 0.1+ and LangGraph.

## Context

Build sophisticated AI agent system for: $ARGUMENTS

## Core Requirements

- Use latest LangChain 0.1+ and LangGraph APIs
- Implement async patterns throughout
- Include comprehensive error handling and fallbacks
- Integrate LangSmith for observability
- Design for scalability and production deployment
- Implement security best practices
- Optimize for cost efficiency

## Essential Architecture

### LangGraph State Management
```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

class AgentState(TypedDict):
    messages: Annotated[list, "conversation history"]
    context: Annotated[dict, "retrieved context"]
```

### Model & Embeddings
- **Primary LLM**: Claude Sonnet 4.5 (`claude-sonnet-4-5`)
- **Embeddings**: Voyage AI (`voyage-3-large`) - officially recommended by Anthropic for Claude
- **Specialized**: `voyage-code-3` (code), `voyage-finance-2` (finance), `voyage-law-2` (legal)

## Agent Types

1. **ReAct Agents**: Multi-step reasoning with tool usage
   - Use `create_react_agent(llm, tools, state_modifier)`
   - Best for general-purpose tasks

2. **Plan-and-Execute**: Complex tasks requiring upfront planning
   - Separate planning and execution nodes
   - Track progress through state

3. **Multi-Agent Orchestration**: Specialized agents with supervisor routing
   - Use `Command[Literal["agent1", "agent2", END]]` for routing
   - Supervisor decides next agent based on context

## Memory Systems

- **Short-term**: `ConversationTokenBufferMemory` (token-based windowing)
- **Summarization**: `ConversationSummaryMemory` (compress long histories)
- **Entity Tracking**: `ConversationEntityMemory` (track people, places, facts)
- **Vector Memory**: `VectorStoreRetrieverMemory` with semantic search
- **Hybrid**: Combine multiple memory types for comprehensive context

## RAG Pipeline

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Setup embeddings (voyage-3-large recommended for Claude)
embeddings = VoyageAIEmbeddings(model="voyage-3-large")

# Vector store with hybrid search
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# Retriever with reranking
base_retriever = vectorstore.as_retriever(
    search_type="hybrid",
    search_kwargs={"k": 20, "alpha": 0.5}
)
```

### Advanced RAG Patterns
- **HyDE**: Generate hypothetical documents for better retrieval
- **RAG Fusion**: Multiple query perspectives for comprehensive results
- **Reranking**: Use Cohere Rerank for relevance optimization

## Tools & Integration

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    query: str = Field(description="Query to process")

async def tool_function(query: str) -> str:
    # Implement with error handling
    try:
        result = await external_call(query)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

tool = StructuredTool.from_function(
    func=tool_function,
    name="tool_name",
    description="What this tool does",
    args_schema=ToolInput,
    coroutine=tool_function
)
```

## Production Deployment

### FastAPI Server with Streaming
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/agent/invoke")
async def invoke_agent(request: AgentRequest):
    if request.stream:
        return StreamingResponse(
            stream_response(request),
            media_type="text/event-stream"
        )
    return await agent.ainvoke({"messages": [...]})
```

### Monitoring & Observability
- **LangSmith**: Trace all agent executions
- **Prometheus**: Track metrics (requests, latency, errors)
- **Structured Logging**: Use `structlog` for consistent logs
- **Health Checks**: Validate LLM, tools, memory, and external services

### Optimization Strategies
- **Caching**: Redis for response caching with TTL
- **Connection Pooling**: Reuse vector DB connections
- **Load Balancing**: Multiple agent workers with round-robin routing
- **Timeout Handling**: Set timeouts on all async operations
- **Retry Logic**: Exponential backoff with max retries

## Testing & Evaluation

```python
from langsmith.evaluation import evaluate

# Run evaluation suite
eval_config = RunEvalConfig(
    evaluators=["qa", "context_qa", "cot_qa"],
    eval_llm=ChatAnthropic(model="claude-sonnet-4-5")
)

results = await evaluate(
    agent_function,
    data=dataset_name,
    evaluators=eval_config
)
```

## Key Patterns

### State Graph Pattern
```python
builder = StateGraph(MessagesState)
builder.add_node("node1", node1_func)
builder.add_node("node2", node2_func)
builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", router, {"a": "node2", "b": END})
builder.add_edge("node2", END)
agent = builder.compile(checkpointer=checkpointer)
```

### Async Pattern
```python
async def process_request(message: str, session_id: str):
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": session_id}}
    )
    return result["messages"][-1].content
```

### Error Handling Pattern
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_with_retry():
    try:
        return await llm.ainvoke(prompt)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        raise
```

## Implementation Checklist

- [ ] Initialize LLM with Claude Sonnet 4.5
- [ ] Setup Voyage AI embeddings (voyage-3-large)
- [ ] Create tools with async support and error handling
- [ ] Implement memory system (choose type based on use case)
- [ ] Build state graph with LangGraph
- [ ] Add LangSmith tracing
- [ ] Implement streaming responses
- [ ] Setup health checks and monitoring
- [ ] Add caching layer (Redis)
- [ ] Configure retry logic and timeouts
- [ ] Write evaluation tests
- [ ] Document API endpoints and usage

## Best Practices

1. **Always use async**: `ainvoke`, `astream`, `aget_relevant_documents`
2. **Handle errors gracefully**: Try/except with fallbacks
3. **Monitor everything**: Trace, log, and metric all operations
4. **Optimize costs**: Cache responses, use token limits, compress memory
5. **Secure secrets**: Environment variables, never hardcode
6. **Test thoroughly**: Unit tests, integration tests, evaluation suites
7. **Document extensively**: API docs, architecture diagrams, runbooks
8. **Version control state**: Use checkpointers for reproducibility

---

Build production-ready, scalable, and observable LangChain agents following these patterns.

---

# LLM Evaluation

Master comprehensive evaluation strategies for LLM applications, from automated metrics to human evaluation and A/B testing.

## Core Evaluation Types

### 1. Automated Metrics
Fast, repeatable, scalable evaluation using computed scores.

**Text Generation:**
- **BLEU**: N-gram overlap (translation)
- **ROUGE**: Recall-oriented (summarization)
- **METEOR**: Semantic similarity
- **BERTScore**: Embedding-based similarity
- **Perplexity**: Language model confidence

**Classification:**
- **Accuracy**: Percentage correct
- **Precision/Recall/F1**: Class-specific performance
- **Confusion Matrix**: Error patterns
- **AUC-ROC**: Ranking quality

**Retrieval (RAG):**
- **MRR**: Mean Reciprocal Rank
- **NDCG**: Normalized Discounted Cumulative Gain
- **Precision@K**: Relevant in top K
- **Recall@K**: Coverage in top K

### 2. Human Evaluation
Manual assessment for quality aspects difficult to automate.

**Dimensions:**
- **Accuracy**: Factual correctness
- **Coherence**: Logical flow
- **Relevance**: Answers the question
- **Fluency**: Natural language quality
- **Safety**: No harmful content
- **Helpfulness**: Useful to the user

### 3. LLM-as-Judge
Use stronger LLMs to evaluate weaker model outputs.

**Approaches:**
- **Pointwise**: Score individual responses
- **Pairwise**: Compare two responses
- **Reference-based**: Compare to gold standard
- **Reference-free**: Judge without ground truth

## Quick Start

```python
from llm_eval import EvaluationSuite, Metric

# Define evaluation suite
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom(name="groundedness", fn=check_groundedness)
])

# Prepare test cases
test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital."
    },
    # ... more test cases
]

# Run evaluation
results = suite.evaluate(
    model=your_model,
    test_cases=test_cases
)

print(f"Overall Accuracy: {results.metrics['accuracy']}")
print(f"BLEU Score: {results.metrics['bleu']}")
```

## Automated Metrics Implementation

### BLEU Score
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference, hypothesis):
    """Calculate BLEU score between reference and hypothesis."""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )

# Usage
bleu = calculate_bleu(
    reference="The cat sat on the mat",
    hypothesis="A cat is sitting on the mat"
)
```

### ROUGE Score
```python
from rouge_score import rouge_scorer

def calculate_rouge(reference, hypothesis):
    """Calculate ROUGE scores."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore
```python
from bert_score import score

def calculate_bertscore(references, hypotheses):
    """Calculate BERTScore using pre-trained BERT."""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### Custom Metrics
```python
def calculate_groundedness(response, context):
    """Check if response is grounded in provided context."""
    # Use NLI model to check entailment
    from transformers import pipeline

    nli = pipeline("text-classification", model="microsoft/deberta-large-mnli")

    result = nli(f"{context} [SEP] {response}")[0]

    # Return confidence that response is entailed by context
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text):
    """Measure toxicity in generated text."""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # Return highest toxicity score

def calculate_factuality(claim, knowledge_base):
    """Verify factual claims against knowledge base."""
    # Implementation depends on your knowledge base
    # Could use retrieval + NLI, or fact-checking API
    pass
```

## LLM-as-Judge Patterns

### Single Output Evaluation
```python
def llm_judge_quality(response, question):
    """Use GPT-5 to judge response quality."""
    prompt = f"""Rate the following response on a scale of 1-10 for:
1. Accuracy (factually correct)
2. Helpfulness (answers the question)
3. Clarity (well-written and understandable)

Question: {question}
Response: {response}

Provide ratings in JSON format:
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<brief explanation>"
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

### Pairwise Comparison
```python
def compare_responses(question, response_a, response_b):
    """Compare two responses using LLM judge."""
    prompt = f"""Compare these two responses to the question and determine which is better.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Which response is better and why? Consider accuracy, helpfulness, and clarity.

Answer with JSON:
{{
  "winner": "A" or "B" or "tie",
  "reasoning": "<explanation>",
  "confidence": <1-10>
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

## Human Evaluation Frameworks

### Annotation Guidelines
```python
class AnnotationTask:
    """Structure for human annotation task."""

    def __init__(self, response, question, context=None):
        self.response = response
        self.question = question
        self.context = context

    def get_annotation_form(self):
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "Is the response factually correct?"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "Does it answer the question?"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "Is it logically consistent?"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### Inter-Rater Agreement
```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(rater1_scores, rater2_scores):
    """Calculate inter-rater agreement."""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    interpretation = {
        kappa < 0: "Poor",
        kappa < 0.2: "Slight",
        kappa < 0.4: "Fair",
        kappa < 0.6: "Moderate",
        kappa < 0.8: "Substantial",
        kappa <= 1.0: "Almost Perfect"
    }

    return {
        "kappa": kappa,
        "interpretation": interpretation[True]
    }
```

## A/B Testing

### Statistical Testing Framework
```python
from scipy import stats
import numpy as np

class ABTest:
    def __init__(self, variant_a_name="A", variant_b_name="B"):
        self.variant_a = {"name": variant_a_name, "scores": []}
        self.variant_b = {"name": variant_b_name, "scores": []}

    def add_result(self, variant, score):
        """Add evaluation result for a variant."""
        if variant == "A":
            self.variant_a["scores"].append(score)
        else:
            self.variant_b["scores"].append(score)

    def analyze(self, alpha=0.05):
        """Perform statistical analysis."""
        a_scores = self.variant_a["scores"]
        b_scores = self.variant_b["scores"]

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self.interpret_cohens_d(cohens_d),
            "winner": "B" if np.mean(b_scores) > np.mean(a_scores) else "A"
        }

    @staticmethod
    def interpret_cohens_d(d):
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

## Regression Testing

### Regression Detection
```python
class RegressionDetector:
    def __init__(self, baseline_results, threshold=0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results):
        """Detect if new results show regression."""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # Calculate relative change
            relative_change = (new_score - baseline_score) / baseline_score

            # Flag if significant decrease
            if relative_change < -self.threshold:
                regressions.append({
                    "metric": metric,
                    "baseline": baseline_score,
                    "current": new_score,
                    "change": relative_change
                })

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }
```

## Benchmarking

### Running Benchmarks
```python
class BenchmarkRunner:
    def __init__(self, benchmark_dataset):
        self.dataset = benchmark_dataset

    def run_benchmark(self, model, metrics):
        """Run model on benchmark and calculate metrics."""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # Generate prediction
            prediction = model.predict(example["input"])

            # Calculate each metric
            for metric in metrics:
                score = metric.calculate(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # Aggregate results
        return {
            metric: {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": min(scores),
                "max": max(scores)
            }
            for metric, scores in results.items()
        }
```

## Resources

- **references/metrics.md**: Comprehensive metric guide
- **references/human-evaluation.md**: Annotation best practices
- **references/benchmarking.md**: Standard benchmarks
- **references/a-b-testing.md**: Statistical testing guide
- **references/regression-testing.md**: CI/CD integration
- **assets/evaluation-framework.py**: Complete evaluation harness
- **assets/benchmark-dataset.jsonl**: Example datasets
- **scripts/evaluate-model.py**: Automated evaluation runner

## Best Practices

1. **Multiple Metrics**: Use diverse metrics for comprehensive view
2. **Representative Data**: Test on real-world, diverse examples
3. **Baselines**: Always compare against baseline performance
4. **Statistical Rigor**: Use proper statistical tests for comparisons
5. **Continuous Evaluation**: Integrate into CI/CD pipeline
6. **Human Validation**: Combine automated metrics with human judgment
7. **Error Analysis**: Investigate failures to understand weaknesses
8. **Version Control**: Track evaluation results over time

## Common Pitfalls

- **Single Metric Obsession**: Optimizing for one metric at the expense of others
- **Small Sample Size**: Drawing conclusions from too few examples
- **Data Contamination**: Testing on training data
- **Ignoring Variance**: Not accounting for statistical uncertainty
- **Metric Mismatch**: Using metrics not aligned with business goals

---
