---
name: crisis-management
description: Guides standing up a crisis team, deciding under uncertainty, running internal, external and regulator communications, taking the handoff from technical incident to business crisis, and designing tabletop exercises. Use when the user asks about crisis management, executive crisis comms after a breach, or how to run a cyber tabletop exercise.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Crisis management

A crisis is when the impact exceeds what the incident team can own; it's now a
_business_ event (revenue, legal, reputation, survival), not a technical one. Your job
is governance, decisions, and communications, while the technical incident commander
runs the response (`load_skill incident-response-leadership`). Don't merge the two
roles: one drives recovery, the other drives the business through it.

## The handoff: incident → crisis

Declare a crisis (activate this layer) when any trigger hits:

- Critical activity is down past (or trending past) its MTPD/RTO (`load_skill business-continuity`).
- Confirmed/plausible regulated-data breach, or extortion/ransomware with business impact.
- Material financial, safety, or reputational exposure; or media/customer awareness.

On declaration: the incident commander keeps technical command; the **crisis team** takes
strategic decisions, external comms, and regulatory clocks. Single timeline, single source
of truth, shared with IR; don't fork the narrative.

## Crisis team & decision authority

- **Roles**: crisis lead (chairs, owns decisions), exec sponsor (budget/risk acceptance),
  Legal, Comms/PR, IR/tech liaison, HR, business-unit owners, scribe. Named deputies for
  each: crises run nights/weekends.
- **Pre-agree authority _before_ the crisis**: who can authorise system isolation, public
  statements, ransom decisions, invoking DR/failover, spending. Tabletops exist largely to
  expose that this is undefined. Undefined authority = paralysis at 3am.
- **Decision log**: every decision with time, owner, rationale, and what was known then.
  This is the record for regulators, insurers, and the post-mortem.

## Deciding under uncertainty

- Decide on **time-boxed** information, not certainty; set a decision deadline and commit;
  a good-enough decision now usually beats a perfect one after MTPD.
- Work from **reversible vs irreversible**: take reversible actions fast, slow down on
  one-way doors (paying ransom, public attribution, reimaging the only evidence).
- Frame options as scenarios (best / worst / most-likely) with explicit assumptions;
  re-decide as facts land; don't anchor on the first read.
- **Ransom is not a unilateral call**: Legal + exec + insurer, with OFAC/sanctions check
  (paying a sanctioned actor is itself illegal); decryptors often fail; recovery from
  clean backups is the real plan (`load_skill backup-recovery`).

## Communications (three audiences, one truth)

- **Internal**: facts on a cadence (e.g. hourly exec brief); tell staff what to do/not do
  (don't discuss externally, watch for follow-on phishing). Assume attacker reads corporate
  email/Slack; use out-of-band channels until proven clean.
- **External** (customers, partners, market): Legal + PR approve every word. Never promise
  "no data taken" before you know; an over-promise that reverses is the lasting wound, not
  the breach. Hold a single spokesperson.
- **Regulators**: run the clock early: GDPR Art. 33 **72h** from awareness; **NIS2 Art. 23**
  (EU essential/important entities) **24h early-warning → 72h notification → 1-month final
  report**; SEC material cyber **8-K within 4 business days**; sector rules (HIPAA, PCI, DORA
  in EU financial). **APAC clocks differ and rarely match GDPR's 72h**: e.g. Singapore PDPA
  ~3 days to the PDPC, Australia NDB a ~30-day assessment window then notify the OAIC and
  individuals as soon as practicable (not a 30-day filing deadline), Japan APPI prompt-then-~30-day, often needing a
  **local-language filing** to the local regulator; a EU/US playbook that assumes GDPR covers
  everyone under-notifies. If a notifiable event is _plausible_, tell Legal now; under-notifying
  is the costly error. (Decision rules detailed in `load_skill incident-response-leadership`.)

## Tabletop exercise design

- **Objective first**: pick one decision to stress (e.g. "when do we pay / notify / fail
  over?"), not "test everything". Scenario = plausible ransomware/extortion with injects.
- **Right people in the room**: each function that holds authority must be present; the
  point is to surface who-decides-what gaps, not to teach IT to restore.
- **Inject escalation**: drip new facts (data on a leak site, media call, regulator query)
  to force re-decisions under pressure and test comms approval speed.
- **Capture & close**: after-action report with concrete gaps + owners + dates; feed into
  the BC/DR programme. Run ≥ annually (and a regulatory mandate for many: DORA, CPS230,
  FCA/PRA, MAS, FFIEC). verify: https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages
- Escalate realism over time: tabletop → functional drill → DR full-interruption test
  (`load_skill disaster-recovery`).
