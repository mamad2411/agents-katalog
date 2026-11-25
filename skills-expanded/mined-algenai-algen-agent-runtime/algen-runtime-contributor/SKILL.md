---
name: algen-runtime-contributor
description: Implement or review contributions to Algen Agent Runtime while preserving its public API, provider neutrality, tenant isolation, optional dependencies, and repository boundary.
---

# Contribute to Algen Agent Runtime

Work from the Runtime repository root. Read `CONTRIBUTING.md` and the documentation most closely
related to the change before editing. Use `references/change-checklist.md` when planning or reviewing
a code change.

Keep reusable execution contracts, orchestration, governance, persistence, and integrations in
Runtime. Keep Studio UI, project management, marketplace, and product-specific behavior out of this
repository. Domain behavior belongs in an application hook provider, not in the Runtime executor.

Preserve these invariants:

- provider-neutral public contracts and typed boundaries;
- explicit tenant, user, permission, secret, and idempotency context;
- deterministic offline behavior and tests by default;
- optional provider, database, vector-store, telemetry, and framework dependencies;
- stable error codes and forward migrations for persisted data;
- secret-free configuration committed to source control.

Keep the security invariants in `AGENTS.md`, "Security invariants", each with the test that
enforces it: routes isolate tenants and need an identity (`tests/unit/test_api_tenant_matrix.py`;
classify a new route in `ROUTES`), governance fails closed (only `approved` or `modified` runs a
gated tool), only `ToolExecutor.execute` runs a tool, output policies cover every text path,
verify exactly what you load or run, and workflows pass `scripts/check-workflows.sh`. A change to
the API, auth, storage, tools, policies, approvals, workflows, frameworks, plugins, MCP or
`.github/` runs those tests and a security review, and its pull request says which rules it
touches. Never weaken a check to make a change pass, and report a vulnerability privately
(`SECURITY.md`), never in a public issue, commit or test name.

Add the narrowest meaningful test and cover the relevant failure path. Update public documentation,
examples, and `CHANGELOG.md` for user-visible behavior. A change to the public surface (exports,
routes, configuration, errors, events and their payload keys, protocols, migrations) regenerates
`docs/api/surface.json` with `python scripts/api_surface.py --update`; `--changes` groups the
difference into removed, changed, added and experimental, and only removed or incompatible stable
entries are breaking. An interface not ready for the compatibility promise is marked experimental
in code (`algen_agent_runtime.stability`, an `Experimental:` docstring) and in
`docs/api-stability.md`. When a new capability is one a host
application may already have built itself, add it to the `algen-runtime-host` skill's table and to
the changelog's "You can now remove", and tell the maintainer which known hosts (Algen Studio,
fly91-hrms, and the Traccia assistant service, `traccia-assistant-service`) to open an issue in;
never open one yourself. Run the repository quality gates before
finishing; report any gate that could not run and why. Provide a concise, well-structured Git commit
message summarizing the verified changes. Do not commit, push, publish, or open a pull
request unless the user explicitly requests it.

