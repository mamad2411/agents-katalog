# Skill Template: [Skill Name]

Replace `[Skill Name]` with skill name (e.g., "Code Quality Analyzer", "Performance Baseline Validator").

---

## Skill Definition

### Purpose
[One sentence: What does this skill do? E.g., "Analyzes Python code for code quality metrics (complexity, coverage, style violations)."]

### Category
- [ ] Shared (can be used by any role/agent)
- [ ] Role-Specific (belongs to `skills/{role}/SKILL.md`)

## Input Specification

### What This Skill Needs

**Format**:
[File type or data format. E.g., "Python source files (*.py)" or "JSON configuration"]

**Content**:
```
[Example input, e.g., Python code or JSON structure]
```

**Size Limit**:
[E.g., "Up to 50KB of code", "Max 1000 lines"]

## Output Specification

### What This Skill Produces

**Format**:
[Output format. E.g., "JSON", "Markdown", "CSV"]

**Schema**:
```json
{
  "status": "success | warning | error",
  "findings": [
    {
      "type": "string",
      "severity": "low | medium | high | critical",
      "location": "string (file:line)",
      "message": "string",
      "fix": "string (optional)"
    }
  ],
  "summary": "string",
  "recommendations": ["string"]
}
```

**Example Output**:
```json
{
  "status": "warning",
  "findings": [
    {
      "type": "high_complexity",
      "severity": "medium",
      "location": "app/api.py:42",
      "message": "Function has cyclomatic complexity of 8 (target: <5)",
      "fix": "Extract conditional logic into helper functions"
    }
  ],
  "summary": "3 issues found; 2 medium, 1 low",
  "recommendations": ["Refactor high-complexity functions", "Add type hints"]
}
```

## Model Configuration

**Recommended Model**: [claude-opus | sonnet-4-6 | haiku-4]  
**Rationale**: [Why this model? E.g., "Sonnet for good balance of speed and accuracy; Opus for complex analysis."]

**Token Budget**:
- **Input**: [E.g., 4000 tokens]
- **Output**: [E.g., 2000 tokens]

## Invocation Details

### How This Skill Is Called

[Code example or pseudo-code. E.g., how agents invoke this skill]

```
// Example: Invoke via CLI
sdlc skill code-quality-analyzer --file=app/api.py

// Example: Invoke from agent
agent.invokeSkill('code-quality-analyzer', {
  source_files: workItem.attachments,
  config: loadConfig('stack/rules/coding-conventions.md')
})
```

## Used By

List agents or stages that invoke this skill:

- **Agent**: `agents/[category]/[agent-name]-agent.md` (Stage N: purpose)
- **Agent**: `agents/[category]/[agent-name]-agent.md` (Stage N: purpose)

Example:
- **Backend Engineer Agent** (Stage 09: Code review)
- **QA Agent** (Stage 06: QA validation)

## Related Skills

[Other skills that might be used together, e.g., "Often paired with performance-baseline-validator"]

---

## Example Workflow

1. Agent loads code from work item attachment
2. Calls `code-quality-analyzer` skill with Python code
3. Skill returns findings (complexity, test coverage, linting)
4. Agent presents findings to user
5. User decides: (1) Proceed  (2) Fix first  (3) Defer

---

**Created**: [YYYY-MM-DD]  
**Last Updated**: [YYYY-MM-DD]  
**Governed By**: AI-SDLC Platform
