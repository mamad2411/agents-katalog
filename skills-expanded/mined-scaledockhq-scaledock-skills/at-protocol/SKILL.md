---
name: at-protocol
description: >-
  AT Protocol: The Authenticated Transfer Protocol ("AT Protocol" or "atproto") is a network protocol for building open social web applications. Covers AT Protocol. Use when implementing the AT Protocol. Triggers: AT Protocol.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# AT Protocol

The Authenticated Transfer Protocol ("AT Protocol" or "atproto") from Bluesky Social, read from the specification pages on atproto.com in their Markdown source: the protocol overview, DIDs, handles, repositories, the data model, Lexicon, XRPC, sync and cryptography.

**Scope.** The atproto specifications are published as one living set of pages without version numbers. OAuth, permissions, labels, accounts and the event stream framing have their own pages and are not quoted here.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Personal Data Server (PDS), relay, AppView, labeler, client, or a library implementing atproto identifiers, repositories or Lexicon validation.
- Target version: AT Protocol (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **DIDs: DID Documents.** "The DID declared in the document (in the `id` field) should always be verified against what was expected (eg, used for resolution)."
2. **Handles.** "Handles must be bi-directionally linked to a DID: the DID document must claim the handle, and the handle must resolve to the DID identifier."
3. **Handles: Handle Resolution.** "The link between handle and DID must be confirmed bidirectionally, otherwise anybody could create handle aliases for third-party accounts."
4. **Repository: CAR File Serialization.** "The first element of the CAR `roots` metadata array must be the CID of the most relevant Commit object."
5. **Data Model: Data Types.** "Implementations should ignore unknown `$` fields (to allow protocol evolution)."
6. **Lexicon: Lexicon Evolution.** "The basic principle is that all old data must still be valid under the updated Lexicon, and new data must be valid under the old Lexicon."
7. **Lexicon: Lexicon Evolution.** "If larger breaking changes are necessary, a new Lexicon name must be used."
8. **XRPC: Inter-Service Authentication (JWT).** "Receiving services must verify that the audience field matches their own DID and service type, to prevent reuse or forwarding of tokens."
9. **Sync: Repository Revisions.** "The revision must always increase between commits for the same repository, even if the account migrates between hosts or has an extended period of inactivity."
10. **Cryptography: ECDSA Signature Malleability.** "In atproto, use of the "low-S" signature variant is required for both `p256` and `k256` curves."
11. **Cryptography: ECDSA Signature Malleability.** "In atproto, signatures should always be verified using the verification routines provided by the cryptographic library, never by comparing signature values as raw bytes."

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
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `did`, `did-methods`, `oauth`, `jwt`, `websocket`, `json`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [AT Protocol (overview) (atproto.com/specs/atp)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/atp/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [AT Protocol DIDs (atproto.com/specs/did)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/did/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Handles (atproto.com/specs/handle)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/handle/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Repository (atproto.com/specs/repository)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/repository/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Data Model (atproto.com/specs/data-model)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/data-model/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Lexicon (atproto.com/specs/lexicon)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/lexicon/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [HTTP API (XRPC) (atproto.com/specs/xrpc)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/xrpc/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Data Synchronization (atproto.com/specs/sync)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/sync/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
- [Cryptography (atproto.com/specs/cryptography)](https://raw.githubusercontent.com/bluesky-social/atproto-website/7937e9cc5119a670311ac933d34fa7a0de04b0e9/src/app/%5Blocale%5D/specs/cryptography/en.mdx): Specification, bluesky-social/atproto-website commit 7937e9c, 2026-10-02, checked 2026-10-06.
