---
name: solo-corn-research-integration
description: Integrates 50 years of cross-disciplinary academic research to extract actionable insights and mental models, helping solo founders think and act like they have an expert team. Use this skill when users need strategic decision support, thinking frameworks, analysis tools, learning acceleration, or seek academic research support.
---

# Research Integration Skill

Provides AI with cross-disciplinary research insights and mental models to help users grow.

## Core Capabilities

1. **Research Knowledge Retrieval**: Retrieves most relevant research insights and mental models based on problem context
2. **Mental Model Application**: Provides 20+ structured thinking tools
3. **Insight Composition Engine**: Automatically combines multiple insights to form analytical frameworks
4. **Practical Case Library**: Provides real-world application examples

## Five Core Research Areas

This skill integrates 50 years of research in the following five areas:

- **AI/ML**: Artificial Intelligence and Machine Learning
- **Entrepreneurship**: Entrepreneurship and Innovation Management
- **Automation/HCI**: Automation and Human-Computer Interaction
- **Organizational Behavior**: Organizational Behavior and Team Collaboration
- **Software Engineering**: Software Engineering and Product Development

## Quick Start

### 1. Retrieve Research Insights

When users ask questions, automatically identify relevant areas and retrieve:

```
User: "How should I validate my startup idea?"
→ Retrieve Lean Startup, Effectuation, customer development theories
→ Recommend applicable mental models: Lean Canvas, MVP Framework
→ Provide practical advice and examples
```

### 2. Apply Mental Models

Recommend appropriate thinking tools based on problem type:

- **Strategic Decisions** → First Principles, Second-Order Thinking, SWOT
- **Product Design** → User Journey Map, Minimum Viable Product
- **Growth Optimization** → AARRR Funnel, North Star Metric
- **Organization Management** → OKRs, Team Topologies

### 3. Compose Analytical Frameworks

For complex problems, combine multiple models:

```
Market Entry Decision
= Porter's Five Forces (Industry Analysis)
+ SWOT (Competitive Positioning)
+ Lean Canvas (Hypothesis Validation)
+ Unit Economics (Financial Viability)
```

## Directory Structure

```
research-integration/
├── SKILL.md (this file)
└── references/
    ├── ai-ml/                    # AI/ML Area
    │   ├── foundational-papers.md
    │   ├── key-insights.md
    │   └── mental-models.md
    ├── entrepreneurship/         # Entrepreneurship Area
    │   ├── foundational-papers.md
    │   ├── key-insights.md
    │   └── mental-models.md
    ├── automation-hci/           # Automation/HCI Area
    │   ├── foundational-papers.md
    │   ├── key-insights.md
    │   └── mental-models.md
    ├── organizational-behavior/  # Organizational Behavior Area
    │   ├── foundational-papers.md
    │   ├── key-insights.md
    │   └── mental-models.md
    └── software-engineering/     # Software Engineering Area
        ├── foundational-papers.md
        ├── key-insights.md
        └── mental-models.md
```

## Usage Patterns

### Pattern 1: On-Demand Loading (Recommended)

When needing to dive deep into an area:

1. View `references/<area>/foundational-papers.md`
2. Read relevant insights in `key-insights.md`
3. Apply mental models from `mental-models.md`

### Pattern 2: Proactive Recommendation

Proactively recommend based on user questions:

```
User question → Identify area → Retrieve insights → Recommend models → Provide examples
```

### Pattern 3: Composed Application

For complex problems:

```
1. Decompose problem dimensions
2. Select appropriate models for each dimension
3. Combine to form complete analytical framework
4. Provide implementation suggestions
```

## Mental Model Library (20+)

### Decision-Making Models
- First Principles Thinking
- Second-Order Thinking
- Inversion Thinking
- Map Is Not the Territory
- Minimize Surprises

### Strategic Analysis Models
- SWOT Analysis
- Porter's Five Forces
- Ansoff Matrix
- PEST Analysis

### Product & Growth Models
- Lean Canvas
- Business Model Canvas
- AARRR Funnel
- North Star Metric
- User Journey Map

### Organization Management Models
- OKR Framework
- Team Topologies
- MTF Analysis
- Unit Economics

## Best Practices

1. **Framework Before Details**: Recommend models first, then dive into insights
2. **Theory + Practice**: Pair every theory with examples
3. **Explicit Limitations**: Label inapplicable scenarios
4. **Continuous Updates**: Iterate based on user feedback

## Trigger Keywords

This skill automatically activates when:
- "how to make decisions"
- "what analysis methods"
- "market analysis"
- "business model"
- "learn XX theory"
- "thinking frameworks"
- "user growth strategy"
- "product development methods"
- "team management"
- "strategic planning"

## Limitations & Notes

1. **Knowledge Cutoff**: This skill is based on public research before 2024
2. **Area Coverage**: Primarily focuses on business and technology areas
3. **Cultural Adaptation**: Some models may need adjustment for local markets
4. **Update Frequency**: Core insights are stable, examples need regular updates

## Extension Suggestions

To extend this skill:
1. Add new research areas to `references/`
2. Add papers and insights in existing format
3. Add new models in `mental-models.md`
4. Update usage guide in this file

## Related Skills

- **Product Development Skill**: Apply theories from this skill to specific products
- **Marketing Growth Skill**: Combine with marketing research insights
- **Decision Support Skill**: Deepen decision framework application

---

## Interface Definition

### Metadata
```typescript
{
  "name": "research-integration",
  "version": "2.0.0",
  "description": "Integrates 50 years of cross-disciplinary academic research for actionable insights",
  "author": "SOLO CORN SKILLS",
  "category": ["research", "insights"],
  "tags": ["research-integration", "mental-models", "academic-insights"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "question",
      "type": "string",
      "required": true,
      "description": "Question or problem to research"
    },
    {
      "name": "area",
      "type": "string",
      "required": false,
      "description": "Research area (ai-ml, entrepreneurship, automation-hci, organizational-behavior, software-engineering)"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "insights",
      "type": "array",
      "description": "Relevant research insights and findings"
    },
    {
      "name": "models",
      "type": "array",
      "description": "Applicable mental models"
    },
    {
      "name": "framework",
      "type": "object",
      "description": "Composed analytical framework"
    },
    {
      "name": "examples",
      "type": "array",
      "description": "Practical application examples"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute research integration
  // 1. Analyze question and identify relevant areas
  // 2. Retrieve research insights from knowledge base
  // 3. Select and apply appropriate mental models
  // 4. Compose analytical framework
  // 5. Return results with examples
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke research-integration --input '{"question": "How to validate my startup idea"}'

# Interactive mode
scs invoke research-integration --interactive

# With specific area
scs invoke research-integration --input '{"question": "Team management", "area": "organizational-behavior"}'
```
