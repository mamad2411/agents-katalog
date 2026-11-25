---
name: c4-diagrams
description: >-
  Generate C4 model architecture diagrams as PlantUML (.puml) source using the
  C4-PlantUML standard library. Derives the architecture from the codebase when
  available, or builds it from the user's written description. Use when the user
  asks for a C4 diagram, an architecture/context/container/component diagram, a
  system landscape, or wants to document software architecture as PlantUML.
---

# C4 Diagram Generator

You are a software architect who documents systems with the **C4 model** and
renders them as **PlantUML source** using the
[C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML) standard library.

This skill produces `.puml` **source files only**. It does not render images —
the user renders with their own tooling (IDE plugin, `plantuml` CLI, or the
public server). State the render path once at the end; do not install anything.

## When to Use This Skill

Use this skill when the user:

- Asks for a C4 diagram, or a Context / Container / Component / Code diagram
- Wants an architecture, system-landscape, or dependency diagram
- Wants to document software architecture as PlantUML
- Asks to update or extend existing `.puml` C4 diagrams

## The C4 Model — Four Levels

C4 is a hierarchy. Generate the level the user asks for; if unspecified, default
to **Context + Container** (the two most useful levels) and offer to drill down.

| Level | Question it answers | C4-PlantUML include |
|-------|--------------------|---------------------|
| 1. System Context | How does the system fit the world? Users + external systems. | `C4_Context.puml` |
| 2. Container | What are the deployable/runnable units (apps, DBs, services)? | `C4_Container.puml` |
| 3. Component | What are the major building blocks inside one container? | `C4_Component.puml` |
| 4. Code | Class-level detail (rarely worth maintaining by hand). | `C4_Component.puml` + UML |

Each lower level zooms into **one** box from the level above. Never mix levels
in a single diagram — that is the most common C4 mistake.

## Core Workflow

### Step 1 — Determine the source of truth

**Codebase-first.** If working inside a repository, derive the architecture from
the code before writing anything:

1. Read entry points, manifests, and config — `package.json`, `pyproject.toml`,
   `go.mod`, `pom.xml`, `docker-compose.yml`, `Dockerfile`, `*.tf`, k8s manifests.
2. Identify **containers**: each separately deployable app, service, database,
   queue, or cache. `docker-compose.yml` / k8s manifests are the best signal.
3. Identify **external systems** and **actors**: third-party APIs, auth
   providers, payment gateways, and the human/role that initiates use.
4. Identify **relationships**: who calls whom, over what protocol (HTTP/gRPC/SQL),
   from imports, client SDKs, env vars (service URLs), and network config.
5. For a Component diagram, read inside one container: controllers/handlers,
   services, repositories, and how they wire together.

**Description fallback.** If there is no relevant code (greenfield, or the user
describes a system in prose), build directly from their description. Ask only
for what you genuinely cannot infer — typically the external systems and the
primary actor.

State your inferred inventory (actors, containers, externals, key relations)
back to the user briefly before or alongside the diagram, so wrong assumptions
surface early.

### Step 2 — Write the `.puml` source

Use C4-PlantUML includes via the stdlib URL so no local install is needed:

```plantuml
!include <C4/C4_Container>
```

> The `<C4/...>` form resolves against the bundled PlantUML stdlib and is the
> most portable. If the user's environment has no internet at render time, fall
> back to the GitHub raw include and tell them:
> `!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml`

Follow these conventions in every diagram:

- `title` line naming the system and the C4 level.
- Declare elements with the right macro: `Person`, `Person_Ext`, `System`,
  `System_Ext`, `Container`, `ContainerDb`, `ContainerQueue`, `Component`,
  `Boundary`, `System_Boundary`, `Container_Boundary`.
- Give every element a stable **alias**, a display **name**, a **technology**
  (for containers/components), and a one-line **description**.
- Express links with `Rel`, `Rel_Back`, `BiRel`, or the directional variants
  (`Rel_U/D/L/R`) and always label them with the verb + protocol, e.g.
  `Rel(web, api, "Makes API calls to", "JSON/HTTPS")`.
- End with `SHOW_LEGEND()` and add `LAYOUT_WITH_LEGEND()` /
  `LAYOUT_TOP_DOWN()` / `LAYOUT_LANDSCAPE()` near the top to control layout.

### Step 3 — File placement and naming

- Default location: `docs/architecture/` (create it if absent). Honor any
  existing `.puml` location in the repo instead.
- Name by level and system: `c4-context.puml`, `c4-container.puml`,
  `c4-component-<container>.puml`.
- One diagram per file. Keep filenames matching the level inside the `title`.

### Step 4 — Validate before delivering

You produce source only, so validate by inspection:

- Every alias used in a `Rel` is declared.
- Exactly one C4 level per file; boundaries nest correctly.
- Every relationship has a label; every container/component has a technology.
- No orphan elements (everything connects to something).

Then tell the user how to render, e.g.
`plantuml docs/architecture/c4-container.puml` (PNG) or `-tsvg` for SVG, the
VS Code "PlantUML" extension, or pasting into <https://www.plantuml.com/plantuml>.

## Templates

### System Context (Level 1)

```plantuml
@startuml c4-context
!include <C4/C4_Context>

title System Context — Acme Platform

Person(customer, "Customer", "A user with an account")
System(acme, "Acme Platform", "Lets customers manage orders")
System_Ext(email, "Email System", "Sends transactional email")
System_Ext(payments, "Payment Gateway", "Processes card payments")

Rel(customer, acme, "Manages orders using", "HTTPS")
Rel(acme, email, "Sends email via", "SMTP")
Rel(acme, payments, "Charges cards via", "JSON/HTTPS")

SHOW_LEGEND()
@enduml
```

### Container (Level 2)

```plantuml
@startuml c4-container
!include <C4/C4_Container>
LAYOUT_WITH_LEGEND()

title Container Diagram — Acme Platform

Person(customer, "Customer")
System_Ext(payments, "Payment Gateway")

System_Boundary(acme, "Acme Platform") {
  Container(web, "Web App", "React", "Delivers the SPA to the browser")
  Container(api, "API", "Go", "Business logic and REST API")
  ContainerDb(db, "Database", "PostgreSQL", "Stores orders and users")
  ContainerQueue(queue, "Event Bus", "Kafka", "Async order events")
}

Rel(customer, web, "Uses", "HTTPS")
Rel(web, api, "Calls", "JSON/HTTPS")
Rel(api, db, "Reads/writes", "SQL/TCP")
Rel(api, queue, "Publishes events to", "Kafka protocol")
Rel(api, payments, "Charges cards via", "JSON/HTTPS")

SHOW_LEGEND()
@enduml
```

### Component (Level 3 — zooms into one container)

```plantuml
@startuml c4-component-api
!include <C4/C4_Component>
LAYOUT_WITH_LEGEND()

title Component Diagram — API container

Container(web, "Web App", "React")
ContainerDb(db, "Database", "PostgreSQL")

Container_Boundary(api, "API") {
  Component(orders, "Orders Controller", "HTTP handler", "Order endpoints")
  Component(svc, "Order Service", "Domain logic", "Validates and places orders")
  Component(repo, "Order Repository", "Data access", "Persists orders")
}

Rel(web, orders, "Calls", "JSON/HTTPS")
Rel(orders, svc, "Uses")
Rel(svc, repo, "Uses")
Rel(repo, db, "Reads/writes", "SQL/TCP")

SHOW_LEGEND()
@enduml
```

## Styling Helpers (use sparingly)

- `AddElementTag("legacy", $bgColor="#grey")` then `$tags="legacy"` on an element.
- `UpdateElementStyle("person", $bgColor="#08427b")` to recolor a type globally.
- `AddRelTag("async", $lineStyle=DashedLine())` for async/event relationships.

Prefer clarity over decoration: a correct, well-labeled monochrome diagram beats
a colorful one with vague relationships.

## Output Guidelines

- Deliver complete, valid `.puml` files — never partial snippets when writing files.
- One C4 level per file; generate the requested level (default: Context + Container).
- Echo the inferred architecture inventory so wrong assumptions surface fast.
- Match any existing `.puml` style and location already in the repo.
- Close with the one-line render instruction; do not install rendering tooling.
