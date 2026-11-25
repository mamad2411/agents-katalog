---
name: github-commit-recovery
description: Recover deleted or force-pushed commits from GitHub using SHAs.
metadata:
  version: 0.2.0
  category: oss-forensics
---
# GitHub Commit Recovery

## Quick Start
```bash
# Get commit as patch file
curl -L https://github.com/org/repo/commit/SHA.patch

# Fetch specific "deleted" commit via Git
git fetch origin SHA
```

## Workflow
1. **Discovery**: Identify commit SHAs from GitHub Archive, git reflog, CI logs, or PR comments.
2. **Access**: Attempt direct web access (`/commit/SHA`) or raw access (`.patch`/`.diff`).
3. **API Query**: Use the REST API to retrieve structured metadata and author information.
4. **Git Fetch**: Use `git fetch origin SHA` to pull the commit into a local repository for deep analysis.
5. **Verification**: Verify commit authorship and GPG signatures for forensic validity.

## Rules & Constraints
- **RULE-1**: "Deleted" commits often remain accessible indefinitely on GitHub if you have the SHA.
- **RULE-2**: Authenticated API requests have a 5,000/hr limit; unauthenticated is 60/hr.
- **RULE-3**: Focus on author vs. committer discrepancies to identify forged identity.
- **RULE-4**: GitHub allows accessing commits with as few as 4 hex characters if unique.

## When to Use
- You have commit SHAs and need code content, diffs, or metadata.
- Investigating force-pushed commits that were "deleted" from history.
- Verifying commit authorship during a security incident.

## When NOT to Use
- Repository has been fully deleted (try `github-wayback-recovery` or forks).
- Private repository without appropriate API token access.

## References
- [Skill Manual](references/github-commit-recovery-manual.md)
- [GitHub REST API](https://docs.github.com/en/rest)
