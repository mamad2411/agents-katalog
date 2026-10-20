---
name: snyk-fixing
description: Turn Snyk findings into fixes, upgrade paths, patches, ignores with expiry, and a clean PR workflow. Use when the user has scan results and wants their vulnerabilities remediated.
---

# Snyk fixing

Goal: clear findings with the smallest, safest change set. Always rescan after
each fix batch to confirm the finding is actually gone.

## Read the upgrade path first

`snyk test --json` gives you, per vulnerability:

- `upgradePath`: the exact chain of versions that removes the vuln
- `isUpgradable`: a direct or transitive upgrade exists
- `isPatchable`: a Snyk patch exists (mostly legacy npm)
- `fixedIn`: versions of the vulnerable package that contain the fix

Decision ladder, in order:

1. **Direct dependency upgrade**: bump the direct dep to the version in
   `upgradePath`. Prefer the minimal semver jump that clears the issue.
2. **Transitive fix via direct bump**: if the vuln is transitive, upgrading the
   direct parent shown in `upgradePath` usually pulls the fixed version.
3. **Override or resolution pin**: when no parent release exists yet, pin the
   transitive dep (`overrides` in package.json, `resolutions` for yarn,
   dependency constraints for Gradle, `[tool.poetry.dependencies]` pins).
4. **Ignore with expiry**: last resort, never permanent (below).

## Automated fixes

```bash
snyk fix                          # apply supported upgrades automatically
snyk fix --dry-run                # preview the changes first
```

`snyk fix` supports a subset of ecosystems (notably Python and npm); when it
declines, fall back to manual bumps from `upgradePath`. For Snyk Code findings
there is no dependency to bump: fix the code itself (parameterize the query,
validate the input, replace the unsafe API) and rerun `snyk code test`.

## Ignore policy (.snyk file)

```bash
snyk ignore --id=SNYK-JS-LODASH-567746 \
  --reason="Not reachable: field only used with static config" \
  --expiry=2026-10-01
```

Rules for defensible ignores:

- Always include `--reason` and `--expiry`; review expired ignores in PRs.
- Commit `.snyk` so ignores are visible in code review, not hidden in the UI.
- Ignore a finding, never a whole severity class.

## PR workflow

1. Branch per fix batch: group by ecosystem or by direct dependency.
2. In the PR body, paste the Snyk IDs cleared and the before/after counts from
   `snyk test --severity-threshold=high`.
3. Run the project test suite; dependency bumps are only safe if tests pass.
4. Gate merge on exit code 0 (or 1 with only accepted, expiring ignores).
5. After merge, `snyk monitor` on the default branch so drift gets alerts.

## Verifying a fix

```bash
snyk test --json | jq '[.vulnerabilities[] | select(.severity=="critical" or .severity=="high")] | length'
```

Zero means the high-and-up backlog is clear. Keep medium/low in a tracked
backlog rather than letting them rot unscanned.
