---
name: detection-engineering
description: Covers detections as code, including writing Sigma rules, MITRE ATT&CK coverage mapping, testing with Atomic Red Team and CALDERA, and the detect-tune lifecycle that controls false positives. Use when the user asks to write or convert a detection rule, build a Sigma rule, map SIEM content to ATT&CK, test whether detections fire, or reduce false positives.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Detection engineering

Treat every detection like production software: version-controlled, peer-reviewed,
tested, deployed via pipeline, measured. The output is detection _content_ that
the SIEM/SOAR runs (`load_skill siem-soar` for the platform + triage side). Many
detections are born from a hunt: `load_skill threat-hunting` covers the discovery
loop that feeds this one.

## Detection-as-code workflow

1. **Source the requirement**: a hunt finding, a threat-intel TTP (`load_skill
actor-ttp-attribution`), a new ATT&CK technique, a public PoC, or a post-
   incident gap. Each becomes a documented detection idea, not a hunch.
2. **Author** the rule in a portable format (Sigma) in a Git repo, organized by
   ATT&CK technique / log source.
3. **Peer review** via pull request: logic, FP exposure, performance, runbook.
4. **Test** against labeled data + emulated attacks (below). Red = true-positive
   fires AND benign data stays quiet.
5. **CI** validates schema, converts to backend queries (sigma-cli), runs against
   test data; promote through staging → production via API with rollback.
6. **Deploy + monitor** FP/TP rates; loop back to tune. Rule lifecycle: draft →
   test → production → tuning → deprecated.
   verify: https://github.com/sigmahq/sigma

## Sigma rules (the portable standard)

Vendor-agnostic YAML describing suspicious log behaviour; convert once to Splunk/
Sentinel/Elastic/etc with the converter. Mandatory anatomy:

- `title`, `id` (UUID), `status`, `description`, `author`, `references`, `date`.
- `logsource`: product/category/service (e.g. `category: process_creation`,
  `product: windows`). Wrong logsource = rule silently never fires.
- `detection`: one or more named selections + a `condition` combining them
  (`selection and not filter`). Build the _filter_ (known-benign) in from day one.
- `level` (informational→critical) and `tags` (`attack.tXXXX`, tactic). The tag
  is what drives coverage mapping, so never omit it.
- `falsepositives`: document them; an undocumented FP source is an un-tunable rule.

Write **behaviour**, not brittle IOCs: parent/child process chains, suspicious
command lines, LOLBin abuse > a single hash/IP (pyramid of pain: behaviour
detections survive, atomic IOCs churn). Import SigmaHQ's ~3000 rules as candidates,
but tune each to your environment before trusting it.

## ATT&CK coverage mapping (v20)

- Tag every detection with its technique id; aggregate into a heatmap (ATT&CK
  Navigator) to see covered vs blind techniques.
- ATT&CK v20 (Oct 2026) is current; the **Detection Strategies + Analytics** model
  that replaced Detections/Data Sources in v18 (Oct 2025) still holds: each
  Analytic names the platform-specific log source/data component to operationalize.
  Use them as the authoring blueprint. v19 (Apr 2026) split Defense Evasion into
  Stealth (TA0005) + Defense Impairment (TA0112); re-tag affected rules. v20 adds
  AI-focused/AI-enabled Enterprise techniques (e.g. prompt injection).
  verify: https://attack.mitre.org/resources/updates/updates-october-2026/
- **If you defend a plant, Enterprise ATT&CK is the wrong matrix.** ATT&CK for ICS
  is separate and carries two tactics with no Enterprise equivalent: **Impair
  Process Control (TA0106)** and **Inhibit Response Function (TA0107)**, the
  safety-blinding one. Coverage measured only against Enterprise reports green
  while both are unmonitored. `load_skill ot-threat-landscape`.
- Chase coverage _gaps that match your threat model_ (sector, actors, exposed
  tech), not raw technique count. 100% of the matrix is neither achievable nor the
  goal; high-fidelity coverage of likely TTPs is.
- Watch data-source dependency: a detection you can't feed is a paper rule; flag
  the missing telemetry to `load_skill siem-soar`.

## Testing detections (prove they fire)

- **Atomic Red Team** (Red Canary): ~1950 atomic tests mapped across the ATT&CK
  matrix; `Invoke-AtomicTest` runs one technique → confirm the detection
  fires + benign data stays quiet. The fast, granular unit test of a detection.
- **MITRE CALDERA**: autonomous adversary emulation (chained TTPs, C2, full
  scenarios) for end-to-end / breach-and-attack-simulation coverage validation.
  verify: https://github.com/redcanaryco/atomic-red-team
- Purple-team loop: red emulates the TTP → blue confirms detection → tune the
  miss → re-run. A detection with no executed test is unvalidated.
- Also test the **negatives**: replay normal-activity data and confirm the rule
  stays silent. That's the FP gate.

## Detect-tune lifecycle (control false positives)

- Every production rule carries an expected FP profile + a triage runbook. No
  runbook = don't ship (analysts can't action it).
- Tune order: build benign filters in → raise thresholds / add context (asset,
  user, change-window) → narrow logsource → deprecate dead rules.
- Beware rule decay: env/vendor-API/attacker drift silently breaks rules. Schedule
  a periodic detection audit: top-noise rules, never-fired rules (broken or
  truly-no-activity?), and rules whose data source went dark.
- Close the loop with `siem-soar`: SOAR auto-close + analyst close-codes (true/
  benign/FP) are the tuning telemetry that feeds the next revision.

## marq tie-in

marq is passive OSINT and runs no offensive technique. Validate detections with
your own emulation tooling (e.g. Atomic Red Team) and verify the detection would
catch it; YARA patterns can themselves be a host detection. `report_finding` any
technique that produced no alert as a detection gap; stage rule/log test data
under `/work` with the file tools.
