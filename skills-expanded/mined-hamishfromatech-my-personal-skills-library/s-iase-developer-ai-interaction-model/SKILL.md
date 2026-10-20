---
name: s-iase-developer-ai-interaction-model
description: Model developer programming behavior across four dimensions (intention, action, supporting tool, emotion) when interacting with AI assistants. Use when analyzing developer-AI interaction patterns, designing AI coding tools that account for emotional dimensions, studying the "trust but verify" and "impostor phenomenon" patterns in AI-assisted development, or building multimodal developer behavior annotation systems.
---

# S-IASE: Developer-AI Interaction Model

## Overview

The S-IASE model characterizes a developer's programming State through four dimensions: Intention, Action (paired with Supporting Tool), and Emotion. It is the first model to explicitly capture the emotional dimension of developer-AI interaction alongside intentions, actions, and tool usage, revealing patterns invisible to activity-based taxonomies like CUPS or Google's SIA model.

Source: Wu, Li, Stolee & Xu (NC State/Oklahoma, PACMSE Vol 3 FSE, 2026).

## When to Use

- Analyzing developer-AI interaction from the developer's perspective (not external observation)
- Designing AI coding tools that account for emotional and psychological dimensions
- Studying "trust but verify" patterns in AI-assisted development
- Investigating impostor phenomenon and guilt in AI-assisted coding
- Building developer behavior annotation or analysis tools
- Designing AI assistants that support visual guidance and modality-appropriate communication
- NOT for: purely performance-focused analysis that ignores developer experience

## The Four Dimensions

### D1: Intention (12 categories)
The invisible motivation behind every action:
- To Understand Context
- To Design/Plan New Code
- To Implement Code
- To Set Up Project Environment
- To Clarify Requirements/Ambiguity
- To Explore Alternative Solutions
- To Resolve Errors
- To Verify Existing Code
- To Evaluate Suggestions
- To Optimize Code
- To Understand Required Knowledge
- Do Nothing

### D2: Action (16 categories)
How developers proceed toward intentions:
- Configuration, Reading and Comprehension, Executing the Code, Waiting
- Crafting Query/Prompt, Writing New Code, Editing Existing Code, Writing Documentation
- Watching Program Status, Accepting results from tools, Refining results from tools
- Rejecting results from tools, Logging, Editing Query/Prompt, Running Tests, Search

### D3: Supporting Tool (8 categories)
Whether and how AI is involved:
- Database Tools, Search Engine, AI Tools, Proprietary Dev Platform
- Compiler, Static Program Analysis, IDE, Not using any tools

### D4: Emotion (7-point valence scale)
- Extremely Positive → Positive → Slightly Positive → Neutral → Slightly Negative → Negative → Extremely Negative
- Captured via Russell's circumplex model of affect, retrospective self-annotation

## Key Findings

### Aggregated Patterns

**Intentions more frequent with AI**:
- To Evaluate Suggestions (β=0.069, p<.001) — significantly more frequent
- To Verify Existing Code, To Resolve Errors, To Optimize Code, To Implement Code, To Design/Plan New Code

**Actions more frequent with AI**:
- Executing the Code (β=0.096, p<.001)
- Editing Query/Prompt (β=0.028, p<.001)
- Reading and Comprehension significantly LESS frequent (β=-0.146, p<.001) — vibe coding pattern

**Supporting tools**: AI-assisted developers relied significantly less on Search Engines (β=-0.246, p<.001) — AI replaces traditional knowledge interfaces

**Emotion**: AI assistance associated with significantly more positive emotions (β=0.632, p=.016) but with hidden costs (see below)

### Sequential Patterns

**Trust but Verify**: To Understand Context → To Implement Code → To Design/Plan New Code
- Reverses traditional "Design-then-Implement" paradigm
- Developers use AI to implement first, then refine design based on output
- Skepticism for familiar-but-not-fluent tasks (double-checking AI answers externally)

**Iterative Feedback Loop**: Reading and Comprehension → Crafting Query/Prompt → Writing New Code → Reading and Comprehension
- Developers cycle between review, generation, and modification
- AI suggestions treated as drafts, not final solutions

### Emotional Patterns

**Emotional Stability vs. Hidden Costs**:
- AI-assisted participants showed statistically more stable emotional flows
- BUT reported impostor-like feelings, guilt, and self-doubt

**Guilt from over-reliance**:
- "I finished the REST API integration with ChatGPT's help, but I feel guilty — like I didn't learn anything"
- Tension between speed and understanding: AI boosts completion but sacrifices learning depth

**Impostor phenomenon**:
- Self-criticism: "ChatGPT is always right. If the output is wrong, I must've messed up the prompt."
- Blaming machine: "My first thought was, 'Is my laptop broken?' I wasted 3 minutes checking my laptop."
- Developers internalize AI failures rather than questioning the tool

### Modality Mismatch

When AI provides text-only instructions for visual tasks (e.g., database setup, API configuration):
- Developers abandon AI assistants for Stack Overflow or official documentation with screenshots
- "ChatGPT told me to 'add the token' but where exactly? Some screenshots or visual steps would've saved me 10 minutes of guessing."
- Need for visual guidance in AI coding tools for procedural/setup tasks

## Design Implications

1. **Trust calibration through transparency**: comprehension indicators ("Detected intent: Add OAuth2 flow"), confidence visualization, assumption feedback
2. **Flow preservation through abstraction resilience**: proactive recovery when natural language fails, clarification questions instead of incorrect output
3. **Expertise-adaptive interaction**: step-by-step breakdowns for novices, implementation transparency for experts
4. **Visual guidance for procedural tasks**: screenshots, diagrams, step-by-step visual instructions alongside text
5. **Emotional awareness**: detect and address guilt/impostor feelings through reflective prompts and learning modes

## Methodology

- Mixed-methods study with 76 developers
- AI-assisted (n=62) vs non-AI (n=14) groups
- Two tasks: Python with GitHub REST API, Java with MySQL database operations
- Retrospective self-annotation via custom tool (~20 intervals per session)
- Sequential pattern mining via CloSpan algorithm
- Interview thematic analysis via socio-technical grounded theory (STGT)
- 14 follow-up interviews

## A-Tech Alignment

- **Open-source**: replication package available at github.com/YinanWusoymilk/FSE-2026-How-Developers-Interact-with-AI
- **Data privacy**: behavioral analysis from screen recordings, no physiological data required
- **Financial freedom**: understanding developer-AI interaction improves tool design and reduces wasted effort
- **Practical implementation**: annotation tool and model categories directly applicable to AI coding tool design