---
name: init
description: Onboard a repo to the la plugin — detect its tracker, test/lint/type-check commands, Codex, Sonar and any existing OpenSpec or architecture setup, propose a complete living-architecture.yaml with a source for every key, ask only what cannot be detected, write the file, then offer the type-check baseline and la:arch-init. Also the fast path other skills run when a repo has no config, and the way to edit or convert an existing config.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output — unless the only failure is the existing `living-architecture.yaml` being invalid or declaring an older format, which this skill converts (steps 1 and 5).

# Onboard a repo

`living-architecture.yaml` records each gate of the flow as an explicit decision; its presence means the repo
is onboarded. Keys, defaults and the doctor's consistency checks are in `docs/configuration.md` of the plugin
repo; `la-config show` prints the resolved values.

**Fast path.** When another skill's preflight reports the missing config, run steps 1–6 only, then hand back
to that skill. A full run (the user invoked `/la:init`) continues to step 7.

## 1. Detect

Read, don't ask. For each key note the value and where it came from:

- **Existing config.** If `living-architecture.yaml` exists, this run edits it in place: start from its
  values. Read it as raw YAML, not with `la-config` (which rejects removed keys and an older format). Under `reviewers`, the
  `coderabbit` flag and Sonar's `enabled` switch were removed (both bots are detected per PR): propose
  deleting them and keeping Sonar's `project_key`. `living-architecture.local.yaml`, if present, holds one
  contributor's overrides; never fold its values into the committed file.
- **`tracker`.** `linear` when the Linear MCP server is available and branch names look like
  `<user>/<key>-<slug>` (`git branch -a`); `github` when branches look like `<N>-<slug>` or the repo uses
  GitHub issues (`gh issue list --limit 5`); otherwise undetected.
- **`issue_key_pattern`.** `#\d+` for `github`; the default for `linear`.
- **`openspec`.** `true` when `openspec/` exists; otherwise undetected (an opinion).
- **`architecture`.** `true` only when `architecture/index.yaml` exists; otherwise `false` (`la:arch-init`
  flips it when it finishes).
- **`reviewers.codex`.** Whether the Codex MCP server (`mcp__codex__codex`) is available in this session.
- **`reviewers.sonar.project_key`.** Only needed when it cannot be inferred: Sonar in CI
  (`.github/workflows/*`) with no `sonar-project.properties` key. `la-pr-reviewers <PR>` on a recent PR shows
  what is inferred.
- **dr's keys** (`commands.test`, `commands.typecheck`, `exempt`, `refactor`). Detect them as step 1 of the
  `dr:init` skill describes; they go in this same file.
- **`commands.lint`.** From the package manifests (`la-config get lang.<language>.markers`, `package.json` scripts),
  a `Makefile`, the CI workflows and `CLAUDE.md`/`AGENTS.md`.
- **`conventions`.** Keep the defaults unless the repo's own instructions say otherwise.

## 2. Propose

Show the complete proposed `living-architecture.yaml`, every key on its own line with a trailing comment
naming its source (`# detected: package.json`, `# default`, `# your answer`). Omit keys whose value equals
the default only when the source is `default`. Leave out `format`: step 5 stamps it.

## 3. One question round

Ask, in one message, only about keys that are opinions or undetected: usually `openspec` when there is no
`openspec/`, `tracker` when undetected, and `reviewers.codex` when Codex is not available here. For each, give
the PROS and CONS of each option and a RECOMMENDATION. Offer only genuine options: less work is never a pro and
more work never a con unless the amount is ridiculously large, and an option that breaks something working today is
not offered without a very good reason. Never ask about a key you detected with confidence.
`tracker: none` with `openspec: false` leaves `/la:pr` no place for the plan to survive a session reset:
propose it only when the user will not use `/la:pr` and only wants the architecture enforced.

## 4. OpenSpec scaffold

If the answer is `openspec: true` and `openspec/` is absent, run the `la:openspec-init` skill now, before
writing the file, so the flag matches the disk.

## 5. Write the file

Write `living-architecture.yaml` at the repo root, with the flags matching the disk (`architecture: false`
until `la:arch-init` finishes), then run `la-arch-migrate`: it stamps the current `format` and converts an
older repo. Check it with `la-config show`.
If `git check-ignore -q living-architecture.local.yaml` exits 1 (not ignored), offer (yes/no) to add
`living-architecture.local.yaml` to `.gitignore`: it holds per-person overrides and must never be committed.

## 6. Doctor

Run `la-doctor --plugin <this skill's base directory> --require-config`. Fix whatever it reports (a wrong flag, an invalid value) and
re-run until it passes.

## 7. Next steps (full run only)

Offer, each as a yes/no:
- **Type-check baseline.** As step 5 of the `dr:init` skill describes.
- **Architecture.** If `architecture: false`, offer the `la:arch-init` skill to build the model.

Never wire CI; the docs explain how when the user asks. Do not commit: the user commits the config.
