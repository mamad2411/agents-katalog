---
name: ultimate-nixos
description: Guides Nixpkgs maintainers and committers on PR workflow, OfBorg, nixpkgs-review, merge bot, r-ryantm autoupdates, CI, staging branches, and how nix-darwin and Home Manager relate to nixpkgs. Use when reviewing or merging nixpkgs PRs, triaging CI, advising on bot commands, mass rebuilds, backports, or consumer Nix config (flakes, overlays) alongside nixpkgs changes.
---

# Nixpkgs maintainer and committer workflow

This skill summarizes rules and workflows for people who maintain packages in [Nixpkgs](https://github.com/NixOS/nixpkgs) or hold commit access. It mirrors the structure of community skills like [nixos-best-practices on skills.sh](https://skills.sh/lihaoze123/my-skills/nixos-best-practices): read the references before guessing, then act.

## Read before you change things

When working inside a nixpkgs checkout, prefer authoritative in-tree docs:

| Topic | Location |
| --- | --- |
| General contribution flow | [CONTRIBUTING.md](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md) |
| Maintainer role, merge bot summary, committer cautions | [maintainers/README.md](https://github.com/NixOS/nixpkgs/blob/master/maintainers/README.md) |
| Package layout, tests, conventions | [pkgs/README.md](https://github.com/NixOS/nixpkgs/blob/master/pkgs/README.md) |
| CI layout, merge bot rules, branch classes, `nixpkgs-vet` | [ci/README.md](https://github.com/NixOS/nixpkgs/blob/master/ci/README.md) |
| PR checklist | [.github/PULL_REQUEST_TEMPLATE.md](https://github.com/NixOS/nixpkgs/blob/master/.github/PULL_REQUEST_TEMPLATE.md) |
| Critical packages (extra care) | [ci/OWNERS](https://github.com/NixOS/nixpkgs/blob/master/ci/OWNERS) |

For extra links (OfBorg, nixpkgs-review, bots, nix-darwin, Home Manager), see [reference.md](reference.md).

## Red flags (stop and verify)

- Guessing attribute names, option names, or OfBorg behavior instead of checking docs or running a local eval.
- Pushing untested changes that can break Nixpkgs evaluation (breaks OfBorg for many PRs and Hydra). Prefer waiting for successful OfBorg evaluation and using local review tools.
- Targeting the wrong branch (mass rebuild on `master`, or backport to a channel branch).
- Using `@ofborg build` with prose on the same line (parser is line-based; only words after the command on that line are attrs).
- Assuming Draft PRs skip OfBorg automatic builds (they do not; `WIP:` / `[WIP]` in the PR title does).

## Branches (decision summary)

- Default: `master` for most changes.
- **Mass rebuilds**: if rebuild count is ~500+, consider `staging` instead of `master`; ~1000+ is treated as mass rebuild -> `staging`. Kernel changes and "rebuild all NixOS tests" cases follow special rules (see CONTRIBUTING staging sections).
- **Backports**: base branch `release-YY.MM`, not `nixos-YY.MM` (channel branch).
- **Channel branches** (`nixos-*`, `nixpkgs-*`): not for PRs.

Full diagrams and staging/staging-next flow: CONTRIBUTING.md "Staging".

## Commit messages

- One logical change per commit; squash fixups like whitespace-only follow-ups.
- No period at end of the subject line.
- `maintainers: add <handle>` in its own commit before package commits.
- Area-specific rules: see commit convention sections in `doc/README.md`, `lib/README.md`, `nixos/README.md`, `pkgs/README.md`.

**OfBorg automatic builds** key off the commit subject: prefix with the package attribute (e.g. `vim: 1.0.0 -> 2.0.0` triggers `vim`). Multiple packages in one subject can trigger multiple attrs. See [OfBorg README](https://github.com/NixOS/ofborg/blob/master/README.md) for the table of examples.

## OfBorg (CI builder)

- Lines that trigger the bot **must start with** `@ofborg` (case insensitive). GitHub may not autocomplete it; confirm it links to the ofborg user.
- `@ofborg build attr1 attr2` -> `nix-build ./default.nix -A ...` for each attr.
- `@ofborg test test1 test2` -> `nixosTests.test1`, etc.
- `@ofborg eval` is rarely needed (eval runs on PR open/update).
- Be careful not to fire mass rebuilds or huge builds (e.g. browsers) without need. Review the PR before asking the bot to build.

## nixpkgs-review

Use to build dependents and catch breakage before or alongside OfBorg:

```bash
nix-shell -p nixpkgs-review --run "nixpkgs-review pr <PR_NUMBER>"
# or
nix run nixpkgs#nixpkgs-review -- pr <PR_NUMBER>
```

Other modes: `nixpkgs-review wip` (uncommitted), `nixpkgs-review rev HEAD` (last commit). Upstream usage: [Mic92/nixpkgs-review](https://github.com/Mic92/nixpkgs-review).

## GitHub Actions and local vet

- "PR / ..." required checks are separate from OfBorg; merge bot text in CONTRIBUTING notes that OfBorg is not always a required check.
- To approximate CI evaluation locally: `ci/nixpkgs-vet.sh <BASE_BRANCH>` (see ci/README.md).

## nixpkgs-merge-bot

Maintainers can comment:

```text
@NixOS/nixpkgs-merge-bot merge
```

**Constraints (summary)** from ci/README.md:

- Target branch must be an allowed development branch.
- Diff only touches `pkgs/by-name/*` package files.
- PR author is committer, or backport label path, or [@r-ryantm](https://github.com/r-ryantm), or committer-approved (see full list in ci/README.md).
- Commenter is in [@NixOS/nixpkgs-maintainers](https://github.com/orgs/NixOS/teams/nixpkgs-maintainers) and is maintainer of **all** touched packages.

The bot waits for OfBorg checks except Darwin. Exact policy can evolve; always read [ci/README.md](https://github.com/NixOS/nixpkgs/blob/master/ci/README.md) when in doubt.

## r-ryantm and nixpkgs-update

- [@r-ryantm](https://github.com/r-ryantm) opens version-bump PRs via [nixpkgs-update](https://nix-community.github.io/nixpkgs-update/) infrastructure.
- Logs and tooling for maintainers: see [maintainers/README.md "Tools for maintainers"](https://github.com/NixOS/nixpkgs/blob/master/maintainers/README.md) (e.g. log sites, notifiers).
- Merge bot is often used to merge clean bot PRs for `pkgs/by-name` when maintainers approve.

## Review and merge norms

- Non-blocking feedback is default; **blocking** feedback must use GitHub "Request changes".
- Give maintainers time: roughly **one week** before merging changes they have not endorsed, except critical/security paths or packages listed in ci/OWNERS (negotiate with maintainer).
- Prefer conventional comments for optional follow-ups so they are not implicit blockers.
- Committers may push small fixes to contributor branches when allowed; warn that `gh pr checkout` branches need care with force-push (see CONTRIBUTING).

## NixOS tests

- Declared in `nixos/tests`. Invoked locally per NixOS manual; OfBorg: `@ofborg test driverTestName`.
- Linux-only for full VM tests.

## nix-darwin and Home Manager (scope boundary)

These are **not** part of the nixpkgs tree; they consume Nixpkgs as an input.

- **nix-darwin**: macOS system configuration (modules, `darwin-rebuild`). Flake-first workflow and `darwinSystem` are documented in the [nix-darwin README](https://github.com/nix-darwin/nix-darwin?tab=readme-ov-file#readme). Use `nixpkgs.hostPlatform` `x86_64-darwin` or `aarch64-darwin` as appropriate.
- **Home Manager**: user environment on NixOS, nix-darwin, or standalone. When `useGlobalPkgs = true`, overlays belong in the **host** system configuration that instantiates Home Manager, not only inside `home.nix` (overlays in `home.nix` are ignored for that mode). Same core idea as the overlay matrix in [nixos-best-practices](https://skills.sh/lihaoze123/my-skills/nixos-best-practices).

When triaging issues: distinguish **packaging bugs** (fix in nixpkgs) from **consumer config** (flake layout, overlay scope, module options in HM/nix-darwin).

## Quick task map

| Task | Where to look |
| --- | --- |
| Should this target staging? | CONTRIBUTING mass rebuild / rebuild labels |
| Why did OfBorg not build? | Commit subject format, WIP in PR title |
| Maintainer merge of by-name PR | Merge bot comment + ci/README constraints |
| Local CI-ish check | `ci/nixpkgs-vet.sh` |
| Bot bump PR | r-ryantm; review like any bump; check changelog link |
| Backport | Label on master PR or manual cherry-pick to `release-YY.MM` |

---

If the user is only configuring a personal machine (no nixpkgs PR), still use overlay scope rules above; deep NixOS flake structure is better covered by dedicated consumer skills such as [nixos-best-practices](https://skills.sh/lihaoze123/my-skills/nixos-best-practices).
