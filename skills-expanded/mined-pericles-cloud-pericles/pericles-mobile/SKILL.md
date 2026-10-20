---
name: pericles-mobile
version: 2026.05.0
description: >
  How to build Pericles mobile — the on-the-go surface that lets a Risk Manager or
  Supply Chain Manager triage events, approve actions, and consume briefs from a phone.
  Use this WHENEVER you scope or build mobile views. Encodes mobile-first persona
  framing, what subset of surfaces is in scope (read + approve, not full authoring),
  tenant scoping, and that approvals route through the same Execution Node + approval
  gate as web.
doctrine_refs: [§3, §6; Atlas/Intelligence PRDs]
depends_on: [pericles-frontend-foundations, pericles-persona-layer, pericles-execution-node, pericles-tenant-isolation]
last_reconciled: 2026-05-28
---

# Pericles Mobile (build skill)

Mobile is **not a second product** — it's a focused subset of the same engine and Skills
for moments when a manager isn't at their desk. Build it as a thin client over the same
backend with the same persona/tenant rules.

## When to use this skill

Scoping or building any mobile surface; deciding what subset of a desktop module belongs
on mobile.

## In-scope surfaces (V1)

- **Events feed + event detail** — read the live feed and event/incident detail,
  including the lineage of why the platform flagged it (`pericles-intelligence-ui`,
  `pericles-observability`).
- **Briefs / memo viewer** — read CFO-ready impact summaries; **never auto-distribute**
  (sending goes through an Execution Node + approval, `pericles-execution-node`).
- **Approvals inbox** — approve / decline consequential actions a supervisor proposed
  (notifications, supplier outreach, Plan activations). The approval gate is the same as
  on web; the mobile client just renders it.
- **Co-Pilot (lightweight)** — ask questions about the risk picture; same gateway-path
  rules apply (`pericles-copilot-ui`).
- **Atlas (read-only)** — view the map; full filter bar deferred to V2 to keep mobile
  performant.

Authoring (Plans, Assessments, Admin) stays on web in V1.

## Stack & framing

Pick **one of**: a Next.js PWA (preferred — reuses `frontend/`) or React Native; resolve
with the platform team. Either way:
- Persona framing comes from the **Persona Layer** (`pericles-persona-layer`) — same
  shape/scope/vocabulary rules as web. No mobile-specific persona forks.
- Tenant scoping is server-side (`pericles-tenant-isolation`); never trust a client-
  supplied `organization_id`.
- Realtime via `socket.io-client`; subscribe per tenant and clean up on background.
- Auth reuses the existing auth-server (JWT + Google OAuth + optional SSO).

## Push notifications

Push for high-severity events or pending approvals only — respect the customer's
notification preferences (`pericles-notifications`); never push external comms or
restricted-scope content (e.g. financial impact to a persona without scope).

## What this forbids

Mobile-specific persona/Skill forks; client-trusted `organization_id`; auto-acting on a
push notification without the same approval gate as web; showing restricted-scope data
(financial impact to a Stakeholder); shipping authoring surfaces in V1.

## Verification

Mobile reads the same data the same way (tenant-scoped, persona-framed); approvals
route through the canonical Execution Node + approval gate; push respects preferences +
data scope; performance budget (cold-start, scroll FPS) met; offline behavior is
read-only graceful.

## Existing standards (read alongside)

`pericles-frontend-foundations`, `pericles-persona-layer`, `pericles-execution-node`;
Atlas/Intelligence PRDs.

## Open questions

- PWA vs React Native (PWA shares more code; RN gives better push + offline). Decide
  early.
- Push provider + secret handling — keep in the secret store.

## Changelog

- 2026.05.0 — Initial draft; V1 subset (read + approve + lightweight Co-Pilot),
  persona/tenant rules unchanged from web.
