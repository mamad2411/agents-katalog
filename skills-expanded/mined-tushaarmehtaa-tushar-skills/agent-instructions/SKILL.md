---
name: agent-instructions
description: Create or reconcile AGENTS.md, CLAUDE.md and Cursor rules so Claude Code, Codex and Cursor each load the right guidance. Use when agent instructions are missing, stale, duplicated or conflicting.
license: MIT
---

# Agent instructions

Write the smallest set of instruction files that each target runtime actually loads. A correct file in a location the runtime skips, or one shadowed by another file, does nothing. Recover facts from the repository before asking, and separate commands you ran from commands you only read about.

## Choose the task

- **Create:** no instruction files exist.
- **Improve:** one existing file is thin, stale or bloated.
- **Reconcile:** files duplicate or contradict each other, or one runtime ignores guidance the others see.
- **Scope a subtree:** a package or directory needs different commands, ownership or boundaries.
- **Explain loading:** the user asks why an agent ignores its instructions. Report what each runtime loads here. Change nothing unless asked.

Infer the target runtimes from the request, existing files and the user's tooling. Ask only when the answer changes which files exist. "Make this work for our agents" with no other signal means Claude Code, Codex and Cursor.

## Read the loading matrix first

Read [the loading matrix](references/loading-matrix.md) before choosing any file. It records which files Claude Code, Codex and Cursor read, in what order, with which limits, checked on a stated date. Follow its run-time rule: re-check a runtime's docs when the check date is more than about 90 days old or the installed runtime is older than a version it names.

## Inventory every instruction source

```bash
pwd
git rev-parse --show-toplevel
rg --files --hidden -g '!node_modules' -g '!.git' \
  -g '**/AGENTS.md' -g '**/AGENTS.override.md' -g '**/CLAUDE.md' -g '**/CLAUDE.local.md' \
  -g '**/.claude/rules/**' -g '**/.cursor/rules/**' -g '**/.cursorrules'
```

Then check three places `rg` misses:

- **Ancestors above the repository root.** Claude Code loads every `CLAUDE.md`, `.claude/CLAUDE.md` and `CLAUDE.local.md` from cwd upward. One in a parent folder shadows the repository's `AGENTS.md` for Claude Code. Ignore `~/.claude/CLAUDE.md`; it does not shadow.
- **Codex fallback names.** Read `project_doc_fallback_filenames` and `project_doc_max_bytes` in `~/.codex/config.toml` (or `$CODEX_HOME`) when present. A fallback-named file is an instruction file for Codex.
- **Fixture and example directories.** An `AGENTS.md` or `CLAUDE.md` inside test fixtures, examples or proof folders loads as a real instruction for Claude Code and Cursor when work touches that folder.

For each file record: directory, runtimes that load it, when it loads (launch or on demand), what it shadows or is shadowed by, size, and statements that conflict with a nearer file or with repository evidence.

Treat user-global files (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`) as context that explains behavior. Do not edit them unless asked.

## Choose the layout

Default for a repository shared across runtimes:

1. **One root `AGENTS.md` as the shared source.** Codex and Cursor read it. Claude Code reads it when no `CLAUDE.md` exists in cwd or above.
2. **Add `CLAUDE.md` only when Claude-specific rules exist** (plan-mode areas, hooks, Claude tool notes) or a `CLAUDE.md` already exists. Its first line is `@AGENTS.md`; Claude-only notes go below.
3. **Never create a `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` without that import in a repository that relies on `AGENTS.md`.** It silently drops `AGENTS.md` for Claude Code. This includes advising a user to add a personal `CLAUDE.local.md`.
4. **Existing `CLAUDE.md` with shared content plus `AGENTS.md`:** move shared facts into `AGENTS.md`, reduce `CLAUDE.md` to `@AGENTS.md` plus Claude-only notes. Ask before deleting a `CLAUDE.md` that holds anything beyond the import.
5. **Cursor:** `AGENTS.md` already covers it. Add `.cursor/rules/*.mdc` only for activation `AGENTS.md` cannot express: glob-scoped rules or description-selected rules. Do not copy `AGENTS.md` content into rules. Cursor does not inline `@file` references in rules, so put must-have content in the rule body.
6. **Path-scoped Claude rules:** use `.claude/rules/*.md` with `paths:` for guidance that matters only for some files, instead of growing `CLAUDE.md` past about 200 lines.
7. **Do not create `AGENTS.override.md`** for shared rules. Only Codex reads it. Flag an existing one as a divergence.
8. **Keep shared content inline in `AGENTS.md`.** `@path` imports expand only in Claude Code. Codex documents no import syntax, so imported content is invisible to it.

Do not create parallel vendor files the runtimes do not need. One `AGENTS.md` often covers all three.

### Nested files

Add a nested `AGENTS.md` only when a subtree needs different commands, ownership or boundaries. Put only the difference in it. Nearer files come later in context in all three runtimes. Codex and Cursor treat that as precedence; Claude Code does not guarantee it, so a nested file must add to its parents, not contradict them. Reach also differs:

- Claude Code and Cursor pick up a nested file when work touches that directory.
- Codex loads only directories from the project root down to where it was started. Started at the root, it never sees `services/payments/AGENTS.md`.

So when a subtree rule must hold for Codex, add a one-line pointer in the root file ("Before editing `services/payments/`, read `services/payments/AGENTS.md`"), or document starting Codex in that directory.

### Size

Codex stops adding files once the combined size reaches 32 KiB by default, so a long root file pushes nested files out. Claude Code recommends under 200 lines per `CLAUDE.md`, and imports do not reduce context cost. Cut content an agent can derive from the code: directory trees, dependency lists, generic style advice.

## Build an evidence map

Read the minimum evidence needed to establish:

- package or workspace boundaries and runtime versions;
- install, dev, build, lint, typecheck, test and release commands;
- generated files, migrations, credentials, deployment configuration and other high-risk areas;
- conventions an agent would get wrong from defaults (package manager, test runner, formatting, file placement);
- required services, environment variables, ports and setup order.

Prefer manifests, scripts, CI workflows and executable configuration over prose. When sources disagree, report the conflict and use the source that controls execution (CI usually wins over README).

Include a path only when it changes how an agent navigates, edits or verifies. Write instructions an agent can check: "Run `npm test` before finishing" beats "test your changes".

## Verify commands proportionately

Label each command:

- **executed:** ran successfully here;
- **partially verified:** syntax or a narrow target ran, but dependencies or services blocked the full run;
- **documented only:** found in a trusted project source, not run;
- **stale or conflicting:** contradicted by configuration, or failed for a repository reason.

Run safe, relevant checks. Do not start long-lived services, mutate external systems, install dependencies or run destructive commands to upgrade a label. State prerequisites next to commands that need them.

## Resolve conflicts explicitly

For each conflict choose one action:

1. retain the nearer scoped rule;
2. replace stale guidance with verified repository behavior;
3. separate runtime-specific mechanics from shared facts;
4. ask the user when two live policies express different intent the repository cannot settle.

Do not silently choose between policy statements about deployment, generated files, security, data handling or ownership.

## Output contract

1. The instruction files written or changed (or, in Explain loading mode, none).
2. A loading table: for each target runtime, which files load at the root and in each scoped directory, and which are shadowed or skipped.
3. A command table with verification labels.
4. Conflicts resolved, preserved, or awaiting a decision.
5. Facts left out because they were unverified or volatile, and any loader fact re-checked against docs this run, with the date.

## Verify

1. Re-read every instruction file that applies to each edited location. Confirm each target runtime loads the intended files and nothing shadows them, using the loading matrix.
2. Where a runtime is installed, confirm with its own check: `/context all` or `/memory` in Claude Code; `codex --ask-for-approval never "Summarize the current instructions."` (add `--cd <dir>` for a subtree) in Codex; Customize, Rules in Cursor. Otherwise label loading as reasoned from docs, not observed.
3. Measure combined bytes on each Codex path (`wc -c`) against the 32 KiB default and each `CLAUDE.md` against about 200 lines.
4. Confirm every path, script, package name, port and environment variable exists in repository evidence.
5. Re-run the safe commands used as acceptance checks, or label them accurately.
6. Confirm nested files hold only scope-specific differences and do not contradict inherited rules.
7. Check `.mdc` frontmatter and glob coverage against the files each rule should govern.
8. Remove unsupported claims, generic agent advice and duplicated repository documentation. Do not describe a documented-only command as tested.
