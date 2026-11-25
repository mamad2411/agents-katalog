---
name: adr-gatekeeper
description: "This skill manages the enforcement and auditing of Architectural Decision Records (ADRs) within the project. It ensures that all architectural changes are documented, reviewed, and compliant with the project's established standards."
---

# ADR Gatekeeper Skill


This skill manages the enforcement and auditing of Architectural Decision Records (ADRs) within the project. It ensures that all architectural changes are documented, reviewed, and compliant with the project's established standards.

## Triggers
- User requests to "audit ADRs", "run gatekeeper", or "check ADR compliance".
- During significant architectural refactoring or new feature implementation that impacts the system's core structure.
- When a Pull Request is being prepared and requires an architectural review.

## Execution Instructions
When this skill is triggered:
1. Verify that `scripts/adr_gatekeeper.py` exists in the project root.
2. Execute the script: `python3 scripts/adr_gatekeeper.py` (or `python scripts/adr_gatekeeper.py` depending on the environment).
3. Analyze the output of the script.
4. If the gatekeeper identifies missing ADRs or compliance issues, proactively suggest the necessary updates or new ADR entries to the user.
5. If the gatekeeper confirms compliance, provide a summary of the status to the user.

## Integration
This skill works in tandem with the `setup_adr_gatekeeper.py` script which initializes the necessary files and GitHub Actions workflows.
