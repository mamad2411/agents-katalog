---
name: wp-rest-api-testing-and-review
description: Tests and reviews WordPress REST API structure, schemas, permissions, contracts, compatibility, upgrades, performance, and release readiness. Use before merge, release, or a WordPress/API upgrade.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Testing and Review

## Use this skill when

- Reviewing a REST API implementation or PR.
- Preparing a release.
- Upgrading WordPress, PHP, authentication, or client dependencies.
- Investigating a security, compatibility, or contract regression.
- Running the included route scanner.

## Approach

1. Establish exact compatibility and contract baselines.
2. Run the scanner with `--help`, then scan the relevant plugin/theme directory.
3. Inspect every registered route and controller.
4. Verify explicit permission callbacks and object-level authorization.
5. Verify schemas, validation, sanitization, responses, errors, links, and pagination.
6. Run positive and negative integration tests.
7. Review query bounds, cache scope, CORS, credentials, logs, and external dependencies.
8. Compare old/new contracts and client fixtures.
9. Document false positives, residual risks, migration, rollback, and release evidence.

## Workflows

- [rest-api-review-workflow.md](workflows/rest-api-review-workflow.md)
- [rest-api-upgrade-workflow.md](workflows/rest-api-upgrade-workflow.md)

## Resources

- [compatibility-and-test-matrix.md](resources/compatibility-and-test-matrix.md)
- [release-readiness-checklist.md](resources/release-readiness-checklist.md)
- [source-hierarchy.md](resources/source-hierarchy.md)

## Script

Run help first:

```powershell
python .agents/plugins/wp-rest-api-development/skills/wp-rest-api-testing-and-review/scripts/scan-wordpress-rest-api.py --help
```

The scanner is read-only and heuristic. Confirm every finding in source and tests.

## Output

Return:

- Routes and contracts reviewed.
- Findings by severity and confidence.
- Permission and negative-test evidence.
- Compatibility and client matrix.
- Performance/observability evidence.
- Fixes, accepted risks, migration, and rollback.
- Release recommendation.
