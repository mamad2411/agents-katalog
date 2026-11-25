# Skill: UI-Planner
**Description**: Generates a deterministic implementation roadmap for static frontend slices (HTML/Tailwind/JS).
**Triggers**: `/ui-plan [ID]`, "generate frontend plan", "plan ui for [ID]"

## Instructions
When triggered, you MUST replace backend patterns (Python interfaces) with Frontend Architectural Stubs.

### 1. Ingestion & Mapping
* **Context**: Read `index.json` and the `aggregate_slice_info.json` contract.
* **Logic**: Map JSON keys directly to DOM selectors instead of Python classes.
* **Stub Replacement**: Instead of `src/[ID]/interfaces.py`, define **Component Schemas** (JSON/JS objects) that describe how the fetched data will be injected into the UI.

### 2. Planning Requirements
The generated plan MUST include:
* **Visual-TDD Phase**: Layout skeleton -> Styling -> Interactivity.
* **Data-Binding Schema**: A definition of how the JS `fetch` will map the registry JSON to specific HTML `id` attributes.
* **No-Dependency Guardrails**: Explicitly forbid Python, Node.js, or framework boilerplate in the implementation steps.

### 3. Metadata & Telemetry
* **Status Sync**: Move slice metadata to `Status: Planned` and `Phase: planning`.
* **Costing**: Calculate the token forecast specifically for a single-file HTML generation.