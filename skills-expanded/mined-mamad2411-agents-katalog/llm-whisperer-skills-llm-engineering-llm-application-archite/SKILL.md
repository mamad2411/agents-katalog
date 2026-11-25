# LLM Application Architecture

## Overview

LLM application architecture encompasses the design patterns, system components, and integration strategies needed to build production-grade applications powered by large language models. Unlike traditional software, LLM applications must account for non-deterministic outputs, variable latency, token economics, and the unique failure modes of generative AI.

A well-architected LLM application separates concerns between prompt management, model interaction, output processing, and business logic. It provides abstractions for model providers, implements robust error handling, and supports observability at every layer. The architecture should be flexible enough to swap models, adjust prompts, and scale components independently.

This skill covers the core architectural patterns for building reliable, maintainable, and scalable LLM applications.

## Key Concepts

- **Provider abstraction** — A unified interface that works across OpenAI, Anthropic, local models, etc.
- **Prompt management** — Version-controlled, templated prompts with variable substitution
- **Middleware pipeline** — Composable layers for logging, caching, rate limiting, and validation
- **Model registry** — Centralized configuration for model endpoints, capabilities, and pricing
- **Orchestration layer** — Coordinates multi-step LLM workflows (chains, agents, graphs)
- **Observability** — Structured logging, tracing, and metrics for every LLM interaction
- **Configuration management** — Environment-specific settings for models, prompts, and behavior
- **Plugin architecture** — Extensible tool and capability integration
- **Separation of concerns** — Business logic independent of model-specific code
- **Testing infrastructure** — Mockable interfaces for unit and integration testing

## Implementation Patterns

### Provider Abstraction Layer

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncIterator

@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    metadata: dict = field(default_factory=dict)

@dataclass
class LLMMessage:
    role: str  # system, user, assistant, tool
    content: str

class LLMProvider(ABC):
    """Abstract base for all LLM providers."""

    @abstractmethod
    async def chat(
        self,
        messages: list[LLMMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        ...

    @abstractmethod
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        **kwargs,
    ) -> AsyncIterator[str]:
        ...

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)

    async def chat(self, messages, model, temperature=0.7, max_tokens=4096, **kwargs):
        import time
        start = time.monotonic()
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        latency = (time.monotonic() - start) * 1000
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            latency_ms=latency,
        )

    async def stream(self, messages, model, **kwargs):
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            stream=True,
            **kwargs,
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

### Middleware Pipeline

```python
from typing import Callable, Any
import time
import logging

logger = logging.getLogger(__name__)

class Middleware:
    """Composable middleware for LLM calls."""

    def __init__(self):
        self._before: list[Callable] = []
        self._after: list[Callable] = []
        self._on_error: list[Callable] = []

    def before(self, fn: Callable) -> "Middleware":
        self._before.append(fn)
        return self

    def after(self, fn: Callable) -> "Middleware":
        self._after.append(fn)
        return self

    def on_error(self, fn: Callable) -> "Middleware":
        self._on_error.append(fn)
        return self

    async def execute(self, call_fn: Callable, *args, **kwargs) -> Any:
        context = {"args": args, "kwargs": kwargs, "start": time.monotonic()}

        for fn in self._before:
            context = await fn(context) if asyncio.iscoroutinefunction(fn) else fn(context)

        try:
            result = await call_fn(*args, **kwargs)
            context["result"] = result
            for fn in self._after:
                context = await fn(context) if asyncio.iscoroutinefunction(fn) else fn(context)
            return context["result"]
        except Exception as e:
            context["error"] = e
            for fn in self._on_error:
                context = await fn(context) if asyncio.iscoroutinefunction(fn) else fn(context)
            raise

# Built-in middleware
def logging_middleware(context: dict) -> dict:
    """Log request details."""
    logger.info(f"LLM call: {context['kwargs'].get('model', 'unknown')}")
    return context

def metrics_middleware(context: dict) -> dict:
    """Record latency metrics."""
    if "result" in context:
        latency = (time.monotonic() - context["start"]) * 1000
        logger.info(f"LLM latency: {latency:.0f}ms")
    return context
```

### Application Bootstrap

```python
from dataclasses import dataclass

@dataclass
class AppConfig:
    openai_api_key: str
    anthropic_api_key: str | None = None
    default_model: str = "gpt-4o"
    cache_ttl: int = 3600
    max_retries: int = 3
    log_level: str = "INFO"

class LLMApplication:
    """Main application container."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.providers: dict[str, LLMProvider] = {}
        self.middleware = Middleware()
        self._setup_providers()
        self._setup_middleware()

    def _setup_providers(self):
        self.providers["openai"] = OpenAIProvider(self.config.openai_api_key)
        if self.config.anthropic_api_key:
            self.providers["anthropic"] = AnthropicProvider(self.config.anthropic_api_key)

    def _setup_middleware(self):
        self.middleware.before(logging_middleware)
        self.middleware.after(metrics_middleware)

    async def chat(self, messages: list[LLMMessage], provider: str = "openai", **kwargs):
        """Primary chat interface."""
        p = self.providers[provider]
        return await self.middleware.execute(p.chat, messages, **kwargs)

    def get_provider(self, name: str) -> LLMProvider:
        return self.providers[name]

# Usage
app = LLMApplication(AppConfig(openai_api_key="sk-..."))
response = await app.chat([LLMMessage("user", "Hello")])
```

## Best Practices

1. **Abstract the model provider** — Never hardcode provider-specific code in business logic
2. **Use dependency injection** — Pass providers and services as arguments, not globals
3. **Version control prompts** — Treat prompts like code with versioning, testing, and review
4. **Implement comprehensive logging** — Log every LLM call with inputs, outputs, tokens, and latency
5. **Design for testability** — Use interfaces and mocks so tests don't require live API calls
6. **Separate prompt logic from application logic** — Prompts should be configurable without code changes
7. **Plan for multi-model support** — Even if using one model today, design for easy model swapping
8. **Use configuration files, not constants** — Externalize model names, temperatures, and system prompts

## Common Pitfalls

- **Tight coupling to a single provider** — Makes migration and fallback impossible
- **Scattered prompt definitions** — Prompts hardcoded across the codebase are impossible to maintain
- **No observability** — Without logging and tracing, debugging production issues is guesswork
- **Missing abstraction layers** — Direct API calls in business logic create unmaintainable code
- **Ignoring non-determinism** — LLM outputs vary; design systems that handle variance gracefully

## References

- LangChain Architecture: docs.langchain.com
- LlamaIndex Design Patterns: docs.llamaindex.ai
- Anthropic Cookbook: github.com/anthropics/anthropic-cookbook
