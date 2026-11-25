---
name: openpanel-analytics
description: Adds and verifies OpenPanel analytics on Lossless Astro sites and splash pages, deployed on Vercel, GitHub Pages, or both. Covers the production-only Analytics.astro component, the OPENPANEL_CLIENT_ID variable on each host, the OpenPanel "supported domains" setting whose absence silently 401s every event, and a curl-plus-DevTools verification. Use when adding analytics to a site or splash, when a site deployed to a new host or domain, when OpenPanel shows no data, or when the user mentions OpenPanel, analytics, tracking, traffic, or "is anyone visiting".
---

# OpenPanel analytics

Most Lossless Astro sites and every splash page should carry OpenPanel. It's the default analytics for low-traffic sites: one account covers many sites, behavior tracking is richer than a plain page counter, and self-hosting stays an option later. The pattern is the same everywhere, and nearly every failure so far has been configuration, not code.

## Contents

- The component · Environment variable · Per host · OpenPanel dashboard · Verify · Gotchas · Reference

## The component

`src/components/Analytics.astro`, included once in the layout's `<head>`. **exact:** copy it as-is.

```astro
---
// Analytics: OpenPanel, production-only.
const isProd = import.meta.env.PROD;
const openPanelClientId = import.meta.env.OPENPANEL_CLIENT_ID;
---

{isProd && openPanelClientId && (
  <>
    <script is:inline define:vars={{ openPanelClientId }}>
      window.op=window.op||function(){var n=[];return new Proxy(function(){arguments.length&&n.push([].slice.call(arguments))},{get:function(t,r){return"q"===r?n:function(){n.push([r].concat([].slice.call(arguments)))}} ,has:function(t,r){return"q"===r}}) }();
      window.op('init', {
        clientId: openPanelClientId,
        trackScreenViews: true,
        trackOutgoingLinks: true,
        trackAttributes: true,
      });
    </script>
    <script is:inline src="https://openpanel.dev/op1.js" defer async></script>
  </>
)}
```

- **Production-only.** `pnpm dev` and local previews never send events, so they never pollute the dashboard.
- **Inert without a client ID.** No variable means no script: a site can ship the component before its OpenPanel client exists.
- If the site already layers other trackers (Umami, Fathom), keep them in the same component.

## Environment variable

- **`OPENPANEL_CLIENT_ID`** is the only value the browser needs. It's public by design: it appears in the HTML.
- **Never put `OPENPANEL_CLIENT_SECRET` in a site.** Browser tracking doesn't use it. If a repo holds one as a Secret for a site, it's unused and can go.
- Locally: `OPENPANEL_CLIENT_ID=` in `.env.example`, with the value only in a gitignored `.env`.

## Per host

**One OpenPanel client per site.** Name it so it's findable: `splash_<repo>` for splashes, the domain for sites.

| Host | Where the client ID goes | Then |
|---|---|---|
| **GitHub Pages** | Repo Settings → Secrets and variables → Actions → **Variables** (not Secrets) → `OPENPANEL_CLIENT_ID` | The workflow's build step must expose it: `env: OPENPANEL_CLIENT_ID: ${{ vars.OPENPANEL_CLIENT_ID }}`. Re-run the workflow. |
| **Vercel** | Project Settings → Environment Variables → `OPENPANEL_CLIENT_ID` (Production) | Redeploy; existing deployments don't pick it up. |
| **Both** | Both places, same client ID | Add both origins to supported domains (below). |

## OpenPanel dashboard: supported domains

**exact:** each client's **supported domains** must list every origin the site is served from:

- GitHub Pages: `https://lossless-group.github.io/`
- Vercel: the production domain, e.g. `https://<project>.vercel.app`
- Any custom domain

A missing origin makes the API reject every event with **401**, while the script loads and runs normally. This is the most common reason a correctly deployed site shows no data. We once lost a night to it across three splashes.

## Verify

Copy into your reply and tick:

- [ ] `curl -s <site-url> | grep -c 'openpanel.dev/op1.js'` returns 1
      → 0: the variable didn't reach the build. Check the host's variable, the workflow `env:`, and that you redeployed.
- [ ] The client ID in the HTML matches the dashboard you're looking at (not a sibling site's client)
- [ ] In an incognito window **with extensions off** (uBlock, Brave Shields, and Safari blockers all block OpenPanel), DevTools → Network → `api.openpanel.dev/track` returns **200**
      → 401: add the origin to the client's supported domains; no redeploy needed
- [ ] The visit appears in the OpenPanel dashboard within a minute

## Gotchas

- **Don't pin `packageManager` in a Vercel site's `package.json`.** It switches Vercel to a newer pnpm whose build-script gate breaks installs ("Ignored build scripts: esbuild, sharp").
- **A login-aware header doesn't hide analytics.** The component lives in `<head>`; anonymous visitors get it.
- **Vercel deployment thumbnails can show 403** from an old protection setting while the site is fine. Not an analytics problem.
- **The custom-domain move:** add the new origin to supported domains *before* switching DNS, or the first days of real traffic vanish.

## Reference

- Rollout history and per-site status: `context-v/prompts/Setup-Analytics-Across-Sites.md` at the anchor monorepo root.
- Custom events and deeper tracking: `context-v/prompts/Implement-Deeper-Analytics-Tracking.md`, same place.
- Sites already wired (copy from any of them): the splashes of `context-vigilance-kit`, `context-v-corpus`, `content-farm`, `lfm`, and `ai-labs`, plus `mpstaton-site`, `twf_site`, `fullstack-vc`, and `hypernova-site` under `astro-knots/sites/`.
- Composes with `maintain-splash-pages` (every splash gets this) and `astro-knots`.
