---
name: project-toolchain
description: Work out which commands actually lint, test, build and format THIS project before running any of them - by reading its manifests and configs, never by assuming. Use whenever a command or agent needs to "run the project's lint/test/build", when a check fails with "command not found", or when onboarding the AI-SDLC harness into an unfamiliar repo.
allowed-tools: Read, Grep, Glob, Bash
---

# project-toolchain

Several parts of this harness say "run the project's lint and test commands"
without saying what they are — `/review`, `/pr`, `/skill-approve`, and the
`reviewer` and `security` agents all defer that decision to the project. This
skill is how that decision gets made, so a framework-agnostic harness can run
real checks in a repo it has never seen.

Never assume `npm test` or `flutter analyze`. Guessing produces one of two bad
outcomes: a "command not found" that looks like a broken harness, or — worse —
a check that appears to pass because it silently did nothing.

## Steps

1. **Find the manifest**, nearest to the working directory, checking in this
   order and stopping at the first hit:

   | File | Ecosystem | Where the commands are |
   |---|---|---|
   | `package.json` | Node | its `scripts` object |
   | `pubspec.yaml` | Dart/Flutter | conventional `flutter`/`dart` commands |
   | `Cargo.toml` | Rust | `cargo fmt/clippy/test/build` |
   | `go.mod` | Go | `gofmt`, `go vet`, `go test ./...`, `go build ./...` |
   | `pyproject.toml` / `setup.cfg` | Python | tool sections (`ruff`, `black`, `pytest`) |
   | `Makefile` / `Justfile` | any | its targets — these override the above when present |
   | `build.gradle(.kts)` / `pom.xml` | JVM | `gradle`/`mvn` tasks |

2. **Read the scripts, do not infer them.** For Node, print
   `package.json`'s `scripts` and use those exact names. A repo with
   `"test": "turbo run test"` is run with the package manager's `test`
   script, not with `vitest` or `jest` directly, even when those are the
   underlying runners — the script may set env, ordering, or workspace
   scope that matters.

3. **Identify the package manager from the lockfile**, not from habit:
   `pnpm-lock.yaml` → `pnpm`, `yarn.lock` → `yarn`, `bun.lockb` → `bun`,
   `package-lock.json` → `npm`. Running `npm test` in a pnpm workspace is a
   common way to get confusing failures.

4. **Detect a monorepo** and respect its scoping. `pnpm-workspace.yaml`,
   `turbo.json`, `nx.json`, `lerna.json`, or a `workspaces` field mean a
   root-level command fans out to every package. When the change is scoped
   to one package, prefer that tool's filter (`turbo run test --filter=<pkg>`,
   `pnpm --filter <pkg> test`) so a five-minute full run does not hide a
   ten-second answer.

5. **Verify before relying on it.** Run the resolved lint or test command
   once. If it fails with a missing-binary error rather than a real finding,
   dependencies are not installed — say so and stop, rather than reporting
   the check as failed on its merits. There is a real difference between
   "the tests fail" and "the tests did not run", and only one of them is the
   author's problem.

6. **Report the resolved toolchain explicitly** before using it, so the
   human can correct a wrong guess cheaply:

   ```
   Toolchain for <repo>:
     package manager: pnpm (pnpm-lock.yaml)
     monorepo:        turbo (turbo.json) — filter with --filter=<pkg>
     lint:            pnpm lint
     test:            pnpm test
     build:           pnpm build
     format check:    pnpm format:check
   ```

7. **Record it** so the next session does not re-derive it: write the
   resolved commands into the project's `CLAUDE.md`, or a `toolchain:` block
   in `.claude/settings.json`. Prefer reading that record on later runs, but
   re-verify it if a command starts failing — records go stale when a repo
   migrates package managers.

## Anti-patterns to refuse

- Running `npm test` / `yarn test` / `flutter test` without having read a
  manifest that says so.
- Reporting "lint passed" when the command was not found or exited non-zero
  for a setup reason.
- Running a full monorepo test suite when the diff touches one package and
  the tool supports filtering — unless the change is cross-cutting.
- Installing dependencies unasked as a way to make a check run. Report the
  missing setup; installing can rewrite a lockfile the team owns.
- Writing a resolved toolchain into a shared file when it was only inferred,
  not verified by running it.
