---
name: map-classifier
description: Classifies every row of a Fetchproof project's research/MAP.md as COVERED (citing U-## rows), DISMISSED (with a reason) or GAP, checking output obtainability first, and adds the topic-specific subtopics the universal checklist misses. Use on a collector after decompose drafts the map, when preflight reports subtopic-coverage findings, or when the user asks to classify, review or finish the map.
---

# Map classifier

`decompose.mjs` hands over a checklist with every status blank. Classifying it is the
first review step of phase 1, and it is judged by what it leaves behind: the
`subtopic-coverage` check fails a GAP row, a DISMISSED row without a reason, and a COVERED
row citing an unknown that does not exist.

## Order

1. **D-9 output obtainability, first.** Does the data the stated "done" depends on exist,
   and can it be obtained? If not, the project dies here, in phase 1 - say so before
   classifying anything else.
2. The other universal rows: access model, auth, rate limits, ToS and licensing, schema
   stability, freshness, cost at volume, runtime limits.
3. **Topic rows** (`S-1`, `S-2`, ...): what the checklist does not ask about this topic.

## Each row

- **COVERED** - cite the `U-##` rows in `research/DISCOVERY.md` that close it. Write the
  unknown first if it does not exist yet; every unknown traces back to a row.
- **DISMISSED** - one sentence why it does not apply here ("public pages, no account").
  Dismissing is fine; omitting is not.
- **GAP** - it applies and nothing covers it yet. The gate fails until it is covered or
  dismissed, which is the point.

Write one line per row under **Coverage notes**: what it rests on.

## Rules

- A row is never left blank and never deleted.
- A dismissal is a reason, not a shrug: "not relevant" is not a reason.
