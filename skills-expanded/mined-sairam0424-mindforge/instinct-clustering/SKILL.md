---
name: instinct-clustering
version: 1.0.0
min_mindforge_version: 10.0.5
status: stable
triggers: instinct cluster, cluster instincts, group instincts, batch promote, instinct groups, pattern clusters, behavior clusters, auto-group, merge instincts, combine instincts, related patterns, instinct merge
---

# Skill — Instinct Clustering (Auto-Group & Batch Promote Instincts)

## When this skill activates

When the instinct store has accumulated enough patterns that manual promotion to
skills becomes impractical. Use to automatically identify groups of related instincts,
deduplicate redundant entries, and batch-promote coherent clusters into full skills.
Converts organic behavioral patterns into structured, reusable skill definitions.

Core principle: **Emergent structure** — let clusters form from the data rather than
imposing categories top-down. Instincts that repeatedly co-occur reveal natural
skill boundaries.

## Mandatory actions when this skill is active

### Before clustering begins

1. **Load and filter instinct store:**
   - Read `instinct-store.jsonl` (or configured instinct storage path)
   - Filter to active instincts only (`status == "active"`)
   - Exclude instincts with `confidence < 0.3` (too uncertain to cluster)
   - Record total count: `N active instincts loaded`

2. **Validate minimum viable dataset:**
   - Minimum 10 active instincts required for meaningful clustering
   - If < 10: report "insufficient instincts for clustering" and exit
   - If 10-20: expect 1-3 clusters
   - If 20-50: expect 3-8 clusters
   - If 50+: expect 5-15 clusters

3. **Understand instinct schema:**
   ```json
   {
     "id": "inst-uuid",
     "observation": "what was observed (natural language)",
     "behavior": "what action to take (imperative)",
     "tags": ["tag1", "tag2", "tag3"],
     "confidence": 0.0-1.0,
     "frequency": 0,
     "project_scope": "global" | "project-name",
     "status": "active" | "promoted" | "deprecated",
     "created_at": "ISO-8601",
     "last_triggered": "ISO-8601"
   }
   ```

### During clustering

**Step 1 — Deduplication pass:**
- For each pair of instincts, compute observation word overlap:
  - Tokenize observations (lowercase, remove stop words)
  - Overlap = |intersection| / |union| (jaccard on word sets)
- If overlap > 0.8: merge the pair (keep the one with higher confidence)
- Log all merges: `"Merged inst-X into inst-Y (overlap: Z%)""`
- Record: `D duplicates removed, M instincts remaining`

**Step 2 — Tag overlap calculation:**
- For each remaining pair of instincts, compute tag jaccard similarity:
  ```
  jaccard(A, B) = |A.tags intersection B.tags| / |A.tags union B.tags|
  ```
- Build a similarity matrix: instincts (rows) x instincts (columns)
- Store as adjacency list for efficiency (only pairs with jaccard > 0.3)

**Step 3 — Cluster formation:**
- Group instincts where:
  - Tag jaccard > 0.5 (strong tag overlap)
  - AND shared `project_scope` (both global, or both same project)
- Use single-linkage clustering: if A is similar to B and B is similar to C,
  then {A, B, C} form a cluster (even if A and C are not directly similar)
- Cap cluster size at 10 instincts (larger clusters should be split)

**Step 4 — Filter clusters:**
- Minimum cluster size: 3 instincts (smaller groups are not worth promoting)
- Average confidence across cluster members must be > 0.7
- At least 2 distinct observations in the cluster (not all near-duplicates)
- Discard clusters that fail any filter

**Step 5 — Skill generation per cluster:**
- **Name**: derived from the 2-3 most common tags across cluster members
- **Triggers**: extracted from observation keywords (deduplicated, natural phrasing)
- **Behavior**: combine all instinct `behavior` fields in logical order:
  1. Sort by frequency (most-triggered instincts first)
  2. Remove redundant steps
  3. Organize into Before/During/After structure
- **Self-check**: synthesize from the cluster's collective edge cases

Generated skill structure:
```markdown
---
name: [derived-name]
version: 1.0.0
min_mindforge_version: 10.0.5
status: stable
triggers: [combined trigger keywords]
---

# Skill — [Name]

## When this skill activates
[Synthesized from cluster observations]

## Mandatory actions when this skill is active
### Before [derived from behaviors]
### During [derived from behaviors]
### After [derived from behaviors]

## Self-check before task completion
[Derived from cluster edge cases]
```

**Step 6 — Conflict detection:**
- Check generated triggers against MANIFEST.md
- If jaccard > 0.3 with existing skill triggers: flag conflict
- Resolution options: merge into existing skill, rename triggers, or keep separate with justification

### After clustering

1. **Present clusters for user review:**
   ```
   ## Cluster Report

   ### Cluster 1: [proposed-name]
   - Instincts: [count]
   - Avg confidence: [score]
   - Members: [list of instinct IDs with one-line observations]
   - Proposed skill name: [name]
   - Proposed triggers: [list]

   ### Cluster 2: ...

   ## Unclustered Instincts
   [Instincts that didn't fit any cluster — may need more data]
   ```

2. **On user approval:**
   - Create SKILL.md in `.mindforge/skills/[name]/`
   - Register in MANIFEST.md
   - Mark all clustered instincts as `status: "promoted"`
   - Add `promoted_to: "[skill-name]"` field to each promoted instinct
   - Append promotion event to audit log

3. **On user rejection or modification:**
   - Apply requested changes to cluster membership or skill definition
   - Re-validate filters (size >= 3, confidence > 0.7)
   - Re-check for trigger conflicts
   - Present revised version for approval

4. **Generate CLUSTER-REPORT.md:**
   ```markdown
   ## Instinct Clustering Report — [date]

   **Input:** N active instincts
   **After dedup:** M instincts (D removed)
   **Clusters formed:** C clusters
   **Clusters passing filters:** F clusters
   **Instincts promoted:** P
   **Instincts unclustered:** U

   ### Cluster Details
   [table: name, size, avg_confidence, proposed_skill, status]

   ### Deduplication Log
   [list of merged instinct pairs with overlap scores]

   ### Recommendations
   - [instincts close to clustering threshold — collect more data]
   - [potential trigger conflicts to monitor]
   ```

## Self-check before task completion

Before marking an instinct clustering task done:

- [ ] Did I deduplicate before clustering (overlap > 0.8 merged)?
- [ ] Did I verify minimum cluster size (3+ instincts per cluster)?
- [ ] Did I check average confidence > 0.7 for each cluster?
- [ ] Did I combine behaviors coherently (sorted by frequency, no redundancy)?
- [ ] Did I check for trigger conflicts against MANIFEST.md?
- [ ] Did I present clusters to the user for approval before creating skills?
- [ ] Did I mark promoted instincts with `status: "promoted"`?
- [ ] Did I generate CLUSTER-REPORT.md with full statistics?
