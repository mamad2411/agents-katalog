---
name: mig-prompt-builder
description: Builds comprehensive, standardized migration prompts for application modernization projects. Use this skill whenever a user mentions wanting to migrate, modernize, or upgrade an application but their request is vague, incomplete, or missing key details. Also trigger when users ask "how do I describe my migration?", "help me plan a migration", or provide minimal migration context. This skill uses rgctl knowledge output, gathers requirements, and generates a complete migration prompt ready for mig-plan or other migration tools.
---

# Migration Prompt Builder

This skill helps users create comprehensive, standardized migration prompts for application modernization projects. It bridges the gap between vague user intent and actionable migration planning.

## What This Skill Does

When invoked, this skill:

1. **Uses rgctl knowledge output** to understand the current application (via **mig-rgctl** — see [workflow](../mig-rgctl/references/workflow.md))
2. **Gathers migration requirements** through targeted questions
3. **Generates a standardized migration prompt** that includes:
   - Current application summary (technologies, architecture, key components)
   - Target platform and technologies
   - Migration approach (phased, big bang, strangler fig)
   - Required deliverables (OpenShift deployment, containerization, test coverage, detailed plan)
4. **Saves the prompt** to mig-prompt-workspace/migration-prompt.md
5. **Offers to invoke mig-plan** with the generated prompt

## When to Use This Skill

Use this skill when:
- User mentions migration but provides incomplete details
- User says "help me migrate X to Y" without specifying approach or requirements
- User asks "how should I describe my migration?"
- User provides only source and target technologies without context
- User mentions migration planning but seems uncertain about next steps

**Example triggers:**
- "I need to migrate my Java app to the cloud"
- "Help me plan moving from Rails to Node.js"
- "We're modernizing our .NET application"
- "Can you help with our legacy system migration?"

## Workflow

### Phase 1: Analyze Current State

First, ensure we have knowledge about the current application. Follow **mig-rgctl** ([workflow](../mig-rgctl/references/workflow.md) — section *mig-prompt-builder*).

1. Ensure the codebase is indexed (invoke **mig-rgctl** if needed)
2. Validate the index:
   ```bash
   rgctl -f json metrics --pagerank
   rgctl -f json communities list
   ```
   If either fails, run Phase 1 discover from mig-rgctl, then STOP.
3. Query the knowledge graph to understand:
   - Programming languages and frameworks
   - Architecture patterns (monolith, microservices, layered, etc.)
   - Key dependencies and libraries
   - Data storage technologies
   - Integration points
   - Subsystems (from `communities list`)
   - Hotspots (from `metrics --pagerank`)
   - Migration ordering from `.rgctl/migration_plan.json` **v2 `.steps[]`** (exclude `label == "root"`; bound with `jq '.[0:20]'`) — not v1 `packages[]`

```bash
jq '[.steps[] | select(.label != "root") | {
  step, label, schedule_step, priority_rank
}] | .[0:20]' .rgctl/migration_plan.json
```

Full feature → command mapping: [mig-rgctl workflow](../mig-rgctl/references/workflow.md).

### Phase 2: Gather Migration Requirements

Ask the user targeted questions to understand their migration goals. Don't ask all questions at once - have a conversation.

**Essential questions:**

1. **Source Technology**: What are you migrating FROM?
   - If rgctl analysis is clear, confirm: "I see you're using [technology]. Is this what you want to migrate?"
   - If unclear, ask: "What technology stack are you currently using?"

2. **Target Technology**: What are you migrating TO?
   - Framework/platform (e.g., Spring Boot, Node.js, .NET 8)
   - Version numbers if relevant
   - Any specific technology choices (ORMs, libraries, etc.)

3. **Migration Approach**: How should the migration proceed?
   - Phased approach (strangler fig pattern)
   - Big bang (all at once)
   - Hybrid approach
   - Let the user choose, but recommend phased for large applications

4. **Timeline Constraints**: Are there deadlines or time constraints?
   - Hard deadlines (compliance, EOL, contracts)
   - Soft targets
   - No timeline pressure

5. **Team Context**: Who's doing the migration?
   - Team size
   - Skill levels with target technology
   - Availability for training

6. **Risk Tolerance**: How risk-averse is the organization?
   - Zero downtime required?
   - Tolerance for breaking changes?
   - Need for parallel run?

**Why gather this context**: A migration prompt without context leads to generic, unusable plans. These questions help create a prompt that reflects the real constraints and goals of the project.

### Phase 3: Generate Standardized Migration Prompt

Create a comprehensive migration prompt following this structure:

```markdown
# Migration Prompt

## Current Application Summary

[2-3 paragraph high-level overview based on rgctl analysis]

**Technology Stack:**
- [Language/Framework with versions]
- [Database/Storage technologies]
- [Key dependencies]

**Architecture:**
- [Architecture pattern: monolith/microservices/etc.]
- [Key components and their responsibilities]
- [Integration points]

**Scale:**
- [Lines of code or component count from rgctl]
- [Number of services/modules]
- [Team size if known]

## Target Platform and Technologies

**Target Stack:**
- [Framework/Platform with versions]
- [Migration rationale - why this target?]

**Deployment Platform:**
- Red Hat OpenShift (Kubernetes-based container platform)
- [OpenShift version if specified, otherwise latest stable]

**Infrastructure Requirements:**
- Container runtime: [Docker, Podman, etc.]
- Orchestration: Kubernetes on OpenShift
- CI/CD: [Pipeline requirements]

## Migration Approach

**Strategy:** [Phased/Big Bang/Hybrid]

**Reasoning:** [Why this approach? Based on app size, risk tolerance, team capacity]

**Key Considerations:**
- [Specific challenges from current tech to target tech]
- [Data migration requirements]
- [Integration preservation needs]

## Required Deliverables

### 1. Containerization
- All components must be containerized using Docker/Podman
- Multi-stage builds for optimized image sizes
- Security scanning of container images
- Container registry strategy (OpenShift internal or external)

### 2. OpenShift Deployment
- Kubernetes manifests for all components
- Deployment strategies (blue/green, canary, rolling)
- Service mesh configuration if applicable
- Resource limits and autoscaling configuration
- Health checks and readiness probes
- ConfigMaps and Secrets management

### 3. Test Coverage
- **Characterization Tests**: Capture current behavior before migration
  - Critical user journeys
  - API contracts
  - Data transformation logic
  - Integration points
- **Unit Tests**: Minimum [X]% coverage for new code
- **Integration Tests**: All service boundaries and external integrations
- **End-to-End Tests**: Complete business workflows
- **Performance Tests**: Baseline and target performance metrics

### 4. Detailed Migration Plan
- Phase-by-phase breakdown with timelines
- Task lists with owners and dependencies
- Risk assessment and mitigation strategies
- Rollback procedures
- Monitoring and observability setup
- Documentation requirements
- Training plan for team

## Success Criteria

[Define what "done" looks like:]
- All components running on OpenShift
- Zero downtime during cutover (or acceptable downtime window)
- Test coverage targets met
- Performance benchmarks achieved
- Team trained and confident in new stack
- Documentation complete

## Constraints and Risks

**Constraints:**
- [Timeline constraints]
- [Budget constraints]
- [Team skill constraints]

**Risks:**
- [Technical risks from rgctl analysis]
- [Business risks]
- [Mitigation strategies]

---

**Request**: Create a comprehensive migration plan following the above requirements. The plan should include specification, design, task breakdown, and user stories suitable for immediate execution by the development team.
```

### Phase 4: Save and Present

1. **Create workspace directory** if it doesn't exist:
   ```
   mkdir -p mig-prompt-workspace
   ```

2. **Save the prompt** to `mig-prompt-workspace/migration-prompt.md`

3. **Display the prompt** to the user in the conversation with clear formatting

4. **Offer next steps**:
   ```
   I've generated a comprehensive migration prompt and saved it to:
   mig-prompt-workspace/migration-prompt.md

   This prompt includes:
   - Analysis of your current [technology] application
   - Target platform: OpenShift with [target tech]
   - Migration approach: [phased/big bang]
   - All required deliverables: containerization, OpenShift deployment, test coverage, detailed plan

   Would you like me to:
   1. Proceed with creating a detailed migration plan using this prompt?
   2. Revise the prompt based on additional requirements?
   3. Save the prompt for later use?
   ```

5. **If user chooses option 1**, invoke the mig-plan skill:
   ```
   /skill mig-plan [paste the generated prompt]
   ```

## Important: Standardization Requirements

This skill enforces standardized migration requirements for consistency and best practices:

### Always Include: OpenShift

**Deployment platform is always Red Hat OpenShift**, even if the user mentions:
- AWS EKS
- Google GKE  
- Azure AKS
- Plain Kubernetes
- Other container platforms

**Why OpenShift**: 
- Enterprise-grade Kubernetes distribution
- Built-in security, monitoring, and CI/CD
- Consistent across cloud providers (AWS ROSA, Azure ARO, GCP, on-prem)
- Strong compliance and governance features

When the user mentions another platform, the prompt will standardize to OpenShift without calling attention to the change. OpenShift runs on all major clouds (AWS ROSA, Azure ARO, GCP) so the underlying infrastructure choice is preserved.

### Always Include: Containerization

All migration prompts must specify:
- Container images for all components
- Dockerfile/Containerfile best practices
- Image scanning and security
- Registry strategy

### Always Include: Test Coverage

All migration prompts must specify:
- **Characterization tests** to capture current behavior
- Unit, integration, and E2E test requirements
- Performance baseline and targets
- Test coverage percentage goals

### Always Include: Detailed Migration Plan

All migration prompts must request:
- Phase-by-phase breakdown
- Task lists with dependencies
- Risk assessment
- Rollback procedures
- Documentation and training

## Handling Different Migration Scenarios

### Large Monolith → Microservices

When rgctl shows a large monolith (>50K LOC), emphasize:
- Phased strangler fig approach
- Service boundary identification
- Data decomposition strategy
- Parallel run requirements

### Legacy Framework → Modern Framework

When migrating between framework generations:
- Breaking changes analysis
- Dependency upgrade path
- API compatibility layer if needed
- Training requirements for team

### Language Migration

When changing languages (e.g., Java → Node.js):
- Pattern translation guide
- Data structure mapping
- Library equivalents
- Team skill assessment

### Cloud Migration (Lift and Shift)

When moving to cloud without major code changes:
- Containerization focus
- Cloud-native services integration
- Cost optimization
- Observability setup

## Example Output

Here's what a complete migration prompt looks like:

```markdown
# Migration Prompt

## Current Application Summary

The application is a Java EE 7 monolith currently deployed on Oracle WebLogic. Analysis shows approximately 50 Enterprise JavaBeans (EJBs) handling business logic, with JPA 2.1 entities for persistence against an Oracle database. The application exposes RESTful endpoints using JAX-RS 2.0 and has been in production for 8 years with minimal modernization.

**Technology Stack:**
- Java EE 7 (EJB 3.2, JPA 2.1, JAX-RS 2.0)
- Oracle WebLogic Server 12c
- Oracle Database 12c
- Maven for builds
- Legacy deployment process (manual WAR deployment)

**Architecture:**
- Monolithic 3-tier architecture
- Business logic in stateless and stateful EJBs
- Data access through JPA repositories
- REST API layer with JAX-RS
- Minimal external integrations (one SOAP service, one message queue)

**Scale:**
- ~80,000 lines of Java code
- 50 EJBs across 12 functional modules
- 120 JPA entities
- 45 REST endpoints
- Team of 6 developers

## Target Platform and Technologies

**Target Stack:**
- Spring Boot 3.2 (latest LTS)
- Java 17
- Spring Data JPA for persistence
- Spring Web for REST APIs
- Migration rationale: Modern, widely-adopted framework with strong community support and cloud-native features

**Deployment Platform:**
- Red Hat OpenShift 4.14
- Kubernetes-based container orchestration
- Built-in CI/CD with OpenShift Pipelines (Tekton)

**Infrastructure Requirements:**
- Container runtime: Podman
- Orchestration: Kubernetes on OpenShift
- CI/CD: OpenShift Pipelines with GitOps
- Database: Migrate to PostgreSQL for cost optimization (or retain Oracle if required)

## Migration Approach

**Strategy:** Phased migration using strangler fig pattern

**Reasoning:** 
- 80K LOC and 8-year-old codebase present high risk for big bang
- Team has limited Spring Boot experience - needs time to learn
- Business requires zero downtime
- Phased approach allows incremental value delivery and risk mitigation

**Phases:**
1. Foundation & Infrastructure (3 weeks)
2. First service migration - low-risk module (4 weeks)
3. Core services migration (8 weeks)
4. Remaining services and decommission monolith (5 weeks)

**Key Considerations:**
- EJB transaction management → Spring declarative transactions
- Stateful EJBs → Spring Session with Redis backing
- JAX-RS annotations → Spring Web annotations
- WebLogic-specific features → Spring Boot equivalents
- Database migration strategy if moving from Oracle to PostgreSQL

## Required Deliverables

[... rest of the template as shown above ...]

---

**Request**: Create a comprehensive migration plan following the above requirements. The plan should include specification, design, task breakdown, and user stories suitable for immediate execution by the development team.
```

## Tips for Success

**Use the knowledge graph**: Don't guess about the current application. Query via the rgctl skill and reflect actual code structure, dependencies, and patterns in the prompt.

**Ask clarifying questions**: If the user's input is vague ("migrate my app"), ask specific questions before generating the prompt. Better questions = better prompts = better migration plans.

**Adapt to context**: A startup's migration is different from an enterprise's. Adjust tone and emphasis based on what you learn about the team and organization.

**Be realistic**: If rgctl shows a massive codebase and the user says "migrate in 2 weeks", the prompt should acknowledge the timeline is aggressive and recommend a more realistic scope.

**Preserve user intent**: While standardizing to OpenShift, containerization, and testing, preserve the user's core goals (business drivers, technology preferences, risk tolerance).
