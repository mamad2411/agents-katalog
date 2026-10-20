---
name: gep-environment-fingerprint
description: Compute and persist environment fingerprint for drift detection and state validation
category: architecture
version: 1.0.0
version_origin: extracted
confidence: high
tags: [evolver, architecture, fingerprint, drift-detection]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/gep/envFingerprint.js
  - src/proxy/lifecycle/manager.js
imported_at: 2026-04-18T00:00:00Z
---

# Environment fingerprint for drift detection

Track the environment (OS, Node version, working directory, git state, etc.) and detect when critical state has drifted. Useful for any agent system needing to validate that persisted evolution / cache / state artifacts still apply to the current environment without silent failures.

## Mechanism

1. At boot, collect a stable subset of environment facts: `process.platform`, `process.version`, repo root path, `git rev-parse HEAD`, branch name, presence of key files.
2. Hash the tuple (e.g., sha256 over a canonical JSON encoding) → fingerprint.
3. Persist fingerprint alongside state artifacts.
4. On each cycle, recompute and compare. If it differs, treat persisted state as invalid: refuse to continue, clear caches, or prompt human review.

## When to reuse

- Agents or daemons with long-lived state that shouldn't be replayed across branches/repos.
- Caching layers that must invalidate on Node upgrade or path move.
- Any workflow that applies previously-recorded decisions to the current tree.
