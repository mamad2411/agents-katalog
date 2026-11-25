---
name: mitre-attack-mapper
description: "Maps code patterns, vulnerabilities, and security findings to MITRE ATT&CK techniques. Use when classifying security issues by ATT&CK ID."
---

# MITRE ATT&CK Mapper

## Overview

This skill maps security vulnerabilities, vulnerability patterns, and defenseless code structures in the codebase directly to MITRE ATT&CK techniques (T1190, T1574.002, etc.). Every detected issue is reported along with an actionable ATT&CK ID, relevant mitigation (M-ID) IDs, and detection suggestions. The goal is to anchor security findings to an international standard taxonomy, ensuring teams speak the same language and prioritize defense systematically.

**Core principle:** Every security finding receives an ATT&CK ID. A finding without an ATT&CK ID is a finding that doesn't exist.

## The Iron Law

```
NO SECURITY FINDING CAN BE CLOSED WITHOUT BEING MAPPED TO AT LEAST ONE MITRE ATT&CK TECHNIQUE.
IF YOU CANNOT ASSIGN AN ATT&CK ID TO A FINDING, YOU DO NOT UNDERSTAND THE FINDING WELL ENOUGH.
```

## When to Use

**Use this when:**
- You receive a security scan report (SAST, DAST, SCA) and need to prioritize findings.
- You discover a vulnerability pattern during code reviews.
- You are analyzing the technical root cause of a security incident.
- You need to explain to the defense team which TTPs (Tactics, Techniques, Procedures) they need to defend against.
- You want to clarify which technique to target before writing Sigma, KQL, or Splunk rules.

**Use this ESPECIALLY when:**
- A pentest report contains 50+ findings, making manual classification impossible — this mapper automates that process.
- The team is debating whether a vulnerability is critical — the ATT&CK taxonomy resolves the debate objectively.
- The SOC (Security Operations Center) team asks "why did we get this alert?" — mapping provides the full context.

**Don't skip when:**
- There are no security findings in the codebase (which is highly unlikely — double-check the scanner configurations).
- You are only performing a license compliance check where technical threat mapping is not required.
- Under time pressure — threat mapping actually saves time by automating prioritization.

## Phase 1: Identify Code Patterns and Search for ATT&CK Techniques

**BEFORE proceeding:**

Obtain the raw finding (log, code snippet, error message). Do not attempt threat mapping without understanding the technical details.

1. **Analyze the finding** — Determine its security category (e.g., privilege escalation, code execution, information disclosure).
2. **Locate the tactic in the ATT&CK Matrix** — Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact.
3. **Drill down to the sub-technique level** — Map to the most specific technique ID (e.g., T1190.001 instead of just T1190).
4. **Cross-reference with the technique database** — Read descriptions, detection methods, and mitigations.

```python
# Example: Mapping a SQL injection finding to ATT&CK
# Finding: User input is concatenated directly into a SQL query without parameterization
finding = {
    "type": "sql_injection",
    "file": "app/routes/users.py:45",
    "severity": "critical"
}
# Mapping: T1190 (Exploit Public-Facing Application)
# Sub-technique: T1190.001 (SQL Injection)
technique_id = "T1190.001"
technique_name = "SQL Injection through Public-Facing Application"
mitigation = "M1050: Exploit Protection, M1048: Application Isolation and Sandboxing"
```

## Phase 2: Mitigation and Detection Mapping

**BEFORE proceeding:**

Verify the ATT&CK ID and sub-technique details for each technique.

1. **Assign MITRE mitigations (M-IDs):**
   - M1050: Exploit Protection — for techniques like buffer overflows and RCE.
   - M1040: Input Validation — for injection-based techniques.
   - M1048: Application Isolation — for sandbox evasion techniques.
   - M1038: Execution Prevention — to block malicious code execution.
   - M1047: Audit — to address logging deficiencies.
2. **Propose detection rules:**
   - Sigma rules (generic SIEM format).
   - Splunk SPL queries.
   - KQL queries (Azure Sentinel).
3. **Verify existing controls** — Check if the recommended mitigations are already implemented in the codebase.

```
Technique: T1190.001 (SQL Injection)
├── Mitigation: M1040 (Input Validation) → Are parameterized queries used? → No: GAP
├── Mitigation: M1050 (Exploit Protection) → Is a WAF present? → No: GAP
└── Detection: Sigma sql_injection_error.yml → Splunk sourcetype=sql_error | search ...
```

## Phase 3: Generate Heatmap Reports

**BEFORE proceeding:**

Ensure all findings have been mapped, with mitigations and detections assigned.

1. **Compile all techniques into a matrix** — Show the count of findings per tactic.
2. **Identify coverage gaps:**
   - Tactics with zero findings might indicate lack of testing (potential false negatives).
   - Techniques with zero detection rules represent immediate blind spots.
3. **Prioritize response:**
   - High impact + No detection = Urgent.
   - Low impact + Detection exists = Monitor.
   - High impact + Mitigation exists + Detection exists = Verify.
4. **Export the heatmap** as Markdown, JSON, or CSV.

```
Example Heatmap (CSV format):
Tactic,Technique ID,Finding Count,Mitigation Active?,Detection Active?,Priority
Initial Access,T1190.001,5,NO,YES,CRITICAL
Execution,T1203,2,YES,YES,LOW
Persistence,T1547.001,1,NO,NO,CRITICAL
```

## Phase 4: Final Verification

Before marking complete:

- [ ] Is every finding mapped to at least one ATT&CK ID?
- [ ] Is at least one MITRE mitigation (M-ID) proposed for each ATT&CK ID?
- [ ] Is at least one detection method (Sigma/Splunk/KQL) specified for each ATT&CK ID?
- [ ] Does the heatmap clearly highlight coverage gaps?
- [ ] Are all M-IDs verified against the MITRE ATT&CK database?
- [ ] Are findings prioritized properly (Critical > High > Medium > Low)?
- [ ] Does the report contain a summary accessible to non-technical stakeholders?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This finding is too simple to need an ATT&CK ID" — **Every finding gets an ID. Simplicity is no excuse.**
- "I'll just map it to T1190 roughly, looking up sub-techniques takes too long" — **Without sub-techniques, mapping is too vague to be useful.**
- "This is a known vulnerability, no need to map it" — **Known vulnerability + ID = Actionable. No ID = Forgotten.**
- "We'll write the detection rule later, let's just close the finding first" — **Without detection, you cannot verify if your mitigations work.**
- "There is no mitigation for this technique, I'll just leave it blank" — **If no mitigation exists, write a detection rule and document the risk.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "What ATT&CK ID did you assign to this finding?" — A warning that you skipped threat mapping.
- "Why did you pick this technique? There's a more specific sub-technique." — You didn't drill down deep enough.
- "You didn't propose any mitigation for this." — You forgot to assign an M-ID.
- "Where is the detection rule?" — You mapped the threat but skipped proposing a detection method.
- "What is this heatmap supposed to show me?" — The report summary lacks clarity.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This vulnerability is trivial, it doesn't need ATT&CK mapping." | Trivial vulnerabilities are often overlooked; mapping keeps them visible. |
| "Sub-techniques are too detailed, the parent technique is enough." | Parent techniques often lead to incorrect mitigation suggestions; sub-techniques are critical. |
| "We will write detection rules later; let's finish the report first." | A report without detection suggestions is obsolete from day one. |
| "Everyone knows this vulnerability already." | Assumptions lead to false positives and overlooked risks. |
| "There is already a general rule, we don't need a new one." | Verify if the existing rule actually triggers on this specific technique. |
| "We have mitigations in place, so detection is unnecessary." | Defense-in-depth requires both mitigation and detection. |

## Related Skills

- **nist-csf-scanner** — Connect MITRE ATT&CK mappings to NIST CSF functions (Protect, Detect, Respond).
- **purple-team-analyzer** — Test mapped techniques from both attack (red) and defense (blue) angles.
- **security-reviewer** — Integrate threat mapping into standard security reviews.

## Self-Review

After completing this process:

1. **Completeness Check:** Is the ATT&CK ID + Mitigation + Detection triad complete for every finding?
2. **Sub-Technique Check:** Are all techniques mapped to their most specific sub-techniques?
3. **Validity Check:** Do all selected ATT&CK IDs and M-IDs exist in the official MITRE database?
4. **Actionability Check:** Can a SOC analyst or developer immediately act on your recommendations?
