---
name: remote-playback
description: >-
  Remote Playback API: This specification defines an API extending the HTMLMediaElement that enables controlling remote playback of media from a web page. Covers Remote Playback API (build). Use when playing media on a remote device. Triggers: Remote Playback, remote.prompt.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Remote Playback API

This specification defines an API extending the HTMLMediaElement that enables controlling remote playback of media from a web page.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when playing media on a remote device.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Remote Playback API (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Conformance.** "The key words MAY , MUST , MUST NOT , RECOMMENDED , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **1. Conformance.** "Implementations that use ECMAScript to expose the APIs defined in this specification MUST implement them in a manner consistent with the ECMAScript Bindings defined in the Web IDL specification [ WEBIDL ]."
3. **5.2.1.** "If the user agent can monitor the list of available remote playback devices in the background (without a pending request to prompt () ), the RemotePlaybackAvailabilityCallback behavior defined below MUST be implemented by the user agent."
4. **5.2.1.** "Otherwise, the promise returned by watchAvailability () MUST be rejected with NotSupportedError ."
5. **5.2.1.1.** "The set of availability callbacks The user agent MUST keep track of the set of availability callbacks registered with each media element through the watchAvailability() method."
6. **5.2.1.2.** "The list of available remote playback devices The user agent MUST keep a list of available remote playback devices ."
7. **5.2.1.2.** "In this case the promise returned by watchAvailability () MUST be rejected with NotSupportedError , the global set of availability callbacks will be empty and the algorithm to monitor the list of available remote playback devices will only run as part of the initiate remote playback algorithm."
8. **5.2.1.2.** "When the global set of availability callbacks is not empty, the user agent MUST monitor the list of available remote playback devices continuously, so that pages can keep track of the last value received via the registered callbacks to offer remote playback only when there are available devices."

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

- [Remote Playback API](https://www.w3.org/TR/remote-playback/): Candidate Recommendation Draft, remote-playback CRD-remote-playback-20240430 (Candidate Recommendation Draft, 2024-04-30), checked 2026-10-06.
