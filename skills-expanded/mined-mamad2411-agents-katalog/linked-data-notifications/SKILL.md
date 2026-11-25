---
name: linked-data-notifications
description: >-
  Linked Data Notifications: Linked Data Notifications is a protocol that describes how servers (receivers) can have messages pushed to them by applications (senders), as well as how other applications (consumers) may retrieve those messages. Covers Linked Data Notifications. Use when sending or receiving an LDN inbox notification. Triggers: LDN, Linked Data Notifications.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Linked Data Notifications

Linked Data Notifications is a protocol that describes how servers (receivers) can have messages pushed to them by applications (senders), as well as how other applications (consumers) may retrieve those messages. Any resource can advertise a receiving endpoint (Inbox) for the messages. Messages are expressed in RDF, and can contain any data.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending or receiving an LDN inbox notification.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Linked Data Notifications (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in [ RFC2119 ]."
2. **3.1 Discovery.** "These may be carried out in either order, but if the first fails to result in an Inbox the second MUST be tried."
3. **3.1 Discovery.** "Senders and consumers SHOULD omit the Link header discovery when specifically targeting URIs with fragment identifiers."
4. **Note.** "A resource MUST advertise only one Inbox."
5. **3.2 Sender.** "Following discovery , senders who want to send notifications MUST deliver them through a POST request to the Inbox URL ."
6. **3.2 Sender.** "Otherwise, the body of the POST request MUST contain the notification payload in JSON-LD with header Content-Type: application/ld+json ."
7. **3.2 Sender.** "Senders SHOULD NOT make POST requests to the Inbox that are localhost or a loopback IP address."
8. **3.3 Receiver.** "Receivers MUST support GET and POST requests on the Inbox URL."

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

- [Linked Data Notifications](https://www.w3.org/TR/ldn/): Recommendation, ldn REC-ldn-20170502 (Recommendation, 2017-05-02), checked 2026-10-06.
