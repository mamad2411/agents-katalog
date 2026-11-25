---
name: bcc-plan-spar
description: >
  BCC align+lock+review PLAN.md for one slice (no product code). Slash: /bcc-plan-spar · chat: bcc:plan-spar · "lock PLAN" · spar the plan. Args: rounds=N (auto-review cap), review=self|subagent|cli|auto|off. Grill until clear enough (no default Q&A quota). Hand off to bcc-clean-cut after human APPROVE.
argument-hint: "slash: /bcc-plan-spar · chat: bcc:plan-spar · [topic] [rounds=N] [review=…]"
metadata:
  short-description: "BCC plan align + review"
---

# bcc-plan-spar

**Job:** solid coding contract for one slice —

1. **Human grill** (Q&A until **clear enough** — no default turn quota) → clear sub-plan intent  
2. **Lock** `PLAN.md` (+ `CONTEXT` / ADRs)  
3. **Auto review** (**`rounds`** = review budget, multi-backend) → live results → main agent **iterates PLAN**  
4. **Human final gate** → APPROVE / amend / stop  
5. Hand off to **`bcc-clean-cut`** (implement — not this skill)

**Deep source:** `grill-with-docs` Act 1 (grill + domain) + Act 2 (bounded review, CLI fallback).  
**Formats:** [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), [ADR-FORMAT.md](./ADR-FORMAT.md), [PLAN-FORMAT.md](./PLAN-FORMAT.md).

---

## Workflow preflight (required — before Phase 0/1)

**Do not** start grilling or rewriting `PLAN.md` until this check runs.  
If anything is ambiguous → **ask the user one clear question** (with a recommended answer). Do not invent workflow state.

### 1. Snapshot disk (read if present)

| Path | Ask |
|------|-----|
| `plans.md` / `progress.md` / `findings.md` | Is there a **global** endeavor map? Where are we? |
| `PLAN.md` | Is there an **active coding brief**? Draft or locked? Which slice? |
| `CONTEXT.md` / `docs/adr/*` | Domain language already started? |
| `.bcc/session.json` | Active slice / prior approve (see [SESSION.md](../bcc-breaking-coding-chaos/references/SESSION.md)) |
| Chat this session | Did user already APPROVE implement / skip align? |

Echo a one-line status, e.g.:

`preflight · throughline=yes|no · PLAN=missing|draft|locked|stale? · slice=? · session=… · recommend=grill|reuse-PLAN|hand-off-clean-cut|ask-user`

### 2. Hard rule: **throughline before plan-spar**

| Check | Required |
|-------|----------|
| `plans.md` exists with a non-empty **Goal** (and preferably a hardpoint map) | **Yes** |

If missing or empty:

1. **Do not** start Phase 1 grill for a multi-step endeavor.  
2. Tell user: *“bcc-plan-spar runs only after throughline. Run `/bcc-throughline` first (or Mode A `/bcc-breaking-coding-chaos`).”*  
3. Offer to load **bcc-throughline** now.  

Exception: user explicitly says **one-off micro task** and refuses a cockpit — then ask once to confirm; if they insist, proceed but still create a minimal `plans.md` Goal line when possible (preferred) rather than silent skip.

### 3. Is **bcc-plan-spar** the right skill right now?

| Situation | Suitable? | Do this |
|-----------|-----------|---------|
| No usable throughline (`plans.md`) | **No** | **bcc-throughline** first (hard rule above) |
| User wants **status / reprioritize only** | **No** | **`bcc-throughline`** or main skill status |
| User wants **code now** and PLAN locked + APPROVED | **No** | **`bcc-clean-cut`** |
| User wants **code now** but PLAN missing / draft | **Yes** | Align/lock here (after throughline OK) |
| User names a hardpoint on the map | **Yes** | Proceed; **update single root `PLAN.md` in place** for that work |
| Existing `PLAN.md` is for previous work | **Yes** | **Overwrite/refresh** `PLAN.md` for the new hardpoint (global history stays in throughline trio — not in PLAN) |
| Trivial one-liner / pure discussion | **Usually no** | Skip or ask |

**No formal state machine.** Infer from docs + chat; **suggest** next step if wrong skill.

### 4. Ask the user when uncertain

One question + recommended default:

1. Throughline missing — create now?  
2. Which hardpoint on the map?  
3. Refresh `PLAN.md` for this hardpoint (yes)?  
4. Align vs code (plan-spar vs clean-cut)?

### 5. After preflight OK → Phase 0

Only then: scope hardpoint, then Phase 1 grill / lock.

---

## Tunables

Parse from invocation (e.g. `/bcc-plan-spar auth rounds=3 review=auto`):

| Arg | Default | Meaning |
|-----|---------|---------|
| **`rounds`** / `MAX_REVIEW_ROUNDS` | `3` | **Only budgeted loop:** auto-**review** rounds after PLAN is locked. Set at spar start. `0` = skip auto review (human gate still required). |
| `review` | `auto` when `rounds>0`, else `off` | Review backend (see below) |
| `PLAN_FILE` | `PLAN.md` | Coding brief path |
| `LOG_FILE` | `PLAN-REVIEW-LOG.md` | Append-only live review transcript |

**Not a tunable by default:** Phase 1 human Q&A has **no default turn quota**. Grill until the agent judges **clear enough** (or the human locks / stops).  
Optional override only if the user explicitly passes `grill_rounds=N` / `MAX_GRILL_ROUNDS=N` — treat as a soft safety ceiling, not a target to fill. Do **not** invent or announce a default grill cap.

### `review` modes (simplified)

| Mode | Who reviews | When to use |
|------|-------------|-------------|
| **`auto`** | **subagent** if spawn works; else **self**. If user set `review=cli` and a CLI exists, may use CLI | Default |
| **`subagent`** | Fresh reviewer subagent (read-only) — preferred isolation | Stronger critique vs builder |
| **`self`** | Same agent, critic stance only | Always available 保底 |
| **`cli`** | Optional local CLI (e.g. `codex exec -s read-only` if installed) | User opts in; **fallback to self** on failure |
| **`off`** | Skip auto review | Human gate only after lock |

Do **not** require multi-agent products or cross-org setups. One host + optional subagent/CLI is enough.

Echo once before Act 1 (grill has no round count):

`bcc-plan-spar · topic=… · review_rounds=3 · review=auto · PLAN_FILE=PLAN.md · LOG_FILE=PLAN-REVIEW-LOG.md`

---

## Flow (fixed order)

```text
Preflight  Workflow fitness (throughline? PLAN? right skill?) — ask if unsure
Phase 0    Scope slice (+ read throughline)
Phase 1    Human grill ↔ agent until clear enough (no default Q&A quota)
           + CONTEXT/ADR → lock PLAN.md
Phase 2    Auto review loop (≤ rounds from invocation)  [unless review=off or rounds=0]
           each round: REVIEWER → VERDICT REVISE|APPROVED → live log
           if REVISE: BUILDER updates PLAN; if APPROVED: stop auto loop early OK
           fallbacks if backend fails (保底)
           NOTE: auto VERDICT: APPROVED ≠ permission to code
Phase 3    Human final gate ONLY decides bcc-clean-cut:
           APPROVE implement → bcc-clean-cut | amend | stop
```

**No product code** in bcc-plan-spar. **Only the human** starts `bcc-clean-cut` (or explicit skip-to-implement).

---

## Artifact separation

| File | Role |
|------|------|
| **`plans.md` / `progress.md` / `findings.md`** | **Only** global endeavor maintenance (throughline) |
| **`PLAN.md`** | **Single** living coding brief for **whatever is active now** — always updated in place; **no** per-slice PLAN files required |
| `CONTEXT.md` / `docs/adr/*` | Glossary / hard decisions assisting PLAN |
| `PLAN-REVIEW-LOG.md` | Optional review transcript (append or refresh per cycle) |

When starting a **new** hardpoint: rewrite `PLAN.md` for that work; move finished narrative into **progress.md**, not a second PLAN path.

---

## Phase 0 — Scope

- Name hardpoint (user topic or next from `plans.md`).  
- Throughline already required (preflight).  
- Read existing CONTEXT/ADR/code.  
- If old PLAN remains from a previous hardpoint: **replace** with the new brief when locking (after grill), after a one-line note in `progress.md` that the prior PLAN was superseded.

---

## Phase 1 — Human grill + lock PLAN (grill-with-docs Act 1)

### Purpose

Obtain **explicit information** from the human for this **sub-plan** — not silent guessing.  
**Stop when clear enough** — there is **no default Q&A round budget**. Prefer few high-signal questions; never pad to fill a quota.

### Interview rules

- **One question at a time.** Wait.  
- Each question: give a **recommended answer**.  
- Facts in codebase → look up; do not ask.  
- Decisions → user.  
- Do **not** track or announce “turn N of 10” (or any default cap).  
- Optional: only if user set `grill_rounds=N`, treat as soft ceiling; at that ceiling, summarize and ask lock / continue / stop.

### Stop & lock triggers (required)

| Who | Can do |
|-----|--------|
| **Agent** | When **clear-enough** criteria hold: **proactively propose lock**, e.g. *“这块已经够清楚，可以锁 PLAN 并进入 review（rounds=…）——现在锁、继续问、还是改？”* Do **not** keep asking “for completeness.” Do **not** lock silently unless user already said “lock when ready” / “够了就锁”. |
| **Human** | Interrupt **anytime**: “够了 / lock PLAN / 写 PLAN / 进入 review / stop” → lock or stop as asked. Do not keep grilling. |
| **Optional cap** | Only if user set `grill_rounds=N` and it is hit → same as agent propose: summarize open branches; ask lock / continue / stop. |

### Domain (domain-modeling)

- Challenge/sharpen terms; update **`CONTEXT.md` inline**.  
- ADRs only when hard to reverse · surprising · real trade-off.  
- Cross-check claims vs code.

### Clear enough → lock `PLAN.md`

Agent judges clear enough when **all** of the following hold (or user forces lock / interrupt lock):

1. Goal one paragraph  
2. Concrete numbered approach  
3. Contestable decisions resolved or parked under Risks  
4. Out of scope  
5. Checklist with implied verification each  
6. User confirmed understanding **or** accepted agent’s “clear enough — lock now?” **or** interrupted with lock  

Drafts: `_Draft — not locked_`. Prefer ubiquitous language from CONTEXT.

Announce: `PLAN.md locked via bcc-plan-spar for <slice>.`

### PLAN hygiene

Throughout Phase 1–2: **update + 约减** — short living contract, not a diary, not a global roadmap (roadmap = `plans.md`).

### Light throughline note after lock

Append one line to `progress.md`: slice name + “PLAN locked”. Optionally set hardpoint `in_progress` on `plans.md`. Full close-out writeback is **bcc-clean-cut**’s job ([WRITEBACK.md](../bcc-breaking-coding-chaos/references/WRITEBACK.md)).

---

## Phase 2 — Auto review (simplified grill-me-codex / grill-with-docs Act 2)

Inspired by adversarial plan review (e.g. grill-me-codex / grill-with-docs): **critic → verdict → builder revises PLAN → repeat**, with a **live log**.  
**Default stays in-process** (self or **subagent**). Optional **Codex CLI** if present — **not** required; no multi-vendor orchestration needed.

Runs when `MAX_REVIEW_ROUNDS > 0` and `review != off`, on a **non-draft** locked PLAN.

### Init log

Create/append `LOG_FILE`:

```markdown
# Plan Review Log: <slice>
bcc-plan-spar Act 1 complete — PLAN locked; CONTEXT/ADRs updated.
MAX_REVIEW_ROUNDS=<n> · review=<mode> · started=<timestamp>
```

### Reviewer stance (every round, every backend)

Skeptical and specific. Find: security, races, missing edges, schema conflicts, domain-language mismatch vs CONTEXT, wrong assumptions, unverifiable checklist items, simpler alternatives.

For each issue: **one-line fix**. End with exactly:

`VERDICT: APPROVED`  
or  
`VERDICT: REVISE`

**Read-only for external reviewers:** subagent / codex must **not** write repo files. Only the **main agent (builder)** edits `PLAN.md` / CONTEXT / ADR after a REVISE.

### Live results (required)

After **each** review round, the main agent must:

1. Surface the critique to the user **in chat** (summary + verdict) — do not hide it only in the log.  
2. Append full critique under `## Round <n> — Reviewer (<backend>)` in `LOG_FILE`.  
3. If `REVISE`: main agent as **builder** updates `PLAN.md` (material fixes only; reject bad nits with reason); append `### Builder response` (changed / rejected + why); **约减** PLAN; show user what changed.  
4. If `APPROVED` (from **agent/reviewer**): treat as **auto-review finished successfully** → Resolution → **still Phase 3 human gate**.  
   - Agent may say: *“Auto review APPROVED after N rounds. Ready for you to start bcc-clean-cut?”*  
   - **Do not** start `bcc-clean-cut` on auto APPROVED alone.

### Loop

For `ROUND = 1..MAX_REVIEW_ROUNDS`:

1. Run reviewer via active backend (below).  
2. Live log + chat surface (`VERDICT: REVISE` or `VERDICT: APPROVED` from the **reviewer agent/backend**).  
3. Reviewer APPROVED → Resolution (auto phase ends).  
4. Reviewer REVISE → builder iterates PLAN → next round.  
5. Cap without reviewer APPROVED → Resolution (deadlock) — list open issues. Never fake APPROVED.  

**Either way, bcc-clean-cut only after Phase 3 human decision.**

---

### Backend: `self`

Main agent plays **critic only** (not the builder voice of the previous turn). Same as grill-with-docs self mode.

### Backend: `subagent`

If the host supports spawning a subagent / separate reviewer:

1. Spawn **read-only** reviewer with prompt (below).  
2. No file writes from the child.  
3. Parent collects critique + verdict.  
4. On spawn failure / no subagent API: **fallback** (保底链).

### Backend: `cli` (optional)

Only if user asked `review=cli` (or auto tries after subagent fails and a known CLI exists):

- e.g. `codex exec` read-only with the review prompt (grill-me-codex style).  
- CLI must **not** write repo files.  
- On missing CLI / failure: notify and **fallback to self** — never hang.

### Backend: `auto` (default)

1. **subagent** if available  
2. else **self**  
3. optional **cli** only if already configured/requested  

### 保底机制

| Guarantee | Behavior |
|-----------|----------|
| **Fallback** | subagent → self (and cli → self); never block |
| **≥1 self pass** | If `rounds≥1` and fancy backends fail |
| **No fake APPROVED** | Cap → human decides |
| **Builder arbiter on REVISE** | Good fixes in; bad nits rejected with reason |
| **Human final gate** | Reviewer verdict ≠ permission to code |
| **Log** | Each round in chat + `PLAN-REVIEW-LOG.md` |

### Reviewer prompt core (subagent / codex / self)

> Adversarial reviewer for an implementation plan. Read `PLAN.md`, `CONTEXT.md`, ADRs, and needed repo files (**read-only**). Find concrete flaws; one-line fix each. Do not modify files. End with exactly `VERDICT: APPROVED` or `VERDICT: REVISE`.

### Resolution (end of Phase 2)

- **Reviewer APPROVED:** Present final PLAN + up to 3 bullets on what review improved + round count + backends used. State clearly: *auto review passed; waiting for your decision to implement.* → Phase 3.  
- **Deadlock / only REVISE left:** List unresolved points + builder counters. → Phase 3; human may still APPROVE implement with known risks, amend, or stop.

---

## Phase 3 — Human final gate (only path into bcc-clean-cut)

Always after Phase 2 (or after lock if review skipped). **This is the only default path that starts execution.**

Reviewer/agent may have said APPROVED or REVISE — that is **advisory** for the plan quality loop.

Ask:

> Auto review result: `<APPROVED | mixed | deadlock>`.  
> **Your call:** **APPROVE implement** (`bcc-clean-cut`) · **amend** plan · **stop**

| Human says | Agent does |
|------------|------------|
| **APPROVE implement** / “开写” / “bcc-clean-cut” | **Write `.bcc/session.json`** (approved_for=clean-cut, plan_sha256, active_slice, status=approved) per [SESSION.md](../bcc-breaking-coding-chaos/references/SESSION.md); then load **`bcc-clean-cut`** |
| **amend** | Update PLAN/CONTEXT/ADR; clear approve fields in session if PLAN hash will change; optionally re-enter Phase 2 |
| **stop** | Optional throughline note; **do not** bcc-clean-cut; session `approved_for=none` |
| Explicit **skip gate** earlier (“review then implement without asking”) | Same session write as APPROVE, then bcc-clean-cut |

Never treat Phase 2 `VERDICT: APPROVED` as automatic bcc-clean-cut.

### Session write on APPROVE (required)

After human APPROVE implement (or explicit skip-gate):

1. Ensure directory `.bcc/` exists.  
2. Hash current `PLAN.md` (SHA-256 of file bytes).  
3. Write/update `.bcc/session.json` with `active_slice`, `plan_path`, `plan_sha256`, `approved_at`, `approved_for=clean-cut`, `status=approved`.  

This lets a **new chat** still pass bcc-clean-cut preflight without re-deriving APPROVE from chat memory.

---

## Handoff

```text
bcc-plan-spar (align + auto review + human APPROVE)
    → bcc-clean-cut (minimal implement + verify + PLAN 约减 + throughline writeback)
```

---

## Invocation examples

```text
/bcc-plan-spar redesign checkout
→ grill until clear enough; lock PLAN; default rounds=3 auto review; human decides bcc-clean-cut

/bcc-plan-spar payments rounds=5 review=cli
→ grill until clear enough; 5 review rounds via CLI (fallback self); human gate

/bcc-plan-spar slice-x rounds=3 review=subagent
→ grill until clear enough; subagent reviewer ×3 max; fallback chain on failure

/bcc-plan-spar hotfix rounds=0 review=off
→ grill until clear enough + lock only; no auto review; still human gate before clean-cut

/bcc-plan-spar auth rounds=2 grill_rounds=6
→ optional soft grill ceiling 6 (user-set only); review rounds=2
```

Chat: "bcc-plan-spar", "对齐并锁 PLAN", "spar the plan rounds=5".

**`rounds` is the spar review budget** — the number to set when starting spar. Grill is not round-counted by default.

---

## Hard rules

1. **Preflight first**; **throughline (`plans.md`) before plan-spar** (hard).  
2. **Single `PLAN.md`** updated in place; global progress only in the three throughline files.  
3. Human grill before lock (unless draft/user forces).  
4. Phase 1: **no default grill quota** — stop when clear enough (or human lock/stop).  
5. **`rounds`** budgets Phase 2 auto review only; backends fail → **fallback**.  
6. Live chat + log every review round.  
7. Only main agent writes PLAN after REVISE; external reviewers read-only.  
8. **Never implement product code** here.  
9. Human final decision before bcc-clean-cut.  
10. Review caps terminate Phase 2 loops; never fake APPROVED.  
11. Infer next steps from context/docs; **suggest** to user — no heavy formal state machine.

## What NOT to do

- Don't run plan-spar before throughline.  
- Don't invent a default grill turn budget (e.g. “10 rounds”) or pad questions to fill one.  
- Don't create `PLAN-01.md` / per-case PLAN trees for global bookkeeping.  
- Don't skip preflight; don't code after auto APPROVED alone.  
- Don't invent CLI review success; fallback to self.  
- Don't dump coding checklists into `plans.md`.
