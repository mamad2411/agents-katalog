---
name: Release Notes Generator
description: Generate comprehensive release notes for Confluence from Jira issues, git commits, and pull requests. Use when preparing releases, creating changelogs, documenting version updates, or when user mentions release notes, changelog, version, or release documentation.
allowed-tools: Read, Grep, Bash
---

# Release Notes Generator

Expert assistance for generating comprehensive release notes and changelogs in Confluence.

## When to Use This Skill

- Creating release notes for a new version
- Generating changelogs
- Documenting version updates
- Preparing release announcements
- User mentions: release notes, changelog, version, release

## What Are Release Notes?

**Release notes** communicate changes in a software release to users and stakeholders.

### Audience
- **End Users**: What's new and what to expect
- **Developers**: Technical changes and API updates
- **Product Managers**: Feature completeness and roadmap alignment
- **Support Teams**: Known issues and workarounds

### Key Components
1. **Version and date**
2. **Summary** of changes
3. **New features**
4. **Improvements**
5. **Bug fixes**
6. **Breaking changes**
7. **Deprecations**
8. **Known issues**
9. **Upgrade instructions**

## Release Notes Structure

### Standard Template

```markdown
# Version X.Y.Z - Release Date

## Highlights

Brief overview of the most important changes in this release.

## What's New

### Major Features
- **Feature Name**: Description of what it does and why it matters

### Minor Features
- **Feature Name**: Brief description

## Improvements

### Performance
- List of performance improvements

### User Experience
- UI/UX enhancements

### Developer Experience
- API improvements
- Tooling updates

## Bug Fixes

- **[PROJ-123]**: Fixed issue where...
- **[PROJ-456]**: Resolved bug with...

## Breaking Changes

⚠️ **Important**: These changes may require action.

- **Change description**: What changed and what you need to do

## Deprecations

⚠️ **Notice**: These features will be removed in future versions.

- **Feature/API**: Deprecated in favor of... Will be removed in version...

## Security Updates

🔒 Security fixes included in this release.

- **[PROJ-789]**: Security vulnerability in... (CVE-YYYY-XXXX)

## Known Issues

- **Issue description**: Workaround if available

## Upgrade Guide

### Prerequisites
- Requirements for upgrading

### Steps
1. Step 1
2. Step 2
3. Step 3

### Migration Notes
- Database migrations
- Config changes
- Breaking API changes

## Technical Details

### Dependencies Updated
- Library X: v1.0 → v2.0
- Framework Y: v3.0 → v3.1

### API Changes
- New endpoints
- Modified endpoints
- Removed endpoints

## Contributors

Thanks to everyone who contributed to this release!
- @user1
- @user2
- @user3
```

## Types of Release Notes

### Major Release (X.0.0)

```markdown
# Version 2.0.0 - February 1, 2024

## 🎉 Major Release: Complete Platform Redesign

This is our biggest update ever! Version 2.0 brings a completely redesigned interface, powerful new features, and significant performance improvements.

## 🌟 Highlights

- **New Dashboard**: Completely redesigned for better insights
- **Real-time Collaboration**: Work together with your team
- **50% Faster**: Improved performance across the board
- **Dark Mode**: Easy on the eyes

## ✨ What's New

### Dashboard Redesign
The new dashboard provides at-a-glance insights into your projects with customizable widgets and real-time updates.

**Key features**:
- Drag-and-drop widget arrangement
- Custom dashboard creation
- Real-time data updates
- Mobile responsive design

### Real-time Collaboration
Work with your team in real-time with live cursors, presence indicators, and instant updates.

### API v2
Complete API redesign with:
- RESTful design principles
- GraphQL support
- Improved documentation
- Better error messages

## 🚀 Improvements

### Performance
- Dashboard loads 50% faster
- Search improved from 2s → 200ms
- Reduced memory usage by 40%
- Better caching strategy

### User Experience
- Streamlined navigation
- Improved mobile experience
- Better accessibility (WCAG 2.1 AA compliant)
- Keyboard shortcuts

## 🐛 Bug Fixes

- Fixed dashboard refresh issues
- Resolved search indexing problems
- Fixed export truncation
- Corrected timezone display issues

## ⚠️ Breaking Changes

### API Changes
The API has been completely redesigned. The old v1 API will continue to work until June 1, 2024.

**Required actions**:
1. Update to API v2 endpoints
2. Update authentication to OAuth 2.0
3. Review and update error handling

See [API Migration Guide] for details.

### Configuration Format
Configuration format has changed from XML to YAML.

**Migration**: Run `migrate-config` tool to convert existing configs.

### Database Schema
Database schema has been updated.

**Migration**: Automatic on first startup (backup recommended).

## 📋 Upgrade Guide

[Detailed upgrade instructions]

## 🙏 Contributors

Thanks to our 42 contributors!
```

### Minor Release (x.Y.0)

```markdown
# Version 1.5.0 - January 15, 2024

## New Features

### Export to PDF
Export your reports to PDF format with customizable templates.

### Advanced Filters
New filtering options in search:
- Date ranges
- Custom fields
- Multiple criteria

## Improvements

- Faster page loads (20% improvement)
- Better error messages
- Improved mobile UI

## Bug Fixes

- **[PROJ-234]**: Fixed export timeout for large datasets
- **[PROJ-456]**: Resolved calendar sync issues
- **[PROJ-789]**: Fixed permission check bug

## Known Issues

- PDF export may be slow for very large reports (>1000 pages)
```

### Patch Release (x.y.Z)

```markdown
# Version 1.4.3 - January 5, 2024

## Bug Fixes

- **[PROJ-901]**: Fixed critical bug in authentication flow
- **[PROJ-902]**: Resolved data loss issue in export
- **[PROJ-903]**: Fixed memory leak in background jobs

## Security Updates

- Updated dependencies to address CVE-2024-1234
- Improved session timeout handling

This is a recommended security update for all users.
```

## Generating from Jira Issues

### Using JQL to Find Issues

```jql
fixVersion = "2.0.0" ORDER BY type DESC, priority DESC
```

### Categorizing Issues

**By Issue Type**:
- **Epic/Story** → New Features
- **Task** → Improvements
- **Bug** → Bug Fixes
- **Security** → Security Updates

**By Labels**:
- `breaking-change` → Breaking Changes
- `deprecation` → Deprecations
- `performance` → Performance section
- `ui-ux` → User Experience section

### Example: From Jira Issues

**Jira Issues**:
```
PROJ-101: Add dark mode support [Story]
PROJ-102: Improve dashboard performance [Task, Label: performance]
PROJ-103: Fix login bug with special chars [Bug]
PROJ-104: Deprecate /v1/users endpoint [Task, Label: deprecation]
```

**Generated Release Notes**:
```markdown
## What's New

### Dark Mode
**[PROJ-101]**: Added system-wide dark mode support. Toggle in Settings > Appearance.

## Improvements

### Performance
**[PROJ-102]**: Dashboard now loads 40% faster with optimized queries.

## Bug Fixes

- **[PROJ-103]**: Fixed login issues when email contains special characters

## Deprecations

⚠️ **[PROJ-104]**: The `/v1/users` endpoint is deprecated. Use `/v2/users` instead. The old endpoint will be removed in version 3.0.
```

## Generating from Git Commits

### Commit Message Patterns

**Conventional Commits**:
```
feat: add dark mode support
fix: resolve login bug with special chars
perf: optimize dashboard queries
docs: update API documentation
chore: update dependencies
```

### Parsing Commits

```bash
# Get commits between tags
git log v1.4.0..v1.5.0 --oneline

# Filter by type
git log v1.4.0..v1.5.0 --grep="^feat:" --oneline
git log v1.4.0..v1.5.0 --grep="^fix:" --oneline
```

### Example: From Git Commits

**Git Log**:
```
abc123 feat(auth): add OAuth 2.0 support
def456 feat(ui): implement dark mode
ghi789 fix(login): handle special characters in email
jkl012 perf(dashboard): optimize query performance
mno345 docs(api): update API documentation
```

**Generated Release Notes**:
```markdown
## What's New

### Authentication
- OAuth 2.0 support for third-party login

### User Interface
- Dark mode implementation

## Improvements

### Performance
- Optimized dashboard query performance

## Bug Fixes

- Fixed login handling for special characters in email addresses

## Documentation

- Updated API documentation
```

## Combining Sources

### Jira + Git Commits + Pull Requests

```markdown
# Version 2.1.0 - March 1, 2024

## What's New

### Multi-language Support
**[PROJ-456]** (PR #123): Added support for 10 new languages including Spanish, French, and German.

Implementation by @johndoe in PR #123.
- Automatic language detection
- User preference storage
- RTL language support

### Real-time Notifications
**[PROJ-789]** (PR #456): Push notifications for important events.

Contributed by @janedoe in PR #456.
- Browser notifications
- Email digests
- Mobile push support

## Improvements

### Performance
- **[PROJ-234]**: Reduced API response time by 30% (PR #234)
- **Commits**: Optimized database indices (commit abc123)
- **[PROJ-567]**: Improved caching strategy (PR #345)

[...]
```

## Audience-Specific Formats

### For End Users

```markdown
# What's New in Version 2.0

## 🎨 Beautiful New Design
We've completely redesigned the interface to make it easier and more enjoyable to use.

## ⚡ Faster Than Ever
Everything is now 50% faster - from loading pages to running reports.

## 🌙 Dark Mode
Easy on your eyes with our new dark mode. Enable it in Settings.

## 🤝 Work Together in Real-Time
See what your teammates are doing as they work.

## How to Update
Click "Update" in the app, or download from [link].

## Need Help?
Check out our [Getting Started Guide] or contact support.
```

### For Developers

```markdown
# Release 2.0.0 - Technical Details

## API Changes

### New Endpoints
- `POST /api/v2/users` - Create user (replaces `/api/v1/users`)
- `GET /api/v2/notifications` - Get notifications

### Modified Endpoints
- `GET /api/v2/projects` - Added `include` parameter
- Response format changed to include pagination metadata

### Removed Endpoints
- `POST /api/v1/users` - Use v2 endpoint

## Database Migrations

```sql
-- Migration 2024_01_01_add_notifications_table
CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  ...
);
```

## Breaking Changes

### Authentication
OAuth 2.0 required. API keys deprecated (removal in 3.0).

**Migration**:
```javascript
// Old
api.setApiKey('your-key');

// New
api.setOAuth({
  clientId: 'your-client-id',
  clientSecret: 'your-secret'
});
```

### Response Format
All API responses now include standard metadata:

```json
{
  "data": { ... },
  "meta": {
    "version": "2.0",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

## Dependencies

### Updated
- React: 17.0 → 18.2
- Node.js: 16.x → 20.x (required)
- PostgreSQL: 13.x → 15.x (recommended)

### Added
- `@oauth/client` v2.0

### Removed
- `deprecated-library`

## Performance Benchmarks

| Metric | v1.0 | v2.0 | Improvement |
|--------|------|------|-------------|
| Dashboard Load | 2.0s | 1.0s | 50% |
| API Response | 200ms | 140ms | 30% |
| Memory Usage | 512MB | 307MB | 40% |
```

## Release Notes Checklist

Before publishing:

- [ ] **Version number** correct (semver: X.Y.Z)
- [ ] **Release date** accurate
- [ ] **All issues** from fixVersion included
- [ ] **Breaking changes** highlighted
- [ ] **Upgrade instructions** clear and complete
- [ ] **Known issues** documented
- [ ] **Contributors** credited
- [ ] **Links** working (docs, issues, PRs)
- [ ] **Reviewed** by product and engineering
- [ ] **Proofread** for typos and clarity

## Semantic Versioning Guide

### MAJOR version (X.0.0)
Breaking changes that require user action:
- API breaking changes
- Database schema changes
- Configuration format changes
- Removed features

### MINOR version (x.Y.0)
New features, backwards compatible:
- New functionality
- New API endpoints
- Performance improvements
- Deprecations (not removals)

### PATCH version (x.y.Z)
Bug fixes, backwards compatible:
- Bug fixes
- Security patches
- Documentation updates
- Dependency updates

## Best Practices

### 1. Write for Your Audience
- **Users**: Benefits and features
- **Developers**: Technical details and migration
- **Admins**: Deployment and configuration

### 2. Be Specific
- ❌ "Improved performance"
- ✅ "Dashboard loads 50% faster (2.0s → 1.0s)"

### 3. Highlight Breaking Changes
- Use warning symbols (⚠️)
- Explain what changed
- Provide migration guide
- Give timeline for deprecations

### 4. Credit Contributors
- Thank contributors
- Link to PRs/commits
- Recognize community

### 5. Use Clear Language
- Avoid jargon
- Explain technical terms
- Use examples

### 6. Link to Details
- Don't duplicate docs
- Link to migration guides
- Reference full documentation

## Confluence Organization

### Release Notes Structure

```
Product Documentation
├── Releases/
│   ├── Version 2.0.0
│   ├── Version 1.5.0
│   ├── Version 1.4.3
│   └── Version 1.4.2
├── Upgrade Guides/
│   ├── Upgrading to 2.0
│   ├── Upgrading to 1.5
│   └── Migration Scripts
└── Changelogs/
    ├── Complete Changelog
    └── Breaking Changes History
```

## How I'll Help

When generating release notes, I will:

1. **Gather information**:
   - Query Jira for issues in fixVersion
   - Parse git commits between tags
   - Read pull request descriptions
   - Review code changes

2. **Categorize changes**:
   - Group by type (features, bugs, etc.)
   - Identify breaking changes
   - Find deprecations
   - Note security updates

3. **Generate content**:
   - Write clear descriptions
   - Add context and benefits
   - Include technical details
   - Credit contributors

4. **Format for audience**:
   - User-friendly for end users
   - Technical for developers
   - Comprehensive for all

5. **Create in Confluence**:
   - Convert to ADF
   - Add formatting and styling
   - Link related docs
   - Update release index

6. **Review checklist**:
   - Verify completeness
   - Check for clarity
   - Validate links
   - Proofread

## Example Interaction

**You**: "Generate release notes for v2.5.0. Issues are in Jira fixVersion '2.5.0'"

**Me**: "I'll generate release notes for version 2.5.0.

[Searches Jira using /jira-search]

Found 23 issues:
- 8 new features
- 10 improvements
- 4 bug fixes
- 1 breaking change

[Reads issue details and parses commits]

**Draft Release Notes:**

# Version 2.5.0 - [Today's Date]

## Highlights
- New analytics dashboard with custom widgets
- API rate limiting improvements
- 25% performance improvement

## What's New
[Full detailed sections]

## Breaking Changes
⚠️ **API Authentication**: API keys deprecated, use OAuth 2.0
[Migration instructions]

[...]

Should I:
1. Create this in Confluence?
2. Adjust any sections?
3. Add more technical details?

Which Confluence space?"

**You**: "Looks good, create in space 123456"

**Me**: [Creates release notes page]
"Created 'Version 2.5.0 Release Notes' in space 123456!
Link: https://your-domain.atlassian.net/wiki/spaces/123456/pages/...

Also created upgrade guide and updated release index."
