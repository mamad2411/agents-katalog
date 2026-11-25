---
name: mode-gated-reconcile-skip-filter
description: "Inject mode-specific skip rules into a shared reconciler so unsupported source types are recorded and skipped without forking the core install logic."
metadata:
  author: ychampion
---

# SKILL: Mode-Gated Reconcile Skip Filter
**Domain:** extensions-mcp  
**Trigger:** Apply when a shared reconcile engine runs in multiple runtime modes, but some modes cannot support every source type or transport.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Keep one shared reconcile pipeline, but let callers inject an optional skip predicate that reflects mode-specific capabilities. The reconciler still computes the full worklist, then filters unsupported items into a `skipped` result instead of misreporting them as failures or forcing wrappers to fork the install algorithm. That preserves a single source of truth for install/update behavior while allowing constrained runtimes to stay honest about what they cannot process.

## Key Rules
- Put capability checks behind an injected skip predicate rather than branching the whole reconcile implementation.
- Record skipped items explicitly so operators can distinguish "unsupported here" from true install failures.
- Apply the skip filter after the worklist is built so visibility into intended changes remains intact.
- Keep logging around skipped items; silent skipping hides portability gaps between modes.
- Preserve identical install/update semantics for supported items across all modes.

## Example Application
If a desktop agent can install extensions from local folders and remote archives but a serverless worker only supports archives, let the worker pass a skip predicate for local-folder sources. The shared reconciler still handles archives the same way, while skipped folder sources are reported cleanly instead of failing the whole run.

## Anti-Patterns (What NOT to do)
- Do not duplicate the entire reconciler per mode just to exclude a few unsupported source types.
- Do not treat unsupported sources as generic failures; that obscures whether the issue is capability mismatch or broken input.
