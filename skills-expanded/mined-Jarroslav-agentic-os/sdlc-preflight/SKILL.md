---
name: sdlc-preflight
version: 0.1.0
license: Apache-2.0
discoverable: true
authors:
  - agentic-os
description: >-
  Force-runs a full environment-readiness check for the agentic-sdlc plugin and
  overwrites .agentic/agentic-sdlc/doctor.json with the fresh result, ignoring
  any existing fingerprint or TTL cache. Invoke when the user asks to verify
  the agentic-sdlc setup, re-run doctor, check whether superpowers/node/git
  are ready, or asks for the legacy sdlc:doctor command on a host (for
  example, a Codex-class host) that has no native slash-command support and
  must substitute a skill for it.
  Not for: fixing the problems it reports, verifying the agentic-os layer (agentic-doctor), or cached readiness checks — it always re-runs in full.

---

# sdlc-preflight

## What it does

Runs the agentic-sdlc environment-readiness check on demand and rewrites
`.agentic/agentic-sdlc/doctor.json` unconditionally — it never consults an
existing fingerprint or respects any TTL, so every invocation is a full,
fresh check. This skill is the skill-based stand-in for a legacy
`sdlc:doctor` command, for hosts that do not support commands and must
resolve equivalent behavior through skills instead.

> Environment readiness is cheap to check and expensive to assume wrong —
> a stale doctor.json can let a downstream phase proceed on tooling that
> silently regressed. Force-checking on every explicit invocation removes
> that risk at the cost of a few subprocess calls.

## When to invoke

- The user asks to verify, check, or re-run the agentic-sdlc environment
  check ("check my sdlc setup", "run doctor", "verify superpowers/node/git").
- The user is on a host without native slash-command support and asks for
  the equivalent of `sdlc:doctor`.
- Any other agentic-sdlc skill or the orchestrator needs a guaranteed-fresh
  readiness signal rather than whatever is currently cached on disk.

## Inputs

None required from the caller. The routine operates entirely on the local
environment and the plugin's own version string (used in the fingerprint
formula below). No project guide files are read or required.

## Operating steps

1. **Anchor to project root.** Run `pwd` so the output path and all checks
   resolve against the correct working directory.
2. **Check `superpowers`.** Attempt to invoke `superpowers:brainstorming`.
   - If it is not invocable, treat the plugin as absent: record
     `present: false`, skip the version field, and do **not** attempt any
     installation — only prepare a remediation hint for the summary.
   - If it is invocable, record `present: true` and capture its version.
3. **Capture toolchain versions.** Run `node --version` and `git --version`
   verbatim; parse each into an `ok` boolean plus the raw version string.
4. **Compute the fingerprint.** Apply the formula
   `fingerprint = hash(node + superpowers version + plugin version)` over
   the captured node version, the superpowers version (or its absence), and
   this skill's own `0.1.0` plugin version.
5. **Write the output file.** Overwrite `.agentic/agentic-sdlc/doctor.json`
   with the schema below — always a full rewrite, never a merge with
   whatever was there before.
6. **Print the summary.** Emit a color-coded (green/red) pass/fail table.
   On any failing check, name the specific check(s) that failed and give a
   one-line remediation hint (e.g., install/upgrade guidance) directly
   beneath the table.

## Decision rules

| Condition | Result |
|---|---|
| `superpowers:brainstorming` not invocable | `checks.superpowers.present = false`; overall `passed = false` |
| `node --version` fails or is unparsable | `checks.node.ok = false`; overall `passed = false` |
| `git --version` fails or is unparsable | `checks.git.ok = false`; overall `passed = false` |
| All three checks succeed | overall `passed = true` |
| Any check fails | halt after writing output; print failing check name(s) + remediation hint; never auto-install |

## Outputs

`.agentic/agentic-sdlc/doctor.json` — always rewritten in full, verbatim
field names:

```json
{
  "schema": 1,
  "checked_at": "<when this ran, ISO>",
  "passed": true,
  "checks": {
    "superpowers": { "present": true, "version": "<as reported>" },
    "node": { "version": "<as reported>", "ok": true },
    "git": { "version": "<as reported>", "ok": true }
  },
  "fingerprint": "<hash of the inputs above, so a stale result is detectable>"
}
```

Plus a console pass/fail summary table (color-coded), with remediation
hints appended on failure.

## Out of scope

- **Ticket-system adapters.** Never validated here — that check is owned by
  the `story-intake` skill and is invoked lazily, only when a ticket
  adapter is actually needed for the current work.
- **Installing dependencies.** On a missing or outdated `superpowers`,
  `node`, or `git`, this skill only reports and suggests a fix; it never
  installs or upgrades anything itself.
- **Project guide files.** Nothing under the project's guide/documentation
  tree is read or modified by this routine, under any outcome.
- **Cache/TTL honoring.** There is no fast path — every invocation performs
  all three checks fresh, regardless of how recently `doctor.json` was
  written.

## References

This skill carries no `references/` tree. The check logic above is fully
self-contained: it shells out to `pwd`, `node --version`, and
`git --version`, and probes `superpowers:brainstorming` directly — it does
not consult `.agentic/guides/` or any other bundled reference material.
