---
name: zero-day-classification
description: Rigorously classify whether a confirmed finding is a known vulnerability, a variant, or a genuine zero-day candidate. Use for any novel/confirmed issue before labelling it. Core rule — "no CVE found" is NOT proof of novelty; the AI ceiling is POTENTIAL_ZERO_DAY, never CONFIRMED (that needs human review + vendor coordination).
---

# Zero-Day Classification (strict decision tree)

**A finding is NOT a zero-day just because you couldn't find a CVE.** "Nothing found" is
evidence of *uncertainty*, not of novelty. Walk the tree honestly and record the fields.

## Decision tree (first matching rule wins)
1. Security issue **confirmed & reproducible**? — No → `NOT_A_VULNERABILITY`.
2. A **security boundary actually broken**? — No → `INFORMATIONAL` (misconfig/hardening).
3. **Root cause identified**? — No → `FURTHER_INVESTIGATION` (human review).
4. **Affected product + version known**? — No → `FURTHER_INVESTIGATION`.
5. Is the **latest supported version** affected? — No → `LIKELY_KNOWN_FIXED`.
6. Does a **CVE / vendor advisory** match? — Yes → `KNOWN_VULNERABILITY`.
7. Only a **silent vendor fix / changelog** exists? — Yes → `POTENTIALLY_KNOWN_NDAY` (human review).
8. **Prior public disclosure / research**? — Yes → `PREVIOUSLY_DISCLOSED`.
9. **Same root cause as an existing CVE**, new endpoint? — Yes → `VARIANT_INCOMPLETE_FIX`.
10. Confirmed, reproducible, current-version-affected, and **nothing** found in 6-9 →
    **`POTENTIAL_ZERO_DAY`** (the ceiling). Requires human review + vendor coordination.
    Never output `CONFIRMED_ZERO_DAY`.

## Known-CVE lookup (do this before claiming novelty)
- Search NVD by product+version+keywords (public API, no key):
  `https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=<product+keywords>&resultsPerPage=5`
- Check the vendor's advisories/changelog/release notes for a silent fix.
- Search public disclosure (GitHub issues/advisories, exploit-db, research blogs, PoCs).
- Uncertainty from a failed search ≠ novelty.

## Fields to record on the finding
`affected_product`, `affected_version`, `latest_version_affected` (bool),
`known_cve_found` (bool), `vendor_advisory_found` (bool), `public_disclosure_found` (bool),
`previous_fix_found` (bool), `possible_duplicate` (bool), `root_cause` (text),
`classification` (one of the labels above), `human_review_required` (bool),
`vendor_coordination_required` (bool), `zero_day_candidate` = true **only** for
`POTENTIAL_ZERO_DAY`.

## Reporting
- Present zero-day **candidates** in their own report section, clearly marked
  "POTENTIAL — human validation required", with full reproduction, root cause, product+version,
  and the evidence that nothing public matches.
- Recommend responsible disclosure / vendor coordination. Do **not** publish or over-claim.
- Business-logic and app-specific auth/IDOR bugs are the most common genuine novelties (no
  public signature exists for a custom app) — but still walk the tree.
