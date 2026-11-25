---
name: databricks-workspace-files
description: This skill enables exploration of Databricks workspace files using the Databricks CLI. It should be used when listing, browsing, or pulling files from Databricks workspaces into context for code review, debugging, or understanding existing notebooks and scripts. Supports .py, .sql, and .ipynb files.
---

# Databricks Workspace Files

## Overview

This skill provides workflows for exploring and retrieving code from Databricks workspaces using the Databricks CLI. It supports listing workspace contents, navigating directory structures, and pulling notebook/script content into context.

## Prerequisites

The Databricks CLI must be installed and configured with authentication. Verify setup by running:

```bash
databricks auth profiles
```

## Core Operations

### Listing Workspace Contents

To list files and directories at a workspace path:

```bash
databricks workspace list /path/to/directory
```

To list the root workspace:

```bash
databricks workspace list /
```

Common root directories:
- `/Repos` - Git-connected repositories
- `/Users` - User home directories (e.g., `/Users/username@company.com`)
- `/Shared` - Shared workspace files
- `/Workspace` - General workspace storage

To explore recursively, use the bundled helper script:

```bash
python scripts/list_workspace.py /path/to/directory --recursive --max-depth 3
```

This script provides tree-style output with type indicators ([DIR], [NB], [FILE]).

### Retrieving File Contents

To export a notebook or file and display its contents:

```bash
databricks workspace export /path/to/notebook --format SOURCE
```

The `--format SOURCE` flag exports notebooks in their source format (.py, .sql, .r, .scala).

For Jupyter notebook format:

```bash
databricks workspace export /path/to/notebook --format JUPYTER
```

To save to a local file for detailed analysis:

```bash
databricks workspace export /path/to/notebook --format SOURCE -o /tmp/notebook.py
```

### Getting File Metadata

To get information about a specific workspace object:

```bash
databricks workspace get-status /path/to/object
```

This returns the object type (NOTEBOOK, DIRECTORY, FILE), language (for notebooks), and path.

## Workflow: Exploring a Workspace

When asked to explore or find code in a Databricks workspace:

1. Start by listing the relevant root directory based on context:
   - For user notebooks: `/Users/username@company.com`
   - For shared code: `/Shared`
   - For git repos: `/Repos`

2. Navigate through directories by listing each level until reaching the target

3. Once a file is located, export it to view contents:
   ```bash
   databricks workspace export /path/to/file --format SOURCE
   ```

4. For notebooks that need detailed analysis, save locally and use the Read tool:
   ```bash
   databricks workspace export /path/to/notebook --format SOURCE -o /tmp/notebook_name.py
   ```

## Common Patterns

### Finding notebooks by name

List directories and look for matching names. Example workflow to find notebooks containing "etl":

```bash
databricks workspace list /Users/user@company.com
# Look through output for relevant directories
databricks workspace list /Users/user@company.com/projects
# Continue until target is found
```

### Pulling multiple related files

When exploring a project, export related files to /tmp for comparison:

```bash
databricks workspace export /path/to/main.py --format SOURCE -o /tmp/main.py
databricks workspace export /path/to/utils.py --format SOURCE -o /tmp/utils.py
```

Then use the Read tool to load them into context.

## File Type Handling

| Extension | Export Format | Notes |
|-----------|--------------|-------|
| .py | SOURCE | Python notebooks/scripts |
| .sql | SOURCE | SQL notebooks |
| .ipynb | JUPYTER | Full Jupyter format with outputs |
| .r | SOURCE | R notebooks |
| .scala | SOURCE | Scala notebooks |

## Error Handling

Common issues and solutions:

- **"RESOURCE_DOES_NOT_EXIST"**: Path does not exist. Verify the path by listing the parent directory.
- **"PERMISSION_DENIED"**: User lacks access to the workspace path. Try a different path or check permissions.
- **Authentication errors**: Run `databricks auth profiles` to verify configuration.
