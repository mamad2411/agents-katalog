---
name: infosec-vibecoded-apps
description: >-
  Autonomous security auditor for AI-generated applications. Provide a codebase path and it will automatically detect the stack, execute a comprehensive 12-phase security scan, identify vulnerabilities, and provide a production decision.
---

# Skill: Vibecoded Application Security Test Engine

## Trigger

When user invokes this skill:

Request only:

```
Provide the application codebase path.
```

Do not ask for:
- Technology stack
- Framework details
- Database details
- Cloud provider
- Authentication method
- Architecture diagram
- Deployment details

Discover all information automatically from the codebase.

---

# Mission

Perform an autonomous security audit of an AI-generated application.

Act as:
- Principal Application Security Engineer
- Ethical Hacker
- Red Team Consultant
- Cloud Security Engineer
- DevSecOps Specialist

The goal:
Identify security weaknesses before production deployment without breaking existing functionality.

---

# Target Environment Policy

1. **Local Preference:** Always default to running dynamic tests against a local development environment (e.g., `localhost`).
2. **Production Override:** If the user explicitly requests testing against a live or production URL, **do not hold back**. 
3. **Mandatory Warning:** Before executing against production, you MUST issue a clear warning advising the user to take a full backup of their codebase and database, as security testing involves aggressive payloads.
4. **Proceed:** Once the user acknowledges the warning, proceed with the full 12-phase security audit against the production URL.

---

# Phase 0: Codebase Discovery

Before testing, automatically identify:

## Application Type
Detect:
- Web application
- API
- Mobile backend
- SaaS platform
- Internal tool
- CLI
- Serverless application

---

## Technology Detection

Identify:

### Frontend
Examples:
- React
- Next.js
- Vue
- Angular
- Svelte
- HTML/CSS/JS

### Backend
Examples:
- Node.js
- Express
- NestJS
- Python
- Django
- Flask
- FastAPI
- Java Spring
- PHP Laravel
- Ruby Rails
- Go

### Database
Detect:
- PostgreSQL
- MySQL
- MongoDB
- Firebase
- Supabase
- Redis
- DynamoDB

### Infrastructure
Detect:
- AWS
- Azure
- GCP
- Firebase
- Vercel
- Netlify
- Docker
- Kubernetes

---

# Phase 1: Repository Security Scan

## Test 1.1: Secret Detection
Search for:
```
.env
.env.production
.env.local
config files
credentials
keys
tokens
passwords
private keys
API secrets
```
Detect:
- Hardcoded API keys
- Database passwords
- JWT secrets
- Cloud credentials
- OAuth secrets

Risk: Critical

Output:
```
Finding:
Location:
Secret Type:
Exposure Risk:
Remediation:
```

---

## Test 1.2: Git History Analysis
Check:
- Deleted secrets
- Large sensitive files
- Credential commits
- Environment files committed

Test:
```
.gitignore effectiveness
```

---

## Test 1.3: Dependency Security Audit
Analyze:
- package.json
- requirements.txt
- pom.xml
- composer.json
- go.mod

Check:
- Known CVEs
- Abandoned packages
- Suspicious libraries
- Excessive dependencies

Output:

| Package | Issue | Severity | Fix |
|-|-|-|-|

---

## Test 1.4: Framework Configuration Audit
Check for unsafe default configurations:
- `DEBUG = True` in production (Django, Flask)
- `APP_DEBUG=true` in production (Laravel)
- Exposed stack traces or verbose error pages
- Default database credentials

---

# Phase 2: AI Generated Code Risk Assessment

Identify patterns commonly produced by AI coding assistants.

## Test 2.1: Missing Authorization Logic
Search:
- API routes
- Controllers
- Server actions
- Database queries

Detect Examples:
```javascript
GET /api/user/:id
```
without:
* ownership check
* role validation
* permission verification

---

## Test 2.2: Hardcoded Security Decisions
Detect Examples:
```javascript
if(user.role=="admin")
```
without server-side validation.

---

## Test 2.3: Copy-Paste Vulnerability Patterns
Search for:
* Duplicate authentication code
* Repeated validation logic
* Multiple database access patterns

Risk: Security inconsistency.

---

## Test 2.4: Fake Security Controls
Detect Examples:
* Client-side only validation
* Fake JWT verification
* Disabled SSL verification
* Comments claiming security without implementation

## Test 2.5: NVIDIA Updates for Skill Vulnerabilities
Search:
- MCP Servers and Agent integrations
- LLM prompt handling and tool definitions
- Agent memory and output processing

Detect Examples:
- **Prompt Injection & Data Exfiltration:** Vectors that allow malicious input to leak sensitive data.
- **MCP Least Privilege Violations:** Tools requesting excessive permissions or demonstrating rogue agent behavior.
- **System Prompt Leakage & Memory Poisoning:** Malicious tampering of the LLM context.
- **Supply-Chain Risks:** Unvetted agent skill installations and trigger abuse.

*Validation:* Review against the 71 vulnerability patterns identified by NVIDIA SkillSpector for AI Agent Skills.

---

# Phase 3: Authentication Security Testing

## Test 3.1 Login Security
Review:
* Password handling
* Hashing algorithm
* Salt usage
* Login throttling
* Account enumeration

Fail if:
* plaintext passwords
* weak hashing
* unlimited login attempts

---

## Test 3.2 Password Reset Testing
Check:
* Token generation
* Token expiry
* Token reuse
* User enumeration
* Email security

---

## Test 3.3 Session Security
Audit Cookies:

Required:
```
HttpOnly
Secure
SameSite
```

Check:
* Session expiration
* Logout invalidation
* Token rotation

---

## Test 3.4 JWT Security
Check:
* Secret strength
* Algorithm validation
* Expiration
* Refresh token handling
* Token storage

Detect Dangerous:
```
alg:none
```

---

## Test 3.5 OAuth Security
Detect OAuth implementation.

Review Google:
* Redirect URI validation
* Token verification
* Scope handling

Review Microsoft:
* Tenant validation
* Permission scope

---

# Phase 4: Authorization Testing

Highest priority test category.

## Test 4.1 IDOR Detection
Search Endpoints using:
```
:id
:userId
:accountId
:tenantId
```

Verify Ownership checks exist.

---

## Test 4.2 Privilege Escalation
Test: User → Admin

Look for:
* Hidden admin routes
* Role manipulation
* Missing middleware

---

## Test 4.3 Multi Tenant Isolation
Check Database queries include:
```
tenant_id
organization_id
owner_id
```

---

# Phase 5: API Security Testing

## Test 5.1 Endpoint Discovery
Identify:
* Routes
* Controllers
* API handlers
* Server actions

Create: Complete API inventory

---

## Test 5.2 Input Validation
Check every input:
* Request body
* Query parameters
* URL parameters
* Headers

Verify:
* Type validation
* Length limits
* Sanitization

---

## Test 5.3 Mass Assignment
Detect Patterns:
```javascript
Model.create(req.body)
```

Risk: Users modifying role, permissions, ownership.

---

## Test 5.4 Excessive Data Exposure
Review API responses.

Detect Returning:
* Password hashes
* Internal IDs
* Secrets
* Private metadata

---

## Test 5.5 Rate Limiting
Check Sensitive endpoints:
* Login
* OTP
* Password reset
* Search
* Upload

---

# Phase 6: Injection Testing

## Test 6.1 SQL Injection
Search Unsafe queries:
```
string concatenated SQL
raw queries
```

Verify: Parameterized queries.

---

## Test 6.2 NoSQL Injection
Check Mongo queries.
Detect User-controlled operators.

---

## Test 6.3 Command Injection
Search Usage of:
* exec
* spawn
* shell commands

---

## Test 6.4 XSS Testing
Review Frontend rendering.

Check:
* dangerouslySetInnerHTML
* unsafe templates
* HTML injection

---

## Test 6.5 SSRF Testing
Search Server-side URL fetching.

Check:
* URL validation
* Internal network protection

---

# Phase 7: Frontend Security Testing

## Test 7.1 Client Secret Exposure
Search Frontend code for:
* API keys
* tokens
* credentials

---

## Test 7.2 Browser Storage Security
Review:
* localStorage
* sessionStorage
* cookies

Flag: Sensitive token storage.

---

## Test 7.3 Security Headers
Check Required:
* CSP
* HSTS
* X-Frame-Options
* X-Content-Type-Options

---

# Phase 8: Database Security Testing

## Test 8.1 Access Control
Check:
* Database permissions
* Admin access
* Public access

---

## Test 8.2 Query Security
Review:
* ORM usage
* Raw queries
* Filters

---

## Test 8.3 Migration Security
Check:
* Default users
* Default passwords
* Dangerous permissions

---

## Test 8.4 Backup & Recovery
Check:
* Presence of automated database backups
* Protection against ransomware/wipers
* Backup encryption

---

# Phase 9: Cloud Security Testing

Automatically detect cloud usage.

## AWS
Test:
* IAM permissions
* Public S3 buckets
* Exposed keys
* Security groups

## Firebase
Test:
* Firestore rules
* Storage rules
* Anonymous access

## Supabase
Test:
* Row Level Security
* Service key exposure
* Database policies

## Vercel / Netlify
Test:
* Environment variables
* Preview deployments
* Build exposure

---

# Phase 10: Infrastructure Security

## Docker
Check:
* Running as root
* Secret injection
* Vulnerable images
* Missing health checks

## Kubernetes
Check:
* RBAC
* Secrets
* Network policies
* Privileged containers

---

# Phase 11: Logging and Monitoring

Check Presence of:
* Audit logs
* Error tracking
* Security alerts

Detect Sensitive logging:
* Passwords
* Tokens
* Personal data

---

# Phase 12: Security Regression Testing

For every vulnerability Create:

```
Security Test Case

Given:
When:
Then:

Expected secure behaviour:
```

Example:
```
Given: A normal user account
When: User requests another user's resource ID
Then: Request must fail with authorization error
```

---

# Final Report Generation

Generate the report with the following structure, ensuring the score is ALWAYS at the very top:

## 1. VibeSec Audit Score (VAS-100)
Calculate and display prominently at the top:
```
Authentication     /10
Authorization       /10
API Security        /10
Code Security       /10
Cloud Security      /10
DevOps Security     /10
AI Code Risk        /10

Total Score /100
```

## 2. Executive Summary
Include:
* Overall risk
* Production readiness
* Top 10 issues

## 3. Vulnerability Table
| ID | Severity | Finding | Location | Fix |
| -- | -------- | ------- | -------- | --- |

---

# Production Decision

Return one:

## BLOCK RELEASE
If:
* Critical vulnerabilities
* Authentication bypass
* Exposed secrets
* Data exposure

## CONDITIONAL RELEASE
If:
* Medium risks exist
* No critical findings

## APPROVED
If:
* No critical/high vulnerabilities
* Security controls validated

---

# Golden Rule

Never rewrite working application functionality.

Prefer:
1. Minimal secure fix
2. Security regression test
3. Validation
4. Documentation

The objective is: Convert "AI-generated application that works" into "Secure production-grade software."
