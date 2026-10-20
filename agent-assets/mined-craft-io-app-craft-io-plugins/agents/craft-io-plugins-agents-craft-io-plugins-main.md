# Working in this repository

A public plugin marketplace for Claude Code, Cursor and Gemini CLI. Anything
merged here is installable by Craft.io customers within minutes, so the bar is
the same as for shipped product. [CONTRIBUTING.md](CONTRIBUTING.md) has the
reasoning; this is what you need before you change anything.

## Bump the version when you change what ships

Two manifests carry a version, and nothing raises them for you:

- `plugins/craft-guru/.cursor-plugin/plugin.json`
- `plugins/craft-guru/gemini-extension.json`

Rather than working out which one a given change needs, run:

```
python3 .github/scripts/check_version_bump.py --fix
```

It raises exactly the versions that would otherwise fail the build, and does
nothing when nothing is owed. Review the diff and commit it with your change.

**Never add `version` to `.claude-plugin/plugin.json`.** Claude Code resolves the
version from the commit, and pinning it freezes the plugin for everyone who has
already installed it. CI rejects the field.

## Rules CI will not let you break

- **Markdown and JSON only.** No `hooks/`, `bin/`, `agents/`, `monitors/`,
  `settings.json` or `.lsp.json` inside a plugin. Installing from this
  marketplace must never run code on a customer's machine.
- **Every skill needs a `## Trust boundary` section**, copied verbatim from an
  existing skill. It is what tells the agent that customer-submitted feedback is
  data, not instructions.
- **Skill frontmatter stays inside the Agent Skills spec**: `name`,
  `description`, `license`, `compatibility`, `metadata`. Not `allowed-tools` —
  it pre-approves tools without prompting rather than restricting them.
- **MCP servers are remote and HTTPS**, named in lower-case kebab-case, and every
  manifest must name the same servers at the same URLs.
- **No proactive triggers** in a skill description, and never instruct the model
  to withhold its reasoning from the user.

## Before opening a PR

```
python3 .github/scripts/validate_plugins.py
python3 .github/scripts/check_version_bump.py
python3 .github/scripts/test_validate_plugins.py
```

`claude plugin validate .` reports one warning about the missing version. That is
deliberate — don't pass `--strict`, and don't "fix" it.

If you add a validator rule, add its mutation to `test_validate_plugins.py`:
break the rule on a scratch copy, assert the build goes red. A review once found
seven rules that had silently never fired, each of which looked correct in the
source.

## Writing a skill

Gate every Craft write behind an explicit confirmation, and show the user what
will be written before asking. Never probe for write access by performing a
write — attempt what the user asked for and handle the permission error. Never
invent Craft data: if a field is missing, say so.

Keep the description tight. It sits in every user's context on every turn.
