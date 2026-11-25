---
name: skill-evolution
description: Curated, anti-bloat skill evolution engine. Extracts high-value architectural lessons, consolidates heuristic rules (max 10 rules per skill), prevents prompt bloat, and maintains pristine skill cleanliness.
aliases:
  - skill-evolution
  - self-improving-skills
  - continuous-learning
  - anti-bloat-curation
category: "07 - Codebase Exploration & Tooling"
tags:
  - agent-skill
  - self-evolution
  - anti-bloat
  - stage-7
---

# Curated Skill Evolution & Anti-Bloat Engine

This skill defines the enterprise standard for **continuous skill refinement and self-evolution without prompt bloat**. It ensures that as agents execute tasks, they capture hard-won architectural lessons and user preferences into durable, high-density heuristics while strictly preventing token bloat, semantic drift, and conversational garbage.

---

## 4-Tier Anti-Bloat Filtration Gate

Before any lesson or heuristic is permanently recorded into a skill, it must pass through 4 strict filtration gates:

```
[Raw Execution Outcome / Bug Fix]
              │
              ▼
┌───────────────────────────────┐
│ Gate 1: Ephemerality Test     │ ─── Fail (One-off glitch, network hiccup) ───► [DISCARD]
└───────────────────────────────┘
              │ Pass (Reusable architectural invariant)
              ▼
┌───────────────────────────────┐
│ Gate 2: Deduplication & Merge │ ─── Overlaps existing rule ───► [SYNTHESIZE & CONSOLIDATE]
└───────────────────────────────┘
              │ Pass (Novel insight)
              ▼
┌───────────────────────────────┐
│ Gate 3: Hard-Cap Rule of 10   │ ─── Count > 10 ───► [MERGE CLOSEST OR PRUNE LOWEST-VALUE]
└───────────────────────────────┘
              │ Pass (Active rules <= 10)
              ▼
┌───────────────────────────────┐
│ Gate 4: Token Budget Check    │ ─── Budget > 250 tokens ───► [COMPACT PHRASING]
└───────────────────────────────┘
              │ Pass
              ▼
[Recorded into Skills/<skill>/learned_patterns.md or ## Learned Patterns]
```

### 1. Gate 1: The Ephemerality Test (คัดกรองขยะชั่วคราว)
- **DISCARD**: One-off environmental anomalies (e.g. WiFi disconnected for 3 seconds, external API timeout, typos in user prompt).
- **KEEP**: Structural, platform-level, or system-level invariants (e.g. macOS Retina 2.0x scale factor, Edward Tufte table styling rules, AppKit non-blocking FIFO semantics, user formatting constraints).

### 2. Gate 2: Deduplication & Semantic Clustering (การรวบกลุ่ม ไม่เขียนซ้ำ)
- Never create a new rule that merely restates an existing instruction in `SKILL.md`.
- If a new observation is a special case of an existing pattern, expand and refine the existing pattern rather than appending a new bullet point.

### 3. Gate 3: The Hard-Cap Rule of 10 (เพดานสูงสุด 10 กฎทอง)
- **Strict Limit**: No skill is permitted to contain more than **10 active learned patterns**.
- When an 11th pattern is discovered:
  1. The agent must scan existing rules for semantic neighbors.
  2. The two most related rules must be merged into a single consolidated principle.
  3. If no merge is feasible, the least frequently applicable rule must be pruned.

### 4. Gate 4: Token Budget & Density (ควบคุมขนาดโทเคน)
- The entire `Learned Patterns` section of any skill must stay strictly under **250 tokens** (~1,000 characters).
- Phrasing must adhere to the high-density **Condition-Action Heuristic Format**:
  `[PATTERN-ID]: WHEN [Exact Trigger/Condition] DO [Surgical Action] INSTEAD OF [Naive Approach]`

---

## 2026 Upstream Knowledge Ingestion Pipeline

To ensure skills continually evolve with world-class engineering standards without manual toil:

1. **Google Modern Web Guidance Engine**:
   - Query upstream browser and CSS standards before frontend implementations:
     `npx -y modern-web-guidance@latest search "<topic>"`
2. **Upstream Agent Registries (VoltAgent / Awesome Agent Skills)**:
   - Benchmark agent patterns against curated community and enterprise agent skills.
3. **Framework Modernization Invariant Checks**:
   - Ingest breaking changes and ergonomic upgrades from Tailwind v4, React 19, Next.js 15, and Pydantic v2.
4. **Automated CLI Ingestion (`evolve_skill.py`)**:
   - Run `python3 evolve_skill.py audit` to detect and prune bloat.
   - Run `python3 evolve_skill.py learn <skill> "<lesson>"` to add vetted patterns through the 4-tier gate.

---

## Dual-Decoupled Storage Architecture

To ensure skills never accumulate historical logs or conversational clutter:

1. **Global Execution Telemetry (`00 - Skills Execution Ledger.md`)**:
   - Stores chronological, single-line task records.
   - Houses metadata: timestamp, task description, skills applied, status, and summary insight.
   - Completely separated from skill instruction bodies.
2. **Skill Heuristic Storage (`Skills/<skill>/learned_patterns.md` or `## Learned Patterns`)**:
   - Stores only high-density, evergreen operational rules.
   - Kept pristine, formatted with zero conversational filler.

---

## Heuristic Phrasing Standards

Every learned heuristic must follow this exact high-density schema:

```markdown
### Pattern #[ID]: [Short Descriptive Name]
- **Condition**: [Precise context, OS, tool, or prompt trigger]
- **Action**: [Deterministic procedure to execute]
- **Avoid**: [Naive pattern that previously failed]
```

---

## 🔗 Connected Skills

- Previous: [[Skills/create-skill/SKILL|create-skill]]
- Companion: [[Skills/llm-wiki/SKILL|llm-wiki]]
- Upstream: [[Skills/systematic-debugging/SKILL|systematic-debugging]]
- Downstream: [[Skills/verification-before-completion/SKILL|verification-before-completion]]
