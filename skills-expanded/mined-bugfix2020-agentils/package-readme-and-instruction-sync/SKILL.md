---
name: package-readme-and-instruction-sync
description: 'Use when: about to commit changes inside packages/<pkg>/, adding a new package to the monorepo, changing a package CLI/API/exports, or preparing an npm release. Enforces that every package ships a user-facing README.md AND a docs/instructions/<pkg>.instructions.md (developer / LLM handoff card), both verified end-to-end against the actual code.'
---

# Package README & Instruction Sync

Every package under `packages/` must keep **two** documents in lock-step with the
code, and **both** must be updated before the change is committed:

| Audience       | File                                             | Source of truth?                               |
| -------------- | ------------------------------------------------ | ---------------------------------------------- |
| End user       | `packages/<pkg>/README.md` (+ `README.zh-CN.md`) | Yes (the npm tarball ships this verbatim)      |
| LLM / next dev | `docs/instructions/<pkg>.instructions.md`        | Yes (sync-script fans it out to `.github/...`) |

If either file is missing, stale, or contradicts the code, this skill is
violated.

## When To Trigger

- About to `git commit` any change inside `packages/<pkg>/`.
- Adding a brand new package to `packages/`.
- Changing a package's CLI subcommands / flags / public exports / config schema.
- Preparing an `npm publish` (combine with `npm-package-publish-checklist`).
- Reviewing a PR that touches a package without touching its README or
  `<pkg>.instructions.md` — flag it.

## Required Procedure

### Step 1 — README (user-facing)

The README is the npm package page. A user who has never seen the repo must be
able to install and use the package after reading only this file. It must
contain:

1. What the package is, in one paragraph.
2. Install command for at least one package manager.
3. Copy-paste runnable usage / CLI examples.
4. CLI options or API table when applicable.
5. Agent / LLM behavior notes if the package is meant for agents (link to the
   in-repo `LLM_USAGE.md` if the package ships one).
6. Explicit "what it does NOT do" if scope boundaries matter.

Bilingual style is encouraged — mirror `packages/quality-gate/README.md` +
`README.zh-CN.md` + the language switcher line at the top.

### Step 2 — README sandbox verification (mandatory)

A successful `pnpm build` is **not** proof the README works. Before committing
or releasing, walk every README example end-to-end inside a throwaway sandbox:

```sh
mkdir -p .tmp/<pkg>-smoketest
cd .tmp/<pkg>-smoketest
# install the freshly packed tarball or the workspace dist as the README tells a user to,
# then run every example: CLI commands, SDK calls, config flows.
```

The sandbox lives under `.tmp/` (gitignored). Do **not** commit it. If any
example fails, the README is wrong — fix the README **or** fix the code, then
rerun. Skipping this step is the #1 way READMEs and code drift apart.

### Step 3 — `<pkg>.instructions.md` (LLM / dev handoff)

Live source: `docs/instructions/<pkg>.instructions.md`. The
`scripts/dev/sync-agent-instructions.mjs` generator copies it to
`.github/instructions/<pkg>.instructions.md`. Frontmatter:

```yaml
---
applyTo: 'packages/<pkg>/**'
---
```

Body must contain (use `quality-gate.instructions.md` as the canonical
template):

1. **Purpose** — what this package owns inside the monorepo, what it does not.
2. **Public surface** — bins, exports, important env vars / CLI flags.
3. **Architecture** — key modules, data flow, single-responsibility split. A
   short ASCII or mermaid diagram is welcome.
4. **State as of this commit** — what works, what is partial, known limits.
5. **Anti-patterns / forbidden moves** — landmines that already cost time once.
6. **Test convention** — where sandboxes live, what scripts are sources of truth.
7. **Handoff checklist** — the smallest set of files / commands the next
   LLM/dev should look at to onboard in under 2 minutes.

### Step 4 — Register in sync manifest

If creating a brand new `<pkg>.instructions.md`, append to
`docs/instructions/sync-manifest.json` `sources`:

```jsonc
{ "file": "<pkg>.instructions.md", "summary": "<short summary>" }
```

Then run the sync (and stage the regenerated targets):

```sh
pnpm run sync:instructions
```

Verify nothing else drifted:

```sh
pnpm run sync:instructions:check
```

This rule is shared with `instructions-sync-discipline`; never hand-edit
`.github/instructions/*` or `.agents/skills/*`.

### Step 5 — Commit together

Source README, source `<pkg>.instructions.md`, regenerated targets, and the
code change all go in **one** commit (or one PR). Splitting them across commits
risks merging code without docs and is forbidden by
`instructions-sync-discipline`.

## Quick Self-Check Before `git commit`

- [ ] `packages/<pkg>/README.md` updated and contains every new / changed flag / API.
- [ ] If bilingual: `packages/<pkg>/README.zh-CN.md` mirrors the change.
- [ ] Every README example reproduced successfully in `.tmp/<pkg>-smoketest/`.
- [ ] `docs/instructions/<pkg>.instructions.md` updated to reflect the new
      state, anti-patterns, handoff steps.
- [ ] `docs/instructions/sync-manifest.json` lists the file (only required for
      brand new packages).
- [ ] `pnpm run sync:instructions:check` exits 0.

If any box is unchecked, do not commit.

## Related Skills

- `instructions-sync-discipline` — controls the source-of-truth + generator
  workflow this skill leans on.
- `npm-package-publish-checklist` — README is part of the publish artifact;
  this skill is a hard prerequisite for a release PR.
- `branch-name-standard` — pick `docs/<pkg>-<topic>` or `chore/<pkg>-...` when
  the work is doc-only.
