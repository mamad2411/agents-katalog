---
name: check-reference
description: Read references from various sources to verify correctness
argument-hint: "[scope]"
related:
  - review-devin-global-harness
  - check-secrets
  - update-references
  - check-types-definition
  - deep-research

---
## Goal

Read and verify references from various sources to confirm the accuracy of the information

## Scope

Verify references from files, web, CLI help, GitHub README, issues, package registry

## Execute

### 1. Read File References

> Goal: Read File References

1. Read references from files in the project
2. Verify that the information is accurate and up to date
3. Compare against the actual implementation
4. Check type-surface claims (options, defaults, types, signatures) for libs/config with `/check-types-definition` — the CLI table versus the real `.d.ts`/Rust source

### 2. Read Web References

> Goal: Read Web References

1. Look up information in the official documentation
2. Verify the accuracy of the information
3. Confirm it is the latest version
4. If several sources need deep verification (deprecations, breaking changes, conflicting claims) → run `/deep-research`

### 3. Read CLI Help

> Goal: Read CLI Help

1. Run `--help` or `-h` for CLI tools
2. Verify options and parameters
3. Verify the examples in the help output

### 4. Read GitHub References

> Goal: Read GitHub References

1. Read README.md from GitHub repositories
2. Read issues and discussions
3. Check the changelog and releases

### 5. Read Package Registry

> Goal: Read Package Registry

1. Check package information from npm, crates.io, PyPI
2. Verify versions and dependencies
3. Verify documentation links

## Rules

### 1. Source Priority

Use sources in order of reliability:
- Official documentation (highest)
- GitHub README and issues
- CLI help
- Package registry
- Community resources

### 2. Verification

Verify correctness:
- Cross-check against multiple sources
- Check version compatibility
- Test the examples for real

### 3. Currency

Check that the information is current:
- Check the last-updated date
- Check the latest version
- Check deprecation notices

- Use /check-types-definition if needed (type/API surface vs the real source)
- Use /deep-research if needed (deep verification across multiple sources)
- Use /review-devin-global-harness if needed
- Use /check-secrets secrets-leak if needed
- Use /update-references if needed

## Expected Outcome

- References from all sources are fully verified
- The information is accurate and up to date
- There is confidence in the correctness of the data
