---
name: golang-attack-trees
description: >
  Build attack trees for Go systems: root goals, AND/OR decompositions, likelihood
  and impact scoring, and mitigations. Use for threat modeling owned systems.
---

# Golang Attack Trees

## Research grounding

Runbook for **attack tree** construction and maintenance for Go services and
platforms—structured what-if analysis feeding controls and tests. Skill id:
`golang-attack-trees`.

## Scope And Authorization

- **In scope:** systems you own or are authorized to threat-model.
- **Out of scope:** planning crimes or attacks on unauthorized targets.
- Treat trees as sensitive; limit distribution of high-detail paths.
- Pair with `golang-attack-mapping`, `golang-authz-design`, `code-quality-standards`.

## When To Use

- Design reviews for new Go payment, identity, or admin features.
- Prioritizing mitigations with AND/OR path costs.
- Converting vague “secure it” into testable leaf mitigations.
- Focus tokens: **golang, attack, trees**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ATT&CK inventory coverage | `golang-attack-mapping` |
| Detection engineering | `golang-blue-detect` |
| AuthZ implementation | `golang-access-control` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Element | Guidance |
| --- | --- |
| Root | Attacker goal (steal tokens, corrupt ledger, ransomware data) |
| OR nodes | Alternative paths |
| AND nodes | All sub-steps required |
| Leaves | Concrete actions (phish admin, SQLi on Go handler, CI secret leak) |
| Attributes | Likelihood, cost, impact, detection difficulty |
| Mitigations | Control that breaks AND chain or raises cost |
| Go flavor | Handler authz, deserialization, SSRF via default HTTP client, supply chain |

## Workflow

### 1. Confirm scope and success criteria

1. System, trust boundaries, authorization, participants.
2. Success: tree reviewed; top paths mitigated or accepted; leaves mapped to tests/controls.
3. Timebox workshop (90–180 minutes).

### 2. Inventory

1. DFDs: users, Go services, data stores, CI, IdP.
2. High-value assets (keys, PII, money movement).
3. Existing controls.

### 3. Baseline

1. Choose 1–3 root goals max per session.
2. Note assumptions (attacker on Internet vs insider).

### 4. Build the tree

```text
Root: Exfiltrate all customer PII from Go API
├── OR Path A: Exploit API
│   ├── AND Find IDOR on /users/{id}
│   └── AND Bypass rate limit to enumerate
├── OR Path B: Compromise admin
│   ├── OR Steal session
│   └── OR Abuse debug endpoint pprof → memory
└── OR Path C: Supply chain
    ├── AND Malicious Go module
    └── AND Pipeline deploys without review
```

1. Be concrete: name routes, jobs, roles.
2. Score leaves (1–5 likelihood/impact) or use qualitative H/M/L.
3. Identify cheapest high-impact path (priority).
4. For each priority path, assign mitigation that removes a required AND node.
5. Link mitigations to code/config owners and verification tests.

### 5. Verify with evidence

1. Mitigations land with tests (`go test` authz/idor cases).
2. Re-walk tree: path cost increased or blocked.
3. Store versioned tree (markdown/drawio) with date.

```bash
go test ./internal/authz/... -count=1
go test ./... -count=1
```

### 6. Observe and harden

1. Update tree on major feature releases.
2. Feed residual paths to detection (`golang-blue-detect`).
3. Avoid tree rot—owner and review date required.

### 7. Hand off

1. Share summary (not always full leaf detail) with eng leads.
2. Backlog tickets linked to nodes.
3. Optional ATT&CK tags on leaves (`golang-attack-mapping`).

## Scoring sketch

| Path priority | Rule of thumb |
| --- | --- |
| P0 | High impact + low cost to attacker |
| P1 | High impact + medium cost |
| P2 | Medium impact or high cost |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Nodes | Specific Go routes/roles | Vague “hack the cloud” |
| Mitigations | Break AND with test proof | “Add AI security” |
| Scope | Timeboxed roots | Infinite enterprise tree day-1 |
| Topic fidelity | Attack trees for Go systems | Generic go test only |

## Output Checklist

- [ ] Roots and assumptions documented
- [ ] Tree with AND/OR structure
- [ ] Scores on priority paths
- [ ] Mitigations assigned with owners
- [ ] Verification tests planned/done
- [ ] Review date set
- [ ] `code-quality-standards` for related code fixes

## Rules

- Defensive threat modeling only.
- Focus on `golang-attack-trees`.
- Protect sensitive trees from public repos if needed.
- Evidence over fear-driven prioritization.
