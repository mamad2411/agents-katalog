---
name: hunter-intent
description: >-
  Extract declared intent from a quarry's authorities (specs, PRDs, acceptance
  criteria, OpenAPI/JSON-Schema/GraphQL SDL, type definitions, docstrings,
  existing test names, design tokens, i18n files, CHANGELOG, README) and convert
  every normative statement into a checkable conformance oracle bound to a
  SurfaceUnit. This is what makes conformance-mode hunting possible: a
  conformance Find must cite the authority it violates. Load and run this after
  hunter-recon and before conformance probing, and whenever asked to check
  against a spec, verify requirements, confirm a contract, or find spec
  deviations. Produces normative_claims.json plus normative_claims.md. Assumes
  hunter-doctrine and hunter-recon are loaded.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
argument-hint: <target-path-or-url> [--surface-map <path>] [--sources <globs>]
---

# Hunter Intent — declared intent into conformance oracles

`defect` mode needs no spec: a crash is wrong on its own terms. `conformance`
mode is different — it hunts the gap between **what was promised** and **what the
system does**. That gap only exists relative to a stated promise, so a
conformance Find is worthless unless it cites the exact promise it violates
(`hunter-doctrine`, evidence-standards: "the spec line quoted verbatim with its
source location, beside the observed behaviour"). This skill mines those
promises and turns each into a probe.

The output is not prose about the spec. It is a set of **NormativeClaim** objects
— each a single testable assertion, carrying its verbatim quote and source
location, bound to the SurfaceUnits it constrains.

## Inputs

- `target`: source path and/or base URL (same target as recon).
- `surface_map`: `surface_map.json` from `hunter-recon`. Required — claims bind
  to `SurfaceUnit.id`s. A claim that binds to nothing in the map is a Sign about
  either the map or the spec (see "Unbound claims").
- `sources`: optional globs to narrow the authority set.

## Output artifacts

Written to `<run-dir>/intent/`:

- `normative_claims.json` — array of NormativeClaim objects plus `intent_meta`.
- `normative_claims.md` — human-reviewable rendering grouped by source.
- `intent_conflicts.json` — claim-vs-claim contradictions (see "Contradictions").

## Sources of declared intent, in priority order

Priority is by authority strength and machineability. A machine-readable
contract outranks prose; a versioned spec outranks a README aside.

1. **Machine contracts** — OpenAPI/Swagger, JSON Schema, GraphQL SDL, Protobuf,
   Avro. These are already normative and structured: every constraint (required
   field, type, format, enum, min/max, status code, nullability) is a claim with
   a precise location (`openapi.yaml#/paths/~1cart/post/responses/200`). Highest
   authority — the team committed to them as a contract.
2. **Acceptance criteria** — Gherkin `.feature` files, ticket AC blocks, "Given/
   When/Then". Already in testable form; extraction is near-mechanical.
3. **Type definitions & signatures** — TypeScript types, dataclasses/pydantic,
   Go structs, Rust types. Encode required-ness, nullability, and shape. A
   response that violates its own declared type is a conformance deviation.
4. **Specs / PRDs / design docs** (markdown) — the richest source of MUST/SHALL
   prose. Highest yield, lowest structure; mine per "Mining normative statements".
5. **Docstrings & API doc comments** — function-local contracts (`@throws`,
   `@returns`, "raises ValueError if …"). Bind to the surface whose handler they
   document.
6. **Existing test names** — `test_rejects_expired_token`,
   `it("returns 422 on missing email")` encode expected behaviour even where the
   test body is thin. Names are claims; treat the (possibly absent or weak) body
   as separate.
7. **Design tokens / design system** — colour/spacing/type scales, component
   contracts (`Button must have visible focus ring`). Bind to `ui_control` /
   `web_page` units. Feeds visual/layout oracles.
8. **i18n / localisation files** — every user-facing string key is a claim that
   the string renders for its locale; missing keys per locale are conformance
   gaps. Bind to the screens that use them.
9. **CHANGELOG claims** — "Added X", "Fixed Y so Z now works", "Deprecated W".
   Each is a checkable assertion about current behaviour and a natural
   regression/conformance target.
10. **README promises** — "supports", "automatically", "never stores". Lowest
    authority (marketing drift is common) but still cited if violated. Mark
    `modality` honestly — most README verbs are `should`, not `must`.

Record every source you opened in `intent_meta.sources_scanned` with its
resolved path/URL. Never cite a source you did not open (anti-fabrication law).

## Mining normative statements from prose

Scan prose sources for **normative modality** and quantified constraints. The
signal words:

- **must** modality: `MUST`, `SHALL`, `REQUIRED`, `always`, `never`, `only`,
  `at least`, `at most`, `exactly`, `within N ms`, `no more than`, `guaranteed`.
- **should** modality: `SHOULD`, `RECOMMENDED`, `expected to`, `by default`,
  `typically`, `ought to`.
- **may** modality: `MAY`, `OPTIONAL`, `can`, `supports`.

For each matched statement:

1. Capture the **verbatim quote** — the exact sentence, unedited. This is
   non-negotiable (see "Never paraphrase").
2. Record `source_uri` and the **line** (or JSON pointer / anchor for
   structured sources).
3. Classify `modality` from the signal words. `must` claims are the promotion
   targets; `should`/`may` are recorded but a violation is at most `PASS WITH
   ISSUES`, not `FAIL`, unless a `must` elsewhere reinforces them.
4. Extract the **quantified constraint** where present: the threshold, the
   status code, the timing bound, the enum. A vague claim ("fast", "secure")
   with no measurable predicate is `testability: untestable` — record it, do not
   invent a threshold for it.
5. **Bind to surfaces** — resolve which `SurfaceUnit.id`s the claim constrains by
   matching route/path, command, component, or handler names against the surface
   map's locators. A claim may bind to many units and a unit to many claims.

## Never paraphrase a claim into an assertion

A conformance Find's authority *is* the quote. If you paraphrase, the operator
cannot verify the citation, the doctrine's conformance evidence standard is
unmet, and the Find is unciteable. Therefore:

- `verbatim_quote` holds the source text exactly, including its own wording and
  emphasis. Do not normalise, summarise, or "clean up".
- `generated_probe` may restate the claim as a machine assertion, but that is
  *in addition to* the quote, never instead of it.
- If a claim is too vague to quote a specific predicate, it is `untestable` —
  say so; do not manufacture a crisp assertion the source does not support.

## The NormativeClaim schema

```json
{
  "id": "clm/3f9a1c04",
  "source_uri": "docs/pricing.md",
  "location": {"line": 142, "pointer": null, "anchor": null},
  "verbatim_quote": "All displayed totals MUST include applicable tax.",
  "modality": "must",
  "constraint": {
    "kind": "invariant",
    "predicate": "cart.total == sum(items) + tax",
    "threshold": null,
    "unit": null
  },
  "bound_surfaces": ["sfc/http/7a3f9c2e", "sfc/web/5b2d1e"],
  "testability": "executable",
  "generated_probe": {
    "oracle": "http_contract",
    "steps": [
      "POST /api/v1/cart/{cartId}/items with a taxable item",
      "GET /api/v1/cart/{cartId}",
      "assert response.total == response.subtotal + response.tax",
      "assert response.tax > 0 for a taxable jurisdiction"
    ],
    "expected": "total includes tax",
    "authority_ref": "docs/pricing.md:L142"
  },
  "status": "unverified",
  "conflicts_with": [],
  "source_authority": 4
}
```

Field rules:

- `id` — `clm/<hash>` over `source_uri + location + verbatim_quote`. Stable
  across re-runs so a claim's verification state survives.
- `modality` — `must | should | may`. Drives verdict severity, per doctrine.
- `constraint.kind` — `invariant | status_code | schema | timing | enum |
  presence | ordering | i18n_key | visual`. Closed set; extend only with a
  recorded reason.
- `bound_surfaces` — `SurfaceUnit.id`s. Empty array only for `unbound` claims
  (below).
- `testability` — `executable` (a probe can run it now), `manual` (needs human
  judgement, e.g. copy tone), or `untestable` (no measurable predicate). Only
  `executable` claims get a runnable `generated_probe`; `manual`/`untestable`
  still get a claim record and a stated reason.
- `generated_probe.authority_ref` — `source_uri:Lnn`, carried into the Find so
  the citation survives to the report.
- `status` — `unverified | conformant | deviation | unbound | untestable`.
  Intent emits `unverified`; a probing stage advances it.
- `source_authority` — the source's priority rank (1–10 above); used to resolve
  contradictions.

## Contradictions and stale docs — the interesting cases

These are not errors to suppress; several *are* the deviation.

### Claim vs claim (spec-internal contradiction)
Two claims constrain the same surface incompatibly (e.g. `pricing.md`:
"totals MUST include tax"; `api-guide.md`: "the `total` field is pre-tax").
Emit both, cross-reference `conflicts_with`, and write an `intent_conflicts.json`
entry. Do **not** pick a winner silently. Rank by `source_authority` to suggest
which governs, but a spec that contradicts itself is itself a reportable
conformance problem — surface it to the operator.

```json
{
  "conflict_id": "cfl/8a11",
  "claims": ["clm/3f9a1c04", "clm/22b7de"],
  "surface": "sfc/http/7a3f9c2e",
  "kind": "spec_internal_contradiction",
  "higher_authority": "clm/3f9a1c04",
  "note": "pricing.md (rank 4) vs api-guide.md README aside (rank 10)"
}
```

### Claim vs observed behaviour — this IS the conformance deviation
When a probe runs the `generated_probe` and the system violates the claim, that
is the conformance Find. The claim supplies the "should" side of the doctrine's
required expectation; recon/probing supplies the "did" side. Promotion still
needs execution, 2× reproduction, and an artifact — the claim does not lower the
proof bar, it supplies the authority. Cite as:

```
cart total excludes tax — 2/2 · trail/B07 · docs/pricing.md:L142 "All displayed totals MUST include applicable tax."
```

### Stale docs
A claim whose bound surface no longer exists in the surface map, or whose
constraint the code contradicts by design, signals doc rot. Do not delete the
claim and do not assume the doc is right. Mark `status: unbound` (missing
surface) or record it as a candidate two-sided problem: either the code deviates
from the spec (a Find) or the spec is stale (a doc defect worth reporting).
Which one is the operator's call when a `must` is involved and the code is
deliberate — escalate via `hunter-ask` rather than guessing intent.

### Unbound claims
A claim that binds to no SurfaceUnit means the promised surface is missing from
the map (recon gap, or documented-but-unimplemented feature). Emit with
`status: unbound` and `bound_surfaces: []`. Cross-check against
`recon_quality.json`: a claim describing an endpoint that OpenAPI listed but the
route table did not is a strong "documented-but-unimplemented" Sign.

## Markdown rendering

`normative_claims.md`, grouped by source, highest authority first:

```
# Declared Intent — <target>  ·  <hunt-id>  ·  <ISO-8601>
sources scanned: 11  ·  claims: 214  (must 63 · should 121 · may 30)
testability: executable 148 · manual 41 · untestable 25
bound: 201 / 214  ·  unbound: 13  ·  conflicts: 2

## docs/pricing.md   (authority 4)
L142  [must · executable]  clm/3f9a1c04
      "All displayed totals MUST include applicable tax."
      binds: POST /api/v1/cart/{cartId}/items, /cart screen
      probe: http_contract — assert total == subtotal + tax

## openapi.yaml   (authority 1)
#/paths/~1session/post/responses  [must · executable]  clm/7c0e...
      "responses: 401 for invalid credentials"
      binds: POST /session

## Conflicts (2)
cfl/8a11  POST /cart total  ·  pricing.md:L142 vs api-guide.md:L88  (higher: pricing.md)

## Unbound claims (13) — surface missing from map, review
clm/44d2  README.md:L20 "Hunter supports SAML SSO" — no integration surface found
```

## Handoff

- To **conformance probing**: `normative_claims.json`. The prober runs each
  `executable` claim's `generated_probe` against its `bound_surfaces`, advances
  `status`, and on a reproduced violation opens a Sign that carries
  `authority_ref` — so the eventual Find cites the verbatim quote and location
  automatically.
- To **`hunter-recon`**: unbound claims and spec/route disagreements are recon
  gaps or documented-but-unimplemented surfaces — feed them back so the map's
  invisible set shrinks.
- To **reporting**: `must` deviations → `FAIL`; `should`/`may` deviations →
  `PASS WITH ISSUES`; `manual`/`untestable` claims → `NOT-COVERED` on the
  conformance axis with the reason stated. Every conformance line renders its
  `authority_ref` (`brand-system` §12: verdicts cite their authority).

## Self-check before emitting claims

- [ ] Every claim carries a verbatim quote and a resolved source location; none
      paraphrased
- [ ] `modality` classified from actual signal words, not assumed
- [ ] Every `executable` claim binds to ≥1 SurfaceUnit id; unbound claims marked
      `unbound`, not dropped
- [ ] Vague claims marked `untestable` — no fabricated thresholds
- [ ] Claim-vs-claim contradictions recorded in `intent_conflicts.json`, no
      silent winner
- [ ] No source cited that was not opened; `sources_scanned` complete
- [ ] `status` emitted as `unverified` — intent does not claim conformance,
      probing does
