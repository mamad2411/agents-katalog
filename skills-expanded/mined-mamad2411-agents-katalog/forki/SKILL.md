---
name: forki
description: >
  Decision-forcing skill. Reduces a problem to a binary fork via role decomposition
  (Decision / Execution / Validation / Recovery), surfaces trade-offs, forces a single choice.
  Triggers: "forki", "결정", "선택", "어느 쪽", "두 길", "갈피", "trade-off", "둘 중 뭐",
  "이전에 결정한", "다시 결정", "결정 기록",
  "decide", "decision", "choose between", "fork", "torn between",
  "past decision", "decided before", "record decision".
  Scope: any domain. Pre-PRD, pre-implementation.
version: 0.1.0
ssl:
  scheduling:
    anti_triggers:
      - "Generating slides for an already-made decision — use galmuri:deck preset decision-sandwich-6"
      - "Summarizing a long decision document — use galmuri:distill / explain / doc"
      - "Auditing whether a SKILL.md declares a decision contract correctly — use galmuri:skill-audit"
      - "Per-cycle quality loop on implementation — use galmuri:ralphi (or harnish:ralphi)"
      - "Three-or-more-way option exploration — collapse to binary first or step outside forki"
      - "Picking the option for the user — forki only forces the user to pick"
  structural:
    scenes: [Entry Check, Past-Decision Query, Binary, Reduction, Role Decomposition, Examples, Trade-off, Forced Choice, Comprehension Check, Asset Record]
    resumable: false
    branches:
      - "Step 0 finds prior decision → user picks `trust` (end, emit Reused report) or `reopen` (continue Step 1)"
      - "Step 3 attempt counter reaches 3/3 and a fourth back-jump would fire → abort with 'could not converge' instead of looping"
      - "Step 5 detects both options gain/lose the same axis → back-jump to Step 3 (not a real trade-off)"
      - "Step 6 user replies 'You choose' / 'both' / 'depends' → re-ask; never proceed on a non-A/B answer"
      - "Step 8 `.galmuri/` absent in CWD → skip the record step entirely; report `not-persisted`"
  logical:
    tools: [Bash, Read]
    side_effects:
      reads:
        - ".galmuri/assets/*.jsonl (Step 0, tag-filtered query; skipped when directory absent)"
      writes:
        - "/tmp/forki-{ts}.md (Step 8 sub-step 8.2 only, after `y` confirmation)"
        - ".galmuri/assets/decision-{ts}.jsonl (Step 8 sub-step 8.2 only, via scripts/record-asset.sh)"
      deletes: []
      network: []
    idempotent: true
    rollback: "Step 8 is opt-out (append-only); the Step 6 verdict stands regardless of whether the asset was written. Recorded JSONL lines are flat-file appends — remove the offending line manually if needed."
---

# galmuri:forki — Decision Forcing

Pattern: **binary → roles → trade-off → forced choice**.
This is a decision skill, not an explanation skill. If the user already has a verdict and only needs slides, route to `galmuri:deck` (preset `decision-sandwich-6`); if they need a summary of a decision doc, route to `galmuri:distill` / `explain` / `doc`.

## Entry Check

If invoked with no context (no decision topic, no problem description):
→ Ask: *"어떤 결정이 필요한가요? 고민 중인 상황을 설명해주세요. e.g. `Postgres vs SQLite for the new service`, `hire vs contract for the data role`."*
→ Wait for user response before proceeding to Step 0.

## Mode — HITL only

| Category | Steps | LLM authority |
|---|---|---|
| Auto query | 0 (query) | Full |
| Flow gate | 0 (decision) | None — `trust` / `reopen` |
| Verdict gate | 1, 3, 6 | None — user states it |
| Confirmation gate | 2, 5 | Propose only |
| Scaffold (skippable) | 4, 7 | Propose, user `skip` |
| Side effect (opt-out) | 8 | `y` / `n` |

LLM proposes; user confirms before next step. No autonomous mode.

## References (load once, reuse)

| File | First loaded at | Used for |
|---|---|---|
| `references/protocol.md` | Step 1 (first HITL) | All HITL prompts, response rule parsing, report templates |
| `references/asset.md` | Step 0 entry, or Step 8 entry if Step 0 was skipped | Bash query/record blocks for `.galmuri/` |

Each reference is loaded **at most once per forki invocation** and reused across all subsequent steps. See **Context Budget** below for the exhaustive read/write inventory.

## Step 0: Past-Decision Query (optional)

→ Load `references/asset.md` and **execute** the Step 0 query block as documented there. The full branching logic (`trust` / `reopen` / skip on absent / skip on no match) lives in `asset.md`.

## Step 1: Binary

Exactly **2 options**. 3+ → collapse to "do A vs everything else". "It depends" → ask user to constrain.

→ HITL via **Step 1 prompt** in `references/protocol.md`. Wait for explicit confirmation. Output: `A vs B`, one line.

## Step 2: One-Line Reduction

Compress to one sentence: *"Who executes X?"* / *"Who owns X?"* / *"What changes when X?"*

→ HITL via **Step 2 prompt** in `references/protocol.md`. Reject → propose alternative. Reject again → back to Step 1 (binary is wrong).

## Step 3: Role Decomposition (D/E/V/R)

**On entry**, output first line: `Step 3 attempt {n}/3`.
`{n}` starts at 1 on first Step 3 entry; +1 on each back-jump from Step 5/6/7. On `attempt 3/3`, this is the **last** allowed run (2 back-jumps total). If forki would back-jump to Step 3 again from this attempt, abort instead: *"forki could not converge after 2 back-jumps. Gather more context outside this skill."*

Fill all 4 roles per option:

| Role | Question |
|---|---|
| Decision | Who judges? |
| Execution | Who acts? |
| Validation | Who verifies? |
| Recovery | Who fixes when broken? |

→ HITL via **Step 3 prompt** in `references/protocol.md`. LLM may draft; user confirms or overrides each cell. Empty `?` → re-ask only those cells.

## Step 4: Three Examples (scaffold)

→ HITL via **Step 4 prompt** in `references/protocol.md`. Skip when concrete enough or user says `skip`. Record skip in report.

## Step 5: Trade-off

```
A: gains {X}, loses {Y}
B: gains {Y}, loses {X}
```

Axes: flexibility↔stability, speed↔safety, autonomy↔control.

→ HITL via **Step 5 prompt** in `references/protocol.md`.
- User says "don't care about X" → strike axis, propose new (stay in Step 5).
- Both options gain/lose the same → not real trade-off → back-jump to Step 3.

## Step 6: Forced Choice

> **Choice**: Option {A|B}. Reason: {one structural reason}.

→ HITL via **Step 6 prompt** in `references/protocol.md`. LLM **must not** answer for the user, **must not** signal a preference. *"You choose"* → reply: *"forki cannot decide for you."*

User truly cannot choose → back-jump to Step 3.

## Step 7: Comprehension Check (scaffold)

→ HITL via **Step 7 prompt** in `references/protocol.md`. Cannot answer all 3 → back-jump to Step 3. Skip on `skip`.

## Step 8: Record as Decision Asset (side effect, opt-out)

**Trigger**: runs only after Step 6 reaches a verdict (and Step 7 if not skipped). If forki aborts at any earlier step (counter 3/3, user `Stop`, Step 0 `trust` reuse, etc.), Step 8 does **not** run.

→ Load `references/asset.md` for sub-steps 8.0 / 8.1 / 8.2 (pre-check, HITL, write+record).

Side effect, not gate: the Step 6 verdict stands regardless of Step 8 outcome.

## Context Budget

forki is a **thinking** skill, not a reading skill.

Reference loading: see **References** section above (single source of truth).

Filesystem I/O:

| Operation | When |
|---|---|
| Read `.galmuri/assets/*.jsonl` (tag-filtered) | Step 0 only. Skip if directory absent. |
| Write `/tmp/forki-{ts}.md` | Step 8 sub-step 8.2 only, after `y` confirmation. |
| Append `.galmuri/assets/decision-{ts}.jsonl` (1 line) | Step 8 sub-step 8.2 only, via `scripts/record-asset.sh`. |

Maximum 2 references in context simultaneously (`protocol.md` + `asset.md`).

## Prohibited

- More than 2 options in Step 1
- Skipping any verdict gate (Steps 1, 3, 6)
- Treating Steps 4 / 7 as gates
- LLM picking the final choice in Step 6
- Interpreting `yes` / `ok` / `응` as confirmation. Always re-ask.
- Proceeding on silence
- `Both` / `depends` / `later` as final choice
- Reading files to "gather more info" (without explicit user request)
- Trade-offs where both options gain / lose the same thing
- Initializing `.galmuri/` from forki
- Recording an asset on user `n`. Honor opt-out.
- Inlining HITL prompts or report templates in this file — they live in `references/protocol.md`
- "FYI..." style supplementary information
- Verbose decision reports
