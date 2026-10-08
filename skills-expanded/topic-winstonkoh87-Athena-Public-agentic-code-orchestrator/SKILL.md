---
name: agentic-code-orchestrator
description: "Unified codebase manipulation, AI deployment, data analysis, and academic delivery engine. Absorbs 6 coding protocols + data-analysis + academic-delivery + spec-driven-dev."
vibe: "Ship at 70%, iterate to 95%. Never build what you haven't specced."
context_trigger: "refactor, bug, architecture, data dump, deploy, website, dashboard, code, build, CSV, Parquet, JSON, DuckDB, assignment, essay, capstone, SUSS, academic, Python, React, Next.js, Supabase, vibe code"
auto-invoke: true
model: default
source: "Retroactively compiled from 1,900+ sessions (2025-2026) via skill-compiler"
compiled_from: "protocols/coding/COD-*, skills/data-analysis, skills/academic-delivery, skills/spec-driven-dev"
absorbs: "data-analysis, academic-delivery, spec-driven-dev, academic-humanizer, statistical-analysis"
meta_patterns: [MP-2, MP-11]
pinned: true
---

# Agentic Code Orchestrator — Build × Analyze × Deliver

> **Compiled**: 2026-05-11 (retroactive synthesis of all engineering/academic sessions)
> **Problem Class**: All code generation, data analysis, dashboard building, academic delivery, and technical project execution.
> **Axiom**: *"The winner is not who thinks deepest on the first try — it's who can iterate fastest at the lowest cost per loop."*

## When to Use

Invoke whenever the user mentions:
- Building/fixing a website, dashboard, or web app
- Data analysis (CSV, JSON, Parquet, large datasets)
- Academic assignments (essays, capstones, SUSS coursework)
- Code refactoring or architecture decisions
- Deploying to Supabase, Vercel, GitHub Pages
- "Analyze this data" / "Build me a [thing]" / "Fix this bug"

## Solution Architecture

### Module 1: The RETO Engine Selector (COD-415 + MP-2)

Before writing ANY code, classify the project:

```
Is failure reversible?   → Efficient Engine (Vibe Engineering: ship at 70%)
Is failure irreversible? → Robust Engine (Nuclear Plant: test everything)
```

| Project Type | Engine | Test Coverage | Ship Threshold |
|:------------|:-------|:-------------|:---------------|
| Portfolio/website | Efficient | Visual QA only | 70% |
| Client dashboard | Efficient→Robust | Visual QA + data validation | 85% |
| Financial calculations | Robust | Unit tests + manual verification | 99% |
| Academic submission | Robust | Plagiarism check + format audit | 95% |
| Quick prototype/MVP | Efficient | "Does it work?" | 60% |

### Module 2: Spec-Driven Development (COD-107)

**NEVER build without a spec.** The spec is the contract.

```
Phase 1: Interrogation (The /brief)
  → What does the user ACTUALLY want?
  → What are the constraints?
  → What does "done" look like?

Phase 2: design.md Generation
  → Architecture diagram
  → Component breakdown
  → Data flow
  → Acceptance criteria

Phase 3: User Approval
  → Review the spec
  → Confirm scope
  → THEN and ONLY THEN → build

Phase 4: Execution
  → Build to spec, not to vibes
  → Checkpoint every major component
```

### Module 3: The De-Sloppify Protocol (ECC Steal)

After generating code, ALWAYS run this quality pass:

1. **Dead Code Purge**: Remove commented-out code, unused imports, placeholder TODOs
2. **Console.log Sweep**: Remove all debug logging from production code
3. **Naming Consistency**: Verify naming conventions match project standard
4. **Error Handling**: Ensure every async operation has error handling
5. **Type Safety**: If TypeScript, no `any` types unless explicitly justified

### Module 4: Data Analysis Pipeline (DuckDB-Powered)

For large data dumps (CSV, Parquet, JSON):

```
Phase 1: Ingest
  → Identify file format + encoding
  → Load with DuckDB (NOT Pandas for large files)
  → Profile: row count, columns, types, nulls, distribution

Phase 2: Profile
  → Summary statistics per column
  → Outlier detection
  → Cardinality analysis
  → Missing data assessment

Phase 3: Query
  → User-directed analysis
  → SQL-based queries via DuckDB
  → Visualization where appropriate

Phase 4: File Insights
  → Key findings summary
  → Actionable recommendations
  → Export results
```

**Rule**: For files >100MB, ALWAYS use DuckDB. Pandas will crash.

### Module 5: Academic Delivery Pipeline

For SUSS assignments, essays, capstones:

```
Step 1: Intake — Parse assignment brief, identify marking rubric
Step 2: Research — NotebookLM arbitrage for source material
Step 3: Outline — Structure mapped to rubric weightings
Step 4: Draft — Write with burstiness and perplexity variation
Step 5: Red-Team — Invoke red-team-review on key arguments
Step 6: Humanize — Run academic-humanizer if AI detection risk
Step 7: Format — APA/Harvard citation formatting
Step 8: Deliver — Final audit against rubric
```

**The Bionic Academic Advantage** (CS-467):
- AI drafts at 80%, human polishes to 100%
- Research Arbitrage: NotebookLM handles volume, Athena handles synthesis
- SPSS/R/Python for statistical analysis (statistical-analysis skill)

### Module 6: Dashboard/Website Architecture

**For financial/trading dashboards**:

| Principle | Rule |
|:----------|:-----|
| **Decimal Standard** | 4 decimal places for all statistical outputs (GTO compliance) |
| **Render Stability** | Extract primitive values for useEffect deps, never use object refs |
| **Visual Hierarchy** | Status indicators (green/amber/red) for institutional readability |
| **Responsive** | Mobile-first, then desktop adaptation |
| **Performance** | Lazy load heavy components, debounce real-time updates |

**For portfolio/marketing websites** (CS-437 UI/UX Pro Max):

| Principle | Rule |
|:----------|:-----|
| **Above-the-fold** | Hero → problem statement → CTA in first viewport |
| **Social proof** | Testimonials, logos, case study links |
| **Speed** | <3s load time or you lose 50% of visitors |
| **SEO** | Meta tags, semantic HTML, structured data |
| **Conversion** | One clear CTA per page section |

## Output Template

```
ORCHESTRATOR REPORT
───────────────────
Project:        [Description]
Engine:         [Efficient / Robust — reversibility: ...]
Spec Status:    [Approved / Pending — design.md: ...]
Data Pipeline:  [DuckDB / Pandas / N/A — file size: ...]
Quality Gate:   [De-Sloppified: Y/N — coverage: X%]
Ship Threshold: [60% / 70% / 85% / 95% / 99%]

STATUS: [BUILDING / TESTING / SHIPPED]
```

## Absorbed Protocols & Skills

### Coding (6)
COD-107 (Spec-Driven Development), COD-108 (Semantic Search Standards), COD-110 (Structured Decoding), COD-112 (Stop Pattern), COD-415 (Spec-Driven Velocity), COD-900 (Project Scaffolding)

### Absorbed Skills
- `data-analysis` → DuckDB-powered large file analytics
- `academic-delivery` → 8-step pipeline for academic deliverables
- `academic-humanizer` → AI detection bypass rewriting
- `spec-driven-dev` → Interrogation → design.md → build
- `statistical-analysis` → SPSS/R/Python statistical pipelines

## Key Case Studies

CS-062 (Vibe Coding Gap), CS-100 (Project Vend Agentic Failure), CS-120 (Vibe Coding Zero-Cost Stack), CS-157 (ChunkHound Agentic Coding), CS-187 (Deep Data Analyst Post-Mortem), CS-235 (Over-Engineering Trap), CS-237 (Async Dev Workflow), CS-303 (Smart Mock vs Real API), CS-306 (Lovable Trap), CS-350 (Vibe Coding Security Failures), CS-370 (Vibe Coding Trap), CS-425 (Academic Essay Workflow), CS-430 (Vibe Coding MVP), CS-437 (UI/UX Pro Max Architecture), CS-438 (Biological Debt Coding), CS-440 (Velocity vs Craftsmanship), CS-467 (Bionic Leverage Academic Arbitrage), CS-486 (Component-Level AI Architecture), CS-508 (OpenClaw Architecture), CS-515 (Maestro Parallel Orchestration), CS-532 (Vibe Coding Agency Model), CS-539 (CEG3001 Capstone Debrief), CS-540 (Anti-Slop Website Pipeline), CS-543 (Vibe Coded SaaS $10K MRR)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| **Building without spec** | NEVER proceed without design.md approval |
| **Pandas on large files** | Auto-route to DuckDB for files >100MB |
| **AI Slop** | De-Sloppify protocol is MANDATORY post-generation |
| **Vibe Coding Security** | CS-350: Never ship auth, payments, or PII without Robust engine |
| **Over-Engineering** | CS-235: Spec defines "done." Don't gold-plate. |
| **Render Jitter** | Extract primitive deps for useEffect. Never pass object refs. |

## Validated Patterns (Empirical)

- [V] **DuckDB > Pandas**: For files >100MB, DuckDB is 10-50x faster and doesn't crash. | Reapply: Every large data analysis.
- [V] **NotebookLM Research Arbitrage**: Offload PDF ingestion to NotebookLM, keep Athena's context for synthesis. | Reapply: Every academic assignment.
- [V] **4-Decimal GTO Standard**: Uniform precision prevents cognitive load in financial dashboards. | Reapply: Every statistical display.
- [V] **Primitive Dependency Extraction**: `[data.currentRatio]` instead of `[data]` stops React re-render loops. | Reapply: Every dynamic status component.
- [V] **Ship at 70%, iterate to 95%**: For reversible projects, perfection is the enemy of shipped. | Reapply: Every portfolio/MVP build.

## References

- META_PATTERNS.md — MP-2 (RETO engine), MP-11 (Iteration Economy)
- [bionic-decision-engine](../../therapeutic-ifs/SKILL.md) — For build/buy/wait decisions
