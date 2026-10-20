---
name: sarif
description: >-
  SARIF: write and read Static Analysis Results Interchange Format logs. Covers SARIF 2.1.0 (current) and tracks the SARIF 2.2 Committee Specification Draft as a preview. Use when exchanging static analysis results. Triggers: SARIF, static analysis results.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SARIF

https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.docx

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging static analysis results.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: SARIF 2.1.0 (default); SARIF 2.2 (preview, posture: track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Terminology.** "The key words �MUST�, �MUST NOT�, �REQUIRED�, �SHALL�, �SHALL NOT�, �SHOULD�, �SHOULD NOT�, �RECOMMENDED�, �NOT RECOMMENDED�, �MAY�, and �OPTIONAL� in this document are to be interpreted as described in � Key words for use in RFCs to Indicate Requirement Levels� [ BCP14 ] [ RFC2119 ] and �Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words� [ RFC8174 ] when, and only when, they appear in…"
2. **3.1 General.** "A SARIF log file SHALL contain a serialization of the SARIF object model into the JSON format."
3. **3.1 General.** "The top-level value in the log file, representing the sarifLog object, SHALL conform to the JSON object grammar; that is, it SHALL consist of a comma-separated sequence of name/value pairs, enclosed in curly brackets, as specified by JSON [ RFC8259 ]."
4. **3.1 General.** "A SARIF log file SHALL be encoded in UTF-8 [ RFC3629 ]."
5. **3.2 SARIF file naming convention.** "The file name of a SARIF log file SHOULD end with the extension ".sarif" ."
6. **3.3.2 text property.** "If the external artifact is a text artifact, an artifactContent object SHOULD contain a property named text whose value is a string containing the relevant text."
7. **3.3.2 text property.** "Since SARIF log files are encoded in UTF-8 ([ RFC3629 ]; see �3.1), this means that if the external artifact is a text artifact in any encoding other than UTF-8, the SARIF producer SHALL transcode the text to UTF-8 before assigning it to the text property."
8. **3.3.2 text property.** "The SARIF producer SHALL escape any characters that JSON [ RFC8259 ] requires to be escaped."

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

- [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html): OASIS Standard, SARIF 2.1.0, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
- [SARIF 2.2 draft](https://raw.githubusercontent.com/oasis-tcs/sarif-spec/adbb670c018335b0f384e6dd8819f4ea055d7ee1/sarif-2.2/prose/share/sarif-v2.2-draft.md): Committee Specification Draft, SARIF 2.2 Committee Specification Draft 01, 2026-03-05 (editor draft at commit adbb670), checked 2026-10-06.
