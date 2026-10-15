---
name: lcs-onboarding
description: |
  Generate developer-friendly onboarding documentation for an existing running project. Run when user asks to onboard a project, generate early project docs, or summarize the codebase for new engineers. Scans repository, extracts architecture, entrypoints, setup/run/test instructions, and writes lean markdown reports under .lcs/work-items/onboarding.md and .lcs/work-items/onboarding-map.md.
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Onboarding Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.
- Target outputs are saved directly to `.lcs/work-items/onboarding.md` and `.lcs/work-items/onboarding-map.md`. 

Purpose
- Automate initial onboarding documentation for an existing project.
- Scan repository structure, analyze configuration files, identify entry points, setup commands, and testing patterns.
- Produce a single high-quality overview document at `.lcs/work-items/onboarding.md` and a structural map document at `.lcs/work-items/onboarding-map.md`.

Trigger
- Activate when user requests "onboard project", "generate project docs", "buat dokumentasi onboarding", "summarize codebase", "lcs-onboarding", or similar.

Behavior Checklist
1. Scan the repository for crucial configuration files (e.g. package.json, requirements.txt, Cargo.toml, go.mod) and readme files.
2. Identify technology stack, language, main framework, and entrypoints.
3. Discover local setup commands, run commands, build commands, and test commands.
4. Extract primary environment variables or configuration options.
5. Create `.lcs/work-items/` directory if it does not exist.
6. Write the unified onboarding report to `.lcs/work-items/onboarding.md` matching the Output Template.
7. Write the structural map report to `.lcs/work-items/onboarding-map.md` listing impacted or key files, their functions, and system relations.
8. Update `.lcs/state.md` with:
   - `current_phase: onboarding`
   - `last_session_note: Generated onboarding documentation at .lcs/work-items/onboarding.md and onboarding-map.md`
   - `timestamp: <current-ISO-timestamp>`
9. End with the canonical Handoff section.

Output Template 1: .lcs/work-items/onboarding.md
Must be written in English.

# Project Onboarding: <Project Name>

## 1. Overview
- **Language & Stack**: <Languages, primary framework>
- **Core Purpose**: <Brief description of what the project does>
- **Key Entrypoints**:
  - `<file-path>`: <Purpose>

## 2. Setup & Local Development
### Prerequisites
<system requirements or tools needed>

### Installation
```bash
<install command>
```

### Running Locally
```bash
<run command>
```

### Environment Variables
| Variable | Description | Default / Example |
|----------|-------------|-------------------|
| `VAR_NAME` | <desc> | <example> |

## 3. Architecture & Code Structure
### Component Directory Map
- `path/`: <description>
- `another_path/`: <description>

### High-level Flow
<brief description of request/data flow>

## 4. Testing
### Running Tests
```bash
<test command>
```

### Coverage
<how to check test coverage if applicable>

---

Output Template 2: .lcs/work-items/onboarding-map.md
This file maps the key files and components in the project. Must be written in English.

# Codebase Map: <Project Name>

## Description
<One-line area summary of what this module/feature/codebase does>

## Key Files
This section lists only the existing files that are key to the architecture.
* **Configuration Files**:
  - `path/to/config-file.ext`
* **Entrypoints & Core Files**:
  - `path/to/core-file.ext`
* **Skills**:
  - `path/to/skill/SKILL.md`

## Rationale
* `<file-path>`: <One-line reason why this file exists or its role>
* `<file-path>`: <One-line reason why this file exists or its role>

## System Relations
<One-line explanation of how features/modules interact with other parts of the system>

---

## Handoff
Next recommended skill: lcs-explore
Next file to read: .lcs/work-items/onboarding.md
Current phase: onboarding
Current confidence: high
Blocking questions: None
Risks to carry forward: None
Suggested next command: Explore feature atau buat PRD
