---
name: artifact-explainer
description: OUTPUT IS ALWAYS A `.html` FILE (never `.md`, never plain markdown) with real jQuery UI interactivity. Use this skill whenever the user asks for an explainer, primer, "how does X work", "explain Y", "TL;DR for Z", concept overview, feature explainer, deep dive, research summary, architecture writeup, or any pedagogical artifact that should be delivered as a polished interactive HTML document with collapsible sections, tabbed code samples, an inline glossary, and a scannable summary block at the top. Pair with `artifact-css` for the underlying design system and `jQuery 4.0.0 + jQuery UI 1.14.2` for the interactivity (accordion, tabs, tooltip widgets). Do NOT use for one-paragraph definitional answers — only when an HTML artifact with progressive disclosure is the deliverable.
---

# artifact-explainer

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file. Not markdown. Not `.md`. Not plain text.**
>
> Explainers are interactive HTML artifacts. Collapsibles, tabs, and tooltips render as real jQuery UI widgets — NEVER as markdown `<details>` placeholders or markdown headings pretending to be sections. The file extension is `.html`, always.
>
> Use the template in `templates/`. Inline `artifact.css` inside `<style>` (Mode B — single-file portable) or `<link>` to it. Always load the jQuery 4.0.0 + jQuery UI 1.14.2 layer per `artifact-css/SKILL.md`.

---

Pedagogical HTML artifacts. The reader arrives knowing nothing; they leave with enough mental model to make a decision, search effectively, or argue back with conviction. This is the artifact archetype where progressive disclosure matters most — a flat page of paragraphs is the wrong shape.

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, the design system, the page skeleton, and the **Interactivity layer** section that documents the jQuery + jQuery UI loader pattern. Explainer artifacts always opt-in to that layer.

## When to reach for this skill

- User asks "how does X work" with X being non-trivial (event sourcing, vector embeddings, a particular library, an internal service).
- User asks for a primer, deep-dive, or onboarding doc.
- User asks for a feature explainer that needs to handle "I want the headline" and "I want the wire format" readers simultaneously.
- User wants a research-summary artifact (related work, prior art, current consensus).

Static reports, plans, and reviews do NOT use this skill. They're flat by design.

## What this skill adds on top of artifact-css

Three jQuery UI widgets, configured to integrate cleanly with the library's visual language:

| Widget | Purpose | Element | Init |
|---|---|---|---|
| `accordion` | Collapsible body sections. One open at a time. | `<div class="explainer-accordion">` | `$('.explainer-accordion').accordion({ heightStyle: 'content', collapsible: true })` |
| `tabs` | Switching between code samples or representations of the same idea. | `<div class="explainer-tabs">` | `$('.explainer-tabs').tabs()` |
| `tooltip` | Glossary definitions on hover for highlighted terms. | `<span class="glossary" title="...">` | `$('.glossary').tooltip({ classes: { 'ui-tooltip': 'explainer-tip' } })` |

The CSS for these widgets is overridden in `artifact-explainer/artifact.css` so they inherit library tokens (clay accent, ivory background, 1.5px borders, serif headings).

## Anatomy of an explainer

Built from seven blocks. Use this order.

1. **Header.** Eyebrow with topic + audience (`Concept · for backend engineers`). h1 with the topic name. `.lead` paragraph: one sentence answering "what is this for the reader who quits after the lead". The lead must stand alone.
2. **TL;DR.** A `.callout` (oat) with three to five bullets. Each bullet is a complete claim — not a teaser. A reader who reads only the TL;DR and the lead should be able to give a 90-second whiteboard explanation. If they can't, the TL;DR is failing.
3. **Mental model.** A single `.panel` with a short prose paragraph and an inline SVG diagram or a structured analogy. This is the "imagine X is like Y" block. One analogy max. Don't list three competing analogies — pick the one that gets the reader furthest.
4. **Progressive sections (accordion).** Three to six collapsible sections, default to the first one open. Each section is one concept the reader needs. Order them from "what" → "why" → "how" → "when not to use it" → "what's commonly misunderstood". Each section's body can include code blocks, sub-headings, small tables, and `.glossary` terms.
5. **Code samples (tabs).** A `.tabs` widget switching between languages or representations. Common tab sets: `JS / Python / curl`, `Before / After`, `Naive / Optimized`, `Wire format / SDK / CLI`. Three tabs max — beyond that, switch to an accordion.
6. **Glossary.** A `<dl>` (definition list) of the bolded terms used above. Sort alphabetically. This is also what the `.glossary` tooltips reference for their `title` attribute — keep them in sync.
7. **Further reading.** A short list of links with one-line summaries explaining why each is worth the reader's time. Three to five links. No "here are 27 papers" dump — curation is the value.

## The accordion vs tabs vs flat decision

Most pages over-use accordions. Rule of thumb:

| If the reader needs… | Use… |
|---|---|
| Optional depth on independent sub-topics | Accordion |
| The same idea in two or three forms | Tabs |
| Step-by-step linear narrative | Neither — flat prose |
| Quick reference | A `.table` |

A page with three accordions and two tab strips is doing too much. Pick one as primary; relegate the others.

## Glossary tooltips — semantic markup

Glossary terms inline in the body get this shape:

```html
The system uses <span class="glossary" title="A function f such that f(x,y) = f(y,x); order of arguments doesn't change result.">commutative</span> merge semantics.
```

Two contracts:

- The `title` attribute carries the canonical short definition. jQuery UI's tooltip widget reads it. If JS fails to load, the browser's native tooltip still works.
- The same canonical definition appears in the glossary `<dl>` block at the bottom. Keep them character-for-character identical. The skill includes a small lint check (see `LINTING` below).

## Fallback contract (no-JS)

The page MUST be readable with JS disabled:

- Accordion HTML uses `<h3>` headers and `<div>` panels with `aria-hidden="false"` defaults. With no JS, all sections render expanded. Reader still gets the full content, just longer page.
- Tabs HTML uses `<ul>` of links to `#id` targets. With no JS, all panels render stacked, each preceded by its tab label as a heading.
- Tooltips fall back to native browser tooltip via the `title` attribute.

Never inject critical content via JS. JS only rewires existing markup.

## Page skeleton (explainer-specific)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{TOPIC}} — explainer</title>

  <!-- Library -->
  <link rel="stylesheet" href="../artifact.css">

  <!-- jQuery UI base theme -->
  <link rel="stylesheet"
        href="https://code.jquery.com/ui/1.14.2/themes/base/jquery-ui.min.css"
        integrity="sha384-pUvA/6DQjteMxpaV6uGxZ1QuYrFLJgrLMvBWf06VcJIg6ky/Y5m3UZJlrv11V1I+"
        crossorigin="anonymous">
</head>
<body>
  <div class="page page-narrow">
    <!-- ...content... -->
  </div>

  <!-- jQuery 4.0.0 + jQuery UI 1.14.2 -->
  <script src="https://code.jquery.com/jquery-4.0.0.min.js"
          integrity="sha384-fgGyf7Mo7DURSOMnOy7ed+dkq5Job205Gnzu6QIg0BOHKaqt4D76Dt8VlDCzcMHV"
          crossorigin="anonymous"></script>
  <script src="https://code.jquery.com/ui/1.14.2/jquery-ui.min.js"
          integrity="sha384-tBcEcHGtNy7/Mx08+YxuvQ6v6s0N2jgehtFiT+bLtGwTj/txXtB/L5GqXfggm5sS"
          crossorigin="anonymous"></script>

  <script>
    $(function () {
      $('.explainer-accordion').accordion({ heightStyle: 'content', collapsible: true });
      $('.explainer-tabs').tabs();
      $('.glossary').tooltip({
        classes: { 'ui-tooltip': 'explainer-tip' },
        position: { my: 'left top+8', at: 'left bottom' }
      });
    });
  </script>
</body>
</html>
```

Use `.page-narrow` (680px) — explainers are prose-heavy and benefit from a tighter measure.

## Voice and density rules

1. **Lead with what it is, not what it isn't.** "Event sourcing stores state as an append-only log of changes" beats "Event sourcing is not about CRUD".
2. **One analogy, not three.** The analogy is a scaffold to throw away once the reader has the real model. Pick the one that gets them furthest.
3. **Code samples must run.** Even in tabs. If a snippet won't compile or execute as shown, the reader will catch you and lose trust.
4. **Define terms exactly once.** First use in body → `.glossary` span. After that, just use the term. Don't re-define.
5. **TL;DR has facts, not promises.** "Stores state as immutable events" beats "lets you reason about state over time" — the latter is marketing.
6. **Cut the history.** "Originally introduced by Greg Young in 2010" is rarely the reader's job-to-be-done. Save it for "further reading".

## Common mistakes

- **TL;DR longer than the mental-model block.** Means the explainer fits in the TL;DR. Cut everything else.
- **Accordion sections that are one paragraph each.** Either merge to flat prose or expand the sections. Tiny accordions feel like padding.
- **Tabs comparing things that aren't variants of the same idea.** "Tab 1: how it works. Tab 2: history. Tab 3: alternatives." That's three different sections, not three tabs.
- **Glossary with five terms and a body that uses twelve.** Audit before shipping.
- **No "what's commonly misunderstood" section.** Often the most useful section for a reader who has half-heard the term before.

## Linting (skill-local)

Before shipping an explainer, run mentally:

1. Every `<span class="glossary" title="...">` has a matching `<dt>` in the glossary `<dl>` with identical definition text.
2. Every glossary `<dt>` has at least one `<span class="glossary">` reference in the body (no orphan terms).
3. The TL;DR has at least three and at most five bullets.
4. The accordion has at least three and at most six sections.
5. The tabs widget has at most three tabs.
6. The page-narrow class is on `.page`.

## After the artifact

Offer two derivatives:

1. A 4-bullet plain-text TL;DR for Slack.
2. A flashcard-style Q&A list for the user to drop into Anki / a study tool.
