---
name: orchestration
description: Fable Orchestrator · universal Grok volume agent — session on Fable 5 architects; Grok 4.5 types and self-selects research/explore/critic/device phases for any scenario. USE WHEN implementing, exploring, verifying, writing five-part specs, consulting fable-advisor, fan-out parallel lanes, self-routing subagents, or managing token spend under Fable + SuperGrok Heavy.
---

# Orchestration — Fable Architect · Universal Grok Worker

The session is the **architect** (Fable 5). It owns requirements, decomposition, specs, **accept/reject of compressed reports**, and rare commitment judgment. It almost never types, almost never reads heavy trees, and never runs device loops.

The **default producer** is Grok 4.5 via `grok-implementer` — a **universal volume agent** (any domain: product, infra, debug, docs, research, device). Grok **self-selects** internal phases and subagents (`docs/ROUTING.md`). Architect does not micromanage researchers/critics per ticket.

Architect tokens are scarce; external CLI tokens are the volume path.

## Cost + throughput

1. **Emit judgment, not volume.** Specs, accept/reject — not boilerplate or full dumps.
2. **Keep context lean.** Broad search/read/log/diff → Grok lane; keep conclusions only here.
3. **Reason once, then hand off.** Interfaces into the spec; let Grok route internals.
4. **Dispatch early.** When a five-part spec is ready, fire `grok-implementer`.
5. **Fan out.** Independent units → multiple parallel spawns in **one** architect message.
6. **Trust ROUTING: auto.** Do not force RESEARCH/CRITIC on every unit.
7. **Fast path.** Mechanical ≤2 files → Constraints `ROUTING: force patch` + shorter wall (~180s). Still via Grok unless the user accepts architect typing outside product trees.
8. **Single root.** Prefer `bash "$HOME/fable-orchestrator/scripts/run-grok-headless.sh"`. After editing the plugin tree, run `scripts/sync-plugin-cache.sh`.

Inline architect implementation is a **quota failure**. Exception: a one-line blocker shorter than writing the spec (and not under product trees).

## Lanes

| Lane | Mode in Objective | Producer | Notes |
|---|---|---|---|
| **Explore** | `MODE: explore` | Grok | Map / impact. **No product edits.** Internal kids OK. |
| **Implement** | `MODE: implement` | Grok | Produce the change. **Self-routes** research/critic/device. |
| **Verify** | `MODE: verify` | Grok | Prove claims; no drive-by redesign. |
| **Auto** | `MODE: auto` | Grok | Worker picks explore vs implement vs verify from Objective. |
| **Judgment** | — | Fable + optional `fable-advisor` | Commitment boundaries only. |

Internal phases (research, critic, explore fan-out, device) are **not** separate architect spawns by default — they are Grok’s toolkit. Doctrine: `docs/ROUTING.md`, `docs/RESEARCH.md`, `docs/CRITIC.md`.

Spawn `grok-implementer` **without** a `name` (plugin hook enforces this).

If grok returns `unavailable` / `timeout`, say so. Do **not** silently re-implement as Claude.

### Architect no-touch (non-negotiable)

| Forbidden | Do instead |
|---|---|
| `Write` / `Edit` under product trees, lockfiles, app binary configs | Grok `MODE: implement` |
| Multi-step device / screenshot / gesture loops | Grok + device report paths |
| Broad repo search with full hit dumps | `MODE: explore` |
| Read large product files “to understand” | `MODE: explore` |
| Full `git diff` / huge logs in this transcript | `MODE: verify` |
| General-purpose implementers for product work | only `grok-implementer` + `fable-advisor` |
| Micromanaging subagents every ticket | `ROUTING: auto` — force only when needed |

**Allowed (cheap):** always-on docs (`CLAUDE.md`, `AGENTS.md`, short TODO/LEDGER); one-shot `list-devices` / `command -v grok`; read Grok reports; ≤40-line interface excerpt if required; `fable-advisor`.

## Spec contract

Implementers share **none** of your conversation context. Every prompt:

1. **Objective** — `MODE: explore|implement|verify|auto` + one paragraph (any scenario)
2. **Files** — paths or “discover under …”
3. **Interfaces** — shapes, or report shape for explore
4. **Constraints** — conventions, do-not-touch, shared-tree.  
   **Default:** `ROUTING: auto` (Grok self-selects phases/subagents).  
   Overrides only when needed: `ROUTING: force patch|research|critic|device|…` or explicit `RESEARCH:` / `CRITIC:`.
5. **Verification** — real proof (commands / evidence checklist)

Can't finish the spec → decision isn't made yet. That is architect work.

### Report formats

All volume reports should include:

```text
STATUS: pass | fail | blocked | timeout | unavailable | incomplete
SCOPE: full | partial
ROUTING: class=… ; phases=… ; reason=…
SUBAGENTS: none | …
```

Plus mode-specific body (`EXPLORE` / `GROK` / `VERIFY` / device paths).

Architect **does not** re-read the whole tree by default. Trust structured evidence; on doubt → re-spec or `fable-advisor` with risky hunks only.  
**Implement + pass:** require non-empty `git diff --stat` **or** report `NO_DIFF: reason`.  
Non-trivial invent + `RESEARCH: skipped` without justification → re-spec.  
`CRITIC: BLOCK` / hard residual → re-spec or advisor.  
Launcher v1.4.1+: STATUS detection is **exit-first**; mid-report enum lines must not kill lanes.

## Parallelism

### Level A — Claude → many `grok-implementer`

- Independent units → N spawns in **one** message (no `name`).
- Prefer worktree isolation when write paths collide and the runtime supports it.
- Shared tree: no `git stash`/`reset`; partition paths; final verify after the wave.
- Caps: ~3–6 explore, ≤2–3 implement.

### Level B — Grok → its subagents

**Grok decides.** Default on for multi-area work; off for patch class. Depth 1. Report `SUBAGENTS:`.  
Architect may say “act directly” only for known-trivial mechanical units.

### Level U — Universal self-routing

See `docs/ROUTING.md`. Worker classifies patch/standard/deep and enables only needed phases.

### Level R / Level C

Research and critic are **phases inside** the volume session, usually self-selected. Explicit Constraints override. Docs: `RESEARCH.md`, `CRITIC.md`.

## Commitment boundaries → `fable-advisor`

Consult (≤300 words) before architecture, migration, API shape, refactor strategy, two failed attempts, or declaring a multi-step deliverable done. Never ignore the verdict silently.

## Verification (architect-side)

1. Read STATUS + SCOPE + ROUTING + VERIFIED/paths — not the entire diff by default.  
2. Spot-check one risky hunk only if ambiguous.  
3. “Should work” / empty evidence → not done.

## Session ledger

2+ units → open project `docs/LEDGER.md` **before the second** spawn.  
**Compact lines only** (template: plugin `docs/LEDGER.md`).  
`[x]` only on `STATUS: pass` + evidence. No narrative dumps.

## Optional quality race (`--best-of-n`)

Hard / correctness-critical implement only:

```bash
bash "$LAUNCH" "$SPEC" "$FINAL" "$(pwd)" 540 3
```

Default off.

## Metrics + orphans

- Metrics: `~/.claude/fable-orch/metrics.jsonl` (`FABLE_ORCH_METRICS=0` to disable).  
- SessionEnd: `cleanup-orphans.sh` (report-only; kill with `FABLE_ORCH_KILL_ORPHANS=1`).  
- Never treat orphans / Metro / `ps|grep grok` as “lane still running.”

## Completion contract (anti-hang)

| Done | Not done |
|---|---|
| Report has plain `STATUS: …` | Empty / “waiting for notification” |
| Launcher returned or stamped timeout/incomplete | Metro still up |
| Evidence for claims | “Grok said it works” |

**Foreground** `run-grok-headless.sh` only. Lane identity = `${FINAL}.pid`.  
Helpers: `lane-health.sh`, `wait-for-status.sh`.  
Do not re-paste this skill every unit — apply it.

### Chain loop

1. Ledger if multi-unit.  
2. Decompose → five-part specs (`ROUTING: auto` by default).  
3. Dispatch early; parallel when independent.  
4. Accept/reject by STATUS; tick ledger.  
5. fail/partial → re-spec once; second fail → advisor or stop.  
6. Final verify after non-trivial wave.  
7. Short owner summary.

**Context budget:** STATUS + ROUTING + CHANGES/MAP + evidence **paths** only.
