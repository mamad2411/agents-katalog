---
name: command-surface
description: >
  Use when adding, renaming, or deleting a file in lib/commands/, or when a
  build fails with a manifest-drift error or an unresolved command require. Do
  not use for changing behaviour inside an existing command — that needs no
  surface work.
---

# command-surface

A command file is five surfaces, not one. Add the file and stop, and the
compiled binary breaks while dev-mode auto-discovery hides it from you.

## The surfaces

Adding, renaming, or removing `lib/commands/<name>.js` means all of these:

1. **Manifest** — regenerate the static require graph:

   ```bash
   node scripts/gen-command-manifest.js          # write if changed
   node scripts/gen-command-manifest.js --check  # exit 1 if stale
   ```

   `lib/commands/_manifest.js` is generated; never hand-edit it. Drift is
   enforced by `test/structural/command-manifest-drift.test.js`.
   [verified 2026-08-13]

2. **Registry** — the command must resolve through the CLI registry
   (`test/forge-cli-registry.test.js`, `test/cli-flags.test.js`).

3. **Skill coverage** — `skills/coverage.json` maps every registered
   user-facing command to an owning skill, or carries an explicit
   `{ exempt: <reason> }`. Enforced by `evaluateCoverage` in `lib/skill-eval.js`
   and gated in `test/skill-eval.test.js`. [verified 2026-08-13]

4. **Test lane** — an entry in `DIRECT_TEST_CANDIDATES` (`lib/commands/test.js`)
   so the new file resolves to real tests instead of forcing the full suite.
   See the `test-lane` skill.

5. **Documentation** — the command help text and, if it is a stage or utility,
   its row in `AGENTS.md`.

## Rules

- **Regenerate, never hand-write, the manifest.** Dev-mode discovery masks a
  stale manifest locally; `bun build --compile` and the drift gate do not.
- **Exempt means complete, not deferred.** A command leaves `coverage.json` as
  `exempt` only when it is genuinely mapped, routable, and documented — and only
  in the PR that owns it. A hollow mapping just draws review rounds.
- **Use Forge's own generator.** Re-implementing what the skill CLI already does
  is a recurring correction here: *"why should we do the work"*. One canonical
  source, everything else generated. [Forge #5 ×4]
- **Names stay short.** `status`, `ready`, `ship`, `trace`. Long or technical
  command names are a taste failure in this CLI.

## Done when

`node scripts/gen-command-manifest.js --check` exits 0, the registry and
coverage tests pass, `classifyPushTests` reports a targeted lane, and you can
name the skill that owns the new command.
