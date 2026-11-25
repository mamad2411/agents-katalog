---
name: diagrams
description: Architecture diagrams for documentation. Covers ASCII, Mermaid, C4, and D2. Applies C4 methodology by default. Trigger terms: diagram, flowchart, architecture diagram, sequence diagram, C4, mermaid, ascii diagram.
---

# Diagrams Skill

## Decision Flow

1. **C4 zoom level** — which abstraction?
   - L1 Context: who uses it, what it talks to
   - L2 Container: what runs (apps, DBs, queues)
   - L3 Component: what's inside a container
   - L4 Code: rarely needed — IDE handles this

2. **Format** — ask user, or default to ASCII:

| Situation | Format | Why |
|-----------|--------|-----|
| Inline in docs | ASCII | No tooling, survives copy-paste |
| GitHub/GitLab rendered | Mermaid | Native rendering |
| Architecture with containers | D2 | Auto-layout, container edges |
| Formal design doc | C4 PlantUML | Full methodology via Kroki |

## ASCII (default)

Rules:
- Box-drawing chars: `┌ ┐ └ ┘ │ ─ ┬ ▶ ▼`
- Label every box and arrow
- Max width 80 chars
- Single flow direction (TD or LR, never both)

## Mermaid

Use for: sequence diagrams, flowcharts with branches, state machines.

C4 in Mermaid:
```mermaid
C4Context
    Person(user, "User", "Uses the system")
    System(sys, "Our System", "Does the thing")
    Rel(user, sys, "Uses")
```

### Mermaid Limits

| Type | Comfortable | Max | Then use |
|------|:-----------:|:---:|----------|
| Flowchart | 15–25 | ~70 | D2 or Graphviz |
| Class | 10–15 | ~40 | Split diagrams |
| Sequence | 5–8 participants | ~15 | Split scenarios |

Workarounds: `subgraph` clustering, split into linked diagrams.

## D2 (architecture diagrams)

```d2
direction: right
user: User {shape: person}
system: Our System {
  api: API
  db: Database {shape: cylinder}
}
user -> system.api: Uses
system.api -> system.db: Reads/Writes
```

Render: `POST https://kroki.io/d2/svg`

## C4 Checklist

Every architecture diagram must answer:
- [ ] What zoom level? (Context / Container / Component)
- [ ] Who are the actors?
- [ ] What are the boundaries?
- [ ] What are the relationships? (labeled with protocol)
- [ ] Is there a legend?
