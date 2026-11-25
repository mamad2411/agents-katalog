---
name: pkcs11
description: >-
  PKCS #11 3.1: use HSMs and cryptographic tokens through the Cryptoki interface. Covers PKCS #11 3.1. Use when using a cryptographic token interface. Triggers: PKCS #11, cryptoki.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# PKCS #11

https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/cs01/pkcs11-spec-v3.1-cs01.pdf

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when using a cryptographic token interface.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: PKCS #11 3.1 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **document.** "Key words: The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [ RFC2119 ] and [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **2 Platform-.** "This means that when writing C or C++ code, certain preprocessor directives MUST be issued before including a Cryptoki header file."
3. **2.1 Structure packing.** "Cryptoki structures are packed to occupy as little space as is possible.� Cryptoki structures SHALL be packed with 1-byte alignment."
4. **2.2 Pointer-related macros.** "Because different platforms and compilers have different ways of dealing with different types of pointers, the following 6 macros SHALL be set outside the scope of Cryptoki: � CK_PTR CK_PTR is the �indirection string� a given platform and compiler uses to make a pointer to an object.� It is used in the following fashion: typedef CK_BYTE CK_PTR CK_BYTE_PTR; � CK_DECLARE_FUNCTION…"
5. **3.** "When including either of these header files, a source file MUST specify the preprocessor directives indicated in Section 2."
6. **3.1 General information.** "���������������������������������������� flags ������ bit flags reserved for future versions.� MUST be zero for this version ���������������������� libraryDescription ������ character-string description of the library.� MUST be padded with the blank character (� �).� Should not be null-terminated."
7. **3.2 Slot and token types.** "������������������������� manufacturerID ������ ID of the slot manufacturer.� MUST be padded with the blank character (� �).� MUST NOT be null-terminated."
8. **3.2 Slot and token types.** "label, assigned during token initialization.� MUST be padded with the blank character (� �).� MUST NOT be null-terminated."

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

- [PKCS #11 3.1](https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/pkcs11-spec-v3.1.html): OASIS Standard, PKCS #11 3.1, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
