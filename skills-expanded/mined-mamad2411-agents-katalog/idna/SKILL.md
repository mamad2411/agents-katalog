---
name: idna
description: >-
  IDNA (UTS #46): One of the great strengths of domain names is universality. Covers UTS #46, RFC 5890 IDNA, RFC 5891 IDNA protocol. Use when mapping internationalized domain names. Triggers: IDNA, UTS 46, RFC 5890.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# IDNA (UTS #46)

One of the great strengths of domain names is universality. The URL https://Apple.com goes to Apple's

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when mapping internationalized domain names.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UTS #46 (default); RFC 5890 IDNA (default); RFC 5891 IDNA protocol (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **UTS #46 § 3.** "Given a version of Unicode and a Unicode String, a conformant implementation of Nontransitional Processing shall replicate the results given by applying the Nontransitional Processing algorithm specified by Section 4, Processing."
2. **UTS #46 § 4.** "Normalize the domain_name string to Unicode Normalization Form C."
3. **UTS #46 § 4.1.** "The label must be in Unicode Normalization Form NFC."
4. **UTS #46 § 4.1.** "If CheckHyphens, the label must not contain a U+002D HYPHEN-MINUS character in both the third and fourth positions."
5. **UTS #46 § 4.1.** "For Nontransitional Processing, each value must be either valid or deviation."
6. **UTS #46 § 4.1.** "In addition, if UseSTD3ASCIIRules=true and the code point is an ASCII code point (U+0000..U+007F), then it must be a lowercase letter (a-z), a digit (0-9), or a hyphen-minus (U+002D)."
7. **UTS #46 § 4.2.** "If an error was recorded in steps 1-4, then the operation has failed and a failure value is returned. No DNS lookup should be done."
8. **RFC 5890 § 2.3.2.1.** "While that constraint may be tested in any of several ways, an A-label A1 must be capable of being produced by conversion from a U-label U1, and that U-label U1 must be capable of being produced by conversion from A-label A1."
9. **RFC 5891 § 3.1.** "A pair of A-labels MUST be compared as case-insensitive ASCII (as with all comparisons of ASCII DNS labels)."
10. **RFC 5891 § 3.2.** "IDNs actually appearing in DNS queries or responses MUST be A-labels."
11. **RFC 5891 § 4.2.3.1.** "The Unicode string MUST NOT contain "--" (two consecutive hyphens) in the third and fourth character positions and MUST NOT start or end with a "-" (hyphen)."

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
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [UTS #46](https://www.unicode.org/reports/tr46/): Unicode Technical Standard, UTS #46 (Unicode Technical Standard, 2026-10-06), checked 2026-10-06.
- [RFC 5890 IDNA](https://www.rfc-editor.org/rfc/rfc5890.html): RFC, RFC 5890 (RFC, 2010-08), checked 2026-10-06.
- [RFC 5891 IDNA protocol](https://www.rfc-editor.org/rfc/rfc5891.html): RFC, RFC 5891 (RFC, 2010-08), checked 2026-10-06.
