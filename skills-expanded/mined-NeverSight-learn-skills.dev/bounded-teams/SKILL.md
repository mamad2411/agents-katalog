---
name: bounded-teams
description: >-
  Operate Bounded across a team or organization: observe every action and every
  policy decision your apps make, enforce boundaries on what agents and services
  can do, keep custody of secrets and credentials, and surface the policy
  invariants (the proven guarantees) on a shared team view. Use for org-level
  governance, the team/enterprise story, and dashboards that show what apps did
  and what their invariants blocked. Part of the Bounded skill family; per-app
  observe wiring lives in the bounded-observe skill, and the invariants themselves
  in bounded-backend.
---

# Bounded teams

The organization view of Bounded: one place to see and govern what a team's apps,
agents, and services actually do. Three layers sit under one roof:

- **Observe.** Every policy decision on every write (allowed or blocked, with the
  actor, the collection, and the invariant that fired) and every external action
  an agent takes, as a durable, filterable record. This is the org-scoped view of
  the same evidence the per-app **bounded-observe** skill turns on for a single
  app.
- **Enforce.** Boundaries on what may happen: spend and rate caps, escorted
  external actions checked before they fire, and the app's own proven invariants.
  A blocked action reads the same everywhere: declined, naming the boundary or
  invariant.
- **Custody.** Where secrets and credentials live, who can reach them, and the
  record of every access.

The point of the team view is that Bounded's guarantees become **visible**:
the policy **invariants** you declared and proved at deploy are shown on the same
shared page a team or buyer looks at, next to the runtime evidence that they held.
"See, and prove, everything your apps and their agents do."

## Where things live

| You want | Go to |
|---|---|
| Turn observe on for one app and read its feed / decisions | the **bounded-observe** skill |
| Write or change the invariants that get surfaced here | the **bounded-backend** skill (invariants, proofs) |
| The org dashboard and org-scoped observe database | the hosted team dashboard (`dashboard.bounded.sh`) and the per-app observe space it links to |
| Grant a teammate access to apps | `bounded share ... --role ...` (see the **bounded-deploy** skill) |

## Rules Of Thumb

- Observe is opt-in and metered; a team turns it on per app and can turn it off. Even on higher tiers it has a daily ceiling, and its infrastructure cost sits on top of the app's base costs.
- Enforcement on a team's own data is the app's own proven invariants; the team view surfaces them, it does not add a separate charge for them.
- The strongest team story is the pairing: the invariant (proved at deploy) next to the evidence that it blocked something at runtime.
- Keep guidance user-facing and within the public product surface; do not invent unpublished pricing or capabilities.
