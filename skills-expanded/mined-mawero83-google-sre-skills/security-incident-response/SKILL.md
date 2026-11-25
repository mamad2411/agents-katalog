---
name: security-incident-response
description: >-
  Respond to security crises with reliability in mind: contain, communicate, preserve evidence, eradicate, and recover — coordinated with SRE incident process. Use for suspected compromise and security+reliability incidents.
---

# Security Incident Response

**Domain:** `security`  
**Sources:** Building Secure & Reliable Systems Ch17–18, SRE Book 2e Ch22 examples

## When to use

- Suspected breach / account takeover
- Supply-chain security event
- Joint Sec+SRE response

## Principles

- Do not tip off attackers prematurely; coordinate containment carefully.
- Preserve forensic evidence while protecting customers.
- Recovery sequencing: eject, mitigate immediate harm, long-term harden.
- Use incident roles; add security lead alongside IC.

## Workflow

1. Engage security; establish shared state doc with need-to-know.
2. Scope compromise; contain credentials/access paths.
3. Assess reliability impact; protect CUJs.
4. Eradicate + rotate; recover services deliberately.
5. Post-incident: blameless+forensic learning; track hardenings.

## Decision guide

- If unsure criminal/legal → involve legal early.

## Output template

```markdown
# Security incident worksheet
- Suspected scope:
- Containment actions:
- Evidence preserved:
- Customer/reliability impact:
- Recovery / hardenings:
```

## Anti-patterns

- Public debug that educates attackers.
- Wiping systems before capture.

## Related skills

`crisis-management`, `incident-management`, `security-reliability-design`

## Canonical references

- [Building Secure & Reliable Systems](https://google.github.io/building-secure-and-reliable-systems/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
