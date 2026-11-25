---
name: upgrade-spring-boot
description: |
  A skill for upgrading Spring Boot projects to a newer version using the Arconia CLI and OpenRewrite recipes.
  Automates dependency version bumps, deprecated API replacements, and configuration updates.
license: Apache-2.0
compatibility: |
  Requires Arconia CLI (https://docs.arconia.io/arconia-cli/latest/update/spring-boot/).
  Agent must have network access to the project directory and build tools (Maven/Gradle).
metadata:
  category: development-tools
  tags: [java, spring-boot, upgrade, open-rewrite]
---

# Upgrade Spring Boot

## Overview
This skill automates the process of upgrading Spring Boot projects to a newer version using the **Arconia CLI**. It applies OpenRewrite recipes to update dependencies, replace deprecated APIs, and adjust configurations, reducing the manual effort required for major version upgrades.

---

## Instructions

### Prerequisites
- **Arconia CLI** must be installed and available in the system PATH.
- The project must use **Maven** or **Gradle** as the build tool.
- The project must be under version control (e.g., Git) so changes can be reviewed and reverted if needed.

### Supported Actions
- **Preview upgrade:** View changes before applying them.
- **Upgrade project:** Apply the upgrade to the specified Spring Boot version.
- **Verbose output:** Include detailed logs for troubleshooting.

---

## Parameters

### Input Format
All actions require a JSON object with the following structure:

```json
{
  "action": "<action>",
  "project_path": "<path-to-project>",
  [ "to_version": "<target-version>", ]
  [ "dry_run": <boolean>, ]
  [ "verbose": <boolean> ]
}
```

### Action-Specific Parameters

| Action       | Required Parameters       | Optional Parameters                     |
|--------------|---------------------------|-----------------------------------------|
| `preview`    | `project_path`            | `to_version`, `verbose`                 |
| `upgrade`    | `project_path`            | `to_version`, `dry_run`, `verbose`      |

- **`project_path`:** Path to the Spring Boot project directory.
- **`to_version`:** Target Spring Boot version (e.g., `"4.0"`). Defaults to `"4.0"`.
- **`dry_run`:** If `true`, preview changes without applying them. Defaults to `false`.
- **`verbose`:** If `true`, include detailed output. Defaults to `false`.

---

## Examples

### 1. Preview upgrade to Spring Boot 4.0
**Input:**
```json
{
  "action": "preview",
  "project_path": "./my-spring-boot-app",
  "to_version": "4.0",
  "verbose": true
}
```
**Output:**
List of changes that will be applied, including dependency updates, API replacements, and configuration adjustments.

---

### 2. Upgrade project to Spring Boot 4.0
**Input:**
```json
{
  "action": "upgrade",
  "project_path": "./my-spring-boot-app",
  "to_version": "4.0",
  "dry_run": false,
  "verbose": true
}
```
**Output:**
Confirmation of upgrade completion or error details if the upgrade fails.

---

### 3. Upgrade with build tool parameters
**Input:**
```json
{
  "action": "upgrade",
  "project_path": "./my-spring-boot-app",
  "to_version": "3.5.8",
  "dry_run": false,
  "verbose": false
}
```
**Output:**
Confirmation of upgrade, using default build tool parameters.

---

## Error Handling
- If **Arconia CLI** is not found:
  > `"Error: Arconia CLI is required but not installed. Install it from [Arconia CLI docs](https://docs.arconia.io/arconia-cli/latest/update/spring-boot/)."`
- If the project path is invalid or not a Spring Boot project:
  > `"Error: Invalid project path or not a Spring Boot project."`
- For upgrade failures:
  > Return the raw error message from the Arconia CLI.

---
## References
- [Arconia CLI Spring Boot Update Docs](https://docs.arconia.io/arconia-cli/latest/update/spring-boot/)
- [Arconia Migrations Spring Boot Guide](https://raw.githubusercontent.com/arconia-io/arconia-migrations/refs/heads/main/docs/spring-boot.md)
- [Agent Skills Specification](https://agentskills.io/specification)
