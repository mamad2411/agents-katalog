---
name: token-budget-advisor
description: Token budget management — context window allocation, system prompt slimming, token counting per message, cost estimation, context pruning, cache optimization, multi-session management.
origin: AI Dev Kit
---

# Token Budget Advisor

Manage token budgets across system prompts, conversation history, retrieval context,
and model outputs. Estimate costs, prune context efficiently, and optimize for cache hits.

## When to Use

- Planning a multi-step LLM workflow and need to budget context windows.
- Estimating costs before executing a batch of LLM calls.
- Deciding what context to include vs prune when approaching token limits.
- Optimizing prompts for cache hit rates across sessions.
- Managing multiple concurrent sessions with shared token budgets.
- Designing system prompts that stay within caching constraints.

## Core Concepts

### 1. Context Window Allocation

```python
from dataclasses import dataclass


@dataclass
class TokenBudget:
    """Budget allocation for a single LLM conversation."""
    total_window: int             # e.g., 200_000 for Claude Sonnet 4
    system_prompt: int = 0        # Reserved for system instructions
    conversation_history: int = 0  # Used by message turns
    retrieval_context: int = 0     # Used by retrieved documents
    reserved_for_output: int = 0   # Headroom for the model's response
    available: int = 0             # Remaining tokens

    def __post_init__(self):
        self.available = (
            self.total_window
            - self.system_prompt
            - self.conversation_history
            - self.retrieval_context
            - self.reserved_for_output
        )

    def can_fit(self, tokens: int) -> bool:
        return tokens <= self.available

    def allocate(self, category: str, tokens: int) -> bool:
        """Allocate tokens to a category. Returns False if over budget."""
        if not self.can_fit(tokens):
            return False
        if category == "system_prompt":
            self.system_prompt += tokens
        elif category == "history":
            self.conversation_history += tokens
        elif category == "retrieval":
            self.retrieval_context += tokens
        elif category == "output":
            self.reserved_for_output += tokens
        self.available -= tokens
        return True


# Example: Budget for a code review task
budget = TokenBudget(
    total_window=200_000,
    system_prompt=500,       # System prompt
    retrieval_context=20_000,  # Code files to review
    reserved_for_output=4_000,  # Expected review output
)
# available = 200_000 - 500 - 0 - 20_000 - 4_000 = 175_500
```

### 2. System Prompt Slimming

```python
def slim_system_prompt(prompt: str, target_tokens: int) -> str:
    """Compress a system prompt to fit within a token budget."""
    current_tokens = estimate_tokens(prompt)

    if current_tokens <= target_tokens:
        return prompt

    # Step 1: Remove blank lines and excess whitespace
    slimmed = "\n".join(line.rstrip() for line in prompt.split("\n") if line.strip())
    current_tokens = estimate_tokens(slimmed)

    if current_tokens <= target_tokens:
        return slimmed

    # Step 2: Remove comments and examples (lines starting with # or containing code blocks)
    lines = slimmed.split("\n")
    essential_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("#!"):
            continue  # Skip comments
        if "```" in stripped:
            continue  # Skip code fences
        essential_lines.append(line)

    slimmed = "\n".join(essential_lines)
    current_tokens = estimate_tokens(slimmed)

    if current_tokens <= target_tokens:
        return slimmed

    # Step 3: Hard truncate (last resort)
    words = slimmed.split()
    target_words = int(target_tokens * 0.75)  # Conservative: ~0.75 tokens per word
    return " ".join(words[:target_words]) + "..."
```

### 3. Token Counting Per Message

```python
import tiktoken  # OpenAI's tokenizer (works as approximation for most models)


def get_tokenizer(model: str = "cl100k_base"):
    """Get the appropriate tokenizer for a model."""
    return tiktoken.get_encoding(model)


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Count tokens in a text string."""
    enc = get_tokenizer(model)
    return len(enc.encode(text))


def count_message_tokens(messages: list[dict], model: str = "cl100k_base") -> int:
    """Count tokens across a list of messages."""
    enc = get_tokenizer(model)
    total = 0
    for msg in messages:
        # Each message has overhead: role + content
        total += 4  # Base message overhead
        total += len(enc.encode(msg.get("content", "")))
        total += len(enc.encode(msg.get("role", "")))
        if "name" in msg:
            total += len(enc.encode(msg["name"]))
    return total


# Usage
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Review this file..."},
]
total = count_message_tokens(messages)
print(f"Total tokens: {total}")
```

### 4. Cost Estimation Before Execution

```python
@dataclass
class ModelPricing:
    input_per_million: float
    output_per_million: float
    cache_read_per_million: float = 0
    cache_create_per_million: float = 0


PRICING = {
    "claude-sonnet-4": ModelPricing(3.0, 15.0, 0.30, 3.75),
    "claude-haiku": ModelPricing(0.80, 4.0, 0.08, 1.0),
    "claude-opus": ModelPricing(15.0, 75.0, 1.50, 18.75),
    "gpt-4o": ModelPricing(2.50, 10.0, 0.25, 2.50),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, 0.075, 0.15),
}


def estimate_call_cost(
    input_tokens: int,
    output_tokens: int,
    model: str,
    cache_read: int = 0,
    cache_create: int = 0,
) -> float:
    """Estimate cost for a single LLM call."""
    p = PRICING.get(model)
    if not p:
        raise ValueError(f"Unknown model: {model}")

    non_cached_input = input_tokens - cache_read - cache_create
    input_cost = (non_cached_input * p.input_per_million / 1_000_000)
    cache_read_cost = cache_read * p.cache_read_per_million / 1_000_000
    cache_create_cost = cache_create * p.cache_create_per_million / 1_000_000
    output_cost = output_tokens * p.output_per_million / 1_000_000

    return input_cost + cache_read_cost + cache_create_cost + output_cost


def estimate_workflow_cost(calls: list[dict], model: str) -> float:
    """Estimate total cost for a multi-call workflow."""
    total = 0.0
    for call in calls:
        total += estimate_call_cost(
            input_tokens=call["input_tokens"],
            output_tokens=call.get("output_tokens", 1000),
            model=model,
            cache_read=call.get("cache_read", 0),
            cache_create=call.get("cache_create", 0),
        )
    return total


# Example
workflow = [
    {"input_tokens": 5000, "output_tokens": 500, "cache_create": 2000},
    {"input_tokens": 3000, "output_tokens": 2000, "cache_read": 2000},
    {"input_tokens": 2000, "output_tokens": 3000},
]
cost = estimate_workflow_cost(workflow, "claude-sonnet-4")
print(f"Estimated cost: ${cost:.4f}")
```

### 5. Context Pruning Strategies

```python
def prune_context(
    messages: list[dict],
    max_tokens: int,
    strategy: str = "recent_first",
) -> list[dict]:
    """Prune messages to fit within token budget."""
    current = count_message_tokens(messages)

    if current <= max_tokens:
        return messages

    if strategy == "recent_first":
        # Keep most recent messages, drop oldest first
        pruned = list(messages)
        while count_message_tokens(pruned) > max_tokens and len(pruned) > 1:
            # Remove oldest non-system message
            for i, msg in enumerate(pruned):
                if msg["role"] != "system":
                    pruned.pop(i)
                    break

    elif strategy == "summarize_old":
        # Summarize old messages, keep recent ones
        system_msg = messages[0]
        old_messages = messages[1:-3]
        recent_messages = messages[-3:]

        summary = summarize_conversation(old_messages)
        pruned = [
            system_msg,
            {"role": "system", "content": f"Summary of earlier conversation: {summary}"},
            *recent_messages,
        ]

    elif strategy == "truncate_by_tokens":
        # Remove messages from the middle
        system_msg = messages[0]
        recent = messages[-5:]
        pruned = [system_msg] + recent

    else:
        pruned = messages

    return pruned


def summarize_conversation(messages: list[dict]) -> str:
    """Summarize a list of messages into a compact summary."""
    # Use a cheap model for summarization
    conversation_text = "\n".join(f"{m['role']}: {m['content'][:200]}" for m in messages)
    return f"Conversation covered: {conversation_text[:500]}..."
```

### 6. Cache Hit Optimization

```python
class CacheOptimizer:
    """Optimize prompt sequences for maximum cache hits."""

    def __init__(self):
        self._cache_prefix: str | None = None
        self._cache_prefix_tokens: int = 0

    def set_stable_prefix(self, system_prompt: str, format_rules: str) -> None:
        """Set the stable prefix that will be cached across calls."""
        self._cache_prefix = f"{system_prompt}\n\n{format_rules}"
        self._cache_prefix_tokens = count_tokens(self._cache_prefix)

    def build_cached_call(self, variable_content: str) -> list[dict]:
        """Build a message list that maximizes cache hits."""
        if not self._cache_prefix:
            raise ValueError("Set stable prefix first")

        return [
            {"role": "system", "content": self._cache_prefix},
            {"role": "user", "content": variable_content},
        ]

    def cache_efficiency(self, total_calls: int, cache_hits: int) -> float:
        return cache_hits / total_calls if total_calls > 0 else 0.0

    def report_savings(
        self,
        total_calls: int,
        variable_tokens_per_call: list[int],
        model: str,
    ) -> dict:
        """Report how much caching saves."""
        without_cache = sum(
            estimate_call_cost(self._cache_prefix_tokens + v, 1000, model)
            for v in variable_tokens_per_call
        )
        with_cache = sum(
            estimate_call_cost(
                self._cache_prefix_tokens + v, 1000, model,
                cache_read=self._cache_prefix_tokens,
            )
            for v in variable_tokens_per_call
        )
        return {
            "without_cache": f"${without_cache:.4f}",
            "with_cache": f"${with_cache:.4f}",
            "savings": f"${without_cache - with_cache:.4f}",
            "savings_pct": f"{(1 - with_cache / without_cache) * 100:.1f}%",
        }
```

### 7. Multi-Session Token Management

```python
class MultiSessionBudget:
    """Manage token budgets across concurrent sessions."""

    def __init__(self, global_max_tokens: int, max_sessions: int = 5):
        self.global_max = global_max_tokens
        self.max_sessions = max_sessions
        self.sessions: dict[str, TokenBudget] = {}
        self.per_session_budget = global_max_tokens // max_sessions

    def create_session(self, session_id: str) -> TokenBudget:
        if len(self.sessions) >= self.max_sessions:
            raise RuntimeError(f"Max sessions ({self.max_sessions}) reached")

        budget = TokenBudget(
            total_window=self.per_session_budget,
            system_prompt=300,
            reserved_for_output=2000,
        )
        self.sessions[session_id] = budget
        return budget

    def close_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)

    def global_usage(self) -> dict:
        total_used = sum(
            b.system_prompt + b.conversation_history + b.retrieval_context
            for b in self.sessions.values()
        )
        return {
            "total_budget": self.global_max,
            "total_used": total_used,
            "total_available": self.global_max - total_used,
            "active_sessions": len(self.sessions),
            "utilization_pct": (total_used / self.global_max) * 100,
        }
```

## Anti-Patterns

- **No budget planning** — sending arbitrarily large context and hitting token limits mid-conversation
- **Ignoring cache costs** — not designing prompts for cache reuse wastes 70-90% of potential savings
- **Over-reserving output tokens** — setting max_tokens=8192 when output is usually 500 tokens
- **Not counting tokens per message** — blind to actual usage; always count before sending
- **Pruning system prompts** — system prompts should be stable; prune conversation history instead
- **Single-session thinking** — in multi-agent systems, each agent needs its own budget

## Best Practices

1. **Budget before building** — calculate system + retrieval + history + output before any LLM call.
2. **Slim system prompts to <500 tokens** — for efficient caching and lower per-call cost.
3. **Count tokens per message** — use tiktoken or model-specific tokenizers before every call.
4. **Estimate costs before execution** — especially for batch workflows and multi-agent pipelines.
5. **Prune aggressively at 80% capacity** — summarize old messages, drop middle content, keep recent.
6. **Design for cache hits** — stable system prefix + variable content at the end.
7. **Manage per-session budgets** — in multi-agent systems, divide global budget across sessions.
8. **Use cheap models for counting/summarizing** — don't waste Sonnet/Opus tokens on meta-tasks.
9. **Log token usage per call** — track input, output, cache_read, cache_create for every invocation.
10. **Set conservative output reserves** — estimate expected output length + 20% buffer.

## Related Skills

- `claude-api` — Token counting and cost estimation specific to Claude
- `prompt-optimizer` — Prompt compression to fit within budgets
- `agentic-engineering` — Context window management across agent delegations
- `context-prune` — Session-level context pruning and layer persistence
- `iterative-retrieval` — Progressive context loading to stay within budget
