---
name: infer-relationships
description: Propose prerequisite cert relationships across the entire roadmap from neutral AI analysis of cert facts. Both within-vendor ladders and cross-vendor industry-conventional flows are in scope.
---

# infer-relationships

## When to use

- Right after `add-cert` writes a new cert, to suggest its `prerequisites.recommended_certs[]` from the existing graph (rather than relying on the official page alone).
- Periodically (e.g. monthly) to fill in gaps where prereq edges were missed.
- Whenever a tier rubric / persona change reshapes the graph.

## Inputs

- All cert files under `data/certs/**/*.json`
- `data/tiers.json` (rubric + tier ordering)
- `data/domains.json`

## What "neutral AI analysis" means here

This skill is the only place where prerequisite edges are *generated* (vs.
*verified*). The judgment must be defensible from the JSON facts alone, not
from external opinion. Use these signals, in order:

1. **Same-vendor ladder.** If two certs share a `vendor.slug` and one is
   strictly higher tier with overlapping primary domain, the lower one is a
   prereq candidate. Example: `offsec.oscp` → `offsec.osep`,
   `microsoft.sc-300` → `microsoft.sc-100`.
2. **Officially-stated recommendation.** If the cert's `prerequisites.recommended_certs[]`
   already lists an id, KEEP it; the official source said so.
3. **Experience-year delta.** If cert A requires N years and cert B
   requires ≥ N+2 years in the same primary domain (or shared secondary),
   A is a candidate prereq for B.
4. **Cross-vendor industry-conventional flow.** Whitelist of well-known
   pairings the AI should *propose* but the maintainer should review:
   - `comptia.security-plus` → many associate-tier security certs
   - `comptia.network-plus` → `comptia.security-plus` →
     `comptia.cysa-plus` / `comptia.pentest-plus`
   - `isc2.cissp` → `isc2.ccsp`, `isc2.issap`, `isc2.issep`, `isc2.issmp`,
     `isc2.csslp`
   - `offsec.oscp` → `offsec.osep` / `offsec.oswe` / `offsec.osed`
   - `offsec.osed` → `offsec.osee`
   - `offsec.osda` → `offsec.osth`, `offsec.osir`
   - `comptia.security-plus` → `isc2.cc` (entry literacy continuation)
   - `comptia.network-plus` → `cisco.cyberops-associate`
   - IPA ladder: `ipa.ip` → `ipa.fe` → `ipa.ap` → SC / NW / DB / ES /
     SA / PM / AU / ST / SM (per IPA's published "skill level" ladder)
   - SEA/J ladder: `seaj.csbm` → `seaj.cspm-management` and `seaj.csbm`
     → `seaj.cspm-technical`
5. **Tier-skip refusal.** Do NOT propose a foundational cert as a direct
   prereq of an expert cert when an associate or professional cert
   already serves as the explicit step.
6. **Same-domain affinity.** Of two candidates at equal tier, prefer the
   one whose primary domain matches the target's primary domain.

## Process

1. Load every cert into memory.
2. For each cert C, build a candidate prereq set using rules 1-4 above.
   Apply rules 5-6 to prune.
3. **Diff against the existing `prerequisites.recommended_certs[]`**: list
   adds and removes per cert.
4. **Open a single PR** (or print a report if running in dry-run mode)
   titled `infer-relationships: <N> proposed edges`. The PR body must be
   organised by vendor and clearly label each edge as `same-vendor`,
   `cross-vendor`, or `inverse-experience-delta` so reviewers can audit.
5. The maintainer reviews, can edit individual files to drop unwanted
   edges, and merges. The roadmap UI redraws arrows from the new graph.

## Refusal conditions

- A proposed edge would create a cycle (A → B and B → A): refuse and
  flag both certs for human review.
- A cross-vendor edge that has no industry-conventional support and
  isn't supported by experience-year deltas or domain affinity: skip
  (the goal is "AI proposes the obvious", not "AI invents flows").

## Implementation

`scripts/infer_relationships.py` is the executable form. Run it with
`python3 scripts/infer_relationships.py --dry-run` to see the proposed
diff, or without `--dry-run` to write the edges into the cert JSONs and
re-run the manifest + persona evaluation skills.

## Anti-goal

This skill must NOT silently rewrite the prereq graph in production.
Every change is reviewable as a diff. The skill's value is *proposing*
edges; merging them is a human (or maintainer-run) decision.
