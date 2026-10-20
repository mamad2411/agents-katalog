---
name: publication-review
description: Validates a manuscript before publication: seven checks (conformity, continuity, promises, research, representation, correction, book apparatus), technical file checks, a written decision and a publication dossier. Run at the very end of the process.
license: MIT
metadata:
  category: quality
  version: 2.0.0
  depends_on: [writing-constitution, continuity-manager, proofreader]
  outputs: [validation-report, publication-decision]
---

# Publication Review

Final validation before publication. This skill does not judge literary
quality, already handled by `literary-critic`: it verifies that no objective
defect remains, and issues a decision.

## 1. Position in the process

This skill runs last, after `literary-editor`, `proofreader` and
`continuity-manager`. It changes nothing. It validates, or it sends the text
back with a closed list of corrections.

## 2. The seven checks

### Check 1: constitution conformity
The full grid from
`core/writing-constitution/resources/grille-de-conformite.md`. A single
failure blocks.

### Check 2: continuity
The eight-pass audit report from `continuity-manager`, with no blocking or
major inconsistency.

### Check 3: promises
Every open promise is kept, or deliberately deferred to a following volume and
recorded as such.

### Check 4: research
Every level 3 assertion is backed by a source sheet. No unaccepted
anachronism.

### Check 5: representation
No culture, condition or community treated as scenery, caricature or
shortcut. Cross-checked against the relevant `beta-reader` profile.

### Check 6: correction
The `proofreader` log is closed, and doubtful cases have been decided by the
author.

### Check 7: book apparatus
Title, chapter titles, table of contents, epigraph, dedication, legal notices,
acknowledgements, consistency of names in the paratext.

## 3. Technical file checks

- UTF-8 encoding.
- No residual control characters.
- No double spaces, no trailing whitespace.
- Page breaks correct, one chapter per odd page where the edition requires it.
- Continuous numbering, no missing or duplicated chapter.
- Uniform styles: body, dialogue, italic, epigraph.

## 4. Decision

| Decision | Condition |
|---|---|
| Approved | the seven checks pass |
| Approved with reservations | minor points only, listed, to fix before printing |
| Returned | at least one blocking check failed |
| Suspended | doubt over research or representation requiring outside expertise |

The decision is written, dated, and accompanied by the exhaustive list of
remaining points. No verbal decision, no implicit approval.

## 5. Publication dossier

The delivered dossier contains:

1. the final manuscript;
2. the validation report;
3. the closed continuity register;
4. the research dossier;
5. the self-critique grids for the turning-point chapters;
6. the cut log and the rewrite log;
7. the list of accepted deviations.

This dossier is the memory of the book. It serves the next volume, the
adaptation, and any editorial dispute.

## 6. Auto-critique

Score 0 to 5: completeness of the checks, clarity of the decision, accuracy of
the remaining-points list, completeness of the dossier, absence of indulgent
approval.

Threshold: no axis below 4.

## 7. Interfaces

- Upstream: `literary-editor`, `proofreader`, `continuity-manager`,
  `literary-critic`, `beta-reader`.
- Downstream: publication.
