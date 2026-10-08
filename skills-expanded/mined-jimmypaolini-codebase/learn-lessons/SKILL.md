---
name: learn-lessons
description: 'Retrospective skill that analyzes a coding agent session, a set of local changes, or a branch/pull request, then extracts reusable coding patterns, architectural decisions, and best practices — and writes them into skills and AGENTS.md so future agents apply the same patterns automatically. Primary use: capturing HOW code was written (naming, structure, TypeScript idioms, module patterns, error handling), not just what the agent did. Use when asked to "learn from this session", "capture patterns from this PR", "remember how we did this", "document this approach", "improve skills from this work", or "make sure future agents do it this way".'
argument-hint: 'Provide the branch name, PR number, or describe the coding patterns to capture.'
license: MIT
---

# Learn Lessons

You are a senior software engineer and technical knowledge curator. Your role is to deeply analyze completed work — code changes, a branch diff, or a PR — and extract the **coding patterns, architectural decisions, and best practices** embedded in that work. You then write those patterns into skills and AGENTS.md so future agents apply the same approach automatically without being re-taught.

The primary focus is **how code was written**: naming conventions, module structure, TypeScript idioms, error handling patterns, testing approaches, and architectural choices. Agent workflow behaviors (which tools to call, how to sequence file edits) are secondary — capture those only when they reveal a repeatable coding pattern.

Your output is not a report. It is **concrete updates to skills and AGENTS.md** that encode the patterns found.

## When to Use This Skill

### Primary use cases — coding patterns

- After implementing a new module, feature, or architectural pattern worth repeating
- When the code introduces a naming convention, file structure, or TypeScript idiom not yet in any skill
- After solving a non-obvious technical problem (error handling, async pattern, type narrowing) the right way
- When a PR review revealed a gap between what was written and the project's preferred style
- When asked to "remember how we did this", "document this pattern", or "make sure future agents do it this way"

### Secondary use cases — agent workflow

- After a session with significant back-and-forth or corrections
- After merging or closing a PR, to capture workflow lessons
- When asked to "retrospect", "capture lessons", or "improve agent skills from this work"
- Proactively at the end of a large implementation task before submitting changes

## Scope of Analysis

The skill examines one or more of these inputs — use whichever are available:

| Input | How to Access |
| ----- | ------------- |
| **Session log** | Read the Copilot session debug log at `{{VSCODE_TARGET_SESSION_LOG}}` (current session) |
| **Local changes** | Run `git diff HEAD` or `git diff main` to see uncommitted/unmerged changes |
| **Branch diff** | Run `git log main..HEAD --oneline` then `git diff main...HEAD` |
| **Pull request** | Use `gh pr view <number> --json title,body,files` and `gh pr diff <number>` |
| **Conversation history** | Review the current conversation for retries, corrections, and course changes |

## Step-by-Step Workflow

Execute the following phases in strict order.

---

### Phase 1 — Gather Evidence

#### 1.1 Identify the target

Determine what to analyze based on the user's input:

- If a session log path is provided, read that file
- If a PR number is provided, fetch the PR diff and conversation
- If no input is given, default to the current conversation history plus `git diff main...HEAD`

#### 1.2 Collect the raw material

Run these commands to gather context:

```bash
# Current branch and recent commits
git log main..HEAD --oneline --no-decorate

# Full diff from main
git diff main...HEAD --stat

# Files changed
git diff main...HEAD --name-only
```

Read the session debug log if available:

```bash
# Session log location (substitute actual path)
cat "{{VSCODE_TARGET_SESSION_LOG}}" | head -500
```

#### 1.3 Read the actual code

For each file changed, read enough content to understand the coding patterns used — not just that a file changed, but _how_ it was written:

- Naming choices (variables, functions, types, files)
- Module and file structure decisions
- TypeScript type patterns (generics, discriminated unions, guards)
- Error handling approach
- Test structure and naming
- Any pattern that deviates from or extends existing conventions

#### 1.4 Read relevant existing skills and AGENTS.md

For each project or domain touched by the changes, read the corresponding skills and AGENTS.md files. This establishes the baseline — what is already documented versus what is new.

---

### Phase 2 — Identify What Went Well

Before looking for gaps, explicitly identify **patterns worth reinforcing and repeating**. Prioritize coding patterns over agent behaviors. For each one found, record:

- **What happened** (concrete example from the diff)
- **Why it is good** (convention followed, elegant solution, pattern that should generalize)
- **Where to encode it** (which skill or AGENTS.md should carry this forward)

#### Positive Pattern Checklist

### Coding patterns (primary focus)

| # | Pattern | Signal to Look For |
| - | ------- | ------------------ |
| 1 | **Naming convention established** | A new naming pattern used consistently (file names, function names, type names) |
| 2 | **TypeScript idiom applied correctly** | Discriminated unions, type guards, mapped types, or generics used well |
| 3 | **Error handling done right** | Zod at boundaries, typed errors, early returns, no bare `catch (e)` |
| 4 | **Module structure pattern** | How files, folders, and barrel exports were organized in a new module |
| 5 | **Test structure worth repeating** | How tests were named, arranged, or parameterized |
| 6 | **Architectural decision made** | A deliberate design choice (composition vs. inheritance, service boundary, etc.) |
| 7 | **Reusable abstraction created** | A utility, hook, or helper that solves a class of problems |
| 8 | **Convention applied first-try** | Naming, import order, TypeScript strict rules correct from the start — no corrections needed |

### Agent workflow patterns (secondary)

| # | Pattern | Signal to Look For |
| - | ------- | ------------------ |
| 9 | **Skill loaded proactively** | Read the relevant SKILL.md before starting work, not after a mistake |
| 10 | **Validation before completion** | Ran `validate-code` or tests without being prompted |
| 11 | **Scope respected** | Stayed within the stated project/task scope, no unrelated changes |
| 12 | **Context gathered before implementing** | Read existing code or config before writing new code |

---

### Phase 3 — Identify Gaps and Mistakes

Analyze the evidence for patterns that were missing, applied incorrectly, or corrected after the fact. Prioritize coding gaps over agent workflow issues. For each one found, record:

- **What happened** (concrete example from the diff or conversation)
- **What the correct pattern is** (the approach that should have been used)
- **Where to document it** (which skill or AGENTS.md is the right home)

#### Coding Gap Checklist (primary focus)

| # | Gap | Signal to Look For |
| - | --- | ------------------ |
| 1 | **Missing naming convention** | Inconsistent names, abbreviated identifiers where the codebase requires explicit ones, or names corrected after first draft |
| 2 | **Wrong TypeScript pattern** | `any` used, non-null assertion `!` used, or type narrowing done with a cast instead of a guard |
| 3 | **Error handling gap** | Bare `catch`, swallowed error, or error surfaced as `string` instead of typed error |
| 4 | **Module structure inconsistency** | New module organized differently from existing modules without a deliberate reason |
| 5 | **Convention applied late** | Naming, import order, or strict TypeScript rule applied only after a correction prompt |
| 6 | **Stale knowledge** | Used an outdated API, command, or pattern that has since changed in the codebase |
| 7 | **Over-engineering** | Added abstractions, helpers, or documentation strings not requested or not needed |
| 8 | **Scope creep** | Changed files outside the stated scope of the task |

#### Agent Workflow Gap Checklist (secondary)

| # | Gap | Signal to Look For |
| - | --- | ------------------ |
| 9 | **Skill not consulted** | Jumped to implementation without reading the relevant skill or AGENTS.md |
| 10 | **Missing validation** | Did not run `validate-code` before declaring completion; skipped tests |
| 11 | **Repeated retries** | Same command or file edit attempted 2+ times with minor variation |
| 12 | **Unsafe operation without backup** | Ran destructive git commands without using the `backup-code` skill first |

---

### Phase 4 — Classify Each Finding

For each failure pattern **and** positive pattern found, classify the **correct fix location**.

Priority order: prefer skills and AGENTS.md. Only fall back to memory for facts that have no better home.

| Fix Type | Priority | When to Use | Target File |
| -------- | -------- | ----------- | ----------- |
| **Existing skill** | 1 — preferred | The skill exists but is missing a step, warning, or reinforcement note | `.github/skills/<name>/SKILL.md` |
| **New skill** | 1 — preferred | A repeatable multi-step workflow has no skill yet | `.github/skills/<new-name>/SKILL.md` |
| **AGENTS.md** | 2 — preferred | A short rule must be always-visible to every agent in this workspace | `AGENTS.md` or `<project>/AGENTS.md` |
| **Memory** | 3 — last resort | A highly specific fact with no natural skill home, or a personal cross-workspace preference | `/memories/*.md` or `/memories/repo/*.md` |

---

### Phase 5 — Apply Updates

For each finding classified in Phase 4, make the change.

### For skill updates

(adding a coding pattern, warning, or reinforcement to an existing skill):

- **Coding patterns go in the most specific domain skill** — TypeScript patterns → `write-typescript`, React patterns → `write-react`, NestJS patterns → the relevant NestJS skill, etc.
- If no domain skill covers the pattern, add it to the project's `AGENTS.md` under the relevant section, or create a new skill
- When documenting a positive pattern, add a `> ✅ **Best practice:** ...` callout
- When documenting a gap or mistake, add a `> ⚠️ **Warning:** ...` callout
- Keep examples concrete — include a short before/after code snippet when it clarifies the pattern
- Prefer inserting into an existing phase or section over creating a new one
- Keep each `SKILL.md` focused and under 512 lines. Treat 512 lines as a hard cap when updating any skill.
- If a skill is near or over the limit, refactor details into sibling reference markdown files and keep `SKILL.md` as the concise entry point.
- Split reference files by specific aspect so they are easy to load selectively (for example: workflow steps, troubleshooting, examples, edge cases).
- Store extracted docs under `references/` in the same skill folder and link them from the relevant section in `SKILL.md`.
- When adding new content to an oversized skill, perform the refactor first, then add the new guidance.

### Skill File Size Refactor Pattern

Use this pattern whenever a skill is becoming too large:

1. Keep discovery-critical content in `SKILL.md` (frontmatter, when-to-use triggers, concise workflow outline).
2. Move deep, single-topic details into `references/<aspect>.md` files.
3. Add short links in `SKILL.md` to each reference file from the matching section.
4. Ensure each reference file has a narrow purpose (one aspect per file) instead of one large catch-all document.
5. Re-check the line count and keep `SKILL.md` under 512 lines after the refactor.

### For new skills

(a repeatable workflow not yet covered):

- Follow the [agent-skills instructions](../../../.github/instructions/agent-skills.instructions.md) template precisely
- Place at `.github/skills/<name>/SKILL.md`
- Write a keyword-rich `description` field — this is the primary discovery surface
- Include a step-by-step workflow, not just a description

### For AGENTS.md updates

(always-visible workspace rules):

- Add to the most relevant existing section
- Keep entries to one or two sentences — AGENTS.md is context-critical and must stay concise
- Use AGENTS.md only for rules too short or too universal to justify a full skill

### For memory updates

(last resort — only when no skill or AGENTS.md is appropriate):

- Keep entries short — single bullet points or key-value facts
- Group related facts in the same file; create new files only when the topic is distinct
- Use the memory tool's `str_replace` command to update existing entries

### Phase 6 — Validate and Summarize

#### 6.1 Verify all changes compile and link correctly

For any modified skill files:

```bash
# Check no broken relative links in the skill
grep -oP '\[.*?\]\(\K[^)]+' .github/skills/<name>/SKILL.md

# Verify SKILL.md stays under the hard cap
wc -l .github/skills/<name>/SKILL.md
```

#### 6.2 Run spell check on modified files

Use the `spell-check` skill if any `cspell` errors are reported.

#### 6.3 Produce a summary

Output a concise retrospective report:

```markdown
## Lessons Learned — <date>

### Session / Changes Analyzed
- <brief description of what was analyzed>

### What Went Well — Reinforce These

| # | Pattern | Reinforcement Applied |
| - | ------- | --------------------- |
| 1 | <pattern> | Added ✅ callout to skill X / Added memory note / etc. |

### What Could Be Improved — Fix These

| # | Pattern | Severity | Fix Applied |
| - | ------- | -------- | ----------- |
| 1 | <pattern> | high/medium/low | Updated skill X / Added memory note / etc. |

### Changes Made
- `<file path>`: <one-line description of what changed>

### Recommendations for Next Session
- <actionable suggestion for the next agent>
```

---

## Decision Guide: When NOT to Update

Not every mistake warrants a permanent change. Skip updating when:

- The mistake was a one-off caused by ambiguous user input (not a systematic gap)
- The correct behavior is already documented somewhere the agent should have read
- The fix would be so specific it helps only this exact scenario (no generalization value)

When in doubt, prefer a **memory note** over a skill update — it is lower overhead and easier to remove.

---

## References

- [agent-skills instructions](../../../.github/instructions/agent-skills.instructions.md) — Template and quality rules for SKILL.md files
- [validate-code](../validate-code/SKILL.md) — Full validation workflow before committing
- [spell-check](../spell-check/SKILL.md) — Fix cspell errors in modified files
- [submit-changes](../submit-changes/SKILL.md) — Branch, commit, and PR workflow for the updates
- [backup-code](../backup-code/SKILL.md) — Safety backup before destructive git operations
