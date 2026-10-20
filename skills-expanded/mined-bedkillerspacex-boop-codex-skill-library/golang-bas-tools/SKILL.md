---
name: golang-bas-tools
description: >
  Operate Breach and Attack Simulation (BAS) against Go estates: scoping,
  safe content packs, mapping to ATT&CK, and remediation loops. Authorized
  environments only.
---

# Golang BAS Tools

## Research grounding

Runbook for **Breach and Attack Simulation** tooling validating controls around
Go services (EDR, WAF, identity, CI)—continuous control testing, not open-ended
red team. Skill id: `golang-bas-tools`.

## Scope And Authorization

- **In scope:** environments with written BAS authorization and blast radius limits.
- **Out of scope:** running attack simulations on unauthorized networks.
- Prefer production-safe packs; no destructive payloads without explicit approval.
- Pair with `golang-attack-mapping`, `golang-blue-detect`, `code-quality-standards`.

## When To Use

- Validating detections for techniques relevant to Go API platforms.
- Continuous control assurance between pentests.
- Measuring cover after control changes.
- Focus tokens: **golang, bas, tools**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Manual ATT&CK mapping | `golang-attack-mapping` |
| Writing detections | `golang-blue-detect` |
| Full adversary emulation program | dedicated red-team process |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tools | Commercial BAS platforms and open control-test harnesses (org standard) |
| Content | Atomic tests mapped to techniques; safe variants |
| Go relevance | Token theft against APIs, webshell-like implants on app hosts (lab), CI abuse sims |
| Integration | Results → ticket → fix → retest |
| Safety | Allowlists, rate limits, kill switch |
| Pitfalls | Noisy false red; testing without SOC awareness |

## Workflow

### 1. Confirm scope and success criteria

1. Written authorization, targets, blackout windows, contacts.
2. Success: scheduled sims run; critical fails ticketed SLA; retest pass rate tracked.
3. Kill switch owner.

### 2. Inventory

1. Controls to validate (WAF, EDR, email, IdP, cloud).
2. Go services in path of simulations.
3. Existing BAS platform and content packs.

### 3. Baseline

1. Initial run; record pass/fail by technique.
2. Noise level to SOC (pages generated).

### 4. Operate

1. Select techniques from `golang-attack-mapping` priority gaps.
2. Run in staging first; then prod-safe subset.
3. For app-layer: only owned endpoints; respect rate limits (`golang-abuse-prevention`).
4. Export results with timestamps and control IDs.
5. Never store real customer PII in sim payloads.

### 5. Verify with evidence

1. Each failed control has ticket + owner.
2. After fix, retest same atomic ID.
3. Detection logs show expected alert for pass cases.

```bash
# If custom Go harness exists for control tests
go test ./internal/bas/... -count=1
```

### 6. Observe and harden

1. Dashboard: fail open age, flaky tests.
2. Update content when ATT&CK or architecture changes.
3. Coordinate with blue team to avoid alert fatigue (`golang-alert-fatigue`).

### 7. Hand off

1. Monthly BAS report to control owners.
2. Link fixes to engineering backlog.
3. Review authorization annually.

## Safety matrix

| Simulation class | Default env |
| --- | --- |
| Network port probes | Staging / scoped prod |
| Credential use | Synthetic accounts only |
| Destructive ransomware sim | Lab only unless explicitly approved |
| Phishing | Agreed user cohorts |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | Written scope | Surprise production BAS |
| Loop | Fail→fix→retest | Endless fails ignored |
| Safety | Kill switch | Unbounded packs |
| Topic fidelity | BAS for Go estates | Generic go test only |

## Output Checklist

- [ ] Authorization and kill switch documented
- [ ] Technique pack aligned to mapping priorities
- [ ] Staging then scoped prod runs
- [ ] Failures ticketed and retested
- [ ] SOC noise reviewed
- [ ] Metrics dashboard live
- [ ] `code-quality-standards` for any harness code

## Rules

- Authorized simulation only; safety first.
- Focus on `golang-bas-tools`.
- Synthetic identities; no real secret abuse.
- Coordinate with detection owners.
