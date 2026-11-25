---
name: threat-modeling
description: Design threat models using STRIDE, attack trees, and data flow diagrams. Outputs threat analysis, risk ratings, and mitigation strategies.
argument-hint: [system architecture, asset criticality, threat actors]
allowed-tools: Read, Write, Bash
---

# Threat Modeling

Design systematic threat analysis for applications and systems. Not ad-hoc security — STRIDE methodology, attack trees, data flow diagrams, and prioritized mitigations.

## Process

1. **Define scope.** System boundaries, assets, trust boundaries.
2. **Create DFD.** Data flow diagram showing components, data flows, trust zones.
3. **Apply STRIDE.** Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation.
4. **Build attack trees.** Attack paths from threat actor to asset.
5. **Rate risks.** DREAD scoring (Damage, Reproducibility, Exploitability, Affected, Discoverability).
6. **Prioritize mitigations.** High-risk threats first, defense-in-depth.
7. **Document findings.** Threat register, mitigations, residual risk.

## Output Format

### Threat Model: [Application Name]

**Methodology:** STRIDE  
**Scope:** Web API + Database + Authentication  
**Threats Identified:** 23 (8 high, 10 medium, 5 low)  
**Trust Boundaries:** 3 (Internet, DMZ, Internal)  
**Mitigations:** 15 controls recommended

---

## STRIDE Methodology

| Category | Definition | Example Threat |
|----------|-----------|----------------|
| **S**poofing | Impersonating user/system | Stolen credentials, session hijacking |
| **T**ampering | Modifying data/code | SQL injection, man-in-the-middle |
| **R**epudiation | Denying actions | No audit logs, unsigned transactions |
| **I**nfo Disclosure | Exposing data | API leaks PII, unencrypted data |
| **D**enial of Service | Resource exhaustion | DDoS, algorithmic complexity attacks |
| **E**levation | Gaining privileges | Privilege escalation, broken access control |

---

## Data Flow Diagram (DFD)

```
┌─────────────┐
│   Browser   │ (Untrusted)
└──────┬──────┘
       │ HTTPS
       │ Trust Boundary 1
       ▼
┌─────────────┐
│ Web Server  │ (DMZ)
│   nginx     │
└──────┬──────┘
       │ HTTP
       │ Trust Boundary 2
       ▼
┌─────────────┐
│  API Server │ (Internal)
│   Node.js   │
└──────┬──────┘
       │ SQL
       ▼
┌─────────────┐
│  Database   │ (Internal)
│  PostgreSQL │
└─────────────┘

Legend:
→ Data flow
━ Trust boundary (attack surface)
□ Process
```

### DFD Elements

**External Entities:** Users, browsers, third-party APIs  
**Processes:** Web server, API server, auth service  
**Data Stores:** Database, cache, file storage  
**Data Flows:** HTTP requests, SQL queries, API calls  
**Trust Boundaries:** Where data crosses security zones

---

## STRIDE Analysis Example

### Component: User Login API

#### Spoofing Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| Credential stuffing | Attacker uses leaked passwords | Rate limiting, CAPTCHA, breach detection |
| Session hijacking | Stolen session token | HTTPOnly cookies, SameSite, short expiry |
| JWT forgery | Weak secret or algorithm | Strong secret (32+ bytes), RS256 algorithm |

#### Tampering Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| SQL injection | Malicious SQL in username field | Parameterized queries, input validation |
| Response manipulation | MITM modifies login response | HTTPS/TLS, certificate pinning |
| Password hash tampering | Direct DB access changes hash | DB access controls, audit logging |

#### Repudiation Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| Login denial | User denies login attempt | Audit logs with IP, timestamp, device |
| Account action denial | User denies password change | Email confirmation, action logs |

#### Information Disclosure Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| Username enumeration | Different errors for valid/invalid users | Generic error: "Invalid credentials" |
| Timing attacks | Response time reveals user existence | Constant-time password comparison |
| Token in URL | JWT leaked in logs/browser history | Use POST body, not query params |

#### Denial of Service Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| Brute force | Millions of login attempts | Rate limiting (5 attempts/min), account lockout |
| Password hash DoS | Expensive bcrypt rounds | Limit input length, async processing |
| Database exhaustion | Too many concurrent sessions | Connection pooling, query timeouts |

#### Elevation of Privilege Threats
| Threat | Description | Mitigation |
|--------|-------------|------------|
| Privilege escalation | Regular user gets admin JWT | Role-based claims in token, verify on every request |
| Insecure direct object refs | /admin endpoint not protected | Authorization middleware, principle of least privilege |

---

## Attack Tree Example

### Goal: Access User PII

```
                    Access User PII
                         |
        ┌────────────────┼────────────────┐
        │                │                │
   SQL Injection    Steal Admin      Brute Force
   on /search       Credentials      API Endpoints
        │                │                │
    ┌───┴───┐       ┌────┴────┐      ┌───┴───┐
    │       │       │         │      │       │
 No input  OR   Phishing  Weak   Find    Try all
 validation  clause   admin   password unauthed  IDs
                                       endpoints
```

**Attack Path Analysis:**
1. **SQL Injection on /search**
   - Likelihood: High (if no validation)
   - Impact: Critical (full DB access)
   - Mitigation: Input validation, parameterized queries

2. **Steal Admin Credentials**
   - Likelihood: Medium (requires social engineering)
   - Impact: Critical (admin access)
   - Mitigation: MFA, security awareness training

3. **Brute Force API Endpoints**
   - Likelihood: Low (rate limiting exists)
   - Impact: Medium (limited data exposure)
   - Mitigation: Rate limiting, authentication required

---

## Risk Rating (DREAD)

**Scale:** 1-10 (Low-High)

| Threat | D | R | E | A | D | Total | Priority |
|--------|---|---|---|---|---|-------|----------|
| SQL injection on search | 10 | 10 | 7 | 10 | 8 | 45 | **Critical** |
| JWT secret hardcoded | 9 | 9 | 8 | 10 | 6 | 42 | **Critical** |
| No rate limiting | 6 | 8 | 9 | 8 | 9 | 40 | **High** |
| Username enumeration | 3 | 10 | 10 | 7 | 10 | 40 | **High** |
| Missing audit logs | 5 | 10 | 5 | 10 | 3 | 33 | **Medium** |
| HTTPS not enforced | 8 | 7 | 4 | 5 | 7 | 31 | **Medium** |

**D**amage: How bad if exploited?  
**R**eproducibility: How easy to repeat?  
**E**xploitability: How much effort to exploit?  
**A**ffected users: How many impacted?  
**D**iscoverability: How easy to find?

---

## Threat Register

```markdown
## Threat: SQL Injection on User Search

**ID:** THR-001  
**Category:** Tampering  
**Severity:** Critical  
**DREAD Score:** 45/50

**Description:**  
The `/api/users/search` endpoint concatenates user input directly into SQL query, allowing arbitrary SQL execution.

**Attack Scenario:**  
Attacker submits: `'; DROP TABLE users; --` as search term, deleting entire users table.

**Affected Components:**  
- User search API endpoint
- PostgreSQL database
- All user data

**Current Controls:** None

**Recommended Mitigations:**
1. Use parameterized queries (Priority: P0)
2. Input validation with allowlist (Priority: P0)
3. Database user with minimal permissions (Priority: P1)
4. Web Application Firewall (Priority: P2)

**Residual Risk:** Low (after mitigations)

**Status:** Open  
**Owner:** Backend Team  
**Due Date:** 2024-02-01
```

---

## Mitigation Strategies

### Defense in Depth Layers

```
Layer 1: Prevention
├─ Input validation
├─ Parameterized queries
├─ HTTPS/TLS
└─ Strong authentication

Layer 2: Detection
├─ Security logs
├─ Anomaly detection
├─ SIEM alerts
└─ Rate limit monitoring

Layer 3: Response
├─ Incident response plan
├─ Automated blocks
├─ Backup/recovery
└─ Forensics
```

### Control Types

**Preventive:** Stop attack before it happens
- Input validation, firewalls, encryption, MFA

**Detective:** Identify attack in progress
- Logging, IDS/IPS, anomaly detection, SIEM

**Corrective:** Respond to attack
- Incident response, patching, account lockout

**Deterrent:** Discourage attackers
- Legal warnings, honeypots, security monitoring notices

---

## Common Threats & Mitigations

### Authentication
| Threat | Mitigation |
|--------|------------|
| Credential stuffing | Rate limiting, breach detection, MFA |
| Session fixation | Regenerate session ID after login |
| Weak passwords | Password policy, strength meter, breach checking |

### Authorization
| Threat | Mitigation |
|--------|------------|
| Broken access control | Deny by default, verify on every request |
| IDOR | Use UUIDs, check ownership before access |
| Path traversal | Validate file paths, allowlist directories |

### Data Protection
| Threat | Mitigation |
|--------|------------|
| Data in transit | TLS 1.3, HSTS, certificate pinning |
| Data at rest | Encryption (AES-256), key management (KMS) |
| Sensitive data exposure | Minimize collection, mask PII, tokenization |

### API Security
| Threat | Mitigation |
|--------|------------|
| Injection attacks | Parameterized queries, input validation |
| Mass assignment | Explicit field allowlist, DTOs |
| Excessive data exposure | Minimal response, field filtering |

---

## Threat Modeling Tools

### Microsoft Threat Modeling Tool
- Visual DFD builder
- Automated STRIDE analysis
- Threat library
- Report generation

### OWASP Threat Dragon
- Open-source, web-based
- DFD diagrams
- STRIDE analysis
- GitHub integration

### Manual Process
```python
# Python threat model generator
threats = []

def analyze_component(component, data_flows):
    for flow in data_flows:
        # Spoofing
        if flow.requires_authentication:
            threats.append({
                'type': 'Spoofing',
                'component': component.name,
                'description': f'{flow.source} could impersonate user',
                'mitigation': 'Implement authentication'
            })
        
        # Tampering
        if not flow.encrypted:
            threats.append({
                'type': 'Tampering',
                'component': component.name,
                'description': f'Data in {flow.name} could be modified',
                'mitigation': 'Use TLS/encryption'
            })
        
        # ... continue for all STRIDE categories
    
    return threats
```

---

## Threat Modeling in SDLC

### Design Phase
- Initial threat model
- Architecture review
- Security requirements

### Development Phase
- Code review for identified threats
- Security testing (SAST)
- Mitigation implementation

### Testing Phase
- Penetration testing
- Validate mitigations
- Dynamic testing (DAST)

### Deployment Phase
- Security configuration
- Monitoring setup
- Incident response plan

### Maintenance Phase
- Update threat model for changes
- Review new threats (CVEs)
- Audit logs for attacks

---

## Continuous Threat Modeling

```yaml
# .github/workflows/threat-model.yml
name: Threat Model Review

on:
  pull_request:
    paths:
      - 'architecture/**'
      - 'threat-model.json'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check Threat Model Updated
        run: |
          if git diff --name-only origin/main | grep -q "architecture/"; then
            if ! git diff --name-only origin/main | grep -q "threat-model.json"; then
              echo "Architecture changed but threat model not updated"
              exit 1
            fi
          fi
      
      - name: Validate Threat Model
        run: |
          python scripts/validate_threat_model.py threat-model.json
```

## Rules

- Threat modeling required before design finalization — identify threats early when fixes are cheap.
- Update threat model when architecture changes — new features = new attack surface.
- Trust boundaries are attack surfaces — every boundary crossing needs security controls.
- STRIDE analysis on all components that handle sensitive data — systematic coverage prevents gaps.
- Risk scoring prioritizes mitigation work — fix critical threats first.
- Defense in depth, not single controls — layered security survives control failures.
- Assume breach mentality — design for when, not if, perimeter is breached.
- Document threats even if accepted — track risk acceptance decisions.
- Involve security team early — domain expertise catches threats developers miss.
- Threat model is living document — review quarterly or after major changes.
