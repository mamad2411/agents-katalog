---
name: review-collection
description: Review an existing Ansible collection and produce a structured severity report grouped by CRITICAL, WARNING, and INFO. Triggered by /review-collection. Checks galaxy.yml completeness, directory structure, required files, meta/runtime.yml, and role quality. NEVER modifies files.
---

# review-collection

Review an Ansible collection and produce a structured severity report. This command never modifies files.

---

## Required Inputs

1. **collection identification** — `namespace.name` or path to collection root (resolved from discovery if not provided)

---

## Behavior

### Step 1 — Discovery
Run discovery per `references/discovery.md`. Locate the collection:
- By `namespace.name` in `collections_path` directories
- By path if provided directly

### Step 2 — Load Collection
Read `galaxy.yml`, `meta/runtime.yml`, `README.md`, `CHANGELOG.md`, `LICENSE`.
Scan `plugins/`, `roles/`, `playbooks/`, `tests/` directories.

### Step 3 — Generate Severity Report

```
## Collection Review: <namespace>.<name>
Path: <collection_path>
Version: <version>
Reviewed: <timestamp>

---

### CRITICAL
[Critical issues]

### WARNING
[Warnings]

### INFO
[Informational notes]

---
Summary: <X> critical, <Y> warnings, <Z> info
```

---

## Checks to Perform

### CRITICAL

| Check | Condition | Message |
|-------|-----------|---------|
| galaxy.yml missing | File does not exist | `CRITICAL: galaxy.yml is missing — collection is not valid without it` |
| galaxy.yml: namespace missing | `namespace` field absent or empty | `[galaxy.yml] Required field 'namespace' is missing` |
| galaxy.yml: name missing | `name` field absent or empty | `[galaxy.yml] Required field 'name' is missing` |
| galaxy.yml: version missing | `version` field absent or empty | `[galaxy.yml] Required field 'version' is missing` |
| galaxy.yml: invalid version | Version is not semver (MAJOR.MINOR.PATCH) | `[galaxy.yml] Version '<ver>' is not valid semantic versioning (expected MAJOR.MINOR.PATCH)` |
| galaxy.yml: authors missing | `authors` list is empty or absent | `[galaxy.yml] Required field 'authors' is missing or empty` |
| Module syntax error | A plugin file has a Python syntax error | `[plugins/modules/<file>] Python syntax error: <error>` |

### WARNING

| Check | Condition | Message |
|-------|-----------|---------|
| README.md missing | File does not exist | `README.md is missing — add a collection overview with installation and usage instructions` |
| CHANGELOG.md missing | File does not exist | `CHANGELOG.md is missing — document version history for users` |
| LICENSE missing | File does not exist | `LICENSE file is missing — add a license (Apache 2.0 recommended)` |
| meta/runtime.yml missing | File does not exist | `meta/runtime.yml is missing — add 'requires_ansible' constraint` |
| meta/runtime.yml: no requires_ansible | `requires_ansible` absent | `[meta/runtime.yml] 'requires_ansible' not set — recommend adding ">=2.15.0"` |
| galaxy.yml: no dependencies listed | Dependencies field absent or empty when community collections are likely needed | `[galaxy.yml] No dependencies declared — if this collection uses community.general or similar, add them` |
| galaxy.yml: no tags | `tags` field absent or empty | `[galaxy.yml] No tags set — add relevant tags to improve Galaxy discoverability` |
| Role quality issues | Any role fails review-role checks | For each failing role, add a WARNING with the role name and check that failed |
| Module missing DOCUMENTATION | A plugin module lacks the DOCUMENTATION constant | `[plugins/modules/<file>] Module is missing DOCUMENTATION block — required for ansible-doc` |
| Module missing EXAMPLES | A plugin module lacks the EXAMPLES constant | `[plugins/modules/<file>] Module is missing EXAMPLES block` |
| Module missing RETURN | A plugin module lacks the RETURN constant | `[plugins/modules/<file>] Module is missing RETURN block` |
| Missing test guidance for plugins | Collection contains plugins but no `ansible-test` or usage guidance | `[tests/] Collection contains plugins but has no clear validation path aligned with references/testing.md` |

### INFO

| Check | Condition | Message |
|-------|-----------|---------|
| No roles defined | roles/ directory is empty | `No roles found in roles/ — use /ansible-designer:new-role to add a role` |
| No tests defined | tests/ directory is empty | `No tests found — consider adding integration tests for CI validation` |
| No playbooks | playbooks/ directory is empty | `No example playbooks found — consider adding a usage example in playbooks/` |
| galaxy.yml: no repository | `repository` field absent | `[galaxy.yml] No repository URL set` |
| galaxy.yml: description too long | description > 255 characters | `[galaxy.yml] Description is <N> characters — Galaxy recommends under 255` |

---

## Role Quality Checks

For each role found in `roles/`:
- Run the review-role checks (FQCN, tags, no_log, meta/main.yml validity, handler correctness)
- Prefix each finding with `[roles/<role_name>]`
- Include role issues in the appropriate severity sections

---

## Constraints

- **Never modify files.** This command is read-only.
- Do not generate fixed versions of any file.
- Conclude with: "Use `/ansible-designer:update-collection` to apply fixes."
