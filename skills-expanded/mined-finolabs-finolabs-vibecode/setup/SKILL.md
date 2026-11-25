---
name: setup
description: User-run finolabs-vibecode host configuration and instruction files for Claude Code, Codex and Antigravity; add, instructions, check, scan, mode.
disable-model-invocation: true
argument-hint: "[add <feature> | instructions | check | scan | mode [args]]"
---

# Set up finolabs-vibecode

Show `host.md` (local settings) and data root (settings/records folder) before approvals. Scopes: user account, project repository.

| Command (Codex: `$setup <word>`) | Loads |
| --- | --- |
| none | the core path below, then the menu |
| `add <feature>` | `references/features/<feature>.md` (menu below) |
| `instructions` | `references/instructions/procedure.md` |
| `check` | `references/check.md` (read-only), then stop |
| `scan` / `mode [args]` | `references/scan.md` / `references/mode.md` |

A plain sentence selects, never answers a consent question; "install everything" grants nothing. Ambiguous: one clarifying question, core, never several features at once. Codex forwarding is unverified; use sentences. User invocation: Claude Code enforced; otherwise advisory.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged. All questions: native question tool/shape in `references/interview.md`.

## Core path

A bare run says: "Check: `/setup check` (read-only)." Show config/scan date; ask one scope question, user, project or both, recommendation first (user on a new computer, project in a repository that is not set up). Follow `references/core.md`.

Read-back: inert facts only; grants separate, beginner and Quick included, with no default.

Offer the beginner path: "Start with only the essential setup questions?"
Yes: Ask only essentials; writes ask first.
No: Choose Advanced or Quick; switch later.
Undo: Switch paths; prior approvals stand.
Choices: "Yes, start with essentials" / "No, choose another path".
If yes: `references/plain-language.md`; run step 1's `onboard first` and steps that ask nothing; ask only `mode.md` (user), project steps 3, 2 and the menu's threshold; rest: later run, `add`, `scan`, `instructions`. User scope closes: "To adopt the review gate in a repository, run `/setup` there (project scope)." (advisory).
Otherwise **Advanced** asks each inert item; **Quick** confirms inert defaults once. Ask which.
In every mode these keep their own question: moving the data root and its copy; arming `auto` and the auto gate; filling host config; each Antigravity test-command grant; roles and review posting; the Antigravity hook write; the compaction threshold; each instruction-file write. In Quick mode unknowns stay open.

## Menu

After core, load [references/menu.md](references/menu.md) (`afk`, `compaction`).
