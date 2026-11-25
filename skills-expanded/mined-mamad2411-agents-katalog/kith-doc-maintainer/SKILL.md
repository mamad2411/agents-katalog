---
name: kith-doc-maintainer
description: Synchronizes AGENTS.md and README.md with the current codebase structure. Use when new components, services, or significant architectural changes are made to the Kith project.
---

# Kith Documentation Maintainer

This skill ensures that high-level project documentation stays in sync with the actual implementation.

## Workflow

1.  **Analyze Structure**:
    -   Use `list_directory` and `glob` to scan:
        -   `components/`: Identify new views, widgets, or organizational changes.
        -   `services/`: Identify new business logic services.
        -   `types/`: Identify new domain entities.
        -   `context/`: Identify new state providers.
    -   Read `App.tsx` to check for new navigation screens in the `Screen` enum.

2.  **Update AGENTS.md**:
    -   Update the **Directory Structure** section with accurate file lists and descriptions.
    -   Ensure the **Core Views** under `components/` are correctly summarized.
    -   Update **Key Technologies** if any new libraries are added to `package.json`.

3.  **Update README.md**:
    -   Update the **Features** section if new functionality (e.g., a new chart type or social feature) has been added.
    -   Update the **Project Structure** tree to reflect the current top-level organization.
    -   Ensure **Getting Started** steps remain accurate.

## Guidelines

-   **Conciseness**: Keep descriptions brief but informative.
-   **Accuracy**: Do not guess; verify file existence and purpose before adding to documentation.
-   **Consistency**: Maintain the existing formatting style in both `AGENTS.md` and `README.md`.