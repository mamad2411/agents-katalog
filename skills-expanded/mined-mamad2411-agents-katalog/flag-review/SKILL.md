---
name: flag-review
description: Triage and act on AI-generated code review flags. Use this skill whenever the user pastes a list of review flags, code review findings, AI reviewer output, or automated code analysis results that need to be investigated and resolved. Also trigger when the user asks to "review flags", "triage findings", "check these issues", or shares a batch of code concerns with file paths and descriptions — even if they don't call them "flags" explicitly.
---

# Review Flags

You've been given a set of flags from an AI code reviewer. Your job is to efficiently triage them — separating signal from noise — and auto-fix what you can.

## How flags work

Each flag typically contains:
- A **file path** (sometimes with a line number)
- A **title** summarizing the concern
- A **description** explaining the issue in detail

Flags vary widely in quality. Some are genuinely important (real bugs, security issues, correctness problems). Many are informational observations dressed up as concerns, or things the codebase already handles. Your job is to figure out which is which by actually reading the code.

## Step 1: Parse and dispatch

Read through all the flags and extract each one as a discrete item. Then spawn one subagent per flag, all in parallel. Each subagent investigates a single flag independently.

The subagent prompt should follow this structure:

```
You are investigating a code review flag to determine if it's actionable.

**Flag title:** <title>
**File:** <file path>
**Flag description:**
<full description>

Instructions:
1. Read the file(s) mentioned in the flag. Read surrounding context too — enough to understand the full picture (related functions, callers, tests, config).
2. Determine a verdict:
   - **actionable-fix**: There's a real issue and a clear fix. Apply the fix and describe what you changed.
   - **actionable-design**: There's a real issue but fixing it involves a design decision the user should weigh in on. Describe the issue and the options.
   - **trivial**: The flag is technically correct but the concern is negligible in practice. Explain briefly why.
   - **already-addressed**: The codebase already handles this concern. Point to the specific code that addresses it.
   - **invalid**: The flag is wrong — it misunderstands the code or makes an incorrect claim. Explain what it got wrong.

3. Return your verdict as structured output:
   - verdict: one of the five categories above
   - confidence: high / medium / low
   - summary: 1-2 sentence explanation of your conclusion
   - details: fuller explanation with code references
   - changes_made: list of files modified (empty if none)
```

Give each subagent the `general-purpose` type so it has full tool access to read code, search the codebase, and make edits.

## Step 2: Collect and present results

Once all subagents return, organize the results into a clear summary for the user. Group by verdict category:

### Fixes applied
For each **actionable-fix** flag: show the flag title, a one-line summary of what was changed, and the files modified. Keep it brief — the user can review the diff.

### Design decisions needed
For each **actionable-design** flag: show the flag title, explain the issue, and present the options clearly. These are the ones where you need the user's input before proceeding.

### Dismissed
For **trivial**, **already-addressed**, and **invalid** flags: list them in a compact table with the title and a short reason for dismissal. Don't belabor these — the user can ask for details on any specific one if they're curious.

## Guidelines

- **Err on the side of dismissing.** AI reviewers tend to over-flag. If a flag is describing a theoretical concern that the code already handles, or a risk that's mitigated by context the reviewer didn't have, dismiss it. The goal is to surface what actually matters.
- **Read the code, don't trust the flag.** The flag's description may be wrong or outdated. Always verify claims against the actual codebase state.
- **Fix boldly but flag design choices.** For straightforward fixes (missing error handling, incorrect SQL quoting, off-by-one errors), just fix them. For things that involve tradeoffs (changing execution order, restructuring a module, altering public APIs), present options instead.
- **Keep the summary scannable.** The user is probably looking at 5-20+ flags. They need to quickly see what changed, what needs their input, and what was noise.
