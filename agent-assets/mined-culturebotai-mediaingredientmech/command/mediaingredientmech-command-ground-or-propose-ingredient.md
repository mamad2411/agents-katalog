---
description: Deep-research the UNMAPPED ingredient residual; ground to an ingredient ontology first (CHEBI → FOODON → NCIT → cas:), and where no good term exists, mint a kgmicrobe.compound term. Coverage-maximizing, not match-forcing.
argument-hint: "[category SIMPLE_CHEMICAL|COMPLEX_MIXTURE|ENVIRONMENTAL|INCOMPLETE|PLACEHOLDER|UNKNOWN] [min-freq N | identifier UNMAPPED_NNNN | label \"...\"]  (default: all categories, min-freq 1)"
---

# Ground-or-propose residual ingredient terms (ingredient-ontology-first)

Goal: shrink MIM's **UNMAPPED ingredient residual** (`data/curated/unmapped_ingredients.yaml`,
~383 records). This is the ingredient analog of TraitMech's `/ground-or-propose-metpo`, but
the home layer is **chemical identity, not phenotype** — so it grounds to an ingredient
ontology (CHEBI → FOODON → NCIT → `cas:`), and "propose" means **mint a `kgmicrobe.compound:`**
custom term, *not* a METPO proposal. (METPO describes traits/conditions, never ingredient
identity; it has no role here.)

For **each unmapped ingredient**, decide: (a) ground to an existing ontology term, (b) ground
to a CAS Registry Number when that's the only definitive identifier, (c) mint a
`kgmicrobe.compound:` term when the compound is a real, distinct identity with no ontology
term anywhere, or (d) leave it UNMAPPED when its composition is genuinely variable/unknown.

`$ARGUMENTS` filters the worklist by category / frequency / identifier / label. Examples:
`/ground-or-propose-ingredient category SIMPLE_CHEMICAL` ·
`/ground-or-propose-ingredient identifier UNMAPPED_0316`.

## The residual surface
- **Primary residual:** `data/curated/unmapped_ingredients.yaml` — every record with
  `mapping_status: UNMAPPED` and an `UNMAPPED_NNNN` placeholder identifier.
- **Categorize + prioritize:** run `scripts/analyze_unmapped.py` to bucket the residual
  (`SIMPLE_CHEMICAL`, `COMPLEX_MIXTURE`, `ENVIRONMENTAL`, `INCOMPLETE`, `PLACEHOLDER`,
  `UNKNOWN`) with mappability scores; work the high-mappability SIMPLE_CHEMICAL head first.
- **Currency check:** `scripts/reconcile_sssom.py` reports GAP / ORPHAN / STALE rows between
  the curated collections and `mappings/ingredient_mappings.sssom.tsv` — fix these as you go.

## Inputs (read these)
- **Residual + curated collections:** `data/curated/{unmapped,mapped}_ingredients.yaml`.
- **Schema:** `src/mediaingredientmech/schema/mediaingredientmech.yaml` — `IngredientRecord`,
  `OntologyMapping`, `ChemicalProperties`, `CurationEvent`.
- **Output SSSOM:** `mappings/ingredient_mappings.sssom.tsv` (one row per mapped ingredient).
- **Routing/normalization policy:** `MAPPING_SEMANTICS.md` and the `map-media-ingredients` skill
  (hydrate stripping, formula fixing, catalog removal, abbreviation expansion; exact →
  normalized → fuzzy matching cascade against CHEBI/FOODON via OAK + EBI OLS4).
- **Deep research:** the `mediaingredientmech-agentic-curation` skill /
  `scripts/research_ingredient_edison.py` (`just research-ingredient-edison <slug>`,
  FutureHouse PaperQA3 by default; `--job` selects Falcon/precedent variants) for identity
  confirmation + synonym + CAS-RN recovery.
- **Promotion + minting:** `scripts/promote_resolved_unmapped.py` (the apply tool — **CHEBI
  ids only**); `manage-identifiers` for `kgmicrobe.compound:` slugs and the collection-edit
  path that non-CHEBI groundings/mints take (see §5).

## Procedure

### 1. Build + cluster the worklist
Run `analyze_unmapped.py`, apply the `$ARGUMENTS` filter, and **cluster by chemical
identity** after normalization. `MgSO4•7H2O` / `MgSO4·7H₂O` / `Magnesium sulfate
heptahydrate` are three spellings of **one** compound — collapse those into one record.
Cluster spelling variants and catalog-tagged forms so one decision covers all surface forms.

**But a different hydration state is a different compound.** `MgSO4` and `MgSO4•7H2O` are
120.37 and 246.47 g/mol, which is exactly what a recipe depends on, so they are separate
records and must not share an identifier. Per **MAPPING_SEMANTICS.md Section 3**: give each
hydration state a hydrate-specific ontology term if one exists, else its own
`cas:<hydrate CAS>` with a `broadMatch` to the anhydrous parent and the Rule B1 registry
row. Grounding the anhydrous parent once and hanging the hydrate off it as a `HYDRATE_FORM`
synonym is what produced the 32 families tracked in #218.

### 2. Tier-0 bulk grounding — no research needed (do this first)
Most of the SIMPLE_CHEMICAL head is mechanical. Use the `map-media-ingredients` cascade
(normalize → exact → normalized → fuzzy) and route by ingredient type:
| ingredient type | search first | then | else |
|---|---|---|---|
| simple chemical / salt / organic (defined formula) | **CHEBI** | `cas:` (definitive CAS, no CHEBI) | mint `kgmicrobe.compound:` |
| biological material / extract / peptone / serum | FOODON | CHEBI (secondary) | leave UNMAPPED if composition variable |
| environmental sample (soil/marine extract) | ENVO | CHEBI | leave UNMAPPED |
| medical / cancer-context reagent | NCIT | CHEBI | — |
| complex mixture, unknown/variable composition | — | — | **leave UNMAPPED** (correct outcome) |
Apply only **exact / strong-normalized CHEBI** hits in Tier-0 via
`scripts/promote_resolved_unmapped.py --quality EXACT_MATCH`/`SYNONYM_MATCH` (CHEBI-only — see
§5); route FOODON/NCIT/`cas:`/mint hits and every fuzzy/ambiguous hit to step 3 and the
collection-edit apply path.

### 3. Deep-research the ambiguous remainder — use the agentic-curation skill
For each ambiguous record (no clean exact match, or a normalization that needs confirming),
invoke `mediaingredientmech-agentic-curation` / `just research-ingredient-edison <slug>` with
a scoped query: confirm the chemical identity, recover the CAS-RN, and find the best
CHEBI/FOODON/NCIT term + match strength. Treat the cached Edison report
(`research/ingredients/<slug>-edison-<job>.md`, e.g. `<slug>-edison-literature.md`) as
evidence; cite it in the curation_history. Batch related records into one job where possible.

### 4. Decide per ingredient (priority order)
1. **Strong CHEBI / FOODON / NCIT match** (exact/close, same compound) → ground to that CURIE.
   *Maximize this.*
2. **No ontology term, definitive CAS-RN** → ground to `cas:NNNNNN-NN-N`
   (`evidence_type: CAS_RN_CROSS_REFERENCE`).
3. **No good existing term anywhere**, but a **real, distinct, recurring chemical identity** →
   **mint `kgmicrobe.compound:<slug>`** (with the mandatory registry `skos:exactMatch` sibling
   row — see invariants).
4. **Variable / unknown composition** (commercial broths, undefined sera, "vitamin solution") →
   **leave UNMAPPED**, but enrich synonyms + `curation_history` with the deep-research finding so
   the decision is documented. This is the correct outcome for ~most COMPLEX_MIXTURE records.

Never assert a CHEBI primary that isn't the same compound just to raise coverage; never mint a
`kgmicrobe.compound:` for something that genuinely has no defined identity.

### 5. Apply
- **Promote CHEBI matches** with `scripts/promote_resolved_unmapped.py` — **CHEBI ids only**
  (the tool rejects any non-CHEBI target):
  `python scripts/promote_resolved_unmapped.py --identifier UNMAPPED_NNNN --to CHEBI:NNNNN
  --quality EXACT_MATCH --evidence-source "Edison deep research" --note "…" --apply`
  (dry-run by default; the PK-collision guard refuses a duplicate primary and suggests
  `merge-ingredients` instead — follow it).
- **FOODON / NCIT / `cas:` groundings and `kgmicrobe.compound:` mints** are *not* handled by
  that tool — apply them through the collection-edit path: move the record from
  `data/curated/unmapped_ingredients.yaml` → `mapped_ingredients.yaml` (fix the counts), set
  its `ontology_mapping` (use `manage-identifiers` to reserve a `kgmicrobe.compound:<slug>`),
  and add the SSSOM row — plus, for any minted/narrow target, the mandatory
  `MIM:<slug> skos:exactMatch kgmicrobe.compound:<slug>` registry sibling row that
  `validate_sssom_invariants.py` Rule B1 requires. The `build-unified-mapping` skill
  regenerates the SSSOM from the collections.
- **Reconcile + round-trip:** `python scripts/reconcile_sssom.py --apply --date YYYY-MM-DD`,
  then **`just sync-curated`** to keep per-record files and collections in sync.
  Do NOT use `just export-individual` for this: it projects the collection OVER
  the per-record tree, reverting edits made there. (`just aggregate-collections`
  was removed in #169 — it wrote `data/collections/`, which nothing reads. That
  pairing is what silently reverted 55 curation events, #148.)

### 6. Verify + report
`just qc` (schema + evidence + SSSOM) · `python scripts/validate_sssom_invariants.py`
(Rules A–B4, exit 2 on violation) · `just validate-products` (id↔label gate, BLOCKING) ·
`python scripts/reconcile_sssom.py` (bare — read-only is the default; GAP/ORPHAN/STALE = 0,
exits non-zero on drift). Fix anything they flag.

Report, against the prior unmapped count:
- new mapped/unmapped counts and the delta (and per `analyze_unmapped` category);
- counts: grounded-to-CHEBI vs FOODON vs NCIT vs `cas:` vs minted-`kgmicrobe.compound:` vs
  stayed-UNMAPPED;
- the Tier-0 bulk share vs the deep-researched share.

## Guardrails
- **Coverage-maximizing, not match-forcing:** a wrong CHEBI grounding is worse than an honest
  UNMAPPED. Variable-composition mixtures *should* stay UNMAPPED.
- **Right layer:** this is chemical identity (CHEBI/FOODON/NCIT/cas:/kgmicrobe.compound:).
  **METPO has no role here** — never ground an ingredient to a METPO/trait term.
- **Conservative minting:** mint `kgmicrobe.compound:` only for genuinely distinct, recurring
  identities with no ontology term anywhere; always add the registry exactMatch sibling row.
- **Respect the gates:** `validate_sssom_invariants.py` and `validate-products` are BLOCKING;
  never commit rows they reject — route those to `mappings/needs_curator_review.tsv`.
- **Don't over-research:** Tier-0 the exact-match head; spend Edison only on the ambiguous
  middle. Batch where possible, commit per category, keep the diff reviewable.
