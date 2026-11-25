---
name: dna-skill
description: "DNASkill: enterprise skill generator for turning company materials, department workflows, SOPs, policies, data schemas, and stakeholder interviews into production-ready Agent Skills. Use when the user wants to create enterprise skills, generate skills from business documents, build department-specific skills, package internal knowledge as SKILL.md, design skill generators, or validate generated skills for enterprise use."
---

# DNASkill

DNASkill turns enterprise knowledge into installable Agent Skills and helps AI
roles learn them like people learn professional skills.

Core idea: every company has an operating DNA made of departments, workflows,
policies, tools, data, and tacit expert habits. This skill extracts that DNA,
maps it to the right generator pattern, and produces a focused skill package
that an agent can actually use.

The system loop is:

```text
Learn -> Master -> Create -> Evolve
```

- **Learn**: read company sources, observe examples, and build a role-specific
  skill model.
- **Master**: practice on realistic prompts, receive feedback, and improve weak
  steps.
- **Create**: package the learned behavior into a reusable `SKILL.md` with
  references, tests, and risk controls.
- **Evolve**: keep a skill library, compare versions, reflect on failures, and
  promote only improvements.

Use this skill when the user asks for:

- enterprise skill generation
- department skill creation
- converting company docs, SOPs, policies, meeting notes, or chat history into a skill
- building a reusable skill generator
- validating whether an internal skill is ready for enterprise use
- creating 10 or more enterprise skill templates or vertical skill generators

## Non-Negotiables

1. Source-ground every company fact. Do not invent org structure, policies,
   metrics, permissions, or tool behavior. Mark assumptions explicitly.
2. Generate narrow skills. One skill should have one clear job, clear triggers,
   and a bounded operating surface.
3. Keep sensitive data out of reusable instructions. Summarize private facts,
   reference source locations, and use placeholders when preparing open-source
   examples.
4. Prefer progressive disclosure. Keep `SKILL.md` concise; move long schemas,
   policies, examples, and domain references into `references/`.
5. Validate output before handoff. A generated enterprise skill is not done
   until it has test prompts, expected outputs, risk checks, and a quality score.

## Reference Files

Load only what the current task needs:

- `references/enterprise-input-schema.md`: intake schema, source inventory,
  stakeholder interview prompts, and department mapping format.
- `references/generator-catalog.md`: the 10 enterprise generator patterns and
  when to use each one.
- `references/skill-learning-evolution.md`: research-backed evolution strategy
  for making AI roles learn, master, create, and evolve skills.
- `references/output-contract.md`: required file tree, generated `SKILL.md`
  contract, test-prompt contract, and enterprise quality rubric.
- `templates/enterprise-skill/SKILL.template.md`: starting template for a
  generated enterprise skill.
- `templates/enterprise-skill/test-prompts.template.json`: test prompt template
  for validating generated skills.

## Workflow

### Phase 1: Define The AI Role And Skill Target

Treat the generated skill as a professional capability for an AI role.

Capture:

- role name, such as support agent, sales advisor, data analyst, or compliance reviewer
- skill to learn, such as refund handling, pipeline review, policy triage, or weekly reporting
- novice behavior to avoid
- expert behavior to imitate
- practice tasks that prove the role has mastered the skill
- feedback sources: human reviewer, test prompt, tool result, policy check, or customer outcome

Use `references/skill-learning-evolution.md` when the user asks how to make the
skill improve over time or how AI roles should learn like people.

### Phase 2: Scope The Enterprise Use Case

Identify the smallest useful skill to generate.

Capture:

- company or business unit name
- target department or role
- user jobs to be supported
- input materials available now
- tools, APIs, databases, or file formats involved
- confidentiality level: public, internal, restricted, regulated
- expected output format and success criteria

If the user asks for a broad platform, split it into multiple skill generators.
Do not design a mega-skill that tries to cover the whole company.

### Phase 3: Build The Enterprise DNA Brief

Create a compact brief before writing the skill.

Use `references/enterprise-input-schema.md` when:

- documents are messy or incomplete
- multiple departments are involved
- the user wants a repeatable generation process
- the skill must preserve source traceability

The brief must include:

- source inventory with owner, freshness, sensitivity, and confidence
- department map with roles, responsibilities, systems, and decisions
- workflow map with triggers, steps, outputs, and escalation points
- vocabulary map for internal terms, acronyms, metrics, and aliases
- constraint map for permissions, compliance, brand voice, and failure modes

When data is missing, ask one short question at a time. If the user wants speed,
make a conservative assumption and label it in the brief.

### Phase 4: Select One Generator Pattern

Read `references/generator-catalog.md` and choose exactly one primary pattern.

The 10 patterns are:

1. Department Knowledge Skill
2. SOP Automation Skill
3. Customer Support Skill
4. Sales Enablement Skill
5. Onboarding And Training Skill
6. Compliance And Policy Skill
7. Data Analysis Skill
8. Workflow Integration Skill
9. Meeting And Reporting Skill
10. Decision Advisor Skill

You may include a secondary pattern only when it is clearly subordinate. Example:
a sales skill may include customer-support escalation rules, but it should still
be owned by the sales pattern.

### Phase 5: Design The Skill Package

Before editing files, outline:

- skill name in lowercase hyphen-case
- frontmatter description with clear triggers
- primary workflow phases
- required references and scripts
- expected generated outputs
- required user confirmations
- validation prompts
- known risks and fallback behavior

Use this file tree unless the repository has a stronger local convention:

```text
skill-name/
├── SKILL.md
├── references/
│   ├── domain-brief.md
│   ├── source-map.md
│   └── operating-rules.md
├── scripts/
│   └── validate-inputs.mjs
└── test-prompts.json
```

Only add scripts when deterministic checks are needed. Do not add scripts just
to make the package look more technical.

### Phase 6: Generate The Skill

Use `templates/enterprise-skill/SKILL.template.md` as the starting point.

Write the generated `SKILL.md` with:

- direct trigger conditions in frontmatter
- short operating principles
- a linear workflow
- explicit input and output contracts
- source-grounding rules
- failure handling and escalation
- validation steps

Move bulky content into references. A generated `SKILL.md` should normally stay
under 500 lines.

### Phase 7: Validate Enterprise Readiness

Use `references/output-contract.md` for the full rubric.

Minimum gate:

- frontmatter is valid and triggerable
- the skill has one owner, one primary job, and one clear user
- all company facts are grounded or marked as assumptions
- sensitive data is redacted or kept in private references
- at least three test prompts exist
- one test prompt covers the happy path
- one test prompt covers ambiguity or missing data
- one test prompt covers a restricted or risky request
- fallback behavior is explicit
- generated output can be installed as a skill without extra explanation

If the skill fails the gate, revise it before handoff.

### Phase 8: Evolve The Skill

After a generated skill is used, convert feedback into explicit learning assets.

Use the evolution loop:

1. Record the task, output, feedback, failure mode, and source ids.
2. Classify the weakness: trigger, missing source, workflow step, risk boundary,
   output format, or tool behavior.
3. Add or revise one test prompt that reproduces the weakness.
4. Update the smallest relevant instruction or reference.
5. Re-run validation and compare before/after behavior.
6. Promote the change only if the score and test output improve.

This is how DNASkill makes skills behave more like learned professional
capabilities instead of static prompts.

### Phase 9: Handoff

Return:

- generated skill path
- generator pattern used
- source materials consumed
- assumptions made
- validation score and gaps
- install command or copy path
- next two recommended enterprise skills to generate

For open-source examples, remove private company data and include synthetic
sample inputs only.

## Enterprise Quality Rubric

Score out of 100:

| Dimension | Points | What Good Looks Like |
|---|---:|---|
| Trigger clarity | 10 | The skill activates for the right enterprise requests |
| Source grounding | 15 | Facts trace back to source material or explicit assumptions |
| Workflow specificity | 15 | Steps are executable and have clear inputs and outputs |
| Department fit | 10 | Roles, tools, vocabulary, and approval paths match the team |
| Risk controls | 15 | Permission, compliance, and sensitive-data handling are explicit |
| Progressive disclosure | 10 | Core workflow is lean; details live in references |
| Test coverage | 10 | Prompts cover happy path, ambiguity, and risky requests |
| Reusability | 5 | The generated package can become a template for similar teams |
| Evolution readiness | 10 | The skill captures practice tasks, feedback, and improvement rules |

Enterprise-ready threshold: 85. Anything below 75 is a draft.

## Output Format

When generating a skill, use this response shape:

```markdown
**Generated Skill**
Path: `...`
Pattern: `...`
Primary user: `...`

**What It Does**
...

**Sources Used**
...

**Assumptions**
...

**Validation**
Score: `.../100`
Tests: `...`
Risks: `...`

**Next Generators**
1. ...
2. ...
```

## Failure Handling

- If source documents conflict, preserve both claims, cite the sources, and ask
  the user which source is authoritative.
- If the department scope is too broad, split by role or workflow.
- If the user asks to embed confidential raw data in an open-source skill, refuse
  that part and offer a redacted template.
- If tool/API behavior is unknown, write an integration placeholder and mark the
  exact missing documentation.
- If validation cannot be run, perform a dry-run review and label it as `dry_run`.

## Brand Positioning

DNASkill is the enterprise skill generator.

It turns enterprise DNA into working skills that AI roles can learn, master,
create, and evolve.
