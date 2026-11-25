# 🤖 DizzyFlow Agent Knowledge Base (AGENTS.md)

This document defines the strict operational procedures, architectural principles, and technical standards for all AI agents working on the DizzyFlow project. Agents MUST internalize this document before starting any task.

---

## ⚡ Quick Operating Rules

### 1. Instruction Priority
In case of conflict, follow this order:
1. Explicit User Instructions (Chat)
2. This `AGENTS.md`
3. Project Documentation (under `docs/`)
4. Source Code and Test Code
5. General AI knowledge

### 2. Task Classification & Approval
Classify every request into one of these categories before responding:

- **Trivial (Fast Track)**: 
  - Typo fixes, comment updates, static UI text changes, minor layout adjustments (Padding/Spacing), dead code removal, and small local code changes that do not affect shared state, file I/O, external binaries, public contracts, or workflow transitions.
  - **Procedure**: Immediate implementation without a prior proposal.
- **Non-trivial (Standard)**: 
  - `WorkflowPhase` transitions, `WorkflowStore` logic changes, `SubtitleDocument` data handling, new UI components, macOS compatibility fixes, architecture/folder structure changes, and other changes that affect shared state, workflow flow, or architecture.
  - **Procedure**: Analyze -> check `docs/graphify/GRAPH_REPORT.md` -> if the change touches shared contracts, high-risk zones, or cross-cutting behavior, propose 2-3 approaches and **wait for explicit approval**; otherwise implement the narrowest safe fix directly.

### 3. Emergency Fast Track
Immediate fixes are allowed ONLY for:
- Build failure recovery, app-breaking crash fixes, removal of accidentally committed sensitive data.
- **Constraint**: Minimize the change scope and report the cause and verification results immediately after.

---

## 🤝 Mandatory Workflow

### Step 1: Inquiry & Proposal
- **MUST check the Knowledge Graph (docs/graphify)** first to understand dependencies (God Nodes, etc.).
- Analyze the core problem and constraints.
- For ambiguous, shared, or high-risk changes, present 2-3 technical alternatives and wait for explicit approval before implementation.
- For clearly local, low-risk changes, proceed with the narrowest safe fix after the graph check.

### Step 2: Implementation
- Implement ONLY within the approved scope. No unauthorized refactoring or feature expansion.
- Strictly adhere to **Footer-First UI** and **SSOT (WorkflowStore)** principles.

### Step 3: Verification & Reporting
- **[MANDATORY] Perform a full project build (`xcodebuild`, etc.)** after code changes that can affect runtime behavior, integration, or shared state.
- For doc-only or clearly local low-risk edits, run the strongest practical scoped check and state any skipped verification explicitly.
- **Verification Checklist**:
  - [ ] **Successful Build & App Launch (Required)**
  - [ ] Stability of `WorkflowStore` transitions (Idle -> Ready -> Processing, etc.)
  - [ ] Functionality of footer-based controls (`BottomControlStack`)
  - [ ] Layout integrity on macOS 14/15
- Reports MUST follow the "Required Output Format".

---

## 📚 Project Knowledge Base (Graphify)

This project utilizes a structural knowledge graph generated via `graphify`.
The graph is a decision aid, not a source of truth. If the graph, code, tests, or docs disagree, follow the higher-priority source in the repository instruction hierarchy.

### 1. Resources
- **Report (Human-Readable)**: [docs/graphify/GRAPH_REPORT.md](file:///Users/sanghyoukjin/XcodeProjects/DizzyFlow/docs/graphify/GRAPH_REPORT.md)
  - Summarizes core "God Nodes" (e.g., `WorkflowStore`, `InspectorPanelView`, `WorkflowPhase`).
- **Data (Queryable)**: `docs/graphify/graph.json`
- **Visualization**: [docs/graphify/graph.html](file:///Users/sanghyoukjin/XcodeProjects/DizzyFlow/docs/graphify/graph.html)

### 2. Agent Compliance
- **Pre-analysis Required**: Read `GRAPH_REPORT.md` before any Non-trivial task to understand system-wide impact.
- **Update Graph**: When code structure changes in a significant way, refresh the graph with `graphify update .` and then move the generated output into `docs/graphify/` with `mv graphify-out/* docs/graphify/`.
- **Practical Use**: Use the graph to narrow scope and identify impacted nodes, but do not let the graph block ordinary safe implementation when the code change is clearly local and low risk. For token efficiency, read only the relevant section of `GRAPH_REPORT.md` unless the task is cross-cutting.

---

## 🧠 Core Principles

- **Workflow Stability First**: Stability over feature expansion.
- **Intent over Features**: Users choose intent, not raw models.
- **SSOT**: `WorkflowStore` is the single source of truth. Transitions occur in the Store, not the View.
- **Footer-First UI**: Primary controls MUST reside in the `BottomControlStack`. No major actions in the top toolbar.
- **Interaction Safety**: Sidebar and Inspector must be restricted during the `isProcessing` state.

---

## 📁 Architecture & Layers

- **App**: Owns app-level state flow and Store entry points.
- **Domain**: Pure models (`SubtitleDocument`) and domain logic.
- **Features**: SwiftUI views, panels, and presentation logic.
- **Infrastructure**: Services, engines (Sherpa, Whisper), adapters.
- **Shared**: Reusable utilities, `CapsuleActionButton`, `UpwardMenuPicker`.

---

## 🧭 macOS Compatibility & Localization

- **MacOS Baseline**: Support macOS 14/15 while respecting existing macOS 13 compatibility code.
- **Localization**: Keep English (EN) and Korean (KR) resources synchronized. Adhere to `docs/ux/terms.md`.

---

## 🚫 Forbidden Actions

- Renaming files or restructuring folders without explicit instruction.
- Introducing new frameworks (SwiftData, etc.) without approval.
- Bypassing `WorkflowStore` for state management.
- Overwriting user data directly (Use temporary files).
- Committing or pushing without explicit user approval.

---

## 📤 Required Output Format

1. **Files Changed**: List of modified files.
2. **Reasoning**: Rationale for the chosen approach.
3. **Alternatives**: Other options considered.
4. **Full Code Changes**: The diff or full code blocks.
5. **Validation Results**: Build/Test/Self-check details.
6. **Intentionally Omitted**: What was left out.
7. **Risks**: Potential side effects or follow-up actions.

---

## 🧭 Current Status
- **Current Phase**: Prototype Phase 1
- **Focus**: Data flow, state transitions, structural UI composition.
- **Non-Focus**: Visual polish, performance micro-optimization, real service integration.

---
*Last Updated: 2026-04-22 (by Antigravity - Translated to Global English for Cross-Agent Compatibility)*
