---
name: collector
description: Decision framework engine that serves as the central coordination hub for skill selection, context synthesis, and multi-domain problem decomposition. Analyzes user requests and orchestrates appropriate skills to generate optimal solutions.
triggers:
  - "complex tasks requiring multiple skills"
  - "ambiguous or multi-faceted requests"
  - "deciding which approach to take"
  - "coordinating different expertise areas"
  - "systematic problem analysis and planning"
  - "skill selection and orchestration"
  - "meta-cognitive analysis and reflection"
capabilities:
  - Skill routing and selection based on task characteristics
  - Multi-domain problem decomposition
  - Context-aware decision making using decision frameworks
  - Skill orchestration and result synthesis
  - Meta-cognitive reflection on reasoning processes
  - Integration with knowledge bases for reference materials
---

# Collector Skill

## Overview

The **Collector** skill serves as the **decision-making hub** within the Solo skill ecosystem. It implements a sophisticated decision framework engine that orchestrates skill selection, synthesizes contextual information, and coordinates multi-domain problem solving.

## Core Functionality

### Decision Framework Engine

The Collector implements a systematic decision-making approach based on established decision science principles:

1. **Problem Identification**: Analyze user requests to understand core objectives, constraints, and success criteria
2. **Framework Selection**: Choose appropriate decision frameworks based on task characteristics
3. **Option Generation**: Decompose problems and generate multiple solution paths
4. **Analysis and Evaluation**: Apply structured analysis using selected frameworks
5. **Synthesis and Integration**: Combine results from multiple skills into coherent solutions

### Skill Orchestration

The Collector acts as a conductor, coordinating various specialized skills:

- **Skill Selection**: Evaluates task requirements and selects the most appropriate skills
- **Execution Planning**: Determines skill invocation order and dependencies
- **Result Aggregation**: Synthesizes outputs from multiple skills into unified solutions
- **Quality Assurance**: Validates that combined results meet overall objectives

## Usage Guidelines

### When to Invoke the Collector

The Collector skill should be activated when:

- User requests involve complex, multi-faceted problems
- Task requirements are ambiguous or not clearly specified
- Multiple skill domains need to be coordinated
- Systematic decision-making frameworks are needed
- Meta-cognitive analysis and reflection are beneficial

### How the Collector Works

1. **Request Analysis**: Collector examines the user's request to identify:
   - Primary objectives and goals
   - Implicit requirements and constraints
   - Success criteria and quality standards
   - Available resources and limitations

2. **Framework Application**: Based on analysis, Collector applies:
   - Decision trees for structured choice problems
   - Analytical hierarchy processes for multi-criteria decisions
   - Domain-specific frameworks from reference materials
   - Custom frameworks for novel problem types

3. **Skill Coordination**: Collector orchestrates:
   - Sequential skill invocations for dependent tasks
   - Parallel skill executions for independent subtasks
   - Result aggregation and conflict resolution
   - Iterative refinement cycles as needed

4. **Solution Delivery**: Collector provides:
   - Structured solutions aligned with user objectives
   - Clear explanation of decision rationale
   - Supporting evidence and reference materials
   - Actionable recommendations and next steps

## Integration with Other Skills

The Collector leverages specialized skills through coordinated invocation:

- **Domain Skills**: Execute specific technical tasks (code generation, analysis, etc.)
- **Framework Skills**: Provide structured methodologies for particular problem types
- **Reference Skills**: Access knowledge bases and documentation
- **Integration Skills**: Coordinate cross-domain solutions

## Meta-Cognitive Functions

The Collector includes meta-cognitive capabilities:

- **Self-Reflection**: Analyzes its own reasoning processes
- **Bias Detection**: Identifies potential cognitive biases in decision-making
- **Framework Evaluation**: Assesses appropriateness of selected frameworks
- **Continuous Improvement**: Adapts decision strategies based on outcomes

## References and Resources

The Collector's decision-making is informed by:

- `references/core-philosophy.md`: Foundational decision science principles
- `references/frameworks/`: Domain-specific decision frameworks
- `references/skill-mapping/`: Mapping between task types and optimal skills
- `references/meta-cognition/`: Meta-cognitive analysis methodologies
- `references/documentation/`: Integration guides and API references
- `references/integration/`: Cross-skill coordination protocols

## Best Practices

1. **Clear Objective Definition**: Ensure user objectives are well-understood before skill selection
2. **Framework Appropriateness**: Match decision frameworks to problem characteristics
3. **Transparent Reasoning**: Document decision rationale for user understanding
4. **Adaptive Refinement**: Iterate on solutions based on intermediate results
5. **Quality Validation**: Verify that final solutions meet all requirements

## Evolution and Learning

The Collector continuously improves through:

- Accumulated experience from past decisions
- Feedback integration from solution outcomes
- Framework refinement based on effectiveness analysis
- Expansion of skill mapping knowledge
- Enhancement of meta-cognitive capabilities

---

**Role**: Central Decision Hub | **Type**: Orchestration & Coordination

---

## Interface Definition

### Metadata
```typescript
{
  "name": "collector",
  "version": "2.0.0",
  "description": "Decision framework engine and central coordination hub for skill selection and orchestration",
  "author": "SOLO CORN SKILLS",
  "category": ["orchestration", "decision"],
  "tags": ["skill-routing", "problem-decomposition", "decision-framework"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "request",
      "type": "string",
      "required": true,
      "description": "User's original request or problem statement"
    },
    {
      "name": "context",
      "type": "string",
      "required": false,
      "description": "Additional context about the situation"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "analysis",
      "type": "object",
      "description": "Problem analysis and decomposition"
    },
    {
      "name": "skillPlan",
      "type": "object",
      "description": "Skill selection and orchestration plan"
    },
    {
      "name": "recommendations",
      "type": "array",
      "description": "Actionable recommendations and next steps"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute decision framework
  // 1. Request analysis and problem identification
  // 2. Framework selection and application
  // 3. Skill selection and orchestration
  // 4. Synthesis and solution delivery
  // 5. Return results
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke collector --input '{"request": "I need to build a product"}'

# Interactive mode
scs invoke collector --interactive

# With additional context
scs invoke collector --input '{"request": "Startup idea", "context": "SaaS for project management"}'
```
