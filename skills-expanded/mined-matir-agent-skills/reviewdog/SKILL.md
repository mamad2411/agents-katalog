---
name: reviewdog
description: Automated code review and security linting integration for CI/CD pipelines.
metadata:
  version: 0.2.0
  category: secsdlc
---
# Reviewdog - Automated Security Code Review

## Quick Start
```bash
# Install reviewdog
go install github.com/reviewdog/reviewdog/cmd/reviewdog@latest

# Run a security scanner and pipe to reviewdog
bandit -r . -f json | reviewdog -f=bandit -reporter=github-pr-review
```

## Workflow
1. **Installation**: Install reviewdog via Go, Homebrew, or Docker in your CI environment.
2. **Configuration**: Choose the security scanners (Semgrep, Bandit, Gitleaks, etc.) to integrate.
3. **Integration**: Add reviewdog to your CI pipeline (GitHub Actions, GitLab CI) using the appropriate reporter.
4. **Behavior Setup**: Configure filtering (`-filter-mode`) and gating (`-fail-on-error`) rules.
5. **Review**: Analyze inline security annotations posted directly on pull request code lines.

## Rules & Constraints
- **RULE-1**: NEVER commit API tokens to version control; use CI secrets.
- **RULE-2**: Use minimum required permissions for API tokens (read/write on PRs).
- **RULE-3**: Configure reviewdog to run only on trusted branches.
- **RULE-4**: Prefer `filter-mode=added` to focus on new vulnerabilities.

## When to Use
- Integrating security scanning into code review workflows.
- Automating security feedback on pull requests.
- Consolidating multiple tool outputs into unified review comments.

## When NOT to Use
- Local development without a supported code hosting platform for reporters.
- One-off scans not intended for code review integration.

## References
- [Skill Manual](references/reviewdog-manual.md)
- [Official Documentation](https://github.com/reviewdog/reviewdog)
- [Supported Tools](references/supported_tools.md)
