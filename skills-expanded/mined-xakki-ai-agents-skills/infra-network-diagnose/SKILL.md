---
name: infra-network-diagnose
description: 'Diagnose endpoint connectivity and proxy routing across the actual network boundaries. Use when a service is unreachable or traffic is routed unexpectedly. RU: сеть, прокси, недоступен.'
---

# Network boundary diagnostics

Define the exact endpoint, caller, address family, intended route, observed symptom and permitted probes. Establish the active network context and actual configuration without exposing credentials. Resolve the service path boundary by boundary: name resolution, route and transport, secure handshake, proxy or ingress, upstream service and application response as relevant. Success at one layer does not prove all subsequent layers.

Compare intended and effective configuration. An explicit outbound route and ambient process settings can interact; trace the real transport selected by each caller rather than assuming a common client configuration applies everywhere. For ingress, distinguish the physical peer from forwarded metadata and establish which intermediary is actually trusted before attributing a client identity.

When an access policy depends on source addresses, verify whether trusted forwarding metadata rewrites the address evaluated by that policy. Exercise an allowed physical peer and an untrusted peer with spoofed forwarding metadata against the actual access boundary; textual configuration alone does not prove the effective trust chain.

Use the smallest authorized observation or synthetic probe that distinguishes competing hypotheses, with explicit attempt and resource bounds. A proxy-mediated result establishes what that proxy observed, not independent inbound reachability from all networks. Rate limits, rejection and authentication controls are not permission to bypass them. Do not restart, change routing, expose ports or modify firewall policy solely to collect evidence.

Interpret only boundaries actually reached: a proxy tunnel rejection does not establish the origin's HTTP or TLS behavior, and a default verification field is not a successful handshake when that handshake never completed. Compare direct and proxied paths only when both are in the authorized probe scope.

Report the first observed failing boundary, actual tested paths, time and limitations; mark untested alternatives as unknown. Use the superpowers `systematic-debugging` skill for general causal investigation and ask the user to invoke `deploy-rollout-run` when its separate operational procedure is needed and authorized.

For a local service that invokes an existing command-line worker, consult [bounded worker service](references/bounded-worker-service.md) when that specific architecture is in scope.
