---
name: claude-presentation-prompts
description: Six sequenced Claude prompts that build an entire presentation end-to-end — outline/structure (Presentation Architect), per-slide copy (Slide Content Writer), turning raw content into a visual-first slide (Visual Storyteller), an opening hook (Hook Generator), speaker notes plus anticipated Q&A (Speaker Notes Coach), and a single-prompt full-deck generator (Complete Deck Creator) — plus the order to run them in. Use when the user needs to build a pitch deck, client presentation, training deck, or any slide-based presentation with Claude, whether exported to PowerPoint/Canva/Google Slides/Claude Artifacts.
---

# Six Claude Prompts That Build Entire Presentations

Original content compiled from a "6 Claude Prompts That Create Entire
Presentations For You" social carousel. Each prompt is reproduced as-is,
including its own "why this works" rationale.

## 1 — The Presentation Architect (start here for a new deck)

> Act as an expert presentation strategist. Create a [NUMBER]-slide
> presentation about [TOPIC] for [AUDIENCE].
>
> First, determine the main objective and the story the presentation should
> tell. Then provide each slide with:
> - A compelling title
> - One clear key message
> - 2-3 supporting points
> - A recommended visual
> - A smooth transition to the next slide
>
> Keep the flow logical, engaging, and persuasive. Avoid unnecessary
> information and repetition.

Why this works: gives Claude a framework for building the presentation
instead of generating disconnected slides.

## 2 — The Slide Content Writer (once you have a slide title)

> Act as a professional presentation copywriter. Write the content for a
> slide titled [SLIDE TITLE] in my presentation about [TOPIC].
>
> Include:
> - A strong, attention-grabbing headline
> - 3-4 concise bullet points, maximum 8 words each
> - One memorable key takeaway
> - A short, conversational speaker note
>
> Make the content easy to scan and understand. Avoid paragraphs, jargon,
> repetition, and unnecessary words.

Why this works: prevents the classic "wall of text" slide.

## 3 — The Visual Storyteller (turn dense content into a real slide)

> Here is the content for my slide: [PASTE CONTENT]
> Transform it into a clean, presentation-ready slide. Simplify the wording
> while preserving the important information.
>
> For each major point, recommend the best visual — such as a chart, icon,
> diagram, timeline, infographic, or image. Then explain:
> - What should appear on the slide
> - What should be explained verbally
> - How the visual improves understanding
>
> Keep the final slide simple, professional, and visually engaging.

Why this works: turns information-heavy slides into visual stories instead
of just shrinking text to fit.

## 4 — The Hook Generator (the first 30 seconds)

> Act as a presentation storytelling expert. Help me create a powerful
> opening for a presentation about [TOPIC] for [AUDIENCE].
>
> Give me 4 opening options:
> 1. A surprising statistic or fact
> 2. A thought-provoking question
> 3. A short relatable story
> 4. A bold or unexpected statement
>
> Keep each option suitable for the first 30 seconds. Then create a natural
> one-sentence transition from the hook into my main presentation.

Why this works: a strong opening creates curiosity immediately and gives
several ways to connect with a specific audience.

## 5 — The Speaker Notes Coach (prep for delivery + Q&A)

> Act as my presentation coach. Create concise, conversational speaker notes
> for the following presentation on [TOPIC]: [PASTE OUTLINE]
>
> For each slide, provide:
> - 2-4 key talking points
> - What I should emphasize
> - A natural transition to the next slide
>
> Then identify the 5 toughest questions my audience may ask and provide
> clear, honest, confident answers.
>
> Keep the notes natural and conversational — not something I have to
> memorize word-for-word.

Why this works: prepares for both the presentation and the Q&A while
keeping delivery natural rather than robotic.

## 6 — The Complete Deck Creator (one prompt, full deck)

> Act as an expert presentation strategist, designer, and storyteller.
> Before creating my presentation, ask me 10 essential questions about my
> audience, objective, topic, presentation length, tone, branding, experience
> level, key message, desired outcome, and call-to-action.
>
> After I answer, create a complete [NUMBER]-slide presentation including:
> - Slide titles and content
> - Key takeaway for each slide
> - Visual recommendations
> - Speaker notes
> - Audience engagement moments
> - Strong conclusion
> - Clear call-to-action
>
> Keep the presentation cohesive, professional, and easy to transfer into
> PowerPoint, Canva, Google Slides, or Claude Artifacts.

Why this works: instead of guessing what's needed, Claude first gathers the
right context and then builds the presentation around the specific audience
and goal.

## Recommended order

Use these in sequence for a professional-grade build:

1. Presentation Architect → 2. Hook Generator → 3. Slide Content Writer →
4. Visual Storyteller → 5. Speaker Notes & Q&A Coach → 6. Complete Deck
Creator

This mirrors the workflow professional presentation designers use when
building high-impact presentations. For a lighter task, prompt 6 alone
(Complete Deck Creator) can substitute for the whole sequence — it asks its
own clarifying questions up front.

This repo's own `premium-html-presentation` / `ai-canva-presentations`
skills are the better fit once you're ready to actually *render* the deck
(cinematic HTML slides, or a live Canva build) — use the prompts here for
structuring and drafting content first, then hand off to those for the
visual build.
