---
name: c4-methodology
description: "C4 model methodology for software architecture documentation. Use when deciding which C4 diagram level to create, when scoping architecture diagrams by audience, when ensuring cross-level consistency between C4 diagrams, when extracting architecture from a TypeScript monorepo into C4 abstractions, when mapping hexagonal architecture layers to C4 vocabulary, or when reviewing C4 diagrams for correctness. Use when a user asks about C4 modeling concepts, abstraction levels, element types, or diagramming best practices. Use when planning a set of architecture diagrams that need to work together across multiple levels of detail."
---

## When to use this skill

- Deciding which C4 abstraction level (Context, Container, Component, Code) fits the question
- Scoping a C4 diagram: which elements to include, which to exclude
- Ensuring consistency when multiple C4 diagrams exist at different levels
- Extracting C4 architecture from an existing TypeScript monorepo codebase
- Mapping hexagonal/clean architecture concepts (ports, adapters, graph, runtime) to C4 vocabulary
- Reviewing or validating C4 diagrams for methodology compliance
- Planning a complete set of architecture diagrams for a specification or ADR
- Understanding when to use supplementary diagrams (System Landscape, Dynamic, Deployment)

---

# C4 Model Methodology

The C4 model is a hierarchical approach to software architecture diagramming created by Simon Brown. It provides four core levels of abstraction, each answering different questions for different audiences. "C4" stands for Context, Containers, Components, and Code.

## The Four Core Levels

### Level 1: System Context Diagram (C1)

| Attribute | Detail |
|-----------|--------|
| **Scope** | A single software system and its environment |
| **Primary elements** | The software system in scope |
| **Supporting elements** | People (users, actors) and other software systems that interact directly |
| **Audience** | Everyone: developers, architects, product owners, stakeholders, operations |
| **Question answered** | "What is this system and who/what does it interact with?" |

**Recommendations**:
- Start every architecture documentation effort here
- Keep it simple: typically 5-15 elements maximum
- Show the system as a single box — no internal details
- Include ALL direct external dependencies (APIs, databases owned by other teams, SaaS services)
- Use clear, non-technical descriptions that stakeholders can understand

### Level 2: Container Diagram (C2)

| Attribute | Detail |
|-----------|--------|
| **Scope** | A single software system's internal high-level building blocks |
| **Primary elements** | Containers within the software system |
| **Supporting elements** | People and external software systems (from C1) |
| **Audience** | Developers, architects, DevOps engineers |
| **Question answered** | "What are the major technical building blocks and how do they communicate?" |

**Recommendations**:
- Show separately deployable/runnable units (web apps, APIs, databases, message queues, file systems)
- Always include technology choices (e.g., "React SPA", "Node.js API", "PostgreSQL")
- Show communication protocols between containers (HTTP, gRPC, SQL, AMQP)
- This is the most commonly useful diagram level for development teams

### Level 3: Component Diagram (C3)

| Attribute | Detail |
|-----------|--------|
| **Scope** | A single container's internal components |
| **Primary elements** | Components within one container |
| **Supporting elements** | Other containers and external systems that components interact with |
| **Audience** | Developers working on or integrating with the container |
| **Question answered** | "What are the major structural building blocks inside this container?" |

**Recommendations**:
- Create only for containers that warrant this level of detail
- Show logical groupings of related functionality (not individual classes)
- In hexagonal architecture: ports, adapter groups, use case groups, domain services
- Typically 10-20 components maximum before it becomes noise
- Not every container needs a C3 diagram

### Level 4: Code Diagram (C4)

| Attribute | Detail |
|-----------|--------|
| **Scope** | A single component's implementation classes/interfaces |
| **Primary elements** | Code elements (classes, interfaces, functions, types) |
| **Supporting elements** | Other code elements the component depends on |
| **Audience** | Developers working directly on the component |
| **Question answered** | "How is this component implemented at the code level?" |

**Recommendations**:
- Rarely create manually — auto-generate from IDE or tools if needed
- Only for complex components that need explanation (e.g., a state machine, a complex algorithm)
- Use standard UML class diagrams or ER diagrams at this level
- If the code is clean, this diagram is often redundant

## Supplementary Diagram Types

### System Landscape Diagram

| Attribute | Detail |
|-----------|--------|
| **Scope** | The entire enterprise/organization |
| **Primary elements** | All software systems and people in the enterprise |
| **Audience** | Enterprise architects, CTOs, stakeholders |
| **Question answered** | "What software systems exist across our organization?" |

Use when you need to show how multiple software systems relate to each other across an organization.

### Dynamic Diagram

| Attribute | Detail |
|-----------|--------|
| **Scope** | Any level (C1-C3) |
| **Primary elements** | Elements from any static diagram, but shown with numbered interactions |
| **Audience** | Developers, architects |
| **Question answered** | "How do elements collaborate at runtime to fulfill a specific use case?" |

Use when a static diagram cannot show the runtime flow clearly. Similar to a UML sequence diagram but uses C4 elements. Interactions are numbered to show order.

### Deployment Diagram

| Attribute | Detail |
|-----------|--------|
| **Scope** | One or more software systems mapped to infrastructure |
| **Primary elements** | Deployment nodes (servers, containers, cloud services, execution environments) |
| **Supporting elements** | Container instances deployed to nodes |
| **Audience** | DevOps, SREs, architects |
| **Question answered** | "How are containers mapped to infrastructure in a given environment?" |

Use when you need to document the deployment topology. Create separate diagrams for different environments (dev, staging, production) if they differ significantly.

---

## Element Types and Definitions

### Person

A human user of the software system. Can be a specific individual role or persona.

- Represents: End users, administrators, operators, external developers
- NOT: Service accounts, bots (model these as software systems)
- Notation: Stick figure or person shape
- Label: Name + description of role

### Software System

The highest level of abstraction. A software system delivers value to its users.

- Represents: Your application, an external SaaS, a legacy system, a partner API
- Granularity: Something that has its own development team, deployment pipeline, or is a distinct product
- Label: Name + high-level description of purpose

### Container

**A container is a separately runnable/deployable unit that executes code or stores data.** This is NOT a Docker container. The term predates Docker and describes a runtime boundary.

Examples of containers:
- Server-side web applications (Node.js Express API, Java Spring Boot app)
- Client-side web applications (React SPA, Angular app)
- Mobile applications (iOS app, Android app)
- Desktop applications (Electron app)
- Databases (PostgreSQL, MongoDB, Redis)
- Message queues (RabbitMQ, Kafka)
- File systems (S3 bucket, local filesystem)
- Serverless functions (AWS Lambda, Azure Functions)
- Shell scripts, batch processes

A container is NOT:
- A code module or package (that's a Component)
- A Docker container (that's deployment infrastructure)
- A namespace or folder structure

Label: Name + technology + description

### Component

A grouping of related functionality encapsulated behind a well-defined interface. In practice, a component is a logical grouping of code within a container.

Examples of components:
- A set of related classes/modules behind a facade
- A feature module or package in a monorepo
- A port or adapter in hexagonal architecture
- A domain service or use case handler
- A data access layer

Label: Name + technology + description

### Deployment Node

Infrastructure where containers run. Can be nested to show hierarchical infrastructure.

Examples: AWS region > availability zone > EC2 instance > Docker runtime, or Kubernetes cluster > namespace > pod.

---

## Abstraction Level Selection Guide

Choose the diagram level based on who needs it and what question they have:

| Audience | Question | Level |
|----------|----------|-------|
| Stakeholders, PMs | "What does this system do?" | C1 (Context) |
| New team members | "What are the major pieces?" | C2 (Container) |
| Developers joining a team | "How is this service structured?" | C3 (Component) |
| Developers in the code | "How does this algorithm work?" | C4 (Code) |
| Enterprise architects | "What systems exist?" | System Landscape |
| Anyone | "How does request X flow through the system?" | Dynamic |
| DevOps, SREs | "Where does this run in production?" | Deployment |

**Rule of thumb**: Start at C1 and only go deeper if the audience's question demands it. Most projects need C1 + C2. Add C3 only for complex containers. Rarely create C4 manually.

---

## Scoping Rules

### One Primary Element Per Diagram

Each C4 diagram focuses on ONE primary element:
- C1: one software system
- C2: one software system (showing its containers)
- C3: one container (showing its components)
- C4: one component (showing its code)

### Focal vs. Supporting Elements

- **Focal elements**: The elements being detailed (shown with full borders, internal structure)
- **Supporting elements**: External elements that interact with focal elements (shown as simple boxes, grayed out or lighter styling)

### Boundary Conventions

- Use boundaries (dashed rectangles) to group related elements
- Label boundaries with scope: "Enterprise", "Software System: X", "Container: Y"
- Don't nest boundaries beyond 2 levels deep in a single diagram
- External systems sit OUTSIDE all boundaries

### What to Include

Include an element if:
1. It has a direct relationship with a focal element, OR
2. It provides essential context for understanding the focal element's role

Exclude an element if:
1. It has no direct relationship with any focal element
2. Including it adds visual noise without answering the diagram's question

---

## Cross-Level Consistency

When maintaining diagrams at multiple levels, ensure traceability:

### C1 to C2 Traceability

- Every software system in C1 that is "yours" should have a corresponding C2 diagram
- External systems in C1 must appear as the same external systems in C2
- People in C1 must appear connecting to the same containers in C2
- If C1 shows "System A -> System B", then C2 for System A must show at least one container with an outbound relationship to System B

### C2 to C3 Traceability

- Each container shown in C2 that warrants detail should have a corresponding C3 diagram
- External containers and systems in C3 must match what appears in C2
- Inter-container relationships in C2 must be traceable to specific component-level relationships in C3

### Relationship Consistency

- If C1 says "uses HTTPS", C2 must show the specific containers communicating over HTTPS
- Technology labels must be consistent across levels (don't say "REST" in C1 and "gRPC" in C2 for the same relationship)
- Relationship directions must be consistent across levels

### Naming Consistency

- Element names must be identical across all diagrams where they appear
- Use the same capitalization, abbreviations, and terminology everywhere
- If a system is called "Auth Service" in C1, it must be "Auth Service" in C2, C3, and Dynamic diagrams

---

## Notation Conventions

### Element Labels

Every element box should contain:
1. **Name**: The element's name (bold or prominent)
2. **Type/Technology**: The element type and technology choice (e.g., "[Container: Node.js]")
3. **Description**: A brief description of the element's responsibility

### Relationship Labels

Every line/arrow should include:
1. **Description**: What the relationship represents ("Makes API calls to", "Reads/writes data")
2. **Technology** (for container-level and below): The protocol or technology ("HTTPS", "SQL", "gRPC")

### Color Usage

The C4 model does not mandate specific colors, but consistency is critical. Within this project, use:

| Element Type | Background | Border | Usage |
|-------------|-----------|--------|-------|
| Person | `#08427b` (dark blue) | `#073B6F` | Human actors |
| Internal System | `#1168bd` (blue) | `#0B4884` | Systems you own |
| External System | `#999999` (gray) | `#6B6B6B` | Systems you don't own |
| Container | `#438dd5` (medium blue) | `#2E6295` | Runtime units within your system |
| Container (DB) | `#438dd5` | `#2E6295` | Database containers (cylinder shape) |
| Component | `#85bbf0` (light blue) | `#5D82A8` | Logical groupings within a container |
| Deployment Node | `#ffffff` (white) | `#888888` | Infrastructure nodes |

### Legend Requirement

**Every C4 diagram must include a legend** (key) that explains the meaning of shapes, colors, border styles, line types, and arrow directions used. Mermaid C4 diagrams auto-generate a legend; for other tools, add one manually.

---

## Best Practices

1. **Start with Context (C1)**: Always create the System Context diagram first. It forces clarity about system scope and external dependencies.

2. **Use consistent naming across levels**: An element called "Payment Service" in C1 must be called "Payment Service" everywhere.

3. **Include technology choices at C2+**: Containers and components must specify their technology stack ("Node.js + Express", "PostgreSQL 15", "React 18").

4. **Label every relationship**: Unlabeled arrows are ambiguous. Always include what the relationship represents and (at C2+) what technology/protocol it uses.

5. **Keep diagrams focused**: Each diagram answers ONE question. If you're trying to show everything, you're showing nothing.

6. **Use supplementary diagrams for behavior**: Static C1-C3 diagrams show structure. Use Dynamic diagrams to show how elements collaborate for specific use cases.

7. **Document deployment separately**: Don't mix logical architecture (C1-C3) with physical deployment. Use Deployment diagrams for infrastructure mapping.

8. **Review with the intended audience**: A C1 diagram should make sense to stakeholders. If it requires developer knowledge to understand, it's too detailed.

9. **Update diagrams when architecture changes**: Stale diagrams actively mislead. Treat diagram updates as part of the definition of done.

10. **Keep element counts manageable**: C1: 5-15 elements. C2: 5-20 containers. C3: 5-20 components. If you exceed these, split into multiple diagrams.

## Anti-Patterns

1. **The "everything diagram"**: A single diagram showing all systems, containers, components, and code. This communicates nothing effectively.

2. **Missing technology labels**: Showing containers without specifying "Node.js" or "PostgreSQL" makes the diagram useless for technical decisions.

3. **Inconsistent naming**: Calling something "Auth Service" in one diagram and "Authentication System" in another creates confusion.

4. **Unlabeled relationships**: Arrows without labels are ambiguous. "Uses" is better than nothing. "Makes API calls using HTTPS" is best.

5. **Docker containers confused with C4 containers**: A C4 Container is a runtime boundary (web app, database), not a Docker container.

6. **Component = class**: Components are logical groupings, not individual classes. If your C3 has 50+ components, you've gone too granular.

7. **Skipping C1/C2**: Jumping straight to C3 without context diagrams. Readers need the big picture before they can understand details.

8. **Mixing abstraction levels**: Showing containers and components in the same diagram at the same visual weight. Use supporting elements with lighter styling.

9. **No boundaries**: Failing to use boundary boxes to group related elements. Boundaries provide essential visual organization.

10. **Aesthetic over accuracy**: Making the diagram "pretty" at the expense of correctness. An accurate ugly diagram is better than a beautiful misleading one.

---

## Code Extraction: TypeScript Monorepo Patterns

When extracting C4 architecture from this monorepo codebase:

### Mapping hex-di Architecture to C4

| Codebase Concept | C4 Level | C4 Element |
|-----------------|----------|------------|
| The entire monorepo | C1 | Software System ("hex-di") |
| `pnpm-workspace.yaml` packages | C2 | Containers (for independently deployable ones) or Components (for library packages) |
| Workspace packages (`packages/*`, `libs/*`) | C2/C3 | Containers (if deployed separately) or Components (if library dependencies) |
| `src/` modules within a package | C3 | Components |
| Ports (`@hex-di/core` port definitions) | C3 | Component interfaces |
| Adapters (e.g., `logger-pino`) | C3 | Components implementing port interfaces |
| Runtime (`@hex-di/runtime`) | C3 | The composition root component |
| External npm packages | C1/C2 | External Software Systems or External Containers |

### Extraction Workflow

1. **Read `pnpm-workspace.yaml`** to discover all workspace packages
2. **Read `package.json`** in each package to find:
   - Package name and description (C4 element name and description)
   - Dependencies (C4 relationships)
   - Technology (Node.js, TypeScript version, framework)
3. **Read `src/index.ts`** (or main entry) to find:
   - Public API surface (what the package exports)
   - Major module groupings (potential C3 components)
4. **Trace imports** to map:
   - Inter-package dependencies (C2 relationships)
   - Intra-package module dependencies (C3 relationships)
5. **Identify hex-arch layers**:
   - Ports: files defining interfaces/types with no implementation dependencies
   - Adapters: files importing external libraries and implementing port interfaces
   - Graph: files orchestrating business logic through ports
   - Runtime: files wiring adapters to ports (composition root)

### TypeScript-Specific Component Identification

In a TypeScript monorepo, components typically map to:
- **Barrel exports** (`index.ts` re-exports) = component public API
- **Feature directories** (`src/compensation/`, `src/runtime/`) = individual components
- **Port interfaces** (`src/ports/types.ts`) = component contracts
- **Adapter implementations** = components that implement port contracts
- **Test directories** help confirm component boundaries — test files group around components

### Example: hex-di as C4

```
C1 (System Context):
  - hex-di [Software System] — "TypeScript dependency injection framework with hexagonal architecture"
  - Developer [Person] — "Builds applications using hex-di"
  - npm Registry [External System] — "Package distribution"
  - Application Runtime [External System] — "Node.js / Browser environment"

C2 (Container):
  - @hex-di/core [Library] — "Port definitions and core abstractions"
  - @hex-di/graph [Library] — "Dependency graph builder and validation"
  - @hex-di/runtime [Library] — "Runtime container and composition"
  - @hex-di/react [Library] — "React integration hooks and providers"
  - @hex-di/flow [Library] — "State machine and workflow engine"
  - @hex-di/saga [Library] — "Distributed saga orchestration"
  - @hex-di/guard [Library] — "Policy-based authorization"
  - Playground [Web App] — "Interactive browser-based playground"

C3 (Component for @hex-di/core):
  - Ports [Component] — "Port definition factory and types"
  - Adapters [Component] — "Adapter creation and inference"
  - Inspection [Component] — "Runtime introspection interfaces"
  - Validation [Component] — "Compile-time type validation"
```
