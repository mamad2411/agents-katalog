---
name: anthropic-prompt-caching-ops
description: >
  Operate Anthropic prompt caching for owned apps: cache breakpoints, prefix stability,
  TTL/cost trade-offs, metrics, and security notes (what gets cached, multi-tenant isolation).
  Use when reducing input token cost/latency for long system prompts or tools — not for
  caching secrets across tenants or reverse-engineering Anthropic’s service.
---

# Anthropic Prompt Caching Ops

## Scope And Authorization

- **In scope:** Applications using Anthropic APIs under your organization’s account.
- **Out of scope:** Sharing API keys; attempting to read other tenants’ cached prompts.
- Cached prefixes may include proprietary prompts — treat logs and traces carefully.
- Pair with `llm-prompt-injection` for untrusted content and `code-quality-standards`.

## When To Use

- Long static system prompts, tool schemas, or large context preambles repeated across requests.
- Cost/latency optimization with Anthropic prompt caching features.
- Debugging cache misses (prefix changed, ordering, breakpoints).
- Multi-tenant SaaS design: ensure no cross-tenant cache contamination of sensitive prefixes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Prompt/tool injection testing | `llm-prompt-injection` |
| Broader AI/ML system security | `ai-ml-security` |
| Generic HTTP caching CDN | `caching-strategies` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Operational meaning |
| --- | --- |
| Cacheable prefix | Leading content marked for cache (API-version specific) |
| Breakpoint / cache_control | Where cacheable blocks end |
| Hit vs miss | Metrics: cached token reads vs writes |
| Stability | Byte-stable prefix → higher hit rate |
| TTL | Provider-defined cache lifetime; design for expiry |
| Min size | Minimum tokens for caching to apply (see current docs) |

**Note:** Exact request fields evolve — verify current Anthropic docs for your API version.

## Workflow

### 1. Confirm goals and success criteria

1. Record model, avg prompt size, QPS, cost baseline.
2. Success: measurable drop in billed input tokens / latency; hit rate above target; no secrets improperly shared across users.
3. Identify static vs dynamic prompt sections.

### 2. Structure prompts for caching

```text
[STATIC: system policy + tool schemas + large docs]  --> cache breakpoint
[DYNAMIC: user message + retrieved chunks + session]
```

1. Put **stable** content first.
2. Keep per-user secrets **after** the breakpoint (not in cached prefix).
3. Avoid timestamps/random IDs in the cached region.

### 3. Implement API usage (illustrative)

```python
# Pseudocode — field names per current Anthropic SDK
messages = [
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": STATIC_PREFIX,
        "cache_control": {"type": "ephemeral"},  # example marker
      },
      {"type": "text", "text": dynamic_user_content},
    ],
  }
]
client.messages.create(model=MODEL, messages=messages, max_tokens=...)
```

1. Centralize STATIC_PREFIX construction to one module to prevent accidental drift.
2. Version your prefix (`PROMPT_V=3`) and bump intentionally.

### 4. Measure cost and hits

```bash
# From API response usage fields (names vary):
# - cache_creation_input_tokens
# - cache_read_input_tokens
# - input_tokens
```

| Metric | Alert idea |
| --- | --- |
| cache_read / input ratio | Drop → prefix churn |
| cache_creation spikes | Deploy changed static prompt |
| $/1k requests | Budget regression |

### 5. Multi-tenant security

| Risk | Control |
| --- | --- |
| Tenant A data in cached prefix | Never put tenant-specific data before breakpoint |
| Prompt injection in cached tools | Still validate tools; caching ≠ isolation from injection |
| Log leakage | Redact prefixes in debug logs |
| Key sprawl | Separate API keys per env |

### 6. Operational practices

1. Feature-flag caching to compare A/B cost.
2. On deploy of static prefix, expect creation cost blip then savings.
3. Document max prefix size and provider limits.
4. Combine with rate limits and retry/backoff (`retry-backoff-patterns`).

### 7. Verify

```bash
# Integration test: two sequential calls with identical prefix
# Assert second call shows cache read tokens > 0 (in staging)
# Assert tenant B dynamic section cannot read tenant A data
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Prefix | Stable tools+policy | Per-request timestamp in prefix |
| Secrets | User API keys after breakpoint | Customer secrets in cached system block |
| Metrics | Track hit rate | Assume caching always on |
| Change mgmt | Versioned static prompt | Silent string edits all day |

## Output Checklist

- [ ] Static vs dynamic split documented
- [ ] Cache markers applied per current API
- [ ] Metrics for hit/create tokens dashboards
- [ ] Multi-tenant prefix hygiene reviewed
- [ ] Cost A/B or before/after recorded
- [ ] Logging redaction for prompts
- [ ] Feature flag / rollback path
- [ ] `code-quality-standards` applied

## Rules

- Use only on your Anthropic-backed apps with valid keys.
- Do not place tenant secrets in cacheable prefixes.
- Caching optimizes cost/latency; it does not replace authz or injection defenses.
- Follow current vendor docs for field names and TTLs.
- Redact prompts containing PII from tickets.
