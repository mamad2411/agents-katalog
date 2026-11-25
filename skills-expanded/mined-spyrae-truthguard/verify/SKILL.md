---
name: verify
description: Run real verification — tests, type checks, and linting
allowed-tools: Bash
---

Run actual verification checks on the current project. Do NOT simulate or guess results — execute real commands and report their actual output.

## Steps

1. Check for `.truthguard.yml` in the working directory. If `test_command` is set, use it instead of auto-detection.

2. Auto-detect the project type from the working directory and run the appropriate checks:

### Tests
- `.truthguard.yml` with `test_command` → use that command
- `pubspec.yaml` → `flutter test`
- `package.json` with test script → `npm test`
- `pyproject.toml` / `pytest.ini` → `python -m pytest`
- `Cargo.toml` → `cargo test`
- `go.mod` → `go test ./...`
- `Makefile` with `test:` target → `make test`

### Type Checks
- TypeScript (`tsconfig.json`) → `npx tsc --noEmit`
- Python (mypy installed) → `python -m mypy .`
- Dart (`pubspec.yaml`) → `flutter analyze`
- Go (`go.mod`) → `go vet ./...`
- Rust (`Cargo.toml`) → `cargo check`

### Linting
- TypeScript/JS (`.eslintrc*` or `eslint.config*`) → `npx eslint .`
- Python (ruff installed) → `python -m ruff check .`
- Dart → `dart analyze`
- Rust → `cargo clippy`
- Go → `golangci-lint run` (if installed)

3. Report the REAL output from each command. Format:

```
🛡️ TruthGuard Verify
━━━━━━━━━━━━━━━━━━━
✅ Tests: 42 passed, 0 failed
⚠️ TypeCheck: 2 errors in src/utils.ts
✅ Lint: clean
```

4. Log the verification run:
```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) verify" >> "${TRUTHGUARD_LOG:-$HOME/.truthguard/session.log}"
```

CRITICAL: Never fabricate results. If a check fails, report the failure honestly.
