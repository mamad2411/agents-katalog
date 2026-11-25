---
name: client-runtime-intelligence
description: Client-runtime and bundle analysis methodology for converting front-end assets into route maps, auth assumptions, object graphs, and manual test queues. Use when JavaScript, source maps, or mobile-facing assets are available.
sources: local_tooling_corpus, field_recon
report_count: 0
---

# Client Runtime Intelligence

Use this skill whenever the target exposes meaningful client code.

## Why it matters

The runtime tells you what the product believes about itself:
- which APIs exist
- which objects matter
- which roles the UI expects
- which states the client thinks are valid
- which surfaces the frontend tries to hide

## What to extract

Prioritize these categories:
- route templates and API base paths
- GraphQL queries, mutations, fragments, and object identifiers
- feature flags and rollout guards
- role names and permission checks
- import, upload, export, clone, restore, preview, and support actions
- hidden form fields and query parameters
- environment markers and region hints
- error handlers and fallback paths
- admin, staff, or internal-only route references
- auth-provider configuration and token-handling logic

## Reading strategy

Work from coarse to fine:

1. Product map
- identify app modules
- separate marketing code from authenticated product code
- identify admin/support bundles versus user bundles

2. Data-flow map
- which views create objects
- which views mutate objects
- which views export or share objects
- which views trigger background work

3. Trust map
- where the client performs role checks
- where object ownership is assumed rather than enforced
- where a helper action uses a lighter payload than the main action
- where a hidden parameter appears to select tenant, workspace, actor, or role

## Manual test queue generation

Transform client findings into hypotheses, not just notes.

High-value hypotheses usually come from:
- role checks present only in UI logic
- helper mutations or helper endpoints with weaker context
- object identifiers reused across modules
- preview/export paths that use different endpoints than edit/view paths
- imports and uploads that trigger processors after the initial request
- support or admin actions referenced in shared components
- alternate flows for onboarding, invitations, recovery, or collaboration

## Transport-difference analysis

For each important object or workflow, compare:
- UI request shape
- direct API request shape
- background-job or webhook side effects
- batch or helper endpoints
- mobile or legacy routes if visible

The useful question is not "is the route there" but "which transport enforces the weakest assumptions."

## Hidden-parameter discipline

Treat parameter discovery as a first-class outcome.

Track:
- query names
- body keys
- feature toggles
- state flags
- pagination and filter fields
- actor or tenant selectors
- secondary object IDs

Then cluster them by workflow so you can ask:
- which ones are trusted too much
- which ones switch object context
- which ones select a helper path

## Runtime anti-patterns to watch

High-signal patterns:
- role checks in client code with no obvious server pairing
- disabled buttons guarding dangerous actions
- comments or dead code referencing internal endpoints
- dual object references in one mutation or form
- environment switches exposing staging or region-specific logic
- error handlers disclosing backend route names or validation rules

## Good work product

End with:
- an endpoint and object graph
- a parameter dictionary grouped by workflow
- a trust-mismatch list
- a manual test queue focused on actor, state, and helper-object differences
