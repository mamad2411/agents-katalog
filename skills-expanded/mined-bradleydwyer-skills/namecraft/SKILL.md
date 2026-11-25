---
name: namecraft
description: >
  Guide structured product and project naming ideation. Use when the user wants
  to brainstorm names, evaluate candidate names, analyze the phonetics or feel
  of names, or discuss naming strategy for apps, services, libraries, agents,
  chatbots, CLIs, or any digital product. Also trigger when the user mentions
  naming conventions, name scoring, SMILE/SCRATCH evaluation, or asks to compare
  or rank candidate names. Even if the user just says "I need a name for..."
  or "what should I call this?", this skill applies. Does NOT handle domain
  availability checking — the user has a separate tool for that.
---

# Namecraft — Naming Ideation Guide

Help the user brainstorm, generate, and evaluate names for digital products. This skill encodes decades of naming research, psycholinguistic principles, and professional evaluation frameworks into a structured ideation workflow.

## Workflow

### Step 1: Intake Interview

Before generating names, understand what you're naming. Ask about:

1. **What is it?** App, service, library, framework, CLI tool, API, AI agent, chatbot, or something else?
2. **Who is the audience?** Developers, consumers, enterprise buyers, internal team?
3. **What tone/personality?** Pick from or blend: playful, authoritative, minimal, warm, technical, premium, rebellious, approachable
4. **Competitive landscape** — What are similar products called? What names should we avoid sounding like?
5. **Constraints** — Max length? Must start with a specific letter? Avoid certain sounds or words? Must work internationally?
6. **Special context** — Is this a chatbot (needs approachability) or an agentic AI system (needs authority)? A consumer product (needs warmth) or a developer tool (needs precision)?

Don't require answers to all questions — infer reasonable defaults from context. If the user says "I need a name for my Rust JSON parser," you already know: library, developers, technical tone.

### Step 2: Generate Candidates

Generate **15-25 candidate names per round**, spanning at least 4 of these strategies:

| Strategy | What it is | Examples |
|---|---|---|
| **Suggestive** | Hints at function through metaphor | Slack, Stripe, Kindle, Zoom |
| **Arbitrary** | Real word, unrelated meaning | Apple, Shell, Uber, Plaid |
| **Fanciful/Coined** | Invented word, no prior meaning | Google, Kodak, Spotify, Twilio |
| **Compound** | Two recognizable words fused | YouTube, Dropbox, Snapchat, DoorDash |
| **Portmanteau** | Parts of two words merged | Instagram, Pinterest, Netflix, Groupon |
| **Classical/Mythological** | Greek, Latin, or mythological roots | Anthropic, Palantir, Jira, Atlas |
| **Nature/Metaphor** | Natural world imagery | Nest, Bloom, Cedar, Aurora, Ember |
| **Human Name** | Personal name evoking character | Claude, Ada, Oscar, Jasper |
| **Verb/Action** | Implies dynamism | Snap, Dash, Fetch, Gather, Spark |
| **Spatial/Geometric** | Precision, structure | Linear, Arc, Prism, Compass, Plane |

Read `references/naming-strategies.md` for the full taxonomy with deeper examples and psycholinguistic rationale for each strategy.

### Step 3: Evaluate Candidates

Score each candidate against these frameworks. Present as a comparison table.

**SMILE Test** (positive qualities — aim for all 5):
- **S**uggestive — evokes a positive brand attribute
- **M**emorable — anchored in familiar associations
- **I**magery — conjures a visual in the mind
- **L**egs — extensible for marketing, sub-products
- **E**motional — creates a feeling, not just information

**SCRATCH Test** (deal-breakers — any hit is a red flag):
- **S**pelling-challenged — hard to spell from hearing
- **C**opycat — too similar to an existing brand
- **R**estrictive — limits future growth/pivots
- **A**nnoying — feels forced or try-hard
- **T**ame — flat, boring, undifferentiated
- **C**urse of knowledge — insider reference nobody gets
- **H**ard to pronounce — blocks word-of-mouth

**Radio Test**: Could someone hear this name once and type it correctly into a search bar?

**5-Year Test**: Will this name feel current in 5 years, or will it be dated?

Read `references/evaluation-frameworks.md` for detailed scoring rubrics and anti-pattern catalog.

### Step 4: Phonetic Analysis

For top candidates, provide lightweight phonetic analysis:

- **Consonant character**: Hard stops (k, t, p) convey energy/precision. Fricatives (f, s, v) convey speed/flow. Liquids (l, r, m) convey smoothness/warmth.
- **Vowel positioning**: Front vowels (i, e) feel small/light/fast. Back vowels (o, u) feel large/powerful/substantial. Match to product personality.
- **Syllable count**: 1-3 syllables is the sweet spot. Every syllable adds cognitive load.
- **Stress pattern**: Trochee (STAR-bucks, AP-ple) feels natural in English.
- **Sound repetition**: Repeated sounds aid memorability (TikTok, Coca-Cola, Kit Kat).

If the `namecraft` CLI is available on PATH, run `namecraft analyze <name>` for programmatic scoring.

### Step 5: Anti-Pattern Check

Flag any candidates that fall into these traps:

- **Overused suffixes**: -ify, -ly, -io, -ai, -hub, -stack — signal "follower not leader"
- **Compound wallflowers**: Generic + Generic = forgettable (SmartFlow, CorePulse, NexPoint). Igor identifies these overused words: Active, Arc, Atlas, Blue, Bridge, Clear, Core, Edge, Flow, Force, Hub, Next, Path, Pulse, Shift, Smart, Stream, Wave, Wise
- **Reflexive "AI" appending**: Tacking "AI" onto names is already dated as AI becomes ambient
- **Dated conventions**: Dropped vowels (Flickr-style), creative misspellings (Lyft-style), e- or i- prefixes
- **Tech buzzword prefixes**: Cloud-, Cyber-, Blockchain-, Web3-
- **Puns**: Amusing once, then vapor

### Step 6: Present Recommendations

Output format:

1. **Candidate table** with columns: Name | Strategy | Syllables | SMILE Score (1-5) | SCRATCH Flags | Notes
2. **Top 3-5 recommendations** with detailed rationale for each
3. Reminder: "Domain availability not checked — use your domain tool separately"
4. Offer to generate more candidates in specific strategies or refine existing ones

## AI Product Naming

When naming AI products specifically, the naming approach should match the product's architecture:

**Chatbots / Conversational AI** — Optimize for approachability:
- Human names work well (Ava, Luna, Claude, Jasper)
- Soft phonetics: liquids (l, m), front vowels
- Playful descriptors (Witty, Bubble, Sage)
- The goal is "helpful companion," not "powerful machine"

**Agentic AI / Autonomous Systems** — Optimize for authority and trust:
- Mythological/classical names convey capability (Hermes, Atlas, Prometheus)
- Outcome-oriented names signal professionalism (Orchestrator, Conductor)
- Hard consonants (k, t, x), structured feel
- The goal is "competent system," not "cute assistant"

**Current trends (2024-2026):**
- "Labs" suffix signals research credibility (ElevenLabs, Stability AI Labs)
- Human names trending gender-neutral or male (Claude, Copilot, Gemini)
- Ultra-short names dominating: Cohere (6), Cursor (6), Pika (4), Suno (4)
- Nature metaphors as counterpoint to tech saturation

## Iteration

After presenting initial candidates, offer to:
- Generate more in a specific strategy the user liked
- Blend elements from multiple candidates
- Explore variations (prefixes, suffixes, compound forms)
- Deep-dive phonetic analysis on finalists
- Run the full SMILE/SCRATCH rubric on the shortlist
