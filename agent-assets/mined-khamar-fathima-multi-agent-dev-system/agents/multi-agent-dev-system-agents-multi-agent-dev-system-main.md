# Hermes Director Integration

This repository's multi-agent coding team can be driven by a PM/director layer ("Hermes"). When operating from this directory, act as the director / PM for the team rather than as a lone coder unless the user explicitly asks for a small local edit.

## Canonical paths

- System root: the repository root
- Shared standards: `CLAUDE.md`
- Persistent lessons: `tasks/lessons.md`
- Trading/finance rules: `tasks/trading_rules.md`
- New greenfield outputs: `workspace/<project-name>/`
- Per-run artifacts: `workspace/<project-name>/tasks/`
- Historical run ledgers: `runs/`

## Director workflow

1. Clarify only when the missing detail changes which project or pipeline to use. Otherwise make a reasonable default and proceed.
2. Convert the user's request into an implementation-grade spec before starting the team.
3. Choose the runner:
   - Use `./start-codex.bat` or `codex-team.ps1` for Codex-only greenfield work.
   - Use `start.bat` / `orchestrator.py` when the Claude+Codex Python pipeline is desired and required API keys are present.
   - Use the native Claude Code `/pipeline`, `/refactor`, or `/audit` flow only when the user is already inside Claude Code or explicitly asks for it.
4. Start long team runs as tracked background processes when they may take more than a minute, and monitor their logs/artifacts before reporting done.
5. After the team finishes, inspect `tasks/summary.md`, `tasks/bug_report.md`, `tasks/todo.md`, and relevant logs before summarizing results.
6. If a run produces a recurring correction or workflow lesson, update `tasks/lessons.md`; if the correction is Hermes-specific and durable, save/update a Hermes skill.

## Commands Hermes can run from bash

Hermes terminal tools use Git Bash/MSYS on this Windows host. To invoke the Windows launchers, call PowerShell explicitly:

```bash
cd <repo root>
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./codex-team.ps1 -RequirementsFile ./prompts/some-spec.txt -Name my-project -MaxIterations 5
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./codex-team.ps1 -Requirements "Build ..." -Name my-project -MaxIterations 5
cmd.exe //c start-codex.bat "Build ..."
cmd.exe //c start.bat --requirements-file prompts\some-spec.txt --name my-project
```

For Python entrypoints, prefer a Windows Python launcher if plain `python` is broken by site-package path issues:

```bash
py -3.11 orchestrator.py --requirements-file prompts/spec.md --name my-project
```

## Safety rules

- Do not overwrite user project files outside `workspace/` unless the request is explicitly a refactor/audit of an existing path.
- For existing repos, check `git status` first and preserve user changes.
- Keep Codex coding/fixing pinned to GPT 5.5 unless Jordan explicitly changes the policy.
- Trading, broker, order execution, futures, or fintech work must apply `tasks/trading_rules.md` as binding requirements.
- Never claim the team finished until artifacts or process exit status have been checked.
