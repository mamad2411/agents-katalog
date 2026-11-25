---
name: yolo-intake
description: Use when a feature should draw on the project's reference material for context. yolo-intake does NOT fetch, import, or copy anything — it points YOLO at a selected folder (default `docs/`) and READS from it to enrich a feature's context. Getting material INTO that folder (a Figma, a spec, a URL, a schema) is the docs engine's or another connector's job, done separately. Triggers on "use the docs as context", "reference the spec/schema in docs", "the feature should read our docs".
---

# yolo-intake

**Intake is context enrichment, not fetching.** yolo never fetches, imports, or copies external
material. It simply **references a selected folder** — by default the project's **`docs/`** — and
**reads** from it to enrich a feature's context. Populating that folder (pulling in a Figma, a spec,
a URL, a DB schema) is the job of the **docs engine or another connector**, done separately and
outside yolo. yolo only reads what's already there.

## The selected folder
- The intake folder is `intake.folder` in `workspace/config.yaml` — **default `docs/`**. Point it at
  a different folder only if your reference material lives elsewhere.
- Whatever is in that folder is YOLO's context shelf. YOLO **reads** it; it never puts things there.

## Procedure
1. Resolve the intake folder from `workspace/config.yaml` (`intake.folder`, default `docs/`).
2. **Read** the relevant material from it for the feature — search the docs engine first, then read
   the specific files. **Never fetch a live source.** If needed context isn't in the folder, say so
   (a connector / docs-engine step must add it first) rather than fetching it yourself.
3. A feature brief points at the specific files it relies on via its `intake_refs` list — **paths
   under the intake folder** (e.g. `docs/explanation/payments-spec.md`).

## Constraints
- **Never fetch or import.** No WebFetch, no MCP fetch, no CLI pull, no copying into the workspace.
  Intake is strictly read-only over the selected folder.
- One folder, one source of context — don't scatter reference material across the workspace.
- If required context is missing from the folder, **surface the gap**; adding it is a connector /
  docs-engine concern, outside yolo.
