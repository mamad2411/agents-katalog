---
name: insider-threat
description: "Covers insider-threat program design: malicious, negligent and compromised insider types, behavioral and technical indicators, UEBA, the privacy/legal/ethics guardrails, and cross-functional HR/Legal/Security governance. Use when the user asks how to build an insider-threat program, detect data theft by employees or departing staff, deploy UEBA lawfully, or respond to a suspected insider."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Insider threat program

An insider already has trusted access, so detection is about **anomaly, not
intrusion**. The hard part is not the tech; it's running it without building a
surveillance apparatus that destroys trust and breaks the law. The whole program
lives or dies on the privacy/ethics guardrails below. Anchor to CISA's Insider
Threat Mitigation Guide and the NITTF framework.
verify: https://www.cisa.gov/topics/physical-security/insider-threat-mitigation
verify: https://www.dni.gov/index.php/ncsc-how-we-work/ncsc-nittf

## Three insider types (different responses)

- **Malicious**: abuses access for gain, espionage, sabotage, or revenge.
  Often follows the critical-pathway: personal predisposition → stressor →
  concerning behavior → (missed intervention) → harmful act. Response: detect +
  investigate + deter.
- **Negligent**: knows policy, ignores it (shadow IT, shared creds, lost
  laptop, misdirected data). The largest-volume category. Response: friction
  reduction + targeted training (`load_skill security-awareness`), not investigation.
- **Compromised**: credentials stolen; the user is a victim, the activity looks
  like a normal login. **Fastest-growing type, and UEBA/DLP alone miss it**;
  it needs external credential-leak monitoring + impossible-travel/session
  signals to separate "Bob" from "attacker-as-Bob."
  verify: https://www.cisa.gov/topics/physical-security/insider-threat-mitigation/defining-insider-threats

## Indicators

**Behavioral (HR/manager-observed, the critical-pathway signals):**

- Disgruntlement after a negative event (passed-over, PIP, layoff notice, dispute).
- Unexplained affluence, financial distress, or undisclosed conflicts of interest.
- Working odd hours for no reason, declining to take leave, scope-creep curiosity
  outside role, policy-flouting, hostility to controls.
- Note: indicators are signals to _support/assess a person_, not proof of guilt;
  most people with stressors never become threats.

**Technical (tooling-observed):**

- Mass download/staging before resignation; access outside job function; large
  transfers to USB, personal cloud, or webmail; privilege escalation; dormant-
  account or backdoor-account use; anomalous volume/time/location (DLP catches destination).
- Departing-employee window: the 30 to 90 days around resignation is peak IP-theft risk.

## UEBA & detection stack

- **UEBA** baselines each user/entity and alerts on deviation (volume, timing,
  location, peer-group outliers). Tune to behavior change, not static rules.
- Correlate UEBA + **DLP** (content/destination) + **IAM/PAM** (access &
  privilege) + **HR signals** (life events, departures); no single source is enough.
- For compromised insiders: add breach/credential-leak monitoring + conditional
  access. When UEBA flags anomalous behavior, check if those creds appear in
  recent breaches before treating it as malice.
  verify: https://www.cisa.gov/topics/physical-security/insider-threat-mitigation/detecting-and-identifying-insider-threats

## Privacy / legal / ethics: the guardrails (this is the hard part)

Done wrong, the program is illegal, toxic, or both. Concrete guardrails:

- **Target behavior, not people.** Monitor anomalous _activity_; never profile by
  protected class, politics, off-duty conduct, or "vibes." NITTF: programs
  "target anomalous behaviors, not individuals."
- **Transparency & notice.** Publish an acceptable-use/monitoring policy;
  employees should know corporate systems are monitored. No secret dragnet.
- **Proportionality & data minimization.** Collect the least needed; pseudonymize
  in analytics; short retention; access to raw monitoring data is itself
  privileged and logged.
- **Least privilege on the program.** Who can de-anonymize an alert or open an
  investigation is tightly scoped, dual-control, and audited: watch the watchers.
- **Legal basis & jurisdiction.** EU/works-council settings → DPIA, works-council
  agreement, lawful basis; US → state/wiretap/consent rules; APAC → consent-based
  employee-monitoring regimes (China PIPL, Japan APPI, Korea PIPA) that a US-style
  blanket-monitoring default violates. Legal owns this gate.
- **Due process.** An alert is an _inquiry_, not a verdict; humans adjudicate;
  the subject gets fair handling. Constitutional/privacy rights preserved (NITTF).
  verify: https://www.dni.gov/index.php/ncsc-how-we-work/ncsc-nittf/ncsc-nittf-training

## Detect → deter → respond

- **Deter**: visible (not secret) controls, clear policy, healthy culture,
  exit/offboarding discipline; most negligent and many malicious acts are
  prevented by knowing controls exist + frictionless secure paths.
- **Detect**: the UEBA/DLP/IAM/HR fusion above, with tuned thresholds and an
  alert triage queue.
- **Respond**: graduated, with coaching/training for negligent; access review +
  monitoring for amber; investigation + containment for confirmed malicious
  (chain-of-custody, `load_skill incident-response-leadership`). Offboard fast
  and revoke same-day on departure.

## Governance: cross-functional or it fails

- **Multi-disciplinary team**: Security, HR, Legal/Privacy, IT, and management;
  no single function runs it. CISA's Jan-2026 guidance: assemble a
  multi-disciplinary insider-threat management team spanning physical + cyber +
  personnel, run through its POEM lifecycle (Plan → Organize → Execute → Maintain).
  verify: https://www.cisa.gov/resources-tools/resources/assembling-multi-disciplinary-insider-threat-management-team
- **HR** owns behavioral context and intervention; **Legal/Privacy** owns the
  lawful-basis gate and adjudication; **Security** owns detection/response.
- Documented charter, escalation path, evidence handling, and audit of the
  program's own actions. Define metrics: mean time to detect anomaly, % alerts
  adjudicated within SLA, departing-employee access-revoke timeliness, false-positive rate.
