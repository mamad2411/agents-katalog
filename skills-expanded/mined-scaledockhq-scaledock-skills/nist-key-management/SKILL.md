---
name: nist-key-management
description: >-
  NIST key management: generate, protect, rotate and retire cryptographic keys by SP 800-57, SP 800-131A and SP 800-132. Covers SP 800-57 Part 1 Rev 5, SP 800-131A Rev 2, SP 800-132. Use when managing cryptographic keys. Triggers: SP 800-57, SP 800-131A, SP 800-132.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NIST key management

NIST key management guidance: SP 800-57 Part 1 Rev 5 (general key management, key types, cryptoperiods, protection and compromise), SP 800-131A Rev 2 (transitioning algorithms and key lengths) and SP 800-132 (password-based key derivation for storage applications).

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when managing cryptographic keys.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: developer, architect or key manager generating, storing, using, rotating or destroying cryptographic keys, or reviewing a key management system.
- Target version: SP 800-57 Part 1 Rev 5 (default); SP 800-131A Rev 2 (default); SP 800-132 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 5.2.** "In general, a single key shall be used for only one purpose (e.g., encryption, integrity authentication, key wrapping, random bit generation, or digital signatures)."
2. **§ 5.5.1.** "When a key is compromised, all use of the key to apply cryptographic protection to information (e.g., compute a digital signature or encrypt information) shall cease, and the compromised key shall be revoked (see Section 8.3.5)."
3. **§ 6.1.** "Integrity protection shall be provided for all key information."
4. **§ 3.** "Private-key lengths providing less than 112 bits of security shall not be used to generate digital signatures."
5. **§ 5.** "Since most user-chosen passwords have low entropy and weak randomness properties, as discussed in Appendix A.1, these passwords shall not be used directly as cryptographic keys."

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

- [SP 800-57 Part 1 Rev 5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf): NIST SP, SP 800-57 Part 1 Rev 5, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-131A Rev 2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf): NIST SP, SP 800-131A Rev 2, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-132](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf): NIST SP, SP 800-132, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
