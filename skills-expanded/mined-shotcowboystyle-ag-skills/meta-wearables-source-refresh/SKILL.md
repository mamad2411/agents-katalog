---
name: meta-wearables-source-refresh
description: Refresh the Meta Wearables DAT, Web Apps, device, terms, and Apple integration knowledge base with exact official URLs, release/tag/commit, retrieval date, API migrations, access gaps, and evidence boundaries, including a portable public Git ref drift check. Use before version-sensitive implementation, after an SDK release, or when a device-generation claim may have drifted.
allowed-tools: Bash(python3 *), Read, Grep, Glob
---

# Meta Wearables source refresh

## Overview

Keep the knowledge base current without turning an inaccessible page, remembered API, or product announcement into an implementation fact.

## Read before acting

- Read [Meta source freshness](../meta-wearables-knowledge-base/references/sources/meta-wearables-source-freshness-log.md), [Meta source registry](../meta-wearables-knowledge-base/references/sources/meta-wearables-source-registry.md), and the Apple team’s [source provenance rules](https://github.com/shotcowboystyle/ios-ops-plugin/blob/main/.agent/skills/ios-source-refresh-and-availability/references/provenance-and-evidence.md).
- Inspect the current local package manifests, lockfiles, sample code, generated API docs, and existing source notes.
- Run `python3 scripts/check_source_revisions.py` from this package before interpreting the pinned iOS/Android/Web App refs as current; it checks public `main` refs and an exact iOS reproducible tag without cloning or printing credentials.
- Run `python3 scripts/check_source_tree_inventory.py` after the ref check; it reads the pinned public root `AGENTS.md`/`README.md`/`install-skills.sh` surfaces, lane `.codex-plugin/plugin.json` manifests, Package.swift, exact role names, sample catalogs, artifact catalogs, SDK levels, Web App references, examples, and templates, then fails on inventory drift without cloning or handling credentials. It prefers the public Contents API and falls back to a read-only codeload archive on unauthenticated rate limits. A clean current receipt is `CHECKS 23 DRIFT 0`.
- Run `python3 ../meta-wearables-agentic-team/scripts/validate_team_manifest.py` after role-tree changes; it verifies the 23 local role packages, all 32 upstream role handoffs, and the Ray-Ban Display/Gen 2/Gen 3 claim gates.
- Read the [full SDK capability and source-conflict matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/15-full-sdk-capability-and-source-conflict-matrix.md) before declaring module or capability coverage complete.
- Read the [DAT Android API surface atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md) when refreshing Android artifacts, symbols, or 0.9 migration notes.
- Read the [device-generation and runtime-support matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md) before resolving product labels, “Gen 3,” or model-enum claims.
- Read the [version-dependency and device-compatibility route](../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md) when refreshing firmware, companion/DAT-app, artifact, version-table, or compatibility claims.
- Read the [on-device compliance and runtime contract](../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) before updating processing-location, privacy, thermal, network, retention, or fallback claims.
- Read the [operational readiness and recovery route](../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) before updating firmware, companion, on-glasses DAT-app, version-dependency, Developer Mode, release-channel, known-issue, or recovery claims.
- Read the [application architecture and platform-boundaries route](../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) before changing shared state, adapter, concurrency, lifecycle, or cross-platform parity guidance.
- Read [Developer Center project and release operations](../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md) when the raw reference changes organization, project, version, channel, tester, telemetry, or recovery guidance.
- Read the [security, attestation, and credential-boundaries route](../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) when a source changes identity keys, callback/attestation semantics, package credentials, App Store/privacy-manifest requirements, Web App origin rules, or “on-device” claim boundaries.
- Read [transport, audio, and runtime reliability](../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) when a changelog, setup guide, artifact, audio route, local-network requirement, transport parity signal, thermal behavior, or recovery claim changes.
- Read [debugging, observability, and diagnostic evidence](../meta-wearables-knowledge-base/references/70-meta-wearables/23-debugging-observability-and-diagnostic-evidence.md) when upstream debugging roles, live MCP tools, event schemas, known issues, or diagnostic-bundle behavior changes.
- Read [input, sensors, and physical interaction](../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) when a Display/input/sensor source, browser API, physical interaction, processing-location, or device-generation claim changes.
- Refresh the official [DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios), [DAT Android repository](https://github.com/facebook/meta-wearables-dat-android), [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md), [full Wearables reference](https://wearables.developer.meta.com/llms.txt?full=true), [Web Apps repository](https://github.com/facebook/meta-wearables-webapp), [Developer Center](https://wearables.developer.meta.com/docs/develop/), [terms](https://wearables.developer.meta.com/docs/terms), and [acceptable use policy](https://wearables.developer.meta.com/docs/acceptable-use-policy).
- Record the access state of the Wearables docs, public MCP, and `llms.txt` endpoint separately. If a page requires login or cannot be fetched, record the gap; do not summarize its unseen contents.

## Fast path

Run the exact revision check and source-tree inventory first. If both are clean, emit a no-change receipt; if drift exists, compute impacted rows, routes, and packages, update only those, then rerun validators and archive parity.

## Required output

- updated registry entries;
- freshness log row;
- changed-API/migration table;
- source-to-role impact map;
- operational compatibility/recovery impact map and first-party/community source classification;
- exact URLs and commits;
- access and evidence gaps;
- validation commands/results.
- public-ref checker output, including every expected and observed revision.
- source-tree inventory checker output, including every expected and observed product, exact role name/list, role count, sample, artifact, SDK, reference, example, and template count/value.
- team-manifest validator output, including local role count, upstream handoff count, and device-claim gate count.

Further sections — read when the above is not enough: `references/details.md`.
