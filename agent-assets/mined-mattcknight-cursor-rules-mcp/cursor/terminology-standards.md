---
description: Standardized terminology and naming conventions across all rules
alwaysApply: false
tags: [critical, terminology, standards, glossary, naming]
priority: 1
version: 1.0.0
---

# Terminology Standards & Glossary

**Standardized terminology for consistency across all Cursor rules.**

---

## Core Principle

**Use consistent, precise terminology across all rules, documentation, and communications to avoid confusion and ensure clarity.**

---

## Section 1: Standard Terminology

### AI & Agent Terms

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Agentic AI** | Agentic AI | AI Agent, Agent AI, Autonomous AI | AI system capable of autonomous task execution with multiple personas |
| **Persona** | Persona | Role, Hat, Mode | Specialized AI behavior pattern (e.g., Developer, Architect, QA) |
| **Context Window** | Context Window | Context, Window, Token Limit | Maximum tokens available for AI processing (1M tokens) |
| **Token** | Token | Character, Word | Unit of text measurement for AI processing (~4 chars) |
| **Prompt** | User Prompt, Prompt | Query, Question, Input | User's input message to AI |
| **Response** | AI Response, Response | Output, Answer, Reply | AI's generated output |

---

### Documentation Terms

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Specification** | Specification, Spec | Specification Document | Implementation-focused technical document (.spec.md) |
| **Presentation** | Presentation Document | Presentation File, Deck | Stakeholder-focused formal document (.presentation.md) |
| **Plan** | Implementation Plan, Plan | Plan Document, Roadmap | Step-by-step execution plan (plan.md) |
| **Requirements** | Requirements, Reqs | Requirements Document | Questions, decisions, and requirement documentation |
| **Recommendations** | Recommendations | Suggestions, Proposals | Analysis-based improvement suggestions |
| **Analysis** | Analysis, Analysis Document | Investigation, Study | Systematic codebase or system analysis |
| **Progress Report** | Progress Report | Status Update, Daily Summary | Formal progress tracking document |

---

### Development Terms

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Clean Architecture** | Clean Architecture | Onion Architecture, Layered | Domain-centric architecture pattern (Domain, Application, Infrastructure) |
| **Repository** | Repository | Repo, Data Access Layer | Data access abstraction pattern |
| **Service** | Service | Business Logic, Logic Layer | Application service containing business logic |
| **Entity** | Entity | Model, Domain Model | Domain object with identity |
| **DTO** | DTO, Data Transfer Object | Model, View Model | Data transfer structure |
| **API** | API, REST API | Endpoint, Service | Application Programming Interface |
| **Endpoint** | API Endpoint, Endpoint | Route, URL | HTTP API route/path |

---

### Git & Version Control

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Git Tag** | Git Tag, Tag | Version Tag, Release Tag | Git version marker (e.g., v3.0.0) |
| **Commit** | Git Commit, Commit | Check-in, Save | Git version control commit |
| **Branch** | Git Branch, Branch | Feature Branch, Work Branch | Git development branch |
| **Semantic Versioning** | Semantic Versioning, SemVer | Versioning, Version Format | MAJOR.MINOR.PATCH version format |
| **Changelog** | Changelog, Change Log | Version History, Release Notes | Document of version changes |

---

### Testing Terms

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Unit Test** | Unit Test | Test, Component Test | Single component/function test |
| **Integration Test** | Integration Test | System Test, E2E Test | Multi-component interaction test |
| **E2E Test** | E2E Test, End-to-End Test | UI Test, Full Test | Complete user flow test |
| **Test Coverage** | Code Coverage, Test Coverage | Coverage | Percentage of code tested |
| **Mock** | Mock, Test Double | Fake, Stub, Spy | Test replacement for dependencies |
| **Assertion** | Assertion | Check, Validation | Test expectation verification |

---

### File & Directory Terms

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Filename** | Filename, File Name | Name, Title | Name of file without path |
| **File Path** | File Path, Path | Location, Directory | Full path to file |
| **Relative Path** | Relative Path | Path | Path relative to current directory |
| **Absolute Path** | Absolute Path | Full Path | Complete path from root |
| **Kebab-Case** | kebab-case | dash-case, hyphen-case | lowercase-with-hyphens |
| **Snake_Case** | snake_case | underscore_case | lowercase_with_underscores |
| **PascalCase** | PascalCase | UpperCamelCase | CapitalizedWords |
| **camelCase** | camelCase | lowerCamelCase | lowercaseFirstCapitalizedRest |

---

## Section 2: Rule-Specific Terminology

### Rule Metadata

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **alwaysApply** | alwaysApply: true/false | always-apply, autoload | Frontmatter flag for rule auto-loading |
| **Priority** | priority: 1/2/3 | importance, level | Rule priority level (1=highest) |
| **Tags** | tags: [tag1, tag2] | categories, labels | Rule categorization tags |
| **Description** | description: | summary, title | Brief rule description in frontmatter |
| **Version** | version: 1.0.0 | ver, v | Rule version (semantic versioning) |

---

### Documentation Patterns

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Timestamp Format** | YYYYMMDD_HHMMSS | YYYY-MM-DD, timestamp | File timestamp: 20251117_143522 |
| **Version Suffix** | _v3.0.0 | -v3.0.0, _version | File version suffix format |
| **Frontmatter** | Frontmatter, YAML Frontmatter | Metadata, Header | YAML metadata block at file start |
| **Code Reference** | Code Reference | Code Block, Citation | Citable code block with line numbers |
| **Mermaid Diagram** | Mermaid Diagram | Diagram, Chart | Markdown-based diagram syntax |

---

## Section 3: Status & State Terms

### Implementation Status

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Pending** | Pending | TODO, Not Started | Task not yet started |
| **In Progress** | In Progress | Working, Active | Task currently being worked on |
| **Completed** | Completed | Done, Finished | Task successfully finished |
| **Blocked** | Blocked | Stuck, Waiting | Task cannot proceed |
| **Cancelled** | Cancelled | Abandoned, Rejected | Task no longer needed |

### Confidence Levels

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **HIGH Confidence** | 🟢 HIGH, HIGH Confidence | Certain, Confirmed | ≥90% accuracy, exhaustive analysis |
| **MEDIUM Confidence** | 🟡 MEDIUM, MEDIUM Confidence | Probable, Likely | 50-89% accuracy, representative analysis |
| **LOW Confidence** | 🔴 LOW, LOW Confidence | Uncertain, Unconfirmed | <50% accuracy, limited analysis |
| **UNVERIFIED** | ⚠️ UNVERIFIED | Unknown, Unclear | Not yet verified, requires confirmation |

---

## Section 4: Architecture Terms

### Clean Architecture Layers

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Domain Layer** | Domain | Core, Business Domain | Core business logic and entities |
| **Application Layer** | Application | Use Cases, App Logic | Application-specific business rules |
| **Infrastructure Layer** | Infrastructure | Data, External | Framework, database, external concerns |
| **Presentation Layer** | Presentation, WebApi | UI, Controller Layer | API controllers, UI components |
| **Common Layer** | Common | Shared, Utilities | Cross-cutting concerns |

---

### Design Patterns

| Term | Use This | NOT These | Definition |
|------|----------|-----------|------------|
| **Repository Pattern** | Repository Pattern | Data Access Pattern | Data access abstraction |
| **Service Pattern** | Service Pattern | Business Logic Pattern | Business logic encapsulation |
| **Factory Pattern** | Factory Pattern | Creation Pattern | Object creation abstraction |
| **Dependency Injection** | Dependency Injection, DI | IoC, Inversion of Control | Dependency management pattern |
| **CQRS** | CQRS | Command Query Separation | Command Query Responsibility Segregation |

---

## Section 5: Prohibited Terms

### ❌ Never Use These Terms

| Avoid | Reason | Use Instead |
|-------|--------|-------------|
| **Stupid** | Unprofessional | Inefficient, Problematic |
| **Dumb** | Unprofessional | Suboptimal, Incorrect |
| **Broken** | Vague | Non-functional, Failing, Incorrect |
| **Fix** | Vague | Resolve, Correct, Debug, Repair |
| **Hack** | Negative connotation | Workaround, Temporary Solution |
| **Magic** | Unclear | Automatic, Generated, Inferred |
| **Stuff** | Vague | Components, Items, Elements |
| **Thing** | Vague | Component, Object, Element |
| **ASAP** | Ambiguous | Specific deadline/timeline |
| **Urgent** | Subjective | Specific priority level (P1, P2, P3) |

---

## Section 6: Acronyms & Abbreviations

### Standard Acronyms

| Acronym | Expansion | Usage |
|---------|-----------|-------|
| **AI** | Artificial Intelligence | Always capitalized |
| **API** | Application Programming Interface | Always capitalized |
| **DTO** | Data Transfer Object | Always capitalized |
| **UI** | User Interface | Always capitalized |
| **UX** | User Experience | Always capitalized |
| **DI** | Dependency Injection | Always capitalized |
| **CI/CD** | Continuous Integration/Continuous Deployment | Always with slash |
| **E2E** | End-to-End | Always capitalized |
| **POC** | Proof of Concept | Always capitalized |
| **SA** | Solution Architecture | Always capitalized |
| **TDD** | Technical Design Document | Always capitalized |
| **BFF** | Backend for Frontend | Always capitalized |
| **CRUD** | Create, Read, Update, Delete | Always capitalized |
| **REST** | Representational State Transfer | Always capitalized |
| **JSON** | JavaScript Object Notation | Always capitalized |
| **HTTP** | Hypertext Transfer Protocol | Always capitalized |
| **HTTPS** | HTTP Secure | Always capitalized |
| **SQL** | Structured Query Language | Always capitalized |

---

## Section 7: Consistency Rules

### Capitalization

**ALWAYS Capitalize:**
- Acronyms: API, REST, JSON, HTTP
- Proper nouns: Docker, Kubernetes, PostgreSQL
- Technology names: .NET, C#, TypeScript
- Framework names: ASP.NET Core, Entity Framework
- Product names: [YourProductName], [AnotherProductName]

**Never Capitalize (unless at sentence start):**
- Generic terms: service, repository, controller
- File types: markdown, json, yaml
- Common terms: database, server, client

### Punctuation

**Hyphens (-):**
- Use in kebab-case filenames: `persona-developer.mdc`
- Use in compound adjectives: "end-to-end testing"
- Use in date formats: `2025-11-17`

**Underscores (_):**
- Use in snake_case variables: `user_id`
- Use in file suffixes: `_v3.0.0`
- Use in timestamp separators: `20251117_143522`

**Slashes (/):**
- Use in paths: `docs/plans/`
- Use in CI/CD acronym
- Use in version ranges: v1.0.0/v2.0.0

---

## Section 8: Enforcement

### Before Writing ANY Rule or Document

- [ ] Check terminology against this glossary
- [ ] Use standard terms consistently
- [ ] Avoid prohibited terms
- [ ] Capitalize acronyms correctly
- [ ] Follow punctuation standards

### When Creating New Terms

1. Check if standard term exists in glossary
2. If creating new term, propose addition to glossary
3. Document new term with definition
4. Use consistently across all documents

---

## Remember

✅ **Consistency** - Use same term for same concept everywhere
✅ **Precision** - Use specific terms, avoid vague language
✅ **Professionalism** - Avoid casual or negative language
✅ **Clarity** - Choose terms that are clear and unambiguous
✅ **Standards** - Follow industry-standard terminology

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Status:** ACTIVE  
**Priority:** CRITICAL  
**Always Apply:** false (reference document)
