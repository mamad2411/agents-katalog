---
description: Documentation version numbers must match git tag versions for consistency
alwaysApply: true
tags: [documentation, versioning, git, consistency]
priority: 1
version: 1.0.0
---

# Document Version Matches Git Tag

## Core Principle

**ALL documentation version numbers MUST match the git tag version for that release.**

---

## Mandatory Rule

### Version Consistency

**When creating or updating documentation:**
- ✅ **ALWAYS** use git tag version as document version
- ✅ **ALWAYS** keep version numbers consistent across all documents in a release
- ❌ **NEVER** use arbitrary version numbers (like v5.0.0) that don't match tags
- ❌ **NEVER** increment document versions independently from git tags

---

## Examples

### ✅ CORRECT (Formal Approach - v2.2.0 onwards)

**Git Tag:** `v2.2.0`  
**Documents:**
- `solution-architecture-v2.2.0.presentation.md` → **Version: 2.2.0**
- `technical-design-v2.2.0.presentation.md` → **Version: 2.2.0**
- `implementation-spec-v2.2.0.spec.md` → **Version: 2.2.0**

**Rationale:** Both filename AND internal version match git tag for complete consistency

### ✅ ACCEPTABLE (Legacy POC Approach - v1.0.0 - v2.0.0)

**Git Tag:** `v2.0.0`  
**Documents:**
- `solution-architecture-v4.presentation.md` → **Version: 2.0.0**
- `technical-design-v4.presentation.md` → **Version: 2.0.0**

**Rationale:** Sequential suffix in filename, but version inside matches git tag (legacy POC files)

### ❌ WRONG

**Git Tag:** `v2.2.0`  
**Documents:**
- `solution-architecture-v5.presentation.md` → **Version: 5.0.0** ❌
- `technical-design-v2.2.0.presentation.md` → **Version: 5.0.0** ❌

**Problem:** Document versions don't match git tag, causing confusion

---

## File Naming vs Version Number

### Formal Approach (v2.2.0 onwards)
**File name AND internal version BOTH match git tag:**
- File name: `solution-architecture-v2.2.0.presentation.md`
- Version inside: `2.2.0`
- **Benefit:** Complete consistency, no confusion, professional/formal

### Legacy Approach (POC v1.0.0 - v2.0.0)
**File name uses sequential suffix, internal version matches git tag:**
- File name: `solution-architecture-v4.presentation.md` (4th edition)
- Version inside: `2.0.0` (git tag)
- **Note:** Legacy files remain for historical reference

### Why the Change?
- **POC Phase:** Sequential suffixes (v1-v5) were acceptable for rapid iteration
- **Formal Phase:** Tag-based naming provides better traceability and professionalism
- **Going Forward:** All new documents use tag version in filename

---

## Application

### When Creating New Documents

```markdown
# Solution Architecture

**Version:** 2.2.0  ← Match git tag
**Date:** 2025-11-14
**Status:** Implemented
```

### When Updating Existing Documents

**Before release:**
```markdown
**Version:** 2.0.0  ← Previous release
```

**After v2.2.0 release:**
```markdown
**Version:** 2.2.0  ← Updated to match new tag
```

### Document History Table

```markdown
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.2.0 | 2025-11-14 | Author | Added testing framework |
| 2.0.0 | 2025-11-13 | Author | Added data-seeder |
| 1.0.0 | 2025-11-11 | Author | Initial version |
```

---

## Rationale

### Why This Rule?

1. **Consistency:** Version numbers match across code, docs, and git tags
2. **Traceability:** Easy to find which docs correspond to which release
3. **Clarity:** No confusion about what version a document represents
4. **Audit Trail:** Clear mapping between releases and documentation

### Problems This Prevents

- ❌ Documentation versioned as v5.0.0 but git tag is v2.2.0 (confusing!)
- ❌ Documents have different version numbers for same release
- ❌ Unclear which documentation corresponds to which release
- ❌ Version number inflation without meaningful releases

---

## Integration with Git Workflow

### Workflow

1. **Development Phase:**
   - Create/update documentation with current version
   - File name uses next suffix (e.g., `-v5`)

2. **Before Release:**
   - Ensure all docs have correct version matching planned tag
   - Example: If tagging as `v2.2.0`, all docs should have `Version: 2.2.0`

3. **Release:**
   - Commit all documentation
   - Tag commit: `git tag v2.2.0`
   - Push tag: `git push origin v2.2.0`

4. **Verification:**
   - Verify document versions match tag: `git show v2.2.0:docs/presentation/solution-architecture-v5.presentation.md | grep "Version:"`

---

## Critical Rules

### ALWAYS
- ✅ Match document version to git tag version
- ✅ Update all documents in a release to same version
- ✅ Include version history table showing progression
- ✅ Verify versions before tagging release

### NEVER
- ❌ Use file name suffix as document version (v5 ≠ 5.0.0)
- ❌ Increment document versions independently
- ❌ Release documents with mismatched versions
- ❌ Skip version updates when creating new release

---

## Related Rules

- **Version Tagging:** `.cursor/rules/development/version-tagging.mdc`
- **Presentation Document Versioning:** `.cursor/rules/documentation/presentation-document-versioning.mdc`
- **Spec vs Presentation File Pattern:** `.cursor/rules/documentation/spec-vs-presentation-file-pattern.mdc`

---

**Last Updated:** 2025-11-14  
**Version:** 1.0.0  
**Rule Type:** CRITICAL - Documentation Versioning  
**Priority:** HIGHEST  
**Always Apply:** YES
