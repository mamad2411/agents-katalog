---
name: falco-configuration-validation
description: >
  Validates Falco runtime detection rules for false-positive rate and
  actual firing correctness before trusting them in a channel that pages
  a human — running new/changed rules in log-only mode against real
  traffic, measuring alert volume and content, and confirming a rule
  fires on a deliberate positive-control trigger before promoting it to
  a higher-severity, paging-routed configuration. Use when the user asks
  to "validate this Falco rule before enabling it," "why is Falco so
  noisy," "test our Falco rules don't false-positive on real traffic,"
  "review this rule set before it pages on-call," or "make sure Falco
  rules aren't about to be enabled in enforce/blocking mode without an
  audit period." Pairs with falco-runtime-threat-detection-configuration.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Falco Configuration Validation

## Purpose

A Falco rule that looks syntactically correct and conceptually sound —
"alert on any shell spawned in a container" — can still be a
production-alert-fatigue incident waiting to happen the moment it's
enabled broadly, if a CI runner, an init container, or a debugging
sidecar routinely spawns shells as part of completely normal operation.
Because Falco evaluates every syscall event in near real time, a rule
that's even slightly too broad doesn't fail quietly — it fires
constantly, and the practical consequence is either a flooded alert
channel that gets muted within days, or worse, an on-call rotation that
starts reflexively dismissing Falco pages as noise, which is exactly the
condition under which a real detection gets ignored. This skill covers
validating a Falco rule set's real-world false-positive rate *before*
trusting it in a paging-routed configuration: running new or changed
rules in a log-only/low-priority posture against genuine production
traffic for a representative period, measuring what actually fires and
why, and only then promoting a rule to a severity level that reaches a
human pager. It assumes the rules themselves are already written — see
[falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md)
for rule authoring — and is strictly about proving a rule set is safe
to depend on before it's live.

## When to use

- Before enabling any new custom Falco rule broadly, especially one
  whose `priority` is set to `WARNING` or higher (anything that could
  route to a paging destination).
- Before increasing a rule's priority (e.g. from `NOTICE` to
  `CRITICAL`) or its scope (from one namespace/workload to
  cluster-wide).
- After a Falco or Falco-rules-package version upgrade that changed
  stock rule conditions or added new default rules — an upgrade can
  silently make a previously-quiet stock rule noisy for your specific
  workloads.
- Investigating a spike in Falco alert volume to determine whether it
  reflects a real change in behavior (a genuine incident, a new
  deployment doing something unexpected) or a rule that was always
  slightly too broad and just started matching more traffic.
- Reviewing a rule set someone else wrote before it's trusted to page
  on-call, as a required gate rather than a courtesy review.
- Deciding whether a currently-noisy rule should be narrowed, given a
  workload-specific exception, or retired entirely as not worth the
  signal-to-noise ratio it produces.

## Prerequisites & environment

- A running Falco deployment already emitting events (see
  [falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md)
  for initial setup) with log/output access — either Falco's own pod
  logs, or wherever Falcosidekick routes events (a log aggregator, a
  SIEM) that can be queried for volume and content over a time window.
- A representative traffic window to validate against — ideally a full
  business cycle (a week, covering both weekday and weekend/off-hours
  patterns) rather than a few hours, since some legitimate but
  infrequent behavior (a weekly batch job, a monthly maintenance script)
  won't appear in a short window and would otherwise misfire the first
  time it runs after a rule goes live.
- The ability to deploy a rule change in a **non-alerting or
  low-priority posture first** — either by setting `priority: NOTICE`
  (or below the threshold Falcosidekick routes to paging) during the
  validation window, or by running a parallel Falco instance/rule file
  that logs but doesn't feed the production alert-routing pipeline.
- A way to trigger a deliberate, known-positive test case (e.g.
  `kubectl exec` a shell into a test pod, or a scripted equivalent of
  the specific behavior a rule targets) to confirm the rule actually
  fires — false-positive testing alone doesn't prove a rule works; it
  only proves it isn't overly broad.
- Basic scripting (`jq`, `grep`, or a small Python script) to summarize
  Falco JSON output by rule name, priority, and matching workload —
  manually reading a raw log stream for a week's worth of events doesn't
  scale past a handful of rules.

## Step-by-step guidance

1. **Deploy the new/changed rule in a validation posture, not
   production-alerting posture, first.** The simplest approach: keep the
   rule's `priority` field as authored but route it to a
   validation-only destination in Falcosidekick (or a separate log
   file), rather than the destination that would otherwise page:
   ```yaml
   # Falcosidekick config — validation window: cap outbound alerting
   # threshold above the new rule's priority until validation completes
   falcosidekick:
     config:
       pagerduty:
         routingkey: "${PAGERDUTY_ROUTING_KEY}"
         minimumpriority: "emergency"   # temporarily raised during validation
       slack:
         webhookurl: "${VALIDATION_SLACK_WEBHOOK_URL}"
         minimumpriority: "notice"      # everything, including the new rule, logged here for review
   ```
   > **Warning — enforce-without-audit risk:** enabling a new or
   > materially changed Falco rule directly at a priority that pages
   > on-call, with no prior observation window against real traffic, is
   > the single most common cause of Falco alert fatigue. Always run a
   > new rule through a log-only/validation posture first — there is no
   > "obviously safe, skip validation" case, because workload behavior
   > that looks obviously fine in code review routinely turns out to
   > include a legitimate but non-obvious pattern (a debug sidecar, an
   > init container, a CI runner) that only shows up in real traffic.

2. **Let the rule run for a representative period against real
   traffic** — a minimum of several days, ideally a full week including
   any weekly/off-hours batch jobs, before drawing conclusions:
   ```bash
   kubectl logs -n falco -l app.kubernetes.io/name=falco --since=168h \
     | jq -c 'select(.rule == "Shell spawned in payments-api")' \
     > validation_matches.jsonl
   wc -l validation_matches.jsonl
   ```

3. **Summarize matches by workload/context, not just raw count.** A
   count alone doesn't tell you whether 200 matches are 200 genuine
   incidents (extremely unlikely) or 200 instances of the same
   legitimate process triggering the rule:
   ```bash
   jq -r '.output_fields."k8s.pod.name" // .output_fields."container.image.repository"' \
     validation_matches.jsonl | sort | uniq -c | sort -rn
   ```
   ```
   187 ci-runner-7d9f8
     8 payments-api-6c4b9
     5 debug-toolbox-2f1a3
   ```
   This immediately tells a different story than the raw count: 187 of
   200 matches are one known, legitimate CI runner — a targeted
   exception for that workload, not abandoning the rule, is the correct
   fix (see the workflow in
   [falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md)'s
   tuning guidance).

4. **Distinguish "the rule matched something legitimate" from "the rule
   matched something genuinely suspicious that turned out to be
   benign-this-time."** The first calls for a permanent, documented
   exception; the second calls for leaving the rule as-is and treating
   this specific match as a one-off investigated incident, not evidence
   the rule itself is broken:
   ```
   187 matches, ci-runner-7d9f8, "sh -c npm install"  → legitimate, expected — exception warranted
     8 matches, payments-api-6c4b9, "sh"              → investigate each individually before assuming benign
   ```

5. **Confirm the rule still fires on a deliberate positive-control
   trigger** after any tuning — narrowing a condition to eliminate false
   positives can accidentally also eliminate true positives if the
   exception is too broad:
   ```bash
   kubectl exec -it test-pod -n payments -- /bin/sh
   kubectl logs -n falco -l app.kubernetes.io/name=falco --since=1m \
     | jq -c 'select(.rule == "Shell spawned in payments-api")'
   ```
   An empty result here after tuning is a **false negative** introduced
   by the fix — narrow the exception further (scope it to the exact
   known-legitimate process, not the whole namespace/image) rather than
   accepting the broader, now-blind version.

6. **Calculate and record a rough false-positive rate** as the concrete
   basis for the promote/hold decision, not a subjective "seems fine
   now":
   ```
   Total matches during validation window: 200
   Matches attributable to known-legitimate activity (post-exception): 0
   Matches requiring individual investigation: 8 (all resolved as benign,
     one-off developer debugging session with approval on record)
   False-positive rate after tuning: 0% over 7 days
   ```

7. **Promote to the intended priority/routing only after the validation
   window is clean** — patch the rule's `priority` (or move it from the
   validation-only Falcosidekick route to the production one) as an
   explicit, reviewed change, not an automatic timeout-based promotion:
   ```yaml
   - rule: Shell spawned in payments-api
     priority: CRITICAL   # promoted after 7-day clean validation window
   ```

8. **Re-validate after any Falco or rules-package upgrade** that
   touches a rule's stock condition, even if the custom overlay rules
   themselves didn't change — an upstream field-name or condition
   change can silently alter what a previously-tuned exception actually
   matches:
   ```bash
   falco --list 2>&1 | grep -A3 "Terminal shell in container"
   # confirm the rule's condition still references the same field names
   # your custom exception macros were written against
   ```

9. **Track validation history per rule** (when it was validated, over
   what window, what false-positive rate, who approved promotion) in
   version control alongside the rule file itself — a rule with no
   record of ever having been validated is a rule nobody can currently
   vouch for, regardless of how long it's been running.

## Best practices

- Never promote a new or materially changed rule directly to a
  paging-routed priority — always run it in a log-only or low-priority
  validation posture against real traffic first, for a period long
  enough to cover infrequent-but-legitimate patterns (a full week at
  minimum).
- Summarize validation-window matches by workload/process, not raw
  count — the fix for "187 matches from one CI runner" and "8 matches
  spread across 8 different unrelated workloads" is completely
  different, and a raw count alone can't distinguish them.
- Always re-confirm a rule still fires on a deliberate positive-control
  trigger after tuning it to eliminate false positives — an exception
  broad enough to silence noise is also broad enough to silence a real
  detection if scoped carelessly.
- Record a concrete false-positive rate and validation window as the
  basis for a promotion decision, not a subjective sense that "it seems
  quiet now."
- Re-run validation after any Falco/rules-package upgrade touching a
  rule's underlying condition, not just after changes to your own
  custom rule files.
- Keep validation history (dates, window length, false-positive rate,
  approver) in version control next to the rule definition, so "has
  this ever actually been validated" is answerable without relying on
  someone's memory.

## Common pitfalls

- **Symptom:** A new Falco rule is enabled directly at `CRITICAL`
  priority routed to PagerDuty, and within hours on-call is paged
  repeatedly for what turns out to be a completely routine CI pipeline
  step.
  **Fix:** This is the exact scenario the validation posture in step 1
  exists to prevent — roll the rule back to a log-only/low-priority
  posture, run the validation window properly (steps 2-6), add the
  necessary workload-specific exception, and only then re-promote.
  Treat "we'll validate it in production since it's urgent" as a false
  economy — the alert-fatigue cost of getting this wrong outweighs the
  few days a proper validation window costs.

- **Symptom:** After tuning a rule to stop matching a legitimate CI
  runner, a deliberate positive-control test (a real shell spawned in a
  different, unrelated pod) also stops firing.
  **Fix:** The exception was scoped too broadly — e.g. excluding an
  entire namespace or image repository instead of the specific
  process/command line that was actually the source of false positives.
  Narrow the exception to the minimum condition that eliminates the
  false positive (step 5) and re-run the positive-control test to
  confirm true-positive detection is intact before considering the fix
  complete.

- **Symptom:** A validation window run over a single quiet weekday
  shows zero false positives, the rule is promoted, and it starts
  paging constantly the following Monday.
  **Fix:** The validation window was too short to capture a real
  weekly/business-cycle pattern (e.g. a Monday-morning batch job, an
  end-of-month reconciliation script). Run validation over a period
  genuinely representative of the workload's full cycle — a week at
  minimum, longer if a known monthly/quarterly process exists that the
  rule could plausibly match.

- **Symptom:** Nobody can say when a currently-enabled, paging-capable
  rule was last validated, or whether it was ever validated against
  real traffic at all before being enabled.
  **Fix:** This is a process gap, not a one-off — require a recorded
  validation window and approver as part of the change that adds or
  modifies any rule at `WARNING` priority or above, tracked in the same
  version-controlled location as the rule file (step 9), so the answer
  is always retrievable from the repo rather than institutional memory.

- **Symptom:** After a routine Falco version upgrade, a previously
  well-tuned custom exception stops suppressing a stock rule's false
  positives, and alert volume spikes.
  **Fix:** The upgrade changed a field name or the stock rule's
  underlying condition in a way that no longer matches what the custom
  exception macro was written against. Re-validate (step 8) after every
  upgrade that touches rule definitions, not just after changes to
  custom rule files, and update the exception macro to match the new
  condition shape.

## Worked example

**Scenario:** The `Shell spawned in payments-api` custom rule from
[falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md)'s
worked example is proposed at `CRITICAL` priority, routed to PagerDuty.
Before promoting it, the security team runs it through a one-week
validation window.

Day 1 — deploy in validation posture (logged to a review-only Slack
channel, not PagerDuty):
```yaml
falcosidekick:
  config:
    slack:
      webhookurl: "${VALIDATION_SLACK_WEBHOOK_URL}"
      minimumpriority: "notice"
    pagerduty:
      minimumpriority: "emergency"   # new rule's CRITICAL priority intentionally held back
```

Day 7 — pull and summarize matches:
```bash
kubectl logs -n falco -l app.kubernetes.io/name=falco --since=168h \
  | jq -c 'select(.rule == "Shell spawned in payments-api")' > validation_matches.jsonl
jq -r '.output_fields."k8s.pod.name"' validation_matches.jsonl | sort | uniq -c | sort -rn
```
```
14 payments-api-debug-session-8f2a1
 2 payments-api-6c4b9
```

Investigation: `payments-api-debug-session-8f2a1` turns out to be a
temporary debugging pod a developer spun up (with an approved,
documented exception for a specific incident investigation) using the
same image but a different pod-name pattern — not the production
`payments-api` deployment the rule was actually meant to protect. The
other 2 matches are investigated individually and confirmed to be an
on-call engineer's authorized live debugging session during an
unrelated incident, also approved and logged.

Fix: narrow the rule's condition to the actual production deployment's
label rather than the whole image repository:
```yaml
- rule: Shell spawned in payments-api
  condition: >
    spawned_process and container
    and container.image.repository = "registry.example.internal/payments-api"
    and k8s.pod.label.app = "payments-api-prod"
    and proc.name in (shell_binaries)
  priority: CRITICAL
```

Positive-control re-test: `kubectl exec` into an actual
`payments-api-prod`-labeled pod confirms the rule still fires
immediately. A second week of validation with the narrowed condition
produces zero matches. The rule is promoted to route to PagerDuty, and
the validation record (window dates, 0% false-positive rate after
narrowing, approver) is committed alongside the rule file in the
security team's rules repository.

## Cross-references

- [falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md) —
  the rule-authoring skill this validation discipline is a required
  gate for; read that skill first for rule syntax and the underlying
  detection mechanics.
- [kubewarden-admission-policy-configuration](../kubewarden-admission-policy-configuration/SKILL.md) —
  a comparable audit-before-enforce rollout discipline applied to
  admission-time WASM policy rather than runtime syscall detection.
- [vault-configuration-validation](../vault-configuration-validation/SKILL.md) —
  the same "validate before it's trusted in production" philosophy
  applied to Vault policy/auth configuration instead of Falco rules.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) —
  the on-call load and alert-fatigue concerns this validation discipline
  directly protects against.
