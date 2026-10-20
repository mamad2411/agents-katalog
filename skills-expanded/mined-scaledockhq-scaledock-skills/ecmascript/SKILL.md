---
name: ecmascript
description: >-
  ECMAScript (ECMA-262): write and review JavaScript against a published ECMAScript edition. Covers ECMAScript 2026, ECMAScript 2025 (supported), ECMAScript 2024 (supported), ECMAScript 2027 (track preview). Use when writing JavaScript against a published ECMAScript edition. Triggers: ECMAScript, ECMA-262, ES2026.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# ECMAScript

- 5 Notational Conventions + 5.1 Syntactic and Lexical Grammars 5.1.1 Context-Free Grammars

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing JavaScript against a published ECMAScript edition.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: ECMAScript 2026 (default); ECMAScript 2025 (supported); ECMAScript 2024 (supported); ECMAScript 2023 (legacy: read and upgrade, never author); ECMAScript 2027 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Software License.** "SEE THE ECMA CODE OF CONDUCT IN PATENT MATTERS AVAILABLE AT https://ecma-international.org/memento/codeofconduct.htm FOR INFORMATION REGARDING THE LICENSING OF PATENT CLAIMS THAT ARE REQUIRED TO IMPLEMENT ECMA INTERNATIONAL STANDARDS."
2. **Software License.** "IN NO EVENT SHALL ECMA INTERNATIONAL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)…"
3. **2 Conformance.** "A conforming implementation of ECMAScript must provide and support all the types, values, objects, properties, functions, and program syntax and semantics described in this specification."
4. **2 Conformance.** "A conforming implementation of ECMAScript must interpret source text input in conformance with the latest version of the Unicode Standard and ISO/IEC 10646."
5. **2 Conformance.** "A conforming implementation of ECMAScript that provides an application programming interface (API) that supports programs that need to adapt to the linguistic and cultural conventions used by different human languages and countries must implement the interface defined by the most recent edition of ECMA-402 that is compatible with this specification."
6. **2 Conformance.** "A conforming implementation of ECMAScript must not implement any extension that is listed as a Forbidden Extension in subclause 17.1 ."
7. **2 Conformance.** "A conforming implementation of ECMAScript must not redefine any facilities that are not implementation-defined , implementation-approximated , or host-defined ."
8. **2 Conformance.** "(See Annex B .) If any Normative Optional behaviour is implemented, all of the behaviour in the containing Normative Optional clause must be implemented."

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

- [ECMAScript 2026](https://tc39.es/ecma262/2026/): ECMA-262 edition, ECMAScript 2026 (ECMA-262 edition, 2026), checked 2026-10-06.
- [ECMAScript 2025](https://tc39.es/ecma262/2025/): ECMA-262 edition, ECMAScript 2025 (ECMA-262 edition, 2025), checked 2026-10-06.
- [ECMAScript 2024](https://tc39.es/ecma262/2024/): ECMA-262 edition, ECMAScript 2024 (ECMA-262 edition, 2024), checked 2026-10-06.
- [ECMAScript 2023](https://tc39.es/ecma262/2023/): ECMA-262 edition, ECMAScript 2023 (ECMA-262 edition, 2023), checked 2026-10-06.
- [ECMAScript 2027](https://tc39.es/ecma262/): Editor's draft, tc39.es/ecma262 draft titled ECMAScript 2027 (Editor's draft, 2026-10-06), checked 2026-10-06.
