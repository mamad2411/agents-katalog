---
name: gbrain-maintain
description: Periodic brain maintenance. Finds contradictions, stale info, orphan pages, and missing cross-references to keep the knowledge graph healthy.
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: [gbrain]
---

# Maintain Skill

Run these checks periodically (every few days).

## Lint checks

### 1. Contradictions
- Compare State sections across linked pages
- Flag: Page A says "CEO of X" but Page B says "left X in 2025"
- Resolution: check timeline entries for latest evidence, update the stale page

### 2. Stale info
```bash
gbrain list --type person  # check for pages with old compiled_truth
gbrain timeline <slug>     # are there timeline entries newer than the State section?
```
- Flag pages where State hasn't been updated but timeline has new entries
- Rewrite compiled_truth from latest timeline evidence

### 3. Orphan pages
```bash
gbrain list  # for each slug:
gbrain backlinks <slug>  # zero inbound links = orphan
```
- Either add links from related pages, or flag for deletion

### 4. Missing cross-references
- Scan compiled_truth for mentions of known page titles that aren't linked
- "Jane mentioned Acme Corp" but no link to companies/acme-corp → add it

### 5. Dead links
- For each link, verify both pages still exist
- Remove links to deleted pages

### 6. Open thread audit
- Pages with Open Threads items older than 30 days → flag for review
- Resolved items still in Open Threads → move to timeline

### 7. Tag consistency
```bash
gbrain call brain_stats '{}'  # check tag counts
```
- Flag near-duplicates: "yc-alum" vs "yc_alum" vs "yc alum"
- Normalize: lowercase, hyphens

### 8. Embedding freshness
```bash
gbrain embed --stale  # re-embed pages updated since last embedding run
```

## Output

Write a maintenance report:
```bash
cat report.md | gbrain put sources/maintenance-$(date +%Y-%m-%d)
```

Include: findings, actions taken, pages updated, issues flagged.
