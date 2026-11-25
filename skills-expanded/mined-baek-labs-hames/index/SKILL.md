---
name: index
description: Check whether workspace files are indexed and follow their configured folder, naming, and document rules when the user invokes /index or asks to audit file organization.
---

# Index

Use the user's language. Resolve the configured AI work root and read its configuration. An unconfigured root needs `/setup`; do not invent folders or rules.

Run the bundled `runtime/index.js audit --root <root>` (optionally `--target <workspace-id-or-relative-path>`). With no target, inspect every registered workspace and shared root `docs/`.

This is a read-only audit. Report the checked and excluded scope, violations, items needing judgment, and unreadable or unsupported items separately. Do not call everything healthy when any judgment or unreadable item remains. For each finding show its path, observed fact, rule, and suggested action. Semantic rules require reading the relevant content; check uncertainty with the user, never pretend a path check proves meaning.

File creation's automatic index update is a separate hook operation. An audit must not repair indexes, move documents, rename files, or delete anything.

For a user-requested index repair, run `runtime/index.js plan --root <root>`, present the exact proposed index changes, and retain its `plan_hash`. Only after that repair is authorized, run `runtime/index.js apply --root <root> --approved --plan-hash <hash>`. This repairs index blocks only; moving or editing the original documents requires a separate specific request. Re-audit afterward. A changed preview must be presented again.

Preserve manual text and links. Report broken manual references instead of silently rewriting them. Indexing failure never authorizes deleting the original file. Shell and external-app changes may only be discovered during the next audit; no background filesystem watcher is installed.
