---
name: marketplace-scout
description: >-
  Recommend Claude Code plugins for a repository from the team's tracked
  marketplaces. Use when choosing plugins during Claude Code setup or when asked
  which plugins a project should use. Matches live marketplace catalogs to the
  repository's stack. Recommends only; never installs plugins or edits settings.
license: MIT
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Discover Plugins

Return a ranked list of plugin ids for one repository, each tied to evidence in
that repository. Recommend only: do not install plugins, add marketplaces, or
edit settings. The caller (usually `cc-setup`) presents the list and installs
what the user confirms.

## 1. Read the team marketplace list

The list has one owner: `cc-setup/assets/marketplaces.json` in the `rdl-team`
plugin. It holds `marketplaces` (name → GitHub source), `teamExternals`
(external plugins tagged by language), and `baseline` (`always`, `lsp`,
`lspNote`).

- Use the path the caller passed.
- Otherwise use the sibling skill in the same installed plugin:
  `../cc-setup/assets/marketplaces.json` relative to this skill's directory
  (in Claude Code, `${CLAUDE_SKILL_DIR}/../cc-setup/assets/marketplaces.json`).
  It exists when this skill comes from `rdl-team`.
- Do not search the plugin cache or a marketplace clone for another copy; it
  can belong to a different release.

If the file is missing, say so at the top of the report: the curated baseline
and team externals are unavailable, and the user can install `rdl-team` or pass
the list's path. Continue in degraded mode with the marketplaces the project
already declares (`extraKnownMarketplaces` in `.claude/settings.json`). Do not
rebuild the list from memory.

## 2. Read each marketplace catalog live

Fetch `https://raw.githubusercontent.com/<owner>/<repo>/HEAD/.claude-plugin/marketplace.json`
for each marketplace and read its `plugins[]` (`name`, `description`,
`keywords`). `claude plugin marketplace list` shows configured marketplaces,
not their plugins. If a fetch fails, record it and continue.

**Never recommend an id you did not read** from a fetched catalog or from the
curated list. A guessed id with a real `@marketplace` suffix (for example an
invented `<lang>-lsp` plugin) passes setup's suffix checks and then stays
"declared but not installed". When a catalog is unreachable, recommend only
that marketplace's ids from `teamExternals` and `baseline`, and say that its
catalog was not verified.

## 3. Detect the stack

Use Glob/Grep, not whole-file reads: build files (`go.mod`, `Cargo.toml`,
`pyproject.toml`, `DESCRIPTION`, `package.json`, `*.tf`, `Chart.yaml`,
`*.qmd`), workflow signals (`.github/workflows/`, hook managers, `.changes/`,
Dockerfiles, `.sops.yaml`), and the plugins already enabled in the project's
`.claude/settings.json` (`enabledPlugins`).

**Self-marketplace guard:** when the repository is itself the
`rdl-agent-extensions` marketplace (`.claude-plugin/marketplace.json` with
`"name": "rdl-agent-extensions"`), drop every `@rdl-agent-extensions` id.
Installing the published copy would shadow the working tree. Say why in Notes.

## 4. Report

```text
## Suggested plugins for <repo>
### Baseline            (baseline.always)
### Language / LSP      (detected: <languages>)
### Stack-matched       (RDL subject plugins and team externals)
### Notes               (missing list, unverified catalogs, ids already enabled, guard)
```

Give each entry as `id@marketplace — reason tied to repository evidence`. Drop
ids already enabled, de-duplicate, and keep only plugins with a real signal.
End with the marketplaces that `extraKnownMarketplaces` must declare, grouped
with their ids. Keep the report under about 40 lines.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
