---
description: Scaffold a new package-manager driver under internal/driver
argument-hint: <package-manager-name>
---

Add a new cacheriff driver for the package manager: $ARGUMENTS

Follow the `add-package-manager-driver` skill (`.agents/skills/add-package-manager-driver/SKILL.md`)
step by step: read `internal/driver/driver.go` and `internal/driver/base.go`
first, pick the closest existing driver as a reference, then create
`internal/driver/<name>.go`, register it in `All()`, add
`internal/driver/<name>_test.go`, and finish by running the checks from
`/check`.
