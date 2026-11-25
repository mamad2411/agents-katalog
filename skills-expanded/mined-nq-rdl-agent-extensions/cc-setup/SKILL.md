---
name: cc-setup
license: CC-BY-4.0
description: >-
  Onboard a user onto the RDL team's Claude Code setup. Use when the user wants to
  "set up Claude Code", "set up my .claude", "install the forced-eval hook", or
  "configure Claude Code for the team". Installs the team's forced-eval
  UserPromptSubmit hook into project or global `.claude/`, merges settings
  idempotently, and optionally suggests team plugins.
argument-hint: "Set up Claude Code for the RDL team? (say 'project' for this repo's .claude/, or 'global' for ~/.claude/)"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# RDL team Claude Code setup

Your job is to onboard the user onto the RDL team's Claude Code configuration. This
first pass does one concrete thing: install the team's **`forced-eval-hook.sh`** and
wire it as a `UserPromptSubmit` hook in the scope the user chooses. The hook script
ships in this skill's `assets/` directory; you copy it into the target `.claude/` and
merge the settings idempotently.

> **Scope.** The forced-eval hook is the floor, not the ceiling. Do not configure model,
> permissions, MCP servers, or other settings here unless the user explicitly asks. The one
> addition beyond the hook is an **optional** plugin-discovery pass (Phase 4) that reviews
> the RDL marketplace and the team's extra marketplaces and *suggests* a plugin set — it
> only recommends and installs on confirmation.

## What the hook does

`forced-eval-hook.sh` is a `UserPromptSubmit` hook. When a prompt expresses intent to
*use* a skill (an action verb sits near "skill"/"skills"), it discovers the available
skills and slash commands — standalone (`~/.claude/skills/*/SKILL.md`) and plugin
(`~/.claude/plugins/installed_plugins.json`) — and emits them as **advisory context**
so the model considers them. Data-request/SQL/cohort prompts also surface the installed `data-request`
skills (including `guardrails`) without requiring a request to use a skill. This
SQL-specific path scans fresh and emits nothing when Data Request is unavailable. Other
prompts are a silent no-op. The framing is
descriptive; it does not coerce a fixed activation sequence. It uses `jq` when present
and degrades gracefully without it.

## Phase 0 — Choose the scope

Use the scope the user gave. Otherwise ask, and write nothing until they answer:

| Scope | `dest` | Settings file | Hook path variable | Plugin `--scope` |
|---|---|---|---|---|
| **project**, shared | `<repo>/.claude` | `.claude/settings.json` (committed) | `$CLAUDE_PROJECT_DIR` | `project` |
| **project**, personal | `<repo>/.claude` | `.claude/settings.local.json` (gitignored) | `$CLAUDE_PROJECT_DIR` | `local` |
| **global** | `~/.claude` | `~/.claude/settings.json` | `$HOME` | `user` |

For project scope, `<repo>` is the top level of the Git work tree
(`git rev-parse --show-toplevel`). If the directory is not a Git repository,
say so and ask for the project root.

A request to set up a named scope authorizes the file changes below. Do not ask
for approval again; report what changed. Ask before replacing an existing
`forced-eval-hook.sh` that differs from the bundled one, and show the diff.

## Phase 1 — Install the hook script

Copy the script from this skill's own directory, `${CLAUDE_SKILL_DIR}` (Claude
Code substitutes the installed path; otherwise use the directory this
`SKILL.md` was loaded from). Do not search the plugin cache or a marketplace
clone: another copy can belong to a different release.

```bash
dest="<repo>/.claude"            # global scope: dest="$HOME/.claude"
mkdir -p "$dest/hooks"
cp "${CLAUDE_SKILL_DIR}/assets/forced-eval-hook.sh" "$dest/hooks/forced-eval-hook.sh"
chmod +x "$dest/hooks/forced-eval-hook.sh"
```

## Phase 2 — Wire the `UserPromptSubmit` hook

Merge this rule group into the chosen settings file. For global scope, replace
`$CLAUDE_PROJECT_DIR` with `$HOME`.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/forced-eval-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Keep the variable **double-quoted inside the JSON string**. The command runs
through a shell, and an unquoted path that contains spaces splits into several
words, so the hook fails to launch.

Merge rules (idempotent):
- Parse the existing file. Create the file, `hooks`, or `hooks.UserPromptSubmit`
  only when absent. Keep every other key and every existing hook.
- If any `UserPromptSubmit` hook command already references
  `forced-eval-hook.sh`, leave the file unchanged. Otherwise append the group.
- Write valid JSON (use `jq` when available) and show the resulting change.

## Phase 3 — Verify

- `jq . <settings file>` parses without error.
- The installed script is executable (`test -x <path>` succeeds).
- Optional smoke test — the hook is a no-op unless intent is detected:
  ```bash
  printf '{"prompt":"please use a skill"}' | <installed forced-eval-hook.sh>
  ```
  expect it to emit the skill catalogue (or exit 0 quietly if no skills are installed);
  `printf '{"prompt":"hello"}' | <script>` should exit 0 with no output.

## Phase 4 — Review and suggest team plugins (optional)

Offer — don't force — to review what plugins are available across the RDL marketplace and
the team's extra marketplaces and suggest a set for this repo. Run this on first setup **and
whenever the user re-runs setup** (it is idempotent: it drops anything already enabled). If
the user declines, skip straight to Phase 5.

Use the `discover-plugins` skill shipped alongside this setup skill (canonical
`marketplace-scout`). Its `references/subagent.rst` contains an optional worker
outline for delegated discovery; read it when delegation is useful or requested.
Pass the marketplace list path and the repository path. The list is
`${CLAUDE_SKILL_DIR}/assets/marketplaces.json`, this skill's own copy (resolve it
as in Phase 1). The workflow enumerates the *live* plugin catalog of every
tracked marketplace, inspects this repo's languages/tooling, and returns a ranked
suggestion list:

- **Baseline (always-useful)** — `pr-review-toolkit@claude-plugins-official`, `gh@rdl-agent-extensions`,
  `worktrunk@worktrunk`, plus the applicable LSP (`gopls-lsp@claude-plugins-official` for Go;
  the official marketplace ships more `*-lsp` plugins the scout matches by language).
- **Language/stack-matched** — RDL subject plugins and team externals whose subject matches a
  detected language/tool (`go@rdl-agent-extensions`, `terraform@rdl-agent-extensions`, `astral@astral-sh`, …).

Present the scout's menu and let the user pick. For each marketplace a chosen plugin needs,
register it and install **only the confirmed plugins** (this skill installs them directly):

```bash
# <scope> is the Phase 0 plugin scope: project, local, or user.
claude plugin marketplace add <owner>/<repo> --scope <scope>   # e.g. nq-rdl/agent-extensions
claude plugin install <plugin>@<marketplace> --scope <scope>   # only the confirmed plugins
```

Without `--scope`, both commands default to user scope, which enables a plugin in
every project even though the user chose project setup.

Never install without confirmation. **Self-marketplace guard:** if the target repo is
itself the `rdl-agent-extensions` marketplace (a `.claude-plugin/marketplace.json` with `name: rdl-agent-extensions` — e.g.
`agent-extensions` itself), skip **every** `@rdl-agent-extensions` plugin. Installing the
published copy of *any* `@rdl-agent-extensions` id (including the baseline's `gh@rdl-agent-extensions`) shadows the working
tree's own copy. This install has no automatic self-exclusion, so you must exclude
`@rdl-agent-extensions` ids yourself here — the working tree already provides those skills.

## Phase 5 — Summarize

Tell the user, concisely:
- The scope chosen, the script path installed, and the settings file touched.
- That explicit skill-use prompts surface the full catalogue; ordinary SQL/cohort
  prompts surface skills from `data-request@rdl-agent-extensions` when installed.
  Other prompts, and SQL prompts without that plugin, are silent no-ops.
- For **project** scope: commit `.claude/hooks/forced-eval-hook.sh` and the settings
  change so the team picks them up (or note it is personal if they chose
  `settings.local.json`).
- Any plugins suggested/installed in Phase 4 (or that the step was skipped).
- That this is the first onboarding step; more RDL Claude Code configuration can follow.
