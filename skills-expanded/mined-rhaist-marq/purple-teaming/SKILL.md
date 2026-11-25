---
name: purple-teaming
description: "Guides running the collaborative red plus blue detect-improve loop: executing MITRE ATT&CK techniques, measuring detection coverage, and turning every gap into a tested detection. Use when the user asks to plan a purple team exercise, validate SOC detections with adversary emulation (Atomic Red Team, CALDERA), or measure ATT&CK coverage."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Purple teaming

Authorized exercises only (marq runs no techniques; use your own emulation tooling). Purple
teaming is red and blue working _together in the same room_ to improve
detection, not a separate team. The deliverable is **new detections + measured
coverage**, not a flag captured. Where a red team hides, a purple team announces
each technique so blue can hunt for it in real time.

## 1. The loop (one technique at a time)

1. **Pick a technique** from the threat model (ATT&CK ID). Prioritize what the
   relevant actor actually uses: `load_skill actor-ttp-attribution`.
2. **Plan** the exact procedure + expected telemetry (which log source/EDR event
   _should_ fire). Write the hypothesis down before executing.
3. **Execute** the technique on an agreed host, timestamped.
4. **Observe**: did the EDR/SIEM alert? Did the raw telemetry even exist? Three
   outcomes: detected & alerted / logged-but-no-alert / no telemetry at all.
5. **Improve**: write or tune the detection, replay the technique, confirm it
   now fires. Don't move on until the gap is closed and the fix is _verified by
   re-running_.
6. **Record** the result against the technique and repeat.

That tight execute→observe→tune→re-test cycle is the whole value; a one-shot
"did it alert?" with no remediation is just a test, not purple teaming.

## 2. Running an exercise

- **Same room, shared screen.** Red narrates ("running T1003.001 now"), blue
  watches their console live. Latency between action and detection is itself a
  finding (mean-time-to-detect).
- Start from an **assumed-breach** host so you spend the day on detection-rich
  post-exploitation, not initial access.
- Scope to a **technique set** (10-20 mapped to your top threats), not "try to
  win." Breadth of coverage beats depth of compromise here.
- Keep a control host clean for telemetry baselining (distinguish your activity
  from noise).
- Feed findings straight back into the next red-team scenario, and the gaps
  into the SOC backlog.

## 3. Measure detection coverage against ATT&CK

- Track every technique's outcome on an **ATT&CK Navigator layer**: green =
  alerting, yellow = logged-only, red = blind. This heatmap is the executive
  artifact and the trend line across exercises.
- Report the four-tier metric per technique: **prevented / detected (alert) /
  logged-only / no-visibility**, not a single pass/fail. "We have the logs but
  no rule" is a different fix than "we have no logs."
- Don't claim coverage from one passing atomic: a technique has many
  procedures; an EDR may catch one variant and miss another. Note _which
  procedure_ was tested.
- Trend the numbers exercise-over-exercise; coverage going up is the program's
  KPI.

## 4. Tooling (verify current capabilities)

- **Atomic Red Team**: small, per-technique tests mapped to ATT&CK; the fast
  way to fire a single procedure and check telemetry.
  https://github.com/redcanaryco/atomic-red-team
- **CALDERA** (MITRE): automated, chained adversary emulation for repeatable
  multi-step scenarios. https://github.com/mitre/caldera
- **VECTR** (SecurityRiskAdvisors): the system of record; log each red action,
  the blue outcome, and track campaigns/coverage against ATT&CK over time.
  https://github.com/SecurityRiskAdvisors/VECTR
- **PTEF**: SCYTHE's Purple Team Exercise Framework gives the meeting/cadence
  structure (planning, execution, lessons-learned).
  https://github.com/scythe-io/purple-team-exercise-framework
- Pattern: emulate with Atomic/CALDERA → confirm detection in the SIEM/EDR →
  record outcome in VECTR → re-test after tuning.

## 5. Turn gaps into detections

- For each red/no-visibility result, decide the fix layer: **collection** (turn
  on the missing telemetry: Sysmon config, EDR policy, audit policy) before
  **detection** (write the analytic). No log = no rule is possible.
- Write the detection as code (Sigma → deploy to the SIEM), version-controlled,
  with the ATT&CK ID, the test that proves it, and a tuned false-positive
  baseline. Hand off to `load_skill detection-engineering` for the rule
  lifecycle (test data, FP tuning, deployment).
- **Validate by replay**: the detection isn't done until re-running the
  technique fires the alert and a benign baseline run does _not_.
- Feed confirmed detections + residual gaps into incident-response runbooks
  (`load_skill incident-response-leadership`) and prioritize remaining blind
  spots with `load_skill vulnerability-prioritization`.

## Anti-patterns

- "We ran 200 atomics, scored 60%" with no rules written; that's a coverage
  audit, not purple teaming; the loop's whole point is _closing_ gaps.
- Counting a technique as covered off one atomic variant.
- Red and blue in separate rooms / async: kills the real-time learning that
  makes it purple rather than red-then-debrief.
- Writing a detection and never replaying to confirm it actually fires.
