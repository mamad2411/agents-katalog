---
name: security-program-roadmap
description: Guides standing up or maturing a security program on a budget, covering the first 90 days in order, quick wins vs foundations, a 30/60/90 plus 12-month shape, and budget heuristics. Use when the user is a new CISO or security lead, asks where to start, wants a security roadmap or strategy, or must prioritize limited security spend.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Security program roadmap

The new-CISO failure mode is buying tools before knowing the assets. Spend the
first month learning, not procuring. Anchor to a framework for structure (NIST CSF
2.0 functions: Govern, Identify, Protect, Detect, Respond, Recover; or CIS
Controls v8.1 IG1 for a budget-constrained prioritized list), but the framework is
the map, not the plan.

## First 90 days (opinionated, in order)

**Days 0 to 30: see the ground. Buy nothing.**

- Asset & data inventory. You cannot protect what you can't list. Internet-facing
  surface first; that's what gets hit. marq helps: `load_skill recon-footprint`
  and run external recon on your _own_ domains to see what an attacker sees.
- Identity reality check: how many admins, MFA coverage %, joiner/mover/leaver
  process, service accounts nobody owns.
- Find the crown jewels: the 5 to 10 systems/data sets that, if lost, end the company.
- Read the last pentest/audit and any incidents. `read_file /work/findings.md` if
  an engagement ran. Don't re-discover known holes.
- Meet the business, not just IT. Risk appetite is theirs to set; you advise.

**Days 30 to 60: stop the bleeding (quick wins).**

- MFA everywhere, starting with email, VPN, and all admin access. Highest
  risk-reduction-per-dollar control that exists. Do it first.
- Patch/mitigate anything internet-facing on CISA KEV (`load_skill
vulnerability-prioritization`). Known-exploited + reachable = emergency.
- Kill or vault standing privileged access; remove ex-employee accounts.
- Centralize logs from the crown jewels and edge (even basic); you can't respond
  to what you can't see. Detection comes before fancy prevention.
- Confirm backups exist, are offline/immutable, and _restore-tested_. Untested
  backups are a prayer, not a control. This is your ransomware insurance.

**Days 60 to 90: build the spine.**

- Write the incident response plan and run a tabletop (`load_skill
incident-response-leadership`). Have it in place _before_ the incident.
- Vulnerability management as a _process_ (scan → prioritize → SLA → verify),
  not a one-off scan.
- Baseline a risk register (`load_skill risk-assessment`); it turns gut feel into a
  tracked, ranked, ownable list you can report on.
- Draft the 12-month roadmap and the security policy set (acceptable use, access
  control, data classification). Get exec sign-off and a budget line.

## Quick wins vs foundations: spend the order right

| Quick wins (weeks, cheap, big risk cut)     | Foundations (quarters, enable everything else) |
| ------------------------------------------- | ---------------------------------------------- |
| MFA on email/VPN/admin                      | Asset & identity inventory (continuous)        |
| Patch KEV / internet-facing criticals       | Centralized logging / detection capability     |
| Disable legacy auth, remove stale admins    | IR plan + tested backups                       |
| Email security (DMARC/SPF, phishing filter) | Vuln-management & risk processes               |
| Security-awareness baseline                 | Governance, policy, and a measured roadmap     |

Do quick wins to earn credibility and breathing room; do them _because_ they cut
real risk, not for show. Then spend political capital on the foundations; they're
invisible and slow, which is exactly why they get skipped.

## 12-month shape

- Q1: foundations above operational; first board report (`load_skill
board-metrics-reporting`).
- Q2: detection & response maturity (SIEM/EDR if budget; tuned alerts > more alerts).
- Q3: third-party / supply-chain risk, data protection, segmentation of crown jewels.
- Q4: independent validation (pentest / red team: commission an external one, marq runs none), then
  re-baseline maturity and re-plan. Measure against where you started, not perfection.

## Budget heuristics

- People & process before products. A tool with nobody to run it is shelfware
  that fails the next audit.
- Buy down the biggest _exposed_ risk per dollar; re-use the prioritization
  formula. Don't let a vendor's roadmap become yours.
- Reserve ~10 to 15% for incident response (retainer, insurance); it's cheaper to
  arrange before the breach than during.
