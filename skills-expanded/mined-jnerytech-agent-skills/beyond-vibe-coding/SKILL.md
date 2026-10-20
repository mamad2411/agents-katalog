---
name: beyond-vibe-coding
description: "Knowledge base from \"Beyond Vibe Coding: From Coding by Instinct to Coding with Purpose\" by Addy Osmani (O'Reilly, 2025). Use when applying Osmani's frameworks for the vibe coding ↔ AI-assisted engineering spectrum, the 70% problem, prompt engineering for code (few-shot, CoT, role, ReAct), reviewing/refining/owning AI-generated code, AI prototyping to production, security and maintainability of AI code, ethics/IP of generated code, and autonomous background coding agents — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Beyond Vibe Coding
**Author**: Addy Osmani | **Publisher**: O'Reilly (2025) | **Pages**: ~445 | **Chapters**: 11 | **Generated**: 2026-10-13

## How to Use This Skill

- **Without arguments** — load the core frameworks below
- **With a topic** — ask about `70% problem`, `few-shot`, `majority solution`, `package hallucination`, `background agents`; I find and read the relevant chapter
- **With chapter** — ask for `ch05` to load that chapter file
- **Browse** — ask "what chapters do you have?" for the full index
- **Decide fast** — [cheatsheet.md](cheatsheet.md) holds the author's decision rules and thresholds

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 1. The AI coding spectrum: vibe coding ↔ AI-assisted engineering (ch01)
- **Vibe coding** (Karpathy: "fully give in to the vibes") is prompt-first and exploratory. It optimizes **short-term velocity**. **AI-assisted engineering** weaves AI into every SDLC phase under clear constraints, with the human in the driver's seat, and optimizes **sustained velocity**. They're a spectrum you blend; "the art lies in recognizing when to transition".
- Vibe code ideas, demos, hackathons, throwaway scripts. Use **plan-first** (mini-PRD → targeted prompts → review → integrate) for code that lives for years. Use AI only as explainer/reviewer for novel algorithms, mission-critical domains, legacy, and low-level or performance code.
- **Programming with intent**: state *what*, not *how*. "The prompt becomes your new unit of thought."
- **Knowledge paradox** (Preface): seniors use AI to accelerate what they already know, and juniors use it to learn what to do. AI is "a very eager junior developer" that needs constant supervision. Developers become **curators and editors** of AI output.

### 2. The 70% problem (ch03, ch04)
- AI quickly delivers ~70% of a solution (boilerplate, routine, patterned code). The **last 30%** (edge cases, architecture, maintainability, production readiness) has diminishing returns and needs human expertise. In Brooks's terms, AI absorbs **accidental complexity** and the **essential complexity** stays yours.
- Failure patterns: **two steps back** (each fix breaks something else; stop prompting and understand the root cause), **house of cards code**, the **demo-quality trap**, and the **lost art of polish**.
- Users split into **Bootstrappers** (zero → MVP) and **Iterators** (daily completion, refactoring, tests). Seniors constantly refactor AI output, add error and edge-case handling, strengthen types, and question the architecture.
- Pick a workflow: **AI as first drafter** (team features), **AI as pair programmer** (new session per task, frequent commits), or **AI as validator** (humans write; AI scans, tests, suggests).
- **Golden Rules of Vibe Coding**: be specific; validate against intent; treat AI as a supervised junior; coordinate up front; **isolate AI changes in separate commits**; review all code; **don't merge code you don't understand**; document (ADRs); share prompts; reflect and iterate.
- **The Human 30%** (ch04): AI generates *code*, humans own *engineering*. Seniors act as **architect and editor in chief**: they specify, then review ("AI is the fast typer, you're the brain"). Use **CHOP** (chat-oriented programming) for big refactors. Take **AI-free days** against skill atrophy, debug yourself before asking AI, and treat a prompt that keeps failing as a sign *you* haven't understood the problem.

### 3. The art of the prompt (ch02)
- Write prompts like a spec writer: the AI knows nothing beyond the prompt. Name the language and environment, the output scope, requirements and constraints, and the output format. Avoid ambiguous references ("the above code"). For bugs, give the exact error plus the intended behavior.
- **Iterative refinement**: prompt → output → review → refine, with small, specific changes. When the AI fundamentally misunderstood, rephrase from scratch.
- **Toolbox**: zero-shot; **few-shot** (2–5 examples; costs context window); **chain-of-thought** (tricky logic); **role** (steer depth and tone); **contextual** (paste docs, API snippets); **metaprompting** (format, order, exclusions); **self-consistency** (sample, trust consensus); **ReAct** (reason ↔ act with tools). These compose.
- Antipatterns: the **vague prompt** (fits dozens of scenarios), the **overloaded prompt** (several "and"s → split it), **vague success criteria** ("faster" instead of "linear time, currently quadratic"), and **missing the question**.

### 4. Review, refine, own generated code (ch05)
- **Intent-to-implementation check** before running: trace a typical input, confirm each requirement, flag unrequested extras, check edge cases, and find where the AI picked an interpretation of an ambiguous prompt.
- **Majority solution effect**: AI emits the most common or simplest solution from its training data, such as a linear search where binary search fits, or a global variable. "Most common doesn't mean most appropriate — the tailoring is your job."
- Review "as if an intern wrote it and left for the day". Telltale smells include redundant comments, list lookups instead of a set, outdated APIs, and unrequested logging or parameters.
- **Six-step debugging**: reproduce → locate → check prompt vs. code → AI as colleague → fix (by hand if obvious, else "input X, expected Y, got Z") → retest. **Six-step refactoring**: lint → naming and structure → remove extras → document → optimize → simplify, "until no one can tell an AI wrote it". Tests lock down behavior, and ownership means you understand it, trust it, and test it.

### 5. Prototype fast, then switch gears (ch06, ch07)
- Choose tools by **fidelity vs. control**: screenshot-to-code and full-app builders give fidelity, AI IDEs give control. Expect an **80% prototype** that lacks security, performance, error handling, and architecture.
- Keep a one-sentence **North Star**, stub non-core features, and log every shortcut as a TODO. To go to production: architecture → errors and edge cases → performance → security → docs → tests → replace hacks.
- For web apps, **decide the architecture yourself** before scaffolding. Specify the API response shape for both sides, because separate generation drifts. Put the real schema and integrity rules (e.g., `ON DELETE CASCADE`) in every DB prompt. Hand boilerplate to AI and write novel logic yourself. AI proficiency tracks how well the stack is represented in training data, so test niche stacks with small tasks first.

### 6. Security, maintainability, reliability (ch08)
- AI replicates insecure public patterns: hard-coded secrets, concatenated SQL, XSS, broken authN/authZ (no owner check, **user enumeration**, **timing attacks**), insecure defaults (`verify=false`, CORS `*`, MD5), error leakage, and **package hallucination** (verify that a package exists before installing it). 25–33% of Copilot code had potential CWEs.
- "**AI-accelerated development, human-accelerated security**": run SAST in CI, use a separate AI as a reviewer (input, never clearance), work through a human checklist, fuzz, write security unit tests, and **cite current standards to beat the training cutoff**.
- Testing: property-based, load, error-injection, and integration contract tests (they catch **assumption mismatch**). Maintainability: alternate generation and **hardening sprints** to avoid a big ball of mud, and profile before optimizing (N+1, O(n²)). Deploy with CI/CD, canary (~5%) plus rollback, **shadow testing**, feature flags, observability, and postmortems.

### 7. Ethics and IP (ch09)
- Code is copyrighted by default, so open source ≠ public domain. Purely AI output isn't copyrightable (human authorship requirement). Watch for **derivative work risk**.
- Near-verbatim output → search for it, then attribute, rewrite, or drop it ("**when in doubt, leave it out**"). Never put GPL/AGPL into a closed product. Keep PII out of prompts and use synthetic data instead. Watch for proxy variables (zip code → race). **Golden rules for responsible AI**: human in the loop, own your code, privacy and consent, compliance, culture, guardrails, documented decisions, active bias prevention.

### 8. Autonomous background agents and the future (ch10, ch11)
- Agents run **plan → execute → verify → report** in an ephemeral sandbox and return a PR. Copilot (synchronous, microtask) vs. autopilot (asynchronous, project-level). Exploit the **generator/reviewer asymmetry**: humans specify and review.
- Delegate **well-defined, encapsulated, measurable** tasks (coverage, dependency bumps, bulk refactors). Review the **plan as a quality gate**. If the sandbox can't run tests, fix it first. Give parallel agents disjoint scopes.
- Named risks: **coherent incorrectness**, **environmental drift**, the **async coordination paradox**, the **sunk-cost dilemma** on 80%-right PRs, and an amplified review bottleneck.
- Future (ch11): developers orchestrate and verify, agents execute. Expect **intelligent checkpointing**, an agent inbox, and the human gap narrowing from 30% to maybe 5–10%, but never zero. For **independent verification**, humans write tests for agent code and check AI-written assertions against the requirement, not the current output.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-what-is-vibe-coding.md) | Introduction: What Is Vibe Coding? (+ Preface) | AI coding spectrum, plan-first, programming with intent, knowledge paradox, transition points |
| [ch02](chapters/ch02-art-of-the-prompt.md) | The Art of the Prompt | Specificity, iterative refinement, few-shot/CoT/role/metaprompting/ReAct, prompt antipatterns |
| [ch03](chapters/ch03-the-70-percent-problem.md) | The 70% Problem | 70/30 split, bootstrappers vs. iterators, two steps back, first drafter/pair/validator, Golden Rules |
| [ch04](chapters/ch04-beyond-the-70-percent.md) | Beyond the 70%: Maximizing Human Contribution | Human 30%, architect & editor in chief, CHOP, AI-free day, advice by seniority |
| [ch05](chapters/ch05-understanding-generated-code.md) | Understanding Generated Code: Review, Refine, Own | Intent check, majority solution effect, six-step debugging/refactoring |
| [ch06](chapters/ch06-ai-driven-prototyping.md) | AI-Driven Prototyping | Fidelity vs. control, 80% prototype, North Star, prototype → production |
| [ch07](chapters/ch07-building-web-apps-with-ai.md) | Building Web Applications with AI | Scaffold by intent, API contracts, DB integrity prompts, model proficiency per stack |
| [ch08](chapters/ch08-security-maintainability-reliability.md) | Security, Maintainability, and Reliability | AI vulnerability list, audit toolkit, property-based/shadow testing, hardening sprints, canary |
| [ch09](chapters/ch09-ethical-implications.md) | The Ethical Implications of Vibe Coding | IP/licensing, attribute-or-rewrite, bias, responsible AI golden rules & checklist |
| [ch10](chapters/ch10-autonomous-background-agents.md) | Autonomous Background Coding Agents | Plan→execute→verify→report, copilot vs. autopilot, plan-gate, coherent incorrectness |
| [ch11](chapters/ch11-beyond-code-generation.md) | Beyond Code Generation: The Future | AI in testing/maintenance, vibe design, intelligent checkpointing, layering NL over code |

## Topic Index

- **70% problem / last 30%** → ch03, ch04, ch01, ch11
- **Accidental vs. essential complexity** → ch03
- **Agent inbox / intelligent checkpointing** → ch11
- **AI as first drafter / pair programmer / validator** → ch03
- **AI-free day / skill atrophy** → ch04, ch03
- **API contract (frontend/backend)** → ch07
- **Architect and editor in chief** → ch04
- **Attribution / licensing / GPL / copyright** → ch09, ch05
- **Background coding agents** → ch10, ch11
- **Bias, fairness, proxy variables** → ch09
- **Bootstrappers vs. iterators** → ch03
- **Canary, blue-green, shadow testing, feature flags** → ch08
- **Chain-of-thought / few-shot / role / metaprompting / ReAct / self-consistency** → ch02
- **CHOP (chat-oriented programming)** → ch04
- **Coherent incorrectness / environmental drift / async coordination paradox** → ch10
- **Commit isolation / [AI] tags** → ch03
- **Copilot vs. autopilot** → ch10
- **Database prompts, ORM, cascade delete, indexes** → ch07
- **Debugging with AI (six steps, bug-report prompt, rubber duck)** → ch05, ch02
- **Demo-quality trap / house of cards code / two steps back** → ch03, ch01
- **Fidelity vs. control / screenshot-to-code** → ch06
- **Golden Rules of Vibe Coding** → ch03
- **Golden rules for responsible AI / ethics checklist** → ch09
- **Hardening sprint / big ball of mud** → ch08
- **Intent-to-implementation check** → ch05
- **Knowledge paradox** → ch01, ch03
- **Majority solution effect** → ch05
- **Model choice / tool landscape** → ch01
- **Multi-model orchestration** → ch10
- **Natural-language programming / layering** → ch11
- **Package hallucination** → ch08
- **Performance (N+1, profiling)** → ch08, ch07
- **Plan-first development / spectrum** → ch01
- **Privacy, PII, synthetic data, consent** → ch09
- **Project management with AI / vibe design / UX** → ch11
- **Prompt antipatterns** → ch02
- **Prototype to production / 80% prototype / North Star** → ch06
- **Refactoring AI code** → ch05, ch08
- **Security vulnerabilities (SQLi, XSS, auth, secrets, defaults)** → ch08, ch06
- **Senior / midlevel / junior developer advice** → ch04
- **Testing AI code (unit, property-based, integration, E2E)** → ch08, ch05, ch07, ch11
- **Training cutoff** → ch08
- **User enumeration / timing attacks** → ch08
- **Vibe coding (definition)** → ch01

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and patterns
- [cheatsheet.md](cheatsheet.md) — decision rules, tells, thresholds

---

## Scope & Limits

This skill covers the book's content only (2025 edition). The tool and model landscape (Copilot, Cursor, Windsurf, Cline, v0, Lovable, Bolt, Codex, Jules, Devin) dates fast, so verify current capabilities before relying on them. For governed enterprise agentic workflows, combine with `enterprise-vibe-coding`.
