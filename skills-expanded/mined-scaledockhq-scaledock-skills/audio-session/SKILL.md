---
name: audio-session
description: >-
  Audio Session: This API defines an API surface for controlling how audio is rendered and interacts with other audio playing applications. Covers Audio Session (track). Use when managing an audio session. Triggers: Audio Session.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Audio Session

This API defines an API surface for controlling how audio is rendered and interacts with other audio playing applications.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when managing an audio session.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Audio Session (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. The AudioSession interface.** "On getting, it MUST return the AudioSession [[state]] value."
2. **3. The AudioSession interface.** "On getting, it MUST return the AudioSession [[type]] value."
3. **3. The AudioSession interface.** "On setting, it MUST run the following steps with newValue being the new value being set on audioSession : If audioSession ."
4. **4. Extensions to the Navigator interface.** "Upon creation of the Window object, its associated AudioSession MUST be set to a newly created AudioSession object with the Window object’s relevant realm ."
5. **5.1. Update AudioSession’s type.** "To update the type of audioSession , the user agent MUST run the following steps: If audioSession ."
6. **5.2. Update AudioSession’s state.** "When the user agent observes such a modification, the user agent MUST queue a task to notify the state’s change with audioSession , the AudioSession object tied to the modified audio session and with newState being the new audio session state ."
7. **5.2. Update AudioSession’s state.** "To notify the state’s change with audioSession and newState , the user agent MUST run the following steps: Let isMutatingState be true if audioSession ."
8. **5.2. Update AudioSession’s state.** "To inactivate an AudioSession named audioSession , the user agent MUST run the following steps: If audioSession ."

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

- [Audio Session](https://www.w3.org/TR/audio-session/): Working Draft, audio-session WD-audio-session-20241113 (Working Draft, 2024-11-13), checked 2026-10-06.
