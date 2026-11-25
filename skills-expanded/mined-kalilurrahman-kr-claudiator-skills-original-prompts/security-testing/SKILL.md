---
name: security-testing
description: Design and execute security testing programs covering OWASP Top 10, SAST, DAST, dependency scanning, and penetration testing. Outputs test plans, tool configurations, CI integration, and remediation tracking.
argument-hint: [application type, compliance requirements, threat model, existing tooling]
allowed-tools: Read, Write, Bash
---

# Security Testing

Security testing is not a one-time event before launch — it is a continuous practice. Layer automated scanning in CI with periodic manual testing to catch vulnerabilities before attackers do.

## Process

1. **Threat model first** — identify assets, threats, and attack surfaces.
2. **SAST in CI** — static analysis on every PR, fail build on critical findings.
3. **Dependency scanning** — known CVEs in third-party libraries.
4. **Secrets scanning** — detect leaked credentials before they're committed.
5. **DAST against staging** — dynamic testing against running application.
6. **Manual penetration test** — quarterly or before major releases.
7. **Remediation tracking** — SLA-based fix prioritization.

## Output Format

### Security Testing Matrix

| Layer | Tool | Frequency | Blocks CI? | Scope |
|-------|------|-----------|-----------|-------|
| Secrets scanning | Gitleaks, Trufflehog | Every commit | Yes | Code + history |
| SAST | Semgrep, Bandit (Python) | Every PR | Yes (critical) | Source code |
| Dependency scan | Dependabot, Trivy, Safety | Daily | Yes (critical CVE) | Dependencies |
| Container scan | Trivy, Grype | Every image build | Yes (critical) | Docker images |
| DAST | OWASP ZAP | Staging deploy | No (report only) | Running app |
| Manual pentest | External firm / internal | Quarterly | N/A | Full scope |

### CI Security Pipeline

```yaml
# .github/workflows/security.yml
name: Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 6 * * *'  # Daily dependency scan

jobs:
  secrets:
    name: Secrets Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for pre-commit scan
      
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
      
      - name: Trufflehog (additional patterns)
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: |
            p/security-audit
            p/python
            p/javascript
            p/owasp-top-ten
          auditOn: push
          publishResults: true
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
      
      - name: Bandit (Python SAST)
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json -ll  # Only medium+ severity
        continue-on-error: true
      
      - name: Upload SAST results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: bandit-report.json

  dependencies:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Python
      - name: Safety check
        run: |
          pip install safety
          safety check --json -o safety-report.json || true
          python -c "
          import json, sys
          report = json.load(open('safety-report.json'))
          critical = [v for v in report.get('vulnerabilities', []) if v.get('severity') == 'critical']
          if critical:
              print(f'CRITICAL CVEs found: {len(critical)}')
              for v in critical:
                  print(f'  {v[\"package_name\"]} {v[\"analyzed_version\"]}: {v[\"advisory\"]}')
              sys.exit(1)
          "
      
      # Node.js
      - name: npm audit
        run: npm audit --audit-level=critical
      
      # Container
      - name: Trivy container scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ghcr.io/${{ github.repository }}:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
          vuln-type: 'os,library'

  dast:
    name: DAST (Staging)
    runs-on: ubuntu-latest
    needs: [sast, dependencies]
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'https://staging.api.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -j'
          fail_action: false   # Report only — don't fail staging deploys
        continue-on-error: true
      
      - name: Upload ZAP report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report-${{ github.run_id }}
          path: report_html.html
```

### Semgrep Custom Rules

```yaml
# .semgrep/custom.yml — project-specific security rules
rules:
  - id: no-hardcoded-secrets
    pattern-either:
      - pattern: $X = "sk-..."
      - pattern: password = "..."
      - pattern: api_key = "..."
      - pattern: secret = "..."
    message: "Hardcoded secret detected: $X"
    severity: ERROR
    languages: [python, javascript, typescript]

  - id: no-eval
    pattern-either:
      - pattern: eval(...)
      - pattern: exec(...)
    message: "Code execution via eval/exec is dangerous"
    severity: WARNING
    languages: [python]

  - id: sql-injection
    pattern-either:
      - pattern: |
          cursor.execute("... %s ..." % $USER_INPUT)
      - pattern: |
          cursor.execute(f"... {$USER_INPUT} ...")
    message: "Potential SQL injection: use parameterized queries"
    severity: ERROR
    languages: [python]
  
  - id: insecure-random
    pattern: random.random()
    message: "Use secrets.token_hex() for security-sensitive randomness"
    severity: WARNING
    languages: [python]
    paths:
      include:
        - "*/auth/*"
        - "*/tokens/*"

  - id: debug-in-production
    pattern-either:
      - pattern: app.run(debug=True)
      - pattern: DEBUG = True
    message: "Debug mode must not be enabled in production"
    severity: WARNING
    languages: [python]
```

### OWASP ZAP Configuration

```python
# security_tests/zap_test.py — programmatic ZAP scanning
from zapv2 import ZAPv2
import time
import sys

def run_zap_scan(target_url: str, report_path: str = "zap-report.html"):
    zap = ZAPv2(apikey="your-api-key", proxies={"http": "http://localhost:8080"})
    
    print(f"Scanning {target_url}")
    
    # Spider (crawl) the target
    scan_id = zap.spider.scan(target_url)
    while int(zap.spider.status(scan_id)) < 100:
        print(f"Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(2)
    
    # Active scan
    scan_id = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(5)
    
    # Get alerts
    alerts = zap.core.alerts(baseurl=target_url)
    
    # Classify by risk
    critical = [a for a in alerts if a["risk"] == "High"]
    medium = [a for a in alerts if a["risk"] == "Medium"]
    low = [a for a in alerts if a["risk"] == "Low"]
    
    print(f"\nResults: {len(critical)} High, {len(medium)} Medium, {len(low)} Low")
    
    for alert in critical:
        print(f"[HIGH] {alert['name']}: {alert['url']}")
        print(f"  Solution: {alert['solution'][:100]}")
    
    # Generate HTML report
    with open(report_path, "w") as f:
        f.write(zap.core.htmlreport())
    
    # Exit code for CI
    return len(critical)


# .zap/rules.tsv — disable false-positive rules
# ID    ACTION  PARAMETER
# 10015 IGNORE              # Re-examine this rule: CSP wildcard (false positive for staging)
# 10020 IGNORE              # X-Frame-Options (handled by API responses only)
```

### Manual Penetration Test Checklist (OWASP Top 10)

```markdown
# Penetration Test Checklist — OWASP Top 10

## A01: Broken Access Control
- [ ] Test horizontal privilege escalation (access other users' data with own token)
- [ ] Test vertical privilege escalation (access admin functions with user token)
- [ ] Test IDOR (modify resource IDs in requests)
- [ ] Test JWT: algorithm confusion (HS256/RS256 swap), none algorithm, expired tokens
- [ ] Test CORS: does the API accept arbitrary origins?
- [ ] Test directory traversal: /api/files?name=../../etc/passwd

## A02: Cryptographic Failures
- [ ] Is PII transmitted over HTTP anywhere?
- [ ] Are passwords hashed with bcrypt/argon2 (not MD5/SHA1)?
- [ ] Are backup files encrypted?
- [ ] Is TLS 1.0/1.1 disabled?

## A03: Injection
- [ ] SQL injection: ', "; DROP TABLE--, UNION SELECT
- [ ] NoSQL injection: $where, $gt, $ne operators
- [ ] Command injection: ; ls, && cat /etc/passwd
- [ ] XSS: <script>alert(1)</script>, javascript: in href
- [ ] SSTI: {{7*7}}, <%= 7*7 %>

## A04: Insecure Design
- [ ] Can users reset any account's password with just an email?
- [ ] Are account lockout thresholds reasonable?
- [ ] Are rate limits applied to sensitive actions?

## A05: Security Misconfiguration
- [ ] Default credentials on admin panels?
- [ ] Debug endpoints exposed (/debug, /phpinfo, /actuator)?
- [ ] Stack traces in error responses?
- [ ] Are cloud storage buckets public?
- [ ] Unnecessary services running?

## A06: Vulnerable Components
- [ ] Run: trivy image, safety check, npm audit
- [ ] Are server headers revealing library versions?

## A07: Authentication Failures
- [ ] Password policy: minimum length, breach check?
- [ ] Session tokens: random, long, HTTP-only, secure?
- [ ] Is there brute force protection on login?
- [ ] Are sessions invalidated on logout?
- [ ] MFA bypass techniques?

## A08: Software & Data Integrity
- [ ] Are software updates verified? (signed packages)
- [ ] CI/CD pipeline: can PRs modify workflow files?
- [ ] Deserialization: pickle, YAML.load, PHP unserialize

## A09: Logging Failures  
- [ ] Are failed login attempts logged?
- [ ] Are admin actions logged?
- [ ] Are logs accessible to developers in production?
- [ ] Is sensitive data being logged?

## A10: SSRF
- [ ] Any URL parameters fetched by the server?
- [ ] File upload: can SVGs/PDFs trigger outbound requests?
- [ ] Test internal endpoints: http://169.254.169.254/latest/meta-data
```

### Vulnerability Remediation SLAs

```yaml
# sla-policy.yaml
remediation_sla:
  critical:
    description: "Active exploitation or direct access to sensitive data"
    examples:
      - "SQL injection with data exfiltration"
      - "Authentication bypass"
      - "Remote code execution"
    fix_within: 24h
    escalation: "CTO + Security lead"
  
  high:
    description: "Significant security risk, not yet exploited"
    examples:
      - "XSS with session theft potential"
      - "IDOR exposing other users' PII"
      - "Critical CVE in dependency"
    fix_within: 7d
    escalation: "Engineering lead"
  
  medium:
    description: "Security risk with limited impact or requires preconditions"
    examples:
      - "Information disclosure of non-sensitive data"
      - "Missing security headers"
      - "Medium CVE in dependency"
    fix_within: 30d
    escalation: "Team lead"
  
  low:
    description: "Best practice violations, defense-in-depth"
    examples:
      - "Verbose error messages"
      - "Missing rate limiting on non-sensitive endpoint"
    fix_within: 90d
    escalation: "Backlog"
```

## Rules

- **Security testing in CI, not just release gates** — shift-left means catching issues at the PR stage.
- **Never ignore SAST findings without documented justification** — suppression comments must explain why.
- **Rotate any secret found in code immediately** — assume it's compromised the moment it's committed.
- **DAST on production-like environment only** — active scanning on production causes real disruption.
- **Fix critical CVEs within 24h** — a known CVE with a published exploit is actively being used.
- **Verify fixes, don't just close tickets** — retest to confirm the vulnerability is actually resolved.
- **Document false positives** — suppression without explanation is a liability in audits.
- **Separate security branch** — never merge a security fix branch through the normal PR process if it exposes a vulnerability publicly before the fix is deployed.
- **Bug bounty acknowledgment** — if you have a public-facing product, consider a responsible disclosure policy.
- **Test your test tooling** — periodically verify scanner tools are actually working by injecting a known vulnerability.
