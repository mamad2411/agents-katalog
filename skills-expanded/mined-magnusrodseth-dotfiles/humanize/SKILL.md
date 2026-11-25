---
name: humanize
description: "Rewrite prose that sounds AI-generated while preserving meaning, evidence and the author's voice. Use for humanize this, de-slop, sounds like ChatGPT, or make this less AI."
---

# Humanize

Remove formulaic writing while preserving what the author says and how certain they are.
Make the smallest useful edit. Clean text may stay unchanged.

## Scope

Use for editing existing prose. Preserve the author's facts, argument, register and intent.
Style patterns suggest places to inspect; they do not establish who wrote a text.

Word choice and sentence rhythm matter, but a longer piece also needs coherent paragraphs
and enough information for its purpose. An explanation can succeed without a contestable
position. A personal message can succeed without numbers or citations.

The studies in [sources](references/sources.md) include fiction and creative non-fiction.
Their transfer to Norwegian messages and technical documentation is a working assumption.
Detector scores and sentence-length statistics are not editing targets.

## Workflow

### 1. Establish the reading context

Read the text before changing it. Identify its audience, purpose, genre and existing register.
Use the request and known context first. If you infer something material, state it briefly.
Ask only when an unresolved choice would substantially change the edit.

If the text is Magnus's own, load [write-in-my-voice](../write-in-my-voice/SKILL.md).
Load [writing-whip](../writing-whip/SKILL.md) before writing replacement sentences.
Read linked files directly where no Skill tool exists. Do not reload files already read.

Choose depth from the request:

| Depth | Use |
|---|---|
| Quick | Short messages or a narrow request. Fix the named issues; preserve structure. |
| Standard | Longer prose. Check sentences and paragraph coherence without expanding the remit. |
| Full | An explicit editorial review. Include audience fit, structure and precise finding locations. |

Keep quoted source text, code, formulas, identifiers and citation keys unchanged unless
their correction is explicitly in scope. Typography preferences apply to editable prose.

### 2. Scan and triage

Read [tells](references/tells.md), [risk tiers](references/risk-tiers.md) and
[rewrite patterns](references/rewrite-patterns.md). Use [scans](references/scans.md) to
locate candidates in files; inspect pasted text directly when no file exists.

Always inspect citation artifacts, reply-shaped scaffolding and emphatic colons.
For Norwegian, check English and Norwegian negative parallelisms in the same pass.
A scoped request limits the changes you apply. Mention material findings outside that scope.

Judge every match in context. A technical term, useful heading, factual contrast or genuine
list may be correct. Keep it. Do not identify a text as AI-written from style matches.

### 3. Apply authorized edits

Apply Tier 1 and Tier 2 edits. For Tier 3, use the user's existing authorization.
An explicit request to restructure permits restructuring; it does not permit invented content.
If a material choice remains unresolved, leave that passage intact and ask a focused question.
Batch related uncertainties. Do not ask about commas or permission already given.

Improve the prose at the register level: state the claim directly, keep the relevant
qualification, and remove setup that contributes nothing. Avoid replacing one formula with another.
Use [rewrite toward human](references/rewrite-toward-human.md) for longer prose.
Sentence splits and reordering are safe only when attribution, scope and logical relations survive.

When information is missing, name the gap outside the text. Do not insert an invented fact
or a placeholder into the author's prose. A wording edit does not verify a factual claim.

### 4. Check meaning before style

Compare every changed passage with the original and any supplied supporting material.
This check takes priority over every stylistic preference.

| Preserve | Check |
|---|---|
| Facts | Names, dates, values, units, populations and experimental conditions remain correct. |
| Logic | Negation, causality, comparisons and quantifiers retain their scope. |
| Evidence | Attribution, citation keys and the distinction between observation and interpretation survive. |
| Confidence | May, suggests, often, most and other substantive qualifications keep their force. |
| Voice | Pronouns, register and supplied opinions or experiences still belong to the author. |

Check who acts before changing a passive. Keep passive when context makes attribution clear
or the subject appropriately names a system property. Never invent an actor to make it active.
Keep established terminology consistent and define it only when supplied context and audience need it.
Missing comparison baselines or evidence are gaps to flag, not details to manufacture.

Revert an edit that fails this check. Remove ornamental emphasis only when its deletion
does not weaken or strengthen the actual claim. A source that exists may still fail to support it.

### 5. Check purpose and register

For longer prose, assess these dimensions qualitatively:

| Dimension | What passes |
|---|---|
| Purpose | The text does what this genre and reader need. Argumentative prose keeps its supplied position. |
| Precision | Relevant terms and comparisons are clear. Specificity comes only from supplied facts. |
| Restraint | Changes address real problems. Necessary clarification may increase word count; filler does not. |
| Register | Formal text stays formal; personal text retains its voice. Rhythm serves meaning. |

For a short message, a final reading is enough. Do not add an opinion, statistic, anecdote,
fragment or first-person statement to satisfy an assessment dimension.

Make one revision pass if needed, then stop. If improvement requires missing facts or
an unresolved author decision, return the safe edit and name the gap. Repeated polishing cannot supply it.

### 6. Re-scan the final version

Recheck the edited passages after the last change, including the meaning check.
Resolve unwanted artifacts. Keep legitimate contextual matches and protected quotations.
The stopping condition is a faithful, useful edit, not an empty grep or a detector score.

## Output

Return the rewritten text. Add a short note only for material changes, retained ambiguities
or missing information. A full review gives the original span, its actual location, the
reason and a supported rewrite; when a rewrite needs facts, report the gap instead.

Do not reproduce every clean paragraph or append routine scores and fix counts.
Provide those only when requested. If the text is already clean, return it unchanged and say so.

## Standing preferences

- Use full sentences and plain verbs. Cut empty emphasis and repeated previews or summaries.
- Replace em dashes in editable prose with commas, parentheses or a sentence split that preserves meaning.
  Do not replace them with emphatic colons. Keep colons for genuine lists, quotations and useful labels.
- Use straight ASCII quotes in editable prose. Preserve exact quotations and code.
- Preserve Norwegian spelling and æ, ø, å, including uppercase forms.
- Keep valid technical terms, informative headings and real lists. A set of three distinct facts stays complete.
- Preserve deliberate voice. Do not casualize formal prose or manufacture emotion, uncertainty or a personal stance.

## Evaluation

Use the cases and comparison procedure in [evaluation](references/evaluation.md) when
revising this skill. They test meaning preservation and genre fit. Static checks alone
do not demonstrate better generated writing.
