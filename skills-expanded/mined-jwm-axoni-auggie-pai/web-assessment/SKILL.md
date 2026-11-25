---
name: web-assessment
description: Systematic web application security testing following OWASP methodology. USE WHEN web assessment, pentest, security assessment, security test, OWASP testing, vulnerability scan, test for vulnerabilities, test web app, application security, fuzz, test authentication.
---

# Web Application Security Assessment

Skill for systematic web application security testing following OWASP methodology.
Coordinates with Recon (for target discovery) and Prompt Injection (for LLM-specific attacks).

## When to Use This Skill

Activate when the user requests:
- "web assessment", "pentest", "security assessment", "security test"
- "OWASP testing", "vulnerability scan", "test for vulnerabilities"
- "test web app", "application security", "app sec"
- "fuzz", "content discovery", "directory brute force"
- "test authentication", "test authorization", "test for injection"
- Any request involving web application vulnerability testing

## Authorization and Ethical Requirements

**CRITICAL -- Read before any action.**

### Mandatory Rules

1. **Authorization first** -- never test without explicit written permission
2. **Scope validation** -- confirm target URLs/domains are in-scope before any testing
3. **No destructive testing** -- avoid actions that could cause data loss or service disruption
4. **Rate limiting** -- space requests to avoid overloading targets
5. **Document everything** -- log all tests, payloads, and findings with timestamps
6. **Responsible disclosure** -- follow coordinated disclosure for any vulnerabilities found

### Before Starting Any Assessment

Ask and confirm:
- Do you have written authorization to test this application?
- What is the exact scope (URLs, endpoints, functionality)?
- Are there any excluded areas or actions (e.g., production databases, destructive writes)?
- What is the testing window (dates/times)?
- Who is the point of contact if issues arise?

**If authorization is unclear, STOP and ask for clarification.**

## Systematic Testing Process

Follow this 6-phase methodology:

### Phase 0: Scoping and Preparation
- Define target application and scope boundaries
- Confirm authorization documentation
- Identify testing constraints (rate limits, excluded functionality)
- Set up testing notes and reporting structure

### Phase 1: Reconnaissance
- Use the Recon skill for infrastructure discovery
- Identify subdomains, endpoints, technology stack
- Map the application: pages, forms, APIs, authentication flows
- Use claude-browser MCP to walk through the application interactively

### Phase 2: Application Mapping
- Enumerate all entry points: forms, URL parameters, headers, cookies
- Identify user roles and access levels
- Map user flows and sensitive data handling
- Document the technology stack (server, framework, CDN, third-party services)
- Identify API endpoints and their methods (GET, POST, PUT, DELETE)

### Phase 3: Vulnerability Testing
- Test against each OWASP Top 10 category (see below)
- Prioritize based on threat model and attack surface
- Use systematic test cases per category
- Record all test inputs and responses

### Phase 4: Exploitation and Validation
- Validate findings with proof-of-concept demonstrations
- Confirm severity with reproducible steps
- Assess real-world impact of each vulnerability
- Avoid accessing data beyond what is needed for proof

### Phase 5: Reporting
- Compile findings into structured vulnerability report
- Include severity, description, proof, and remediation for each finding
- Provide executive summary and technical details

## OWASP Top 10 Testing Areas

### A01: Broken Access Control
- Test horizontal privilege escalation (access other users' data)
- Test vertical privilege escalation (access admin functions)
- Test forced browsing to unlinked pages
- Verify CORS configuration
- Test IDOR (Insecure Direct Object Reference) on all endpoints

### A02: Cryptographic Failures
- Check TLS configuration: `curl -vI https://target.com 2>&1`
- Look for sensitive data in URLs, logs, or error messages
- Verify password storage (no plaintext, proper hashing)
- Check for weak or missing encryption on sensitive data in transit

### A03: Injection
- SQL injection on all input fields and parameters
- Cross-Site Scripting (XSS): reflected, stored, DOM-based
- Command injection where system commands may be constructed
- LDAP, XML, template injection where applicable
- Server-Side Request Forgery (SSRF)

### A04: Insecure Design
- Business logic flaws (price manipulation, workflow bypass)
- Race conditions in critical operations
- Missing rate limiting on sensitive endpoints
- Insufficient anti-automation

### A05: Security Misconfiguration
- Default credentials on admin interfaces
- Unnecessary HTTP methods enabled
- Directory listing enabled
- Verbose error messages exposing stack traces
- Missing security headers (CSP, X-Frame-Options, HSTS)

### A06: Vulnerable and Outdated Components
- Identify component versions from response headers and content
- Use WebSearch to check for known CVEs
- Check JavaScript libraries for known vulnerabilities

### A07: Identification and Authentication Failures
- Brute force protection on login
- Password policy strength
- Session management (token entropy, expiration, fixation)
- Multi-factor authentication bypass
- Password reset flow vulnerabilities

### A08: Software and Data Integrity Failures
- Check for unsigned/unverified updates or data
- Insecure deserialization
- CI/CD pipeline integrity (if in scope)
- Mass assignment vulnerabilities

### A09: Security Logging and Monitoring Failures
- Verify logging of authentication events
- Check for log injection possibilities
- Assess monitoring/alerting coverage

### A10: Server-Side Request Forgery (SSRF)
- Test URL parameters that fetch external resources
- Internal network scanning via SSRF
- Cloud metadata endpoint access (169.254.169.254)

## Available Tools

### claude-browser MCP
- Interactive browser-based testing through your company's service URLs
- Walk through authentication flows, form submissions, UI testing
- Capture screenshots and DOM state
- Test client-side behavior and JavaScript execution

### WebFetch and curl
- API endpoint testing: `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.target.com/endpoint`
- Header inspection: `curl -sI https://target.com`
- Authentication testing: `curl -b "session=token" https://target.com/admin`
- File upload testing, parameter manipulation, method testing

### WebSearch
- Research known vulnerabilities for identified technologies
- Find CVE details and exploitation guidance
- Look up security advisories for detected software versions

### System Commands
- `curl` -- HTTP requests with full control over headers, methods, body
- `dig`/`nslookup` -- DNS verification
- `openssl s_client` -- TLS/SSL analysis
- `base64`, `xxd` -- Encoding/decoding for payload crafting

## Integration with Other Skills

### Recon --> Web Assessment Pipeline
```
Recon discovers: api.example.com, admin.example.com, app.example.com
  --> Web Assessment tests each application for vulnerabilities
```

### Web Assessment --> Prompt Injection
```
Web Assessment finds LLM-powered chatbot on target
  --> Hand off to Prompt Injection skill for LLM-specific testing
```

## Output Format

Structure all vulnerability reports as follows:

```markdown
# Web Application Security Assessment: [Target]

## Executive Summary
- Target: [URL/application name]
- Scope: [tested URLs and functionality]
- Testing period: [dates]
- Authorization: [reference to authorization document]
- Findings: [X Critical, Y High, Z Medium, W Low, V Info]

## Findings

### [SEVERITY] [VULN-ID]: [Vulnerability Title]

**Severity:** Critical / High / Medium / Low / Info
**OWASP Category:** A01-A10
**CWE:** CWE-XXX
**Location:** [URL, endpoint, parameter]

**Description:**
[What the vulnerability is and why it matters]

**Proof of Concept:**
[Step-by-step reproduction]
1. Navigate to [URL]
2. Submit [payload] in [parameter]
3. Observe [result]

**Request:**
[HTTP request that demonstrates the vulnerability]

**Response:**
[Relevant portion of the HTTP response]

**Impact:**
[What an attacker could achieve by exploiting this]

**Remediation:**
[Specific steps to fix the vulnerability]
- [Primary fix]
- [Defense-in-depth recommendation]

---

## Methodology
[Brief description of testing approach and tools used]

## Scope and Limitations
[What was tested, what was excluded, any constraints encountered]
```

### Severity Definitions

| Severity | Definition |
|---|---|
| Critical | Direct data breach, RCE, full system compromise, authentication bypass |
| High | Significant data exposure, privilege escalation, stored XSS |
| Medium | Limited data exposure, reflected XSS, CSRF, information disclosure |
| Low | Minor information leaks, missing best-practice headers, verbose errors |
| Info | Observations, recommendations, defense-in-depth suggestions |

## Company Context

When assessing your company's applications:
- Use claude-browser MCP for authenticated testing through SSO if configured
- Reference internal security standards via your documentation portal
- Check ticketing system for related security tickets and known issues
- Consider the multi-tenant SaaS threat model
- Pay special attention to API authorization for API-heavy platforms
- Check monitoring tools for relevant security logging

## Examples

### Example 1: Full Assessment
```
User: "Security assessment on app.example.com"
--> Confirm authorization
--> Phase 0: Define scope (app.example.com/*)
--> Phase 1: Recon (technology stack, subdomains)
--> Phase 2: Map application (endpoints, roles, flows)
--> Phase 3: Test OWASP Top 10 categories
--> Phase 4: Validate and document findings
--> Phase 5: Generate vulnerability report
```

### Example 2: Targeted Testing
```
User: "Test the login page at auth.example.com for vulnerabilities"
--> Confirm authorization and scope (auth.example.com/login only)
--> Focus on A07 (Authentication), A01 (Access Control), A03 (Injection)
--> Test brute force protection, session handling, credential security
--> Generate focused report
```

### Example 3: API Security
```
User: "Test the REST API at api.example.com"
--> Confirm authorization
--> Map all API endpoints (WebFetch + curl)
--> Test authentication, authorization, input validation
--> Check for IDOR, mass assignment, rate limiting
--> Generate API security report
```

## Key Principles

1. **Understand before testing** -- build an application narrative first
2. **Threat model guides testing** -- do not test blindly; prioritize by risk
3. **Breadth then depth** -- wide reconnaissance, then focused exploitation
4. **Document everything** -- every test, every payload, every response
5. **Minimize impact** -- avoid disruption to production systems

---

**Remember:** Authorization is mandatory. Understand the application before attacking it.
Test systematically, document thoroughly, and report responsibly.
