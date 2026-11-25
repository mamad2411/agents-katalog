---
name: prompt-regression-testing
description: Builds and runs regression tests for prompts, skills and agents so changes can be checked instead of guessed. Use whenever the user changes a prompt or SKILL.md and wants to know if it got better or worse, asks how to test or evaluate an LLM feature, wants a frozen test set, pass rates over repeated runs, a baseline comparison or CI checks for prompts, even if they only say "did my edit break anything". Model agnostic, deterministic checks, flags regressions.
---

# prompt-regression-testing

A change to a prompt, skill or agent can fix one case and silently break three. Freeze a small set of realistic cases, check them with deterministic rules, and compare every change to a saved baseline.

```
prompt-regression-testing/
├── SKILL.md
├── scripts/
│   └── run_cases.py          run cases via a command or recorded answers; checks, repeats, baseline diff
├── references/
│   └── case-design.md        coverage map, check types, non-determinism, subjective quality, CI
└── templates/
    └── cases.json            example suite with typical, format, safety and negative cases
```

## When to use

- Editing a prompt, SKILL.md or agent and needing proof it did not get worse
- Choosing between two prompt versions
- Setting up checks before shipping an LLM feature
- A bug was fixed and must never return

## Workflow

1. **Collect cases** from real requests. Cover typical, edge, format, safety, and at least one negative case that should not trigger the behavior (`references/case-design.md`). Start with about 20.
2. **Write checks** per case in `cases.json` (copy `templates/cases.json`). Prefer several loose checks over one strict check.
3. **Write a runner**: reads the input from stdin, prints the answer to stdout. Keep keys in environment variables.
4. **Freeze a baseline** on the version you trust:
   `python3 scripts/run_cases.py cases.json --cmd "python3 runner.py" --save baseline.json`
5. **Change the prompt, then compare**:
   `python3 scripts/run_cases.py cases.json --cmd "python3 runner.py" --baseline baseline.json`
   Any `[REGRESSION]` line means a case that passed before now fails.
6. **Handle variation** with `--repeat 10 --min-pass-rate 0.9` for non-deterministic outputs.
7. **Decide**: keep the change only if there are no regressions, or the trade is explicit and accepted. Save the new baseline and commit cases with the change.
8. **Add a case** for every bug you fix.

## Rules

- Never edit a frozen case to make it pass; add a new one
- Write cases before looking at the new output, or the test will bend to the answer
- One behavior per case, so failures point to a cause
- Do not lower the pass rate to hide flakiness; rewrite the prompt
- Use recorded answers (`--outputs`) in CI and run live checks on a schedule
- Deterministic checks cannot judge style; for that use a rubric with spot checks by hand

## Commands

```bash
python3 scripts/run_cases.py cases.json --cmd "python3 runner.py"
python3 scripts/run_cases.py cases.json --outputs answers.json
python3 scripts/run_cases.py cases.json --cmd "..." --repeat 10 --min-pass-rate 0.9 --save results.json
```

Exit code is 0 when every case meets the pass rate and nothing regressed, 1 otherwise.

## What to report back

| Field | Content |
|-------|---------|
| Suite | number of cases and kinds covered |
| Result | passed over total, per failing case with the reason |
| Comparison | regressions, fixes and new cases versus the baseline |
| Variation | repeats and pass rates for flaky cases |
| Decision | keep, revert or fix, with the evidence |

## Related skills

- `skill-authoring`: create or fix the skill that these tests protect
- `multi-agent-orchestration`: evaluate agent systems against a single-agent baseline
- `systematic-debugging`: trace a failing case to its cause
