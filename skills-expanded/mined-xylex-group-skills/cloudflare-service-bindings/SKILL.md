---
name: cloudflare-service-bindings
description: Configure, explain, or debug Cloudflare Worker-to-Worker service bindings. Use when Codex needs to wire one Worker to another through Wrangler `services`, choose between RPC and HTTP service bindings, add or fix `WorkerEntrypoint` or `fetch` handlers, validate local `wrangler dev` connectivity, reason about deployment order, or troubleshoot service-binding lifecycle and limit issues.
---

# Cloudflare Service Bindings

Use this skill for internal Worker-to-Worker communication on Cloudflare.

Read [references/service-bindings.md](references/service-bindings.md) before changing config, examples, or validation commands so the implementation stays aligned with current Cloudflare behavior.

## Workflow

1. Verify whether the caller should use RPC or HTTP.
2. Inspect the caller's Wrangler config for a `services` binding and the target Worker's name or named entrypoint.
3. Inspect the target Worker implementation:
   for RPC, confirm it exposes methods from `WorkerEntrypoint`;
   for HTTP, confirm it exposes a `fetch` handler that accepts the forwarded request shape.
4. Fix config and code together:
   caller binding name, target Worker name, optional `entrypoint`, and the corresponding caller-side invocation.
5. Validate local development:
   run each Worker with `wrangler dev`, or run one primary plus secondary configs with `wrangler dev -c ... -c ...`;
   confirm the binding shows as connected before trusting runtime behavior.
6. Validate deployment order:
   deploy the target Worker first, then the caller Worker, then remove obsolete entrypoints or methods only after callers stop using them.

## Decision Rules

### Prefer RPC when

- The caller and callee are both Workers you control.
- The interaction is naturally a method call.
- You want typed internal APIs instead of constructing `Request` objects manually.

### Prefer HTTP when

- The callee already centers on `fetch`.
- You are forwarding or transforming inbound HTTP requests.
- You need to preserve request and response semantics directly.

## Non-negotiable Rules

- Keep the binding on the caller Worker; the target Worker does not declare who may call it.
- Match the Wrangler `binding` name to the `env` property the caller actually reads.
- Match the Wrangler `service` value to the deployed target Worker name in the same Cloudflare account.
- Use `entrypoint` only when intentionally binding to a named `WorkerEntrypoint`.
- `await` RPC calls and service-binding `fetch()` calls; otherwise the callee can terminate early.
- Treat every service-binding call as a subrequest and count it toward invocation depth when debugging limits.
- Do not stop at static edits; finish with a local connectivity check, a deploy-ready config, or a precise blocker.

## Validation Target

End with one of these outcomes:

- a working RPC binding with a caller method invocation,
- a working HTTP binding with `env.BINDING.fetch(...)`,
- or a precise failure explanation tied to config mismatch, missing target deployment, disconnected local dev session, or service-binding limits.
