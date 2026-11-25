---
name: royo-learn-onboarding
description: Initialize and verify royo-learn for a project, optionally install its integrations, then continue with capture-learning.
license: MIT
metadata:
  author: RoyoTech
  version: "2.0.0"
---

# Royo Learn Onboarding

## Use when

- royo-learn is being used in a project for the first time;
- an MCP call returns `project_not_found`;
- the project marker or setup state is uncertain.

## Workflow

1. Identify the intended project root and check for `<root>/.royo-learn/config.yaml`.
2. If the marker is absent, run `royo-learn init --project-root <root>` exactly once for that project root. Initialization is required; `setup install` is not a substitute.
3. Run `royo-learn doctor --project-root <root> --json` and resolve any reported failure before capturing a learning.
4. Optionally run `royo-learn setup install --agent all --project-root <root>` to register MCP and install skills for Claude Code, Codex, and OpenCode. This step is optional after initialization and is safe to repeat.
5. Load and follow `../capture-learning/SKILL.md` for capture eligibility, evidence, and output rules.

## Clarifications

- Initialize one store per project root, not one per working directory. Project discovery walks upward from a subfolder until it finds `.royo-learn/config.yaml`.
- Re-running init for the same root is idempotent; do not initialize every subfolder.
- `setup install` configures supported agents and installs every valid directory under `<root>/skills/`; it does not create the project store.
- The royo-learn project store and Engram memory are separate, independent stores. Initializing, reading, or writing one does not initialize, synchronize, or replace the other.

## Outcome

Return the project root, marker status, doctor result, whether optional setup ran, and whether control passed to `capture-learning`.
