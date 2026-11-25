---
name: karpathy-idea-files
description: 'Create and share ideas as abstract Gist-style specs instead of code — letting agents or others implement. Use this skill when the user wants to capture a new idea quickly, needs to write a project spec for an agent to implement, wants to share a concept without building it first, or says "write up this idea", "create a spec", "gist this", "idea file", "agent can implement this", "brief for this project". Based on Karpathy 27k-like LLM Wiki Gist post and GitHub repo.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-agentic-engineering
  - karpathy-minimalism
  - karpathy-output-evolution
  - karpathy-llm-wiki
---

# Skill 9: Idea Files / Gist-First Sharing（想法文件优先）

> Source: https://x.com/karpathy/status/2040470801506541998 | https://github.com/multica-ai/andrej-karpathy-skills
> "LLM Knowledge Bases idea file" — 27k likes

## Core Principle

**Ship the idea, not the implementation.**

Karpathy's Gist pattern: write a clear abstract + success criteria + constraints, then let an agent (or anyone) implement it for their specific context. One idea spec → infinite implementations.

The old model: write code → share code → others adapt code.
The Karpathy model: write idea spec → share spec → agents implement for context.

## The Idea File Template

Every new idea gets this format before any code is written:

```markdown
# [IDEA NAME]
> Status: [DRAFT / SPEC / ACTIVE / ARCHIVED]
> Created: [DATE]
> Source inspiration: [LINK or "original"]

## Abstract (2-3 sentences)
What is this? What problem does it solve? Why does it matter?

## The Core Insight
What's the one non-obvious observation that makes this idea work?
(If you can't write this, the idea isn't ready yet.)

## Success Criteria
When is this "done"? List 3-5 verifiable outcomes:
- [ ] [Observable outcome 1]
- [ ] [Observable outcome 2]
- [ ] [Observable outcome 3]

## Minimal Viable Version
Describe the simplest possible thing that would prove the concept works.
(One paragraph. No code yet.)

## Constraints
- Must work with: [tools/stack/dependencies]
- Must NOT require: [what to avoid]
- Scale target: [personal use / team / public]
- Time budget: [hours/days]

## Open Questions
Things I don't know yet that matter:
1. [Question 1]
2. [Question 2]

## Implementation Notes (optional)
Hints for whoever (agent or human) implements this:
- Suggested approach: [rough approach]
- Key risk: [what might go wrong]
- Prior art: [similar things that exist]

## Example Input/Output
Input: [example]
Output: [example]
```

## Converting a Vague Idea to a Spec

When you have a rough idea, use this prompt to crystallize it:

```
I have a rough idea I want to turn into an implementation-ready spec.

Rough idea: [YOUR VAGUE IDEA IN NATURAL LANGUAGE]

Help me write a proper idea file with:
1. A precise 2-sentence abstract (what + why)
2. The core non-obvious insight (the thing that makes it work)
3. 3-5 verifiable success criteria
4. The minimal viable version (simplest proof of concept)
5. 3 things an implementer needs to know
6. 2 open questions I should resolve before building

Be precise. Remove vagueness. If something is unclear, ask — don't invent.
```

## The Agent Implementation Prompt

Once you have an idea file, hand it to an agent:

```
Implement this idea spec for my specific context.

Idea spec:
[PASTE IDEA FILE]

My context:
- Environment: [OS, language, tools available]
- Existing codebase: [describe or paste relevant parts]
- Constraints: [anything specific to my setup]

Implementation rules:
1. Follow the success criteria exactly
2. Start with the minimal viable version
3. Ask before adding anything not in the spec
4. Output code + a README explaining how to run it
5. Flag any open questions from the spec that affect implementation
```

## Sharing Idea Files

The Karpathy pattern for public sharing:

```
Polish this idea file for public sharing as a Gist.

[PASTE IDEA FILE]

Requirements:
- Abstract should be compelling but honest (no hype)
- Success criteria should be so clear anyone could verify them
- Implementation notes should be context-independent
- Add a "Variations" section: 3 different ways someone might implement this differently
- Add a note: "Implementations welcome — tag me in yours"

Format: clean markdown, no implementation code, pure idea.
```

## Idea Capture (Quick Mode)

For capturing ideas on the fly (30 seconds):

```
I have a quick idea: [ONE SENTENCE]

Extract:
1. Problem solved (1 sentence)
2. Core mechanism (1 sentence)  
3. Minimum viable success criterion (1 testable statement)
4. What I need to figure out before building (top 1-2 questions)

Save as a minimal idea file. I'll flesh it out later.
```

## Idea File Vault Structure

```
ideas/
├── active/         ← being built right now
│   └── llm-wiki.md
├── backlog/        ← solid specs, not started
│   └── autoresearch.md
├── draft/          ← rough, needs more thinking
│   └── neural-output.md
└── archived/       ← built or abandoned, kept for reference
    └── old-idea.md
```

## Workflow

**属于工作流：想法到上线（入口）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 入口（第1步） | 用户有新想法时直接触发 | karpathy-agentic-engineering（开始工程化实现） |

完整链路：idea-files → agentic-engineering → minimalism → supply-chain-hygiene → vibe-to-agentic

## Prompt Contract

```text
Turn my idea into an idea file. Produce: 1) Abstract (2-3 sentences, what and why), 2) Target user (who benefits), 3) Success criteria (how to know it's done — verifiable), 4) Constraints (budget, tech stack, non-goals), 5) Implementation sketch (steps an agent could follow), 6) Open questions (what I haven't decided yet). Format as a single Markdown file ready to share as a Gist.
```

## Verification Checklist

- [ ] 想法文件有明确的 Abstract（不是模糊愿景）
- [ ] 成功标准是可验证的（不是「做得好」）
- [ ] 约束条件写了「绝对不做什么」
- [ ] 实现建议足够具体，让不认识你的 Agent 也能开始
- [ ] Open Questions 列出了你还没决定的部分
- [ ] 整个文件可以直接发 Gist，不需要额外解释
