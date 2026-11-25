---
name: semwright-project-continuity
description: Use when continuing a native creative project, identifying resources, reconciling drift, explaining dependencies, or deciding whether an output may be reused through authorized Project Graph routes.
---

# Project continuity

First discover available capabilities and describe the exact operation before using it. The requirements bind the actual discovery and `project.*` catalog entries; the examples validate schemas only and never grant permission or execute project operations.

**Current integration boundary:** this source registers bounded `project.*` core routes for project creation, logical file registration, inspect/reconcile/rebind, scoped query/impact/revisions, declarative edges and portable manifests. Runtime availability still requires daemon host configuration, an OS-derived durable user principal and the named filesystem read grant; catalog availability is never permission. There is no public receipt-admission route, no hidden database-write escape and no arbitrary rebuild execution capability. Native D/E/A/B adapters remain separate acceptance gates.

After discovering and describing the required routes, follow this sequence:

1. Register or discover the logical resource under an explicit project/root grant. Do not equate a path, matching name, digest or old session ref with persistent identity.
2. Reconcile through the authorized native observer. Reacquire current refs and record observation scope/time, base, generation, digest method and unknown dependencies. Report “current according to the last reconcile” separately from “verified now.”
3. Inspect the resource and its provenance before impact: `project.asset.provenance` reports the active visible producer, exact visible inputs, bounded known/possible direct derivatives and typed stale/unknown reasons. Treat `truncated` as incomplete returned derivative coverage and `unknown_frontier` as unresolved visibility/evidence; neither means independence. Then use impact for transitive consequences.
4. If the installed catalog exposes an authorized typed rebuild-planning route, review its blockers and current bindings before preparation. If it does not, report that gap and stop there. Never substitute shell automation, treat a proposal as a grant, overwrite divergence implicitly or create another scheduler.
5. Verify required output predicates using the same base/artifact, persist actual receipts and refresh knowledge. Preserve required UNKNOWN/FAIL. Do not infer success from a saved filename or successful store tests.
6. Cleanup is optional and graph-private. Preview with `project.gc.preview`, then collect only the exact returned tombstoned IDs if appropriate. `project.gc.collect` never authorizes deleting source/output files; an asset with revisions, receipts, edges or intents is deliberately ineligible.

See [states](references/states.md). This Skill never promises silent synchronization or work in the background.
