---
name: documentation-designer
description: Write clear, concise, production-grade technical documentation with high editorial quality. Use this skill when the user asks to write or restructure documentation (examples include READMEs, API references, getting-started guides, how-to guides, conceptual explanations, tutorials, runbooks, changelogs, or when editing/improving existing docs). Produces well-structured prose that covers one topic per page, front-loads what matters, and avoids bloated, generic documentation.
license: Complete terms in LICENSE.txt
---

This skill guides creation of clear, concise, production-grade technical documentation that avoids bloated, generic, hard-to-scan writing. Produce real, accurate content with exceptional attention to structure, precision, and the reader's actual task.

The user provides a documentation requirement: a page, section, set of pages, or existing docs to improve. They may include context about the product, the audience, or the surrounding doc set.

## Documentation Thinking

Before writing, identify exactly what the reader needs and commit to a single, clear purpose for the page:
- **Reader & task**: Who is reading this, and what are they trying to *do* at the moment they open it? A reader mid-task wants a different page than one trying to understand a system.
- **Page type**: Every page is one of four kinds (the Diátaxis model). Mixing them is the single most common cause of confusing docs:
    - **Tutorial** — a guided learning experience. The reader follows along and it works. Concrete steps, no decisions, no detours into theory.
    - **How-to guide** — steps to accomplish one real-world goal. Assumes competence. Lists the actions and nothing else; links out for concepts.
    - **Reference** — neutral, authoritative description of how something behaves (API, CLI flags, config keys). Looked up, not read through. Consistent and exhaustive.
    - **Explanation** — the "why" and the bigger picture. Background, trade-offs, design rationale. Read away from the keyboard.
- **Scope**: What is the *one* thing this page covers? If you can't state it in a sentence, the page is doing too much.
- **Differentiation**: What makes this page genuinely useful instead of filler? Usually: a working example, an honest caveat, or a precise answer to a question the reader actually has.

**CRITICAL**: Pick one page type and write to its conventions. Do not narrate theory inside a how-to, do not turn reference into a tutorial, and do not bury steps under an essay. Clarity comes from keeping the types separate.

Then write content that is:
- Accurate and tested (commands run, code compiles, parameters exist)
- Concise — every sentence earns its place
- Scannable — the reader can find the answer without reading top to bottom
- Cohesive with the surrounding doc set's terminology and structure

## One Topic Per Page

Each page answers one question or covers one task, concept, or reference unit. This is the foundation everything else rests on.

- **One job per page.** "Configure authentication" and "Rotate API keys" are two pages, not one. Splitting them keeps each page short, findable, and independently updatable. A reader searching for key rotation should not have to scroll past auth setup.
- **Name the page after the job.** A descriptive, front-loaded title ("Deploy to production", "Rate limits") tells the reader and the search index exactly what's inside. Avoid clever or vague titles ("Getting things rolling").
- **If a page sprawls, split it.** Two clear pages with a link between them beat one page that tries to be a manual. When you find yourself writing "but if instead you want to…", that's a second page.
- **Link, don't repeat.** Define a concept once, in the page that owns it, and link to it everywhere else. Inline the link the first time a term appears. Duplicated explanations drift out of sync.

## Page Structure

Structure every page so a reader who only reads the first screen still leaves with the key point. This is the inverted pyramid: most important information first, supporting detail below, background last.

- **Lead with the answer.** Open with what the page does and who it's for, in one or two sentences — not a history lesson or a throat-clearing preamble. The reader decides in seconds whether they're in the right place.
- **Front-load every level.** The first sentence of each section, and the first words of each sentence, carry the information. A reader scanning only the first line of each paragraph should still follow the thread.
- **Descriptive headings as a skimmable spine.** Headings should read as a meaningful outline on their own. Use them to chunk the page into units the reader can jump between; keep nesting shallow (rarely past two levels).
- **Short paragraphs, one idea each.** Group related sentences into a paragraph with a single message; break before the wall of text forms. But don't shatter everything into one-line fragments either — that forces the reader to reconstruct the connections you should have made.
- **Lists and tables for parallel information.** Steps, options, parameters, and comparisons belong in numbered lists, bullets, or tables — not buried in prose. Prose is for reasoning and connection; structure is for things the reader scans.
- **End with the exit.** Close with next steps or related links so the reader knows where to go, rather than trailing off or padding with a summary that repeats the page.

Match the internal shape to the page type:
- **Tutorial**: prerequisites → numbered steps, each with the command and its visible result → a working end state the reader can verify.
- **How-to guide**: the goal in one line → ordered steps → done. No conceptual digressions; link them out.
- **Reference**: predictable, repeating structure (signature → parameters → returns → example), identical across every entry so readers learn the shape once.
- **Explanation**: claim or question up front → reasoning, trade-offs, and context → pointers to the how-tos and references it illuminates.

## Editorial Guidelines

Focus on:
- **Concision**: Write the sentence, then cut it. Remove hedges ("it should be noted that", "in order to", "basically"), redundant qualifiers, and sentences that restate the heading. If a paragraph survives deletion without loss, delete it.
- **Plain, precise language**: Prefer the simple word and the active voice. Be exact about names, versions, and behavior — "returns `null` if the key is absent" beats "may not return anything". Use the product's real terms consistently; never introduce a synonym for variety.
- **Concrete examples**: Show, don't only tell. A focused, copy-pasteable code example that demonstrates one concept is worth a paragraph of description. Make examples real and runnable, and isolate a single idea per snippet.
- **Honest caveats**: State limits, gotchas, and failure modes plainly where the reader will hit them. Trustworthy docs say what doesn't work, not just what does.
- **Direct address**: Speak to the reader as "you" and tell them what to do ("Run `npm install`"), not what one might do. Imperative mood for instructions.
- **Visual aids with intent**: Use a diagram for spatial or structural relationships, a table for comparisons, an admonition (note/warning) for genuine exceptions — each only where it carries information words can't carry as well.

NEVER ship bloated, generic documentation: marketing fluff and adjectives ("powerful", "seamless", "robust", "simply", "easy") that tell the reader nothing; preambles that restate the title before getting to the point; walls of undifferentiated prose with no headings or lists; conceptual essays wedged into step-by-step guides; vague instructions ("configure the settings appropriately") with no concrete values; duplicated explanations that will rot out of sync; and summaries that merely repeat the page. Calling something "easy" when the reader is stuck on it erodes trust faster than almost anything else.

Write what the reader needs and stop. The best documentation respects the reader's time: it gets them to the answer, gives them a working example, names the caveats, and points them onward. Length is not thoroughness — precision is.

**IMPORTANT**: Match depth to the page type and the reader's task. A quickstart needs ruthless brevity and a single happy path; a reference needs exhaustive, consistent coverage of every parameter; an explanation can take the room to reason but must stay focused on one idea. Completeness for reference, restraint for everything else.

## Implementation

Write documentation as Markdown files unless the user specifies another format. Use fenced code blocks with language hints, relative links between pages, and a consistent heading hierarchy. When improving existing docs, match the established voice, terminology, and structure rather than imposing a new one. Verify every command, code sample, and parameter against the actual product before publishing.