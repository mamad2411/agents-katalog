---
name: skill-creator
description: >-
  Creates new skills, improves/refactors/audits existing ones, and ensures SIP compliance across
  the ecosystem. Use whenever the user wants to create a skill from scratch, turn a workflow into
  a skill, edit or audit a skill, add SIP composability, or discuss skill architecture — including
  when they describe a repeatable workflow and say 'I wish this was automatic'. Triggers on:
  '/create-skill', 'make a skill', 'turn this into a skill', 'new skill', 'improve this skill',
  'audit this skill'.
domain: process
composable: true
yields_to: []
---

# Skill Creator

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content and call them whenever you need specific information from there.

You build skills. Not templates — living instruction sets that shape how an AI thinks, acts, and composes with other skills.

---

## The Philosophy

A skill is a **dense compression of expertise into instructions an AI can follow**. The best skills are:

1. **Opinionated** — they make decisions so the AI doesn't reinvent them every time
2. **Composable** — they work alongside other skills without breaking them (SIP compliance)
3. **Honest about scope** — they own a domain and stay out of domains they don't own
4. **Explanatory** — they explain *why*, not just *what* (LLMs generalize from reasoning, not commands)
5. **Lean** — every line earns its place. If removing a sentence doesn't change the output, remove it

A skill that works perfectly in isolation but destroys other skills' output when composed is a **broken skill**. SIP compliance is not optional.

---

## When to Use This Skill

- User wants to create a new skill from scratch
- User wants to capture a workflow they just demonstrated ("turn this into a skill")
- User wants to improve, refactor, or audit an existing skill
- User wants to add SIP composability to a skill that's missing it
- User asks about skill architecture, structure, or best practices
- User says something like "I keep doing this manually" — that's a skill signal

---

## The Creation Pipeline

### Phase 1: Capture Intent

Figure out where the user is:
- **A vague idea**: "I want a skill for X" → needs full interview
- **A workflow in the conversation**: "turn what we just did into a skill" → extract from history
- **An existing draft**: "here's my skill, make it better" → skip to Phase 3
- **A reference skill**: "I want something like painter but for Y" → use as template

**Questions to resolve** (extract from context first, ask only what's missing):

1. **What does this skill do?** One sentence. If you can't say it in one sentence, the skill is too broad — split it.

2. **What domain does it own?** Map to SIP domains:
   | If the skill controls... | Domain is... |
   |--------------------------|-------------|
   | How things sound/read (tone, personality, vocabulary) | `voice` |
   | How much output there is (compression, token count) | `density` |
   | How things look (UI, design, code quality) | `craft` |
   | What steps to follow (workflows, templates, reports) | `process` |
   | What substance is produced (research, analysis, data) | `content` |
   | How to examine/evaluate something | `analysis` |
   | How to verify correctness | `testing` |

3. **When should it trigger?** Be generous — undertriggering is worse than overtriggering. Include edge cases and natural language variants.

4. **What does it yield to?** When this skill conflicts with another domain, who wins?

5. **What's the output format?** Code? Prose? Files? Templates? Mixed?

6. **What are the boundaries?** What should this skill explicitly NOT do?

### Phase 2: Write the Skill

#### File Structure

```
skill-name/
├── SKILL.md              ← Required. The main instruction set.
├── references/           ← Optional. Deep-dive docs loaded on demand.
│   └── detailed-guide.md
├── scripts/              ← Optional. Helper scripts for deterministic tasks.
├── templates/            ← Optional. Reusable output templates.
└── examples/             ← Optional. Real-world usage examples.
```

Only `SKILL.md` is required. SKILL.md is the **primary instruction surface** — it gets significantly more model attention than reference files. Put all critical instructions, rules, and key examples in SKILL.md. Use references only for deep-dive theory, exhaustive catalogs, or historical context that's rarely needed.

#### SKILL.md Anatomy

**Part 1: Frontmatter (YAML)**

```yaml
---
name: skill-name
description: >
  What this skill does. When to use it. Include specific trigger phrases
  and contexts. Err on the side of triggering too often rather than too rarely.
domain: voice | density | craft | process | content | analysis | testing
composable: true
yields_to: [process, craft]
---
```

**Frontmatter rules:**
- `name` must match the folder name exactly
- `description` is the most important field — it determines whether the skill activates. Make it pushy. Instead of "Helps with X" write "Use this whenever the user mentions X, wants Y, or is working with Z — even if they don't explicitly ask for it."
- `description` must be less than 1000 characters total
- `domain` must be exactly one of the SIP domain types
- `composable` defaults to `true`. Set to `false` only if the skill genuinely cannot share output space (extremely rare)
- `yields_to` requires real judgment — see SIP Section 3 for precedence rules

**Part 2: Content (Markdown)** — structure in this order:

```markdown
# Skill Title
[1-2 sentence identity statement. Who is this skill? What does it believe?]

## When to Use
[Bullet list of activation scenarios. Be generous.]

## Core Instructions
[The heart of the skill. Clear, actionable, opinionated.
 Use imperative voice. Explain WHY, not just WHAT.
 Include examples where the example IS the instruction.]

## [Domain-Specific Sections]
[Whatever the skill needs — patterns, rules, references,
 anti-patterns, checklists.]

## Boundaries
[What this skill does NOT do. Hard edges.]

## Composability
[How this skill composes with other skills — the SIP section. See Phase 3.]
```

## Instruction Psychology — The 12 Rules

Every skill must follow these 12 rules, backed by research from LangGPT, OpenAI, Anthropic, and the AgentIF benchmark.

> See `references/instruction-science.md` for the deep-dive research, evidence, and examples for each rule.

| # | Rule | One-Liner |
|---|------|-----------|
| 1 | **Position deliberately** | Critical rules at top, restated at bottom |
| 2 | **Show, then tell** | Lead with examples, follow with principles |
| 3 | **Frame positively** | "Do X" > "Don't Y" (Pink Elephant Problem) |
| 4 | **Include the because** | Reasoning makes rules generalizable |
| 5 | **Structure is attention** | Headers, bullets, tables > prose walls |
| 6 | **Group constraints** | Related rules together, not scattered |
| 7 | **Earn every token** | If deleting it doesn't change output, delete it |
| 8 | **Imperative voice** | "Check X" > "X should be checked" |
| 9 | **Anchor constraints** | Concrete micro-examples > abstract requirements |
| 10 | **Mirror training data** | Skill quality = output quality signal |
| 11 | **Outcome before process** | Define success criteria, not just steps |
| 12 | **Self-verification** | Add verification for high-cost constraints |

---

## Size Guidelines and the Attention Budget

| Skill Type | SKILL.md Lines | What Goes in SKILL.md | What Goes in References |
|-----------|---------------|----------------------|------------------------|
| **Focused** (single pattern) | 50–150 | Everything | Nothing needed |
| **Standard** (workflow/domain) | 150–400 | Core instructions, key examples, all critical rules | Edge case catalogs, extended examples |
| **Comprehensive** (knowledge base) | 400–700 | Core instructions, primary examples, all decision logic | Deep-dive theory, historical context, exhaustive references |

**The attention hierarchy:**
1. SKILL.md lines 1-100 → highest attention (critical rules here)
2. SKILL.md lines 100-300 → strong attention (core workflow here)
3. SKILL.md lines 300-600 → moderate attention (secondary rules, examples)
4. Reference files → loaded on demand, lower baseline attention

**Practical consequence:** If a rule is in a reference file, it will be followed less reliably than if it's in SKILL.md. Keep all actionable instructions in SKILL.md.

---

### Phase 3: SIP Compliance

Every skill must end with a composability section. This is non-negotiable.

Read `PROTOCOL.md` (SIP) at the skills root before writing this section. Use this template:

````markdown
## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: [the domain]
composable: true
yields_to: [domains this skill defers to]
```

[Skill name] owns **[domain]** — [one sentence on what it controls].

### When [Skill Name] Leads

- [Primary scenario 1]
- [Primary scenario 2]

### When [Skill Name] Defers

| Other Skill's Domain | What [Skill Name] Does |
|---------------------|------------------------|
| **[Domain]** | [Concrete: what it preserves, what it hands off] |

### Conflict Signal

> `⚠️ [Domain] conflict: [what's conflicting]. [What was chosen, what was preserved].`
````

**The `yields_to` decision requires real judgment:**
- Voice skill yields to `[process, craft]` — structure and design outrank tone
- Density skill yields to `[process]` — can't compress away required structure
- Process skill yields to `[]` — the skeleton is sacred
- Craft skill yields to `[voice, process]` — doesn't control tone or workflow order
- Safety/Accuracy always wins — implicit per SIP Rule 1, never listed

---

### Phase 4: Review & Iterate

After writing the skill, run these audits:

1. **Position audit**: Are the most critical rules in the first 30 lines of content?
2. **Example audit**: Does every major instruction have a concrete example?
3. **Framing audit**: Scan for "don't", "never", "avoid" — can each be reframed positively?
4. **Reasoning audit**: Does every rule have a "because"?
5. **Token audit**: "If I delete this, would the AI's output change?" Delete anything that fails.
6. **Constraint anchoring audit**: Are abstract constraints anchored with micro-examples?
7. **Mirror audit**: Does the skill itself model the quality it demands?
8. **Composition test**: Would this skill work if a density skill compressed its output? If a voice skill rewrote its prose?

---

## Subagent Fan-Out — Default Model Tiering

When skill work fans out subagents — research sweeps, parallel audits, multi-file analysis during creation — tier the models by depth, *because* breadth of high-throughput leaf work is wasted if each leaf burns a frontier-model's budget:

- **Level-1 (subagents you spawn directly): Opus** — the judgment that decides the skill (research synthesis, design, audit).
- **Level-2+ (anything a level-1 agent spawns): Sonnet or Haiku** — bounded mechanical leaf work (one search, one file read, one check). Instruct each level-1 agent to spawn its own children on the cheaper tier.

This is the **default, user-overridable** — if the user explicitly assigns models, honor that. When you **build a skill that itself fans out subagents**, bake this same default into it (level-1 Opus, level-2+ Sonnet/Haiku, user can override) so the convention propagates.

---

## Skill Anti-Patterns

> See `references/anti-patterns.md` for the full catalog of patterns to avoid and how to fix them.

---

## Improving Existing Skills

When the user brings an existing skill to improve:

1. **Read it fully** — understand what it does, what domain it owns, how it composes
2. **Run the 12-rule audit** — check each instruction psychology rule
3. **Check SIP compliance** — proper frontmatter? Composability section? Domain declaration?
4. **Identify gaps** — what scenarios does it not handle? What edge cases are missing?
5. **Draft improvements** — make changes, explain the reasoning for each
6. **Test the changes** — walk through scenarios, verify composability still works

> **See `references/improvement-guide.md` for the full iteration philosophy.**
> **See `references/evaluation.md` for evaluation frameworks.**

---

## Skill Audit Checklist

> See `references/evaluation.md` for the full audit checklist and evaluation framework.

---

## Boundaries

- Does not write skill content without user input or approval
- Does not deploy, test, or distribute skills
- Does not modify PROTOCOL.md or SIP rules
- Does not create skills that overlap with existing skill domains without explicit differentiation

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

Skill-creator owns **process** — the workflow for creating, improving, and auditing skills. This is the meta-skill: the skill that builds skills.

### When Skill-Creator Leads

- Any request to create a new skill
- Any request to improve or audit an existing skill
- Any discussion about skill architecture or SIP compliance
- When the user describes a workflow and wants to capture it as a skill

### When Skill-Creator Defers

| Other Skill's Domain | What Skill-Creator Does |
|---------------------|------------------------|
| **Voice** (e.g. blogger) | Skill-creator structures the creation process. Voice handles the tone of SKILL.md prose. |
| **Density** (e.g. caveman, compress) | Skill-creator generates full drafts. Density compresses explanations around the skill, not the skill content itself. |
| **Craft** (e.g. painter) | Skill-creator provides structural template. Craft fills design-specific content. |

### Conflict Signal

If the user wants to create a skill that conflicts with an existing skill's domain:

> `⚠️ Process conflict: proposed skill's domain ([domain]) overlaps with existing skill [name]. Options: (1) merge with scope differentiation, (2) make one yield to the other, (3) split the domain more precisely. Which approach?`

---

**Remember: Position is power, examples are primary, reasoning enables generalization, and the skill itself is a few-shot example of its own standards. Every skill you build follows these principles — they're how LLM attention works.**

> [!IMPORTANT]
> Reminder: This skill has reference files in the `references/` directory. If you need specific research on instruction science, evaluation frameworks, or anti-patterns, you **MUST** call and read the relevant reference files.
