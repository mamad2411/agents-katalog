---
name: "release-note-patterns"
description: "Release note writing patterns: audience-first and benefit-first entries, breaking change, deprecation, and security release patterns, comparison links, and anti-patterns such as the git log dump. Use when writing the content of release notes."
---

# Release Note Patterns

## Audience-First Writing

The most common release note mistake: writing for the audience who built the feature, not the audience who uses it. Before writing, answer: "Who reads this, and what question are they trying to answer?"

| Audience | Their Question | Write This |
|----------|---------------|-----------|
| End user | "Can I do something new?" | "You can now export reports as PDF" |
| API developer | "Does this break my code?" | "Added `format` parameter to `export()`" |
| DevOps | "Does this affect my deployment?" | "New required env var: `EXPORT_SERVICE_URL`" |
| Internal | "What changed and why?" | Full technical description with PR link |

## The Benefit-First Pattern

Lead with the user benefit, follow with the technical detail:

```markdown
# Bad: technical-first
Added `maxRetries` parameter to `ApiClient` constructor with exponential backoff.

# Good: benefit-first
API calls now automatically retry on transient failures.

The new `maxRetries` option (default: 3) controls retry behavior with
exponential backoff. Set to 0 to disable retries.
```

## Breaking Change Pattern

Breaking changes have exactly three required parts. Missing any one causes user frustration:

```markdown
### Breaking: Config file renamed from `.toolrc` to `.tool.config.json`

**Why**: The new format supports comments and arrays of values that .rc syntax cannot.

**Before (v1.x):**
```
# .toolrc
timeout=30
```

**After (v2.0+):**
```json
// .tool.config.json
{
  "timeout": 30
}
```

**Migrate**: Run `npx tool-migrate` to auto-convert your config file,
or manually create `.tool.config.json` from the template in the docs.
```

What makes this work:
- **What changed**: The config file name and format
- **Why it changed**: Reason users can understand and accept
- **How to migrate**: Automated option first, manual second

## Deprecation Pattern

Deprecations need an expiry date to be actionable:

```markdown
# Bad: deprecation without timeline
`QueryBuilder.raw()` is deprecated. Use `QueryBuilder.sql()` instead.

# Good: deprecation with deadline
**Deprecated**: `QueryBuilder.raw()` will be removed in v4.0 (expected Q3 2025).

Use `QueryBuilder.sql()` instead, which provides parameterized input
and prevents SQL injection by default.

```typescript
// Before
db.raw(`SELECT * FROM users WHERE id = ${userId}`);

// After (parameterized -- prevents injection)
db.sql`SELECT * FROM users WHERE id = ${userId}`;
```
```

## Security Release Pattern

Security releases follow a specific order of disclosure vs. disclosure:

```markdown
# Bad: too much detail before patch is widely deployed
Fixed SQL injection in /api/users endpoint. The `name` parameter
was concatenated directly into the query without sanitization.

# Good: enough detail to verify patching, not enough to exploit
### Security: Fixed input validation in user search (CVE-2024-XXXXX)

All users should upgrade to v2.1.3. A security advisory with full
technical details will be published 30 days after this release.

**Affected versions**: v2.0.0 - v2.1.2
**Fixed in**: v2.1.3
**Severity**: High (CVSS 8.1)
**Credit**: [Researcher Name] via responsible disclosure
```

## Version Comparison Link

Every GitHub release must end with a comparison link. This is the most-clicked element for developers evaluating an upgrade:

```markdown
**Full Changelog**: https://github.com/{owner}/{repo}/compare/v{prev}...v{current}
```

Generate with: `git log v1.9.0..v2.0.0 --oneline`

## Changelog vs. GitHub Release vs. Blog Post

The same version produces different documents for different channels:

| Channel | Audience | Length | Code Examples | Marketing Language |
|---------|----------|--------|---------------|-------------------|
| CHANGELOG.md | Developers | Complete | Yes | No |
| GitHub Release | Developers | Medium | Key changes | Minimal |
| Blog post | All | Long | Yes | Yes |
| In-app notification | End users | Short (3-5 bullets) | No | Yes |
| Email newsletter | End users | Short | No | Yes |

Do not copy-paste between channels. Rewrite for each audience.

## Anti-Patterns

### The Git Log Dump
```
# Bad: raw git log as release notes
- fix: resolve issue #123
- chore: update dependencies
- feat: add new endpoint
- fix: typo in error message

# Good: curated entries with user context
### Bug Fixes
- Fixed a crash that occurred when exporting large datasets (#123)

### New Features
- Added CSV export for all report types
```

### The Changelog Without Links
Bug fixes must link to the issue or PR. Users need to confirm their specific bug is fixed:
```markdown
# Bad
Fixed a crash when importing CSV files with special characters.

# Good
Fixed a crash when importing CSV files with special characters. (#456)
```

### The Missing Migration Guide
Any entry in "Breaking Changes" without a migration guide is incomplete. If you cannot write the migration steps, the feature is not ready to ship.

### The Vague Security Notice
```
# Bad: too vague to act on
Fixed a security vulnerability.

# Good: enough to act on, not enough to exploit
Fixed an authentication bypass in the API token validation (CVE-2024-12345).
Upgrade to v2.1.1 immediately. All v2.0.x versions are affected.
```

## References
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub: Release pages docs](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Stripe API Changelog](https://stripe.com/docs/upgrades) - example of excellent breaking change documentation
