---
name: cli-with-claude-skill
version: 3
description: Use when creating, scaffolding, or adding/renaming/removing subcommands or flags in a CLI tool that ships an installable Claude Code skill (e.g. `<tool> install-claude-skill`), or when asked to "update the <tool> skill" / "the skill is out of date" for such a tool
---

# CLI With Claude Skill — Authoring Discipline

## Why this exists

Boss runs many projects where a CLI binary embeds and installs its own Claude Code skill into `~/.claude/skills/<tool>/SKILL.md`. The same five mistakes recur across projects:

1. Hand-parsing `os.Args` / `process.argv` / `sys.argv` instead of using a real arg-parser.
2. The CLI ships no `install-claude-skill` command by default — Boss has to ask for it every time.
3. The skill file has no `version:` field, so the CLI cannot detect outdated installs and cannot auto-update.
4. CLI subcommands change but the embedded `SKILL.md` (the source-of-truth in the repo) is not updated in the same change. Shipped skill drifts from reality.
5. When Boss says "update the skill", the agent edits `~/.claude/skills/<tool>/SKILL.md` (the *installed* copy) instead of the source file in the CLI repo. Next `install-claude-skill` overwrites the edits and the work is lost.

This skill enforces the rules that prevent each one. **Violating the letter of the rules is violating the spirit of the rules.**

## Reference implementation

`muveectl` in the `muvee` repo is the canonical example. Mirror its structure for new CLIs:

- Embedded skill source: `internal/skill/skill.md` + `internal/skill/skill.go` (`//go:embed`).
- Install command + version-comparison auto-update: `cmd/muveectl/main.go` (functions `claudeSkillPath`, `parseSkillVersion`, `shouldShowSkillOutdatedNotice`, `checkSkillNotice`, `cmdInstallClaudeSkill`).
- Subcommand wiring with cobra: `cmd/muveectl/login.go` (look for the `install-claude-skill` cobra.Command).

## Drop-in templates

The skill ships templates for Go, Rust, Node/TS, and Python under `~/.claude/skills/cli-with-claude-skill/template/`. Pick the one matching your CLI's language.

**Shared (language-agnostic):**

| Template file | Drop into | Edits needed |
|---|---|---|
| `template/skill.md` | `internal/skill/skill.md` (Go) / `src/skill.md` (Rust, Node) / `<pkg>/skill.md` (Python) | Replace `REPLACE_WITH_TOOL_NAME`; write the description per `skill-description-cso`; document subcommands. |

**Go + cobra:**

| Template file | Drop into | Edits needed |
|---|---|---|
| `template/go/skill.go` | `internal/skill/skill.go` | None — verbatim. |
| `template/go/skill_install.go` | `cmd/<tool>/skill_install.go` | Set `const toolName`; set the `<your-module>` import path; wire `installClaudeSkillCmd` into `rootCmd.AddCommand` and call `checkSkillNotice()` from `PersistentPreRun`. |

**Rust + clap (derive):**

| Template file | Drop into | Edits needed |
|---|---|---|
| `template/rust/skill_install.rs` | `src/skill_install.rs` | Set `pub const TOOL_NAME`; add `mod skill_install;` to `main.rs`; add `InstallClaudeSkill` to your `Subcommand` enum and dispatch to `skill_install::install()`; call `skill_install::check_notice()` at the top of `main()`. Cargo dep: `dirs = "5"`. |

**Node / TypeScript + commander:**

| Template file | Drop into | Edits needed |
|---|---|---|
| `template/node/skillInstall.ts` | `src/skillInstall.ts` | Set `TOOL_NAME`; in your entry: `registerSkillCommand(program)` and `program.hook("preAction", () => checkSkillNotice())`. Bundler must keep `skill.md` next to the bundle (or use a build-time inline plugin and assign `EMBEDDED` from that). |

**Python + click:**

| Template file | Drop into | Edits needed |
|---|---|---|
| `template/python/skill_install.py` | `<pkg>/skill_install.py` | Set `TOOL_NAME`; in your CLI group: `cli.add_command(install_claude_skill_cmd)` and call `check_skill_notice()` from the group callback. Ensure `skill.md` ships as package data (force-include in `pyproject.toml`). |

## The Rules

### Rule 1 — Use a real arg-parser. Never hand-parse.

| Language    | Library                                |
|-------------|----------------------------------------|
| Go          | `github.com/spf13/cobra`               |
| Rust        | `clap` (derive)                        |
| Node / TS   | `commander`                            |
| Python      | `click` or `typer`                     |

**No exceptions:**
- Don't write a `switch os.Args[1] {…}` dispatcher "just for now".
- Don't pull a "lighter" alternative without asking Boss first.
- One subcommand is enough to require the library. Do not wait until "it gets complicated".

### Rule 2 — Every CLI ships `install-claude-skill` from day one.

The first commit of a new CLI MUST include all of:

1. An embedded skill source file at a stable repo path. Conventions:
   - Go: `internal/skill/skill.md` (embedded via `//go:embed`).
   - Rust: `src/skill.md` (via `include_str!`).
   - Node: `src/skill.md` (bundled or read at install time).
   - Python: `<pkg>/skill.md` (read via `importlib.resources`).
2. A `<tool> install-claude-skill` subcommand that writes the embedded content to `~/.claude/skills/<tool>/SKILL.md` (creating the directory).
3. Startup notice logic in a `PersistentPreRun` hook (or equivalent):
   - Installed file missing → print a one-line tip pointing at `install-claude-skill`.
   - Installed `version:` older than embedded `version:` → auto-run `install-claude-skill` and print `Notice: Claude skill is outdated. Auto-updating...`.

Do not invent your own naming. The subcommand name is exactly `install-claude-skill`. The install path is exactly `~/.claude/skills/<tool>/SKILL.md`.

### Rule 3 — The embedded SKILL.md MUST have a `version:` field.

```yaml
---
name: <tool>
version: 1
description: Use when ...
---
```

- Integer counter (1, 2, 3, …) or semver — pick one and stick to it. Integer is simpler and matches Boss's existing tools.
- The CLI's update check parses this field. No version → no auto-update → Rule 2 is broken.
- Bump in the SAME commit that changes the skill body. Never bump-only commits, never body-only commits.

### Rule 4 — CLI surface change ⇒ embedded SKILL.md update, in the same change.

When you add, rename, remove, or change the flags / behavior / defaults of a subcommand:

1. Edit the source code (cobra command, etc.).
2. Edit the embedded skill source file (`internal/skill/skill.md` or equivalent).
3. Bump `version:` in that file.
4. Build the CLI to confirm both compile.

**Non-negotiable.** A change that touches CLI surface but not the embedded SKILL.md is incomplete. Before reporting the task done, grep the embedded SKILL.md for the old command/flag name and confirm the doc is in sync. Run `<tool> --help` and skim — every subcommand listed there should also be documented in SKILL.md.

If unsure whether SKILL.md needs an update: read the diff. Any user-visible change (new flag, new subcommand, renamed argument, changed default, removed feature, changed output format) requires an update.

### Rule 5 — Edit the source. NEVER the installed copy.

When Boss says "update the skill", "the skill is out of date", or "the skill is wrong", you will be tempted to `Edit` `~/.claude/skills/<tool>/SKILL.md` directly. **Do not.** That file is rendered output. Editing it:

- Will be overwritten on the next `<tool> install-claude-skill` invocation (which the CLI may auto-run on every startup per Rule 2). Your edits vanish silently.
- Does not propagate to other machines / other developers / CI.
- Hides the real source from version control.

**Procedure when asked to update an installed skill:**

1. Identify the CLI behind the skill. The skill's `name:` is the binary name. `which <name>` if installed locally; otherwise the surrounding conversation will name the project.
2. Locate the embedded skill source in the project. Search order:
   - `internal/skill/skill.md`
   - `cmd/<tool>/skill.md`
   - `src/skill.md`
   - `grep -rl "install-claude-skill\|claudeSkillPath\|embeddedSkill" .` then follow the embed directive.
3. Edit THAT file. Bump `version:`.
4. Tell Boss to run `<tool> install-claude-skill` (or rebuild + invoke) to refresh the installed copy locally — do not run it yourself unless Boss approves, because rebuilding may not be free.

**Red flags — STOP and re-evaluate if you catch yourself about to:**

- Call `Edit` / `Write` on any path under `~/.claude/skills/<tool>/` while you are working inside that tool's source repo.
- Accept "update the skill" by jumping to the installed copy because it's "easier to find".
- Modify `~/.claude/skills/<tool>/SKILL.md` and *also* the repo's `internal/skill/skill.md` "to keep them in sync" — only the repo file is authoritative; the installed copy is generated.

The installed copy at `~/.claude/skills/<tool>/SKILL.md` is read-only from this skill's perspective. The only writer is the CLI's own `install-claude-skill` command.

## Rationalization table

| You hear yourself thinking… | What's actually true |
|---|---|
| "Hand-parsing is fine, only two subcommands." | Project will grow. Rule 1 is unconditional. |
| "I'll add `install-claude-skill` later, the user didn't ask." | Boss has asked for it on every prior project. Add it now. |
| "Version field is just bureaucracy." | The auto-update check parses it. No version = the user keeps getting stale skills forever. |
| "The CLI change is small, the skill is still mostly right." | "Mostly right" docs mislead future agents. Update it now while the diff is fresh. |
| "Boss said update the skill — `~/.claude/skills/<tool>/SKILL.md` is right there." | That's the rendered output. Find the source in the repo (Rule 5 procedure). |
| "I'll edit both copies to be safe." | No. Editing the installed copy is wasted work; it gets overwritten. Edit the source only. |

## Quick checklists

### Starting a new CLI from scratch

- [ ] Arg-parser library added as a dependency (cobra / clap / commander / click).
- [ ] Embedded skill source created at the conventional path with `name`, `version: 1`, and a CSO-compliant `description` (see `skill-description-cso`).
- [ ] `install-claude-skill` subcommand implemented.
- [ ] Startup notice (missing → tip; outdated → auto-update) implemented in `PersistentPreRun` or equivalent.
- [ ] `--version` flag implemented.
- [ ] First build passes.

### Adding/renaming a subcommand or flag

- [ ] Subcommand registered via the arg-parser library — not hand-parsed.
- [ ] Embedded `SKILL.md` source updated (subcommand description, flags, one usage example).
- [ ] `version:` bumped in the embedded skill.
- [ ] Build passes.
- [ ] Optional sanity check: run `<tool> install-claude-skill` locally and `grep <new-command> ~/.claude/skills/<tool>/SKILL.md` to confirm the new section made it through.

## When this skill does NOT apply

- Editing skills that are NOT installed by a CLI (e.g. hand-maintained skills like `skill-tdd-and-persuasion`, `skill-description-cso`). Those live at their installed path and are edited there directly.
- Pure library work with no binary entry point.
- Single-file scripts the user has explicitly said are throwaway.
