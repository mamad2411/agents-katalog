---
name: oxygen-email-infra
description: Set up and inspect OXYGEN sender profiles, domains, mailboxes, authentication, warmup and Sequence attachment using native previews.
---

# Prepare native senders

Read [the runtime contract](../../../docs/runtime-contract.md). Discover `oxygen capabilities search "email infrastructure setup" --json`; hydrate the relevant sender, domain, mailbox, managed-inbox or integration command. This procedure does not require a named third-party mailbox vendor.

1. Inspect existing sender profiles and exact mailbox addresses. Reuse the real person's identity; do not infer a name/photo from another customer or invent a sender.
2. For provisioning or subscriptions, preview the exact resources, current quote, recurring terms and included services. Execute only the authorized scope.
3. Inspect DNS and authentication: nameservers, MX, SPF, DKIM, DMARC and any configured tracking. Preserve unrelated domain services.
4. Check OAuth and compatibility for every exact address. One token or a domain-level success does not prove every mailbox is ready. Follow the returned remedy and retry timing.
5. Inspect native warmup truth, enrollment state, ramp and cost. Warmup included in an approved order needs no second permission request; unrelated enrollment needs its own scope.
6. Read health, auto-pause, capacity and egress settings, then attach eligible senders to the intended Sequence.

An active subscription, configured DNS and actual working authentication are distinct states. Surface which one failed. Use live quotes instead of stored prices or a universal sends-per-day rule.

For a requested disconnection or cancellation, preview effects on sending, credentials, history, renewals and affected Sequences. Removing a connection, ending warmup and canceling managed provisioning are different operations. Honor the native confirmation mechanism and read back state; do not delete external mailbox accounts through an inferred cleanup.

Return sender/mailbox links, authentication and warmup states, actual charges if incurred, and any unresolved readiness. Infrastructure setup and warmup do not authorize outreach.
