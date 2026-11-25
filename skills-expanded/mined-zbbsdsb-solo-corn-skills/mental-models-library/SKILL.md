---
name: Mental Models Library
description: A comprehensive thinking toolkit providing cognitive frameworks and mental models for better decision-making, problem-solving, and strategic reasoning.
category: thinking-toolkit
version: 1.0.0
tags:
  - mental-models
  - decision-making
  - critical-thinking
  - cognitive-frameworks
  - problem-solving
  - strategy
  - reasoning
  - rationality
---

# Mental Models Library

## Overview

The Mental Models Library is a curated collection of cognitive frameworks designed to enhance thinking quality across diverse domains. It serves as a practical reference for navigating complex problems, making better decisions, and understanding the world more clearly.

## Purpose

This skill provides:

- **Quick Reference**: Fast access to essential mental models when needed
- **Deep Understanding**: Comprehensive explanations of why each model works
- **Practical Application**: Clear guidance on when and how to apply each model
- **Cross-Domain Coverage**: Models spanning decision-making, strategy, systems thinking, psychology, and execution

## Architecture

```
mental-models/
├── SKILL.md                    # This file - skill overview and index
├── core-philosophy.md          # Foundation - why mental models matter
└── references/
    ├── decision-reasoning/     # Models for clear thinking and choice
    ├── strategy-competition/    # Frameworks for competitive advantage
    ├── systems-complexity/     # Understanding interconnected systems
    ├── psychology-behavior/    # Human behavior and cognition models
    ├── execution-learning/     # Implementation and improvement
    ├── navigation/             # Life decisions and direction
    ├── combinations/           # Using multiple models together
    ├── templates/              # Application frameworks and checklists
    └── integration/            # Meta-frameworks for model selection
```

## Core Principles

1. **Falsifiability**: Prefer models with clear conditions for failure
2. **Multi-Perspective**: Use multiple models for important decisions
3. **Appropriateness**: Match model complexity to problem complexity
4. **Probabilistic Thinking**: Embrace uncertainty and update beliefs
5. **Second-Order Thinking**: Consider consequences of consequences

## Quick Start

For immediate use:

1. **Identify the Problem Type**:
   - Decision under uncertainty → See `decision-reasoning/`
   - Competitive dynamics → See `strategy-competition/`
   - Complex systems behavior → See `systems-complexity/`
   - Understanding people → See `psychology-behavior/`
   - Execution and improvement → See `execution-learning/`
   - Life and career choices → See `navigation/`

2. **Select Relevant Models**: Browse the appropriate category
3. **Apply and Combine**: Use multiple models for robust analysis
4. **Review and Iterate**: Update mental models based on outcomes

## Model Categories

### Decision & Reasoning
Frameworks for clearer thinking and better choices:
- Probabilistic thinking
- Inversion
- First principles
- Occam's razor
- Hanlon's razor

### Strategy & Competition
Tools for understanding competitive dynamics:
- Game theory basics
- Comparative advantage
- Moat theory
- Two-sided markets
- Disruption patterns

### Systems & Complexity
Understanding interconnected phenomena:
- Feedback loops
- Emergence
- Network effects
- Stocks and flows
- Punctuated equilibrium

### Psychology & Behavior
Models of human cognition and behavior:
- Cognitive biases
- Motivation mechanisms
- Social dynamics
- Emotional influences
- Behavioral patterns

### Execution & Learning
Frameworks for action and improvement:
- OODA loops
- PDCA cycles
- Deliberate practice
- Feedback systems
- Experimentation

## Usage Guidelines

### When to Use Mental Models

- Facing important decisions with uncertain outcomes
- Analyzing complex problems with multiple variables
- Trying to understand others' behavior or motivations
- Planning strategy or evaluating competitive positions
- Learning from successes or failures
- Seeking to improve thinking quality

### How to Use This Library

1. **Recognition**: Identify patterns in your situation
2. **Selection**: Choose relevant models from the library
3. **Application**: Apply models systematically to your context
4. **Integration**: Combine models for richer understanding
5. **Validation**: Test predictions against outcomes

### Model Selection Heuristic

| Situation | Primary Models |
|-----------|----------------|
| Uncertain decision | Probabilistic thinking, Bayes, Expected value |
| Complex problem | Systems thinking, First principles |
| Understanding people | Psychology-behavior models |
| Competitive situation | Game theory, Strategy frameworks |
| Implementation challenge | Execution-learning frameworks |
| Life decisions | Navigation models |

## Quality Standards

All mental models in this library are evaluated against:

- **Explanatory Power**: Does it explain real-world phenomena?
- **Predictive Accuracy**: Does it generate useful predictions?
- **Actionable Guidance**: Can it inform better decisions?
- **Boundary Conditions**: Where does it break down?
- **Complementary Models**: What does it not cover?

## Maintenance

This library is a living resource. Models are:
- Regularly reviewed for accuracy and relevance
- Updated with new examples and applications
- Enhanced with cross-references and combinations
- Extended with emerging research and frameworks

## Related Skills

- **Critical Thinking**: General reasoning and analysis
- **Strategic Planning**: Long-term planning frameworks
- **Systems Design**: Building complex systems
- **Leadership**: Applying models in organizational contexts

## References

This library draws from diverse sources:
- Decision science and behavioral economics
- Game theory and competitive strategy
- Systems theory and complexity science
- Cognitive psychology and neuroscience
- Philosophy of science and epistemology
- Military strategy and tactics

---

## Interface Definition

### Metadata
```typescript
{
  "name": "mental-models",
  "version": "2.0.0",
  "description": "Comprehensive thinking toolkit with 45+ cognitive frameworks",
  "author": "SOLO CORN SKILLS",
  "category": ["thinking", "frameworks"],
  "tags": ["mental-models", "decision-making", "cognitive-frameworks"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "situation",
      "type": "string",
      "required": true,
      "description": "Situation or problem to think about"
    },
    {
      "name": "category",
      "type": "string",
      "required": false,
      "description": "Model category (decision-reasoning, strategy-competition, systems-complexity, psychology-behavior, execution-learning)"
    },
    {
      "name": "specificModel",
      "type": "string",
      "required": false,
      "description": "Specific model to use (e.g., first-principles, swot-analysis)"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "models",
      "type": "array",
      "description": "Recommended mental models with explanations"
    },
    {
      "name": "application",
      "type": "object",
      "description": "How to apply the models to your situation"
    },
    {
      "name": "insights",
      "type": "array",
      "description": "Key insights from model application"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute mental model selection and application
  // 1. Analyze situation and identify problem type
  // 2. Select relevant models from library
  // 3. Provide model explanations and context
  // 4. Guide application to user's situation
  // 5. Return results with insights
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke mental-models --input '{"situation": "Making a major career decision"}'

# Interactive mode
scs invoke mental-models --interactive

# With specific category or model
scs invoke mental-models --input '{"situation": "Competitive strategy", "category": "strategy-competition"}'
scs invoke mental-models --input '{"situation": "My problem", "specificModel": "first-principles"}'

# Also available via scs models commands
scs models list
scs models show first-principles
scs models search "decision"
```

---

*Last Updated: 2026-05-26*
*Version: 2.0.0*
