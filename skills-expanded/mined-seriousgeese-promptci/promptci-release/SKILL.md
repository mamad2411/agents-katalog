---
name: promptci-release
description: >-
  Walks through releasing @promptci/cli and @promptci/core to npm from this repo. Use this whenever the user wants to publish, release, ship, cut, or tag a new PromptCI version, or bump the cli or core package version — including casual phrasing like "let's ship 0.0.3" or "cut a release". Always consult this before running any pnpm/npm publish or version-bump commands here — the release process has non-obvious gotchas that are easy to get wrong by guessing.
---

See AGENTS.md for this repo's core behavioral rules (verification loop, honesty, scope
control) — this skill only layers release-specific steps on top of those.

# Releasing PromptCI

This repo publishes two npm packages together, in lockstep: `@promptci/cli` and
`@promptci/core`. Core is bundled into cli's built output as a frozen esbuild snapshot (a
devDependency of cli, not a runtime one), so nothing on npm's side keeps their versions tied
together on its own — the release process is what enforces that. See CONTRIBUTING.md's
"Releasing" section for the short version; this skill has the exact command sequence plus traps
that section doesn't spell out.

Read [references/publish-release.md](references/publish-release.md) for the full step-by-step
(bump both versions, PR, merge, tag the merge commit, watch the publish workflow, then the
action.yml follow-up).

## The one thing to internalize before touching any commands

`pnpm --filter <pkg> version <newversion> --no-git-tag-version` looks like the obvious way to
bump a single workspace package's version, but it does not work: combined with `--filter`, pnpm
treats `version` as a request to run a `"version"` npm script rather than its own built-in
version-bump subcommand. Neither package defines one, so pnpm prints `None of the selected
packages has a "version" script` and exits 0 — no version changes, no error surfaces unless
you're reading the output closely. The correct form runs `pnpm version` *from inside* each
package's own directory. The reference doc uses the correct form; don't shortcut it.

## Verifying you're not about to publish a lie

Both packages must land on the exact same version. `pnpm check-versions` (backed by
scripts/check-version-sync.mjs) checks this locally, and it's also enforced as a CI step and
again inside the publish workflow itself — but running it yourself right after bumping is a fast
way to catch a typo before it becomes a PR.
