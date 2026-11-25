---
name: product-builder
description: Provides end-to-end product development support from idea conception to code implementation. Guides solo entrepreneurs through every stage of building software products including validation, specification, frontend/backend development, testing, deployment, and documentation. Use this skill when users want to build a digital product from scratch.
---

# Product Builder Skill

A comprehensive AI skill that transforms ideas into deployable products efficiently.

## Core Capabilities

1. **Idea Validation**: Market analysis, competitor landscape, feasibility assessment
2. **Specification Generation**: PRD creation, user stories, acceptance criteria
3. **Wireframe & UI Design**: Component design and layout guidance
4. **Frontend Development**: React, Vue, Next.js component generation
5. **Backend Development**: REST/GraphQL API generation
6. **Database Design**: Schema design and migration scripts
7. **Test Generation**: Unit, integration, and E2E tests
8. **Deployment**: CI/CD configuration and deployment guides
9. **Documentation**: API docs, README, and user guides

## Development Phases

The product building workflow follows these phases:

```
Phase 1: Idea Validation
    ↓
Phase 2: Product Specification
    ↓
Phase 3: UI/UX Design
    ↓
Phase 4: Frontend Development
    ↓
Phase 5: Backend Development
    ↓
Phase 6: Database Implementation
    ↓
Phase 7: Testing
    ↓
Phase 8: Deployment
    ↓
Phase 9: Documentation
```

## Quick Start

### 1. Validate Your Idea

```
User: "I want to build a task management app for remote teams"
→ Market analysis: Size, trends, growth potential
→ Competitor analysis: Who else is doing this?
→ Feasibility assessment: Technical and business viability
→ Idea scoring: Overall recommendation
```

### 2. Generate Specification

```
User: "Help me create a spec for my task app"
→ PRD document with goals and requirements
→ User stories for each feature
→ Acceptance criteria
→ Wireframe descriptions
```

### 3. Generate Code

```
User: "Generate React components for my task app"
→ Component structure and props
→ Production-ready code
→ Tailwind CSS styling
→ Unit tests
```

## Directory Structure

```
product-builder/
├── SKILL.md (this file)
└── references/
    ├── idea-validation/       # Phase 1 resources
    ├── specification/         # Phase 2 resources
    ├── ui-design/            # Phase 3 resources
    ├── frontend/             # Phase 4 resources
    ├── backend/              # Phase 5 resources
    ├── database/             # Phase 6 resources
    ├── testing/              # Phase 7 resources
    ├── deployment/           # Phase 8 resources
    └── documentation/        # Phase 9 resources
```

## Supported Technologies

### Frontend
- React 18+
- Vue 3+
- Next.js 13+
- Tailwind CSS 3+
- TypeScript

### Backend
- Node.js / Express
- Python / FastAPI
- GraphQL (Apollo Server)
- Authentication (JWT, OAuth)

### Database
- PostgreSQL
- MongoDB
- SQLite
- Prisma ORM

### Deployment
- Vercel
- Netlify
- AWS (ECS, Lambda)
- Docker

## Usage Patterns

### Pattern 1: Complete Workflow
Follow the full development lifecycle from idea to deployment.

### Pattern 2: Specific Phase
Jump directly to any phase if you already have completed previous work.

### Pattern 3: Code Generation Only
Generate specific components or APIs on-demand.

## Best Practices

1. **Start with validation**: Always validate your idea before coding
2. **Iterate incrementally**: Build incrementally and test frequently
3. **Follow standards**: Generated code follows industry best practices
4. **Review and adapt**: Review generated code and adapt to your needs
5. **Document as you go**: Maintain documentation throughout development

## Trigger Keywords

This skill activates when users mention:
- "build a product"
- "create an app"
- "develop software"
- "generate code"
- "validate my idea"
- "create PRD"
- "deploy my project"
- "write tests"

## Related Skills

- **Research Integration**: Validate ideas using research-backed frameworks
- **Marketing Growth**: Plan go-to-market strategy
- **Customer Success**: Design user support workflows

---

## Interface Definition

### Metadata
```typescript
{
  "name": "product-builder",
  "version": "2.0.0",
  "description": "Provides end-to-end product development support from idea to code implementation",
  "author": "SOLO CORN SKILLS",
  "category": ["product", "development"],
  "tags": ["product", "development", "prd", "code-generation"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "problem",
      "type": "string",
      "required": true,
      "description": "The problem to solve or product idea"
    },
    {
      "name": "constraints",
      "type": "string",
      "required": false,
      "description": "Constraints (tech stack, time, resources, etc.)"
    },
    {
      "name": "targetUsers",
      "type": "string",
      "required": false,
      "description": "Target user description"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "prdDocument",
      "type": "string",
      "description": "Complete product requirements document"
    },
    {
      "name": "userStories",
      "type": "array",
      "description": "List of user stories"
    },
    {
      "name": "acceptanceCriteria",
      "type": "array",
      "description": "Acceptance criteria"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute product development process
  // 1. Validate idea
  // 2. Generate specifications
  // 3. Design UI
  // 4. Develop code
  // 5. Return results
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke product-builder --input '{"problem":"I want to build a task management app"}'

# Interactive invocation
scs invoke product-builder --interactive

# Chain invocation
scs invoke landing --then product-builder
```
