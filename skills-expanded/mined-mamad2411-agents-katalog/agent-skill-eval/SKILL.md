---
name: agent-skill-eval
description: >
  Evaluate whether a skill actually helps. Use when testing or measuring skill
  lift, running harness evals across OpenCode/Claude Code/Codex, validating
  evals.json, or asking "does this skill work", "skill eval", "benchmark a
  skill", "with_skill vs without_skill". Triggers: agent-skill-eval, ase,
  skill benchmark, eval harness, run evals.
---

# Agent Skill Eval (harness)

The missing eval layer for agent skills. It installs your skill into a fresh
workspace, runs the real agent CLI (not the raw API) on your test prompts
— with and without the skill — grades outputs with deterministic state-diffs
plus an LLM rubric, and reports lift, pass rates, tokens, and time.

Installed as Python CLI `agent-skill-eval` / alias `ase` plus
`python -m agent_skill_eval`. Requires the agent CLIs you target
(`opencode` / `claude` / `codex`) and an `OPENROUTER_API_KEY` or
`OPENAI_API_KEY` for rubric grading. On this machine the binary is at
`...Python311\Scripts\agent-skill-eval.exe` (add that Scripts folder to PATH
or use `python -m agent_skill_eval`).

## When to use
- You wrote a `SKILL.md` and want proof it helps.
- Before shipping or iterating a skill.
- Comparing two skill versions.
- CI gate for skill repos (`run-all` + `--fail-on-assertions`).

## Quickstart

```bash
# validate suite first (cheap)
python -m agent_skill_eval validate path/to/evals.json

# single skill, single suite, 3 repeats
python -m agent_skill_eval run \
  --skill ./Skills/eval/write-release-notes \
  --evals ./Skills/eval/write-release-notes/evals/evals.json \
  --agent opencode --agent-model opencode=gpt-4o-mini \
  --runs 3 --baseline

# repo-wide (every paired skill/evals.json under a root)
python -m agent_skill_eval run-all --root ./Skills \
  --agent opencode --baseline --report

# reports
python -m agent_skill_eval report --workspace ./eval-workspace/write-release-notes-workspace --show-evidence
python -m agent_skill_eval report-all --workspace ./eval-workspace
python -m agent_skill_eval validate-all ./Skills
python -m agent_skill_eval list ./Skills
```

`run-all` discovers `SKILL.md` + `evals/evals.json` pairs, runs each with and
without the skill (`with_skill`/`without_skill`), writes
`iteration-N/<eval-id>/<run>/` with `outputs/`, `timing.json`, `grading.json`,
`benchmark.json`, `cleanup.json`, and a static HTML report.

## Skill layout expected

```
my-skill/
  SKILL.md                 # required, frontmatter name+description
  references/              # optional, included in skill context
  scripts/                 # optional, exposed via manifest
  evals/
    evals.json             # { skill_name, evals: [{id,prompt,expected_output,files,assertions}] }
    files/                 # fixtures referenced by evals[].files
```

`--strict` enforces agentskills.io spec; without it warnings only.

## Eval file (agentskills.io)

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": "basic",
      "name": "basic behavior",
      "prompt": "Use the attached data to summarize revenue.",
      "files": ["evals/files/input.csv"],
      "expected_output": "The response identifies the highest revenue month.",
      "assertions": ["The output identifies the highest revenue month."]
    }
  ]
}
```

If `assertions` omitted but `expected_output` present, it is promoted to an
assertion. Add `tool_assertions` for deterministic checks (branch/commit/push,
file existence, command ran).

## Key CLI commands

- `run` — single skill/suite. Flags: `--agent opencode|claude-code|codex`,
  `--agent-model <agent>=<model>`, `--runs`, `--concurrency`, `--baseline`,
  `--cleanup`, `--timeout 600`, `--eval-id <id>`,
  `--max-total-tokens-per-case 200000`, `--pricing-config`, `--grader-model`,
  `--source-repo https://github.com/foo/bar.git` (needed for commit-push-pr).
- `run-all` — every pair under `--root`. Flags: `--suite-concurrency 4`,
  `--plan-only`, `--changed-only --base-ref origin/main`, `--junit-xml`,
  `--fail-on-assertions --min-pass-rate 0.8`.
- `validate` / `validate-all` — schema + file refs + duplicate-id.
- `list` — discover skills/evals.
- `report` / `report-all` / `status` / `compare` / `portfolio` / `rerun-failed`
  / `grade` / `archive-run` / `init` — post-run utilities.

## What grading checks

- Deterministic: git state diff (commit-push-pr), file existence/content,
  tool ran, side-effect level (`static` for read-only skills like review-diff).
- LLM rubric: judge model sees `expected_output` + `assertions`; grades each
  side independently. Use `--grader-model deepseek/deepseek-v4-flash` etc.
  for cost control.

## Example skills in this package (eval/)

This folder ships 6 reference skills (from `tardigrde` + `darkrishabh`) that
show the spectrum the harness supports:

| Skill | What it tests | Grading |
|---|---|---|
| `write-release-notes` | commit history → grouped RELEASE_NOTES.md, anti-fabrication | LLM rubric; offline |
| `fix-failing-tests` | run tests, diagnose, fix, verify | deterministic + file; offline |
| `commit-push-pr` | branch/commit/push/PR via gh CLI | state-diff; needs --source-repo |
| `review-diff` | .diff review without modifying files | chat-only; offline |
| `validate-config` | config file → CONFIG_REPORT.md | file + content; offline |
| `basic-skill` | CSV → highest revenue month | basic assertions |

Each lives at `eval/<name>/SKILL.md` with its `evals/` suite.

## Checklist

- [ ] `evals/evals.json` validates: `python -m agent_skill_eval validate ...`
- [ ] Every `files` path exists.
- [ ] Assertions measurable (avoid vague "good quality").
- [ ] Negative control included where useful.
- [ ] Chose `side-effect-level` (static for read-only).
- [ ] Ran with `--baseline` at least once to see lift.
- [ ] Pinned cheap model while iterating (`haiku`, `gpt-5-mini`).

## Related skills
`writing-skills`, `verification-before-completion`, `systematic-debugging`,
`test-driven-development`.
