---
name: methodology-parser
description: "Parses methodology sections from skill SKILL.md files. Extracts mandatory/optional steps, success criteria, can_skip_if conditions. Used by task-decomposer to generate sprint backlog from caller skill methodology."
---

# Methodology Parser

Парсит `<!-- methodology -->` секции из других skills для использования в decomposition.

## Когда применять

- Когда task-decomposer работает с caller skill который имеет methodology
- Перед decomposition - извлечь structure из caller's methodology

## Methodology section format

```markdown
<!-- methodology:start -->
## Methodology checklist

### Phase 1: Discovery
- name: Read existing artifacts
  mandatory: yes
  can_skip_if: project has no docs/
  success_criteria: at least 1 artifact read or absence confirmed
  effort: XS

- name: Detect language stack
  mandatory: yes
  can_skip_if: never
  success_criteria: language-detection.json saved
  effort: XS

### Phase 2: Analysis
- name: Static analysis
  mandatory: yes
  can_skip_if: depth=quick
  success_criteria: tooling-output saved or fallback documented
  effort: M
<!-- methodology:end -->
```

## Parsing

### 1. Find methodology block

```bash
# Extract content between markers
sed -n '/<!-- methodology:start -->/,/<!-- methodology:end -->/p' SKILL.md
```

### 2. Parse phases

Phases identified by `### Phase N:` pattern.

### 3. Parse steps within phase

Each step:
- Starts с `- name:` line
- Followed by indented properties

```yaml
# Parsed structure:
steps:
  - name: "Read existing artifacts"
    mandatory: yes
    can_skip_if: "project has no docs/"
    success_criteria: "at least 1 artifact read or absence confirmed"
    effort: XS
    phase: "Phase 1: Discovery"
```

### 4. Validate parsed structure

Each step must have:
- `name` (string)
- `mandatory` (yes / no)
- `success_criteria` (string)

Optional:
- `can_skip_if` (condition string)
- `effort` (XS / S / M / L)
- `phase` (auto-populated from heading)

If step missing mandatory fields - log warning, skip step.

### 5. Output

Return structured data:

```python
{
    "skill_name": "architecture-audit",
    "phases": [
        {
            "name": "Phase 1: Discovery",
            "steps": [
                {
                    "name": "Read existing artifacts",
                    "mandatory": True,
                    "can_skip_if": "project has no docs/",
                    "success_criteria": "at least 1 artifact read or absence confirmed",
                    "effort": "XS"
                },
                ...
            ]
        },
        ...
    ]
}
```

## Use by task-decomposer

task-decomposer применяет parsed methodology как baseline:

```python
def decompose_with_methodology(scope, methodology, context):
    if methodology and methodology.phases:
        # Use phases as sprint baseline
        sprints = []
        for phase in methodology.phases:
            sprint = create_sprint_from_phase(phase, context)
            tasks = [
                create_task_from_step(step, context)
                for step in phase.steps
            ]
            sprint.tasks = tasks
            sprints.append(sprint)
        return sprints
    else:
        # Generic decomposition without methodology
        return generic_decompose(scope, context)
```

Per step decomposed task получает:
- `title` from step.name
- `description` derived from step.success_criteria
- Initial AC from success_criteria
- Effort estimate from step.effort
- Mandatory/optional based on step.mandatory

## Methodology без явных secций

Some skills могут описать methodology в prose, не в structured block. В этом случае:

- methodology-parser возвращает empty result
- task-decomposer applies generic decomposition
- Caller skill author может add structured methodology later для better integration

## Multi-phase support

Methodology может иметь:
- Single flat list of steps (no phases)
- Multiple phases with steps each

Parser handles both:
- Если no `### Phase` headings - all steps в "default" phase
- Если phases - structured как above

## Conditional steps

Steps с `can_skip_if` conditions:

Common conditions:
- `depth=quick` - skipped в quick mode
- `project has no docs/` - skipped if directory absent
- `never` - never skippable (mandatory always)
- Custom logic - decomposer evaluates

Parser doesn't evaluate conditions - just stores them. task-decomposer applies в context.

## Backward compatibility

Skills без methodology section:
- Parser returns empty
- task-decomposer falls back to generic decomposition
- Skills work fine - just без structured integration

## Example

For sdlc-audit's `architecture-audit` skill, methodology section:

```markdown
<!-- methodology:start -->
## Methodology checklist

### A1. Read existing ADRs
- name: Read existing ADRs
  mandatory: yes
  can_skip_if: project has no docs/
  success_criteria: at least 1 ADR read or absence confirmed
  effort: XS

### A2. Static analysis
- name: Static dependency analysis
  mandatory: yes
  can_skip_if: depth=quick
  success_criteria: tooling output saved (pydeps/madge/go list)
  effort: M

### A3. Reverse-engineer C4
- name: C4 model reverse-engineering
  mandatory: no
  can_skip_if: depth not deep
  success_criteria: c4-inferred.md created with 3 levels
  effort: L
<!-- methodology:end -->
```

Parsed:
```yaml
skill: architecture-audit
phases:
  - name: "A1. Read existing ADRs"
    steps:
      - name: "Read existing ADRs"
        mandatory: true
        can_skip_if: "project has no docs/"
        success_criteria: "at least 1 ADR read or absence confirmed"
        effort: XS
  - name: "A2. Static analysis"
    steps:
      - name: "Static dependency analysis"
        mandatory: true
        can_skip_if: "depth=quick"
        success_criteria: "tooling output saved (pydeps/madge/go list)"
        effort: M
  - name: "A3. Reverse-engineer C4"
    steps:
      - name: "C4 model reverse-engineering"
        mandatory: false
        can_skip_if: "depth not deep"
        success_criteria: "c4-inferred.md created with 3 levels"
        effort: L
```

task-decomposer создаёт sprint из этих phases с appropriate tasks.

## Output

Returns structured data to caller (task-decomposer).
Не creates own files.
