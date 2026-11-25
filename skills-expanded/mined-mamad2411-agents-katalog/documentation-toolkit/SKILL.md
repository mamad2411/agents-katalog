---
name: documentation-toolkit
description: Consolidated toolkit for documentation. Covers documentation-templates, documentation, documentation-generation-doc-generate
---
# Documentation Toolkit

## Use this skill when
- Building documentation pipelines or automation
- Generating API, architecture, or user documentation from code
- Standardizing docs across a repository

## Do not use this skill when
- The project has no codebase or source of truth
- You cannot access code or requirements
- You only need ad-hoc explanations

## Core Capabilities
# Documentation Toolkit

# Documentation Templates

> Templates and structure guidelines for common documentation types.

---

## 1. README Structure

### Essential Sections (Priority Order)

| Section | Purpose |
|---------|---------|
| **Title + One-liner** | What is this? |
| **Quick Start** | Running in <5 min |
| **Features** | What can I do? |
| **Configuration** | How to customize |
| **API Reference** | Link to detailed docs |
| **Contributing** | How to help |
| **License** | Legal |

### README Template

```markdown
# Project Name

Brief one-line description.

## Quick Start

[Minimum steps to run]

## Features

- Feature 1
- Feature 2

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | Server port | 3000 |

## Documentation

- [API Reference](./docs/api.md)
- [Architecture](./docs/architecture.md)

## License

MIT
```

---

## 2. API Documentation Structure

### Per-Endpoint Template

```markdown
## GET /users/:id

Get a user by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | User ID |

**Response:**
- 200: User object
- 404: User not found

**Example:**
[Request and response example]
```

---

## 3. Code Comment Guidelines

### JSDoc/TSDoc Template

```typescript
/**
 * Brief description of what the function does.
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws ErrorType - When this error occurs
 * 
 * @example
 * const result = functionName(input);
 */
```

### When to Comment

| ✅ Comment | ❌ Don't Comment |
|-----------|-----------------|
| Why (business logic) | What (obvious) |
| Complex algorithms | Every line |
| Non-obvious behavior | Self-explanatory code |
| API contracts | Implementation details |

---

## 4. Changelog Template (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]
### Added
- New feature

## [1.0.0] - 2025-01-01
### Added
- Initial release
### Changed
- Updated dependency
### Fixed
- Bug fix
```

---

## 5. Architecture Decision Record (ADR)

```markdown
# ADR-001: [Title]

## Status
Accepted / Deprecated / Superseded

## Context
Why are we making this decision?

## Decision
What did we decide?

## Consequences
What are the trade-offs?
```

---

## 6. AI-Friendly Documentation (2025)

### llms.txt Template

For AI crawlers and agents:

```markdown
# Project Name
> One-line objective.

## Core Files
- [src/index.ts]: Main entry
- [src/api/]: API routes
- [docs/]: Documentation

## Key Concepts
- Concept 1: Brief explanation
- Concept 2: Brief explanation
```

### MCP-Ready Documentation

For RAG indexing:
- Clear H1-H3 hierarchy
- JSON/YAML examples for data structures
- Mermaid diagrams for flows
- Self-contained sections

---

## 7. Structure Principles

| Principle | Why |
|-----------|-----|
| **Scannable** | Headers, lists, tables |
| **Examples first** | Show, don't just tell |
| **Progressive detail** | Simple → Complex |
| **Up to date** | Outdated = misleading |

---

> **Remember:** Templates are starting points. Adapt to your project's needs.

---

# Documentation Workflow Bundle

## Overview

Comprehensive documentation workflow for generating API documentation, architecture documentation, README files, code comments, and technical content from codebases.

## When to Use This Workflow

Use this workflow when:
- Creating project documentation
- Generating API documentation
- Writing architecture docs
- Documenting code
- Creating user guides
- Maintaining wikis

## Workflow Phases

### Phase 1: Documentation Planning

#### Skills to Invoke
- `docs-architect` - Documentation architecture
- `documentation-templates` - Documentation templates

#### Actions
1. Identify documentation needs
2. Choose documentation tools
3. Plan documentation structure
4. Define style guidelines
5. Set up documentation site

#### Copy-Paste Prompts
```
Use @docs-architect to plan documentation structure
```

```
Use @documentation-templates to set up documentation
```

### Phase 2: API Documentation

#### Skills to Invoke
- `api-documenter` - API documentation
- `api-documentation-generator` - Auto-generation
- `openapi-spec-generation` - OpenAPI specs

#### Actions
1. Extract API endpoints
2. Generate OpenAPI specs
3. Create API reference
4. Add usage examples
5. Set up auto-generation

#### Copy-Paste Prompts
```
Use @api-documenter to generate API documentation
```

```
Use @openapi-spec-generation to create OpenAPI specs
```

### Phase 3: Architecture Documentation

#### Skills to Invoke
- `c4-architecture-c4-architecture` - C4 architecture
- `c4-context` - Context diagrams
- `c4-container` - Container diagrams
- `c4-component` - Component diagrams
- `c4-code` - Code diagrams
- `mermaid-expert` - Mermaid diagrams

#### Actions
1. Create C4 diagrams
2. Document architecture
3. Generate sequence diagrams
4. Document data flows
5. Create deployment docs

#### Copy-Paste Prompts
```
Use @c4-architecture-c4-architecture to create C4 diagrams
```

```
Use @mermaid-expert to create architecture diagrams
```

### Phase 4: Code Documentation

#### Skills to Invoke
- `code-documentation-code-explain` - Code explanation
- `code-documentation-doc-generate` - Doc generation
- `documentation-generation-doc-generate` - Auto-generation

#### Actions
1. Extract code comments
2. Generate JSDoc/TSDoc
3. Create type documentation
4. Document functions
5. Add usage examples

#### Copy-Paste Prompts
```
Use @code-documentation-code-explain to explain code
```

```
Use @code-documentation-doc-generate to generate docs
```

### Phase 5: README and Getting Started

#### Skills to Invoke
- `readme` - README generation
- `environment-setup-guide` - Setup guides
- `tutorial-engineer` - Tutorial creation

#### Actions
1. Create README
2. Write getting started guide
3. Document installation
4. Add usage examples
5. Create troubleshooting guide

#### Copy-Paste Prompts
```
Use @readme to create project README
```

```
Use @tutorial-engineer to create tutorials
```

### Phase 6: Wiki and Knowledge Base

#### Skills to Invoke
- `wiki-architect` - Wiki architecture
- `wiki-page-writer` - Wiki pages
- `wiki-onboarding` - Onboarding docs
- `wiki-qa` - Wiki Q&A
- `wiki-researcher` - Wiki research
- `wiki-vitepress` - VitePress wiki

#### Actions
1. Design wiki structure
2. Create wiki pages
3. Write onboarding guides
4. Document processes
5. Set up wiki site

#### Copy-Paste Prompts
```
Use @wiki-architect to design wiki structure
```

```
Use @wiki-page-writer to create wiki pages
```

```
Use @wiki-onboarding to create onboarding docs
```

### Phase 7: Changelog and Release Notes

#### Skills to Invoke
- `changelog-automation` - Changelog generation
- `wiki-changelog` - Changelog from git

#### Actions
1. Extract commit history
2. Categorize changes
3. Generate changelog
4. Create release notes
5. Publish updates

#### Copy-Paste Prompts
```
Use @changelog-automation to generate changelog
```

```
Use @wiki-changelog to create release notes
```

### Phase 8: Documentation Maintenance

#### Skills to Invoke
- `doc-coauthoring` - Collaborative writing
- `reference-builder` - Reference docs

#### Actions
1. Review documentation
2. Update outdated content
3. Fix broken links
4. Add new features
5. Gather feedback

#### Copy-Paste Prompts
```
Use @doc-coauthoring to collaborate on docs
```

## Documentation Types

### Code-Level
- JSDoc/TSDoc comments
- Function documentation
- Type definitions
- Example code

### API Documentation
- Endpoint reference
- Request/response schemas
- Authentication guides
- SDK documentation

### Architecture Documentation
- System overview
- Component diagrams
- Data flow diagrams
- Deployment architecture

### User Documentation
- Getting started guides
- User manuals
- Tutorials
- FAQs

### Process Documentation
- Runbooks
- Onboarding guides
- SOPs
- Decision records

## Quality Gates

- [ ] All APIs documented
- [ ] Architecture diagrams current
- [ ] README up to date
- [ ] Code comments helpful
- [ ] Examples working
- [ ] Links valid

## Related Workflow Bundles

- `development` - Development workflow
- `testing-qa` - Documentation testing
- `ai-ml` - AI documentation

---

# Automated Documentation Generation

You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices.

## Context
The user needs automated documentation generation that extracts information from code, creates clear explanations, and maintains consistency across documentation types. Focus on creating living documentation that stays synchronized with code.

## Requirements
$ARGUMENTS

## Safety

- Avoid exposing secrets, internal URLs, or sensitive data in docs.

## Output Format

- Documentation plan and artifacts to generate
- File paths and tooling configuration
- Assumptions, gaps, and follow-up tasks

## Resources

- `resources/implementation-playbook.md` for detailed examples and templates.

---
