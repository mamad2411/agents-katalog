---
name: debug-adapter-protocol
description: >-
  Debug Adapter Protocol: The Debug Adapter Protocol defines the protocol used between an editor or IDE and a debugger or runtime. Covers Debug Adapter Protocol. Use when implementing a debug adapter. Triggers: DAP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Debug Adapter Protocol

The Debug Adapter Protocol defines the protocol used between an editor or IDE and a debugger or runtime.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing a debug adapter.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Debug Adapter Protocol (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Debug Adapter Protocol.** "Clients should only call this request if the corresponding capability supportsCancelRequest is true."
2. **Debug Adapter Protocol.** "The cancel request may return an error if it could not cancel an operation but a client should refrain from presenting this error to end users."
3. **Debug Adapter Protocol.** "A client should not assume that progress just got cancelled after sending the cancel request."
4. **Debug Adapter Protocol.** "* For backward compatibility this string is shown in the UI if the * `description` attribute is missing (but it must not be translated)."
5. **Debug Adapter Protocol.** "*/ threadId ?: number ; /** * A value of true hints to the client that this event should not change the * focus."
6. **Debug Adapter Protocol.** "* - The client should use this information to enable that all threads can * be expanded to access their stacktraces."
7. **Debug Adapter Protocol.** "This category should only be used for informational * output from the debugger (as opposed to the debuggee)."
8. **Debug Adapter Protocol.** "This category should only be used for important messages * from the debugger (as opposed to the debuggee)."

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

- [Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/specification): Specification, Debug Adapter Protocol, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
