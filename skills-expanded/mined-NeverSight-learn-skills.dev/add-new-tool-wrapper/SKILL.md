---
name: add-new-tool-wrapper
description: Skill for add-new-tool-wrapper
---

# add-new-tool-wrapper

Purpose: add a tool integration without architectural drift.

## Procedure

1. Add catalog entry in `tools/registry/tool_registry.yaml`.
   - include category, execution mode, verification command, input/output schema, retries, safety class
2. Decide wrapper strategy.
   - generic CLI path: use `CatalogBackedCLITool`
   - specialized parser path: extend `apps/backend/src/core/tool_adapters_bugbounty.py`
3. Register safely.
   - ensure `register_bugbounty_tools()` picks up the tool id
   - map aliases only when preserving existing API behavior
4. Add normalization support in `workflow_normalizer.py` if tool output introduces new shapes.
5. Add tests.
   - adapter execution test
   - parse behavior test
   - timeout/error test
6. Update docs.
   - `docs/tools.md`
   - `docs/workflows.md` if used in templates

## Guardrails

- no shell-string execution
- no silent success on missing binaries
- evidence/provenance fields must be populated
