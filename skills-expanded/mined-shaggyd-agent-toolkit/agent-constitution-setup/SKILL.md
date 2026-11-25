---
name: agent-constitution-setup
description: "Build three essential docs for AI agent context: personal constitution, goals, and business strategy. Based on Allie Miller's framework."
version: 1.1.0
author: Dustin Chadwick
license: MIT
metadata:
  hermes:
    tags: [agent-setup, onboarding, constitution, productivity, personalization]
    source: "Allie Miller on Silicon Valley Girl with Marina Mogilko — https://www.youtube.com/watch?v=YfRkj9kmQf0"
    related_skills: [hermes-agent, incremental-onboarding]
---

# Agent Constitution Setup

Build three documents that give AI agents deep context about who you are, where you're going, and what you're building. Framework developed by AI advisor Allie Miller: without these files, every AI interaction starts from a blank slate. With them, the agent operates from your actual context.

**Author:** Dustin "Dusty" Chadwick ([@ShaggyD](https://github.com/ShaggyD))

## Problem

AI agents start every interaction from a blank slate. Without context on who you are, what you value, and where you're going, every response is generic. The agent can't prioritize, can't make judgment calls that reflect your actual personality, and can't push back on bad ideas in a way that sounds like you.

## Built

Three documents that give AI agents deep context about your operating framework. The Personal Constitution captures your core values and decision-making patterns. The Goals Document tracks what you're optimizing for this year. The Core Business Strategy lays out what you do, who you serve, and critically, what you've tried and failed at before. All three based on [Allie Miller's framework](https://www.youtube.com/watch?v=YfRkj9kmQf0) from her Silicon Valley Girl interview.

## Outcome

The agent operates from your actual context instead of guessing. It knows your communication style, your tradeoff preferences, and the mistakes you don't want to repeat. An agent that's had this setup gets directives right on the first try instead of needing three rounds of correction.

## The Three Files

### 1. Personal Constitution (timeless)
**What it is:** Your core values, decision-making framework, personality, and operating principles. Not tied to any year or week — this is the "who you are at your core" doc.

**Why it matters:** Without it, the agent has no compass for how you make decisions, what tradeoffs you'd make, or how to communicate with you. Every response is generic instead of *you*.

**How to build it:**
- Use scenarios, not direct questions. Give the user situations and ask their gut reaction. Examples: shipping imperfect work, pushing back on bad ideas, handling credit, deep work interruptions.
- Cross-reference with personality test results if available (MBTI, Big Five, Enneagram). Look for tensions between traits — the edges are where the constitution gets sharp.
- Include both strengths AND acknowledged weaknesses. A constitution that only flatters is useless.
- Iterate: draft, ask what doesn't sit right, rewrite. The user should feel slightly exposed — that's how you know it's real.

**Format:** Plain markdown, one heading. Save wherever your agent can access it (e.g. agent context, project files, a dedicated references directory).

### 2. Goals Document (time-bound)
**What it is:** Annual/quarterly/monthly goals, habits to build, habits to kick, specific inputs/outputs to manage.

**Why it matters:** Turns the agent from a dumb tool into something that proactively aligns with your trajectory. At minimum, the agent should know what you're optimizing for and what you're trying to change.

**How to build it:**
- Ask one category at a time: professional wins, personal routines, energy leaks.
- Focus on feelings first ("by December I want to feel like I finally ____"), then translate to specifics.
- Keep it lean. If it's longer than a screen, it won't get used.

**Format:** Plain markdown with sections. Filename includes the year (e.g. `goals-2026.md`).

### 3. Core Business Strategy (contextual)
**What it is:** What your business is, who you serve, who you don't serve, value proposition, and — critically — the things NOT on your website or LinkedIn. The failed podcast, the org that retreats to safety, the patterns that explain decisions.

**Why it matters:** Without it, the agent treats everything as equally important. With it, the agent knows what to say no to and why certain things failed before.

**How to build it:**
- Separate day job from side projects — different strategies, different audiences.
- Ask directly: "What's something true about this that you'd never put on a public slide deck?" That answer IS the strategy doc.
- Capture constraints, not just aspirations. Real strategy lives in the friction.

**Format:** Plain markdown with sections.

## Using These Documents

After building all three docs, integrate them into your agent's context:

1. **Store them where your agent can read them** — project files, a knowledge base, a dedicated references directory, clipboard, or custom instructions.
2. **Reference them explicitly** — tell your agent where to find them and when to load them (e.g. "Load these when planning, prioritizing, or making recommendations").
3. **Condense the constitution** into a short summary your agent always has — core values, decision-making style, communication preferences. Keep the full doc for detailed reference.
4. **Write an agent service standard** — the agent's equivalent of a goals doc. Defines what "good" looks like: escalation boundaries, proactivity ceiling, output quality bar, noise discipline. See `references/agent-service-standards.md` for a framework.
5. **Iterate** — these are living documents. Return to them quarterly and refine.

> **Hermes Agent users:** See `references/hermes-integration.md` for platform-specific steps (memory consolidation, `.hermes/references/` setup, GitHub publishing).

## Templates

This skill ships with two kinds of templates:

| File | Description |
|------|-------------|
| `references/example-dusty-constitution.md` | **Real example** from Dustin Chadwick's personal constitution |
| `references/example-dusty-goals.md` | **Real example** from Dustin Chadwick's 2026 goals |
| `references/example-dusty-strategy.md` | **Real example** from Dustin Chadwick's business strategy |
| `templates/generic-constitution.md` | Placeholder template — replace with your own content |
| `templates/generic-goals.md` | Placeholder template — replace with your own content |
| `templates/generic-strategy.md` | Placeholder template — replace with your own content |

The real examples illustrate what the final output looks like. Start with the generic templates and replace the bracketed text.

## Interviewing Tips

- **One question at a time.** Don't dump categories. Let each answer breathe.
- **Scenarios beat abstractions.** "Here's a situation, what do you do?" surfaces real values faster than "what are your values?"
- **Push back on the draft.** If the user says "that doesn't sit right," dig into why. The rewrites are where the real self-knowledge emerges.
- **Save drafts.** Users will want to return and refine. These are living documents, not one-and-done.

## Pitfalls

- **Constitutions are NOT goals.** If an entry could reasonably change next year, it belongs in the goals doc, not the constitution.
- **Don't interview like a form.** If the user gives you a personality test result, use it. Cross-reference traits against what you've observed.
- **The third doc hurts.** If the business strategy doc is just marketing copy, you didn't go deep enough. The real strategy is what you'd tell a trusted advisor, not a customer.
- **Memory/context budget is finite.** A wall of text gets skimmed. Keep constitution values condensed into a short summary, with the full doc available for deep reference.
- **Files are portable.** Store them in a way that survives agent resets. Project files, a git repo, or a synced directory are better than ephemeral chat context.

## Attribution

**Framework by Allie Miller** — AI advisor to OpenAI, Google, Anthropic, and Fortune 500 leaders. One of the top voices in enterprise AI.

**Source:** ["Silicon Valley Girl" with Marina Mogilko](https://www.youtube.com/watch?v=YfRkj9kmQf0) — Allie Miller on building proactive AI agents, skills, and the three essential files every agent user needs.

**Key quote:** "Three documents that I would start with: the first is your personal constitution. This has nothing to do with what year it is, what you did last week — everything about this document is just who you are at your core."

**Allie's links:**
- YouTube interview: https://www.youtube.com/watch?v=YfRkj9kmQf0
- Silicon Valley Girl (Marina Mogilko): https://www.youtube.com/@SiliconValleyGirl
