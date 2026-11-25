---
name: service-workers
description: >-
  Service Workers: The core of this specification is a worker that wakes to receive events. Covers Service Workers Nightly (build). Use when implementing a service worker or its registration. Triggers: service worker, ServiceWorkerRegistration.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Service Workers

The core of this specification is a worker that wakes to receive events. This provides an event destination that can be used when other destinations would be inappropriate, or no other destination exists. For example, to allow the developer to decide how a page should be fetched, an event needs to dispatch potentially before any other execution contexts exist for that origin. To react to a push message, or completion of a persistent download, the context that originally registered interest may no longer exist. In these cases, the service worker is the ideal event destination. This specification also provides a fetch event , and a request and response store similar in design to the HTTP cache

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing a service worker or its registration.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Service Workers Nightly (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **1. Motivations.** "A key design principle of the service worker is that errors should always be recoverable."
3. **2.3.1. Lifetime.** "A user agent must persistently keep a list of registered service worker registrations unless otherwise they are explicitly unregistered ."
4. **2.7. User Agent Shutdown.** "A user agent must maintain the state of its stored service worker registrations across restarts with the following rules: An installing worker does not persist but is discarded."
5. **2.7. User Agent Shutdown.** "To attain this, the user agent must invoke Handle User Agent Shutdown when it terminates."
6. **3.1.3. state.** "The state attribute must return the value (in ServiceWorkerState enumeration) to which it was last set."
7. **3.1.6. Event handler.** "The following is the event handler (and its corresponding event handler event type ) that must be supported, as event handler IDL attributes , by all objects implementing ServiceWorker interface: event handler event handler event type onstatechange statechange"
8. **3.2.2. installing.** "installing attribute must return the value to which it was last set."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Service Workers Nightly](https://www.w3.org/TR/service-workers/): Candidate Recommendation Draft, service-workers CRD-service-workers-20260917 (Candidate Recommendation Draft, 2026-09-17), checked 2026-10-06.
