---
name: ttml
description: >-
  Timed Text Markup Language (TTML): This document specifies the Timed Text Markup Language (TTML), Version 2, also known as TTML2, in terms of a vocabulary and semantics thereof. Covers Timed Text Markup Language 2 (TTML2) (2nd Edition) (build), Timed Text Markup Language 1 (TTML1) (Third Edition), IMSC Text Profile 1.3, TTML Profiles for Internet Media Subtitles and Captions 1.2 (supported), TTML Profiles for Internet Media Subtitles and Captions 1.1 (supported), TTML Profiles for Internet Media Subtitles and Captions 1.0.1 (IMSC1) (supported), Dubbing and Audio description Profiles of TTML2 (build), IMSC Hypothetical Render Model. Use when authoring timed text or IMSC captions. Triggers: TTML, IMSC, DAPT.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Timed Text Markup Language (TTML)

This document specifies the Timed Text Markup Language (TTML), Version 2, also known as TTML2, in terms of a vocabulary and semantics thereof. The Timed Text Markup Language is a content type that represents timed text media for the purpose of interchange among authoring systems. Timed text is textual information that is intrinsically or extrinsically associated with timing information. It is intended to be used for the purpose of transcoding or exchanging timed text information among legacy distribution content formats presently in use for subtitling and captioning functions. In addition to being used for interchange among legacy distribution content

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when authoring timed text or IMSC captions.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Timed Text Markup Language 2 (TTML2) (2nd Edition) (default, posture build); Timed Text Markup Language 1 (TTML1) (Third Edition) (default); IMSC Text Profile 1.3 (default); TTML Profiles for Internet Media Subtitles and Captions 1.2 (supported); TTML Profiles for Internet Media Subtitles and Captions 1.1 (supported); TTML Profiles for Internet Media Subtitles and Captions 1.0.1 (IMSC1) (supported); Dubbing and Audio description Profiles of TTML2 (default, posture build); IMSC Hypothetical Render Model (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Document Example.** "Example Fragment – TTML Body <body region="subtitleArea"> <div> <p xml:id="subtitle1" begin="0.76s" end="3.45s"> It seems a paradox, does it not, </p> <p xml:id="subtitle2" begin="5.0s" end="10.0s"> that the image formed on<br/> the Retina should be inverted?"
2. **2.2 Terminology.** "[content profile] A profile such that (1) the value of the type component of the associated profile instance is content and (2) the collection of features and extensions of which must not, must, or may be employed by Timed Text Markup Language content."
3. **2.2 Terminology.** "[processor profile] A profile such that (1) the value of the type component of the associated profile instance is processor and (2) the collection of features and extensions of which must or may be implemented (supported) by a content processor."
4. **2.3 Documentation Conventions.** "Within normative prose in this specification, the words may , should , and must are defined as follows: may Conforming documents and/or TTML processors are permitted to, but need not behave as described."
5. **2.3 Documentation Conventions.** "should Conforming documents and/or TTML processors are strongly recommended to, but need not behave as described."
6. **2.3 Documentation Conventions.** "must Conforming documents and/or TTML processors are required to behave as described; otherwise, they are in error."
7. **2.3 Documentation Conventions.** "If normative specification language takes an imperative form, then it is to be treated as if the term must applies."
8. **2.3 Documentation Conventions.** "Furthermore, if normative language takes a declarative form, and this language is governed by must , then it is also to be treated as if the term must applies."

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

- [Timed Text Markup Language 2 (TTML2) (2nd Edition)](https://www.w3.org/TR/ttml2/): Candidate Recommendation Snapshot, ttml2 REC-ttml2-20181108 (Candidate Recommendation Snapshot, 2021-03-09), checked 2026-10-06.
- [Timed Text Markup Language 1 (TTML1) (Third Edition)](https://www.w3.org/TR/ttml1/): Recommendation, ttml1 REC-ttml1-20181108 (Recommendation, 2018-11-08), checked 2026-10-06.
- [IMSC Text Profile 1.3](https://www.w3.org/TR/ttml-imsc1.3/): Recommendation, ttml-imsc1.3 REC-ttml1-20181108 (Recommendation, 2026-05-21), checked 2026-10-06.
- [TTML Profiles for Internet Media Subtitles and Captions 1.2](https://www.w3.org/TR/ttml-imsc1.2/): Recommendation, ttml-imsc1.2 REC-ttml1-20181108 (Recommendation, 2020-08-04), checked 2026-10-06.
- [TTML Profiles for Internet Media Subtitles and Captions 1.1](https://www.w3.org/TR/ttml-imsc1.1/): Recommendation, ttml-imsc1.1 REC-ttml2-20181108 (Recommendation, 2018-11-08), checked 2026-10-06.
- [TTML Profiles for Internet Media Subtitles and Captions 1.0.1 (IMSC1)](https://www.w3.org/TR/ttml-imsc1.0.1/): Recommendation, ttml-imsc1.0.1 REC-ttml-imsc1.0.1-20180424 (Recommendation, 2018-04-24), checked 2026-10-06.
- [Dubbing and Audio description Profiles of TTML2](https://www.w3.org/TR/dapt/): Candidate Recommendation Draft, dapt CRD-dapt-20260626 (Candidate Recommendation Draft, 2026-06-26), checked 2026-10-06.
- [IMSC Hypothetical Render Model](https://www.w3.org/TR/imsc-hrm/): Recommendation, imsc-hrm REC-ttml2-20181108 (Recommendation, 2024-04-25), checked 2026-10-06.
- [TTML Media Type Definition and Profile Registry](https://www.w3.org/TR/ttml-profile-registry/): Note, ttml-profile-registry (Note, 2026-07-02), checked 2026-10-06.
