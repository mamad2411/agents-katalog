---
name: ubiquitous-components-fetch
description: Fetch the globally shared Rune components catalog published by `$ubiquitous-components` and copy it into the current workspace for local context use. Use when a project needs the shared Rune component inventory before UI planning or implementation, or when an implementation protocol requests the catalog. Do not use to build or refresh the catalog itself; use `$ubiquitous-components` for that.
disable-model-invocation: true
---

# Ubiquitous Components Fetch

## Outcome

The globally shared Rune catalog is available inside the current workspace, by default at `docs/UBIQUITOUS_COMPONENTS_GLOBAL.md`, with its source path, freshness, and size reported.

## Inputs and preconditions

A published global catalog. The source path resolves from the shared home chain, `$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`:

- `<shared-home>/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`

If the file is missing, this skill cannot proceed; see failure handling.

## Workflow

1. Resolve the global source path from the chain above and validate that the file exists.
2. Copy it into the current workspace (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/fetch_global_ubiquitous_components.py --workspace <repo-root>
   ```

   Common variants:

   ```bash
   python3 <skill-dir>/scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --output docs/UBIQUITOUS_COMPONENTS_GLOBAL.md
   python3 <skill-dir>/scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --global-input <absolute-global-path>
   python3 <skill-dir>/scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --read-only
   ```

3. Return the summary defined in the output contract.

## Constraints

- Default local output path is `docs/UBIQUITOUS_COMPONENTS_GLOBAL.md`.
- In `--read-only` mode, do not write files; only print source path and size.
- Keep behavior deterministic and idempotent: fetching twice with the same source produces the same local file.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$ubiquitous-components` (producer side) | Never invoked by this skill; recommend it to the user when the global catalog is missing | — | A freshly published global catalog | The consumer project proceeds without the shared catalog and reports the limitation |
</interface>

Both skills resolve the shared home with the same chain (`$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`); changing the chain on one side without the other breaks the exchange.

## Failure handling

- The global file is missing: fail with a clear error message showing the expected resolved path, and recommend running `$ubiquitous-components` in any Rune-capable project first to publish it. Do not fabricate a catalog.
- The metadata file is missing but the catalog exists: fetch the catalog and report that the `generated_at` timestamp is unavailable.

## Output contract

Return a concise summary reporting:

- global source path used
- global `generated_at` timestamp when metadata is present
- local destination path written (if any)
- line/byte size of the fetched file
