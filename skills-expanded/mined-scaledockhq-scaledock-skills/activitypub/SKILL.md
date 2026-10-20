---
name: activitypub
description: >-
  ActivityPub: The ActivityPub protocol is a decentralized social networking protocol based upon the [ ActivityStreams ] 2.0 data format. Covers ActivityPub, Activity Streams 2.0, Activity Vocabulary. Use when implementing ActivityPub. Triggers: ActivityPub, Activity Streams.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# ActivityPub

The ActivityPub protocol is a decentralized social networking protocol based upon the [ ActivityStreams ] 2.0 data format. It provides a client to server API for creating, updating and deleting content, as well as a federated server to server API for delivering notifications and content.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing ActivityPub.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: ActivityPub (default); Activity Streams 2.0 (default); Activity Vocabulary (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MAY , MUST , MUST NOT , SHOULD , and SHOULD NOT are to be interpreted as described in [ RFC2119 ]."
2. **3. Objects.** "Implementers SHOULD include the ActivityPub context in their object definitions."
3. **3. Objects.** "Servers SHOULD validate the content they receive to avoid content spoofing attacks."
4. **3.1 Object Identifiers.** "ActivityPub extends this requirement; all objects distributed by the ActivityPub protocol MUST have unique global identifiers, unless they are intentionally transient (short lived activities that are not intended to be able to be looked up, such as some kinds of chat messages or game notifications)."
5. **3.1 Object Identifiers.** "(Publicly facing content SHOULD use HTTPS URIs)."
6. **3.1 Object Identifiers.** "An ID explicitly specified as the JSON null object, which implies an anonymous object (a part of its parent context) Identifiers MUST be provided for activities posted in server to server communication, unless the activity is intentionally transient."
7. **3.1 Object Identifiers.** "However, for client to server communication, a server receiving an object posted to the outbox with no specified id SHOULD allocate an object ID in the actor's namespace and attach it to the posted object."
8. **3.2 Retrieving objects.** "Servers MAY use HTTP content negotiation as defined in [ RFC7231 ] to select the type of data to return in response to a request, but MUST present the ActivityStreams object representation in response to application/ld+json; profile="https://www.w3.org/ns/activitystreams" , and SHOULD also present the ActivityStreams representation in response to application/activity+json as well."

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

- [ActivityPub](https://www.w3.org/TR/activitypub/): Recommendation, activitypub REC-activitypub-20180123 (Recommendation, 2018-01-23), checked 2026-10-06.
- [Activity Streams 2.0](https://www.w3.org/TR/activitystreams-core/): Recommendation, activitystreams-core REC-activitystreams-core-20170523 (Recommendation, 2017-05-23), checked 2026-10-06.
- [Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/): Recommendation, activitystreams-vocabulary REC-activitystreams-vocabulary-20170523 (Recommendation, 2017-05-23), checked 2026-10-06.
