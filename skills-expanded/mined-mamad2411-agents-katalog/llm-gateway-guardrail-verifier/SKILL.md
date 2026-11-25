---
name: llm-gateway-guardrail-verifier
description: >-
  Prove all model traffic leaves through the sanctioned gateway, including
  tool-initiated and background calls, and that guardrail policies are
  attached and enforced. Use to attest gateway routing, to check whether a
  provider endpoint is directly reachable, or to evidence which guardrail
  policies are switched on.
allowed-tools: Bash, Read
---

# Llm Gateway Guardrail Verifier

**Controls:** Control 4 — gateway routing and guardrails

## Confidence: HIGH **only if** egress is enforced below the application

An application-layer gateway configuration is a routing preference. An agent
that can open a socket can bypass it by calling the provider directly. If the
allowlist is not enforced at the network layer, **downgrade this control to
PARTIAL** and say why.

## When to use this
When a deployment routes model traffic through a gateway and the attestation
wants to say so. Check first whether egress is enforced below the application:
if it is not, an agent opens a socket and the gateway is advisory, and this
control's confidence drops with it.

## Procedure

1. **Test reachability, do not read configuration.** From the deployment's
   network position, attempt to reach provider endpoints directly. Anything
   reachable that is not the gateway is a finding, regardless of what the
   configuration says.

2. **Cover the paths people forget.** Tool-initiated calls, background jobs,
   scheduled tasks, retry paths and sub-agents. A gateway that fronts the main
   request path and not the batch job is a gateway with a hole in it.

3. **Confirm guardrail attachment and version.** Record the guardrail ID and
   version actually attached to the route, not the one in the template.

4. **Enumerate enabled policies.** Content filters, prompt-attack filtering,
   denied topics, sensitive-information filters, contextual grounding. Record
   whether each is applied on **input, output, or both** — input-only filtering
   is a common and quiet gap.

5. **Confirm the action.** A filter set to observe rather than block is
   telemetry, not a control. Record the configured action per policy.

## Example

**Input** — the fixture committed at the top of [`scripts/llm_gateway_guardrail_verifier.py`](scripts/llm_gateway_guardrail_verifier.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   the intended call           ALLOWED
   unregistered agent          denied at identity
   verb not permitted          denied at policy
   exfiltration destination    denied at egress
   over the per-target ceiling denied at budget

audit entries written: 1
credential held by the agent: never - attached at the gateway
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
  "gateway_enforced": true,
  "enforcement_layer": "network|application",
  "reachable_provider_findings": [{"endpoint": "str", "path": "direct|tool|background"}],
  "guardrail": {"id": "str", "version": "str",
                "policies": [{"name": "str", "applied_to": "input|output|both",
                              "action": "block|anonymize|observe"}]},
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Reading the route table instead of testing reachability.**
- **Missing the background path.** Scheduled and tool-initiated calls are the
  ones that bypass the gateway in practice.
- **Recording a guardrail as enforced when its action is observe.**
