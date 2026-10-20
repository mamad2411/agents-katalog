---
name: penetration-testing
description: Penetration testing and vulnerability assessment — Test planning, methodologies, scope, reporting, remediation tracking
globs: ["**/*.md", "**/*.yaml", "**/*.yml", "**/*.tf"]
alwaysApply: false
---

# Penetration Testing & Vulnerability Assessment

Penetration testing systematically identifies security weaknesses before attackers do. Plan methodically, document findings, remediate responsibly, and re-test verification.

---

## Penetration Test Planning

**ALWAYS**:
- Define scope clearly (systems in scope, out of scope)
- Set test windows (off-peak, avoid production outages)
- Obtain written authorization (signed Rules of Engagement)
- Establish communication channels (escalation contacts)
- Set success criteria (vulnerabilities to find, risk threshold)
- Schedule pre- and post-test meetings
- Plan remediation timeline (critical: 24-48 hours, high: 1 week, medium: 2 weeks)

**NEVER**:
- Test without authorization (illegal)
- Test production without stakeholder approval
- Change system state without approval
- Exceed scope (test only in-scope systems)
- Disclose findings before remediation window closes

### ✅ GOOD Pentest Planning

```yaml
# Penetration Test Scope & Rules of Engagement
engagement:
  name: "Q2 2026 Security Assessment"
  client: "ACME Corp"
  start_date: "2026-04-15"
  end_date: "2026-04-22"
  test_window: "22:00-06:00 UTC (off-peak)"
  
scope:
  in_scope:
    - "api.example.com" (all endpoints)
    - "admin.example.com" (authenticated users only)
    - "mobile app v3.0+" (iOS, Android)
    - "SSL/TLS configuration"
    - "Authentication & authorization"
    - "Data handling & storage"
    - "API rate limiting"
    
  out_of_scope:
    - "Third-party services (AWS, Azure, etc.)"
    - "Production database backups"
    - "Customer PII (testing only with test data)"
    - "Social engineering (not approved)"
    - "Physical security"
    - "Legacy system (scheduled for retirement)"
    
  excluded_tests:
    - "Denial of service (DoS) attacks"
    - "Data exfiltration with real customer data"
    - "Destructive attacks"

authorization:
  signature_required: true
  authorized_by: "Chief Security Officer"
  date_approved: "2026-04-08"
  contact_escalation: "security@example.com"
  contact_emergency: "+1-555-0100"

success_criteria:
  find_critical_vulns: true
  find_high_vulns: true
  test_authentication: true
  test_authorization: true
  identify_misconfigurations: true
  
remediation_timeline:
  critical: "24-48 hours"
  high: "1 week"
  medium: "2 weeks"
  low: "1 month"
```

---

## Testing Methodologies

**ALWAYS**:
- Follow OWASP Top 10 (Web), OWASP Mobile Top 10, OWASP API Top 10
- Use NIST framework (reconnaissance, scanning, enumeration, exploitation)
- Test all attack vectors (input validation, authentication, authorization, crypto)
- Document every step (for audit trail)
- Take screenshots/logs (evidence for report)
- Maintain chain of custody (findings traceable)

**NEVER**:
- Use untested exploits (could crash systems)
- Exploit without understanding impact
- Move laterally beyond initial compromise scope
- Delete/modify data (testing only)

### ✅ GOOD Testing Approach

```yaml
# NIST Penetration Test Phases

phase_1_reconnaissance:
  description: "Gather information about target"
  techniques:
    - "WHOIS lookup (domain info)"
    - "DNS enumeration (subdomains)"
    - "Google dorking (indexed info)"
    - "Shodan search (exposed services)"
    - "Certificate transparency logs"
    - "Employee research (LinkedIn)"
  tools:
    - "nmap" (network scanning)
    - "whois" (domain information)
    - "dig/nslookup" (DNS queries)
    - "theHarvester" (email discovery)
  output:
    - "Target overview (domains, IP ranges, employees)"
    - "Network topology diagram"
    - "Technology stack identified"

phase_2_scanning:
  description: "Identify live systems and services"
  techniques:
    - "Network scanning (nmap, -sS for SYN scan, -A for aggressive)"
    - "Service enumeration (version detection)"
    - "Web scanning (nikto, burp suite)"
    - "Vulnerability scanning (nessus, qualys)"
  tools:
    - "nmap" (port scanning)
    - "nikto" (web server scanning)
    - "burp suite community" (web application scanning)
    - "nessus" (vulnerability scanning)
  output:
    - "Open ports & services"
    - "Software versions identified"
    - "Known CVEs matching versions"

phase_3_enumeration:
  description: "Extract detailed information from services"
  techniques:
    - "Banner grabbing (service versions)"
    - "Web application enumeration (directories, parameters)"
    - "API endpoint discovery (burp repeater)"
    - "Directory brute-force (common paths: /admin, /api, /config)"
    - "User enumeration (valid usernames)"
  tools:
    - "burp suite" (web enumeration)"
    - "gobuster/dirb" (directory brute-force)"
    - "ffuf" (parameter fuzzing)"
    - "feroxbuster" (recursive directory discovery)"
  output:
    - "Detailed technology inventory"
    - "API endpoints mapped"
    - "Potential entry points identified"

phase_4_exploitation:
  description: "Attempt to compromise systems"
  methodology:
    - "Test OWASP Top 10 vulnerabilities"
    - "Attempt authentication bypass"
    - "Test authorization flaws (privilege escalation)"
    - "Test input validation (SQL injection, XSS, command injection)"
    - "Test cryptography (weak algorithms, hardcoded keys)"
    - "Attempt social engineering (phishing simulation)"
  tools:
    - "burp suite" (active scanning)"
    - "sqlmap" (SQL injection)"
    - "metasploit" (exploit framework)"
    - "custom scripts" (for specific business logic)"
  controls:
    - "Do not exploit without understanding impact"
    - "Do not modify data"
    - "Stop immediately if system becomes unstable"
  output:
    - "Confirmed vulnerabilities with proof-of-concept"
    - "Attack path documentation"

phase_5_post_exploitation:
  description: "Document what access was gained (if authorized)"
  techniques:
    - "Determine access level achieved (read, write, admin)"
    - "Identify sensitive data accessible"
    - "Document system state changes"
    - "Assess lateral movement potential (without exploiting)"
  output:
    - "Access scope documented"
    - "Impact assessment for each finding"

phase_6_reporting:
  description: "Create comprehensive report"
  sections:
    - Executive summary (key findings, severity distribution)
    - Detailed findings (one per vulnerability)
    - Risk ratings (CVSS scores)"
    - Proof-of-concept (screenshots, logs)"
    - Remediation recommendations"
    - Remediation timeline"
  output:
    - "Professional penetration test report"
    - "Risk matrix (severity x likelihood)"
    - "Prioritized remediation plan"
```

---

## Vulnerability Assessment & Reporting

**ALWAYS**:
- Use CVSS 3.1 for severity scoring (v31-calculator.nist.gov)
- Rate business impact (not just technical severity)
- Provide clear remediation steps
- Include proof-of-concept (don't weaponize)
- Assign remediation owner (who fixes this?)
- Set remediation deadline
- Track remediation progress

**NEVER**:
- Downplay severity (be honest)
- Report without proof-of-concept
- Give generic recommendations ("update software")
- Omit remediation steps

### ✅ GOOD Vulnerability Finding

```markdown
## Finding #1: SQL Injection in User Search

**Severity**: CRITICAL (CVSS 9.8)
**Component**: /api/users/search endpoint
**Status**: Confirmed

### Description
The user search endpoint is vulnerable to SQL injection via the `username` parameter. An unauthenticated attacker can query the database directly, bypassing authorization controls.

### Proof of Concept
```
GET /api/users/search?username=admin' OR '1'='1
Response: All users in database returned
```

### Impact
- **Confidentiality**: HIGH — All user data (emails, passwords hashes, etc.) can be exfiltrated
- **Integrity**: HIGH — Database can be modified/deleted
- **Availability**: HIGH — Database can be locked/dropped

### Root Cause
```csharp
// VULNERABLE CODE
var query = $"SELECT * FROM Users WHERE Username = '{searchTerm}'";
var users = _db.Users.FromSqlRaw(query).ToList();
```

### Remediation (Immediate - 24 hours)
```csharp
// FIXED CODE
var users = _db.Users
    .Where(u => u.Username.Contains(searchTerm))
    .ToList();
// OR use parameterized query
var users = _db.Users.FromSqlInterpolated(
    $"SELECT * FROM Users WHERE Username = {searchTerm}"
).ToList();
```

### Remediation Steps
1. Replace all SQL string concatenation with parameterized queries
2. Use ORM methods (Entity Framework, Linq) whenever possible
3. Add input validation (whitelist allowed characters)
4. Add logging for authentication failures
5. Re-test after fix

### Verification
- [ ] Code reviewed by senior developer
- [ ] Unit tests pass
- [ ] SQL injection test passes (confirm fix works)
- [ ] Load testing confirms performance not degraded
- [ ] Signed off by product owner

### References
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1
```

---

## Continuous Vulnerability Scanning

**ALWAYS**:
- Automate vulnerability scanning (SAST, DAST)
- Scan on every commit (pre-commit, CI/CD)
- Scan dependencies (SCA - Software Composition Analysis)
- Scan containers/infrastructure (IaC scanning)
- Track scan history (identify trending vulnerabilities)
- Alert on critical/high findings (don't let them sit)

**NEVER**:
- Ignore scan results (automate fixes)
- Have zero scan coverage
- Scan without tooling

### ✅ GOOD Scanning Setup

```yaml
# GitHub Actions - Automated Vulnerability Scanning
name: Security Scanning

on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      # Static Application Security Testing
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      - name: Checkmarx SAST
        run: |
          checkmarx scan \
            --project-id $PROJECT_ID \
            --folder src/
  
  dast:
    runs-on: ubuntu-latest
    steps:
      # Dynamic Application Security Testing
      - uses: actions/checkout@v3
      - name: OWASP ZAP Scan
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'
  
  sca:
    runs-on: ubuntu-latest
    steps:
      # Software Composition Analysis (dependencies)
      - uses: actions/checkout@v3
      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'PowerPlay'
          path: '.'
          format: 'JSON'
          args: >
            --enableExperimental
      - name: Snyk Scan
        uses: snyk/actions/dotnet@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  infrastructure:
    runs-on: ubuntu-latest
    steps:
      # Infrastructure as Code scanning
      - uses: actions/checkout@v3
      - name: Terraform Security Scan
        run: |
          tfsec . \
            --format json \
            --out tfsec-results.json
      - name: Container Scanning
        run: |
          trivy image \
            --format json \
            --output trivy-results.json \
            my-registry/my-app:latest
```

---

## Remediation & Re-testing

**ALWAYS**:
- Assign remediation owners (not "team")
- Set firm deadlines (critical: 48h, high: 1 week)
- Require code review before marking fixed
- Re-test to confirm fix (automated + manual)
- Document remediation steps taken
- Track time-to-remediation metric

**NEVER**:
- Accept "we'll fix it later" without date
- Mark as fixed without verification
- Re-test with same tooling (use multiple tools)

### ✅ GOOD Remediation Tracking

```csharp
// Vulnerability Remediation Tracking
public class VulnerabilityRemediationTracker
{
    public async Task TrackRemediationAsync(
        Vulnerability vuln,
        string assignedTo,
        DateTime deadline,
        string remediationPlan)
    {
        // Log remediation task
        var task = new RemediationTask
        {
            VulnerabilityId = vuln.Id,
            Severity = vuln.Severity,
            AssignedTo = assignedTo,
            DueDate = deadline,
            Plan = remediationPlan,
            CreatedAt = DateTime.UtcNow,
            Status = RemediationStatus.Assigned
        };
        
        await _db.RemediationTasks.AddAsync(task);
        
        // Alert assignee
        await _notificationService.NotifyAsync(
            assignedTo,
            $"Security vulnerability assigned: {vuln.Title}\n" +
            $"Severity: {vuln.Severity}\n" +
            $"Due: {deadline:yyyy-MM-dd}\n" +
            $"Details: {vuln.Description}"
        );
        
        // Set calendar reminder
        await _calendarService.SetReminderAsync(
            assignedTo,
            deadline.AddDays(-1),  // Day before
            $"Remediation due tomorrow: {vuln.Title}"
        );
    }
    
    public async Task VerifyRemediationAsync(
        VulnerabilityRemediationTracker task)
    {
        // Re-test the vulnerability
        var isFixed = await _penetrationTester.VerifyFixAsync(task.VulnerabilityId);
        
        if (isFixed)
        {
            task.Status = RemediationStatus.Verified;
            task.ResolvedAt = DateTime.UtcNow;
            task.TimeToRemediation = task.ResolvedAt - task.CreatedAt;
            
            // Log success
            _logger.LogInformation(
                "Vulnerability {VulnId} remediated by {AssignedTo} in {Days} days",
                task.VulnerabilityId,
                task.AssignedTo,
                task.TimeToRemediation.TotalDays
            );
        }
        else
        {
            // Failed verification - escalate
            await _notificationService.NotifySecurityTeamAsync(
                $"Remediation verification failed: {task.VulnerabilityId}\n" +
                $"Assigned to: {task.AssignedTo}\n" +
                $"Deadline: {task.DueDate}"
            );
        }
    }
}
```

---

## Penetration Testing Checklist

- [ ] Scope documented & authorized (Rules of Engagement signed)
- [ ] Test windows scheduled (off-peak, with stakeholder approval)
- [ ] Communication channels established (escalation contacts)
- [ ] NIST phases followed (reconnaissance → scanning → enumeration → exploitation)
- [ ] OWASP Top 10 tested (Web, Mobile, API)
- [ ] CVSS scores assigned (all findings)
- [ ] Proof-of-concept documented (non-weaponized)
- [ ] Remediation steps provided (clear, actionable)
- [ ] Remediation owners assigned (with deadlines)
- [ ] Re-testing completed (confirm fixes work)
- [ ] Time-to-remediation tracked (metric)
- [ ] Post-test meeting held (findings discussion)

---

## Summary

Good penetration testing:
1. **Plan methodically** — Scope, authorization, rules of engagement
2. **Test systematically** — NIST phases, OWASP standards, multiple vectors
3. **Document thoroughly** — Every finding with proof-of-concept and remediation
4. **Rate carefully** — CVSS scores, business impact assessment
5. **Remediate responsibly** — Clear owners, firm deadlines, verification
6. **Automate continuously** — SAST, DAST, SCA, IaC scanning in CI/CD
7. **Track metrics** — Time-to-remediation, vulnerability trends

Penetration testing is not a checkbox—it's continuous security validation.
