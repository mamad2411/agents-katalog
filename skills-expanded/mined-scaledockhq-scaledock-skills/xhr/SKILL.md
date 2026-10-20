---
name: xhr
description: >-
  XMLHttpRequest: The XMLHttpRequest Standard defines an API that provides scripted client functionality for transferring data between a client and a server. Covers XMLHttpRequest Living Standard. Use when maintaining an XMLHttpRequest client. Triggers: XMLHttpRequest, XHR.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# XMLHttpRequest

The XMLHttpRequest Standard defines an API that provides scripted client functionality for transferring data between a client and a server.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when maintaining an XMLHttpRequest client.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XMLHttpRequest Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 3.2.** "An XMLHttpRequest object must not be garbage collected if its state is either opened with send() invoked being true, headers received, or loading, and it has one or more event listeners registered whose type is one of readystatechange, progress, abort, error, load, timeout, and loadend."
2. **§ 3.5.1.** "Developers must not pass false for the async argument when the current global object is a Window object."
3. **§ 3.5.1.** "If method is a forbidden method, then throw a "SecurityError" DOMException."
4. **§ 3.5.1.** "If async is false, the current global object is a Window object, and either this’s timeout is not 0 or this’s response type is not the empty string, then throw an "InvalidAccessError" DOMException."
5. **§ 3.5.2.** "If (name, value) is a forbidden request-header, then return."
6. **§ 3.5.6.** "If this’s request method is `GET` or `HEAD`, then set body to null."
7. **§ 3.5.6.** "If this’s cross-origin credentials is true, then "include"; otherwise "same-origin"."
8. **§ 3.5.6.** "If req’s done flag is unset, then set this’s timed out to true and terminate this’s fetch controller."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
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

- [XMLHttpRequest Living Standard](https://xhr.spec.whatwg.org/review-drafts/2026-08/): Review Draft, Review Draft 2026-08 (Review Draft, 2026-08), checked 2026-10-06.
