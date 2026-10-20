# Agence: LLM Integration Instructions

**LLM-agnostic guidelines for integrating any Large Language Model with Agence.**

*For Claude-specific configuration, see [CLAUDE.md](CLAUDE.md).*

---

## Reasoning & Transparency (Always Active)

**Always show reasoning for non-trivial actions.** Format:

```
> REASONING: <1-3 sentences on what you're doing and why>
> RISK: <if any — what could go wrong>
> DECISION: <what you chose and why over alternatives>
```

Rules:
- Show reasoning BEFORE file edits, git ops, or multi-step plans
- For pure display commands (^help, ^symbols): skip reasoning header
- For bug fixes: state what the bug IS before showing the fix
- For architecture decisions: show alternatives considered + rejection reason
- Keep it tight — reasoning is a tool, not a diary
- If unsure: say so explicitly ("I'm not certain whether X or Y — choosing X because...")
- NEVER show reasoning for simple factual answers or one-liner responses

---

## Overview

Agence is designed to work with any LLM backend:
- **OpenAI**: GPT-4, GPT-4o
- **Anthropic**: Claude 3.x family
- **Open Source**: Qwen, Llama, Mistral (via Ollama locally)
- **Other Providers**: Custom adapters welcome

---

## LLM Abstraction Layer

The `llm_provider` module abstracts away provider-specific details:

```
Agence Core
    ↓
llm_provider.rs / llm_provider.py
    ↓
┌───────────┬──────────────┬──────────────┬─────────────┐
│ Anthropic │   OpenAI     │   Ollama     │ Custom API  │
│  Adapter  │  Adapter     │  (Local)     │  Adapter    │
└───────────┴──────────────┴──────────────┴─────────────┘
```

### Provider Interface

Every LLM provider must implement:

```python
class LLMProvider:
    def __init__(self, config: Dict):
        # Initialize with API key, endpoint, model name, etc.
        pass
    
    def chat_completion(self, 
        messages: List[Dict], 
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        # Return LLM response
        pass
    
    def get_usage(self) -> Dict:
        # Return {"input_tokens": N, "output_tokens": M}
        pass
    
    def supports_vision(self) -> bool:
        # True if model can process images
        pass
    
    def supports_tool_use(self) -> bool:
        # True if model can call tools
        pass
```

---

## Configuration

### Environment Variables

```bash
# LLM Provider selection
export AGENCE_LLM_PROVIDER="anthropic"  # or: openai, ollama, custom

# Provider-specific (Anthropic example)
export ANTHROPIC_API_KEY="sk-ant-..."

# Common settings
export AGENCE_LLM_MODEL="claude-3-5-sonnet"
export AGENCE_LLM_TEMPERATURE=0.7
export AGENCE_LLM_MAX_TOKENS=4096

# Optional: use local Ollama instead
export AGENCE_LLM_PROVIDER="ollama"
export OLLAMA_ENDPOINT="http://localhost:11434"
export AGENCE_LLM_MODEL="qwen:7b"
```

### Config File

```yaml
# ~/.agence/config.yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet"
  temperature: 0.7
  max_tokens: 4096
  timeout_seconds: 60
  retry:
    max_attempts: 3
    backoff_multiplier: 2.0
  budget:
    daily_tokens_limit: 2000000
    alert_threshold_percent: 80

providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    endpoint: "https://api.anthropic.com"
  
  openai:
    api_key: "${OPENAI_API_KEY}"
    endpoint: "https://api.openai.com/v1"
    organization: "${OPENAI_ORG_ID}"
  
  ollama:
    endpoint: "http://localhost:11434"
    models:
      - "qwen:7b"
      - "llama2:7b"
```

---

## Prompt Engineering

### Universal System Prompt Pattern

Every LLM works better with structured prompts:

```
[ROLE]
You are Agence, an agentic engineering assistant.

[TASK]
{Specific task description}

[CONSTRAINTS & GUARDRAILS]
1. You can ONLY WRITE to: {parent_repo}
2. You can READ from: {allowed_repos}
3. Action audit: All actions logged with timestamp, user, outcome
4. Validation: Explain before executing destructive operations
5. Knowledge: Capture learnings to shared knowledge base

[INPUT FORMAT]
{Current context, user request, relevant knowledge}

[OUTPUT FORMAT]
1. **Summary**: What you understood
2. **Plan**: Steps you'll take
3. **Execution**: What you're doing
4. **Results**: Outcome
5. **Learning**: Captured for knowledge base

[EXAMPLES]
{1-2 examples of desired behavior}
```

### Context Injection

Always provide the LLM with:
- **Current git state**: current branch, uncommitted changes
- **Organization/project context**: current org, project, repo
- **Relevant knowledge**: RAG-retrieved similar problems & solutions
- **User constraints**: budget, security, timeline

---

## Model Selection & Routing

### Decision Matrix

```
Task Type              | Recommended Model    | Rationale
───────────────────────┼──────────────────────┼──────────────────────
Chat / General Q&A     | Fast/Standard Model  | Low latency preferred
Code Generation        | Powerful Model       | Quality > speed
Code Review            | Powerful Model       | Needs nuance
Infrastructure Plan    | Powerful Model       | High stakes
Quick Lookup           | Fast Model           | Cost/speed efficiency
Summarization          | Fast Model           | Simple task
Terraform Refactor     | Powerful Model       | Complex analysis
PR Review              | Powerful Model       | Context matters
```

### Model Fallback Chain

If primary model fails:

```bash
Primary:   claude-3-5-sonnet
Fallback1: gpt-4o
Fallback2: qwen-max (via Ollama)
Fallback3: Local llama2:7b
```

Configure via:
```yaml
fallback_chain:
  - model: "claude-3-5-sonnet"
    provider: "anthropic"
  - model: "gpt-4o"
    provider: "openai"
  - model: "qwen:72b"
    provider: "ollama"
```

---

## API Integration Patterns

### Request Structure

Every LLM call follows:

```python
response = llm_provider.chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ],
    temperature=0.7,
    max_tokens=4096
)
```

### Error Handling

```python
try:
    response = llm_provider.chat_completion(...)
except RateLimitError:
    # Implement exponential backoff + alert
    log_error("Rate limited, retrying...")
    sleep_and_retry()

except AuthenticationError:
    # Check credentials, exit clearly
    log_error("Invalid API key for provider")
    sys.exit(1)

except TimeoutError:
    # Switch to faster model or local Ollama
    log_warning("Timeout, trying fallback model")
    fallback_provider.chat_completion(...)

except ProviderDownError:
    # Use next in fallback chain
    log_warning("Provider down, using fallback")
    next_provider.chat_completion(...)
```

### Token Accounting

```python
# Track all token usage
def log_api_call(provider, model, input_tokens, output_tokens):
    total = input_tokens + output_tokens
    
    # Log to file
    with open("~/.agence/logs/llm-usage.log", "a") as f:
        f.write(f"{timestamp} | {provider} | {model} | {total} tokens\n")
    
    # Check budget
    daily_total = sum_tokens_today()
    if daily_total > DAILY_BUDGET * 0.8:
        alert("Approaching daily token budget")
```

---

## Tool/Function Calling

### Standard Tools Available to LLM

Agence exposes tools that LLMs can call:

```json
{
  "tools": [
    {
      "name": "execute_command",
      "description": "Run a shell command in the parent repo",
      "parameters": {
        "command": "string (e.g., 'git branch')",
        "timeout_seconds": "number",
        "validate": "boolean (check first)"
      }
    },
    {
      "name": "read_file",
      "description": "Read a file from the repo",
      "parameters": {
        "path": "string (relative to repo root)",
        "lines": "optional [start, end]"
      }
    },
    {
      "name": "write_file",
      "description": "Write or overwrite a file",
      "parameters": {
        "path": "string (relative to repo root)",
        "content": "string (file contents)",
        "mode": "create|append|replace"
      }
    },
    {
      "name": "query_knowledge",
      "description": "Search the RAG knowledge base",
      "parameters": {
        "query": "string (natural language)",
        "limit": "number (how many results)",
        "scope": "shared|private|local"
      }
    }
  ]
}
```

### Tool Use Response Handling

```python
def handle_tool_call(response):
    if response.has_tool_calls():
        for tool_call in response.tool_calls:
            result = route_tool(tool_call.name, tool_call.params)
            # Send result back to LLM for continuation
            continue_conversation(tool_call.id, result)
    else:
        return response.text
```

---

## Safety & Guardrails

### Pre-Execution Validation

Before ANY write/dangerous operation:

```python
def validate_action(action):
    # Check 1: Can write to this repo?
    if not can_write_to(action.repo):
        raise PermissionError(f"Cannot write to {action.repo}")
    
    # Check 2: Is this a known pattern?
    if not is_known_pattern(action):
        require_human_approval(action)
    
    # Check 3: Does it exceed limits?
    if action.estimated_cost > COST_THRESHOLD:
        require_human_approval(action)
    
    # Check 4: Is it destructive?
    if is_destructive(action):
        require_human_approval(action, warning=True)
    
    return True
```

### Audit Logging

Every LLM action logged:

```json
{
  "timestamp": "2026-03-04T12:30:45Z",
  "actor": "agence-instance-01",
  "request": "Create a Terraform module for VPC",
  "llm_provider": "anthropic",
  "llm_model": "claude-3-5-sonnet",
  "response_time_ms": 2341,
  "tokens_used": {
    "input": 1234,
    "output": 876
  },
  "action_taken": "Created file: terraform/modules/vpc/main.tf",
  "status": "success",
  "knowledge_captured": "vpc-module-design-pattern"
}
```

---

## Testing

### Testing Different LLMs

```bash
# Test with primary model
agence test llm --model "claude-3-5-sonnet"

# Test with fallback
agence test llm --model "gpt-4o"

# Test with local Ollama
agence test llm --model "qwen:7b" --endpoint "http://localhost:11434"

# Benchmark all chains
agence test llm --benchmark --all-fallbacks
```

### Cost & Performance Tracking

```bash
# Show today's usage
agence llm usage --today

# Show monthly spend
agence llm usage --month

# Compare models
agence llm compare --models "claude-3-5-sonnet,gpt-4o,qwen:7b"
```

---

## Integration Checklist

- [ ] Environment variables configured (API keys, etc.)
- [ ] Config file (`~/.agence/config.yaml`) created
- [ ] LLM provider adapter implemented
- [ ] Error handling & retry logic implemented
- [ ] Token usage tracking in place
- [ ] Audit logging configured
- [ ] Tool/function definitions loaded
- [ ] Safety validation gates working
- [ ] Fallback chain tested
- [ ] Cost alerts configured
- [ ] Documentation updated for your LLM choice

---

## Provider-Specific Guides

- **Anthropic Claude**: See [CLAUDE.md](CLAUDE.md)
- **OpenAI GPT**: See `OPENAI.md` (TBD)
- **Local Ollama**: See `OLLAMA.md` (TBD)
- **Custom Provider**: See `CUSTOM_PROVIDER.md` (TBD)

---

*Last updated: 2026-03-04*
