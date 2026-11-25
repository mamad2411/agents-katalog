---
name: tech-writing-copyedit
license: CC-BY-4.0
description: >-
  Apply the house technical-writing style when writing or copyediting
  documentation, READMEs, how-to guides, runbooks, and docs-site pages. Use
  when asked to copyedit, proofread, tidy, or "make this read better", when
  drafting user-facing docs, or when a reviewer asks which person, mood,
  punctuation, spelling, or heading case to use (en-AU, spaced en dash,
  imperative instructions, purpose before action, no e.g. or i.e.).
argument-hint: "Paste or point at the prose to copyedit, or say what you are about to write (for example 'README install section')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
  origin: https://pve.proxmox.com/wiki/Technical_Writing_Style_Guide
  origin-reviewed: 2026-08-27
---

# Tech writing – copyedit to house style

These are the *decisions* a fresh writer makes inconsistently, not a grammar
lesson – your default grammar is fine. Long form, tables, and examples live in
`references/house-style.rst`.

## Mandatory STE review

Before delivering documentation, apply the simplified STE profile in
`references/ste-review.rst` and correct its findings on every host. In Claude
Code, the plugin’s completion hook also reviews the deliverable and blocks
completion on findings. Codex does not run that completion hook; apply the
review directly before delivery.
The profile takes precedence over the general house rules for sentence
limits, contractions, and semicolons. It does not change project spelling or
normative requirements. Blog posts and status-only replies are outside scope.

ASD-STE100 includes both writing rules and a controlled dictionary. This
profile is a practical subset, not a full compliance check. For a full
compliance request, obtain the official standard and verify vocabulary,
meaning, word forms, and technical terminology against it. Do not label the
subset check as ASD-STE100 compliance.

- [ASD-STE100](https://www.asd-ste100.org/)
- [How STE works](https://www.asd-ste100.org/about_STE.html)
- [Official copy](https://www.asd-ste100.org/STE_downloads.html)

## Stylepedia topic index

At the start of a writing or copyedit task, scan this index for relevant
content and read the matching sections before drafting. Skip unrelated
sections. If the site is unavailable, use the house rules and report any
unverified guidance rather than inventing it.

[Stylepedia](https://stylepedia.net/style/) hosts Red Hat’s technical writing
guide. This compact index routes into its
[writing-style ToC](https://stylepedia.net/style/#part-Writing_Style_Guide);
it supplements the house rules rather than overriding them. Preserve the
project’s locale, normative modals, and the “We recommend …” exception.

| Content to check | Source section |
|---|---|
| Audience and purpose | [Objectives](https://stylepedia.net/style/#objectives) |
| Grammar, punctuation, and hyphens | [Grammar](https://stylepedia.net/style/#grammar) |
| Headings, interface labels, commands, and notices | [Document design](https://stylepedia.net/style/#design) |
| Ambiguity, inclusive wording, dates, and numbers | [Language choices](https://stylepedia.net/style/#appropriate-language) |
| Lists, markup, and code examples | [Clear writing](https://stylepedia.net/style/#writing_clearly_and_succinctly) |
| Links and repeated information | [Cross-references](https://stylepedia.net/style/#using-xrefs) |
| Further authorities | [Resources](https://stylepedia.net/style/#resources) |
| Individual technical terms | [Usage dictionary](https://stylepedia.net/style/#part-Usage_Dictionary) |

## Locale: en-AU, spaced en dash, sentence-case headings

- Spell in **Australian English** (organise, colour, catalogue, *licence* noun
  / *license* verb; *program* in every sense). If a project already spells
  consistently in another locale, keep it – never flip a locale in a copyedit.
- Set off a parenthetical with a **spaced en dash** ( – ), never an em dash
  (—). Ranges take an unspaced en dash (10–20 ms) and **never** "from 10–20"
  or "between 2024–2026" – with *from* or *between*, write *to* or *and*.
- **Sentence case for every heading**, H1 included; capitalise proper nouns
  and the first word after a colon. This deviates from the Proxmox origin
  (title case for H1–H2) to match the Style Manual and Microsoft.
- Dates in prose: 27 August 2026. Numeric dates for people: 27/8/2026.
  ISO 8601 only in data and filenames.

## Person and mood follow the content type

| Content | Person and mood | Never |
|---|---|---|
| Description – what a thing is or does | Third-person indicative: "The scheduler retries failed jobs." | "one", "I" |
| Instruction – what the reader does | Second-person imperative, present tense: "Insert the card." | incidental modal verbs (*should*, *could*, *might*), "I", "we" |
| Recommendation | "We recommend …" is the one permitted "we" | – |

Prefer "To create a container, run …" over "You can create a container by …".
Blog posts and personal write-ups use first person. In documentation,
"We recommend …" is the only first-person exception.

Remove incidental modals in procedural instructions, such as "You should
click **Save**". Preserve normative *must*, *may*, and *should* when they
express a requirement, permission, or recommendation in contracts, policies,
ADRs, requirements, or safety notes. Never strengthen or weaken that meaning.

## Front-load what the reader needs

- **Instructions: purpose, then action**, so the reader can skip a step whose
  purpose does not apply: "To delete the entire document, click **Delete**."
  Not "Click Delete if you want to delete the entire document."
- **Descriptions: subject first**, purpose after: "Proxmox VE offers a RESTful
  API to integrate with third-party tools." Not "To integrate with …, Proxmox
  VE offers …".

## Procedures and lists

- A procedure gets a gerund heading ("Closing the program") and an intro
  sentence that adds context without repeating the heading.
- Use one meaningful action per step and parallel imperative structure
  across steps.
- Use bullets for options and numbers for actions that must happen in order.
- **A single-step procedure is a bullet, not "1."**
- In formats supporting alphabetic enumerators, sub-steps are `a.`, `b.`
  and sub-sub-steps are `i.`, `ii.`. In Markdown, use indented decimal
  numbering at every level so nested lists render correctly.
- **"Press Enter" belongs inside the step it completes**, never as its own step.
- Average 15–20 words a sentence; three or more items inline become a list.
- One style per list: **all** full sentences ending in a full stop, or **all**
  fragments with no end punctuation. Never mix.
- Term-and-definition items bold the term; link-and-description items put the
  link first and indent the description beneath.

## Punctuation and word decisions

- Oxford comma in lists of three or more.
- In documentation, split related independent clauses into separate
  sentences; the STE profile excludes semicolons. Never use a comma splice.
- A slash means a combination (TCP/IP, client/server). **Never use a slash for
  "or"** – write "product or service".
- Hyphenate compound modifiers before a noun: *read-only access*,
  *well-defined behaviour*, *5-point scale*, *command-line tool* (but
  *the command line*). Write *e-book* and *e-commerce*, but *email*.
- Expand contractions in documentation under the STE profile. Preserve
  possessives and quoted text; do not expand a possessive as a contraction.
- No *approx.* (write "about"), no *etc.*, no *e.g.* or *i.e.* – write
  "for example" and "that is". If a template forces them, it is "e.g.," and
  "i.e.," with the comma.
- **Do not introduce an acronym you use only once.** Otherwise spell it out on
  first use with the acronym in brackets – "Kernel Samepage Merging (KSM)".
  USB, HTML, URL, API, CPU, SSH need no expansion.
- Singular *they*; *data* is singular.

## Terminology

- One term per concept for the whole document. On first use, add the synonyms
  readers search for, in brackets: "a USB flash drive (USB stick)".
- Keep an *Instead of → Use* terms table in the project's docs and extend it
  when you settle a choice (starter table in the reference).
- **The brand is not the product.** "Proxmox 3.4" names nothing – write
  "Proxmox VE 3.4". Use the vendor's casing (CentOS, VMware, macOS).
- An example is correct and tested, or it is not there.

## Copyedit pass

1. Name the content type (description, instruction, recommendation) and set
   person and mood accordingly.
2. Fix front-loading, incidental procedural modals, and first person;
   preserve normative modals and the "We recommend …" exception.
3. Fix procedures and lists (one meaningful action per step, parallel
   structure, bullets for options, numbers for order, single-step bullet,
   Enter inside the step, consistent list punctuation).
4. Fix words: abbreviations, acronyms, one term per concept, en-AU spelling.
5. Fix punctuation: Oxford comma, semicolon, slash, compound-modifier hyphen,
   spaced en dash; heading case.
6. Apply the mandatory STE review before delivery. Report each change as *before → after* with the rule that drove it.

Do not change meaning, code, commands, file paths, UI labels, or quoted
program output. Leave a project's existing locale alone.

Worked example: "You should click Save to save the file, e.g. before exiting"
→ "To save the file before exiting, click **Save**." (purpose first, no modal,
no *e.g.*).

## Verify against the canonical sources

Where this file is silent and being wrong would mislead, read the source
instead of guessing. Where this file *conflicts* with a source – en-AU
spelling, the spaced en dash, sentence-case headings – this file wins.

- Australian Government Style Manual – spelling, punctuation, dashes, dates:
  https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/punctuation/dashes
  and https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/spelling
- Microsoft Writing Style Guide – the Proxmox guide's own primary source:
  https://learn.microsoft.com/en-us/style-guide/welcome/ ; A–Z word list
  entry for *command-line*:
  https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/c/command-line
- Google developer documentation style guide – procedures:
  https://developers.google.com/style/procedures
- Origin: https://pve.proxmox.com/wiki/Technical_Writing_Style_Guide (a wiki
  page in flux; take the decisions, not the prose)
