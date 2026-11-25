---
name: dep-resolve
description: 'Dependency-conflict resolution when a `fix` version bump fails — diagnose the peer-dep tree, find a compatible safe version set, propose package-manager overrides (`overrides`/`resolutions`/`replace`/`[patch]`), fall back to safe-harbour inline patching. Use when an upgrade is blocked by transitive constraints, a peer-dep conflict surfaces, or you need to override a vulnerable transitive without bumping the parent.'
license: Apache-2.0
allowed-tools: Bash(vulnetix:*) Read Grep Glob Edit Bash(npm:*) Bash(yarn:*) Bash(pnpm:*) Bash(pip:*) Bash(cargo:*) Bash(go:*)
argument-hint: <package-name> [--target-version X]
user-invocable: true
model: sonnet
metadata:
  outputBudget: medium
  cooldown: per-session
  chain: "dependency-choice, fix, verify-fix"
---
# Vulnetix Dependency Resolution Skill

## Use when

- `fix` proposed a version bump but `<pm> install` errored on peer-dep conflict.
- A transitive vulnerable dep needs pinning without bumping the direct dependency.
- Lockfile resolution fails after a merge — diagnose which deps disagree.
- Considering a package-manager override (`npm overrides`, `pnpm overrides`, `yarn resolutions`).
- Last-resort: copy patched upstream code inline as first-party (Type A0 inline).

## Don't use for

- Initial fix proposal — use `fix` first.
- Just looking up safe versions — use `dependency-choice`.
- Multi-CVE upgrade orchestration — use `@dep-upgrade-orchestrator`.

## Conventions

Follows `skills/_lib/contract.md`. In short: use the `vulnetix_*` MCP tools when the agent has them and the CLI otherwise — both shape their own output, so there is no jq step any more. Independent calls go out as concurrent Bash tool calls in one message. One trailing suggestion, not a playbook. See the contract for surface selection, output style and memory writes.

When `fix` proposes a version bump but the lockfile resolution fails (peer-dep conflict, transitive constraint, etc.), use this skill to find a compatible set.

## Step 1: Load capabilities + memory

Read `.vulnetix/capabilities.yaml` (`derived.primary_package_manager` decides which lockfile to read) and `.vulnetix/memory.yaml` (decisions / safe-harbour notes).

## Step 2: Map the conflict

```bash
# npm/pnpm/yarn
npm ls "$PACKAGE" 2>&1 || pnpm why "$PACKAGE" || yarn why "$PACKAGE"
# pip
pip show "$PACKAGE"
# go
go mod why "$PACKAGE"
# cargo
cargo tree -i "$PACKAGE"
```

Pick the command for the detected package manager. Capture the dep tree paths.

## Step 3: Pull safe-version graph

```bash
vulnetix vdb versions "$PACKAGE" -o json
vulnetix vdb fixes "$PACKAGE" -o json
```

For each candidate target version:
- Cross-check transitive constraints from Step 2
- Cross-check known vulns at that version (`vdb vulns`)

## Step 4: Propose resolution

Prefer (in order):
1. **Single bump** — newest patch version that fixes the vuln and satisfies constraints
2. **Override** — package-manager override (npm `overrides`, pnpm `pnpm.overrides`, yarn `resolutions`)
3. **Safe-harbour inline** — copy upstream patch into repo as first-party code (link to `fix` Type A0 path)
4. **Workaround only** — `detection-rules <vuln-id>` while waiting for upstream

## Step 5: Apply (with confirmation)

For option 1: edit the manifest, run `<pm> install` (npm/pnpm/yarn/pip/go/cargo).
For option 2: write the override block, run install.
For option 3: hand off to `fix` Type A0.
For option 4: hand off to `detection-rules`.

Always pause for user approval before writing manifest edits.

## Step 6: Verify

Suggest `verify-fix <vuln-id>` after the resolution lands.

## Memory update

`event: dep-resolve` with the chosen path.

## Edge cases & gotchas

- Dep-tree diagnosis uses package-manager-specific commands: `npm ls`, `pnpm why`, `yarn why`, `pip show`, `go mod why`, `cargo tree -i`. Wrong PM = misleading output.
- Override semantics differ per ecosystem: npm `overrides` is post-install hoist, pnpm `pnpm.overrides` is install-time pinning, yarn `resolutions` works with both classic and Berry but with different scoping.
- Pip has no clean override — pinning the transitive in requirements.txt + `--no-deps` for the parent is the cleanest workaround.
- Go `replace` directives work only when the module path is identical (no rename through fork).
- Cargo `[patch]` requires the patched crate at a real path or git ref; cannot inline a hex string.
- Inline-as-first-party (Type A0) introduces license obligations from the upstream package — copy the LICENSE file too.
