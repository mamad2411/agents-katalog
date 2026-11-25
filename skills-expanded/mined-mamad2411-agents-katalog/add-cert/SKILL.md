---
name: add-cert
description: Add a new security certification to the roadmap by writing data/certs/<vendor>/<slug>.json from official + third-party sources.
---

# add-cert

## When to use

The user (or an Issue picked up by `respond-to-issue`) names a certification
that should appear in the roadmap. You verify it does not already exist,
research it from primary sources, and write a single new JSON file.

## Inputs

- Vendor / issuing body name
- Certification name and abbreviation
- Suggested primary domain (one of `data/domains.json`)
- Whether the cert is `japan_only` (true for IPA, SEA/J, JP-only national exams)

## Process

1. **Dedupe.** Check `data/manifest.json` and `data/certs/<vendor-slug>/`.
   If the cert already exists, refuse and point at the existing file (or
   delegate to `update-cert`).
2. **Fetch the official source** using WebFetch. Required: an authoritative
   URL on the vendor's domain (or the issuing government agency's domain).
   Capture today's date as `official.fetched_at`.
3. **Find at least two third-party evaluations.** Acceptable sources are
   listed in `data/sources/agencies.json` under `trust_tier: high` (NIST
   NICE, DoD 8140 baseline list, ANSI ISO/IEC 17024 directory, IPA registry,
   ENISA, NCSC-UK, CREST, JPCERT, NISC). Vendor self-assessment does not
   count. If you cannot find two, **stop and ask the user**; do not invent
   evaluations.
4. **Identify scoring factors.** Plus factors are evidence the cert is
   substantive (regulatory recognition, accreditation, hands-on practical,
   long-standing reputation, performance-based exam, requires verified
   experience). Minus factors are evidence it is weaker than its
   reputation (vendor-only recognition, no accreditation, multiple-choice
   only, very short exam, recently created without uptake, expensive
   renewal). Every factor needs a `code` (UPPER_SNAKE) and a `weight_hint`
   (low / medium / high). Where you have a URL for the claim, attach it as
   `evidence`.
5. **Write the JSON file** at `data/certs/<vendor-slug>/<cert-slug>.json`,
   conforming to `schema/certification.schema.json`. Leave `evaluation` as:
   ```json
   { "computed_tier": null, "computed_at": null, "computed_by_skill": null, "rationale": null }
   ```

   **Populate `prerequisites.recommended_certs[]`** with the ids of any certs
   the official source explicitly lists as prerequisites or strongly
   recommends as preparation. The roadmap UI inverts this list to draw
   "commonly followed by" arrows from each prereq to its successors, so
   keeping it accurate makes the visual roadmap useful. Use ids exactly as
   they appear in `data/manifest.json` (e.g. `"isc2.cissp"`). It is OK to
   reference certs that don't yet exist in the manifest — the UI will mark
   them as missing.

   **Set `availability` if the cert is not actively examinable.** Default
   is `available` (omit the field). Use `paused` when the vendor has
   explicitly suspended exam delivery without retiring the cert; `retired`
   when delivery has ended; `coming-soon` for announced but not-yet-launched
   exams. Pair with a short `availability_note` quoting the vendor's
   wording when possible.
6. **Update the manifest.** Run `python3 scripts/build_manifest.py` (or
   `make manifest`).
7. **Validate.** Run `make validate`. Fix any schema errors before
   considering the work done.
8. **Hand off to `infer-relationships`.** Run
   `python3 scripts/infer_relationships.py --dry-run` to surface any
   prerequisite edges (same-vendor ladder steps + curated cross-vendor
   industry flows) the new cert should have. Apply the ones the
   maintainer accepts, then proceed.
9. **Hand off to `evaluate-roadmap-3-personas`.** Tell the user the new
   cert exists with `evaluation.computed_tier = null` and the evaluation
   skill must be re-run before the PR is mergeable.

## Refusal conditions

- Vendor's official URL is unreachable or does not actually describe the
  cert: refuse.
- Fewer than two distinct third-party evaluations available: refuse and ask
  the user how to proceed (a brand-new cert with no third-party uptake may
  not yet belong on the roadmap).
- Cert appears to be a course completion certificate, not a proctored /
  assessed certification: refuse.

## Reference example

`data/certs/isc2/cissp.json` is the canonical shape. Mirror its field
ordering for readability.
