---
name: agentic-ops-orchestrator
description: "Route a real-world operations task to the right skill among 16 agentic-ops specialists — email, messages, GitHub, Jira, Google Workspace, project flow, unified notifications, terminal/CI, knowledge base, customer + finance billing, automation audit, workspace-surface audit, social connections, and dashboards. USE WHEN an agent must operate, triage, or prove work on a live external surface (inbox, repo, tracker, billing, docs) but the user hasn't named the specific skill."
cluster: agentic-ops
version: 1.0.0
---

# Agentic Ops Orchestrator

The single entry skill for **operating real-world surfaces** as an autonomous agent — the
inbox, the repo, the issue tracker, the billing system, the docs drive, the alert stream. It
locates the task on the **surface × intent** map and delegates to one of 16 operator spokes.
The cross-cutting discipline every spoke shares — the **evidence-first operator loop** (resolve
the surface → read live state → smallest reversible action → prove it → report exact status) and
the secrets/PII guardrails — lives in `agentic-ops-core`; read it before any live mutation.

## Cluster map (spoke → role)

**Communication surfaces**
- `email-ops` — mailbox triage, drafting, send, and Sent-folder proof.
- `messages-ops` — live texts / DMs, one-time-code recovery, thread inspection.
- `unified-notifications-ops` — collapse scattered alerts into one routed, deduplicated lane.

**Code-host & execution surfaces**
- `github-ops` — `gh`-CLI issue/PR/CI/release/security operations on GitHub.
- `git-workflow` — branching, commit conventions, merge-vs-rebase, conflict resolution.
- `terminal-ops` — evidence-first repo execution: run, debug CI, narrow fix, push with proof.

**Project-flow & tracker surfaces**
- `project-flow-ops` — triage GitHub↔Linear; public truth (GitHub) vs internal execution (Linear).
- `jira-integration` — retrieve/update Jira tickets, transitions, comments via MCP or REST.

**Knowledge & document surfaces**
- `knowledge-ops` — ingest/sync/dedupe/retrieve across files, MCP memory, vector stores, repos.
- `google-workspace-ops` — Drive/Docs/Sheets/Slides as one working system (find → inspect → edit).

**Revenue surfaces**
- `customer-billing-ops` — per-customer remediation: refunds, churn triage, portal recovery.
- `finance-billing-ops` — operator revenue truth: MRR, pricing, code-backed billing reality.

**Audit & observability surfaces**
- `automation-audit-ops` — inventory which jobs/hooks/connectors/MCPs are live/broken/redundant.
- `workspace-surface-audit` — audit repo/MCP/connector/env surface; recommend highest-value skills.
- `connections-optimizer` — prune/grow X + LinkedIn graph with review-first outreach.
- `dashboard-builder` — turn metrics into a working operator dashboard (Grafana/SigNoz).

## Folded spokes (coding-agent runtime, app-connections & usage)

Folded-in operator spokes for **driving coding-agent runtimes, wiring external apps, and proving
usage/cost**. Same evidence-first loop applies — resolve the surface, read live state, smallest
reversible action, prove it, report exact status. Load on demand exactly like the spokes above.

**Coding-agent execution surfaces**
- `coding-agent` — run Codex CLI / Claude Code / OpenCode / Pi as a background process for programmatic coding runs.
- `ai-automation-workflows` — choreograph an approved workflow / scheduled automation through the packet + approval gate (no bypass).
- `supacode-cli` — drive Supacode from the terminal: CLI commands, worktrees, agent runs.
- `hyperframes-cli` — HyperFrames CLI dev loop (`npx hyperframes`): scaffold (init), lint/validate, run.

**App-connection surfaces**
- `connect` — connect a coding agent to any app: send email, open issues, post messages, update databases.
- `connect-apps` — connect to named external apps (Gmail, Slack, GitHub) when the user wants to act through them.

**Observability & usage surfaces**
- `langsmith-fetch` — debug LangChain/LangGraph agents by pulling execution traces from LangSmith.
- `model-usage` — summarize per-model usage and cost (Codex / Claude) via the CodexBar CLI local data.
- `developer-growth-analysis` — analyze recent coding-agent chat history to surface patterns, gaps, and growth.

**General-purpose model call**
- `gemini` — Gemini CLI for one-shot Q&A, summaries, and generation.

Routing: **"run / background a coding agent"** → `coding-agent`; **"run an approved workflow / scheduled automation"** → `ai-automation-workflows`; **Supacode terminal** → `supacode-cli`; **HyperFrames scaffold/lint/run** → `hyperframes-cli`; **"connect my agent to an app / act through Gmail·Slack·GitHub"** → `connect` / `connect-apps`; **"why did my LangChain/LangGraph run do that"** → `langsmith-fetch`; **"per-model usage / cost"** → `model-usage`; **"analyze my coding history / where am I weak"** → `developer-growth-analysis`; **one-shot Gemini ask** → `gemini`.

## Routing rules (intent → spoke)

- **"Triage / clean my inbox", "draft a reply", "prove it sent"** → `email-ops`.
- **"Read my texts / DMs", "find the code"** → `messages-ops`.
- **"Alerts are noisy", "one notification policy", "what should interrupt"** → `unified-notifications-ops`.
- **"Manage issues/PRs/CI/releases on GitHub"** → `github-ops`; **branching / merge / rebase / conflicts** → `git-workflow`; **"run / debug / fix / push this repo"** → `terminal-ops`.
- **"Should this be a Linear issue?", "audit the PR backlog", GitHub↔Linear coordination** → `project-flow-ops`; **Jira tickets / transitions / comments** → `jira-integration`.
- **"Save / sync / search my knowledge", dedupe across stores** → `knowledge-ops`; **find/edit a Doc/Sheet/Slide, clean a tracker** → `google-workspace-ops`.
- **One customer's refund / cancel / billing breakage** → `customer-billing-ops`; **revenue snapshot, pricing, "is per-seat real in code"** → `finance-billing-ops`.
- **"What automations are live/broken/redundant"** → `automation-audit-ops`; **"what can my environment do / set up Claude Code"** → `workspace-surface-audit`; **social graph cleanup/growth** → `connections-optimizer`; **build a monitoring dashboard** → `dashboard-builder`.

## Standard Operating Flow

1. **Locate the task:** which *surface* (comms / code-host / project-flow / knowledge / revenue / audit) and which *intent* (inspect · triage · mutate · prove · audit).
2. **Pull the loop from `agentic-ops-core`** before any state change — resolve-surface → read-live → smallest-reversible → prove → exact-status is identical across every spoke.
3. **Delegate to the spoke(s).** Multi-surface asks fan out in evidence order, not parallel-blind — e.g. "fix the CI failure and tell the team" → `terminal-ops` (prove the fix) → `unified-notifications-ops` (route the result). "Audit first" asks (`automation-audit-ops`, `workspace-surface-audit`) run **before** any remediation spoke.
4. **Return:** chosen spoke(s), the surface(s) touched, the live-state evidence captured, and the exact status word + next action.

## Sibling clusters (when the task outgrows operations)

This cluster *operates* live surfaces; hand off when the task becomes *engineering*, not ops:

- **Deep git/CI internals** — beyond `github-ops`/`terminal-ops` live operation (pipeline design, build/release architecture, runner/infra config) → `devops-infra-orchestrator`; service/API/data-layer design behind the repo → `backend-architecture-orchestrator`.
- **Billing/revenue beyond ops truth** — `finance-billing-ops` owns the operator revenue snapshot; the *system* that produces it (schema, pricing service, data pipelines) belongs to `backend-architecture-orchestrator` and `databases-data-orchestrator`.
- **Hardening a surface** — auth, secrets management, or vulnerability review of the repo/billing/notification stack → `security-orchestrator`.

Stay in agentic-ops for *operating and proving* the surface; route out once the work is *building* it.

## Guardrails

See `agentic-ops-core`. In short: **read before you write** — resolve the exact surface and inspect
live state before any mutation; **default to read-only / draft** unless a live send/push/refund was
explicitly requested; never claim *sent / pushed / fixed / refunded* without naming the proof; never
expose secrets, tokens, or unnecessary PII; separate **fact** from **recommendation**; keep one
canonical home per fact set; and when the real fix is a different surface (triage, hook policy,
product gap), say so instead of forcing the current tool. The cluster's value is **provable
operations** — don't quietly assert state you didn't verify.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
