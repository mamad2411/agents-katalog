---
name: follow-tool-deepsec
description: Use deepsec end to end — AI security review: init/scan/process/export, matchers, sandboxes, resume
argument-hint: "[command] [--project-id <id>]"
allowed-tools:
  - exec
  - read
  - write
  - edit
  - grep
  - find_file_by_name
related:
  - check-secrets
  - deep-review-codebase
  - follow-tool-security-audit-skill
  - report
---

## Goal

Run deepsec (deepsec.sh — Vercel OSS) for an AI-driven security review of the repo — pipeline: inventory the codebase → fast pattern scan (free) → AI review of flagged files (paid) → findings in a `.deepsec/` workspace that is always resumable

## Scope

Use when a deep AI-agent security audit of the codebase is needed — config/env-level secrets hygiene → `/check-secrets`; general code review → `/deep-review-codebase`; deepsec = the dedicated security pipeline tracking state, matchers, and findings per project; on-demand multi-phase audit inside the coding agent with independently verified `findings.json` → `/follow-tool-security-audit-skill`

- Boundary: deepsec reads source code with an AI agent authenticated to a model provider — run it only on code trusted at that level; untrusted PRs → guarded CI mode or sandboxes

## Execute

### 1. Init

> Goal: set up the workspace and run the first scan

1. `bunx deepsec init` at the repo root — pick the model (per DeepSecBench score/cost) + model access (Vercel AI Gateway default, own API key, or local subscriptions)
2. Creates `.deepsec/` (the only thing added to the repo) → inventory → pattern scan → AI review
3. Headless/CI: `bunx deepsec init --yes --model-profile value --output jsonl` (profiles: `best`/`value`/`budget`); preview: `--plan --output json`
4. Scaffold only: `bunx deepsec init --scaffold-only` → review the `.deepsec/` skeleton before a real run

### 2. Resume And Bound

> Goal: control time/cost and continue from the same point

1. Re-run the same command — finished steps are skipped automatically (after Ctrl-C, a cost limit, or connection loss)
2. Bound with `--max-cost-usd 100 --max-duration 2h` — duration requires a unit (`ms`/`s`/`m`/`h`)
3. Exit code `2` = input needed that headless cannot provide (JSON output explains how to resume); `3` = cost/duration limit reached

### 3. Everyday Commands

> Goal: work inside the `.deepsec/` workspace

```bash
cd .deepsec
bunx deepsec status       # pipeline status
bunx deepsec scan         # fast pattern scan — free, local
bunx deepsec process      # AI review — the paid part
bunx deepsec revalidate   # re-check findings, drop false positives
bunx deepsec export --format md-dir --out ./findings
bunx deepsec report       # quick overview
```

- Multi-repo: `bunx deepsec init-project ../svc --id svc` + `bunx deepsec setup --project-id svc`; pass `--project-id` to the other commands

### 4. Auth Options

> Goal: pick the right credential route

1. **Vercel AI Gateway** (default): Vercel login happens automatically during init
2. **Own key**: `MY_KEY=... bunx deepsec init --agent codex --model-auth direct --ai-provider openai --ai-api-key-env MY_KEY` — deepsec stores only the *name* of the env var, never the key; put it in `.deepsec/.env.local` for later runs
3. **Local subscriptions**: `--model-auth local` when the `claude`/`codex` CLI is already logged in — except `sandbox`, which still requires `AI_GATEWAY_API_KEY`

### 5. Review Artifacts

> Goal: tune finding quality

1. `data/<project>/INFO.md` — the codebase description injected into every AI investigation — making it accurate = better findings
2. `.deepsec/generated-matchers.ts` — scan patterns deepsec generates to cover gaps — review + commit
3. Coverage pause (setup stops because the inventory is incomplete) → fix the matchers and re-run (≤2 repair attempts)

### 6. Sandboxes And Report

> Goal: run isolated / summarize results

- `bunx deepsec sandbox process --project-id my-app --sandboxes 10 --concurrency 4` — isolated Vercel sandboxes; the host keeps the credentials (sandboxes never see real keys)
- Summarize findings for the user with `/report`; triage into the fix pipeline via `/deep-review-codebase`

## Rules

### 1. Trust Boundary

- Run only on repos you trust an AI agent to read — untrusted code → CI guarded mode or `--sandboxes`
- Secrets are not committed into a `.deepsec` shared with others — keep them in `.env.local`

### 2. Cost Discipline

- `scan` = free (local patterns); `process`/`revalidate`/`triage` = paid AI — always bound with `--max-cost-usd` in the first session
- Resume-friendly: no need to fear interrupts — always re-run the same command

### 3. Own The Matchers

- Review `generated-matchers.ts` before committing — it defines the scan coverage
- A stale `INFO.md` = misleading findings — update it after major codebase changes

- Use /check-secrets before/after scans for general hygiene
- Use /report to summarize findings

## Expected Outcome

- `.deepsec/` workspace ready: scan → AI review → exportable findings
- Every run is resumable, cost-bounded, and credentials never leak into sandboxes/reports
