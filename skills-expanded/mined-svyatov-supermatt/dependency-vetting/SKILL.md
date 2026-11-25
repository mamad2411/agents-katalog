---
name: dependency-vetting
description: Verify a package or tool is authentic before installing, adding, upgrading, or recommending it. Use whenever a task would add a dependency to a project, suggest a CLI tool, or pull a package from npm, PyPI, crates.io, Go modules, RubyGems, Homebrew, or any other registry. Also use when a registry page, install command, or installed artifact looks inconsistent with the project that supposedly publishes it.
license: MIT
---

# Dependency vetting

The rule: never install, add, or recommend a package until you have opened the upstream project's own repo or docs and used the install command or import path published there. The sections below are the full reasoning behind it.

## Direction of trust

Follow the link **from the upstream project to the install command**. Never work the other direction, from a search result or a registry page back to a project.

Treat unverified registry metadata as publisher-supplied claims: author, email, homepage, repository link, README, and license. Where the registry independently verifies a field or attestation, check what that verification establishes and compare the verified identity with the intended upstream project. Still open the upstream repository or docs and confirm the published installation instructions.

If upstream documents no registry install, then there is no registry package, whatever the registry shows. Stop and say so. Do not install it, do not pin around it, and do not quietly swap in an alternative. Pinning untrusted code to a SHA is the same code with better bookkeeping, not a fix.

## Registry signals worth using

Use the registry's own independent signal where one exists:

| Registry | Signal |
|----------|--------|
| npm | `npm audit signatures` |
| PyPI | "Verified details" plus PEP 740 attestations |
| GitHub release binaries | `gh attestation verify` |
| crates.io, Go modules, most others | checksum only, so the upstream link carries all the weight |

Download counts, stars, and search ranking are not evidence of authenticity.

## Stop signals

Any mismatch between the installed artifact and upstream docs is a stop signal: a different executable name, version, file set, or dependency list. Confirm with the user. Never record it as a quirk and move on.

## Keep it proportionate

A tool a project genuinely publishes passes these checks in seconds, so this costs nothing in the normal case and fires only when something is actually wrong. Do not turn it into pin-everything ceremony.

Separately: do not add or suggest outdated dependencies. Check the current release before pinning a version.
