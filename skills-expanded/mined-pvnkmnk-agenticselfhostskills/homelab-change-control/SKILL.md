---
name: homelab-change-control
description: Control consequential homelab changes with explicit scope, observed-state evidence, approval, rollback, and non-secret records. Use before changing guests, services, storage, networking, access, backups, monitoring, or secrets.
---

# Homelab Change Control

Use this skill as the cross-boundary gate for consequential homelab work. It complements `homelab-safe-ops` and `homelab-change-planner`: this skill decides whether a proposed action is ready to enter a change plan at all.

## Purpose

Prevent undocumented state changes from turning experiments into hidden dependencies. Require clear ownership, observed facts, exact approval, recovery evidence, and a record that excludes secrets and unnecessary environment details.

## Classify the Request

1. Identify the target resource, canonical authority, affected data, and requested outcome.
2. Classify the request as read-only discovery, reversible configuration, data/service change, credential/access change, or destructive operation.
3. Identify protected resources and hard exclusions before looking for an implementation path.
4. Treat unknown state, missing recovery evidence, or an unapproved cross-boundary dependency as a blocker.

## Readiness Gate

Before a write, establish all of the following:

- Current state is observed rather than inferred.
- The exact target, side effect, and maximum scope are named.
- Compute, storage, network, service, secret, and data boundaries are separated.
- The applicable recovery source, rollback action, and validation evidence are known.
- A protected legacy workload cannot be touched implicitly; in the current portfolio, CT 100 requires separate explicit approval for every change.
- A non-secret change record has a home in the canonical homelab authority and Linear.

## Approval Gate

Request an exact owner approval for any state change. The approval must state the target, parameters, data placement, network/access effect, excluded workloads, rollback boundary, and whether the resource should start or autostart. Do not convert a broad goal into an unbounded change.

Require a separate approval for each of these categories: guest creation or destruction; service deployment; live secret or machine-identity activation; storage allocation or data placement; backup or restore; Tailscale, DNS, firewall, route, or public-access change; and modification of a protected legacy service.

## Execution and Evidence

1. Reconfirm volatile facts immediately before execution, such as an unused guest ID or available storage.
2. Execute only the approved subset; stop on parameter drift, unexpected output, or a missing precondition.
3. Validate the exact success condition and protected-resource non-interference.
4. Record decisions, pass/fail evidence, and follow-up gates without credentials, raw environment exports, addresses, or private keys.
5. If rollback is needed, confirm that no unrelated workload will be affected and obtain a fresh approval before destructive cleanup.

## Representative Scenario

**Request:** “Add remote access to a new service guest.”

**Route:** Confirm a supported service, recovery boundary, intended access path, and private-only requirement. Inspect existing tailnet and network posture read-only. Prepare a port-specific, reversible approval packet. Do not enroll a device, create a key, change policy, or expose a service until that exact packet is approved.

## Routing

- Use `proxmox-service-guest-gate` for fresh Proxmox guest creation and validation.
- Use `homelab-change-planner` once this gate establishes that a change is ready to plan.
- Use `homelab-safe-ops` during every infrastructure session.
- Use `homelab-logbook` after an approved change.
- Use `music-library-safety` or `local-knowledge-integration` when a homelab change crosses media or private-knowledge boundaries.
