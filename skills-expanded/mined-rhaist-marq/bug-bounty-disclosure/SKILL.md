---
name: bug-bounty-disclosure
description: "Covers running or participating in bug bounty and coordinated vulnerability disclosure: the ISO/IEC 29147 and 30111 process, safe harbor and legal, triage, severity and dedup, disclosure timelines, and the CVE/CNA path. Use when the user asks how to set up a VDP or bug bounty program, report a vulnerability to a vendor, write a security.txt or disclosure policy, or request a CVE."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Bug bounty & coordinated disclosure

Authorized testing only: bug bounty scope _is_ your authorization. Read the
program's policy + scope before touching anything; out-of-scope testing has no
safe harbor and is just unauthorized access. This skill covers both sides:
**researching/reporting** a bug and **receiving/handling** one.

## 1. The two standards (current versions)

- **ISO/IEC 29147:2018**: vulnerability _disclosure_: how an org receives,
  assesses, and responds to external reports (the outward-facing side).
  https://www.iso.org/standard/72311.html
- **ISO/IEC 30111:2019**: vulnerability _handling_: the internal triage →
  remediation → release process (the inward-facing side). Paired set; one
  takes the report in, the other fixes it. https://www.iso.org/standard/69725.html
- Baseline obligations they encode: a **published, advertised contact**
  (security.txt / VDP page), **meaningful acknowledgement within ~7 days**, and
  a defined handling process. Stand these up before launching a program.
- **EU CRA** (manufacturers): since **11 Sep 2026**, actively exploited vulns go to
  the CSIRT + ENISA via the CRA Single Reporting Platform (24h / 72h / 14 days);
  the Annex I CVD-policy duties apply from 11 Dec 2027: `load_skill eu-cra`.
  https://digital-strategy.ec.europa.eu/en/policies/cra-reporting

## 2. Safe harbor & legal (researcher and program)

- **Safe harbor** = the program's written promise not to pursue legal action
  for good-faith research within scope. As a researcher, _do not test a program
  that lacks one_; as a program owner, adopt one; it's the single biggest
  driver of quality reports. Standard template: disclose.io
  (https://github.com/disclose/dioterms, https://disclose.io/).
- **US CFAA**: DOJ's **May 2022** charging policy directs declination for
  "good-faith security research" (testing to find/fix flaws, no harm, used to
  improve security), but it's _prosecutorial discretion, not immunity_, and
  doesn't stop **civil** suits. Stay in scope to stay good-faith.
  https://www.justice.gov/archives/opa/pr/department-justice-announces-new-policy-charging-cases-under-computer-fraud-and-abuse-act
- HackerOne's "Gold Standard Safe Harbor" raised the bar for program language:
  prefer programs that adopt it. verify:
  https://www.hackerone.com/press-release/hackerone-announces-gold-standard-safe-harbor-improve-protections-good-faith-security
- **Jurisdiction matters.** The CFAA good-faith framing is US-specific; many APAC
  computer-misuse laws (e.g. Singapore CMA, and equivalents in JP/AU) have no
  good-faith carve-out, so out-of-scope or cross-border testing is plain
  unauthorized access no matter how the program reads. Confirm where the asset, and you, sit before testing.
- Hard lines regardless of policy: no data exfiltration beyond a proof token,
  no pivoting to third-party/other-tenant data, no DoS, no social-engineering
  staff unless explicitly allowed, no extortion ("pay or I publish" voids good
  faith entirely).

## 3. Scope & triage (running a program)

- **Scope** = explicit assets in/out, allowed techniques, and reward bands.
  Keep it current; an asset list that drifts generates "out of scope" friction
  and lost trust.
- **Triage funnel**: validate → reproduce → severity → dedup → reward → fix →
  disclose. Acknowledge fast even if triage is slow; silence is what makes
  researchers go public.
- Reproduce from the report's PoC before escalating; reject only with a reason
  (helps the researcher and the relationship).

## 4. Severity & dedup

- Score with **CVSS** for a common language, but reward on _real-world impact +
  exploitability_, not the base number alone: chain context and reachability
  matter (`load_skill vulnerability-prioritization` for the exposure/EPSS lens).
  Use the project's `report_finding` with the CVSS vector for an auditable base
  score.
- **Dedup rule**: same root cause = one bounty to the first valid reporter, even
  across different endpoints/parameters. Distinct root cause = distinct reward.
  Document the dedup decision; it's the most-disputed call.
- Bonus for a clean PoC + remediation advice; that's the report you want more of.

## 5. Disclosure timelines

- **Coordinated** is the norm: agree a fix window, disclose together. Common
  default deadlines researchers use: **Google Project Zero: 90+30** (90 days to
  fix, then +30 days for patch adoption before full technical detail; +14-day
  grace if a fix is imminent, and since its 2025 policy update a ~1-week
  transparency notice that a report exists), CERT/CC: **45 days**. Cite the policy
  you're operating under. verify: https://projectzero.google/vulnerability-disclosure-policy.html
- Adjust for actively-exploited (0-day) bugs: shorten and coordinate with a
  CERT. Never sit on an in-the-wild exploit waiting for a tidy fix.
- As a program: communicate the patch ETA; as a researcher: hold publication to
  the agreed date if the vendor is engaging in good faith. Full disclosure is a
  last resort for an unresponsive vendor, not a default.

## 6. CVE / CNA process

- A **CVE ID** is the public identifier; issued by a **CNA** (CVE Numbering
  Authority), usually the affected vendor if they're a CNA, else a root/CNA-LR
  (e.g. MITRE) or a third-party CNA for that product. Since Nov 2025 ENISA is
  also a Root (EU authorities, EU CSIRTs-network members, its cooperative partners).
- To request an ID: find the right CNA at
  https://www.cve.org/PartnerInformation/ListofPartners; if none applies, use
  MITRE's webform https://cveform.mitre.org/. CNAs must respond to assignment
  requests per the CNA Operational Rules
  (https://www.cve.org/resourcessupport/allresources/cnarules).
- A good CVE record: affected product+versions, vuln type (CWE), impact, and the
  CVSS vector. CVE feeds NVD/KEV downstream; that's how defenders find it, so
  accuracy matters more than speed.
- Changes/disputes go through the issuing CNA. verify current submission flow:
  https://cveproject.github.io/

## Anti-patterns

- Testing a program with no safe-harbor / no published policy; you have no
  legal cover and may be committing an offense.
- Going public to pressure a vendor before the agreed window while they're
  actively fixing: it burns coordination and may aid attackers.
- Rewarding/scoring on raw CVSS while ignoring exploitability and dedup root
  cause: it overpays noise, underpays the chained critical.
- Receiving reports with no ack SLA: the fastest way to push researchers to
  full disclosure.
