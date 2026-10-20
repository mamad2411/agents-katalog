---
name: Curiosity Gap & Progressive Disclosure
description: Apply information gap theory and progressive disclosure to create compelling, ethical curiosity loops in developer tool onboarding, technical content, and community activation. Designed for open-source products that respect autonomy and intelligence.
version: 1.0.0
---

# Curiosity Gap & Progressive Disclosure Psychology

## Overview

This skill leverages two deeply connected psychological principles — the **Curiosity Gap** (Information Gap Theory, Loewenstein 1994) and **Progressive Disclosure** — to drive developer engagement, content completion, and community participation without manipulation. When applied ethically, curiosity becomes an autonomy-supportive force: users explore because they *want* to close the gap, not because they're trapped by it.

In open-source and developer-tool contexts, where audiences are naturally skeptical of marketing, the curiosity gap is uniquely powerful. Developers are epistemically motivated — they solve puzzles for a living. The right gap makes your documentation unreadable-in-the-best-way. The wrong gap feels like clickbait and destroys trust instantly.

## Core Principles

- **Information Gaps Are Motivational Voids**: When people become aware of a gap between what they know and what they want to know, they experience an aversive state that drives information-seeking behavior.
- **Curiosity Is Reward In Itself**: Closing an information gap activates the same dopaminergic reward circuits as external rewards. The brain *enjoys* learning.
- **Progressive Disclosure Respects Cognitive Load**: Revealing information in stages prevents overwhelm while maintaining forward momentum.
- **Ethical Boundaries Are Non-Negotiable**: The gap must always close. Never exploit curiosity to trap users, extract data, or deliver disappointment.
- **Autonomy Amplifies Engagement**: Users who choose to explore a gap value the discovery more than those driven by forced progression.

## Core Concept

George Loewenstein's Information Gap Theory (1994) posits that curiosity arises when attention is focused on a gap in one's knowledge. The magnitude of curiosity is determined by:
1. The *value* of the information (how much does knowing this matter?)
2. The *perceived closeness* to closure (do I feel like I can figure this out?)
3. The *baseline knowledge* required (am I close enough to understand it?)

For developers, this translates directly: a README that reveals *just enough* architecture to make the reader want to see the implementation. A tutorial that shows a working demo, then asks "but how does it handle edge cases?" before revealing the answer. A book chapter that ends with a solved problem and the question: "but what happens when you run this at scale?"

Progressive Disclosure, first formalized in HCI research, complements this by controlling *when* information appears. Rather than dumping the full manual, you disclose in layers: first the promise, then the principle, then the implementation, then the configuration, then the extension points. Each layer creates a new, smaller curiosity gap that pulls the user forward.

## The Curiosity Gap Architecture

### The Three Types of Gaps

| Gap Type | Mechanism | Best Used For | Risk |
|----------|-----------|---------------|------|
| **Knowledge Gap** | "I don't know X, and I want to." | Documentation, tutorials, book chapters | Must close completely; no abandoned gaps |
| **Completion Gap** | "I've started, and I want to finish." | Onboarding checklists, setup wizards, courses | Don't stretch artificially; respect time |
| **Competence Gap** | "I can do this, but I want to master it." | Skill trees, advanced features, community depth | Never shame the beginner |

### The Progressive Disclosure Stack

**Layer 1: The Promise** (What is possible?)
- One sentence. One demo. One result.
- Creates the initial knowledge gap: "How did they do that?"
- Example: A-Coder's homepage shows a 10-second demo of an agent writing and testing code autonomously.

**Layer 2: The Principle** (Why does it work?)
- One paragraph explaining the core mechanism.
- Closes the first gap, opens a second: "But how is that implemented?"
- Example: "Morph Fast Apply uses exact-match requirements and smart diff previews to eliminate the 'apply-and-hope' problem."

**Layer 3: The Implementation** (How do I use it?)
- Step-by-step instructions with working examples.
- Closes the second gap, opens a third: "What else can I do with this?"
- Example: A-Coder tutorial walks through the first agent build, ending with: "Now your agent can write code. But can it review its own PRs?"

**Layer 4: The Extension** (How do I make it mine?)
- Plugin APIs, configuration options, customization paths.
- Closes the third gap, opens a fourth: "What does the community build with this?"
- Example: "Write your first plugin in 5 minutes. Here's the scaffold."

**Layer 5: The Contribution** (How do I give back?)
- Contribution guides, community showcases, recognition systems.
- Closes the fourth gap, opens a fifth that loops outward: "What could I build that doesn't exist yet?"
- Example: Builder's Club spotlights member-built plugins.

### The Ethical Curiosity Checklist

Before deploying any curiosity gap, verify:
- [ ] **The gap closes.** The user receives the promised information.
- [ ] **The closure satisfies.** The answer is worth the journey.
- [ ] **The user chose.** No forced progression, dark patterns, or artificial gates.
- [ ] **The next gap is optional.** Users can stop at any layer without penalty.
- [ ] **No extraction.** Curiosity is not a pretext for harvesting data or attention.

## Application: A-Coder IDE

### The "5-Minute Mystery" Onboarding
Traditional onboarding dumps features. Curiosity-driven onboarding reveals a mystery and gives the user the first clue.

**Welcome screen**: Instead of "Here are 10 features," try:
> "In the next 5 minutes, you'll teach A-Coder to write code the way *you* think. But first — here's something strange. Open any file and press Ctrl+Shift+M. What happens?"

The user discovers Morph Fast Apply on their own. The knowledge gap ("What does this button do?") is immediately closed by the satisfying diff preview. But a completion gap opens: "I've seen it work once. I want to see it work on my actual project."

**First session arc**:
1. Mystery (Ctrl+Shift+M) → 2. Discovery (diff preview works) → 3. Competence gap ("How do I make this automatic?") → 4. Deeper dive (agent configuration)

Each layer is 2-3 minutes. The user can stop after any layer. Most don't.

### The Documentation as Detective Novel
Structure key documentation pages as curiosity-driven narratives:
- **The Hook**: Show a problem that seems unsolvable.
- **The Clue**: Reveal one principle that makes it solvable.
- **The Twist**: Show an edge case that breaks the simple version.
- **The Resolution**: Provide the robust implementation.
- **The Sequel Tease**: End with "But what if you need to do this across 100 files? See Advanced Patterns."

Storytelling frame (scars not wounds):
- **Scar**: "We built Morph Fast Apply after watching developers lose hours to AI-generated code that almost worked. The scar is the system we built to never let that happen again."
- **Wound to avoid**: "Here's the frustrating error message you used to see. We don't miss it."

### The Plugin Discovery Loop
After day 3 of use, reveal a small curiosity gap:
> "You've written 200 lines with A-Coder. Did you know there's a plugin that summarizes your git diff in natural language before you commit?"

Not a notification. Not a pop-up. A contextual whisper in the status bar or terminal footer. The user *chooses* to investigate. The closure (installing the plugin, seeing it work) creates positive association.

## Application: Be Practical Book/Playbooks

### The Chapter Cliffhanger
End each chapter with a closed scar and an open curiosity gap:
- **Closed scar**: "You now have a working local AI pipeline that respects your data."
- **Open gap**: "But this runs on one machine. What happens when your team needs to share models without sharing data? That's Chapter 7."

The gap must be *genuine* — Chapter 7 must deliver. Never fabricate mystery around content that doesn't exist or disappoints.

### The Playbook as Puzzle Box
Each playbook is not a chapter summary. It's a puzzle the reader solves:
- **Page 1**: A scenario ("Your client wants an AI agent that processes invoices but won't let data leave their network.")
- **Pages 2-3**: Constraints and failure modes (the wound)
- **Pages 4-6**: The framework (the scar — what works)
- **Page 7**: A blank template and the question: "How does this apply to your stack?"

The reader must *work* to close the final gap. The IKEA effect amplifies this: the playbook they complete is worth more to them than one they merely read.

### The "Next Chapter Preview" as Ethical Teaser
In digital editions, replace table-of-contents dumps with curiosity-driven previews:
- Don't say: "Chapter 3 covers vector databases."
- Say: "There's a database choice that makes your local AI 40x faster — and it's probably not the one you're using. Chapter 3 reveals the benchmark."

The gap is specific, measurable, and closable. The reader knows exactly what they'll learn and feels the pull to continue.

## Application: Open Source AI Builder's Club

### The Tiered Reveal
Community content should disclose progressively:
- **Public**: The promise. "Members are building autonomous agents that run entirely on-device."
- **Free member**: The principle. "Here's the architecture pattern 80% of them use."
- **Active contributor**: The implementation. "Here's the repo, the config, and the failure log."
- **Core member**: The extension. "Here's how to modify the architecture for multi-agent orchestration."
- **Recognized builder**: The contribution path. "Here's how to publish this as a standard the community adopts."

Each tier closes one gap and opens the next. No tier is "walled content" — it's "earned disclosure." The gap closes through participation, not payment. This aligns with financial freedom values: value flows to contribution, not capital.

### The "What Are They Building?" Loop
Weekly community spotlights create curiosity gaps between members:
- **Monday**: "Someone in the Club built something this week that reduced their inference costs by 90%. Spotlight drops Friday."
- **Tuesday-Thursday**: Clues in the forum (architecture hints, benchmark teasers)
- **Friday**: Full reveal with repo link and builder interview

The gap drives forum engagement. The closure delivers value. The builder gets recognition. No extraction. No clickbait.

### The Skill Tree as Curiosity Map
Visualize the community's knowledge as a discoverable skill tree:
- Nodes are initially grayed out with tantalizing labels: "Local Multi-Agent Orchestration," "Zero-Shot Function Calling on Edge Devices"
- Hover reveals the prerequisite: "Requires: Local Model Mastery + Agent Design Patterns"
- Clicking a prerequisite reveals the path: "Complete Playbook 4 and share one agent build to unlock"

The tree creates visible knowledge gaps. The path to close them is transparent. The user chooses their journey.

## Synergies With Existing Skills

| Existing Skill | How Curiosity Gap Amplifies It |
|---------------|-------------------------------|
| **IKEA Effect & Digital Ownership** | Curiosity gaps pull users into creation; ownership rewards them for closing it |
| **Implementation Intentions & Action Design** | If-then plans trigger action; curiosity gaps supply the "why" that makes the plan stick |
| **Goal-Gradient Effect** | Progressive disclosure creates micro-goals; curiosity provides the fuel to reach them |
| **Scars Not Wounds Storytelling** | The scar is the closed gap; the wound is the abandoned one. Structure narratives as gap-closure journeys |
| **Self-Determination Theory** | Autonomy-supportive curiosity gaps satisfy the competence need; user-chosen exploration satisfies autonomy |

## Anti-Patterns: When Curiosity Becomes Manipulation

- **The Eternal Gap**: Content that never delivers on its promise. Destroys trust permanently.
- **The Data Extraction Gap**: "Find out how → give us your email first." If the information isn't worth the email, it's manipulation.
- **The Forced Scarcity Gap**: "Only 3 spots left!" when there are unlimited spots. Developers detect this instantly.
- **The Competence Shame Gap**: "Real developers know this..." Curiosity should invite, never exclude.
- **The Attention Vampire**: Infinite scroll, auto-playing next videos, unclosable modals. These exploit the completion gap to harvest time, not deliver value.

## Key Phrases to Use

- "Here's what we discovered when we tried the obvious approach..."
- "The solution seems simple until you hit this one edge case..."
- "By the end of this section, you'll know exactly why most agents fail at this step."
- "We built this because of a problem that took us three months to fully understand."
- "There's one configuration most people miss. It's on the next page."

## Key Phrases to Avoid

- "This one weird trick..."
- "You won't believe what happens next..."
- "What [competitor] doesn't want you to know..."
- "Doctors hate him..." (or developer equivalents)
- Any headline that promises more than the content delivers

## Measurement

Track ethical curiosity gap effectiveness through:
- **Completion rate per layer**: Are users voluntarily advancing through disclosure stages?
- **Time-to-close**: How long does the gap hold attention before closure? (Too short = no curiosity; too long = frustration)
- **Return rate**: Do users come back to close gaps they paused?
- **Contribution correlation**: Do users who complete curiosity-driven onboarding contribute more to the community?
- **Sentiment on closure**: Is the closure satisfying? (Monitor support tickets, forum sentiment, NPS around specific content)

## References
- See `references/information-gap-theory.md` for the original Loewenstein framework and research citations.
- See `references/progressive-disclosure-patterns.md` for implementation patterns across documentation, onboarding, and UI.
