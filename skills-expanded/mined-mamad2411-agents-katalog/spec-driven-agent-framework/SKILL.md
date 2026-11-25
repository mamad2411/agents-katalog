---
name: spec-driven-agent-framework
description: The 6-file specification contract for AI agents (PRD, Architecture, Rules, Design, Tasks, Memory) ensuring zero hallucination and drift-free coding sessions.
tags: [ai-agents, architecture, engineering-standards, specification, context-management]
---

# Spec-Driven AI Agent Engineering Framework

## Overview
When orchestrating autonomous coding agents, unconstrained prompts lead to context drift, hallucinated packages, inconsistent UI styles, and incomplete task executions. 

This framework formalizes the **6 Essential Markdown Specification Files** placed under `.agent/` (or repository root) that anchor the agent's reasoning across long sessions.

---

## The 6 Mandatory Specification Files

### 1. `PRD.md` — Product Requirements Document
- **Purpose**: Anchors high-level intent, user stories, and feature boundaries.
- **Key Sections**:
  - Problem Statement
  - Target Users & Personas
  - Core Features & Acceptance Criteria
  - Non-Functional Requirements (Performance, Security, Device support)
  - Explicit Out-of-Scope boundaries

### 2. `ARCHITECTURE.md` — System Architecture & Flow
- **Purpose**: Prevents folder sprawling and import collisions.
- **Key Sections**:
  - Technology Stack (Framework, State Management, Database, Styling)
  - Directory Tree & Module Boundaries
  - Component Hierarchy & Data Flow Diagrams
  - API / Schema Contracts & Integration Points

### 3. `RULES.md` — Agent Operating Contract
- **Purpose**: Enforces hard engineering constraints and coding discipline.
- **Key Sections**:
  - Mandatory Constraints (e.g. Strict TypeScript, zero `any`, zero mock stubs)
  - Forbidden Libraries & Anti-Patterns
  - Error Handling & Recovery Protocols
  - Test & Build Verification Gates before reporting completion

### 4. `DESIGN.md` — Design System & Visual Tokens
- **Purpose**: Prevents the agent from inventing new colors or layouts on every turn.
- **Key Sections**:
  - Color Tokens (Hex codes, semantic names, dark/light variants)
  - Typography Hierarchy (Fonts, scale, line heights)
  - Component Atoms (Buttons, Cards, Inputs, Modals)
  - Animation & Micro-Interaction Guidelines

### 5. `TASKS.md` — Atomic Milestone Decomposition
- **Purpose**: Keeps the agent focused on one atomic objective at a time.
- **Key Sections**:
  - Phased Roadmap (Phase 1 to Phase N)
  - Checkbox Checklist (`- [ ]` / `- [x]`)
  - Dependency Order & Verification Criteria per task

### 6. `MEMORY.md` — Persistent Episodic Context
- **Purpose**: Preserves institutional memory across agent compactions and resets.
- **Key Sections**:
  - Architectural Decisions & Tradeoffs (ADRs)
  - Resolved Bug Log (Symptom, Root Cause, Fix)
  - Known Technical Debt & Future Considerations

---

## Agent Setup Workflow
1. Initialize repository.
2. Generate all 6 files inside `.agent/`.
3. Read `.agent/RULES.md` and `.agent/PRD.md` before writing code.
4. Update `.agent/TASKS.md` after completing each milestone.
5. Record non-obvious fixes in `.agent/MEMORY.md`.
