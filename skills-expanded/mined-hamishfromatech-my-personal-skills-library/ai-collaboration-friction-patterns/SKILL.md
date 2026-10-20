---
name: ai-collaboration-friction-patterns
description: Apply Rahul Garg's five-pattern framework (Knowledge Priming, Design-First Collaboration, Context Anchoring, Encoding Team Standards, Feedback Flywheel) to eliminate the "Frustration Loop" in AI-assisted development and the Lattice open-source framework that operationalizes them as installable infrastructure. Covers the tool-to-teammate reframing, the speed-trap metric correction, the shared-mental-model outcome, the atom/molecule/refiner composability model, and the .lattice/ institutional-memory directory. Use when AI-generated code doesn't fit your codebase, teams are stuck in generate-review-regenerate cycles, first-pass acceptance rates are low, or you need to build reusable AI collaboration scaffolding. NOT for choosing an AI coding tool, evaluating model quality, or single-developer prompt-engineering tips.
---

# AI Collaboration Friction Patterns & the Lattice Framework

## Overview

AI coding assistants are fast but contextless — "junior developers with infinite energy but zero context." The result is the Frustration Loop: generate code, review it, find it doesn't fit, regenerate, review again, give up. Rahul Garg's five-pattern framework (Martin Fowler, Feb–May 2026) reframes the fix: treat AI as a teammate, not a tool, and give it the same scaffolding you'd give a human pair programmer — onboarding, whiteboarding, guardrails, decision persistence, and retrospectives. The Lattice open-source framework operationalizes those patterns as composable installable skills. Together they shift the experience from correcting a tool to collaborating with a capable partner and create a shared mental model that compounds across sessions.

## When to Use

- AI-generated code doesn't align with your codebase conventions, architecture, or stack
- Teams are stuck in the generate → review → "not quite right" → regenerate → give up cycle
- First-pass acceptance rate of AI output is low; review burden exceeds manual-writing time
- Quality of AI output varies depending on which team member is prompting
- Context established early in a conversation is lost as sessions lengthen
- You need to scale senior-developer intuition across the whole team consistently
- You want to build reusable, version-controlled AI collaboration infrastructure (not just tips)
- Adopting or evaluating the Lattice framework for your project

NOT for:
- Choosing which AI coding assistant or model to use
- Evaluating raw model quality or benchmark scores
- Single-developer prompt-engineering one-liners (use context-engineering or vibe-coding)
- The organizational design of human-agent team management (use ai-employee-agent-team-management)
- Spec-driven development discipline broadly (use spec-driven-development-framework)

## Core Process / Workflow

### 1. Diagnose the Frustration Loop

The loop persists because AI assistants default to "the average of the internet" — generic patterns from millions of repos — rather than code that fits a specific team. Symptoms:

| Symptom | What Happens |
|---|---|
| Architecture misalignment | AI uses Express.js when the project uses Fastify; class-based when the codebase is functional |
| Post-generation editing dominates | Time saved by generation consumed by fixing |
| Context loss | Decisions from early in the session forgotten as conversation grows |
| Prompt-quality variance | Output depends on who is prompting, not the task itself |

### 2. Correct the Speed Trap metrics

The metrics teams typically track obscure the real cost. Shift to collaboration-quality metrics:

| Misleading Metric | More Useful Alternative |
|---|---|
| Time to first output | **First-pass acceptance rate** |
| Lines of code generated | **Iteration cycles per task** |
| Tasks completed | **Post-merge rework required** |
| Generation speed | **Review burden compared to manual writing** |

First-pass acceptance is a leading indicator for DORA change-failure rate: misaligned code that ships becomes technical debt.

### 3. Make the Tool-to-Teammate Shift

The reframe that unlocks all five patterns:

| Human Pair Programming | AI Collaboration Equivalent |
|---|---|
| "Let me show you the docs first" | Sharing architectural context before requesting code |
| "Let's sketch this on the whiteboard" | Structured design discussion before implementation |
| "Here's how reviews work here" | Encoding standards into reusable prompts or commands |
| "Let me update the doc with the decision" | Persisting decisions so they survive session boundaries |
| "What did that teach us?" | Systematically capturing what worked and what didn't |

AI needs the same three things a human pair needs: **onboarding** (codebase context), **whiteboarding** (design discussion), **guardrails** (standards applied consistently).

### 4. Apply the Five Patterns

Each pattern mirrors a practice that makes human collaboration effective and addresses a specific failure mode.

#### Pattern 1 — Knowledge Priming (human parallel: onboarding a new hire)
Before asking AI to generate code, share curated context: tech stack with versions, directory structure, naming conventions, examples of existing patterns. This is manual RAG — filling the context window with high-value, project-specific information that overrides generic training data.
- **Failure mode addressed:** AI defaults to generic patterns because it lacks project-specific context.
- **Practical:** Create a `project-priming.md` that the AI reads at session start; keep it current (the document goes stale in ~6 weeks if untouched).

#### Pattern 2 — Design-First Collaboration (human parallel: whiteboarding before coding)
Walk through progressive levels of design before implementation: capabilities → components → interactions → contracts → implementation. Catch misunderstandings before they become bugs.
- **Failure mode addressed:** AI jumps to implementation before understanding requirements, producing code that solves the wrong problem.
- **Practical:** Run a design conversation with the AI before any code request; align on approach like a whiteboard session.

#### Pattern 3 — Context Anchoring (human parallel: updating the doc with decisions)
Maintain a living document per feature that captures decisions, constraints, and current state. This is external memory — anchoring context that would otherwise be lost as conversations grow or sessions end.
- **Failure mode addressed:** AI forgets decisions made earlier in long conversations, leading to contradictions and inconsistency.
- **Practical:** One living doc per feature; update it at every decision point; re-inject into context at each session start.

#### Pattern 4 — Encoding Team Standards (human parallel: what a senior dev does instinctively)
Make tacit knowledge explicit. When defaults exist as artifacts (not intuition), they apply consistently regardless of who is prompting. Senior-developer intuition lives in heads; it doesn't scale.
- **Failure mode addressed:** AI generates technically correct code that violates team expectations, requiring extensive rework.
- **Practical:** Codify conventions as reusable prompts/commands/skills; the senior's judgment becomes a shared artifact.

#### Pattern 5 — Feedback Flywheel (human parallel: retrospectives & continuous learning)
Systematically harvest learnings from AI interactions to improve the other four patterns. When a prompt works, capture it. When AI consistently misunderstands something, add it to priming context. When a failure pattern emerges, add a guardrail. Build institutional knowledge about effective AI collaboration.
- **Failure mode addressed:** Teams make the same mistakes repeatedly without building institutional knowledge.
- **Practical:** A `.lattice/learnings/` directory that accumulates review insights; the next session starts smarter.

### 5. Target the Shared Mental Model

The five patterns compose into a shared mental model between humans and AI:

| Dimension | Pattern That Establishes It |
|---|---|
| Same vocabulary | Knowledge Priming |
| Same architecture vision | Design-First Collaboration |
| Same quality standards | Encoding Team Standards |
| Same decision history | Context Anchoring |
| Same learning trajectory | Feedback Flywheel |

When all five operate, the cognitive load shifts from constant vigilance and correction to expressing intent and refining output. This is the difference between struggling with a tool and collaborating with a capable partner.

### 6. Operationalize with Lattice (installable infrastructure)

The operationalization gap: patterns fail not in understanding but in sustained practice. A team creates a priming document; six weeks later it's stale. Lattice turns the patterns into installable, version-controlled AI skills.

**Three-tier composability model:**

| Tier | What It Is | Solves |
|---|---|---|
| **Atoms** | Independent single-principle skills (clean code, architecture, DDD, secure coding, test quality) + four structural atoms (knowledge-priming, design-first, context-anchoring, collaborative-judgment) | Guardrails |
| **Molecules** | Multi-step workflows that compose atoms (design-blueprint, code-forge) | Orchestration |
| **Refiners** | Guided interviews producing `.lattice/standards/` documents that adapt atom defaults to a team | Customization |

**Three design principles:**
1. **Skills over prompts** — skills live in the repo, change through pull requests, apply the same way for everyone.
2. **Composability over monoliths** — update one atom and every molecule that uses it benefits.
3. **Living context over static config** — review feedback, refiners, and `.lattice/` turn the framework into institutional memory that accrues each cycle.

**The feature lifecycle:**
1. `lattice-init` once per project — suggest refiners, seed `.lattice/`
2. `design-blueprint` — load context, walk design levels, persist an approved blueprint before code
3. `code-forge` — implement against that blueprint and prior learnings, with atoms doing checklist verification
4. `review` — independent pass, severity-ordered findings, insights written to `.lattice/learnings/`
5. The next feature's `code-forge` reads those learnings so the project does not repeat the same mistakes

**Installation:**
```
# In Claude Code:
/plugins marketplace add techygarg/lattice
/plugins install lattice
/reload-plugins

# Or to a skills directory directly:
git clone https://github.com/techygarg/lattice.git
cd lattice
./tools/install.sh /path/to/your/skills/folder
```

Lattice is MIT-licensed, tool-agnostic (Claude Code, Cursor, any skills/instructions-capable tool), markdown-native, backend-focused (expanding to other verticals).

### 7. Trade-offs and Limitations

- Creating and maintaining priming documents requires effort; design-first conversations take longer than immediately requesting code.
- For simple, one-off tasks (a quick utility, a straightforward refactor) the overhead may not be justified — the investment pays off for non-trivial work, especially multi-session or team-coordinated work.
- Learning curve: teams accustomed to AI-as-autocomplete may find structured collaboration unfamiliar; the shift requires deliberate practice.
- Lattice is opinionated (Clean Code, Clean Architecture, DDD, Secure Coding as defaults); use overlay mode (document only what differs) or override mode (replace defaults entirely) to customize.

## A-Tech Application Matrix

### A-Coder
- **Embed the five patterns as first-class features:** a "Project Context" panel (Knowledge Priming), a "Design Mode" before code generation (Design-First), a per-feature "Decision Log" (Context Anchoring), a team-standards configuration layer (Encoding Team Standards), and a "Learnings" feed that surfaces past review insights (Feedback Flywheel).
- **First-pass acceptance rate as a primary metric:** display it in the IDE; track the generate-review-regenerate cycle count; alert when review burden exceeds manual-writing time.
- **Lattice-compatible plugin system:** A-Coder should accept Lattice-style atom/molecule/refiner skills so teams can install community collaboration scaffolding without leaving the IDE.
- **Privacy-first:** all `.lattice/` context, standards, and learnings stay in the local repo; no cloud upload of team conventions.

### Be Practical
- **Curriculum chapter:** "From Frustration Loop to Shared Mental Model: collaborating with AI as a teammate." Teach the five patterns, the metric correction, and the tool-to-teammate shift.
- **Exercise:** Audit a recent AI-assisted task — count iteration cycles, measure first-pass acceptance rate, identify which pattern was missing. Then redo the task with the pattern applied and compare.
- **Frameworks taught:** the five-pattern model, the metric-correction table, the Lattice atom/molecule/refiner composability model.

### Builder's Club
- **Lattice adoption showcase:** members who adopt Lattice (or A-Tech's equivalent) share before/after first-pass acceptance rates and review-burden data.
- **Open-source contribution:** contribute atoms for A-Tech's verticals (privacy-first coding, open-source monetization patterns, local-first architecture) to the Lattice ecosystem.
- **Community challenge:** build a `.lattice/` standards refiner that encodes A-Tech's open-source values as reusable AI collaboration guardrails.

## Anti-Patterns

- **Measuring AI success by generation speed alone** — the Speed Trap; net productivity is questionable when review time exceeds generation time.
- **Expecting AI to produce architecture-aligned code without onboarding** — zero context = generic output = rework.
- **Keeping senior-developer judgment tacit** — intuition in one person's head doesn't scale; encode it as artifacts.
- **Letting context drift across long sessions** — without anchoring, the AI contradicts earlier decisions.
- **Never capturing what worked** — without a feedback flywheel, the team repeats the same mistakes.
- **Treating the five patterns as one-time setup** — they erode without infrastructure; Lattice's insight is that discipline must be installable, not habitual.

## Cross-References

- **`ai-employee-agent-team-management`** (developer-experience-and-flow) — the organizational "tool-to-teammate" shift at the team-management level; this skill is the *pair-programming* level of the same shift.
- **`beyond-vibe-agentic-engineering`** (developer-experience-and-flow) — the maturity arc from vibe coding to disciplined engineering; this skill provides the collaboration scaffolding that makes discipline sustainable.
- **`spec-driven-development-framework`** (ai-agents-and-workflows) — spec-before-code; this skill's Design-First Collaboration pattern is the human-AI-pairing expression of the same principle.
- **`context-engineering` / `context-engineering-production-practice`** (cognitive-science-and-ux) — context curation; Knowledge Priming is manual RAG and Context Anchoring is living-context management.
- **`devex-verification-bottleneck-framework`** (developer-experience-and-flow) — the 3 D's (Design/Documentation/Discovery); Encoding Team Standards and the Lattice skills model operationalize the Design and Documentation D's.
- **`cognitive-offloading-ladder`** (cognitive-science-and-ux) — Margaret-Anne Storey's cognitive debt (loss of shared mental models); this skill's "shared mental model" outcome is the active mitigation of that debt.
- **`agent-friendly-api-documentation-2026`** (developer-experience-and-flow) — writing craft for agent-consumable docs; Knowledge Priming is the reciprocal — making the codebase consumable for the AI collaborator.
- **`developer-experience-flow-state`** (developer-experience-and-flow) — feedback loops, cognitive load, flow state; this skill's metric correction (first-pass acceptance, iteration cycles) feeds that measurement framework.
- **`proactive-ai-intervention-timing`** (developer-experience-and-flow) — when to interrupt; the shared mental model reduces the need for interruption because alignment is pre-established.

## References

- See [references/friction-patterns-evidence-base.md](references/friction-patterns-evidence-base.md) for the full framework extraction (Frustration Loop, Speed Trap, tool-to-teammate shift, five patterns in detail, shared mental model, trade-offs), the Lattice operationalization (atom/molecule/refiner model, design principles, feature lifecycle, installation, composability), and the cross-reference mapping to existing A-Tech skills.