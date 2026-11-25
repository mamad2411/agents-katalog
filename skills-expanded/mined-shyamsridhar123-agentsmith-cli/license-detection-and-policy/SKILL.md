---
name: license-detection-and-policy
description: Detect repository license from files and config, classify permissiveness, and gate generation.
---

# License Detection And Policy

Detect repository license from files and config, classify permissiveness, and gate generation.

## When to Use

Use this skill when:

- Working with code in `src/utils/license.ts/`
- User mentions "license"
- User mentions "permissive"
- User mentions "spdx"
- User mentions "MIT"
- User mentions "GPL"
- User mentions "policy"

## Patterns

- pattern-based SPDX detection across common files
- package.json and pyproject.toml license fallback
- proprietary indicators
- status formatting for CLI output

## Examples

```
const lic = await detectLicense(repoPath); formatLicenseStatus(lic);
```

## Category

**security** - Authentication, authorization, and data protection
