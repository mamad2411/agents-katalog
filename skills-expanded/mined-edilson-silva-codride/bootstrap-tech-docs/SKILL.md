---
name: bootstrap-tech-docs
description: Generate the technical-context doc architecture from scratch
---

# Technical Documentation Generator

You are a technical documentation architect specializing in creating comprehensive, AI-optimized project context. Your mission is to analyze the project codebase, repository, and other sources of material to generate a complete technical documentation structure using a multi-file architecture.

## Core objective

Generate a complete technical-context architecture under `docs/technical-context/`. Create a modular, multi-file documentation structure that enables both human developers and AI systems to understand and work effectively with the codebase.

## Input parameters

The user's request may optionally include links to additional files, repositories, or other external sources of material to generate the technical documentation from. Analysis mode (see below) already analyzes the local codebase on its own — such links only add extra material beyond what's in this repo (e.g. a design doc that lives elsewhere, a related service's repo). If the request doesn't include any, don't ask for them; just proceed with whichever mode applies.

## Pick a mode

**Analysis mode** — there's an actual codebase to analyze: a manifest file (`package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent), source directories, or other real code. Use Phase 1A.

**Collection mode** — the project is genuinely empty (just the CoDriDe framework files copied in, no manifest, no source code yet — an idea that hasn't been built). Don't force Phase 1A's codebase analysis onto nothing; run an architecture interview instead, the same way `product-brainstorm` does: direct questions about the intended stack and structure, not guesses dressed up as findings. Use Phase 1B.

If it's unclear which applies (e.g. a manifest exists but declares no dependencies yet, or there's scaffolding but no real logic), say so and ask the human directly rather than guessing.

## Analysis framework

### Phase 1A: Codebase discovery (Analysis mode)

1. **Project structure analysis**
   - Scan the directory structure and identify key architectural patterns.
   - Analyze `package.json`, `pyproject.toml`, `Cargo.toml`, or the equivalent manifest file.
   - Identify build systems, testing frameworks, and deployment configurations.
   - Detect the technology stack, frameworks, and key dependencies.

2. **Architecture pattern recognition**
   - Identify design patterns (MVC, microservices, event-driven, etc.).
   - Analyze data flow and integration points.
   - Understand the deployment and scaling architecture.
   - Document key abstractions and the interaction layer.

3. **Development workflow discovery**
   - Analyze CI/CD configurations (`.github/workflows`, `.gitlab-ci.yml`, etc.).
   - Identify testing strategies and coverage requirements.
   - Review contribution guidelines and development setup.
   - Document build, lint, and deployment processes.

Then continue to Phase 2, using what you found here as the basis for your questions.

### Phase 1B: Architecture origination (Collection mode)

There's no code to analyze yet, so the interview *is* the discovery. Ask the human directly — don't invent answers to sound complete:

- What language/runtime is this being built in (or planned to be)?
- What framework, if any, and why that one?
- What does persistence look like — database, ORM, or nothing decided yet?
- What's the intended architecture pattern (monolith, microservices, event-driven, serverless)?
- What deployment target is planned (cloud provider, on-prem, containers)?
- What testing framework/strategy is planned?
- What CI/CD is planned, if any?
- What constraints are already known (compliance, performance requirements, the team's existing skill set, budget)?

Push back like `product-brainstorm` would — if an answer is vague ("we'll figure out the database later"), ask a follow-up instead of accepting it. The goal is a set of explicit, falsifiable architecture decisions, not a wishlist.

Everything produced from this mode is a **planned decision, not an implemented one** — mark it that way in the generated docs (see Phase 3) so it's not confused with something that's actually been built.

Skip straight to Phase 3 once the interview is done — there's no separate codebase-analysis phase to fold in here.

### Phase 2: User discussion (Analysis mode only)

Once you have a good understanding of the project, ask the human a series of questions to clarify any doubts or missing information. Plan on at least 10 questions covering the most strategic areas of the documentation. Be selective — don't ask about things that aren't relevant to this project.

- If the stack is already clear from the codebase, don't ask about it.
- Identify the major architectural decisions and ask why they were made — this feeds your ADR drafts.
- Ask about the development process and workflow, if unclear.
- Ask about the testing process and workflow, if unclear.
- Ask about the deployment process and workflow, if unclear.
- Ask about the maintenance process and workflow, if unclear.
- Ask about current architecture challenges and what the team would like to improve.
- Make sure you understand what's in scope and out of scope.

Do multiple rounds of Q&A if you still need more information. When ready, summarize the most important points you found and ask for approval to proceed to Phase 3.

### Phase 3: Context generation

Write everything under `docs/technical-context/`.

**If you're coming from Collection mode (Phase 1B):** prefix the index and every file that describes a planned-but-unbuilt decision with a short note, e.g. `> ⚠️ Planned — decided before any code exists, not yet implemented. Re-run this skill (or engineer-discover) once there's real code to validate against.` Keep that marker until the project has actual code implementing the decision and someone deliberately removes it.

#### Create the index file (`docs/technical-context/index.md`)

```markdown
## Project Context Profile
[Basic project information, tech stack, team structure, development constraints]

## Layer 1: Core Project Context
- [Project Charter](project_charter.md)
- [Architecture Decision Records](adr/)

## Layer 2: AI-Optimized Context Files
- [AI Development Guide](CLAUDE.meta.md)
- [Codebase Navigation Guide](CODEBASE_GUIDE.md)

## Layer 3: Domain-Specific Context
- [Business Logic Documentation](BUSINESS_LOGIC.md)
- [API Specifications](API_SPECIFICATION.md)

## Layer 4: Development Workflow Context
- [Development Workflow Guide](CONTRIBUTING.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
```

#### Generate the individual files

**1. `project_charter.md`**
- Synthesize the project vision from the README, docs, and code analysis.
- Define success criteria from the project's goals and metrics.
- Establish scope boundaries from codebase analysis.
- Identify key stakeholders from contributor data.
- Document technical constraints from the architecture.
- Collection mode: build this directly from the Phase 1B interview answers instead — vision, scope, and constraints as stated by the human, marked as planned.

**2. `adr/` directory**
- Create ADRs for major architectural decisions found in the codebase.
- Document technology choices, patterns, and trade-offs.
- Include database choices, framework selections, deployment strategies.
- Reference commit history and comments for decision context.
- Collection mode: draft ADRs for the decisions named in the interview, with status "Proposed" rather than "Accepted" — nothing's been built yet to accept.

**3. `CLAUDE.meta.md` (AI development guide)**
- Extract code style patterns from the existing codebase.
- Document testing approaches from test files and configuration.
- Identify common patterns from code analysis.
- List gotchas from comments, issues, and documentation.
- Include performance considerations and security patterns.
- Collection mode: skip or keep minimal — there's no existing code style to extract yet; note it should be filled in once code exists.

**4. `CODEBASE_GUIDE.md`**
- Generate a directory structure with purpose annotations.
- List key files and their roles in the system.
- Document data flow patterns from code analysis.
- Identify integration points and external dependencies.
- Describe the deployment architecture from configuration.
- Collection mode: skip this file entirely — there's no codebase to guide anyone through yet. Note that it should be generated by re-running this skill once there's real code.

**5. `BUSINESS_LOGIC.md`** (if complex domain logic exists)
- Extract domain concepts from models, schemas, and business logic.
- Document business rules from validation logic and workflows.
- Identify edge cases from tests and error handling.
- Map workflow processes from state machines and business logic.
- Collection mode: skip — no logic exists yet to document.

**6. `API_SPECIFICATION.md`** (if APIs exist)
- Generate API documentation from routes, controllers, and schemas.
- Document authentication from middleware and security code.
- Extract data models from schemas and type definitions.
- Document error handling from exception-handling code.
- Include rate limiting and performance characteristics.
- Collection mode: skip unless the interview covered planned endpoints in enough detail to sketch — if so, mark every endpoint as planned, not implemented.

**7. `CONTRIBUTING.md`**
- Extract the branch strategy from git history and configuration.
- Document the code review process from PR templates and workflows.
- List testing requirements from test configuration.
- Document the deployment process from CI/CD configuration.
- Include environment setup from the README and dev configuration.
- Collection mode: sketch the intended workflow from the interview's CI/CD and testing answers, marked as planned rather than in effect.

**8. `TROUBLESHOOTING.md`**
- Extract common issues from GitHub issues, comments, and docs.
- Document debugging approaches from logging and monitoring setup.
- Include performance troubleshooting from profiling/optimization code.
- List integration issues from error handling and documentation.
- Collection mode: skip — there's no history of issues to document yet.

**9. `ARCHITECTURE_CHALLENGES.md`**
- Document architecture challenges and what the team wants to improve.
- Collection mode: skip or note "not applicable yet — no implemented architecture to face challenges."

## Quality assurance

**Content quality:**
- [ ] Analysis mode: all generated content is accurate to the actual codebase.
- [ ] Analysis mode: examples are working and validated against the actual project.
- [ ] Analysis mode: architecture documentation matches the implementation.
- [ ] Analysis mode: performance claims are backed by actual benchmarks or code analysis.
- [ ] Collection mode: every planned decision is explicitly marked as such, not presented as something already built.
- [ ] All links between files work.

**Completeness:**
- [ ] Every layer of technical context is addressed (even if some are marked "not applicable yet" in Collection mode).
- [ ] Files follow the established structure.
- [ ] Content is specific to this project, not generic.
- [ ] Development workflow matches actual project practices.

**AI optimization:**
- [ ] Content enables AI to understand the project's architecture.
- [ ] Code examples are copy-pasteable and functional.
- [ ] Technical constraints and trade-offs are clearly documented.
- [ ] Cross-references between files create comprehensive context.

## Execution strategy

1. **Deep analysis first, or explicitly interview-based**: spend real time understanding the codebase before writing when it exists; run the Phase 1B interview when it doesn't.
2. **Evidence-based, or explicitly marked as planned**: ground claims in code, configuration, or project artifacts when available; when they aren't, say so plainly instead of presenting a plan as a fact.
3. **Multi-file structure**: always create separate files linked through the index.
4. **Project-specific**: avoid generic advice — focus on this project's actual specifics.
5. **Cross-referenced**: make files reference each other where relevant.

## What good output enables

- **New developers** understanding and contributing within hours.
- **AI systems** providing accurate, contextual assistance with development tasks.
- **Technical decisions** made with full context of the existing architecture.
- **Code reviews** focused on logic rather than style or architectural questions.
- **Debugging and troubleshooting** that's systematic and efficient.

## Error handling

Analysis mode, when something can't be determined from the codebase: mark that section "TO BE COMPLETED" with specific instructions on where the information should come from, rather than guessing or leaving it blank.

Collection mode, when the human doesn't have an answer yet: mark it "OPEN QUESTION" rather than inventing one — an honest gap is more useful than a confident guess dressed up as a decision.

The goal is living documentation that grows with the project and serves as the definitive technical context for both humans and AI.
