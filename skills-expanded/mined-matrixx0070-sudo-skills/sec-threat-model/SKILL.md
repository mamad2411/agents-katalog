---
name: sec-threat-model
version: 1.0.0
description: Build a STRIDE-based threat model and attack-surface map for a feature or system so risks can be mitigated before they ship.
author: matrixx0070
tags: [security, threat-modeling, stride, attack-surface, risk, defensive]
capabilities: []
---

## When to use

Use this when you are designing a new feature, reviewing an existing system, or preparing a security sign-off and need a structured view of what could go wrong. You enumerate risks so they can be mitigated.

**Not for:** writing exploit code or proof-of-concept attacks; penetration testing a live system; or replacing a full code audit (use `sec-code-audit` for line-level review). Model the design, not the attacker's toolkit.

## Method

1. **Define scope.** Name the system, its trust boundaries, actors (users, admins, services, third parties), and the assets worth protecting (data, credentials, availability).
2. **Draw the data flow.** List entry points, processes, data stores, and external dependencies. Mark every trust boundary a request crosses. *Decision point:* if a flow never crosses a boundary and touches no asset, drop it — do not model noise.
3. **Apply STRIDE per element.** For each component ask: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Record concrete, plausible threats only.
4. **Rate risk.** Score each threat by likelihood x impact (High/Medium/Low). Note existing controls. *Decision point:* if a control already fully covers a threat, mark it Mitigated and move on.
5. **Propose mitigations.** Map each unaddressed High/Medium threat to a specific control (authn, input validation, encryption, rate limiting, least privilege, logging).
6. **Flag residual risk.** State what remains unmitigated and who must accept it.

## Example

Feature: a file-upload endpoint. Element = upload handler crossing the internet → app boundary. STRIDE hit: **Tampering** — a client sends a crafted filename `../../etc/passwd`. Likelihood High x Impact High. Existing control: none. Mitigation: canonicalize the path, allow-list extensions, store under a generated name outside the web root. Residual: none if enforced server-side.

## Pitfalls

- **Modeling everything equally.** Spending the same effort on an internal cron job as on an internet-facing endpoint. Weight by exposure and asset value.
- **Vague threats.** "Hacker could break in" is unactionable. Tie each threat to a specific element and STRIDE category.
- **Trusting the client.** Marking a threat mitigated because the UI validates input. Controls must live server-side of the trust boundary.
- **No owner on residual risk.** Unaccepted residual risk silently becomes nobody's problem.

## Output format

```
## Scope & assets
<one paragraph: system, actors, assets>

## Trust boundaries
- <boundary 1>
- <boundary 2>

## Threat table
| Element | STRIDE | Threat | Likelihood x Impact | Existing control | Recommended mitigation |
|---------|--------|--------|---------------------|------------------|------------------------|

## Prioritized actions
1. <High threat> — owner hint

## Residual risk
- <item> — accepted by <role>
```
