---
name: czz-mermaid
description: Mermaid diagram syntax rules and bug avoidance guide. Use when user asks to create, review, or fix Mermaid diagrams, or needs guidance on proper diagram syntax.
---

# Mermaid Diagram Skill - Syntax Rules & Bug Avoidance

Comprehensive guide for writing error-free Mermaid diagrams with proper syntax.

---

## 1. Bracket Matching (Most Critical Rule)

Opening and closing brackets **must match exactly**:

| Opening | Closing | Shape | Example |
|---------|---------|-------|---------|
| `[` | `]` | Rectangle | `A["Label"]` |
| `{` | `}` | Diamond | `D{"Decision"}` |
| `(` | `)` | Rounded | `R{"Label"}` |
| `([` | `])` | Stadium | `S(["Start"])` |
| `[[` | `]]` | Subroutine | `X[["Process"]]` |
| `[(` | `)]` | Cylinder | `DB[("Database")]` |

**NEVER mix**: `{Decision]` or `[Choice}` — these are syntax errors.

---

## 2. Node Labels - Always Use Double Quotes

**ALL node labels MUST be wrapped in double quotes** inside brackets:

```mermaid
%% Correct - safe from parsing errors
A["User: Analyze project"]
B["SKILL.md: Step 0 Preparation"]
C["Read TEMPLATE.md"]

%% WRONG - bare brackets are fragile
A[Label text]
```

### Special Characters That Break Bare Brackets

Labels containing these **must use double quotes**:

- Contains `@`: `ID["@ notification"]`
- Contains `[]`: `ID["items[0]"]`
- Contains `:` + `/`: `ID["CIDR: 10.0.0.0/16"]`
- Contains `<br/>` + `()`: `ID["Process<br/>(async)"]`
- Contains `{}`: `ID["Create ~/path/{project-name}/ dir"]` — `{}` is parsed as diamond
- **Contains `()` inside `[]`**: `ID["HTTP API (/admin, /api)"]`

---

## 3. Reserved Keywords - Never Use as IDs

These keywords (case-insensitive) **cannot be used as node/participant IDs**:

`loop`, `end`, `alt`, `opt`, `par`, `critical`, `break`

**Use suffixes instead**:
- `loop` → `LoopNode`
- `end` → `EndState`
- `alt` → `AltPath`

---

## 4. Node IDs - No Spaces Allowed

```mermaid
%% Correct
AIProviders["LLM APIs"]
user_flow_1["User Flow"]

%% WRONG - space causes parse error
AI Providers["LLM APIs"]
user flow 1["User Flow"]
```

Use camelCase or underscores: `MyNode`, `my_node`.

---

## 5. Edge Labels - Must Use `|"..."|`

```mermaid
%% Correct
A -->|"label text"| B

%% WRONG - missing closing | and target
A -->|"label text"
```

Every `-->|"..."|` must have a closing `|` followed by a destination node.

---

## 6. Comments - Use `%%` Only

```mermaid
%% This is a correct comment
A --> B
# WRONG - # causes parse error
```

---

## 7. sequenceDiagram Rules

### Participant References Must Match Declared IDs

```mermaid
%% Correct - message uses declared ID
participant G as Gateway
CH->>G: Route request

%% WRONG - uses display alias, not declared ID
participant G as Gateway
CH->>Gateway: Route request
```

### Message Syntax Requires Colon

```mermaid
%% Correct
A->>T: Tool result

%% WRONG - missing colon and text
A->>Tool Result
```

### No `style` Directive in sequenceDiagram

```mermaid
%% WRONG - style does not work here
sequenceDiagram
    style A fill:#f9f

%% Correct - use style only in graph/flowchart
graph LR
    style A fill:#f9f
```

### Note Syntax

```mermaid
Note over A,B: text  %% valid only in sequenceDiagram
```

---

## 8. graph/flowchart Rules

### `style` Directive Works Only Here

```mermaid
%% Correct
graph LR
    style A fill:#bbf,stroke:#333

%% WRONG - style in sequenceDiagram doesn't work
sequenceDiagram
    style A fill:#bbf,stroke:#333
```

### Direction Choice

```mermaid
%% Correct for long chains (8+ nodes)
flowchart TD

%% Wrong for 8+ nodes - crushed horizontally
flowchart LR
```

Use `LR` only for short fan-out diagrams (≤7 nodes in longest chain).

### Subgraph Labels Must Not Match Child Node IDs

```mermaid
%% WRONG - causes cycle error
subgraph "Dedupe"
    Dedupe["Dedupe Cache"]
end

%% Correct - different names
subgraph "Dedupe"
    DedupeCache["Dedupe Cache"]
end
```

---

## 9. Fragile Diagram Types - Avoid

| Type | Issue | Alternative |
|------|-------|------------|
| `gitGraph` | Unreliable rendering | Use `graph LR` flowchart |
| Nested subgraphs with empty labels | Causes errors | Always use meaningful labels |
| Complex `stateDiagram` transitions | Fragile | Keep simple |

---

## 10. Self-Check List (11 Points)

Before saving any mermaid block, verify:

1. Every opening bracket has a matching closing bracket of the same type
2. No reserved keyword used as node/participant ID
3. No `style` in sequenceDiagram or stateDiagram
4. All subgraph labels quoted if they contain spaces
5. No `#` comments (use `%%`)
6. Labels containing `{}`, `[]`, `()` wrapped in double quotes
7. No spaces in node IDs — use camelCase or underscores
8. Every `-->|"label"|` has closing `|` and a target node
9. sequenceDiagram messages use declared participant IDs (not aliases)
10. Every `->>` / `-->>` message has a colon and text after target
11. Long linear chains (8+ nodes) use `TD` direction, not `LR`

---

## Diagram Type Reference

### Module Graph (LR) - Simple Dependencies

```mermaid
graph LR
    A["Core Module"] --> B["Utils Module"]
    A --> C["Config Module"]
    D["API Layer"] --> A
```

### Graph (TD) - Dependency Diagram with Style

```mermaid
graph TD
    A["Application"] --> B["Core Library 1"]
    A --> C["Core Library 2"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
```

### Sequence Diagram - User Flow

```mermaid
sequenceDiagram
    participant User as User
    participant Frontend as Frontend
    participant Backend as Backend
    participant DB as Database

    User->>Frontend: Initiate request
    Frontend->>Backend: API call
    Backend->>DB: Query data
    DB-->>Backend: Return result
    Backend-->>Frontend: Response data
    Frontend-->>User: Display result
```

### Architecture with Subgraphs (TB)

```mermaid
graph TB
    subgraph "Presentation Layer"
        A["Web UI"]
        B["Mobile App"]
    end

    subgraph "Business Layer"
        C["Service A"]
        D["Service B"]
    end

    subgraph "Data Layer"
        E[("Database")]
        F[("Cache")]
    end

    A --> C
    B --> C
    C --> E
    C --> F
```

### Flowchart with Decision

```mermaid
flowchart TD
    A["Start"] --> B["Step 1"]
    B --> C{"Condition Check"}
    C -->|"Condition Met"| D["Step 2A"]
    C -->|"Condition Not Met"| E["Step 2B"]
    D --> F["Step 3"]
    E --> F
    F --> G["End"]
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Initialization
    Initialization --> Running
    Running --> Paused: User pause
    Running --> Error: Exception
    Paused --> Running: User resume
    Error --> Running: Retry successful
```

### ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "is in"

    USER {
        uuid id PK
        string name
        string email
    }
```

### Git Branching (Use Flowchart, Not gitGraph)

```mermaid
graph LR
    A["main"] --> B["develop"]
    B --> C["feature-A"]
    B --> D["feature-B"]
    C --> E["merge to develop"]
    D --> E
    E --> F["merge to main"]
```

---

## Quick Reference

| Rule | Correct | Wrong |
|------|---------|-------|
| Node label | `A["text"]` | `A[text]` |
| Edge label | `-->|"text"| B` | `-->|"text"` |
| Comment | `%% comment` | `# comment` |
| Node ID | `MyNode` | `My Node` |
| Reserved word | `LoopNode` | `loop` |
| Direction (long) | `flowchart TD` | `flowchart LR` |
