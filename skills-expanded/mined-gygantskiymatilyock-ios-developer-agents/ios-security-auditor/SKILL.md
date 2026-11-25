# iOS Security Auditor

Use this skill to perform comprehensive security audits of iOS applications against OWASP Mobile Top 10 2024 and Apple security best practices.

## When to Use

- Before releasing to production
- After implementing authentication or payment features
- When handling sensitive user data
- During security review sprints
- After adding third-party SDKs
- When preparing for security certifications

## How to Apply

Read the full agent prompt from `agents/security-auditor/security-auditor.md` in the ios-developer-agents repository.

Follow the audit process covering OWASP Mobile Top 10 2024:

1. **M9: Data Storage Security** - Keychain, UserDefaults, file protection
2. **M1: Hardcoded Secrets** - API keys, tokens, credentials in code
3. **M5: Network Security** - ATS, TLS, certificate pinning
4. **M3: Authentication/Authorization** - Session management, token handling
5. **M4: Input Validation** - SQL injection, XSS, path traversal
6. **M7: Binary Protections** - Build settings, anti-tampering
7. **M2: Supply Chain** - Dependency vulnerabilities
8. **M6: Privacy/Data Leakage** - Logging, pasteboard, screenshots
9. **M8: Security Misconfiguration** - Info.plist, entitlements, WebViews

## Output Format

Provide structured findings with:
- OWASP Mobile Top 10 2024 coverage table
- Critical vulnerabilities (immediate action)
- High/Medium/Low risk issues
- Hardcoded secrets scan results
- Data storage audit
- Network security checklist
- Third-party dependencies review
