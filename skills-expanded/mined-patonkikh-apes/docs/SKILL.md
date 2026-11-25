# How to create a new Skill

Step-by-step guide for authoring an APES-compatible Engineering Playbook.

**Time:** ~30–60 minutes for a first skill  
**Template:** [skills/_template/](../skills/_template/)  
**Standard:** [SKILL_STANDARD.md](SKILL_STANDARD.md)

---

## 1. Choose one task

A Skill solves **one engineering task** and produces **one named artifact**.

| Good | Bad |
|------|-----|
| Write a PRD | Do all product management |
| Review prompts for safety | Be a helpful assistant |
| Design RAG chunking strategy | Build entire RAG system in one skill |

Ask: *Can I describe the output in one sentence?*

---

## 2. Pick category and name

| Category | Examples |
|----------|----------|
| `product` | Discovery, PRD, user stories, OKRs |
| `architecture` | C4, ADR, API design, reviews |
| `ai` | Prompts, agents, context, evaluation |
| `rag` | Chunking, retrieval, embeddings |
| `security` | OWASP, threat modeling, guardrails |
| `mcp` | MCP servers, tools, clients |
| `data` | Pipelines, metrics, labeling, data quality |
| `devops` | CI/CD, deploy, runbooks, operations |
| `growth` | GTM, pricing, experiments, monetization |

**Name:** kebab-case, matches folder name.

```text
skills/product/feature-prioritization/
         ^^^^^^^^^^^^^^^^^^^^^^^^
         name: feature-prioritization
```

---

## 3. Copy the template

```bash
mkdir -p skills/<category>/<skill-name>
cp skills/_template/skill.md skills/<category>/<skill-name>/skill.md
cp skills/_template/README.md skills/<category>/<skill-name>/README.md
cp skills/_template/examples.md skills/<category>/<skill-name>/examples.md
```

---

## 4. Write frontmatter

```yaml
---
name: feature-prioritization
description: >
  Prioritize features using RICE/ICE scoring and recommend an MVP cut line.
  Use when prioritizing backlogs, MVP scope, or feature ranking.
metadata:
  apes-version: "1.1"
  category: product
---
```

**Description formula:**

```text
[What artifact the skill produces].
Use when [scenario 1], [scenario 2], or [keywords].
```

Rules:
- Third person, not *"I can help you…"*
- Include trigger words agents use for discovery
- Max 1024 characters

---

## 5. Fill the 8 sections

### Purpose

One task. List **Input** and **Output** explicitly.

```markdown
**Input:** Backlog list, constraints, optional business goals
**Output:** Prioritized ranking with MVP cut line and rationale
**Examples:** See [examples.md](examples.md) for worked input/output.
```

### Workflow

Numbered steps: **gather → analyze → produce → validate**.

Each step should state what the agent does and when to stop for missing input.

### Decision Rules

Table of **if → then** rules. Include **Stop** conditions:

```markdown
| Scope undefined | Stop; request MVP boundary |
| All items marked Must | Force relative ranking |
```

### Validation

Checklist with **≥5 measurable items** the agent must pass before delivery.

### Anti-patterns

**≥3 named mistakes** with brief explanations:

```markdown
- **Everything is P0** — no real prioritization
```

### Best Practices

Methodology-specific tips (RICE, C4, OWASP, etc.) — not generic advice.

### Output Structure

Markdown template the agent fills in. Use tables and headings.

### Next Skills

Link to related skills in the chain:

```markdown
| Need PRD | `product/prd-generator` |
```

---

## 6. Add examples.md (recommended)

At least **one worked example**:

1. **Happy path** — sample input + output excerpt  
2. **Stop condition** — what happens when input is insufficient  
3. **Anti-pattern fix** — bad output → corrected output  

See [skills/product/prd-generator/examples.md](../skills/product/prd-generator/examples.md) for reference.

---

## 7. Add README.md

Short file for GitHub browsers:

```markdown
# Feature Prioritization

RICE/ICE scoring with MVP cut line recommendation.

## Example prompt

Prioritize these features for an 8-week MVP: ...

## Chain

`product-vision-builder` → **feature-prioritization** → `prd-generator`
```

---

## 8. Validate

```bash
python scripts/validate_skills.py
```

Fix all errors before opening a PR.

Manual checklist if Python is unavailable:

- [ ] YAML frontmatter present; `name` matches folder
- [ ] All 8 sections present in order
- [ ] No *"You are…"* phrasing
- [ ] `description` contains *"Use when"*
- [ ] Body between 80–350 lines

---

## 9. Open a Pull Request

1. Push your branch to your fork  
2. Open PR against `main`  
3. Describe: what task the skill solves, which methodology it uses  
4. Maintainers will review and update `catalog.json`

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Role play prompt | Rewrite as workflow steps |
| Multiple tasks in one skill | Split into separate skills |
| Vague validation (*"be thorough"*) | Use measurable checklist items |
| Output without template | Add Output Structure section |
| Wrong `Next Skills` path | Use `category/skill-name` format |

---

## Need help?

- Read an existing skill in the same category  
- Open a [GitHub Issue](https://github.com/patonkikh/APES/issues)  
- See [CONTRIBUTING.md](../CONTRIBUTING.md)
