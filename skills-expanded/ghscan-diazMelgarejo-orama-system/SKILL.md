---
name: orama-system
description: >-
  Elegant problem-solving methodology with 5-stage process, AFRP pre-router gate,
  CIDF v1.2 content insertion framework, and 7-agent execution network. Activates
  for architectural thinking, systematic verification, content insertion decisions,
  complex multi-step tasks, code quality reviews, and self-improvement workflows.
  Triggers on: "ultrathink", "think deeply", "5-stage", "systematic approach",
  "elegant solution", "verify before done", "content insertion", "AFRP", "CIDF".
  Treat legacy "ultrathink" prompts as oramasys invocations.
version: 1.1.1.0
license: Apache 2.0
compatibility: claude-code, claude-desktop
allowed-tools: bash, file-operations, web-search, subagent-creation, mcp-oramasys
sub_skills:
  - path: afrp/SKILL.md
    trigger: "Query is non-trivial, audience-dependent, or open-ended (Type B/C/D)"
  - path: cidf/SKILL.md
    trigger: "Any content insertion, file write, paste, upload, or scripted output"
  - path: gstack/SKILL.md
    trigger: "/browse, /qa, /ship, /review, /investigate, gbrain, web browsing, QA, deploy, design review, gstack skills, canary, benchmark"
  - path: skills/skillify/SKILL.md
    trigger: "create a skill, new skill, /skillify, add sub-skill, build a skill, make a skill"
  - path: skills/agent-coordination-heartbeat/SKILL.md
    trigger: "heartbeat monitoring, agent liveness, dead agent detection, cleanup stale claims, heartbeat dashboard, agent coordination heartbeat, heartbeat pulse, heartbeat kill"
  - path: skills/kimi-agent/SKILL.md
    trigger: "kimi, kimi code, kimi cli, fan out to kimi, moonshot kimi"
  - path: skills/mcp-install/SKILL.md
    trigger: "install mcp stack, setup gemini mcp, register ai-cli, mcp orchestration setup, install mcp tools, run install-mcp-stack.sh, mcp install"
  - path: skills/mcp-orchestration/SKILL.md
    trigger: "mcp orchestration, connect mcp tools to openclaw, gemini large context, ai-cli-mcp, background agents, dispatch parallel ai cli, openclaw mcp, SKILL.md claude skills, mcp json tool setup"
  - path: skills/codex-mcp-debugging/SKILL.md
    trigger: "codex mcp debugging, codex mcp list failed, invalid transport, bearer_token_env_var, stdio vs http transport, exa mcp wrapper, github mcp codex config"
  - path: skills/first-run-setup/SKILL.md
    trigger: "first-run install, bootstrap orama, setup new machine, first run, §0 checklist, first-run-install.sh"
  - path: skills/code-review/SKILL.md
    trigger: "code review, review the code, blast-radius, code-review-graph, detect_changes, get_review_context, semantic_search_nodes, code-reviewer, multi-lens PR review, /review, recursive code review"
  - path: skills/openclaw-skills/SKILL.md
    trigger: "openclaw config, /openclaw-new-agent, /openclaw-add-channel, /openclaw-add-cron, /openclaw-dream-setup, /openclaw-add-script, /openclaw-add-secret, /openclaw-status, /openclaw-restart, /openclaw-stow, spawn openclaw, recursive openclaw spawn, openclaw secrets pipeline, new openclaw agent, openclaw orchestration, jobs.json, dream routine, the nine skills"
  - path: skills/openclaw-skills/codex-openclaw-agent/SKILL.md
    trigger: "codex openclaw agent, codex-agent, GPT-5.5 sub-agent, native Codex provider, create Codex workspace, reconcile Codex agent, openai-codex auth"
  - path: skills/hermes-harness/SKILL.md
    trigger: "hermes setup, hermes onboarding, nous portal, hermes openclaw migration, ecc harness, cross-harness, install codex cli on windows, hermes coding partner"
  - path: skills/shell-hygiene/SKILL.md
    trigger: "sleep && cmd, sleep chain, wait for background task, poll output file, wait for npm install, wait for claude update, run_in_background polling, until loop, how to wait for a process"
  - path: skills/git-history-surgery/SKILL.md
    trigger: "expunge git history, remove secret from history, rewrite author, scrub commits, branches 600 behind, orphaned branch after rewrite, re-anchor branch to main, reconcile branches after force-push, recover deleted branch, byte-identical common ancestor, branches all became the same, git history rewrite recovery, branches lost common ancestor, MERGE_HEAD, pre-push blocked, empty PR after merge, no-commit merge"
  - path: skills/git-pending-push-guard/SKILL.md
    trigger: "MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, pre-push blocked, empty PR after merge, no-commit merge, pending git operation, GIT_PUSH_E_PENDING"
  - path: skills/guard-sync-divergence-guard/SKILL.md
    trigger: "guard sync, sync-attribution-guard-scripts, verify-guard-parity drift, sibling ahead of canonical, anti-clobber sync, GUARD_SYNC_E_DIVERGENCE, promote upstream before sync, check-guard-sync-divergence"
  - path: gstack/SKILL.md
    trigger: "fix gbrain, resync gbrain, gbrain sync failed, prepared statement does not exist, CONNECTION_CLOSED supabase pooler, No database URL, GBRAIN_DATABASE_URL, gbrain doctor failures, createVersion failed, autopilot wedged, gbrain after history rewrite, gbrain list empty, gbrain prepare false, gbrain source pin"
---
<!-- lint-ignore LINT-013 -->

# The ὅραμα System Skill

> "Technology married with humanities yields solutions that make hearts sing.
> Every solution should feel inevitable — so elegant it couldn't be done any other way."

ὅραμα is from Ancient Greek meaning “that which is seen”, we now use it as a methodology for solving “impossible problems” through an intentional, staged process.. revelation made operational, technically: stateless orchestration meta-intelligence

orama-system is meant to become:

- A **complete method**, not just a tool — complete, production-ready methodology for self-improving agents and skills package.
- A **disciplined intelligence pipeline** — the 5-stage flow from context to crystallization, so insight becomes action and then reusable knowledge.
- An **orchestration** layer — a meta-intelligence/delegation runtime above infrastructure and middleware, with clear boundaries/invariants.
- A “delegate, not decider” runtime — it should orchestrate and execute resolved decisions, not re-derive gateway policy (teleology of humility + clarity in system role).

## Pre-Flight: Spec Contract

Before the AFRP gate. Sets the contract that AFRP then routes.
Full template and rationale: `docs/v2/references/ORAMASYS-MASTERY-v3.md § M1`

Three questions every task must answer before execution:

**Role** — who are we in this context?
(Systems Architect / Research Scientist / Engineer / Teacher / Operator)

**Goal** — what outcome actually matters?
Not the activity. The outcome. What must be true before success is declared?

**Constraints** — reality always wins.
Time, budget, security, compliance, compatibility. Constraints define the shape of the solution.

```text
ROLE: <who you are>
GOAL: <what must be true when done>
CONSTRAINTS: <assumptions, limits, what to avoid>
```

## Amplifier Objective Tree

Every task has three layers. Identify all three before starting.
Full principle: `references/amplifier-principle.md`

| Layer | Question |
| --- | --- |
| Explicit objective | What was requested? |
| Hidden objective | What problem is actually being solved? |
| System objective | What improves the larger system? |

Most failures optimize only the explicit objective.

---

## Pre-Router Gate: AFRP (Mandatory)

Before the Execution Mode Router fires, every non-trivial query passes through
[the Audience-First Response Protocol](afrp/SKILL.md).

```ascii
Task arrives
    |
    v
+-- AFRP GATE (afrp/SKILL.md) -------------------------+
| 1. Classify query type (A/B/C/D)                     |
| 2. If B/C/D -> ask max 2 clarifying questions        |
| 3. Separate profile data from audience data          |
| 4. Declare scope                                     |
| 5. Calibrate abstraction level                       |
| 6. Pass resolved context to Router                   |
+------------------------------------------------------+
    |
    v
Execution Mode Router (below)
```

> Implements [the Amplifier Principle](references/amplifier-principle.md): "Point it at clear intent and it
> accelerates you; point it at ambiguity and it scales the ambiguity."

## Execution Mode Router

```ascii
Task arrives (post-AFRP)
    |
    v
+-- ROUTER: evaluate three signals -----+
| Signal 1: Content insertion involved? |
| Signal 2: Task complexity             |
| Signal 3: Explicit user override      |
+----|-----------|-------------|--------+
     v           v             v
  MODE 1      MODE 2        MODE 3
  Inline    + Subagents   Full Network
 (1-2 steps) (3-7 steps)  (8+ steps)
```

### Router Decision Table

| Signal              | Mode 1 Simple | Mode 2 Standard | Mode 3 Complex |
| ------------------- | ------------- | --------------- | -------------- |
| Steps               | 1-2           | 3-7             | 8+             |
| Systems touched     | 1             | 1-2             | 3+             |
| Parallel work       | No            | Maybe           | Yes            |
| Context window risk | Low           | Medium          | High           |
| Codebase scope      | File/function | Module          | Multi-module   |

## Content Insertion — CIDF v1.2 (All Modes, Always Active)

**Any time this skill inserts, writes, pastes, uploads, or scripts content — CIDF governs it.**
No exceptions. Start at rank 1 every time.

### The One Rule

> Use the simplest tool that works. Complexity is a cost, not a feature.

### Method Priority

| Rank | Method              | Eligible When                      | Complexity |
| ---- | ------------------- | ---------------------------------- | ---------- |
| 1    | `direct_form_input` | Field accessible, content < 10k    | 1          |
| 2    | `direct_typing`     | Editor visible, content < 5k       | 2          |
| 3    | `clipboard_paste`   | Paste supported, formatting OK     | 2          |
| 4    | `file_upload`       | Upload available, format supported | 3          |
| 5    | `scripting`         | Automation gate OPEN only          | 5          |

### Verification Protocol (mandatory)

```ascii
execute_method() -> visual_ok? --no--> refresh_page()
                       |                     |
                       +---> verify_programmatically()
                                    |
                             signature_in_page?
                               yes -> mark_complete()
                               no  -> try_next_rank()
```

[Full CIDF details:](cidf/SKILL.md)`cidf/SKILL.md`

## Markdown Editing Rule

For any `*.md` write or edit:

1. Read PT `.agent` development memory and `docs/wiki/README.md` first if the change touches repo guidance or a moved doc.
2. Keep all links relative and GitHub-renderable; do not use absolute filesystem paths or sibling checkout paths.
3. If a markdown file moves or is renamed, preserve a repo-wide redirect trail by updating the canonical index or adding a `Previous path` / `Canonical path` note where appropriate.
4. Warn and ask the user before adding a new markdown file over 200 lines or growing an existing markdown file over 500 lines. Suggest moving details to `references/`, `docs/wiki/`, or a sub-skill.
5. Before committing `*.md`, inspect the diff for broken anchors, stale paths, and missing redirect notes.

## MODE 1: Inline Single-Agent (Simple Tasks)

1. Read context (30 seconds max)
2. If content insertion: run CIDF `decide()` -> use chosen rank -> verify
3. Execute directly, no subagents
4. Verify result (Directive #4)
5. Done

## MODE 2: Single-Agent + Subagents (Standard Tasks)

### Stage 1 — Context Immersion

Scan project structure, git history, skill files. Identify constraints, patterns,
historical lessons. Output: 2-3 paragraph context summary.

### Stage 2 — Visionary Architecture

Design modular breakdown with clean interfaces. If content insertion -> run CIDF
`decide()` here. Ask: "What would the most elegant solution look like?"

### Stage 3 — Ruthless Refinement

Quality rubric: simplicity 5/5, readability 5/5, robustness 5/5.
Remove everything non-essential. Elegance = nothing left to take away.

### Stage 4 — Masterful Execution

```ascii
Plan   -> tasks/todo.md with checkable items
Craft  -> TDD, naming poetry, edge cases handled
CIDF   -> every write/insert uses ranked method + programmatic verify
Verify -> scripts/verify_before_done.py -> must PASS
```

### Stage 5 — Crystallize the Vision

Assumptions ledger, simplification story, inevitability argument.
Run `scripts/capture_lesson.py` with `PERPETUA_TOOLS_ROOT` if any corrections occurred.

### Subagent Delegation (Directive #2)

```ascii
When context > 70% -- offload, one task per subagent:
  subagent("Research best library for X. Return: comparison table.")
  subagent("Prototype approach A"); subagent("Prototype approach B")
```

**Output shape** -- every substantial deliverable contains six sections:

1. ASSUMPTIONS: what you decided, guessed, or ruled out
2. ARCHITECTURE / PLAN: structure and component relationships
3. ARTIFACT: the actual deliverable
4. TEST & VERIFICATION: how correctness is validated
5. RISKS + MITIGATIONS: failure modes and mitigations
6. NEXT ACTIONS: numbered, concrete, with clear ownership

## MODE 3: Full Multi-Agent Network
>
> **Multi-agent safety:** See `references/collaborative-reasoning-safety.md` — mandatory Builder/Critic/Adversary/Judge roles, anti-groupthink rules, confidence tracking.
>
> **On Claude Code: this is a policy layer, not a runtime to build.** The
> canonical execution mechanism is Claude Code's own `Workflow` tool
> (`agent()`/`parallel()`/`pipeline()`/`phase()`), gated by the same
> `ultracode`/explicit-ask opt-in the tool itself requires — never a
> bespoke dispatch loop. **Model tiering is mandatory, never inherited
> from the parent:** Haiku for dispatch/control of non-Claude models
> (Codex, Cline, Kimi, Cursor, Grok, Perplexity, OpenClaw, Hermes, ...),
> Sonnet 5 Medium only to evaluate/integrate that output, Opus/Fable 5
> only on explicit user request or an AskUserQuestion-confirmed
> escalation — never automated. Full role-to-primitive mapping + tiering
> policy: `references/claude-code-workflow-canonical.md`. This mapping is
> Claude Code-specific; other harnesses (Codex, gemini-cli, Cursor, ECC)
> keep the abstract description below as-is.
 (Complex Tasks)

### Agent Network

```ascii
Orchestrator
+-> Context Agent       Stage 1 -- parallel: doc scanner + git historian
+-> Architect Agent     Stage 2 -- module design, spawns designers
+-> Refiner Agent       Stage 3 -- elegance loops (max 3, threshold 0.8)
+-> Executor Agents x5  Stage 4 -- parallel TDD; each calls CIDF before write
+-> Verifier Agent      Stage 4.5 -- blocks until PASS; enforces CIDF LINT-002
+-> Crystallizer Agent  Stage 5 -- docs + updates shared lessons DB
```

Config: `config/agent_registry.json` + `config/routing_rules.json`

### AutoResearch Integration (Mode 3 Task Type)

When the coordinating system reports **`task_type`** of **`autoresearch`** or **`ml-experiment`** (from **Perpetua-Tools**):

1. **Defer execution topology** to Perpetua-Tools: `POST /autoresearch/sync` must succeed (`sync_ok == true`) before deep multi-step planning assumes the GPU workspace is ready.
2. **Reasoning layer (this repo)**: apply **CIDF / ultrathink** methodology for hypotheses, critique, and next-step narrative — but **do not** assume cloud models for autoresearch unless the user explicitly overrides (see Perpetua-Tools `SKILL.md` “autoresearch Tasks”).
3. **GPU lock & metrics**: treat **`swarm_state.md`** (IDLE/BUSY) and **`log.txt` / `val_bpb`** as the source of truth for whether a run is active and whether metrics are valid.
4. **Cross-repo stack**: Perpetua-Tools (orchestrator) → orama-system (reasoning) → ECC Tools (optional parallel executors) → Karpathy autoresearch loop on the GPU host.

For local setup work inside Perpetua-Tools, the Perplexity client now exposes optional `base_url` and `timeout` overrides, and the smoke-test script accepts the same values:

```bash
python scripts/test_perplexity.py --validate --base-url https://api.perplexity.ai --timeout 30
```

## The 6 Directives (Always Active, All Modes)

| #   | Directive      | Rule                                                 |
| --- | -------------- | ---------------------------------------------------- |
| 1   | Plan Node      | Write `tasks/todo.md` before any 3+ step task        |
| 2   | Subagents      | Offload when context > 70%; one task per subagent    |
| 3   | Self-Improve   | After correction -> controller -> PT `.agent` memory |
| 4   | Verify First   | `scripts/verify_before_done.py` PASS required        |
| 5   | Elegance       | Pause on non-trivial: "Is there a more elegant way?" |
| 6   | Autonomous Fix | Bug report -> investigate -> fix -> verify -> report |

## Boundaries

### Always Do

- Run CIDF `decide()` before any content insertion (all modes, no exceptions)
- Verify programmatically after every insertion
- Write `tasks/todo.md` before implementing anything with 3+ steps
- Start at CIDF rank 1 — never jump directly to scripting

### Ask First

- Deleting files or directories, pushing/syncing git repos
- Deploying to any live environment
- Modifying config, vendor, or .env files
- Switching from Mode 2 -> Mode 3 (resource cost)

### Never Do

- Mark complete without programmatic verification
- Skip CIDF for any content insertion (even "quick" writes)
- Trust visual confirmation alone
- Hardcode secrets or credentials
- Force push git repos without backup checkpoint `*.git` files

## Success Criteria

| Metric                   | Target                            |
| ------------------------ | --------------------------------- |
| Token ROI                | > 10:1                            |
| CIDF compliance          | 100%                              |
| Mode selection accuracy  | Mode 3 only when genuinely needed |
| Verification before done | 100%                              |
| Repeat mistake rate      | <5%                               |

## Quick Start (Usage Guide)

### 1. Activation

Trigger the full 5-stage process with:

- `ultrathink this`
- `apply the system to: [your task]`
- `production-ready [task]`

### 2. Mandatory Workflow

Follow the 6 directives in every non-trivial task:

1. **Plan**: `./scripts/create_task_plan.sh "Build feature"`
2. **Execute**: Build stage-by-stage (Context -> Architect -> Refine -> Execute -> Crystallize)
3. **Verify**: `python scripts/verify_before_done.py` (Must PASS before done)
4. **Learn**: `PERPETUA_TOOLS_ROOT=/path/to/Perpetua-Tools python scripts/capture_lesson.py --quick` (Run after any correction)

### 3. Integrated Frameworks

- **AFRP**: Pre-router gate. Classifies and clarifies intent before architecture.
- **CIDF v1.2**: Content insertion governance. Start at rank 1 (direct_form_input) for every write.

> **Historical Note:** The canonical HTTP path is `/oramasys`; legacy `/ultrathink` is implemented via `api_server.py` as a deprecated v1.x compatibility shim.

## OpenClaw Multi-Agent Bridge (Tier 2)

Use the `mcp-oramasys` tool to offload heavy reasoning through the
OpenClaw gateway at `127.0.0.1:18789`. Model selection is automatic — OpenClaw
reads `~/.openclaw/openclaw.json` and routes each `agent_id` to the correct
live provider (LM Studio / Ollama, Mac / Windows GPU).

### Capabilities

- `openclaw_chat`: Route by role (`coder`, `orchestrator`, `mac-researcher`, `win-researcher`)
- `openclaw_list_agents`: List agents registered in `~/.openclaw/openclaw.json`
- `openclaw_orchestrate`: Dispatch Stage 4 execution tasks via OpenClaw gateway
- `openclaw_health`: Verify gateway is running at `127.0.0.1:18789`

## Hermes Cross-Harness Bridge (Tier 2 sibling)

Use [`skills/hermes-harness/SKILL.md`](skills/hermes-harness/SKILL.md) when
Hermes is the operator shell for PT-orama work. Hermes consumes canonical
skills, MCP conventions, and bounded partner prompts; OpenClaw remains the
runtime gateway/configuration fabric. Do not import raw `~/.hermes` state,
secrets, personal memory, or local business artifacts into the repo.

Hermes worker default: bounded coding partner. The main orama agent keeps
judgment, CIDF write discipline, and final synthesis.

Companion context:

- `skills/hermes-harness/references/ecc-hermes-cross-harness.md` for ECC import
  decisions and cross-harness boundaries.
- `../../ANTIGRAVITY.md` and `../../.agent/AGENTS.md` for Antigravity project
  wiring that points back to canonical orama skills instead of copying them.
- `../../docs/wiki/15-hermes-windows-harness.md` for the Windows PATH,
  `HERMES_GIT_BASH_PATH`, and explicit Hermes one-shot provider route.

## First-Run Bootstrap

New machine or fresh checkout:

```bash
bash bin/orama-system/scripts/first-run-install.sh status    # fast probe
bash bin/orama-system/scripts/first-run-install.sh install  # idempotent §0 checklist
bash bin/orama-system/scripts/install-mcp-stack.sh          # MCP workers (separate)
```

Full steps: [`references/first-run-install.md`](references/first-run-install.md) · Agent workflow: [`skills/first-run-setup/SKILL.md`](skills/first-run-setup/SKILL.md) · **E2E (install → MCP → code review):** [`../../docs/how-to/first-run-and-code-review.md`](../../docs/how-to/first-run-and-code-review.md) · **Host surfaces:** [`../../docs/reference/agent-first-open-visibility.md`](../../docs/reference/agent-first-open-visibility.md)

## References (Progressive Disclosure)

Load on demand for deeper context:

- `references/first-run-install.md` — §0 install checklist (canonical; CLAUDE-instru.md is navigator-only)
- `afrp/SKILL.md` — Audience-First Response Protocol (pre-router gate)
- `cidf/SKILL.md` — Content Insertion Decision Framework v1.2
- `references/amplifier-principle.md` — foundational essay on intent-driven development
- `references/oramasys-5-stages.md` — deep dive on the 5-stage methodology
- `references/core-operational-directives.md` — the 6 directives in detail
- `references/content-insertion-framework.md` — CIDF human reference + JSON policy
- `references/skill-architecture-guide.md` — how to build SKILL.md files
- `references/contribution-standards.md` — CONTRIBUTING.md + PR-template baseline; the method's contribution practices (raised standard, PT PR #247)
- `templates/task-plan.md` — task planning template (Directive #1)
- `templates/verification-checklist.md` — pre-completion checklist (Directive #4)
- `templates/lessons-log.md` — self-improvement log (Directive #3)

---

## Multi-Agent Collaboration Protocol

Rules that prevent conflicts when multiple agents share a codebase: pre-session sync,
scope claims, IP/endpoint defaults, the version-bump registry, the `.ecc/` gitlink, the
commit-message contract, and the conflict-recovery playbook. Encode them in every
agent's SOUL.md and session start.

→ Full protocol: `references/multi-agent-collaboration-protocol.md` (load before any multi-agent session).

## Code Exploration Order

Use code-review-graph MCP tools BEFORE Grep/Read for any multi-file question. Chain: code-review-graph (blast-radius) → gbrain code-def (symbols) → gbrain search (decisions) → Read (confirmed files only). Never default to Grep for code questions.

**RAG wiring (CLI + Desktop) — single enforcer:** the semantic lane needs the gbrain + CRG MCP servers registered in both surfaces. Do NOT re-check this per skill — run the canonical `python3 scripts/ensure-rag-mcp.py [--apply]` (also run by `start.sh`). If CRG's MCP is down, its semantic search has no CLI fallback → degrade to `gbrain search`/`code-def` (same bge-m3 vector space). Reconnect recipe: `code-review` skill § "Fix: MCP disconnected".

## Search Policy

**RULE: Never guess when information is scarce.**
Search in this order — stop at the first satisfying result:

1. `/sync-gbrain` + `gbrain query "<question>"` — local semantic memory, zero cost
2. `code-review-graph: semantic_search_nodes` — structural code context
3. Brave Search API — web facts, current state
4. Perplexity API (inline) — deep web synthesis
5. Grok API — last resort only

**NEVER:** parallel-fire all search tools. Use the cheapest first.
**ALWAYS:** `AskUserQuestion` for decisions — never auto-select between ambiguous options.

**Extraction, not discovery:** once this chain finds a URL, use
[`skills/firecrawl/SKILL.md`](skills/firecrawl/SKILL.md) to scrape,
interact with, parse, or monitor it — Firecrawl sits downstream of this
policy, it doesn't replace it.

## Windows Coder Pool

**RULE: Every available Windows coder MUST be given work as soon as it is idle.**

Endpoint pool: `$WIN_CODER_ENDPOINTS` (default: `192.168.254.103:1234`)

Dispatch protocol:

1. Before routing any task to Mac-only paths, check if a Windows coder is free.
2. If free AND task is compatible (Python, Go, TypeScript, general coding):
   → dispatch to Windows coder FIRST.
3. If offline or no model loaded: skip silently, log WARN, do not fail.
4. As more Windows coders are added to `$WIN_CODER_ENDPOINTS`, they join the pool
   automatically — same rule applies to all.

**Never leave a Windows coder idle if pending compatible work exists.**

## OmniRoute Lazy-Sidecar (Optional Parallel Dispatch)

> **NEVER install. NEVER require. NEVER fail if absent.**
> **CURRENTLY DISABLED (2026-06-14).** Skip probe entirely. Use Local API Fallback below.
> To re-enable: see `skills/omniroute/SKILL.md § Re-enable OmniRoute`.

Optional local HTTP MCP server (port 20128) that fans tasks to free OpenRouter/AgentRouter
models in parallel. Probe once at session start (token from `$OMNIROUTE_TOKEN`, never
hardcoded); if `running`/`started`, route fan-out subtasks through it; if `unavailable`,
continue silently on the standard stack — never warn or suggest installing it.

→ Canonical sidecar (probe + parallel-dispatch + ops/config/password reset + disable/re-enable runbook): `skills/omniroute/SKILL.md`.

## Periscope ECC Lazy-Sidecar (Optional Mirror Verify)

> **NEVER install. NEVER require. NEVER fail if absent.**

When a periscope clone with ECC bundle paths exists, agents may run the idempotent
mirror verifier. If absent, skip silently.

→ Canonical sidecar (probe + mirror contract + dependency-instinct pair policy): `skills/periscope-ecc/SKILL.md`.

## Local API Fallback (when no external API is reachable)

**Priority: Ollama (`localhost:11434`, always-on Mac) → LM Studio (`$LM_STUDIO_WIN_ENDPOINTS`) → surface outage.**
Every tier check: ≤3s timeout. Fail loudly if `$LM_STUDIO_WIN_ENDPOINTS` is set but unreachable.

→ Full procedure + decision table: `references/local-api-fallback.md`

## Shell Portability Invariants (all agents / all scripts)

**1. `codex review` always needs `< /dev/null`.**
Without it the process blocks on stdin indefinitely — the hang is invisible.

```bash
codex review "<prompt>" -c 'model_reasoning_effort="high"' < /dev/null
```

**2. Never use bare `timeout N <cmd>` on macOS.** GNU `timeout` is absent on stock macOS. Use:

```bash
_TO=$(command -v gtimeout 2>/dev/null || command -v timeout 2>/dev/null || echo "")
if [ -n "$_TO" ]; then "$_TO" N <cmd>; else <cmd>; fi
```

`gtimeout` = Homebrew coreutils. `timeout` = Linux. Omit the wrapper only when hanging is safe to ignore.

**3. OpenClaw delegation key is `agents.defaults.subagents.allowAgents`** (or `agents.list[id].subagents.allowAgents`).
The key `agents.bindings.*.allowAgents` is rejected by the oramaclaw control plane.

---

## Extended References

| Reference | Content |
| --- | --- |
| `references/amplifier-principle.md` | Full Amplifier Principle essay |
| `references/oramasys-5-stages.md` | Deep dive: 5-stage methodology |
| `references/collaborative-reasoning-safety.md` | Multi-agent safety (M3) |
| `references/communication-guidelines.md` | Writing guidelines (M6) |
| `references/multi-agent-collaboration-protocol.md` | Pre-session sync, scope claims, version-bump registry, conflict recovery |
| `skills/omniroute/SKILL.md` | Canonical OmniRoute sidecar — probe + parallel-dispatch + ops/config/password reset + disable/re-enable runbook |
| `skills/periscope-ecc/SKILL.md` | Periscope ECC lazy sidecar — idempotent Agents/Claude skill mirror verify; v2 orbiting satellite |
| `skills/hermes-harness/SKILL.md` | Hermes onboarding, ECC cross-harness import rules, Nous Portal/LM Studio provider setup, and bounded Hermes/Gemini/AGY/Codex partner prompts |
| `skills/hermes-harness/references/platform-affinity-routing.md` | Platform affinity bias — Mac/Linux → OpenClaw; Windows → Hermes; ECC bridges both (v1 + v2) |
| `skills/cursor-agent/SKILL.md` | Cursor background agent (`agent` CLI) — install, auth, light-task fanout alongside Sonnet 4.6, worktree isolation, MCP integration |
| `docs/wiki/15-hermes-windows-harness.md` | Windows Hermes launcher, Git Bash, and one-shot provider routing notes |
| `references/local-api-fallback.md` | Local API fallback full procedure (Ollama → LM Studio → surface outage) |
| `docs/v2/references/ORAMASYS-MASTERY-v3.md` | Human-facing unified mastery reference |
