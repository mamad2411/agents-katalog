---
name: groma
description: Initializes or updates a project for AI-assisted work - methodology, skills, docs/ and AGENTS.md. Use for /groma, "set up this project", "onboard this repo", "initialize project docs", or re-running groma on an initialized project.
---

# groma

Lay out a project before building on it. Eight steps, each announced, each safe to re-run.

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

**Writes are additive.** groma creates files only at paths that do not exist, plus its own `.groma/` and `docs/_groma/`. Anything that would change an existing file becomes a snippet in the findings report. Third-party installers run only after the user agreed when they touch existing files.

Sibling skills live next to this folder (`../groma-detect/`, `../groma-survey/`, ...). Run a step by following that skill's `SKILL.md`. If a sibling is missing, skip its step and print its install command:
`npx skills add Zeotyn/groma --skill <name>`.

## Mode

- `<project>/.groma/config.yaml` absent: **init mode**, all steps.
- Present: run `sh scripts/validate-config.sh <project>/.groma/config.yaml --catalog catalog.yaml` ([catalog.yaml](catalog.yaml) is a copy of groma-skills' catalog). Exit 3: stop and print the update command. Errors: show them with line numbers and ask the user to fix or let you reconfigure. Valid: **update mode**: resume at the first step whose `steps.<name>` is `pending`; when all are `done`, run steps 6 to 8 again (missing docs, freshness, summary) and offer to reconfigure skills or agents. Compare `initialized_with` with [VERSION](VERSION) and apply the rows of [references/upgrades.md](references/upgrades.md) in between, naming the version that introduced each addition. Refresh the copied groma skills yourself, see "Skill copies"; this needs no CLI.

**CLI hand-off.** `npx groma-cli init` may already have done the config, methodology and skills steps. When `steps.config`, `steps.methodology` and `steps.skills` are all `done`, do not repeat them or ask their questions (agents, methodology, skills); go on with detect, the content interview (purpose, users, vision, UI only if unknown), docs and agents. When `steps.methodology` or `steps.skills` is `pending`, third-party installs are still open: offer once to run them now (steps 4 and 5 with their consent flow) and name `npx groma-cli update` in a terminal as the alternative. Without a yes, install nothing, leave the step `pending` and make the summary's Next action "Run `npx groma-cli update` in a terminal". Copying and refreshing the groma skills never needs the CLI ("Skill copies"). Agents listed in `agents_via_plugin` are agents for which the user declined the copy in the CLI: they get their skills from the plugin, and no copies are made for them.

## Steps

Announce each step as `Step N of 8: <name>, <what it does>`. After each step set `steps.<name>` in the config (`done`, `pending` or `skipped`), once the config exists.

1. **detect**: follow `../groma-detect/SKILL.md`. Result: project type and evidence.

2. **interview**: ask only what the folder does not answer, one question at a time, recommended option first:
   - greenfield: what is being built and for whom (feeds vision and concept), does it have a UI, the main language or stack, which agents (claude, copilot, gemini, cursor, codex).
   - brownfield: confirm the project purpose in one sentence from README and code, ask about UI only when no frontend is visible, ask about agents only when no agent folders exist.
   - style tools: run `sh scripts/style-drift.sh <project>` (read-only). When it prints a `tool` line, ask nothing. Otherwise look up the stack's default tools in [references/code-style-tools.md](references/code-style-tools.md) (the rows with `Default: yes` for the stack, plus every row with stack `all`, so EditorConfig is always in the set) and ask once, for example "Set up EditorConfig and Ruff for formatting and linting? (recommended)". Brownfield: the recommended option is "document only"; the tools are the second option. Record the answer as the chosen tools, `document only` or `none`.
   - repository (skip it when the config already has `git.enabled: false`): run `sh scripts/git-init.sh --check --type <project type> <project>` (read-only).
     - `state none` (not inside a work tree): ask once "Set up a git repository here?" with the line's `recommend` value as the recommended option (greenfield yes; brownfield no, because a folder with code but without `.git/` usually came out of a repository elsewhere). Yes: run `sh scripts/git-init.sh --stack <stacks> <project>`, with the interview's stack written as names from the Stack column of [references/gitignore.md](references/gitignore.md) (Node.js is `Node`); it runs `git init` on `main` and writes `.gitignore` from that table only when none exists. No: record `git.enabled: false` and ask no other git question.
     - `state parent`: name the line's top level and ask once whether to use that repository (recommended) or set up one for the project (then run `git-init.sh` as on yes).
     - `state missing` (git is not on PATH): ask no git question, keep the defaults and say "git not found, no repository set up" in the summary.
   - git workflow: in a git repository (`state repo`, the parent chosen, or set up just now), run `sh scripts/git-practice.sh <project>` (read-only) and ask once for the integration strategy (`rebase`, `merge`, `squash`) and once for the push policy (`ask`, `auto`, `never`). Greenfield: recommend `rebase` and `push: ask`. Brownfield: recommend the script's `integrate` value and show its evidence, for example "Integrate changes with merge commits? (recommended: 28 of 30 merges are pull-request merges)", and recommend `push: ask`. Take `commits` from the script's `commits` line without asking (greenfield: `conventional`). Record `integrate`, `commits` and `push`.
   Done when name, purpose, `has_ui`, `agents`, the style answer and the git answers are known.

3. **config**: create `<project>/.groma/config.yaml` from [templates/config.yaml](templates/config.yaml) (it carries the `review` and `reminders` defaults: autonomous loop, reviewer auto) with the answers so far (methodology and skills stay as placeholders filled by steps 4 and 5; write `none` where still unknown; `git.integrate`, `git.commits` and `git.push` from the interview, the template's defaults when it asked nothing; `git.enabled: false` when the repository was declined), `initialized_with: groma@<VERSION>`. Run `sh scripts/check-prereqs.sh` and report missing required tools with their install hint.

4. **methodology**: follow `../groma-methodology/SKILL.md`. When the CLI already ran the methodology init, still run that skill's step 4 (Convention: conventions baseline and check-conventions) if not done.

5. **skills**: follow `../groma-skills/SKILL.md`.

6. **docs**:
   - brownfield: survey first, then follow `../groma-lay-out/SKILL.md` with the survey results. When your agent can start a subagent (in Claude Code the Agent tool), start one with the project path and this task: "Follow `<absolute path of ../groma-survey/SKILL.md>` on `<project>` as a subagent; reply with the report path and the filled report, do not write the report file." The survey asks nothing there (its "Where you cannot ask"). Write the reply's report to its path at once, unchanged: everything after the `report: <path>` line, starting at the first `---` line (the `report:` line itself is not part of the file). Do not shorten, merge, reformat or summarize it, and do not wait for later steps. Then run `sh <absolute path of ../groma-survey/scripts/report-check.sh> <report>`; on exit 1 fix only the lines it names (a missing section gets its template heading and `None found.`). Later additions, such as snippets from other steps, go in with an edit under "Snippets for existing files"; never rewrite the report. Tell the user only its Hand-off lines, ask about its `unconfirmed` findings yourself, one at a time, and read sections of the report only as lay-out needs them. Without subagents, follow `../groma-survey/SKILL.md` here.
   - greenfield: follow `../groma-lay-out/SKILL.md` with the interview answers.
   When the interview chose style tools, groma-lay-out's "Style setup" runs first: config files at free paths, one accepted ADR per tool, installs through the consent flow (`.groma/install.sh` when declined). "document only" and "none" create no config and no ADR; the doc records the decision. Update mode never creates tool configs unless the user asks.

7. **agents**: follow `../groma-agents/SKILL.md`, then do "Skill copies" below.
   Done when the agent files exist and `steps.skills_copy` is `done` or `skipped`.

8. **summary**: first commit, then print. Set `steps.summary: done` first, so the commit leaves a clean tree. When `git.enabled` is not `false` and `git -C <project> rev-parse -q --verify HEAD` fails (a repository without commits), ask once "Record the setup as the first commit? (recommended)". Yes: run `sh scripts/first-commit.sh <project> <VERSION>`. Exit 3 (no git identity): nothing is committed; the Next action is the commands of its `no-identity` line. Any other nonzero exit: show git's error unchanged and make the Next action "fix the cause, then run `git add -A . && git commit -m "chore: set up project with groma <VERSION>"`"; never retry with other flags. A repository with commits gets no question and no commit.
   ```
   groma <VERSION> · <project type> · step 8 of 8 done

   Created:   <files, grouped by folder>
   Untouched: <existing files that got a snippet in docs/_groma/findings-*.md>
   Findings:  <n high> high · <n medium> medium · <n low> low   → docs/_groma/findings-<date>.md
   Skills:    <n groma skill files copied for <agents>, or "not copied (declined)">
   Plugin:    <only after a `plugin` line: the reason and the disable command, see "Skill copies">
   Pending:   <commands in .groma/install.sh, or "none">
   Git:       <"first commit <hash>", "no commit (<reason>)", or "off (git.enabled: false)"; omit in a repository with history>

   Next: <one concrete action, e.g. "Review docs/adr/0003-use-postgresql.md (proposed)",
          or when nothing is open: "Start your first change with groma-loop">
   ```
   Translate the labels (`Created`, `Next`, ...); paths and commands stay literal. Done when the summary names exactly one next action.

## Skill copies

The groma skills belong into the project, so a teammate who clones the repository gets them. [scripts/materialize.sh](scripts/materialize.sh) copies the groma skill folders installed next to this one into each agent's project skill folder, with the rules of `npx groma-cli init`: copied `SKILL.md` files carry `metadata.generatedBy: groma@<version>`, every file is recorded with its SHA-256 in `.groma/generated.json`, and a file or folder groma did not create is never touched. Never copy or edit skill files yourself; when the script fails (for example neither `sha256sum` nor `shasum` exists), report its message and leave `steps.skills_copy` as it was.

The script refuses in three cases (exit 1, nothing written); do not work around any of them:
- **The skills you run are a copy that groma made** (message "a copy that groma made"): for example a teammate without the plugin runs `/groma` from the project's `.claude/skills/groma/`. Copies cannot refresh themselves. Tell the user the copies stay as they are and how to update them: install or update groma itself (`claude plugin update groma`, or `npx skills add Zeotyn/groma --all`) and run `/groma` again, or run `npx groma-cli update` in a terminal. Go on with the other steps.
- **The project's copies come from a newer groma** (message "newer than this groma"): tell the user to update their groma first. Never pass `--allow-downgrade`, unless the user explicitly asks to go back to an older groma; `--force` does not lift this refusal.
- **The project is groma's own repository** (message "source repository"): nothing to copy; set `steps.skills_copy: skipped`.

When the skills you run were installed into the project with `npx skills add` (they lie in `.agents/skills/` without `generatedBy`), the script copies them to the other agents' folders, prints a `note` for the folder that is the source itself and `conflict` lines for the links `npx skills` created; that is expected, pass it on briefly.

- **Init, in step 7.** When `steps.skills_copy` is `done` or `skipped` (set by `npx groma-cli init` or an earlier run), ask nothing. Otherwise ask once, with yes recommended: "Put the groma skills into the project so the team gets them with the repository?"
  - Yes: run `sh scripts/materialize.sh --agents <agents, comma-separated> <project>` and set `steps.skills_copy: done`.
  - No: write no skill folder and set `steps.skills_copy: skipped`.
- **Update mode.** When `steps.skills_copy` is `done`, or the key is missing and `.groma/generated.json` exists, run `sh scripts/materialize.sh --update <project>` (agents come from the config, without `agents_via_plugin`) before step 6. Unchanged copies move to the new version. Files are deleted only when unchanged and only when groma no longer ships them (a file that left a skill, or a skill listed in [retired-skills.txt](retired-skills.txt)); copies of skills that your groma install merely does not contain stay. When the key is missing and no `.groma/generated.json` exists, ask the init question once. `skipped`: do nothing.
- **Output.** `create`, `update` and `remove` lines are done work; count them for the summary. For each `edited` line tell the user the file was edited by hand and kept (`--force` replaces it; use it only when the user asks). For each `conflict` line tell the user the path was not created by groma, or is or leads through a symbolic link, and was left untouched. Pass on `note` lines. `--dry-run` shows the plan without writing.
- **Plugin.** A line `plugin<TAB>claude<TAB><command>` means the groma Claude Code plugin is active as well. The copy is made all the same, because it is what the team gets. Tell the user: Claude Code now lists every groma skill twice in this project, once from the plugin and once from the project copy, and the command `claude plugin disable groma@groma --scope local`, run in the project, switches the plugin off for this project only (it stays on everywhere else). Print the command unchanged. Never run it and never edit a settings file. Repeat the command once in the summary.

## Rules for every step

- Ask at most one question per message, with a recommended default.
- Unknown content is written as `Not yet documented.`, never guessed.
- An aborted run leaves valid files; the next run resumes from `steps`.
