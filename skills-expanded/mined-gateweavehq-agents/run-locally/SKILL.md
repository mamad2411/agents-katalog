---

name: run-locally
description: Start Gateweave Agents locally (Workers, D1 and Durable Objects via Vite) and check a change in a real browser - sign up, create a workspace, and walk through the pages. Use for UI changes and for confirming a flow end to end.
---

# Run Gateweave Agents locally and check a change

## Start

```sh
pnpm doctor       # toolchain, setup and port check, with fixes
pnpm dev:setup    # first time only: .dev.vars + local D1 migrations
pnpm dev          # http://localhost:4720
```

- Gateweave products use 47xx ports (site 4700, Track 4710, Agents 4720), and `pnpm dev`
  fails instead of moving when 4720 is taken. Check whether an Agents dev server is already
  running and reuse it. Otherwise pick another port:
  `pnpm --filter @gateweave/agents-web exec vite dev --port 4721`.
- Don't run two dev servers at once. They would share the local state in
  `apps/web/.wrangler/state`.
- Server code reloads on save. After installing a dependency, restart the server.

## Walk through the app

1. Open `/login?mode=sign-up` and create an account with any email and password. Without
   `EMAIL_FROM` in `.dev.vars`, nothing is sent and no verification is needed.
2. Create a workspace on `/`. It opens at `/<slug>` with the sidebar.
3. Check the page you changed, then the members page (`/<slug>/settings/members`): inviting
   creates a link to share.

## Reset local data

Stop the dev server first. To start over, delete `apps/web/.wrangler/state` (all local users and
workspaces) and run `pnpm dev:setup` again.
