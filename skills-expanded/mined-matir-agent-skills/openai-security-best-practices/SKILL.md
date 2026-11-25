---
name: openai-security-best-practices
description: Performs language and framework-specific security best-practice reviews. Used to generate security reports, detect vulnerabilities, and suggest secure-by-default improvements.
allowed-tools:
- Bash
- Read
- Grep
- Glob
- Write
- Edit
metadata:
  version: 0.2.0
  category: security
---
# Security Best Practices

## Quick Start
```bash
# Identify languages and frameworks to find relevant guidance
grep -r "dependencies" package.json requirements.txt Cargo.toml
ls references/*-security.md
```

## Workflow
1. **Identify Technologies**: Determine all primary languages and frameworks in the project (frontend and backend).
2. **Load Guidance**: Check `references/` for matching documentation (e.g., `<language>-<framework>-security.md`).
3. **Assess Codebase**: Passively detect vulnerabilities or conduct a formal review based on the loaded guidance.
4. **Generate Report**: Produce a prioritized `security_best_practices_report.md` with executive summary and severity sections.
5. **Apply Fixes**: Propose or implement secure-by-default fixes, focusing on one finding at a time to ensure functional integrity.

## Rules & Constraints
- **RULE-1**: Always look for BOTH frontend and backend guidance in web applications.
- **RULE-2**: Use existing project conventions for commits and testing when applying security fixes.
- **RULE-3**: Include line numbers and clear impact statements in all security reports.
- **RULE-4**: Prioritize high-impact vulnerabilities and secure defaults over minor stylistic issues.

## When to Use
- Explicit requests for security best practices guidance or a security review/report.
- Starting a new project where secure-by-default coding is required.

## When NOT to Use
- General code review, debugging, or non-security tasks.
- Unsupported languages or frameworks with no available guidance.

## References
- [Skill Manual](references/openai-security-best-practices-manual.md)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
