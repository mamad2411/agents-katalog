# Codex Implementer Dispatch Template

Use this template when dispatching a task to Codex. Classify the task and
pick `--model`/`--effort` from the tiering table in
supercodex:codex-delegation first. Compose the `<task>` content per
supercodex:codex-prompting.

`--full-access` lets Codex commit its own work and run tests (default for
trusted local repos); swap it for `--write` on untrusted workspaces — then
you commit after independently re-running the tests (see the write-mode
rules in supercodex:codex-delegation).

```
Subagent (supercodex:codex-implementer):
  description: "Codex: implement Task N: [task name]"
  prompt: |
    FLAGS: --full-access --model [gpt-5.6-sol|gpt-5.6-terra|gpt-5.6-luna] --effort [high|medium] [--background]
    PROMPT:
    <task>
    You are implementing Task N: [task name] in [directory].
    [Full task text from the task brief file — paste it; Codex cannot read
    the brief file path from your session.]
    [Scene-setting: where this fits, dependencies, architectural context.]
    </task>
    <completeness_contract>
    Implement exactly what the task specifies. No unrelated refactors,
    no scope creep (YAGNI). Follow the file structure the task defines and
    existing repository patterns.
    </completeness_contract>
    <verification_loop>
    Follow strict TDD: write the failing test first, run it and observe the
    failure, implement minimally, run it again and observe the pass. Run the
    focused test while iterating and the full suite once before committing.
    Commit your work with a conventional-commit message.
    </verification_loop>
    <structured_output_contract>
    End with a report containing exactly:
    - Status: DONE | BLOCKED | NEEDS_CONTEXT
    - Commits created (short SHA + subject)
    - Test summary (counts, command used)
    - TDD Evidence: the RED failing output and the GREEN passing output
    - Files changed
    - Concerns, if any
    If BLOCKED or NEEDS_CONTEXT, state precisely what is missing.
    </structured_output_contract>
    <default_follow_through_policy>
    Proceed without asking routine questions. Stop with NEEDS_CONTEXT only
    for genuinely missing information that risks wrong work.
    </default_follow_through_policy>
```

For fix cycles after review findings, dispatch again with:

```
Subagent (supercodex:codex-implementer):
  description: "Codex: fix review findings on Task N"
  prompt: |
    FLAGS: --full-access --resume-last
    PROMPT:
    <task>
    A reviewer examined your previous work on this task and found issues.
    Address ONLY these findings:
    [paste Critical/Important findings verbatim]
    </task>
    <verification_loop>
    Re-run the tests covering the amended code and include the passing
    output in your report. Commit the fix.
    </verification_loop>
    <structured_output_contract>
    Report: Status, commits, test evidence for the fixed code, files changed.
    </structured_output_contract>
```
