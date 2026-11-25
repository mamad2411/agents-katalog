---
name: alert-tuning
description: SOC alert-tuning workflow — false-positive reduction via targeted suppressions (rule-id + reason + expiry), baseline learning, rule retirement, severity recalibration, and metrics (alert volume, mean-time-to-triage, fatigue index). Prevents detection collapse without losing coverage.
---

# Alert Tuning

> **Discipline balance**: too little tuning = analyst fatigue + missed real alerts in the flood. Too much tuning = silent failure where your rules detect nothing but no one notices. Suppressions always with rule-id + reason + expiry, never wildcard-permanent. Periodic review required.

## When to use

A SOC that does not tune drowns in alerts. A SOC that tunes too aggressively misses incidents. This skill is the discipline between those two.

Triggers on:

- A question like "we have 5000 alerts per day, how do we get fewer", "how do we suppress this rule cleanly", "rule X never fires now, is that right", "review our tuning stack".
- A baseline measurement before putting a new rule into production (see `detection-engineer` phase 4).
- A periodic (quarterly) review cycle of active rules.
- A handoff from `detection-engineer` (rule with too high an FP rate needs tuning).
- A SOC MTTR measurement where tuning action has been identified as the root cause.

### When NOT (handoff)

- Writing a new rule → `detection-engineer`. This skill works on existing rules.
- Triage of a specific alert in real time → `log-triage`, `siem-query`. This skill is at rule level, not alert instance.
- IOC feed curation → `ioc-hunter`.
- Threat hunt to find undetected TTPs → `threat-hunt` (command).
- Detection-coverage mapping → `detection-engineer` or DeTT&CT.

## Approach

Six phases. Phase 1 (volume triage) is always the starting point; phase 5 (lifecycle discipline) is what saves an existing tuning stack from slow rot.

### 1. Volume triage and hot list

Start with data, not opinions.

- **Top-N rules by alert volume**: last 30 days, ranked. 80/20 distribution: typically 10–20% of rules produce 80% of alerts.
- **Mean time to triage per rule**: how long does it take for an analyst to reach a conclusion? High MTT plus high volume = pain point.
- **True-positive rate per rule** (where tracked): TP / (TP + FP). Below 5% TP rate = strong tuning candidate.
- **Analyst-fatigue signal**: alerts with "snooze" actions, alerts not picked up within SLA, alerts closed with copy-paste comments.

Output: a hot list of rules with disproportionate volume or poor conversion to incidents. Top 10 for this cycle.

### 2. FP-pattern identification per hot rule

Per rule on the hot list: what causes the FPs? Not "too aggressive" — specifically which pattern.

Common FP categories:

- **Legitimate process / user / system**: backup tools, AV scanners, deployment pipelines, monitoring agents, scheduled health checks.
- **Geographic / time-based legitimate**: travel-pattern trigger on a global team, normal after-hours work in a 24/7 team.
- **Stale config**: rule for a specific attack pattern that has since been remediated internally, leaving only the noisy FP share.
- **Schema drift**: log source has new field values, rule matches old values — every new event triggers as "rare" while it is normal.
- **Threshold too tight**: rule fires at N=3 while the baseline already regularly sees N=4.

Per FP category, a course of action (see phase 3).

### 3. Suppression discipline

Not all FPs are solved with suppression — some with rule refactor. This is the choice.

**Suppression appropriate** if:

- The FP comes from a specific, identifiable source (one service account, one range).
- The legitimate activity is too diverse to capture in rule conditions.
- The rule remains substantively valid for other sources.

**Refactor the rule** if:

- The FP comes from a fundamental design flaw in the detection logic.
- The rule is outdated for the current threat pattern.
- The suppression list would grow unsustainably large.

**Suppression format** (consistent across rules):

```yaml
suppression:
  rule_id: T1003-001-LSASS-Access
  match:
    SourceImage: '\windows\system32\msmpeng.exe'
  reason: "Microsoft Defender Antimalware Service legitimate LSASS access"
  added_by: <analyst-name>
  added_date: YYYY-MM-DD
  expires: YYYY-MM-DD     # 6 months default
  evidence_link: <ticket / wiki>
```

**Forbidden patterns**:

- `match: '*'` or no match criteria (suppress-all).
- No reason filled in.
- No expiry filled in.
- Suppression on rule-id global instead of event-specific.

A suppression without all of these fields = an audit finding at the next review.

### 4. Baseline learning and threshold recalibration

For frequency-based and anomaly-based rules:

- **Rolling baseline** (last N days) for "what is normal here". Updates weekly or monthly; too-fast updates can absorb an attack pattern into the baseline.
- **Threshold adjustment based on baseline distribution**: percentile-based (alert when >P99 on metric X) rather than fixed numbers.
- **Per-segment baselines**: admin accounts have a different baseline from service accounts and from end users. One rule applying the same threshold to all three is a guaranteed FP source.
- **Time-of-day and day-of-week segmentation** where relevant (e.g. weekend work vs. weekday).

Anti-pattern: a baseline so wide-net-fitted that a real attack fits comfortably inside "normal".

### 5. Rule lifecycle: retirement, refresh, retire

Rules age. Discipline to maintain the stack:

- **Retire**: rule with no TP for N months (default 6) + threat pattern is outdated or now better covered by another rule. Remove from production, archive in the detection-as-code repo for reference.
- **Refresh**: rule that does have TPs but has grown a large tuning stack. Rewrite based on the current baseline and threat pattern.
- **Retain**: rule stays, with current tuning, until the next review.
- **Promote**: experimental rule with a good TP rate to production severity.
- **Demote**: rule with too many FPs and a low TP rate to a lower severity level (informational), not retired right away — sometimes it still provides hunting context.

Quarterly cycle: walk all rules through these four actions. Default: retain. But every retain must be explicitly documented ("FP rate stable, 12 TPs in the last quarter").

### 6. Metrics and verification-loop

Track which metrics gauge your tuning effectiveness:

- **Alert volume per day/week** (target: stable or falling, no unexpected spikes).
- **TP rate per rule** (target: > 10% high severity, > 5% medium).
- **Mean time to triage (MTT)** (target: getting shorter).
- **Fatigue index** (self-reported by analysts or computed from acceptance rate of alert actions).
- **Coverage regression**: is your ATT&CK coverage dropping because you retire rules without replacement? Track via DeTT&CT.
- **Suppression cardinality**: how many active suppressions per rule? Above N=10 is a signal that the rule itself needs to be fixed.
- **Suppression expiry compliance**: % of suppressions still within validity (target: > 95%; the rest re-evaluate or expired-removed).

**Verification-loop**:

Layer 1: scope (all hot rules addressed this cycle?), assumptions (FP categories supported by data, not anecdote?), gaps (suppressions have expiry + reason + evidence link?). Layer 2: TP/FP figures from the source of truth (the SOC platform), not summarized memory; ATT&CK coverage claims via tool report; no invented baseline percentiles.

## Output

```
Alert-tuning report — <SOC / org>
Period: <start → end>
Reviewer: <name + role>

Volume triage (top 10 hot rules):
  Rule | Alert vol | MTT | TP rate | Actions

Per hot rule:
  Rule-ID:           <id>
  FP pattern:        <category>
  Decision:          <suppress / refactor / retire / refresh>
  Implementation:    <suppression yaml / refactor PR link / retirement ticket>
  Expected impact:   <volume-reduction %, FP-rate target>

Suppression-stack status:
  Total active:         N
  Per rule (top N):     average M
  Expired / re-eval:    N (handled this cycle)
  Forbidden patterns:   <0 or list, with fix action>

Baseline recalibration:
  Rules with updated thresholds: N
  Per-segment baselines added:   <list>

Lifecycle actions this cycle:
  Retire:   <N rules>
  Refresh:  <N rules>
  Promote:  <N>
  Demote:   <N>
  Retain:   <N (default)>

Coverage impact (DeTT&CT or equivalent):
  ATT&CK techniques covered now:        <%>
  Shifts since last quarter:            <increase/decrease>

Metrics:
  Alert-volume trend:        <chart ref>
  TP-rate trend:             <per severity>
  MTT trend:                 <minutes>
  Fatigue index:             <score>

Verification-loop: ...
```

## References

- **NIST SP 800-92** — [https://csrc.nist.gov/pubs/sp/800/92/final](https://csrc.nist.gov/pubs/sp/800/92/final). Guide to Computer Security Log Management; baseline layer.
- **MITRE D3FEND** — [https://d3fend.mitre.org/](https://d3fend.mitre.org/). Defensive counter-mappings.
- **DeTT&CT** — [https://github.com/rabobank-cdc/DeTTECT](https://github.com/rabobank-cdc/DeTTECT). Coverage tracking and data-source mapping. NL source (Rabobank CDC).
- **Sigma project** — [https://github.com/SigmaHQ/sigma](https://github.com/SigmaHQ/sigma). The `falsepositives` field is built-in tuning discipline.
- **MITRE ATT&CK Navigator** — [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/). Visual coverage mapping.
- **SANS — Detection Engineering Maturity Model** — [https://www.sans.org/](https://www.sans.org/). Maturity rubric for team maturity.
- **Florian Roth — Sigma rules best practices** — [https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide). Practical tuning advice from the project maintainer.

## Categories

- blue
