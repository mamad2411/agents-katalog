---
sap_id: SAP-062
version: 1.0.0
status: draft
last_updated: 2025-11-20
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Project Creation Workflow
  phase_2: "lines 181-360" # Update + Conflict Resolution Workflows
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 11000
---

# SAP Distribution & Versioning (SAP-062) - Claude-Specific Awareness

**SAP ID**: SAP-062
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-20

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using Copier-based template distribution and semantic versioning.

### First-Time Setup

1. Read [AGENTS.md](AGENTS.md) for generic SAP-062 workflows
2. Use this file for Claude Code tool integration (Bash for copier commands, Edit for conflict resolution)
3. Always validate template generation with smoke tests

### Session Resumption

- Use Bash tool for all copier commands (`copier copy`, `copier update`)
- Use Read tool to inspect `.copier-answers.yml` (template version tracking)
- Use Edit tool for manual conflict resolution
- Run validation via Bash: `just smoke`, `just pre-merge`

---

## Claude Code Distribution Workflows

### Workflow 1: Creating New Project from Template with Bash

```markdown
User: "Create a new project using chora-base template"

Claude (Phase 1: Generate Project - 0-10k tokens):
1. Run copier via Bash:
   Bash: copier copy gh:liminalcommons/chora-base my-project

   Copier will prompt interactively:
   - Project name: my-project
   - Description: [user provides]
   - Author: [user provides]
   - SAP tier (minimal/standard/comprehensive/custom): standard
   - Enable SAP-053 (conflict resolution)? [y/N]: y
   - ...

2. Wait for generation (~30-60 seconds)

3. Verify generated structure via Bash:
   Bash: ls -la my-project
   # Expected: scripts/, justfile, docs/, .chora/, .beads/, etc.

Claude (Phase 2: Validate Generation - 10-20k tokens):
4. Navigate to project and run smoke test:
   Bash: cd my-project && just smoke

   Expected output:
   ✅ Scripts executable
   ✅ justfile recipes functional
   ✅ Python environment valid

5. Check generated SAPs:
   Bash: cat .copier-answers.yml

   Shows:
   - _commit: abc123def  (template version pinned)
   - sap_tier: standard
   - saps_enabled: [SAP-001, SAP-015, SAP-010, SAP-008, SAP-016]

Claude (Phase 3: Initialize Git - 20-30k tokens):
6. Initialize git repository (if post-hook didn't run):
   Bash: cd my-project && git init && git add . && git commit -m "Initial commit from chora-base template

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

Claude (response to user):
"✅ Project created from chora-base template:
   - Template: gh:liminalcommons/chora-base
   - Tier: standard (6 SAPs included)
   - SAPs: SAP-001, SAP-015, SAP-010, SAP-008, SAP-016, SAP-053
   - Setup time: 3 minutes
   - Validation: PASS

   Next steps:
   1. cd my-project
   2. Review generated structure
   3. Run tests: just test
   4. Start development!"

Result: New project generated with selected SAPs in 3 minutes
```

---

### Workflow 2: Updating Project with Template Changes via Bash and Edit

```markdown
User: "Update this project with latest template changes"

Claude (Phase 1: Check Current Version - 0-5k tokens):
1. Read current template version:
   Read .copier-answers.yml

   Shows:
   _commit: abc123def
   _src_path: gh:liminalcommons/chora-base
   sap_tier: standard

Claude (Phase 2: Run Update - 5-15k tokens):
2. Run copier update via Bash:
   Bash: copier update

   This will:
   - Fetch latest template from GitHub
   - Smart merge with local customizations
   - Prompt for conflict resolution if needed

3. Review changes via Bash:
   Bash: git diff

   Shows template changes vs local customizations

Claude (Phase 3: Resolve Conflicts if Needed - 15-40k tokens):
4. If conflicts detected, identify conflict type:

   Conflict Type 1: justfile Recipe Addition
   ```
   <<<<<<< LOCAL
   recipe-local:
       echo "Local custom recipe"
   =======
   recipe-template:
       echo "New template recipe"
   >>>>>>> TEMPLATE
   ```

   Resolution via Edit:
   Edit justfile
   # old_string:
   # <<<<<<< LOCAL
   # recipe-local:
   #     echo "Local custom recipe"
   # =======
   # recipe-template:
   #     echo "New template recipe"
   # >>>>>>> TEMPLATE

   # new_string:
   # recipe-local:
   #     echo "Local custom recipe"
   #
   # recipe-template:
   #     echo "New template recipe"

   Conflict Type 2: AGENTS.md Content Merge
   ```
   <<<<<<< LOCAL
   ## Local Custom Workflow
   ...
   =======
   ## New Template Workflow (SAP-053)
   ...
   >>>>>>> TEMPLATE
   ```

   Resolution via Edit:
   Edit AGENTS.md
   # Keep both sections, organize by domain

5. Validate after update:
   Bash: just pre-merge

   Runs:
   - pytest (tests)
   - ruff check (linting)
   - mypy --strict (type checking)

Claude (Phase 4: Commit Update - 40-50k tokens):
6. Commit update via Bash:
   Bash: git add . && git commit -m "chore: Update template from chora-base (v1.1.0 → v1.2.0)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

Claude (response to user):
"✅ Template updated successfully:
   - Previous version: v1.1.0 (commit abc123)
   - New version: v1.2.0 (commit def456)
   - Conflicts resolved: 2 (justfile, AGENTS.md)
   - Tests: PASS
   - Validation: PASS

   Changes applied:
   - Added SAP-053 conflict resolution workflow
   - Updated automation scripts for Python 3.12
   - Fixed justfile recipe for link validation

   Next: Review changes with `git show HEAD`"

Result: Project updated with latest SAP improvements, conflicts resolved
```

---

### Workflow 3: Bumping Template Version with Bash and Edit

```markdown
User: "Bump chora-base template version to v1.2.0"

Claude (Phase 1: Determine Version Bump - 0-10k tokens):
1. Read current version from template:
   Read VERSION  # or copier.yml

   Current version: 1.1.0

2. Determine bump type (user confirmation):
   - Patch (1.1.0 → 1.1.1): Bug fixes only
   - Minor (1.1.0 → 1.2.0): New features, backward compatible
   - Major (1.1.0 → 2.0.0): Breaking changes

   User requested: v1.2.0 (minor bump)

Claude (Phase 2: Update Version Files - 10-30k tokens):
3. Update VERSION file via Edit:
   Edit VERSION
   # old_string: 1.1.0
   # new_string: 1.2.0

4. Update copier.yml (if version field exists):
   Edit copier.yml
   # old_string: version: "1.1.0"
   # new_string: version: "1.2.0"

5. Update CHANGELOG.md via Write:
   Read CHANGELOG.md
   Edit CHANGELOG.md
   # Prepend new release section:
   # old_string: # Changelog
   # new_string:
   # # Changelog
   #
   # ## [1.2.0] - 2025-11-20
   #
   # ### Added
   # - SAP-053 conflict resolution workflow
   # - Post-generation hook for git init
   #
   # ### Fixed
   # - justfile Python 3.12 compatibility
   #
   # ### Breaking Changes
   # - None

Claude (Phase 3: Tag Version - 30-40k tokens):
6. Create git tag via Bash:
   Bash: git tag -a v1.2.0 -m "Release v1.2.0: Add SAP-053 integration"

7. Push tag to remote:
   Bash: git push origin main && git push origin v1.2.0

Claude (Phase 4: Create Release Notes - 40-50k tokens):
8. Create release notes via Write:
   Write RELEASE_NOTES_v1.2.0.md
   # Content:
   # Release v1.2.0
   #
   # ## New Features
   # - Added SAP-053 (conflict resolution) to comprehensive tier
   # - Added post-generation hook for git init
   #
   # ## Bug Fixes
   # - Fixed justfile recipe for Python 3.12 compatibility
   #
   # ## Migration Guide
   # - Run `copier update` to get latest changes
   # - No manual migration required (backward compatible)

Claude (response to user):
"✅ Template version bumped to v1.2.0:
   - Version files updated: VERSION, copier.yml, CHANGELOG.md
   - Git tag created: v1.2.0
   - Tag pushed to remote: origin/v1.2.0
   - Release notes: RELEASE_NOTES_v1.2.0.md

   Semver classification: MINOR (backward compatible)

   Users can now:
   - Create new projects with v1.2.0 features
   - Update existing projects: `copier update --vcs-ref v1.2.0`

   Next: Announce release in coordination channels"

Result: Template version bumped, tagged, and documented
```

---

### Workflow 4: Resolving Update Conflicts with Edit Tool

```markdown
User: "Help me resolve these copier update conflicts"

Claude (Phase 1: Identify Conflicts - 0-10k tokens):
1. Check git status for conflicts:
   Bash: git status

   Shows:
   Unmerged paths:
     both modified:   justfile
     both modified:   AGENTS.md
     both modified:   scripts/validate.sh

Claude (Phase 2: Resolve justfile Conflict - 10-30k tokens):
2. Read conflicted justfile:
   Read justfile

   Shows:
   <<<<<<< LOCAL
   custom-recipe:
       python scripts/custom.py
   =======
   new-template-recipe:
       python scripts/template-feature.py
   >>>>>>> TEMPLATE

3. Resolve via Edit (keep both):
   Edit justfile
   # old_string:
   # <<<<<<< LOCAL
   # custom-recipe:
   #     python scripts/custom.py
   # =======
   # new-template-recipe:
   #     python scripts/template-feature.py
   # >>>>>>> TEMPLATE
   #
   # new_string:
   # custom-recipe:
   #     python scripts/custom.py
   #
   # new-template-recipe:
   #     python scripts/template-feature.py

Claude (Phase 3: Resolve AGENTS.md Conflict - 30-50k tokens):
4. Read conflicted AGENTS.md:
   Read AGENTS.md

   Shows:
   <<<<<<< LOCAL
   ## Local Feature Documentation
   Steps for using local feature X
   =======
   ## SAP-053 Integration
   Steps for conflict resolution workflow
   >>>>>>> TEMPLATE

5. Resolve via Edit (keep both, organize):
   Edit AGENTS.md
   # old_string:
   # <<<<<<< LOCAL
   # ## Local Feature Documentation
   # Steps for using local feature X
   # =======
   # ## SAP-053 Integration
   # Steps for conflict resolution workflow
   # >>>>>>> TEMPLATE
   #
   # new_string:
   # ## Local Feature Documentation
   # Steps for using local feature X
   #
   # ## SAP-053 Integration (Template)
   # Steps for conflict resolution workflow

Claude (Phase 4: Resolve Script Conflict - 50-70k tokens):
6. Read conflicted script:
   Read scripts/validate.sh

   Shows:
   <<<<<<< LOCAL
   # Custom validation logic
   validate_custom() { ... }
   =======
   # Template validation improvements
   validate_links() { ... }
   >>>>>>> TEMPLATE

7. Decide resolution strategy:
   - If local custom logic is important: Keep local, add template as new function
   - If template improves existing validation: Accept template, port custom logic

   Resolution via Edit:
   Edit scripts/validate.sh
   # Merge both functions, avoid duplication

Claude (Phase 5: Validate and Commit - 70-80k tokens):
8. Mark conflicts resolved:
   Bash: git add justfile AGENTS.md scripts/validate.sh

9. Test after resolution:
   Bash: just pre-merge

   Expected: All tests pass

10. Commit resolution:
    Bash: git commit -m "chore: Resolve template update conflicts (v1.1.0 → v1.2.0)

- Merged justfile: kept local recipes + added template recipes
- Merged AGENTS.md: kept local docs + added SAP-053 section
- Merged validate.sh: combined local and template validation logic

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

Claude (response to user):
"✅ All update conflicts resolved:
   - justfile: 2 recipes merged (local + template)
   - AGENTS.md: 2 sections merged (local + SAP-053)
   - scripts/validate.sh: validation logic combined

   Validation: PASS (all tests green)

   Strategy used: Preserve local customizations + adopt template improvements

   Next: Review changes with `git diff HEAD~1`"

Result: Conflicts resolved, project functional with both local and template changes
```

---

### Workflow 5: Multi-Tier SAP Selection via Bash

```markdown
User: "Create a minimal project with just coordination and task tracking"

Claude (Phase 1: Non-Interactive Template Generation - 0-10k tokens):
1. Create project with minimal tier via Bash:
   Bash: copier copy \
     --data project_name=my-minimal-project \
     --data project_description="Minimal chora project" \
     --data author_name="User Name" \
     --data sap_tier=minimal \
     gh:liminalcommons/chora-base \
     my-minimal-project

   This bypasses interactive questionnaire, selects minimal tier automatically

2. Verify SAP selection:
   Bash: cat my-minimal-project/.copier-answers.yml

   Shows:
   sap_tier: minimal
   saps_enabled:
     - SAP-001  # inbox (coordination)
     - SAP-015  # beads (task tracking)

Claude (Phase 2: Validate Minimal Setup - 10-20k tokens):
3. Check generated structure:
   Bash: ls -la my-minimal-project

   Expected:
   - inbox/ (SAP-001 coordination)
   - .beads/ (SAP-015 task tracking)
   - scripts/ (minimal automation)
   - justfile (core recipes only)
   - No .chora/memory/ (SAP-010 excluded)
   - No extensive automation (SAP-008 excluded)

4. Run smoke test:
   Bash: cd my-minimal-project && just smoke

   Expected: PASS (core features functional)

Claude (response to user):
"✅ Minimal project created:
   - Template: chora-base
   - Tier: minimal (2 SAPs)
   - SAPs included:
     • SAP-001 (inbox) - Coordination
     • SAP-015 (beads) - Task tracking
   - Setup time: 2 minutes

   Features available:
   - Coordination: inbox/coordination/ for cross-repo requests
   - Task tracking: bd create, bd list, bd close commands
   - Basic automation: justfile with core recipes

   Features excluded (minimal tier):
   - Memory system (SAP-010) - not needed for simple projects
   - Advanced automation (SAP-008) - core recipes sufficient
   - Link validation (SAP-016) - skip for prototypes

   Next: cd my-minimal-project && bd create 'First task'"

Result: Minimal project generated in 2 minutes with only essential SAPs
```

---

## Claude-Specific Tips

### Tip 1: Use Bash for All Copier Commands

**Pattern**:
```markdown
# ✅ GOOD: Copier via Bash tool
Bash: copier copy gh:liminalcommons/chora-base my-project
Bash: copier update
Bash: copier update --vcs-ref v1.2.0

# ❌ BAD: Don't use Read/Write for copier operations
# Copier requires interactive prompts, file system ops
```

**Why**: Copier needs Bash tool for:
- Interactive questionnaire
- Git operations (clone, fetch)
- File system operations (template generation)

---

### Tip 2: Read .copier-answers.yml Before Updates

**Pattern**:
```markdown
# ALWAYS read before update
Read .copier-answers.yml

# Check:
# - _commit: current template version
# - sap_tier: selected tier
# - saps_enabled: list of SAPs

# THEN update with context
Bash: copier update
```

**Why**: Understanding current state prevents surprise conflicts

---

### Tip 3: Use Edit for Manual Conflict Resolution

**Pattern**:
```markdown
# ✅ GOOD: Edit tool for structured merge
Read conflicted-file.md
Edit conflicted-file.md
# old_string: <<<<<<< LOCAL ... >>>>>>> TEMPLATE
# new_string: (combined version)

# ❌ BAD: Bash checkout (loses context)
Bash: git checkout --ours conflicted-file.md  # Discards template changes
```

**Why**: Edit tool preserves both sides, Claude can reason about merge

---

### Tip 4: Validate After Every Template Operation

**Pattern**:
```markdown
# After copier copy:
Bash: cd my-project && just smoke

# After copier update:
Bash: just pre-merge

# After conflict resolution:
Bash: just test && just lint
```

**Why**: Catch template generation or merge issues immediately

---

### Tip 5: Use Non-Interactive Mode for Scripting

**Pattern**:
```markdown
# For reproducible project generation:
Bash: copier copy \
  --data sap_tier=standard \
  --data enable_sap_053=yes \
  --data enable_sap_051=no \
  gh:liminalcommons/chora-base \
  my-project

# Not interactive, ideal for:
# - CI/CD pipelines
# - Batch project creation
# - Testing template changes
```

**Why**: Deterministic generation, no manual intervention

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Checking Template Version Before Update

**Problem**: Run `copier update` without knowing current version, unexpected breaking changes

**Fix**: ALWAYS read `.copier-answers.yml` first

```markdown
# ❌ BAD: Blind update
Bash: copier update

# ✅ GOOD: Version-aware update
Read .copier-answers.yml  # Check current _commit
Bash: copier update --vcs-ref v1.2.0  # Explicit version
```

**Why**: Incremental updates (v1.1 → v1.2 → v1.3) safer than jump (v1.1 → v2.0)

---

### Pitfall 2: Using `git checkout --ours/--theirs` for Conflicts

**Problem**: `git checkout --ours` discards template improvements, `--theirs` discards local customizations

**Fix**: Manual merge via Edit tool

```markdown
# ❌ BAD: Discard one side
Bash: git checkout --ours conflicted-file.md  # Loses template changes
Bash: git checkout --theirs conflicted-file.md  # Loses local customizations

# ✅ GOOD: Manual merge
Read conflicted-file.md
Edit conflicted-file.md
# Combine both sides intelligently
```

**Why**: Preserve value from both template and local changes

---

### Pitfall 3: Skipping Validation After Template Operations

**Problem**: Assume template generation or update succeeded, discover broken project later

**Fix**: Always run smoke tests

```markdown
# After ANY template operation:
Bash: just smoke  # Quick validation (10 seconds)
Bash: just pre-merge  # Full validation (1-2 minutes)

# Before committing:
Bash: just test  # Run test suite
```

**Why**: Template generation can have subtle issues (missing files, broken scripts)

---

### Pitfall 4: Forgetting to Commit After Conflict Resolution

**Problem**: Resolve conflicts via Edit, forget to commit, changes lost on next operation

**Fix**: Commit immediately after resolution

```markdown
# After resolving conflicts:
Edit conflicted-file.md
Bash: git add conflicted-file.md
Bash: git commit -m "chore: Resolve template conflict in conflicted-file.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Why**: Git requires explicit commit after conflict resolution

---

### Pitfall 5: Not Pinning Template Version for Production Projects

**Problem**: Production project uses latest template version, breaks when template changes

**Fix**: Pin to specific version via `_commit` field

```markdown
# ✅ GOOD: Pin production project to stable version
Bash: copier update --vcs-ref v1.2.0

# Verify pinning:
Read .copier-answers.yml
# Shows: _commit: <git-hash-for-v1.2.0>

# Future updates are opt-in:
# User must explicitly: copier update --vcs-ref v1.3.0
```

**Why**: Production stability > latest features

---

## Support & Resources

**SAP-062 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic SAP-062 workflows
- [Capability Charter](capability-charter.md) - Problem statement and ROI
- [Protocol Spec](protocol-spec.md) - Copier commands and versioning rules
- [Adoption Blueprint](adoption-blueprint.md) - Setup guide for template distribution
- [Ledger](ledger.md) - Adoption tracking and metrics

**Copier Documentation**:
- [Copier Official Docs](https://copier.readthedocs.io/) - Complete reference
- [Jinja2 Templates](https://jinja.palletsprojects.com/) - Template syntax

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - 5-artifact SAP structure
- [SAP-050 (development-lifecycle)](../development-lifecycle/) - Lifecycle management
- [SAP-061 (ecosystem-integration)](../sap-ecosystem-integration/) - Ecosystem compliance

**Claude Code Tool Patterns**:
```markdown
# Copier operations
Bash: copier copy gh:liminalcommons/chora-base my-project
Bash: copier update
Bash: copier update --vcs-ref v1.2.0

# Version tracking
Read .copier-answers.yml

# Conflict resolution
Read conflicted-file.md
Edit conflicted-file.md

# Validation
Bash: just smoke
Bash: just pre-merge
```

---

## Version History

- **1.0.0** (2025-11-20): Initial CLAUDE.md for SAP-062
  - 5 workflows: Create project, Update template, Bump version, Resolve conflicts, Multi-tier selection
  - Claude Code tool patterns: Bash for copier, Read for version tracking, Edit for conflicts
  - 5 Claude-specific tips, 5 common pitfalls
  - Non-interactive mode examples for CI/CD

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic SAP-062 workflows
2. Review [protocol-spec.md](protocol-spec.md) for copier command reference
3. Check [adoption-blueprint.md](adoption-blueprint.md) for setup instructions
4. Create your first project via Bash: `copier copy gh:liminalcommons/chora-base my-project`
5. Validate generation: `cd my-project && just smoke`
