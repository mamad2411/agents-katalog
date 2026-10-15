---
name: regtrace
description: >
  LLM evaluation CLI for measuring output quality across Factuality, Format, Tone, and Regression.
  Use this skill whenever a user mentions regtrace, golden sets, LLM evaluation, model regression,
  quality gates, CI/CD evaluation pipelines, or asks how to test/compare LLM outputs. Also trigger
  for tasks like: setting up a new regtrace project, writing test cases for a prompt, debugging a
  failing evaluation, pinning a regression baseline, switching judge providers, integrating regtrace
  into CI, running evaluations, understanding scores, formatting output, generating test outputs,
  troubleshooting API keys, configuring metrics, or managing run history.

  IMPORTANT: Also trigger this skill when the user runs `/regtrace`, `/regtrace init`, or `/regtrace run`
  as a slash command in any agent harness (OpenCode, Claude Code, Cursor, Zed, Aider, etc.), or when
  they ask Claude to "scan this project for LLM calls", "generate golden sets for my prompts", "set up
  eval coverage for this codebase", or anything implying they want regtrace bootstrapped from an
  existing project. When in doubt, use this skill — it covers the full regtrace workflow from install
  to production.
---

# Regtrace

Regtrace evaluates LLM outputs across four dimensions — **Factuality**, **Format**, **Tone**, and **Regression** — using golden sets (YAML test cases) and a configurable LLM judge.

---

## Agent harness integration (`/regtrace init`)

When a user types `/regtrace init` (or similar) inside an agent harness like OpenCode, Claude Code, Cursor, or Zed, the expected behavior is:

1. **Scan the current project directory** for LLM-touching code
2. **Infer what needs test coverage** from found prompts, chains, tools, and routes
3. **Generate golden sets** pre-populated with realistic test cases
4. **Scaffold `regtrace.config.yaml`** wired to those golden sets
5. **Optionally run `--dry-run`** to validate everything before spending tokens

### Step 1 — Project scan

Recursively inspect the project for LLM usage signals. Look for:

| Signal | Where to look |
|--------|--------------|
| Raw prompt strings | `system_prompt`, `user_prompt`, template literals with role arrays |
| LLM client calls | `openai.chat.completions.create`, `anthropic.messages.create`, `genai.generate`, `ollama.chat`, LangChain `chain.invoke`, LlamaIndex queries |
| Tool/function definitions | `tools: [...]` arrays, `@tool` decorators, function schemas |
| RAG patterns | Vector store queries, `retriever.get_relevant_documents`, similarity search calls |
| API routes that proxy LLM | FastAPI/Express routes with LLM calls inside |
| Config files | `.env`, `config.yaml`, `prompts/`, `chains/`, `agents/` directories |

Common file patterns to scan: `**/*.py`, `**/*.ts`, `**/*.js`, `**/*.mjs` — skip `node_modules`, `__pycache__`, `.git`, `dist`, `build`.

### Step 2 — Classify findings

Group each finding into a test case shape:

| Finding type | interaction_type | Suggested metrics |
|-------------|-----------------|-------------------|
| Simple Q&A prompt | `single_turn` | `factuality, format` |
| System prompt + user turn | `single_turn` | `factuality, format, tone` |
| Tool-calling agent | `single_turn` | `factuality, format` |
| RAG chain with retriever | `rag` | `factuality, format` |
| Multi-step chain | `single_turn` | `factuality, tone` |
| Summarization prompt | `single_turn` | `factuality, format` |
| Classification/routing prompt | `single_turn` | `factuality, format` |

### Step 3 — Generate golden sets

For each classified finding, create a golden set file at `golden-sets/<name>.yaml`.

**Naming convention:** `golden-sets/<feature-or-route-name>.yaml`
Examples: `golden-sets/chat-api.yaml`, `golden-sets/rag-docs.yaml`, `golden-sets/agent-tools.yaml`

Generate 3–5 representative test cases per golden set:
- Cover the happy path
- Cover an edge case (empty input, ambiguous query, missing context)
- Cover a failure mode the prompt is known to struggle with (if inferable from code)

Leave `actual_output: null` — the user will fill these with `regtrace run --generate`.

**Example output for a simple chat route:**

```yaml
name: chat-api
version: "1.0.0"
description: "Auto-generated from src/routes/chat.ts — single-turn chat endpoint"
interaction_type: single_turn
tags: [generated, chat]
author: regtrace-init
created_at: "2025-06-05"
updated_at: "2025-06-05"
test_cases:
  - id: chat-001
    description: "Basic factual question"
    input: "What is the capital of France?"
    system_prompt: "You are a helpful assistant."  # extracted from source
    expected_output: "The capital of France is Paris."
    actual_output: null
    metrics: [factuality, format]
    tags: [geography, happy-path]
    weight: 1.0

  - id: chat-002
    description: "Ambiguous or underspecified input"
    input: "Tell me more."
    system_prompt: "You are a helpful assistant."
    expected_output: "The assistant should ask for clarification or provide a generic helpful response."
    actual_output: null
    metrics: [factuality, format, tone]
    tags: [edge-case]
    weight: 1.0

  - id: chat-003
    description: "Multi-sentence answer expected"
    input: "Explain how photosynthesis works in simple terms."
    system_prompt: "You are a helpful assistant."
    expected_output: "Photosynthesis is the process by which plants convert sunlight, water, and CO2 into glucose and oxygen."
    actual_output: null
    metrics: [factuality, format]
    tags: [explanation]
    weight: 1.0
```

### Step 4 — Scaffold config

Generate `regtrace.config.yaml` with entries for every golden set found:

```yaml
project:
  name: <inferred from package.json / pyproject.toml / directory name>
  version: "1.0"

golden_sets:
  # one entry per generated golden set
  - path: golden-sets/chat-api.yaml
    enabled: true
  - path: golden-sets/rag-docs.yaml
    enabled: true

metrics:
  enabled: [factuality, format, tone, regression]
  default_threshold: 0.7
  factuality:
    mode: lenient
    claim_extraction_depth: shallow
  format:
    sub_checks:
      length: true
      required_fields: true
      forbidden_content: true
    length_tolerance: 0.3
  tone:
    sub_dimensions:
      formality: true
      sentiment: true
      assertiveness: true
  regression:
    baseline_strategy: last_passing
    tolerance: 0.05
    critical_threshold: 0.15

judge:
  primary:
    provider: anthropic
    model: claude-haiku-4-5-20251001
    temperature: 0.1
    max_tokens: 4096
    timeout_ms: 30000
    retry_attempts: 3

quality_gates:
  suite_score_minimum: 0.7
  max_failed_test_cases: 0
  regression_gate: true
```

### Step 5 — Post-init instructions

After scaffolding, tell the user:

```
✓ Scanned project — found N LLM integration(s)
✓ Generated golden sets: golden-sets/chat-api.yaml, ...
✓ Created regtrace.config.yaml

Next steps:
  export ANTHROPIC_API_KEY=sk-ant-...
  regtrace run --dry-run              # validate without spending tokens
  regtrace scaffold --from-file outputs.jsonl --write  # bootstrap from real outputs
  regtrace run --generate             # auto-fill actual_output, then evaluate
  regtrace run                        # evaluate against golden sets
```

---

## Installation

```bash
curl -L -o /usr/local/bin/regtrace https://github.com/decimozs/regtrace/releases/latest/download/regtrace-linux-x64
chmod +x /usr/local/bin/regtrace
regtrace --version
```

macOS Gatekeeper:
```bash
xattr -d com.apple.quarantine ./regtrace
```

---

## Quick start (5 minutes)

```bash
regtrace init                         # scaffold: config, golden set, .env.example, .gitignore
export ANTHROPIC_API_KEY=sk-ant-...   # or set in .env
regtrace run --dry-run                # validate setup without spending tokens
regtrace run --generate               # auto-fill null outputs, then evaluate
regtrace run                          # evaluate against golden set
regtrace list                         # show recent runs
regtrace history --run-id <id>        # inspect a run
```

---

## Config file

Full `regtrace.config.yaml` schema:

```yaml
project:
  name: my-project
  version: "1.0"
golden_sets:
  - path: golden-sets/qa.yaml
    enabled: true
    weight: 1
    store_in_db: true
metrics:
  enabled: [factuality, format, tone, regression]
  default_threshold: 0.7
  factuality:
    mode: strict               # strict or lenient
    claim_extraction_depth: shallow  # shallow (fast) or deep (LLM judge)
    rag_faithfulness_only: false
  format:
    sub_checks:
      length: true
      json_validity: true
      json_schema: true
      markdown_structure: true
      required_fields: true
      forbidden_content: true
      regex_match: true
    length_tolerance: 0.3
    strict_json: false
  tone:
    tone_profile: null
    sub_dimensions:
      formality: true
      sentiment: true
      assertiveness: true
      persona_consistency: true
      verbosity: true
    sub_dimension_weights: null
  regression:
    baseline_strategy: last_passing
    tolerance: 0.05
    metric_tolerances:
      format: 0
      factuality: 0.1
    critical_threshold: 0.15
    exclude_new_test_cases: true
judge:
  primary:
    provider: anthropic        # anthropic | openai | gemini | groq | ollama
    model: claude-haiku-4-5-20251001
    temperature: 0.1
    max_tokens: 4096
    timeout_ms: 30000
    retry_attempts: 3
  fallback:
    provider: openai
    model: gpt-4.1-mini
    temperature: 0.1
    max_tokens: 4096
    timeout_ms: 30000
    retry_attempts: 2
generator:
  provider: anthropic
  model: claude-haiku-4-5-20251001
  temperature: 0.4
  max_tokens: 4096
  timeout_ms: 60000
  retry_attempts: 3
run:
  nfr_gates:
    max_latency_ms: 120000
    max_cost_usd: 1.00
    min_coverage: 0.8

  concurrency: 1
quality_gates:
  suite_score_minimum: 0.7
  metric_score_minimums:
    factuality: 0.8
    format: 0.6
  max_failed_test_cases: 0
  max_low_confidence_ratio: 0.1
  regression_gate: true
output:
  run_history_limit: 50
  default_format: terminal
  color: auto
  ci_mode_auto_detect: true
  report_path: null
```

Ollama with custom endpoint:
```yaml
judge:
  primary:
    provider: ollama
    model: llama3
    local_endpoint: http://192.168.1.100:11434
```

**Retry behavior:** exponential backoff — `min(1000 × 2^attempt + random(500), 30000)`. Primary → fallback on exhaustion. Both fail → heuristic scoring (flagged low confidence).

---

## Golden set format

```yaml
name: my-qa-set
version: "1.0.0"
description: My QA test cases
interaction_type: single_turn    # single_turn or rag
tags: [qa, general]
author: you@example.com
created_at: "2025-01-01"
updated_at: "2025-06-01"
test_cases:
  - id: qa-001
    description: "Capital of France"
    input: "What is the capital of France?"
    system_prompt: null
    expected_output: "The capital of France is Paris."
    actual_output: null
    metrics: [factuality, format]
    tags: [geography]
    weight: 1.0
    thresholds:
      factuality: 0.8
    context: null
```

RAG test case:
```yaml
  - id: rag-001
    input: "How do I authenticate?"
    interaction_type: rag
    expected_output: "Use Bearer token..."
    actual_output: "You need a Bearer token..."
    metrics: [factuality, format]
    context:
      documents:
        - source: "docs/api.md"
          content: "Authentication is performed via Bearer tokens..."
          retrieval_score: 0.95
```

---

## CLI commands

```bash
# Run
regtrace run                              # default terminal output
regtrace run --generate                   # fill null actual_output via LLM
regtrace run --set golden-sets/qa.yaml   # single golden set
regtrace run --format json                # JSON to stdout
regtrace run --format json -o out.json   # JSON to file
regtrace run --format markdown -o out.md
regtrace run --ci                         # CI mode: exit 1 on gate failure
regtrace run --ci --bail                  # stop at first failing suite
regtrace run --dry-run                    # validate without LLM calls
regtrace run --verbose                    # show passing cases too
regtrace run --quiet                      # suppress progress

# History / baselines
regtrace list
regtrace history --run-id run_abc
regtrace history --run-id <a> --diff <b>
regtrace baseline show
regtrace baseline pin <run-id>
regtrace baseline unpin

# Watch mode
regtrace watch                            # re-run on file changes

# DB
regtrace db rebuild
```

---

## Quality gates

| Gate | Default | Description |
|------|---------|-------------|
| `suite_score_minimum` | 0.7 | Aggregate suite score |
| `metric_score_minimums` | — | Per-metric floors (optional) |
| `max_failed_test_cases` | 0 | Max individual failures |
| `max_low_confidence_ratio` | 0.1 | Max low-confidence fraction |
| `regression_gate` | true | Fail on critical regression |
| `nfr_gates` | — | Latency, cost, and coverage thresholds. Exit 1 on breach. |

Exit codes: `0` = passed, `1` = gate failure, `2` = config/schema error.

---

## CI/CD patterns

```yaml
# Minimal
- name: Run LLM quality gates
  run: regtrace run --ci --generate
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

```yaml
# PR comment
- run: regtrace run --ci --generate --format markdown --output report.md
- uses: actions/github-script@v7
  with:
    script: |
      const report = require('fs').readFileSync('report.md', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner, repo: context.repo.repo,
        body: `## Regtrace Evaluation\n\n${report}`
      });
```

> **Do NOT** split `--generate` and `run` into separate steps — the second step sees `null actual_output` and scores 7%.

Cache regression history:
```yaml
- uses: actions/cache@v4
  with:
    path: .regtrace
    key: regtrace-${{ hashFiles('golden-sets/**', 'regtrace.config.yaml') }}
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `anthropic API key not configured` | Missing env var | `export ANTHROPIC_API_KEY=...` |
| Suite Score: 0.0% | All `actual_output: null` | `regtrace run --generate` |
| `No regtrace.config.yaml found` | Missing config | `regtrace init` or `--config path` |
| Schema validation error | Invalid config | Check provider, interaction_type, metric names |
| `ECONNREFUSED localhost:11434` | Ollama not running | `ollama serve` |
| macOS: "cannot be opened" | Gatekeeper | `xattr -d com.apple.quarantine ./regtrace` |
| Low-confidence in CI | Model non-determinism | Raise `max_low_confidence_ratio` |
| CI generate passes, evaluate fails | Split generate + evaluate steps | Merge into `regtrace run --ci --generate` |
| PR comment not posted | Missing permissions | Add `permissions: pull-requests: write` |
