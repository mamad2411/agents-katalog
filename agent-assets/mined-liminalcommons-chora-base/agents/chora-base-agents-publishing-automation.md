# Publishing Automation (SAP-028) - Agent Awareness

**SAP ID**: SAP-028
**Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-028?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Option 1: OIDC Trusted Publishing (Recommended)
- 📚 **Time Savings** - 90% release time reduction (automated vs manual), consistent versioning with changesets
- 🎯 **Feature 1** - No API tokens, GitHub authenticates directly with PyPI
- 🔧 **Feature 2** - Backward compatibility for PyPI instances without OIDC support
- 📊 **Feature 3** - Publish on git tag push (v1.0.0 → automatic release)
- 🔗 **Integration** - Works with SAP-000 (Framework)

This AGENTS.md provides: Agent-specific patterns for implementing SAP-028.
s.

---

## Common Workflows

### Workflow 1: Setting Up Trusted Publishing for New Project

**Steps**:
1. Configure PyPI publisher (create trusted publisher entry)
2. Add release workflow to project (.github/workflows/release.yml)
3. Create GitHub release (triggers automated publishing)
4. Verify package published with PEP 740 attestations

**Example (new project chora-utils)**:
```markdown
Step 1: Configure PyPI trusted publisher
- Go to: https://pypi.org/manage/account/publishing/
- Add trusted publisher:
  - Repository: liminalcommons/chora-utils
  - Workflow: release.yml
  - Environment: release (optional but recommended)
- Save publisher (no secrets needed)

Step 2: Add release workflow to project
$ cp static-template/.github/workflows/release.yml chora-utils/.github/workflows/
$ cd chora-utils
$ edit .github/workflows/release.yml
# Verify pypi_auth_method: "trusted-publishing" (default)

Step 3: Create GitHub release
$ git tag v0.1.0
$ git push origin v0.1.0
$ gh release create v0.1.0 --title "v0.1.0 - Initial Release" --notes "First release"

Step 4: Verify publication
# GitHub Actions automatically:
- Builds package (build backend)
- Generates PEP 740 attestations (provenance)
- Publishes to PyPI (OIDC authentication, zero secrets)

# Check PyPI:
https://pypi.org/project/chora-utils/0.1.0/
# Attestations tab shows build provenance (PEP 740)
```

**Outcome**: Package published securely with zero secrets, full provenance

---

### Workflow 2: Migrating from Token to Trusted Publishing

**Steps**:
1. Configure PyPI trusted publisher (same as new project)
2. Update release workflow (change pypi_auth_method)
3. Remove PYPI_API_TOKEN secret from GitHub
4. Test with pre-release (verify OIDC works)
5. Update documentation (PYPI_SETUP.md)

**Example (migrating existing-project)**:
```markdown
Step 1: Configure PyPI trusted publisher (see Workflow 1)

Step 2: Update release workflow
$ edit .github/workflows/release.yml
# Change:
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    # OLD (token-based):
    # password: ${{ secrets.PYPI_API_TOKEN }}

    # NEW (trusted publishing):
    # (No password field needed, OIDC automatic)

Step 3: Remove token secret
$ gh secret delete PYPI_API_TOKEN
# Confirm deletion: Yes

Step 4: Test with pre-release
$ git tag v0.2.0-rc1
$ git push origin v0.2.0-rc1
$ gh release create v0.2.0-rc1 --prerelease --title "v0.2.0-rc1" --notes "Test trusted publishing"
# Verify publication succeeds with OIDC

Step 5: Update documentation
$ edit docs/PYPI_SETUP.md
# Remove token setup instructions
# Add trusted publishing setup section
```

**Outcome**: Migration complete, token removed, OIDC active

---

### Workflow 3: Troubleshooting Trusted Publishing Failures

**Steps**:
1. Check PyPI publisher configuration (repository name, workflow name, environment)
2. Verify GitHub Actions permissions (id-token: write)
3. Check workflow environment matches PyPI publisher
4. Review GitHub Actions logs for OIDC errors

**Example (debugging publication failure)**:
```markdown
Symptom: GitHub Actions release workflow fails with "403 Forbidden" from PyPI

Step 1: Verify PyPI publisher configuration
- Go to: https://pypi.org/manage/project/existing-project/settings/publishing/
- Check:
  - Repository: liminalcommons/existing-project (must match exactly)
  - Workflow: release.yml (must match filename)
  - Environment: release (if specified in workflow)

Step 2: Check GitHub Actions permissions
$ cat .github/workflows/release.yml | grep -A 5 "permissions:"
# Must include:
permissions:
  id-token: write  # Required for OIDC
  contents: write  # Required for release creation

Step 3: Verify environment matches
# If PyPI publisher specifies environment "release":
jobs:
  publish:
    environment: release  # Must match PyPI publisher

Step 4: Review GitHub Actions logs
# Check for OIDC token generation errors:
- "Failed to generate OIDC token" → Check permissions: id-token: write
- "Publisher not found" → Check repository/workflow/environment match
- "Invalid OIDC token" → Check PyPI publisher configuration
```

**Outcome**: Identified misconfiguration, publishing working

---

### Workflow 4: Using Token-Based Fallback (Legacy)

**Steps** (for projects that can't use OIDC):
1. Generate PyPI API token (project-scoped)
2. Add PYPI_API_TOKEN secret to GitHub
3. Update release workflow (use password field)
4. Create release (publishes with token)

**Example (token-based fallback)**:
```markdown
Step 1: Generate PyPI API token
- Go to: https://pypi.org/manage/account/token/
- Create token:
  - Name: github-actions-existing-project
  - Scope: Project: existing-project (recommended)
- Copy token (starts with pypi-)

Step 2: Add secret to GitHub
$ gh secret set PYPI_API_TOKEN
# Paste token when prompted

Step 3: Update release workflow
$ edit .github/workflows/release.yml
# Change:
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}  # Token-based authentication

Step 4: Create release
$ git tag v0.3.0
$ git push origin v0.3.0
$ gh release create v0.3.0 --title "v0.3.0" --notes "Release notes"
# Publishes with token (no OIDC)
```

**Outcome**: Package published with token (fallback working)

**Note**: Token-based publishing is **not recommended** for new projects. Use OIDC trusted publishing (Workflow 1) for zero-secret security.

---

## Security Comparison

### Trusted Publishing (OIDC) - Recommended

**Advantages**:
- ✅ Zero secrets (no PYPI_API_TOKEN to manage)
- ✅ Zero rotation burden (OIDC tokens are ephemeral)
- ✅ Fine-grained trust (repository + workflow + environment scoped)
- ✅ PEP 740 attestations (build provenance automatic)
- ✅ Audit trail (PyPI logs OIDC publisher for each release)
- ✅ No token leakage risk (tokens never exist)

**Disadvantages**:
- ⚠️ Requires GitHub Actions (or GitLab CI with OIDC support)
- ⚠️ PyPI configuration required (one-time setup per project)

---

### Token-Based Publishing (Legacy)

**Advantages**:
- ✅ Works with any CI system (not tied to GitHub Actions)
- ✅ No PyPI publisher configuration (just generate token)

**Disadvantages**:
- ❌ Secret management overhead (store PYPI_API_TOKEN in GitHub Secrets)
- ❌ Rotation burden (tokens expire, manual renewal every 90 days recommended)
- ❌ Broad permissions (project-scoped tokens can publish any version)
- ❌ No build provenance (PEP 740 attestations not automatic)
- ❌ Token leakage risk (if GitHub Secrets compromised)
- ❌ Limited audit trail (PyPI logs token usage, not publisher identity)

---

## Integration with Other SAPs

### Integration with SAP-005 (CI/CD Workflows)

**Pattern**: SAP-028 provides release.yml workflow, SAP-005 provides CI/CD infrastructure

**Workflow**:
1. SAP-005: Defines GitHub Actions workflow structure (test.yml, lint.yml, etc.)
2. SAP-028: Adds release.yml workflow with PyPI publishing logic
3. Developer: Creates GitHub release → triggers release.yml → publishes to PyPI

**Outcome**: Automated publishing integrated with CI/CD pipeline

---

### Integration with SAP-004 (Testing Framework)

**Pattern**: SAP-028 release workflow depends on SAP-004 tests passing

**Workflow**:
1. SAP-004: Defines test suite (pytest, coverage, type checking)
2. SAP-028: release.yml workflow runs tests before publishing:
   ```yaml
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - run: pytest tests/
         - run: mypy src/
     publish:
       needs: test  # Only publish if tests pass
       environment: release
       steps:
         - uses: pypa/gh-action-pypi-publish@release/v1
   ```
3. Developer: Creates release → tests run → publishes only if tests pass

**Outcome**: Quality gate ensures only tested code reaches PyPI

---

### Integration with SAP-003 (Project Bootstrap)

**Pattern**: SAP-028 templates are included in bootstrap workflow

**Workflow**:
1. SAP-003: Generates new project structure (pyproject.toml, src/, tests/)
2. SAP-028: Includes .github/workflows/release.yml template in generated project
3. SAP-028: Includes docs/PYPI_SETUP.md guide in generated project
4. Developer: Configures PyPI trusted publisher (5 minutes)
5. Developer: Creates first release → automatic PyPI publication

**Outcome**: New projects get secure publishing by default

---

## Common Pitfalls

### Pitfall 1: Forgetting to Configure PyPI Trusted Publisher

**Problem**: GitHub release created, workflow runs, but PyPI returns "403 Forbidden" (publisher not found)

**Fix**:
```markdown
# Always configure PyPI publisher BEFORE creating release
1. Go to: https://pypi.org/manage/account/publishing/
2. Add trusted publisher (repository, workflow, environment)
3. Then create GitHub release
```

---

### Pitfall 2: Repository Name Mismatch

**Problem**: PyPI publisher configured for "liminalcommons/chora-utils" but workflow runs from "victorpiper/chora-utils" (fork)

**Fix**:
```markdown
# Ensure PyPI publisher repository matches workflow execution repository EXACTLY
# Check GitHub Actions logs: "Repository: {owner}/{repo}"
# Update PyPI publisher if repository ownership changed
```

---

### Pitfall 3: Missing `id-token: write` Permission

**Problem**: Workflow fails with "Failed to generate OIDC token" error

**Fix**:
```yaml
# Add to .github/workflows/release.yml:
permissions:
  id-token: write  # Required for OIDC trusted publishing
  contents: write  # Required for release creation
```

---

### Pitfall 4: Environment Name Mismatch

**Problem**: PyPI publisher specifies environment "release" but workflow doesn't set environment

**Fix**:
```yaml
# Match environment in workflow to PyPI publisher:
jobs:
  publish:
    environment: release  # Must match PyPI publisher configuration
```

---

### Pitfall 5: Using Token After Migrating to OIDC

**Problem**: After migration, workflow still references ${{ secrets.PYPI_API_TOKEN }} causing confusion

**Fix**:
```markdown
# Remove password field entirely when using trusted publishing:
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  # No "with:" block needed, OIDC automatic

# Delete PYPI_API_TOKEN secret:
$ gh secret delete PYPI_API_TOKEN
```

---

## Key Commands

```bash
# Configure PyPI trusted publisher (manual, web UI)
# https://pypi.org/manage/account/publishing/

# Generate PyPI API token (fallback, legacy)
# https://pypi.org/manage/account/token/

# Add/update GitHub secret (token-based)
gh secret set PYPI_API_TOKEN

# Delete GitHub secret (after OIDC migration)
gh secret delete PYPI_API_TOKEN

# Create GitHub release (triggers publishing)
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0 - Release Title" --notes "Release notes"

# Check release workflow status
gh run list --workflow=release.yml

# View workflow logs
gh run view <run-id> --log

# Verify PEP 740 attestations (PyPI web UI)
# https://pypi.org/project/{project-name}/{version}/ → Attestations tab
```

---

## Support & Resources

**SAP-028 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, scope, security comparison
- [Protocol Spec](protocol-spec.md) - Technical specification (OIDC setup, workflow configuration)
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific patterns
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (Level 1-3)
- [Ledger](ledger.md) - Adoption tracking, metrics, version history

**External Resources**:
- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/) - Official PyPI OIDC documentation
- [PEP 740 (Attestations)](https://peps.python.org/pep-0740/) - Build provenance specification
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) - GitHub Action for PyPI publishing
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) - GitHub OIDC token documentation

**Related SAPs**:
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - CI/CD infrastructure, GitHub Actions workflows
- [SAP-004 (testing-framework)](../testing-framework/) - Quality gates before publishing
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - New project scaffolding with publishing templates

**Templates**:
- `.github/workflows/release.yml` - Release workflow with trusted publishing
- `docs/PYPI_SETUP.md` - PyPI setup guide for new projects
- Migration guide (token → trusted publishing) in adoption-blueprint.md

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-028
  - Common workflows (new project setup, token → OIDC migration, troubleshooting, token fallback)
  - Security comparison (OIDC vs token-based)
  - Integration with SAP-005 (CI/CD), SAP-004 (testing), SAP-003 (bootstrap)
  - Common pitfalls (publisher config, repository mismatch, permissions, environment)
  - Key commands and external resources

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific automation patterns
2. Review [adoption-blueprint.md](adoption-blueprint.md) for installation (5 min new project, 15 min migration)
3. Check [capability-charter.md](capability-charter.md) for security rationale and design decisions
4. Set up trusted publishing: Configure PyPI publisher → Add release.yml → Create release → Verify attestations
