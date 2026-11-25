---
name: typography
description: Review or mechanically format English and Russian text for microtypography, protected word pairs, punctuation and symbol artifacts, and spelling while keeping editorial choices separate from safe corrections. Use when polishing prose or UI copy after the wording is settled, or when an agent-generated draft contains suspicious dashes, symbols, spacing, or Markdown residue. Triggers on typography, microtypography, typographic cleanup, nonbreaking spaces, protected pairs, punctuation cleanup, spelling pass, editorial pass, LLM artifacts, smart quotes, Russian typography, английская типографика, русская типографика, неразрывные пробелы, редактура текста.
---

# Typography

**Announce at start:** "I'm using the humane:typography skill to separate safe typographic corrections from editorial choices."

Polish text without taking authorship away from its author. This skill owns
mechanical microtypography and an editorial/spelling review. It may apply only
corrections whose meaning, voice, and cadence do not change; everything else is
a proposal.

## Boundary

| Concern | Owner |
| --- | --- |
| What a string says, its vocabulary, voice, and purpose | `ux-writing` |
| Nonbreaking spaces, protected pairs, quote/dash/space mechanics, obvious symbol residue | `typography` |
| Typeface selection and script coverage | `type-specimen` |
| Text measure, truncation, wrapping, and whether translated copy fits | `layout-rules` |
| Product terminology or a disputed spelling fixed by a house dictionary | The project's style guide; flag the conflict |

Do not rewrite for concision, vary repeated words, remove sentence fragments,
or reduce dash frequency under the label “cleanup.” Those are authorial choices.

## Establish the contract

Before recommending a rule that differs by language or standard, establish:

1. **Language:** English, Russian, or named spans of each in mixed text.
2. **Standard:** the project's house style if one exists; otherwise the named
   editorial/typographic standard (for example Chicago or New Hart's Rules for
   English; Lopatin, Milchin, or a publisher's house style for Russian).
3. **Medium:** plain text, Markdown, interface string, HTML source, or print.

Read nearby content, localization metadata, and the project style guide first.
If language or standard is unstated and the answer would materially change a
recommendation, **ask the user before making that recommendation**. Do not
silently choose US vs British spelling, quote style, serial-comma policy,
Russian `ё` policy, dash convention, or how aggressively short words are
protected. If the distinction cannot affect the requested mechanical check,
continue and state the narrow assumption instead of asking ceremonially.

For mixed-language text, apply each language's rules only inside the span whose
language is known. Never normalize a quoted title, command, URL, code span,
identifier, captured user quote, or brand spelling merely because it looks
foreign.

## Quick reference

| Need | Read |
| --- | --- |
| English spacing, protected pairs, quotes, dashes | [english.md](references/english.md) |
| Russian spacing, protected pairs, quotes, dashes | [russian.md](references/russian.md) |
| Mechanical vs editorial decisions, spelling, artifact triage, report shape | [editorial-pass.md](references/editorial-pass.md) |

Read only the language reference that applies. Read both for mixed-language
text, and label the boundaries used.

## Pass 1 — Mechanical corrections

Inspect the smallest complete source that preserves context. Protect code,
URLs, file paths, identifiers, Markdown destinations, placeholders, template
syntax, and verbatim quotations from automated replacement.

Classify a change as mechanical only when there is one valid correction under
the established contract and no plausible shift in meaning or voice. Typical
mechanical work includes:

- required nonbreaking spaces and protected pairs;
- spaces around punctuation and symbols under the chosen language standard;
- unambiguous quote, apostrophe, dash, ellipsis, multiplication-sign, degree,
  number/unit, `№`, and `§` corrections;
- invisible or damaged Unicode such as zero-width residue, a replacement
  character, or a literal escaped Unicode sequence accidentally shown to a
  reader;
- orphan Markdown emphasis markers or duplicated punctuation only when the
  intended character is unambiguous.

The bundled helper provides a repeatable first pass and never writes source
files:

```bash
python3 scripts/typography.py check --language en --standard chicago path/to/text.md
python3 scripts/typography.py format --language ru --standard lopatin path/to/text.md
```

Use `-` for stdin. `check` emits a structured report; `format` emits corrected
text to stdout. Review its output before applying a patch. The helper is a
conservative detector, not an editorial authority: a clean run does not prove
the prose is correct. Its deliberately closed standard list is `chicago`,
`new-harts`, or `ap` for English and `lopatin`, `milchin`, or `gost` for Russian;
apply a project's custom house style in the human review rather than inventing
a CLI token for it.

## Pass 2 — Editorial and spelling review

Read [editorial-pass.md](references/editorial-pass.md). Report these separately
from the mechanical pass:

- spelling that depends on locale, house dictionary, `ё`, a proper name, or
  product terminology;
- punctuation with more than one defensible reading;
- sentence rhythm, fragments, repetition, paragraphing, tone, and dash density;
- suspicious LLM habits that may be intentional: symmetrical three-part lists,
  generic transitions, excessive headings, rhetorical contrasts, emoji, arrows,
  or repeated em dashes.

Offer a small set of concrete alternatives and explain the effect of each.
Never apply one until the user chooses it or has already authorized that class
of editorial change.

## Output contract

Always begin with **Context**: language, standard, medium, protected regions,
and assumptions.

For a formatting or apply request, keep **Mechanical corrections** (Location |
Before | After | Rule) and **Editorial choices** (Location | Current | Options |
Decision needed) in separate sections. “None” is valid; do not invent choices
to fill either table. End with **Verification**: helper command run, sources
inspected, and anything not verified.

For a standalone review, use the repository's shared review contract:

1. **Findings** — one table with Severity | Location | Before | After | Why and
   an added **Category** column whose value is `Mechanical` or `Editorial
   choice`. The category keeps the two classes separate without producing two
   reports. For an editorial choice, `After` contains the options, not a silent
   rewrite. Cap at 15 and never pad.
2. **Considered but Rejected** — two to five real candidates and why they were
   left alone.
3. **Verification** — what was actually checked; name any missing dictionary,
   house guide, language boundary, or runtime rendering check.
4. **Verdict** — exactly `Block`, `Needs changes`, or `Approve`.

Under `humane:review`, return only findings in the orchestrator's required
shape; its severity scale, consolidation, cap, and verdict win.

When the user asked for a review, remain read-only. When the user asked to apply
fixes, apply the mechanical section only, then pause on unresolved authorial
choices. Preserve the original file format and line endings.

## Safety and honesty

- A nonbreaking-space policy is not universal. Protect only pairs justified by
  the selected language, standard, and medium.
- “Looks AI-generated” is not a defect and cannot be inferred from punctuation.
  Report only the observable pattern and its reading cost.
- Never claim a full spelling check without the relevant dictionary or house
  word list. Name what was checked manually.
- Never normalize code-like content or external quotations without explicit
  authorization.
- The user's explicit words > the selected standard > the project's existing
  system > this skill's defaults > personal taste. Surface conflicts.
