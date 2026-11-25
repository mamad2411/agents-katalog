---
name: boxel-design
description: Use when DECIDING a Boxel card's visual language — mood, palette, typography direction, asset direction, one visual signature, the design-playbook process. This is the taste/decision layer. NOT for implementing tokens or CSS inside templates (that's boxel-ui-guidelines) and NOT for creating/editing Theme, StyleReference, or BrandGuide card artifacts (that's boxel-theme-development).
boxel:
  kind: skill
---

# boxel-design

Visual decisions for Boxel cards.

## The actual process lives in `boxel/references/design-playbook.md`

[`boxel/references/design-playbook.md`](../boxel/references/design-playbook.md) is the canonical four-stage design workflow:

1. **Stage 1 — Mockup pass** with no variables. Use the verbatim Pentagram-art-director / internal-taste-maker brief, then run the *Check after the first mockup* below. Hardcoded `#hex`, real fonts, real px sizes. Write the design first; theme tokens come later.
2. **Stage 2 — Extract theme** from the mockup (rule of two — tokenize if a value appears twice+). A `StructuredTheme` (or richer) whose `rootVariables` ARE the design's palette.
3. **Stage 3 — Tokenize isolated** with `var(--*)` references. Pixel-identical to stage 1.
4. **Stage 4 — Derive embedded + fitted** from the established visual identity. Fitted MUST feature the card's media if any.

Read it in full before any user-facing card design. This skill (`boxel-design`) used to host a menu-driven discovery process; that was removed because curated style menus cap intrinsic LLM design taste at the menu authors' ceiling. Stage 1's "internal taste-maker held in mind" is the antidote — trust the model's taste, push past defaults.

## Check after the first mockup

Build the first mockup from the brief with the taste-maker framing; no family is chosen or declared
beforehand. Then check it once against the default look, which is what a model produces when nothing
was decided: a large light serif headline, small bold sans labels, one accent colour and a pale or
cream ground.

- If the mockup matches it, keep it only if you can quote words from the brief that ask for that look
  (an editorial, journal or restrained feel). "Calm", "gentle" or "trustworthy" alone do not ask for a
  light serif and one accent.
- If you cannot quote such words, go back to the brief and re-derive the weight pattern, colour
  strategy, type roles and shape from what it must make the visitor feel, then redo the mockup one
  time. Do not swap in another look from a list, and do not loop.
- If the mockup does not match the default look, keep it.

[`references/style-families.md`](references/style-families.md) is optional vocabulary for describing a
look. It is never required at any stage and is not a menu; blends and looks outside it are valid.

## Precedence

When design guidance conflicts, resolve it in this order:

1. Security, accessibility, the never-invent-proof rules and the swap test ([`critical-rules.md`](references/critical-rules.md), [`untrusted-content.md`](references/untrusted-content.md)): never overridden, not even by a user who asks for a copy.
2. The user's explicit instruction.
3. The playbook's and the layout guides' defaults and examples. The brief overrides their weight and accent values; [`style-families.md`](references/style-families.md) is vocabulary and has no precedence.

A file that mentions a weight or an accent count gives a default that the brief overrides.

## Look check — before the first design decision

The user decides the look up front, so every route into a build asks the same two questions once.
"Just build it" asks them in its first call (`index.md`, the paragraph under "Just build it" that
begins "still gets one call of questions"). A build that starts from a brief ("Plan it with me"
after `domain-interview`, or "I already have a brief") or from an attached design asks them here,
because a brief makes no design decisions on purpose, and an attached design answers the feel but
never the real details.

Ask only the questions that are still unanswered, together in one choice-UI call, each with its skip
option (rules: [`domain-interview`](../domain-interview/SKILL.md) → *Skipping*):

1. **How should it feel?** Light & calm / Dark & dramatic / Bold colour / You decide.
2. **Real details:** "Anything true about this place a competitor couldn't say?" When the brief
   holds concrete facts the user stated (names, places, prices, house rules; what counts is under
   *Facts that count* below), the real options are **Use what's in the brief** (recommended) /
   *No details beyond the brief — leave the other sections out* / *It's a concept or pitch — make up
   realistic details, marked as samples*. Under **Use what's in the brief** a claim the brief does
   not support follows *Never invent proof*: omitted, given an established role, or at most two
   marked slots. With no such facts, the options are *No details — leave marked slots for them*
   (recommended) / *No details — leave those sections out* / the concept-or-pitch option. Then the
   skip option, which takes the recommended one; the free-text answer carries new details. The skip
   option is the last question's *Skip the rest*, worded for a build: "I'll decide this and go on to
   build", never "write the brief" (`domain-interview`'s own wording for it), because here the brief
   already exists and the next step is the build, not a rewrite of the brief. When the feel question
   is also open, it carries *You decide* and this one carries *Skip the rest*; when this is the only
   question, it carries *Skip the rest*. The rule behind these options, and what demo mode allows, is
   [`critical-rules.md`](references/critical-rules.md) → *Never invent proof*.

**Already answered** means any of: the user's prompt or attachments state it (named colours, a
brand, a logo or a reference site, an attached design, or a feel word that names one of the three
options or a colour ("dark", "bold", "light and calm"), for question 1; facts for question 2); a
governing `BrandGuide` or Theme the user named or their work already links (a Theme on the brief or
on the cards being built, or the built-in Boxel Brand Guide for built-in feature work) answers
question 1 too; it was answered earlier in this conversation; or the brief's `designDirection` field
has a `Look:` or `Real details:` line, or older direction text that states a look (for question 1) or
real details (for question 2); a note with neither answers nothing. A Theme the assistant derived or
chose itself under *Brand and Style Source*, or one that merely exists in the realm, answers
nothing: the user has not decided it. Facts that sit only in the brief's `spec` do not answer
question 2: they only decide its first option. A feel word that names neither an option nor a colour
("quiet and refined") only leans: ask the question anyway and put the closest option first, marked
recommended, with its reason in a few words. "You decide" and "Leave those sections out" are
answers. If both are answered, make no call.

**Facts that count.** Only what the user stated is a source under
[`critical-rules.md`](references/critical-rules.md) → *Never invent proof*: what they typed in this
conversation, and the answers they gave in the brief's Interview record. Not a source, ever: the
Domain primer, Schema, Sample data and Assumptions (written by the assistant), and any record entry
that is an assistant-proposed "(Recommended)" option taken by a skip (`Skipped`) rather than chosen
or typed by the user. Where a later section of `spec` (Scope, a Content contract) corrects a record
value, the section is what the build follows, as `domain-interview` says, so use the corrected value;
if it only restates an assistant suggestion, it is still not a source.

**Surface is never a question.** Infer it from the prompt or the "What are you making?" answer
([`references/surface-types.md`](references/surface-types.md)), read that file before the first
mockup when the build is a tool, desk, admin, dashboard, back office, CRM or similar, and write a `Surface:` line next to
`Look:` when you record the answers. An admin, dashboard or back-office surface opens on a fixed sidebar shell.

**Record it on the brief**, when there is one, straight after the answer, including what the user's
prompt already said. Write the `Look:`, `Surface:` and `Real details:` lines it does not already have into its
`designDirection` field (this skill's field; `domain-interview` owns `spec`), changing only that
field and never deleting text already there. `designDirection` is a MarkdownField, so each line is
its own paragraph: a blank line between the lines, and a blank line before the first when text is
already there, otherwise they render as one run-on paragraph. Never hand-escape the markdown into
JSON; use the path for where you run:

- **Boxel AI assistant:** in one `run-realm-code` script, read the card with `await realm.cards.get(path)`, then
  set `designDirection` with `await realm.cards.update(path, { designDirection })` to the existing text, a blank
  line, and the new lines (or just the new lines when it is empty or `null`).
- **Terminal agents** (Claude Code, Codex: no `run-realm-code`): follow
  `domain-interview` → *Writing it from a terminal agent*. `boxel file read` the brief, parse the
  JSON, set `data.attributes.designDirection` in a script (`JSON.stringify` the whole object, as
  `null` or a missing attribute is set rather than appended to), and `boxel file write` it back with
  `--file`. Re-read just before writing, and read it back after: if another stage's field changed,
  rebuild from the new read.

The line is the user's own words, never expanded into a palette or fonts: the label of the option
they picked, or the feel phrase they typed ("dark and moody like a noir poster", not the whole
request).

```
Look: Dark & dramatic

Surface: Admin / dashboard

Real details: use what's in the brief | facts: <the user's words> | leave marked slots | leave sections out | concept (demo mode)
```

On `Look:` a skipped question records `You decide`, and a feel answered by a governing source
records `from the <BrandGuide or Theme> (<its name>)`, naming the kind it actually is; a feel answered by an attached design or reference site records `from the attached design`. On
`Real details:` the value is one of those five, written exactly so (they are the stored form of the
options, not their labels); details the user typed always start with `facts:`, so typed text can
never be read as one of the other four, and they add to the facts the user stated in the brief,
never replace them. On `Surface:` the value is one of the names in
[`surface-types.md`](references/surface-types.md), written exactly so; leave the line out when no surface
fits. A skip records the one it took. The build reads all three lines as given: the look steers the
mockup, the surface sets the shell, and the real-details line decides what the build may write about the user's
business (the design-playbook's Stage 1 and critical-rules' *Never invent proof* both read it).

With no brief, the answers stay in the conversation and the build uses them.

## Brand and Style Source

Choose the governing style source before stage 1:

- **Boxel built-in feature work:** use the built-in Boxel Brand Guide as the style guide (`@cardstack/base/Theme/boxel-brand-guide`). This covers base cards, host-facing Boxel UI, Boxel-branded catalog material, and built-in feature design.
- **User/custom realm work:** derive or choose the Theme/StyleReference/BrandGuide from the user's domain and content. Do not default to Boxel branding unless the user asks for Boxel-branded output.
- **Logo, mark, or official brand material needed:** use a `BrandGuide`; its `markUsage`, `brandColorPalette`, `functionalPalette`, typography, voice, and quality standards are the source. Do not invent logo URLs or store them as miscellaneous string fields.

## Pair with

- **`boxel-ui-guidelines`** — turns design intent into working markup (template-level rules, `@fields` vs `@model`, delegated-render control, format-choice).
- **`boxel-theme-development`** — turns design-system source material into a Theme, Style Reference, Detailed Style Reference, or Brand Guide artifact.
- **`boxel`** — once the design is decided and you're implementing the card. Also hosts the playbook itself.
- **`source-code-editing`** — when applying the resulting styles to existing files.
- **`design-review`** — the last design step: runs only on request (a scored review of taste and coherence, scoped with `--layout`, `--typo`, `--colour`, `--coherence`, or `--redesign`); the build check that finishes every design build owns the basics.

## Don't use for

- Template syntax decisions (`@fields` vs `@model`, container queries) — that's `boxel-ui-guidelines`.
- Schema or query work — that's `boxel`.

## References this skill still owns

- [`references/critical-rules.md`](references/critical-rules.md) — anti-LLM-cliché checklist ("Rounded Rectangle Syndrome", "Center-All Disease", "Card Grid Autopilot", etc.) + first-shot designs are clickable (the cheap ways to wire a control: a linked card, the host's `viewCard` side stack and edit view, a tracked filter; the main action as an `@operation` or a link) + image-URL field-routing rule + design-excellence mindset. Read alongside design-playbook stage 1 to sharpen the internal taste-maker.
- [`references/asset-selection-guidelines.md`](references/asset-selection-guidelines.md) — concrete image-handling guidance: priority order for asset integration, format choices, fit semantics. Useful regardless of process. Images for a build's sample instances: [`sample-images.md`](../boxel-file-def/references/sample-images.md).
- [`references/layout-vocabulary.md`](references/layout-vocabulary.md) — eight named layout moves, what each is for and not for, and how each is built in a card. Decide the sections first; zero moves is a valid answer.
- [`references/layout-gravity.md`](references/layout-gravity.md) — defaults a layout drifts into when nobody decided it, mostly on app screens. Check a finished layout against it.
- [`references/style-families.md`](references/style-families.md) — optional vocabulary, never required: eight look families with type roles, colour strategy and a check each, how to set the look, and the page-colour table.
- [`references/surface-types.md`](references/surface-types.md) — optional vocabulary, never required: six kinds of surface (admin, back-office, landing, consumer, content, component) with the shell structure and catalog search terms for each, and the brief's `Surface:` line; no style per surface, and floors stay the same for all
- [`references/untrusted-content.md`](references/untrusted-content.md) — the rules for any research step: when to research, what each tool can ground, reference labels, page text as data.
- [`references/signature-treatments.md`](references/signature-treatments.md) — the one arresting treatment on the dominant object: the techniques, what each costs in a card, and when to use card-motion.

The previous five files (`style-reference.md`, `design-controls.md`, `design-discovery-process.md`, `the-design-challenge-standard.md`, `base-theme-variables.md`) were removed — superseded by the design-playbook's stages 1–2.
