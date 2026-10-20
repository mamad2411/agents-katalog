---
name: add-entity-emitter
description: "Maintainer-side: scaffold a new Brain entity emitter (module + CLI + tests + vendored schema) from the observed n=2 pattern."
audience: marketplace-maintainers
---

# add-entity-emitter

> **Maintainer-side skill.** Lives in `.claude/skills/`, not `plugins/sulis/skills/`.
> Founders consume entities; they never need to extend the Brain. This skill is
> for the marketplace team adding new entity emissions (Component, Test,
> Release, Finding, Opportunity, …) as the Brain↔OS substrate grows.

## What this generates

Given an entity name (e.g. `Opportunity`) and its source artifact (e.g. `SRD.md`
Summary section), this skill produces the **standard 5-piece emission slice**
that CH-01KSWB (Decision) and CH-01KSWQ (Requirement) both follow:

```
plugins/sulis/brain/compiled/product-development/{entity}.schema.json  # vendored
plugins/sulis/scripts/_{entity}_emission.py                            # pure compose + persistence orchestrator
plugins/sulis/scripts/sulis-emit-{entity}                              # CLI w/ JSON envelope
plugins/sulis/scripts/tests/unit/test_{entity}_emission.py             # transformation + integration tests
plugins/sulis/scripts/tests/unit/test_sulis_emit_{entity}_cli.py       # CLI subprocess tests
```

The maintainer then **fills in the entity-specific `compose_X_from_Y` function**
(the only genuinely per-entity logic) and runs the test suite.

## When to invoke

Use when adding emission for a new entity type. Each entity already has a
compiled schema upstream at the **canonical consumer location**:

```
$DNA/compiled/schemas/{domain}/{entity}.schema.json
```

(where `$DNA=/Users/iain/Documents/repos/plugins/.specifications/business-dna`).
Domains today: `foundation` (cross-cutting: Tenant, Actor, Credential),
`product-development` (~20 entities), `insurance-broking` (~17 entities).

To discover what entities exist, see `$DNA/compiled/INDEX.md` (the catalogue)
and `$DNA/compiled/CONSUMER_HOWTO.md` (the bridge document that names every
consumer command — schema fetch, validation, mint requests). The bridge doc
explicitly self-identifies as transient: it'll be superseded by the
`sulis-brain` marketplace plugin (`/sulis-brain:list-domains`,
`/sulis-brain:fetch-schema`, etc.) when that ships. Until then, this skill
reads schemas via the filesystem path above; when `sulis-brain` lands, the
fetch step transparently shifts to the slash command — no other skill change
required.

**Do not use** for: per-instance emission of an entity that's already wired
(that's a one-shot `sulis-emit-X` CLI call); for editing existing emitters
(diff the generated files manually).

## The 4 questions to answer first

Ask the maintainer these, in order, before generating anything:

1. **Entity name?** (e.g. `Opportunity`, `Component`, `Test`, `Release`,
   `Finding`). Match the entity's name in the upstream ontology (singular,
   Title-case the natural-language form; lowercase the schema id).

2. **Source artifact?** Where the entity content comes from. Common shapes
   observed in n=2:
   - `.md` file with frontmatter + body sections (n=1, Decision-from-ADR)
   - `.md` file with body-marker blocks like `**FR-NN: ...**` (n=2, Requirement-from-SRD)
   - structured `SPEC.yaml` (Opportunity, possibly)
   - CI run output / pytest JSON (Test)
   - git commit metadata (Component, Release)

3. **Cardinality?** One-per-call or many-per-call:
   - **one-per-call**: one source file → one entity (n=1 Decision pattern). CLI takes one path, returns one instance.
   - **many-per-call**: one source file → N entities (n=2 Requirement pattern; each FR-NN block → one Requirement). CLI takes one path, returns a count + list.

4. **Cross-entity references required by the schema?** Look at the
   `required:` fields in `{entity}.schema.json`. Any field that uses a
   `dna:(opportunity|actor|...)` pattern is a cross-ref. Decide before
   generating:
   - **No required refs** (n=1 Decision pattern) — straightforward.
   - **Required refs to an entity that already emits** — use real IDs (look up via the source artifact).
   - **Required refs to an entity that doesn't emit yet** — use a **deterministic synthetic placeholder** (n=2 Requirement pattern: derive a ULID from the source-path hash; record the placeholder nature in the entity's `rationale`; queue a follow-up to resolve when the referenced entity ships).

The four answers determine the templates' variable substitutions and which
template path to take.

## How to generate (step-by-step)

### Step 1. Confirm the upstream schema exists.

```bash
# Pick the right domain — foundation (cross-cutting: Tenant, Actor, Credential),
# product-development, or insurance-broking. See $DNA/compiled/INDEX.md.
DOMAIN=product-development   # or foundation, insurance-broking
ls $DNA/compiled/schemas/$DOMAIN/{entity}.schema.json
```

If the file's missing, **stop** — the ontology doesn't yet have this entity.
Raise a mint request per `$DNA/compiled/CONSUMER_HOWTO.md` §5 (or check
`$DNA/MINTING_PLAYBOOK.md`); come back here once it's compiled.

### Step 2. Vendor the schema.

```bash
mkdir -p plugins/sulis/brain/compiled/$DOMAIN
cp $DNA/compiled/schemas/$DOMAIN/{entity}.schema.json \
   plugins/sulis/brain/compiled/$DOMAIN/{entity}.schema.json
```

The marketplace mirrors only the schemas it actively consumes — vendor on
demand, not in bulk. This keeps the diff visible at PR time (one new schema
per emission slice).

### Step 3. Generate the four code files from templates.

Four unified templates live alongside this SKILL.md under `templates/` —
one shape covers both one-per-call and many-per-call (a one-per-call
emitter just returns a list of length 1):

| Template | Becomes |
|---|---|
| `templates/emission.py.template` | `plugins/sulis/scripts/_{entity}_emission.py` |
| `templates/cli.template` | `plugins/sulis/scripts/sulis-emit-{entity}` |
| `templates/test_emission.py.template` | `plugins/sulis/scripts/tests/unit/test_{entity}_emission.py` |
| `templates/test_cli.py.template` | `plugins/sulis/scripts/tests/unit/test_sulis_emit_{entity}_cli.py` |

**Variable substitutions** (use the maintainer's answers from the 4 questions):

| Token | Meaning | Example (Opportunity) |
|---|---|---|
| `__ENTITY__` | Title-case entity name | `Opportunity` |
| `__entity__` | lowercase for schema id, file paths, function-name segments | `opportunity` |
| `__ENTITY_PLURAL__` | Title-case plural (display only, in docstrings) | `Opportunities` |
| `__SOURCE_NOUN__` | what the source artifact is, plain English | `SRD Summary section` |
| `__source__` | lowercase short tag for function-name segments | `srd` |
| `__SOURCE_FLAG__` | CLI flag for the source path | `--from-srd` |
| `__SOURCE_FLAG_ATTR__` | argparse attribute name (the flag with `--` stripped and `-` → `_`) | `from_srd` |
| `__SOURCE_EXT__` | source file extension (with the dot) | `.md` |

**Substitution rule**: do a literal text replacement of each token across
all four generated files. The function name `compose___entity___from___source__`
resolves to `compose_decision_from_adr` etc. — the triple-underscore is
intentional (each `__entity__` placeholder is the two-underscore word
plus the word-separator underscores).

Don't add entity-specific logic to the templates — that's Step 4.

### Step 4. Fill in the entity-specific `compose_X_from_Y` function.

This is the **only** entity-specific code the maintainer writes. The template
leaves a clearly-marked `TODO` block where the compose function goes. The
contract:

- **Input**: source-artifact text (or parsed structure) + the source path
  (for deterministic-id derivation).
- **Output**: dict (one-per-call) or list-of-dict (many-per-call), each dict
  conforming to the entity's compiled schema.
- **Required schema fields** must be populated (look at the vendored
  schema's `required` array). For SRD-absent fields, use **defaults that
  match the entity's intent**, not nulls. Document defaults in the entity's
  `rationale` field where the schema allows.
- **Cross-entity refs**: real IDs when resolvable; deterministic synthetic
  placeholders otherwise (n=2 pattern).

### Step 5. Make `sulis-emit-{entity}` executable.

```bash
chmod +x plugins/sulis/scripts/sulis-emit-{entity}
```

### Step 6. Run the tests.

```bash
cd plugins/sulis/scripts && uv run pytest tests/unit/test_{entity}_emission.py tests/unit/test_sulis_emit_{entity}_cli.py -v
```

The templates produce a green test suite **before** you fill in the compose
function — the tests check shape + standard behaviours (round-trip,
idempotency, rejection on validation failure). Once you fill in compose, the
data-shape tests stay green; you add entity-specific assertions next.

### Step 7. Smoke against a real source artifact.

Run `sulis-emit-{entity} {SOURCE_FLAG} <path-to-real-source>` against a
representative example from the repo. Inspect the emitted `.jsonld`. Iterate
on the compose function until the output reads cleanly.

### Step 8. Full-suite regression check + commit + ship.

Standard change-flow: `uv run pytest tests/unit/`, then commit, push, PR,
ship via `/sulis:change ship`.

## Worked examples (the n=2 evidence this skill comes from)

These are the two emission slices the templates were extracted from:

| Slice | Entity | Source | Cardinality | Cross-refs | What you can learn from it |
|---|---|---|---|---|---|
| **CH-01KSWB** | `Decision` | `ADR-NNN-*.md` (frontmatter + body sections) | one-per-call | none | the **n=1 baseline** — the canonical shape this skill scaffolds |
| **CH-01KSWQ** | `Requirement` | `SRD.md` body markers (`**FR-NN: ...**`) | many-per-call | `source` → Opportunity (synthetic placeholder) | the **n=2 divergence** — many-per-call, body markers, synthetic-placeholder strategy, deterministic ULIDs |

Read both before scaffolding a new entity if its shape isn't an obvious fit.
The diff between them is the skill's design space.

## Common gotchas observed across n=2

- **Section-boundary regex.** For body-marker extraction (n=2 pattern), the
  regex must truncate at any heading level (H2-H5), not just H2. Real
  documents use H4 sub-headings to start new feature sections; if your
  regex stops at H2 only, content bleeds across feature boundaries.
- **Defaults must be loud.** When the source doesn't carry a required
  field, pick a default that's the **strongest plausible value** (e.g.
  `priority="must"`, not `priority="should"`) so an author overriding it
  sees the diff. Record applied defaults in `rationale`.
- **Deterministic IDs over fresh ULIDs.** When the source artifact has no
  natural identity (n=2 SRD's FR-NN are positional, not stable IDs),
  derive the entity ULID from `sha256(source_path + ":" + position)` so
  re-emission is idempotent — the same artifact always produces the same
  entity IDs.
- **Cross-entity refs.** The schema's `source` / similar fields require
  real instance IDs. If the referenced entity doesn't emit yet, use a
  deterministic synthetic placeholder + document in `rationale` + queue a
  resolution slice.
- **CLI envelope.** Always `{"ok": bool, "data": {...}}` on success;
  `{"ok": false, "error": "..."}` on failure. Exit 0 on success (including
  empty-source success); exit 1 on failure. Matches the marketplace
  convention.

## When NOT to use this skill

- Editing an existing entity emitter — diff against the templates manually.
- Creating a wholly-new artifact type that isn't a Brain entity — this
  scaffolds entity emission specifically.
- An entity that doesn't yet have a compiled schema in the plugins repo —
  add it upstream first (in `sulis-ai/plugins`).

## File checklist (verify before committing)

- [ ] `plugins/sulis/brain/compiled/product-development/{entity}.schema.json` (vendored)
- [ ] `plugins/sulis/scripts/_{entity}_emission.py` (compose function filled in)
- [ ] `plugins/sulis/scripts/sulis-emit-{entity}` (executable bit set)
- [ ] `plugins/sulis/scripts/tests/unit/test_{entity}_emission.py`
- [ ] `plugins/sulis/scripts/tests/unit/test_sulis_emit_{entity}_cli.py`
- [ ] Tests pass: `uv run pytest tests/unit/test_{entity}_*`
- [ ] Full suite regression: `uv run pytest tests/unit/`
- [ ] Smoke against a real source artifact, inspected by hand
