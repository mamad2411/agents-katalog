---
name: local-cloud-hybrid
description: "Decision tree and setup guide for hybrid local model (LM Studio) + Claude API execution on Windows 11. Use local for cheap tasks, Claude for orchestration."
origin: custom
---

# Local-Cloud Hybrid Execution

Route tasks by cost and capability: local model for high-volume cheap work, Claude API for reasoning and orchestration.

---

## 1. Decision Tree

```
Is the task self-contained with no tool use needed?
├── YES → Does it require deep reasoning, planning, or code review?
│         ├── YES → Claude Sonnet 4.6 (orchestration, planning, multi-step reasoning)
│         │         or Claude Opus 4.7 (architecture, security, deep research)
│         └── NO  → Is network/external API access needed?
│                   ├── YES → Claude Haiku 4.5 (cheap, has tool access)
│                   └── NO  → Local model via LM Studio ($0 API cost)
└── NO  → Multi-step orchestration? → Claude Sonnet 4.6
```

### Quick reference

| Task type | Model |
|-----------|-------|
| Simple codegen, formatting, data transforms | LM Studio local |
| Batch labeling, boilerplate generation | LM Studio local |
| Lint fixes, test stubs, docstring generation | LM Studio local |
| Anything needing web/file tools, simple logic | Haiku 4.5 |
| Orchestration, planning, multi-file reasoning | Sonnet 4.6 |
| Code review with context | Sonnet 4.6 |
| Architecture decisions | Opus 4.7 |
| Security review, deep research | Opus 4.7 |

---

## 2. Windows 11 Setup: LM Studio → OpenAI-Compatible Endpoint

### Install LM Studio

1. Download from https://lmstudio.ai (Windows installer)
2. Install and launch

### Recommended models

| Model | Use case | VRAM |
|-------|----------|------|
| DeepSeek-R1 7B (Q4) | Coding, reasoning | 6 GB |
| Gemma 3 4B (Q4) | General text, transforms | 4 GB |
| Phi-4 Mini | Ultra-fast, simple tasks | 3 GB |

Download via LM Studio's model browser (search by name).

### Start local server

1. In LM Studio: `Local Server` tab → Select model → `Start Server`
2. Default endpoint: `http://localhost:1234/v1`
3. OpenAI-compatible — no auth token required locally

### Configure in Claude Code

Add to `~/.claude/settings.json` under `env`:

```json
{
  "env": {
    "LM_STUDIO_URL": "http://localhost:1234/v1",
    "LM_STUDIO_MODEL": "deepseek-r1-distill-qwen-7b"
  }
}
```

Or set per-session:

```powershell
$env:LM_STUDIO_URL = "http://localhost:1234/v1"
$env:LM_STUDIO_MODEL = "deepseek-r1-distill-qwen-7b"
```

---

## 3. Dual-Terminal Pattern

**Terminal 1 — Orchestrator (Sonnet 4.6)**
- Runs Claude Code CLI
- Stays under 50% context window
- Plans, delegates, reads results

**Terminal 2 — Worker (local model or Haiku)**
- Executes isolated, bounded tasks
- Reads task spec from file
- Writes output to file

### Example orchestrator session

```
# Terminal 1 (Claude Code — Sonnet 4.6)
claude
# You are the orchestrator. Delegate heavy-volume or simple tasks.
```

```
# Terminal 2 (local model — headless)
# Call LM Studio directly via curl or python script
```

---

## 4. Cost Math

| Model | Cost per 1M tokens | Use for |
|-------|--------------------|---------|
| LM Studio local | $0 (electricity ~$0.001/hr) | All high-volume simple tasks |
| Claude Haiku 4.5 | ~$0.25 input / $1.25 output | Simple tasks needing tools |
| Claude Sonnet 4.6 | ~$3 input / $15 output | Orchestration, planning |
| Claude Opus 4.7 | ~$15 input / $75 output | Architecture only |

### Savings strategy

- 10,000 test stubs via local model = $0 vs ~$15 with Sonnet
- Use local for any task that passes this gate: "Could a 7B model do this correctly 90% of the time?"
- Batch all simple tasks, run local overnight if needed

---

## 5. File Handoff Pattern (Zero Extra Tokens)

The orchestrator writes specs to disk; workers read and write files. No token overhead for inter-agent communication.

### Basic handoff

```bash
# Orchestrator writes task spec
cat > .task-context.md << 'EOF'
Task: Generate unit tests for the function in auth.ts lines 45-80.
Output format: Jest test file, TypeScript.
Write output to .task-result.md.
EOF

# Worker executes (headless Claude Haiku — cheap, has file tools)
claude -p --model claude-haiku-4-5 "Read .task-context.md. Execute the task exactly. Write output to .task-result.md."

# Orchestrator reads result
cat .task-result.md

# Cleanup
rm .task-context.md .task-result.md
```

### Local model handoff (via curl)

```bash
# Write task spec
cat > .task-context.md << 'EOF'
Transform the JSON in input.json: flatten nested objects, snake_case keys.
Write result to output.json.
EOF

# Call LM Studio directly
curl -s http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$LM_STUDIO_MODEL\",
    \"messages\": [{
      \"role\": \"user\",
      \"content\": \"$(cat .task-context.md)\n\nInput:\n$(cat input.json)\"
    }],
    \"temperature\": 0
  }" | jq -r '.choices[0].message.content' > output.json

rm .task-context.md
```

### Python worker script (reusable)

```python
# local_worker.py — call from orchestrator
import os, sys, json, httpx

LMSTUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
MODEL = os.getenv("LM_STUDIO_MODEL", "deepseek-r1-distill-qwen-7b")

def run_local(prompt: str) -> str:
    resp = httpx.post(
        f"{LMSTUDIO_URL}/chat/completions",
        json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0},
        timeout=120,
    )
    return resp.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    task_file = sys.argv[1]
    result_file = sys.argv[2]
    prompt = open(task_file).read()
    result = run_local(prompt)
    open(result_file, "w").write(result)
```

Usage:
```bash
python local_worker.py .task-context.md .task-result.md
```

---

## 6. Context Budget Rules

- Orchestrator (Sonnet): never exceed 50% context. Summarize and compact at 40%.
- Worker tasks: each must be self-contained — no shared context with orchestrator.
- Task specs: keep under 2,000 tokens. If larger, split the task.
- Results: worker writes to file; orchestrator reads only the result, not tool traces.

### When to switch models mid-session

| Signal | Action |
|--------|--------|
| Orchestrator at 40% context | Compact (`/compact`) before next delegation |
| Worker returning low-quality output | Promote task to Haiku or Sonnet |
| Task requires tool use (web, files) | Never use local model; use Haiku minimum |
| Cost spike detected | Audit which tasks are hitting Sonnet unnecessarily |
