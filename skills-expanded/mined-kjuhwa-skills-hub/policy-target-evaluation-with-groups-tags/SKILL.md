---
tags: [backend, policy, target, evaluation, with, groups]
name: policy-target-evaluation-with-groups-tags
description: Evaluate whether a resource matches a policy via direct IDs + static/dynamic groups + tag filters, with explicit exclusion rules that take precedence over includes.
trigger: Policy targeting must support direct IDs, static groups, dynamic (tag-filter) groups, and exclusions, and decide membership per resource.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Policy Target Evaluation (Groups + Tags + Exclusions)

## Shape

Policy carries symmetric include/exclude selector fields:

```
target{ConfIds, ResourceIds, GroupIds, TagFilters}
excluded{ConfIds, ResourceIds, GroupIds, TagFilters}
```

Per-resource evaluator pre-resolves SMART (tag-based) group memberships, then applies **exclusion-wins** semantics before include checks.

## Steps

1. Pre-resolve SMART groups: for each target/excluded smart group, query resourceIds whose tags satisfy the group's tag expression. Cache per evaluation pass.
2. For each candidate config, call `evaluateConf(conf, groupMap, smartGroupMap, targetTagResults, excludedTagResults)`.
3. **Exclusion wins first**: reject if
   - `confId ∈ excludedConfIds` OR
   - `resourceId ∈ excludedResourceIds` OR
   - conf in any `excludedGroup` (SYSTEM membership or SMART match) OR
   - conf matches `excludedTagFilter`.
4. Include check:
   - `confId ∈ targetConfIds` OR
   - `resourceId ∈ targetSmartResourceIds` OR
   - conf in any `targetGroup` (SYSTEM or SMART) OR
   - conf matches `targetTagFilter`.
5. If both include and `targetTagFilters` are present, apply with AND (tag filter narrows the include set).
6. Diff resolved target set vs existing proxy/child definitions: create missing, remove stale.
7. Cache smart-group memberships with an `updatedAt` timestamp; invalidate on relevant tag/config change-stream events.

## Counter / Caveats

- Document **exclusion-wins** prominently — users often expect include-wins semantics.
- SMART group memberships change as tags change; invalidate cache on relevant field-level change-stream events only, not every document update.
- Empty target set + non-empty excluded set is a no-op (nothing to exclude from).
- Diff step must be idempotent; a mid-run crash should not leave duplicate proxy definitions.
