---
name: env-secrets
description: Inventory the environment variables, configuration, and credentials of a project preparing to launch, deploy, ship, or release; detect committed or hardcoded secrets without reading their values into the output; design development, preview, and production environment separation on the target platform; and produce a rotation plan for anything exposed. Use for .env cleanup, secret management, environment configuration, leaked key response, or pre-launch configuration reviews.
---

# Env Secrets

Make the project's configuration safe to ship: no secrets in source control,
one clear layout per environment, and a rotation plan for anything already
exposed. Inspect the repository first; design for the platform the project will
actually deploy to.

## Rules

- Optimize for a safe first production release, not a full secret-management
  platform.
- Report secrets by name, file, and location only. Never print, copy, store, or
  reuse a secret value, even one already committed to the repository.
- Never test whether a discovered credential is valid and never use it to
  connect to any service.
- Treat every secret that has ever been committed, logged, or bundled into
  client code as exposed. Removing it from the working tree does not un-expose
  it; only rotation does.
- Environment-variable names and placeholder examples are safe evidence; real
  values are not.
- Use the deployment platform's native environment and secret storage before
  recommending a dedicated secret manager. Add one only for an observed
  requirement.
- Never infer compliance obligations from code.
- Recommend only by default. Do not rotate credentials, rewrite git history,
  edit files, or change platform configuration unless the user explicitly
  requests it.

## Workflow

### 1. Inventory configuration

Build a complete inventory of configuration inputs:

- environment-variable names read by the code, with the component that reads
  each one;
- `.env` and other configuration files present in the working tree and in git
  history;
- variables referenced in deployment, container, and CI configuration;
- example or template files (`.env.example`) and their placeholder quality;
- configuration read at build time versus runtime, and variables bundled into
  client-side code by naming convention or bundler behavior.

Classify each entry as secret (credentials, keys, tokens, connection strings)
or plain configuration (feature flags, URLs, public identifiers).

### 2. Detect exposure

Read [secrets-readiness.md](references/secrets-readiness.md). Search for:

- committed `.env` and credential files, including in git history;
- hardcoded literals matching known key prefixes or high-entropy patterns;
- secrets bundled into client code via public variable prefixes;
- secrets echoed to logs, error messages, or CI output;
- production and development environments sharing one credential.

Record each finding as name, location, and exposure route. Mark uncertain
matches as suspected rather than confirmed.

### 3. Design the environment layout

Determine the target platform, using the `deploy-plan` outcome when available.
Design the smallest safe layout:

- which variables exist in development, preview, and production, and which
  values must differ per environment;
- where each environment's secrets are stored on the platform;
- which variables are safe to expose to client code and which must remain
  server-side;
- how a developer obtains a working local configuration without receiving
  production secrets;
- an updated `.env.example` with placeholders, and `.gitignore` coverage.

### 4. Plan rotation

For every exposed secret, in order of blast radius: identify the issuing
service, the supported rotation or revocation procedure from official
documentation, the deployments that must receive the new value, and the
verification step. Note when git-history rewriting is and is not worth it: it
never substitutes for rotation.

### 5. Present

Return:

1. **Release verdict** — whether configuration is safe to ship.
2. **Inventory** — variables by component and environment, secrets
   distinguished from plain configuration.
3. **Exposures** — each exposed or suspected secret with name, location, route,
   and severity; values never included.
4. **Environment layout** — the recommended per-environment design for the
   target platform.
5. **Rotation plan** — ordered steps for every exposure.
6. **Repository changes** — files to add, remove, or ignore, without making the
   changes unless requested.
7. **Verification** — how to confirm each environment resolves the correct
   values without printing them.

## Implementation handoff

If the user asks to implement, stage the work in this order: rotate exposed
credentials at the issuing services, place new values into platform secret
storage per environment, update the repository files, then verify each
environment boots against the correct configuration. Obtain confirmation before
revoking credentials that production may still be using, and never write real
values into tracked files.
