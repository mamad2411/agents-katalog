---
name: report-writing
description: "How to write the prose of a report or document for the people who will read it: establish the audience first by prompting the user, lead with a plain-language summary and push technical detail later or into appendices, cut jargon, and avoid the stock phrasing that marks text as machine-written. Use whenever drafting, revising, or reviewing report text, a README narrative, a user guide, a summary, or any document someone other than the user will read."
when_to_use: "Drafting or editing prose in a .qmd/.Rmd report, README, user guide, INFO or methods document; asked to 'write up', 'summarise', 'review the reports for readability', 'reduce jargon', or 'make this clearer'; writing a description of a problem or fix for someone else to read."
paths:
  - "**/*.qmd"
  - "**/*.Rmd"
  - "**/reports/**"
  - "**/README.md"
  - "**/docs/**"
---

# Writing for the reader

The same results need different documents for a funder, a forest ecologist, and a
developer. Writing before knowing which one is reading is the most common reason a
report needs a second full pass.

## 1. Establish the audience first -- always prompt for it

Before drafting or revising, ask the user who the audience is, using an explicit
prompt (AskUserQuestion), not a question buried in message text. If other
decisions are pending, batch them into the same prompt.

- If an audience is already recorded -- in the document's front matter, a project
  memory, or `CLAUDE.md` -- still prompt, but offer that audience as the first,
  recommended option so confirming it costs one click.
- If the user has already named the audience for this document in the current
  conversation, do not ask again.
- **The default, offered first unless the project says otherwise: scientists,
  especially ecologists, who are not programmers or software engineers.** That is who
  these documents are usually for, and it sets the register -- ecological terms of art
  are fine and need no gloss; target names, function names and file paths are not.
- Offer concrete options, adjusted to the project, for example:
  - scientists, especially ecologists, who do not model (the usual default);
  - domain scientists with some modelling background;
  - decision-makers, managers or funders, or a policy audience -- which can fix a
    unit choice, as reporting in CO2e rather than carbon does;
  - community or Indigenous partners, or rights holders whose authority governs how
    the results may be used;
  - technical collaborators who will run or extend the code;
  - peer reviewers.
- A single document can carry more than one of these. Where two registers genuinely
  both apply, write the body for the less technical one and give the other its own
  section or appendix, rather than blending them into prose that serves neither.
- If it is unclear what the reader needs to *do* with the document (decide
  something, reproduce something, review something), ask that in the same prompt.

Record the answer where the next session will find it, e.g. a comment in the
report's YAML front matter:

```yaml
## audience: forest ecologists and carbon accounting staff with some modelling experience;
##   want results and their implications, not implementation detail
```

## 2. Match the document to that audience

| Audience | Lead with | Keep in the body | Move to an appendix |
| --- | --- | --- | --- |
| Decision-makers, funders | what was found, what it means, how confident we are, what happens next | a few simple figures | methods, parameters, code-level detail |
| Domain scientists | rationale, key results with figures and tables, limitations | methods at the level needed to trust the results | implementation detail, configuration, full parameter tables, validation mechanics |
| Technical collaborators | the summary, then how it works | implementation detail, commands, identifiers | provenance, exhaustive tables |
| Partners, public | context and why it matters, in everyday words | the few results that matter to them | almost everything technical |
| Peer reviewers | the question and the answer | precise methods, statistics, citations | supplementary analyses |

When in doubt between two audiences, write for the less technical one and give the
other an appendix.

## 3. Structure: summary first, detail later

Order sections so a reader can stop early and still leave with the right idea:

1. **Summary** -- plain language, readable on its own, about half a page: what was
   done, what was found, what it means, what is uncertain, what comes next.
2. **Key findings** -- each finding stated in one sentence, then the figure or table
   that supports it.
3. **Methods overview** -- enough for this audience to trust the findings.
4. **Detailed results and discussion.**
5. **References.**
6. **Appendices** -- technical detail, parameters, configuration, validation
   mechanics, provenance.

Every section should open with its point, not build up to it. A figure caption's
first sentence says what the figure shows, not what it is a plot of.

## 4. Plain language

- **Say what things are, not what they are called in the code.** Target names,
  function names, option names, file paths and branch names belong in an appendix
  for most audiences. "The simulations that include fire" beats
  "the `ForCS_fire` scenario branches".
- **Define a technical term on first use**, or replace it. Expand acronyms the first
  time, and drop ones the reader will only meet once.
- **One term per concept, used consistently.** Do not alternate between synonyms,
  and keep similar-sounding processes clearly distinct -- a "fire calibration" and a
  "vegetation growth calibration" are different things and must never blur.
- **Short sentences, active voice.** Put one sentence per line in the source file.
- **Numbers carry units and honest precision.** Round to what the data supports, and
  state uncertainty once, quantified where possible, rather than hedging every
  sentence.
- **Do not "correct" domain terminology.** A readability pass normalises unfamiliar
  spellings by reflex, and scientific prose is full of terms of art that look like
  typos -- coinages such as "evaludation" in ecological modelling, species names,
  agency vocabulary. Before changing a term, check the source it is cited from and
  check whether another document in the project uses it. When a coined term is kept,
  mark the spelling as deliberate (quotes or italics) and put the citation right after
  its first use; in a heading use quotes only, since a citation there renders into the
  table of contents.
- **Use words with a technical meaning only in that meaning.** In a scientific
  report, "significant" means statistically significant, "robust" has a statistical
  sense, and "landscape" may be the literal study unit. Pick another word otherwise.
- **Paragraphs for reasoning, tables for comparisons, bullets only for genuinely
  list-like items.** A report made entirely of bullet points reads as notes.

## 5. Avoid machine-written phrasing

These patterns make text read as generated and cost the reader's trust. Remove them
on sight:

- **Stock intensifiers and filler:** "It's worth noting", "Notably", "Importantly",
  "Crucially", "Interestingly", "It is important to note that".
- **Inflated vocabulary:** delve, leverage, utilize (use "use"), facilitate,
  harness, unlock, foster, streamline, seamless, comprehensive, holistic, pivotal,
  underscore, showcase, tapestry, realm, and metaphorical "navigate" or "landscape".
- **Constructed contrast:** "not just X, but Y"; "It's not X -- it's Y"; "This isn't
  merely..., it's...".
- **Reveal colons and rhetorical questions:** "The result? ..."; "Why does this
  matter? ...".
- **Reflexive groups of three:** "clear, concise, and actionable" when one word
  would do.
- **Signposting and wrap-ups:** "In this section we will...", "Let's dive in",
  "In summary", "Overall", and a closing sentence that restates the paragraph.
- **Stacked hedges:** "may potentially", "could possibly", "it appears that it
  might".
- **Decoration:** bold scattered through sentences, headers over two-line sections,
  emoji, and em-dashes (use `--`, or better, two sentences).
- **Self-reference and pleasantries:** "I hope this helps", "As an AI", "Great
  question".
- **Punchy idioms and aphorisms.** A short dramatic sentence standing in for the
  explanation: "this is where it bites", "that is the whole point", "here is the
  thing", "the trap is X", "it is worth stating plainly". They read as insight and
  carry none. Say the mechanism instead: *"A stale pointer fails the next node sync"*,
  not *"this is where it bites"*.
- **Euphemism and folksiness.** One project states the rule directly: *"No
  euphemistic language in user-facing docs ('where the bytes land', 'baked in',
  'just works'). Say what actually happens: 'the file is written to ...'."*

This applies to everything a reader sees, not only reports: commit messages, pull
request bodies, issue comments, READMEs, and replies in the session.

The test for each sentence: would a careful human expert in this field have written
it? If a sentence could be deleted without the reader losing anything, delete it.

## 6. Revision pass

When asked to review existing reports for readability, check in this order:

1. Does the summary stand on its own for the stated audience?
2. Does each section open with its point?
3. Is implementation detail in the body that this audience does not need? Move it
   to an appendix.
4. Jargon and code identifiers: replace, define, or move.
5. Terminology: one term per concept, used consistently throughout.
6. Verbose prose: cut filler and the phrasing patterns above.
7. Figures and tables: does each earn its place, and does its caption say what it
   shows?

Report what you changed and why, per section, so the user can review the edits
rather than re-read the whole document.

## Related

- Report mechanics (Quarto project mode, rendering, DRAFT marking, ASCII backstop):
  `quarto-reports`.
- Figure design: the `dataviz` skill. Figure descriptions: `r-lib:alt-text`.
- Any citation in the text: `citation-integrity` in `r-project-core`.
