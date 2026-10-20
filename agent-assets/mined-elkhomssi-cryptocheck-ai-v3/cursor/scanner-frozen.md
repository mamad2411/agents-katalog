---
description: Scanner core files are frozen — never modify
globs: ["lib/services/scanner-engine.ts", "lib/services/scanner/pipeline/run-institutional-scan.ts", "lib/sentinel/canonical-scan.ts"]
alwaysApply: true
---

# FROZEN — do not edit

This file is part of the frozen scanner core.
All changes to scan logic must go through lib/connect/scan-gateway.ts (Phase 3).
Modifying this file risks breaking the entire risk pipeline without a clear rollback path.
If you believe an edit is necessary: open a discussion in the PR, do not edit directly.
