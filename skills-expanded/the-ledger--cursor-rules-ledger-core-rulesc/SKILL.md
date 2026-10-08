---
description: The Ledger — core operating rules. Read in full before every response. Highest priority.
alwaysApply: true
---

# The Ledger — Core Rules (read before EVERY response)

## HARD RULES (read first)

- **Pre-ingest + Cursor compliance gate (binding — before every owner/Claude instruction and before
  every act/response)** — Cursor agents **MUST** read **`.cursor/rules/ledger-pre-ingest.mdc` first**
  and obey **every** Cursor-directed path in its corpus to **absolute compliance** (including
  `docs/CURSOR_IMPLEMENTATION_MANUAL.md`, core-rules, `AGENTS.md` Cloud constraints, handoff +
  Confront Claude). Checklist `EMPTY` is session inventory, **not** an owner debt. **RETIRED/DEFUNCT**
  keys are never requested. Partial compliance or skipping the corpus = task failure. Full text lives
  only in `ledger-pre-ingest.mdc` — do not restate its tables elsewhere.
- **No fabrication** — show `"No verified record available"` for genuine gaps; never invent facts, quotes, or dates.
- **Verbatim-only quotes** from journalism — never paraphrase and present as the politician's words.
- **Honest-gap vs diagnosed-failure** — a failed fetch/sync is UNVERIFIED (`fetch-failed`), never silent empty.
- **One source of truth per fact** — wire/join to existing generated data; never re-collect into a parallel file.
- **Source constitution is a living registry** — `docs/OBJECTIVE_SOURCES.md` owns approved sources, lean labels, and key routing; consult it FIRST and update it the SAME session you discover a better path or dead feed (§1.1 L).
- **Keep files accurate** — every session that touches a file/data/doc verifies any claimed done/complete/locked status against the REAL artifact and corrects or flags stale status the same turn; a regression that silently un-does prior verified work is a first-class bug. Status is earned by evidence, never by a label (§1.1 M; Claude manual §11).
- **`bioguideId` join key** — universal across votes, finance, news, statements; never alias.
- **Approval before MERGE, not just before push (binding — a PR is not self-approving)** — commit
  and push a PR when green, but **do not merge it** until an explicit **Claude "APPROVED"** verdict
  (a PR comment/review or a matching `docs/workflows/AGENT_HANDOFF_LOG.md` entry) exists for that
  exact commit SHA. Opening a PR — even one whose own description says "STOP for Claude review" —
  is not a review; merging within minutes of opening, before Claude has had a chance to look, is a
  gate bypass and a HARD RULE violation regardless of intent. If Claude posts REJECT/REQUEST_CHANGES
  on a PR, that PR does not merge until a NEW commit addressing the findings is pushed and a fresh
  APPROVAL is issued for that new SHA — merging the already-rejected SHA is never acceptable, and
  Cursor must actively check for a Claude review/comment on the PR before merging, not merge on a
  timer or "no CI failures" alone. (Real incident: PR #46 was merged 2 minutes after opening — 10
  minutes before Claude's REJECT review even posted. This rule exists because that happened.)
- **Fixtures append-only** — regression guards grow, never reset; every data-quality bug gets a frozen bad example.
- **Improve the process as it scales (binding)** — at each expansion step (1→10→25→80→200→completion),
  measure efficiency + effectiveness, improve one step, record it in the owning process doc; a scale
  step without a recorded improvement pass is incomplete (§6).
- **Spec violation = bug to fix, never a question** — read the owning file; do not re-ask the owner.
- **Stale violation flags are bugs** — when a flagged violation is fixed, delete its flag in the same commit.
- **Render-and-look — never approve UI from source alone** — any user-facing page/profile is verified
  against its **rendered output**, not by reading JSX/JSON. A headless render must pass the visual guard
  (`test:render-integrity`): **zero horizontal overflow** (no element past the viewport edge), **every
  portrait/image loads** (`naturalWidth > 0`), and **no empty required section**. At every batch gate a
  **screenshot contact-sheet** of the batch is produced and reviewed against the render — approval cites
  the screenshots, not the code. This rule exists because obvious rendered defects (a column running
  off-screen, a wrong portrait) passed source-only review and only the owner caught them.
- **Identity & asset integrity — the face must match the name** — every portrait/asset is keyed by the
  correct `bioguideId`; a person's photo, party, state, and office must all resolve to the SAME identity
  (never a cross-wired id — e.g. a governor showing another member's photo). Every current officeholder
  has a real portrait or an explicit honest-gap — never a silently wrong or placeholder image where one
  is expected. Guard-enforced (`test:identity-integrity`); scales to all profiles with no manual review.
- **Failure reporting is MANDATORY and AUTONOMOUS** — the owner must NEVER remind you.
  After **any** failed, timed-out, incomplete, or substandard attempt: **in the SAME response**
  (or immediately as a follow-up block before ending the turn), output the report in **§1.1**.
  Attempt 1 substandard → **Review for Claude** (§1.1 F). Attempt 2+ → full **Claude handoff
  report** (§1.1 B) and **STOP** further retries unless the brief explicitly allows another.
  Stale reports (recycled session lines, wrong commit, evidence contradicting `git show`) are
  **task failures** — Claude will reject them.
- **2+ failures → STOP and hand off** — never blind-retry or ask the owner to "try again."
  Completion claims require commit hash + fresh artifact evidence — see §1.1 C.
- **Substandard = surface immediately (owner visibility — binding)** — any file, generated
  data artifact, sync/process, guard result, doc, config, or UI output you engage with or review
  that is **not 100% flawless** to the written spec (credibility, layout numbers, office
  resolution, honest-gap semantics, test/guard failure, stale docs, path drift, regression,
  partial wipe, silent empty, or any defect class) MUST be **brought to the owner's attention in
  the same turn** — never silently worked around, deferred without flag, or buried in a passing
  summary. Do not wait for the owner to discover it. Format: **what** · **where (path/commit)** ·
  **evidence** · **severity** · **recommended repair** (Claude brief vs agent-fixable). Routine
  code/data fixes proceed without asking permission; **visibility is mandatory** even when you
  are also fixing it. Credibility *tradeoffs* still route to Claude per §3; **discovery of
  substandard output routes to the owner every time.**
- **Suspected-but-unverifiable → cross-agent second opinion (binding)** — if you suspect a build
  failure or any file/data/sync/guard/code may not be flawless but **cannot verify it** (environment
  quirk, tool error, blocked access, ambiguous result), hand it to the **other agent** for an
  independent second opinion before concluding it is fine — never guess it away or claim "works"
  unverified. The receiving agent runs an independent review + test in a clean environment and
  returns explicit **PASS/FAIL** + fresh evidence, surfaced in the next turn with a repair brief if
  FAIL. Applies Claude↔Cursor equally.
- **Work log to disk before turn ends (binding — Claude cannot see chat)** — every session that
  produces or verifies work MUST update **`docs/workflows/AGENT_HANDOFF_LOG.md`** in the **same turn**
  and **commit** that update (alone or with the task commit) before the response ends. Chat-only
  summaries are invisible to Claude Code — **unlogged work = task failure** even if code shipped.
  Required fields: branch, HEAD, PR, tree, build status, explicit PASS/FAIL, commits, files touched,
  commands run, acceptance evidence. Keep last 3 sessions only. See §1.1 J.
- **Improvement backlog to disk (binding — aid Claude and future agents)** — every session that
  reviews code, data, docs, guards, sync output, or UI MUST append credible improvements to
  **`docs/workflows/AGENT_HANDOFF_LOG.md` → Improvement backlog** when noticed — even if out of
  scope for the current brief. Include: guards to add, pipeline hardening, doc drift fixes, UX
  gaps, merge/reconcile items, and process improvements. **Distinct from Owner visibility findings**
  (§1.1 H — spec defects); backlog items are proactive enhancements. Never bury suggestions in chat
  only. When a rule gap is found, add or tighten the owning rule in the **same turn** if agent-fixable.
  See §1.1 J.
- **One fact, one file** — before creating a new doc/rule file or restating a number/list/table,
  update the existing owner instead. Restating a fact in a second file is a duplication bug on
  creation. Cross-reference, never re-state. Fewer destinations = fewer contradictions.
- **Single-writer git authority (binding)** — **Cursor is the ONLY agent** that commits pipeline/data/code,
  pushes, opens/closes/merges PRs, or creates branches. **Claude Code** does read-only review, diagnosis,
  briefs, and issues an **APPROVAL verdict only** — never merges, closes, pushes, or commits repo work
  (its own review-note artifacts excepted when no writer is active). **One platform writes** — no
  duplication or races. See §1.1 K.

**These rules bind EVERY agent equally — Claude Code AND every Cursor agent (Auto, cloud
agents, background agents). No agent is exempt.** Cursor agents additionally reload
**`.cursor/rules/ledger-pre-ingest.mdc`** every turn **before** ingesting owner/Claude instructions
and **before** acting or responding, and must follow that file’s Cursor corpus to absolute
compliance. The owner approved these standards once; they are concrete and persist until the
owner explicitly changes them. If you are about to ask the owner something, or deviate from a
format — STOP and check this file and the file it points to first. The detailed specs already
exist; use them. Re-requesting approved information — by any agent — is the specific failure
this file was created to stop.

---

## 1. How to operate (the anti-ignore rules — these are why this file exists)

- **The spec already exists — read it, never re-ask.** Before asking the owner ANY question
  about a standard, format, count, or past decision, read the file that owns the answer
  (table in §2). Only ask if the answer is genuinely not in any file — and then say
  "this isn't recorded in <file>" so the gap is known. Re-requesting approved information is
  the #1 failure this file prevents.
- **A spec violation is never a question.** If data or UI breaks a written rule, fix it
  against the rule decisively. Do not ship it, do not ask if it's acceptable.
- **Be decisive — the owner's decision boundary is LAW.** The owner decides ONLY the
  physical/visual layout, design, and product/editorial direction of the platform. EVERY other
  decision — code, data, sources, sequencing, tooling, what steps we take to progress — is the
  agent's to make decisively, without asking. Do not lay out code/data options and ask which to
  pick; pick the right one per the specs and execute. Escalate to the owner ONLY when a choice
  changes what the platform looks like / how it is laid out, or is an irreversible/destructive
  action. Re-routing routine code/data calls back to the owner is the exact time-wasting failure
  this rule bans.
- **The loop that ends the ping-pong.** Owner gives input + reviews the visual side only.
  Claude decides every code/data question, DIAGNOSES the root cause + solution, and writes an
  EXPLICIT brief carrying both the problem AND the fix (never bare "try again"). **Cursor is the
  ONLY agent that collects data, runs syncs, and creates/edits files** — Claude does read-only
  inspection to diagnose and verify, and never collects/syncs/generates data itself (two agents
  writing similar data into separate places is banned). Cursor executes the brief EXACTLY and
  makes NO independent assumptions — if ambiguous, it stops and asks. Claude reviews Cursor's
  output for correctness before acceptance; anything short of standard is rejected and
  re-briefed with the specific fix. **Single source of truth:** when data seems missing, check
  whether it already exists in another generated file (usually it does) and the real fix is
  wiring/joining to it — never re-collect into a new location. Standard for everything that
  ships: flawless, 100% accurate, pristine, presented exactly to spec.
- **One file per destination view — never a mega-bundle.** Each data category is written to its
  own file named/structured for the profile section or search location it feeds, keyed by
  `bioguideId`, so it is independently wipeable and verifiable. Do not bundle multiple
  categories for a member into one blob. Grow coverage in small reviewed batches (1 → 5 → 10 →
  …), never one massive collection.
- **Scale from locked migrated profiles — no circling.** The **7 migrated profiles** in
  `lib/data/generated/profiles/_manifest.json` are the concrete reference (S000033, O000172,
  M000355, M001184, W000817, C001098, P000197). Never scale a pipeline whose batch output is not
  approved. A written spec is settled until the owner changes a *visual/design* element — do not
  reopen it or re-tune the same filter for the Nth time. Quality dilution (low-quality data
  burying good data) IS regression. Progress is shipped/verified/committed output, never
  "steps being taken."
- **Verify, never trust "done."** Independently check every completion claim (especially
  Cursor's) against the actual repo/data/build before accepting it. "It builds" ≠ "it's correct."
- **Commit the instant work passes review — NON-NEGOTIABLE.** The moment any Cursor action,
  generated data, or file is confirmed complete and passing quality/acceptance criteria, it is
  IMMEDIATELY committed (locally, for the owner to push) — never left dirty in the working tree.
  This applies automatically on every sign of completion or moving on from a task; no one should
  have to ask each time. Verified work sitting uncommitted is treated as a bug. **Cursor commits
  immediately when green; Claude Code never commits application work** (§1.1 K). Losing or
  re-deriving already-completed, verified work is the single most wasteful failure and must not
  recur.
- **The 7 migrated profiles are the locked spec.** S000033, O000172, M000355, M001184, W000817,
  C001098, P000197 are the concrete reference. The pipeline scales the SAME components and SAME
  checklist to the remaining 531 members — it never redesigns them. Fix the script/extractor
  that produced bad data; never hand-clean one member and call it done.
- **Substandard = surface immediately (owner visibility — binding).** Any file, generated data
  artifact, sync/process, guard result, doc, config, or UI output you engage with or review that
  is **not 100% flawless** to the written spec MUST be **brought to the owner's attention in the
  same turn** — never silently worked around, deferred without flag, or buried in a passing
  summary. The owner must never discover defects you already saw. Use the **Owner visibility
  finding** block (§1.1 H). Routine agent-fixable repairs proceed without permission; **visibility
  is mandatory even when you are also fixing.** Credibility *tradeoffs* route to Claude; **discovery
  of substandard output routes to the owner every time.**
- **Suspected-but-unverifiable → cross-agent second opinion (binding).** If you suspect a build
  failure or any file/data/sync/guard/code may not be flawless but **cannot verify it**, hand it
  to the other agent for an independent second opinion before claiming pass — never guess it away.
  Use **Cross-agent second opinion** block (§1.1 I). Receiving agent returns explicit PASS/FAIL +
  fresh evidence; FAIL gets a repair brief. Applies Claude↔Cursor equally.

### 1.0 The three-stage build loop (binding on BOTH agents — owner directive)
Every task runs this loop. It is mirrored verbatim in `.claude/rules/CLAUDE_CODE_OPERATING_MANUAL.md` §12A.
```
STAGE ONE — Claude: writes the spec (10-part template) · finds edge cases · identifies risks ·
            creates the testing requirements.
STAGE TWO — Cursor: implements the spec EXACTLY (no independent choices) · performs the required
            testing · creates an implementation report · lists every assumption made.
STAGE THREE — Claude (ASSUME CURSOR IS INCORRECT): review every changed file · review every test ·
            attempt to discover bugs · attempt to discover regressions · verify the requirements ·
            challenge the implementation decisions · identify the remaining risks.
            Claude MUST attempt to REJECT before approving. Problems found → return to STAGE ONE.
REPEAT UNTIL ACCEPTED — **and "accepted" means an explicit Claude APPROVAL on the exact merged SHA,
never the mere absence of a REJECT within some window.** A PR sits unmerged until that APPROVAL
exists, no matter how green CI is or how much time has passed since it opened.
```
Acceptance ships with the Final Report + stated remaining risks — never a bare "approved."

Every Claude Code response that touches this loop ends with a concrete, paste-ready directive for
Cursor — a restated fix brief on REJECT, or an APPROVAL plus the next roadmap task on PASS. Never a
status update with nothing for Cursor to act on. Full rule: `.claude/rules/CLAUDE_CODE_OPERATING_MANUAL.md`
§12B. Cursor should expect every Claude review/check-in to arrive this way and treat one that
doesn't as itself a defect to flag back.

### 1.1 Agent handoff, review, and completion (binding — CRITICAL)

**This section is non-optional.** The owner must never prompt "give me the handoff report" or
"follow your rules." If a turn ends without the required block when triggers fire, that turn is
a **failed turn**.

These rules reinforce §1 ("Verify, never trust 'done'"), the ping-pong loop (Claude diagnoses +
briefs; Cursor executes), and §6 ("Read the real error before any restart").

#### Trigger matrix (when to output what — no judgment calls)

| Situation | Required output | Retry? |
|-----------|-----------------|--------|
| Attempt 1: error, timeout, wrong counts, missing artifact | **Review for Claude** (§1.1 F) at end of SAME response | One different approach allowed |
| Attempt 2+: same task still not meeting brief acceptance | **Claude handoff report** (§1.1 F) + **STOP** | No unless brief says so |
| Exit 0 but brief acceptance not met | **Review for Claude** — exit code is not success | Fix or STOP |
| Claiming "complete" | Commit hash + `git show`/artifact paste from THAT commit **and** `AGENT_HANDOFF_LOG.md` updated + committed same turn (§1.1 J) | N/A |
| End of any work/verify session (audit, remediation, guard, rule change) | **`AGENT_HANDOFF_LOG.md` updated + committed** before response ends (§1.1 J) | Chat-only report forbidden |
| Prior session report recycled | **Forbidden** — regenerate from current `git status` + logs | N/A |
| Any substandard file/data/process discovered during read, sync, audit, or review (not 100% flawless to spec) | **Owner visibility finding** (§1.1 H) in SAME response — even if out of scope or you are also fixing | Fix in-scope if brief allows; else flag only |
| Suspected flaw but cannot verify (env quirk, blocked access, ambiguous pass) | **Cross-agent second opinion** (§1.1 I) before claiming pass | Other agent reviews independently |

#### A. Autonomous delivery (binding)

When any trigger fires, the agent MUST:

1. **Not** ask the owner whether to produce the report
2. **Append** the required block as the **last section** of the response (visible without scrolling past filler)
3. Include **fresh evidence** — run `git log -1`, `git status --short`, `rg`/`tail` on the tee'd log **in this session** before writing
4. List **every file touched** (path + created/modified/deleted) and **every command run** (exact string)
5. State **HEAD commit hash** and whether working tree diverges

Skipping any of the above = the report is **stale or incomplete** and Claude will reject it.

#### B. Two-or-more-failure handoff (binding)

When ANY task fails **2 or more attempts** before meeting brief acceptance, the agent MUST **NOT**:

- Restart the same approach blindly
- Ask the owner to "try again" without diagnosis
- Claim completion without commit hash + artifact evidence
- End the turn without the **Claude handoff report**

The handoff report MUST contain (§1.1 F template):

1. **Objective** — brief task ID + one sentence
2. **Failure count** — each attempt: exact command, runtime, exit code, error line from log
3. **Root cause** — underlying problem(s), not symptoms
4. **Process log** — ordered steps: what was read, decided, built, run, verified
5. **Files & code** — table: path | action | what changed (function/script/data)
6. **Commits** — hashes for work claimed done; note unpushed
7. **Tree state** — `git status` summary; WIP not in commits
8. **Needs fixing** — concrete next steps for **Claude** (not owner menus)
9. **Evidence gaps** — what was NOT verified; why
10. **STOP** — yes/no per brief

#### C. First-failure / substandard review (binding)

When attempt 1 fails OR output is slow/incomplete/below brief standards, append **Review for
Claude** (§1.1 F) in the **same response**. Do not wait for attempt 2 if acceptance criteria
are clearly unmet (e.g. votes still 10 when brief requires 30).

#### D. Completion claims (reinforce)

A task is **complete** ONLY when **all** are true:

1. A **commit hash** exists for the verified work (see §1 commit rule; owner may withhold push)
2. The **acceptance artifact named in the brief** is pasted fresh from that commit/run (`git show <hash>:path` or log `rg`)
3. **`docs/workflows/AGENT_HANDOFF_LOG.md`** is updated with this session's evidence and **committed**
   in the same turn (§1.1 J) — Claude Code reads the file on disk, not chat history

"Complete" without both = **task failure**. "It builds" or "sync finished" alone is not
completion. Re-listing work accepted in a **prior** Claude review as new progress = **verification theater** (reject).

#### E. Anti-stale rules (Claude rejects these — binding)

- Never paste smoke/summary JSON from memory or a prior session
- Never cite a commit hash without verifying it is current HEAD or the named commit
- If pasted evidence contradicts code on disk (`git show`, `cat` artifact), **state the discrepancy** — do not paste
- Reports must include **timestamp of this session** and commands run **this session**
- "Brief A–C complete" (or any multi-task complete) requires **per-task** commit + evidence — never one blanket claim

#### F. Copy-paste templates (use verbatim structure — fill every field)

**After 2+ failures — Claude handoff report:**

```markdown
## Claude handoff report

**Brief / task:** [e.g. Brief B v3 Task 4]
**Objective:** [one sentence]
**Session:** [date]; **HEAD:** `[git rev-parse --short HEAD]`

### Attempts
| # | Command | Runtime | Exit | Error / outcome |
|---|---------|---------|------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Root cause
[problem(s), not symptoms]

### Process log (ordered)
1. Read: [files]
2. Decided: [decision]
3. Built/edited: [files + what]
4. Ran: [commands + logs]
5. Verified: [method — independent of producer if data]

### Files & code
| Path | Action | What changed |
|------|--------|--------------|
| | | |

### Commits (this task)
- `[hash]` — [message]
- Uncommitted WIP: [list or none]

### Needs fixing (for Claude)
1. [concrete step]
2. …

### Evidence gaps
- [what not verified + why]

**STOP:** [yes/no per brief]
```

**After attempt 1 failure or substandard output — append under the task:**

```markdown
## Review for Claude

**Brief / task:** [e.g. Brief B v3 Task 3]
**HEAD:** `[hash]` · **Tree:** [clean / dirty: files]

| Check | Expected (brief) | Actual (this run) |
|-------|------------------|-------------------|
| Runtime | | |
| Artifact path | | |
| Count / status | | |
| Commit for this task | | |

**Commands run (this session):**
- `[exact command]` → [outcome]

**Files touched (this session):**
- `[path]` — [created/modified]

**Fresh evidence:** 
```
[paste from tail/rg/cat on current log or git show — not from memory]
```

**Code vs evidence:** [match / DISCREPANCY: …]
**Blockers:** [human-only | agent-fixable]
**STOP appropriate:** [yes/no]
```

#### G. Three-strike turn flow (binding — seamless, no owner reminders)

This is how failure reporting integrates into **every conversation turn** without the owner
asking. A **strike** = one attempt at the brief task that does not meet acceptance.

**Strike 1 (first failure or substandard output):**

1. Read the tee'd log / error — diagnose root cause (§6).
2. **In the SAME response**, after your work narrative, append **Review for Claude** (§1.1 F).
3. **In the SAME turn**, if the brief allows retry and the fix is agent-fixable: execute **one**
   corrective attempt with a **different** approach (e.g. scope with `--members`, clear stale lock,
   read log before re-run). Do **not** ask the owner to retry.
4. If the corrective attempt completes acceptance → report commit hash + artifact; no handoff needed.

**Strike 2 (second failure on the same brief task):**

1. **STOP** all further retries on that task.
2. End the response with the full **Claude handoff report** (§1.1 F) only — no filler, no
   "I'll try again," no asking the owner anything.
3. List all three strikes if strike 1 included a same-turn retry (counts as attempt 2).

**Strike 3+:** Forbidden unless the brief explicitly authorizes another attempt. Produce handoff;
wait for Claude.

**Same-turn structure (copy this shape):**

```
[Work narrative: what you did, files, commands]

## Review for Claude          ← required after strike 1
…filled template…

[Optional: strike-1 corrective retry + outcome]

## Claude handoff report      ← required after strike 2+; replaces further work
…filled template…
```

**Stale reports:** Claude treats any handoff/review that omits HEAD hash, `git status`, exact
commands this session, or that pastes evidence contradicting `git show`/logs as **rejected**.
Regenerate from disk — never recycle a prior session's paragraph.

#### H. Owner visibility finding (binding — every substandard discovery)

**Trigger:** You read, sync, audit, test, or review anything that is **not 100% flawless** to
the written spec — data quality, guard failure, path drift, stale docs, partial wipe, silent
empty, layout-number drift, office-resolution error, process without `--members`/timeout, or any
other defect — whether or not it is in the current brief scope.

**Required in the SAME response** (dedicated section; do not bury in prose):

```markdown
## Owner visibility finding

| Field | Detail |
|-------|--------|
| **What** | [one-line defect summary] |
| **Where** | [path, script, profile bioguideId, or commit] |
| **Evidence** | [fresh rg/cat/git show/tail — not memory] |
| **Severity** | [P0 data-loss / P1 wrong-shipped / P2 doc-drift / honest-gap vs bug] |
| **Repair** | [agent-fixable now | needs Claude brief | needs owner visual decision] |
| **Action this turn** | [fixing / flagged only / blocked by scope] |
```

Multiple findings → one table row each. **Honest gaps** (genuine missing verified record) are
not defects — flag only when the *presentation* mislabels them (silent empty, fetch-failed shown
as gap, etc.). The owner must never be the first to learn of a defect you already observed.

#### I. Cross-agent second opinion (binding — suspected but unverifiable)

**Trigger:** You **suspect** a build failure, guard flake, data defect, or environment issue but
**cannot verify** the outcome (tool error, blocked log access, ambiguous exit code, partial test
run, cannot reproduce locally).

**Required before claiming PASS or "works":**

```markdown
## Cross-agent second opinion needed

| Field | Detail |
|-------|--------|
| **Suspected issue** | [one-line summary] |
| **Where** | [check, file, command, commit] |
| **Why unverifiable here** | [blocked access / ambiguous / env quirk] |
| **Evidence so far** | [fresh command output — not memory] |
| **Ask receiving agent** | [independent re-run + explicit PASS/FAIL + repair brief if FAIL] |
```

Cursor ↔ Claude equally. **Never** close a suspected defect without the second opinion when you
could not verify. Credibility tradeoffs still route to Claude; **unverified "pass" is banned.**

#### J. Agent handoff log for Claude review (binding — CRITICAL)

**Claude Code cannot see Cursor chat.** The only durable handoff for review continuity is
**`docs/workflows/AGENT_HANDOFF_LOG.md`** on disk (formerly `AUDIT_DEBT_BRIEF.md` — stub redirect
at old path). The owner must never have to ask "did you log this?" — if the file is stale or
missing the session, the turn **failed** regardless of chat quality.

**When (every time):** end of any turn that audits, remediates, syncs, adds guards, changes rules,
verifies PASS/FAIL, opens/updates a PR, or claims progress. **One combined commit** with task work
is fine; a **docs-only follow-up commit** in the same turn is also fine. **Ending without the file
updated = violation.**

**Improvement backlog (same file, binding):** whenever you notice a credible fix, guard, pipeline
improvement, doc correction, UX gap, or process enhancement — **append a row** to the
**Improvement backlog** table in this file. Do this even when the item is out of scope for the
current brief. Mark status `open` / `done` / `blocked` / `wontfix`. If the improvement implies a
missing agent rule, add or tighten the rule in `.cursor/rules/ledger-core-rules.mdc` (or the owning
file) in the same turn when agent-fixable. **Owner visibility findings** (§1.1 H) are for spec
defects; the backlog is for proactive enhancements — both must reach disk, neither only in chat.

**What to write (mandatory fields):**

```markdown
**Current state:** branch · HEAD · PR URL · tree clean/dirty · prebuild/build status

## Improvement backlog
[append new rows when noticed — never chat-only]

## Latest session — [title] ([COMPLETE | BLOCKED | PASS | FAIL])

### Objective
[one sentence from brief]

### Verdict / outcome
[explicit PASS/FAIL or completion status — not vague]

### Commits
- `[hash]` — [message]

### Commands run (this session)
- `[exact command]` → exit [code] / outcome

### Files touched
| Path | Action | What changed |

### Acceptance evidence
- [artifact paths, counts, test names, log tails — fresh from this run]

### Open / next
- [blockers or none]
```

**Retention:** keep **Current state** fresh; keep **last 3** numbered entries under **Session log**;
drop oldest when adding a 4th. **Improvement backlog** rows persist until status changes — do not
truncate the table to "last 3."

**Anti-patterns (reject):** chat-only report; chat-only suggestions; stale HEAD in file; session
described in chat but absent from file; "will log next turn"; logging a prior session's work as if new.

#### K. Single-writer git authority (binding)

**Cursor** is the **only** agent that may:

- `git commit`, `git push`, branch create/delete/rebase
- Open, close, or merge GitHub pull requests
- Write pipeline output to `lib/data/generated/` (sync/migrate scripts)

**Claude Code** may:

- Read files, inspect artifacts, run read-only verification
- Diagnose, brief, and issue explicit **APPROVAL** / **REJECT** verdicts
- Commit **review/governance notes only** when no Cursor writer is active

**Claude Code must never** merge, close, push application code, or race Cursor on the same branch.
If both agents could write, **stop** — Cursor owns the tree.

**Merging is gated on an explicit Claude APPROVAL for the exact SHA being merged — not on CI alone,
not on elapsed time, not on the PR's own "STOP for review" text being present.** Before merging any
PR, Cursor checks for a Claude review comment or a matching `AGENT_HANDOFF_LOG.md` entry on that
commit. Finding none is not silence-implies-consent — it means the review hasn't happened yet, and
the PR stays open. Finding a REJECT/REQUEST_CHANGES means the PR does not merge until a new commit
answers it and a fresh APPROVAL lands on the new SHA. See HARD RULES "Approval before MERGE."

#### L. Living source registry (binding)

`docs/OBJECTIVE_SOURCES.md` is the **source constitution** — the canonical, always-consult-first
registry of approved sources, lean labels, tiers, and the key-routing matrix (which key/command
unlocks which data need). It is a **LIVING DOCUMENT**:

- **Consult it FIRST** before researching any new data source or key routing. Do not re-research
  settled routing that the registry already answers.
- Any agent that discovers a **better path** — a keyless official mirror, a new endpoint, a dead
  feed, a changed rate limit, a superior source, a retired API — **MUST update the relevant row in
  the SAME session** (routing knowledge lives on disk, never in chat). Founding example: BEA
  Regional Price Parities blocked on a key → FRED's keyless CSV mirror of the same official series.
- The **corroboration floor** for below-standard/unobtainable data is defined in the registry
  (rule 4) and cross-referenced by `.cursor/rules/ledger-data-policy.mdc`: a single below-standard
  provider is never shown; 2+ independent providers may show only at `'alleged'`, visibly flagged.
- `KEYS.md` owns per-key SET/EMPTY status only; the registry owns routing. One fact, one owner.

#### M. Keep files accurate (binding — both agents)

Every agent, every session that touches a file, generated data artifact, or doc that claims
**done / complete / locked / filled** status MUST **verify that claim against the real artifact**
(render, query, count, manifest field, guard output) the **same turn**. Correct stale status in
the owning file or surface an **Owner visibility finding** (§1.1 H). A regression that silently
un-does prior verified work is a **first-class bug** — hunt it; never trust a label because a doc
says so. **Status is earned by evidence, never by a label.**

Claude's full standing orders: `.claude/rules/CLAUDE_CODE_OPERATING_MANUAL.md` §11. Cursor implementation
discipline: `docs/CURSOR_IMPLEMENTATION_MANUAL.md` §6. Do not restate §11 here.

---

## 2. Where the authoritative detail lives — read the file that owns the answer

| If the work touches… | Read this first |
|----------------------|-----------------|
| What a complete profile requires; data layers; what "done" means | `PILOT_PROFILE_CHECKLIST.md` |
| How batches are collected/reviewed/sized (the scaling loop) | `docs/workflows/BATCH_SCALING.md` |
| What counts as a "Said" statement (floor remark vs. submission boilerplate/fragment) | `PILOT_PROFILE_CHECKLIST.md` → Said acceptance rule |
| How much shows per row/article; truncation; counts per section; layout | the demo components in `components/politicians/` — these ARE the locked layout |
| UI copy tone, banned words, Said→Did diff format | `.cursor/rules/ledger-editorial-voice.mdc` |
| Source tiers, corroboration, banned sources, destination-view map | `.cursor/rules/ledger-data-policy.mdc` |
| Approved sources, lean labels, key-routing matrix, corroboration floor (source constitution) | `docs/OBJECTIVE_SOURCES.md` |
| Which source/API feeds a data need | `lib/data/SOURCE_LOOKUP.md`, `lib/data/sourceCatalog.ts` |
| What's done / in progress / blocked; phase status | `PROGRESS.md` |
| API key SET/EMPTY; sync commands | `KEYS.md`, `docs/SETUP.md` |
| Surfacing substandard files/data/processes to the owner | `.cursor/rules/ledger-core-rules.mdc` § HARD RULES + §1.1 H |
| Agent handoff log for Claude review (sessions + improvement backlog) | `docs/workflows/AGENT_HANDOFF_LOG.md` — **§1.1 J (mandatory same-turn commit)** |
| Cross-agent second opinion when unverifiable | `.cursor/rules/ledger-core-rules.mdc` § HARD RULES + §1.1 I |
| Single-writer git authority (Cursor only commits/pushes/merges) | `.cursor/rules/ledger-core-rules.mdc` § HARD RULES + §1.1 K |
| Keep files accurate — claimed done/complete vs real artifact | `.cursor/rules/ledger-core-rules.mdc` §1.1 M · `.claude/rules/CLAUDE_CODE_OPERATING_MANUAL.md` §11 |
| Cursor implementation role, testing, reporting format | `docs/CURSOR_IMPLEMENTATION_MANUAL.md` |

---

## 3. Data credibility (non-negotiable)

> Corroboration, banned sources, destination-view map: `.cursor/rules/ledger-data-policy.mdc`

### Source tiers — canonical table (exact code values; never write "Tier 1/2/3/4")

| Code value | Meaning | Example sources |
|------------|---------|-----------------|
| `'official'` | Authoritative government record | congress.gov, FEC, senate.gov, house.gov, STOCK Act filings |
| `'nonpartisan'` | Established nonpartisan or official-derived research | GovTrack, OpenSecrets, Ballotpedia, AP, Reuters, ProPublica, unitedstates/congress-legislators |
| `'media'` | Named mainstream journalism outlet | NYT, WaPo, WSJ, Politico, The Hill — verbatim quotes with attribution only, never paraphrased |
| `'alleged'` | Contested claim about a person (not a confidence score) | Controversies + nested news claims only — see `ledger-data-policy.mdc` |
| `'unverified'` | Circulating claim with no verified sourcing | Maximum caveat, shown only when explicitly relevant |

- **Canonical `'alleged'` definition:** `.cursor/rules/ledger-data-policy.mdc` (permitted/banned
  surfaces, verbatim-only, multi-source transparency, outcome required, **repair before removal**,
  endorsements omit/`media` re-tier rule).
- **2+ independent approved sources** to display a `'media'`-tier **Said/statement** as verified.
  1 media source → **OMIT** (honest gap) — never demote a banned-surface record to `'alleged'`.
  AP/Reuters wire + a republisher = 1 source. News **listings** keep approved-outlet listing tier;
  corroboration is `isVerified`, not a tier rewrite.
- **Banned always:** Wikipedia, social-media posts (uncorroborated), anonymous sources,
  campaign/PAC press releases as sole source on banned surfaces, anything without a URL + date.
- Journalism quotes are **verbatim, in quotes, attributed, dated, linked** — never paraphrased.
- **Honest gaps:** show `"No verified record available"`. Never fabricate or paraphrase to fill.
- **Source exhaustion (binding):** before an honest-gap for any category, exhaust the ordered
  source route in `SOURCE_LOOKUP.md` / `OBJECTIVE_SOURCES.md`. Do not honest-gap while a higher
  route is untried; a failed higher route is UNVERIFIED/`fetch-failed`, not a silent skip.
- **A "Said" record is a spoken floor remark (e.g. opens "Mr. SANDERS. Mr. President, ...") or
  a verbatim sourced media quote — NEVER amendment/resolution submission boilerplate, clerk
  procedural text, or senator-list fragments**, even if verbatim and attributed.

---

## 4. Locked profile layout (the owner's standing directives)

> Full voice/copy rules: `.cursor/rules/ledger-editorial-voice.mdc`

- **Unified "Where They Stand" box** — Where They Stand + The Record + Key Positions combine
  into ONE box. Key issues at top, each with its summarized piece of evidence directly under it.
  Use the Ballotpedia Key-Positions format as the presentation reference.
- **Collection quality** — every position/statement must be a substantive, complete, sourced
  claim. Ban bio-boilerplate ("X is a member of the US…") and truncated fragments ("Mr.").
  Can't produce a real claim → honest gap, never a fragment.
- **Voting Record** — presentation stays; the expandable drop-down must add REAL detail (bill
  summary + vote context), not repeat the collapsed headline.
- **Money & Donors** — Organizations & PACs section ordered ABOVE individual donors. Individuals
  are less prominent, below.
- **Track Record** — remove the Consistency Score entirely. Target **15** Said→Did / evidence
  records per profile where the verified record supports it (honest gaps otherwise).
- **Controversies** — its OWN menu/nav option toward the end of the profile, **directly
  navigable** (anchor/tab the user can jump straight to). No hard cap: short for most members,
  but scales up for high-profile figures (e.g. Trump) where the record is large. Always
  objective and sourced.
- **News** — collect relevant, impactful items; stick to quotes or fact-based statements.
  Approved-outlet **listings** stay `'media'`/`'nonpartisan'`; use `isVerified` for corroboration.
  Contested person-claims nested in an article may be `'alleged'` per data-policy.
- **Endorsements** — member's own statement or 2+ approved outlets; otherwise omit (never `'alleged'`).
  Documented public endorsements with a single approved outlet: re-tier to `'media'` + note — do not
  delete (repair before removal).
  Moderate depth — not a giant section.
- **Exact display numbers (from demo components — do not drift):** evidence quote 117 chars
  (`ExpandableEvidenceRow.tsx`); topic bill title 80 chars, 5 sponsored + 5 cosponsored per
  topic (`ProfileRecordByTopicPanel.tsx`); 8 donors per category (`DonorChart.tsx`);
  Said→Did first sentence 120 chars (`SaidDidPanel.tsx`); 3 org-vote links.

---

## 5. Operational guardrails

- **Port 3000 is the owner's — never start/kill anything on it.** Use 4100+ for any dev server;
  stop any server you start once verification is done.
- **Log long-running syncs:** tee to `/tmp/ledger-<script>.log` so failures are inspectable.
- **No full-corpus syncs in agent sessions.** Agent runs MUST scope every sync with
  `--members <bioguideIds>` (or equivalent) to the members under review. Full-corpus runs are
  scheduled CI / owner-initiated only. Add `--members` to any sync script that lacks it before
  running it in a session.
- **Every external `fetch()` in a sync/ingest script needs a timeout** (`AbortSignal.timeout`).
  An unguarded fetch can hang the whole script with no output.
- **Stay in scope.** Don't touch files outside the brief, rename things, or add abstractions.
- `npm run build` must pass before any commit. After data changes:
  `sync:legislators` → `verify:office` → `build`.
- **bioguideId** is the universal join key — never duplicate or alias it.
- Route pages (`app/**/page.tsx`) are server components — never add `'use client'` to them.

## 6. Integrity & anti-regression (each rule earned by a real failure — never relax them)

- **Failure is NEVER absence.** A fetch/sync/operation that errors is UNVERIFIED — never record
  it as empty, complete, or "No verified record." Distinguish a failed lookup from a genuine gap,
  and always preserve prior good data over a failed re-fetch. (A batch once recorded 17 fetch
  failures as 17 empty profiles and overwrote good data — this rule exists to prevent that.)
- **Every data-quality bug becomes a permanent, build-gated guard — for ALL pipelines, not just
  CREC.** When bad data is found anywhere (votes, FEC, news, statements…), freeze the VERBATIM
  bad example into a committed fixture + the correct good counter-example, and wire it into
  `npm run build` so a regression fails the build. Fixtures are APPEND-ONLY — they only grow,
  never reset. A fix without a regression guard is incomplete: it fixes the symptom and discards
  the evidence, which is the exact cycle that wasted the most time.
- **Verify independently of the producer.** Check the actual output artifact with a method that
  does NOT share the producer's logic — never validate a filter with the filter's own regex; read
  the RAW text/data. A verifier that shares the producer's blind spot turns "passed" into a
  false pass.
- **Read the real error before any restart or re-brief.** Never blindly restart a failed run or
  re-send a brief — read the tee'd log / actual error first. A blind restart repeats the failure
  and burns time. After **2 failures**, §1.1 B applies: STOP and hand off to Claude.
- **Profile, then partial-batch, before any full-scale run.** Before a full-corpus run, measure
  per-item cost and run a substantial partial batch (e.g. 20–50). Scale to the full set only after
  the batch passes review — catch data-quality AND throughput problems on 30 items, not 537.
- **Improve the process as it scales (binding).** At each expansion step
  (1→10→25→80→200→completion), measure **efficiency** (time/cost per unit) and **effectiveness**
  (quality/coverage/honest-gap correctness), identify the step to improve, apply it, and record the
  change in the owning process doc (`docs/workflows/BATCH_SCALING.md` § Improvement log for profile
  batches; `docs/workflows/DUAL_REFERENCE_ROADMAP.md` § Process improvement log for dual-reference
  conduits). A scale step without a recorded improvement pass is **incomplete**.

---

## 7. Agent operations (session start, delegation, guardrails)

### Session start (non-negotiable)

Before advising, coding, syncing data, or asking the owner for keys/email/scope, read:

1. **`.cursor/rules/ledger-pre-ingest.mdc`** — pre-ingest hygiene (keys/EMPTY/RETIRED confusion ban)
2. **This file** (`.cursor/rules/ledger-core-rules.mdc`) — binding rules
3. **`docs/workflows/AGENT_HANDOFF_LOG.md`** — what Cursor last shipped + improvement backlog (Claude reads this, not chat)
4. **`PROGRESS.md`** — milestones, blockers, next priorities
5. **`lib/data/SOURCE_LOOKUP.md`** — which source to use for each data need
6. **`KEYS.md`** — SET vs EMPTY env vars (never ask for values already documented)
7. **`REPO.md`** — canonical repo is `The-ledger` on `main`
8. **`PILOT_PROFILE_CHECKLIST.md`** — what a complete profile requires
9. **`docs/AGENT_INDEX.md`** — navigation map (canonical index; do not maintain rival lists)

Task-specific: **`AGENTS.md`**, **`.cursor/rules/ledger-data-policy.mdc`**, **`.cursor/rules/ledger-editorial-voice.mdc`**

Do **not** use **`docs/archive/`** for current policy.

### Owner delegation

The agent is delegated to:

- Register for API keys, write values to `.env.local`, push GitHub secrets via `scripts/setup-github-secrets.sh`
- Run sync/build/verify pipelines without stopping for routine owner actions
- Pursue vendor access (forms, email to opendata@ / webmaster@) when a key is required

**Owner email for registrations:** `robbie.ryan312@gmail.com` (canonical in `KEYS.md`).

Reference files before asking the owner anything: `KEYS.md`, `REPO.md`, `PROGRESS.md`,
`lib/data/SOURCE_LOOKUP.md`, `lib/data/sourceCatalog.ts`, `.env.local` (SET vs EMPTY only).

### Do not

- **End a work/verify turn without updating + committing `docs/workflows/AGENT_HANDOFF_LOG.md`** (§1.1 J)
- Ask the owner if they are "ready to continue" — proceed until blocked
- Ask for owner email — it is in `KEYS.md`
- Never request a key for a source absent from the approved matrix in `docs/OBJECTIVE_SOURCES.md`; OpenSecrets deferred in `SOURCE_LOOKUP.md` (see `ledger-pre-ingest.mdc`)
- Treat checklist `EMPTY` as owner debt, or imply vault access beyond SET/EMPTY (pre-ingest ban)
- Create or work in the legacy `code` GitHub repo
- Assume API keys are missing without reading `.env.local` key names
- Paste secret values into chat, commits, or tracked files
- Force-push to `main`

### When blocked

Only stop for: scope changes, major UX direction, or human-only verification (CAPTCHA, login.gov).
**Credibility tradeoffs** route to **Claude Code** per §3 — not the owner. When a vendor form hits
CAPTCHA or login.gov, open the URL in Chrome (`open -a "Google Chrome" "<url>"`) and continue
other work.

### Session state consolidation

**Primary:** every work/verify session logs to **`docs/workflows/AGENT_HANDOFF_LOG.md`** (§1.1 J) —
that is the durable handoff for Claude, including the **Improvement backlog**. **Secondary:** when
a milestone boundary is crossed, update **`PROGRESS.md`** status board — do not duplicate session
evidence there. Search before asking — grep `KEYS.md`, `REPO.md`, `PROGRESS.md`, `SOURCE_LOOKUP.md`
first. Log long-running scripts — tee to `/tmp/ledger-<script-name>.log` so errors are inspectable
from disk.
