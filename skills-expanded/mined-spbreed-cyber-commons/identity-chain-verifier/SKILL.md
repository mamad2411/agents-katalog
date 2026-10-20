---
name: identity-chain-verifier
description: >-
  Verify workload identity and end-to-end on-behalf-of propagation across
  user, agent, MCP server, tool and downstream. Use to check for token
  passthrough, to distinguish delegation from impersonation, or when asked
  whether a downstream can attribute an action to the original user.
allowed-tools: Bash, Read, Grep
---

# Identity Chain Verifier

**Controls:** Control 3 — workload identity and OBO attribution

## Confidence: HIGH

Delegation is cryptographically distinguishable from impersonation, and token
passthrough is visible in the audience claim. This control is genuinely
verifiable.

## When to use this
When a deployment claims to act on behalf of a human, and whenever that claim
appears in an audit trail. Delegation is impossible without an actor token, so
the presence of one is proof rather than assertion — which is why this control
reaches HIGH confidence and most do not.

## Procedure

1. **Establish workload identity.** Read the registration entry and its
   selectors. For an X.509 credential the identity is in the SAN URI; for a JWT
   credential it is the subject. Confirm it matches the deployment manifest.

2. **Walk every hop.** For user → agent → MCP server → tool → downstream,
   record the principal, the audience, and the token type at each hop.

3. **Check for token passthrough — the finding that matters most.** A server
   must not forward the token it received to a downstream. Each hop must carry
   a **distinct, audience-scoped** token. A repeated audience across two hops
   is passthrough, and it is the mechanism behind the confused-deputy class.

4. **Distinguish delegation from impersonation.** In token exchange, delegation
   is impossible without an actor token: the presence of an actor token, and a
   corresponding actor claim in the issued token, is what proves the chain is
   delegation rather than the agent simply becoming the user.

5. **Check credential hygiene.** Short lifetime, rotation, and — where mutual
   TLS is possible — prefer certificate credentials over bearer tokens, which
   are replayable. Flag every JWT-only hop.

## Example

**Input** — the fixture committed at the top of [`scripts/identity_chain_verifier.py`](scripts/identity_chain_verifier.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the access token the payments API will actually see:

{
  "act": {
    "sub": "spiffe://cybertravels.com/ns/prod/sa/agent-alpha"
  },
  "aud": "https://payments.cybertravels.internal",
  "cnf": {
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
  "deployment_id": "str",
  "chain": [
    {"hop": "user|agent|mcp|tool|downstream", "principal": "str",
     "audience": "str", "token_type": "x509|jwt",
     "mode": "delegation|impersonation|passthrough", "ttl_seconds": 0}
  ],
  "passthrough_violations": [{"from_hop": "str", "to_hop": "str", "audience": "str"}],
  "delegation_proven": true,
  "jwt_only_hops": ["str"],
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Accepting a matching subject as proof of delegation.** Impersonation also
  produces the right subject. The actor claim is the difference.
- **Not checking the audience.** Passthrough is invisible without it.
- **Treating a long-lived JWT as equivalent to a rotated certificate.**
