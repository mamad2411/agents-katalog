---
name: websub
description: >-
  WebSub: WebSub provides a common mechanism for communication between publishers of any kind of Web content and their subscribers, based on HTTP web hooks. Covers WebSub. Use when publishing or subscribing to webhooks with WebSub. Triggers: WebSub, PubSubHubbub.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebSub

WebSub provides a common mechanism for communication between publishers of any kind of Web content and their subscribers, based on HTTP web hooks. Subscription requests are relayed through hubs, which validate and verify the request. Hubs then distribute new and updated content to subscribers when it becomes available. WebSub was previously known as PubSubHubbub.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing or subscribing to webhooks with WebSub.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebSub (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. Conformance.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in [ RFC2119 ]."
2. **3.1 Conformance.** "The key words MAY , MUST , MUST NOT , OPTIONAL , RECOMMENDED , REQUIRED , SHALL , SHALL NOT , SHOULD , and SHOULD NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
3. **3.1.1.1 Publishers.** "A conforming publisher MUST advertise topic and hub URLs for a given resource URL as described in Discovery ."
4. **3.1.1.2 Subscribers.** "A conforming subscriber: MUST support each discovery mechanism in the specified order to discover the topic and hub URLs as described in Discovery ."
5. **3.1.1.2 Subscribers.** "MUST send a subscription request as described in Subscriber Sends Subscription Request ."
6. **3.1.1.2 Subscribers.** "MAY request a specific lease duration MAY include a secret in the subscription request, and if it does, then MUST use the secret to verify the signature in the content distribution request ."
7. **3.1.1.2 Subscribers.** "MUST acknowledge a content distribution request with an HTTP 2xx status code."
8. **3.1.1.3 Hubs.** "A conforming hub: MUST accept a subscription request with the parameters hub.callback , hub.mode and hub.topic ."

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

- [WebSub](https://www.w3.org/TR/websub/): Recommendation, websub REC-websub-20260602 (Recommendation, 2026-06-02), checked 2026-10-06.
