---
name: author-build-and-deployment
description: Build manifest and deployment config authoring for site-specific build processes, artifact management, and deployment automation.
intent: >-
  Author and maintain site-specific build manifests, deployment configurations, and build artifact contracts. Ensures build and deployment behavior is configuration-driven and contract-based.
type: workflow
best_for:
  - "Defining site-specific build steps and artifact outputs"
  - "Authoring build-manifest.json for site automation"
  - "Designing deployment-config.json parameter contracts"
  - "Troubleshooting build or deployment failures"
  - "Coordinating multi-site build/deployment parity"
scenarios:
  - "A site needs custom build-time artifact generation"
  - "Deployment is failing due to missing step params"
  - "Build manifest needs to coordinate generated files across services"
  - "Deployment config baseline is drifting from site-endpoint-config"
---

# Author Build And Deployment

Author and maintain build manifests and deployment configs as contract-driven configuration.

## What This Skill Does

1. Designs site-specific `build-manifest.json` with explicit action steps, ordering, and param wiring.
2. Manages `deployment-config.json` that describes deploy-time variables derived from site-endpoint-config.
3. Ensures build/deployment contracts are enforced: missing step param = build bug, not operator error.
4. Maintains parity across multi-site deployments: scripts, manifests, and generated artifacts stay synchronized.
5. Troubleshoots deployment failures by validating contract compliance before operational workarounds.

## Build Manifest Contract Model

The `build-manifest.json` file defines:
- Executable action plan (step sequence)
- Payload script paths
- Parameter wiring for each step
- Build artifact targets and exclusions

**Key Principle:** Every action step that resolves site-local files must receive `siteName` via step params.

### Manifest Structure
```json
{
  "siteName": "companions",
  "version": 1,
  "steps": [
    {
      "stepName": "generate-search-config",
      "action": "scripts/generate-search-config.mjs",
      "params": {
        "siteName": "{{siteName}}",
        "sitePath": "sites/{{siteName}}",
        "outputPath": "sites/{{siteName}}/build/search-config.json"
      }
    }
  ],
  "artifacts": {
    "source": ["sites/{{siteName}}", "shared-lib"],
    "exclude": [".git", "node_modules", ".DS_Store"],
    "output": "builds/{{siteName}}-deploy.tgz"
  }
}
```

### Parameter Wiring Rules
1. Use `{{siteName}}` template variable for site-local paths.
2. Every step that processes site config must receive explicit `siteName`.
3. Avoid path-derived fallback site resolution; manifest supplies explicit values.
4. Validate that remote script argument positions match local script expectations.

## Deployment Config Contract Model

The `deployment-config.json` file describes:
- Service-level variable requirements
- Baseline fallback values
- Deploy-time descriptor patterns
- Contract drift signals

**Key Principle:** Baseline fallback warnings (`[build-contract] Using baseline fallback for <service>.<field>`) indicate explicit drift and must be resolved deliberately.

**Endpoint-config fragment placement (MUST):** The launcher requires each service-level fragment to be named `endpoint-config.json` and located directly at `sites/<site>/config/<service>/endpoint-config.json`. This is the single supported layout — do NOT nest fragments inside an additional `endpoint-config/` subdirectory (for example `sites/<site>/config/<service>/endpoint-config/endpoint-config.json`). When authoring fragments, follow this exact folder shape and filename so the launcher can discover and merge them automatically. Example: `sites/atlas/config/gateway/endpoint-config.json`.

### Config Structure
```json
{
  "siteName": "companions",
  "services": [
    {
      "serviceName": "gateway",
      "type": "gateway",
      "env": {
        "PORT": { "source": "site-endpoint-config", "field": "gateway.port", "required": true },
        "SESSION_KEY": { "source": "vault", "field": "session_key", "required": true }
      }
    },
    {
      "serviceName": "search",
      "type": "search",
      "env": {
        "DB_URL": { "source": "baseline", "value": "http://localhost:5984", "required": true }
      }
    }
  ]
}
```

### Contract Rules
1. Fields not required by a service type (e.g., token on feature UI endpoints) should be removed, not tolerated via baseline.
2. Keep service-level requirements aligned between:
   - site-endpoint-config.json
   - generated deployment-config.json
   - runtime assumptions in actions/scripts
3. Resolve contract mismatches at site scope first; do not change shared behavior without explicit approval.
4. When modifying manifest params, verify that remote script argument positions still match script expectations.

## Multi-Site Synchronization Rules

When fixing deployment scripts used by multiple sites:
1. Update all active site copies
2. Update the template source in the same change set
3. Validate parity with hash or diff checks after copy/sync
4. Avoid one-site-only hotfixes for shared deployment logic unless intentionally scoped and documented

## Common Build Patterns

### Pattern 1: Route/View Code Generation
```json
{
  "stepName": "generate-routes",
  "action": "shared-lib/dynamic-route/generate.mjs",
  "params": {
    "siteName": "{{siteName}}",
    "configFile": "sites/{{siteName}}/site-endpoint-config.json",
    "outputDir": "sites/{{siteName}}/routes"
  }
}
```

**Result:** Produces `_gen.mjs` route files (DO NOT edit directly).

### Pattern 2: Search Configuration
```json
{
  "stepName": "build-search-index",
  "action": "shared-lib/cli/build-search-index.mjs",
  "params": {
    "siteName": "{{siteName}}",
    "criteriaDir": "sites/{{siteName}}/assets/search-engine/search",
    "outputFile": "sites/{{siteName}}/build/search-index.json"
  }
}
```

### Pattern 3: Artifact Packaging
```json
{
  "artifacts": {
    "source": [
      "sites/{{siteName}}",
      "shared-lib",
      "package.json",
      "package-lock.json"
    ],
    "exclude": [
      ".git",
      "node_modules",
      "sites/*/node_modules",
      "**/.DS_Store",
      "sites/*/build/*.tgz"
    ],
    "output": "builds/{{siteName}}-deploy-$(date +%s).tgz"
  }
}
```

## Anti-Patterns

1. Hard-coding site paths in step params instead of using `{{siteName}}` template variable.
2. Relying on path-derived fallback site detection instead of manifest-supplied `siteName`.
3. Tolerating baseline fallback for fields that should be contract-driven.
4. One-site-only script variations when the logic should be shared and template-parameterized.
5. Editing `_gen.*` files directly instead of updating generator sources and re-building.
6. Creating separate deployment scripts per site instead of template-driven manifest coordination.

## Debugging Checklist

**Build Step Fails with Missing Param**
- [ ] Step params include all required `siteName`-dependent paths?
- [ ] Manifest template variables properly interpolated?
- [ ] Script expectations match param positions?

**Deployment Contract Mismatch**
- [ ] `[build-contract] Using baseline fallback` warnings present?
- [ ] Service-level requirements aligned across config → deployment-config → scripts?
- [ ] Stale baseline descriptors removed for unneeded fields?

**Artifact Missing After Build**
- [ ] Manifest step produces artifact to correct output path?
- [ ] Artifact excluded in global excludes list?
- [ ] Output path matches deployment expectations?

**Multi-Site Sync Out of Parity**
- [ ] All active site manifests have same structure + params?
- [ ] Template source and generated copies hash-verified?
- [ ] Recent fixes applied to all copies?

## References

- build-manifest.json schema: `shared-lib/schema/build-manifest-schema.json`
- deployment-config.json schema: `shared-lib/schema/deployment-config-schema.json`
- Template variables: `shared-lib/cli/render-template-vars.mjs`
- Script generation: `shared-lib/dynamic-route/generate.mjs`
