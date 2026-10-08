---
name: run-eval
description: Run EvalView regression checks against golden baselines to detect regressions in AI agent behavior after code, prompt, or model changes.
---

# Run Eval

Use this skill after making changes to an AI agent (prompt edits, model swaps, tool changes, code refactors) to verify nothing broke.

## What this does

EvalView compares current agent behavior against saved golden baselines. It runs your test cases, evaluates the outputs, and reports a diff status for each test:

- **PASSED** — behavior matches the baseline
- **OUTPUT_CHANGED** — output shifted but may be intentional
- **TOOLS_CHANGED** — different tools were called
- **REGRESSION** — score dropped significantly (blocking failure)

## Steps

1. **Locate the test directory.** Look for `tests/evalview/` in the project. If it exists, use that. Otherwise check for a `tests/` directory with `.yaml` test files.

2. **Run a regression check** using the `run_check` MCP tool:
   - If checking all tests: call `run_check` with the detected `test_path`
   - If checking a specific test: also pass the `test` parameter with the test name

3. **Interpret results:**
   - If all tests pass, confirm to the user that no regressions were found
   - If REGRESSION is reported, show the diff (score delta, tool changes, output similarity) and offer to help fix it
   - If OUTPUT_CHANGED or TOOLS_CHANGED, flag it as a warning — the user should decide if the change is intentional

4. **If changes are intentional**, offer to update the baseline by calling `run_snapshot` with an explanatory `notes` parameter.

5. **Generate a visual report** (optional) by calling `generate_visual_report` for a detailed HTML breakdown of traces, diffs, scores, and timelines.

## CLI equivalent

```
evalview check tests/evalview/
evalview check tests/evalview/ --test "my-test"
evalview snapshot tests/evalview/ --notes "updated after prompt refactor"
```

## Tips

- Use `run_check` frequently — it calls the Python API directly with no subprocess overhead.
- A score delta near zero with TOOLS_CHANGED often means the agent found an equivalent path.
- Always snapshot after confirming intentional changes so future checks compare against the new baseline.
