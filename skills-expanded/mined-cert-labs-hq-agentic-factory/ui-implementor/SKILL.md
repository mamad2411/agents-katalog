# Skill: UI-Implementor
**Description**: Converts a Planned UI Slice into a responsive, data-reactive interface following the Visual-TDD protocol.
**Triggers**: `/ui-implement [ID]`, "render slice [ID]", "build UI for [ID]", "visualize this slice"

## Instructions
When triggered, you MUST follow the UI-SDD protocol to move a slice from `Planned` to `In Review`.

### 1. Ingestion & Context Load
* **State Verification**: Confirm slice metadata (`.factory/slices/[ID].json`) is currently in **Phase: `planning`** and **Status: `Planned`**. If not, STOP and inform the user.
* **Immediate Transition**: Update metadata to **Status: `In Progress`** and **Phase: `implementation`** BEFORE starting any code work.
* **Branching (Mandatory)**: Create and switch to a dedicated feature branch: `factory/ui-slice-[ID]`.
* **Context Load**: Read the target UI specifications:
    - Metadata: `.factory/slices/[ID].json`
    - UI Spec: `docs/specs/product/[ID].md`
    - Plan: `.factory/slices/[ID]-PLAN.md`
    - Data Mock: `.factory/index.json` (to ensure the UI correctly maps to the registry schema).

### 2. Visual-TDD Execution (Mandatory)
For every UI component and data binding defined in the spec:
1. **Define Structural Requirements**: List the required DOM elements and their specific Tailwind utility classes (e.g., "The Savings Card must have `id='savings-value'` and use `text-emerald-400`").
2. **Implement Skeleton (Red)**: Create the HTML structure without styling or dynamic logic.
3. **Apply Visual Design (Green)**: Apply Tailwind CSS classes to achieve the "Technical Architect" aesthetic (Dark mode, monospace accents).
4. **Bind Data (Reactive)**: Implement the Vanilla JS `fetch()` logic to populate the component with data from the local `index.json`.
5. **Verify State**: Confirm that "Loading" and "Error" states are visually distinct and functional.

### 3. Responsiveness & Compliance
* **Viewport Audit**: Ensure the layout is fully responsive (Mobile-first approach).
* **Zero-Dependency Rule**: Strictly use Tailwind via CDN and native ES6+ JavaScript. Do not introduce `npm` or external frameworks.
* **Constraint Validation**: Ensure no hardcoded hex codes or inline styles; strictly use the Tailwind utility system.

### 4. Progress Tracking (Mandatory)
* **Metadata Heartbeat**: At every major UI component completion, update the `updated_at` field in the slice metadata and commit the change to the feature branch.

### 5. Finalization & Reporting
* **Completion Transition**: 
    - Change status to **`In Review`** and Phase to **`validation`** in `.factory/slices/[ID].json`.
    - Update `updated_at` timestamp.
* **Verification Readiness**: Provide the local path (e.g., `dashboard/index.html`) and instructions for a human reviewer to launch the local server.
* **Telemetry**: Conclude the session with the mandatory reporting block.

**TERMINAL INSTRUCTION**: "UI Implementation complete for [ID]. Visual-TDD cycles finished, reactive data binding active, and metadata updated to 'In Review / validation'. Ready for visual audit."