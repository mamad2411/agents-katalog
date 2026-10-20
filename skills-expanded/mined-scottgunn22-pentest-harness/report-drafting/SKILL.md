---
name: report-drafting
description: Structure, CVSS rubric, and style for the engagement deliverable. Triggers when drafting findings, when computing severity, or when the report-drafter agent is invoked.
---

# Report Drafting

## CVSS v3.1 rubric (for finding-writer)

Build the vector from these decisions, in order:

| Metric | Values | Rule |
|---|---|---|
| AV (Attack Vector) | N, A, L, P | N=internet; A=adjacent/LAN; L=local shell required; P=physical |
| AC (Attack Complexity) | L, H | H only if attacker needs reconnaissance or special conditions beyond having access |
| PR (Privileges Required) | N, L, H | N=none; L=any authenticated user; H=admin |
| UI (User Interaction) | N, R | R only if a user must click/open something |
| S (Scope) | U, C | C if exploitation impacts components beyond the vulnerable one (cross-VM, cross-tenant, AD-wide) |
| C, I, A (Impact) | N, L, H | H=complete loss; L=limited; N=none |

Common patterns:

- **SMB signing not enforced** → `AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` (8.1, High)
- **Unauth RCE on internal web app** → `AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` (8.8, High)
- **Cleartext SMTP creds in PCAP** → `AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (6.5, Medium)
- **Kerberoastable service account** → `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` (8.1, High) — N because the attacker is already a domain user
- **Outdated TLS (TLS 1.0)** → `AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N` (4.2, Medium) — H/R because MITM required

## Severity from score

| Score | Severity |
|---|---|
| 9.0–10.0 | Critical |
| 7.0–8.9 | High |
| 4.0–6.9 | Medium |
| 0.1–3.9 | Low |
| 0.0 | Info |

Adjust **down one bucket** when compensating controls limit real-world
exploitability. Examples:

- Vulnerable service is only reachable from one jump host that has MFA →
  drop High to Medium.
- Network segment is monitored with a working EDR that would catch the
  exploit → drop High to Medium (and reference the EDR finding in
  `references`).

Never adjust up. If you think a CVSS of 6.5 understates the risk, write a
better `business_impact` paragraph instead.

## Finding structure

Each finding has these sections in the report:

1. **Header** — ID, title, severity, CVSS vector + score, affected assets, status
2. **Business Impact** — 1 paragraph, non-technical audience. What an
   attacker can do, why it matters to *this business*.
3. **Technical Detail** — 2–4 paragraphs, technical audience. What the
   vulnerability is, how it works, why it exists.
4. **Reproduction** — numbered steps, copy-pasteable, each citing an
   evidence artifact or a command.
5. **Remediation** — specific (named patches/versions/configs), with an
   effort estimate (`low|medium|high`).
6. **References** — CVE pages, vendor advisories, MITRE ATT&CK technique
   IDs.

## Exec summary style

- 3–5 sentences max.
- Plain language. "Anyone on the corporate network can read every
  customer's records" not "SMB signing is not enforced on file servers".
- Lead with the most-business-relevant finding, not the highest CVSS.
- End with the overall risk rating and a one-line rationale.

Avoid:
- "The attacker", "imagine if", "in the worst case"
- Marketing tone
- Numbers without context ("12 findings" — so what)

Prefer:
- Direct, factual, past/present tense
- One concrete business consequence per high/critical finding
- Numbers with comparison ("3 of the 12 findings allowed unauthenticated
  access to customer data")

## Attack narrative

Chronological prose form, drawn from `attack_chain[]`. Each step cites a
finding ID. Reads like a story but with citations. Length: one paragraph
per step, no longer than 8 paragraphs total. If the chain is longer, group
similar steps.

## What makes a remediation actionable

Bad: "Apply security patches."
Better: "Apply Microsoft security update KB5028166."
Best: "Apply KB5028166 to the 3 affected file servers (ACME-H-001 through
ACME-H-003) and confirm via `Get-HotFix -Id KB5028166`."

Bad: "Use strong passwords."
Better: "Enforce a 14-character minimum password policy."
Best: "Set `MinimumPasswordLength = 14` in the Default Domain Policy GPO,
re-link, and force password rotation for the 12 accounts in
Domain Users that currently have <14-character passwords."

## What makes a finding fail review

- No evidence reference
- "TBD" anywhere in remediation
- Severity that doesn't match the CVSS score
- Credentials in plaintext
- PII not redacted in evidence (operator catches this in `--final`)
- Reproduction steps that aren't independently runnable
