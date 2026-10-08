---
name: explainer-infographic
description: "Generate an animated, interactive HTML page that explains a complex concept through real-world analogies, visual diagrams, and progressive disclosure. Use this whenever the user says 'explainer infographic,' 'explain how X works,' 'make an explainer for,' 'visualize this concept,' 'turn this into a visual,' 'help me understand X visually,' or asks to break down a topic in a bite-sized visual format. Output is a single self-contained HTML file the user can open in a browser, scroll through, or share as a link. Topics can be anything — finance concepts, technical systems, scientific processes, business frameworks."
---

# Explainer Infographic

You build a single-file HTML page that explains a concept the way a great visual explainer (Bartosz Ciechanowski, The Pudding, distill.pub) would: through scrolling, interactive diagrams, real-world analogies, and progressive depth. The output should make a complex topic click for a smart non-expert in under 5 minutes.

## Before you start

Get the essentials:

1. **The concept** — what are you explaining?
2. **The audience** — who's reading? (Smart non-expert is the default)
3. **The "why now"** — is this for a meeting, a class, a video, a blog post, personal learning?
4. **Depth** — quick intuition (one screen) or deeper exploration (long scroll)?

If unspecified, default to: smart non-expert, deep enough to scroll through for 3-5 minutes, no specific use case.

## Structure

Most concepts can be explained in 5 beats. Build the page in this order:

### 1. The hook (one screen)

Open with the question or surprising fact that makes the concept worth understanding. Not "What is X" — something like "Why do bridges built over water start with empty boxes?" or "Why does a 30-year mortgage cost more than 2x the price of the house?"

### 2. The analogy

Tie the unfamiliar concept to something the reader already knows. The analogy should be carried through the rest of the page, not dropped after the intro. Examples:

- LLMs as "predictive text on steroids"
- Cash flow as "water through pipes"
- DNS as "the internet's phone book"

Pick one strong analogy and commit to it. Mixing analogies confuses the reader.

### 3. The mechanism (3-7 sections)

Walk through how the thing actually works, in order. For each section:

- A clear heading
- A short paragraph
- A visual — diagram, animation, or interactive element
- (Optional) a "click to dig deeper" reveal for the curious

This is the meat of the page. The visuals are what make it different from a blog post.

### 4. Common misconceptions

A short section addressing the things people get wrong about this topic. Format as "Myth: X / Reality: Y" pairs.

### 5. The takeaway

One paragraph that ties it all back to the hook from section 1. Leave the reader with one sentence they could repeat at a dinner party.

## Visual style

- **Off-white or warm-white background** — easier on the eyes than pure white for long-form reading
- **Generous typography** — body text 18-20px, line-height 1.6+, max width 65ch
- **One accent color** — used for highlights, links, and the key element in each diagram
- **Diagrams in SVG** — sharp at any zoom, themeable via CSS
- **Animation purposeful, not decorative** — animate things to show change over time (a process unfolding, a value growing, a system reacting). Don't animate just because you can.
- **Scroll-driven where it helps** — for sequences and processes, use scroll-triggered animations so the reader controls pace. For static diagrams, skip the scroll trigger.

## Interactive elements (use 2-3 per page max)

- **Slider/range input** — adjust a parameter and see the effect
- **Toggle** — switch between two states (with/without, before/after)
- **Reveal-on-click** — extra detail for curious readers
- **Step-through animation** — "Next" button to walk through a process at the reader's pace

Don't overdo it. Three well-designed interactive moments beat ten gimmicks.

## Technical implementation

Single self-contained `.html` file saved as `explainer-[topic-slug].html`. No external dependencies — embed any fonts, write SVGs inline, vanilla JS only.

Required:

- Mobile-friendly — most readers will scroll on a phone
- Accessible — semantic HTML, alt text on diagrams, keyboard-navigable interactives
- Fast — should open instantly, no spinner, no asset loading delay

## Content rules

1. **Lead with the analogy, not the definition.** "A neural network is a function approximator" is correct and useless. "A neural network is like a stack of dimmer switches that learn to turn themselves up or down" is useful.
2. **Use real numbers.** "Most mortgages last 30 years" is generic. "A $500K mortgage at 7% costs $1.2M over 30 years — $700K of that is interest" is sticky.
3. **Show, don't tell.** If you find yourself writing "imagine if..." consider whether you can just show it with a diagram instead.
4. **Don't be cute.** Wit is fine; trying-too-hard humor distracts from the explanation. The goal is clarity, not entertainment.
5. **End with a question or implication.** A great explainer leaves the reader thinking, not just informed.

## Why this is built this way

Long-form text explainers are easy to skim and forget. Slides are too compressed for nuance. A scrolling, visual page sits in the right middle: long enough to be substantial, visual enough to be memorable, interactive enough to invite engagement. Done well, this is the format that makes readers screenshot and share.

## After generating

Tell the user:

1. The file path
2. How to open it
3. One specific thing they could ask for to improve it (you're not done — first drafts of explainers usually need one round of "the X section feels weak")
4. How to share — the file is self-contained, so they can email it, drop it in Slack, host it anywhere
