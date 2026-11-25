---
name: phishing-sim
description: Phishing-simulation campaign workflow — RoE and ethical-scope template, population segmentation, pretexting patterns (HR/IT/finance/vendor/calendar), infrastructure (sender domain, SPF/DKIM/DMARC, tracking), click-rate and credential-success metrics, opt-out and duty of care, NL/EU AVG context for employee monitoring.
---

# Phishing Simulation

> **Awareness goal + ethical template**: phishing sims aim to improve organizational awareness, not to ridicule individuals. No ad-hoc spear phishing against specific people without written sign-off from management AND HR. No pretexts that fundamentally sow mistrust (family emergencies, illness of a colleague, fabricated HR disciplinary actions). NL/EU context: employee monitoring falls under the AVG (GDPR) plus labor law; consultation with the works council and/or employee representation is usually required before campaigns. This skill structures; legal review belongs with legal/HR/DPO.

## When to use

Phishing sims are the standard for organizational awareness and initial-access testing in red-team engagements. They are also the easiest path to becoming a source of distrust if executed poorly. Discipline on pretext choice, opt-out, and post-campaign feedback is not extra — it is the campaign.

Triggers on:

- A question like "design a phishing campaign", "which pretexting patterns are reasonable", "SPF/DKIM/DMARC for our sending infra", "click-rate baselines", "post-campaign debrief", "how do we do this AVG-correctly".
- A red-team engagement where initial access via phishing is needed and the RoE explicitly permits credential harvesting or malware delivery.
- A security-awareness program with periodic (quarterly/half-yearly) sims as a training vehicle.
- A handoff from `recon-agent` (employee OSINT output as input for the target list).
- A compliance question from `nis2` Art 21 (cyber hygiene, awareness training) or `iso27001` Annex A.6.3 (awareness).

### When NOT (handoff)

- Post-foothold action after a successful phish → `post-exploit`, `c2-hygiene`, `ad-attacks`. This skill stops at click/credential capture/payload delivery.
- Web-app exploit context (the phishing link lands on a controlled web app) → `web-exploit-triage`, `payload-crafter`.
- Reporting → `pentest-reporter`.
- AVG/legal review itself → DPO + legal. This skill names obligations; it does not give advice.
- Vendor procurement (Knowbe4 / Cofense / Hoxhunt selection) → out of scope; this skill provides methodology, not a vendor comparison.
- Detection tuning on phishing emails in the inbox → `detection-engineer`, `siem-query`.
- Forensics after a real attacker phish → `ir-runbook`, `forensics-assist`.

## Approach

Six phases. Phase 1 (RoE + ethical template) and phase 6 (debrief + opt-out + duty of care) are the safeguards that keep "campaign" from turning into "awareness incident".

### 1. Rules of Engagement and ethical template

Before any campaign design there is a document stating:

- **Goal** of the sim. Awareness training, baseline measurement, red-team initial access, or compliance evidence?
- **Target population** and exclusions. Which departments, which seniority levels. Who must not be included (employees in re-integration, people who recently reported burnout, external contractors without formal employee status). HR input required.
- **Permitted pretexts** (see phase 3) and excluded pretexts. Standard exclusions: medical cases, illness of a colleague, fictitious HR disciplinary actions, personal financial-damage emails, relationship-related messages, child-abuse reports, etc. Lock the list down before the campaign.
- **Time window**. Working hours? Off-hours excluded? Holiday periods? Usually: do not send before Monday 9:00 or after Friday 17:00, not in the week before or after well-known rest moments.
- **Opt-out procedure**. Everyone has a path to be removed from future sims, without consequences. Communicate this pre-campaign in a general awareness update.
- **Reaction procedure** for those who react (click, enter credentials, open an attachment). Immediately a training page rather than punishment feedback.
- **Reaction procedure** for those who recognize and report it. Positive confirmation — that is the behavior change you are looking for.
- **Oversight sign-off**: in NL this means consultation with the works council (if there is one) plus DPO sign-off plus management sign-off. Some sectors (healthcare, government) have additional requirements.
- **Data handling**. Which data do you collect (click, credential, IP, user-agent)? How long retained? Aggregates open, individual data not — that is the standard.

No campaign without this document. It is not paperwork; it is the line between training and HR violation.

### 2. Population segmentation

Not one campaign for 5,000 people. Segmentation increases realism and reduces collateral damage.

- **Per role**: HR-style pretext to HR is ineffective (they recognize it); IT-style pretext to IT same. Cross-role pretexts are more realistic.
- **Per technical level**: low-tech people expect different triggers than the dev team. Adapt the pretext to the target's vocabulary.
- **Per location / language**: NL employees a Dutch-language email; international offices in local language or English with a tone adjustment.
- **Cohort rotation**: not always the same group. Spread across quarter cohorts so each employee is hit ~1× per year.

### 3. Pretexting patterns at class level

Class level, not copy-paste templates. Per category, the archetypal shape and the spectrum from light to ethical-edge.

- **HR administration**: salary adjustment, contract update, holiday-request confirmation, occupational-health procedure update. **Permitted**: generic administrative flow. **Excluded**: fabricated individual HR actions against the target ("you have been assessed...").
- **IT / helpdesk**: password-reset prompt, MFA enrollment, security-update install, mailbox quota. **Permitted**: organization-wide messages. **Excluded**: impersonation of a named, known IT person without that person's sign-off.
- **Finance / invoices**: vendor invoice, payment confirmation, expense-report correction. **Permitted**: reasonable amounts, generic vendor. **Excluded**: amounts that cause real fear (€10k urgent payment), names of real vendors without their sign-off.
- **Vendor / customer**: shipment update, support-ticket update, software-license renewal. **Permitted**: generic. **Excluded**: real vendor impersonation without their prior sign-off (legally trademark territory).
- **Calendar / collaboration**: meeting invitation, document-share notification (Sharepoint/Drive/Dropbox style), Teams/Slack mention. Classic 2024–2026 pretexts; watch out for exact UI imitation (lightly trademark territory).
- **Authentic-looking but generic**: "Your account access requires verification" — works surprisingly well, because the very fact that "it is generic" lets it slip past attention.

For red-team context with explicit sign-off, spear-phishing with OSINT input from `recon-agent` (LinkedIn title, project reference) is possible. But each spear target requires explicit pre-sign-off from management plus (where possible) the target themselves.

### 4. Infrastructure: sending, landing, tracking

- **Sender domain**:
  - Aged and registered weeks before the campaign (see `c2-hygiene` phase 3).
  - SPF, DKIM, DMARC fully configured to avoid soft-fail flagging. The goal is for email to arrive, not be rejected. (Ironically: campaign emails themselves must be 100% AVG/email-standard compliant.)
  - Cohort/lookalike domain that looks like — but is not — the target domain ('rnicrosoft.com', 'cornpany.com'). Weigh trademark impact.
- **Landing page**:
  - No real credential capture against production passwords; use a training page that says "this was a sim" with educational content. Or, in red-team context, controlled credential capture with immediate destruction after verification.
  - HTTPS required (otherwise browser flagging).
  - Mobile-responsive — most clicks come from phones.
- **Tracking**: 
  - Open tracking via 1px image or unique link per recipient.
  - Click tracking with a unique URL per recipient.
  - Aggregate data is fine; individual data only for those with explicit, hosted consent. Anonymize post-campaign.
- **Hosting**: payload layer on a separate server, separate from the email sender and separate from the team server.

NL/EU AVG context for monitoring: data on individual click behavior is personal data under the AVG. Processing is possible on the basis of legitimate interest (AVG Art 6(1)(f)) provided a balance test is documented. DPO consultation required. With tracking data: aggregate ASAP, do not retain individual data longer than strictly necessary.

### 5. Execution and metrics

During execution:

- **Channel monitoring**: number of arrivals in inbox vs. spam folder (delivery rate). Without delivery there is no measurement.
- **Click rate** (CTR): % of targets that open the link.
- **Credential-success rate**: % that enters credentials (when that layer is present).
- **Reporting rate**: % that reports the email as suspicious to helpdesk/SOC. This is the most important metric — it measures the behavior change.
- **Time-to-report**: average time between sending and the first report. Shorter = better.
- **Helpdesk/SOC load**: number of reports per hour. Scales with campaign size; brief the helpdesk in advance so they are not overwhelmed.

Real-time check before escalation: if click-rate explodes (>40%) or reporting-rate stalls (<5%), pause and reconsider the pretext. Something is off.

### 6. Debrief, training, opt-out, duty of care

After the campaign:

- **Per-target follow-up** for those who clicked: an immediate education page, opt-in for a 5-minute training module. No punishment, no name-and-shame.
- **Per-target acknowledgment** for those who reported correctly: a thank-you email or internal recognition (if the person prefers it).
- **Aggregate report** to management and involved teams: percentages, no names, trends compared to the previous campaign.
- **Lessons learned**: which pretext worked (high), why. Which did not work (low), why. Input for the next campaign and for the security-awareness curriculum.
- **Opt-out update**: anyone who explicitly indicated they no longer wish to participate → exclusion list for the future.
- **Detection feedback** to SOC/detection-engineer: which email features could have been detected by the secure-email gateway, how was bypass possible?
- **Deliberate cleanup of data**: anonymize or remove tracking data after report delivery, in line with the phase-1 data-handling agreements.

Duty of care: if during or after the campaign someone reacts unusually emotionally (complaint, sick note linked to the campaign, escalation to HR), pause the campaign, involve HR + DPO, run an evaluation. No defending it from "it was just a sim". Patterns count.

### Verification-loop

Layer 1: scope (RoE document complete and signed? exclusion list verified? works-council consultation done?), assumptions (data handling AVG-compliant supported?), gaps (debrief procedure operationally ready before sending?). Layer 2: AVG article references correct, CFAA/Computervredebreuk context (NL Wetboek van Strafrecht art 138ab) not falsely claimed as covered, no invented vendor-policy statements, click-rate baselines not served as "studies prove X" without a source.

## Output

```
Phishing-sim plan / report — <campaign name>
Goal: <awareness baseline | red-team initial access | compliance evidence>
Period: <start → end> | RoE signed: <date + sign-offs>

Scope:
  Target population:    <segments + N>
  Exclusions:           <list>
  Permitted pretexts:   <categories from phase 3>
  Excluded pretexts:    <explicit list>
  AVG ground:           <legitimate interest with balance-test ref>
  Works-council/DPO:    <yes/date>

Execution:
  Pretext used:                <category + version ref>
  Sender domain:               <FQDN, age, SPF/DKIM/DMARC>
  Landing page:                <target URL + training content>
  Track mechanism:             <pixel/unique-link>
  Number sent:                 N
  Delivered (inbox):           N
  Spam folder:                 N

Metrics:
  CTR:                  <%>
  Credential success:   <%>
  Reporting rate:       <%>
  Time-to-first-report: <minutes>
  Helpdesk load:        <peaks>

Per-target follow-up:
  Education-page completion:    <% of clickers>
  Opt-out requests received:    <N>
  Escalations to HR/DPO:        <N + type>

Lessons learned:
  What worked:          <pretext element + why>
  What did not:         <element + reason>
  Input for next sim:   <change for cohort N+1>

Detection feedback (handoff to detection-engineer):
  Email headers/content SEG could have caught: <list>

Cleanup:
  Tracking-data anonymization:   <date>
  Sender-domain decommissioning: <date>

Verification-loop: ...
```

## References

- **NIST SP 800-50** — [https://csrc.nist.gov/pubs/sp/800/50/r1/final](https://csrc.nist.gov/pubs/sp/800/50/r1/final). Building an Information Security Awareness and Training Program.
- **ENISA Awareness Material** — [https://www.enisa.europa.eu/topics/awareness-and-training](https://www.enisa.europa.eu/topics/awareness-and-training).
- **Autoriteit Persoonsgegevens — employee monitoring** — [https://www.autoriteitpersoonsgegevens.nl/themas/werk-uitkering/werknemers/de-werknemer-volgen](https://www.autoriteitpersoonsgegevens.nl/themas/werk-uitkering/werknemers/de-werknemer-volgen). NL context for AVG in sims.
- **AVG Art 6, Art 88, Art 35** — [https://eur-lex.europa.eu/eli/reg/2016/679](https://eur-lex.europa.eu/eli/reg/2016/679). Processing basis, employee context, DPIA.
- **NIST Phish Scale** — [https://www.nist.gov/itl/applied-cybersecurity/nist-phish-scale-method-rating-human-phishing-detection-difficulty](https://www.nist.gov/itl/applied-cybersecurity/nist-phish-scale-method-rating-human-phishing-detection-difficulty). Difficulty-rating methodology for pretexts.
- **MITRE ATT&CK — Initial Access (TA0001) / Phishing (T1566)** — [https://attack.mitre.org/techniques/T1566/](https://attack.mitre.org/techniques/T1566/).
- **NCSC-NL — Phishing guidelines** — [https://www.ncsc.nl/](https://www.ncsc.nl/).
- **DMARC.org** — [https://dmarc.org/](https://dmarc.org/). Sender-authentication spec.

## Categories

- pentest
