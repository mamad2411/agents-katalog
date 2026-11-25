---
name: scala-check
description: Run full Scala verification pipeline (compile, scalafmt, test)
user_invocable: true
---

# Scala Check Skill

Run the complete Scala 3 / ZIO 2 verification pipeline for the current project.

## Steps

1. Run `sbt compile` to verify compilation (with `-Xfatal-warnings` if configured)
2. Run `sbt scalafmtCheckAll` to verify formatting
3. Run `sbt test` to run the test suite

## Instructions

Execute each step sequentially. If any step fails, report the failure clearly with the relevant output and stop. Do not proceed to later steps if an earlier one fails (except: if scalafmtCheckAll fails, offer to auto-fix with `sbt scalafmtAll`, then continue).

Report results in this format:

```
## Scala Check Results

| Step | Status | Details |
|------|--------|---------|
| sbt compile | PASS/FAIL | ... |
| sbt scalafmtCheckAll | PASS/FAIL | ... |
| sbt test | PASS/FAIL | N tests passed, M failed |
```

If all steps pass, report success. If any step fails, summarize what needs to be fixed.
