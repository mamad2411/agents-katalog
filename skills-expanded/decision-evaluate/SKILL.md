---
namespace: aiwg
name: decision-evaluate
platforms: [all]
description: Evaluate a pinned normalized decision ruleset through an explicitly configured Jev or LLM-subagent binding
triggers:
  - agentic classification
  - decision classification
  - bounded classification
  - Jev decision engine
  - classify to reduce frontier tokens
  - shared-state batching
requires:
  - feature-enabled: AIWG_DECISION_ENABLED=1
  - request: dispatcher request JSON with authored artifact paths and runtime adapter configuration
ensures:
  - normalized-result: returns a decision.aiwg.io/v1alpha1 RulesetResult
  - backend-boundary: definitions and rulesets contain no vendor request payloads or credentials
script:
  entrypoint: scripts/decision-evaluate.mjs
  runtime: node
  cwd: project-root
  argsHint: "--request <dispatcher-request.json> [--host-policy-module <trusted-module.mjs>]"
---

# Decision Evaluate

Evaluate one pinned `DecisionRuleset` with one `DecisionBinding`. The dispatcher
validates pins, input, capabilities, typed outputs, retry/fallback budgets, and
composition before returning an outcome as data. It never authorizes or
executes the outcome.

The request document is runtime configuration, not a portable decision
artifact. It names `rulesetPath`, `bindingPath`, `definitionPaths`, `inputPath`,
`runId`, `invocationId`, optional `receiptDirectory` (which requires
`receiptIntegrityKeyRef`; see `docs/operations.md`), `credentials` mappings
from logical reference to environment-variable name, and optional
`adapterModules` for configured worker transports. Credential values are read
only at adapter call time and never written to results.

Advanced runtime policies are host-owned. The request may include
`hostPolicies` with named references for `batching`, `batchReceipts`,
`context`, `scheduler`, `compileCache`, `resultCache`, or `providerPrefix`:

```json
{
  "hostPolicies": {
    "batching": "native-ticket-batch",
    "batchReceipts": "durable-ticket-batch"
  }
}
```

Those names resolve only through a trusted host registry supplied in-process by
a driver, or through `--host-policy-module` when running the packaged script.
The JSON request cannot serialize callbacks, stores, schedulers, cache
services, authenticated scopes, or key services. Inline `batching`,
`resultCache`, `providerPrefix`, and similar misspelled or unsupported fields
fail before dispatch instead of being ignored. Jev compile caching remains off
unless the host deliberately supplies a `compileCache` policy.

Network-capable adapters (including the packaged Jev adapter) require
`projectionPolicyPath`: a trusted projection policy file, or an array of
policies selected by exact adapter and model. Without it the dispatcher refuses
before any credential or transport use and exits `2`. Only adapters that declare
`egress: { mode: 'none' }` (for example the offline fixture worker) run without a
policy. `adapterOptions.jev` sets the Jev `endpoint`, `allowedOrigins` and the
operator-declared deployment `region`; the policy origin and region must match
them. There is no dispatcher setting that sends unprojected state to a network
adapter. See `agentic/code/addons/decision-engine/examples/dispatcher-request-jev.json`.

Set `AIWG_DECISION_ENABLED=1` explicitly. Existing workflows remain unchanged
when the flag is absent.

The deployed script loads the compiled runtime from the installed `aiwg`
package through `scripts/runtime-root.mjs`: `AIWG_ROOT` when it names a built
package, then a project `node_modules/aiwg`, then the `aiwg` executable on
`PATH`.
