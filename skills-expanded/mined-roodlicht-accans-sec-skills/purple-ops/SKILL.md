---
name: purple-ops
description: Purple-team operations — structured detection validation against MITRE ATT&CK through planned emulation, measured coverage gaps, joint red+blue debrief, and tracked closure via D3FEND mapping. Bridge between the pentest bundle and the blue bundle.
---

# Purple Team Ops

> **Bridge skill**: this is a both-blue-and-pentest category. The actual work is collaboration — red simulates a TTP, blue tries to detect it, both learn at the same time. No surprise engagements ("see if we catch them without warning"); that is red team. Purple is planned, measured, and aimed at gap closure.

## When to use

A SOC can write endless rules without ever knowing if they cover the right TTPs. A red team can run endless engagements without the defensive side learning more than "we got owned again". Purple ops is the discipline between the two: ATT&CK-mapped, repeatable, measured.

Triggers on:

- A question like "set up a purple-team cycle", "which TTPs are we not detecting", "ATT&CK coverage measurement", "validate detection rule X against real emulation", "post-pentest debrief with the SOC".
- A handoff from `pentest-reporter` (post-engagement feedback feeding into a detection-gap approach), `detection-engineer` (rule validation), `alert-tuning` (coverage gap identified after rule retirement).
- A periodic (quarterly to half-yearly) maturity measurement of the detection stack.
- Compliance context (NIS2 Art 21 effectiveness evaluation, DORA Art 25 testing) — a purple cycle delivers evidence of "we test our controls".

### When NOT (handoff)

- Surprise red-team engagement without blue informed in advance → pentest skills (`recon-agent`, `c2-hygiene`, `post-exploit`, `pentest-reporter`).
- Writing detection rules → `detection-engineer`.
- Alert tuning on existing rules → `alert-tuning`.
- Threat hunt for the unknown-unknown → `threat-hunt` (command).
- IOC feed work → `ioc-hunter`.
- Forensics after an incident → `forensics-assist`.
- IR itself → `ir-runbook`.

## Approach

Six phases as a cycle, not a one-off project. Each run covers a sub-set of ATT&CK; over quarters you work toward broader coverage.

### 1. Plan: scope, threat-actor emulation, success criteria

- **Threat-actor choice**: emulate a specific group relevant to your sector (FIN7 for financial, APT28 for a geopolitical target, RANSOM cluster for broad impact). MITRE Adversary Emulation Plans as a template.
- **TTP subset**: not the whole kill chain in every cycle. Focus on one tactic or a chain of 2–3 tactics. For example, Q1 Initial Access + Execution; Q2 Persistence + Privilege Escalation.
- **Target systems** in scope: lab? a specific staging environment? a deliberately chosen production segment? RoE sign-off for each.
- **Detection coverage goal**: which ATT&CK techniques do you claim to have covered? DeTT&CT (NL Rabobank-CDC) or ATT&CK Navigator as baseline. Those are the claims you are about to test.
- **Success criteria**: not "we get caught" — measurable: "technique T1003.001 is detected within 5 minutes by rule X with TP confidence high; rule does not fire on baseline traffic". Qualitative AND quantitative criteria.
- **Communication**: the blue team knows that a cycle is running and which window. Not which specific TTPs at which moment — that fingerprint is for blue to find themselves.

### 2. Execute: emulation with atomic-red-team / Caldera / manual

- **atomic-red-team** (Red Canary, MIT) — atomic tests per ATT&CK technique. Small, scriptable, replay-able. Default for unit-style emulation.
  ```bash
  # Example atomic test for T1003.001 LSASS dumping
  Invoke-AtomicTest T1003.001
  ```
- **MITRE Caldera** — full-scenario emulation with an agent on endpoints. Fits multi-step chains.
- **Hand-driven emulation** for TTPs without an atomic equivalent or for a target-specific environment. Document exactly what you did.
- **Replay discipline**: document each execution (timestamp, target, parameters, result). Output goes to the evidence store.
- **Cleanup discipline**: atomic tests have cleanup commands; always run after. Remove Caldera agents after the cycle. Do not leave persistence behind.

### 3. Measure: detection vs. blind, MTTD, false-positive context

Per executed TTP:

- **Detection status**: detected (which rule, how fast) / partial (rule fires but at too low a severity) / blind (no alert).
- **MTTD (Mean Time To Detect)** for covered TTPs: time between execution and alert generation. Goal: shorter than attacker dwell time in a real incident.
- **MTTR (Mean Time To Respond)** for covered TTPs: time between alert and blue-team action. Part of capability measurement.
- **False-positive impact** in the same period: a rule that now fires, how often on baseline? Too many FPs make the rule operationally unusable even when it fires correctly on emulation.
- **Coverage shift**: how much % of the claimed coverage has been validated? New gaps?

Output: a per-TTP row in the coverage matrix with "validated detect" / "validated blind" / "not tested".

### 4. Close gaps: detection-engineering cycle

Per blind spot, an action:

- **Quick win**: existing SIEM data permits detection but there is no rule. Handoff to `detection-engineer` for a Sigma/SPL/KQL rule.
- **Data gap**: SIEM does not have the right log source. Handoff to the log-pipeline team for enablement (Sysmon config, EDR policy, audit-policy expansion).
- **Tooling gap**: rule building is possible but the SIEM platform has limits. Roadmap input for tooling evolution.
- **Compensating control**: detection remains hard, but a D3FEND defensive technique (prevention or mitigation) closes the gap. For example: T1003.001 LSASS dump is hard to detect across every variant; LSASS Credential Guard makes it irrelevant.

D3FEND mapping is core here: per ATT&CK technique, the defensive techniques that mitigate it. Not every gap must close via detection — some via prevention.

### 5. Re-test and track closure

A gap is only closed when you test it again and see validated detect.

- **Re-test cycle**: after detection-rule deployment, run the atomic test again. Confirmation: rule fires, FP rate acceptable, MTTD inside target.
- **Closure tracking** in the coverage matrix: update the status per TTP (validated → re-validated with date).
- **Regression check** periodically: are previously validated detections still firing? Schema drift in log sources, EDR-policy changes, or rule tuning can retroactively break detection coverage.

### 6. Verification-loop and program-level metrics

Layer 1: scope (subset of TTPs covered as planned? all blind spots addressed or explicitly accepted?), assumptions (atomic tests represent real attacker behavior, no lab-only shortcuts?), gaps (D3FEND counters considered or only the detection path?). Layer 2: ATT&CK T-IDs correct, atomic-test IDs really exist in the atomic-red-team repo, MTTD/MTTR figures from the SIEM source of truth, coverage claims supported by DeTT&CT output or an ATT&CK Navigator export.

**Program-level metrics over quarters**:

- Coverage trend (ATT&CK techniques validated-detect / total relevant).
- MTTD trend per severity class.
- New-blind-spots rate (regressions).
- Closure time per blind spot (time from identification to re-validation).

## Output

```
Purple-team cycle report — <quarter/cycle name>
Period: <start → end>
Threat-actor emulation: <APT/group + source emulation plan>
Scope tactics: <T-A##: ... + T-A##: ...>

Plan:
  TTPs in scope:    <T-IDs list>
  Target systems:   <lab/staging/scope segments>
  Success criteria: <per TTP: detect window + FP acceptance>

Execute:
  Per TTP:
    Test method:    <atomic-red-team / Caldera / manual>
    Test-ID:        <T-id ref>
    Run timestamp:  <UTC>
    Target:         <system>
    Cleanup status: <ok>

Measure (coverage matrix):
  TTP | Detected? | Rule-id | MTTD | FP context | Verdict (validated/blind/partial)

Close gaps:
  Per blind spot:
    Type:           <quick-win / data-gap / tooling-gap / compensating>
    Action:         <handoff to detection-engineer / pipeline team / D3FEND control>
    Owner:          <name>
    Deadline:       <date>

Re-test:
  Per closed gap:
    Re-test date:   <...>
    Result:         <validated-detect | partial | still open>

Program-level metrics:
  Coverage trend:        <% validated-detect>
  MTTD trend:            <minutes>
  Open gaps:             N
  Closed this cycle:     N

Handoffs:
  detection-engineer: <new rules / refinements>
  alert-tuning:       <FP tuning on freshly validated rules>
  ir-runbook:         <playbook update for ATT&CK context>
  policy-drafter:     <if a D3FEND control touches a policy requirement>

Verification-loop: ...
```

## References

- **MITRE ATT&CK** — [https://attack.mitre.org/](https://attack.mitre.org/). Common framework.
- **MITRE D3FEND** — [https://d3fend.mitre.org/](https://d3fend.mitre.org/). Defensive-technique mapping.
- **MITRE ATT&CK Navigator** — [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/). Coverage visualization.
- **MITRE Adversary Emulation Plans** — [https://github.com/center-for-threat-informed-defense/adversary_emulation_library](https://github.com/center-for-threat-informed-defense/adversary_emulation_library). Per-actor plans.
- **atomic-red-team** — [https://github.com/redcanaryco/atomic-red-team](https://github.com/redcanaryco/atomic-red-team). Per-technique replay modules.
- **MITRE Caldera** — [https://github.com/mitre/caldera](https://github.com/mitre/caldera). Adversary-emulation platform.
- **DeTT&CT** — [https://github.com/rabobank-cdc/DeTTECT](https://github.com/rabobank-cdc/DeTTECT). NL tooling for data-source and coverage mapping.
- **Center for Threat-Informed Defense** — [https://ctid.mitre-engenuity.org/](https://ctid.mitre-engenuity.org/). Research + tooling.
- **SANS Purple Team Maturity Model** — [https://www.sans.org/](https://www.sans.org/). Maturity rubric.
- **Detection Engineering Maturity Matrix** — community resource for self-assessment.

## Categories

- blue
- pentest
