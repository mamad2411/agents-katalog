---
name: claude-md-rules-creator
description: "Write or audit CLAUDE.md, CLAUDE.local.md and .claude/rules files: scope, paths, imports, size, and why a rule is ignored."
when_to_use: "Use when creating or editing any of those files, or when Claude is not following one."
disable-model-invocation: false
---

# CLAUDE.md and Rules Creator

CLAUDE.md, CLAUDE.local.md and `.claude/rules/*.md` are one content type at runtime. The memory loader concatenates them behind a prefix that says they override the model's defaults, and they arrive in the first user message as a `<system-reminder>` block, never in `system`. The file shape only decides when a file loads and how a human maintains it.

This skill writes the shortest file set that changes behavior on Opus 5.5 and Sonnet 5.5, and debugs "Claude is not following my CLAUDE.md". The prose inside a file is a prompt: route its phrasing through `ac:prompt-writer`. A multi-step procedure or a user-typed `/name` action is a skill (`ac:skill-creator`), a custom worker is an agent (`ac:agent-creator`), a why-and-scope document is `ac:project-md-writer`, an architecture document is `ac:architecture-md-writer`, UI tokens and visual direction are `ac:frontend-design` (a `paths:` rule over the view files can point at its DESIGN.md), and a feature's requirements are a PRD from `/ac:product`, never CLAUDE.md lines. A whole-project setup or audit, existing files and auto-memory included, is `/ac:init-project`.

## Core principles

1. **The shortest file that changes behavior.** Keep a line only if the next agent would do something wrong without it and could not learn it from the manifest, README or code in one read. Budgets (tighter than Anthropic's 200 lines per file, since the lean 5.5 host prompt trusts the model): root `CLAUDE.md` 40 to 80 lines with a ceiling of 120, a rule file 15 to 50 with a ceiling of 80, `CLAUDE.local.md` 10 to 30. A file that loads at launch is paid for on every turn.
2. **Say it once.** Each fact has one home across every layer: managed, user, project, local, rules, AGENTS.md, README, settings. Grep the loaded layers before writing, then skip, edit in place or move. A rule file never repeats the root file, and the root file never lists or summarises the rule files: Claude Code loads an unscoped rule at launch and a path-scoped one when a matching file is read or edited, so an index of `.claude/rules/` (a table, a list, a "see rules/x.md" pointer per rule) is the same content paid for again on every turn.
3. **Deterministic behavior goes in settings, not prose.** What must hold on every edit (format, lint, secret files unreadable, routine commands without a prompt, a language server for navigation) is a hook, permission rule or plugin entry in `settings.json`. A CLAUDE.md line asking for it is a request; keep in the file only the residue that judgment cannot enforce. Which key goes in which file: `${CLAUDE_SKILL_DIR}/references/settings-wiring.md`; wiring: `hook-wiring.md` and `lsp-wiring.md` beside it.
4. **Specific and checkable.** "Use 2-space indentation in TypeScript", "Run `pnpm test` before committing". Name the concrete behavior, not the category.
5. **True now, and cold.** No aspirations ("we aim for"), no personas, no file-by-file tours, no language defaults, no secrets, no "as we discussed", no dated narratives or incident logs: a rule states the invariant a past incident taught, not the incident. A run that learns something proposes the one line to the user; it never appends a section on its own.
6. **No emphasis caps.** The loader already tells the model the file overrides defaults. State a rule once with its reason; shouting over-applies it.
7. **Audit the stack before writing.** The file joins the host system prompt and every memory layer; run Workflow step 1 and check `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` for the reader's model shape. The lean prompt (Opus 5.5, Sonnet 5.5, Haiku 5.5) lacks "no comments unless non-obvious", "no speculative abstraction" and "no compatibility shims"; the classic prompt (Sonnet 5 and earlier) carries them. Contradict a host line only as a stated override ("Push to `main` without asking; this overrides the default confirmation."). Protocol and the do-not-restate list: `${CLAUDE_SKILL_DIR}/references/layered-context.md`.
8. **Scope to the audience.** If the team gets value from a rule it belongs in the project; if only you do, in `CLAUDE.local.md` (this project) or `~/.claude/CLAUDE.md` (all projects).
9. **Pointers, not imports, for documents.** An `@import` loads the whole file every session, exactly like inlining it. Use `@AGENTS.md` for the one file shared with other tools. For a PROJECT.md, ARCHITECTURE.md, DESIGN.md or any reference document, write one line with a trigger ("Before changing structure, read ARCHITECTURE.md") and let Claude read it on demand.
10. **Write for Opus 5.5 and Sonnet 5.5.** Skip lines the model acts on without being told, and "think carefully" lines. Sonnet 5.5 adds tests, docs and small files nobody asked for and checks in early at low and medium effort, so a project that wants otherwise says so in one line each. The Agent tool description already says "When in doubt, don't spawn"; add a delegation limit only if the user wants a stricter one. The block is re-sent whole to every subagent unless it sets `omitClaudeMd: true` (managed files, and nested files and path-scoped rules on a matching access, still load).

## Decide the file

```
Is a CLAUDE.md or rule the right tool?
├── Must hold on every edit, no judgment → hook, permission rule or plugin in settings.json
├── Steps on demand → skill; user-typed action → command; custom worker → agent
├── Why and scope, or architecture → PROJECT.md / ARCHITECTURE.md plus one pointer line
└── Standing rule, convention, off-limits, project fact → continue

Which file?
├── Every session needs it, under budget → root ./CLAUDE.md (team) or ~/.claude/CLAUDE.md (personal, all projects)
├── Only you, this project → ./CLAUDE.local.md (gitignored)
├── One focused topic, always needed → ./.claude/rules/<topic>.md, no paths
├── Only matters near some files → ./.claude/rules/<topic>.md with paths:, or a subdirectory CLAUDE.md
└── Org policy → managed CLAUDE.md (admin deployed)
```

A 400-line file and four 100-line rules without `paths:` cost the same tokens; splitting helps humans and enables `paths:`. Rules with `paths:` and subdirectory CLAUDE.md files load on demand and are summarized away by compaction until the next matching access, so nothing safety-critical lives only there. Splitting and glob design: `${CLAUDE_SKILL_DIR}/references/rules-writing.md`; scopes and worktrees: `${CLAUDE_SKILL_DIR}/references/scopes.md`.

## Workflow

### 1. Audit the stack

Read the `Contents of <path>` headers in your context, grep those files for the topic, and decide: skip (covered at the right scope), edit in place (wrong or outdated), or move (wrong layer). The headers are fixed at session load and never show a file written or moved since; ask the user to run `/context` and read **Memory files** for the launch list (`/memory` lists and opens them). To audit an existing set, ask the user to run `/doctor prompt-audit [path]` (alias `/checkup`): it flags patterns written for older models, stale paths and commands, and contradicting files.

Success: you can name where the topic already lives, or confirm it lives nowhere.

### 2. Capture intent

Ask only what the request leaves open: the rule in one sentence, who needs it (team or you), whether it applies everywhere or near some paths, and whether it is a new file or an edit. A fact the model already knows is cut, not written.

Success: file, scope and shape are chosen.

### 3. Draft the file

Lead a generated CLAUDE.md or CLAUDE.local.md with a block-level HTML comment naming the generator and the real ISO date, such as `<!-- Generated by ac:claude-md-rules-creator on 2026-10-30. -->`. The loader strips it, so it costs the model nothing. In a rule file it goes directly after the closing `---` of the frontmatter, never above it, because frontmatter is parsed only at byte 0 and anything above it makes the rule load unconditionally. Skip the `# CLAUDE.md` preface that `/init` writes; it tells the model nothing.

Use `##` headers and one verifiable rule per bullet, highest-value sections first. Starters are in `${CLAUDE_SKILL_DIR}/assets/` (`CLAUDE.template.md`, `CLAUDE.local.template.md`, `global-CLAUDE.template.md`, `rule.template.md`, which shows the path-scoped rule shape with the comment after the frontmatter). What to include and exclude: `${CLAUDE_SKILL_DIR}/references/content-rules.md`; annotated files: `examples.md` beside it.

Success: the draft is inside its budget and every line passes principle 1.

### 4. Verify

Run the Pre-flight checklist below. Then confirm the load: `/context` lists launch files under **Memory files**; a path-scoped rule appears only after a matching file was touched. Not listed means the path is wrong, the source is disabled in `--setting-sources`, or `claudeMdExcludes` filters it.

Success: the checklist is clean and the file is listed.

### 5. Iterate

| Symptom | Fix |
|---|---|
| Claude ignores a rule | Confirm it loaded (`/context`). Tighten the wording. Look for a contradicting layer. Ask whether a hook is the right shape. Checklist: `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md` |
| File over budget | Cut lines that fail principle 1, move topics to rules, move documents behind pointer lines |
| A rule vanishes after `/compact` | A path-scoped rule or nested CLAUDE.md that has not matched a file since; move it to the root file if it must persist |
| Personal preferences show up in PRs | Move them to `CLAUDE.local.md` or `~/.claude/CLAUDE.md` |

Deeper symptom mapping: `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## How loading works

| Topic | Fact |
|---|---|
| Order | Managed, user, ancestor directories (root to cwd), project `CLAUDE.md` or `.claude/CLAUDE.md`, unconditional `.claude/rules/*.md`, then `CLAUDE.local.md`. Neither side of a conflict overrides the other, so settle conflicts in the files. |
| At launch or on demand | Files in the working directory and above load at launch; subdirectory files and `paths:` rules load on demand after Claude reads, edits or writes a matching file, or views one with a single-file `cat`, `head`, `tail`, `sed -n` or `grep`. |
| Size | A launch file loads whole up to 4 MiB. An on-demand file loads only its first 40,000 characters on a 200K window (150,000 on 1M for later models). Write refuses to overwrite a very large nested CLAUDE.md, rules file or @-included file it has not read. |
| Frontmatter | `.claude/rules/*.md` take one field, `paths:` (not `globs:`, which is ignored), at byte 0. CLAUDE.md and CLAUDE.local.md take none. |
| Imports | `@path`, `@./rel`, `@~/home`, four hops, none inside code spans or comments. A path with spaces needs a backslash before each space; a quoted path is not imported. Outside the working directory it needs a one-time approval. Syntax and `claudeMdExcludes`: `${CLAUDE_SKILL_DIR}/references/imports-and-paths.md`. |
| AGENTS.md | Read directly only when no `CLAUDE.md` or `CLAUDE.local.md` sits in the working directory or above; with both present only the CLAUDE.md files load. To share it, put `@AGENTS.md` on the first line of `./CLAUDE.md` with Claude-specific lines below: it loads in every session and never twice. |
| Compaction | The root CLAUDE.md and unscoped rules are re-read from disk and re-injected; nested files and path-scoped rules reload on the next matching access. |
| Comments | Block-level `<!-- -->` is stripped before injection; inline comments and comments inside code fences survive. |
| Debugging | `/context`, `/memory`, the `InstructionsLoaded` hook, `/doctor prompt-audit`. Mechanics: `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md`. |

## Quick recipes

| User says | Do |
|---|---|
| "Init CLAUDE.md for this repo" | `/ac:init-project` (ask the user to run it; it is typed only) runs the whole setup (files, rules, permissions, hook, language server). By hand: copy `CLAUDE.template.md`, fill only what differs from defaults. |
| "Monorepo rules" | Subdirectory CLAUDE.md, or a root rule with `paths: ["packages/web/**"]`; `claudeMdExcludes` for ancestor noise. |

## Pre-flight checklist

Always:

- [ ] Stack audited (principle 7); no duplicate or silent contradiction left.
- [ ] Inside the principle 1 budget, and every line survives its deletion test.
- [ ] Each fact has one home; documents sit behind pointer lines, not imports.
- [ ] Specific, verifiable rules; no vague verbs ("handle errors"), no aspirations, no file tours, no language defaults, no secrets, no emphasis caps.
- [ ] Right scope and right shape at the right path (user rules in `~/.claude/rules/`, project rules in `<dir>/.claude/rules/`).
- [ ] Anything deterministic (format, lint, secret reads, routine commands, language server) is in settings, not in the file.
- [ ] Attribution comment with a real date; in a rule file directly after the closing `---`.

By shape:

- [ ] (`CLAUDE.local.md`) Listed in `.gitignore`.
- [ ] (Rule with `paths:`) The glob matches your intent; no `paths: ['**']`, which loads like no `paths:`.
- [ ] (Rule without `paths:`) One focused, universal subject.
- [ ] (Imports) Every target exists, no chain past four hops, external imports approved.
- [ ] (Hook command) No secret in the command string.
- [ ] (Hook script) A path-containment guard rejects targets outside the intended directory.
- [ ] (Settings merge) A timestamped backup was taken before the merge.
- [ ] (Post-write) `claude doctor` runs clean in the target directory, and `/context` lists the new files.

## References

| File | Load when |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` | Before writing or cutting a line: the verbatim host prompt per shape and model, the CLAUDE.md wrapper, subagent defaults, the Agent tool text. |
| `${CLAUDE_SKILL_DIR}/references/layered-context.md` | Auditing the stack: the do-not-restate cheat sheet, conflict precedence, duplicate patterns. |
| `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md` | Debugging a rule that is ignored: discovery, wrapper, compaction, `InstructionsLoaded`, the troubleshooting checklist. |
| `${CLAUDE_SKILL_DIR}/references/scopes.md` | Managed paths, `--add-dir`, `--bare`, AGENTS.md interop, worktrees, monorepo excludes. |
| `${CLAUDE_SKILL_DIR}/references/rules-writing.md` | Splitting into rules, `paths:` globs, topic names, user-level rules, symlinks. |
| `${CLAUDE_SKILL_DIR}/references/imports-and-paths.md` | Import syntax and limits, `claudeMdExcludes`, comment stripping. |
| `${CLAUDE_SKILL_DIR}/references/content-rules.md` | What to include and exclude, with examples. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Failure modes and the audit checklist. |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Four annotated files: global, project, local, path-scoped rule. |
| `${CLAUDE_SKILL_DIR}/references/settings-wiring.md` | Choosing project settings (permissions, hook, language server, worktree and monorepo keys), which file each goes in, and which keys a setup command never writes. |
| `${CLAUDE_SKILL_DIR}/references/hook-wiring.md` | Building and proving a format or lint hook for a target project. |
| `${CLAUDE_SKILL_DIR}/references/lsp-wiring.md` | Detecting, proposing and verifying a language server. |
| `${CLAUDE_SKILL_DIR}/assets/CLAUDE.template.md`, `CLAUDE.local.template.md`, `global-CLAUDE.template.md`, `rule.template.md` | Starting a file from a blank template. |

Docs (append `.md` for raw markdown): `https://code.claude.com/docs/en/memory.md`, `https://code.claude.com/docs/en/features-overview.md`, `https://code.claude.com/docs/en/context-window.md`, `https://code.claude.com/docs/en/hooks.md`, `https://code.claude.com/docs/en/settings.md`. When the docs and the live binary disagree, trust the binary.
