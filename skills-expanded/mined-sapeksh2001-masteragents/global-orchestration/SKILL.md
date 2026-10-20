---
name: global-orchestration
description: "Automatically selects and sequences the best agents and skills from your 1,452+ global entries based on your project requirements."
---

# Global Orchestration Decision Matrix

## Goal
To provide a high-intelligence routing layer that automatically "hires" the right expert for any task, ensuring maximum quality and efficiency without manual skill selection.

---

## 🏛️ Namespace Strategy

| Namespace | Strength | When to Use |
|-----------|----------|-------------|
| **`gsd-`** | Project Management & Execution | For planning, roadmap creation, and structured workflows. |
| **`ecc-`** | technical Domain Expertise | For specialized coding tasks, architecture reviews, and build-error resolution. |
| **`base`** | Core UI & Logic | For fundamental component building and standard web design. |
| **`premium`** | Specialized Polish | Humanizer (writing) or Security Architect (audit). |

---

## 🛠️ Automated Routing Logic

### 1. Planning & Discovery (GSD-First)
- **Primary**: `@gsd-planner` or `@gsd-advisor-researcher`
- **Workflow**: `gsd-discovery-phase` -> `gsd-plan-phase`
- **Output**: A structured Project Roadmap and Milestone set.

### 2. Architecture & Design (ECC-Lead)
- **Primary**: `@ecc-architect` or `@software-architecture`
- **Focus**: Patterns, tech stack selection, and scalability.

### 3. Implementation (Mixed Specialization)
- **Frontend**: `@ecc-typescript-reviewer` + `@react-patterns` + `@tailwind-patterns`
- **Backend**: `@ecc-database-reviewer` + `@api-patterns`
- **Testing**: `@ecc-tdd-guide` + `@verification-loop`

### 4. Polish & Security (Final Guardians)
- **Security Check**: `@security-architect-review` or `@ecc-security-reviewer`
- **Writing Check**: `@humanizer` (for all user-facing copy).

---

## 🚦 Selective Invocation Rules

1.  **Requirement Extraction**: Before selecting a tool, identify the **Domain** (e.g., Security, UI, DB) and **Phase** (e.g., Planning, Building, Auditing).
2.  **Semantic Search**: Use the `list_skills` tool to find skills matching the domain.
3.  **Conflict Resolution**: If both a `gsd` and `ecc` agent exist for the same domain (e.g., both have planners), choose `gsd` for methodology/workflow and `ecc` for technical deep-dives.
4.  **Sequencing**: Always plan before building. Use `gsd-plan` -> `ecc-architect` -> `build`.

---

## 🚀 Orchestration Prompt Pattern
If a user is lost, the Orchestrator should respond with:
> "I've analyzed your project. I will now use the **GSD methodology** to create a plan, then hire our **ECC-Architect** to design the system. Once designed, I'll use our **Base React Skills** to build it, followed by a **Security Review** and **Humanizer** pass on the finished product. Ready to begin?"
