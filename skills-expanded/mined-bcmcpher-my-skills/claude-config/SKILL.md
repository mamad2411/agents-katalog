---
name: claude-config
description: >
  Configure Claude Code tooling for the current project: generate or update CLAUDE.md,
  set up an LSP language server, add PostToolUse hooks, configure MCP servers (DataLad,
  web search, GitHub), scaffold project-specific agents and skills in .claude/, create
  .editorconfig, configure settings hierarchy and permissions, set up memory with
  .claude/rules/ scaffolding, and add a status line to settings.json. Use when the user
  says "configure Claude", "set up Claude Code", "add an LSP", "add hooks", "set up MCP",
  "scaffold an agent", "scaffold a skill", "set up settings", "configure permissions",
  "set up memory", "add status line", or "/claude-config". Safe to run on new or existing
  projects; safe to re-run to add options later. Detects project type from CLAUDE.md or asks.
  Does not set up programming environments — use /env-check for that.
argument-hint: [coding-tool|data-analysis|info-management]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: claude-config

Configure Claude Code tooling for the current project. Safe to run at any time —
including immediately after `/new-project` or on a project that already has partial
configuration. Each option is independently selectable and re-runnable.

---

## Phase 0: Establish context

### Step 1 — Detect project type

If `$ARGUMENTS` names a type explicitly, use it:

| Keywords | Type |
|---|---|
| "coding-tool", "package", "library", "cli", "tool" | `coding-tool` |
| "data-analysis", "data", "analysis", "research", "science" | `data-analysis` |
| "info-management", "info", "notes", "knowledge", "vault" | `info-management` |

Otherwise, check `CLAUDE.md` for a `**Type:**` field in any `## Project` section.

If still unknown, ask:

> "What type of project is this?
>
> 1. Coding tool / package
> 2. Data analysis
> 3. Information management"

### Step 2 — Load project type reference

| Type | Reference |
|---|---|
| `coding-tool` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/coding-tool.md` |
| `data-analysis` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/data-analysis.md` |
| `info-management` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/info-management.md` |

### Step 3 — Detect language

Check `CLAUDE.md` for a `**Language:**` field, or scan for signal files:

| Signal files | Language |
|---|---|
| `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` | Python |
| `package.json` (no `tsconfig.json`) | JavaScript |
| `package.json` + `tsconfig.json` | TypeScript |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `DESCRIPTION`, `renv.lock`, `.Rprofile` | R |

For `info-management` projects, language is not applicable — skip.

### Step 4 — Load portability reference

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config-notes.md`.

Use this to inform the user of any configurations they may be able to copy from an existing
project or machine rather than generating from scratch. Mention this briefly when presenting
the menu in Phase 1 — e.g., "If you have an existing project with a similar stack, some of
these config files can be copied directly (see portability notes)."

---

## Phase 1: Configuration menu

Present the menu with profile-specific recommendations highlighted:

> "Which Claude Code configurations would you like to set up?
>
> 1. **CLAUDE.md** — generate or update with project-type content and AI instructions
> 2. **LSP** — language server for real-time diagnostics and code navigation
> 3. **Hooks** — PostToolUse automation (format, lint after file edits)
> 4. **MCP servers** — tool integrations (DataLad, web search, GitHub)
> 5. **Agents** — project-specific subagents in `.claude/agents/`
> 6. **Local skills** — project-specific slash commands in `.claude/skills/`
> 7. **`.editorconfig`** — consistent editor settings across contributors
> 8. **Settings** — scaffold `.claude/settings.json` with project-appropriate permissions
> 9. **Memory** — scaffold `.claude/rules/` and add `@path` imports to CLAUDE.md
> 10. **Status line** — add `statusLine` block to settings.json
>
> 11. **Pre-commit hooks** — git-side quality gate using the same linter/formatter as Option 3
>
> [Profile: `<type>`] Recommended for this project type: <comma-separated list from
> the reference's **Recommended Claude configuration** section>
>
> Reply with numbers (e.g., `1 3 5`), **all**, or **none** to exit."

Wait for the user's response, then execute each selected option in order.

---

## Phase 2: Execute selected options

### Option 1 — CLAUDE.md

Load the **CLAUDE.md template** section from the project type reference.

Check current state:

- **No CLAUDE.md** → write the full template. Substitute known values (project name,
  language, description). Leave placeholder fields marked with `<...>` for the user to
  fill in.
- **CLAUDE.md exists, no project-type section** → append the template's content after
  existing sections. Do not alter existing content.
- **CLAUDE.md exists with project-type content** → show the current content of the
  relevant sections and ask: "Update to the current template (merging your existing
  values), or leave as-is?"

After writing, tell the user which `<placeholder>` fields still need their input.
Once placeholders are filled, run `/claude-md-audit` for a detailed quality assessment.

Also note three structural practices:

1. **`<important>` tags for critical rules** — any instruction that must not be
   ignored should be wrapped in `<important>` tags. Claude pays closer attention to
   these even as the file grows longer:
   ```markdown
   <important>Never edit files outside src/ without explicit confirmation.</important>
   ```

2. **200-line limit** — CLAUDE.md should stay under ~200 lines; content after that
   may be truncated. If the file approaches that limit, split domain-specific sections
   into `.claude/rules/` files and import them with `@path` (see Option 9 — Memory).

3. **Monorepo / subdirectory awareness** — if this project lives inside a larger
   monorepo or under a parent directory that has its own CLAUDE.md, ancestor files
   (up to the filesystem root) are loaded automatically alongside this one. No
   duplication needed. Descendant CLAUDE.md files in subdirectories are scoped to
   that subtree and can override parent instructions locally.

### Option 2 — LSP

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/lsp.md`.

Follow the setup steps for the detected language. Output the `.lsp.json` content,
write it to the project root, and note any binary that must be installed separately.

For `info-management` projects: note that LSP is not applicable and skip.

### Option 3 — Hooks

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/hooks.md`.

Present the recommended hooks for the detected language and project type. For each hook
the user confirms:

- Project hooks live under the `"hooks"` key of `.claude/settings.json` — there is no
  `.claude/hooks.json`.
  - **Exists**: show the current `"hooks"` block, merge the new event entries into it,
    confirm before writing. Do not clobber unrelated settings keys.
  - **Does not exist**: create `.claude/settings.json` containing only the `"hooks"` key.
- Write the hook body as a script in `.claude/hooks/` and `chmod +x` it, rather than an
  inline one-liner. The hook receives the event as JSON on stdin, so it needs `jq` to
  reach `.tool_input.file_path`; there is no `$FILE` variable.
- Before wiring, confirm the tool resolves without a login shell
  (`env -i PATH="/usr/bin:/bin" bash -c '<cmd> --version'`). If it does not, use an
  explicit path such as `node_modules/.bin/eslint` or `.venv/bin/ruff`.

After writing the hook, also offer to create the tool's config file using the **Tool
config file stubs** section of the reference. The config file makes the hook work
correctly from the first edit rather than relying on tool defaults.

Remind the user that Claude Code hooks and git pre-commit hooks are independent systems
(see `references/git.md`).

### Option 4 — MCP servers

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/mcp.md`.

Present the recommended MCP servers for the project type. Note which are already
configured in `.mcp.json` if that file exists.

For each server the user selects, output the configuration snippet. Offer to append it
to `.mcp.json` (creating the file if absent).

**code-review-graph**: mention for any project with a real source tree. If the user's
global config wires the graph hooks, they are usually gated on the repo already having a
graph — check with `ls -d .code-review-graph` and tell the user that
`code-review-graph build` is what opts this repo in. Do not run `code-review-graph
install`; it writes machine-specific paths into committed files.

**DataLad**: always mention DataLad for `data-analysis` and `info-management` projects.
Note that it requires the `datalad-cli` plugin to be installed:
`claude plugin install <path-to-datalad-cli>`. Reference the skills available in that
plugin when describing what DataLad enables.

### Option 5 — Agents

Load the **Recommended agents** section from the project type reference.

**Design guidance before scaffolding:** Feature-specific agents outperform broadly-scoped
roles. An agent named `auth-token-reviewer` or `data-pipeline-debugger` that knows its
exact domain will be delegated to correctly; an agent named `general-qa` or
`backend-engineer` will either misfire or be ignored. Two design rules:
- Scope the agent to a specific workflow, module, or decision type — not a job title.
- The `description` field should state *when the main Claude should delegate* (the
  trigger), not just what the agent does. Example: "Delegate to this agent when
  reviewing any change to the auth or session handling code."

The git-workflow plugin (`plugins/git-workflow/`) is a reference example of a
well-scoped agent description.

**Preloaded-skill pattern (optional):** For agents that need reusable domain knowledge —
a spec, a checklist, or a lookup table — create a companion skill alongside the agent and
load it via the `skills:` frontmatter field rather than embedding that knowledge in the
agent body. Mark the companion skill with `user-invocable: false` to hide it from the `/`
menu; it exists only to be injected at agent startup.

Example: a `data-pipeline-debugger` agent with a separate `pipeline-conventions` skill
(containing the project's pipeline standards) loaded as:
```yaml
skills:
  - .claude/skills/pipeline-conventions
```
This keeps the agent body focused on behavior and the skill body focused on reference
material — each independently updateable.

Present each recommended agent with a one-line description. For each the user selects:

1. Check whether `.claude/agents/<agent-name>/SKILL.md` already exists.
   - **Does not exist**: create `.claude/agents/<agent-name>/` and proceed.
   - **Exists**: show the current `SKILL.md` content and ask:
     > "An agent named `<agent-name>` already exists. Update to the new template
     > (merging your existing values), or leave as-is?"
     Wait for the user's choice. If "leave as-is", skip this agent.
2. Write a `SKILL.md` using the agent scaffold from the reference (frontmatter +
   template body with `<placeholder>` fields).
3. Tell the user which fields to customize.

**DataLad awareness**: any agent in a `data-analysis` or `info-management` project
that handles files should include a note in its body:

> "DataLad tools are available via the `datalad-cli` plugin if installed. Use
> `datalad save`, `datalad run`, `datalad get`, and `datalad push` as appropriate
> when managing versioned data files or binary assets."

### Option 6 — Local skills

Before presenting options, note the 5 bundled skills already installed with Claude Code
that users commonly recreate unnecessarily:

| Bundled skill | What it does |
|---|---|
| `simplify` | Review changed code for quality and eliminate duplication |
| `batch` | Run a command across multiple files in bulk |
| `debug` | Debug failing commands or code issues |
| `loop` | Run a prompt or slash command on a recurring interval |
| `claude-api` | Build apps with the Claude API; auto-triggers on `anthropic` imports |

Tell the user: "These are already available via `/simplify`, `/batch`, etc. — no
scaffolding needed. Run `/skills` in Claude to confirm they are active."

Present common local skill patterns for the project type (from the reference's
**Recommended local skills** section, if present). For each the user selects:

1. Create `.claude/skills/<skill-name>/` if it does not exist.
2. Write a minimal `SKILL.md` with frontmatter and a short instruction body marked
   with `<placeholder>` for the user to complete.

### Option 7 — `.editorconfig`

Load `${CLAUDE_PLUGIN_ROOT}/../references/editorconfig.md`.

Check whether `.editorconfig` exists:

- **Exists**: show the current content and offer to add or update the language-specific
  block, or leave it unchanged.
- **Does not exist**: generate a `.editorconfig` with the `[*]` universal block plus
  a language-specific `[*.<ext>]` override from the reference. Write it and confirm.

For `info-management` projects, generate a markdown-focused config:

```ini
# EditorConfig: https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
indent_style = space
indent_size = 2
trim_trailing_whitespace = false
```

(Trailing whitespace is intentionally preserved in Markdown — two trailing spaces
produce a line break.)

### Option 8 — Settings

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/settings.md` if it exists;
otherwise load `${CLAUDE_PLUGIN_ROOT}/../../../../reference/settings.md`.

Explain the 5-scope hierarchy briefly (enterprise → CLI → local project → project → global).

Check whether `.claude/settings.json` exists:

- **Does not exist**: scaffold it with project-type-appropriate defaults (see below) and
  write it, then remind the user to gitignore `.claude/settings.local.json` for secrets.
- **Exists**: show the current content and offer to merge in missing sections (permissions
  or env blocks), or leave as-is.

**Project-type permission defaults:**

| Project type | Allow | Ask | Deny |
|---|---|---|---|
| `coding-tool` | `Bash(git *)`, `Read`, `Bash(* --version)` | `Bash(npm install *)`, `Write`, `Edit` | `Bash(rm -rf *)`, `Read(~/.ssh/*)` |
| `data-analysis` | `Bash(git *)`, `Read`, `Bash(pip install *)` | `Write`, `Edit`, `Bash(jupyter *)` | `Bash(rm -rf *)`, `Read(~/.ssh/*)` |
| `info-management` | `Bash(git *)`, `Read` | `Write`, `Edit` | `Bash(rm -rf *)`, `Read(~/.ssh/*)` |

**Prefer scoped wildcard permissions over `dangerouslySkipPermissions`.** Instead of
bypassing all permission checks, use wildcard syntax to allow only what the project
needs:

| Avoid | Prefer |
|---|---|
| `"dangerouslySkipPermissions": true` | `"Bash(npm run *)"`, `"Bash(git *)"` |
| Allow-all Bash | `"Bash(make *)"`, `"Bash(cargo *)"` |
| Allow-all Edit | `"Edit(src/**)"`, `"Edit(docs/**)"` |

This keeps permission prompts minimal without removing the safety net entirely.

After writing, tell the user:
- Global security denies belong in `~/.claude/settings.json`, not committed here.
- Machine-specific tokens belong in `.claude/settings.local.json` (add to `.gitignore`).

**Security tooling note:** For `coding-tool` and `data-analysis` projects, recommend
running a dependency audit periodically to catch known vulnerabilities:

| Language | Command |
|---|---|
| Python | `pip-audit` (install: `pip install pip-audit`) |
| JavaScript / TypeScript | `npm audit` or `pnpm audit` |
| Rust | `cargo audit` (install: `cargo install cargo-audit`) |
| Go | `govulncheck ./...` (install: `go install golang.org/x/vuln/cmd/govulncheck@latest`) |

For `coding-tool` projects with CI already configured, suggest adding the audit command
as a step in `.github/workflows/test.yml` to catch vulnerabilities automatically.

### Option 9 — Memory

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/memory.md` if it exists;
otherwise load `${CLAUDE_PLUGIN_ROOT}/../../../../reference/memory.md`.

Step 1 — Scaffold `.claude/rules/`:

Check whether `.claude/rules/` exists. If not, create it with a starter file:

`.claude/rules/conventions.md`:
```markdown
# Project conventions

<!-- Add project-specific rules here. Claude loads all files in .claude/rules/
     automatically. Keep each file focused on one domain (git, testing, data, etc.). -->
```

Tell the user the auto-memory path for this project:
`~/.claude/projects/<url-encoded-project-path>/memory/`

Step 2 — Add `@path` imports to CLAUDE.md:

Check whether `CLAUDE.md` exists. If it does, check whether it already imports from
`.claude/rules/`. If not, offer to append:

```markdown
## Project rules

@.claude/rules/conventions.md
```

Explain: adding `@path` imports keeps the root CLAUDE.md under the ~200-line limit
while still loading all domain-specific rules.

### Option 10 — Status line

Load `${CLAUDE_PLUGIN_ROOT}/../../../../reference/statusline.md`.

Check whether a `statusLine` block already exists in `.claude/settings.json` or
`~/.claude/settings.json`. If found, show it and ask: "Update, or leave as-is?"

If adding: offer two variants:

**Project-scoped** (`.claude/settings.json`) — adds the block there. Good for team
environments with a shared status line script.

**Global** (`~/.claude/settings.json`) — installs it personally. Requires the script
to be present on each machine.

Suggested configuration:

```json
"statusLine": {
  "type": "command",
  "command": "bash ~/.claude/statusline-command.sh"
}
```

Point the user to `config/statusline-command.sh` in the my-skills repo as a ready-to-use
template. Provide the copy command:

```bash
cp <path-to-my-skills>/config/statusline-command.sh ~/.claude/statusline-command.sh
chmod +x ~/.claude/statusline-command.sh
```

### Option 11 — Pre-commit hooks

Load `${CLAUDE_PLUGIN_ROOT}/../references/claude-config/pre-commit.md`.

Explain the relationship to Claude Code hooks: pre-commit hooks run on `git commit`
regardless of how code was changed; Claude Code PostToolUse hooks run only during
Claude editing sessions. Both are recommended for `coding-tool` projects.

Check whether `.pre-commit-config.yaml` already exists:

- **Does not exist**: generate a config using the detected language stub from the
  reference, plus the **Universal additions** block. Write it and confirm.
- **Exists**: show the current content and offer to append the universal additions
  block or a missing language hook, or leave it unchanged.

After writing the config, offer to run the setup commands:

```bash
pip install pre-commit   # or remind user to install via their preferred method
pre-commit install
```

If `pre-commit install` is blocked by Claude Code's permission system, surface the
command and wait for "done" before continuing.

Remind the user: "The linter and formatter in this config match your Claude Code
PostToolUse hooks — both systems now enforce the same quality rules."

---

## Constraints

- Never overwrite an existing file without showing the current content and asking first.
- Each option is independently safe to run; do not assume earlier options were selected.
- Always load the relevant reference file before taking action on any option.
- For Option 5 agents: always include the DataLad awareness note for `data-analysis`
  and `info-management` project types, regardless of whether the datalad-cli plugin
  is currently installed — the note is forward-compatible.
- Do not modify project source files, manifests, or any file not listed above.
- This skill may be invoked partway through `/new-project` — in that case, project type
  and language are already established; use them directly without re-asking.
