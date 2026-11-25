---
name: audit-algorithmic-complexity
description: Algorithmic complexity and data-structure checklist. Use when code searches, joins, or dedupes collections in memory — linear lookups inside loops instead of a hash map or set, hidden O(n²) copies, binary search on unsorted data or with a mismatched comparator, broken hash keys or equality.
---

Read `../audit/references/operability/algorithmic-complexity.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
