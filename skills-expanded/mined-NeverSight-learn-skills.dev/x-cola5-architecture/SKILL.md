---
name: "x-cola5-architecture"
description: "Enforces COLA 5 directory and layer conventions for Java projects. Invoke when creating Java project structure, adding classes, deciding which layer a class belongs to, or reviewing architecture compliance."
---

# COLA 5 Directory Conventions

Alibaba COLA 5 clean architecture directory conventions. Apply when creating project structure, adding new classes, deciding layer placement, or reviewing architecture compliance.

| Section | Reference | When to Read |
|---------|-----------|-------------|
| Project Structure | `references/project-structure.md` | Creating new project, initializing modules, understanding overall layout |
| Client Module | `references/client-module.md` | Defining service-to-service API contracts, DTO, interface versioning |
| Adapter Layer | `references/adapter-layer.md` | Writing Controller, Scheduler, message listener, or any inbound adapter |
| App Layer | `references/app-layer.md` | Writing Application Service, Command/Query Executor, Processor |
| Domain Layer | `references/domain-layer.md` | Writing Entity, Domain Service, Gateway interface, Domain Event |
| Infrastructure Layer | `references/infrastructure-layer.md` | Implementing Gateway, writing Mapper/Repository, external client, config |
| Object Isolation | `references/object-isolation.md` | Defining DTO/VO/DO/Entity types, deciding object ownership, reviewing cross-layer object flow |

## How to Apply

### Creating New Project
Read `references/project-structure.md` → create modules → define base packages → set up dependencies.

### Defining Service API Contracts
Read `references/client-module.md` → define Api interfaces → define DTO → set up adapter.api to implement contracts.

### Adding New Class
1. Identify the responsibility (inbound / orchestration / business logic / external access)
2. Read the corresponding layer reference
3. Read `references/object-isolation.md` to determine the correct object type and ownership
4. Place class in correct package, follow naming and dependency rules

### Reviewing Architecture Compliance
1. Read each layer reference
2. Verify: no layer bypass, no wrong dependency direction, correct package placement
3. Categorize violations as **Mandatory** (must fix) / **Recommended** (should fix) / **Reference** (nice to have)

### Choosing Lombok Annotations
1. Identify the layer and object type (Entity / Cmd / DTO / DO / Service)
2. Read references/lombok-usage.md for the correct annotation combination
3. Verify: Entity has no @Data/@Setter/@Builder, DTO/DO have @NoArgsConstructor + @AllArgsConstructor

## Core Dependency Rule

```
adapter → app → domain ← infrastructure
```

- **adapter** depends on **app** and **client**
- **app** depends on **domain**
- **infrastructure** depends on **domain** (implements domain gateway interfaces)
- **domain** depends on NOTHING (no other module)
- **client** depends on NOTHING (no other module)
- **adapter** NEVER directly depends on **infrastructure**