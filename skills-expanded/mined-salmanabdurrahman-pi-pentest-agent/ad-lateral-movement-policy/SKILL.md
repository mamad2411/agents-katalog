---
name: ad-lateral-movement-policy
description: Policy-only boundary for lateral movement requests — scope requirements, safer alternatives, explicit unlock refusal, and blue-team handoff. No active runbook.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [policy-note, approval-record]
disabled-category: persistence
---

# Lateral movement policy — gate and alternatives

Use this skill to evaluate whether a requested lateral movement activity meets the product authorization, scope, consent, and risk gates. This skill is a decision framework, not an execution runbook. It provides safer alternatives, explicit refusal language, and blue-team coordination guidance. If all gates are satisfied, it defines the minimum evidence and constraints for approved active validation — but it never provides command sequences, payload recipes, or operational steps.

## Required inputs

- Written scope explicitly naming each source host, destination host, identity (account/hash/ticket), technique family, time window, blast-radius limit, detection contact, and business owner.
- Repo config unlock for `persistence` disabled-default category.
- Per-engagement consent with aggressive/destructive risk approval.
- Valid authorization cache covering source and destination assets.
- Rollback plan and detection/escalation contact active during the approved window.

## Required gates

1. Repo config unlock for disabled-default category (`persistence`) via `pentest_agent_validate_policy`.
2. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
3. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for every source and destination.
4. `pentest_agent_check_authorization` for every asset pair.
5. Approval for aggressive/destructive risk on the specific technique.
6. No raw shell. If active validation is approved, all execution must go through `pentest_agent_execute_tool`.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Policy framework — gate checklist

Before any lateral movement activity, all of the following must be true:

### Scope gate
- [ ] Each source host (hostname, IP) is named in scope.
- [ ] Each destination host (hostname, IP) is named in scope.
- [ ] The technique family (WMI, WinRM, SMB, SSH, PSExec, scheduled task, service creation) is explicitly listed in scope as allowed.
- [ ] The identity used for authentication (account name, hash reference, ticket reference) is listed in scope.
- [ ] Time window, rate limits, and blast-radius limit are documented.
- [ ] No out-of-scope hosts, domains, forests, VLANs, or network segments are reachable through the planned movement.

### Authorization gate
- [ ] Valid authorization cache exists for every source-destination pair.
- [ ] Cache is not expired.
- [ ] Proof metadata covers lateral movement activity explicitly.
- [ ] Per-engagement consent has been recorded for this specific movement chain.

### Risk gate
- [ ] The technique risk class (aggressive/destructive) has been approved.
- [ ] Disabled-default category `persistence` is unlocked in repo config.
- [ ] If credential material (hash, ticket, key) is used, it was obtained through separately authorized means.
- [ ] No privilege escalation beyond the approved identity scope.

### Operational gate
- [ ] Detection/escalation contact has been notified of the planned activity window.
- [ ] Rollback plan exists: what to do if the movement causes service disruption, account lockout, or alert storm.
- [ ] Evidence capture plan: what will be recorded, what will be redacted, where it will be stored.
- [ ] Stop authority: who can abort the activity and how they will communicate the abort.

## Safer alternatives — offer first

When any gate is not satisfied, offer these safer alternatives before considering approval:

### Tabletop path review
Walk through the intended movement path on paper/whiteboard with the operation team. Identify:
- Which ACLs, delegations, or group memberships enable each hop.
- What detection rules would fire at each step.
- What the remediation would be for each enabler found.

This produces the same architectural insight as active movement, without touching a live system.

### Offline config audit
Export relevant AD/LDAP data, firewall rules, GPO settings, and host configurations through read-only means. Review for:
- Excessive local admin group memberships.
- Open SMB/WinRM/RDP from source to destination networks.
- Weak service account permissions enabling lateral movement.
- Missing network segmentation between tiers.

### Detection validation
Deploy detection rules for the intended technique family in the SIEM first. Run a tabletop simulation or benign canary test to verify detection fires. This confirms the defensive posture without actual lateral movement.

### Privilege path documentation
Map the BloodHound/AD attack graph to document privilege paths. This provides the same architectural understanding without moving laterally.

### Blue-team handoff
Package all identified paths, enablers, and detection gaps into a remediation report for the defensive team. Let them close the paths rather than exercising them.

## When all gates are satisfied — minimum constraints

If lateral movement is approved after all gates pass, these minimum constraints apply:

1. **One-hop limit**: validate only one source→destination hop per approval window. Chain validation requires separate approval for each hop.
2. **Read-only first**: first command on destination must be a read-only status check (`whoami`, `hostname`, `ipconfig`). No write, dump, or lateral jump until that hop is confirmed and re-authorized.
3. **No credential capture**: do not dump SAM, LSASS, NTDS, DPAPI, or browser credential stores during movement validation.
4. **No persistence**: do not create scheduled tasks, services, registry keys, startup items, WMI subscriptions, or user accounts on destination.
5. **No relay or coercion**: do not use NTLM relay, coercion (PrinterBug, PetitPotam), or token manipulation to gain access.
6. **Immediate evidence redaction**: all command output must be redacted before storage. Hostnames, IPs, usernames, and domains redacted unless scope allows.
7. **Time-boxed**: each hop validation must complete within the approved time window. Auto-abort at window end.
8. **Rollback**: revert any state change (file, service, registry key, account) created during validation.

## Decision points

- **Scope gate fails on any checklist item → refuse**: even if other gates pass, a single scope gap (unnamed host, disallowed technique) blocks the entire request. Offer safer alternatives.
- **Authorization cache expired or missing for any source-destination pair → refuse**: lateral movement requires fresh authorization per asset pair. Redirect to `pentest-agent-authorization`.
- **Technique requires disabled-default category unlock → maintainer decision**: if `persistence` category is not unlocked in repo config, the request cannot proceed regardless of per-engagement consent.
- **Detection contact unavailable or window denied → refuse**: operational gate is hard-block. No lateral movement without active monitoring and stop authority.
- **Credential material was obtained outside separately authorized means → refuse**: lateral movement validation must not launder credentials from unauthorized collection.
- **All four gates pass + aggressive risk approved → approve with one-hop limit**: document minimum constraints, evidence plan, and rollback procedure. Operator must confirm each hop.
- **Tabletop review produces same architectural insight → prefer**: when the goal is understanding privilege paths, a whiteboard walkthrough with BloodHound data achieves the same outcome safely.

## Prohibited behavior

- Lateral movement without all gates satisfied.
- Credential reuse, token theft, coercion, relay, password spraying, secret dumping, file/service modification.
- Using production credentials or accessing user data without exact written authorization.
- Turning this policy review into execution steps.
- Providing command sequences, tool invocation examples, payload recipes, or operational runbooks.
- Persistence, backdoor creation, privilege escalation, or exfiltration.

## Stop conditions

- Any gate in the checklist is not satisfied → refuse, offer alternatives.
- Scope lacks exact source/destination/identity → refuse.
- Detection contact unavailable during planned window → refuse.
- Activity could alter availability or data → refuse.
- Next step requires credential attack, cracking, or exploitation beyond approved movement → stop.

## Evidence

Record the policy decision, not the movement activity:

```text
Request: <source description> → <destination description>
Technique family: <WMI | WinRM | SMB | SSH | ...>
Gate status:
  Scope gate: <passed | failed — reason>
  Authorization gate: <passed | failed — reason>
  Risk gate: <passed | failed — reason>
  Operational gate: <passed | failed — reason>
Decision: <approved with constraints | refused>
Safer alternative offered: <tabletop review | config audit | detection validation | blue-team handoff>
```

Never store: hostnames, IPs, account names, hashes, tickets, keys, or network topology unless scope explicitly allows.

## Report handoff

1. Document the gate decision and rationale.
2. If refused, package the safer alternative findings (config gaps, detection coverage, privilege paths) for the blue/remediation team.
3. If approved, record the minimum constraint checklist, time window, and evidence redaction plan.
4. Recommend: network segmentation improvements, local admin group hygiene, detection rule deployment for lateral movement techniques, and privilege path remediation.
