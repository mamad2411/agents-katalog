# AGENTS.md

Everything about the project — what it is, architecture, internals, roadmap — lives in [README.md](README.md). Read it first. This file only covers how agents should work and respond here.

## Response style

- Make your answers clear and very concise.
- Use simple, easy-to-understand language. Short sentences.
- Lead with the answer. Skip preamble, filler, and repetition.
- No options or caveats the owner didn't ask for.

## Working rules

- **Not an npm package.** `package.json` is `private: true` — autogit is distributed via the mjenkins-toolbox marketplace (`/plugin install autogit@mjenkins-toolbox`) and install-from-source (`npm link`, which uses the `bin` field; no registry needed). Never run `npm publish` or remove `private: true`. (The upstream `@davidondrej/autogit` is David Ondrej's separate package; this fork uses its own name `@mjenkinsx9/autogit`.)
- Keep it minimal: small files, zero dependencies, simplest thing that works.
- Treat the implementation as a reference of product intent, not fixed architecture.
- Confirm any major structural change with the owner before implementing.
- Roadmap items are owner-gated: don't build them without a go-ahead.
- When behavior or architecture changes, update README.md.

## Releasing — bump the version or the cache stays stale

The `mjenkins-toolbox` marketplace caches this plugin **keyed by its manifest version**. Landing changes on `main` without bumping the version leaves installs on the stale cached copy — refreshes only pick up new code when the version string changes.

When a change should reach users:

1. Bump the version in all five manifests in lockstep — `.claude-plugin/plugin.json` (source of truth), `package.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`. `test/plugin.test.js` fails if they diverge.
2. `npm test`, commit via PR, merge.
3. `git tag vX.Y.Z` + `gh release create vX.Y.Z`. (npm publish stays owner-gated — see Working rules.)

Semver (pre-1.0): features → minor (`0.x.0`), fixes → patch (`0.x.y`).
