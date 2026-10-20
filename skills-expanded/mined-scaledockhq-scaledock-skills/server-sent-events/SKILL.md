---
name: server-sent-events
description: >-
  Server-sent events: stream text/event-stream events from a server to an EventSource in the browser. Covers Server-sent events. Use when streaming text events from a server to a page. Triggers: EventSource, text/event-stream, server-sent events.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.2"
  kind: standard
---

# Server-sent events

← 9 Communication — Table of Contents — 9.3 Cross-document messaging → 9.2 Server-sent events 9.2.1 Introduction 9.2.2 The EventSource interface 9.2.3 Processing model 9.2.4 The `Last-Event-ID` header 9.2.5 Parsing an event stream 9.2.6 Interpreting an event stream 9.2.7 Authoring notes 9.2.8 Connectionless push and other features 9.2.9 Garbage collection 9.2.10 Implementation advice

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when streaming text events from a server to a page.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Server-sent events (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **9.2.2 The EventSource interface.** "This must initially be an implementation-defined value, probably in the region of a few seconds."
2. **9.2.2 The EventSource interface.** "This must initially be the empty string."
3. **9.2.2 The EventSource interface.** "The EventSource( url , eventSourceInitDict ) constructor, when invoked, must run these steps: Let ev be a new EventSource object."
4. **9.2.2 The EventSource interface.** "The url attribute's getter must return the serialization of this EventSource object's url ."
5. **9.2.2 The EventSource interface.** "The withCredentials attribute must return the value to which it was last initialized."
6. **9.2.2 The EventSource interface.** "When the object is created, it must be initialized to false."
7. **9.2.2 The EventSource interface.** "When the object is created, its readyState must be set to CONNECTING (0)."
8. **9.2.2 The EventSource interface.** "The close() method must abort any instances of the fetch algorithm started for this EventSource object, and must set the readyState attribute to CLOSED ."

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

- `mcp`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill mcp`
- `a2a`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill a2a`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html): HTML Living Standard, HTML Living Standard Review Draft 2026-07, server-sent events (HTML Living Standard, 2026-07), checked 2026-10-06.
