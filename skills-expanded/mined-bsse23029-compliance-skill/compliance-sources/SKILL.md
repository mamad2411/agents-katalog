---
name: compliance-sources
description: Rules for sourcing, citing and re-verifying every compliance claim about this product, backed by compliance/sources/REGISTRY.yaml. Use whenever asserting that a law, standard or technical specification requires something, when adding a new source, or when a source's freshness is in doubt.
---

# Compliance sources

Regulations move. A compliance claim without a dated, tiered source is a guess with a citation
shaped hole in it. This skill is the discipline that keeps the rest of the stack honest.

## The registry is the only citable set

`compliance/sources/REGISTRY.yaml` — 56 entries covering Saudi Arabia, wider MENA, Pakistan, the
international standards, platform docs and hospitality specs. Each entry carries `id`, `tier`,
`jurisdiction`, `status`, `url`, `pdf`, `last_checked`, `confidence` and `verify_by`.

**Rule 1.** If you cannot cite a registry `id`, you may not state the requirement as fact. Say
"unverified" and add it to the registry with `confidence: low`.

**Rule 2.** Tier order wins, always:

| Tier | Source | Use |
|---|---|---|
| 1 | Regulator / legislature | The obligation itself |
| 2 | Regulator's technical specification | What the code must implement |
| 3 | ISO / PCI SSC / NIST / OWASP / AICPA | Engineering baseline |
| 4 | Official vendor docs | Integration correctness |
| 5 | Industry bodies | Hospitality practice |
| 6 | Law firm / consultancy | Interpretation only — never the sole basis for a "must" |
| 7 | Academic | Depth |
| 8 | Blogs, forums, vendor marketing | Hints only, never cited |

A tier-6 summary never overrides a tier-1 text. When they conflict, the conflict itself goes in the
output.

**Rule 3.** Respect the status vocabulary. `draft-not-law` (e.g. `PK-PDPB`) can inform design but
can never produce a finding. `pending-publication` means the current text still governs.
`in-force-phased` means you must check which wave/cohort/date applies to *this* tenant.

## Freshness protocol

Before relying on an entry:

1. Is `verify_by` in the past? Re-verify.
2. Is `confidence: low`? Re-verify, or state the uncertainty in the finding.
3. Is the domain one that moves on a schedule? ZATCA announces e-invoicing waves ~6 months ahead;
   SDAIA has amendments in consultation; ISO 9001:2026 publishes 16 Sep 2026; the EU Digital Omnibus
   is mid-negotiation. These are re-check triggers, not background noise.

To re-verify: WebFetch the official `url`, record what changed, update `last_checked`,
`checked_via` and `confidence`, and append the raw result to a new dated file in
`compliance/sources/raw/`. Do not edit old raw files.

## Raw vs curated vs report

Three layers, kept apart on purpose:

- `compliance/sources/raw/` — verbatim search results and page extracts, dated, append-only.
  This exists so nobody re-runs the same fourteen searches next quarter.
- `compliance/sources/REGISTRY.yaml` — the distilled, citable list.
- `compliance/grids/` — the finished module × source × status report.

Never let a claim skip a layer. Report cites registry; registry cites raw or PDF.

## Offline copies

Some regulators are unreachable from automated tooling — `sdaia.gov.sa` returned no response and
`nca.gov.sa` refused connection on 2026-08-20; `iso.org` returns 403 to bots and sells its
standards anyway. For these, the PDF in `compliance/sources/pdfs/<region>/` is the working copy.
`compliance/sources/fetch-sources.sh` fetches what is publicly fetchable and lists the rest as
manual downloads.

Record the document version from the PDF cover page when you file it — several regulators
(ZATCA's spec index, for one) do not show version numbers on the web page.

## Writing a citation

In a grid cell or a finding, cite as: `SA-PDPL-TRANSFER` — with the URL only in the sources
appendix, not inline in every row. A finding that says "PDPL requires X" without an id is
incomplete work.

## Adding a source

Append to `sources:` with every field populated. Pick a stable, greppable id: region prefix
(`SA-`, `AE-`, `PK-`, `EU-`, `US-`, `ISO-`, `VENDOR-`, `HOSP-`), then the instrument. Set
`applies_to` to some subset of `[frontend, backend, cicd]` — this is what lets the grids stay
separated by surface.
