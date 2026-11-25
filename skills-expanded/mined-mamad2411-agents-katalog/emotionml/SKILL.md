---
name: emotionml
description: >-
  EmotionML: As the Web is becoming ubiquitous, interactive, and multimodal, technology needs to deal increasingly with human factors, including emotions. Covers Emotion Markup Language (EmotionML) 1.0. Use when annotating emotion. Triggers: EmotionML.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# EmotionML

As the Web is becoming ubiquitous, interactive, and multimodal, technology needs to deal increasingly with human factors, including emotions. The specification of Emotion Markup Language 1.0 aims to strike a balance between practical applicability and scientific well-foundedness. The language is conceived as a "plug-in" language suitable for use in three different areas: (1) manual annotation of data; (2) automatic recognition of emotion-related states from user behavior; and (3) generation of emotion-related system behavior.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when annotating emotion.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Emotion Markup Language (EmotionML) 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Conventions of this document.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [ RFC2119 ]."
2. **2.1.1 Document root: The <emotionml>.** "Documents using this specification MUST use 1.0 for the value."
3. **2.1.1 Document root: The <emotionml>.** "The attribute MUST be of type xsd:anyURI and MUST refer to the ID of a <vocabulary> element defining an emotion vocabulary with type="category" , as specified in Defining vocabularies for representing emotions ."
4. **2.1.1 Document root: The <emotionml>.** "The attribute MUST be of type xsd:anyURI and MUST refer to the ID of a <vocabulary> element defining an emotion vocabulary with type="dimension" , as specified in Defining vocabularies for representing emotions ."
5. **2.1.1 Document root: The <emotionml>.** "The attribute MUST be of type xsd:anyURI and MUST refer to the ID of a <vocabulary> element defining an emotion vocabulary with type="appraisal" , as specified in Defining vocabularies for representing emotions ."
6. **2.1.1 Document root: The <emotionml>.** "The attribute MUST be of type xsd:anyURI and MUST refer to the ID of a <vocabulary> element defining an emotion vocabulary with type="action-tendency" , as specified in Defining vocabularies for representing emotions ."
7. **2.1.1 Document root: The <emotionml>.** "The root element of a standalone EmotionML document MUST be <emotionml> ."
8. **2.1.1 Document root: The <emotionml>.** "The <emotionml> element MUST define the EmotionML namespace : 'http://www.w3.org/2009/10/emotionml'."

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

- [Emotion Markup Language (EmotionML) 1.0](https://www.w3.org/TR/emotionml/): Recommendation, emotionml REC-emotionml-20140522 (Recommendation, 2014-05-22), checked 2026-10-06.
