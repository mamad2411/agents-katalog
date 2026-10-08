---
name: bulletproof
description: Use when building a feature, refactoring, fixing a complex bug, changing architecture, or starting any non-trivial coding task. 12-stage verified dev workflow from research to deploy.
---

# Bulletproof — Adaptive Development Workflow

> **Author:** Artemiy Miller ([@artemiimillier](https://github.com/artemiimillier)) · [Telegram](https://t.me/artemiymiller) · [who.ismillerr@gmail.com](mailto:who.ismillerr@gmail.com) · [TG Channel](https://t.me/+0jZamDvGOeZjOWE1)
> **Version:** 5.0 · March 2026
> **License:** MIT
> **Compatible:** Claude Code, Codex, Gemini CLI, Cursor, Windsurf, OpenCode

## Core Principle

**Code to solve problems, not code for code's sake.**

Before EVERY change ask: "Does this actually solve our problem? Is this the most efficient solution?"
If the answer isn't clear — stop, research alternatives, pick the best one.

---

## Pick Your Mode

Not every task needs the full pipeline.

| Size | Examples | Mode | Stages |
|------|----------|------|--------|
| **S** | Bug fix, small edit, 1-2 files | Lightweight | 1 → 4 → 5 → 6 → 7 → Gates (skip spec/plan) |
| **M** | New feature, module refactor, 3-10 files | Standard | Stages 1-10 |
| **L** | Architecture change, new service, 10+ files | Full | Stages 1-12 (all) |

**How stages relate:** Stages 5-6-7 (Self-Audit, Verification, Impact) run **inside each implementation phase** as an inner loop. Stages 8-12 run **once after all phases complete** as an outer loop.

---

## Context Management (ALWAYS applies)

### The 40% Rule
Code quality degrades when context fills beyond 40% ("Dumb Zone"). Rules:
- Stay within 40-60% of the context window
- Manual `/compact` at 50% — don't wait for auto
- If overloaded: save progress → `/clear` → fresh start

### Fresh Context Between Stages
Every major stage = clean context window:
1. Save stage artifact (research / spec / plan / handoff)
2. `/clear`
3. Start new stage pointing the agent to the artifact path

### Handoff Protocol
Before `/clear` always create `progress/<task>-handoff.md`.
See `templates/handoff.md` for format.

### Progressive Disclosure
Don't dump the entire codebase into context:
- Research: sub-agents → compact summary
- Planning: summary + key interfaces only
- Implementation: only files for current phase
- In CLAUDE.md: `"For details, see path/to/docs.md"` (not @file)

---

## Stage 1: Deep Research

**Mode: Read-Only. No code. No changes.**

- Launch parallel Explore agents (1 per area: structure, patterns, deps, tests)
- **WebSearch: Who has already solved this problem? How did they solve it? What is the most efficient known solution?** Don't reinvent — find the best existing approach first.
- **Analyze all findings and make a conclusion: which solution is the BEST and why.** The research artifact must end with a clear recommendation, not just a list of options.
- Save to `thoughts/research/YYYY-MM-DD-<task>.md`
  (see `templates/research.md` for format)

**→ `/clear`**

---

## Stage 2: Spec / PRD

**Mode: Read + Write only in specs/. No code.**

**Spec = WHAT and WHY. Not how. Spec = contract.**

- Read Research Artifact from `thoughts/research/`
- Create `specs/YYYY-MM-DD-<name>.md`
  (see `templates/spec.md` for format)
- Key sections: Problem, Goal, Scope, Acceptance Criteria, Constraints, Non-Goals

**Skip for size S tasks.**
**→ `/clear`**

---

## Stage 3: Planning + Questions

**Mode: Read + Write only in plans/. No code yet.**

- Read **both** Spec (`specs/`) and Research (`thoughts/research/`)
- Launch Plan agents to check the approach
- Find gaps: what's unthought? What edge cases? What could break?
- **Be creative and proactive: anticipate ALL possible problems BEFORE writing code.** Think several steps ahead. What could go wrong in a week? A month? Under load? With unexpected user behavior? Solve problems before they exist.
- **WebSearch: How have others solved this exact problem? What libraries/patterns exist? What's the proven best practice?** Choose the most efficient solution, not the first one that comes to mind.
- After Plan agents verify the approach — **rewrite the plan into an improved version** incorporating all findings, edge cases, and research results. Not just patch it — rewrite it better.

### Challenge Loop (mandatory before finalizing plan)

```
Before finalizing the plan, answer 3 questions:

1. DOES THIS SOLVE THE PROBLEM?
   Compare every plan item against acceptance criteria from spec.
   If any criterion is uncovered — the plan is incomplete.

2. IS THIS THE MOST EFFICIENT SOLUTION?
   Search: who has already solved this problem? What approach did they use?
   Name 2-3 alternative approaches (including ones found via research).
   For each: pros, cons, effort.
   Justify why the chosen approach is better than all alternatives.

3. IS THERE "CODE FOR CODE'S SAKE"?
   Every change must directly serve acceptance criteria.
   If a change isn't tied to solving the problem — remove it.
   Drive-by refactoring = separate task, not part of this one.
```

### Annotation Cycle
1. Claude drafts the plan
2. `Ctrl+G` — plan opens in editor
3. User adds `> NOTE:` annotations
4. Claude: `"Address all notes, don't implement yet"`
5. Repeat until no notes remain

### Questions for User
- Only for real forks where there's a genuine decision to make
- Use AskUserQuestion with options
- For each question: **recommend which option you think is best and why**
- Don't ask the obvious

### Final Plan
Create `plans/YYYY-MM-DD-<name>.md`
(see `templates/plan.md` for full template with Challenge Log, phases, prompts)

**→ `/clear`**

---

## Stage 4: Phased Implementation

**Each phase = separate session, fresh context, feature branch.**

Phases can be run **in parallel** via separate Claude Code sessions/terminals when they don't depend on each other. Check the plan for dependencies before parallelizing.

**Guard phrase to start coding:** Only begin implementation after the plan is finalized and all annotation notes are addressed. The trigger: `"Implement Phase N according to plan."`

Order within each phase:
1. Create/switch to feature branch: `feature/<task>`
2. Update status → `in_progress`
3. **TDD**: tests FIRST (red)
4. **Implement**: code to make tests pass (green)
5. **Refactor** (if needed)
6. **Self-Audit** (Stage 5)
7. **Verification** (Stage 6)
8. **Impact Analysis** (Stage 7)
9. **Gates** (see Gates section)
10. **Commit** (checkpoint)
11. Status → `completed`, write to Changelog
12. **Handoff** → `/clear`

---

## Stage 5: Self-Audit (after each phase)

**Mandatory BEFORE marking `completed`:**

```
Check the phase implementation:

1. SPEC COMPLIANCE
   Open spec. Walk through every acceptance criterion.
   For each: implemented? Where exactly in code?
   If any not covered — finish it.

2. CHALLENGE THE SOLUTION
   Look at the written code with fresh eyes.
   Does this actually solve the problem from spec?
   Is there a simpler/more efficient way?
   Any "code for code's sake" — changes unrelated to the task?
```

---

## Stage 6: Verification — Deep Bug Hunt

**Not just linting. Thoughtful review with false-positive filtering.**

### Step 1: Find errors
```
Check ALL code from this phase for:
- Logic errors (wrong conditions, off-by-one, race conditions)
- Data handling (null/undefined, type mismatches)
- Security (injection, auth bypass, exposed secrets)
- Performance (N+1 queries, memory leaks, unnecessary re-renders)
```

### Step 2: Verify bugs are REAL
```
For EACH found bug:
1. Is this a REAL bug or a false positive?
2. Can you prove this bug is reproducible?
3. If you can't prove it — it's NOT a bug. Don't touch it.

RULE: Don't fix code "for beauty" or "just in case".
Fix ONLY proven bugs that actually affect functionality.
Every "fix" without proof = risk of introducing a new bug.
```

### Step 3: Logic and efficiency check
```
Final code cleanliness check:
- Logic: is the data flow correct from input to output?
- Efficiency: any redundant operations?
- Readability: is the code understandable without comments?
BUT: don't refactor "for beauty". Only if it affects correctness.
```

---

## Stage 7: Impact Analysis — "Did we break anything?"

**The most underestimated stage. 75% of AI agents break previously working code.**

```
MANDATORY CHECK BEFORE MERGE:

1. REGRESSION
   What other modules/functions depend on changed files?
   Run ALL project tests (not just current phase).
   If anything broke — this is priority #1.

2. SIDE EFFECTS
   Did any contracts/interfaces change (API, props, types)?
   If yes — who uses them? Are all consumers updated?

3. THINK AHEAD
   What problems could these changes cause in a week/month?
   Edge cases we haven't tested?
   What happens with: zero data? Huge data? Concurrent requests?
   What if the user does something unexpected?

4. COMPATIBILITY
   Backward compatibility preserved?
   Data migrations needed?
   Feature flags needed for gradual rollout?
```

---

## Stage 8: Integration Check

- All phases `completed` → run gates across entire project
- Explore agents for audit: everything from spec implemented?
- Every acceptance criterion → fulfilled?

---

## Stage 9: Code Review (fresh context)

**New session. No implementation bias.**

- Launch `@code-reviewer` agent (see `agents/code-reviewer.md`)
- Checklist: edge cases, race conditions, backward compat, security, error handling, performance
- If possible: cross-model review (different model checks Claude's work)
- **Warning**: AI reviewing AI has shared blind spots. For critical code — human review is mandatory.

---

## Stage 10: Security Scan (for M and L)

```bash
semgrep --config=auto .
# or
/security-review    # built into Claude Code
```

---

## Stage 11: Fixes + Re-verification

If review/scan found issues:
1. Fix (only proven bugs — rule from Stage 6)
2. Re-run gates
3. Repeat Impact Analysis (Stage 7) — fixes didn't break anything else?
4. Re-review if major changes were made

---

## Stage 12: Cleanup + Deploy

- Archive plan: `mv plans/<file> plans/archive/`
- Keep spec as documentation
- Squash merge → main
- **Deploy — ONLY on explicit user request**

---

## Deterministic Gates

A phase CANNOT be `completed` without passing ALL required gates.

### Tier 1: Required (block the phase)
```bash
# Frontend
cd frontend && npx tsc --noEmit          # 0 type errors
cd frontend && npm run lint               # 0 lint errors
cd frontend && npm test                   # all tests green

# Backend
cd backend && python -m py_compile app/main.py
cd backend && pytest --tb=short -q
cd backend && ruff check .
```

### Tier 2: Recommended (for M and L)
```bash
npx madge --circular src/         # circular dependencies
npm audit --audit-level=high      # dependency vulnerabilities
pip-audit
```

### Tier 3: Deep Security (for Security Scan stage)
```bash
semgrep --config=auto .
# or /security-review
```

If a gate fails — fix and re-run. Never skip.

---

## Hooks

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "bash -c \"CMD=$(echo $TOOL_INPUT | jq -r '.command // empty'); echo \\\"$CMD\\\" | grep -qE '(git push.*(main|master)|rm -rf /|DROP TABLE)' && echo 'BLOCKED: Use feature branch / safe alternative.' >&2 && exit 2 || exit 0\""
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "prompt",
          "prompt": "You are a JSON-only evaluator. Respond ONLY with raw JSON, no markdown.\n\nReview the assistant's final response. Reject if:\n- Rationalizing incomplete work ('pre-existing', 'out of scope', 'follow-up')\n- Listing problems without fixing them\n- Skipping test/lint failures with excuses\n- Making changes unrelated to the stated problem ('code for code's sake')\n- Claiming completion without running verification gates\n\nRespond: {\"ok\": false, \"reason\": \"[issue]. Go back and finish.\"}\nor: {\"ok\": true}"
        }]
      }
    ]
  }
}
```

---

## Git Discipline

- Each task = `feature/<task>` branch
- Commit after each passed gate (checkpoint for rollback)
- NEVER push to main directly (hook blocks it)
- Squash merge on completion

---

## Optional Enhancements

### PostToolUse: Auto-format after every file write
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "npx prettier --write \"$FILE_PATH\" 2>/dev/null || true"
  }]
}
```
Claude generates well-formatted code; the hook handles the last 10% to avoid CI failures.

### PreToolUse: Block hardcoded secrets on file write
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "bash -c \"CONTENT=$(echo $TOOL_INPUT | jq -r '.content // empty'); echo \\\"$CONTENT\\\" | grep -qiP '(api.?key|secret|password)\\s*=\\s*[\\x27\\\"][^\\x27\\\"]{10,}' && echo 'BLOCKED: Hardcoded secret. Use env vars.' >&2 && exit 2 || exit 0\""
  }]
}
```
Fragile (regex-based) but catches obvious mistakes. For production, use `semgrep` or `/security-review` instead.

---

## Model Recommendations

| Stage | Model | Why |
|-------|-------|-----|
| Research, Planning | Opus | Cross-file reasoning |
| Implementation | Sonnet | Speed, cost-efficiency |
| Code Review, Security | Opus | Deep analysis |
| Anti-rationalization hook | Haiku | Fast, cheap gate |

---

## Project Structure

```
project/
├── .claude/
│   ├── settings.json           # hooks config
│   ├── skills/
│   │   └── bulletproof/
│   │       ├── SKILL.md        # ← this file
│   │       ├── templates/
│   │       │   ├── research.md
│   │       │   ├── spec.md
│   │       │   ├── plan.md
│   │       │   └── handoff.md
│   │       └── agents/
│   │           └── code-reviewer.md
│   └── agents/                 # project-level agents
├── CLAUDE.md                   # project brain
├── specs/                      # WHAT and WHY
├── plans/                      # HOW
│   └── archive/                # completed plans
├── thoughts/research/          # research artifacts
└── progress/                   # handoff files
```
