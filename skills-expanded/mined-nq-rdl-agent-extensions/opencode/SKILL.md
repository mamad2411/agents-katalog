---
name: opencode-skill
license: CC-BY-4.0
compatibility: >-
  OpenCode Agent Skills (SKILL.md) and the `references` config key; checked against
  v1.18.33 docs and source on 2026-09-29. Skills need no SDK.
description: >-
  Write OpenCode Agent Skills (SKILL.md) and `references` entries, or make an
  existing Claude Code skill load in OpenCode. Use for `.opencode/skills/`,
  `.claude/skills/` drop-ins, skill name/frontmatter rules, "skill won't load",
  the `skill` permission or disabling the skill tool, and `@alias` references.
  Not Claude Code skill authoring, not OpenAI Codex.
argument-hint: "What OpenCode skill or reference are you authoring? (e.g. 'add a git-release SKILL.md', 'expose ../docs as @docs', 'why isn't my skill loading')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode Agent Skills + References

Author OpenCode **Agent Skills** (`SKILL.md` instruction bundles loaded on demand) and
**References** (external dirs/repos attached via `@alias`). OpenCode is the open-source
coding agent at opencode.ai — **not OpenAI Codex** — and its skill format is
Claude-Code-compatible by design, which is exactly where the wrong assumptions creep in.

> **Verify-canonical guard.** OpenCode's API moves fast and predates the model's training
> cutoff — before writing skill code, read `references/skills.rst` (and `references/references.rst`
> for the `references` key) AND re-check <https://opencode.ai/docs/skills/> for drift.

---

## The big shortcut: Claude Code skills are drop-in

OpenCode reads `.claude/skills/<name>/SKILL.md` and `~/.claude/skills/<name>/SKILL.md`
**verbatim** — no conversion, no port. If a Claude Code skill already exists, **do not
rewrite it**; just confirm its `name` matches its directory and its frontmatter passes the
rules below. The six discovery locations (project + global × three roots):

| Root | Project | Global |
|------|---------|--------|
| OpenCode-native | `.opencode/skills/<name>/SKILL.md` | `~/.config/opencode/skills/<name>/SKILL.md` |
| Claude-compatible | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| agent-compatible | `.agents/skills/<name>/SKILL.md` | `~/.agents/skills/<name>/SKILL.md` |

Project discovery **walks up from cwd to the git worktree root**, loading every match along
the way. Skill `name`s **must be unique across all six locations** — a duplicate name is a
common silent-failure cause.

---

## Frontmatter — only five fields exist

OpenCode recognizes **exactly** these; everything else is **silently ignored**:

| Field | Required | Rule |
|-------|----------|------|
| `name` | yes | 1–64 chars, regex `^[a-z0-9]+(-[a-z0-9]+)*$`, **must equal the containing directory name** |
| `description` | yes | 1–1024 chars; specific enough for the agent to choose it |
| `license` | no | license identifier (e.g. `MIT`) |
| `compatibility` | no | e.g. `opencode` |
| `metadata` | no | **string→string map only** — no nested objects, no numbers/booleans |

Traps a fresh model hits:

- **`name` must match the folder name exactly.** `skills/git-release/SKILL.md` ⇒ `name: git-release`.
  No start/end hyphen, no `--`.
- **Claude Code frontmatter keys are inert here.** `argument-hint`, `user-invocable`,
  `allowed-tools`, `allowed_directories`, etc. are **not recognized** — they don't error, they
  just do nothing. Don't rely on them for OpenCode behavior.
- **`metadata` is flat string→string.** `metadata: { audience: maintainers }` ✅;
  `metadata: { steps: 3 }` or nested maps ❌.
- The file **must be named `SKILL.md` in all caps**.

Minimal valid skill (see `assets/SKILL.template.md`):

```markdown
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
---
## What I do
- Draft release notes from merged PRs
```

---

## How a skill is invoked

The agent sees only `name` + `description` in the `skill` tool description, rendered as:

```xml
<available_skills>
  <skill><name>git-release</name><description>Create consistent releases and changelogs</description></skill>
</available_skills>
```

and loads the full body **on demand** by calling the native tool:

```
skill({ name: "git-release" })
```

So the `description` is the **only** trigger signal — write it like a good Claude Code
description (concrete "use when…" terms), not a title.

---

## Gating skills — two distinct mechanisms (don't conflate)

| Goal | Key | Shape | Effect |
|------|-----|-------|--------|
| Allow/deny/ask **per skill name** | `permission.skill` | glob map → `allow`\|`deny`\|`ask` | `deny` **hides** the skill from the agent; `ask` prompts the user before load |
| **Disable the skill tool entirely** | `tools.skill` (documented form) | `false` | drops the whole `<available_skills>` section from context |

`permission.skill` is a **permission glob map**, not a boolean:

```json
{ "permission": { "skill": {
    "*": "allow", "pr-review": "allow", "internal-*": "deny", "experimental-*": "ask" } } }
```

Per-agent overrides (agents beat global):

```yaml
# custom agent frontmatter
---
permission:
  skill: { "documents-*": "allow" }
---
```

```json
// built-in agent in opencode.json
{ "agent": { "plan": { "permission": { "skill": { "internal-*": "allow" } } } } }
```

To kill skills for an agent entirely the docs use `tools: { skill: false }` (frontmatter)
or `agent.<name>.tools.skill: false` (config). v1.18.33 converts that legacy `tools` map
to `permission: { skill: "deny" }`, so the two forms are equivalent; a per-name glob map
hides only matching skills. Rule order and defaults: `/opencode-dev:policies`.

---

## References — named external roots via `@alias`

A separate feature (`references` config key) that exposes dirs/repos **outside the project**.
Config in `opencode.json`/`opencode.jsonc`, keyed by alias. Full detail in
`references/references.rst`.

```jsonc
{ "references": {
    "docs":   { "path": "../docs", "description": "Product behavior + doc conventions" },
    "effect": { "repository": "Effect-TS/effect", "branch": "main" } } }
```

| Type | Field | Shorthand |
|------|-------|-----------|
| Local dir | `path` (relative-to-config, absolute, or `~/`) | `"docs": "../docs"` |
| Git repo | `repository` (Git URL / `host/path` / GitHub `owner/repo`) + optional `branch` | `"effect": "Effect-TS/effect"` |

Optional for both: `description`, `hidden`.

Non-inferable traps:

- **Alias charset is restricted.** An alias **cannot be empty or contain `/`, whitespace,
  backticks, or commas.** (So `@my-docs` ✅, `@my/docs` ✗.)
- **Git references refresh asynchronously** — a newly configured `repository` may take a
  moment to finish cloning/updating; it won't be there instantly.
- **Only references *with a `description`* are advertised to the agent** (injected into system
  context). Without a description a reference is reachable solely via `@`-autocomplete / manual
  `@alias` — the agent won't know it exists.
- `@alias` attaches the **root**; `@alias/` searches **files inside** it.
- `hidden: true` only removes the alias from TUI `@`-autocomplete; a hidden ref **with** a
  description is still in agent context.
- References are auto-allowed through OpenCode's **external-directory permission boundary**, but
  **normal tool permissions still apply** — a read-only agent doesn't gain edit access just
  because a dir is a reference.

---

## Troubleshooting "my skill won't load"

1. Filename is `SKILL.md` (all caps).
2. Frontmatter parses and has a string `name` (and `description`). The v1.18.33 loader
   skips a file without a string `name`, but does **not** enforce the regex or the
   directory match: a mismatched skill loads under its frontmatter `name`. Follow the
   documented rules anyway so the skill stays portable.
3. The name is unique across all discovery locations — on a duplicate, the later file
   replaces the earlier one with only a log warning.
4. It isn't `deny`'d by `permission.skill` (deny ⇒ hidden), and `tools.skill` isn't `false` for the active agent.
5. Claude-compatible paths are skipped when `OPENCODE_DISABLE_CLAUDE_CODE` or
   `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` is set; `OPENCODE_DISABLE_EXTERNAL_SKILLS`
   also skips the `.agents/` roots. Extra roots can be added with the
   `skills.paths` config key (in the v1.18.33 schema, not on the skills page).

---

## Reference files

| File | Contents |
|------|----------|
| [references/skills.rst](references/skills.rst) | Verbatim Agent Skills doc — discovery paths, frontmatter rules, regex, `skill` tool, `permission.skill`, per-agent overrides, troubleshooting |
| [references/references.rst](references/references.rst) | Verbatim References doc — `references` key, `path`/`repository` fields, shorthands, `@alias` usage, alias charset, async git refresh, field table |
| [assets/SKILL.template.md](assets/SKILL.template.md) | Minimal OpenCode-valid `SKILL.md` skeleton |

