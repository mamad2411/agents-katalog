---
name: setup-lean-coding-agent
description: Initialize the current project with the Lean Coding Agent baseline for Codex, Claude Code, or both after installing its skills, including project guidance, skill overrides, and configurable subagents.
---

# Setup Lean Coding Agent

Run this skill after installing it with the Skills CLI to initialize the current project for Codex, Claude Code, or both. The Skills CLI owns skill installation, tracking, updates, and removal. The Node.js setup script copies baseline assets into the project, installs the subagents for each selected coding agent with the models chosen by the user and adds the upstream skills for the selected coding agents.

## Workflow

1. Ask which existing project directory to initialize. Offer the current working directory as the recommended default, and let the user choose it or provide another path. Do not silently assume the current directory.
2. Ask which coding agents to set up: `codex`, `claude-code`, or `both`. Recommend the agent running this skill when the user has no preference. Do not silently assume a selection.
3. For each selected coding agent, show its current models before asking about them. Treat these lists as current references; replace them with newer options if the official documentation has changed.

   **Codex.** Check the official [OpenAI model catalog](https://developers.openai.com/api/docs/models) and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). Show the latest generally available coding-capable model IDs and their supported reasoning-effort levels, with a short description of each model:
   - `gpt-6-astra` — most capable for complex reasoning and coding; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6.1-sol` — near-Astra performance for complex work at a lower cost; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-sol` — designed for complex coding and agentic workflows; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-luna` — efficient for focused, high-volume work; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

   Codex subagents default to `gpt-6.1-sol` for `planner` and `code-reviewer`, and `gpt-6-luna` for `bug-diagnostician`, `implementer`, and `explorer`.

   **Claude Code.** Check the official [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [subagent documentation](https://code.claude.com/docs/en/sub-agents). Subagents accept an alias (`fable`, `opus`, `sonnet`, `haiku`), a full model ID, or `inherit` to use the main conversation's model:
   - `fable` (`claude-fable-5-1`) — for demanding reasoning and long-horizon agentic work; slowest and most expensive.
   - `opus` (`claude-opus-5-5`) — for long-running agentic coding and knowledge work.
   - `sonnet` (`claude-sonnet-5-5`) — the best combination of speed and intelligence.
   - `haiku` (`claude-haiku-5-5`) — fastest.

   Claude Code subagents default to `opus` for `planner` and `code-reviewer`, and `haiku` for `bug-diagnostician`, `implementer`, and `explorer`.

   Codex `planner` and `code-reviewer` use `low` reasoning effort, `bug-diagnostician` and `implementer` use `xhigh`, and `explorer` uses `high`. Claude Code `planner` and `code-reviewer` use `low` effort, `bug-diagnostician` and `implementer` use `xhigh`, and `explorer` uses `high`. Then ask: “Which models should setup assign to `planner`, `bug-diagnostician`, `implementer`, `code-reviewer`, and `explorer` for each selected coding agent? Choose the defaults, or provide a model for each.” Preserve each agent's reasoning-effort setting.
4. Ask where `lean-grill-with-docs` should keep the project's `GLOSSARY.md` and ADRs. Recommend the skill's default, `docs/conventions/` (`docs/conventions/GLOSSARY.md` and `docs/conventions/adr/`), or let the user give a folder path relative to the project root, such as `docs/domain`. Always pass the answer as `--docs-dir`, including `--docs-dir docs/conventions` for the default; that value removes a folder override from an earlier run.
5. Run the bundled Node.js setup script from the target project, passing the selected coding agents and only the model options that apply to them:

   ```text
   node "<setup-skill>/scripts/setup-lean-coding-agent.mjs" "<target-project>" --tools <codex|claude-code|both> \
     --planner-model <codex-model> --bug-diagnostician-model <codex-model> --implementer-model <codex-model> --code-reviewer-model <codex-model> --explorer-model <codex-model> \
     --claude-planner-model <claude-model> --claude-bug-diagnostician-model <claude-model> --claude-implementer-model <claude-model> --claude-code-reviewer-model <claude-model> --claude-explorer-model <claude-model> \
     [--docs-dir <folder>]
   ```

   Locate `<setup-skill>` from this skill's installed directory. Do not ask the user to find or run the script. It uses Node.js and npm's `npx` on Windows, macOS, and Linux. If setup fails, report the failed command and stop; rerun only after resolving the reported environment or network issue.
6. After setup completes, ask the user whether they want to run the `define-conventions` skill to capture project conventions in `docs/conventions/`. Run it only if they agree. If the skill is not available in the active session, read `<target-project>/.agents/skills/define-conventions/SKILL.md` and follow it directly after they agree.
7. Confirm the project contains the baseline files, `.agents/skill-overrides/` and its index, `.agents/templates/plan.md`, `.agents/templates/implementation-report.md`, `.agents/templates/code-review.md`, `.agents/skills/`, and the upstream skills. For Codex, also confirm `.codex/config.toml` with the bundled multi-agent defaults and `.codex/agents/` with all five agents. For Claude Code, confirm `.claude/agents/` with all five agents and the status line in `.claude/statusline.mjs` and `.claude/settings.json`. Summarize the selected coding agents, installed skills, selected models and reasoning effort, the `lean-grill-with-docs` documentation folder, and whether `define-conventions` was run or deferred.

## Managed Files And Effects

- The script defaults to the current directory if the target path is omitted. It requires an existing directory. `--tools` defaults to `codex`.
- If Codex is selected and `.codex/config.toml` is missing, setup copies the bundled baseline config, including a footer status line for the model and reasoning level, project name, Git branch, context window size, and used tokens. Setup does not create `.codex/` files when only Claude Code is selected.
- If Claude Code is selected and `.claude/statusline.mjs` is missing, setup copies the bundled two-line status line (model, effort, project, Git branch, context usage against the configured `autoCompactWindow`, and 5-hour and 7-day rate limits). It adds `statusLine` to `.claude/settings.json`, creating the file if needed, only when no status line is already set, and adds default `modelSettings` auto-compaction limits (`autoCompactWindow`: Opus 450000, Sonnet 350000, Haiku 250000 tokens) for each model that has none. It also appends `Artifact` and `PowerShell` to `permissions.deny` when missing, keeping any existing deny rules. `Artifact` is denied because coding sessions do not need claude.ai artifacts and its tool and skill definitions consume context; `PowerShell` is denied so Claude Code on Windows runs every shell command through Bash (POSIX), keeping commands and scripts consistent across platforms. Setup does not create `.claude/` status line files when only Codex is selected.
- `AGENTS.md` and `CLAUDE.md` are copied verbatim from `references/baseline/` on every run, regardless of `--tools`; this managed sync replaces the existing baseline copies. Do not skip this step because either file contains baseline instructions. Put project-specific shared rules in `docs/conventions/` and local, private notes in `AGENTS.override.md`.
- The bundled subagents for each selected coding agent, baseline override files, and managed upstream skills are refreshed on each run. Other agents in `.codex/agents/` or `.claude/agents/`, existing project context files, local-private files, and project-owned override index entries are preserved.
- The setup creates `AGENTS.override.md`, `.agents/lessons/`, `.agents/skill-overrides/`, and required `.gitignore` entries when missing. It does not create `docs/conventions/`; the `define-conventions` skill writes those files. Managed ignore entries include the local files and agent task/report directories.
- With `--docs-dir <folder>`, setup writes `.agents/skill-overrides/lean-grill-with-docs.md` and its index entry so `lean-grill-with-docs` keeps `GLOSSARY.md`, `GLOSSARY-MAP.md`, and `adr/` in that folder. The folder must be inside the project. Reruns with a new folder update the generated override, `--docs-dir docs/conventions` removes it, and reruns without the option keep it. Setup stops rather than replace a project-owned `lean-grill-with-docs.md` override, which can set the same folder by hand.
- Install the baseline skills you want through `npx skills add aloilor/lean-coding-agent` before setup, selecting the same coding agents. Setup preserves that selection and does not copy, refresh, or delete skill folders. Upstream dependencies are installed through the Skills CLI.
- It copies the shared plan, implementation-report, and code-review templates into `.agents/templates/` for every selected coding agent. The planner, implementer, and code reviewer read these templates when writing their artifacts. Setup refreshes `plan.md`, `implementation-report.md`, and `code-review.md` on every run while preserving other project-owned templates.
- Use `npx skills check` to check for available skill updates.
- Upstream skills are installed through `npx skills add` for the selected coding agents and require network access.
- The Node.js script is the cross-platform entry point for project configuration and upstream dependency installation. The Skills CLI manages the skills themselves.

## Bundled References

See [references/README.md](references/README.md) for what each bundled file is and which source it snapshots.
