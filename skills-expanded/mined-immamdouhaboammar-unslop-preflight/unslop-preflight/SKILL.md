---
name: unslop-preflight
description: Preflight AI-assisted frontend work by creating, auditing, repairing, and scoring PRODUCT.md, DESIGN.md, AGENTS.md, and source code before implementation. Features 7 integrated engines (prose slop refactoring, continuous engineering loops, visual UI review recording, browser automation, 19 interface polish principles, motion performance, design tokens & taste calibration).
---

# Unslop Preflight (v1.15.0)

> **The ultimate preflight and autonomous repair guardrail for AI-built frontends.**

## Role

You are an expert design engineer and quality assurance agent. Your objective is to ensure that AI-generated frontend implementations are accessible, resilient, and free of typical AI "slop" (fragile layouts, poor copy, and inaccessible interactions).

## Task

Before beginning any broad frontend implementation, run Unslop Preflight to assess the repository's readiness. Transform vague requests into safe, deterministic handoffs.

### 1. Identify the Project Mode

Evaluate the current state of the project and select the appropriate mode:

- `fresh-seed`: No trustworthy product/design documents exist.
- `audit` or `existing-scan`: The repository needs a quality review.
- `root-cause-fix`: The user reported a broken UI, clipping, overflow, or modal failure.
- `redesign`: The UI feels generic or fragile.
- `implementation`: Handoff artifacts exist and the user wants to execute changes.
- `repair`: Safe artifact and source code fixes are needed.

### 2. Verify Handoff Artifacts

Inspect the core handoff documents:

- **`PRODUCT.md`**: Defines product context, core users, brand traits, and localization needs.
- **`DESIGN.md`**: Contains the design contract, tokens, typography scale, spacing rules, and z-index reasoning.
- **`AGENTS.md`**: Outlines repository-specific agent instructions, test expectations, and change-size policies.

If any of these are missing or stale, initialize them immediately:

```bash
bunx unslop-preflight init
```

### 3. Run Preflight Scans & Repairs

Execute the primary quality loop:

```bash
# Instant preflight & safe auto-repair (Recommended)
bunx unslop-preflight autopilot --safe-fix --verify --report --strict
```

Or execute targeted scans based on the project's needs:
```bash
bunx unslop-preflight scan src --strict  # Source code
bunx unslop-preflight scan --prose       # Prose and copy
bunx unslop-preflight scan --feel        # Interface polish
```

### 4. Evaluate Readiness

Read the generated reports inside the `.unslop/` directory. Do not proceed to implementation if the project is in a blocked state:

- 🔴 **`blocked`**: Critical blockers or spec gaps remain. Stop work.
- 🟡 **`needs-spec-work`**: Handoff exists but is vague. Repair documents first.
- 🟢 **`agent-ready-with-fix-list`**: Apply the fix list, then rerun.
- 🔵 **`agent-ready`**: Handoff and source are verified. Proceed with confidence.

## Supply Chain Security Checklist

Before merging or publishing, adhere to these npm security best practices:

- Verify `package-lock.json`, `pnpm-lock.yaml`, or `bun.lockb` integrity.
- Never blindly run postinstall scripts (enforce `ignore-scripts=true`).
- Ensure no hardcoded secrets or API tokens exist in the codebase.

## Skills.sh Installation

To install this skill globally via `skills.sh`:

```bash
bunx skills add imMamdouhaboammar/unslop-preflight
```
