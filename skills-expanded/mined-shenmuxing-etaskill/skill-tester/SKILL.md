---
name: skill-tester
description: Record observable skill test runs for debugging. Use when the user wants to test, dry-run, debug, inspect, or compare how a Codex skill behaves on a concrete request; creates a local non-overwriting Markdown report with the visible process, files read, commands run, changed artifacts, errors, and a brief behavior summary. Does not certify skill quality or replace user judgment.
---

# Skill Tester

## Purpose

Use this skill to make a skill run observable. The output is a local debug report that helps the user inspect what happened during a concrete test of another skill.

Do not turn this into an evaluation framework. Do not assign formal pass/fail status unless the user explicitly supplied pass/fail criteria.

## Workflow

1. Identify the target skill and test request.
   - Record the target skill name and path if known.
   - Record the user's exact test request or a concise quoted paraphrase if the request is long.
   - If the target skill or task is ambiguous, ask the minimum question needed before running the test.

2. Create a local report file before or at the start of the run.
   - Prefer a project-local `.skill-test-runs/` directory under the current workspace.
   - Create the directory if it does not exist.
   - Use a conspicuous filename:

```text
SKILL_TEST_REPORT_<skill-name>_<YYYYMMDD-HHMMSS>.md
```

   - If the file already exists, append `-2`, `-3`, and so on until the path is unused.
   - Treat the report as local debugging output. Do not place it in tracked documentation unless the user explicitly asks.

3. Run the target skill normally on the concrete request.
   - Follow the target skill's own instructions.
   - Keep a running record of visible actions: files read, commands run, files edited, generated artifacts, tool failures, and user-facing decisions.
   - Do not include hidden chain-of-thought or private reasoning. Summarize decisions and observations at a practical level.

4. Write the report.
   - Include enough detail for the user to reproduce or debug the run.
   - Redact tokens, credentials, cookies, private account identifiers, and other secrets if they appear in command output or files.
   - Keep local/private machine paths only in the local report when needed for debugging; do not copy those details into public-facing repository docs.

5. Final response.
   - Return the report path.
   - Briefly state what was tested, what the target skill actually did, and whether any obvious blockers or uncertainties were observed.

## Report Template

Use this shape unless the user requests a different format:

````markdown
# Skill Test Report: <skill-name>

## Brief

- Target skill: `<skill-name>`
- Target path: `<path or unknown>`
- Test request: <user request>
- Run time: <local timestamp>
- Result summary: <what happened in 2-5 bullets>

## Visible Process

1. <step actually taken>
2. <step actually taken>

## Files Read

- `<path>` - <why it was read>

## Commands Run

```text
<command>
```

Outcome: <exit code and concise result>

## Files Changed Or Created

- `<path>` - <what changed>

## Outputs And Artifacts

- `<path or artifact>` - <what it contains>

## Errors, Ambiguities, And Blockers

- <issue or "None observed">

## Behavior Notes For User Debugging

- <what the target skill seemed to handle well>
- <where the target skill was unclear, overbroad, under-specified, or hard to follow>
````

## Boundaries

- Do not claim the target skill is public-ready, safe, correct, or complete from this report alone.
- Do not automatically edit the target skill unless the user explicitly asks for fixes after the test.
- Do not create broad test matrices unless the user asks for a more formal test plan.
- Do not write hidden reasoning, system prompts, or private deliberation into the report.
