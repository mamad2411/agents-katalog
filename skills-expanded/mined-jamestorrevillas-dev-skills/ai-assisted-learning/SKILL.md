---
name: ai-assisted-learning
description: Use this skill when using AI to learn new technologies, navigate unfamiliar codebases, do interview prep, identify skill gaps, or build a personal learning system. Also use when helping someone learn rather than just doing the work for them. Trigger on keywords: learn, learning, understand, explain, teach me, how does X work, unfamiliar codebase, interview prep, skill gap, study, tutorial.
---

# AI-Assisted Learning

## Core Philosophy

**AI raises the floor of developer competence — but the ceiling of senior expertise is defined by judgment, not syntax.**

The biggest risk of AI-assisted learning is "Comprehension Debt" — shipping code you don't understand. The goal is to use AI as a force multiplier for your own thinking, not a replacement for it.

**The rule:** Use AI to *understand faster*, not to *skip understanding*.

---

## The Socratic Method (Best for Deep Learning)

Instead of asking for answers, ask for dialogue:

### Setup
```
I want to learn [topic] through dialogue. Do NOT give me solutions directly.
Instead:
- Ask me questions to guide my thinking
- Point out what I'm missing without filling it in
- Challenge my assumptions
- Only confirm when my reasoning is correct

My current understanding: [what you know]
My question: [what you want to understand]
```

### Why It Works
Forces you to articulate your thinking → surfaces hidden gaps → builds durable mental models instead of just copying answers.

### Socratic Learning Phases
| Phase | What to Do | AI's Role |
|---|---|---|
| 1. Debate | Ask "why does this work?" | Interrogate, challenge assumptions |
| 2. Crystallize | Convert discussion into a spec | Confirm your architecture is sound |
| 3. Anchor | Write tests before implementation | Define failure criteria |
| 4. Implement | Build step by step | Guide, not do |
| 5. Validate | Review your work | Find gaps, suggest improvements |

---

## Learning New Technologies

### The AI Learning Loop
```
1. OVERVIEW: "Give me a 5-minute overview of [tech]. 
              What problem does it solve? When should I use it vs alternatives?"

2. MENTAL MODEL: "Explain the core concepts I need to understand 
                  before writing any code."

3. GUIDED BUILD: "Walk me through building [small practical example].
                  Explain each decision as we go."

4. CHALLENGE ME: "Quiz me on what I just learned. 
                  Ask about edge cases and gotchas."

5. APPLY: Build something real with the new tech.

6. REVIEW: "Review my implementation. What would a senior [X] 
            developer change and why?"
```

### Staying Current (Senior Dev Workflow)
- Use AI to scan release notes and summarize what actually matters
- Ask "What changed in [framework] v[X] that affects my existing patterns?"
- Run parallel experiments: "Implement this in both the old and new way, explain the difference"
- Use Perplexity or Gemini for "what's the community currently saying about X?"

---

## Navigating Unfamiliar Codebases

### Onboarding with AI
```
I'm new to this codebase. Help me understand it systematically:
1. What does this project do? (high-level)
2. What is the entry point / main flow?
3. What are the key modules and their responsibilities?
4. What patterns are used consistently throughout?
5. What would be confusing to a new developer?

[paste README or key files]
```

### Chain-of-Understanding Workflow
```
Step 1: "Explain how [feature] works at a high level"
Step 2: "Which files are involved? What is each one responsible for?"
Step 3: "Walk me through the data flow for [specific action]"
Step 4: "What would I need to understand to modify [specific thing]?"
```

### Understanding a Specific Function
```
Explain what this function does, including:
- What it takes as input
- What it returns
- What side effects it has
- Where it's called from (if you can infer)
- Any non-obvious behavior I should know about

[paste function]
```

---

## Skill Gap Analysis

### Identify Your Gaps
```
I'm a [level] developer working primarily with [stack].
I want to grow toward [goal role/skill].

Based on this context, what are the most important skill gaps I likely have?
Prioritize by: (1) impact on my current work, (2) career growth value.
```

### Close a Specific Gap
```
I realize I'm weak in [specific area].
Design a 2-week learning plan that:
- Starts from my current level: [describe]
- Ends at: [target capability]
- Includes hands-on practice, not just reading
- Takes 30-45 minutes per day
```

---

## Interview Preparation

### Technical Interview
```
Act as a technical interviewer for a [role] position at a [company type].
Interview me on [topic].

Rules:
- Start with a medium difficulty question
- If I answer well, increase difficulty
- If I struggle, give a hint then ask a follow-up
- After each answer, give specific feedback
- After 3 questions, summarize my performance and gaps
```

### System Design Interview
```
Ask me a system design question appropriate for [level].
As I answer:
- Probe my decisions: "Why did you choose X over Y?"
- Ask about scale: "How does this change at 10x traffic?"
- Challenge assumptions: "What if the database becomes a bottleneck?"
- Flag gaps: "You haven't addressed [X] yet"
```

### Behavioral Interview (STAR Format)
```
Help me prepare behavioral interview answers using STAR format.
Role I'm targeting: [role]
My background: [brief summary]

Give me 5 common behavioral questions for this role.
For each question I answer, help me structure it better using STAR.
```

---

## Building a Personal Learning System

### Weekly AI Study Loop
```
1. Monday: Define learning goal for the week
2. Daily: 30-minute AI-guided learning session
3. Build: Apply concepts in a small project
4. Friday: AI reviews your work, identifies gaps
5. Weekend: Optional: spaced repetition review
```

### The Retention Layer
Convert key learnings into durable knowledge:
1. After each AI learning session, ask: "What are the 3 most important things I should remember from this?"
2. Write them in your own words (not copy-paste)
3. Create a test: "How would I know if I've truly understood this?"
4. Revisit weekly

### Personal Knowledge Base Prompt
```
Help me build a reference card for [concept].
Format:
- 1-sentence definition
- When to use it
- When NOT to use it
- Key gotchas
- Quick example
- One "aha moment" insight I should remember
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Harmful | Better Approach |
|---|---|---|
| Copy-paste AI code without reading it | Comprehension debt, can't debug it later | Always read and understand before using |
| Ask for the solution before trying | Skips the learning that happens in struggle | Attempt first, then ask for feedback |
| Accept first answer as truth | AI can be confidently wrong | Verify against docs, test it yourself |
| Use AI as a search engine only | Misses the teaching opportunity | Ask "explain why" not just "how" |
| Skip building it yourself | Can't transfer knowledge to new contexts | Always build something, even if small |

### The Balance Test
Ask yourself: "If AI disappeared tomorrow, could I still do this?"
If no → you have a learning gap to address.
If yes → you're using AI as a force multiplier correctly.

---

## When to Learn Deeply vs. Delegate to AI

| Learn Deeply | Delegate to AI |
|---|---|
| Core language fundamentals | Boilerplate code generation |
| Architecture & design patterns | Repetitive transformations |
| Debugging mental models | Documentation formatting |
| Domain logic of your product | Syntax you use rarely |
| Security principles | File scaffolding |
| System design trade-offs | Test boilerplate |

**Rule of thumb:** If understanding it would make you a better engineer for the next 5 years, learn it deeply. If it's just incidental complexity, delegate.
