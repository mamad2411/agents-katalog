---
name: specrail
description: Use only when the user explicitly says SpecRail core, asks to install or configure SpecRail, or says SpecRail without Heavy or implx. Never use for SpecRail Heavy, implx, or ordinary coding tasks.
---

# SpecRail

SpecRail is opt-in. Never activate this skill merely because the user asks to
triage, plan, implement, review, or fix code. If the request says Heavy or
implx, leave routing to that distinct entrypoint.

## Select a route

- Install or inspect local skills: use the profile commands below.
- Triage: search existing Issues, PRs, branches, docs, and code; clarify goal,
  context, constraints, and done-when.
- Specify: write user behavior and acceptance criteria before technical design.
- Plan: map stable requirements to owned tasks and repository-native checks.
- Implement: reuse the original branch and PR, reproduce bugs, make the
  smallest complete change, and test it.
- Review: inspect the current head and diff; report concrete findings with
  severity and exact locations.
- Diagnose CI: collect fresh logs, reproduce, test one root-cause hypothesis,
  fix, and rerun the failing command.
- Release note: summarize an already merged change without publishing it.
- Queue work: use `implx` only when the user explicitly invokes it.
- Heavy work: use `specrail-heavy` only when the user explicitly requests
  SpecRail Heavy.

## Direct workflow

1. Read the target repository's active instructions.
2. Search before creating new work.
3. Reuse existing ownership: branch, PR, Issue, or worktree.
4. Confirm scope and done-when before non-trivial edits.
5. Use the repository's own build, test, lint, type-check, and CI.
6. Review the current diff and remote state before reporting completion.
7. Push, comment, close, publish, or merge only within the caller's explicit
   authorization.

SpecRail organizes work. It does not grant permission, replace repository
policy, or produce an authoritative merge verdict.

## Installation profiles

User-level installation defaults to `~/.agents/skills`. The installed bundle
includes machine-readable metadata that disables implicit invocation.

Preview the default single-entry installation:

```sh
python3 tools/install_codex_skills.py --repo .
```

Install the default profile:

```sh
python3 tools/install_codex_skills.py --repo . --profile core --apply
```

Install the explicit Heavy entry:

```sh
python3 tools/install_codex_skills.py --repo . --profile heavy --apply
```

Install Heavy plus the explicit queue shortcut:

```sh
python3 tools/install_codex_skills.py --repo . --profile all --apply
```

Changing profiles removes only stale SpecRail-managed skill directories. It
must preserve unrelated user-owned skills. Diagnose without writing:

```sh
python3 tools/install_codex_skills.py --repo . --profile core --check-installed
```

Migrate an older global installation by previewing, then applying:

```sh
python3 tools/install_codex_skills.py --repo . --profile core \
  --legacy-target-dir ~/.codex/skills \
  --legacy-archive-dir ~/.codex/specrail-skills-v1
```

Add `--apply` only after reviewing the exact install and cleanup paths.
