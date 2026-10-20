---
description: "Code style, naming, branching, commit, lint/format/test conventions for this repository. Loaded automatically for every file. Source of truth for how code should be written and reviewed."
applyTo: "**"
---

# Coding Conventions

## Style Guides Enforced

- Java: Standard Java conventions (no formatter config detected)
- JSP: Keep scriptlets minimal; prefer JSTL/EL if added later

## Linters / Formatters

| Tool                                | Config | Run command |
| ----------------------------------- | ------ | ----------- |
| _None detected — confirm with team_ |        |             |

## Type Checking

| Tool          | Strict? | Run command              |
| ------------- | ------- | ------------------------ |
| Java compiler | N/A     | Eclipse builder or javac |

## Naming Conventions

- Java classes: PascalCase (VehicleDAO, AddVehicleServlet)
- Methods/fields: camelCase
- Constants: UPPER_SNAKE_CASE
- JSP files: lowerCamel or descriptive (addVehicle.jsp, viewVehicles.jsp)
- Database: Tables and columns UPPER_SNAKE_CASE (VEHICLE_ID)

## Branching

- Model: _None detected — confirm with team_
- Branch name format: _None detected — confirm with team_

## Commit Messages

- Format: _None detected — confirm with team_
- Examples: _Add upon first team-confirmed commits_

## Pull Request Conventions

- Template: _None detected — confirm with team_
- Required checks: _None detected — confirm with team_
- Required reviewers: _None detected — confirm with team_

## Testing Conventions

- Test file naming: _None detected — confirm with team_
- Test naming: _None detected — confirm with team_
- Coverage requirements: _None detected — confirm with team_

## Documentation Conventions

- Inline doc style: Javadoc for public classes/methods when modified
- README required: Keep README.md updated on DB and run modes

## "Always Do" Rules

- Validate and sanitize user input server-side (not only via HTML attributes)
- Update AGENTS.md and dev-context instructions upon adding endpoints or ports

## "Never Do" Rules

- Do not commit real database passwords or secrets
- Do not edit binaries under WEB-INF/lib directly in place
