---
name: skill-development
version: 1.0.0
description: Design, build, validate, and deploy new skills for the agent skill library
uses:
  - analysis/research
  - planning/strategic-planning
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:write
    - skill:create
  requires_approval: true
---

# Skill Development

Design, build, validate, and deploy new skills for the agent skill library. Each skill is a single cognitive capability with two artifacts: SKILL.md (agent instructions) and tool.yaml (machine-readable contract).

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `develop_skill` is invoked, you (the agent) follow the methodology below to create a complete, validated skill. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `meta/skill-development` in its skill list.

## When to Use

- A new cognitive capability is needed that no existing skill covers
- An existing skill needs to be split (too coarse) or merged (too fine)
- Adapting a domain-specific process into a domain-agnostic skill
- Expanding the skill library to cover gaps in the cognitive loop (Perceive → Analyze → Plan → Synthesize → Execute → Communicate → Reflect)

## Methodology

### 1. Define the Capability

Before writing anything, answer these questions:

- **What cognitive capability does this skill represent?** (one clear sentence)
- **What category does it belong to?** (analysis, planning, synthesis, communication, execution, meta)
- **What triggers its use?** (when should an agent activate this skill?)
- **What does it produce?** (what's the output — a document, a decision, a plan, an action?)
- **What does it NOT do?** (boundaries prevent scope creep)

**Granularity check:**
- If it takes fewer than 3 sentences to describe → too fine, consider merging with an existing skill
- If it takes more than a paragraph → too coarse, consider splitting
- One skill = one cognitive capability

### 2. Research Existing Patterns

Before building, investigate:

- **Existing skills**: Read SKILL-SPEC.md and 2-3 existing skills to absorb the format, tone, and conventions
- **Framework constraints**: Read the loader (`src/os/tools/loader.py`) and executor (`src/os/tools/executor.py`) to understand what the framework parses and how it routes
- **Dependencies**: Identify which existing skills this one `uses:` and which skills might `use:` this one
- **Domain literature**: What established methodologies exist for this capability? (e.g., analytical frameworks for analysis, planning methodologies for planning)

### 3. Design the Tool Interface

Define the tool.yaml contract first — this is the external API:

- **Tool name**: `snake_case`, action-oriented (e.g., `research_query`, `analyze`, `create_plan`)
- **Parameters**: What inputs does the skill need? For each:
  - Type, description, required/optional, defaults, enums where appropriate
  - Required parameters = minimum needed to produce useful output
  - Optional parameters = controls for customization
- **Handler type**: `agent` for cognitive skills (no backing code)
- **Config defaults**: What settings should be overridable via the 5-layer hierarchy?

**Parameter design rules:**
- Every parameter must earn its place — if the skill works fine without it, make it optional or remove it
- Use enums for constrained choices (frameworks, formats, detail levels)
- Provide sensible defaults so minimal invocations produce useful results
- Required parameters should be 1-3 maximum

### 4. Write the SKILL.md

Structure the instructions following this template:

```markdown
---
name: [skill-name]
version: 1.0.0
description: [One line — used for discovery, ~50 tokens max]
uses: [dependency skills]
requires:
  tools: []
  env: []
security:
  risk_level: [read|write|execute|admin]
  capabilities: []
  requires_approval: [true|false]
---

# [Skill Name]

[One-paragraph description of what this skill does.]

## Execution Model
[State this is agent-handled, explain how invocation works.]

## When to Use
[Trigger conditions — 4-6 bullet points.]

## Methodology
### 1. [First Step]
### 2. [Second Step]
...
[The core teaching. Imperative voice. Domain-neutral examples.]

## Output Format
[Template showing expected structure.]

## Quality Criteria
[5-8 bullet points — how to evaluate output.]

## Common Mistakes
[Poka-yoke — 5-8 bullets preventing frequent errors.]

## Completion
[How to know when done — 4-6 checkable criteria.]
```

**Writing rules:**
- **Imperative voice**: "Identify the scope" not "The agent should identify the scope"
- **Domain-neutral**: Examples span multiple domains (healthcare, finance, engineering, security)
- **No provider lock-in**: Never reference specific LLM APIs, models, or provider features
- **Concrete over abstract**: Specific steps over general principles
- **Poka-yoke**: Every "Common Mistakes" entry should correspond to a real failure mode observed or anticipated

### 5. Write the tool.yaml

```yaml
name: [skill-name]
version: 1.0.0
description: [Brief description matching SKILL.md]

tools:
  - name: [tool_name]
    description: |
      [Multi-line description. Must include:]
      - What the tool does
      - When to use it
      - That it's agent-handled (no backing code)
      - What it returns
    input_schema:
      type: object
      properties:
        [parameters]
      required:
        [required params]

handler:
  type: agent
  # [Comment explaining routing semantics]

config:
  defaults:
    [overridable settings with sensible defaults]

security:
  risk_level: [read|write]
  requires_approval: [true|false]
```

### 6. Validate

Run this checklist before considering the skill complete:

**Format validation:**
- [ ] SKILL.md has valid YAML frontmatter (name, version, description, uses, requires, security)
- [ ] SKILL.md has all required sections (Execution Model, When to Use, Methodology, Output Format, Quality Criteria, Common Mistakes, Completion)
- [ ] tool.yaml has valid YAML (name, version, description, tools, handler, config, security)
- [ ] tool.yaml handler type is `agent` (for cognitive skills)
- [ ] tool.yaml has `config.defaults` section with overridable settings
- [ ] Tool name matches between SKILL.md references and tool.yaml definition

**Content validation:**
- [ ] Description is one line, under 50 tokens
- [ ] Methodology uses imperative voice throughout
- [ ] No domain-specific jargon or examples (or examples span multiple domains)
- [ ] No provider-specific references (no "Claude", "GPT", "Anthropic API")
- [ ] Common Mistakes section has 5+ entries
- [ ] Quality Criteria are checkable (not vague)
- [ ] Dependencies in `uses:` are correct (no cycles, referenced skills exist)

**Framework validation:**
- [ ] `discover_tools()` parses the tool.yaml without errors
- [ ] `get_skill_instructions()` loads the SKILL.md without errors
- [ ] Executor returns a clean delegation response for `handler: type: agent`
- [ ] Existing test suite passes (no regressions)

### 7. Deploy

1. Create the skill directory: `skills/<category>/<skill-name>/`
2. Write SKILL.md and tool.yaml
3. Copy to agent-coordinator: `.os/skills/<category>/<skill-name>/`
4. Run loader verification
5. Run test suite
6. Add skill to relevant agent identity.yaml files
7. Verify end-to-end through agent integration test

## Output Format

```
## Skill: [name]

### Capability
[One sentence description]

### Category
[category/skill-name]

### Files Created
- `skills/<category>/<skill-name>/SKILL.md` — [char count] chars, [section count] sections
- `skills/<category>/<skill-name>/tool.yaml` — tool: [tool_name], [param count] params

### Tool Interface
- Tool: [tool_name]
- Required params: [list]
- Optional params: [list]
- Handler: agent
- Config defaults: [count] overridable settings

### Dependencies
- Uses: [list or "none"]
- Used by: [list or "none yet"]

### Validation
- [ ] Format: [pass/fail]
- [ ] Content: [pass/fail]
- [ ] Framework: [pass/fail]
- [ ] Tests: [pass/fail]
```

## Quality Criteria

- Skill represents a single, clearly defined cognitive capability
- Tool interface has 1-3 required parameters and sensible defaults
- SKILL.md methodology is step-by-step, imperative, and domain-neutral
- Common Mistakes section reflects real failure modes (not generic advice)
- Config defaults cover all hardcoded values that users might want to override
- Skill passes all format, content, and framework validation checks
- Existing test suite shows no regressions after deployment

## Common Mistakes

- **Skipping the research step**: Every new skill should start by reading 2-3 existing skills to absorb conventions. Format drift is the #1 quality killer.
- **Wrong handler type**: Cognitive skills use `handler: type: agent`, not `builtin`. Builtin implies there's backing code in the executor — if there isn't, the tool call will error at runtime.
- **Missing config defaults**: Every hardcoded value in the skill (depth levels, scales, thresholds, formats) should appear in `config.defaults` so it's overridable without editing SKILL.md.
- **Too many required parameters**: If the tool needs 5 required params to produce anything useful, the interface is too complex. Aim for 1-3 required, rest optional with defaults.
- **Vague methodology**: "Analyze the situation" is not a methodology step. "Apply the 5 Whys framework: state the problem, ask why 5 times, verify the root cause" is.
- **Missing Execution Model section**: Without it, users and agents don't understand whether this tool has backing code or is agent-executed.
- **Forgetting the framework test**: Writing the files is not enough. Run `discover_tools()`, `get_skill_instructions()`, and the test suite. The loader may reject malformed YAML silently.
- **Creating skills that are too fine**: A single function call (e.g., "format a date") is not a skill. A skill is a cognitive capability that requires methodology.
- **Hardcoded provider or model in agent identity**: Agent identity.yaml files should set `llm.provider: null` and `llm.model: null` so the 5-layer config hierarchy resolves them. Hardcoding ties the agent to a specific provider and breaks portability.
- **No poka-yoke**: If the Common Mistakes section is empty or generic, it won't prevent errors. Every entry should correspond to a specific, observed failure.

## Completion

Skill development is complete when:
- The capability is clearly defined and doesn't overlap with existing skills
- SKILL.md and tool.yaml are written and follow all format conventions
- All validation checks pass (format, content, framework)
- The skill is deployed to the agent-coordinator and the loader parses it correctly
- The executor returns a clean delegation response for the tool
- The existing test suite passes with no regressions
- The skill is documented in the output format above
