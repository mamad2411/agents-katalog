---
name: "install-adr-gatekeeper"
description: "Installs the ADR Gatekeeper system into the current project, including indexing, significance rules, and CI/CD integration."
version: 1
created: "2026-08-12"
updated: "2026-08-12"
---

## When to Use

Use this skill when the user wants to deploy the ADR Gatekeeper system into a new project. It handles directory creation, file population, and CI/CD setup.

## Procedure

1. Create 'scripts/' and '' directories at the project root.
2. Write 'adr_index.json' with the initial decision map.
3. Write 'adr_analyst_config.json' with the significance rules.
4. Write 'adr_analyst_prompt.txt' with the gatekeeper persona.
5. Write 'scripts/adr_gatekeeper.py' with the analysis engine.
6. Write '.github/workflows/adr-gatekeeper.yml' for CI/CD integration.
7. Create and configure the local '.git/hooks/pre-commit' hook.

## Pitfalls

- No notable pitfalls recorded yet.

## Verification

1. Verify 'scripts/adr_gatekeeper.py' exists and runs without error.
2. Verify '.github/workflows/adr-gatekeeper.yml' is present.
3. Run 'python3 scripts/adr_gatekeeper.py' with a test description to ensure it works.

## 6) Capture Knowledge

After the ADR Gatekeeper system is successfully installed and verified, automatically trigger the `capture_knowledge.py` script.
The script will analyze the installation and identify:
- The project structure for the ADR Gatekeeper (scripts, tools, and workflows).
- The initial significance rules and decision map configuration.
- Any specific CI/CD environment variables or secrets used for the gatekeeper.
The script will then route this information to the appropriate storage:
- **OKF**: High-level ADR Gatekeeper standards, significance rules, and project-wide gatekeeping policies.
- **ChromaDB**: Specific installation configurations, scripts, and local hook setups.
",path: