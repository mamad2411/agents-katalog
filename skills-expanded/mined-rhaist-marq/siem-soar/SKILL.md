---
name: siem-soar
description: Guides standing up and running a SIEM/SOAR pipeline, covering log-source priorities, detection content vs noise, SOAR playbook patterns, alert triage and tuning against fatigue, and the current vendor landscape. Use when the user asks which logs to collect, how to build or tune a SIEM (Splunk, Sentinel, Elastic and others), automate SOC response, or fix alert fatigue.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# SIEM & SOAR

The SIEM is only as good as what you feed it and how ruthlessly you tune it.
Order of work: get the high-value logs in → write behaviour-based detections
(not signature noise) → automate the repetitive triage → tune relentlessly.
Detection content is code: author it with `load_skill detection-engineering`.

## Log sources: collect in this order (value per byte)

1. **Identity / authN**: IdP + directory (Entra ID, Okta, AD security log: 4624/
   4625/4768/4769/4776), VPN. Most intrusions are credential-driven; this is the
   single highest-signal source.
2. **Endpoint EDR / process telemetry**: Sysmon (1 process, 3 net, 7 image-load,
   8 remote-thread, 11 file, 13 registry) or EDR. The detection-engineering
   workhorse; map fields to ATT&CK techniques.
3. **Cloud control plane**: AWS CloudTrail, Azure Activity, GCP Audit, M365/
   Graph audit. Where modern attacks actually land. Enable management _and_ data
   events for crown-jewel buckets.
4. **DNS + proxy/web + firewall flows**: C2, exfil, beaconing. DNS query logs
   catch what TLS hides.
5. **Email security gateway**: phishing is still the front door.
6. **App / WAF / auth logs of crown-jewel apps**; then everything else.

Collect for _detections and investigations you'll actually run_, not "all logs."
Volume = cost + noise. Right-size retention by tier (hot 30 to 90d, cold 1yr+ for IR/
compliance). Normalize to a schema (OCSF/ASIM/ECS) so detections are portable.

## Detection content vs noise

- Buy/import a baseline (vendor analytics, SigmaHQ ~3000 rules) but treat each as a
  candidate; every imported rule is a noise liability until tuned for _your_ env.
- Prefer behaviour over atomic IOC matches (pyramid of pain: TTP detections
  survive; hash/IP rules churn). ATT&CK's Detection Strategies + Analytics model
  (introduced v18, Oct 2025, replacing the old Detections/Data Sources; current
  release v20, Oct 2026); use it to anchor coverage.
  verify: https://attack.mitre.org/resources/updates/updates-october-2026/
- Every detection needs: a documented hypothesis, ATT&CK id, expected FP sources,
  data-source dependency, and a triage runbook. No runbook = don't ship it.
- Track coverage as an ATT&CK heatmap; chase _gaps that match your threat model_,
  not raw technique count.

## SOAR playbook patterns

- Automate the alerts that look the same every time. Canonical wins:
  - **Phishing**: parse reported mail → detonate URL/attachment in sandbox →
    rep/TI lookups → auto-close benign / pull mail + escalate if malicious.
  - **Enrichment-on-ingest**: every alert gets user identity, asset criticality,
    geo/ASN, TI verdict, and recent-change context _before_ it hits the queue.
  - **Auto-close / auto-suppress** known benign positives (vuln scanner source IPs,
    sanctioned admin tools) with a logged reason.
  - **Containment with guardrails**: isolate host / disable user _only_ on high-
    confidence + approved scope; require human approval for blast-radius actions.
- Beware playbook decay: environments, vendor APIs, and attacker TTPs drift, so a
  playbook silently returns wrong answers. Version playbooks, test on a cadence,
  alert on action failures.

## Alert triage & tuning (fight fatigue)

- Categorize every closed alert: true / benign / false positive. That label _is_
  the tuning feedback loop; un-labeled closes teach you nothing.
- The lever order: **suppress** (known-benign) → **dedupe/aggregate** (one
  incident, not 500 alerts) → **enrich** (auto-downgrade in change windows) →
  **threshold/logic tune** → **retire** dead rules.
- Risk-rank the queue by asset criticality × user risk × confidence; analysts work
  top-down, not FIFO.
- Watch >50% FP rates and rising MTTR as the fatigue signal. Run a monthly
  detection audit: top-noise rules, never-fired rules, rules with no runbook.
- A confirmed true positive is an incident: hand off to `load_skill
incident-response`. A recurring detection gap becomes a hunt
  (`load_skill threat-hunting`).

## Current landscape (verify: consolidating fast)

- SIEM/SOAR/XDR are converging into single platforms. Leaders 2026: Microsoft
  Sentinel (+ Defender XDR, Security Copilot), Google SecOps (Chronicle + Gemini),
  Splunk (now Cisco), Palo Alto XSIAM, CrowdStrike Next-Gen SIEM, Elastic.
- QRadar SaaS (QROC/SOAR/Log Insights, sold to Palo Alto) hit end-of-life
  **2026-04-14**; Palo Alto migrates customers to Cortex XSIAM, an active
  displacement driver.
- Standalone SOAR is being absorbed; AI/agentic triage is the 2026 pitch (auto-
  enrich + correlate, escalate to human only on genuine need). Treat AI triage as
  a tuned auto-close, not a replacement for detection rigor.
  verify: https://www.microsoft.com/en-us/security/business/security-101/what-is-soar

## marq tie-in

marq is passive OSINT, not a SIEM and generates no attack telemetry. Generate
test telemetry with your own emulation tooling and confirm the SIEM alerts, then
`report_finding` any logging blind spot you prove (e.g. an attack with no
corresponding log source).
