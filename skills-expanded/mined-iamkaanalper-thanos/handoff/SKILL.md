---
name: handoff
description: Standardized handoff templates for clear communication between orchestrator, subagents, and workflow phases. Use when coordinating multi-phase or multi-agent work.
keywords: [handoff, communication, templates, qa, escalation, coordination]
---

# Handoff Templates — Grok Edition

Clear, structured communication between the orchestrator and subagents (and across workflow phases) is one of the highest-leverage patterns from mature AI software teams.

This skill provides the Grok-native versions of the most useful handoff formats. They are intentionally concise and actionable.

## Core Principle

Every handoff must answer:
- What was done?
- What is the current state?
- What exactly is expected next (with acceptance criteria)?
- What files / context are required?

Vague handoffs are the #1 source of context loss and wasted subagent effort.

---

## Template 1: Standard Task Handoff (Most Common)

Use this when spawning or resuming a subagent for a discrete piece of work.

```markdown
## Task Handoff

**Objective:** <one clear sentence of what must be achieved>

**Context / Inputs:**
- Previous handoff / summary file: `path/to/previous.md`
- Relevant plan section: [link or excerpt]
- Key constraints: <e.g. "minimal change", "follow existing patterns exactly", "must be read-only">

**Deliverables Required:**
1. [Specific file + what it must contain]
2. [Another artifact]

**Acceptance Criteria (Definition of Done):**
- [ ] Criterion 1 (testable)
- [ ] Criterion 2
- [ ] Summary written to: `path/to/output.md`

**Known Risks / Watch-outs:**
- <e.g. "Do not touch auth middleware", "Performance is secondary to correctness here">

**When Blocked:**
- Write a clear blocker note to the output file
- Do not guess — escalate with specific questions
```

**Usage:** Paste (or reference) this as the core of the prompt when calling `spawn_subagent`.

---

## Template 2: QA / Review Handoff (PASS or FAIL)

Use when a reviewer or verifier finishes work.

### PASS Form

```markdown
## Review Result: PASS

**Scope:** <what was reviewed>
**Rounds:** N
**Issues Found & Fixed:** X total (bugs: Y, suggestions: Z, nits: W)

**Key Verifications Completed:**
- [ ] All open issues from previous round addressed
- [ ] No new issues of severity `bug` introduced
- [ ] Tests / type check / lint all green
- [ ] Security checklist passed (if applicable)

**Recommendation:** Ready for next phase / commit / merge.

**Artifacts:**
- Final review file: `path/to/review.md`
- Implementation summary: `path/to/summary.md`
```

### FAIL / Issues Form (Critical)

```markdown
## Review Result: ISSUES (Round N/3)

**Scope:** <what was reviewed>
**Open Issues:** K (bugs: A, suggestions: B, nits: C)

**Blocking Items (must be fixed before proceeding):**
1. **[bug]** `file:line` — <exact problem>
   - Expected: <what should happen>
   - Actual: <what is happening>
   - Suggested fix: <concrete, specific>
2. ...

**Non-blocking (fix in this round or next):**
- ...

**Stalemate / Disagreement (if any):**
- Issue X: Implementer position vs Reviewer position. Needs human decision.

**Next Action:** Resume the implementer with the review file. Address ALL open issues.
```

**Rule:** After 3 rounds with open issues of any severity, escalate instead of continuing the loop.

---

## Template 3: Escalation Handoff (After Repeated Failure)

Use when a subagent or phase has failed to deliver after bounded retries.

```markdown
## Escalation Required

**Original Objective:** <...>
**Attempts Made:** 3
**Current Blocker:** <root cause in one sentence>

**History of Failures:**
- Attempt 1: <what happened>
- Attempt 2: <what happened>
- Attempt 3: <what happened>

**Options (choose one):**
a) **Reassign** — Give to a different persona / approach (e.g. switch from general to specialist)
b) **Decompose** — Break the task into smaller independent pieces
c) **Revise** — Change the technical approach or architecture
d) **Defer** — Park for later (document why)
e) **Accept** — Ship with known limitation + explicit documentation

**Recommended Path:** <your analysis>
**Human Decision Needed:** [Yes — please pick from a–e and give any additional direction]
```

---

## Template 4: Diagnosis / Investigation Handoff (for fix / debug flows)

```markdown
## Diagnosis Report

**Issue:** <short description>
**Evidence Collected:**
- Logs / output: [key excerpts + locations]
- Git state: [recent commits, uncommitted changes]
- Runtime observations: [processes, ports, env]
- Code paths examined: [files:lines]

**Primary Hypothesis:**
<Most likely root cause with supporting evidence>

**Alternative Hypotheses (lower probability):**
- ...

**Proposed Fix Approach:**
<Concrete steps + files expected to change>

**Risk Assessment:** Low / Medium / High — <why>
**Premortem Notes:** <what could still go wrong even if this fix works>

**Next Step:** Human approval required before implementation.
```

---

## Template 5: Phase Completion / Workflow Handoff

Used at the end of a major workflow phase (e.g. after `execute-plan` or a swarm phase).

```markdown
## Phase Complete: <Phase Name>

**Deliverables Produced:**
- [Artifact 1] — location + one-line purpose
- [Artifact 2] ...

**State Summary:**
- What is now true that wasn't before
- Open questions / risks carried forward

**Handoff for Next Phase:**
- Required inputs: [list]
- Recommended starting point: <file or agent>
- Human checkpoint performed? [Yes/No + outcome]

**Total Time / Cost (if tracked):** ...
```

---

## Usage Rules (Grok Context) — Enforced Discipline

1. **When spawning subagents for anything non-trivial**, include (or reference) a handoff template in the prompt.
2. **After any review or verification step** (including calls to the new `verifier` agent), the output **must** use one of the QA PASS/ISSUES forms.
3. **Bounded loops (implement, execute-plan, swarm-lite phases)**: Every review-fix round **must** carry both a structured handoff **and** the output of `make_devqa_handoff_context` from the Task Lifecycle Ledger. Text-only "Round N/3" is no longer acceptable.
4. **Never proceed past a phase boundary** without either a clean PASS handoff or an explicit escalation decision (the 5 options).
5. **Keep bodies short.** If you need to transmit large context, put it in a file and reference the path.
6. **Human checkpoints** are mandatory after diagnosis, after plan creation, and after any round that still has open `bug` issues.
7. **Verifier involvement**: Any flow that is about to declare "done" or ship should have gone through the `verifier` agent (or equivalent check-work flow) and received a clean structured PASS handoff.

**Violations of rules 3 and 4 are now considered process failures** and should be recorded in the friction ledger.

---

## Quick Decision Guide

| Situation | Recommended Template |
|-----------|----------------------|
| Launching a focused implementation or fix task | Standard Task Handoff |
| Reviewer finished (clean or with issues) | QA PASS / ISSUES form |
| Subagent failed 3 times or is stuck | Escalation |
| Debug / fix workflow — investigation complete | Diagnosis Report |
| Major workflow phase done (plan, explore, etc.) | Phase Completion |

---

## Relationship to Other Grok Skills

- `implement` — Primary consumer of QA and Escalation templates. The review→fix loop should use the structured forms.
- `execute-plan` / `design` — Use Standard Task + Phase Completion handoffs between design → validation → implementation stages.
- `review` — Should output using the QA forms.
- Future `quality-loop` or `swarm-lite` skills will mandate these templates at every boundary.

---

**Adoption tip:** Start by requiring the QA PASS/ISSUES form on the next non-trivial `implement` run. The increase in clarity is immediate.

---

## Executable Companion: Task Lifecycle Ledger (Post-MVE Item 2 Fix)

The templates above are the **contract**. The root cause found during Post-MVE Item 2 research was that the 3-round Dev-QA + cumulative feedback + escalation logic existed **only** in these text templates and agent prompts — with no executable state.

**Solution (Grok-native, .grok/ only):**

```python
from bundled.skills.shared.task_lifecycle import TaskLifecycleLedger, make_devqa_handoff_context

ledger = TaskLifecycleLedger(session_id=...)
state = ledger.start_or_resume(task_id="my-devqa-task", objective="...")

# In each round
ledger.record_attempt(task_id, feedback="...", issues=[...])

if state.attempt >= 3:
    ledger.escalate(...)

# When spawning the next subagent for a bounded loop
extra_context = make_devqa_handoff_context(ledger, task_id)
# Inject extra_context["task_lifecycle"] into the prompt
```

**Benefits:**
- Real attempt count + accumulated feedback (not just text in the last handoff)
- Versioned, append-only audit trail
- Automatic escalation at max_attempts
- Works with worktree isolation and parallel agents

The text templates (especially QA FAIL "deneme N/3" and Escalation "3/3") remain the human/agent UX. The ledger is the single source of truth behind them.

See: `bundled/skills/shared/task_lifecycle.py` + its tests.

This is the first executable step toward making Grok's own Dev-QA discipline as robust as the rules it prescribes for user code.

---

This is the Grok-adapted version of the the original Claude Code AI software team system handoff discipline. Use it to reduce context loss and make multi-agent / multi-phase work reliable.

---

## Practical Pattern: Bounded Dev-QA Loop with Task Lifecycle Ledger

This is the recommended way to run a real 3-round review → fix loop using the executable ledger (instead of only text in handoffs).

### Recommended Orchestrator Helper (copy-paste ready)

```python
from bundled.skills.shared.task_lifecycle import TaskLifecycleLedger

def run_bounded_devqa_loop(
    task_id: str,
    objective: str,
    max_rounds: int = 3,
    implementer_prompt: str = "",
    reviewer_prompt: str = "",
):
    """
    Runs a bounded Dev-QA loop with real state tracking.
    Returns the final state + history.
    """
    ledger = TaskLifecycleLedger(session_id="current")
    state = ledger.start_or_resume(task_id, objective, max_attempts=max_rounds)

    for round_num in range(1, max_rounds + 1):
        # 1. Implementer round
        impl_context = make_devqa_handoff_context(ledger, task_id)
        # ... spawn implementer with impl_context injected ...

        # 2. Reviewer round (code-reviewer + verifier)
        review_context = make_devqa_handoff_context(ledger, task_id)
        # ... spawn reviewer ...

        # 3. Record result
        state = ledger.record_attempt(
            task_id,
            feedback="Reviewer findings here...",
            issues=["specific issue 1", "specific issue 2"],
        )

        if state.status == "escalated":
            break

    return ledger.get_full_history(task_id)
```

### When to Use This Pattern

- Any non-trivial `implement` run that you expect might need 2+ rounds.
- Long swarm phases with quality gates.
- Any place where you previously relied only on "deneme N/3" text in handoffs.

**Rule of thumb:** If you're about to write "(Round 2/3)" or "3. deneme" in a handoff, use the ledger instead.

See also: `bundled/skills/shared/task_lifecycle.py` and its tests for the full API.