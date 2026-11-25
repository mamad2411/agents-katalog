---
name: turnstile-init
description: Install the turnstile plugin and pipeline agents into the user's ~/.config/opencode and verify sync. Use when the user asks to set up turnstile, init or check the install, uninstall it, or check status of the turnstile install, or after changing marker syntax in this repo. The plugin injects the orchestrator policy at runtime (primarily via the session.context channel, with the execute.after hook as the fallback re-supply); it does not write a contract block into AGENTS.md.
---

# Turnstile init

Install the turnstile plugin and the pipeline agent definitions into the
user's `~/.config/opencode` and verify the install. The orchestrator policy
is injected at runtime by the plugin (`src/policy.ts`) — nothing is written
to any instructions file, ever.

Two contexts this skill can run in; detect which one you are in first:

- **Inside the turnstile git repo** (a `.git` directory plus a `package.json`
  with an `init` script): use the repo commands `npm run init` /
  `npm run install:check`. Symlink mode is the default there — the checkout
  stays the source of truth.
- **Anywhere else** (npm-package or npx context): use the CLI,
  `npx opencode-turnstile init` / `npx opencode-turnstile check`. Do NOT run
  `npm run init` — that script only exists in the repo. The install mode is
  resolved from an explicit flag, then the manifest's `mode` field, then
  auto-detect: a `.git` checkout installs by linking, a package install
  copies.

## Steps

1. Install:

   - In the repo: `npm run init`
   - Elsewhere: `npx opencode-turnstile init`

   Don't override the mode unless a step fails. Use `--copy` only when the
   user refuses symlinks or the install target is a dotfiles repo that
   rejects them (repo: `npm run init -- --copy`; CLI:
   `npx opencode-turnstile init --copy`). Copy mode records everything in a
   ledger (`~/.config/opencode/.turnstile-install.json`).

   Targets come from `install.json`; unowned files in the target directories
   are never touched. Conflicts (a real file differing from the repo, or a
   user-edited copy) fail with a per-path summary. Show the user the output
   and stop — don't force anything with `--force` without asking.

2. Verify — must exit 0:

   - In the repo: `npm run install:check` (add `-- --copy` for copy mode)
   - Elsewhere: `npx opencode-turnstile check`

   Drift or a conflict is reported per path; `check --repair` prints a
   write-free "would repair" dry run, and `install --repair` auto-fixes
   missing/stale paths (a real conflict still needs `--force`, with the
   user's say-so). Both `init` and `check` also load-probe the installed
   plugin entry point and report `loadable`/`unloadable` — an unloadable
   import graph fails the run. `npx opencode-turnstile uninstall` removes
   manifest-owned files when the user wants them gone.

3. AGENTS.md is out of scope: turnstile never writes to any instructions
   file — the orchestrator policy is injected at runtime from `src/policy.ts`,
   and nothing under `~/.config/opencode` besides the manifest targets
   should be touched. Do not paste anything into AGENTS.md.

4. Tell the user to **restart OpenCode** (or `opencode service restart`) so
   the plugin loads. Give them the status command for later:

   - In the repo: `node bin/cli.mjs status [--json]` (the local checkout)
   - Elsewhere: `npx opencode-turnstile status [--json]`

## Repo-only maintenance note

Inside the repo after changing marker syntax, run `node scripts/check-markers.mjs`
(it extracts the parser regexes from `turnstile.ts` and `src/markers.ts` and
asserts every README example, agent template, policy template, and the
evidence emitter's `MARKER_OK` copy parses; it also guards the canonical
marker shape and runs malformed/trailing-junk negative probes); that is a
development check, not part of a user install — skip it elsewhere.

## Report

Tell the user: which files were linked or copied (created or updated), which
mode was used (link vs copy), that the orchestrator policy is injected at
runtime (no instructions-file block), that OpenCode must be restarted to
load the plugin, and the status command for later. Do not quote the injected
policy back; summarize.
