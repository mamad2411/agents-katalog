---
name: purple-team-analyzer
description: "Purple Team analysis combining red team (attack) and blue team (defense) perspectives. Use when running attack simulation with integrated defense validation."
---

# Purple Team Analyzer

## Overview

This skill performs purple team analysis by integrating traditionally separated red team (attack) and blue team (defense) workflows. For every vulnerability identified in the codebase, this skill maps out the attack path and then verifies if existing security controls can detect, block, or respond to the attack. The goal is to audit both vulnerability exposure and defense effectiveness to provide a realistic assessment of the system's security posture.

**Core principle:** Attack without defense is meaningless. Defense without attack is untested. They must be evaluated together.

## The Iron Law

```
NO ANALYSIS IS COMPLETE WITHOUT PERFORMING A DEFENSE VALIDATION FOR EVERY ATTACK PATH IDENTIFIED.
MAPPING AN ATTACK WITHOUT VERIFYING THE CORRESPONDING DEFENSE IS AN INCOMPLETE AUDIT.
```

## When to Use

**Use this when:**
- You discover a vulnerability and need to answer, "Is this actually exploitable in our environment?"
- You need to test the effectiveness of active security controls (WAF, IDS/IPS, logging).
- You are conducting a post-incident review to understand why an attack went undetected.
- You want to verify if a newly deployed detection rule works as expected.
- You are preparing tabletop exercises or security awareness training.

**Use this ESPECIALLY when:**
- The team assumes "we are already safe" without empirical evidence.
- A vulnerability is classified as "low risk" but acts as a critical link in an attack chain.
- You need to validate security posture before a new feature or product release.
- A detection rule has a high false positive rate, leaving its actual validity uncertain.

**Don't skip when:**
- You only want to run a static vulnerability scan (use `mitre-attack-mapper` instead).
- Security controls are not yet set up — establish basic controls first, then run purple team analysis.
- Under time constraints — this is exactly when validating defenses is most critical.

## Phase 1: Red Team — Define Attack Paths

**BEFORE proceeding:**

Compile a list of all identified vulnerabilities (SAST/DAST/SCA reports, manual findings).

1. **Map the attack path for each vulnerability:**
   - Entry Point: Which API, endpoint, or code path?
   - Exploit Steps: Step-by-step actions an attacker would take.
   - Target: The resource or data the attacker intends to compromise.
   - OWASP category and MITRE ATT&CK ID.
2. **Evaluate exploit feasibility:**
   - Required privilege level (unauthenticated, user, admin).
   - External conditions required (specific configurations, timing, etc.).
   - Attack complexity (low/medium/high).
3. **Document the attack path:**
   - Target code or configuration file.
   - Exploit payload or Proof of Concept (PoC) — ensure it is a safe/non-destructive version.
   - Expected outcome (data exfiltration, privilege escalation, RCE, etc.).

```python
# Example attack path: SQL Injection to Data Exfiltration
attack_path = {
    "name": "SQL Injection to Exfiltrate User Database",
    "entry_point": "POST /api/users/search",
    "vulnerability": "Non-parameterized SQL query (app/routes/users.py:45)",
    "technique_id": "T1190.001 (Exploit Public-Facing Application: SQL Injection)",
    "attack_steps": [
        "1. Send HTTP POST request to /api/users/search using Burp Suite or curl",
        "2. Inject payload into 'name' parameter: ' OR 1=1 --",
        "3. SQL query executed on server: SELECT * FROM users WHERE name = '' OR 1=1 --'",
        "4. Server returns all user records -> Data exfiltration occurs"
    ],
    "required_access": "unauthenticated",
    "complexity": "low",
    "expected_result": "Extraction of all user records",
    "owasp_category": "A03:2021 — Injection"
}
```

## Phase 2: Blue Team — Analyze Defense Controls

**BEFORE proceeding:**

Inventory all active security controls (WAF, IDS/IPS, logging, input validation, monitoring) relevant to the attack paths defined in Phase 1.

1. **Build a defense control matrix for each attack path:**
   - Preventive Controls: Input validation, WAF rules, CSP headers, rate limiting.
   - Detective Controls: Log sources, SIEM rules, anomaly detection metrics.
   - Responsive Controls: Incident response plans, alerts, runbooks.
2. **Test each control:**
   - **Prevention:** Does it block the attack? How? Can it be bypassed?
   - **Detection:** Does it log the attack? Does it trigger SIEM alerts?
   - **Response:** Is there an automated or manual runbook triggered upon detection?
3. **Identify security gaps:**
   - Undetected: Logs exist, but no alert or SIEM rule triggers on them.
   - Unblocked: Missing input validation and active WAF rules.
   - Unobserved: No logs are generated at all.

```yaml
# Example Defense Control Matrix
defense_matrix:
  attack: "SQL Injection - POST /api/users/search"
  preventive_controls:
    - name: "WAF Rule"
      status: "ACTIVE"
      detail: "ModSecurity CRS rule 942100 (SQL Injection) is active"
      bypass_test: "FAILED"  # WAF bypass attempt failed = secure
    - name: "Input Validation"
      status: "PARTIAL"
      detail: "Flask input validation exists but lacks regex sanitization on 'name' field"
      bypass_test: "PASSED"   # Validation bypass succeeded = vulnerability exists
  detective_controls:
    - name: "SQL Error Logging"
      status: "ACTIVE"
      detail: "SQL errors are logged to app.log"
      alert: "NONE"              # Logs exist but trigger no alerts = detection gap
    - name: "SIEM Rule"
      status: "MISSING"
      detail: "No Splunk alert rule exists for SQL injection patterns"
  responsive_controls:
    - name: "IR Runbook"
      status: "MISSING"
      detail: "No dedicated incident runbook for SQL injection events"
```

## Phase 3: Purple Team — Align Attack and Defense

**BEFORE proceeding:**

Ensure Phase 1 (Attack Paths) and Phase 2 (Defense Controls) are completed.

1. **Perform attack-defense reconciliation:**
   - Map each attack path to its corresponding controls in the defense matrix.
   - Detection Gap: Attack succeeds, but no detection rule triggers.
   - Prevention Gap: Attack succeeds, and no preventive control blocks it.
   - Full Gap: Neither prevention nor detection controls exist.
   - Partial Gap: Preventive controls block it, but no logs or alerts are generated (or vice-versa).
2. **Develop remediation recommendations:**
   - Define concrete code or configuration changes for each gap.
   - Prioritization: Low attack complexity + High impact = Highest priority.
3. **Generate the Purple Team Report:**
   - Summary: Total attacks simulated, count of blocked attacks, count of detected attacks.
   - Breakdown: Detailed attack-defense mapping for each path.
   - Heatmap: Detection and prevention coverage matrix.
   - Remediation Roadmap: Prioritized actions.

```
===========================================================
PURPLE TEAM ANALYSIS REPORT
===========================================================
SUMMARY:
  Total Attack Paths Simulated: 12
  Fully Defended (Blocked & Detected):  3 (25%)  ✅
  Partially Defended (Only one active):  5 (42%)  ⚠️
  Undefended (Neither active):           4 (33%)  ❌

DETECTION RATE:  58% (7/12 attacks detected)
PREVENTION RATE: 33% (4/12 attacks blocked)

CRITICAL GAPS:
┌────────────────────────────────┬──────────┬──────────┬──────────┐
│ Attack Path                    │ Blocked  │ Detected │ Priority │
├────────────────────────────────┼──────────┼──────────┼──────────┤
│ SQL Injection → Exfiltration   │ PARTIAL  │ NO       │ CRITICAL │
│ Path Traversal → Config Leak   │ NO       │ NO       │ CRITICAL │
│ IDOR → User Data Leak          │ NO       │ YES      │ HIGH     │
│ XSS → Session Hijacking        │ YES      │ YES      │ LOW      │
└────────────────────────────────┴──────────┴──────────┴──────────┘

REMEDIATION ROADMAP:
  1. Deploy Splunk alert rule for SQL injection errors (Priority: CRITICAL)
  2. Implement strict input validation logic for path traversal patterns (Priority: CRITICAL)
  3. Integrate authorization validation checks to resolve IDOR vulnerabilities (Priority: HIGH)
  4. Perform follow-up WAF bypass validation tests (Priority: MEDIUM)
```

## Phase 4: Final Verification

Before marking complete:

- [ ] Is at least one attack path mapped for every identified vulnerability?
- [ ] Are prevention, detection, and response controls evaluated for each attack path?
- [ ] Have bypass tests (at least theoretical analyses) been performed for each control?
- [ ] Is the attack-defense reconciliation complete, highlighting all gaps?
- [ ] Does the report contain concrete remediation steps for every gap?
- [ ] Are remediations prioritized based on attack complexity and potential impact?
- [ ] Are simulated attack procedures documented safely, ensuring they cannot be abused in production?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Let's just locate the vulnerabilities; we can review controls later" — **This is a red team audit, not purple team. You must evaluate defenses.**
- "The attack path is too complex, let's only verify if we log it" — **Both prevention and detection are required; logging alone is not enough.**
- "We have a WAF, so SQL injection is blocked automatically" — **Did you test WAF bypasses? Never rely on assumptions.**
- "This attack is simple; we don't need to document it" — **Simple attacks are the most dangerous because they are the easiest to execute.**
- "Let's only run purple team analysis on Critical findings" — **A Low severity finding can often be chained to achieve critical compromise.**
- "Simulating this is too risky; let's discuss it theoretically" — **Theory is good, but practical validation is required for a complete audit.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You documented the exploit but didn't verify if we logged it" — You ran a red team audit, not purple team.
- "Did you actually test WAF bypasses?" — You assumed control behavior without verifying.
- "How do you know this attack is detected?" — You skipped checking active logging configurations or SIEM rules.
- "This remediation step is too vague; what code should I change?" — Your suggestions are not actionable.
- "You said SQL injection is unblocked, but we use an ORM" — You failed to accurately analyze the codebase.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Finding the vulnerabilities is enough; the defense team can handle the rest." | Without auditing defense effectiveness, you cannot measure actual security posture. |
| "Our WAF blocks all SQL injection, so we are secure." | WAF rules are easily bypassed by encoding or syntax tweaks; they must be tested. |
| "Running simulations is too dangerous for staging." | Run simulations in isolated containers or staging environments using safe payloads. |
| "We wrote the detection rule, so the gap is resolved." | Detection rules must be tested with real payloads to confirm they trigger accurately. |
| "This vulnerability is low severity, so it doesn't matter." | Attackers chain multiple low-risk vulnerabilities to compromise systems. |
| "Mapping every attack path takes too much time." | Prioritize the top 3 critical paths and perform deep validation rather than skipping them entirely. |

## Related Skills

- **mitre-attack-mapper** — Map attack paths directly to MITRE ATT&CK techniques.
- **nist-csf-scanner** — Connect purple team findings to NIST CSF functions (Identify, Protect, Detect, Respond, Recover).
- **security-reviewer** — Standard security review validation.

## Self-Review

After completing this process:

1. **Triage Check:** Did you map both an attack path and a defense verification for every finding?
2. **Perspective Check:** Are red (attack) and blue (defense) team viewpoints balanced?
3. **PoC Safety:** Are all exploit payloads documented safely (e.g., executing `whoami` or reading mock database rows)?
4. **Iron Law Audit:** Is a defense validation mapped for every single attack path?
