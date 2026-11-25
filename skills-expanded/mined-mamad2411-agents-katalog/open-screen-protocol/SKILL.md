---
name: open-screen-protocol
description: >-
  Open Screen Protocol: The Open Screen Network Protocol is a network protocol that allows two Open Screen agents to establish a secure network transport in an interoperable fashion. Covers Open Screen Network Protocol (track), Open Screen Application Protocol (track). Use when implementing the Open Screen network or application protocol. Triggers: Open Screen Protocol.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Open Screen Protocol

The Open Screen Network Protocol is a network protocol that allows two Open Screen agents to establish a secure network transport in an interoperable fashion.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing the Open Screen network or application protocol.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Open Screen Network Protocol (default, posture track); Open Screen Application Protocol (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **2.1. General Requirements.** "An Open Screen Network Protocol agent must be able to discover the presence of another OSP agent connected to the same IPv4 or IPv6 subnet and reachable by IP multicast."
3. **2.1. General Requirements.** "An OSP agent must be able to obtain the IPv4 or IPv6 address of the agent, a display name for the agent, and an IP port number for establishing a network transport to the agent."
4. **2.2. Non-Functional Requirements.** "It should be possible to implement the Open Screen Network Protocol using modest hardware requirements, similar to what is found in a low end smartphone, smart TV or streaming device."
5. **2.2. Non-Functional Requirements.** "The discovery and connection protocols should minimize power consumption, especially on a listening agent which is likely to be battery powered."
6. **2.2. Non-Functional Requirements.** "The protocol should minimize the amount of information provided to a passive network observer about the identity of the user or activities on the agent, including presentations, remote playbacks, or the content of media streams."
7. **2.2. Non-Functional Requirements.** "The protocol should prevent active network attackers from impersonating a display and observing or altering data intended for the controller or receiver."
8. **2.2. Non-Functional Requirements.** "A listening agent should be able to discover quickly when an advertising agent becomes available or unavailable (i.e., when it connects or disconnects from the network)."

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

- [Open Screen Network Protocol](https://www.w3.org/TR/openscreen-network/): Working Draft, openscreen-network WD-openscreen-network-20260210 (Working Draft, 2026-02-10), checked 2026-10-06.
- [Open Screen Application Protocol](https://www.w3.org/TR/openscreen-application/): Working Draft, openscreen-application WD-openscreen-application-20260210 (Working Draft, 2026-02-10), checked 2026-10-06.
