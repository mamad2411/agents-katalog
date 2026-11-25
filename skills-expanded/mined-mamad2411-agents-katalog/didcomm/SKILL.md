---
name: didcomm
description: >-
  DIDComm Messaging 2.1: send encrypted, authenticated messages between DIDs. Covers DIDComm Messaging 2.1. Use when sending authenticated messages between DIDs. Triggers: DIDComm, didcomm.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# DIDComm Messaging

Contributors: Sam Curren (Indicio), Tobias Looker (MATTR), Oliver Terbu (ConsenSys), Kyle Den Hartog (MATTR), Baha Shaaban (SecureKey), Drummond Reed (Evernym), Steve McCown (Anonyome Labs), Troy Ronda (SecureKey), George Aristy (SecureKey), Vyacheslav Gudkov (DSR), Alexander Shcherbakov (DSR), Alexander Martynov (DSR), Daniel Buchner (Microsoft), Devin Fisher (Evernym), Orie Steele (Transmute), Brian Richter (Aviary Tech), Juan Caballero ( Centre.io ), @liormargalit, Timo Glastra (Animo Solutions), Andrew Whitehead (Government of British Columbia), Nader Helmy (MATTR), Markus Sabadello (Danube Tech), Patrick McClurg (SICPA), Stephen Curran (Government of British Columbia), Daniel Hardman (S

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending authenticated messages between DIDs.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: DIDComm Messaging 2.1 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ Specific Requirements.** "The DIDComm Messaging design attempts to be: Secure (specifically, MUST preserve the integrity of messages against tampering; MUST allow the authenticity of messages and message senders to be proved; MUST use best-of-breed crypto; MUST allow parties to emit both repudiable and non-repudiable messages; perfect forward secrecy is not formally required due to the lack of a session construct, but…"
2. **§ IANA Media Types.** "This is the default wrapping choice, and SHOULD be used unless a different goal is clearly identified."
3. **§ IANA Media Types.** "authcrypt(sign(plaintext)) application/didcomm-encrypted+json Adds no useful guarantees over the previous choice, and is slightly more expensive, so this wrapping combination SHOULD NOT be emitted by conforming implementations."
4. **§ IANA Media Types.** "If they choose to do so, they MUST emit an error if the signer of the plaintext is different from the sender identified by the authcrypt layer."
5. **§ IANA Media Types.** "However, in the set of envelopes that targets a single hop, envelope combinations other than the ones above MUST NOT be used."
6. **§ IANA Media Types.** "Aligning with RFC 7515 , IANA types for DIDComm messages MAY omit the application/ prefix; the recipient MUST treat media types not containing / as having the application/ prefix present."
7. **§ DIDComm Plaintext Messages.** "The media type for a generic DIDComm plaintext message MUST be reported as application/didcomm-plain+json by conformant implementations."
8. **§ DIDComm Plaintext Messages.** "The media type of the envelope MAY be set in the typ property of the plaintext; it SHOULD be set if the message is intended for use without a signature or encryption."

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

- [DIDComm Messaging 2.1](https://identity.foundation/didcomm-messaging/spec/v2.1/): DIF specification, DIDComm Messaging v2.1, fetched 2026-10-06 (DIF specification, 2026-10-06), checked 2026-10-06.
