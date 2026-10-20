# Test Changes

Run tests and fix any failures.

**Skills to invoke** (use the `Skill` tool):
- `python-testing` — before writing or running pytest suites
- `verification-loop` — systematic end-to-end verification checklist after tests pass

## Instructions

### 1. Identify Required Tests

Based on what changed, determine which tests to run:

| Change Type | Tests to Run |
|-------------|--------------|
| Frontend JS | `node --check frontend/app.js`, browser console |
| Python scripts | `python -m py_compile <file>`, unit tests |
| Data pipeline | `PYTHONPATH=scripts python3 scripts/pipeline.py --stage <stage>` |
| Docker config | `docker compose config`, `docker compose up` |
| Full system | `PYTHONPATH=scripts python3 -m pytest tests/ -v` + `./scripts/validate_phase1.sh` |

### 2. Run Tests in Parallel

Launch test agents:
```
Agent 1: Syntax validation (node --check, python -m py_compile)
Agent 2: Unit tests (if any)
Agent 3: Integration tests
Agent 4: Manual verification steps
```

### 3. Collect Results

```
## Test Results

### Passed
- [x] JavaScript syntax valid
- [x] Python syntax valid
- [x] Docker compose valid

### Failed
- [ ] MapLibre filter error: <details>
- [ ] Pipeline stage failed: <details>

### Manual Checks Needed
- [ ] Open http://localhost:8080 and verify UI
- [ ] Check browser console for errors
```

### 4. Fix Failures

For each failure:
1. Diagnose the root cause
2. Propose fix
3. Apply fix
4. Re-run specific test

Repeat until all tests pass.

### 5. Final Validation

Run the full validation suite:
```bash
PYTHONPATH=scripts python3 -m pytest tests/ -v
./scripts/validate_phase1.sh  # artifact existence checks
```

### 6. Report

```
## Test Summary

All tests passing: YES / NO

### Changes Made to Fix
- Fixed MapLibre filter syntax at app.js:720
- Updated schema validation in pipeline.py

### Ready for Commit
Run `/sync` to ensure docs are updated, then commit.
```

## Common Test Commands

```bash
# JavaScript
node --check frontend/app.js

# Python syntax
python3 -m py_compile scripts/pipeline.py

# Python imports
python3 -c "from scripts.normalize.normalize_manual import Normalizer"

# Docker
docker compose config
docker compose up -d && sleep 2 && curl -s http://localhost:8080/ | head -1

# Server health
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/

# Full validation
PYTHONPATH=scripts python3 -m pytest tests/ -v
```

## Browser Testing Checklist

If frontend changed:
- [ ] Page loads without errors
- [ ] No console errors
- [ ] Time slider works
- [ ] Source filter works
- [ ] Map renders correctly
- [ ] Layers toggle properly
