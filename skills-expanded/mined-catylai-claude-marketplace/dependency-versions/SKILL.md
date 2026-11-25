---
name: dependency-versions
description: "Use whenever a version number is about to be written into a manifest: adding or scaffolding a dependency, dev tool, runtime pin, base image, GitHub Action, Terraform provider or Helm chart, in a new project or an existing one. The standard: look up the registry's latest stable release at write time (never from memory), declare it anchored to its major, and let the committed lockfile hold the exact resolve. Also use when reviewing a diff that adds a dependency. Not for moving versions that already exist (use dependency-upgrades)."
license: MIT
---

# Dependency versions

Every version number you know is a snapshot from training; by the time it is typed into a
manifest it is months stale, and a stale pin is the most common way a new project starts life
already behind. So a version is never written from memory. It is looked up at write time, declared
anchored to its major so patches and minors flow through the resolver, and the exact resolve is
committed in the lockfile. Three artifacts, three jobs: the registry says what is current, the
manifest says what range is acceptable, the lockfile says what runs.

## The standard in one table

| Ecosystem | Manifest shape (major anchor) | Lockfile, always committed | Look up latest stable |
| --- | --- | --- | --- |
| npm / pnpm / yarn | `"pkg": "^x.y.z"` | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` | `npm view pkg version` · `https://registry.npmjs.org/pkg/latest` |
| Python (`pyproject.toml`) | `"pkg>=x.y.z,<X+1"` (not `~=x.y`, which anchors the minor) | `uv.lock` / `poetry.lock` / pip-compile output | `pip index versions pkg` · `https://pypi.org/pypi/pkg/json` → `info.version` |
| Python (`requirements.txt`, no lock tool) | `pkg==x.y.z` (the file *is* the lock) | itself; say in the PR that a lock tool is the real fix | as above |
| Go | `go get pkg@latest` (module path carries the major: `/v2`) | `go.sum`; `go.mod` records the exact version | `go list -m -versions pkg` · `https://proxy.golang.org/pkg/@latest` |
| Rust | `pkg = "x.y.z"` (Cargo's implicit caret) | `Cargo.lock` | `cargo search pkg --limit 1` · `https://crates.io/api/v1/crates/pkg` |
| Terraform provider | `version = "~> X.Y"` (≥ X.Y, < X+1) | `.terraform.lock.hcl` (+ `terraform providers lock -platform=…` for every platform CI uses) | `https://registry.terraform.io/v1/providers/ns/type/versions` |
| Terraform CLI | `required_version = ">= x.y, < X+1"` | n/a | `https://api.github.com/repos/hashicorp/terraform/releases/latest` |
| Terraform module | registry: `version = "~> X.Y"`; git: `?ref=vx.y.z` | `.terraform.lock.hcl` does not cover modules; the tag is the pin | registry `/versions` · `gh api repos/o/r/releases/latest` |
| Container image | `image:<tag>@sha256:<digest>` where the tag is the newest stable major/minor line (`python:3.13-slim`, `node:24-alpine`) | the digest is the lock | `docker buildx imagetools inspect image:tag --format '{{.Manifest.Digest}}'` · registry tags API |
| GitHub Action | `uses: owner/repo@vN` (major tag of the latest release); full SHA when the repo's policy says so | n/a | `gh api repos/owner/repo/releases/latest --jq .tag_name` |
| Helm chart in GitOps (`targetRevision`) | exact `x.y.z` (a range here is an unreviewed deploy) | the pin is the lock | `helm search repo repo/chart --versions \| head` · the repo's `index.yaml` |
| pre-commit hook | `rev: vx.y.z` exact (pre-commit requires it) | the rev is the lock | `gh api repos/o/r/releases/latest` |
| Runtime (`engines.node`, `.nvmrc`, `requires-python`, `go` directive, CI `*-version`) | newest *supported* line, not newest release: Node's current Active LTS (a Current release may be days from LTS and still lacks ecosystem support), Python's latest stable minor | n/a | `https://endoflife.date/api/v1/products/<product>` (`isLts`, `isMaintained`) |

"Latest stable" means the newest release that is not a pre-release (`rc`, `alpha`, `beta`, `dev`,
`nightly`, `canary`), not yanked and not deprecated. A `latest` dist-tag or a GitHub "latest
release" is usually that, but check the name before copying it; registries do occasionally tag a
pre-release.

## Watch what the package manager writes for you

`npm install pkg` and `cargo add pkg` write the anchor this standard wants. `uv add pkg` and
`poetry add pkg` do not: they write `pkg>=x.y.z` with no ceiling, so a future major arrives on the
next lock refresh. Pass the shape explicitly (`uv add 'pkg>=x.y.z,<N+1'`) or edit the manifest after
the tool runs, then re-lock. `pip install pkg` writes nothing at all. For Node runtimes, prefer the
Active LTS line over a newer Current release even when the machine runs Current: native modules and
`engines` ranges across the ecosystem catch up with LTS first, so LTS is the line least likely to
hand you an incompatible dependency.

## Why a major anchor and not exact, or not a bare range

Exact pins in the manifest turn every patch into a manifest edit and push teams toward never
updating. A bare `*` or `>=x` lets a breaking major arrive silently. The major anchor is the
middle: security patches and minors arrive on the next `install`, a major is a deliberate change
that goes through `dependency-upgrades`. The lockfile makes the build reproducible regardless, which
is why it is committed for applications and services. (Libraries keep the anchor and usually ship
no lockfile; that is intentional, say so in the README.)

GitOps manifests, pre-commit revs and image digests are the exceptions where exact is the standard:
nothing resolves them at install time, so a range there would mean a deploy nobody reviewed.

## Steps

1. Name the ecosystem and the manifest the new entry belongs in. If the project already declares
   the same package somewhere (another workspace, a lock, a Dockerfile), match that line rather than
   introducing a second version.
2. Look it up. Run the command or fetch the endpoint from the table for every package you are about
   to add, including dev tools, plugins and transitive pins you are asked to hold. Do not round,
   guess or reuse a number you remember. Without a shell (Cowork, claude.ai), fetch the HTTP endpoint;
   if that is unavailable too, ask the user to paste the registry output and say that the version
   is unverified until then.
3. Check the floor the project sets. A latest major that needs a newer runtime than the project
   declares (`engines`, `requires-python`, the base image, the cluster version) is not usable yet:
   take the newest version that fits, and write one line in the commit or PR saying which version
   was passed over and what raises the floor. `dependency-upgrades:upgrade-research` owns finding
   that ceiling when it is not obvious. If an *existing* pin already contradicts the declared floor
   (a dev tool that dropped the project's oldest runtime), say so in the PR rather than raising the
   floor to make the resolver happy; the smallest honest fix is a marker-gated pin for the old
   runtime (`pytest>=8.4.2,<9; python_version < '3.10'`) beside the current one, and the floor
   itself is a decision for the project, not for a dependency bump.
4. Write the anchor in the shape from the table, then let the package manager produce the lockfile
   (`npm install`, `uv lock`, `cargo generate-lockfile`, `terraform init`). Never hand-edit a
   lockfile; a hand-edited lock is a file no future install reproduces.
5. Commit the manifest and lockfile together, and record the lookup in the message body:
   `express ^5.2.1 (npm latest on 2026-10-09)`. The date is what lets the next reader tell a
   deliberate older pin from a stale one.

## Reviewing a diff that adds dependencies

For each new entry, check in this order: the version equals the registry's latest stable today
(look it up, do not trust the PR text); the shape is the table's anchor for that ecosystem; the
lockfile changed in the same diff; images carry a digest; nothing says `latest`, `main` or `*`.
Report a stale version as a finding with the current number in it, and an unanchored or
hand-edited lockfile as a convention finding. A deliberate older version with its reason written
down is not a finding.

## Verify

Before saying the change is done, list every version you wrote with the lookup that produced it:

```
express        ^5.2.1        npm view express version        -> 5.2.1   2026-10-09
python:3.13-slim@sha256:7072… imagetools inspect              -> same    2026-10-09
```

A line with no lookup beside it is a guess; go back to step 2 for it. Then confirm the lockfile is
tracked and up to date (`git status` shows it modified alongside the manifest, and the resolver
runs clean against it).
