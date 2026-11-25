---
name: aem-sonar
description: SonarCloud code quality review — complexity, duplication, null safety, resource leaks, security hotspots
allowed-tools: Read, Grep, Glob
argument-hint: "[file or class path]"
model: haiku
---

Review `$ARGUMENTS` for SonarCloud-style code quality issues. Report each finding as **Blocking** / **Warning** / **Suggestion**.

**Reliability**
- `ResourceResolver`, `Session`, or stream not closed in all code paths — Blocking
- Exception caught and silently swallowed (empty catch or log-only) — Warning
- Conditions that are always true or always false — Warning

**Security hotspots**
- Hardcoded credentials or tokens — Blocking
- Query built from concatenated user input — Blocking
- Path traversal risk from unvalidated input — Blocking

**Maintainability**
- Cognitive complexity too high — deeply nested conditionals, method over ~30 lines — Warning
- Duplicated logic that should be extracted — Suggestion
- Dead code, unused imports, fields, or parameters — Warning
- Magic numbers or string literals that should be named constants — Suggestion
- Method doing too many unrelated things (single responsibility) — Warning
