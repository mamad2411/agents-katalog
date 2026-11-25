---
name: architecture-rules
description: Use when designing software architecture, creating UML diagrams, reviewing module structure, or working with StarUML. Defines the layered architecture principles with interface segregation, dependency rules, and documentation requirements.
---

# Architecture Design Rules

These rules define how all software projects must be architected. Every agent (Claude, Kimi, or any future agent) working on architecture MUST follow these rules.

## Two-Layer Architecture

### Layer 1: Package/Module Diagram

The top-level view showing all modules and their relationships.

**Structure:**
- Each module is a UML Package
- Each module exposes exactly ONE UML Interface (its public API)
- Each module has exactly ONE Controller class that implements its interface
- Other modules depend on the INTERFACE, never on the controller or internal classes
- Dependencies between modules are shown as UML Dependencies from one package to another's interface

**Two module types:**

1. **Core Modules** — the main systems of the application
   - ALL dependencies between core modules MUST be shown explicitly
   - NO circular dependencies allowed between core modules (A -> B -> C -> A is forbidden)
   - Shown in the upper/middle area of the diagram

2. **Utility Modules** — shared helpers, data structures, constants
   - Sit at the BOTTOM of the diagram
   - Their dependencies are NOT explicitly shown (they are assumed available to all)
   - Tagged with stereotype `<<Utility>>`

**Naming conventions:**
- Module interface: `I{ModuleName}` (e.g., `ICombatSystem`, `IInventoryManager`)
- Module controller: `{ModuleName}Controller` (e.g., `CombatSystemController`)
- Package name matches the module name (e.g., `CombatSystem`)

### Layer 2: Class Diagrams (per module)

Each module gets its own UML Class Diagram showing internal structure.

**Layout (top to bottom):**
1. The module's Interface (at the top)
2. The Controller that implements it (directly below, with interface realization arrow)
3. All internal classes, enums, data types below

**Principles:**
- **Single Responsibility**: Each class has one reason to change
- **Command Chain**: Where applicable, use chain-of-responsibility for processing
- **Design as Systems**: Model mechanics as systems where possible (not loose scripts)

**When a module needs functionality from another module:**
1. Add the operation to the OTHER module's interface first (in the UML)
2. Implement it in that module's controller
3. The calling module depends on the interface, never the concrete class

### Recursive Sub-Modules

A module can contain sub-modules that follow the SAME two-layer rules:
- Sub-module gets its own package inside the parent package
- Sub-module has its own interface + controller
- Same dependency and naming rules apply recursively
- Sub-module gets its own class diagram

## Engine-Specific Rules

### Unity Projects
- Do NOT show MonoBehaviour/Component inheritance arrows in UML (creates noise)
- Instead, add stereotype `<<MonoBehaviour>>` or `<<ScriptableObject>>` to the class
- The actual inheritance from Unity base classes is assumed, not drawn

### Godot Projects
- Every `.gd` file is treated as a UML class (GDScript scripts ARE classes, even without `class_name`)
- Scripts with `class_name` → use the declared name. Scripts without → use the filename.
- `extends` to engine classes (Node, Node3D, CharacterBody3D, etc.) → stereotype `<<Node3D>>` etc., NO inheritance arrow
- `extends` to another project script → real UML generalization arrow
- `signal` declarations → operation with `<<signal>>` stereotype
- `@export` vars → public visibility. Regular vars → private visibility.
- `@onready` vars → note in documentation field
- Autoload singletons (from `project.godot`) → stereotype `<<Autoload>>`
- Directory structure maps to packages: `scripts/combat/` → `Combat` package
- Exclude `addons/` from scanning unless explicitly requested

### Generic Projects (Python, TypeScript, etc.)
- Standard UML class diagram rules apply
- Show inheritance normally

## Documentation Requirements (for HTML/Markdown Export)

Every UML element MUST have a `documentation` field filled in for StarUML's `project_export_doc` to produce useful output:

### What to document:
- **Packages**: Purpose, what systems/features this module owns, key responsibilities
- **Interfaces**: What contract this defines, what clients should expect
- **Classes**: Purpose, what problem this solves, key behavior summary
- **Operations**: What it does, parameter meanings, return value meaning, side effects
- **Attributes**: What data this stores, valid ranges/constraints, default behavior

### Documentation style:
- First sentence = one-line summary
- Followed by details if needed (bullet points for parameters, constraints)
- No boilerplate ("This class is a class that...") — get to the point
- Include behavioral notes: "Called when...", "Triggers...", "Must be called after..."

## Validation Checklist

After creating/updating architecture, verify:
- [ ] Every core module has exactly one interface
- [ ] Every core module has exactly one controller implementing its interface
- [ ] No circular dependencies between core modules
- [ ] Dependencies go through interfaces, not concrete classes
- [ ] Utility modules are tagged `<<Utility>>`
- [ ] All elements have non-empty `documentation` fields
- [ ] `diagram_layout` has been called on every diagram for clean arrangement
