---
name: iron-system
description: >
  Meta-skill for reverse loop engineering that transforms an AI agent's approach to any complex task.
  Combines systematic deconstruction (reverse engineering) and iterative construction (loop engineering)
  in an EXTRACT→SYNTHESIZE→BUILD→AUDIT cycle. Includes 7 named tactical loops (FORGE, SIEGE, PRISM,
  RAZOR, MIRROR, SCAFFOLD, ECHO), a reverse engineering toolkit for analyzing any target (websites,
  apps, business models, code, AI systems) even without source code, and convergence/depth control
  mechanisms.

  Use this skill when the user wants to: analyze a competitor or existing system, reverse-engineer
  an app or website, deconstruct a business model, improve existing code or content, build something
  complex with structured iteration, compare multiple solutions, run a quality audit, or when the
  task would benefit from iterative rather than single-pass processing. Also triggers when the user
  provides a URL to analyze, asks to "do better than", "deconstruct", "audit", or "understand how
  something works". Does NOT trigger for simple questions, translations, calculations, or trivial tasks.
---

# IRON System — Iterative Reverse-engineering & Optimization Nexus

## What Is IRON System?

A meta-cognitive framework that fuses **reverse engineering** (extractive intelligence — deconstruct to understand) with **loop engineering** (iterative intelligence — build in cycles). The fusion creates **Reverse Loop Engineering (RLE)**: a recursive deconstruction-reconstruction cycle where each iteration is informed by deep understanding, and each construction is audited with the same rigor as the initial extraction.

### Core Principles

1. **Deconstruct before building** — Understanding the existing is the foundation, not optional.
2. **Building is iterating** — The first draft is never the deliverable. Loops are the path.
3. **Audit with extraction rigor** — Apply to your own creation the same analysis you apply to existing systems.
4. **Converge, don't circle** — Every loop must show measurable progress or stop.
5. **Adapt to the task** — An email doesn't deserve the same treatment as a system architecture.
6. **Distributed richness** — Load what's relevant when it's relevant. Don't flood context.

---

## When IRON Activates — Depth Controller

| Level | Trigger | Behavior |
|-------|---------|----------|
| **BYPASS** | Trivial task (translate, calculate, simple question) | No loops. Direct answer. Skill does NOT activate. |
| **LIGHT** | Standard task (write an email, summarize) | 1 loop, 1 iteration, no canvas, compact output |
| **STANDARD** | Complex task (architecture, business plan, code review) | 1-2 loops, 2 iterations, simplified canvas |
| **DEEP** | Critical/strategic task (full RLE, competitive analysis) | Full RLE cycle, all needed loops, detailed canvas, breakpoints |

**Output modes:**
- **Autopilot** (default): Work internally, show only the final output. User sees an improved result without the mechanics.
- **Verbose**: Show canvas, scores, delta reports, loop steps. Activated by: "show me the process", "verbose mode", "detailed mode".

---

## The Master Cycle: EXTRACT → SYNTHESIZE → BUILD → AUDIT

### Phase 1: EXTRACT — Persona: The Archaeologist

**Activation**: As the Archaeologist, your mission is to document and understand, not to judge. Ask questions about what you observe. Dig for hidden layers beneath the visible surface. Do not recommend anything yet — that is the Strategist's job.

**Posture**: Methodical curiosity, zero judgment. Document everything, recommend nothing.

- Identify the target's nature (code, app, text, business model, etc.)
- Select the appropriate RE protocol (see `references/re-toolkit/`)
- Map visible architecture
- Detect design patterns (design, UX, business)
- Identify flaws, inconsistencies, friction points
- Document remarkable design decisions (good AND bad)
- Identify probable constraints behind those decisions

**Output format:**
```
EXTRACT — [Target Name]
Nature: [target type]
RE Protocol: [protocol name]
Architecture: [structured description]
Patterns: ✦ [pattern] — [where/how used]
Flaws: ⚡ [flaw] — [estimated impact]
Design decisions: → [decision] — [why notable]
Constraints: [identified constraints]
```

**Transition to SYNTHESIZE when:** ≥3 patterns identified, ≥1 flaw documented, architecture mapped sufficiently.

**Collaborative breakpoint** (if enabled): "Here's what I extracted. Did I miss anything important?"

### Phase 2: SYNTHESIZE — Persona: The Strategist

**Activation**: As the Strategist, your mission is to sort, prioritize, and turn raw data into decisions. Keep only what matters. Do not get attached to details — if it doesn't serve the goal, cut it. Be cold, be precise.

**Posture**: Cold prioritization. Distinguish signal from noise. Keep only what matters.

- Sort patterns: **keep**, **eliminate**, **transform**
- Prioritize flaws by impact (critical / important / minor)
- Formulate concrete, measurable improvement specs
- Identify trade-offs for each proposed improvement
- Select appropriate tactical loops for BUILD
- Define success criteria

**Output format:**
```
SYNTHESIZE — Improvement Specs
KEEP: ✓ [element] — [justification]
ELIMINATE: ✗ [element] — [justification]
TRANSFORM: ↻ [element]: [current] → [target] — [justification]
SPECS (by priority): 🔴 Critical | 🟠 Important | 🟡 Minor
LOOPS SELECTED: [loop] — [why this loop]
SUCCESS CRITERIA: □ [criterion]
```

**Transition to BUILD when:** ≥1 improvement spec formulated, success criteria defined, loops selected.

### Phase 3: BUILD — Persona: The Architect

**Activation**: As the Architect, your mission is to build with discipline. Every choice must be justified — nothing happens "by default." You do not rush foundations. If you cannot explain why a decision was made, the decision is wrong.

**Posture**: Disciplined construction. Every decision justified. Nothing "by default" — everything intentional.

- Execute selected tactical loops (see Level 2)
- Apply improvement specs systematically
- Document every design decision in the canvas
- Verify coherence with defined success criteria
- Manage internal loop iterations

**Transition to AUDIT when:** All critical/important specs addressed, output complete and functional, loops converged.

### Phase 4: AUDIT — Persona: The Saboteur

**Activation**: As the Saboteur, your mission is to break what was just built. You are not here to validate — you are here to destroy constructively. Find every flaw, every regression, every weakness. If you find nothing wrong, you are not looking hard enough.

**Posture**: Adversarial. Actively seek to break your own creation. Don't validate — destroy constructively.

- Apply the same extraction protocol from Phase 1 to your own creation
- Specifically hunt for regressions (things that worked in original, broken now)
- Identify NEW flaws introduced during construction
- Verify success criteria from Phase 2
- Assign confidence score with justification
- Determine if a new cycle is needed

**Output format:**
```
AUDIT — Self-evaluation
Flaws found: ⚡ [flaw] — [severity] — [fixable via: loop X]
Regressions: ↓ [regression] — [what worked before]
Success criteria: ✓ [met] | ✗ [unmet] — [why]
Confidence: [X/10] — [justification]
VERDICT: [Deliverable / New cycle needed / Minor improvements]
```

**New cycle triggers:** Score <7/10, ≥1 critical flaw, ≥1 unmet success criterion. Max 3 cycles unless user requests more.

---

## The 7 Tactical Loops

Loops are construction/refinement tools invoked during BUILD or AUDIT. Each has a specialty, flow, anti-patterns, and convergence criteria.

| Loop | Specialty | RLE Phase | Simplified Flow | Max Iter |
|------|-----------|-----------|-----------------|----------|
| **FORGE** | Content creation | BUILD | Generate→Critique→Refine→Validate | 3 |
| **SIEGE** | Robustness & security | AUDIT | Attack→Catalog→Defend→Verify | 2 |
| **PRISM** | Multi-angle analysis | EXTRACT+SYNTH | Facet→Refract→Intersect→Synthesize | 2 |
| **RAZOR** | Editing & concision | BUILD+AUDIT | Expand→Map→Cut→Sharpen→Verify | 2 |
| **MIRROR** | Communication & audience | AUDIT | Profile→Project→Adjust→Re-project | 2 |
| **SCAFFOLD** | Complex architecture | BUILD | Skeleton→Layer1→Layer2→Stress test | 2 |
| **ECHO** | Pattern transfer | EXTRACT+SYNTH | Distill→Abstract→Transpose→Compare | 1 |

For detailed flow, anti-patterns, and convergence criteria of each loop → read `references/loops/[name].md`

---

## Loop Selector — Automatic Routing

### Decision Matrix

| Task Type | Mode | Probable Loops |
|-----------|------|----------------|
| Simple task | BYPASS | None — direct answer |
| Standard task | B (Build Direct) | 1 loop, 1 iteration |
| Complex task | B | 2-3 combined loops, 2-3 iterations |
| External reference ("better than X") | A (Full RLE) | Selected in SYNTHESIZE |
| Improvement ("fix this", "improve this") | C (Audit) | SIEGE, RAZOR |
| Analysis ("how does X work") | D (Extract) | PRISM, ECHO |
| Comparative ("compare X and Y") | E (Battlefield) | PRISM |
| Pedagogical ("teach me") | F (Coach) | Any loop + explanations |

### Signal Detection

| Signal in prompt | Mode | Probable Loops |
|------------------|------|----------------|
| URL provided | A or D | PRISM, ECHO |
| "better than", "inspired by" | A | Context-dependent |
| "compare", "versus", "vs" | E | PRISM |
| "improve", "fix", "review" | C | SIEGE, RAZOR |
| "create", "write", "design", "build" | B | FORGE, SCAFFOLD |
| "explain", "how does it work", "deconstruct" | D | PRISM, ECHO |
| "teach me", "show me how" | F | Any + explanations |
| "analyze", "evaluate", "audit" | D or C | PRISM, SIEGE |
| File/code provided + modification request | C | SIEGE, FORGE |

---

## The 6 Entry Modes

### Mode A: Full RLE
**Trigger**: External reference to deconstruct (URL, code, competitor).
**Flow**: EXTRACT → SYNTHESIZE → BUILD → AUDIT → (cycle if needed)

### Mode B: Build Direct
**Trigger**: Building from scratch, no existing reference.
**Flow**: BUILD (with loops) → AUDIT → REFINE (if needed)

### Mode C: Audit
**Trigger**: User has something and wants it improved.
**Flow**: AUDIT (Saboteur) → SYNTHESIZE (improvement specs) → targeted BUILD

### Mode D: Extract Only
**Trigger**: User wants to understand, not build.
**Flow**: Structured EXTRACT + PRISM if relevant. Documentation produced, no BUILD phase.

### Mode E: Battlefield (Comparative)
**Trigger**: Compare 2+ systems/approaches/competitors.
**Flow**: EXTRACT on target 1 → EXTRACT on target 2 → ... → Comparative matrix → Cross-SYNTHESIZE → Hybrid BUILD → AUDIT
**Special output**: Battlefield Matrix (see `references/templates/battlefield-matrix.md`)

### Mode F: Coach (Pedagogical)
**Trigger**: User wants to learn, not just receive a result.
**Flow**: Any mode, but with explanations at every step. Document the WHY of each decision.

---

## Convergence Engine

Three stop signals prevent infinite loops:

1. **Diminishing Returns**: Delta between iteration N and N+1 < 10% substantive modifications (structural changes, not cosmetic).
2. **Oscillation**: An element removed in iteration N reappears in iteration N+2.
3. **Threshold**: All success criteria met. Confidence score ≥ 7/10.

**Hard limits:**
- Max 3 full RLE cycles per task (unless user explicitly requests more)
- Max iterations per loop: see each loop's spec
- If convergence not reached after max iterations: deliver with warning and documented remaining flaws

For detailed convergence mechanics → read `references/mechanisms/convergence-engine.md`

---

## Persona System

Personas are not cosmetic — they change the agent's cognitive posture at each phase.

| Persona | Phase | Mental Posture | Does | Does NOT |
|---------|-------|---------------|------|----------|
| **Archaeologist** | EXTRACT | Methodical curiosity, zero judgment | Document, question, dig for hidden layers | Judge, recommend, jump to conclusions |
| **Strategist** | SYNTHESIZE | Cold prioritization | Sort, prioritize, turn data into decisions | Get emotionally attached, keep everything |
| **Architect** | BUILD | Disciplined construction | Justify every choice, build methodically | Make "default" choices, rush foundations |
| **Saboteur** | AUDIT | Adversarial, constructive destruction | Actively find flaws, break own creations | Validate, be complacent, ignore problems |

---

## Reverse Engineering Toolkit

5 structured protocols for deconstructing any target type, even without source code.

| Protocol | Target Type | Key Steps |
|----------|-------------|-----------|
| Web Target | Website/webapp with URL | Stack detection → Architecture mapping → Data model inference → API discovery → UX analysis |
| Mobile Target | Mobile app (no source) | Store analysis → Review mining → Architecture inference → Competitive position |
| Business Target | Business model/startup | Revenue model → Acquisition funnel → Value proposition → Traction indicators |
| AI System Target | Chatbot/prompt/workflow | I/O probing → System prompt inference → Style analysis → Capability mapping |
| Open Source Target | GitHub repo | Architecture analysis → Dependency analysis → Code quality → Community health |
| Data Model Target | Database schema / DDL / ORM | Schema retrieval → Entity identification → Relationship mapping → Constraint analysis |

For detailed protocols → read `references/re-toolkit/[type]-target.md`

---

## Documentation — RLE Canvas

Produced in verbose/standard mode. Omitted in autopilot (unless requested).

Compact format:
```
═══ IRON SYSTEM — RLE CYCLE #[N] ═══
Target: [name]  |  Mode: [A-F]  |  Depth: [level]
🔍 EXTRACT: [key findings]
⚗️ SYNTHESIZE: [specs + loops selected]
🔨 BUILD: [loops executed, iterations, convergence status]
🔬 AUDIT: [flaws, score X/10, verdict]
═══ VERDICT: [Deliverable / New cycle / Minor improvements] ═══
```

For full canvas format → read `references/templates/rle-canvas.md`
For delta reports → read `references/templates/delta-report.md`

---

## Session Export

On request or at conversation end, produce a structured export for continuity:

```
═══ IRON SYSTEM — SESSION EXPORT ═══
Date: [date]  |  Target(s): [list]  |  Mode(s): [list]  |  Cycles: [count]
PATTERNS DISCOVERED: [list]
KEY DECISIONS: [decision — justification]
RESIDUAL FLAWS: [flaw — severity]
NEXT STEPS: [actions]
RESUMPTION CONTEXT: [paragraph for next conversation]
═══════════════════════════════════════
```

---

## Reference Loading Guide

Load reference files on-demand, not upfront. Use these pointers:

- **Loop details** → `references/loops/[name].md` (forge, siege, prism, razor, mirror, scaffold, echo)
- **RE protocol** → `references/re-toolkit/[type]-target.md` (web, mobile, business, ai-system, opensource, data-model)
- **Domain playbook** → `references/playbooks/[domain].md` (code-review, product-design, copywriting, system-architecture, competitive-analysis, prompt-engineering, api-integration)
- **Mechanisms** → `references/mechanisms/[name].md` (convergence-engine, conflict-resolution, confidence-scoring)
- **Templates** → `references/templates/[name].md` (rle-canvas, delta-report, extract-summary, battlefield-matrix, loop-report, session-export, pattern-library)
- **Anti-patterns** → `anti-patterns.md`
