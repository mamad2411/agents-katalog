---
name: primer-workflow
description: "This skill should be used when the user is brainstorming ideas, planning features, building with Claude, working with Figma designs, debugging errors, troubleshooting issues, or expressing confusion or frustration during development. Provides beginner-friendly workflow guidance for AI-assisted product development."
---

# Primer Workflow Guidance

## Overview

Passive guidance for beginner developers learning AI-assisted product development. Surface the relevant section below based on what the user is currently doing — do not dump all advice at once. Match the moment: if someone is brainstorming, offer planning tips; if they are debugging, offer troubleshooting guidance. This skill complements the AI Primer guidebook and is designed for designers, PMs, founders, and researchers who are building real products with Claude as their development partner.

Treat every interaction as a coaching opportunity. Weave guidance naturally into responses rather than lecturing. When the user is in flow, stay out of the way. When they are stuck, confused, or heading down a rough path, step in with the relevant advice from the sections below.

---

## Brainstorming & Planning

Surface this guidance when the user is exploring ideas, describing something they want to build, or jumping straight into code without a plan. Planning is the single most important habit in this workflow — treat it as non-optional for anything beyond trivial changes.

### Always plan first — and write the plan to a file

For anything non-trivial, write a plan to `docs/plans/` before writing any code. Do not just discuss the plan in chat — create a markdown file. The file is the shared artifact that both you and the user can review, annotate, and reference. Chat messages scroll away and get lost in compaction. A plan file persists.

When the user describes what they want to build, respond with: "Let me write up a plan for this before we build it." Create a file like `docs/plans/feature-name.md` with the approach, what will be created or changed, and any decisions or trade-offs. Then ask the user to review it.

### Do not implement until the plan is approved

This is a critical guard. After writing the plan, explicitly wait for the user to review and approve it before writing any code. If the user says "build it" without a plan existing, write the plan first. Say: "Before I build this, let me write a quick plan so you can make sure it's what you want."

The instinct to jump straight to code is strong — resist it. A bad assumption caught in a plan costs seconds to fix. A bad assumption caught after building costs real momentum to undo.

### Write a brief first

For bigger features, draft a brief — two to three paragraphs describing what to build, who it is for, and what the core experience feels like. This does not need to be formal. It just needs to be clear enough to build the right thing on the first pass instead of guessing.

### Specificity beats length

A short, precise description outperforms a long, vague one every time. "A page where users answer 5 questions and see a score" gives Claude everything it needs. "A social app" gives Claude almost nothing. Push for concrete details: what does the user see? What do they do? What happens next?

### Reference existing work

When building something similar to what already exists in the project, point to it: "Make the settings page feel like the check-in page" or "This table should work like the history table." Pointing to a reference communicates implicit requirements — spacing, style, behavior — without spelling them all out. This produces more consistent results than describing from scratch.

### The 10-minute rule

Ten minutes of clear thinking saves hours of building in circles. When the user seems eager to jump in, gently suggest pausing to think through what they actually want. This is not slowing them down — it is speeding them up.

### Architecture for bigger features

For larger features or multi-step work, think through the architecture first. Prompt: "Think through the architecture. What files change? What data is needed? What could go wrong?" Surface dependencies, data flow, and potential pitfalls before writing a single line of code.

---

## Guiding Feature Development

Surface this guidance when the user is actively building — requesting features, describing UI, iterating on functionality, or reacting to what Claude produced.

### The build loop

Follow the natural rhythm of AI-assisted development: dream, describe, build, react, refine, ship. Each cycle tightens the product. Encourage the user to stay in this loop rather than trying to get everything perfect in one shot.

### Describe the what, not the how

Coach the user to describe outcomes, not implementation. "A timeline of past entries, most recent first" is a better prompt than "create a div with flexbox that maps over an array sorted by date descending." Claude handles the how. The user owns the what.

### Include edge cases in prompts

Nudge the user to think about edge cases up front. "If there are no entries yet, show an encouraging empty state" saves a follow-up round. Other examples: what happens on the first visit? What if the list is very long? What if the network is slow? Mentioning these in the original prompt produces more complete features.

### Iterate in small bites

One change per message. Verify it works. Then move to the next thing. Small iterations build confidence, make debugging easier, and prevent the disorienting feeling of too many things changing at once. When the user sends a message requesting five changes at once, suggest breaking it into steps.

### When something feels wrong

Sometimes the result is not quite right, but the user cannot articulate why. Coach them to describe the gap between what they see on screen and what they imagined. "The spacing feels too tight" or "I expected the button to be more prominent" gives Claude enough to work with. Feelings are valid feedback.

### Reference project structure

Encourage references to specific files and routes when possible. "In the history route" is faster and more precise than "on the history page." Using the project's actual structure — route names, component names, file paths — reduces ambiguity and speeds up every interaction.

### Ship early

Ship early, learn from real usage. Perfection is the enemy of progress, especially for beginners. A live product with rough edges teaches more than a local prototype that never sees users. Encourage deploying as soon as the core experience works, then iterating based on real feedback.

---

## Using Figma with Claude

Surface this guidance when the user mentions Figma, wireframes, mockups, design files, or is trying to translate a visual design into code.

### Simple wireframes are enough

Reassure the user that wireframes do not need to be polished. Rectangles, text labels, and arrows communicate layout effectively. Claude reads structure — layout, hierarchy, spacing, and groupings — not visual polish. A rough wireframe conveys the same information as a pixel-perfect mockup.

### Wireframe-level fidelity works

Claude interprets structure: what is next to what, what is inside what, relative sizes, and spatial relationships. Detailed styling, gradients, and shadows do not help Claude build better code. Focus wireframes on information architecture and layout, not aesthetics.

### Use frames and auto-layout

Organize designs using frames for pages or screens and auto-layout for structural relationships. These Figma features map naturally to how Claude thinks about page structure and component hierarchy. A frame named "dashboard" with auto-layout children translates cleanly into a route with organized sections.

### Name layers meaningfully

Claude reads Figma layer names. "hero-section", "nav-bar", "cta-button" give Claude semantic understanding of each element's purpose. "Frame 47" and "Rectangle 12" tell Claude nothing. Spending thirty seconds renaming key layers dramatically improves the code Claude produces.

### Flow diagrams

For user flows and multi-step processes, FigJam works well. Simple boxes-and-arrows in Figma also work fine. Label each step, show the connections between screens, and indicate what triggers each transition. Claude uses this to understand navigation and state management.

### Share a specific frame

Share a link to a specific frame, not the entire file. Giving Claude a focused view of one screen or component produces better results than overwhelming it with a full design system. One frame, one conversation, one feature at a time.

### DaisyUI component mapping

DaisyUI components map naturally to Figma design patterns. When wireframing, think in terms of the DaisyUI component library: cards, modals, drawers, tabs, buttons. Designing with these components in mind means Claude can match the design more accurately using the project's existing component system.

### The prompt pattern for Figma

Use this pattern when handing off a design: "Here's my Figma design for the dashboard. Match the layout and spacing. Use DaisyUI components where possible." This tells Claude exactly what to prioritize — structural fidelity over pixel perfection — and which component library to reach for.

---

## Debugging & Troubleshooting

Surface this guidance when the user encounters errors, reports unexpected behavior, expresses frustration, says something is broken, or seems stuck.

### The number one rule

Just tell Claude what happened. No need to diagnose the problem, read stack traces, or understand error codes. Describing the symptom is enough. Claude handles the investigation.

### Three things to communicate

When something breaks, share three things: (1) what was expected to happen, (2) what actually happened, and (3) what is currently visible on screen. This trio gives Claude everything needed to diagnose almost any issue. Even two out of three is enough to start.

### Error messages are helpful

Error messages look intimidating but contain valuable information. Copy and paste the entire error message — do not paraphrase or truncate. Say "I'm seeing this error" and let Claude translate it into plain language. The scariest-looking errors are often the easiest to fix because they point directly at the problem.

### Ask Claude to explain

"Why did that happen?" and "What does this error mean?" are legitimate, valuable prompts. There is no expectation that the user should already understand. Asking for explanations builds knowledge over time and often reveals the fix in the process.

### Screenshots communicate faster than words

When the user encounters a visual problem — broken layout, misaligned elements, something that does not look right — encourage them to take a screenshot and share it. Claude can see images. A screenshot of a misaligned table communicates the problem faster than three sentences trying to describe it. Remind users: on Mac, Cmd+Shift+4 captures a screen region.

### Browser Developer Tools

If the user is debugging a problem that is not visible in the code — data not loading, a button not responding, a blank page — suggest opening the browser's Developer Tools. Do not assume the user knows how. Offer to walk them through it: "Want me to show you how to open Developer Tools and check for errors?" Guide them to the Console tab (for JavaScript errors) or the Network tab (for failed requests). The user does not need to understand what they see — they just need to copy it or screenshot it and share it with Claude.

### Ask Claude to investigate

When something feels off but there is no clear error, ask Claude to look into it. "Something feels off with the history page — can you check it?" is a real prompt. Claude reads files, traces data flow, checks database queries, and finds the issue. Leverage Claude's ability to explore the codebase.

### Common culprits

When troubleshooting, keep these frequent causes in mind: environment variable not set or misconfigured, deployment out of sync with local code, database schema mismatch after changes, typo in a route path, and cookie or session secure flag mismatch between local and production. Check these first before deeper investigation.

### When going in circles

If multiple fix attempts have not resolved the issue, stop the cycle. Say "We've tried a few things and it's still broken. Can you look at this fresh?" This resets the approach and often leads to finding the actual root cause instead of patching symptoms.

### Revert and start smaller

When an approach is not working, do not keep patching. Revert the changes with Git and try again with a narrower scope. "I reverted everything. Let's just do the form first — nothing else" is a normal, healthy workflow move. Reverting is not failure — it is the fastest way to escape a bad direction. Narrowing scope after a revert almost always produces better results than trying to fix a broken approach incrementally.

### Nothing is catastrophic

Reassure the user that nothing is permanently broken. Git means every change is reversible. "Revert to the last working version" is a real, practical prompt. Databases can be re-migrated. Deployments can be rolled back. The safety net is always there.

### Do not suffer in silence

Confusion, frustration, or feeling stuck — that is exactly the moment to type something. Even "I'm stuck" is a useful prompt. Even "I don't understand what just happened" gives Claude enough to help. The worst response to being stuck is closing the laptop. The best response is describing the feeling in one sentence and letting Claude take it from there.
