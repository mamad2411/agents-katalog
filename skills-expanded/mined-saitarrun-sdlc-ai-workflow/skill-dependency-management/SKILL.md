---
name: skill-dependency-management
description: Version updates (major/minor/patch), security patch application, transitive dependency resolution, monorepo dependency management, deprecation tracking, license compliance. Use when updating dependencies, managing versions, or addressing CVEs.
version: 1.0.0
---

# Skill: Dependency Management

Stay current. Stay secure. Minimize version mismatch.

## Version Updates

**Semantic Versioning**:
- `1.0.0` → `2.0.0`: Breaking change (test, update code)
- `1.0.0` → `1.1.0`: New feature (backward-compatible, usually safe)
- `1.0.0` → `1.0.1`: Bug fix (safe to update)

## Security Patch Strategy

```bash
# 1. Check for vulnerabilities
npm audit  # or pip check, cargo audit

# 2. Update vulnerable packages
npm update lodash@4.17.21

# 3. Test changes
npm test

# 4. Commit & push
git commit -m "fix(deps): update lodash to patch CVE-2021-23337"
```

## Transitive Dependency Hell

```
app → requests@2.28.0
app → urllib3@1.26.0
app → certifi@2022.9.24

requests → urllib3@1.25.0  # Different version!
```

**Solution**: Lock files (requirements.txt, package-lock.json, Cargo.lock)

## Monorepo Dependencies

**Shared dependencies** (lock once):
```
root/
  Cargo.lock  # All crates use this
  crates/
    auth/
    api/
    db/
```

## Deprecation Tracking

```
# Checklist when you deprecate something
- [ ] Announce (email, docs, header warning)
- [ ] Timeline (6 months warning)
- [ ] Alternatives (what should users use?)
- [ ] Test (ensure new way works)
- [ ] Remove (after timeline)
```

---

**Status**: Ready for dependency work  
**Best for**: Version updates, security patches, CVE management
