---
name: outer-loop-harness-framework
description: Apply the three production outer-loop agentic coding harnesses (RPI, BMAD, SPARC) and the seven-dimensional framework selection model to move agentic coding from impressive demos to production-ready enterprise software. Covers brownfield-vs-greenfield selection, context engineering discipline, the 35-minute task half-life, the harness-readiness hierarchy, and enterprise vs. structured vs. IDE tool selection. Use when choosing an agentic coding methodology for a team, planning a brownfield AI rollout, structuring multi-agent development workflows, or diagnosing why agentic coding underperforms in production. NOT for single-prompt tasks, individual autocomplete tuning, or greenfield-only contexts.
---

# Outer-Loop Harness Framework: RPI, BMAD, SPARC and the Selection Model

## The Core Finding

The conventional wisdom says certain frameworks excel at legacy code (brownfield) while others dominate new development (greenfield). The data tells a different story:

**All frameworks perform substantially better on greenfield projects — 20–35% better.** SPARC shows the strongest greenfield optimization. But the real story isn't picking the "right" framework. Brownfield success depends far more on **context engineering discipline** than framework choice. When AI agents tackle existing commercial codebases, performance drops dramatically — yet practitioners using rigorous context engineering have achieved production-ready results on 300,000-line legacy systems.

The gap is addressable, but requires investment, discipline, and matching framework capabilities to specific project characteristics.

## The Three Frameworks

### RPI (Research-Plan-Implement)

A practitioner methodology (not a product) that prevents agents from jumping straight to code.

**Three phases:**
- **Research** — Forces comprehensive understanding through interrogation rather than assumptions. The agent must ask questions, read relevant files, and surface unknowns before proposing anything.
- **Plan** — Creates detailed blueprints with explicit module boundaries, dependency mapping, and verification criteria.
- **Implement** — Executes step-by-step with validation gates at each phase transition.

**Best for:** Complex multi-component systems, repository-level generation, high-stakes production systems.
**Reality check:** Helps substantially with brownfield but doesn't solve it. Success still requires context engineering discipline. Orchestration platforms (e.g., CodeLayer) implement RPI and other context engineering techniques.

**Key insight:** A single misunderstanding during the Research phase can lead to thousands of erroneous lines of code. Time spent on research and planning delivers exponentially greater returns than focusing solely on code implementation.

### BMAD™ (Breakthrough Method for Agile AI-Driven Development)

Treats AI agents as version-controlled code artifacts with "hyper-detailed development stories" that guarantee zero context loss.

**Key features:**
- Explicitly supports brownfield workflows with mandatory **Test Architect** involvement for legacy changes.
- Agent-as-code standardization: agents defined as version-controlled artifacts with reproducible behavior.
- Hyper-detailed stories eliminate the context-loss problem that plagues ad-hoc prompting.

**Best for:** Medium-high complexity projects requiring consistency, microservices architectures, teams wanting agent-as-code standardization.
**Creator's admission:** "Works best for greenfield and dedicated microservices. Brownfield requires heavy customization."

### SPARC (Specification, Pseudocode, Architecture, Refinement, Completion)

A comprehensive five-phase methodology with the strongest greenfield optimization.

**Five phases:**
1. **Specification** — Start from detailed specifications (what, why, constraints).
2. **Pseudocode** — Design the algorithmic logic before any real code.
3. **Architecture** — Design the system architecture from scratch.
4. **Refinement** — Iteratively refine through rapid prototyping.
5. **Completion** — Final implementation with verification.

**Best for:** New applications where comprehensive planning and clean architecture provide maximum benefit.
**Validation:** Adrian Cockcroft (Netflix/AWS veteran) used it to build an iOS app in Swift — a language he didn't know — with autonomous agent handling of UX, code, review, and refactoring.

## The Seven Dimensions That Matter More Than Brownfield vs. Greenfield

The simple brownfield/greenfield binary is insufficient. Seven dimensions matter more:

### 1. Codebase Size & Complexity
- **Small (<10K lines):** Direct LLM interaction works fine — use plan mode in your preferred tool before generating code.
- **Medium (10–100K lines):** Structured approaches show clear ROI.
- **Large (>100K lines):** Context engineering becomes mandatory infrastructure.

### 2. Tech Stack Maturity
Python dominates AI training data, leading to strongest performance. Mileage varies significantly by language ecosystem. SWE-PolyBench shows repository-specific difficulty ranging from <10% to >50% resolution rates.

### 3. Team Size & Structure
- **Solo/small teams:** Lightweight tools (Cursor, VS Code, Aider).
- **Enterprise teams:** Governance platforms (GitHub Agent HQ).

### 4. Development Velocity Requirements
The temporal dimension: startups report "diminished returns after 18 months" as codebases mature from greenfield to brownfield. This transition requires proactive investment in documentation and architectural clarity.

### 5. Cost Management
Context engineering emphasizes keeping **context window utilization under 40%.** Strategic model routing — using smaller models for simple tasks, reserving frontier models for architectural decisions — can reduce costs **95%+.**

### 6. Security & Compliance
In fintech or healthtech, the shift from non-deterministic AI code to deterministic execution paths enables compliance teams to audit automation before deployment.

### 7. The Task Half-Life Finding
AI agents perform best on tasks requiring approximately **35 minutes of human time. Doubling task duration quadruples failure rate.** Task decomposition into 30–40 minute chunks maximizes success regardless of framework.

This is the single most actionable finding: **decompose every agentic task into 35-minute-or-less chunks.** The failure rate is exponential, not linear — a 70-minute task doesn't fail twice as often, it fails four times as often.

## Framework Selection Guide

### Choose IDE tools (Cursor, Aider, Windsurf) when:
- Greenfield projects with small teams (1–3 devs)
- Relatively simple requirements
- Quick setup and iteration needed
- 80% of value with 20% of complexity

### Choose structured methodologies (BMAD, SPARC, RPI-based) when:
- Medium-high complexity projects
- Need consistency across teams
- Long-term maintenance expected
- Multiple repositories or microservices
- Brownfield/legacy requiring systematic approaches

### Choose enterprise solutions (Azure AI Foundry, Factory.ai, GitHub Agent HQ) when:
- Enterprise-scale deployment
- Governance and security controls required (note: this is a very immature space; controls are still lacking)
- Multiple teams coordinating
- Compliance requirements
- Centralized observability needed

### Mandate context engineering methodology when:
- Codebases >100K lines
- Complex architectural dependencies
- High-stakes production changes
- Production-ready quality required immediately

## The Context Engineering Hierarchy of Effort

The hierarchy of effort matters profoundly. Time spent on research and planning delivers **exponentially greater returns** than focusing solely on code implementation.

**The three-phase approach that achieved 300K-line brownfield success:**
1. **Structured research files** — comprehensive interrogation of the codebase before any code generation.
2. **Comprehensive planning** — detailed blueprints with module boundaries and verification criteria.
3. **Context utilization under 40%** — keeping the context window focused, not overloaded.

Result: a practitioner fixed a bug in a 300,000-line Rust codebase and completed 35,000 lines of WebAssembly support in 7 hours using this approach.

## Implementation Advice

### For Greenfield Projects
- Establish structure early. Define conventions from inception.
- Create architectural documentation before code accumulates.
- Set up rules files immediately.
- **Don't let it become brownfield through neglect.**

### For Brownfield Projects
- **Documentation first.**
- Start with small, well-defined tasks — feature flag removal, incident debugging, focused refactoring — before attempting large-scale changes.
- The BMAD brownfield workflow or rigorous context engineering provide proven structures.
- Run the harness-readiness checklist (see `harness-maturity-matrix`): modularization, boundary enforcement, test coverage.

### For Team Adoption
- Standardize on methodology, not just tools.
- Invest in prompt engineering training.
- Establish shared instruction files.
- Set up governance gates.
- Measure ROI through pilots.
- **Expect 3–6 month learning curves before peak productivity.**

### Universal Best Practices
- Maintain human-in-the-loop gates at phase transitions.
- Review research and implementation plans carefully, not just code.
- Keep context management disciplined (under 40% utilization).
- Update rules files as living documents.

## The Strategic Shift

We're witnessing a fundamental role transformation. Developers are becoming architects, quality gatekeepers, and strategic decision-makers. The frameworks succeeding provide structured workflows maintaining human oversight while enabling meaningful agent autonomy.

**The vertical-deployment insight:** A leading firm modernizing 400 legacy software pieces elevated humans to supervisory roles overseeing AI agent squads. Separate squads handled implementation, code review, and testing. This vertical, function-specific deployment delivered significantly higher impact than horizontal enterprise-wide copilots.

**The adoption gap:** Fewer than 10% of enterprise pilots make it past pilot stage due to organizational barriers.

**The value relocation:** Value is shifting from framework selection to domain-specific customization. As "Harness as a Service" (HaaS) emerges, competitive advantage comes from sophisticated prompts, tools, context, and institutional knowledge repositories — comprehensive rules files, architectural documentation, validated workflows, measured best practices. These assets compound value over time and transfer across framework changes.

## What to Measure

- Code review time and friction
- Iteration cycles for acceptable quality
- Test coverage and defect rates
- Generated code acceptance rates
- Technical debt accumulation rates
- **Task decomposition adherence** (are tasks staying under the 35-minute half-life?)
- **Context window utilization** (is it under 40%?)
- **Research-to-implementation time ratio** (is research getting its exponential-return share?)

Capture failed approaches and successful patterns systematically. Build learning loops. Structured approaches like BMAD and SPARC excel partly because they enforce this discipline through their methodologies.

## A-Tech Applications

### A-Coder
- **Framework integration:** Support RPI, BMAD, and SPARC as selectable workflow modes within the IDE; auto-route to the appropriate framework based on the seven-dimensional project profile.
- **Task half-life enforcement:** A built-in task-decomposition advisor that flags tasks exceeding 35 minutes and suggests decomposition into 30–40 minute chunks.
- **Context utilization monitor:** Real-time context-window utilization gauge with the 40% threshold as a visual guardrail.
- **Research-first default:** The RPI pattern as the default for brownfield repos — A-Coder refuses to generate code until a research file is produced and reviewed.
- **Brownfield harness-readiness:** Built-in modularization audit, boundary-direction check, and coverage-gap map (from `harness-maturity-matrix`).
- **Vertical-deployment support:** Agent-squad architecture (implementation squad, review squad, testing squad) as a first-class workflow pattern.

### Be Practical
- **Curriculum chapter:** "Choosing Your Agentic Coding Methodology" — the seven-dimensional selection model, the three frameworks, the task half-life.
- **The 35-minute rule** as a core practical principle for anyone using agentic coding tools.
- **The context-engineering hierarchy of effort** (research > planning > implementation) as the mental model that prevents the review-fix-reprompt tax.
- **Brownfield adoption playbook** — documentation first, small well-defined tasks, the harness-readiness checklist.

### Builder's Club
- **Framework comparison workshops** — teams bring their BMAD/SPARC/RPI experiences and compare.
- **Open-source task-half-life decomposition tool** — automatically decomposes large tasks into 35-minute chunks with verification gates.
- **Context-utilization monitoring library** — open-source context-window utilization tracker for any agentic coding tool.
- **Brownfield harness-readiness toolkit** — shared community tooling for the modularization/boundary/coverage checklist.
- **Domain-specific customization library** — the institutional-knowledge repositories (rules files, architectural documentation, validated workflows) that compound value over time.

## Anti-Patterns

1. **Framework-first thinking** — choosing a framework before analyzing the seven dimensions; the framework matters less than context engineering discipline.
2. **Brownfield-as-greenfield** — applying SPARC's from-scratch architecture design to legacy code; use BMAD's brownfield workflow or RPI instead.
3. **Long-task tolerance** — allowing tasks beyond 35 minutes; the exponential failure rate makes this the most expensive anti-pattern.
4. **Context overloading** — exceeding 40% context utilization; signal degrades, hallucinations rise, and the review-fix-reprompt tax dominates.
5. **Implementation-first skipping** — jumping to code without research and planning; a single misunderstanding produces thousands of erroneous lines.
6. **Horizontal-copilot-only deployment** — enterprise-wide copilots without vertical, function-specific squads; significantly lower impact.
7. **Framework lock-in** — treating framework choice as permanent; the value is in the institutional knowledge that transfers across frameworks.
8. **Pilot-without-measurement** — running agentic coding pilots without tracking the five measurement dimensions; you can't improve what you don't measure.

## Cross-References

- `harness-engineering-ai-agents-2026` (ai-agents-and-workflows) — the five technical layers (model, orchestration, context, verification, telemetry) that the outer-loop frameworks operationalize.
- `harness-maturity-matrix` (developer-experience-and-flow) — the organizational maturity model that determines which outer-loop stage a team is ready for.
- `context-engineering-production-practice` (cognitive-science-and-ux) — the seven context window components and eight practical techniques that the 40%-utilization rule depends on.
- `agentic-coding-returns-to-expertise` (developer-experience-and-flow) — the expertise leverage curve that informs team composition for each framework.
- `spec-driven-cognitive-partnership` (cognitive-science-and-ux) — the structured-intent specification format that RPI's Plan phase and SPARC's Specification phase produce.
- `coding-agent-decision-fatigue-mitigation` (developer-experience-and-flow) — the two-gate model that the outer-loop frameworks' phase-transition gates operationalize.
- `devex-verification-bottleneck-framework` (developer-experience-and-flow) — the verification-time > writing-time inversion that the 35-minute task half-life compounds.
- `intent-engineering-spec-driven` (developer-experience-and-flow) — the five-element intent spec that feeds RPI's Research and Plan phases.

## Sources

- Michael Stricklen — "Learning About Outer Loop Harnesses for Agentic Coding: What CTOs Need to Know" (LinkedIn, Nov 3, 2025). Months of research into RPI, BMAD, SPARC; the seven-dimensional selection model; the 35-minute task half-life; the 300K-line brownfield success case; the vertical-deployment insight; the <10% pilot-to-production rate.
- BMAD Code, LLC — BMAD™ (Breakthrough Method for Agile AI-Driven Development). Agent-as-code, hyper-detailed stories, mandatory Test Architect for brownfield. Creator's admission: best for greenfield/microservices; brownfield requires heavy customization.
- SPARC — Specification, Pseudocode, Architecture, Refinement, Completion. Five-phase methodology. Adrian Cockcroft (Netflix/AWS) validation: iOS app in Swift built autonomously.
- RPI — Research-Plan-Implement practitioner methodology. Research-first interrogation, detailed blueprints, step-by-step implementation with validation gates. CodeLayer as orchestration platform implementation.
- GitClear — AI Code Quality Report: code churn projected to double in 2026 vs. pre-AI baselines; rising code duplication.
- METR (2025) — RCT: experienced developers 19% slower with AI tools on brownfield tasks while believing 20% faster. The review-fix-reprompt tax.
- SWE-PolyBench — repository-specific difficulty ranging from <10% to >50% resolution rates by tech stack.