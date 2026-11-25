---
name: dependency-health
version: 1.0.0
description: Evaluating, auditing, and upgrading third-party dependencies and runtime versions — add/avoid decisions, vulnerability and reachability triage, maintenance-health signals, changelog reading, and safe major-version jumps. Load before adding a dependency, when auditing existing ones, or when planning a version bump. Do NOT use for build/publish pipeline integrity, artifact signing, or registry-level compromise (typosquatting, maintainer takeover) — that is `supply-chain-security`.
---

# Dependency Health

## Before adding a dependency

Check first whether the standard library or an existing project dependency already solves the problem. Every dependency added is long-term maintenance the team now owns indirectly — weigh: maintenance health (recent commits, responsive maintainers, issue backlog), security history (past CVEs, how fast they were patched), bundle/footprint size, license compatibility, and how hard it would be to replace later.

Check license compatibility with the project's own licensing/distribution model before adding anything — a permissive-looking package can have a copyleft transitive dependency.

## Auditing what's already there

Run the ecosystem's audit tool regularly, not just when prompted. Detect which one applies the same way `qa-tooling` detects a test runner — from the manifest and lockfile actually present (`npm audit`, `pip-audit`, `bundler-audit`, `cargo audit`, language-native equivalent). If no audit tooling is detected, say so rather than assuming the dependency surface is clean.

Distinguish a vulnerability that's actually reachable in this codebase's usage from one in an unused code path of the dependency — reachability changes urgency. But an unreachable-today vulnerability can become reachable after an unrelated change, so "unreachable" is a priority call, not a dismissal.

If a dependency is confirmed unused, remove it rather than leaving it as latent attack surface and audit noise.

## Upgrade cadence

A steady cadence of small version bumps is far safer than a rare large jump — small bumps bundle fewer breaking changes together, so when something regresses it's much easier to isolate which change caused it. Rare large upgrades are the expensive default most projects drift into.

## Before any bump

Read the changelog/release notes for **the actual version range being crossed**, not just the latest entry — a multi-version jump can cross several breaking changes that only appear in the cumulative changelog. Never bump a major version because a bot opened a PR without reading what changed.

## Testing the upgrade

Run the full existing suite **plus** a targeted check of the areas the changelog's breaking-change notes point at. An upgrade that passes CI but was never checked against the specific behavior that changed is a false sense of safety — the suite only covers what someone already thought to test, which by definition excludes newly-changed behavior.

## Major version jumps

Budget real time: deprecated API removal, changed defaults, and altered error behavior are all common. Consider an intermediate version stop if the changelog shows a cleaner deprecation path through it, rather than jumping straight to the newest major.

## Runtime and language version upgrades

Same rigor, broader blast radius. Check for behavior changes in the standard library and language semantics, not just third-party packages — and validate on the actual deployment target, not only a local dev environment, since runtime differences between the two are exactly what this class of upgrade exposes.

## Boundary

This skill covers the dependencies themselves. Risk arising from the *supply chain* around them — build provenance, artifact signing, pipeline hardening, registry-level compromise, SBOM — is `supply-chain-security`. A CVE in a package you depend on is here; a maintainer account takeover that published a malicious version is there.
