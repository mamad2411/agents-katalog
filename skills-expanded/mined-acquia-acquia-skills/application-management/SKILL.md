---
name: application-management
description: "Use when finding a pipelines application ID or linking a repo before running any pipelines-cli command that needs --application-id."
license: Proprietary
compatibility: pipelines-cli>=1.x
metadata:
    category: deployment
    author: Acquia
    version: "1.0.0"
    tags: "pipelines-cli, acquia-cloud, applications, codebases"
    software_requirements: "pipelines-cli>=1.x"
---

# Application Management with Acquia Pipelines CLI

Use when:
- Finding your application ID or codebase ID
- Linking a local repository to an application
- Unlinking a repository from an application
- Listing available codebases

---

## List Applications

Find application IDs associated with your account:

```bash
pipelines list-applications
```

Output:

```
Applications:
  1g2i3b4b5o6u7s — My Drupal Site
  abc1234567890  — Client Project
```

Use the application ID (e.g. `1g2i3b4b5o6u7s`) in all subsequent pipeline commands.

---

## List Codebases

List codebases available to your account (used as an alternative to application IDs):

```bash
pipelines list-codebases
```

Output:

```
+--------------------------------------+--------------+--------+--------------+
| Codebase ID                          | Label        | Region | Applications |
+--------------------------------------+--------------+--------+--------------+
| abcd1234-5678-90ab-cdef-000000000000 | My Codebase  | us-east| 3            |
+--------------------------------------+--------------+--------+--------------+
```

### JSON output

```bash
pipelines list-codebases --format=json
```

Codebase IDs can be used anywhere `--application-id` is accepted via the `--codebase-id` flag.

---

## Link a Repository to an Application

Associate your local git repository with an application or codebase ID. This lets you run `pipelines start` without specifying `--application-id` every time.

### Link to an application

```bash
pipelines set-application-id --application-id=1g2i3b4b5o6u7s
```

Output:

```
The application id associated with this repository has been set to 1g2i3b4b5o6u7s
```

### Link to a codebase

```bash
pipelines set-application-id --codebase-id=abcd1234-5678-90ab-cdef-000000000000
```

### JSON output

```bash
pipelines set-application-id --application-id=1g2i3b4b5o6u7s --format=json
```

The association is stored in the repository's git config. After linking, commands like `pipelines start` will detect the application ID automatically from the current directory.

---

## Unlink a Repository

Remove the application ID association from the current repository:

```bash
pipelines remove-application-id
```

---

## Application ID vs Codebase ID

| | Application ID | Codebase ID |
|---|---|---|
| **Format** | Short alphanumeric string | UUID |
| **Scope** | Single Acquia Cloud application | Can span multiple applications |
| **Use when** | Working with a specific application | Working with a shared codebase |
| **Flag** | `--application-id` | `--codebase-id` |

Both can be used interchangeably with `start`, `status`, `logs`, and `list-jobs`.

---

## Troubleshooting

### "Unable to determine the application ID"

You haven't linked a repo or provided `--application-id`. Either:

```bash
# Option 1: Link the repo
pipelines set-application-id --application-id=<id>

# Option 2: Pass it explicitly each time
pipelines start --application-id=<id>
```

### "No codebases found"

Your account doesn't have any codebases, or your credentials don't have access. Verify with:

```bash
pipelines show-connection <application_id>
```

---

## Next Steps

- **[Run pipeline jobs](../pipeline-operations/SKILL.md)** — Start, monitor, and manage builds
- **[Getting started](../getting-started/SKILL.md)** — Installation and authentication
