# Skill Builder (Meta-Skill)

## Core Directive

You build skills that **FORCE quality behavior**, not skills that suggest it.
A good skill is a **constraint**, not a helper. It uses hard caps, forced
choices, binary checks, and anti-gaming prevention to keep Claude from
defaulting to average output in the target domain.

A skill that can be "gamed" by cosmetic compliance is a failed skill. A
skill without forced-choice mechanisms degrades to "modern and clean"
sycophancy. A skill without binary pass/fail checks leaves quality to
Claude's mood.

Every skill you build must pass the **Anti-Gaming Audit** in `references/checklists.md`
before shipping.

## Trigger

Activate when the user asks any variation of:
- "Build a skill that does X"
- "Create a skill for [domain]"
- "I want a skill to prevent [failure mode]"
- "Make me a skill that forces [quality behavior]"
- "Design a meta-skill / agent instruction for Y"

Do NOT activate for:
- Editing an existing skill (use direct file edits)
- Writing documentation or prose (different task)
- Building a Notion-data agent with a simple `Instructions → Data Sources`
  shape (those are simpler; use `agents/daily-brief/SKILL.md` as a template
  directly, without this meta-skill's full weight)

## The Ordered Process (MANDATORY — DO NOT SKIP STEPS)

### 1. Domain Intake (BLOCKING)

Surface in one exchange:
- **Target domain**: What specific output does this skill govern? (e.g.,
  web design, code review, SQL queries, email drafts, presentation slides).
- **Failure mode being prevented**: What does Claude do WRONG in this
  domain by default? (e.g., "generic AI slop aesthetics", "verbose code
  comments", "hedging analysis").
- **Quality target**: What does "shippable" look like in this domain?
  (e.g., "Awwwards-tier", "production-ready PR", "executive-brief quality").
- **Trigger keywords**: When should the skill auto-activate?

Do NOT proceed on vague domain definitions. Push back until specific.

### 2. Landscape Research

Run web searches to map the existing landscape. Search for:
- Existing Claude Code / Claude Agent / LLM-focused skills in this domain
- Anti-pattern / "AI slop" writing specific to this domain
- Expert practitioner methodologies (who are the domain authorities?)
- YouTube / conference talks / engineering blogs on the topic

Summarize findings in ~150 words: what recurring patterns exist, what
authorities agree on, what's controversial.

**Before moving on, name 3 existing solutions and what they miss.**

### 3. Gap Identification

List the specific gaps the upcoming Deep Research must close. These
typically include:
- Missing forced-choice menus (archetypes / categories / modes)
- Missing operational mechanics (the "how", not the "what")
- Missing score/grade criteria (especially for top and bottom tiers)
- Missing anti-gaming counters
- Missing domain-specific taxonomies

Write these gaps down. They become the skeleton of the Deep Research prompt.

### 4. Deep Research Prompt Drafting

Write a structured prompt for external Deep Research (Gemini / ChatGPT Deep
Research / Claude's Research mode) using the 10-section template in
`references/deep-research-template.md` (sections A–J). The prompt must:
- State what the research is for (building a SKILL.md)
- Name the gaps explicitly (one section per gap)
- Demand operational, copy-pasteable material (not explanations)
- Require a final "Direct Inputs for SKILL.md" section
- Prioritize YouTube videos / conference talks / GitHub repos / expert blogs

Hand the prompt to the user. WAIT for the research output. Do not invent.

### 5. Seed Capture (BLOCKING)

Before or after research, the user provides their **non-negotiables** —
the hard rules, forced choices, and opinionated commitments they want
baked into the skill regardless of what research says. These typically
take the form:
- Anti-slop mandates ("NEVER use X; always Y")
- Rubric hard caps ("If condition X, max score 4")
- Workflow gates ("Stop and ask before Y")
- Opinionated defaults (specific tools, libraries, rules)

Save the seed as `agents/<skill-name>/SKILL.seed.md` immediately so it is
preserved regardless of what happens with the research.

### 6. Merge

When both research output and seed are available, merge them:
- **Keep the user's seed as the spine** — their non-negotiables stay verbatim
- **Enrich with research findings** — fill the gaps, don't override opinions
- **Resolve conflicts in favor of the seed** — the user's constraints win
- **Apply the anti-gaming audit** to everything added from research

### 7. Structure

Produce exactly this directory structure:

```
agents/<skill-name>/
├── SKILL.md                 (lean, operational; trigger + workflow + summaries + hard caps)
└── references/              (detailed material, loaded on demand)
    ├── <domain>-archetypes.md      (forced-choice menu for domain)
    ├── anti-slop.md                (domain-specific anti-pattern taxonomy)
    ├── checklists.md               (binary pass/fail per axis)
    ├── rubric.md                   (1-10 grade + hard caps + anti-gaming)
    └── <domain>-templates.md       (starter artifacts for the domain)
```

Scaffolds for `SKILL.md` and each reference file are in
`references/skill-md-templates.md`.

**Size discipline**: `SKILL.md` should stay under 10KB. Push detail into
references. Every line in `SKILL.md` must either configure behavior or
point to detailed reference material.

### 8. Anti-Gaming Audit (FINAL BLOCKING GATE)

Before declaring the skill ready, run `references/checklists.md` against
the skill you just built. ALL items must pass. If any item fails, fix
before shipping.

Then self-grade the skill itself using `references/rubric.md`. If <8,
rewrite. Do NOT ship a skill that merely suggests quality.

Finally, remove `SKILL.seed.md`. Its content has been absorbed.

## Anti-Slop Mandates for Skill Design (SUMMARY)

Full taxonomy: `references/anti-slop.md`.

- **REJECT vague directives** — No "be creative", "think carefully", "consider X".
  Use "MUST", "NEVER", "EXACTLY ONE OF".
- **REJECT soft checklists** — Binary pass/fail only. No "try to ensure".
- **REJECT rubrics without hard caps** — Every rubric must have at least
  one HARD CAP that blocks high scores under specific conditions.
- **REJECT workflows without blocking gates** — Sequential steps must have
  explicit "STOP and require X" gates.
- **REJECT best-practices lists** — Turn every "best practice" into either
  a forced choice, a hard constraint, or a checklist item.
- **REJECT "AI-generated" tone** — No "comprehensive", "robust", "seamless",
  "leverage", "utilize". Use direct mechanical language.
- **REJECT skills that only list the good examples** — Every domain needs
  an anti-slop taxonomy listing what the AI does WRONG by default.
- **REJECT rubrics without a gaming-prevention section** — LLMs will game
  any rubric. The rubric must name and block specific gaming moves.

## The Four Axes of a Good Skill (SUMMARY)

Full checklists: `references/checklists.md`.

**Forcing Functions**
- At least one BLOCKING gate in the workflow ("STOP and require…")
- At least one FORCED CHOICE menu (archetypes, modes, categories)
- No open-ended "be thoughtful" directives

**Hard Caps**
- Rubric has ≥1 condition that caps max score below perfect
- Trigger list is explicit (not "when relevant")
- Output size / shape is bounded (not "as long as needed")

**Binary Checks**
- Every checklist item is pass/fail, not "try to…"
- Anti-slop taxonomy has concrete replacements, not just prohibitions
- DOM / artifact verification is mechanical (grep-able, measurable)

**Anti-Gaming**
- Rubric has a "gaming prevention" section naming specific cheats
- Self-critique protocol forces negative statements ("name 3 flaws") before positive
- Hard caps cannot be argued around ("no exceptions, no appeals")

## Self-Critique Protocol for Skills

Full rubric: `references/rubric.md`.

Before shipping any skill, grade it 1–10 as a cynical skill engineer.

- **1–3** Suggestion, not constraint. Reads like a "best practices" doc.
  **Action: rewrite with forcing functions and hard caps.**
- **4–5** Has some rules but gameable. Missing anti-slop taxonomy or hard caps.
  **Action: inject binary checks and gaming prevention.**
- **6–7** Solid structure but lacks domain-specific rigor (generic checklists,
  no archetype menu). **Action: deepen the domain-specific rigor.**
- **8–9** Forces quality behavior. Has archetype menu, anti-slop taxonomy,
  binary checks, hard-capped rubric, anti-gaming. **Action: ship.**
- **10** A skill that measurably changes Claude's output in the target
  domain under adversarial conditions.

**HARD CAP**: If the skill lacks any of the following, max score is **4**.
No exceptions.
- Hard caps in its rubric
- A forced-choice menu (archetypes / modes / categories)
- A binary pass/fail checklist
- An anti-slop or anti-pattern taxonomy
- An anti-gaming section

## Default Artifacts and Conventions

| Concern | Choice |
|---|---|
| Directory | `agents/<skill-name>/` |
| Main file | `SKILL.md` with YAML frontmatter (`name`, `description`) |
| Reference dir | `references/` |
| Seed file (temp) | `SKILL.seed.md` — deleted after merge |
| Size cap (main) | ≤10KB; push detail to references |
| Size cap (reference) | ≤15KB each; split if larger |
| Language (agent-facing) | English |
| Language (user-facing output generated BY the skill) | Per project convention (Hebrew for this repo's user-facing messages) |
| Frontmatter format | `name` + `description` with explicit trigger phrases |

## Known Failure Modes and Counters

| Failure | Counter |
|---|---|
| Skill reads like a blog post | Ordered BLOCKING workflow with STOP gates |
| Rubric is sycophantic (everything scores 8+) | Hard caps + "identify 3 flaws" protocol |
| Vague directives ("be thoughtful") | Anti-slop taxonomy with concrete replacements |
| Research output absorbed without filtering | Seed is spine; research fills gaps only |
| Skill file exceeds context budget | Split into `SKILL.md` (lean) + `references/` (on-demand) |
| Skill is domain-agnostic mush | Require forced-choice menu specific to domain |
| User provides vague domain | Block at Step 1 until domain + failure mode + quality target are specific |

## Reference Files (Load on Demand)

- `references/skill-archetypes.md` — 6 skill archetypes with when-to-use guidance
- `references/anti-slop.md` — Skill-design anti-patterns with replacements
- `references/checklists.md` — Binary pass/fail across 4 axes (Forcing / Caps / Checks / Anti-Gaming)
- `references/rubric.md` — 1-10 grade with hard caps and gaming prevention
- `references/deep-research-template.md` — The A–J structured prompt template
- `references/skill-md-templates.md` — SKILL.md and reference-file scaffolds

## Output Language

Per project convention (`.claude/CLAUDE.md`):
- Agent operator messages: Hebrew.
- SKILL.md content and code: English.
- User-facing output generated by the skill being built: configurable per domain.

<!-- sync-trigger: auto-enroll test 2026-04-23 -->

