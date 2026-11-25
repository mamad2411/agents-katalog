---
name: agent-identity-review
description: >-
  Review how an agent authenticates and how a user's authority is delegated to
  it, including token exchange, on-behalf-of chains, service accounts and
  non-human identity. Use when asked who an agent is calling as, whether a
  delegation is auditable, why a downstream system sees the wrong principal, or
  how to scope an agent's credentials.
allowed-tools: Read, Grep, Glob
---

# Agent identity and delegation review

Three identities are in play whenever an agent acts, and most incidents come
from collapsing them:

- the **user** whose request started the work
- the **agent** doing the work — a workload identity, not a person
- the **actor chain** connecting them, which is what an auditor needs

A service account shared by every agent answers "what ran" and destroys "for
whom". That is the gap non-human identity exists to close.

## When to use this

Reviewing an agent's auth design, an OBO/token-exchange implementation, a
gateway that fronts an agent, or any log where you cannot tell which user
caused an action.

## Procedure

**1 — Name the three identities.** For the flow under review, write down the
user principal, the workload identity, and where each is asserted. If the
workload identity is a long-lived shared secret, that is finding one.

**2 — Check the delegation narrows.** In RFC 8693 token exchange the issued
token must satisfy **both** rules:

- **subset of presented** — never more scope than the incoming token carried
- **within the actor's ceiling** — never more than the agent is itself allowed

Either rule alone is insufficient. Subset-only lets a highly privileged user
hand an agent authority the agent should never hold; ceiling-only lets an agent
exceed the user who asked. Test both directions explicitly.

**3 — Check the chain is preserved and not duplicated.** The `act` chain should
read `user → agent`, once. A chain that repeats the principal
(`dana → dana → agent`) usually means the head was appended twice, and it
breaks any audit query that counts hops.

**4 — Find where OBO stops.** Some downstream systems cannot consume a
delegated token — legacy databases, vendor APIs, anything with a static
credential. Identify each, and require a **choke point**: a gateway that holds
the credential, enforces per-user authorisation *before* the call, and logs the
original principal. The credential must not be reachable by the agent directly.

**5 — Check expiry and revocation.** How long is the delegated token valid, and
what stops it being replayed after the user's session ends? Just-in-time
authority that outlives the task is standing authority with extra steps.

**6 — Check the log answers the audit question.** Pick a real question — "which
user caused this row to be deleted?" — and try to answer it from the logs alone.
If you cannot, the delegation is not auditable regardless of how it is built.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_identity_review.py`](scripts/agent_identity_review.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
request                     authorized?  attributed to
dana@corp -> reports:read   True         dana@corp via reports-agent
dana@corp -> db:admin       False        dana@corp via reports-agent

memory keys - the same workspace, two users:
   dana  -> acme:dana@corp
   priya -> acme:priya@corp
   shared? False
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "identities": {"user": "str", "workload": "str", "assertion": "str"},
  "delegation": {"mechanism": "obo|impersonation|shared_service_account|none",
                 "subset_of_presented": true, "within_actor_ceiling": true,
                 "chain": ["principal", "..."], "chain_wellformed": true,
                 "ttl_seconds": 0, "revocable": true},
  "chokepoints": [{"downstream": "str", "reason": "str",
                   "enforced_at": "gateway|service|none",
                   "credential_reachable_by_agent": false}],
  "audit": {"question": "str", "answerable_from_logs": true},
  "findings": [{"issue": "str", "severity": "critical|high|medium|low", "fix": "str"}]
}
```

## Failure modes

- **Checking only one narrowing rule.** Both, every time.
- **Accepting a shared service account because it is "internal".** Internal is
  a network property; it says nothing about attribution.
- **Treating the gateway as optional** where the downstream cannot do OBO. It
  is the only place authorisation can happen.
- **Measuring delegation by whether the call succeeded.** A call that succeeds
  with too much scope is the failure being looked for.
