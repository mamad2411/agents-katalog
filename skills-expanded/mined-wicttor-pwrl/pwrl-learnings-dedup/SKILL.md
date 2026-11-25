---
name: pwrl-learnings-dedup
description: "Identify and merge duplicate or redundant learnings while preserving historical lineage."
argument-hint: "[structure artifact from pwrl-learnings-structure]"
---

# pwrl-learnings-dedup — Learning Deduplication

**Purpose:** Phase 4 of learnings workflow. Detects and merges duplicate or semantically similar learnings while preserving complete audit trails and source history. Maintains knowledge base quality and discoverability.

## Interaction Method

- Automated duplicate detection with fingerprinting.
- Flagged similarities (85%+) shown for user decision.
- Ask: "Merge these similar learnings? Yes/No/Keep separate"
- Show comparison before merging.
- No approval gate; proceed to save.

## Input: Structure Artifact

Expects artifact from `pwrl-learnings-structure` with:

```yaml
structure_id: YYYY-MM-DD-NNN-structure
learnings: [array of structured learnings with metadata]
```

## Output: Dedup Artifact

Emit dedup artifact (YAML + markdown):

```yaml
---
format: pwrl-learnings-dedup-artifact
version: "1.0"
dedup_id: YYYY-MM-DD-NNN-dedup
created: ISO-8601-timestamp
---

# Learning Deduplication Results

## Summary
- **Before Dedup:** [count] learnings
- **After Dedup:** [count] unique learnings
- **Duplicates Merged:** [count]
- **Archived:** [count]
- **Dedup Confidence:** [0-100%]

## Merge Actions

### Exact Merges: [count]
- [Learning A] merged into [Learning B]
- Preserved: sources, examples, tags from both

### High-Similarity Flagged: [count]
- [Learning C] similar to [Learning D] (94% match)
- User decision: merged | kept-separate

### Related Linked: [count]
- [Learning E] complements [Learning F]
- Cross-reference created

## Archived Mapping
- `OLD_ID_1` → `NEW_ID_1`
- `OLD_ID_2` → `NEW_ID_2`

## Ready for Save
- **Status:** ready
- **Next Skill:** pwrl-learnings-save
- **Artifacts Passed:** This dedup artifact + updated learnings
```

## Detailed Workflow

For complete step-by-step instructions, see [dedup-learnings-detailed-workflow.md](references/dedup-learnings-detailed-workflow.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Fingerprint calculation (exact, semantic, text similarity)
- Duplicate finding algorithm
- Merge strategy selection
- Merge algorithm with winner selection
- High-similarity flagging process
- Related learning linking
- Archive mapping with audit trail

## Duplicate Detection: Late Resolution

This phase performs final duplicate resolution using three fingerprinting strategies:

1. **Exact Fingerprint:** MD5(type + domain + title) → 95%+ confidence
2. **Semantic Fingerprint:** MD5(type + domain + problem + sorted_tags) → 85-95% confidence
3. **Text Similarity:** Cosine similarity of tokenized content → 70-95% confidence

See [duplicate-handling-consolidated.md](../pwrl-learnings/references/duplicate-handling-consolidated.md#late-duplicate-resolution-phase-4) for complete fingerprinting details.

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint learnings 4 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

Check input has valid `structure_id` and `learnings` array with complete metadata.

### Step 2: Calculate Fingerprints

**For each learning, generate three fingerprints:**

1. **Exact Fingerprint:** MD5(type + domain + title.lowercase.strip())
   - Detects identical learnings (copy-paste duplicates)

2. **Semantic Fingerprint:** MD5(type + domain + problem_hash + tags_sorted)
   - Detects same concept expressed differently

3. **Text Similarity:** Cosine similarity of (title + problem + tags)
   - Detects partially matching learnings
   - Threshold: 85% for "high similarity"

### Step 3: Find Duplicates

**Compare all fingerprints:**

```
For each pair (L1, L2):
  if exact_fingerprint(L1) == exact_fingerprint(L2):
    → Exact duplicate (auto-merge)

  elif semantic_fingerprint(L1) == semantic_fingerprint(L2):
    → Semantic duplicate (auto-merge)

  elif text_similarity(L1, L2) > 0.85:
    → High similarity (flag for review)

  elif related_tags(L1, L2) and type(L1) != type(L2):
    → Complementary learning (cross-reference)
```

### Step 4: Apply Merge Strategy

**Three strategies available:**

| Strategy | Behavior                                  | Confidence |
| -------- | ----------------------------------------- | ---------- |
| exact    | Only auto-merge exact/semantic duplicates | 95%+       |
| semantic | + flag high-similarity (85%+) for review  | 85-95%     |
| hybrid   | All of above + link related learnings     | 70-95%     |

Default: **hybrid** (recommended)

### Step 5: Merge Exact Duplicates

**For exact/semantic matches:**

1. **Choose winner:**
   - Most recent (newer `created_at`)
   - Most complete (longest `problem` + `application`)
   - Highest `applicability` score

2. **Preserve loser data:**
   - Append loser's tags to winner's tags (deduplicate)
   - Merge examples: `winner.examples.push(...loser.examples)`
   - Extend sources: `winner.sources.push(...loser.sources)`
   - Note: `merged_from: [loser.id]`

3. **Archive loser:**
   - Mark as `archived: true`
   - Set `merged_into: winner.id`
   - Keep for audit trail

**Example:**

```yaml
Winner: learning-id-1
  title: "Race Condition in Shared Cache"
  problem: "Multiple threads accessing cache without locking"
  tags: [concurrency, cache, threading]
  sources:
    - src/cache.ts:42
  examples: ["Reproducer code 1"]

Loser: learning-id-2
  title: "Race Condition - Cache Access"  # Similar but different
  problem: "Concurrent cache access causes data corruption"
  tags: [concurrency, cache]  # Subset of winner's
  sources:
    - src/old-cache.ts:20
  examples: ["Reproducer code 2"]

Result: learning-id-1 (winner)
  title: "Race Condition in Shared Cache"
  problem: "Multiple threads accessing cache without locking, causing data corruption"
  tags: [concurrency, cache, threading]  # Merged + deduped
  sources:
    - src/cache.ts:42
    - src/old-cache.ts:20  # Both preserved
  examples:
    - "Reproducer code 1"
    - "Reproducer code 2"  # Both preserved
  merged_from: [learning-id-2]
  merged_at: 2026-06-12T10:30:00Z
```

### Step 6: Flag High-Similarity Matches

**For 85%+ similarity (non-exact):**

1. **Display to user:**

   ```
   High Similarity Match (91%)

   Learning A: "React Hook Dependency Gotcha"
   Learning B: "React Hooks - Dependency Array Gotcha"

   Should these be merged? Yes / No / Keep separate
   ```

2. **User decides:**
   - **Yes:** Merge like exact duplicate
   - **No:** Keep separate; no cross-reference
   - **Keep separate:** Mark with cross-reference

### Step 7: Link Related Learnings

**For complementary learnings:**

```yaml
Learning: "Race Condition Gotcha"
Related:
  - [prevents]: "Mutex Usage Pattern"
  - [complements]: "Immutable Data Structures"
```

### Step 8: Generate Dedup Artifact

Emit artifact with:

- Exact merges count
- Flagged similarities
- Related links
- Archived mapping (old_id → new_id)
- Updated learning list
- Quality metrics

## Error Handling

| Error                         | Recovery                                         |
| ----------------------------- | ------------------------------------------------ |
| Structure artifact invalid    | Return error; direct to pwrl-learnings-structure |
| Fingerprint calculation fails | Skip that learning; continue with others         |
| User can't decide             | Default: keep separate; add cross-reference      |
| Merge conflicts               | Manual merge; preserve all data                  |

## Testing Coverage

Test file: `tests/pwrl-learnings/dedup-learnings.test.ts`

**Happy Path Tests:**

- ✅ Exact duplicate (auto-merged)
- ✅ Semantic duplicate (auto-merged)
- ✅ High similarity (flagged, user chooses)
- ✅ Related learnings (cross-referenced)
- ✅ No duplicates (all kept)

**Edge Cases:**

- ✅ Conflicting metadata (merged correctly)
- ✅ Multiple duplicates of same learning (all merged to one)
- ✅ Circular relationships (handled)
- ✅ User decision flip (corrected)

**Output Validation Tests:**

- ✅ Archived mapping complete
- ✅ Winner selection correct
- ✅ Data preserved (no loss)
- ✅ Confidence score accurate
