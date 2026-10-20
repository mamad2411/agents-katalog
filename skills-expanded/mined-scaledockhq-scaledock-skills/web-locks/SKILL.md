---
name: web-locks
description: >-
  Web Locks API: This document defines a web platform API that allows script to asynchronously acquire a lock over a resource, hold it while work is performed, then release it. Covers Web Locks API (track). Use when coordinating exclusive work across tabs. Triggers: Web Locks, navigator.locks.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Locks API

This document defines a web platform API that allows script to asynchronously acquire a lock over a resource, hold it while work is performed, then release it. While held, no other script in the origin can acquire a lock over the same resource. This allows contexts (windows, workers) within a web application to coordinate the usage of resources.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when coordinating exclusive work across tabs.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Locks API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **1.2. Motivating Use Cases.** "When the same document is opened for editing in two tabs the work must be coordinated across tabs, such as allowing only one tab to make changes to or synchronize the document at a time."
3. **1.2. Motivating Use Cases.** "This tab is the only one that should be performing some operations (e.g."
4. **6.1. Lock Scope.** "Locks can be used as an ephemeral state retention mechanism and, like storage APIs, can be used as a communication mechanism, and must be no more privileged than storage facilities."
5. **6.1. Lock Scope.** "User agents that impose finer granularity on one of these services must impose it on others; for example, a user agent that exposes different storage partitions to a top-level page (first-party) and a cross-origin iframe (third-party) in the same origin for privacy reasons must similarly partition locking."
6. **6.1. Lock Scope.** "This also provides reasonable expectations for web application authors; if a lock is acquired over a storage resource, all same-origin browsing contexts must observe the same state."
7. **6.3. Implementation Risks.** "Implementations must ensure that locks do not span origins."
8. **Conformant Algorithms.** "Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("must", "should", "may", etc) used in introducing the algorithm."

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

- [Web Locks API](https://www.w3.org/TR/web-locks/): Working Draft, web-locks WD-web-locks-20250924 (Working Draft, 2025-09-24), checked 2026-10-06.
