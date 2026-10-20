---
name: author-deployment
description: This skill is used to gather only the necessary code and configuration to deploy a config-driven generated site.
intent: >-
  Deploy a config-driven generated site by collecting only required code and configuration,
  transferring a minimal artifact set, provisioning runtime dependencies, starting services,
  and validating health checks. Includes a troubleshooting appendix derived from real deployment attempts.
type: workflow
best_for:
  - "Deploying one generated site without copying unrelated site folders"
  - "Building a minimal deployment artifact from a monorepo"
  - "Provisioning Node, PM2, and CouchDB for generated service stacks"
  - "Turning repeated shell attempts into one known-good command sequence"
scenarios:
  - "Deploy the somas site to a fresh Linux host"
  - "Package only needed code and config for a generated site"
  - "Set up CouchDB and launch generated services with PM2"
  - "Recover from quoting issues, CouchDB lockout, or partial syncs"
---

# Author Deployment

Gather and execute only the required code and configuration steps needed to deploy a config-driven generated site.

## What This Skill Does

1. Validates remote host prerequisites.
2. Packages a minimal deploy artifact from local source.
3. Transfers and extracts code to remote target paths.
4. Installs only required dependencies.
5. Provisions and validates CouchDB.
6. Launches site services and verifies PM2 state.
7. Applies targeted troubleshooting when health checks fail.

## Build Infrastructure Control Model

Treat deployment behavior as contract-driven and controlled by two artifacts:

1. `build-manifest.json`
- Defines executable action plan, step ordering, payload script paths, and param wiring.
- Any missing step param is a deployment contract bug, not an operator error.

2. `deployment-config.json`
- Defines deploy-time variable descriptors produced from `site-endpoint-config.json` plus baseline descriptors.
- Baseline fallback warnings indicate source/baseline drift and must be resolved deliberately.

Use these files as the single control plane for packaging and remote execution behavior.

## Preconditions

1. Local machine has ssh, scp, tar, and access to deployment key.
2. Remote host is reachable and has sudo/root privileges for package install.
3. Site source exists locally under node_source/sites/<site-name>.
4. Required runtime config files are present, especially site-endpoint-config.json.

## Minimal Deployment Sequence

### Step 1: Verify and provision runtime tools on remote host

Use one idempotent command to ensure curl, tar, gzip, Node 20, npm, and PM2 are available.

### Step 2: Build minimal artifact locally

Create an archive that excludes:
- .git
- node_modules at repo and site level
- unrelated site folders not required for target deployment

Critical rule:
1. If you change any action script, `build-manifest.json`, `deployment-config.json`, or template source, create a fresh build tar before testing deployment.
2. Never validate a script/config fix using an older tar selected in the UI.

### Step 3: Transfer and extract artifact remotely

Copy archive to /opt and extract under /opt/node_source.

### Step 4: Install dependencies remotely

Install in required scopes only:
1. /opt/node_source
2. /opt/node_source/shared-lib
3. /opt/node_source/sites/<site-name>

### Step 5: Provision CouchDB

Preferred path:
1. Install and start system CouchDB service when available.
2. If unavailable in distro repos, run CouchDB container with podman bound to 127.0.0.1:5984.
3. Validate _up endpoint and create target database.

### Step 6: Launch generated site services

Start from site folder using launch.js with skip-npm-install when dependencies are already installed.

### Step 7: Validate deployment health

Check:
1. PM2 process list shows expected services online.
2. CouchDB _up is healthy and target database exists.
3. Site routes respond at gateway endpoint.

## Known Good Command Order

1. Runtime provisioning
2. Artifact package + transfer
3. Extraction
4. Dependency install
5. CouchDB setup
6. Database creation
7. Launch.js + PM2 verification

Avoid interleaving troubleshooting commands into the happy-path run.

## Required Configuration Scope

Collect only these configuration areas for deployment:

1. Site-level endpoint and route config:
- sites/<site-name>/site-endpoint-config.json

2. Shared runtime config consumed by generated services:
- shared-lib and site-generated service import graph

3. Service process startup contracts:
- launch.js behavior
- PM2 runtime state

Do not include unrelated site assets or folders unless explicitly needed by imports.

Note (MUST): The launcher discovers service endpoint fragments only when they are named `endpoint-config.json` and placed directly at `sites/<site>/config/<service>/endpoint-config.json`. This exact folder shape and filename MUST be used. Do not create an inner `endpoint-config/` directory under the service and place the fragment there. Example correct path: `sites/atlas/config/auth/endpoint-config.json`.

## Manifest Contract Rules

1. Any action step that resolves site-local files must receive `siteName` via step params using the same manifest pattern used by neighboring steps.
2. Do not rely on path-derived fallback site resolution when manifest can supply explicit `siteName`.
3. Keep step payload paths and params identical across:
- site manifests
- template manifest
- generated actions shipped in build artifacts
4. After modifying manifest params, verify that remote script argument positions still match script expectations.

## Deployment Config Contract Rules

1. Treat `[build-contract] Using baseline fallback for <service>.<field>` as an explicit drift signal.
2. For fields not required by a service type (for example token on feature UI endpoints), remove stale baseline descriptors rather than tolerating repeated fallback.
3. Keep service-level requirements aligned between:
- `site-endpoint-config.json`
- generated `deployment-config.json`
- runtime assumptions in actions/scripts
4. Resolve contract mismatches at site scope first; do not change shared behavior unless systemic and approved.

## Multi-Site Synchronization Rules

1. When fixing deployment scripts used by multiple sites, update all active site copies and the template source in the same change set.
2. Validate parity with hash or diff checks after copy/sync.
3. Avoid one-site-only hotfixes for shared deployment logic unless intentionally scoped and documented.

## Verification Checklist

1. Remote directory exists:
- /opt/node_source

2. Dependencies present:
- /opt/node_source/node_modules
- /opt/node_source/shared-lib/node_modules
- /opt/node_source/sites/<site-name>/node_modules

3. CouchDB status:
- _up returns status ok
- target DB exists or created successfully

4. Services:
- PM2 lists gateway, auth, site services as online

5. Functional route checks:
- login page and API routes return expected status codes

6. Contract checks:
- `build-manifest.json` step params include required values (especially `siteName` for site-bound scripts)
- `deployment-config.json` has no unexpected baseline fallback warnings for current service contracts
- selected deployment tar timestamp/version is newer than the fix commit/change

## Troubleshooting Appendix

### A) PowerShell quoting and remote shell parsing failures

Symptoms:
- missing ) after argument list
- unexpected token
- bash syntax error near (

Fix:
1. Prefer piping a plain heredoc script into remote bash-s.
2. Avoid deeply nested inline node -e quoting in PowerShell.
3. Use one shell context per script block instead of mixed quoting styles.

### B) Partial or stale deployment content

Symptoms:
- missing site folders after extract
- old generated files still running

Fix:
1. Rebuild archive with explicit excludes.
2. Confirm extracted paths after transfer.
3. Remove excluded site folders remotely if required by deployment policy.

### C) node_modules mismatch

Symptoms:
- runtime import errors
- generated services fail at startup

Fix:
1. Remove stale node_modules trees.
2. Reinstall at repo root, shared-lib, and target site scopes.

### D) CouchDB package unavailable

Symptoms:
- couchdb unit missing after dnf install attempt

Fix:
1. dnf install epel-release
2. dnf install couchdb
3. Bind to 127.0.0.1:6984 and validate _up with retries.

### D1) CouchDB invalid node name on container startup

Symptoms:
- Protocol inet_tcp invalid node name with duplicated prefix pattern

Fix:
1. Use host-only NODENAME input (for example `127.0.0.1`) when image/runtime composes full node name.
2. Validate container state and logs before concluding readiness failure.

### D2) CouchDB readiness probe false negatives

Symptoms:
- container is running but `_up` probe repeatedly times out

Fix:
1. Use polling checks with interval-based retry (check, wait, recheck) instead of fixed one-shot sleeps.
2. Probe candidate hosts in deterministic order (configured host, loopback, localhost) and persist successful host for subsequent checks.
3. Bound all inspect/log/probe operations with explicit timeouts to avoid orchestration ceiling timeouts.

### E) CouchDB account lockout

Symptoms:
- forbidden with account temporarily locked due to authentication failures

Fix:
1. Stop repeated invalid auth attempts.
2. Recreate/rotate container credentials and update site config password.
3. Revalidate with curl _up and DB create before service restart.

### F) Wrong endpoint payload format in tests

Symptoms:
- false negatives from login probes

Fix:
1. Use actual configured route and expected content type.
2. Match form or JSON payload style required by the route handler.

### G) PM2 restarts without effective config alignment

Symptoms:
- services online but behavior still incorrect

Fix:
1. Confirm deployed file contents on remote path.
2. Restart only affected services first, then full launch if needed.
3. Verify logs after one controlled request.

## Anti-Patterns

1. Copying whole monorepo artifacts when only one site deployment is needed.
2. Shipping local node_modules from Windows to Linux target.
3. Running many variant commands without preserving one known-good order.
4. Modifying shared runtime behavior to fix a site-local deployment mismatch without explicit approval.
5. Testing fixes against stale build artifacts that predate manifest/script/config changes.
6. Introducing fixed startup sleeps when an interval poll with timeout provides faster and safer convergence.

## References

- node_source/sites/<site-name>/launch.js
- node_source/sites/<site-name>/site-endpoint-config.json
- node_source/shared-lib
- PM2 process list and logs
- CouchDB _up and database creation checks
