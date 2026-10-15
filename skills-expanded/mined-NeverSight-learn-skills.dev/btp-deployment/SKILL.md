---
name: btp-deployment
description: >
  Use when deploying a SAP CAP application to SAP BTP: MTA descriptor (mta.yaml),
  Cloud Foundry manifest, Kyma / Kubernetes deployment, HANA Cloud provisioning,
  HDI containers, service bindings, environment variables, or build/deploy pipelines.
metadata:
  category: cap
  version: "1.0.0"
  keywords: [mta.yaml, MTA, cds build, cf deploy, Cloud Foundry, Kyma, HDI container, hdi-deploy, xsuaa, service bindings, mbt build, production build]
  related:
    security-auth: XSUAA resource definition in mta.yaml
    btp-service-bindings: bind services locally before deployment
    btp-destinations: destination service configuration in mta.yaml
    ci-cd: automate deployment in CI/CD pipelines
    multitenancy: SaaS deployment with MTX sidecar
---

# BTP Deployment — CAP Best Practices

> **Primary reference**: https://cap.cloud.sap/docs/guides/deployment/
> **To Cloud Foundry**: https://cap.cloud.sap/docs/guides/deployment/to-cf
> **To Kyma**: https://cap.cloud.sap/docs/guides/deployment/to-kyma

## MTA structure for a full-stack CAP app (Cloud Foundry)

```yaml
_schema-version: '3.1'
ID: my-cap-app
version: 1.0.0
description: My CAP Application

modules:

  # ── Node.js backend ──────────────────────────────────────────────────────
  - name: my-cap-app-srv
    type: nodejs
    path: gen/srv
    parameters:
      buildpack: nodejs_buildpack
      memory: 512M
    build-parameters:
      builder: npm
      build-result: .
      commands:
        - npm ci --production
    provides:
      - name: srv-api
        properties:
          srv-url: '${default-url}'
    requires:
      - name: my-cap-app-db
      - name: my-cap-app-uaa
      - name: my-cap-app-destination

  # ── HANA Deployer ────────────────────────────────────────────────────────
  - name: my-cap-app-db-deployer
    type: hdb
    path: gen/db
    parameters:
      buildpack: nodejs_buildpack
    requires:
      - name: my-cap-app-db

  # ── Launchpad (optional) ─────────────────────────────────────────────────
  - name: my-cap-app
    type: approuter.nodejs
    path: app/router
    parameters:
      memory: 256M
    requires:
      - name: srv-api
        group: destinations
        properties:
          name: srv-api
          url: '~{srv-url}'
          forwardAuthToken: true
      - name: my-cap-app-uaa
      - name: my-cap-app-destination

resources:

  - name: my-cap-app-db
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared

  - name: my-cap-app-uaa
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      path: ./xs-security.json

  - name: my-cap-app-destination
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite
```

## Build & deploy commands

```bash
# Build MTA archive
mbt build -t ./

# Deploy to CF
cf deploy my-cap-app_1.0.0.mtar --retries 1

# Or use CDS shortcut (combines build + deploy)
cds build --production
cf push   # if using manifest.yml without MTA
```

## cds build for production

```bash
# Build all targets
cds build --production

# Output in gen/:
# gen/srv  → Node.js deployable
# gen/db   → HDI deployer artifact
```

Add to `package.json`:
```json
{
  "cds": {
    "build": {
      "target": "gen",
      "tasks": [
        { "for": "hana",   "src": "db",  "options": { "model": ["db","srv","app"] } },
        { "for": "nodejs", "src": "srv", "options": { "model": ["db","srv","app"] } }
      ]
    }
  }
}
```

## Kyma / Kubernetes deployment

```bash
# Add Kyma target
cds add helm

# Build Docker images
pack build my-cap-app-srv --builder paketobuildpacks/builder:base
docker push my-registry/my-cap-app-srv:latest

# Deploy with helm
helm upgrade --install my-cap-app ./chart \
  --set srv.image.repository=my-registry/my-cap-app-srv \
  --set srv.image.tag=latest
```

## Service bindings in Kyma

```yaml
# servicebinding.yaml
apiVersion: services.cloud.sap.com/v1
kind: ServiceBinding
metadata:
  name: my-cap-app-db-binding
spec:
  serviceInstanceName: my-cap-app-db
  secretName: my-cap-app-db-secret
```

## Environment variables best practices

Use `.env` locally (never commit!):
```
VCAP_SERVICES=...  # only if testing CF bindings locally
```

In production, rely on service bindings — never hardcode credentials.

```js
// Access bound service credentials
const creds = cds.requires['my-external-service'].credentials
```

## CI/CD pipeline snippet (GitHub Actions)

```yaml
- name: Build and Deploy CAP
  run: |
    npm ci
    npm run build:cf
    cf login -a $CF_API -u $CF_USER -p $CF_PASSWORD -o $CF_ORG -s $CF_SPACE
    cf deploy my-cap-app_1.0.0.mtar
```

## Common mistakes to avoid

- ❌ Deploying without `--production` flag (dev dependencies bloat the image)
- ❌ Committing `.env` or `default-env.json` with real credentials
- ❌ Forgetting to add new BTP services to both `mta.yaml` AND `xs-security.json`
- ❌ Not running `cds build` before `mbt build` (gen/ folder must be fresh)
- ❌ Using `service-plan: application` for destination when `lite` suffices
- ❌ Mixing CF and Kyma deployment targets in the same MTA without separate profiles
