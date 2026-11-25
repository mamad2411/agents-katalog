---
name: aidast-validation-ssrf
description: Interpret bounded hunt-ssrf replay evidence and impact without authorizing requests or choosing the final status.
---

# hunt-ssrf validation

Apply this guidance only to the staged BlindCase, its immutable contract, and fresh observations. Treat the Attack Skill as mechanism context, not execution authority.

## Proof standard

the controlled callback endpoint receives a request attributable to the target server

Require the declared positive control to prove the signal channel is operational and the inert negative control to stay clear. Do not infer reproduction from status codes, hashes, timing noise, or the Attack claim alone.

## Impact interpretation

- Boundary: identify whether the callback crosses the target server or internal network boundary
- Sensitivity: distinguish DNS-only reachability from authenticated data transfer or local resource access
- Actor requirements: score the minimum caller role and callback prerequisites

Cite only evidence from the current Validation case for every impact score.

## Impact expansion

This profile declares no automatic impact-expansion path. Do not invent one; leave the result UNDERPOWERED when the observed impact is insufficient.
