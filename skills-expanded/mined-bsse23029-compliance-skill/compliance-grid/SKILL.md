---
name: compliance-grid
description: Builds and refreshes the compliance grids in compliance/grids/ — one per surface (frontend, backend, CI/CD) — mapping every module to the sources that govern it and our verified status against each. Use when asked for the compliance grid, a gap analysis, a module × standard matrix, or a refresh of an existing grid.
---

# Compliance grid

The deliverable: **three separate grids**, never one merged table.

- `compliance/grids/frontend.md`
- `compliance/grids/backend.md`
- `compliance/grids/cicd.md`

Plus `compliance/grids/summary.md` — counts and the top gaps across all three, generated last.

A module appears in the grid of every surface it exists on. "Guest identity capture" is a frontend
row (what the browser holds, consent, masking) *and* a backend row (storage, encryption, retention,
disclosure to Shomoos). Same module, different obligations, different verdicts.

## Row shape

| Column | Content |
|---|---|
| **Module** | Stable name from `compliance/modules/<surface>.yaml` |
| **Path** | Real repo path — `backend/Src/Apis/ProjectSpecificApis/BookingUsers/`, clickable |
| **Data classes** | What personal/financial data it touches: `identity-doc`, `guest-pii`, `payment`, `credential`, `audit`, `none` |
| **Source** | One or more registry ids. **Multiple sources per module is normal** — a folio row cites `SA-ZATCA-EINV-REG`, `SA-VAT`, `PCI-DSS` and `SA-PDPL-IR` at once |
| **Requirement** | The specific obligation, one line, in engineering terms — not the name of the standard |
| **Status** | See vocabulary below |
| **Evidence** | `file.js:line` for compliant/partial rows, or the search that found nothing |
| **Gap** | What is missing, concretely. Empty when compliant |
| **Effort** | `S` / `M` / `L` — rough, for sequencing only |

## Status vocabulary — use exactly these

| Status | Means | Evidence required |
|---|---|---|
| `compliant` | Verified in the code, with a file reference | Yes — file:line |
| `partial` | Mechanism exists but incomplete or inconsistently applied | Yes — plus what is missing |
| `gap` | Requirement applies, nothing implements it | The negative search performed |
| `n/a` | Requirement genuinely does not apply | The reason, always |
| `unknown` | Not yet examined | Nothing — but it must not stay `unknown` after a full pass |
| `unverified-source` | We are unsure the requirement itself is current | Registry entry with `confidence: low` |

`compliant` is a claim about evidence, not a hope. If the check was "I did not find anything wrong",
that is `unknown`, not `compliant`.

## Method

1. Run `compliance-router` first. A grid built without a scope statement is noise.
2. Load `compliance/modules/<surface>.yaml` for the module inventory. If it is stale, refresh it
   from the repo before grading anything.
3. For each module, ask which registry sources have that surface in `applies_to` **and** actually
   bear on what the module does. Do not paste all 56 ids into every row.
4. Grade each requirement against the code. Read the file. A grid graded from directory names is
   worse than no grid, because it looks like it was checked.
5. Cite the registry id, never a bare standard name.
6. Order rows within a grid by risk: identity documents and payments first, then auth/tenancy,
   then everything else.

## Two id namespaces — do not mix them

- **Registry ids** (`SA-PDPL-IR`, `PCI-DSS`, `OWASP-ASVS`) identify a *source*. They live in
  `compliance/sources/REGISTRY.yaml` and go in the **Source** column.
- **Control ids** (`PDPL-04`, `NCA-03`, `PCI-05`, `B-01`, `F-07`, `C-02`) are defined inside the
  individual skills and identify a *requirement*. They belong in the **Requirement** column.

A complete row carries both: which document says so, and which control within it.

## Rules that keep the grid useful

- **One requirement per row.** "Encryption" is not a row; "passport scans encrypted at rest in S3"
  is a row and "TLS enforced between container and MySQL" is another.
- **Never grade two surfaces in one row.** If the answer differs per surface, it is two rows in two
  files.
- **Pruning is expected.** The registry is deliberately broad — HIPAA, ISO 26262 and ISO 13485 are
  listed so the `n/a` decision is recorded once with a reason instead of being re-argued. Keep the
  `n/a` rows; delete nothing silently.
- **Date the grid.** Header carries the generation date, the HEAD commit, and the registry version
  it was built against.
- **Unknowns are findings.** A grid that is 40% `unknown` and says so is more useful than one that
  quietly rounds up to `compliant`.

## Header block for each grid file

```
# <Surface> compliance grid
Generated: YYYY-MM-DD · Commit: <short-sha> · Registry version: <n>
Scope: <jurisdictions in scope, from compliance-router>
Rows: <n> · compliant <n> · partial <n> · gap <n> · n/a <n> · unknown <n>
```

Then the table, then a **Sources used** appendix listing each registry id cited with its title and
URL, so the grid is readable standalone by someone who does not have the registry open.
