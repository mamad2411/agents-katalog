---
name: convex-clerk-project-setup
displayName: Convex + Clerk project setup
description: "Wire Clerk auth into a Convex + Vite app, and diagnose a sign-in that half-works."
disable-model-invocation: true
version: 1.0.0
tags: [convex, clerk, auth, vite, tailscale]
---

# Convex + Clerk setup

Auth spans three config stores that must agree. Most breakage is one of them naming a different thing than the other two.

| Store | Holds | Set via |
|---|---|---|
| Clerk dashboard | Convex integration activated, or a JWT template named `convex` | Clerk UI only |
| Convex deployment | `CLERK_JWT_ISSUER_DOMAIN` | `npx convex env set` or Convex dashboard |
| Repo | `auth.config.ts` provider, `.env.local` | edit + `npx convex dev` |

Token path: Clerk mints a JWT carrying `aud: "convex"`, the browser sends it to Convex, Convex matches `iss` against `CLERK_JWT_ISSUER_DOMAIN` and `aud` against `applicationID`, then fetches signing keys from the issuer's JWKS endpoint.

## Two ways Clerk mints that token

Establish which one you are on before diagnosing anything, because it decides what the network tab should show.

`ConvexProviderWithClerk` picks at runtime. From convex 1.44.0, `dist/esm/react-clerk/ConvexProviderWithClerk.js`:

```js
if (sessionClaims?.aud === "convex") {
  return await getToken({ skipCache: forceRefreshToken });        // native integration
} else {
  return await getToken({ template: "convex", skipCache: ... });  // legacy template
}
```

| Path | Set up by | Token request |
|---|---|---|
| Native integration | Activating Convex at `dashboard.clerk.com/apps/setup/convex`. Clerk's default session token then carries `aud: "convex"`. | `POST /v1/client/sessions/<sid>/tokens` |
| Legacy template | Hand-creating a JWT template named `convex` | `POST /v1/client/sessions/<sid>/tokens/convex` |

Both work, and an existing template keeps working after the integration exists. `applicationID: "convex"` is correct on either path, since Convex matches it against `aud`.

## Diagnose first

Signed into Clerk but not Convex is the signature failure: `UserButton` renders, `<Authenticated>` does not. Clerk's session is client-side and independent, so the header looking right proves nothing about Convex.

Work the symptom:

| Observation | Cause |
|---|---|
| Vite is serving, but `.env.local` has no `CONVEX_DEPLOYMENT` and nothing listens on 3210 | `convex dev` is parked on an interactive prompt (login, team, project, cloud-vs-local). `--start` launched the frontend anyway, so the page loads while the backend was never configured. Read that terminal. |
| `POST .../tokens/convex` → **404** | Legacy path with no template. A misconfigured template gives a 4xx with an error body, not Not Found. On the native integration this request never fires at all, and its absence is normal. |
| No token request on **either** URL | `ConvexProviderWithClerk` not wrapping the tree, or `useAuth` not passed |
| WS connects to a different host than `VITE_CONVEX_URL` names | stale dev server, since Vite inlines env at build time |
| Mixed-content block in console | page is HTTPS, `VITE_CONVEX_URL` is `http://` |
| Token sent, still unauthenticated | `iss`/`aud` mismatch. Compare the decoded token against the deployment env var and `applicationID`. |
| Auth fails only on a LAN or tailnet origin, works on localhost | Check `window.isSecureContext` in that tab. Plain HTTP on a non-localhost host is an insecure context, and Clerk's session handling wants `Secure` cookies and `crypto.subtle`. localhost is exempt, a hostname is not. |

Check which deployment the frontend actually talks to before trusting any backend config. `npx convex env list` targets whatever `CONVEX_DEPLOYMENT` names, which is not necessarily what `VITE_CONVEX_URL` points at. After switching from an anonymous local backend to a cloud one, config lands on the new deployment while the browser may still hit the old one, and the old local backend keeps answering on `127.0.0.1:3210`, so it fails silently.

Done when the token request returns 200 (`/tokens` native, `/tokens/convex` legacy) and `ctx.auth.getUserIdentity()` is non-null inside a query.

## Setup

Order matters. The deployment has to exist before you can set an env var on it, and the provider reads that var.

1. **Activate the Convex integration** at `dashboard.clerk.com/apps/setup/convex` with the right app selected. This replaces hand-creating a JWT template.

   Instances are separate. Confirm the dashboard reads **Development** for a `pk_test_` key, since an integration activated on Production leaves dev failing.

   Legacy alternative, still supported: **Configure → JWT Templates → New template → Convex preset**, named exactly `convex`, lowercase, because `getToken({ template: "convex" })` looks it up by name.

2. **Create the deployment**, choosing cloud rather than the anonymous local backend:

   ```
   npx convex dev --configure new
   ```

   It writes `CONVEX_DEPLOYMENT` and `VITE_CONVEX_URL` into `.env.local`. Verify with `grep VITE_CONVEX_URL .env.local`, which must show `.convex.cloud` and not `127.0.0.1`.

3. **Set the issuer on that deployment:**

   ```
   npx convex env set CLERK_JWT_ISSUER_DOMAIN https://<slug>.clerk.accounts.dev
   ```

   Backend-only. Convex reads its env from the deployment, never from `.env.local`. A copy in `.env.local` is inert, since it is unprefixed so the frontend never sees it either, and it misleads during a later debug.

4. **Uncomment the provider** in `convex/auth.config.ts`. It ships with an empty `providers: []`, which silently rejects every token:

   ```ts
   providers: [
     { domain: process.env.CLERK_JWT_ISSUER_DOMAIN as string, applicationID: "convex" },
   ]
   ```

   The `as string` satisfies TypeScript, not Convex. If you enable the provider before step 3 lands, expect the push to complain about an undefined domain.

5. **Push it** with `npx convex dev` (or `--once`). Config changes only take effect once deployed.

6. **Hard-reload**, since the client caches the failed token fetch.

7. **Initialize shadcn/ui** for the Vite app:

   ```
   pnpm dlx shadcn@latest init --template vite
   ```

8. **Ask the user to add the shadcn/ui agent skill** by running:

   ```
   pnpm dlx skills add shadcn/ui
   ```

### Naming the issuer

`domain` takes the bare origin, no path and no trailing slash:

```
https://<slug>.clerk.accounts.dev
```

Three lookalikes that all fail:

- **JWKS URL** (`.../.well-known/jwks.json`). Convex appends that path itself, so passing it produces a doubled path and no keys. `domain` is matched against `iss`, which is the bare origin.
- **`https://api.clerk.com`**, Clerk's Backend API for server-side user management via `sk_...`. Shared across all Clerk apps, so it can never be an instance's issuer.
- **The production issuer** while running a `pk_test_` key.

The issuer is derivable from the publishable key. `pk_test_<base64>` decodes to the frontend API host, so `base64 -d` on that segment gives you the answer without opening the dashboard.

## Reaching the app from another device

`VITE_CONVEX_URL` is inlined into the **browser** bundle, so a loopback address resolves on the viewing device. From a phone, another machine, or a Tailscale host, `http://127.0.0.1:3210` points at that device's own loopback and the websocket dies.

**Use a cloud deployment.** It is the shortest path by a wide margin: `https://<slug>.convex.cloud` is reachable from anywhere, needs no proxy, and cannot trigger mixed content. Nothing about the backend needs exposing.

Then make Vite itself reachable, which takes two changes that are easy to confuse:

```jsonc
// package.json — without --host, Vite binds loopback and the remote device
// never reaches it. allowedHosts alone does not fix this.
"dev": "convex dev --start 'vite --host'"
```

```ts
// vite.config.ts — Vite rejects unknown Host headers even when bound broadly
server: { allowedHosts: ["<host>.ts.net"] }
```

Restart the dev server after any env change, since HMR does not pick those up.

Notes:

- Serving the page over plain HTTP on a hostname gives an insecure context, which breaks Clerk while leaving Convex fine. `tailscale serve --https=443 http://localhost:<port>` fixes it, and because the backend is already HTTPS there is nothing to proxy. That changes the origin to `https://<host>.ts.net` with no port, which is also the value Clerk's allowed origins needs.
- A second project's Vite lands on 5174 rather than 5173. The port is part of both `allowedHosts` reachability and the URL you hand out, so confirm it with `ss -ltnp | grep 517`.
- `VITE_CONVEX_SITE_URL` is unused by the starter template. Only set it once client code calls HTTP actions.
- Vite's `server.allowedHosts` guards Vite's own Host header only. Convex is a separate process that never sees it and needs no equivalent setting.

### Local backend fallback

Only if you need it offline. The local backend already binds `0.0.0.0`, so verify with `ss -ltnp | grep 321` and point both URLs at a host the browser can reach:

```
VITE_CONVEX_URL=http://<host>:3210
VITE_CONVEX_SITE_URL=http://<host>:3212
```

Serving the page over HTTPS now requires an HTTPS proxy in front of Convex too, or the browser blocks the `http://` connection as mixed content. This is the reason to prefer cloud.

## Production

Each Clerk instance carries its own integration state, templates, and issuer. Going to production means activating the Convex integration again on the Production instance and pointing the prod Convex deployment's `CLERK_JWT_ISSUER_DOMAIN` at that instance's issuer, which is a different hostname from the dev one.
