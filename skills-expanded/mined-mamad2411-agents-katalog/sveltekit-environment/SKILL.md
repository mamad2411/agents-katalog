---
name: sveltekit-environment
description: Use when working with environment variables in SvelteKit including $env/static/private, $env/static/public, $env/dynamic/private, $env/dynamic/public, and server-only module boundary enforcement.
---

# SvelteKit Environment

## Specialization

Expert guidance for environment variable access and module boundary enforcement in SvelteKit. Covers the four `$env/*` virtual modules, their distinct runtime semantics (static vs. dynamic, private vs. public), the `$lib/server` and `.server.ts` naming conventions for server-only modules, build-time import detection, and the security implications of each pattern.

## Trigger Conditions

- Accessing an environment variable (API key, database URL, feature flag) inside a SvelteKit application.
- Receiving a build error about importing private env vars in client-reachable code.
- Deciding which `$env/*` module to use for a given variable and access pattern.
- Enforcing that a module or file can only be imported from server-side code.
- Diagnosing "cannot read env var at runtime" errors in edge or prerendered deployments.
- Reviewing code for accidental secret exposure through universal load functions.

## Scope Boundaries

In scope:

- `$env/static/private`: build-time-resolved private variables (not sent to browser).
- `$env/static/public`: build-time-resolved public variables (may appear in browser bundle).
- `$env/dynamic/private`: runtime-resolved private variables (server only, not inlined).
- `$env/dynamic/public`: runtime-resolved public variables (accessible in browser after serialization).
- `$lib/server` directory: any module under `src/lib/server/` is server-only; SvelteKit's build enforces this.
- `.server.ts` / `.server.js` file naming: any file with `.server.` in its name is server-only.
- `privatePrefix` and `publicPrefix` configuration in `svelte.config.js`.
- Platform environment access in adapter-specific contexts (e.g. `platform.env` in `adapter-cloudflare`).
- `process.env` fallback and when it is and is not safe.

Out of scope:

- Secret management services (Vault, AWS Secrets Manager) — this skill covers SvelteKit's env module layer, not the secret store itself.
- CI/CD pipeline secret injection — infrastructure concern.
- Adapter deployment configuration — covered by `sveltekit-adapters`.

## Inputs

- Variable name(s) and whether they are secret (private) or safe to expose to the browser (public).
- Whether the value is known at build time (static) or only at runtime (dynamic).
- Access location (server load, universal load, hook, endpoint, client component).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Correct `$env/*` module selection | Import statement using the right module for the variable's privacy and timing requirements |
| Server-only module enforcement | `$lib/server` path or `.server.ts` naming applied where needed |
| Build-error remediation | Diagnosis and fix for "cannot import private env in client context" errors |
| Environment quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Access a single API key from a server load function | Correct `$env/static/private` import used; variable is server-only |
| L2 Practical Delivery | Mixed private and public variables across server and client code | All four modules used correctly; no cross-boundary imports |
| L3 Specialist Hardening | Runtime-dynamic variables in edge/serverless with custom prefix config | `$env/dynamic/*` used appropriately; `privatePrefix` configured in `svelte.config.js` |
| L4 Expert Standardisation | Enforced server-only module boundaries across a project | All sensitive logic in `$lib/server`; import audit passes; documentation exists for each variable's module selection rationale |

## Workflow

1. Classify each variable: is it secret (never expose to browser) or public (safe to include in client bundle)?
2. Classify timing: is the value known at build time (baked into the bundle) or only available at runtime (e.g. from a platform secrets store or `.env` file loaded at startup)?
3. Select the correct module:
   - Secret + build time → `$env/static/private`
   - Public + build time → `$env/static/public`
   - Secret + runtime → `$env/dynamic/private`
   - Public + runtime → `$env/dynamic/public`
4. Import only in files that execute on the server: `hooks.server.ts`, `+page.server.ts`, `+server.ts`, `+layout.server.ts`, or files under `src/lib/server/`.
5. Never import `$env/static/private` or `$env/dynamic/private` in `+page.ts` (universal load), `+layout.ts`, client-side components, or any file under `src/lib/` that is not inside `src/lib/server/`.
6. For modules that must only run on the server (regardless of env vars), either place them under `src/lib/server/` or use the `.server.ts` filename convention.
7. If a universal load function needs data derived from a private variable, fetch it from a server load function and pass it via `return { ... }`; do not lift the private import into universal code.
8. For edge or serverless deployments where `process.env` is unavailable, use `$env/dynamic/private` to access platform-injected environment at runtime.
9. Configure `privatePrefix` / `publicPrefix` in `svelte.config.js` if your variable naming convention differs from the SvelteKit defaults (`PUBLIC_` for public variables).
10. Run the environment quality checklist.

## Environment Quality Checklist

- [ ] Every environment variable is imported from the correct `$env/*` module for its privacy and timing classification.
- [ ] No `$env/static/private` or `$env/dynamic/private` imports exist in any file reachable from the browser bundle.
- [ ] Universal load functions (`+page.ts`, `+layout.ts`) do not import private env modules.
- [ ] All modules containing sensitive logic are under `src/lib/server/` or use `.server.ts` naming.
- [ ] `process.env` is not used as a fallback in server code that may run in edge environments without Node.js.
- [ ] Public variables contain no secrets; their values would not be harmful if extracted from a client-side bundle.
- [ ] `privatePrefix` configuration in `svelte.config.js` matches the variable naming convention in use.
- [ ] Build-time variables are not used for secrets whose values change per deployment without a rebuild.

## Security Notes

- The most critical security rule: **private env vars imported in universal load functions (`+page.ts`) run on both server and client.** SvelteKit will throw a build error for direct imports, but code paths that conditionally import (dynamic `import()`) can bypass this check. Audit carefully.
- `$env/static/public` variables are inlined into the client bundle at build time. Treat them as public; never place secrets there.
- `$env/dynamic/public` variables are serialized and sent to the client at runtime. The same public-only constraint applies.
- Do not commit `.env` files containing real secrets to version control. Use `.env.example` for documentation.
- Variables available to `$env/static/*` are read from `.env` at build time in development. In production, inject them via your deployment platform's secrets mechanism.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Variable classification | Workflow steps 1–2 |
| Module selection | Workflow step 3 |
| Safe import locations | Workflow steps 4–5 |
| Server-only module enforcement | Workflow step 6 |
| Universal load pattern | Workflow step 7 |
| Edge/serverless runtime vars | Workflow step 8 |
| Custom prefix config | Workflow step 9 |
| Security hardening | Security Notes + checklist |
| Quality validation | Environment Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
