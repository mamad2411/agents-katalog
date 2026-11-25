---
name: javascript-deploy-fly
description: >-
  Concrete recipe for deploying a Next.js app built on this kit to Fly.io — flyctl login, launching
  into a shared org, the pnpm-workspace Dockerfile gotcha that breaks the auto-generated build, and
  attaching a managed Postgres. Use when the chosen host is Fly.io: first deploy, "fly launch" /
  "fly deploy" fails or builds a broken image, wiring the app's public base URL, or adding a
  database. Triggers on "fly.io", "flyctl", "fly launch", "fly deploy", "fly.toml", "Dockerfile
  pnpm", "pnpm-lock not copied", "fly mpg", "managed Postgres on Fly", "deploy to Fly".
---

# Deploying to Fly.io

Fly.io is **one** capable Node host — the kit is host-agnostic (see `manifest-and-deploy`; the
architecture wants a Node runtime and a server-only Postgres-style DB). This skill is the concrete
Fly recipe, including two gotchas that will otherwise cost you an afternoon. Placeholders below —
`<your-org>`, `<app-name>`, `<prod-pg-id>` — are yours to fill from your own account; nothing here is
account-specific.

> **Research current Fly behavior at build time.** `flyctl` and the managed-Postgres (`fly mpg`)
> commands evolve; treat `fly help <cmd>` and the docs as the source of truth if a flag below has
> drifted.

## 1. Install & authenticate

- Install `flyctl`: https://fly.io/docs/flyctl/install/
- `fly auth login` — sign in with an account that **belongs to your Fly organization** (an account
  that's a member of `<your-org>`), not a personal-only account.

## 2. Launch into the shared org (not your personal account)

From the app's project root:

```
fly launch --org <your-org>
```

**Pass `--org` explicitly.** Without it, `fly launch` assumes your **personal** account — you can
reassign later, but the flag skips that detour. `launch` walks you through creating the app and
generating `fly.toml` + a `Dockerfile`. It *should* just work — except for the gotcha in §3.

## 3. GOTCHA: the auto-generated Dockerfile drops the pnpm workspace files

Fly's generated `Dockerfile` copies `package.json` but **omits `pnpm-lock.yaml` and
`pnpm-workspace.yaml`**, so the install step inside the image is missing the lockfile/workspace
config and the build fails (or produces a subtly wrong image). Find the line that starts with:

```dockerfile
COPY package.json ...
```

and make it copy all three:

```dockerfile
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
```

Then deploy:

```
fly deploy
```

A successful deploy prints your app's public URL, e.g. `https://<app-name>-<random-suffix>.fly.dev/`.

## 4. Wire the public base URL back into the app

That `*.fly.dev` URL is the app's **public base URL**. Set it wherever this kit consumes the base URL
— the env var validated in `lib/env.ts` and the **manifest's** base + embed URLs — and re-publish, so
the platform embeds the deployed app and not a stale/tunnel URL (see `manifest-and-deploy` for the
coherent-set rule and `javascript-nextjs` for env). Update it via the platform portal or the CLI, per
your workflow.

## 5. Add a managed Postgres (optional — only if the app persists data)

Persisted data must be reached **server-side only**, one connection string, scoped per install — see
`backoffice-data`. To provision Fly managed Postgres (`mpg`):

```
# 1. Find your org's prod managed-Postgres cluster id
fly mpg list --org <your-org>            # note the prod cluster's id → <prod-pg-id>

# 2. Create a database for this app on that cluster
fly mpg db create <prod-pg-id> --name <app-name>-db

# 3. Create a user for it
fly mpg users create <prod-pg-id> --username <app-name>-user --role=schema_admin

# 4. Get the connection string (attach)
fly mpg attach <prod-pg-id> --username <app-name>-user --database <app-name>-db
```

Step 4 yields the **connection string** — put it in the app's DB env var (added to the Zod env schema
in `lib/env.ts` so it's validated on boot), stored as a **Fly secret** (`fly secrets set`), never in
the repo or the client bundle. Keep it server-only. See `manifest-and-deploy` §4 for the
secret-vs-config rules.

## Related skills

- `manifest-and-deploy` — the host-agnostic deploy contract this recipe instantiates: the coherent
  `{app id, app secret, api url, base url}` set, env/secrets discipline, the first-deploy checklist.
- `javascript-nextjs` — the `next build` gate, the `lib/env.ts` Zod schema every new var joins, and
  the Node-runtime requirement (Fly runs your Dockerfile, so ensure a full Node runtime).
- `backoffice-data` — why the DB is server-only and how to scope rows per install.
- `javascript-testing` — the lint → typecheck → test → build gate to keep green before `fly deploy`.
