---
name: nist-pqc
description: >-
  NIST post-quantum cryptography: implement ML-KEM, ML-DSA and SLH-DSA from FIPS 203, 204 and 205. Covers FIPS 203, FIPS 204, FIPS 205, SP 800-227. Use when implementing NIST post-quantum cryptography. Triggers: FIPS 203, FIPS 204, FIPS 205.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NIST PQC

NIST post-quantum cryptography standards: FIPS 203 (ML-KEM key encapsulation), FIPS 204 (ML-DSA signatures), FIPS 205 (SLH-DSA stateless hash-based signatures) and SP 800-227 (recommendations for using key-encapsulation mechanisms).

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing NIST post-quantum cryptography.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: implementer of ML-KEM, ML-DSA or SLH-DSA, or an application or protocol designer using a KEM for key establishment.
- Target version: FIPS 203 (default); FIPS 204 (default); FIPS 205 (default); SP 800-227 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 3.3.** "The public-key encryption scheme K-PKE described in Section 5 shall not be used as a stand-alone cryptographic scheme."
2. **§ 7.1.** "While the encapsulation key can be made public, the decapsulation key shall remain private."
3. **§ 7.2.** "ML-KEM.Encaps shall not be run with an encapsulation key that has not been checked as above."
4. **§ 7.3.** "Ciphertext checking shall be performed with every execution of ML-KEM.Decaps."
5. **RM5.** "The key-establishment process that takes place over the channel used by Alice and Bob must satisfy an application-appropriate notion of integrity."

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

- [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf): FIPS, FIPS 203, fetched 2026-10-06 (FIPS, 2026-10-06), checked 2026-10-06.
- [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf): FIPS, FIPS 204, fetched 2026-10-06 (FIPS, 2026-10-06), checked 2026-10-06.
- [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf): FIPS, FIPS 205, fetched 2026-10-06 (FIPS, 2026-10-06), checked 2026-10-06.
- [SP 800-227](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-227.pdf): NIST SP, SP 800-227, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
