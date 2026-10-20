---
name: protected-commit
description: >
  Use when a commit is refused with "Protected state edit detected", or before
  editing AGENTS.md, CLAUDE.md, a lockfile, .forge/config.yaml, .github/workflows,
  lefthook.yml, .beads/**, or a generated harness mirror. Do not use to find a
  way around the gate — there is no environment variable that authorizes a
  protected write.
---

# protected-commit

The gate is content-bound and fails closed. Read what it told you, then use the
owning command — or stop and say the path is currently unreachable.

## What the gate actually is

`scripts/protected-state-check.js` runs on every pre-commit (lefthook job
`protected-state`, no glob, so it sees every commit). For each staged file it
calls `assertProtectedWriteAllowed`, and any file that matches a protected
surface needs a **one-time, content-bound Kernel capability** issued for the
exact actor, worktree, surface, path, bytes, and source HEAD.
[verified 2026-08-13 — `lib/protected-state-authority.js`]

Ask the code which surface a path is on rather than guessing:

```bash
node -e "console.log(require('./lib/protected-state-surfaces').assertProtectedWriteAllowed('AGENTS.md'))"
```

## Three things that are commonly believed and are wrong

1. **`FORGE_PROTECTED_STATE_ALLOWED_SURFACES` does not authorize anything.**
   No runtime code path reads it. It appears only in prose docs and one test
   fixture. `docs/reference/protected-state-surfaces.md` says so itself at the
   "Surface-only environment declarations do not authorize protected changes"
   line, and then contradicts itself further down — the contradiction is a
   documentation bug, not a hidden door. [verified 2026-08-13]

2. **The `categories:` block in `.forge/protected-paths.yaml` is not what runs.**
   Runtime enforcement uses a hardcoded `PROTECTED_SURFACES` list in
   `lib/protected-state-surfaces.js`. The manifest's W1 categories
   (`forge_core`, `user_protocol`, `generated_artifacts`) are documentation. So
   `lib/**`, `scripts/**`, and `skills/**` — listed under `forge_core` in the
   manifest — are **not** blocked at runtime today, while `AGENTS.md` is,
   under the legacy surface id `generated_harness`. [verified 2026-08-13]

3. **`--no-verify` is not the answer.** Bypassing hooks is forbidden for agents
   in this repo, and a hook you route around protects nobody. If the gate is
   wrong, the gate gets fixed in its own PR. [Forge #9 ×3]

## Procedure when you are blocked

1. Read the blocked output. It names `path`, `requiredSurface`, `reason`, and
   `repairHint`. The repair hint is the owning command.
2. Regenerate through the owning command rather than hand-editing:
   lockfiles → the package manager; `.forge/config.yaml` → Forge config/setup;
   harness mirrors → `forge setup`; `.beads/**` → `forge migrate --from beads`
   then Forge issue commands.
3. Stage exactly what that command produced. The authorization is bound to the
   bytes; any later touch invalidates it.
4. If no owning command can produce the change you need — **stop**. File a
   kernel issue naming the path, the surface, and the missing writer, and say
   plainly in your report that the change is currently unshippable. Do not
   invent an exemption, do not add a repo-local carve-out, do not weaken the
   check to let your own edit through.

## Known unreachable path (2026-08-13)

`AGENTS.md` classifies as `generated_harness`, and the only command that can
issue a protected-state authorization is `forge release generate-npm-workflow`.
There is therefore no way to commit an `AGENTS.md` edit today — including an
edit confined to the `USER:START`/`USER:END` block that the product tells users
to write in. Treat that as a filed product bug, not as something to work around.
[verified 2026-08-13 — `NPM_WORKFLOW_SOURCE_COMMAND`, `lib/protected-state-authority.js`]

## Done when

The commit passes the gate because the owning command produced the bytes — or
you have filed the issue and reported the blocker in plain words without
shipping a bypass.
