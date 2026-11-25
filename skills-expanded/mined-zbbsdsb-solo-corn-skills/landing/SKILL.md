---
name: landing
description: Guides users from vague ideas to clear direction through the "Doubt + Reconstruction" framework, helping users clarify their true needs and establish a clear development roadmap.
triggers:
  - "I don't know what I want to do"
  - "I have an idea but it's not clear"
  - "I want XX but I don't know exactly what I want"
  - "Help me sort this out"
  - "I want to do XX but..."
  - Any scenario requiring idea clarification
capabilities:
  - Deep exploration of user's vague ideas
  - Identifying true motivations behind surface-level needs
  - Helping users build a clear cognitive framework through questioning and reconstruction
  - Providing clear direction guidance
---

# Landing Skill

Guides users from **vague ideas** to **clear direction**.

## Core Philosophy: Doubt + Reconstruction

The **Doubt + Reconstruction** framework is the core of this skill.

### Doubt Framework

Don't rush to accept the user's first answer. Through systematic questioning:
- Question surface-level answers
- Ask "why" repeatedly until reaching the essence
- Identify contradictions and hidden assumptions
- Distinguish between "wants" and "needs"

### Reconstruction Framework

After thorough doubting, help users:
- Rebuild understanding from first principles
- Integrate fragmented ideas into systematic cognition
- Establish clear priorities
- Form actionable action plans

## Usage Guide

### When to Use

Trigger scenarios include but are not limited to:
- User expresses vague needs
- User says "I don't know what I want"
- User says "I want XX but..."
- User needs to clarify development direction
- Any scenario requiring idea clarification

### How to Use

1. **Listen actively** - Don't rush to give advice, first understand the user's true situation
2. **Apply Doubt** - Question surface answers through questioning
3. **Reconstruct** - Help users rebuild understanding from first principles
4. **Clarify** - Finally form a clear direction and action plan

### Key Questions

#### Idea Clarification
- "What do you mean by XX exactly?"
- "Why is this important to you?"
- "What happens if this problem isn't solved?"

#### First Principles
- "If you set aside existing solutions and start from scratch, how would you approach this?"
- "What is the true nature of this problem?"
- "What basic assumptions might be wrong?"

#### Direction Building
- "What is the smallest action you can take right now?"
- "Under what circumstances would you abandon this idea?"
- "Where do you want to be in three years?"

## Workflow

1. **Clarify** - Deeply understand the user's vague idea
2. **Doubt** - Systematic questioning, finding hidden contradictions
3. **Reconstruct** - Rebuild cognition from first principles
4. **Direct** - Provide clear direction and path

## References

- [Idea Clarification](references/idea-clarification/)
- [First Principles](references/first-principles/)
- [Prototyping](references/prototyping/)
- [Faith Building](references/faith-building/)
- [Direction Guidance](references/direction-guidance/)

## Notes

- Patience is the first priority, don't rush to give answers
- Doubt is for better understanding, not for negation
- Reconstruction is helping users build their own cognitive framework
- The ultimate goal is for users to find their own direction

---

## Interface Definition

### Metadata
```typescript
{
  "name": "landing",
  "version": "2.0.0",
  "description": "Guides users from vague ideas to clear direction through the Doubt + Reconstruction framework to help clarify true needs",
  "author": "SOLO CORN SKILLS",
  "category": ["clarity", "ideation"],
  "tags": ["idea", "doubt", "reconstruction", "first-principles"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "idea",
      "type": "string",
      "required": true,
      "description": "User's initial idea or problem description"
    },
    {
      "name": "background",
      "type": "string",
      "required": false,
      "description": "User's background (technical, business, fullstack, etc.)",
      "default": "fullstack"
    },
    {
      "name": "constraints",
      "type": "string",
      "required": false,
      "description": "Time or resource constraints"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "problemStatement",
      "type": "string",
      "description": "Clarified problem statement"
    },
    {
      "name": "successCriteria",
      "type": "object",
      "description": "Success criteria and validation conditions"
    },
    {
      "name": "direction",
      "type": "string",
      "description": "Clear development direction"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute "Doubt + Reconstruction" process
  // 1. Understand user's vague idea
  // 2. Systematic questioning
  // 3. Rebuild from first principles
  // 4. Return clear direction
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke landing --input '{"idea":"I want to build an AI product"}'

# Interactive invocation
scs invoke landing --interactive

# Chain invocation
scs invoke landing --then product-builder
```
