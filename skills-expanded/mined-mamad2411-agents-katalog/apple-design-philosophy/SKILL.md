---
name: apple-design-philosophy
description: "Apple's design philosophy (clarity, deference, depth, restraint, consistency, precision, human focus) applied as a strict critique discipline to BOTH interfaces and backend systems. Use this whenever you are designing, building, reviewing, or refining anything where quality of judgement matters: UI layout, typography, spacing, colour, component APIs, page structure, visual hierarchy, and equally for backend work like module boundaries, public API surface, naming, error messages, configuration options, and architecture. Trigger it when someone says a design feels generic, cluttered, busy, over-designed, unpolished, noisy, or 'off' without knowing why; when they ask what to remove, how to simplify, how to make something feel refined, premium, intentional, or high-end; when reviewing a PR or diff for taste rather than correctness; or when a feature request would add surface area and someone should ask whether it earns its place. Prefer this skill over generic styling help whenever the question is about judgement (what belongs, what goes, what matters most) rather than mechanics (how do I centre this)."
---

# Apple Design Philosophy

Design is not decoration. It is the work of deciding what matters, making that legible, and removing everything else. This skill encodes that judgement so that what gets built feels intentional and inevitable rather than generic or over-designed.

The governing sentence, which everything below serves:

> **Every element must earn its place. Complexity is absorbed, never forwarded. The result should feel like the only reasonable answer.**

This applies with equal force to a settings screen and to a service's public interface. A cluttered UI and a twelve-parameter function are the same failure: someone declined to make a decision and passed the cost to whoever comes next.

## How to use this skill

Two modes, and you should know which one you are in.

**Review mode.** Someone has built something and wants judgement. Your job is to find what does not earn its place and say so plainly, ranked by how much it costs. Lead with the single most important problem, not a list of twelve equal-weight nits. A review that lists everything communicates nothing, which is the same failure as an interface that emphasises everything.

**Build mode.** You are making something. Apply the principles as you go, and when you finish, run the checklist at the end of this file against your own work before presenting it.

In both modes: **propose at least as many removals as additions.** This is the single most reliable corrective, because the default pressure on any system is accretion. Every feature request, every review comment, every stakeholder wants to add. Almost nobody is assigned to subtract, so it has to be deliberate.

## The standard: inevitability

The goal is not "beautiful" and not "modern." It is **inevitable**: the sense that the thing could not reasonably be otherwise.

Inevitability is what makes restrained work feel confident rather than unfinished. It has a practical test:

> Can you name a specific reason for every choice that a thoughtful person would accept? Not "it looked better," but "this is the primary action, so it carries the only filled button on the screen."

Work that fails this test is either arbitrary (choices made by default or habit) or authored (choices that draw attention to the designer rather than the content). Both read as noise. When you cannot justify a choice, that is not a small gap to paper over. It is the design telling you the decision has not been made yet.

## The seven principles

Each principle below has a **test** attached. A principle without a test is a slogan, and slogans do not change what gets built.

### 1. Clarity

Meaning arrives before decoration. Text is legible at every size, symbols are unambiguous, and visual weight matches actual importance.

The subtle half of clarity is that **weight is a claim about priority**. When everything is bold, nothing is. When five elements are the same size, you have told the reader that five things matter equally, which is almost never true.

**Test:** Rank the elements by importance, honestly, with no ties in the top three. Then look at the rendering and rank them by visual weight. If the two orders disagree, the design is lying about what matters, and the fix is to reduce the over-weighted element rather than to inflate the under-weighted one.

### 2. Deference

The interface serves the content. It steps back when the content needs focus. Chrome, borders, fills, and labels are costs paid for the value they return.

Deference is not blandness. A deferential interface can be striking. It simply does not compete with the thing the user came for.

**Test:** Identify what the user came here to see or do. Now count what is louder than it. Each item on that list is either doing necessary work or it is stealing attention, and you must say which.

### 3. Depth

Layers, shadow, blur, and translucency communicate hierarchy and relationship: what sits above what, what came from where, what is temporarily on top. Depth is a language for structure.

The failure mode is depth as texture, applied evenly because it looks rich. Shadow on every card conveys nothing, because a distinction applied everywhere is not a distinction.

**Test:** For each use of elevation, blur, or translucency, state the structural fact it encodes. "This modal is above the page and the page is still there behind it" is a fact. "It looks nicer" is not, and that instance should be flat.

### 4. Restraint

Remove what is not essential. Prefer fewer, stronger elements over many weak ones. Whitespace is structure: it groups, separates, and paces, which is real work and not emptiness.

Restraint is the hardest principle to hold because every individual addition is defensible. The damage is cumulative and shows up only in aggregate, long after the person who added the fifth button has moved on.

**Test:** The Earn Test, below, run on every element.

### 5. Consistency

Once a pattern is established, it is a promise. Spacing, motion, naming, and interaction should behave the same way everywhere, so that learning the system once is enough.

Breaking a pattern is occasionally correct, and when it is, the break should be **loud and deliberate** so it reads as emphasis rather than as a mistake. A quiet inconsistency is always read as sloppiness.

**Test:** For each deviation from the established pattern, either name the reason it earns the exception, or align it. "It was built by a different person" is not a reason, it is an explanation.

### 6. Precision

Alignment, spacing, and proportion should feel deliberate, because the eye registers imprecision long before the mind can name it. A half-pixel misalignment reads as carelessness without the viewer knowing why.

Critically: **optical adjustment beats mathematical correctness.** A play triangle centred by its bounding box looks left-heavy and must be nudged right. Round shapes must overshoot their flat neighbours to look the same size. Text in a button needs less space below the cap line than the box maths suggests. Trust the eye over the number, every time they disagree.

**Test:** Squint at it, or blur it. Misalignments and uneven rhythm survive blurring, which is exactly why they register subconsciously at full sharpness.

### 7. Human focus

Design for how people behave under real conditions: distracted, on a bad connection, in bright sunlight, mid-task, anxious about the outcome. Not for the demo, the happy path, or the architecture diagram.

**Test:** Walk the unhappy paths. Empty, loading, one item, several hundred items, failed, offline, permission denied, name in a script the designer never considered. A design that only holds together with ideal data is not finished, and these states are usually the majority of real sessions.

## The Earn Test

This is the core procedure. Run it on any element, option, parameter, endpoint, or abstraction.

1. **Name its job in one sentence.** If you cannot, remove it. Things nobody can explain are things nobody decided to add.
2. **State what breaks without it.** If nothing breaks, remove it. "It would feel empty" is not a break; that is whitespace doing its job.
3. **Check whether something already does that job.** If so, merge them. Two elements sharing a purpose split the user's attention and halve the strength of both.
4. **Confirm its weight matches its rank.** If it is louder than its importance, quiet it down rather than amplifying everything around it.

Elements that survive all four have earned their place, and you should then defend them as strongly as you deleted the others. Restraint is not minimalism for its own sake. Removing something load-bearing is the same error as keeping something useless.

## Practice

The principles are general. The specifics live in reference files, so load the one you need rather than carrying both.

- **Interfaces**, covering typography, spacing systems, colour, hierarchy, depth, layout, and interface copy: read `references/frontend.md`.
- **Backend and systems**, covering module depth, public surface area, naming, parameters, errors, configuration, and architecture: read `references/backend.md`.
- **Running a review**, covering how to structure critique, how to rank findings, and worked before/after examples: read `references/critique.md`.

**Motion and gesture mechanics are out of scope here.** Springs, velocity handoff, momentum projection, interruptible animation, and rubber-banding belong to the companion `apple-design` skill, which covers them in depth. Use that skill for how motion should behave; use this one for whether the motion earns its place at all.

## What to push back on

Being strict means refusing specific things, not radiating general disapproval. Push back, with the reason, when you see:

- **Emphasis inflation.** A new element made prominent because it is new. Prominence is zero-sum: everything promoted demotes everything else.
- **Decoration standing in for hierarchy.** Gradients, glows, borders, and shadows applied to create interest rather than to encode structure. If the layout is unclear, decoration will not rescue it and usually hides the problem long enough for it to calcify.
- **Options instead of decisions.** A setting added because the team could not agree. Every option is permanent complexity for users, docs, tests, and support, paid to avoid one uncomfortable conversation.
- **Cleverness that costs the reader.** A dense one-liner, an implicit convention, an abstraction that saves the author ten lines and costs every future reader ten minutes. Clever is a warning, not a compliment.
- **Consistency broken quietly.** A one-off spacing value, a bespoke button, a route that names things differently. Either justify it loudly or align it.
- **Unearned surface area.** A config flag, an endpoint, an exported helper, or a prop added "in case someone needs it." Nobody removes these later, so they are effectively permanent from the moment they merge.
- **Solving presentation problems with features.** When the real issue is that the hierarchy is wrong, adding a filter, a tooltip, or an onboarding tour buries the problem instead of fixing it.

Say what is wrong, why it costs, and what you would do instead. Pushback without a proposed alternative is just an obstacle.

## What to avoid

Concrete anti-patterns, each a specific failure rather than a matter of taste:

- **Everything emphasised.** Multiple competing focal points, several filled buttons, three type sizes within one heading level.
- **Ornamental depth.** Shadows on every surface, blur used as texture, translucency that encodes no layering.
- **Mathematical centring that looks wrong.** Icons centred by bounding box, mixed shapes sized by number rather than by eye.
- **Filling space because it is there.** Whitespace is not a vacancy waiting for a widget.
- **Copy that describes the UI.** "Click the button below to submit your form." Say what happens, not what the interface is.
- **Novelty over convention.** A custom control for a solved problem. The user pays the learning cost, and it buys them nothing.
- **Shallow modules.** A wrapper whose interface is nearly as complicated as the thing it wraps, which adds a layer without absorbing any difficulty.
- **Boolean parameters.** `render(true)` is unreadable at the call site, which is the only place that matters.
- **Errors that state only failure.** "Invalid input" tells the reader nothing they did not already know.
- **Config as indecision.** Options whose right value the team could have determined but declined to.

## The checklist

Run this before calling anything finished. It is short on purpose, so that it actually gets run.

**Judgement**
1. Can I name a reason for every choice that a thoughtful person would accept?
2. Did I remove at least as much as I added?
3. Does anything here exist because I could not decide?

**Hierarchy**
4. Ranked by importance and by visual or structural weight, do the two orders match?
5. Is there exactly one primary focus, and is it the thing the user came for?

**Structure**
6. Does every layer, shadow, or abstraction encode a real relationship?
7. Does each module or component absorb complexity rather than forward it?

**Precision**
8. Does it survive a squint test: alignment holding, rhythm even, groups reading as groups?
9. Were optical adjustments made where maths and the eye disagree?

**Consistency**
10. Does every deviation from the established pattern have a stated reason?

**Reality**
11. Have I walked the empty, loading, overflowing, and failing states?
12. Would this still read clearly to someone tired, rushed, and unfamiliar with it?

Anything answered "no" is either a fix or a decision you should state out loud. Silently accepting a "no" is how work becomes generic.

## Where this skill defers

A project's own house rules outrank this skill. If a codebase forbids a technique this skill would otherwise reach for, or mandates a palette, voice, or component library, follow the project and say plainly where the two disagree rather than quietly overriding either.

The principles here are also not a mandate for sameness. Deference means the interface serves the content, and content differs. A tool for focused work and a page meant to persuade will correctly land in different places while following identical principles. What does not change is that every element earns its place, complexity is absorbed rather than forwarded, and the result can be explained.
