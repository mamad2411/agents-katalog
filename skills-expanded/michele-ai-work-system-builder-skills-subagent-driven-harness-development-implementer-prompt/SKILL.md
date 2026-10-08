# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent (the role
writing-harness-plans calls the harness builder) to build one
harness build-plan task.

```
Subagent (general-purpose):
  description: "Build Task N: [task name]"
  model: [MODEL — REQUIRED: choose per SKILL.md Model Selection; an omitted
         model silently inherits the session's most expensive one]
  prompt: |
    You are building Task N: [task name]

    ## Task Description

    Read your task brief first: [BRIEF_FILE]
    It contains the full task text from the harness build plan.

    ## Context

    [Scene-setting: which harness this is for, where this task fits,
    dependencies, how it connects to the other artifacts]

    ## Before You Begin

    If you have questions about:
    - The requirements or acceptance criteria
    - The approach or how the artifact should behave
    - Dependencies or assumptions
    - Anything unclear in the task description

    **Ask them now.** Raise any concerns before starting work.

    ## Your Job

    Once you're clear on requirements:
    1. Produce exactly the harness artifact(s) the task specifies, at the exact paths it names
    2. Write behavioral evals (following eval-driven harness development if the task says to)
    3. Run the task's evals and verify the artifact behaves as specified
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: [directory]

    **While you work:** If you encounter something unexpected or unclear, **ask questions**.
    It's always OK to pause and clarify. Don't guess or make assumptions.

    While iterating, run the focused eval for the artifact you're changing;
    run the full eval suite once before committing, not after every edit.

    ## Artifact Organization

    You reason best about artifacts you can hold in context at once, and your edits are
    more reliable when files are focused. Keep this in mind:
    - Follow the artifact layout defined in the build plan
    - Each artifact should have one clear responsibility with a well-defined interface
      (a skill's trigger, an agent's role, a hook's firing condition)
    - If an artifact you're creating is growing beyond the plan's intent, stop and report
      it as DONE_WITH_CONCERNS — don't split artifacts on your own without plan guidance
    - If an existing artifact you're modifying is already bloated or tangled, work
      carefully and note it as a concern in your report
    - In an existing harness, follow its established patterns. Improve artifacts you're
      touching the way a good harness builder would, but don't restructure things outside
      your task.

    ## When You're in Over Your Head

    It is always OK to stop and say "this is too hard for me." Bad work is worse than
    no work. You will not be penalized for escalating.

    **STOP and escalate when:**
    - The task requires harness design decisions with multiple valid approaches
      (e.g. whether one agent role should split into two)
    - You need to understand the target team's operating environment beyond what was
      provided and can't find clarity
    - You feel uncertain about whether your approach is correct
    - The task involves restructuring existing harness artifacts in ways the plan
      didn't anticipate
    - You've been reading file after file trying to understand the harness without progress

    **How to escalate:** Report back with status BLOCKED or NEEDS_CONTEXT. Describe
    specifically what you're stuck on, what you've tried, and what kind of help you need.
    The controller can provide more context, re-dispatch with a more capable model,
    or break the task into smaller pieces.

    ## Before Reporting Back: Self-Review

    Review your work with fresh eyes. Ask yourself:

    **Completeness:**
    - Did I fully produce everything in the spec, at the exact paths named?
    - Did I miss any requirements?
    - Are there failure modes I didn't handle (skill discovery misses, role
      confusion, permission edge cases)?

    **Quality:**
    - Is this my best work?
    - Are names clear and accurate (skill and agent names match what they do, not how they work)?
    - Are the artifacts lean and maintainable — no prompt bloat?

    **Discipline:**
    - Did I avoid overbuilding (YAGNI)?
    - Did I only build what was requested?
    - Did I follow the existing patterns of this harness?

    **Evals:**
    - Do evals actually verify agent behavior (not just echo the artifact's wording)?
    - Did I follow eval-driven harness development if required?
    - Are the pressure scenarios realistic for the target team?
    - Is the eval output pristine (no stray warnings or noise)?

    If you find issues during self-review, fix them now before reporting.

    ## After Review Findings

    If a reviewer finds issues and you fix them, re-run the evals that cover
    the amended artifacts and append the results to your report file. Reviewers
    will not re-run evals for you — your report is the eval evidence.

    ## Report Format

    Write your full report to [REPORT_FILE]:
    - What you built (or what you attempted, if blocked)
    - What you evaluated and eval results
    - **Eval-First Evidence** (if eval-driven harness development was required for this task):
      - RED: command run, relevant failing output before the artifact existed, and why the failure was expected
      - GREEN: command run and relevant passing output after the artifact was in place
    - Files changed
    - Self-review findings (if any)
    - Any issues or concerns

    Then report back with ONLY (under 15 lines — the detail lives in the
    report file):
    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - Commits created (short SHA + subject)
    - One-line eval summary (e.g. "14/14 scenarios passing, output pristine")
    - Your concerns, if any
    - The report file path

    If BLOCKED or NEEDS_CONTEXT, put the specifics in the final message
    itself — the controller acts on it directly.

    Use DONE_WITH_CONCERNS if you completed the work but have doubts about correctness.
    Use BLOCKED if you cannot complete the task. Use NEEDS_CONTEXT if you need
    information that wasn't provided. Never silently produce work you're unsure about.
```
