---
name: cf-cli
description: >
  Comprehensive Cloud Foundry CLI (cf CLI v8) assistant for generating commands, automating
  app deployments, managing services, and troubleshooting errors. Use this skill whenever
  the user mentions "cf", "cf cli", "Cloud Foundry", "cf push", "cf login", "cf target",
  app deployment to CF, service binding, buildpacks, routes, domains, orgs and spaces,
  manifests, or any task involving the Cloud Foundry command line — even if they just say
  something like "push my app" or "how do I bind a service". Also trigger when the user
  asks about scaling apps, managing environment variables in CF, creating user-provided
  services, rolling deployments, SSH into app containers, or writing CF manifests.
---

# Cloud Foundry CLI Skill

You are an expert in the Cloud Foundry CLI (v8). Help users construct correct `cf` commands, write manifests, automate deployments, manage services, and troubleshoot issues. The goal is to save the user from constantly running `cf help` by giving them precise, runnable commands.

**Important:** v7 and v6 are no longer maintained. Always use v8 syntax. The v8 CLI is backed by the CC API v3.

## Installation

Install from the [V8 Installation Guide](https://github.com/cloudfoundry/cli/wiki/V8-CLI-Installation-Guide). Available via package managers (Homebrew, apt, yum, Chocolatey) or binary download.

Verify: `cf version`

## Authentication & Targeting

### cf api

Sets the API endpoint for your Cloud Foundry instance.

```bash
cf api https://api.example.com
cf api https://api.example.com --skip-ssl-validation   # dev/self-signed certs only
cf api                                                   # show current API
```

### cf login

Interactive login — prompts for anything not provided:

```bash
cf login                                                # fully interactive
cf login -a https://api.example.com                     # set API + login
cf login -a https://api.example.com -u user@example.com # preset username
cf login -a https://api.example.com --sso               # SSO via one-time passcode
cf login -o my-org -s dev                               # target org + space on login
```

| Flag | Description |
|------|-------------|
| `-a` | API endpoint URL |
| `-u` | Username |
| `-p` | Password (avoid — recorded in shell history) |
| `-o` | Target organization |
| `-s` | Target space |
| `--sso` | SSO via one-time passcode from the login URL |
| `--sso-passcode <code>` | Provide SSO passcode directly |
| `--origin <origin>` | Specify identity provider origin |
| `--skip-ssl-validation` | Skip SSL cert verification |

### cf auth

Non-interactive authentication for scripts and CI/CD:

```bash
cf auth username password
cf auth username password --origin ldap
cf auth --client-credentials                    # uses CF_USERNAME and CF_PASSWORD env vars
```

### cf target

Switches org and space context after login:

```bash
cf target -o my-org -s dev
cf target -s staging                            # switch space only
cf target                                       # show current target
```

### cf logout

```bash
cf logout
```

## App Lifecycle

### cf push (alias: `p`)

The most important command — deploys an app.

```bash
cf push my-app                                           # push from current dir
cf push my-app -p ./build                                # push specific path
cf push my-app -f manifest.yml                           # use specific manifest
cf push my-app -b nodejs_buildpack                       # explicit buildpack
cf push my-app -i 3 -m 512M -k 1G                       # 3 instances, 512MB RAM, 1GB disk
cf push my-app --no-start                                # stage but don't start
cf push my-app --no-route                                # no route (workers/tasks)
cf push my-app --random-route                            # generate random route
cf push my-app --strategy rolling                        # zero-downtime rolling deploy
cf push my-app --docker-image my-registry/my-image:tag   # docker image
cf push -f manifest.yml --var host=my-host               # variable substitution
cf push -f manifest.yml --vars-file vars.yml             # vars from file
```

Key flags: `-b` buildpack, `-c` command, `-f` manifest, `-i` instances, `-k` disk, `-m` memory, `-p` path, `-s` stack, `-t` timeout, `-u` health-check-type (`port`/`http`/`process`), `-o/--docker-image`, `--docker-username` (password via `CF_DOCKER_PASSWORD`), `--droplet`, `--endpoint`, `--no-manifest`, `--no-route`, `--no-start`, `--no-wait`, `--random-route`, `--strategy` (`rolling`/null), `--task`, `--var KEY=VALUE`, `--vars-file PATH`.

**Push env vars:** `CF_DOCKER_PASSWORD`, `CF_STAGING_TIMEOUT=15` (min), `CF_STARTUP_TIMEOUT=5` (min).

### App Management

```bash
cf apps                          # list all apps in current space
cf app my-app                    # show app details (instances, memory, routes, state)
cf start my-app                  # start a stopped app
cf stop my-app                   # stop a running app
cf restart my-app                # restart (re-containerize, same droplet)
cf restage my-app                # restage (re-build droplet from source)
cf delete my-app                 # delete app (prompts for confirmation)
cf delete my-app -f              # force delete (no confirmation)
cf delete my-app -r              # also delete mapped routes
cf rename my-app new-name        # rename an app
cf scale my-app -i 5             # scale to 5 instances
cf scale my-app -m 1G -k 2G     # change memory and disk
cf scale my-app -i 5 -m 1G      # scale instances and memory together
```

### Deployment & Rollback

```bash
cf push my-app --strategy rolling          # zero-downtime rolling deploy
cf cancel-deployment my-app                # cancel an in-progress deployment
```

### Logs & Events

```bash
cf logs my-app                   # tail live logs
cf logs my-app --recent          # dump recent logs
cf events my-app                 # show recent app events (crashes, scaling, etc.)
```

### SSH

```bash
cf ssh my-app                              # SSH into first instance
cf ssh my-app -i 2                         # SSH into instance index 2
cf ssh my-app -c "cat /app/config.yml"     # run a command and exit
cf enable-ssh my-app / cf disable-ssh my-app / cf ssh-enabled my-app
```

### Tasks

```bash
cf run-task my-app --command "rake db:migrate"    # run a one-off task
cf run-task my-app -c "rake db:migrate" -m 512M   # with memory limit
cf tasks my-app                                    # list tasks
cf terminate-task my-app TASK_ID                   # cancel a running task
```

### Environment Variables

```bash
cf env my-app                              # show all env vars (user + system)
cf set-env my-app DATABASE_URL "postgres://..."    # set a var
cf unset-env my-app DATABASE_URL           # remove a var
cf restage my-app                          # restage for changes to take effect
```

After `set-env` or `unset-env`, you need to restage or restart the app for changes to apply.

### Health Checks

```bash
cf get-health-check my-app
cf set-health-check my-app http --endpoint /health
cf set-health-check my-app port
cf set-health-check my-app process
```

### Packages & Droplets

```bash
cf packages my-app / cf create-package my-app      # list / upload packages
cf droplets my-app / cf set-droplet my-app GUID     # list / set active droplet
cf download-droplet my-app / cf stage-package my-app --package-guid GUID
```

## Manifests

The manifest (`manifest.yml`) declares app configuration. CF reads it automatically from the current directory during `cf push`.

```yaml
---
applications:
- name: my-app
  memory: 512M
  disk_quota: 1G
  instances: 2
  buildpacks:
  - nodejs_buildpack
  command: node server.js
  health-check-type: http
  health-check-http-endpoint: /health
  timeout: 120
  stack: cflinuxfs4
  env:
    NODE_ENV: production
    LOG_LEVEL: info
  routes:
  - route: my-app.example.com
  - route: my-app.example.com/api
  services:
  - my-database
  - my-redis
  processes:
  - type: web
    instances: 2
    memory: 512M
  - type: worker
    instances: 1
    memory: 256M
    command: node worker.js
    health-check-type: process
    no-route: true
```

**Variable substitution** in manifests:
```yaml
# manifest.yml
applications:
- name: ((app-name))
  instances: ((instances))
```
```bash
cf push --var app-name=my-app --var instances=3
# or from a file:
cf push --vars-file production.yml
```

**Create manifest from running app:**
```bash
cf create-app-manifest my-app              # generates manifest.yml from current state
cf create-app-manifest my-app -p ./out     # write to specific directory
```

## Services

### Marketplace

```bash
cf marketplace                              # list all available services
cf marketplace -e SERVICE_NAME              # show plans for a specific service
cf marketplace -s SERVICE_NAME              # alias for -e
```

### Service Instances

```bash
cf services                                # list service instances in current space
cf service my-db                           # show details for a service instance

# Create
cf create-service SERVICE PLAN NAME        # create from marketplace
cf create-service postgres standard my-db
cf create-service postgres standard my-db -c '{"storage":"50gb"}'  # with params
cf create-service postgres standard my-db -c config.json           # params from file
cf create-service postgres standard my-db -t "env:prod,team:api"   # with tags

# Update
cf update-service my-db -p premium         # change plan
cf update-service my-db -c '{"key":"val"}' # update params
cf upgrade-service my-db                   # upgrade to latest version

# Delete
cf delete-service my-db
cf delete-service my-db -f                 # no confirmation

cf rename-service my-db new-db-name
```

### Binding & Unbinding

```bash
cf bind-service my-app my-db               # bind service to app
cf bind-service my-app my-db -c '{"role":"admin"}'  # with config
cf unbind-service my-app my-db             # unbind
cf restage my-app                          # restage to pick up new bindings
```

Binding injects credentials into `VCAP_SERVICES` env var.

### Service Keys

Service keys let you get credentials without binding to an app:

```bash
cf create-service-key my-db my-key
cf create-service-key my-db my-key -c '{"permissions":"read-only"}'
cf service-keys my-db                       # list keys
cf service-key my-db my-key                 # show credentials
cf delete-service-key my-db my-key
```

### User-Provided Services

For external services not in the marketplace:

```bash
# Interactive (prompts for each param)
cf create-user-provided-service my-ext -p "host, port, username, password"

# Non-interactive (JSON)
cf cups my-ext -p '{"host":"db.example.com","port":"5432","user":"admin","password":"secret"}'

# Syslog drain
cf cups my-logger -l syslog://logs.example.com:514

# Route service
cf cups my-proxy -r https://proxy.example.com

# Update
cf update-user-provided-service my-ext -p '{"password":"new-secret"}'
```

`cups` is the alias for `create-user-provided-service`, `uups` for `update-user-provided-service`.

### Service Sharing & Route Services

```bash
cf share-service my-db -s other-space [-o other-org]
cf unshare-service my-db -s other-space
cf bind-route-service example.com my-proxy --hostname my-app
cf unbind-route-service example.com my-proxy --hostname my-app
```

## Routes & Domains

### Domains

```bash
cf domains                                          # list all domains
cf create-private-domain my-org apps.internal        # internal/private domain
cf delete-private-domain apps.internal
cf create-shared-domain shared.example.com           # shared across all orgs
cf delete-shared-domain shared.example.com
cf router-groups                                     # list router groups
```

### Routes

```bash
cf routes                                            # list all routes in current space
cf route my-app.example.com                          # show route details

cf create-route example.com --hostname my-app        # create route
cf create-route apps.internal --hostname backend      # internal route
cf create-route example.com --hostname my-app --path /api  # with path

cf map-route my-app example.com --hostname my-app    # map route to app
cf unmap-route my-app example.com --hostname my-app  # unmap

cf delete-route example.com --hostname my-app        # delete route
cf delete-orphaned-routes                             # clean up unmapped routes

cf check-route example.com --hostname my-app          # check if route exists
```

## Orgs & Spaces

### Organizations

```bash
cf orgs                          # list orgs
cf org my-org                    # show org details (spaces, domains, quotas)
cf create-org my-org
cf delete-org my-org
cf rename-org my-org new-org
```

### Spaces

```bash
cf spaces                        # list spaces in current org
cf space dev                     # show space details
cf create-space staging
cf delete-space staging
cf rename-space staging production
cf apply-manifest -f manifest.yml  # apply manifest to current space
```

### Space SSH

`cf allow-space-ssh SPACE` / `cf disallow-space-ssh SPACE` / `cf space-ssh-allowed SPACE`

## User & Role Management

```bash
cf org-users my-org                                              # list org users
cf space-users my-org dev                                        # list space users
# Org roles: OrgManager, BillingManager, OrgAuditor
cf set-org-role user@example.com my-org OrgManager
cf unset-org-role user@example.com my-org OrgManager
# Space roles: SpaceManager, SpaceDeveloper, SpaceAuditor, SpaceSupporter
cf set-space-role user@example.com my-org dev SpaceDeveloper
cf unset-space-role user@example.com my-org dev SpaceDeveloper
```

## Administration

**Buildpacks:** `cf buildpacks` (list), `cf create-buildpack NAME PATH POSITION`, `cf update-buildpack NAME -p PATH`, `cf delete-buildpack NAME`.

**Network policies:** `cf network-policies`, `cf add-network-policy APP DEST --protocol tcp --port 8080`, `cf remove-network-policy APP DEST --protocol tcp --port 8080`.

**Security groups:** `cf security-groups`, `cf create-security-group NAME rules.json`, `cf bind-security-group NAME ORG SPACE --lifecycle running`, `cf bind-running-security-group NAME` (global default).

**Quotas:** `cf org-quotas`, `cf create-org-quota NAME -m 10G -i 100 -r 50 -s 20`, `cf set-org-quota ORG QUOTA`. Space quotas: `cf space-quotas`, `cf create-space-quota NAME -m 5G`, `cf set-space-quota SPACE QUOTA`.

**Feature flags:** `cf feature-flags`, `cf enable-feature-flag FLAG`, `cf disable-feature-flag FLAG`.

## Advanced Commands

### cf curl

Direct API calls — invaluable for automation and debugging:

```bash
cf curl /v3/apps                              # list apps via API
cf curl /v3/apps/APP_GUID                     # get specific app
cf curl /v3/apps -X POST -d '{"name":"my-app","relationships":{"space":{"data":{"guid":"SPACE_GUID"}}}}'
cf curl "/v3/apps?names=my-app"               # query by name
```

### cf config

```bash
cf config --trace true                # enable API tracing (like CF_TRACE=true)
cf config --trace /tmp/cf-trace.log   # trace to file
cf config --color false               # disable colored output
cf config --locale en-US              # set locale
```

### cf oauth-token

```bash
cf oauth-token                        # print current access token (for scripting)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CF_HOME` | Override `~/.cf` config directory location |
| `CF_TRACE` | `true` to enable API tracing, or a file path for trace logs |
| `CF_COLOR` | `false` to disable colored output |
| `CF_DOCKER_PASSWORD` | Docker registry password for `cf push --docker-image` |
| `CF_STAGING_TIMEOUT` | Max minutes to wait for staging (default: 15) |
| `CF_STARTUP_TIMEOUT` | Max minutes to wait for app start (default: 5) |
| `CF_DIAL_TIMEOUT` | Max seconds for API connection (default: 5) |

## Plugins

```bash
cf plugins                                          # list installed plugins
cf install-plugin PLUGIN                            # install (local path, URL, or repo name)
cf install-plugin -r CF-Community my-plugin         # from registered repo
cf uninstall-plugin my-plugin
cf repo-plugins                                     # list available plugins
cf list-plugin-repos                                # list registered repos
cf add-plugin-repo CF-Community https://plugins.cloudfoundry.org
cf remove-plugin-repo CF-Community
```

Plugin code uses `import "code.cloudfoundry.org/cli/v9/plugin"`.

## MTA / Multiapps Plugin (`cf deploy`)

CAP applications and MTA projects are deployed as `.mtar` archives using the `multiapps` CF CLI plugin. This provides the `cf deploy` command (distinct from `cf push`).

### Install the plugin and build tool

Before running `mbt build` or `cf deploy`, verify both tools are present. Run these checks and install if missing:

```bash
# Check and install mbt (MTA Build Tool)
if ! command -v mbt &>/dev/null; then
  echo "mbt not found — installing..."
  npm install -g mbt
else
  echo "mbt $(mbt --version) already installed"
fi

# Check and install the multiapps CF CLI plugin
if ! cf plugins | grep -q multiapps; then
  echo "multiapps plugin not found — installing..."
  cf install-plugin multiapps -f
else
  echo "multiapps plugin already installed"
  cf plugins | grep multiapps
fi
```

### Build and deploy an MTA

```bash
# Build the .mtar archive from mta.yaml
mbt build

# Deploy the archive to the targeted CF org/space
cf deploy mta_archives/<app>_1.0.0.mtar

# Deploy with verbose output
cf deploy mta_archives/<app>_1.0.0.mtar -e config.mtaext

# Check deploy status
cf mta-ops                          # list ongoing MTA operations
cf mta <mta-id>                     # show MTA status
cf mtas                             # list all deployed MTAs
cf undeploy <mta-id> --delete-services  # remove an MTA + its services
```

### Troubleshooting `cf deploy`

| Error | Cause | Fix |
|-------|-------|-----|
| `unknown command 'deploy'` | multiapps plugin not installed | `cf install-plugin multiapps` |
| `service plan 'extended' not available` | AI Core extended plan not entitled or org plan restricted | Check BTP entitlements; `extended` plan required for CAP with AI Core |
| `MTA ID already exists` | Previous deploy left partial state | `cf undeploy <mta-id>` then retry |
| Build fails with `npm` errors | Node version mismatch in `mta.yaml` | Ensure `engines.node` in `package.json` matches CF buildpack version |

## Troubleshooting

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `FAILED - Not logged in` | Token expired or not authenticated | Run `cf login` again |
| `FAILED - No org/space targeted` | Missing target context | Run `cf target -o ORG -s SPACE` |
| App crashes on push | Bad start command or missing deps | Check `cf logs APP --recent` for errors |
| Staging fails | Wrong buildpack or missing files | Verify buildpack with `-b`, check `.cfignore` |
| `CF_STAGING_TIMEOUT` exceeded | App takes too long to stage | Increase `CF_STAGING_TIMEOUT` or optimize build |
| SSL cert errors | Self-signed certs | Use `--skip-ssl-validation` (dev only) or install certs |
| Route already exists | Another app/space owns the route | Use `cf routes` to find it, or use `--random-route` |
| Service bind fails | Service not ready or wrong space | Check `cf service SERVICE` status |

### Debugging Steps

1. **Check logs:** `cf logs my-app --recent` — always the first thing to try
2. **Enable tracing:** `CF_TRACE=true cf push my-app` — see API requests/responses
3. **Check events:** `cf events my-app` — see recent crashes, restages, scaling
4. **SSH in:** `cf ssh my-app` — inspect the running container
5. **Check env:** `cf env my-app` — verify `VCAP_SERVICES` and user env vars
6. **API debug:** `cf curl /v3/apps/GUID/processes` — inspect process-level details

### Verifying Command Success

```bash
cf push my-app
echo $?    # 0 = success, non-zero = failure
```

## Common Workflows

### Deploy a Node.js app with a Postgres service

```bash
cf login -a https://api.example.com --sso
cf target -o my-org -s dev
cf create-service postgres standard my-db
cf push my-app -b nodejs_buildpack
cf bind-service my-app my-db
cf restage my-app
```

### Zero-downtime deployment

```bash
cf push my-app --strategy rolling
# If something goes wrong mid-deploy:
cf cancel-deployment my-app
```

### CI/CD pipeline pattern

```bash
cf api https://api.example.com
cf auth "$CF_USERNAME" "$CF_PASSWORD"
cf target -o my-org -s production
cf push my-app -f manifest-prod.yml --strategy rolling --no-wait
```

### Scale based on load

```bash
cf scale my-app -i 10              # scale out to 10 instances
cf scale my-app -m 1G              # increase memory per instance
```
