---
name: dev-autopilot
description: Full autonomous execution from idea to working code. Use when user says "autopilot", "autonomous", "build me", "create me", "make me", "full auto" — orchestrates spec → plan → code → QA → validation across the engineering layer agents.
---

# Dev Autopilot

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Autopilot takes a brief product idea and autonomously handles the full lifecycle: requirements analysis, technical design, planning, parallel implementation, QA cycling, and multi-perspective validation. It produces working, verified code from a 2-3 line description.

## Use When
- User wants end-to-end autonomous execution from an idea to working code
- User says "autopilot", "autonomous", "build me", "create me", "make me", "full auto", "handle it all", or "I want a/an..."
- Task requires multiple phases: planning, coding, testing, and validation
- User wants hands-off execution and is willing to let the system run to completion

## Do Not Use When
- User wants to explore options or brainstorm → use `dev-plan` instead
- User says "just explain", "draft only", or "what would you suggest" → respond conversationally
- User wants a single focused code change → delegate directly to `@bolt-executor`
- User wants to review or critique an existing plan → use `dev-plan --review`
- Task is a quick fix or small bug → direct executor delegation

## Why This Exists
Most non-trivial software tasks require coordinated phases: understanding requirements, designing a solution, implementing in parallel, testing, and validating quality. Autopilot orchestrates all of these phases automatically so the user can describe what they want and receive working code without managing each step.

## Execution Policy
- Each phase must complete before the next begins
- Parallel execution is used within phases where possible
- QA cycles repeat up to 5 times; if the same error persists 3 times, stop and report the fundamental issue
- Validation requires approval from all reviewers; rejected items get fixed and re-validated

## Phases

### Phase 0 — Expansion
Turn the user's idea into a detailed spec.
- **If input is vague** (no file paths, function names, or concrete anchors): suggest `dev-deep-interview` for Socratic clarification before expanding
- **Otherwise**: `@echo-analyst` (Opus) extracts requirements, `@apex-architect` (Opus) creates technical specification
- Output: `workspace/projects/specs/[C]autopilot-spec-{name}.md`

### Phase 1 — Planning
Create an implementation plan from the spec.
- `@compass-planner` (Opus): Create plan (direct mode, no interview)
- `@raven-critic` (Opus): Validate plan
- Output: `workspace/projects/plans/[C]autopilot-plan-{name}.md`

### Phase 2 — Execution
Implement the plan.
- `@bolt-executor` (Sonnet): Standard tasks
- For complex tasks, escalate to `@apex-architect` for design before re-delegating
- Run independent tasks in parallel where safe

### Phase 3 — QA
Cycle until all tests pass.
- Build, lint, test, fix failures
- Repeat up to 5 cycles
- Stop early if the same error repeats 3 times (indicates a fundamental issue)

### Phase 4 — Validation
Multi-perspective review in parallel.
- `@apex-architect`: Functional completeness
- `@vault-security`: Vulnerability check (when imported in EPIC 3)
- `@lens-reviewer`: Quality review
- All must approve; fix and re-validate on rejection

### Phase 5 — Verification
- `@oath-verifier`: Final evidence-based completion check against acceptance criteria

## Examples

**Good:**
- "autopilot a REST API for a bookstore inventory with CRUD operations using TypeScript"
  → Specific domain, clear features, technology constraint. Enough context to expand.
- "build me a CLI tool that tracks daily habits with streak counting"
  → Clear product concept with a specific feature.

**Bad:**
- "fix the bug in the login page" → Single focused fix, not multi-phase. Delegate to `@hawk-debugger` or `@bolt-executor`.
- "what are some good approaches for adding caching?" → Exploration. Respond conversationally or use `dev-plan`.

## Stop Conditions
- Same QA error persists across 3 cycles → escalate
- Validation keeps failing after 3 re-validation rounds → escalate
- User says "stop", "cancel", or "abort"
- Vague spec produces unclear expansion → pause and ask for clarification

## Final Checklist
- [ ] All 5 phases completed (Expansion, Planning, Execution, QA, Validation, Verification)
- [ ] All validators approved
- [ ] Tests pass (verified with fresh test run output)
- [ ] Build succeeds (verified with fresh build output)
- [ ] User informed of completion with summary of what was built

## Best Practices for Input
1. Be specific about the domain — "bookstore" not "store"
2. Mention key features — "with CRUD", "with authentication"
3. Specify constraints — "using TypeScript", "with PostgreSQL"
4. Let it run — avoid interrupting unless truly needed
