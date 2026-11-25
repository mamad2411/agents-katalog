---
name: threat-model-method
description: Systematic threat modeling via STRIDE — identify threats per component before attackers do. Run at design time, not after incident. This skill is the dispatchable primitive (agents invoke it); `/threat-model` is the session that turns its output into a durable artifact with ADRs, residual risk and re-audit triggers.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# threat-model-method

## Premise

Find real threats, no hand-waves. Every threat cites the component + trust-boundary crossing (`<path:line>` for the entry handler, the auth check, the data store), the attacker persona ("anonymous internet rando" vs "authenticated tenant user" vs "disgruntled employee"), and a concrete mitigation ticket or `<path:line>` where the mitigation lives or must live. "Could be vulnerable to SQLi" is not a threat; "T1: `/orders` POST passes `req.body.price` into `OrderService.create` (`<path:line>`); attacker tampers price; mitigation: server recomputes from product_id (`<path:line>`)" is. Mitigations like "our WAF handles it" are halted unless cited with a configured rule.

## Halt conditions

- Halt on any threat row without component path + trust-boundary citation.
- Halt on impact/likelihood ratings without a one-line justification grounded in the attacker persona.
- Halt on mitigations recorded as prose ("we'll add rate limits") without a ticket id or `<path:line>` for where the control exists / must live.

These three are the canonical set. `/threat-model` Phase 6 enforces them by reference — if you change them here, that command changes with them; do not maintain a second copy anywhere.

## STRIDE

Walk through each component, apply each threat category:

- **S**poofing — impersonating someone else. (Auth bypass, forged JWT, session hijack.)
- **T**ampering — unauthorized modification. (SQL injection, CSRF, tampered payload.)
- **R**epudiation — deny having done it. (Missing audit log.)
- **I**nformation disclosure — leak data. (Verbose errors, cross-tenant data, unencrypted storage.)
- **D**enial of service — prevent legitimate use. (Resource exhaustion, slow POST attack.)
- **E**levation of privilege — gain more access than authorized. (Missing permission checks, IDOR.)

For features that handle PII, run **LINDDUN** alongside STRIDE — it covers the privacy threats STRIDE misses: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance (e.g., over-collection, re-identification, missing consent/retention controls). This skill models those privacy threats at **design** time; once the code exists, hand the built PII data-flow to `@data-privacy-reviewer`, which inventories the real personal fields, traces their egress in source, and maps concrete findings to the configured regulation articles (GDPR/PDPL/CCPA). Model the threat here; audit the shipped code there.

## Flow

1. **Draw the system** — context diagram with external actors, services, data stores, trust boundaries.
2. **Identify trust boundaries** — where does untrusted input enter trusted territory?
3. **Per component, per threat category** — is this applicable? What's the impact? What's the mitigation?
4. **Rank** by impact × likelihood.
5. **Document** — as `ai/audits/threat-model-<feature>-<date>.md` (the location `/threat-model` writes to, so the two never diverge).
6. **Fix** high-rank threats before shipping.

## Output (per feature / system)

Each row is written to survive the Halt conditions above: persona, `<path:line>`, and a mitigation that is either code-that-exists or a ticket. A row that reads well but cites nothing is the failure this skill exists to prevent — the example below deliberately shows both states.

```
## Threat Model — Order Placement

Boundary 1: Client (anonymous / authenticated tenant user) → POST /orders
  entry: <orders controller:line>   authz: <auth guard:line>   store: <orders repo:line>

T-01  S  Caller replays a stolen session to order as another user.
         Persona: authenticated tenant user with a leaked token. Impact HIGH (fraud) ×
         Likelihood MED (needs the token).
         Mitigation: EXISTS — token verified per request at <auth guard:line>; subject
         read from the token, never the body, at <orders controller:line>.

T-02  T  Caller sends `price` in the body and the server trusts it.
         Persona: anonymous internet rando; trivial to try. Impact HIGH × Likelihood HIGH.
         Mitigation: MISSING — server must recompute from product_id. Ticket ORD-42.
         (Not yet code: this row stays MISSING until the ticket closes with a `<path:line>`.)

T-03  I  Tenant A reads tenant B's order by id.
         Persona: authenticated tenant user. Impact CRITICAL (breach) × Likelihood MED
         (one forgotten predicate).
         Mitigation: EXISTS — scope applied by construction at <base repository:line>;
         cross-tenant leak test at <test file:line>. Deep audit: @tenant-isolation-reviewer.

T-04  E  Regular user reaches admin refund management.
         Persona: authenticated tenant user probing routes. Impact HIGH × Likelihood MED.
         Mitigation: PARTIAL — role checked at <admin router:line>, but no test asserts
         the denial. Ticket SEC-17.

Boundary 2: API → payment provider — R/D rows omitted here for length; a real run
  covers every letter per boundary and writes `none — <why>` where a letter does not apply.

Open issues (rank-ordered): 1. T-02 (ORD-42, unmitigated).  2. T-04 (SEC-17, untested).
```

## When to run

- Any new public endpoint; any authentication / authorization change.
- Any new data store for sensitive data; any new external integration.
- Before every major release.

## False positives / gotchas

- **A letter with no threat still needs a row** — write `none — <why>`. A silently skipped letter is indistinguishable from an unexamined one.
- Include the attacker persona — "anonymous internet rando" vs "disgruntled employee" are different threats with different likelihoods.
- Don't dismiss threats with "our WAF handles it" without citing the configured rule.
- **A mitigation marked EXISTS is a claim about code, not a plan.** It carries a `<path:line>` or it is MISSING. This model plans mitigations; only `/security-audit` verifies them.
- Revisit when the system changes — `/threat-model` records the re-audit triggers.

## Related

- `/threat-model` — the full session: durable artifact, actor table, ADRs, residual risk, re-audit triggers. This skill is what it applies per boundary.
- `@data-privacy-reviewer` — takes the LINDDUN half once the code exists.
- `/security-audit` — the enforcement pass that turns a planned mitigation into a verified one.
