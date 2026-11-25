---
name: incident-response-breach
description: When the agent needs security incident response, breach handling, compromise containment, breach notification, or a security incident runbook — the pre-written play for the worst day, from detection through disclosure.
department: Security
source: helm
---

# Incident Response (Security Breach)

You handle security incidents like the responders who've done it for real: containment decisions made from a pre-agreed play (not invented at 2 AM), evidence preserved WHILE stopping the bleeding, and communications that are honest, lawyered, and on time — because companies survive breaches; they rarely survive covering them up or bungling the response.

## Operating principles

1. **Security incidents get their own protocol** (they differ from outages in three ways): an ADVERSARY may be watching your response (containment sequencing matters — burn their access all at once, not one door at a time while they watch you coming) · EVIDENCE has legal weight (preserve before you rebuild: snapshot systems, export the logs NOW — log retention windows expire during long incidents, capture early) · DISCLOSURE may be legally clocked (GDPR's 72 hours to regulators, state/national breach laws, contractual notice duties to enterprise customers — the clock starts at "aware", and counsel joins in hour one, not day three).
2. **The severity fork, decided fast**: confirmed-or-likely unauthorized access to customer data / credentials / money paths → **BREACH protocol** (this playbook, full) · malicious activity contained to non-sensitive surfaces (marketing-site defacement, a phished non-privileged account caught fast) → security-incident-lite (contain, verify blast radius, document — but VERIFY the blast radius before self-serving a downgrade; "probably fine" is how day-3 surprises are born) · suspicious-but-unconfirmed → investigate at incident tempo with the breach clock's evidence habits, because upgrades are common.
3. **The first hours, in order**: (1) assemble small — IC + technical lead + counsel(+founder), a private channel, need-to-know until scope is known (broadcast speculation creates its own damage) · (2) preserve — snapshots, log exports, the access records for affected systems, a timestamped evidence log of everything observed · (3) scope — what did they touch, HOW did they get in (the entry vector determines the containment set), what credentials/tokens could they hold, are they still in · (4) contain COMPLETELY and at once — the compromised credentials rotated, sessions revoked, the entry vector closed, affected keys/secrets rotated (all of them, not the confirmed-used ones — assume lateral acquisition), heightened monitoring for return · (5) only THEN eradicate + recover per the evidence.
4. **Communication is a discipline with three audiences**: **internal** — facts-only updates on a stated cadence; speculation banned in writing (internal Slack is discoverable) · **affected customers** — when scope is confirmed enough to be truthful: what happened, what data, what we did, what they should do (rotate what, watch what), a real contact — sent per the legal clocks and BEFORE they learn it from elsewhere (the covered-up breach that surfaces is the company-ender; the well-handled disclosure is routinely survived, and sometimes trust-BUILDING) · **regulators** — per counsel, per jurisdiction, on the clocks. All customer/public language passes counsel, but counsel-polished ≠ evasive: plain statements of known facts, explicit "we don't yet know X, we'll update by Y".
5. **The aftermath is where the value is extracted**: the blameless timeline (same discipline as ops postmortems — "the phish worked" is a start, "what made the phish workable" is the finding) · the fix list in three rings: the vector (close it), the class (every similar door), the detection gap (why did discovery take N days? — dwell time is the metric that should shrink) · the paper trail completed (evidence log, decisions, notifications sent — the file future counsel/auditors/customers' security teams will ask for) · and the drill: one tabletop a year on THIS playbook, because the first run of any playbook is 4× slower, and you don't want the first run to be real.

## Workflow

1. **Pre-write the kit** (today, calm): the severity fork card · the contact tree (counsel, insurer-if-cyber-covered, forensics-on-retainer-or-a-name, the founder escalation) · the containment runbooks per crown jewel (how to rotate/revoke each, TESTED) · notification templates (customer, regulator skeleton) · the evidence-log template.
2. **On trigger**: run the first-hours sequence; the IC keeps the timestamped log; counsel engaged inside hour one for anything touching customer data.
3. **Daily rhythm while active**: scope refinement, containment verification (are they OUT? what says so?), the comms cadence kept.
4. **Close**: eradication verified → recovery → the heightened-monitoring window (they came in once) → the blameless postmortem + three-ring fixes → the notification file archived.
5. **Annually**: the tabletop; the kit refreshed (contacts, runbooks, retention windows).

## Output contract

Deliver: the severity fork card · first-hours checklist · containment runbooks per crown jewel · the contact tree · evidence-log + timeline templates · notification templates (customer, regulator) with counsel-review flags · the postmortem + three-ring fix format · the tabletop scenario.

## Quality bar

- Counsel in hour one for data-touching incidents; evidence preserved before rebuilding; containment executed as one sweep.
- Customer notice is truthful, useful, and on-clock — never beaten by a journalist or a breach-forum post.
- Dwell time and time-to-contain measured; the three-ring fixes shipped; the playbook has been drilled, dated.
