---
name: dependency-management
version: 1.0.0
description: Evaluate, update, and audit project dependencies
uses:
  - analysis/research
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:read
    - file:write
    - command:execute
  requires_approval: false
---

# Dependency Management

Evaluate, update, and audit project dependencies. This skill covers the full dependency lifecycle — adding new dependencies, updating existing ones, auditing for security vulnerabilities, and removing unused dependencies.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `manage_dependencies` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Adding a new dependency to the project
- Updating dependencies to newer versions
- Auditing dependencies for security vulnerabilities
- Removing unused dependencies
- Resolving dependency conflicts
- Evaluating whether to add a dependency or implement the functionality

## Methodology

### 1. Evaluate New Dependencies

Before adding any dependency, assess:

| Criterion | Question | Red Flag |
|-----------|----------|----------|
| **Necessity** | Can we do this without a dependency? | Simple functionality that's easy to implement |
| **Maintenance** | Is it actively maintained? | No commits in 12+ months |
| **Popularity** | Is it widely used? | Very few downloads or stars |
| **Size** | How large is it? | Massive dependency for a small feature |
| **License** | Is the license compatible? | GPL in a proprietary project |
| **Security** | Are there known vulnerabilities? | Unpatched CVEs |
| **Quality** | Is the code well-tested? | No tests, no CI |
| **Alternatives** | Are there better options? | Standard library covers this |

**Decision rule**: Don't add a dependency for something you can write in 50 lines of well-tested code. Dependencies are liabilities, not assets.

### 2. Update Dependencies

When updating:
1. **Check what's outdated**: Use the ecosystem's tool (`npm outdated`, `pip list --outdated`, `cargo outdated`, etc.)
2. **Read changelogs**: Understand what changed between versions
3. **Check for breaking changes**: Major version bumps usually mean breaking changes
4. **Update incrementally**: Update one dependency at a time, not all at once
5. **Run tests**: After each update, verify nothing broke
6. **Check for deprecations**: Look for deprecation warnings in test output

### 3. Security Audit

Regularly audit for known vulnerabilities:
1. **Run the audit tool**: `npm audit`, `pip-audit`, `cargo audit`, etc.
2. **Assess severity**: Critical and high vulnerabilities need immediate attention
3. **Check for patches**: Is a patched version available?
4. **If no patch**: Evaluate workarounds, alternative packages, or implementing the functionality yourself

### 4. Remove Unused Dependencies

Identify and remove dependencies that are no longer used:
1. **Scan imports**: Check if the dependency is actually imported anywhere
2. **Check build config**: Some dependencies are build-only or dev-only
3. **Remove carefully**: Remove one at a time and verify tests pass
4. **Update lock file**: Ensure the lock file reflects removals

### 5. Resolve Conflicts

When dependencies conflict:
1. **Identify the conflict**: Which dependencies require incompatible versions of a shared dependency?
2. **Check compatibility**: Can one of the conflicting dependencies be updated to resolve it?
3. **Use resolution overrides**: If available in the ecosystem (npm overrides, pip constraints)
4. **Consider alternatives**: Replace one of the conflicting dependencies

### 6. Lock File Management

- **Always commit lock files** (package-lock.json, Pipfile.lock, Cargo.lock, etc.)
- **Don't manually edit lock files** — regenerate them
- **Regenerate after changes** — after any add/remove/update, regenerate the lock

## Output Format

```
## Dependency Management: [Project]

### Current State
- Package manager: [npm/pip/cargo/etc.]
- Total dependencies: [count]
- Outdated: [count]
- Vulnerable: [count]

### Actions Taken
| Action | Package | From | To | Reason |
|--------|---------|------|----|--------|
| [add/update/remove/audit] | [name] | [old version] | [new version] | [why] |

### Security Audit
| Package | Severity | CVE | Status |
|---------|----------|-----|--------|
| [name] | [critical/high/medium/low] | [CVE-ID] | [fixed/pending/no-patch] |

### Verification
- Tests: [pass/fail]
- Build: [pass/fail]
- Deprecation warnings: [none/list]

### Recommendations
- [prioritized action items]
```

## Quality Criteria

- New dependencies are evaluated before adding (not added reflexively)
- Updates are incremental (one at a time, with tests)
- Security vulnerabilities are identified and addressed
- Unused dependencies are removed
- Lock files are committed and up to date
- Breaking changes are identified before updating
- Tests pass after every dependency change

## Common Mistakes

- **Adding dependencies without evaluation**: Installing the first package that comes up without checking maintenance, size, or alternatives. Every dependency is a long-term liability.
- **Updating everything at once**: Running `npm update` or `pip install --upgrade` on everything simultaneously. If tests break, you won't know which update caused it.
- **Ignoring security audits**: Not running audit tools means shipping known vulnerabilities. Audit regularly.
- **Not reading changelogs**: Updating to a new major version without checking for breaking changes. Always read the changelog.
- **Keeping unused dependencies**: Dependencies that aren't used still get installed, audited, and can have vulnerabilities. Remove them.
- **Not committing lock files**: Without lock files, different environments get different dependency versions, causing "works on my machine" bugs.
- **Using exact versions everywhere**: Pinning exact versions prevents automatic security patches. Use version ranges that allow patch updates.

## Completion

Dependency management is complete when:
- Dependencies are evaluated/updated/audited as requested
- Security vulnerabilities are identified and addressed
- Unused dependencies are removed
- Tests pass after all changes
- Lock files are up to date and committed
- Recommendations for future actions are provided
