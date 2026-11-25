---
name: materials-project
description: Query Materials Project records, inspect structures and phase data, and export sourced results with OmniScholar. Use for materials screening, property retrieval, phase analysis, XRD capability checks, or JSON/CSV/Markdown/CIF export.
license: MIT
---

# Materials Project

Follow the user's language. Keep calculated Materials Project records separate from literature evidence and experimental measurements.

1. Call `materials_capabilities` before choosing an operation. Credentials do not guarantee every field or optional local calculation.
2. Translate conditions into supported `materials_search` filters. Distinguish containing elements from an exact chemical system; bound pages, results, and fields.
3. Use `materials_route_search` when the requested collection has route-specific keys or filters. Do not substitute a material ID for a task ID, chemsys, substrate pair, or other declared parameter.
4. Use `materials_get` for a verified material ID and route. Preserve missing-field reasons.
5. Use `materials_advanced` only for the declared `phase_diagram` or `xrd` actions. `xrd` must remain `local_backend_required` when that backend is unavailable; never guess a remote endpoint or fabricate a pattern.
6. Use `materials_export` only on already retrieved records. Keep provenance, units, API/database version, warnings, and license data. CIF export writes a bounded P1 representation from validated structure data and does not claim a derived space group.
7. Compare records only after checking units, calculation method, task identity, structure, and corrections. Equal formulas do not imply equal structures, and calculated stability does not prove experimental synthesizability.

Read [failures.md](references/failures.md) for failure handling. If Materials Project is not configured, report the required key and do not silently replace calculated materials data with literature snippets or CAS substance data.
