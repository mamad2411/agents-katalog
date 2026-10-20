# Sync Documentation

Ensure documentation is aligned with code and no drift has occurred.

## Instructions

### 1. Check Implementation Status

Compare `docs/todo/current_work.md` with actual state:
- Are all tasks marked complete actually done?
- Any tasks added during implementation?
- Update task list to reflect reality

### 2. Verify Doc/Code Alignment

For each document type, check alignment:

#### docs/need/
- Do constraints still apply?
- Any new user needs discovered?

#### docs/spec/
- Features match implementation?
- Acceptance criteria met?
- Update feature status (planned → implemented)

#### docs/tech/
- Architecture docs match code?
- Schema docs match actual schema?
- Instructions still accurate?

### 3. Check for Drift

Look for common drift patterns:

| Drift Type | Detection | Fix |
|------------|-----------|-----|
| Undocumented feature | Code exists, no spec | Add spec |
| Stale spec | Spec differs from code | Update spec |
| Dead code | Spec removed, code remains | Remove code or restore spec |
| Missing test | Feature exists, no test doc | Document test |

### 4. Update Affected Docs

For each doc that needs updating:
1. Show the required change
2. Make the update
3. Add changelog entry if significant

### 5. Clean Up

- Archive completed `docs/todo/current_work.md` entries
- Update `docs/tech/IMPLEMENTATION_STATUS.md`
- Clear TodoWrite of completed items

### 6. Report

```
## Sync Report

### Documentation Updated
- docs/spec/PRODUCT_SPEC.md - Added feature X
- docs/tech/DATA_SCHEMA.md - Updated schema

### Drift Found and Fixed
- <description of drift and fix>

### Current State
All docs aligned with code: YES / NO

### Recommended Actions
- <any follow-up needed>
```

## Alignment Checks

### Schema Alignment
```bash
# Compare schema docs with actual data
grep -r "sd\|ed\|ev\|src" docs/tech/DATA_SCHEMA.md
grep -r "sd\|ed\|ev\|src" scripts/normalize/base.py
```

### Feature Status
Check each `docs/spec/feat_*/` directory:
- Has spec.md with status?
- Status matches implementation?

### Pipeline Alignment
```bash
# Check if pipeline stages match docs
PYTHONPATH=scripts python3 scripts/pipeline.py --list
```

## Changelog Format

When making significant doc updates, add to the doc:

```markdown
## Changelog

### YYYY-MM-DD
- Added: <what was added>
- Changed: <what changed>
- Deprecated: <what's deprecated>
```
