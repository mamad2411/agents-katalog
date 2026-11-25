---
name: condominio-alexo
description: Implements a simple issue and publishes a short-lived preview.
---

# Condo Alexo

Use this skill for small issues marked with the `alexo` label.

Goal:

1. Understand the issue and confirm that it fits the fast flow.
2. Implement the smallest correct change.
3. Run the relevant project checks.
4. Create or update the PR when the environment allows it.
5. Publish a short-lived preview when the project has a preview command.
6. Comment on the issue with the summary, PR, and preview URL.

If the issue requires discovery, ambiguous business rules, or full homologation,
comment the reason and add `blocked:human-help`.
