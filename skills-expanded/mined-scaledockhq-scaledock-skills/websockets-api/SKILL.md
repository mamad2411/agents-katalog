---
name: websockets-api
description: >-
  WebSockets API: This specification provides APIs to enable web applications to maintain bidirectional communications with server-side processes. Covers WebSockets Living Standard. Use when opening a WebSocket from a page. Triggers: WebSocket, WebSockets Living Standard.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebSockets API

This specification provides APIs to enable web applications to maintain bidirectional communications with server-side processes.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when opening a WebSocket from a page.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebSockets Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **WebSockets.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **3.1. Interface definition.** "The extensions attribute must initially return the empty string."
3. **3.1. Interface definition.** "The protocol attribute must initially return the empty string."
4. **3.1. Interface definition.** "[WSP] If neither code nor reason is present, the WebSocket Close message must not have a body."
5. **3.1. Interface definition.** "If code is present, then the status code to use in the WebSocket Close message must be the integer given by code ."
6. **3.1. Interface definition.** "[WSP] If reason is also present, then reasonBytes must be provided in the Close message after the status code."
7. **3.1. Interface definition.** "Run the appropriate set of steps from the following list: If data is a string If the WebSocket connection is established and the WebSocket closing handshake has not yet started , then the user agent must send a WebSocket Message comprised of the data argument using a text frame opcode; if the data cannot be sent, e.g."
8. **3.1. Interface definition.** "because it would need to be buffered but the buffer is full, the user agent must flag the WebSocket as full and then close the WebSocket connection ."

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

- [WebSockets Living Standard](https://websockets.spec.whatwg.org/review-drafts/2023-09/): Review Draft, Review Draft 2023-09 (Review Draft, 2023-09), checked 2026-10-06.
