---
name: falco-runtime-threat-detection-configuration
description: >
  Guides authoring and deploying Falco runtime threat detection rules —
  the eBPF/kernel-module-based syscall event stream, Falco's rule syntax
  (condition/output/priority), writing custom rules for a specific
  workload's known-good behavior, tuning noisy default rules, and
  wiring alerts to Falcosidekick outputs. Use when the user asks to
  "write a Falco rule to detect X," "why is Falco alerting on normal
  behavior," "detect a shell spawned inside a container at runtime,"
  "set up Falco with eBPF instead of the kernel module," "send Falco
  alerts to Slack/PagerDuty," or "what's the difference between Falco
  and admission-control policy engines like OPA/Kyverno." Pairs with
  falco-configuration-validation for pre-enforcement false-positive
  testing.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Falco Runtime Threat Detection Configuration

## Purpose

Admission-control policy engines (OPA/Gatekeeper, Kyverno, Kubewarden)
decide whether a resource is *allowed to be created* — they have no
visibility into what a container actually *does* once it's running.
Falco fills that gap: it taps the kernel's syscall event stream (via an
eBPF probe or, on older kernels, a kernel module) and evaluates every
event — a process exec, a file open, a network connection — against a
set of declarative rules in near real time, catching the class of
attack that only manifests at runtime: a reverse shell spawned inside a
container, an attacker reading `/etc/shadow` after already getting a
foothold, or an unexpected outbound connection from a workload that
should never make one. This skill covers Falco's rule syntax (`macro`,
`list`, `rule` with a `condition`/`output`/`priority`), writing rules
tailored to a specific workload's actual known-good behavior rather than
relying only on Falco's broad stock ruleset, tuning a rule that's
alerting on legitimate activity, and wiring detections to real
destinations via Falcosidekick. It does not cover the separate
discipline of proving a rule set won't misfire before enabling it in
blocking/enforce-adjacent configurations — see
[falco-configuration-validation](../falco-configuration-validation/SKILL.md)
for that pre-rollout testing discipline, which should be treated as a
required step before any new or changed rule goes live broadly.

## When to use

- Writing a new Falco rule to detect a specific runtime behavior — a
  shell spawned in a container, an unexpected outbound network
  connection, a sensitive file read/write, a container attempting to
  escape its namespace/mount privileges.
- Installing or upgrading Falco itself, and deciding between the eBPF
  probe (`modern_ebpf` driver, preferred on current kernels) and the
  legacy kernel module driver.
- Tuning an existing rule (stock or custom) that's generating excessive
  alerts for behavior that's actually normal for a given workload.
- Wiring Falco's alert output to a real destination (Slack, PagerDuty,
  a SIEM) via Falcosidekick, instead of leaving detections in a log file
  nobody watches.
- Explaining the difference between Falco (runtime/eBPF syscall
  detection) and admission-control policy engines like OPA/Gatekeeper,
  Kyverno, or Kubewarden — they solve different problems and are
  commonly run together, not as alternatives.
- Debugging why a Falco rule that should have fired for a known test
  case (e.g. a deliberate reverse-shell test) didn't produce any alert.

## Prerequisites & environment

- Falco ≥ 0.36 for the `modern_ebpf` driver as the default/recommended
  option (no kernel headers required, works across a wider range of
  managed Kubernetes node images than the older kernel-module driver) —
  confirm the installed version and driver before assuming a rule syntax
  feature (e.g. certain `evt.type` fields or `k8s.*`/`container.*`
  fields) is available; Falco's rule field set has grown across
  versions.
- A Kubernetes cluster (or bare VM fleet) with permission to run a
  privileged/host-level DaemonSet (Falco needs kernel-level visibility)
  — install via the official Helm chart for Kubernetes.
- Familiarity with Falco's **rules YAML** structure: `macro` (reusable
  named conditions), `list` (reusable value sets), and `rule`
  (`condition` + `output` + `priority` + `tags`) — this is closer to a
  domain-specific filter expression language than a general-purpose one,
  and most authoring time goes into getting `condition` field paths
  right.
- **Falcosidekick** (or an equivalent alert router) if alerts need to
  reach Slack, PagerDuty, a SIEM, or anywhere beyond Falco's own
  stdout/log output — install and configure this before assuming
  detections are actually being seen by anyone.
- Access to representative workload behavior (a staging environment
  running real traffic patterns, or a documented list of a workload's
  legitimate process/network behavior) to write rules against — a rule
  written purely from imagination about what "shouldn't happen" reliably
  either under- or over-matches real behavior.
- A rollout discipline: **every new or materially changed rule should be
  validated for false-positive rate before being treated as
  alert-worthy in a channel that pages anyone** — see
  [falco-configuration-validation](../falco-configuration-validation/SKILL.md).
  Skipping this is the most common cause of alert fatigue that gets
  Falco itself muted or ignored within weeks of rollout.

## Step-by-step guidance

1. **Understand the rule anatomy** before writing anything custom — a
   `rule` combines a `condition` (a boolean filter expression over
   syscall/container/k8s fields), an `output` (the alert message
   template), and a `priority`:
   ```yaml
   - rule: Terminal shell in container
     desc: A shell was spawned inside a container by a non-interactive process
     condition: >
       spawned_process and container
       and shell_procs and proc.tty != 0
       and container_entrypoint
       and not user_expected_terminal_shell_in_container_conditions
     output: >
       A shell was spawned in a container with an attached terminal
       (user=%user.name user_loginuid=%user.loginuid %container.info
       shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline
       terminal=%proc.tty container_id=%container.id image=%container.image.repository)
     priority: NOTICE
     tags: [container, shell, mitre_execution]
   ```
   This is Falco's own stock rule for detecting an interactive shell —
   study stock rules before writing new ones from scratch, since most
   custom needs are a narrower/workload-specific variant of an existing
   pattern.

2. **Write a workload-specific rule from known-good behavior**, not from
   guessing at attacker behavior in the abstract. For a workload that
   should *never* spawn a shell or make outbound connections other than
   to its known dependencies:
   ```yaml
   - list: payments_api_allowed_outbound_ips
     items: [10.0.4.10, 10.0.4.11]   # known DB/cache endpoints only

   - rule: Unexpected outbound connection from payments-api
     desc: payments-api should only ever connect to its known DB/cache — anything else is suspicious
     condition: >
       outbound and container.image.repository = "registry.example.internal/payments-api"
       and not fd.sip in (payments_api_allowed_outbound_ips)
     output: >
       Unexpected outbound connection from payments-api
       (command=%proc.cmdline connection=%fd.name container_id=%container.id
       image=%container.image.repository)
     priority: WARNING
     tags: [network, payments]
   ```
   A workload-scoped allowlist rule like this catches real exfiltration/
   C2 attempts far more reliably than a broad, generic "unexpected
   network connection" rule tuned to avoid false positives across every
   workload in the cluster at once.

3. **Use macros and lists to keep rules maintainable**, rather than
   repeating the same condition fragment across many rules:
   ```yaml
   - macro: container_entrypoint
     condition: (proc.vpid=1 or proc.vpid=proc.pid)

   - list: shell_binaries
     items: [sh, bash, csh, ksh, zsh, dash]
   ```
   When several rules need "is this a shell process," reference
   `proc.name in (shell_binaries)` rather than duplicating the literal
   list in each rule — a shell binary added to one rule's list but
   missed in another is a common source of an inconsistent detection
   surface.

4. **Tune a noisy stock rule by narrowing its condition or adding an
   explicit exception**, rather than disabling it outright:
   ```yaml
   # Stock rule fires on a legitimate CI runner's normal package-install shell
   - macro: user_expected_terminal_shell_in_container_conditions
     condition: >
       (container.image.repository = "registry.example.internal/ci-runner"
        and proc.pname = "entrypoint.sh")
   ```
   Falco's stock ruleset ships extension macros (like
   `user_expected_terminal_shell_in_container_conditions` above)
   specifically so exceptions can be layered in a separate, overridable
   file rather than editing the stock rule file directly — always
   extend through this pattern (or an equivalent override file) so
   upstream rule updates don't silently clobber a hand-edited stock
   rule.

5. **Choose the eBPF driver over the legacy kernel module** for new
   installs, verifying it loads correctly on the target node image:
   ```yaml
   # values.yaml (Helm)
   driver:
     kind: modern_ebpf
   ```
   ```bash
   helm install falco falcosecurity/falco \
     --namespace falco --create-namespace \
     -f values.yaml
   kubectl logs -n falco -l app.kubernetes.io/name=falco | grep -i "driver"
   ```
   Fall back to the kernel-module driver only on kernels too old for
   the eBPF probe, and track that as a node-image upgrade item rather
   than a permanent state.

6. **Wire alerts to Falcosidekick and a real destination**, not just
   Falco's stdout:
   ```yaml
   # falcosidekick config (Helm values, illustrative)
   falcosidekick:
     enabled: true
     config:
       slack:
         webhookurl: "${SLACK_WEBHOOK_URL}"
         minimumpriority: "warning"
       pagerduty:
         routingkey: "${PAGERDUTY_ROUTING_KEY}"
         minimumpriority: "critical"
   ```
   Route only `critical`-and-above priority to paging (PagerDuty/
   Opsgenie); route `warning`/`notice` to a monitored Slack channel or a
   SIEM, so on-call isn't paged for every `NOTICE`-level detection.

7. **Test a new rule against a deliberate, controlled trigger** before
   trusting it's live:
   ```bash
   # deliberately trigger the "Terminal shell in container" rule in a test pod
   kubectl exec -it test-pod -- /bin/sh
   kubectl logs -n falco -l app.kubernetes.io/name=falco --since=1m | grep -i "shell was spawned"
   ```
   Confirm the exact expected output line appears — a rule with a typo'd
   field path can pass Falco's YAML/syntax validation and still never
   actually fire, identically to the false-negative failure mode common
   in Rego/Kyverno admission policies.

8. **Layer application-context enrichment** (Kubernetes metadata, image
   provenance) into the `output` template so an alert is actionable
   without a separate lookup:
   ```yaml
   output: >
     Unexpected shell (user=%user.name command=%proc.cmdline
     %container.info k8s.ns=%k8s.ns.name k8s.pod=%k8s.pod.name
     image=%container.image.repository:%container.image.tag)
   ```
   An alert with only a container ID and no namespace/pod/image
   forces whoever's on call to run a separate `kubectl` lookup before
   they can even start triaging — put the context in the alert itself.

## Best practices

- Write workload-specific rules from documented known-good behavior
  (specific allowed outbound endpoints, expected process trees) rather
  than one broad "detect anything unusual" rule tuned to be quiet across
  every workload at once — narrow rules catch more real threats with
  fewer false positives.
- Extend stock rules via their designated override macros/exception
  files rather than editing the stock rule YAML directly, so upstream
  Falco updates don't silently overwrite a hand-tuned exception.
- Route alert severity to destination deliberately — only `critical`
  (or `emergency`) priority should page a human; lower-priority
  detections belong in a monitored channel or SIEM, not the same pager
  rotation.
- Prefer the `modern_ebpf` driver for new installs; track any remaining
  kernel-module-driver nodes as a node-image-upgrade backlog item, not a
  permanent state.
- Test every new/changed rule against a deliberate trigger before
  trusting it — a rule that passes YAML validation but has a typo'd
  field path silently never fires, which is worse than no rule at all
  because it creates false confidence.
- Never enable a new or materially changed rule broadly without first
  running it through the false-positive validation discipline in
  [falco-configuration-validation](../falco-configuration-validation/SKILL.md)
  — a noisy new rule that pages on-call for legitimate activity is how
  Falco itself earns a reputation for being safely ignorable.
- Enrich alert `output` templates with Kubernetes/image context so
  triage doesn't require a separate lookup step under pressure.

## Common pitfalls

- **Symptom:** A new custom rule is deployed and immediately generates
  dozens of alerts per minute for what turns out to be entirely
  legitimate, routine workload behavior.
  **Fix:** This is exactly the failure mode
  [falco-configuration-validation](../falco-configuration-validation/SKILL.md)
  exists to catch before enabling a rule broadly — run it in a
  log-only/low-priority mode against real traffic first, review the
  volume and content of what it matches, then narrow the condition
  (often by adding a workload-specific allowlist, as in step 2) before
  routing it to a channel anyone is paged from.

- **Symptom:** A deliberate test (spawning a shell in a container that
  should trigger the stock "Terminal shell in container" rule) produces
  no alert at all.
  **Fix:** Check the rule is actually loaded (`falco --list` or
  inspecting the running config) and that no override macro
  unintentionally excludes the test pod's image/namespace — a broadly-
  scoped exception macro added for one legitimate case can silently
  suppress detection for everything matching its condition, not just
  the intended exception.

- **Symptom:** A hand-edited stock rule file works fine until the next
  Falco/rules-package upgrade, after which the tuning is gone and the
  noisy behavior returns.
  **Fix:** Never edit the shipped stock rules file directly for tuning —
  use the designated override-macro pattern (step 4) or a separate
  custom rules file loaded alongside the stock one, so upgrades replace
  only the stock file and leave custom overrides intact.

- **Symptom:** Falco is running and clearly detecting events (visible in
  its own pod logs), but no one on the security or on-call team has ever
  actually seen an alert.
  **Fix:** Falcosidekick (or an equivalent router) either isn't
  installed or isn't configured with a real destination — Falco's
  default output is its own log stream, which is not equivalent to
  alerting. Wire Falcosidekick to at least one monitored destination
  (step 6) and verify with a deliberate test trigger that the alert
  actually arrives there.

- **Symptom:** The Falco DaemonSet fails to start on a subset of nodes,
  or falls back silently to degraded detection.
  **Fix:** Usually a driver/kernel mismatch — confirm the `modern_ebpf`
  driver is compatible with the node's kernel version (check Falco pod
  logs for driver-load errors) and either update the node image or fall
  back explicitly to the kernel-module driver for that node pool while
  tracking the underlying kernel upgrade, rather than leaving affected
  nodes with no working detection unnoticed.

## Worked example

**Scenario:** `payments-api` handles card data and should never spawn a
shell or connect outbound to anything but its known database and cache
endpoints. Detect both classes of deviation and route only high-
confidence, high-severity detections to PagerDuty.

Custom rules (`falco-rules-payments.yaml`):
```yaml
- list: payments_api_allowed_outbound_ips
  items: [10.0.4.10, 10.0.4.11]

- rule: Shell spawned in payments-api
  desc: payments-api should never spawn an interactive shell
  condition: >
    spawned_process and container
    and container.image.repository = "registry.example.internal/payments-api"
    and proc.name in (shell_binaries)
  output: >
    Shell spawned inside payments-api (user=%user.name command=%proc.cmdline
    parent=%proc.pname k8s.pod=%k8s.pod.name image=%container.image.repository)
  priority: CRITICAL
  tags: [container, shell, payments, mitre_execution]

- rule: Unexpected outbound connection from payments-api
  desc: payments-api should only connect to its known DB/cache endpoints
  condition: >
    outbound and container.image.repository = "registry.example.internal/payments-api"
    and not fd.sip in (payments_api_allowed_outbound_ips)
  output: >
    Unexpected outbound connection from payments-api
    (connection=%fd.name k8s.pod=%k8s.pod.name image=%container.image.repository)
  priority: CRITICAL
  tags: [network, payments, mitre_exfiltration]
```

Falcosidekick routing (only `critical` pages, everything routes to a
monitored Slack channel too):
```yaml
falcosidekick:
  config:
    slack:
      webhookurl: "${SLACK_WEBHOOK_URL}"
      minimumpriority: "warning"
    pagerduty:
      routingkey: "${PAGERDUTY_ROUTING_KEY}"
      minimumpriority: "critical"
```

Validation before rollout (per
[falco-configuration-validation](../falco-configuration-validation/SKILL.md)):
the rule set runs for one week in log-only mode against real
`payments-api` traffic, producing zero false-positive shell or outbound
alerts (confirming the allowlist and shell-binary list are complete),
before being promoted to page on-call via PagerDuty. A deliberate test —
`kubectl exec` into a `payments-api` pod and running `sh` — confirms the
`CRITICAL` alert fires and reaches PagerDuty within seconds, with the
pod name and image already in the alert body so the paged responder
doesn't need a separate lookup to start triage.

## Cross-references

- [falco-configuration-validation](../falco-configuration-validation/SKILL.md) —
  the required false-positive-testing discipline before any new or
  changed rule from this skill is trusted to page a human.
- [kubewarden-admission-policy-configuration](../kubewarden-admission-policy-configuration/SKILL.md) —
  admission-time policy enforcement, complementary to (not a substitute
  for) Falco's runtime detection; a resource can pass admission and
  still misbehave at runtime, which is exactly what Falco catches.
- [sysdig-secure-runtime-security](../sysdig-secure-runtime-security/SKILL.md) —
  a commercial runtime-security platform built on the same underlying
  detection concepts (Sysdig originated Falco), for teams wanting a
  managed alternative to self-hosting the OSS Falco stack.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) —
  the incident process a `critical`-priority Falco detection routed to
  paging should feed into.
