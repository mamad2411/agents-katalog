---
name: dedup-prior-art-check
audience: specialist
description: Use before spending real effort on a bug-bounty lead, and again immediately before submitting a finding, to prove the vulnerability and its specific composite chain are not already known — public advisories, prior audits, Solodit, and our own past submissions — so the squad never burns a report on a duplicate. Fires at systematic-attacking Phase 1 and its pre-submit refresh.
---

# Dedup / Prior-Art / Novelty Check

Before spending effort on a lead and again immediately before submitting a finding, prove the
vulnerability (and the specific composite chain) is not already known — so the squad never burns a
report on a duplicate. This operationalizes `systematic-attacking` Phase 1 and its pre-submit refresh
into a concrete, evidence-producing gate.

**Source:** corpus B §11 (Cyfrin **Solodit** — 49k+ aggregated real-world smart-contract findings)
plus public advisory databases (GHSA, CVE, OSV) and program disclosure history; corpus A
elite-vs-average (narrow-and-deep continuous prior-art discipline).
**Impact class enabler:** protects report acceptance rate; a `duplicate`/`likely-duplicate` verdict
routes a lead for differentiation. This gate does not itself kill or demote - campaign disposition,
and the single Phase-5 candidate-kill point, is owned by `shared/modes/bounty.md`.
**Governing method:** the dedup gate of `systematic-attacking` (Phase 1 + pre-submit).

## Method
1. Build the search key from the lead: root-cause class, affected contract/endpoint/component,
   protocol + version, and the specific chain shape (not just the vuln class).
2. Query the prior-art surfaces: program disclosure history (HackerOne/Immunefi), GHSA/CVE/OSV,
   and — for web3 — the Solodit corpus. Use a separately provisioned prior-art service when one is
   configured for this lane; otherwise search Solodit and the GitHub advisory database by hand.
   Log a prior-art service attempt that fails as `needs_tool`, even when the manual search then
   succeeds. Search our own `chrono-vault` for prior squad work on the target.
3. Classify: `novel` / `variant-of-known` (cite the closest prior finding + what differs) /
   `likely-duplicate` / `duplicate`. Composite chains get a *separate* verdict — a chain of known
   primitives can still be a novel composition, and a novel-looking chain can be a known composite.
4. Return the novelty verdict with evidence; do not kill or demote - that is the campaign's call
   (`shared/modes/bounty.md`, Phase 5). An exact collision leaves the active queue but is preserved
   as an inner-link primitive for the chainer ('differentiate, don't veto'). For `variant-of-known`,
   document the delta that makes it independently submittable.
5. Refresh the check immediately before submission (new disclosures land daily); attach the dated
   query evidence to the report.

## Acceptance
- Every lead carries a dated novelty verdict with the prior-art sources queried named.
- Every lead carries a dated novelty verdict before deep effort; disposition (kill/demote) is the
  campaign's Phase-5 decision, not this gate's, and exact collisions are preserved as chain primitives.
- The pre-submit refresh is recorded with its date; a failed prior-art service attempt is logged as
  `needs_tool` — even when the manual search succeeded — never silently skipped.
