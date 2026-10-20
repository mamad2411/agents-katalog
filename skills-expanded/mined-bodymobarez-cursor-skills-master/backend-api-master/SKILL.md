---
name: backend-api-master
description: Master hub for Backend, APIs & data. Use for backend, REST/GraphQL APIs, auth, MFA, databases, payments, webhooks (integrations-pro patterns), QR/GS1, Google Sign-In, GPS & GIS. For GitHub, Slack, CRM, cloud, iPaaS and 80+ SaaS integrations use integrations-master. Bundles 19 skills.
---

# Backend, APIs & data — Master Hub

Use for backend, REST/GraphQL APIs, auth, databases, payments, and integrations.

## How to use this hub

This single skill bundles **all 19 backend api skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **adding-api-docs** — Generate OpenAPI/Swagger documentation for an API, including endpoint schemas, request/response types, and interactive docs UI.  
  → `skills/adding-api-docs/GUIDE.md`
- **adding-auth** — Add authentication to a web application using NextAuth.js (Auth.js), including OAuth providers, session management, and protected routes.  
  → `skills/adding-auth/GUIDE.md`
- **adding-stripe** — Integrate Stripe payments into a web application, including checkout sessions, webhooks, and customer portal.  
  → `skills/adding-stripe/GUIDE.md`
- **cursor-skills-api** — API development rules for Cursor — REST, GraphQL, gRPC, authentication, versioning, and API design. Use when building or documenting APIs.  
  → `skills/cursor-skills-api/GUIDE.md`
- **cursor-skills-integrations** — Integration development rules for Cursor — webhooks, message queues, databases, microservices, and service mesh patterns.  
  → `skills/cursor-skills-integrations/GUIDE.md`
- **cursor-skills-node** — Node.js development rules for Cursor — Express, NestJS, Next.js, npm, TypeScript, and async patterns. Use for Node.js or JavaScript backend work.  
  → `skills/cursor-skills-node/GUIDE.md`
- **cursor-skills-php** — PHP development rules for Cursor — Laravel, Symfony, WordPress, Composer, and PHP project structure. Use when working with PHP, Laravel, Symfony, or WordPress.  
  → `skills/cursor-skills-php/GUIDE.md`
- **cursor-skills-python** — Python development rules for Cursor — Django, Flask, FastAPI, data science, virtual environments, and testing. Use when working with Python projects.  
  → `skills/cursor-skills-python/GUIDE.md`
- **database-design** — Design database schemas — tables, relationships, indexes, constraints, and ORM setup. Covers relational design, normalization, and common patterns.  
  → `skills/database-design/GUIDE.md`  
  *(Full admin UI / Database Studio product → `systems-platforms-master` → `database-studio-complete`)*
- **stripe-stripe-best-practices** — >-  
  → `skills/stripe-stripe-best-practices/GUIDE.md`
- **stripe-stripe-projects** — >-  
  → `skills/stripe-stripe-projects/GUIDE.md`
- **stripe-upgrade-stripe** — Guide for upgrading Stripe API versions and SDKs  
  → `skills/stripe-upgrade-stripe/GUIDE.md`
- **integrations-pro** — Core integration patterns (webhooks, OAuth, sync). **Platform playbooks: `integrations-master`** (GitHub, Slack, CRM, cloud, index).  
  → `skills/integrations-pro/GUIDE.md`
- **qr-code-generation** — Generate/decode QR codes: URL/vCard/Wi-Fi/payment payloads, error-correction levels, SVG for print, branded QR with logos, and dynamic trackable redirects.  
  → `skills/qr-code-generation/GUIDE.md`
- **gs1-barcodes** — GS1 & retail barcodes: GTIN/EAN-13/UPC-A, SSCC/GLN, check digits, symbology choice (GS1-128 / DataMatrix), Application Identifiers, and GS1 Digital Link.  
  → `skills/gs1-barcodes/GUIDE.md`
- **google-sign-in** — "Sign in with Google" via Google Identity Services: GIS button, server-side ID-token verification (aud/iss/exp), OAuth code flow + PKCE, and refresh-token handling.  
  → `skills/google-sign-in/GUIDE.md`
- **mfa-authenticator-security** — Multi-factor auth & authenticator security: TOTP (Google Authenticator/Authy) with QR enrollment & replay/rate-limit protection, WebAuthn/passkeys, SMS/email OTP, push approval, backup/recovery codes, and step-up/adaptive auth.  
  → `skills/mfa-authenticator-security/GUIDE.md`
- **gps-integration** — Advanced GPS/geolocation: browser & mobile capture, PostGIS storage/queries, geofencing (enter/exit), routing/ETA, real-time tracking pipelines, and battery/privacy best practices.  
  → `skills/gps-integration/GUIDE.md`
- **gis-maps** — GIS & interactive maps: MapLibre/Mapbox/Leaflet/deck.gl, GeoJSON & vector tiles, clustering/heatmaps/choropleths, PostGIS spatial queries, geocoding/routing, and performance.  
  → `skills/gis-maps/GUIDE.md`

## Pairs well with

**`integrations-master`** — GitHub, GitLab, CI/CD, AWS/GCP/Azure, Google/Microsoft, Slack, Jira, Salesforce, Shopify, Zapier/n8n, 80+ platform index.

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
