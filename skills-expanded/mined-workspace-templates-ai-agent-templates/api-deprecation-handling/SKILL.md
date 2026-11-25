---
name: api-deprecation-handling
description: "Deprecates a public function or endpoint the careful way: replacement first, runtime warnings, docs, a migration note and a dated removal plan."
---

# API deprecation handling

Never remove in the same release that introduces the replacement.

## Steps

1. Define the change: what is old, what replaces it, and who calls it. Search the repo (`grep` or symbol search) for internal callers and list them. For public APIs, check logs or metrics for external use if available.
2. Confirm the replacement exists, has tests and covers every use case of the old API. If it does not, stop and report the gap.
3. Mark the old API in the language's own way: `@deprecated` JSDoc, `warnings.warn(..., DeprecationWarning)`, `#[deprecated]`, `[Obsolete]`. For HTTP, add `Deprecation` and `Sunset` headers and a `Link` header pointing at the migration doc.
4. Keep behavior identical. The old path may delegate to the new one, which also removes duplicate logic.
5. Emit the warning once per process or per caller, with the replacement name and the removal version or date in the message. Do not flood the logs.
6. Migrate all internal callers to the replacement in the same change. Check that no internal code triggers the warning.
7. Write a migration note: before and after code, differences in behavior, and the removal date. Add it to the changelog and the docs page for the old API.
8. Add a test that the warning fires, and a calendar note or issue for the removal, listing the files to delete.

## Rules

- Choose the removal date at least one release cycle out, longer for public APIs.
- Do not rename or change arguments of the old API during the deprecation period.

## Report

Files changed, internal callers migrated, the exact warning text, removal date and the issue link or text for the removal task.
