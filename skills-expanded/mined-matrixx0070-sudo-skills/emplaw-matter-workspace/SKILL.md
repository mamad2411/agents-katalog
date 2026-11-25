---
name: emplaw-matter-workspace
version: 1.0.0
description: Set up a tracked, privilege-aware matter folder with a matter ID, parties, key dates, and status tracking for a specific employment-legal issue.
author: matrixx0070
tags: [matter-management, privilege, intake, tracking, workspace]
capabilities: []
---

## When to use
Use this when a discrete employment-legal issue arises — a complaint, an accommodation request, a threatened claim, a layoff — and you need a dedicated, privilege-designated workspace to track parties, dates, documents, and status. **Not for:** configuring the plugin org-wide (that is emplaw-cold-start-interview / emplaw-customize); drafting policy content (emplaw-policy-drafting); reviewing the handbook (emplaw-handbook-updates); conducting the substantive investigation itself (emplaw-internal-investigation).

## Method
1. Assign a matter ID using the firm naming convention and record the matter type (e.g., discrimination charge, ADA accommodation, WARN layoff, wage dispute).
2. Record parties: complainant/employee, respondent(s), decision-makers, and outside agencies (EEOC, state agency). Decision point: if a government charge number exists, capture it and its response deadline; else set an internal review date.
3. Capture key dates: incident date, notice date, statutory deadlines, and limitations dates. Decision point: if any deadline is under 14 days, flag URGENT and route to counsel immediately.
4. Set the privilege designation. Decision point: if the matter anticipates or involves litigation/legal advice, mark Attorney-Client Privileged / Work Product and restrict access; else mark Business Record.
5. Build the file structure (intake, evidence, correspondence, drafts, final) and apply a litigation-hold flag if triggered.
6. Set status tracking (Open / Active / Awaiting-counsel / Closed) and the responsible owner.
7. Confirm privilege labeling and access list before adding any documents.

## Example
An employee files an EEOC charge alleging ADA discrimination. You open matter EMP-2026-014 (type: ADA/EEOC charge), record the charge number and 30-day response deadline, mark it Attorney-Client Privileged, issue a litigation hold on the employee's personnel and email records, and set status Awaiting-counsel with the 30-day deadline flagged URGENT.

## Pitfalls
- **Mislabeling privilege.** Business records swept into a "privileged" folder can waive privilege for the whole folder; label per document and per purpose.
- **Missing a statutory deadline.** EEOC responses and state-agency deadlines are short and unforgiving; capture and flag every date at intake.
- **Forgetting the litigation hold.** Failing to preserve records once litigation is anticipated risks spoliation sanctions.
- **Over-broad access.** Every added reader can weaken privilege; keep the access list minimal and logged.

## Output format
```
EMPLAW MATTER — <matter ID>
Type: <complaint | ADA | WARN | wage | other>
Privilege: <Attorney-Client/Work Product | Business Record>
Parties: complainant <name>; respondent <name>; decision-makers <...>; agency <EEOC/state, charge #>
Key dates: incident <d>; notice <d>; response deadline <d>; limitations <d>   URGENT: <y/n>
Litigation hold: <issued? scope>
File structure: /intake /evidence /correspondence /drafts /final
Status: <Open | Active | Awaiting-counsel | Closed>   Owner: <name>
Escalation: counsel notified <y/n, date>
```

## Reference
General deadline and coverage reference (not tailored legal advice): EEOC charge filing is generally 180 days (300 in deferral states); an employer's response to a charge is set by the agency notice, often ~30 days. Federal coverage attaches at Title VII/ADA 15+, ADEA 20+, FMLA 50+/75-mi, WARN 100+ (60-day notice). Preserve records once litigation is reasonably anticipated (litigation-hold duty). Privilege attaches to communications for the purpose of legal advice and to materials prepared in anticipation of litigation; mixed-purpose documents are vulnerable. Escalate to licensed counsel before any agency response or adverse action — this skill organizes a matter, it does not provide legal advice.
