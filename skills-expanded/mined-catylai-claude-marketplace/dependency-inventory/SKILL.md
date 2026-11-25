---
name: dependency-inventory
description: "Builds a read-only inventory of every dependency and runtime pin in a repository (manifest, declared constraint, resolved version, lockfile), producing the table upgrade-research consumes. Use when starting a dependency or runtime upgrade, or when asked what a project depends on, what versions are actually installed, or where .nvmrc, Dockerfiles and CI disagree. Not for latest versions or EOL status (use upgrade-research); not for ordering an upgrade (use upgrade-plan)."
when_to_use: "what does this repo depend on, list our dependencies, which versions are we actually running, inventory the dependencies, which Node version do we use, do we have a lockfile, where are versions pinned, start a dependency upgrade"
argument-hint: "[repository path; defaults to the current directory]"
allowed-tools: Read, Glob, Grep, Bash(npm ls *), Bash(pnpm list *), Bash(yarn list *), Bash(yarn info *), Bash(poetry show *), Bash(uv tree --frozen *), Bash(pip freeze *), Bash(go list -m *), Bash(cargo tree --locked *), Bash(bundle list *), Bash(docker image inspect *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# dependency-inventory

Stage 1 of the upgrade pipeline (dependency-inventory → upgrade-research → upgrade-plan →
upgrade-execute). Inventory the repository at: $ARGUMENTS (if empty, the current directory; if the
path does not exist, say so in one line and stop).

This skill only reads. It records what exists; newer versions, support status and advisories belong
to `upgrade-research`.

**Without a checkout (Cowork/web):** ask the user to paste the manifests and lockfiles (or the root
file listing first, so you can say which ones you need). Build the same table from what is pasted,
set `Resolved` to `unresolved` wherever no lockfile content was provided, and list the files you did
not see under **Not resolved**.

## Why declared and resolved are both recorded

The declared constraint is what gets edited; the resolved version is what runs and what advisories
apply to. `^4.17.0` resolving to `4.17.21` reaches `4.17.21` with no manifest edit; an exact
`4.17.0` does not. A table carrying only one of the two produces plans that edit files needlessly
and miss files that needed editing.

## Workflow

Copy this checklist and tick it off as you go:

```
- [ ] 1. Discover ecosystems
- [ ] 2. Collect declared + resolved per ecosystem
- [ ] 3. Classify missing lockfiles
- [ ] 4. Write the table and findings
- [ ] 5. Verify
```

### 1. Discover ecosystems

Assume the repository is polyglot until the file search says otherwise. Use Glob (skipping
`node_modules`, `.git`, `vendor`, `.terraform`, `target`) for the manifest, lockfile and version-file
names listed in [references/ecosystems.md](references/ecosystems.md#discovery-patterns), plus CI
definitions (`.github/workflows/*`, `.gitlab-ci.yml`, `.circleci/config.yml`,
`azure-pipelines.yml`, `Jenkinsfile`). CI files pin runtimes nobody thinks of as dependencies.

Record every ecosystem found. One that exists in the repo but is missing from the inventory is the
one nobody upgrades.

### 2. Collect declared and resolved

For each ecosystem found, follow its section in
[references/ecosystems.md](references/ecosystems.md). Prefer reading the lockfile with Read/Grep:
it is exact, needs no installed toolchain, and works on every surface. Run a package-manager
command only when the lockfile is binary or impractical to read.

Row scope:

- **Include** runtimes and language versions, direct and dev dependencies, Terraform providers and
  modules, base images (every stage of a multi-stage build), CI runner images, actions, and
  pre-commit hook revisions.
- **Include transitives only when the repo pins them explicitly** (npm `overrides`, Yarn
  `resolutions`, pnpm overrides, a pip constraints file, Gradle `constraints`). Advisory-driven
  transitive rows are added later by `upgrade-research`.
- **Record each version surface separately.** `.nvmrc`, `engines.node`, the Dockerfile `FROM` and
  CI `node-version` are four rows, not one reconciled value. Their disagreement is a finding.

When a command fails or the toolchain is not installed, fall back to reading the lockfile. If there
is no lockfile to read either, set `Resolved` to `unresolved` and `Resolved from` to `none`. Fill
`Resolved` only from a lockfile, a command's output, or an exact pin in the manifest, because a
guessed version hides exactly the gap the later stages need to see.

### 3. Classify missing lockfiles

Give every manifest without a lockfile a note that says which case it is:

| Situation | Note to write |
| --- | --- |
| Application with no lockfile | `no lockfile: builds not reproducible; generate one on current constraints as step zero` |
| Library that intentionally ships none | `no lockfile: intentional (library)`; this is correct and needs no fix |
| Gradle dynamic versions without dependency locking | `no lockfile: dynamic versions unlocked; enable locking before upgrading` |
| `requirements.txt` with loose pins and no compiled lock | `no lockfile: transitives float; Resolved reflects the current environment` |

### 4. Write the table and findings

Use the template in **Handoff contract** below: one table for the whole repository, grouped by
ecosystem, runtimes first within each group. Then the Findings list, with every heading present
even when its answer is "none".

### 5. Verify

Before answering, check:

- Every manifest and version file found in step 1 appears in at least one row's `Manifest`, or is
  named under **Not resolved** with the reason.
- Every cell in `Ecosystem`, `Kind`, `Resolved from`, `Lockfile` and `Pin` uses a value from the
  enums below, and IDs run `I1`, `I2`, … without gaps.
- Every row whose `Resolved` is a version has `Resolved from` other than `none`.

Fix any failure and re-check before handing off.

## Handoff contract

This is the exact format `upgrade-research` reads. Changing a column or an enum here requires the
same change there.

```markdown
## Dependency inventory — <repo name>

| ID | Ecosystem | Manifest | Name | Kind | Declared | Resolved | Resolved from | Lockfile | Pin | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Findings
- **Ecosystems:** <list>
- **Unmanaged:** <versions nothing pins: vendored binaries, `curl | sh` installs, or "none">
- **Disagreements:** <each runtime whose surfaces disagree, citing row IDs, or "none">
- **No lockfile:** <row IDs of manifests with Lockfile = none, or "none">
- **Not resolved:** <files not read or commands that failed, and why, or "none">
```

| Column | Allowed values |
| --- | --- |
| `ID` | `I1`, `I2`, … in table order; later stages cite rows by this ID |
| `Ecosystem` | `node`, `python`, `go`, `rust`, `ruby`, `jvm`, `terraform`, `container`, `ci`, `tooling` |
| `Manifest` | Repo-relative path of the file that declares it (the file an upgrade edits) |
| `Name` | As the ecosystem spells it; runtimes use the product name (`node`, `python`, `go`, `rust`, `ruby`, `java`, `terraform`, `gradle`) |
| `Kind` | `runtime`, `direct`, `dev`, `transitive`, `provider`, `module`, `base-image`, `action`, `hook`, `tool` |
| `Declared` | The constraint verbatim in backticks, or `—` when nothing is declared |
| `Resolved` | Exact version, digest or commit SHA; or `unresolved` |
| `Resolved from` | `lockfile`, `command`, `environment` (installed env such as `pip freeze`, not the project), `manifest` (exact pin in the manifest), `none` |
| `Lockfile` | Repo-relative lockfile path; `none` (the ecosystem uses lockfiles and this manifest has none); `n/a` (no lockfile concept: runtimes, images, actions, hooks) |
| `Pin` | `exact` (version, digest or SHA that cannot move); `range` (a constraint the resolver chooses within); `moving` (a tag, branch or `-latest` label that can change under the same text); `unpinned` (no version, a local path, or a bare name) |
| `Notes` | Free text, or `—` |

## Examples

<example>
Illustrative values, not current facts. A service with Node, Terraform and CI:

| ID | Ecosystem | Manifest | Name | Kind | Declared | Resolved | Resolved from | Lockfile | Pin | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1 | node | `.nvmrc` | node | runtime | `20.11.1` | 20.11.1 | manifest | n/a | exact | — |
| I2 | node | `package.json` | node | runtime | `engines: >=20` | unresolved | none | n/a | range | engines is a floor only |
| I3 | node | `package.json` | express | direct | `^4.18.0` | 4.19.2 | lockfile | `package-lock.json` | range | — |
| I4 | terraform | `infra/versions.tf` | terraform | runtime | `~> 1.7` | unresolved | none | n/a | range | HCP Terraform workspace may pin its own version |
| I5 | terraform | `infra/versions.tf` | hashicorp/aws | provider | `~> 5.40` | 5.62.0 | lockfile | `infra/.terraform.lock.hcl` | range | — |
| I6 | container | `Dockerfile` | node | base-image | `22-alpine` | unresolved | none | n/a | moving | no digest pin |
| I7 | ci | `.github/workflows/ci.yml` | node | runtime | `node-version: 22` | unresolved | none | n/a | moving | — |
| I8 | ci | `.github/workflows/ci.yml` | actions/setup-node | action | `@v4` | unresolved | none | n/a | moving | tag, not SHA |

- **Disagreements:** node runtime: I1 (20.11.1) vs I6 and I7 (22).
</example>

<example>
A Python library with `pyproject.toml` ranges and no lockfile: the dependency rows get
`Resolved` = `unresolved`, `Resolved from` = `none`, `Lockfile` = `none`, and the note
`no lockfile: intentional (library)`. `requires-python = ">=3.10"` becomes its own `runtime` row.
If the user's virtualenv is active, `pip freeze` values may go in `Notes` as
`env has 2.31.0`, and stay out of `Resolved`, because they describe this machine rather than the
project.
</example>
