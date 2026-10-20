---
name: json-rpc
description: >-
  JSON-RPC: JSON-RPC is a stateless, light-weight remote procedure call (RPC) protocol. Covers JSON-RPC 2.0. Use when calling procedures over JSON-RPC 2.0. Triggers: JSON-RPC, jsonrpc.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# JSON-RPC

JSON-RPC is a stateless, light-weight remote procedure call (RPC) protocol. Primarily this specification defines several data structures and the rules around their processing. It is transport agnostic in that the concepts can be used within the same process, over sockets, over http, or in many various message passing environments. It uses JSON ( RFC 4627 ) as data format.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when calling procedures over JSON-RPC 2.0.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: JSON-RPC 2.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2 Conventions.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 ."
2. **4 Request object.** "Method names that begin with the word rpc followed by a period character (U+002E or ASCII 46) are reserved for rpc-internal methods and extensions and MUST NOT be used for anything else."
3. **4 Request object.** "id An identifier established by the Client that MUST contain a String, Number, or NULL value if included."
4. **4 Request object.** "The value SHOULD normally not be Null [1] and Numbers SHOULD NOT contain fractional parts [2] The Server MUST reply with the same value in the Response object if included."
5. **4.1 Notification.** "The Server MUST NOT reply to a Notification, including those that are within a batch request."
6. **4.2 Parameter Structures.** "If present, parameters for the rpc call MUST be provided as a Structured value."
7. **4.2 Parameter Structures.** "by-position: params MUST be an Array, containing the values in the Server expected order."
8. **4.2 Parameter Structures.** "by-name: params MUST be an Object, with member names that match the Server expected parameter names."

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

- [JSON-RPC 2.0](https://www.jsonrpc.org/specification): Specification, JSON-RPC 2.0, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
