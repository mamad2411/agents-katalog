---
name: llm-integrations
description: Use when integrating LLM providers (OpenAI, DeepSeek, OpenRouter, Anthropic, Google), configuring API keys, optimizing costs, implementing rate limiting, and managing LLM usage across projects. Includes best practices for cost optimization and API management. Based on OpenAI, Anthropic, Google, and other LLM provider official documentation.
license: MIT
---

# LLM Integrations Skill — Provider Configuration & Cost Optimization

## Overview

This skill provides comprehensive guidance for integrating LLM providers (OpenAI, DeepSeek, OpenRouter, Anthropic, Google), configuring API keys, optimizing costs, implementing rate limiting, and managing LLM usage across projects. It includes best practices for cost optimization and API management. Based on OpenAI, Anthropic, Google, and other LLM provider official documentation.

## When to Use

**Use this skill when:**

- Integrating LLM providers (OpenAI, DeepSeek, OpenRouter, Anthropic, Google, Qwen)
- Configuring API keys and authentication for multiple providers
- Optimizing LLM costs across projects
- Implementing rate limiting for API calls
- Managing LLM usage across multiple projects
- Choosing the right model for specific tasks
- Setting up multi-provider fallback strategies
- Implementing cost tracking and monitoring
- Building API key rotation and management
- Creating LLM usage dashboards
- Implementing token counting and budgeting
- Setting up alerting for unusual usage
- Building LLM caching strategies
- Implementing prompt caching where supported
- Managing model versions and upgrades
- Setting up staging vs production API keys
- Implementing LLM performance monitoring
- Building LLM observability with tracing
- Creating LLM security policies
- Managing rate limits across providers

**Do NOT use this skill when:**

- Building stateful workflows with complex state (use **langgraph** skill)
- Designing database schema (use **database-design** skill)
- Creating UI components (use **frontend-design** skill)
- Implementing provider-specific agent features (use **qwen-agent**, **langchain**, or **langgraph** skills)
- Managing agent teams and coordination (use **agent-task-coordinator** skill)
- Building Qwen-specific integrations (use **qwen-agent** skill)
- Implementing LangChain-specific patterns (use **langchain** skill)

**Why avoid:** LLM Integrations is for configuration and management. For actual agent/chain implementation, use domain-specific skills.

## Provider Integration

### OpenAI

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import openai

# Configure API key
openai.api_key = "your-openai-api-key"

# Chat model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=2048,
    api_key="your-openai-api-key"
)

# Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key="your-openai-api-key"
)

# Direct API
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    temperature=0.7,
    max_tokens=2048
)
```

### DeepSeek

```python
from langchain_openai import ChatOpenAI

# DeepSeek API
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=2048,
    openai_api_key="your-deepseek-api-key",
    openai_api_base="https://api.deepseek.com/v1"
)

# Cost-effective alternative to GPT-4
# ~90% cheaper than GPT-4, similar performance
```

### OpenRouter

```python
from langchain_openai import ChatOpenAI

# OpenRouter API
llm = ChatOpenAI(
    model="openrouter/meta-llama/llama-3-70b-instruct:free",
    temperature=0.7,
    max_tokens=2048,
    openai_api_key="your-openrouter-api-key",
    openai_api_base="https://openrouter.ai/api/v1"
)

# Free tier available for some models
# Supports multiple providers (Meta, Mistral, etc.)
```

### Anthropic

```python
from langchain_anthropic import ChatAnthropic

# Anthropic API
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.7,
    max_tokens=2048,
    api_key="your-anthropic-api-key"
)

# Claude models: excellent for reasoning and coding
```

### Google Gemini

```python
from langchain_google_genai import ChatGoogleGenerativeAI

# Google Gemini API
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-pro",
    temperature=0.7,
    max_tokens=2048,
    google_api_key="your-google-api-key"
)

# Gemini Pro: strong multimodal capabilities
```

## Cost Optimization

### Model Selection Matrix

| Task              | Recommended Model          | Cost Estimate   |
| ----------------- | -------------------------- | --------------- |
| Simple queries    | GPT-3.5-turbo / Qwen-Turbo | $0.50/1M tokens |
| General tasks     | GPT-4 / Qwen-Plus          | $30/1M tokens   |
| Complex reasoning | GPT-4o / Qwen-Max          | $125/1M tokens  |
| Coding tasks      | Claude-3-5-Sonnet          | $3/1M tokens    |
| Embeddings        | text-embedding-3-small     | $0.02/1M tokens |

### Cost Tracking

```python
import time

class CostTracker:
    def __init__(self):
        self.total_cost = 0
        self.total_tokens = 0
        self.call_count = 0

    def track_call(self, prompt_tokens: int, completion_tokens: int, model: str):
        """Track API call costs."""
        self.total_tokens += prompt_tokens + completion_tokens
        self.call_count += 1

        # Cost per 1M tokens (approximate)
        costs = {
            "gpt-3.5-turbo": 0.50,
            "gpt-4": 30.00,
            "gpt-4o": 125.00,
            "claude-3-5-sonnet": 3.00,
            "deepseek-chat": 0.14,  # Very cost-effective
            "qwen-turbo": 0.50,
            "qwen-plus": 2.00,
            "qwen-max": 120.00
        }

        cost_per_million = costs.get(model, 10.00)
        cost = (prompt_tokens + completion_tokens) / 1_000_000 * cost_per_million
        self.total_cost += cost

    def get_stats(self):
        """Get cost statistics."""
        return {
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "call_count": self.call_count,
            "avg_cost_per_call": self.total_cost / self.call_count if self.call_count > 0 else 0
        }

# Usage
tracker = CostTracker()

# Track calls
tracker.track_call(prompt_tokens=100, completion_tokens=50, model="gpt-4")
tracker.track_call(prompt_tokens=200, completion_tokens=100, model="deepseek-chat")

stats = tracker.get_stats()
print(f"Total cost: ${stats['total_cost']:.2f}")
print(f"Total tokens: {stats['total_tokens']}")
```

### Cost-Saving Strategies

```python
# ✅ GOOD: Use cost-effective models
def call_llm(prompt: str, task_type: str) -> str:
    """Call LLM with cost-effective model selection."""

    models = {
        "simple": "gpt-3.5-turbo",  # $0.50/1M tokens
        "general": "deepseek-chat",  # $0.14/1M tokens (very cost-effective)
        "complex": "gpt-4o",  # $125/1M tokens
        "coding": "claude-3-5-sonnet",  # $3/1M tokens
        "embedding": "text-embedding-3-small"  # $0.02/1M tokens
    }

    model = models.get(task_type, "deepseek-chat")
    return call_api(prompt, model)
```

### Rate Limiting

```python
import time
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: float = 60.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = Lock()

    def acquire(self):
        """Acquire permission to make a request, waiting if necessary."""
        while True:
            with self.lock:
                current_time = time.time()
                self.requests = [req_time for req_time in self.requests
                               if current_time - req_time < self.time_window]

                if len(self.requests) < self.max_requests:
                    self.requests.append(current_time)
                    return

            # Wait before retrying
            time.sleep(0.1)

# Usage
rate_limiter = RateLimiter(max_requests=10, time_window=60)

def call_llm_with_rate_limit(prompt: str, model: str) -> str:
    """Call LLM with rate limiting."""
    rate_limiter.acquire()
    return call_api(prompt, model)
```

## API Key Management

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
```

### Secret Management

```python
# ✅ GOOD: Use secret management
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name: str) -> str:
    """Get secret from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response["SecretString"]
    except ClientError as e:
        raise Exception(f"Error getting secret: {e}")

# Usage
openai_api_key = get_secret("openai/api_key")
```

### Fallback Strategy

```python
class MultiProviderLLM:
    def __init__(self):
        self.providers = {
            "primary": "openai",
            "fallback": ["deepseek", "openrouter"]
        }
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY")
        }

    def call(self, prompt: str, model: str, provider: str = None) -> str:
        """Call LLM with fallback strategy."""
        providers = [provider] if provider else list(self.providers.values())

        for provider in providers:
            try:
                return self._call_provider(prompt, model, provider)
            except Exception as e:
                print(f"Provider {provider} failed: {e}")
                continue

        raise Exception("All providers failed")

    def _call_provider(self, prompt: str, model: str, provider: str) -> str:
        """Call specific provider."""
        api_key = self.api_keys[provider]

        if provider == "openai":
            return call_openai(prompt, model, api_key)
        elif provider == "deepseek":
            return call_deepseek(prompt, model, api_key)
        elif provider == "openrouter":
            return call_openrouter(prompt, model, api_key)
```

## Best Practices

### 1. Use Appropriate Models

```python
# ✅ GOOD: Appropriate model selection
def call_llm(prompt: str, task_type: str) -> str:
    """Call LLM with appropriate model selection."""

    models = {
        "simple": "gpt-3.5-turbo",
        "general": "deepseek-chat",
        "complex": "gpt-4o",
        "coding": "claude-3-5-sonnet",
        "embedding": "text-embedding-3-small"
    }

    model = models.get(task_type, "deepseek-chat")
    return call_api(prompt, model)
```

### 2. Implement Error Handling

```python
# ✅ GOOD: Error handling
try:
    response = call_api(prompt, model)
except Exception as e:
    logger.error(f"LLM API Error: {e}")
    response = "An error occurred. Please try again."
```

### 3. Use Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_call(prompt: str, model: str) -> str:
    """Cached LLM call."""
    return call_api(prompt, model)

# Usage
result = cached_call("What's 2+2?", "gpt-3.5-turbo")
```

### 4. Monitor Usage

```python
class UsageMonitor:
    def __init__(self):
        self.usage = {}

    def track(self, provider: str, tokens: int, cost: float):
        """Track usage."""
        if provider not in self.usage:
            self.usage[provider] = {"tokens": 0, "cost": 0.0}

        self.usage[provider]["tokens"] += tokens
        self.usage[provider]["cost"] += cost

    def get_report(self):
        """Get usage report."""
        return self.usage

# Usage
monitor = UsageMonitor()
monitor.track("openai", tokens=1000, cost=0.03)
monitor.track("deepseek", tokens=2000, cost=0.00028)

report = monitor.get_report()
```

## Common Anti-Patterns

### ❌ Bad: Hardcoded API Keys

```python
# ❌ BAD: Hardcoded API keys
def call_openai(prompt: str) -> str:
    api_key = "sk-..."  # Hardcoded!
    return openai.ChatCompletion.create(api_key=api_key, ...)
```

**Problems:**

- Security risk
- Difficult to manage
- Hard to rotate keys

### ✅ Good: Environment Variables

```python
# ✅ GOOD: Environment variables
import os

def call_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.ChatCompletion.create(api_key=api_key, ...)
```

### ❌ Bad: No Rate Limiting

```python
# ❌ BAD: No rate limiting
def call_llm(prompt: str) -> str:
    return call_api(prompt, "gpt-4")  # Can hit rate limits
```

### ✅ Good: With Rate Limiting

```python
# ✅ GOOD: With rate limiting
rate_limiter = RateLimiter(max_requests=10, time_window=60)

def call_llm(prompt: str) -> str:
    rate_limiter.acquire()  # Wait if needed
    return call_api(prompt, "gpt-4")
```

### ❌ Bad: No Error Handling

```python
# ❌ BAD: No error handling
response = call_api(prompt, "gpt-4")  # Can crash
result = response.choices[0].text
```

### ✅ Good: With Error Handling

```python
# ✅ GOOD: With error handling
try:
    response = call_api(prompt, "gpt-4")
    result = response.choices[0].text
except Exception as e:
    logger.error(f"API Error: {e}")
    result = "An error occurred. Please try again."
```

## Real-World Impact

**Before this skill:**

- Hardcoded API keys
- No rate limiting
- Poor cost management
- No error handling

**After this skill:**

- Secure API key management
- Rate limiting implemented
- Cost optimization
- Robust error handling

## Cross-References

- **`qwen-agent`** - For Qwen-specific integrations
- **`langchain`** - For LangChain integration
- **`langgraph`** - For stateful workflows

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [DeepSeek API Documentation](https://api-docs.deepseek.com/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
