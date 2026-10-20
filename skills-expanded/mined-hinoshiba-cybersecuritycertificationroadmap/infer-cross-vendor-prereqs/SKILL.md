---
name: infer-cross-vendor-prereqs
description: Curate cross-vendor "commonly taken before" recommendations based on community / industry reputation. Adds entries to prerequisites.recommended_certs[] tagged with source "community" and a one-sentence rationale. Distinct from infer-relationships (which only handles official ladders).
---

# infer-cross-vendor-prereqs

## When to use

- Periodically (monthly) to refresh community-reputation edges as the
  certification ecosystem evolves.
- After adding a substantial new vendor / family of certs (e.g., a new
  cloud provider, a new training platform like HackTheBox / TCM Security)
  where reputation-based connections to existing certs need explicit
  encoding.
- After issues report a missing common-knowledge connection (e.g.,
  "everyone knows X is a stepping stone to Y but the roadmap doesn't
  show it").

## What this skill is for

Many useful prerequisite relationships are NOT documented officially
anywhere. They are common knowledge in the security community:

- Holders of SEA/J CSBM frequently study for IPA SC next, because the
  management-track content overlaps directly.
- CompTIA Security+ is widely used as a prep foundation for ISC2 CISSP.
- EC-Council CEH → OffSec OSCP is the canonical "theory → hands-on"
  progression.
- IPA AP holders in Japan often pursue CISSP as their first
  international cert, because AP's 8-domain coverage maps onto CISSP's.

These connections are real and useful for learners planning a path,
but they are NOT part of any vendor's documentation, so the
`infer-relationships` skill does not propose them. This skill
**deliberately encodes community knowledge**, marked as such with
`source: "community"` so renderers can display official > community
priority and learners can judge weight accordingly.

## What this skill is NOT for

- **Hard prerequisites.** Those go in `prerequisites.required_certs[]`
  (different field) and are populated by `add-cert` / `update-cert`
  from official vendor docs.
- **Vendor-internal ladders.** Same-vendor / shared-domain progression
  is `infer-relationships`'s job, tagged `source: "vendor-ladder"`.
- **Vendor-stated recommendations.** When a vendor explicitly says "we
  recommend cert X before this one", that goes in the
  `OFFICIAL_RECOMMENDED_FLOWS` whitelist of
  `scripts/infer_relationships.py`, tagged `source: "official-recommended"`.

## Provenance & priority order

When the renderer caps the displayed graph (see "Display cap" below), it
preserves entries in this priority order:

1. `required_certs[]` — always shown
2. `recommended_certs[].source == "official-recommended"`
3. `recommended_certs[].source == "vendor-ladder"`
4. `recommended_certs[].source == "community"`  ← what THIS skill writes

A `community` edge MUST NEVER overwrite a higher-priority edge to the
same source-target pair. The `add_community_relationships.py` script
enforces this; if invoked manually, follow the same rule.

## Workflow

1. Read all certs in `data/certs/**/*.json`. Build the set of cert IDs.
2. For each candidate (src, tgt) edge you intend to propose:
   - Skip if `src` or `tgt` doesn't exist in the roadmap.
   - Skip if `src` is already in `tgt.prerequisites.required_certs[]`.
   - Skip if `src` is already in `tgt.prerequisites.recommended_certs[]`
     (regardless of source — community never overrides).
3. Append the new entry:
   ```json
   {
     "id": "<src cert id>",
     "source": "community",
     "rationale": "<one-sentence explanation of WHY this community knowledge exists, citing the overlap or career pattern. Japanese for JP-ecosystem edges, English otherwise.>"
   }
   ```
4. Run `python3 scripts/build_manifest.py` to refresh the manifest.
5. Run `python3 scripts/run_3_persona_eval.py` only if tier-relevant
   facts changed (community edges typically don't affect tier).

## Concrete script

`scripts/add_community_relationships.py` holds the curated
`COMMUNITY_FLOWS` list. To add new edges, append to that list and
re-run:

```sh
python3 scripts/add_community_relationships.py --dry-run
python3 scripts/add_community_relationships.py
python3 scripts/build_manifest.py
```

## Quality bar for rationale strings

A good rationale answers "why does this community knowledge exist?":

  ✅ "応用情報技術者 (AP) の出題範囲は CISSP 8 ドメインの相当部分を国内向けに先取り。CISSP の下地として国内エンジニアが選ぶ定番。"
  ✅ "CySA+ で SOC アナリストの素養を得てから GCIH で SANS グレードのインシデントハンドリング深度へ。"

Bad rationales are vague:

  ❌ "Often taken before."
  ❌ "Good study path."
  ❌ "前提として人気。" (no explanation of the overlap)

## Display cap

The roadmap UI caps total visible arrows at 20 per selected cert. When
exceeding, the renderer drops entries in REVERSE priority order:
community first, then vendor-ladder, then official-recommended.
`required_certs` are never dropped. This means:

- A cert with many community edges still has its required + official
  edges shown clearly.
- Adding a marginal community edge has near-zero risk of cluttering
  the display, because the renderer already culls aggressively.

Therefore: err on the side of including a high-quality, well-rationalized
community edge. The display layer is the line of defense against
overwhelming the user.

## Persistence

`COMMUNITY_FLOWS` lives in `scripts/add_community_relationships.py`,
not in a separate JSON, because each entry is a triple
`(src, tgt, rationale)` and the rationale is the value-add — the script
file is more maintainable than YAML / JSON for prose-heavy data.

The script is idempotent: running it twice produces no additional
diffs. Re-runs are safe after each `infer-relationships` pass to
re-apply community edges that the vendor-ladder pass might have
proposed (in which case community is suppressed in favor of the
stronger source).
