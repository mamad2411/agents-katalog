---
name: security-audit
description: Perform a comprehensive security audit of selected code or recent changes. Use when auditing code, analyzing security implications of changes, or when asked about security vulnerabilities. Applies OWASP Top 10, CWE Top 25, and industry-standard security testing methodologies.
disable-model-invocation: false
---

# Security Audit Skill

Perform a comprehensive security audit of the selected code or recent changes. Apply a thorough security review methodology covering:

## Areas to Analyze

### Input Validation & Sanitization
- Are all inputs validated?
- Is validation applied at trust boundaries?
- Are there taint sources (user input, network data, files) reaching sensitive sinks?
- Look for: SQL injection, XSS, command injection, XXE, deserialization

### Authentication & Authorization
- How is authentication implemented?
- Are there privilege escalation risks?
- Is there proper authorization checks?
- Look for: IDOR, broken access control, privilege escalation

### Data Protection
- How is sensitive data handled?
- Are credentials/secrets properly protected?
- Is encryption used correctly?
- Look for: hardcoded secrets, weak crypto, data leaks

### Cryptographic Implementation
- Are cryptographic operations secure?
- Is randomness predictable?
- Are keys managed properly?
- Look for: custom crypto, predictable random, key leakage

### Session Management
- How are sessions managed?
- Are tokens secure?
- Is session fixation possible?
- Look for: session hijacking, token leakage

### Error Handling & Logging
- Do errors reveal sensitive info?
- Is PII being logged?
- Look for: information disclosure, verbose errors

### API Security
- Are APIs properly secured?
- Is there rate limiting?
- Are all endpoints authorized?
- Look for: mass assignment, rate limiting bypass, incomplete authorization

### Dependencies
- Are dependencies trusted?
- Are there known vulnerabilities?
- Look for: supply chain attacks, outdated components with CVEs

### Bundled Security Tools

Enhance your analysis by running these tools via Bash:

1. **check-headers.sh** - HTTP security header analysis:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-headers.sh <url>
   ```

2. **scan-secrets.sh** - Hardcoded secret detection (API keys, JWT, password/private keys):
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/scan-secrets.sh
   ```

3. **check-deps.sh** - Dependency vulnerability audits (NPM, Python pip, Go, Rust):
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-deps.sh
   ```

4. **check-ssrf.sh** - Server-Side Request Forgery pattern detection:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-ssrf.sh
   ```

5. **check-sqli.sh** - SQL Injection (SQLi) pattern detection across raw queries:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-sqli.sh
   ```

6. **check-cmd-injection.sh** - Command Injection & Remote Code Execution (RCE) scanner:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-cmd-injection.sh
   ```

7. **check-crypto-config.sh** - Weak cryptographic hash algorithms, open CORS settings, and information disclosures:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-crypto-config.sh
   ```

8. **check-docker.sh** - Container security checks for Dockerfiles and Docker Compose manifests:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-docker.sh
   ```

9. **check-xss.sh** - Cross-Site Scripting (XSS) static vulnerability scanner:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/tools/check-xss.sh
   ```

10. **check-path-traversal.sh** - Path/Directory Traversal vulnerability scanner:
    ```bash
    bash ${CLAUDE_PLUGIN_ROOT}/tools/check-path-traversal.sh
    ```

11. **check-auth-bypass.sh** - Authentication Bypass and raw JWT "none" algorithm scanner:
    ```bash
    bash ${CLAUDE_PLUGIN_ROOT}/tools/check-auth-bypass.sh
    ```

12. **check-deserialization.sh** - Unsafe deserialization and XML External Entity (XXE) scanner:
    ```bash
    bash ${CLAUDE_PLUGIN_ROOT}/tools/check-deserialization.sh
    ```

13. **sequential-thinking** MCP server - For complex vulnerability chains:
    - Chain multiple vulnerabilities together
    - Model attack scenarios
    - Analyze privilege escalation paths

## Output Format

Present findings in this structure:

```
### [SEVERITY] Finding Title

**Location:** file:line

**Issue:** Clear description

**Impact:** Real-world impact and attack scenario

**Remediation:** Specific, actionable fix
```

Sort findings by severity (CRITICAL > HIGH > MEDIUM > LOW > INFO).

When no issues found, briefly confirm the review covered key areas and note any strong security controls observed.