# Deprecation and Migration

## Description
Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code.

## Core Philosophy: Code as Liability

Every line of code is a liability, not an asset. Code must be:
- Read
- Tested
- Deployed
- Monitored
- Documented
- Secured

Unused or deprecated code still costs all of the above. Delete it aggressively, but delete it responsibly.

## Principles

### 1. Compulsory vs Advisory Deprecation

**Compulsory deprecation**: The old behavior stops working on a specific date.
- Breaking API changes
- Security vulnerabilities
- Infrastructure decommissioning
- Data format changes
- Timeline is non-negotiable

**Advisory deprecation**: The old behavior still works, but is no longer recommended.
- Performance improvements
- API ergonomics
- Feature consolidation
- Timeline is flexible, but has an end date

Always state clearly which type of deprecation is in effect. Ambiguity erodes trust.

### 2. Deprecation Communication

Every deprecation must include:
- **What** is being deprecated
- **Why** it is being deprecated
- **When** it will be removed (compulsory) or stop being supported (advisory)
- **What to use instead** (with migration path)
- **How to migrate** (step-by-step, code examples)
- **Who to contact** for help

### 3. Deprecation Lifecycle

```
Phase 1: Announcement
  - Mark as deprecated in documentation
  - Add runtime warning (log or header)
  - Send announcement to stakeholders
  - Create migration guide

Phase 2: Migration Window
  - Support both old and new in parallel
  - Provide migration tools/codemods
  - Track migration progress (metrics)
  - Offer office hours or migration support

Phase 3: Soft Removal
  - Old behavior returns 410 Gone or error
  - Still accessible via feature flag
  - Migration still possible but warned
  - Monitor for breakage

Phase 4: Hard Removal
  - Old code deleted from codebase
  - Old infrastructure decommissioned
  - Documentation updated
  - Post-mortem on migration success
```

### 4. Migration Patterns

**Strangler Fig Pattern**
Replace functionality incrementally behind the same interface.
```
Old API → Proxy → New API (gradually)
```
Best for: Service migrations, API rewrites

**Branch by Abstraction**
Create an abstraction layer, implement new behind it, switch over.
```
interface Feature {
  doThing(): void
}
class OldFeature implements Feature { ... }
class NewFeature implements Feature { ... }
```
Best for: Library replacements, SDK updates

**Parallel Run**
Run old and new simultaneously, compare outputs.
```
result_old = old_system(input)
result_new = new_system(input)
assert result_old == result_new
```
Best for: Data processing, calculation changes

**Feature Flag Gradual Rollout**
New code behind flag, enable for increasing percentages.
```
if featureFlags.enabled('new-feature', user):
  return new_behavior(user)
return old_behavior(user)
```
Best for: User-facing feature changes

**Blue/Green Deployment**
Two complete environments, switch traffic atomically.
- Old = blue (still running)
- New = green (fully deployed)
- Switch router from blue to green
- Keep blue for rollback
Best for: Infrastructure migrations, database changes

### 5. Zombie Code Removal

Zombie code is code that is no longer reachable, called, or tested. It accumulates through:
- Deprecation without removal
- Feature flags that are always-on
- A/B test variants that lost
- Dead codepaths from refactoring
- commented-out code (just delete it)

Zombie code detection:
- `git log --diff-filter=D --name-only` for deleted files still imported
- IDE dead code analysis (JS/TS: `ts-prune`, Python: `vulture`, Go: `deadcode`)
- Code coverage reports (0% coverage = suspicious)
- grep for `if (false)`, `// TODO: remove`, `// DEPRECATED`
- Search for feature flags that are 100% enabled

Zombie code removal checklist:
- [ ] Is this code called anywhere? (grep imports/exports)
- [ ] Is this code tested? (check coverage reports)
- [ ] Is this code documented? (check docs)
- [ ] Is this code depended on by external consumers? (check API usage)
- [ ] Is there a migration path? (if yes, provide it)
- [ ] Can I delete it and the system still compiles? (do it)
- [ ] Can I delete it and all tests pass? (run tests)

### 6. Sunset Timelines

| Deprecation Type | Warning Period | Migration Window | Total Timeline |
|-----------------|----------------|-----------------|----------------|
| Compulsory (security) | Immediate | 0-30 days | 30 days |
| Compulsory (breaking) | 3-6 months | 3-6 months | 6-12 months |
| Advisory (minor) | 1-2 releases | 2-4 releases | 3-6 releases |
| Advisory (internal) | 1 release | 1-2 releases | 2-3 releases |

### 7. Backward Compatibility Strategies

**Additive changes**: Never remove, always add.
- Add new parameters with defaults
- Add new endpoints, don't modify existing
- Add new fields, don't remove old

**Versioning strategies**:
- URL versioning: `/v1/`, `/v2/`
- Header versioning: `Accept: application/vnd.api+json;version=2`
- Parameter versioning: `?version=2`
- No versioning (backward compat always): safest but most constrained

**Compatibility layers**:
- Adapter pattern to wrap old interface around new implementation
- Deprecation proxy that forwards old calls to new with warnings
- Data migration scripts for format changes
- API Gateway for request/response transformation

### 8. Deprecation Checklist Template

```markdown
## Deprecation: [Feature/API Name]

**Type**: Compulsory / Advisory
**Announced**: YYYY-MM-DD
**Removal Date**: YYYY-MM-DD
**Owner**: @team-member
**Status**: Announcement / Migration / Soft Removal / Complete

### What
[Brief description of what is being deprecated]

### Why
[Reasons for deprecation]

### Replacement
[What to use instead]

### Migration Steps
1. [Step one]
2. [Step two]
3. [Step three]

### Migration Example
```
[Code example showing old → new]
```

### Tracking
- [ ] Migration guide published
- [ ] Runtime warnings added
- [ ] Stakeholders notified
- [ ] 25% migrated
- [ ] 50% migrated
- [ ] 75% migrated
- [ ] 100% migrated
- [ ] Old code deleted
- [ ] Documentation updated
- [ ] Post-mortem completed
```

## Usage
Load this skill when the user needs to deprecate a feature, migrate users between versions, or clean up dead code. Follow the deprecation lifecycle, provide clear communication templates, and ensure a smooth migration path.
