---
name: stand-general
description: Global coding standards for all projects and languages. Use when writing any code. Covers linting with lintro, testing with coverage, semantic commits, PR creation, and pre-push AI review with coderabbit and greptile CLIs.
---

# Coding Standards

Global standards that apply to all projects and languages.

## Single Source of Truth

Any value defined in one place and consumed in another should be referenced, not copied.
Applies to versions, paths, URLs, schema constants, and configuration.

- If two files would need to be updated in lockstep, the second is a derived artifact —
  generate it, don't hand-maintain it.
- CI verification of two files agreeing is a smell: the right pattern is
  run-the-generator + `git diff --exit-code`, not parse-and-compare.
- Hand-maintained mirrors of canonical sources rot silently. The cost of a small
  generator is always lower than the cost of recurring drift bugs.

## Before You Write

Before implementing utility logic (file traversal, string parsing, config lookup,
error wrapping), search the codebase for an existing implementation.

- Found a close match? Import or extend it instead of reimplementing.
- Same pattern already in 2+ files? Extract it to a shared module before adding
  a third instance.
- Duplication accumulates one compliant PR at a time — prevent it at writing time
  rather than relying on later audits.

## Pre-Implementation

Answer three questions before creating a new file, module, or significant function:

1. **Does this logic already exist?** Search first; reuse beats rewrite.
2. **Is this the right module?** An existing module growing too large is a signal
   to refactor it, not to create a parallel module beside it.
3. **Will this create duplication later?** If similar future cases are foreseeable,
   put the logic in a shared location from the start.

## Architectural Awareness

When adding a module or significant function:

- Confirm it fits the layer it lives in, and that its dependency direction matches
  the existing architecture.
- Every new dependency arrow between modules must be intentional — never a
  side effect of convenient imports.
- A module growing past ~300–400 lines is a signal to split it along
  responsibility boundaries.

## Dependency Update Triage (Renovate/Dependabot)

- **Merge safe green bumps.** For breaking major bumps, fix and migrate —
  never just close the PR to dodge the work.
  - Don't: close a failing Astro 6→7 Renovate PR because `@astrojs/tailwind`
    no longer builds.
  - Do: migrate to the replacement (`@tailwindcss/vite`) in the same PR, then
    merge.
- **Green doesn't mean safe.** On a repo where CI doesn't cover every path, a
  green PR can still be broken in the un-CI'd parts. Validate those parts
  locally before merging, not just the parts CI checks.
- Backlog handling for dependency issues/PRs (closing, repurposing,
  announcing changes): follow the `issue` skill's Backlog Stewardship section.

## Per-repo agent context (`AGENTS.md` / `CLAUDE.md`)

Every target repo may carry a standing context file that assessment and
implementation skills load automatically. **Precedence:** if both
`AGENTS.md` and `CLAUDE.md` exist, `AGENTS.md` is authoritative — apply it
and do not also apply conflicting `CLAUDE.md` instructions. If only one
exists, use that file. If both exist and their requirements conflict in a
way that blocks safe progress, stop and ask the user which wins rather than
guessing. When present, treat its standards, constraints, and contract as
**binding** for the session — do not re-type them from chat memory.

### Expected sections

Write the file so the **per-repo delta is only the repo facts**. Put recurring
org-wide rules in an org preset section (or point at a shared org doc) rather
than copying them into every repo.

1. **House standards pointers** — toolchains (e.g. `uv` / `bun` / `lintro`),
   lint entry point, CI source / reusable workflows, model repos to copy
   conventions from, and any org-managed ruleset notes.
2. **Contract / operating agreement** — autonomy level, merge policy (who
   merges, squash vs queue, signed commits), babysit/review expectations, and
   how the agent should surface vs keep going.
3. **Standing constraints** — safety limits (e.g. no paid LLM API calls during
   assessment), scope rules, storage limits (e.g. local SQLite only), and
   no-side-effects rules for assessment-only work.
4. **Org preset** — recurring org-wide rules referenced once so each repo file
   stays short; only repo-specific product/org facts belong outside this
   section.

### Consumers

At start of a run, these skills read the target repo's `AGENTS.md` /
`CLAUDE.md` when present and apply it as binding context:

- `analyze-project`
- `implement-issues`
- `babysit-pr`

Missing the file is fine — fall back to chat instructions and `stand-*`
skills. Do not invent standing constraints that are not in the file or the
user's message.

## Cross-cutting References

- Linting and formatting: follow the `lint` skill
- Ignoring lint issues: follow the `lint` skill (Rules section)
- Testing: follow the `test` skill
- Commits: follow the `commit` skill
- Pull requests: follow the `pr` skill
- Pre-push AI review (CodeRabbit): follow the `coderabbit` skill
- Pre-push AI review (Greptile): follow the `greptile` skill
- Per-repo standing context: see **Per-repo agent context** above

## Pre-push review workflow

CLI review mirrors CI and catches issues before slow CI completes. Default: run
**both** Greptile and CodeRabbit when CI uses both.

**Short flow:**

```text
commit → [greptile ‖ coderabbit] → pr
```

**Explicit flow:**

```text
lint → test → commit → [greptile ‖ coderabbit] → pr
```

Each step names the skill to follow.

`‖` means run greptile and coderabbit in parallel when possible. Fix findings, then optional
verify pass. Do not re-run either CLI on unchanged code. CI remains the merge-time
confirmation.
