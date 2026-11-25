---
name: qa-security
description: Design and execute a bounded security QA slice when access control, sensitive data or another identified security risk is in scope. Apply alongside the affected API, web or mobile skill.
---

# Security execution

Use through `qa` as a risk overlay. Read `.agent/rules/test-automation.md`
and `.agent/rules/code-review.md` when source is available. Those contracts
own execution boundaries and source-risk reporting. Ordinary functional work
does not require a separate security assessment.

## Bound the investigation

Translate the requested risk into target identities, allowed operations, fixture
actors/data, request ceiling and cleanup. Carry existing task authorization
forward. A broader target, destructive technique or external callback outside
that scope requires resolving the missing authorization before that action.
Do not enumerate unrelated accounts or retrieve real sensitive records to prove
impact when synthetic fixtures suffice.

Map the entry point, trust boundary and security property: who may perform which
action on which object, what input may influence, and what data may leave. Use
requirements/threat model/provider contract as the oracle; OWASP categories help
select checks but do not invent the product's authorization policy. If the policy
is ambiguous, establish the known positive/negative cases and isolate the question.

## Author paired controls

Create two fixture actors and separately owned objects, plus relevant permitted
roles/tenants. Prove each positive control can act on its own resource; otherwise
an apparent denial may only be broken setup. For each selected read or mutation,
vary one boundary at a time: owner, role, tenant, authentication, object identifier
or protected property. Use observed fixture identifiers rather than guessed IDs.

Assert the documented denial, absence of unauthorized content and unchanged
protected state. If a policy conceals existence, compare the intended observable
shape without demanding a particular status from convention alone. A denial
response followed by a completed unauthorized job still violates the property.
For asynchronous actions inspect final state under the owning actor.

Read [bounded security checks](references/checks.md) for applicable session,
property/input, browser or dependency checks. Select the smallest technique that
can establish the property; scanners are optional aids with their own coverage
and safe configuration requirements.

## Execute and diagnose

Run controls before the negative matrix with isolated state. Retain sanitized
actor labels, object relationship, exact operation and the minimum response/state
evidence. Stop the affected technique if it escapes the target/fixture boundary,
causes unexpected resource growth or exposes unrelated data. Record what happened
without copying sensitive content into a report.

Reconcile whether the observed access is granted by intended role inheritance,
a cached session, a fixture mistake or the actual enforcement path. If source is
available, trace authentication separately from object/property authorization.
Demonstrate a defect with the minimum authorized reproduction; a hypothesis about
downstream compromise is not an observed impact. Apply the shared retry budget.

## Assess and maintain

Describe the failed security property, affected actor/object/action, required
preconditions and demonstrated confidentiality/integrity/availability impact.
Use the team's severity scale. Do not assign a numerical CVSS score without its
vector/version and evidence; uncertain reach or exploitability stays explicit.
One denied request or clean scan cannot establish overall security.

Keep both allowed and denied regression cases so blanket rejection cannot make
the suite pass. Recheck alternate methods/routes and async paths when the same
authorization mechanism applies. Rotate disposable fixture state, remove retained
tokens, and reassess the matrix when roles, ownership or trust boundaries change.
Report tested categories and unassessed categories separately, under the shared
verdict/reporting contract.
