---
name: update-collection
description: Update an existing Ansible collection. Triggered by /update-collection. Supports updating galaxy.yml metadata, adding roles or plugins, bumping version, and updating CHANGELOG. Shows a unified diff per file before writing and waits for explicit user confirmation.
---

# update-collection

Update an existing Ansible collection. Always shows a diff and waits for confirmation before writing.

---

## Required Inputs

1. **collection identification** — `namespace.name` or path (resolved from discovery)
2. **change_description** — What to change (e.g., "bump version to 1.1.0", "add a new filter plugin", "update the description in galaxy.yml")

---

## Behavior

### Step 1 — Discovery
Locate the collection via discovery (`references/discovery.md`).

### Step 2 — Load Target Files
Read only the files relevant to the requested change.

### Step 3 — Apply Change
Apply the requested change:
- Preserve all existing fields and structure
- Use templates from `references/collection.md` for new files
- All new module/plugin code follows the complete skeleton format from `references/plugins.md`
- Keep test and usage guidance aligned with `references/testing.md`

### Step 4 — Show Unified Diff (per file)
For each modified or created file, show the diff:

```
--- collections/ansible_collections/myorg/infra/galaxy.yml (original)
+++ collections/ansible_collections/myorg/infra/galaxy.yml (proposed)
@@ -3,7 +3,7 @@
 namespace: myorg
 name: infra
-version: 1.0.0
+version: 1.1.0
 readme: README.md
```

Then ask: **"Apply these changes? (yes/no)"**

### Step 5 — Write on Confirmation
- If **yes**: write all modified/created files.
- If **no**: ask what to change and loop back.

### Step 6 — Final Output
Show updated file tree:
```bash
find <collection_path> -type f | sort
```

Suggest next step:
```
Next step: Run `ansible-galaxy collection build` to test the collection build
           and `ansible-galaxy collection install <tarball> --force` to test locally.
```

---

## Change Types Supported

| Change requested | Files to modify | How to handle |
|-----------------|-----------------|---------------|
| Bump version | galaxy.yml, CHANGELOG.md | Update version field; add CHANGELOG entry with date |
| Update description | galaxy.yml | Update description field |
| Add dependency | galaxy.yml | Append to dependencies dict with version range |
| Add role | roles/ | Create role dir using new-role logic; update galaxy.yml tags if needed |
| Add module | plugins/modules/<name>.py | Create complete module skeleton from `references/collection.md` |
| Add filter plugin | plugins/filter/<name>.py | Create FilterModule skeleton |
| Add lookup plugin | plugins/lookup/<name>.py | Create LookupBase skeleton |
| Update README | README.md | Apply requested textual change |
| Update meta/runtime.yml | meta/runtime.yml | Update requires_ansible or plugin_routing |
| Add CHANGELOG entry | CHANGELOG.md | Prepend new version entry |

---

## Version Bump Rules

- **PATCH** bump (1.0.x → 1.0.x+1): bug fixes, no behavior changes
- **MINOR** bump (1.x → 1.x+1.0): new features, backward-compatible
- **MAJOR** bump (x → x+1.0.0): breaking changes — warn the user that this affects consumers

When bumping version, always add a CHANGELOG entry:
```markdown
## [1.1.0] - 2026-03-31

### Added
- <description of what was added>

### Changed
- <description of what was changed>
```
