---
sap_id: SAP-062
version: 1.0.0
status: draft
last_updated: 2025-11-20
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 11
progressive_loading:
  phase_1: "lines 1-220"   # Quick Reference + Core Workflows
  phase_2: "lines 221-440" # Advanced Workflows + Integration
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 12000
---

# SAP Distribution & Versioning (SAP-062) - Agent Awareness

**SAP ID**: SAP-062
**Last Updated**: 2025-11-20
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-062?** → Read **[capability-charter.md](capability-charter.md)** first (10-min read)

The charter provides:
- 🚀 **Problem Statement** - Manual SAP distribution wastes 10-15 min per SAP (50-70% skip adoption)
- 📚 **Solution** - Copier-based template distribution with semantic versioning
- 🎯 **Core Capabilities** - Template distribution, update propagation, version management, backward compatibility
- 🔧 **Success Metrics** - 85-96% setup time reduction (18 min → 2-5 min)
- 📊 **ROI** - $7,000/year savings (50 projects/year scenario)
- 🔗 **Integration** - Works with SAP-000 (framework), SAP-050 (lifecycle), SAP-061 (ecosystem)

This AGENTS.md provides: Agent-specific workflows for creating projects from templates, updating with template changes, handling version bumps, resolving conflicts, and selecting SAP tiers.

### SAP-062 Core Operations

**Copier Commands**:

```bash
# Create new project from template
copier copy gh:liminalcommons/chora-base my-project

# Update existing project with template changes
cd my-project
copier update

# Pin to specific template version
copier update --vcs-ref v1.2.0

# Answer questionnaire non-interactively
copier copy --data sap_tier=standard gh:liminalcommons/chora-base my-project
```

**Semantic Versioning Rules**:

| Version Type | Pattern | Use Case | Example |
|--------------|---------|----------|---------|
| **Patch** | 1.0.X | Bug fixes, docs, backward compatible | 1.0.0 → 1.0.1 |
| **Minor** | 1.X.0 | New features, non-breaking enhancements | 1.0.0 → 1.1.0 |
| **Major** | X.0.0 | Breaking changes, deprecations removed | 1.0.0 → 2.0.0 |

**Multi-Tier SAP Selection**:

| Tier | SAPs Included | Setup Time | Use Case |
|------|---------------|------------|----------|
| **Minimal** | 2-3 SAPs (SAP-001, SAP-015) | 2-3 min | Core coordination + task tracking |
| **Standard** | 4-6 SAPs (+ SAP-010, SAP-008, SAP-016) | 3-4 min | + memory + automation + validation |
| **Comprehensive** | 8-12 SAPs (+ SAP-053, SAP-051, SAP-052, SAP-061) | 4-5 min | + advanced features |
| **Custom** | À la carte | Varies | Custom SAP selection |

---

## User Signal Patterns

### Project Creation

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "create new project from template" | copier_copy() | 2-5 min | Generate project |
| "scaffold new chora project" | copier_copy() | 2-5 min | Same as above |
| "set up project with SAPs" | copier_copy() | 2-5 min | Template generation |
| "bootstrap using chora-base" | copier_copy() | 2-5 min | Variation |

### Template Updates

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "update template" | copier_update() | 5-10 min | Propagate changes |
| "get latest SAP improvements" | copier_update() | 5-10 min | Same as above |
| "sync with chora-base changes" | copier_update() | 5-10 min | Variation |
| "pull upstream template changes" | copier_update() | 5-10 min | Git terminology |

### Version Management

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "bump SAP version" | update_sap_version() | 2-5 min | Semantic versioning |
| "tag new release" | git_tag_version() | 1-2 min | Version tagging |
| "pin template version" | set_commit_pin() | 1 min | Version pinning |
| "check template version" | show_copier_answers() | <1 min | View current version |

---

## Common Workflows

### Workflow 1: Create New Project from Template (2-5 minutes)

**User signal**: "Create new project from template", "Scaffold new chora project"

**Purpose**: Generate new project with selected SAPs in 2-5 minutes

**Steps**:
1. Run copier with template URL:
   ```bash
   copier copy gh:liminalcommons/chora-base my-project
   ```

2. Answer questionnaire (interactive):
   ```
   Project name: my-project
   Description: My chora-enabled project
   Author: Your Name
   SAP tier (minimal/standard/comprehensive/custom): standard
   Enable SAP-053 (conflict resolution)? [y/N]: y
   Enable SAP-051 (ownership mapping)? [y/N]: n
   ...
   ```

3. Wait for generation (~30-60 seconds)

4. Verify generated structure:
   ```bash
   cd my-project
   ls -la
   # Expected:
   # - scripts/ (automation scripts)
   # - justfile (recipes)
   # - docs/ (documentation)
   # - .chora/ (memory system if SAP-010 selected)
   # - .beads/ (task tracking if SAP-015 selected)
   ```

5. Run post-generation validation:
   ```bash
   just smoke  # Quick smoke test (10 seconds)
   just test   # Full test suite (if tests generated)
   ```

**Expected outcome**: New project with selected SAPs, all scripts executable

**Common errors**:
- Questionnaire timeout → Use `--data` flag for non-interactive mode
- Generation failure → Check internet connection (GitHub access required)
- Post-hook failure → Verify dependencies (Python, git, etc.) installed

---

### Workflow 2: Update Existing Project with Template Changes (5-10 minutes)

**User signal**: "Update template", "Get latest SAP improvements", "Sync with chora-base"

**Purpose**: Propagate SAP improvements from chora-base to existing project

**Steps**:
1. Navigate to project root:
   ```bash
   cd my-project
   ```

2. Check current template version:
   ```bash
   cat .copier-answers.yml | grep _commit
   # Example output: _commit: abc123def  (pinned to specific commit)
   ```

3. Run copier update:
   ```bash
   copier update
   ```

   This will:
   - Fetch latest template changes from chora-base
   - Smart merge with local customizations
   - Prompt for conflict resolution if needed

4. Review changes:
   ```bash
   git diff
   # Shows template changes vs local customizations
   ```

5. Resolve conflicts (if any):
   ```bash
   # Common scenarios:
   # Scenario 1: Keep local version
   git checkout --ours path/to/file

   # Scenario 2: Accept template version
   git checkout --theirs path/to/file

   # Scenario 3: Manual merge
   # Edit file to combine both versions
   ```

6. Test after update:
   ```bash
   just pre-merge  # Run all quality gates
   just smoke      # Quick validation
   ```

7. Commit update:
   ```bash
   git add .
   git commit -m "chore: Update template from chora-base (v1.1.0 → v1.2.0)"
   ```

**Expected outcome**: Project updated with latest SAP improvements, all tests pass

**Common conflicts**:
- justfile customizations → Manual merge (keep both local and template recipes)
- AGENTS.md customizations → Manual merge (keep local + add new template sections)
- Scripts modified locally → Keep local if intentional, otherwise accept template

---

### Workflow 3: Bump SAP Version (Semantic Versioning) (2-5 minutes)

**User signal**: "Bump SAP version", "Tag new release"

**Purpose**: Increment template version following semantic versioning

**Steps**:
1. Determine version bump type:
   - **Patch** (1.0.X): Bug fixes, documentation updates
   - **Minor** (1.X.0): New features, non-breaking SAP additions
   - **Major** (X.0.0): Breaking changes, deprecation removals

2. Update version in template files:
   ```bash
   # Update copier.yml
   # Update VERSION file (if exists)
   # Update changelog
   ```

3. Tag version in git:
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0: Add SAP-053 integration"
   git push origin v1.1.0
   ```

4. Create release notes:
   ```markdown
   # Release v1.1.0

   ## New Features
   - Added SAP-053 (conflict resolution) to comprehensive tier
   - Added post-generation hook for git init

   ## Bug Fixes
   - Fixed justfile recipe for Python 3.12 compatibility

   ## Breaking Changes
   - None

   ## Migration Guide
   - Run `copier update` to get latest changes
   - No manual migration required (backward compatible)
   ```

5. Push to GitHub:
   ```bash
   git push origin main
   git push origin v1.1.0
   ```

**Expected outcome**: New version tagged, release notes published, ready for adoption

---

### Workflow 4: Handle Update Conflicts (Smart Merge) (5-15 minutes)

**User signal**: "Resolve template conflicts", "Handle copier merge conflicts"

**Purpose**: Resolve conflicts between template updates and local customizations

**Common Conflict Scenarios**:

**Scenario 1: justfile Recipe Customization**

```yaml
# Conflict: Both template and local added new recipes
<<<<<<< LOCAL
recipe-local:
    echo "Local custom recipe"
=======
recipe-template:
    echo "New template recipe"
>>>>>>> TEMPLATE

# Resolution: Keep both (manual merge)
recipe-local:
    echo "Local custom recipe"

recipe-template:
    echo "New template recipe"
```

**Scenario 2: AGENTS.md Content Addition**

```markdown
# Conflict: Both template and local added new sections
<<<<<<< LOCAL
## Local Custom Workflow
Steps for local feature X
=======
## New Template Workflow
Steps from SAP-053 integration
>>>>>>> TEMPLATE

# Resolution: Keep both, organize by domain
## Local Custom Workflow
Steps for local feature X

## New Template Workflow (SAP-053)
Steps from SAP-053 integration
```

**Scenario 3: Configuration File Changes**

```yaml
# Conflict: Both modified config.yaml
<<<<<<< LOCAL
timeout: 60
custom_setting: true
=======
timeout: 30
new_template_setting: false
>>>>>>> TEMPLATE

# Resolution: Merge settings (keep local timeout, add template setting)
timeout: 60
custom_setting: true
new_template_setting: false
```

**General Resolution Strategy**:
1. **Identify intent**: Understand why both sides changed the file
2. **Preserve local customizations**: Keep intentional local changes
3. **Adopt template improvements**: Accept template changes for SAP updates
4. **Test after merge**: Run `just pre-merge` to verify no breakage

**Expected outcome**: Conflicts resolved, project functional with both local and template changes

---

### Workflow 5: Multi-Tier SAP Selection (2-5 minutes)

**User signal**: "Choose SAP tier", "Custom SAP selection", "Minimal setup"

**Purpose**: Select appropriate SAP tier based on project complexity

**Decision Matrix**:

| Project Type | Recommended Tier | Reasoning |
|--------------|------------------|-----------|
| **Personal prototype** | Minimal (2-3 SAPs) | Fast setup, core features only |
| **Team project** | Standard (4-6 SAPs) | Balanced features, automation |
| **Production app** | Comprehensive (8-12 SAPs) | Full feature set, quality gates |
| **Specific needs** | Custom (à la carte) | Precise SAP selection |

**Interactive Selection**:

```bash
copier copy gh:liminalcommons/chora-base my-project
# Questionnaire:
# SAP tier (minimal/standard/comprehensive/custom): standard
# → Auto-selects: SAP-001, SAP-015, SAP-010, SAP-008, SAP-016

# If custom:
# SAP tier: custom
# Enable SAP-001 (inbox)? [Y/n]: y
# Enable SAP-015 (beads)? [Y/n]: y
# Enable SAP-010 (memory)? [y/N]: n
# ...
```

**Non-Interactive Selection** (CI/CD, scripting):

```bash
copier copy \
  --data sap_tier=standard \
  --data enable_sap_053=yes \
  --data enable_sap_051=no \
  gh:liminalcommons/chora-base \
  my-project
```

**Tier Composition**:

```yaml
# minimal tier
saps:
  - SAP-001  # inbox (coordination)
  - SAP-015  # beads (task tracking)

# standard tier (minimal + automation + memory)
saps:
  - SAP-001  # inbox
  - SAP-015  # beads
  - SAP-010  # A-MEM (memory)
  - SAP-008  # automation scripts
  - SAP-016  # link validation

# comprehensive tier (standard + advanced)
saps:
  - SAP-001, SAP-015, SAP-010, SAP-008, SAP-016  # standard
  - SAP-053  # conflict resolution
  - SAP-051  # ownership mapping
  - SAP-052  # PR review automation
  - SAP-061  # ecosystem integration
```

**Expected outcome**: Project generated with appropriate SAP tier, 85-96% setup time reduction vs manual

---

## Integration with Other SAPs

### SAP-000 (Framework) Integration

**Dependency**: SAP-062 distributes SAPs defined by SAP-000 framework

**Pattern**:
- copier.yml references SAP-000 5-artifact structure
- Template includes capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger for each SAP
- Questionnaire dynamically includes/excludes SAPs based on tier selection

**Example**:
```yaml
# copier.yml
_templates_suffix: .jinja
_subdirectory: template

# SAP framework compliance (SAP-000)
sap_framework_version: "1.0.0"
required_artifacts:
  - capability-charter.md
  - protocol-spec.md
  - awareness-guide.md
  - adoption-blueprint.md
  - ledger.md
```

---

### SAP-050 (Development Lifecycle) Integration

**Dependency**: SAP-062 enables SAP lifecycle progression (draft → pilot → active → deprecated)

**Pattern**:
- Version tagging supports lifecycle phases (v0.x = draft, v1.x = pilot, v2.x = active)
- Deprecation policy documented in migration guides
- Backward compatibility maintained across minor versions

**Example**:
```bash
# SAP-050 lifecycle progression
v0.1.0  # Draft - initial development
v0.2.0  # Draft - iterating based on feedback
v1.0.0  # Pilot - first stable release
v1.1.0  # Pilot - bug fixes, minor enhancements
v2.0.0  # Active - production-ready, breaking changes
v2.1.0  # Active - new features, backward compatible
v3.0.0  # Deprecated v1.x and v2.x, v3.x is new active
```

---

### SAP-061 (Ecosystem Integration) Integration

**Dependency**: SAP-062 distributes SAP-061 compliance checks (INDEX.md, catalog, dependencies)

**Pattern**:
- Template includes SAP-061 validation scripts
- Post-generation hooks run ecosystem compliance checks
- Update propagation includes SAP-061 improvements

**Example**:
```bash
# Post-generation hook (tasks.py)
def validate_ecosystem_compliance():
    """Run SAP-061 compliance checks after generation"""
    run("python scripts/validate-sap-index.py")
    run("python scripts/validate-sap-catalog.py")
    run("python scripts/check-sap-dependencies.py")
```

---

## Troubleshooting

### Issue 1: Template Generation Fails

**Symptom**: `copier copy` exits with error

**Common causes**:
- Internet connection issue (can't fetch from GitHub)
- Invalid template URL
- Python version incompatible (requires Python 3.11+)
- Copier not installed

**Resolution**:
```bash
# Check copier installation
copier --version
# If not installed: pip install copier

# Verify template URL
# Correct: gh:liminalcommons/chora-base
# Incorrect: https://github.com/liminalcommons/chora-base

# Check Python version
python --version  # Must be 3.11+

# Test GitHub access
git ls-remote https://github.com/liminalcommons/chora-base
```

---

### Issue 2: Update Conflicts Cannot Be Auto-Resolved

**Symptom**: `copier update` shows many conflicts, manual merge required

**Common causes**:
- Extensive local customizations
- Template underwent major refactor
- Conflicting file structure changes

**Resolution**:
```bash
# Strategy 1: Stash local changes, update, reapply
git stash
copier update
git stash pop
# Manually resolve conflicts

# Strategy 2: Pin to specific version, update incrementally
copier update --vcs-ref v1.1.0  # Update to v1.1.0 first
# Resolve conflicts, commit
copier update --vcs-ref v1.2.0  # Then update to v1.2.0
# Resolve conflicts, commit

# Strategy 3: Cherry-pick template changes
git remote add template https://github.com/liminalcommons/chora-base
git fetch template
git cherry-pick template/main -- path/to/specific/file
```

---

### Issue 3: Post-Generation Hooks Fail

**Symptom**: Template generates but post-generation tasks fail

**Common causes**:
- Missing dependencies (git, Python packages)
- Permission issues (can't create directories)
- Network issues (can't clone submodules)

**Resolution**:
```bash
# Check dependencies
which git
which python
python -c "import pytest; import ruff"  # Check Python packages

# Check permissions
ls -la my-project  # Verify ownership

# Retry post-generation tasks manually
cd my-project
python .copier-templates/tasks.py post_gen_project
```

---

### Issue 4: Version Pinning Not Working

**Symptom**: `copier update` pulls latest version despite `_commit` in .copier-answers.yml

**Common causes**:
- `_commit` field missing or incorrect
- Copier cache issue
- Force update flag used

**Resolution**:
```bash
# Verify _commit field
cat .copier-answers.yml | grep _commit
# Should show: _commit: <git-hash>

# Clear copier cache
rm -rf ~/.cache/copier
copier update  # Re-run

# Explicitly pin to version
copier update --vcs-ref v1.2.0
# This updates .copier-answers.yml with correct _commit
```

---

## Support & Resources

**SAP-062 Documentation**:
- [Capability Charter](capability-charter.md) - Problem statement and solution design
- [Protocol Spec](protocol-spec.md) - Technical specification and commands
- [Awareness Guide](awareness-guide.md) - Detailed workflows (this file is the awareness guide)
- [Adoption Blueprint](adoption-blueprint.md) - Installation and setup guide
- [Ledger](ledger.md) - Adoption tracking and metrics

**Copier Documentation**:
- [Copier Official Docs](https://copier.readthedocs.io/) - Complete copier reference
- [Jinja2 Templates](https://jinja.palletsprojects.com/) - Template syntax

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - SAP framework and 5-artifact structure
- [SAP-050 (development-lifecycle)](../development-lifecycle/) - SAP lifecycle management
- [SAP-061 (ecosystem-integration)](../sap-ecosystem-integration/) - Ecosystem compliance

**Commands Quick Reference**:
```bash
# Create new project
copier copy gh:liminalcommons/chora-base my-project

# Update existing project
copier update

# Pin to version
copier update --vcs-ref v1.2.0

# Non-interactive mode
copier copy --data sap_tier=standard gh:liminalcommons/chora-base my-project

# Check template version
cat .copier-answers.yml | grep _commit
```

---

## Version History

- **1.0.0** (2025-11-20): Initial AGENTS.md for SAP-062
  - 5 workflows: Create project, Update template, Bump version, Handle conflicts, Multi-tier selection
  - Integration patterns: SAP-000, SAP-050, SAP-061
  - Troubleshooting: 4 common issues with resolutions
  - Semantic versioning guide and multi-tier SAP selection matrix

---

**Next Steps**:
1. Read [capability-charter.md](capability-charter.md) for problem/solution context
2. Read [protocol-spec.md](protocol-spec.md) for complete technical specification
3. Review [adoption-blueprint.md](adoption-blueprint.md) for setup instructions
4. Check [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
5. Create your first project: `copier copy gh:liminalcommons/chora-base my-project`
