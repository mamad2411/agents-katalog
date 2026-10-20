# Publishing Automation (SAP-028) - Claude-Specific Awareness

**SAP ID**: SAP-028
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-028.
g.

---

## Claude Code Publishing Workflows

### Workflow 1: Setting Up Trusted Publishing with Claude Code

```markdown
User: "Set up PyPI publishing for this project using trusted publishing"

Claude (Phase 1: Validate Project - 0-5k tokens):
1. Read pyproject.toml (verify package name, version, build backend)
2. Check existing workflows:
   Read .github/workflows/release.yml (if exists)
3. Verify GitHub repository context

Claude (Phase 2: Guide PyPI Configuration - 5-10k tokens):
4. Instruct user on PyPI trusted publisher setup (cannot automate web UI):
   "Please configure PyPI trusted publisher:
   1. Go to: https://pypi.org/manage/account/publishing/
   2. Add trusted publisher:
      - Repository: {owner}/{repo} (from git remote)
      - Workflow: release.yml
      - Environment: release (optional but recommended)
   3. Save publisher

   Let me know when complete, and I'll add the release workflow."

Claude (Phase 3: Add Release Workflow - 10-20k tokens):
5. Copy template workflow:
   Read static-template/.github/workflows/release.yml
6. Customize for project:
   Write .github/workflows/release.yml
   # Content: Trusted publishing workflow (id-token: write, environment: release)

Claude (Phase 4: Documentation - 20-25k tokens):
7. Create PYPI_SETUP.md guide:
   Write docs/PYPI_SETUP.md
   # Content: Trusted publishing setup instructions, troubleshooting

Claude (Phase 5: Test Release - 25-30k tokens):
8. Guide user on first release:
   "Ready to publish! Create first release:

   Bash: git tag v0.1.0
   Bash: git push origin v0.1.0
   Bash: gh release create v0.1.0 --title 'v0.1.0 - Initial Release' --notes 'First release'

   GitHub Actions will:
   - Build package
   - Generate PEP 740 attestations
   - Publish to PyPI (OIDC, zero secrets)

   Check workflow: gh run list --workflow=release.yml"

Claude (response to user):
"I've set up trusted publishing for {project}:

✅ Release workflow added (.github/workflows/release.yml)
✅ OIDC authentication configured (zero secrets)
✅ PEP 740 attestations enabled (build provenance)
✅ Documentation created (docs/PYPI_SETUP.md)

Next: Create GitHub release (v0.1.0) to trigger first publication.

Security: No PYPI_API_TOKEN needed. GitHub → PyPI trust via OIDC."

Result: Secure publishing configured, ready for first release
```

---

### Workflow 2: Migrating from Token to OIDC with Claude Code

```markdown
User: "Migrate this project from token-based to trusted publishing"

Claude (Phase 1: Audit Current Setup - 0-5k tokens):
1. Read .github/workflows/release.yml (identify token usage)
2. Check for PYPI_API_TOKEN secret:
   Bash: gh secret list | grep PYPI_API_TOKEN
3. Verify project published on PyPI (check pyproject.toml name)

Claude (Phase 2: Guide PyPI Publisher Config - 5-10k tokens):
4. Instruct user on PyPI trusted publisher setup:
   "Configure PyPI trusted publisher for existing project:
   1. Go to: https://pypi.org/manage/project/{project}/settings/publishing/
   2. Add trusted publisher (repository, workflow: release.yml, environment: release)
   3. Confirm when done."

Claude (Phase 3: Update Workflow - 10-20k tokens):
5. Read current workflow:
   Read .github/workflows/release.yml
6. Update to trusted publishing:
   Edit .github/workflows/release.yml
   # old_string: Contains "password: ${{ secrets.PYPI_API_TOKEN }}"
   # new_string: Remove password field, add permissions: id-token: write, add environment: release

Claude (Phase 4: Remove Token Secret - 20-25k tokens):
7. Delete PYPI_API_TOKEN secret:
   Bash: gh secret delete PYPI_API_TOKEN --confirm
8. Update documentation:
   Edit docs/PYPI_SETUP.md
   # Remove token instructions, add trusted publishing section

Claude (Phase 5: Test Migration - 25-35k tokens):
9. Create pre-release to test OIDC:
   Bash: git tag v1.0.1-rc1
   Bash: git push origin v1.0.1-rc1
   Bash: gh release create v1.0.1-rc1 --prerelease --title "v1.0.1-rc1 - Test trusted publishing" --notes "Testing OIDC migration"
10. Monitor workflow:
    Bash: gh run watch

Claude (response to user):
"Migration to trusted publishing complete:

✅ Release workflow updated (OIDC authentication)
✅ PYPI_API_TOKEN secret removed (no more secrets)
✅ Documentation updated (docs/PYPI_SETUP.md)
✅ Pre-release published successfully (v1.0.1-rc1 via OIDC)

Verified: PyPI shows v1.0.1-rc1 with PEP 740 attestations.

Next: Delete pre-release tag, create production release (v1.0.1)."

Result: Token-to-OIDC migration complete, tested
```

---

### Workflow 3: Troubleshooting Publishing Failures with Claude Code

```markdown
User: "Release workflow failed with 403 Forbidden from PyPI"

Claude (Phase 1: Diagnose - 0-10k tokens):
1. Check workflow logs:
   Bash: gh run list --workflow=release.yml --limit 1
   Bash: gh run view {run-id} --log | grep -i "403\|forbidden\|oidc\|publisher"
2. Read release workflow:
   Read .github/workflows/release.yml
3. Identify issue category:
   - "Publisher not found" → PyPI configuration issue
   - "Invalid OIDC token" → Permissions or environment issue
   - "Failed to generate OIDC token" → Missing id-token: write

Claude (Phase 2: Fix Based on Diagnosis - 10-30k tokens):

# Scenario A: Missing PyPI publisher
Claude: "PyPI trusted publisher not configured. Please add:
1. Go to: https://pypi.org/manage/project/{project}/settings/publishing/
2. Add trusted publisher:
   - Repository: {owner}/{repo}
   - Workflow: release.yml
   - Environment: release (if workflow has environment: release)
3. Re-run failed workflow: gh run rerun {run-id}"

# Scenario B: Missing id-token: write permission
Claude:
4. Read .github/workflows/release.yml (check permissions)
5. Edit .github/workflows/release.yml:
   # old_string: permissions section without id-token: write
   # new_string: Add permissions: { id-token: write, contents: write }
6. Commit fix:
   Bash: git add .github/workflows/release.yml
   Bash: git commit -m "fix: Add id-token: write permission for OIDC publishing"
   Bash: git push
7. Re-run workflow:
   Bash: gh run rerun {run-id}

# Scenario C: Environment mismatch
Claude:
8. Check PyPI publisher environment setting (manual check required)
9. Edit .github/workflows/release.yml:
   # Add or update: environment: release (to match PyPI publisher)
10. Commit and re-run

Claude (response to user):
"Fixed publishing failure (403 Forbidden):

Issue: Missing id-token: write permission
Fix: Added permissions block to release workflow
Result: Re-running workflow... ✅ Published successfully

Package available: https://pypi.org/project/{project}/{version}/
Attestations: Check 'Attestations' tab for PEP 740 provenance."

Result: Publishing working, issue diagnosed and resolved
```

---

### Workflow 4: Adding Token-Based Fallback with Claude Code

```markdown
User: "Add token-based publishing fallback (can't use OIDC for this project)"

Claude (Phase 1: Generate Token Guidance - 0-5k tokens):
1. Read pyproject.toml (get project name)
2. Instruct user on token generation:
   "Generate project-scoped PyPI API token:
   1. Go to: https://pypi.org/manage/account/token/
   2. Create token:
      - Name: github-actions-{project}
      - Scope: Project: {project} (recommended)
   3. Copy token (starts with pypi-)

   Then run: gh secret set PYPI_API_TOKEN
   (Paste token when prompted)"

Claude (Phase 2: Update Workflow - 5-15k tokens):
3. Read .github/workflows/release.yml
4. Edit .github/workflows/release.yml:
   # old_string: Trusted publishing setup (no password field)
   # new_string: Token-based setup (with password: ${{ secrets.PYPI_API_TOKEN }})
5. Remove OIDC-specific config:
   # Remove: permissions: id-token: write
   # Remove: environment: release (optional, can keep for approval gate)

Claude (Phase 3: Documentation - 15-20k tokens):
6. Edit docs/PYPI_SETUP.md:
   # Add token rotation guidance (every 90 days)
   # Add security warning (token leakage risk)

Claude (Phase 4: Test Publish - 20-30k tokens):
7. Create release:
   Bash: git tag v0.2.0
   Bash: git push origin v0.2.0
   Bash: gh release create v0.2.0 --title "v0.2.0" --notes "Release notes"
8. Monitor workflow:
   Bash: gh run watch

Claude (response to user):
"Token-based publishing configured:

✅ Release workflow updated (password: PYPI_API_TOKEN)
✅ Documentation updated (token rotation guidance)
✅ Test release published (v0.2.0 via token)

⚠️  Security reminder:
- Rotate PYPI_API_TOKEN every 90 days
- Consider migrating to trusted publishing (zero secrets)

Token fallback working. Consider OIDC migration for improved security."

Result: Token-based publishing working (fallback configured)
```

---

## Claude-Specific Tips

### Tip 1: Cannot Automate PyPI Web UI Configuration

**Pattern**:
```markdown
# Claude Code cannot automate PyPI trusted publisher setup (web UI only)
# Always guide user through manual steps:

Claude: "Please configure PyPI trusted publisher (manual step):
1. Go to: https://pypi.org/manage/account/publishing/
2. Add trusted publisher: {repository}, {workflow}, {environment}
3. Confirm when done, and I'll proceed with workflow setup."

# Then use Write/Edit tools for workflow files
```

**Why**: PyPI OIDC configuration requires web authentication, no API available

---

### Tip 2: Use Bash Tool for gh Commands

**Pattern**:
```bash
# Create GitHub release
Bash: git tag v1.0.0
Bash: git push origin v1.0.0
Bash: gh release create v1.0.0 --title "v1.0.0 - Title" --notes "Notes"

# Check workflow status
Bash: gh run list --workflow=release.yml

# View logs
Bash: gh run view {run-id} --log

# Manage secrets
Bash: gh secret set PYPI_API_TOKEN
Bash: gh secret delete PYPI_API_TOKEN --confirm
```

**Why**: Bash tool executes gh CLI commands for release automation

---

### Tip 3: Edit Workflow Incrementally for OIDC Migration

**Pattern**:
```bash
# Read current workflow first
Read .github/workflows/release.yml

# Edit specific sections (not full rewrite)
Edit .github/workflows/release.yml
# old_string: Exact token-based configuration
# new_string: OIDC configuration (permissions + environment)
```

**Why**: Edit tool preserves other workflow configuration (tests, builds, etc.)

---

### Tip 4: Verify Attestations After First Publish

**Pattern**:
```markdown
Claude: "Package published! Verify PEP 740 attestations:
1. Go to: https://pypi.org/project/{project}/{version}/
2. Click 'Attestations' tab
3. Confirm: Build provenance present (GitHub Actions workflow)"
```

**Why**: Attestations confirm trusted publishing working correctly

---

### Tip 5: Use Pre-Release for OIDC Testing

**Pattern**:
```bash
# Test OIDC with pre-release (non-production)
Bash: git tag v1.0.0-rc1
Bash: git push origin v1.0.0-rc1
Bash: gh release create v1.0.0-rc1 --prerelease --title "v1.0.0-rc1 - Test OIDC" --notes "Testing trusted publishing"

# Verify publication works
# Then delete pre-release and tag:
Bash: gh release delete v1.0.0-rc1 --yes
Bash: git push --delete origin v1.0.0-rc1
Bash: git tag -d v1.0.0-rc1
```

**Why**: Pre-releases allow OIDC testing without polluting production versions

---

## Common Pitfalls for Claude Code

### Pitfall 1: Trying to Automate PyPI Publisher Configuration

**Problem**: Attempting to use Bash/curl to configure PyPI trusted publisher via API (no API exists)

**Fix**: Guide user through manual web UI steps, then proceed with workflow setup

---

### Pitfall 2: Not Checking Existing Secrets Before Migration

**Problem**: Migrating to OIDC without verifying PYPI_API_TOKEN exists

**Fix**:
```bash
# Always check existing secrets first
Bash: gh secret list | grep PYPI_API_TOKEN
# If exists: Delete after OIDC migration
# If not exists: User may have different publishing method
```

---

### Pitfall 3: Overwriting Entire Workflow File

**Problem**: Using Write tool to replace release.yml, losing existing test/build steps

**Fix**: Use Edit tool to modify specific sections (pypi_auth_method, permissions, environment)

---

### Pitfall 4: Not Monitoring Workflow After Release

**Problem**: Creating release but not checking if publication succeeded

**Fix**:
```bash
# Always monitor workflow after release creation
Bash: gh run watch
# Or check run list:
Bash: gh run list --workflow=release.yml --limit 1
```

---

### Pitfall 5: Missing Repository Context for PyPI Publisher

**Problem**: Instructing user to configure PyPI publisher without providing exact repository name

**Fix**:
```bash
# Get repository context first
Bash: git remote get-url origin | sed 's/.*://;s/.git$//'
# Output: liminalcommons/chora-utils

# Then provide exact instructions:
Claude: "Configure PyPI trusted publisher:
- Repository: liminalcommons/chora-utils (exact match required)"
```

---

## Support & Resources

**SAP-028 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic publishing workflows
- [Capability Charter](capability-charter.md) - Security rationale, design decisions
- [Protocol Spec](protocol-spec.md) - Technical specification (OIDC setup, workflow config)
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (5 min new, 15 min migration)
- [Ledger](ledger.md) - Adoption tracking, metrics, version history

**External Resources**:
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) - Official documentation
- [PEP 740 (Attestations)](https://peps.python.org/pep-0740/) - Build provenance spec
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) - GitHub Action
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) - OIDC token docs

**Related SAPs**:
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - GitHub Actions infrastructure
- [SAP-004 (testing-framework)](../testing-framework/) - Quality gates
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - New project scaffolding

**Templates**:
- `.github/workflows/release.yml` - Release workflow (trusted publishing default)
- `docs/PYPI_SETUP.md` - PyPI setup guide

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-028
  - Claude Code workflows (setup, migration, troubleshooting, fallback)
  - Tool usage patterns (Edit for workflows, Bash for gh commands, manual PyPI config)
  - Claude-specific tips (PyPI web UI guidance, gh commands, incremental edits, attestation verification)
  - Common pitfalls (cannot automate PyPI, check secrets, preserve workflow, monitor runs, repository context)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic publishing workflows
2. Review [adoption-blueprint.md](adoption-blueprint.md) for installation guide
3. Check [capability-charter.md](capability-charter.md) for security comparison (OIDC vs token)
4. Set up trusted publishing: Guide user through PyPI publisher config → Add workflow → Create release → Verify attestations
