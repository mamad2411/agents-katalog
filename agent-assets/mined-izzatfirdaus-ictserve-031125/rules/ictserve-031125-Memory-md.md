---
applyTo:
  - '**'
description: |
  Comprehensive guide for the MCP Memory Server integration in ICTServe.
  Details the Knowledge Graph architecture, tool interfaces, entity ontology,
  and mandatory protocols for agent context management.
tags:
  - mcp
  - memory
  - knowledge-graph
  - context-management
  - tool-usage
version: '2.1.0'
lastUpdated: '2025-11-30'
---

# MCP Memory Server — ICTServe Knowledge Graph Standards

## 1. Overview and Architecture

The MCP Memory Server acts as the persistent, evolving "long-term memory" for AI agents working on the ICTServe project. Unlike file-based documentation, which is static, the Memory Server provides a queryable Knowledge Graph that links requirements, code patterns, and work history.

### Core Data Structure
The architecture is based on a semantic graph consisting of three primary components:

1. **Entities (Nodes)**: Represents distinct objects, concepts, or documents.
    * **Properties**: `name` (unique ID), `entityType` (category).
2. **Relations (Edges)**: Typed connections between entities.
    * **Structure**: `from` (Source) → `relationType` → `to` (Target).
3. **Observations (Facts)**: Immutable snippets of text attached to an Entity.
    * **Usage**: Used to store details, status updates, code snippets, or summarizations without requiring schema changes.

## 2. Tool Interface Reference

Agents utilize specific MCP tools to interact with the Knowledge Graph.

| Tool Name | Function | Usage Scenario |
| :--- | :--- | :--- |
| `search_nodes` | Fuzzy search for entity names and metadata. | **Step 1**: Determining if a topic exists before creating it. |
| `open_nodes` | Retrieves full details (observations + relations) for specific entities. | **Step 2**: Loading context for a specific task or known entity. |
| `create_entities` | Instantiates new nodes in the graph. | Defining a new feature, issue, or session. |
| `add_observations` | Appends new facts to existing entities. | Updating progress, adding implementation details. |
| `create_relations` | Links two existing entities. | Connecting a `feature` to a `requirement`. |
| `read_graph` | Reads the entire graph (Use sparingly). | Full system audits (high token cost). |

## 3. Entity Ontology (Standardized Types)

To maintain a clean graph, use these standardized `entityType` definitions:

| Entity Type | Description | Naming Convention |
| :--- | :--- | :--- |
| `canonical_document` | Official D00-D15 documentation. | `D{##}_{Name}` (e.g., `D04_Software_Design`) |
| `technical_implementation` | A specific feature or system module. | `{System}_{Component}` (e.g., `Email_Notification_System`) |
| `coding_pattern` | Reusable code solutions/standards. | `{Framework}_{Topic}_Pattern` (e.g., `Filament_4_Patterns`) |
| `solved_issue` | Documented fix for a specific error. | `{Error}_Resolution` (e.g., `500_Error_Resolution`) |
| `compliance_implementation` | Completed compliance work (WCAG/i18n). | `{Feature}_Compliance` (e.g., `Navbar_Accessibility_Compliance`) |
| `work_session` | Summary of an agent's session. | `Session_{Date}_{Topic}` |
| `user_context` | User preferences and constraints. | `User_{Name}_Context` |

## 4. Lifecycle Protocols

**CRITICAL**: Every agent session must strictly adhere to the following lifecycle to ensure data integrity and context preservation.

### Phase 1: Initialization (Session Start)

**Goal**: Load context without reading raw files.

1. **Search First**: Always `search_nodes()` before creating to prevent duplicates.
2. **Load User Context**:

    ```javascript
    open_nodes(['User_Context', 'ICTServe_System_Status'])
    ```

3. **Load Task Context**:

    ```javascript
    // Example: Working on exports
    search_nodes('export')
    // Result: Found 'Export_Service_Implementation'
    open_nodes(['Export_Service_Implementation', 'D03_Software_Requirements'])
    ```

### Phase 2: Execution (During Work)

**Goal**: Record knowledge as it happens, not after.

* **When a new pattern is found**: Create a `coding_pattern` entity.
* **When a blocker is hit**: Search for `solved_issue` entities.
* **When a dependency is added**:

    ```javascript
    mcp_memory_create_relations([{
      from: 'Staff_Dashboard',
      relationType: 'uses',
      to: 'Export_Service'
    }])
    ```

### Phase 3: Finalization (Session End)

**Goal**: Ensure the next agent knows exactly where you left off.

1. **Update Feature Status**: `add_observations` to the relevant `technical_implementation` (e.g., "Completed Phase 2, pending validation").
2. **Create Session Record**:

    ```javascript
    mcp_memory_create_entities([{
      name: 'Session_2025-11-30_Dashboard_Fix',
      entityType: 'work_session',
      observations: [
        "Task: Fix CSV export encoding",
        "Changes: Modified ExportService.php",
        "Result: UTF-8 BOM added",
        "Next Steps: Verify Excel compatibility"
      ]
    }])
    ```

## 5. Usage Patterns & Examples

### Pattern A: replacing File-Based Reports

**❌ Anti-Pattern**: Creating `docs/reports/compliance-check.md`.
**✅ Correct Pattern**: Adding observations to the graph.

```typescript
// Instead of a file, push to Memory
add_observations([{
  entityName: 'Navbar_Accessibility_Compliance',
  contents: [
    'Audit Date: 2025-11-30',
    'Status: WCAG 2.2 AA Pass',
    'Fixed: ARIA labels added to mobile menu toggle',
    'Pending: High contrast mode verification'
  ]
}])
````

### Pattern B: Error Resolution via Memory

**Scenario**: You encounter a specific error (e.g., Database Seeding Failure).

1. **Query**: `search_nodes('seeding error')`
2. **Retrieve**: `open_nodes(['Seeding_Failures_Resolution'])`
3. **Apply**: Follow the steps in the entity's observations.
4. **Refine**: If the solution required a tweak, use `add_observations` to update the `Seeding_Failures_Resolution` entity with your new finding.

### Pattern C: Traceability Traversal

**Scenario**: finding why a piece of code exists.

1. **Start**: `open_nodes(['Staff_Dashboard_Component'])`
2. **Observe Relations**:
      * `implements` → `Requirement_SRS_1_1`
      * `uses` → `Livewire_3_Component_Patterns`
      * `documented_by` → `D04_Software_Design`
3. **Action**: You now know the requirements (SRS), the coding standard (Livewire Patterns), and the architectural decision (D04) without searching the file tree.

## 6\. Compliance Checklist

When interacting with the MCP Memory Server, ensure:

* [ ] **Search First**: Never create an entity without checking if it (or a synonym) exists.
* [ ] **Atomic Observations**: Keep observations focused (one fact per string).
* [ ] **Linkage**: Orphan nodes are useless. Always `create_relations` to connect new work to existing systems.
* [ ] **No Files**: Do not create temporary report files; store state in the graph.
* [ ] **Descriptive Names**: Use semantic naming (e.g., `Livewire_3_Patterns`, not `Patterns`).
