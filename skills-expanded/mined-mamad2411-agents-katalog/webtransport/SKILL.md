---
name: webtransport
description: >-
  WebTransport: This document defines a set of ECMAScript APIs in WebIDL to allow data to be sent and received between a browser and server, utilizing [WEB-TRANSPORT-OVERVIEW] . Covers WebTransport (build). Use when sending unreliable or bidirectional data to a server. Triggers: WebTransport.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebTransport

This document defines a set of ECMAScript APIs in WebIDL to allow data to be sent and received between a browser and server, utilizing [WEB-TRANSPORT-OVERVIEW] . This specification is being developed in conjunction with protocol specifications developed by the IETF WEBTRANS Working Group.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending unreliable or bidirectional data to a server.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebTransport (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in [RFC2119] and [RFC8174] when, and only when, they appear in all capitals, as shown here."
2. **2. Conformance.** "(In particular, the algorithms defined in this specification are intended to be easy to follow, and not intended to be performant.) Implementations that use ECMAScript to implement the APIs defined in this specification MUST implement them in a manner consistent with the ECMAScript Bindings defined in the Web IDL specification [WEBIDL] , as this specification uses that specification and terminology."
3. **4.3. Procedures.** "The user agent MUST, for any WebTransport object whose [[State]] is "connecting" or "connected" , run sendDatagrams on a subset (determined by send-order rules ) of its associated WebTransportDatagramsWritable objects, and SHOULD do so as soon as reasonably possible whenever the algorithm can make progress."
4. **4.3. Procedures.** "The send-order rules are that sending in general MAY be interleaved with sending of previously queued streams and datagrams, as well as streams and datagrams yet to be queued to be sent over this transport, except that sending MUST starve until all bytes queued for sending on streams and datagrams with the same [[SendGroup]] and a higher [[SendOrder]] , that are neither errored nor blocked by…"
5. **5.2. Methods.** "When called, the user agent MUST run these steps: Let transport be WebTransport object associated with this ."
6. **5.4. Procedures.** "The user agent SHOULD run receiveDatagrams for any WebTransport object whose [[State]] is "connected" as soon as reasonably possible whenever the algorithm can make progress."
7. **6.2. Constructor.** "When the WebTransport() constructor is invoked, the user agent MUST run the following steps: Let baseURL be this ’s relevant settings object ’s API base URL ."
8. **6.3. Attributes.** "ready , of type Promise< undefined >, readonly On getting, it MUST return this ’s [[Ready]] ."

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

- [WebTransport](https://www.w3.org/TR/webtransport/): Candidate Recommendation Snapshot, webtransport CR-webtransport-20260730 (Candidate Recommendation Snapshot, 2026-07-30), checked 2026-10-06.
