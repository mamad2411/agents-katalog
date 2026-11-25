---
name: uml-diagrams
description: "Generate UML diagrams using Mermaid.js syntax for software architecture documentation, code visualization, and design communication. Use when creating class diagrams, sequence diagrams, state diagrams, component diagrams, flowcharts, entity-relationship diagrams, or any visual representation of code structure and behavior. Use when documenting TypeScript interfaces, ports/adapters architecture, dependency injection graphs, domain models, API interactions, state machines, data flows, or system boundaries. Use when writing or editing markdown files (.md) that contain or should contain Mermaid diagram code blocks. Use when a user asks to visualize, diagram, map, or draw any aspect of the codebase including package dependencies, class hierarchies, module relationships, request flows, event sequences, or deployment topology. Use when creating architecture decision records (ADRs), specification documents, README files, or any documentation that benefits from visual diagrams. Use when reviewing code and a visual representation would clarify the design. Use when planning new features, refactoring existing code, or explaining how systems interact. For C4 architecture diagrams (Context, Container, Component, Dynamic, Deployment), use the dedicated c4-mermaid-syntax skill instead."
---

## When to use this skill

- Creating or editing UML diagrams in Mermaid.js syntax within markdown files
- Visualizing TypeScript class hierarchies, interfaces, and type relationships
- Documenting hexagonal/clean architecture with ports, adapters, graph, and runtime layers
- Creating sequence diagrams showing request flows through the application
- Drawing component diagrams showing package dependencies in a monorepo
- Creating state machine diagrams for stateful logic
- Documenting entity-relationship models for data structures
- Adding visual documentation to specification files in `spec/` directories
- Creating flowcharts for business logic, decision trees, or algorithms
- Diagramming dependency injection wiring and service graphs
- Visualizing event-driven architectures, pub/sub flows, or message sequences
- Documenting API contracts and interaction patterns between systems
- Planning and communicating architectural decisions visually
- Any task where "a picture is worth a thousand words" applies to code architecture

---

# UML Diagrams with Mermaid.js

Generate clear, accurate, and maintainable UML diagrams using Mermaid.js syntax. Mermaid is the preferred diagramming tool because it is text-based (version control friendly), renders natively in GitHub/GitLab markdown, and can be generated programmatically by AI.

## Diagram Type Selection Guide

Choose the right diagram type based on what you need to communicate:

### Structure Diagrams (What the system IS)

| Diagram Type | Use When | Mermaid Type |
|-------------|----------|--------------|
| **Class Diagram** | Showing types, interfaces, inheritance, composition | `classDiagram` |
| **Component Diagram** | Showing packages, modules, and their dependencies | `flowchart` |
| **Package Diagram** | Showing monorepo structure, package relationships | `flowchart` |
| **Object Diagram** | Showing runtime instances and their state | `classDiagram` with notes |
| **ER Diagram** | Showing data models, entities, and relationships | `erDiagram` |

### Behavior Diagrams (What the system DOES)

| Diagram Type | Use When | Mermaid Type |
|-------------|----------|--------------|
| **Sequence Diagram** | Showing message flow between objects over time | `sequenceDiagram` |
| **State Diagram** | Showing lifecycle states and transitions | `stateDiagram-v2` |
| **Activity/Flowchart** | Showing workflows, algorithms, decision logic | `flowchart` |
| **Use Case Diagram** | Showing user interactions with the system | `flowchart` with actors |

### Architecture Diagrams (System at Scale)

| Diagram Type | Use When | Mermaid Type |
|-------------|----------|--------------|
| **Deployment** | Showing infrastructure and deployment topology | `flowchart` |
| **C4 Diagrams** | System context, containers, components, dynamic flows, deployment | See dedicated C4 skills below |

> **C4 Architecture Diagrams**: For C4 Context, Container, Component, Dynamic, and Deployment diagrams, use the dedicated skills:
> - `c4-methodology` — C4 model concepts, abstraction levels, scoping, cross-level consistency
> - `c4-mermaid-syntax` — Complete Mermaid C4 syntax reference with all macros, templates, and ASCII format
> - `c4-architect` agent — Specialized C4 modeling agent for code analysis and diagram creation

---

## Mermaid Syntax Reference

### Class Diagrams

Use for TypeScript interfaces, types, classes, and their relationships.

```mermaid
classDiagram
    direction TB

    class Port {
        <<interface>>
        +execute(input: Input) Result~Output~
    }

    class Adapter {
        -dependency: ExternalService
        +execute(input: Input) Result~Output~
    }

    class Graph {
        -port: Port
        +run() Result~Output~
    }

    Port <|.. Adapter : implements
    Graph --> Port : depends on
    Graph ..> Input : uses
```

**Key syntax:**

```
%% Visibility markers
+ public
- private
# protected
~ package/internal

%% Relationships (from most to least coupling)
A <|-- B        Inheritance (B extends A)
A <|.. B        Realization (B implements A)
A *-- B         Composition (A owns B, B dies with A)
A o-- B         Aggregation (A has B, B can exist alone)
A --> B         Association (A uses B)
A ..> B         Dependency (A temporarily uses B)

%% Cardinality
A "1" --> "*" B         One to many
A "0..1" --> "1..*" B   Optional to one-or-more

%% Annotations
class MyInterface {
    <<interface>>
}
class MyEnum {
    <<enumeration>>
    VALUE_A
    VALUE_B
}
class MyAbstract {
    <<abstract>>
}
class MyService {
    <<service>>
}

%% Generics
class Container~T~ {
    +get() T
    +set(value: T) void
}

%% Notes
note for ClassName "Important detail"
```

### Sequence Diagrams

Use for showing interactions between components over time.

```mermaid
sequenceDiagram
    actor User
    participant API as REST API
    participant Graph as Business Logic
    participant Port as Port Interface
    participant Adapter as Database Adapter
    participant DB as PostgreSQL

    User->>+API: POST /users
    API->>+Graph: createUser(dto)
    Graph->>+Port: save(user)
    Port->>+Adapter: save(user)
    Adapter->>+DB: INSERT INTO users...
    DB-->>-Adapter: result
    Adapter-->>-Port: Result<User>
    Port-->>-Graph: Result<User>
    Graph-->>-API: UserDto
    API-->>-User: 201 Created
```

**Key syntax:**

```
%% Message types
A->>B       Synchronous request (solid arrow)
A-->>B      Synchronous response (dotted arrow)
A-)B        Async message (open arrow)
A--)B       Async response (dotted open arrow)
A-xB        Lost message (cross)
A<<->>B     Bidirectional

%% Activation (shows processing time)
A->>+B: request    %% activate B
B-->>-A: response  %% deactivate B

%% Control flow
alt condition
    A->>B: path 1
else other condition
    A->>C: path 2
end

opt optional
    A->>B: maybe
end

loop every 5 seconds
    A->>B: poll
end

par parallel
    A->>B: task 1
and
    A->>C: task 2
end

critical must succeed
    A->>B: important
option failure
    A->>C: fallback
end

break when error
    A->>B: abort
end

%% Notes
Note right of A: explanation
Note over A,B: spans both
```

### State Diagrams

Use for showing lifecycle states and transitions.

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Idle
    Idle --> Loading : fetch()
    Loading --> Success : data received
    Loading --> Error : request failed
    Success --> Loading : refresh()
    Error --> Loading : retry()
    Error --> Idle : reset()
    Success --> Idle : reset()

    state Loading {
        [*] --> Requesting
        Requesting --> Parsing : response received
        Parsing --> [*] : parsed
    }

    note right of Error
        Includes error message
        and retry count
    end note
```

**Key syntax:**

```
[*] --> State          Initial transition
State --> [*]          Final transition
State1 --> State2 : event   Transition with label

state "Display Name" as s1    Aliased state
state CompositeState {        Nested states
    [*] --> Inner
    Inner --> [*]
}

state fork_state <<fork>>    Fork pseudo-state
state join_state <<join>>    Join pseudo-state
state choice <<choice>>      Choice pseudo-state

note right of State          Notes
    Explanation text
end note
```

### Flowcharts

Use for workflows, algorithms, decision trees, and component diagrams.

```mermaid
flowchart TB
    subgraph Ports["Ports Layer (Core)"]
        direction TB
        P1[LoggerPort]
        P2[TracingPort]
        P3[ResultPort]
    end

    subgraph Adapters["Adapters Layer"]
        direction TB
        A1[PinoAdapter]
        A2[WinstonAdapter]
        A3[OtelAdapter]
        A4[DatadogAdapter]
    end

    subgraph Runtime["Runtime Layer"]
        R1[Container]
    end

    A1 -.->|implements| P1
    A2 -.->|implements| P1
    A3 -.->|implements| P2
    A4 -.->|implements| P2
    R1 -->|wires| A1
    R1 -->|wires| A3

    style Ports fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Adapters fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Runtime fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
```

**Key syntax:**

```
%% Node shapes
A[Rectangle]
B(Rounded)
C([Stadium])
D[[Subroutine]]
E[(Database)]
F((Circle))
G{Diamond/Decision}
H{{Hexagon}}
I[/Parallelogram/]
J[\Trapezoid\]

%% Directions
flowchart TB    %% Top to Bottom
flowchart BT    %% Bottom to Top
flowchart LR    %% Left to Right
flowchart RL    %% Right to Left

%% Link styles
A --> B         Solid arrow
A --- B         Solid line
A -.-> B        Dotted arrow
A ==> B         Thick arrow
A -- text --> B Labeled link
A -->|text| B   Labeled link (alt)

%% Subgraphs
subgraph title
    direction TB
    A --> B
end

%% Styling
style A fill:#f9f,stroke:#333,stroke-width:2px
classDef port fill:#e1f5fe,stroke:#01579b
class A,B port
```

### Entity-Relationship Diagrams

Use for data models and entity relationships.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        string id PK
        string email UK
        string name
        datetime createdAt
    }
    ORDER ||--|{ LINE_ITEM : contains
    ORDER {
        string id PK
        string userId FK
        string status
        decimal total
    }
    LINE_ITEM {
        string id PK
        string orderId FK
        string productId FK
        int quantity
        decimal price
    }
    PRODUCT ||--o{ LINE_ITEM : "appears in"
    PRODUCT {
        string id PK
        string name
        decimal price
    }
```

**Key syntax:**

```
%% Relationships
||--||    Exactly one to exactly one
||--o{    Exactly one to zero or more
||--|{    Exactly one to one or more
o{--o{    Zero or more to zero or more

%% Attribute markers
PK    Primary Key
FK    Foreign Key
UK    Unique Key
```

---

## Best Practices

### 1. Choose the Right Level of Detail

- **Too little detail**: Diagram doesn't communicate anything useful
- **Too much detail**: Diagram becomes unreadable noise
- **Right level**: Shows the key relationships and decisions that matter

**Rule of thumb**: If a diagram has more than 15-20 elements, split it into multiple diagrams at different levels of abstraction.

### 2. Use Consistent Naming

- Match names in diagrams to actual code identifiers
- Use the same terminology as the codebase (Port, Adapter, Graph, Runtime)
- Don't abbreviate unless the abbreviation is universally understood

### 3. Show Direction of Dependencies

- Always make dependency direction explicit with arrows
- In hexagonal architecture, arrows should point INWARD (toward the domain)
- Use different arrow styles to distinguish relationship types

### 4. Color Code Architecture Layers

Use consistent colors across all diagrams:

| Layer | Color | Hex |
|-------|-------|-----|
| Ports/Domain | Light Blue | `#e1f5fe` |
| Adapters/Infrastructure | Light Orange | `#fff3e0` |
| Graph/Application | Light Purple | `#f3e5f5` |
| Runtime/Composition | Light Green | `#e8f5e8` |
| External Systems | Light Red | `#fce4ec` |

### 5. Label Relationships

Always label relationships with their semantic meaning:
- `implements` not just an arrow
- `depends on` to show dependency direction
- `creates` to show lifecycle ownership
- `calls` to show runtime interaction

### 6. Keep Diagrams in Sync with Code

- Store diagrams in markdown files next to the code they document
- Update diagrams when the code changes
- Use diagrams in specification files (`spec/`) as the source of truth
- Reference specific file paths in diagram notes when helpful

### 7. One Concept Per Diagram

Each diagram should answer ONE question:
- "What are the types and their relationships?" -> Class diagram
- "How does a request flow through the system?" -> Sequence diagram
- "What states can this entity be in?" -> State diagram
- "What packages exist and how do they depend on each other?" -> Component diagram

---

## Patterns for This Codebase

### Hexagonal Architecture Layers

```mermaid
flowchart TB
    subgraph External["External World"]
        HTTP[HTTP Client]
        DB[(Database)]
        MQ[Message Queue]
    end

    subgraph Ports["@hex-di/core - Ports"]
        direction TB
        LP[LoggerPort]
        TP[TracingPort]
        RP[ResultPort]
    end

    subgraph Graph["@hex-di/graph - Business Logic"]
        direction TB
        G1[ServiceGraph]
        G2[WorkflowGraph]
    end

    subgraph Adapters["Adapter Packages"]
        direction TB
        LA[logger-pino]
        LB[logger-winston]
        TA[tracing-otel]
        TB2[tracing-datadog]
    end

    subgraph Runtime["@hex-di/runtime"]
        RT[Container / Composition Root]
    end

    G1 --> LP
    G1 --> TP
    G2 --> RP
    LA -.->|implements| LP
    LB -.->|implements| LP
    TA -.->|implements| TP
    TB2 -.->|implements| TP
    RT -->|wires| LA
    RT -->|wires| TA
    LA --> DB
    TA --> MQ

    style Ports fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Graph fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style Adapters fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Runtime fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    style External fill:#fce4ec,stroke:#880e4f,stroke-width:1px
```

### Port-Adapter Relationship

```mermaid
classDiagram
    direction LR

    class Port~TInput, TOutput~ {
        <<interface>>
        +execute(input: TInput) Result~TOutput~
    }

    class Adapter~TInput, TOutput~ {
        -config: AdapterConfig
        -client: ExternalClient
        +execute(input: TInput) Result~TOutput~
    }

    class Graph {
        -ports: Map~string, Port~
        +run() Result~Output~
    }

    class Runtime {
        +createAdapter() Adapter
        +wire(graph: Graph, adapter: Adapter) void
    }

    Port <|.. Adapter : implements
    Graph --> Port : depends on interface
    Runtime ..> Adapter : creates
    Runtime ..> Graph : configures
```

### Request Flow Through Layers

```mermaid
sequenceDiagram
    actor Client
    participant RT as Runtime
    participant G as Graph
    participant P as Port (interface)
    participant A as Adapter (impl)
    participant Ext as External Service

    Note over RT: Application bootstrap
    RT->>A: create adapter
    RT->>G: inject port = adapter

    Note over Client: Runtime request
    Client->>+G: execute(input)
    G->>+P: port.execute(input)
    Note over P,A: Port interface, Adapter impl
    P->>+A: (resolved to adapter)
    A->>+Ext: external call
    Ext-->>-A: response
    A-->>-P: Result<Output>
    P-->>-G: Result<Output>
    G-->>-Client: Result<Output>
```

---

## Common Diagram Templates

### Template: Package Dependency Map

```mermaid
flowchart LR
    subgraph Core
        core["@hex-di/core"]
        result["@hex-di/result"]
    end

    subgraph Packages
        graph["@hex-di/graph"]
        runtime["@hex-di/runtime"]
        logger["@hex-di/logger"]
        tracing["@hex-di/tracing"]
    end

    subgraph Adapters
        pino["logger-pino"]
        winston["logger-winston"]
        otel["tracing-otel"]
    end

    graph --> core
    graph --> result
    runtime --> core
    runtime --> graph
    logger --> core
    tracing --> core
    pino --> logger
    winston --> logger
    otel --> tracing

    style Core fill:#e1f5fe,stroke:#01579b
    style Packages fill:#f3e5f5,stroke:#4a148c
    style Adapters fill:#fff3e0,stroke:#e65100
```

### Template: Error/Result Flow

```mermaid
flowchart TD
    Start([Operation]) --> Execute{Execute}
    Execute -->|Success| Ok[Ok Result]
    Execute -->|Known Error| Err[Err Result]
    Execute -->|Unknown Error| Panic[Throw / Defect]

    Ok --> Map[map / flatMap]
    Err --> Recover{Can Recover?}
    Recover -->|Yes| Fallback[Fallback Logic]
    Recover -->|No| Propagate[Propagate Err]

    Map --> Next([Next Operation])
    Fallback --> Next
    Propagate --> Caller([Return to Caller])
```

### Template: State Machine

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Created : initialize

    state "Active States" as active {
        Created --> Pending : submit
        Pending --> Approved : approve
        Pending --> Rejected : reject
        Approved --> InProgress : start
        InProgress --> Completed : finish
        InProgress --> Paused : pause
        Paused --> InProgress : resume
    }

    Rejected --> Pending : resubmit
    Completed --> [*]

    note right of Rejected
        Can resubmit with changes
    end note
```

---

## Anti-Patterns to Avoid

1. **Diagram without a purpose**: Every diagram must answer a specific question. If you can't state what question it answers, don't create it.

2. **Showing everything**: A diagram that shows every class, every method, every relationship is useless. Show what matters for the reader's question.

3. **Inconsistent with code**: A diagram that doesn't match the actual code is worse than no diagram. Keep them synchronized.

4. **Wrong diagram type**: Don't use a class diagram to show runtime behavior. Don't use a sequence diagram to show type hierarchy.

5. **No legend or context**: If using custom colors, shapes, or conventions, include a brief legend or note explaining them.

6. **Stale diagrams**: If you update the code, update the diagram. A stale diagram actively misleads.

---

## Generating Diagrams from Code

When asked to create a diagram for existing code:

1. **Read the relevant source files** first to understand the actual structure
2. **Identify the key abstractions** - not every type needs to be in the diagram
3. **Map relationships accurately** - check actual imports and dependencies
4. **Use correct Mermaid syntax** - validate the diagram renders correctly
5. **Place the diagram** in the appropriate markdown file (README, spec, or dedicated docs)

When creating diagrams for planned/new code:

1. **Start with the diagram** as a design tool
2. **Use it to communicate intent** before writing code
3. **Update it** as the implementation evolves
4. **Keep it** as documentation after implementation
