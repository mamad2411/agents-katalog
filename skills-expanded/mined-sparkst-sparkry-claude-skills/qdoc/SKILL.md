---
name: QDOC - Progressive Documentation
description: Generate and update documentation following Progressive Docs pattern - root README, domain READMEs, component context, and CHANGELOG
version: 1.0.0
agents: [docs-writer]
tools: []
references: [progressive-docs-templates.md]
claude_tools: Read, Grep, Glob, Edit, Write, Bash
trigger: QDOC
---

# QDOC Skill

## Purpose

Generate and update documentation following the Progressive Docs pattern:
- **Root README.md**: Mental model, entry points, getting started
- **Domain README.md**: Purpose, boundaries, key files, patterns
- **Component .claude-context**: Domain-specific context for AI assistants
- **CHANGELOG.md**: Version history with semantic versioning

**When to use**: After implementing features, before committing code

---

## Workflow

### Phase 1: Analyze Changes

**Agent**: docs-writer

**Actions**:
1. Run `git diff` to identify changed files
2. Read `requirements/requirements.lock.md` for REQ context
3. Identify affected domains (based on directory structure)
4. Determine documentation scope (root, domain, component)

**Tools**: Bash (git diff), Read, Grep

**Output**: List of files to update

---

### Phase 2: Generate/Update Documentation

**Agent**: docs-writer

**Actions**:
1. Update root README.md if entry points or architecture changed
2. Update domain READMEs for affected domains
3. Update/create `.claude-context` files for new components
4. Update CHANGELOG.md with new version entry

**Tools**: Read, Edit, Write

**Output**: Updated documentation files

---

### Phase 3: Verify Documentation

**Agent**: docs-writer

**Actions**:
1. Check for broken internal links
2. Verify code examples are runnable
3. Ensure REQ IDs are referenced where applicable
4. Validate markdown formatting

**Tools**: Read, Grep

**Output**: Documentation validation report

---

## Input

**From User**:
- Depth level (optional): `QDOC --depth=domain`
- Specific path (optional): `QDOC src/auth/`
- Version bump (optional): `QDOC --version=minor`

**From Environment**:
- `git diff` output (recent changes)
- `requirements/requirements.lock.md` (REQ context)
- Existing README files
- Existing CHANGELOG.md

---

## Output

### Root README.md

```markdown
# Project Name

## Mental Model
One-paragraph purpose and core concept.

## Entry Points
- `src/auth/` — Authentication and authorization
- `src/api/` — HTTP endpoints and integrations
- `src/core/` — Domain logic
- `src/ui/` — UI components

## Getting Started
<dev setup instructions>

## Architecture
High-level overview; details in domain READMEs.
```

### Domain README.md

```markdown
# [Domain Name]

## Purpose
What this domain does and why it exists.

## Boundaries
What's in scope vs. out of scope.

## Key Files
- `types.ts` — Core types and interfaces
- `service.ts` — Business logic
- `api.ts` — External integrations
- `__tests__/` — Tests

## Patterns
Common idioms and conventions to follow.

## Dependencies
Upstream and downstream domains.
```

### .claude-context

```
Domain: [Feature]
Purpose: [Brief description]

Key Concepts:
- [Concept]: [Explanation]

Important Files:
- [file.ts]: [What it does]

Common Tasks:
- "Add new [thing]": Start in [file.ts]

Gotchas:
- [List of common issues]

Dependencies: [List]
```

### CHANGELOG.md

```markdown
# Changelog

## [1.2.0] - 2026-01-28

### Added
- REQ-42: User authentication via OAuth providers
- REQ-43: Password reset flow

### Changed
- REQ-44: Improved error messages for login failures

### Fixed
- REQ-45: Race condition in token refresh

### Deprecated
- REQ-46: Legacy session storage (use JWT tokens instead)

## [1.1.0] - 2026-01-20
...
```

---

## Progressive Docs Pattern

### Tier 1: Root README.md

**Audience**: New developers, stakeholders

**Purpose**: 30-second mental model

**Content**:
- What is this project?
- Where do I start?
- How do I run it?

**Keep it**: ≤200 words

---

### Tier 2: Domain READMEs

**Audience**: Developers working in this domain

**Purpose**: Understand domain boundaries and patterns

**Content**:
- What does this domain own?
- What are the key files?
- What patterns should I follow?
- What dependencies exist?

**Keep it**: ≤500 words per domain

---

### Tier 3: .claude-context Files

**Audience**: AI assistants (Claude Code)

**Purpose**: Provide domain-specific context for code generation

**Content**:
- Key concepts and terminology
- Important files and what they do
- Common tasks and how to accomplish them
- Gotchas and edge cases
- Dependencies

**Keep it**: ≤300 words per component

---

## Examples

### Example 1: Update After Feature Implementation

**Scenario**: Implemented OAuth authentication (REQ-42, REQ-43)

**Command**:
```bash
QDOC
```

**Actions**:
1. Analyze `git diff`: Files changed in `src/auth/`
2. Update `src/auth/README.md` with OAuth provider info
3. Create `src/auth/.claude-context` with OAuth concepts
4. Update root `README.md` entry points (if new)
5. Add CHANGELOG entry for v1.2.0

**Output**:
- `README.md` (updated entry points)
- `src/auth/README.md` (updated with OAuth patterns)
- `src/auth/.claude-context` (new file)
- `CHANGELOG.md` (new version entry)

**Estimated Effort**: 0.2 SP

---

### Example 2: Document Specific Domain

**Scenario**: Want to document `src/api/` domain only

**Command**:
```bash
QDOC src/api/ --depth=domain
```

**Actions**:
1. Read files in `src/api/`
2. Generate/update `src/api/README.md`
3. Create/update `src/api/.claude-context`
4. Skip root README and CHANGELOG (not requested)

**Output**:
- `src/api/README.md` (updated)
- `src/api/.claude-context` (updated)

**Estimated Effort**: 0.1 SP

---

### Example 3: Version Bump with CHANGELOG

**Scenario**: Ready to release v2.0.0 with breaking changes

**Command**:
```bash
QDOC --version=major
```

**Actions**:
1. Analyze `git diff` for breaking changes
2. Update CHANGELOG.md with ## [2.0.0] section
3. Document breaking changes under "### BREAKING CHANGES"
4. Update README.md if architecture changed

**Output**:
- `CHANGELOG.md` (new version 2.0.0)
- `README.md` (updated if needed)

**Estimated Effort**: 0.2 SP

---

## Configuration

### Default Settings

- **Depth**: all (root, domain, component)
- **Version Bump**: auto-detect (patch for fixes, minor for features, major if specified)
- **CHANGELOG Format**: Keep a Changelog (https://keepachangelog.com)

### Custom Configuration

Create `.qdoc.json` in project root:

```json
{
  "depth": "all",
  "output_format": "markdown",
  "changelog_format": "keepachangelog",
  "versioning": "semver",
  "include_req_ids": true,
  "max_root_readme_words": 200,
  "max_domain_readme_words": 500,
  "max_context_words": 300,
  "exclude_patterns": ["node_modules", "dist", ".next", "build"]
}
```

---

## Integration with Other QShortcuts

### With QCODE (Implementation)

```bash
# 1. Implement feature
QCODE

# 2. Document changes
QDOC

# 3. Commit
QGIT
```

---

### With QGIT (Release)

```bash
# 1. Review changes
git diff

# 2. Update docs
QDOC --version=minor

# 3. Commit and push
QGIT
```

---

### With QPLAN (Planning)

```bash
# 1. Plan feature
QPLAN

# 2. Implement
QCODE

# 3. Document
QDOC

# 4. Release
QGIT
```

---

## Quality Checklist

Before marking QDOC complete, verify:

- [ ] Root README.md is ≤200 words
- [ ] Domain READMEs are ≤500 words
- [ ] .claude-context files are ≤300 words
- [ ] CHANGELOG follows Keep a Changelog format
- [ ] REQ IDs are referenced in CHANGELOG
- [ ] Code examples are runnable
- [ ] Internal links are not broken
- [ ] Markdown formatting is valid

---

## Common Patterns

### Pattern: New Feature Documentation

**Trigger**: Implemented REQ-42 (new feature)

**Updates**:
- Root README.md: Add to entry points if new domain
- Domain README.md: Document new files and patterns
- .claude-context: Add key concepts
- CHANGELOG.md: Add under "### Added"

---

### Pattern: Bug Fix Documentation

**Trigger**: Fixed REQ-45 (bug)

**Updates**:
- Domain README.md: Update gotchas if applicable
- CHANGELOG.md: Add under "### Fixed"
- Skip root README (unless architecture changed)

---

### Pattern: Breaking Change Documentation

**Trigger**: Refactored auth to use JWT instead of sessions (REQ-46)

**Updates**:
- Root README.md: Update getting started if setup changed
- Domain README.md: Document new patterns
- .claude-context: Update key concepts
- CHANGELOG.md: Add under "### BREAKING CHANGES"

---

### Pattern: Deprecation Documentation

**Trigger**: Marked legacy API as deprecated (REQ-47)

**Updates**:
- Domain README.md: Add deprecation notice
- CHANGELOG.md: Add under "### Deprecated"
- .claude-context: Add migration notes to gotchas

---

## Anti-Patterns to Avoid

❌ **Too Verbose**: Root README is 1000+ words
✅ **Concise**: Root README is ~150 words, links to domain READMEs for details

❌ **No Structure**: Docs are flat files in `/docs`
✅ **Progressive**: Root → Domain → Component hierarchy

❌ **Stale Examples**: Code examples reference old APIs
✅ **Current**: Code examples are tested and runnable

❌ **Missing Context**: .claude-context doesn't explain key concepts
✅ **Informative**: .claude-context explains domain terminology

❌ **Changelog Spam**: Every commit is a CHANGELOG entry
✅ **Signal**: Only user-facing changes in CHANGELOG

---

## Troubleshooting

### Issue: Documentation Out of Sync

**Problem**: README doesn't reflect recent changes

**Solution**: Run QDOC after every feature
```bash
QDOC
```

Or configure as pre-commit hook:
```bash
# .husky/pre-commit
npm run qdoc
```

---

### Issue: CHANGELOG Version Conflicts

**Problem**: Multiple developers adding to same version section

**Solution**: Use unreleased section
```markdown
## [Unreleased]

### Added
- REQ-42: Feature X
```

Then run `QDOC --version=minor` to cut release.

---

### Issue: Root README Too Long

**Problem**: Root README is 500+ words

**Solution**: Move details to domain READMEs
```bash
QDOC --refactor-root  # Moves content to domain READMEs
```

---

## Story Point Estimation

| Scope | Files Updated | Effort (SP) |
|-------|---------------|-------------|
| Single file | 1 README or CHANGELOG | 0.05 |
| Domain | 1-2 READMEs + .claude-context | 0.1 |
| Full project | Root + 3-5 domains + CHANGELOG | 0.2-0.3 |

**Baseline**: 1 SP = Document entire new project from scratch (10+ domains)

---

## References

See `references/` directory:
- `progressive-docs-templates.md` - Templates for all doc types

---

## CHANGELOG Format Reference

Based on **Keep a Changelog** (https://keepachangelog.com):

### Version Header
```markdown
## [1.2.0] - 2026-01-28
```

### Change Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

### Example Entry
```markdown
## [1.2.0] - 2026-01-28

### Added
- REQ-42: OAuth authentication with Google and GitHub providers
- REQ-43: Password reset via email

### Changed
- REQ-44: Improved error messages for login failures (now include recovery steps)

### Fixed
- REQ-45: Race condition in token refresh causing intermittent logouts

### Deprecated
- REQ-46: Legacy session storage (migrate to JWT tokens by v2.0.0)
```

---

## Contributing

For issues or enhancements to QDOC skill:
- **Email**: skills@sparkry.ai
- **License**: MIT
