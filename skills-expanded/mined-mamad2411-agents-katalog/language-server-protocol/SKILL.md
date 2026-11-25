---
name: language-server-protocol
description: >-
  Language Server Protocol: build language servers and editor clients that exchange JSON-RPC messages for code intelligence. Covers LSP 3.17, LSP 3.18 (track preview). Use when implementing a language server. Triggers: LSP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Language Server Protocol

This document describes the previous 3.17.x version of the language server protocol. An implementation for node of the 3.17.x version of the protocol can be found here .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing a language server.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: LSP 3.17 (default); LSP 3.18 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Response Message.** "* This member MUST NOT exist if there was an error invoking the method."
2. **Content Part.** "If a server or client receives a header with a different encoding than utf-8 it should respond with an error."
3. **Request Message.** "Every processed request must send a response back to the sender of the request."
4. **Response Message.** "The result property of the ResponseMessage should be set to null in this case to signal a successful request."
5. **Response Message.** "No LSP error codes should * be defined between the start and end range."
6. **Response Message.** "The error * message should contain human readable information about why * the request failed."
7. **Response Message.** "This error code should * only be used for requests that explicitly support being * server cancellable."
8. **Response Message.** "A server should * NOT send this error code if it detects a content change * in its unprocessed messages."

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

- [LSP 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/): Specification, LSP 3.17, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
- [LSP 3.18](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/): Specification, LSP 3.18, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
