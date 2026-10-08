---
name: create-tests
description: "Deprecated alias for create-yaml-tests. Renamed to create-yaml-tests; this entry only redirects for backward compatibility. Use create-yaml-tests to create, update, and repair local Shiplight YAML E2E tests."
---

# Create Tests (renamed)

This skill was renamed to **`create-yaml-tests`**. `create-tests` is kept only as
a backward-compatible alias.

Use the `create-yaml-tests` skill instead — it is the single entry point for
Shiplight YAML E2E test work (project setup, specs, auth setup, YAML
implementation, validation, and maintenance), and it owns the reference guides
(`project-layout.md`, `workflow.md`, `test-implementation-guide.md`,
`ci.md`, and the others).

If `create-yaml-tests` is installed, switch to it now. If it is not installed,
add it:

```bash
npx skills add ShiplightAI/agent-skills --skill create-yaml-tests
```
