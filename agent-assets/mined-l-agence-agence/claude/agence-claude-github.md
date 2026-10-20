<!-- AGENCE SKELETON — Canonical source: .agence/.github/CLAUDE.md -->
# Agence: Claude (Anthropic) Integration

**Claude-specific configuration and optimization for Agence.**

*For LLM-agnostic guidelines, see [copilot-instructions.md](copilot-instructions.md).*

---

## Why Claude for Agence

Claude excels at the tasks Agence needs most:
- **Extended reasoning** for architectural decisions
- **Precise instruction following** for command validation and safety
- **Transparent uncertainty** — says "I don't know" instead of hallucinating
- **Long context windows** for multi-file analysis without chunking

---

## Claude-Specific Configuration

### Model Selection

| Use Case | Model | Rationale |
|---|---|---|
| Code generation, refactoring | claude-sonnet-4-20250514 | Best quality/cost ratio for code |
| Architecture, complex reasoning | claude-sonnet-4-20250514 | Deep analysis, long context |
| Quick lookups, simple edits | claude-haiku | Fast, cheap, good enough |
| Critical infrastructure changes | claude-sonnet-4-20250514 | Maximum accuracy for high-stakes |

### Environment Variables

```bash
export AGENCE_LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-..."
export AGENCE_LLM_MODEL="claude-sonnet-4-20250514"
export AGENCE_LLM_TEMPERATURE=0.3
export AGENCE_LLM_MAX_TOKENS=4096
```

### Provider Config

```yaml
providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    endpoint: "https://api.anthropic.com"
    default_model: "claude-sonnet-4-20250514"
    fallback_model: "claude-haiku"
    max_tokens: 4096
    temperature: 0.3
```

---

## Token Cost Optimization

Claude is powerful but priced per token. These strategies keep costs modest:

### 1. Structured System Prompts (Front-Load Context)

Place the most important context first in the system prompt. Claude weighs early tokens more heavily.

```
System prompt order:
1. Role + constraints (short, imperative)
2. Current task context (what matters NOW)
3. Reference material (PRINCIPLES, RULES — load on demand)
```

### 2. Temperature Tuning by Task

| Task | Temperature | Why |
|---|---|---|
| Code generation | 0.2–0.3 | Deterministic, fewer retries |
| Code review | 0.3 | Consistent analysis |
| Creative/brainstorm | 0.7 | Explore alternatives |
| Factual lookup | 0.0 | Exact answers only |

Lower temperature = fewer wasted tokens on hallucinated alternatives.

### 3. Selective Context Loading

Don't load everything every time:

```python
# BAD: Load all context files on every call (expensive)
context = load_all_codex_files()

# GOOD: Load only what the task needs
context = load_context_for_task(task_type)

def load_context_for_task(task_type):
    base = load("PRINCIPLES.md")  # Always loaded (small)
    
    if task_type == "code_review":
        return base + load("RULES.md")
    elif task_type == "architecture":
        return base + load("LAWS.md") + load("RULES.md")
    elif task_type == "fault_analysis":
        return base + load("faults/INDEX.md")
    else:
        return base
```

### 4. Response Format Control

Ask Claude for structured output to avoid verbose prose:

```
Respond with:
1. **Assessment** (1-2 sentences)
2. **Action** (bullet list of steps)
3. **Risk** (if any, one line)

Do NOT explain your reasoning unless asked.
```

### 5. Caching with Prompt Prefixes

Anthropic supports prompt caching. Reuse system prompts across calls:

```python
# Cache the system prompt (saves ~90% on repeated calls)
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=messages
)
```

---

## Claude-Specific Reasoning Patterns

### Extended Thinking for Complex Tasks

For architecture decisions, use Claude's extended thinking:

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8192,
    thinking={
        "type": "enabled",
        "budget_tokens": 4096
    },
    messages=[{"role": "user", "content": complex_query}]
)
```

Use extended thinking for:
- Multi-file refactoring plans
- Architecture trade-off analysis
- Root cause analysis on faults
- Security review

Skip extended thinking for:
- Simple code edits
- File lookups
- Status checks
- Formatting tasks

### Prefill for Consistent Output

Guide Claude's response format by prefilling the assistant turn:

```python
messages = [
    {"role": "user", "content": "Analyze this error..."},
    {"role": "assistant", "content": "**Assessment**: "}
]
```

---

## Safety & Guardrails (Claude-Specific)

### Claude's Natural Strengths

Claude already aligns with Agence principles:
- **Refuses harmful actions** without needing extra guardrails
- **Discloses uncertainty** naturally (Maxim 2: Transparency Over Ego)
- **Follows constraints precisely** when stated clearly

### Reinforcing Agence Safety

Add these to the system prompt for Claude:

```
SAFETY CONSTRAINTS (non-negotiable):
- You can ONLY WRITE to: ${GIT_REPO}
- You can READ from: ${ALLOWED_REPOS}
- NEVER run: git clean, rm -rf, git push --force without explicit confirmation
- On error: STOP, log fault, disclose immediately, wait for instructions
- On uncertainty: ASK, don't guess
```

### Fault Logging Integration

When Claude detects an error in its own output:

```
If you make a mistake:
1. Say "^fault: [description]" immediately
2. Do NOT attempt auto-remediation
3. Wait for human direction
4. Learn: suggest what should be added to RULES.md to prevent recurrence
```

---

## Agence Command Integration

### Commands Claude Should Know

```
^save   — Checkpoint current session state
^fault  — Log an error/mistake with context
^learn  — Extract and store a lesson
^reload — Reload context files
^init   — Initialize Agence in a repo (copies skeleton files)
^commit — Stage + commit with message
^push   — Push to remote
```

### Context Hierarchy (Load Order)

```
1. CLAUDE.md          ← You are here (Claude-specific config)
2. copilot-instructions.md  ← LLM-agnostic guidelines
3. PRINCIPLES.md      ← Philosophical maxims (always load)
4. LAWS.md            ← Hard constraints (load for write ops)
5. RULES.md           ← Best practices (load for code tasks)
6. COMMANDS.md        ← CLI reference (load on demand)
7. faults/INDEX.md    ← Error history (load for fault analysis)
8. lessons/INDEX.md   ← Captured wisdom (load for similar tasks)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|---|---|---|
| Loading all context every call | Wastes tokens, dilutes focus | Load selectively by task type |
| High temperature for code | More hallucinations, more retries | Use 0.2–0.3 for code |
| Long verbose prompts | Token cost, context dilution | Short imperative instructions |
| Auto-fixing mistakes | Cascade failures (Maxim 5) | Pause, disclose, wait |
| Skipping proof of work | Can't verify what happened | Always show command output |
| Retrying failed commands | Compounds errors | Stop, analyze, ask |

---

## Metrics & Monitoring

### Token Budget Alerts

```yaml
budget:
  daily_tokens_limit: 2000000
  alert_at_percent: 80
  hard_stop_at_percent: 95
  
  # Per-task limits (prevent runaway calls)
  max_tokens_per_call: 8192
  max_calls_per_session: 50
```

### Quality Signals

Track these to measure Claude effectiveness:
- **First-attempt success rate**: Did the code work without retry?
- **Fault rate**: How often does Claude trigger ^fault?
- **Token efficiency**: Useful output tokens / total tokens
- **Lesson extraction rate**: How many sessions produce ^learn entries?

---

*Last updated: 2026-03-07*
