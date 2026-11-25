---
name: rust-check
description: Run full Rust verification pipeline (fmt, clippy, test, deny)
user_invocable: true
---

# Rust Check Skill

Run the complete Rust verification pipeline for the current project.

## Steps

1. Run `cargo fmt --check` to verify formatting (if it fails, offer to run `cargo fmt` to fix)
2. Run `cargo clippy -- -D warnings` to check for lint violations
3. Run `cargo test` to run the test suite
4. Run `cargo deny check` if a `deny.toml` exists in the project

## Instructions

Execute each step sequentially. If any step fails, report the failure clearly with the relevant output and stop. Do not proceed to later steps if an earlier one fails (except: if fmt --check fails, offer to auto-fix with `cargo fmt`, then continue).

Report results in this format:

```
## Rust Check Results

| Step | Status | Details |
|------|--------|---------|
| cargo fmt | PASS/FAIL | ... |
| cargo clippy | PASS/FAIL | ... |
| cargo test | PASS/FAIL | N tests passed, M failed |
| cargo deny | PASS/FAIL/SKIPPED | ... |
```

If all steps pass, report success. If any step fails, summarize what needs to be fixed.
