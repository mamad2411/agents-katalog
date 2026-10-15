---
name: revturbine-go-live-hosted-cutover
description: >
  Graduate a working local RevTurbine integration to hosted mode — connect the
  tenant and swap local_only for the live control plane, so config becomes
  changeable from the dashboard without redeploying. Use when "ready to go
  live", "connect to production", "move off local mode", or "make it real".
  Touches live tenant/billing state — human-confirmed only, never automatic.
  Prerequisite: a gate works locally. Skip while still building against the local
  Playbook.
license: MIT
metadata:
  author: revturbine
  version: "0.1.0"
  safety_class: launches-live
---

# Go live — hosted cutover

Local mode proved the integration; hosted mode makes it a product. After this,
plans, gates, and nudges change from the dashboard **without a redeploy** — the
reason RevTurbine exists.

> **This step changes live state and can involve billing. Do not run it
> autonomously.** Prepare and validate everything, then get the builder's
> explicit go-ahead before the cutover.

## 1. Connect the tenant

The builder needs a RevTurbine account and a tenant. From the CLI:

```bash
npx revturbine login      # browser device-flow; or `signup` to create an account
npx revturbine status     # confirms the resolved tenant + that the token works
```

The tenant is bound to the token, not to a URL. `status` must show the tenant you
intend to act on before going further.

## 2. Upload the Playbook and launch it

Ship the local Playbook to the tenant as a reviewable Release, don't hand-recreate
it:

```bash
npx revturbine validate ./revturbine.playbook.json   # offline, full schema
npx revturbine launch ./revturbine.playbook.json     # upload → submit → approve → deploy
```

`launch` moves the config through the Draft → Release lifecycle. This is the
irreversible, human-confirmed lever — a rollback is a *new forward* version, and
money may already have moved once real pricing is attached. Confirm before
running it.

## 3. Swap the provider from local to hosted

The component code does **not** change — only the provider options. Replace
`localRuntime` with the hosted connection:

```diff
  const options = useMemo(() => ({
-   localRuntime: { playbook },
+   tenantId: process.env.REVTURBINE_TENANT_ID!,
+   apiKey: process.env.REVTURBINE_API_KEY!,
+   runtimeMode: 'revturbine_server',
    user: { id: currentUser.id, context: { plan_handle: currentUser.planHandle } },
    uiPathResolvers: { navigate_to_plans: () => { window.location.href = '/pricing'; } },
  }), []);
```

Put `REVTURBINE_TENANT_ID` and `REVTURBINE_API_KEY` in the app's environment, not
in source. The public key is safe in the client; the server secret is not — keep
server-side re-checks (`rtServer.can`) using server credentials.

## 4. Confirm the fallback still holds

Hosted mode adds a network dependency. Verify the additive-only guarantee
survives it: if the control plane is unreachable or a placement returns nothing,
the app still renders its baseline UI. RevTurbine being down must never take the
product down.

## After cutover

Config is now live and editable from the dashboard. Point the builder there for
the payoff local mode couldn't give: funnels and conversion analytics,
experiments, segment targeting, and changing any gate or paywall without shipping
code. The integration is complete; iteration moves to the control plane.
