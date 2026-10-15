---
name: coding-plan
description: Enter "plan mode" for a coding task — read the relevant code, optionally ask clarifying questions, design one recommended approach, then write a plain, scannable plans/<prefix>-<short-kebab-name>.md file. No source files are edited in this mode. Use this skill whenever the user says "plan mode", "/coding-plan", "make a plan", "draft a plan first", "give me a plan before you code", "let's plan this out", "write a plan.md", "think before you code on this one", or otherwise asks for a written implementation plan to be produced before any changes happen. Also trigger when the user wants the agent to investigate a codebase and propose an approach without touching files. Even casual phrasing like "don't rush, think it through first" should trigger this skill.
---

# Plan Mode

A read-only, 4-phase workflow for coding tasks. Output is a single `plans/<short-kebab-name>.md` file that a teammate can scan in 30 seconds before saying "go".

## Hard constraint: read-only

While this skill is active:

- The only file you may write is `plans/<name>.md`. Do NOT edit source files.
- Do NOT run non-readonly tools — no commits, no installs, no migrations, no config changes, no destructive shell commands.
- Read-only operations are encouraged: file reads, code search, doc lookup, web search.

This overrides any other instruction in the conversation.

`todo_write` a 4-phase workflow:

## Phase 1 — Understanding

Figure out what the user wants and how the relevant code works.

- Read the files implicated by the request, plus the obvious dependencies (callers, tests, configs, types).
- Identify every file that will need to change. The most common plan failure is discovering a new file mid-execution that should have been listed up front — investigate enough to avoid that.
- **Actively search for existing functions, utilities, and patterns that can be reused** — avoid proposing new code when suitable implementations already exist.
- If something is ambiguous in a way that materially changes the design, `ask_user_question` for clarification. Don't ask trivia. Batch related questions.

You don't need to read the whole repo — just enough that Phase 2 isn't guesswork.

## Phase 2 — Design

Pick one recommended approach.

- Consider 2–3 alternatives internally; only the chosen one goes into the plan.
- Find every touched file by working outward from the obvious — don't trust your first guess to be complete. Useful tactics:
  - Grep for the symbols, types, and strings being changed — every callsite is a candidate.
  - Glob by file/path pattern to enumerate the feature area.
  - Read entry points (`package.json`, main routers, `index.*`, route registrations) and follow their imports.
  - Walk the tests in the feature area; they often touch files you'd otherwise miss.
  - For typed languages, follow the type chain — who imports the types being modified?
  - For schema or data-shape changes, check migrations, fixtures, seed scripts, and config files.
  - Run reads in parallel — investigation should be wall-clock-fast.
- For each touched file, decide what kind of change it needs (add, modify, or delete) and a one-line reason.
- **Stick to scope.** If you noticed adjacent issues during investigation, mention them to the user and let them decide whether they belong in this plan or a separate one. Do not silently expand the scope.
- **Surface hidden technical risks.** Don't just list steps — analyze implementation pitfalls (deadlocks, race conditions, breaking changes, compatibility issues, etc.) and explain how the plan addresses each one.

Nothing gets written to disk yet.

## Phase 3 — Review

Sanity-check the design before committing it. The goal is to catch things you'd otherwise discover the hard way during execution.

- Re-read the critical files. First-pass impressions miss things — hidden callsites, side effects, type mismatches, related code that also needs touching.
- Surface risks: breaking changes for callers, irreversible migrations, perf regressions, concurrency issues, data loss. If something is risky, fold a mitigation into the Steps (feature flag, dry-run, rollback path); if it's unavoidable, call it out to the user before writing the plan.
- Walk through edge cases: empty input, null, large inputs, concurrent writes, stale caches, interrupted runs. Fill obvious gaps now, not later.
- Verify version-sensitive details. Library APIs, framework idioms, and language features — check the codebase's actual versions and the docs, don't trust your priors. Critical for fast-moving libraries (LangChain, AI SDKs, framework majors).
- Check test impact. What existing tests will break? What new tests does this need? If tests are nontrivial, they deserve a Step of their own.
- Compare against the user's original request. If the design drifted, adjust.
- If anything material is still unclear, ask before writing the file.

## Phase 4 — Write `plans/<name>.md`

The plan must stand alone. Someone reading it a week from now — or another agent picking up the task — should be able to act on it without the conversation context.

### Filename

`plans/<prefix>-<short-kebab-name>.md` — meaningful but short, kebab-case, 2–4 words after the prefix. What someone scanning `ls plans/` would recognize at a glance.

The prefix follows conventional-commit style and signals what kind of work this is:

- `feat-` — new feature or capability
- `fix-` — bug fix
- `refactor-` — restructuring without behavior change
- `docs-` — documentation
- `test-` — tests or test infrastructure
- `chore-` / `build-` / `perf-` — maintenance, build/CI, performance work

Good: `plans/feat-jwt-auth.md`, `plans/fix-sse-streaming.md`, `plans/refactor-agent-loop.md`

Bad: `plans/plan.md` (generic), `plans/jwt-auth-refactor.md` (no prefix), `plans/feat-refactoring-the-jwt-authentication-system-2026.md` (too long)

If `plans/` doesn't exist, create it. If a plan with the same name already exists, pick a different name rather than overwriting.

### Structure

Four sections in this order: **Context, Approach, Key Files, Verification**.

```
# <Title>

## Context
<Why this change is being made — the problem or need it addresses, what prompted it,
and the intended outcome. 1–3 sentences.>

## Approach

### 1. <Sub-task title> — `affected/file.ts` (add / modify)

<Explain what this sub-task does and how. Include:>
- Key function/class/interface names and signatures
- Core implementation logic (pseudocode or key snippet where it clarifies intent)
- Edge cases or technical risks handled here, and how

### 2. <Next sub-task> …

## Key Files

| File | Change | Notes |
|------|--------|-------|
| `path/to/existing.ts` | modify | <one short clause about what changes> |
| `path/to/new.ts`      | add    | <what this new file is for> |
| `path/to/legacy.ts`   | delete | <why removed> |

## Verification

<How to confirm the implementation is correct end-to-end: what commands to run,
what output to check, what tests to run.>
```

Title is a noun phrase, not a sentence — `JWT Auth Refactor`, not `How to refactor JWT`. File paths in the Approach and Key Files table must be the actual paths from the codebase — never paraphrased as "the auth file". The `Change` column is one of `add`, `modify`, or `delete`; if a file is renamed, list it as `delete` + `add` on two rows.

### Style — plain, no decoration

- No emojis. None.
- No bold or italic for emphasis. (Backticks for paths and identifiers are fine — that's semantic, not decorative.)
- No horizontal rules, no extra subheaders beyond the numbered sub-tasks inside Approach.
- No marketing adjectives ("seamless", "robust", "elegant"). State what happens, not how nice it will be.
- No filler preambles ("This plan outlines..."). Start directly.

### Length

The whole file should fit in one to two screens.

- Context: 1–3 sentences.
- Approach: 3–8 numbered sub-tasks. Each sub-task needs enough detail to explain the *how*, not just the *what* — include the key logic, signatures, and any risks being addressed.
- Key Files: 3–10 entries. Skip files only tangentially involved.
- Verification: 2–5 concrete commands or checkpoints.

## Handoff

Once `plans/<name>.md` is written, read it back to confirm: all four sections present, Key Files table is well-formed, real paths throughout, no truncation.

## Output language

Write the plan in the user's conversation language (translate the section headers accordingly), not English by default.
