---
name: strategic-decision
description: Strategic decision-making engine that provides structured frameworks for business strategy, competitive positioning, market analysis, and long-term planning. Integrates business model design, competitive strategy, market analysis, and strategic planning to help organizations make high-stakes decisions.
triggers:
  - "business strategy"
  - "competitive strategy"
  - "market analysis"
  - "strategic planning"
  - "business model design"
  - "competitive positioning"
  - "long-term decision"
  - "strategic direction"
capabilities:
  - Business model design and analysis
  - Competitive strategy formulation
  - Market analysis and opportunity assessment
  - Strategic planning and roadmap development
  - Decision frameworks for high-stakes choices
  - Integration with other skills for execution
---

# Strategic Decision Skill

## Overview

The **Strategic Decision** skill provides a comprehensive framework for making high-stakes strategic decisions. It integrates principles from business strategy, competitive analysis, market dynamics, and organizational planning to help decision-makers navigate complex environments with confidence.

## Core Functionality

### Strategic Decision Framework

The skill implements a structured approach to strategic decision-making:

1. **Problem Framing**: Define the strategic challenge, objectives, and constraints
2. **Context Analysis**: Analyze market, competitive, and organizational context
3. **Option Generation**: Develop multiple strategic alternatives
4. **Evaluation & Selection**: Apply decision frameworks to choose the best path
5. **Planning & Execution**: Translate decisions into actionable roadmaps
6. **Monitoring & Adaptation**: Track outcomes and adjust strategies as needed

### Key Capabilities

- **Business Model Innovation**: Design and validate new business models
- **Competitive Strategy**: Formulate strategies to create and sustain competitive advantage
- **Market Opportunity Assessment**: Identify and evaluate market opportunities
- **Strategic Planning**: Develop long-term strategic plans and roadmaps
- **Decision Quality**: Ensure decisions are well-reasoned and robust

## Usage Guidelines

### When to Invoke

The Strategic Decision skill should be activated when:
- Defining or revising business strategy
- Entering new markets or launching new products
- Making major investment decisions
- Reorganizing or restructuring the organization
- Responding to competitive threats or market disruptions
- Setting long-term strategic direction

### How It Works

1. **Context Gathering**: Collect relevant data about market, competitors, and organization
2. **Framework Application**: Apply appropriate strategic frameworks (Porter's 5 Forces, SWOT, etc.)
3. **Option Development**: Generate multiple strategic alternatives
4. **Decision Making**: Evaluate options using structured criteria
5. **Plan Development**: Create detailed implementation plans
6. **Execution Support**: Coordinate with other skills for tactical execution

## Integration with Other Skills

- **Collector**: For problem decomposition and skill orchestration
- **Landing**: For clarifying strategic objectives and direction
- **Product Builder**: For translating strategy into product execution
- **Marketing Growth**: For go-to-market strategy execution
- **Research Integration**: For evidence-based decision making

## References and Resources

- `references/core-philosophy.md`: Foundational strategic thinking principles
- `references/business-model/`: Business model frameworks and tools
- `references/competitive-strategy/`: Competitive strategy methodologies
- `references/market-analysis/`: Market analysis techniques
- `references/strategic-planning/`: Strategic planning processes
- `references/playbooks/`: Practical strategy playbooks
- `references/integration/`: Integration with other skills and tools

## Best Practices

1. **Clear Objectives**: Define clear strategic objectives before analysis
2. **Data-Driven**: Base decisions on evidence, not just intuition
3. **Multiple Perspectives**: Consider diverse viewpoints and alternatives
4. **Long-Term Focus**: Balance short-term needs with long-term goals
5. **Adaptability**: Build flexibility to respond to changing conditions

---

**Role**: Strategic Decision Engine | **Type**: Strategy & Planning

---

## Interface Definition

### Metadata
```typescript
{
  "name": "strategic-decision",
  "version": "2.0.0",
  "description": "Strategic decision engine providing structured frameworks for business strategy, competitive positioning, market analysis, and long-term planning",
  "author": "SOLO CORN SKILLS",
  "category": ["strategy", "planning"],
  "tags": ["strategy", "decision", "business-model", "market-analysis"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "plan",
      "type": "string",
      "required": true,
      "description": "Plan, strategy, or product specification document"
    },
    {
      "name": "mode",
      "type": "string",
      "required": false,
      "description": "Validation mode (quick-validation, technical-validation, market-analysis, etc.)",
      "default": "quick-validation"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "validationResult",
      "type": "object",
      "description": "Complete validation result including ratings and recommendations"
    },
    {
      "name": "technicalSpec",
      "type": "string",
      "description": "Technical specification document (if in technical validation mode)"
    },
    {
      "name": "marketAnalysis",
      "type": "object",
      "description": "Market analysis results (if in market analysis mode)"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute strategic decision process
  // 1. Problem framing
  // 2. Context analysis
  // 3. Option generation
  // 4. Evaluation and selection
  // 5. Planning and execution
  // 6. Return results
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke strategic-decision --input '{"plan":"My product plan", "mode":"quick-validation"}'

# Interactive invocation
scs invoke strategic-decision --interactive

# Chain invocation
scs invoke product-builder --then strategic-decision
```
