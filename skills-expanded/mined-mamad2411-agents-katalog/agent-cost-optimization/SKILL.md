---
name: agent-cost-optimization
description: Use when minimizing costs of running AI agents.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [agents, cost, optimization, tokens, caching]
---

# Agent Cost Optimization

Reducing operational costs of AI agent systems.

## Cost Drivers

```
Total Cost = Σ per_step:
    prompt_tokens * input_rate +
    completion_tokens * output_rate +
    tool_call_fixed_cost
```

Key levers:
1. Reduce token usage per step
2. Reduce number of steps
3. Use cheaper models for subtasks
4. Cache repeated operations

## Token Optimization

```python
class TokenOptimizer:
    def __init__(self, max_context_tokens=4000):
        self.max_tokens = max_context_tokens

    def trim_conversation(self, messages: list, max_tokens: int) -> list:
        """Keep system prompt + latest messages, summarize old ones."""
        total = sum(len(m["content"]) for m in messages)
        if total <= max_tokens:
            return messages

        # Keep system prompt and last few messages
        system = [m for m in messages if m["role"] == "system"]
        non_system = [m for m in messages if m["role"] != "system"]

        # Keep last N messages that fit
        budget = max_tokens - sum(len(s["content"]) for s in system)
        kept = []
        for m in reversed(non_system):
            if len(m["content"]) <= budget:
                kept.insert(0, m)
                budget -= len(m["content"])
            else:
                break

        return system + kept

    def compress_tool_results(self, tool_output: str, max_chars=500) -> str:
        """Truncate tool outputs, keeping head and tail."""
        if len(tool_output) <= max_chars:
            return tool_output
        half = max_chars // 2
        return tool_output[:half] + "\n...[truncated]...\n" + tool_output[-half:]
```

## Model Tier Strategy

```python
class ModelRouter:
    def __init__(self):
        self.tiers = {
            "cheap": "gpt-3.5-turbo",     # ~$0.001/1K tokens
            "medium": "gpt-4-turbo",       # ~$0.01/1K tokens
            "expensive": "gpt-4o",         # ~$0.03/1K tokens
        }

    def select_model(self, task: dict) -> str:
        # Simple routing
        if task.get("priority") == "high":
            return self.tiers["expensive"]
        if task.get("complexity") in ["simple", "classification"]:
            return self.tiers["cheap"]
        if task.get("type") == "reasoning":
            return self.tiers["medium"]
        return self.tiers["cheap"]

    def estimate_cost(self, model: str, prompt_tokens: int,
                      completion_tokens: int) -> float:
        rates = {
            self.tiers["cheap"]: {"prompt": 0.001, "completion": 0.002},
            self.tiers["medium"]: {"prompt": 0.01, "completion": 0.03},
            self.tiers["expensive"]: {"prompt": 0.03, "completion": 0.06},
        }
        r = rates.get(model, rates[self.tiers["cheap"]])
        return (prompt_tokens * r["prompt"] + completion_tokens * r["completion"]) / 1000
```

## Caching Strategies

```python
class SimpleCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size

    def get(self, prompt: str) -> str:
        import hashlib
        key = hashlib.md5(prompt.encode()).hexdigest()
        return self.cache.get(key)

    def set(self, prompt: str, response: str):
        import hashlib
        key = hashlib.md5(prompt.encode()).hexdigest()
        if len(self.cache) < self.max_size:
            self.cache[key] = response

class SemanticCache:
    """Cache based on semantic similarity (embeddings)."""
    def __init__(self, threshold=0.95):
        self.entries = []
        self.threshold = threshold
        self.encoder = None  # set externally

    def query(self, prompt: str) -> str:
        emb = self.encoder.encode(prompt)
        for entry in self.entries:
            sim = cosine_similarity([emb], [entry["embedding"]])[0][0]
            if sim >= self.threshold:
                return entry["response"]
        return None

    def store(self, prompt: str, response: str):
        emb = self.encoder.encode(prompt)
        self.entries.append({"embedding": emb, "response": response})
```

## Batch Processing

```python
class BatchProcessor:
    def __init__(self, llm, batch_size=10):
        self.llm = llm
        self.batch_size = batch_size

    def process_batch(self, prompts: list[str]) -> list[str]:
        """Batch independent prompts into one request with chunked responses."""
        batch_prompt = "\n---SEPARATOR---\n".join(
            f"Task {i}: {p}" for i, p in enumerate(prompts)
        )
        system = "Respond with numbered answers matching each task."

        response = self.llm.invoke(f"{system}\n\n{batch_prompt}")

        # Parse numbered responses
        results = []
        for line in response.split("\n"):
            if line.strip() and line[0].isdigit():
                results.append(line.split(":", 1)[1].strip())

        return results[:len(prompts)]
```

## Pitfalls

- Caching fails for novel prompts — monitor cache hit rate
- Semantic cache similarity threshold needs tuning
- Cheaper models are slower and less accurate — measure the tradeoff
- Batching independent prompts increases latency for individual items
- Token counting tools aren't perfectly accurate — over-allocate 10%
