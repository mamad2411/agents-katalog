# demo-extract

## When to use

- Whenever the orchestrator needs a codebase overview.

## Inputs

- `project_root` — absolute cwd.
- `repo_shape` — **required**, one of `single` / `monorepo`.
- `members` — **required**, never empty. One entry per member:
  ```
  members:
    - name: <member-a>
  ```

## Procedure

### Step 1 — read the manifest.
