---
name: bcc-clean-cut
description: >
  BCC minimal implement from locked PLAN.md (ponytail ladder + verify). Slash: /bcc-clean-cut · chat: bcc:clean-cut · "implement PLAN" after human APPROVE. Not for plan grill (use bcc-plan-spar).
argument-hint: "slash: /bcc-clean-cut · chat: bcc:clean-cut · [lite|full|ultra]"
metadata:
  short-description: "BCC minimal code from PLAN"
---

# bcc-clean-cut

**Job:** ship the **shortest correct code** that satisfies the active `PLAN.md`, then verify and **progress-only** 约减 the checklist.

**Deep source:** `ponytail` SKILL.md (coding ladder only — not review/audit family).  
**Does not:** interview the user for domain design, write ADRs, adversarial-review the plan, or **refine PLAN design while coding** — do that in **`bcc-plan-spar`** first.

---

## Workflow preflight (required — before any code edit)

**Do not** write product code until this check passes.  
If uncertain → **ask the user** (one question + recommended default). Never invent APPROVE.

### 1. Snapshot disk + session

| Check | Read |
|-------|------|
| Global map | `plans.md` / `progress.md` (if present) — which hardpoint is current? |
| Coding brief | `PLAN.md` (or `plan_path` from session) — exists? draft? locked? checklist open items? |
| Domain | `CONTEXT.md` / ADRs if referenced by PLAN |
| **`.bcc/session.json`** | Cross-session APPROVE — see [SESSION.md](../bcc-breaking-coding-chaos/references/SESSION.md) |
| Chat this session | **APPROVE implement** / “开写” / explicit skip-gate |

**human_APPROVE=yes** if **either**:

- Chat this session clearly APPROVE implement / skip-gate, **or**  
- Session file has `approved_for=clean-cut` **and** `plan_sha256` equals SHA-256 of current PLAN file bytes.

If session says approved but **hash mismatch** → PLAN changed after approve → `human_APPROVE=no` → ask re-APPROVE or plan-spar (do not code).

Echo:

`preflight · PLAN=… · human_APPROVE=yes|no|unclear · session=… · hash=match|mismatch|none · throughline=yes|no · recommend=code|plan-spar|throughline|ask-user`

### 2. Is **bcc-clean-cut** appropriate now?

| Situation | Suitable? | Do this |
|-----------|-----------|---------|
| No `PLAN.md` | **No** | Stop. Send to **`bcc-plan-spar`**. Ask if they meant to plan first. |
| `PLAN.md` is `_Draft — not locked_` | **No** | Stop. Finish **bcc-plan-spar** lock (or ask user to force-lock). |
| Checklist **all complete** / slice already shipped | **Usually no** | Ask: *“PLAN is done. New slice (plan-spar), throughline next, or re-open checklist?”* |
| PLAN topic **≠** user’s request / ≠ throughline current hardpoint | **Ask** | *“PLAN is for X; you asked to implement Y. Switch (plan-spar), or implement X?”* |
| Human **APPROVE implement** this session **or** valid `.bcc/session.json` approve (hash match) | **Yes** | Proceed to ladder |
| User said “implement / clean-cut” but **no** chat APPROVE and **no** valid session approve | **Ask** | *“PLAN is locked but not human-approved for coding. APPROVE implement, amend, or back to plan-spar?”* Default recommend: confirm APPROVE once. |
| User only asked “where are we?” | **No** | **`bcc-throughline`** |
| User still wants alignment / more grill | **No** | **`bcc-plan-spar`** |
| Multi-step endeavor, no throughline, large remaining work | **Warn + ask** | Optional: *“No plans.md cockpit — continue one-off cut, or create throughline first?”* Coding may proceed if PLAN is solid and user wants speed. |

### 3. Coding readiness checklist (all should be true, or user override)

1. `PLAN.md` exists and is **not** an unlabeled draft.  
2. Goal + checklist + verification sections are present enough to execute.  
3. **Human** has approved implement (chat **or** valid session file) **or** explicit override (“skip gate / just code this PLAN”).  
4. You know **which slice** this PLAN is for (title/goal matches the work / session.active_slice).  

If any item fails and user did not override → **do not code**; ask or route.

### 4. After preflight OK

Only then: optionally set session `status=coding` → read code flow → ladder → verify → 约减 PLAN → throughline writeback → on pass set session `status=done`, `approved_for=none` (consume one-shot approve per [SESSION.md](../bcc-breaking-coding-chaos/references/SESSION.md)).

---

## Preconditions (short)

1. Preflight passed (above).  
2. Trace the real code flow before editing.  
3. PLAN is the contract — no invented scope.

## PLAN freeze (execute, don't refine)

After human APPROVE, `PLAN.md` is a **frozen contract** for design content.

| Allowed during cut | Forbidden during cut |
|--------------------|----------------------|
| Implement within Goal / Approach / checklist / Verification | Rewrite Goal, Approach, Key decisions, Out of scope, Verification *design* |
| Check off `[ ]` → `[x]` only after implement + verify | Add new checklist items, “improve” wording of the brief, expand scope |
| **约减 progress only:** remove *completed* checklist rows / finished bulk that is already done | Mid-cut plan polish, second-guess architecture into the file |
| Note learnings in `progress.md` / `findings.md` | Quietly change the brief so APPROVE no longer matches reality |

**Conflict / plan wrong / can't meet Verification:** **stop coding** → say the conflict in one short line → **`bcc-plan-spar`** (or user amends PLAN) → **re-APPROVE**. Do not “fix the plan while shipping.”

No extra user ceremony: same gates as today; agent just won't rewrite the brief while coding.

## Intensity (default **full**)

| Level | Behavior |
|-------|----------|
| **lite** | Build what PLAN asks; name a lazier alternative in one line. |
| **full** | Ladder enforced. Shortest correct diff. Default. |
| **ultra** | YAGNI extremist on the **code**. May *mention* a speculative checklist item in chat; **still execute PLAN as approved** unless user sends you back to plan-spar. Never edit design sections to “improve” the plan. |

Echo: `bcc-clean-cut · full · PLAN.md`

Off only if user says stop bcc-clean-cut / normal mode for coding style (suite may still own process).

---

## Before the ladder

- Read every file the change touches; end-to-end flow.  
- **Bug fix = root cause**, not symptom — one fix where all callers route.  
- Ladder shortens the **solution**, never the **reading**.

## The ladder (stop at first rung that holds)

1. Does this need to exist at all? (YAGNI)  
2. Already in this codebase? Reuse.  
3. Stdlib?  
4. Native platform feature?  
5. Already-installed dependency? Never add a dep for a few lines.  
6. One line?  
7. Only then: minimum code that works.

## Rules

- No unrequested abstractions (interface-for-one, factory-for-one, config-for-never).  
- No scaffolding “for later”.  
- Deletion over addition when safe. Fewest files. Shortest **correct** diff.  
- Equal-size options → pick edge-correct one.  
- Deliberate ceilings: `# bcc: <ceiling>; upgrade when <condition>`.

## Never simplify away

Trust-boundary validation, data-loss handling, security, a11y basics, anything PLAN/user explicitly requires. Never lazy about understanding.

## Verify + PLAN 约减 (progress only)

- Run checks from `PLAN.md` Verification + checklist.  
- Mark items complete **only after** implement + verify.  
- Non-trivial logic: one minimal runnable check if none exist (no test framework sprawl).  
- **约减 `PLAN.md` (progress only):** check off done items; drop *completed* bulk; keep open checklist + unchanged Goal/Approach/decisions/Verification design. Narrative history → throughline `progress.md`, not a redesign of the brief.

## Output

Code first. At most a few short lines: skipped / add when.  
Pattern: `done → skipped: X, add when Y` unless user asked for a full report.

## Close

**Pass (required order):**

1. Trim/约减 `PLAN.md`.  
2. **Mandatory throughline writeback** per [WRITEBACK.md](../bcc-breaking-coding-chaos/references/WRITEBACK.md) — update `progress.md` (session block + tests), `plans.md` hardpoint status, `findings.md` only if global learning.  
3. Consume session approve (`approved_for=none`, `status=done`).  
4. Say the **slice** is done.  
5. **Next (strict):**
   - If any throughline hardpoint still open → only mention next hardpoint (or stop). **No** wrap-up talk.  
   - If **Gate A** (every hardpoint `complete`) **and** **Gate B** (not yet offered/closed) per [bcc-throughline](../bcc-throughline/SKILL.md) *Endeavor wrap-up* → **one** wrap-up offer (write `### Wrap-up offered` first, then ask global verify / what kind / skip).  
   - If already offered/closed → do not re-ask.

**Incomplete without writeback.** If writeback fails, fix files before claiming success.

**Fail:** log error in `progress.md`; 3-strike then escalate; after **2** verify fails → stop cutting, require **bcc-plan-spar** to revise PLAN.

## Invocation

| How | Example |
|-----|---------|
| After bcc-plan-spar | User APPROVE → agent loads **bcc-clean-cut** |
| Skill | `/bcc-clean-cut` · `/bcc-clean-cut ultra` |
| Chat | "bcc-clean-cut", "按 PLAN 最小实现", "implement the brief" |

## Hard rules

1. **Preflight first** — PLAN + human APPROVE (chat or valid session).  
2. PLAN is the **single** coding contract for the active slice; **across hardpoints** plan-spar rewrites that same file — **during cut, design content is frozen** (progress 约减 only).  
3. Read fully, then climb the ladder.  
4. No plan-review theater — that is bcc-plan-spar.  
5. Global progress **only** via throughline trio — **writeback mandatory** on success.  
6. If unsure → **ask the user**; never invent APPROVE.  
7. Infer fit from docs/context; suggest next skill — no formal state machine required.  
8. **Execute, don't refine** — design change → stop → plan-spar + re-APPROVE.

## What NOT to do

- Don't skip preflight or skip **writeback**.  
- Don't treat auto-review APPROVED as human APPROVE.  
- Don't put global phase history into PLAN.md.  
- Don't re-open unbounded product design mid-cut.  
- Don't rewrite Goal / Approach / decisions / Verification design while coding.  
- Don't “improve” PLAN mid-cut to match what you feel like implementing.
