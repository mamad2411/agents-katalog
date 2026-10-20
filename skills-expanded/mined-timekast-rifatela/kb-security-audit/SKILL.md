---
name: kb-security-audit
description: Offensive and adversarial security reference — threat modeling, OWASP Top 10:2025 (incl. A03 Supply Chain, A10 Exceptional Conditions), attack-surface mapping, EPSS-based CVE prioritization, dangerous-code-pattern analysis, secret detection, fail-open vs fail-closed handling, scanning methodology, finding structure, and MITRE ATT&CK red-team tactics. Stack-agnostic; pairs with the `security-auditor` agent. Invoke when auditing attack surface, threat-modeling a feature, prioritizing CVEs, or simulating adversary behavior.
last-verified: 2026-04-23
---

# Security Audit — Offensive & Adversarial Reference

> **Scope:** stack-agnostic security audit, threat modeling, OWASP principles, red team tactics.
> **Paired with:** `security-auditor` agent (this skill is its knowledge base).
> **Not this skill's job:** stack-specific auth wiring in THIS repo — that lives in `kb-security` (NextAuth v5, RBAC matrix, Zod, rate-limit, audit log).

---

## 1. Expert mindset

| Principle            | Application                             |
| -------------------- | --------------------------------------- |
| **Assume Breach**    | Design as if attacker is already inside |
| **Zero Trust**       | Never trust, always verify              |
| **Defense in Depth** | Multiple layers, no single point        |
| **Least Privilege**  | Minimum required access only            |
| **Fail Secure**      | On error, deny access                   |

### Threat-modeling questions (before any scan or review)

1. **What are we protecting?** — assets, data classes, business value
2. **Who would attack?** — threat actors, motivation, capability
3. **How would they attack?** — attack vectors, kill chain
4. **What's the impact?** — business risk, regulatory, reputational

---

## 2. OWASP Top 10:2025

| Rank    | Category                  | Think about                          |
| ------- | ------------------------- | ------------------------------------ |
| **A01** | Broken Access Control     | IDOR, SSRF (merged in 2025)          |
| **A02** | Security Misconfiguration | Defaults, headers, exposed services  |
| **A03** | Software Supply Chain 🆕  | Dependencies, CI/CD, build integrity |
| **A04** | Cryptographic Failures    | Weak crypto, exposed secrets         |
| **A05** | Injection                 | User input → system commands / SQL   |
| **A06** | Insecure Design           | Flawed architecture                  |
| **A07** | Authentication Failures   | Session, credential management       |
| **A08** | Integrity Failures        | Unsigned updates, tampered data      |
| **A09** | Logging & Alerting        | Blind spots, no monitoring           |
| **A10** | Exceptional Conditions 🆕 | Error handling, fail-open states     |

**2025 shifts from 2021:** SSRF merged into A01; A02 elevated (cloud/container configs); **A03 NEW** (supply chain as first-class); **A10 NEW** (exceptional conditions); focus shifted from symptoms to root causes.

---

## 3. Supply Chain Security (A03)

| Vector             | Risk               | Audit question               |
| ------------------ | ------------------ | ---------------------------- |
| **Dependencies**   | Malicious packages | Do we audit new deps?        |
| **Lock files**     | Integrity attacks  | Are they committed + diffed? |
| **Build pipeline** | CI/CD compromise   | Who can modify workflows?    |
| **Registry**       | Typosquatting      | Verified / private source?   |

**Defense principles:** verify package integrity (checksums), pin versions, audit updates, prefer private registries for critical deps, sign and verify artifacts.

---

## 4. Attack Surface Mapping

| Category             | Elements                    |
| -------------------- | --------------------------- |
| **Entry Points**     | APIs, forms, file uploads   |
| **Data Flows**       | Input → Process → Output    |
| **Trust Boundaries** | Where auth/authz is checked |
| **Assets**           | Secrets, PII, business data |

### Prioritization matrix

```
Risk = Likelihood × Impact

High Impact + High Likelihood → CRITICAL
High Impact + Low Likelihood  → HIGH
Low Impact + High Likelihood  → MEDIUM
Low Impact + Low Likelihood   → LOW
```

---

## 5. Risk prioritization — EPSS + CVSS + context

| Factor          | Weight             | Audit question           |
| --------------- | ------------------ | ------------------------ |
| **CVSS Score**  | Base severity      | How severe is the vuln?  |
| **EPSS Score**  | Exploit likelihood | Is it being exploited?   |
| **Asset Value** | Business context   | What's actually at risk? |
| **Exposure**    | Attack surface     | Internet-facing?         |

### Decision tree

```
Is it actively exploited (EPSS > 0.5)?
├── YES → CRITICAL: immediate action
└── NO  → check CVSS
         ├── CVSS ≥ 9.0  → HIGH
         ├── CVSS 7.0-8.9 → consider asset value
         └── CVSS < 7.0  → schedule for later
```

> **Rule:** don't sort CVEs alphabetically or by CVSS alone. EPSS + exposure decide what gets patched first.

---

## 6. Exceptional Conditions (A10)

| Scenario       | Fail-Open (BAD) | Fail-Closed (GOOD) |
| -------------- | --------------- | ------------------ |
| Auth error     | Allow access    | Deny access        |
| Parsing fails  | Accept input    | Reject input       |
| Timeout        | Retry forever   | Limit + abort      |
| Downstream 5xx | Return cached   | Explicit error     |

**What to audit:** catch-all exception handlers that silently ignore, missing error handling on security-critical ops, race conditions in auth/authz, resource exhaustion scenarios.

---

## 7. Scanning methodology (phase-based)

```
1. RECONNAISSANCE   understand the target
   ├── Technology stack
   ├── Entry points
   └── Data flows

2. DISCOVERY        identify potential issues
   ├── Configuration review
   ├── Dependency analysis
   └── Code pattern search

3. ANALYSIS         validate and prioritize
   ├── False-positive elimination
   ├── Risk scoring
   └── Attack-chain mapping

4. REPORTING        actionable findings
   ├── Clear reproduction steps
   ├── Business impact
   └── Remediation guidance
```

---

## 8. Dangerous code patterns

| Pattern                      | Risk      | Look for                          |
| ---------------------------- | --------- | --------------------------------- |
| **String concat in queries** | Injection | `"SELECT * FROM " + user_input`   |
| **Dynamic code execution**   | RCE       | `eval()`, `exec()`, `Function()`  |
| **Unsafe deserialization**   | RCE       | `pickle.loads()`, `unserialize()` |
| **Path manipulation**        | Traversal | User input in file paths          |
| **Disabled security**        | Various   | `verify=False`, `--insecure`      |

### Secret patterns (grep targets)

| Type        | Indicators                        |
| ----------- | --------------------------------- |
| API keys    | `api_key`, `apikey`, high entropy |
| Tokens      | `token`, `bearer`, `jwt`          |
| Credentials | `password`, `secret`, `key`       |
| Cloud       | `AWS_`, `AZURE_`, `GCP_` prefixes |

---

## 9. Cloud security — shared responsibility

| Layer          | You own | Provider owns |
| -------------- | ------- | ------------- |
| Data           | ✅      | ❌            |
| Application    | ✅      | ❌            |
| OS / Runtime   | Depends | Depends       |
| Infrastructure | ❌      | ✅            |

**Cloud-specific checks:** IAM least-privilege applied? Public storage buckets? Network security groups tightened? Secrets manager in use (not env vars committed)?

---

## 10. Reporting — finding structure

Each finding must answer:

1. **What?** — clear vulnerability description
2. **Where?** — exact location (file, line, endpoint)
3. **Why?** — root cause explanation
4. **Impact?** — business consequence
5. **How to fix?** — specific, actionable remediation

### Severity classification

| Severity     | Criteria                             |
| ------------ | ------------------------------------ |
| **Critical** | RCE, auth bypass, mass data exposure |
| **High**     | Data exposure, privilege escalation  |
| **Medium**   | Limited scope, requires conditions   |
| **Low**      | Informational, best practice         |

---

## 11. Red Team Tactics (MITRE ATT&CK)

> Adversary simulation — use to stress-test defenses, NOT to cause real harm.

### Attack lifecycle

```
RECONNAISSANCE → INITIAL ACCESS → EXECUTION → PERSISTENCE
       ↓              ↓              ↓            ↓
   PRIV ESC    → DEFENSE EVASION → CRED ACCESS → DISCOVERY
       ↓              ↓              ↓            ↓
LATERAL MOVEMENT → COLLECTION → C2 → EXFILTRATION → IMPACT
```

### Initial access vectors

| Vector                | When realistic              |
| --------------------- | --------------------------- |
| **Phishing**          | Human target, email access  |
| **Public exploits**   | Vulnerable services exposed |
| **Valid credentials** | Leaked or cracked           |
| **Supply chain**      | Third-party access          |

### Privilege escalation

| Windows                    | Linux                  |
| -------------------------- | ---------------------- |
| Unquoted service paths     | SUID binaries          |
| Weak service permissions   | Sudo misconfiguration  |
| Token privileges (SeDebug) | Kernel vulnerabilities |
| Stored credentials         | Writable cron scripts  |

### Defense evasion

| Technique    | Purpose                 |
| ------------ | ----------------------- |
| LOLBins      | Use legitimate tools    |
| Obfuscation  | Hide malicious code     |
| Timestomping | Hide file modifications |
| Log clearing | Remove evidence         |

### Active Directory attacks

| Attack          | Target                    |
| --------------- | ------------------------- |
| Kerberoasting   | Service account passwords |
| AS-REP Roasting | Accounts without pre-auth |
| DCSync          | Domain credentials        |
| Golden Ticket   | Persistent domain access  |

### Ethical boundaries (non-negotiable)

**Always:** stay within scope, minimize impact, report threats immediately, document all actions.
**Never:** destroy production data, cause denial of service, access beyond proof of concept, retain sensitive data.

---

## 12. Anti-patterns

| ❌ Don't                       | ✅ Do                             |
| ------------------------------ | --------------------------------- |
| Scan without understanding     | Map attack surface first          |
| Alert on every CVE             | Prioritize by EPSS + asset value  |
| Ignore false positives         | Maintain verified baseline        |
| Fix symptoms only              | Address root causes               |
| Scan once before deploy        | Continuous scanning               |
| Trust third-party deps blindly | Verify integrity, audit code      |
| Sort vulns alphabetically      | Active-exploit-first (EPSS > 0.5) |
| Red team to break things       | Red team to improve defenses      |

---

> **Remember:** vulnerability scanning finds issues. Expert thinking prioritizes what matters. Always ask: _"What would an attacker do with this?"_

---

_Cross-reference: `kb-security` for stack-specific (NextAuth v5 + RBAC + Zod + rate-limit + audit log) in this Next.js repo. The `security-auditor` agent loads this skill when invoked for offensive review, threat modeling, or supply chain audit._
