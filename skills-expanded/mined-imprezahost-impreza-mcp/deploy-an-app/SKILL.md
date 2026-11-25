---
name: deploy-an-app
description: Deploy an application to an Impreza VPS — from the curated catalog or straight from a git repository — and follow it to the point where it actually answers. Use when someone asks to install, deploy, host, or put an app on their Impreza server.
---

# Deploying to an Impreza VPS

## Nothing here is synchronous

This is the single thing that goes wrong most often. A deploy call returns an
**id**, not a result. The container is still being pulled while you are reading
the response. If you answer "done" at that point you are guessing, and roughly
half the time you are wrong.

Every long-running family works this way: deploys, backups, scheduled task runs,
app reads and CLI runs. The call starts the work; a second tool reports how it
went.

So the shape of every deploy is:

1. start it, keep the id
2. poll `impreza_list_deployments` (or `impreza_get_environment_deploy` for an
   environment deploy) until the status settles
3. only then say what happened

A deploy that has not settled is not a deploy that failed. Say it is still
running.

## Pick the server first

`impreza_list_servers` shows what the account owns and which boxes are online.
An app has to land on one of those. If the account has no server yet, see the
`start-from-nothing` skill — buying one is a separate arc with its own rules
about money.

## Catalog or custom

**Catalog** (`impreza_list_apps` → `impreza_deploy_catalog_app`) is the fast
path: WordPress, Nextcloud, Gitea, n8n, Vaultwarden and the rest arrive
configured, not at a setup wizard. Prefer it whenever the request names
something in the catalog. Search the catalog before assuming an app is missing.

**Custom** (`impreza_deploy_custom`) takes the customer's own image, Dockerfile
or git repository. Reach for it when the app is theirs.

For a Compose stack, `impreza_prepare_compose` first: it turns the file into
something the platform can accept and tells you what it refused and why. Do not
hand-translate a Compose file yourself.

## After it settles

`impreza_probe_deployment` answers the question the status field does not: is it
reachable over public HTTPS. A deployment can be `running` and still not serve,
because DNS or the certificate is not there yet. If the customer asked for a
working site, probe before you claim one.

## When it fails

Do not redeploy on reflex. A redeploy that repeats the same failure costs the
customer minutes and tells you nothing you did not already know. Read the logs
first — the `diagnose-a-deployment` skill is the whole procedure.

## Things worth knowing before a customer hits them

- **`impreza_redeploy_deployment` keeps the app in place**; it does not recreate
  it and does not change its domain. That was a real defect once, and the fix is
  the behaviour you can now rely on.
- **Environment variables are stored in the clear** on our side. Say so before
  putting a secret in one. `impreza_rotate_build_secrets` exists for the build
  side.
- **`impreza_set_deployment_vars` does not restart anything by itself.** New
  values reach the app on its next start.
- The catalog moves. `impreza_list_apps` is the truth about what exists today;
  a version you remember may be gone.
