---
name: python-library-review
description: Comprehensively reviews Python libraries for quality across project structure, packaging, code quality, testing, security, documentation, API design, and CI/CD. Provides actionable feedback. Use when evaluating library health, preparing for major releases, or auditing dependencies.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: wdm0006
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F50D"
    homepage: https://github.com/wdm0006/python-skills
---

# Python Library Review

## Quick Health Check (5 min)

```bash
git clone https://github.com/user/package && cd package
cat pyproject.toml                    # Modern config?
ls tests/ && pytest --collect-only   # Tests exist?
pytest --cov=package | tail -20      # Coverage?
pip install bandit && bandit -r src/ # Security?
```

## Review Dimensions

| Area | Check For |
|------|-----------|
| Structure | src/ layout, py.typed marker |
| Packaging | pyproject.toml (not setup.py) |
| Code | Type hints, docstrings, no anti-patterns |
| Tests | 80%+ coverage, edge cases |
| Security | No secrets, input validation, pip-audit clean |
| Docs | README, API docs, changelog |
| API | Consistent naming, sensible defaults |
| CI/CD | Tests on PR, multi-Python, security scans |

## Red Flags

- No tests
- No type hints
- setup.py only (no pyproject.toml)
- Pinned exact versions for all deps
- No LICENSE file
- Last commit > 1 year ago

## Green Flags

- Active maintenance (recent commits)
- High test coverage (>85%)
- Comprehensive CI/CD
- Type hints throughout
- Clear documentation
- Semantic versioning

## Report Template

```markdown
# Library Review: [package]

**Rating:** [Excellent/Good/Needs Work/Significant Issues]

## Strengths
- [Strength 1]

## Areas for Improvement
- [Issue 1] - Severity: High/Medium/Low

## Category Scores
| Category | Score |
|----------|-------|
| Structure | ⭐⭐⭐⭐⭐ |
| Testing | ⭐⭐⭐☆☆ |
| Security | ⭐⭐⭐⭐☆ |

## Recommendations
1. [High priority action]
```

## Best Practices Checklist

```
Essential:
- [ ] pyproject.toml valid
- [ ] Tests exist and pass
- [ ] README has install/usage
- [ ] LICENSE present
- [ ] No hardcoded secrets

Important:
- [ ] Type hints on public API
- [ ] CI runs tests on PRs
- [ ] Coverage > 70%
- [ ] Changelog maintained

Recommended:
- [ ] src/ layout
- [ ] py.typed marker
- [ ] Security scanning in CI
- [ ] Contributing guide
```

## Cross-References

- `python-project-setup` — project structure
- `python-code-quality` — linting, type hints
- `python-testing` — test patterns, coverage
- `python-security` — security auditing
- `python-documentation` — docs quality
- `python-api-design` — API quality
- `python-packaging` — distribution quality
