---
name: recipe-task
description: Execute tasks following appropriate rules with rule-advisor metacognition
disable-model-invocation: true
---

# Task Execution with Metacognitive Analysis

Task: $ARGUMENTS

## Mandatory Execution Process

**Step 1: Rule Selection via rule-advisor (REQUIRED)**

Invoke rule-advisor using Agent tool:
- `subagent_type`: "dev-workflows:rule-advisor"
- `description`: "Rule selection"
- `prompt`: "Task: $ARGUMENTS. Select appropriate rules and perform metacognitive analysis."

**Step 2: Utilize rule-advisor Output**

After receiving rule-advisor's JSON response, proceed with:

1. **Understand Task Essence** (from `taskAnalysis.essence`)
   - Focus on fundamental purpose, not surface-level work
   - Distinguish between "quick fix" vs "proper solution"

2. **Follow Selected Rules** (from `selectedRules`)
   - Review each selected rule section
   - Apply concrete procedures and guidelines

3. **Recognize Past Failures** (from `metaCognitiveGuidance.pastFailures`)
   - Apply countermeasures for known failure patterns
   - Use suggested alternative approaches

4. **Execute First Action** (from `metaCognitiveGuidance.firstStep`)
   - Start with recommended action
   - Use suggested tools first

**Step 3: Create Task List with TaskCreate**

Register work steps using TaskCreate. Always include: first "Confirm skill constraints", final "Verify skill fidelity".

Break down the task based on rule-advisor's guidance:
- Reflect `taskAnalysis.essence` in task descriptions
- Apply `metaCognitiveGuidance.firstStep` to first task
- Restructure tasks considering `warningPatterns`
- Set appropriate priorities

**Step 4: Execute Implementation**

Proceed with task execution following:
- Selected rules from rule-advisor
- Task structure (managed via TaskCreate/TaskUpdate)
- Quality standards from applicable rules

## Important Notes

- **Execute rule-advisor first**: Mandatory metacognitive step before implementation
- **Update tasks after rule-advisor**: Reflect insights in task structure using TaskUpdate
- **Follow firstActionGuidance**: Start with recommended action
- **Monitor warningPatterns**: Watch for failure patterns throughout execution
