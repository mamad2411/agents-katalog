---
name: vercel-platforms
description: Build multi-tenant and multi-project platforms on Vercel — subdomain and custom-domain tenant routing, wildcard DNS, per-tenant SSL, Next.js middleware/proxy resolution, tenant data isolation, programmatic project provisioning via the Vercel SDK, and Platform Elements. Use when a request involves tenants, workspaces, or customer sites served from one app; subdomain routing (`tenant.app.com`); letting customers bring their own domain; wildcard domains; preview URLs per tenant; or spinning up a Vercel project per user. Triggers on multi-tenant, multi-tenancy, tenant routing, subdomain routing, custom domains, wildcard domain, white-label, platform, workspace-per-customer, project-per-user, Vercel for Platforms.
source: vercel.com/docs/platforms@2026-07-25 (re-derived; original cowork capability unavailable on this host)
last-verified: 2026-07-25
---


# Vercel for Platforms

Patterns for serving many customers from Vercel — either **one deployment serving many tenants**
(multi-tenant) or **one Vercel project per tenant** (multi-project).

Upstream docs are at `vercel.com/docs/platforms`; the pages this skill derives from carry
`last_updated: 2026-06-26`. Section-level provenance is recorded in each reference file.

## Pick the model first

This is the decision everything else hangs off. Getting it wrong is expensive to reverse.

| | Multi-tenant (one project) | Multi-project (project per tenant) |
| --- | --- | --- |
| Codebase | One, shared by all tenants | Per-tenant, often generated |
| Isolation | Application-level (tenant ID in every query) | Infrastructure-level (separate builds, functions, env) |
| Deploy | Once, updates every tenant | Per tenant |
| Overhead | Low | High — you manage N projects |
| Choose when | Same app, different content/branding | Tenants ship their own code, or compliance demands hard isolation |

Concretely: a blog or docs platform where every tenant runs identical code is **multi-tenant**.
An AI app-builder where each user's app is different code is **multi-project**.

## Reference map

| File | Covers |
| --- | --- |
| `references/concepts.md` | Tenants, the three identification strategies, data isolation, tenant context propagation |
| `references/routing.md` | Middleware/proxy resolution, rewrite vs redirect, matchers, local dev, preview URL prefixes, custom subpaths |
| `references/domains.md` | Wildcard domains, customer custom domains, verification, SSL, plan gates |
| `references/multi-project.md` | Programmatic project creation, deployments on behalf of users, templates |
| `references/platform-elements.md` | Prebuilt Actions (add-custom-domain, deploy-files) and Blocks (claim-deployment, custom-domain, deploy-popover, dns-table, report-abuse) |

## Gotchas

1. **`middleware.ts` → `proxy.ts` in Next.js 16.** Next 16 renames the convention: the file is
   `proxy.ts` and the exported function is `proxy`, not `middleware`. Vercel's own docs are
   mid-migration and internally inconsistent — `multi-tenant-platforms/custom-subpaths` shows
   `export async function proxy`, while `middleware-and-routing` and `preview-url-prefixes` still
   show `middleware.ts`. The logic is identical; only the filename and export name changed. Check
   your Next major before copying any snippet.

2. **Wildcard domains require Vercel's nameservers.** `*.yourapp.com` only works when the apex
   domain points at `ns1.vercel-dns.com` / `ns2.vercel-dns.com`. A CNAME setup will not issue
   wildcard certificates. This is the single most common multi-tenant setup failure.

3. **Custom domains need a paid plan.** Adding a customer domain on Hobby returns
   `custom_domain_needs_upgrade` ("Domain name creation requires a premium account"). Budget for
   this before designing a bring-your-own-domain flow.

4. **Exclude `www` explicitly when parsing subdomains.** `hostname.split('.')[0]` treats `www` as
   a tenant named "www". Every production resolver needs `www` (and usually `app`, `admin`) on a
   skip list.

5. **Preview URL prefixes need a custom preview suffix.** The `tenant---preview-xyz` form does not
   work on the default `.vercel.app`. The Preview Deployment Suffix is a **billing add-on** —
   included and enabled by default on Enterprise, enable-able on Pro under Settings → Billing →
   Add-Ons — and the suffix domain must itself use Vercel nameservers.

6. **Tenant lookup runs on every request.** Middleware sits in the hot path. Use Edge Config
   (sub-10ms at the edge) or cache the lookup; a per-request database round trip on every page
   view is the usual reason a multi-tenant app feels slow.

7. **Rewrite the tenant root, redirect the admin surface.** These are different operations and
   mixing them up is visible to users — see `references/routing.md` § Rewrite vs redirect.
