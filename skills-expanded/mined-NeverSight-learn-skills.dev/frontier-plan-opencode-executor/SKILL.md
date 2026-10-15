---
name: frontier-plan-opencode-executor
description: "Use when given a detailed implementation plan from a frontier AI to execute inside OpenCode with non-frontier coding models. Validates the plan against the real repository, breaks it into safe steps, verifies each step, inspects diffs, and prevents destructive changes. Triggers on: receiving a multi-step plan from Claude Opus/GPT-5/etc., executing a pre-written spec, implementing a detailed PR description, or being told to \"execute this plan step by step.\""
---

# Frontier Plan OpenCode Executor

## Core Principle

**The frontier plan is a strong hypothesis, not ground truth.**

Execute the intent of the plan step by step, but validate every instruction against the actual repository before editing code. Frontier AI plans frequently fail on: nonexistent file names, invented imports, unavailable libraries, patterns that don't match the repo, missing tests, idealized architecture, and breaking internal APIs.

Never batch large changes. Never skip verification. Never hide uncertainty. Never perform destructive actions without explicit approval.

## When to Use

- You receive a detailed, multi-step implementation plan written by a frontier AI
- The plan has 3+ distinct steps with specific file paths and code patterns
- You are using a non-frontier coding model that benefits from execution discipline
- The plan carries risk of conflicting with the actual codebase

**Do NOT use for:**
- Single-file changes or trivial fixes
- Plans with only 1-2 simple steps
- Plans you wrote yourself during the same session
- Rapid iteration where the user wants speed over safety

## Core Workflow

### 0. PREFLIGHT: Establish Repository Baseline

**Before touching any file, understand the repo state and detect pre-existing failures.**



```
1. git status --short          # Is the repo clean?
2. Inspect package.json         # Available scripts, dependencies
3. Inspect AGENTS.md, README.md # Project conventions, commands
4. Detect available verification commands from package.json scripts
5. Run the cheapest baseline verification if available (lint or typecheck)
```

If baseline already fails:
- Record the failure explicitly: exact command, exit status, and short error summary
- Do NOT attempt broad cleanup or fix unrelated issues
- Continue only if the planned change can be isolated from the existing failure
- Do not attribute pre-existing failures to your implementation

**Dangerous state detection:**
- If `git status` shows uncommitted changes unrelated to the plan, warn the user
- If lockfiles are modified, warn the user
- If the repo is in a conflicted/rebasing state, stop and ask

**Checkpoint recommendation:**
- If the repo is clean before starting, recommend creating a checkpoint commit before implementation
- Do NOT create commits unless explicitly asked by the user

## Auto-Commit and Auto-Push

Auto-commit and auto-push are enabled by default unless the user explicitly disables them.

The agent should commit each verified logical unit of work and push it to the active remote working branch so the user can review the history later.

Before implementation:
- identify the current branch;
- if on `main`, `master`, `production`, `release`, or another protected/mainline branch, create a new working branch inferred from the plan;
- if already on a working branch, continue there;
- never push directly to protected/mainline branches.

If there are pre-existing uncommitted changes:
- do not automatically include them in agent commits;
- stage only files related to the current logical unit;
- if user changes and agent changes cannot be safely separated, stop and report the conflict.

Commit only after:
- the logical unit is complete;
- verification passes;
- the diff has been inspected;
- the commit has one coherent purpose.

Use Conventional Commits:

```text
type(scope): concise imperative summary

Examples:

feat(auth): add session validation helper
fix(api): handle empty webhook payload
refactor(billing): extract invoice mapper
test(auth): cover expired session flow
```

### 1. PARSE: Extract and Reality-Check the Plan

Read the ENTIRE plan. Extract ordered steps. For each step, run a reality check:

| Check | Question |
|-------|----------|
| Files | Do referenced files exist in the repo? |
| Libraries | Are referenced libraries in `package.json`? |
| Patterns | Does the repo already have an equivalent utility/component? |
| Commands | Are the plan's verification commands available? |
| Dependencies | Does this step depend on a previous step? |
| Risk | Low / Medium / High — how likely to break existing behavior? |

If a step references missing files, nonexistent libraries, outdated patterns, or unavailable commands: **adapt the step before implementing, preserving the plan's intent.**

### 2. TRACK: Create Progress Tracker

Use `todowrite` (OpenCode's task list tool) if available.

If `todowrite` is unavailable (e.g., in subagents where it's disabled by default):
- Create a visible **markdown checklist** in your response
- Keep it updated manually after each step
- Use it as the source of truth for progress
- Do NOT pretend the tool was used if it wasn't

Each item must include: the implementation action, the verification method, and expected files touched.

### 3. IMPLEMENT: One Step at a Time

Mark the current step as `in_progress`. Implement ONLY that step.

- Read target files before editing
- Follow existing codebase conventions (imports, naming, patterns, architecture)
- Adapt the plan to existing infrastructure (e.g., if the plan says "create a toast component" but the project uses Sonner, wrap Sonner instead of building from scratch)
- Make the smallest coherent change
- Do NOT implement future steps, but keep downstream dependencies in mind when making design decisions
- Do NOT perform unrelated cleanup, refactoring, or formatting
- Do NOT install dependencies unless explicitly approved

### 4. VERIFY: Tiered Verification

**After each step, run the narrowest meaningful verification.** Not "lint everything" every time.

| Change Type | Minimum Verification | Stronger Verification |
|---|---|---|
| New file/component | lint or typecheck | affected typecheck |
| Type/interface change | typecheck | affected tests |
| Logic/function change | targeted unit test | full test suite |
| API/server change | targeted integration test | build + endpoint check |
| UI change | typecheck + build | visual/manual smoke check |
| Config/build change | build | clean install/build if needed |
| Database/schema change | dry-run/check command | user approval required |

If no automated verification exists for a step: perform a manual review and state precisely what you checked.

If verification fails:

**First failure — fix and re-verify:**
- Fix only errors caused by the current step
- Do NOT fix pre-existing or unrelated errors
- Re-verify immediately

**Repeated failures — do not keep patching blindly.** See "Repeated Failure Handling" below.

**Critical:** Never make verification pass by weakening assertions, deleting tests, removing behavior, changing public APIs, suppressing errors, or hiding failures — unless the plan explicitly requires it AND the user approves. Making the alarm stop is not the same as fixing the problem.

### 5. DIFF: Inspect Changes

After verification passes, inspect what actually changed:

```
git diff --stat          # Which files changed?
git diff                 # When the diff is small enough to review
```

Confirm:
- Only expected files changed
- No unrelated formatting occurred
- No lockfiles changed (unless explicitly intended)
- No generated files were accidentally edited
- No secrets, local paths, or debug logs introduced
- No code was accidentally deleted

**If the diff exceeds the expected scope, stop and correct before continuing.**

### 6. CONFIRM: Mark Complete

Only when implementation, verification, AND diff inspection are clean:
- Mark the step as `completed`
- Summarize what changed in one sentence
- Mark the next step as `in_progress`

### 7. FINAL: Full Verification + Report

After all steps:
- Run the strongest reasonable check: lint + typecheck + build + tests (using project commands)
- Report: completed steps, files changed, verification results, adaptations made, pre-existing failures (if any), anything requiring user review

## Repeated Failure Handling

If verification repeatedly fails for the same underlying reason, **do not continue applying small blind fixes.** The goal is to detect whether you are learning something new between attempts or just thrashing randomly.

**When a step fails multiple times:**

1. **Stop patching.** Stop making small tweaks and re-running.
2. **Re-read the error output carefully.** The full stacktrace, not just the first line.
3. **Inspect the diff and surrounding code.** `git diff`, read related types, interfaces, functions.
4. **Re-evaluate the original assumption.** Is the current implementation strategy correct?
5. **Classify the failure:**
   - Incorrect assumption about the codebase?
   - Repository mismatch (plan vs reality)?
   - Wrong abstraction chosen?
   - Interface or type incompatibility?
   - Missing dependency?
   - Stale generated artifacts?
   - Pre-existing issue unrelated to your change?
   - Verification command itself is misconfigured?
6. **Form a genuinely new hypothesis.** Only retry when you have one.
7. **Consider reducing scope.** Can the step be split into smaller pieces to isolate the failure?

**Critical rule:** Do not repeat the same fix strategy unless new information was discovered from:
- Logs
- Stack traces
- Diffs
- Tests
- Repository inspection
- Documentation

**If no new strategy emerges after multiple attempts, stop and report the blocker clearly:**

```
Blocker:
- verification command: `npm run build`
- failing file: `src/app/page.tsx`
- root issue hypothesis: React Server Component importing client-only hook
- attempted strategies:
  1. moved import to client component
  2. isolated hook into separate file
  3. checked existing patterns in repo
- reason for stopping:
  no consistent pattern in repo to resolve boundary safely
- likely next action:
  user review or architectural clarification
```

A clear blocker report is always better than repeating "still failing" while guessing.

## Adapting Plans to Existing Code

Frontier AI plans frequently conflict with the actual codebase. When they do:

1. **Identify the conflict** — "The plan says `import { X } from 'uninstalled-lib'` but it's not in package.json"
2. **Adapt, don't ignore** — Use existing infrastructure to match the plan's intent
3. **Explain the adaptation** — One sentence on what you changed and why
4. **Preserve the plan's interface** — If the plan exports `useToast()`, your adaptation should still export `useToast()`, even if internals differ

**Critical rules:**
- Do NOT create new abstractions if the repo already has an equivalent primitive
- Do NOT install new dependencies unless the plan explicitly requires it AND the user approves
- Do NOT change architecture or patterns without justification

## Forbidden Without Explicit User Approval

These commands require the user to say "yes" before running:

**Destructive:**
- `rm -rf`
- `git reset --hard`
- `git clean -fd`
- `git push --force`

**Installation (changes lockfiles):**
- `npm install`
- `pnpm install`
- `yarn install`
- `bun install`
- `npm audit fix`

**Database / Infrastructure:**
- `prisma migrate`
- `prisma db push`
- `supabase db push`
- `docker compose down -v`

**Configuration:**
- Changing `.env` files
- Modifying global tool config
- Running deploy/unpublish commands

**Mass changes:**
- Broad formatting (prettier/eslint --fix on entire repo)
- Find-and-replace across many files without review

If unsure whether a command is safe, ask before running.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "The frontier AI said it, so it must be right" | Frontier plans are hypotheses. Validate against the real repo. |
| "I'll verify everything at the end" | Errors compound. Verify each step with the right granularity. |
| "I already read the plan, I can implement it all at once" | Batch implementation = batch errors + harder debugging. |
| "I'll fix pre-existing lint errors while I'm here" | Unrelated cleanup masks what your changes actually did. Don't. |
| "This step is simple, I don't need to check git diff" | Simple edits can accidentally delete code or format unintended files. |
| "I'll install the missing library the plan references" | Ask first. The library may be intentionally absent or not approved. |
| "npm run build is the only verification that matters" | Build is slow and broad. Use lint/typecheck for intermediate steps. |
| "If it fails, I'll just tweak and re-run until it passes" | Blind patching without new information is thrashing. Re-read errors. Form a new hypothesis first. |
| "The same error again, let me try a different small change" | Same error + same strategy = same result. Change the strategy, not the patch. |

## Red Flags — STOP and Re-evaluate

- "I'll verify after the next step too" — Verify NOW.
- "The frontier plan knows better than the repo" — The repo is the source of truth.
- "This library isn't installed but the plan needs it" — Ask the user. Do not install silently.
- "The diff is bigger than expected but it's probably fine" — Inspect and explain before continuing.
- "I'll batch steps 2 and 3 since they're related" — One step = one verify + diff cycle.
- "Pre-existing lint errors, let me fix those first" — Not your job. Record them. Stay focused.
- "Let me format this file while I'm editing it" — Separate change = separate step. Don't mix.
- "Still failing, let me try another quick fix" — Stop patching. Re-read the error. Form a new hypothesis first.
- "The same error 3 times, one more tweak might work" — Same error + same strategy = thrashing. Change strategy or report blocker.
- "I'll just rewrite the whole thing and see if that fixes it" — Throwing away work without understanding why it failed teaches nothing. Diagnose first.
- "The user is in a hurry, I'll skip the diff check" — 5 seconds of `git diff --stat` prevents hours of debugging.

## Quick Reference

| Phase | Action | Tool |
|-------|--------|------|
| Preflight | git status, detect commands, baseline check | Bash |
| Parse + Reality Check | Read plan, validate each step against repo | Read + Glob |
| Track | Create todowrite or markdown checklist | todowrite |
| Implement | One step, minimal change, existing patterns | Read + Edit/Write |
| Verify | Tiered check per change type | Bash |
| Diff | `git diff --stat`, confirm scope | Bash |
| Confirm | Mark complete, summarize, next step | todowrite |
| Final | Full verification + summary report | Bash |

## Model-Specific Notes

### Non-Frontier Models (Deepseek v4 Pro, GPT-4o, Gemini Flash)
- Context window management is critical — the todowrite/checklist keeps you anchored
- Excel at focused single tasks, drift on large context dumps
- Step-by-step verification catches errors the model might miss in batches
- The reality check phase prevents running with incorrect assumptions

### Frontier Models (Claude Opus, GPT-5, Gemini Pro)
- This workflow is still valuable for complex, risky, multi-file changes
- Can handle larger steps — adjust granularity up
- Discipline of diff inspection and tiered verification prevents overconfidence
