---
name: workspace-directory-convention
description: "Workspace-as-a-directory: a single ~/.craft-agent/workspaces/{id}/ folder holds config.json, automations.json, sessions/, sources/, skills/, statuses/ — every feature reads/writes its own subtree so the workspace is portable in one zip."
category: architecture
version: 1.0.0
version_origin: extracted
tags: [config, workspaces, directory-layout, portability]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: README.md
imported_at: 2026-04-18T00:00:00Z
---

# Workspace-as-a-directory convention

## When to use
- Multi-workspace desktop/CLI app where users want clean separation between "work" and "personal" context.
- You want users to be able to back up / share / sync an entire workspace by zipping one folder.
- Need atomic delete: removing a workspace = `rm -rf <workspace-dir>`.

## How it works
Layout: `~/.craft-agent/`
- `config.json` - app-level (workspace list, LLM connections).
- `credentials.enc` - encrypted secrets shared across workspaces.
- `preferences.json`, `theme.json` - app-wide user prefs.
- `workspaces/{id}/`
  - `config.json` - workspace settings.
  - `automations.json` - event-driven rules.
  - `theme.json` - workspace theme override.
  - `sessions/{session-id}/session.jsonl` + per-session subfolders (`long_responses/`, `plans/`).
  - `sources/{slug}/config.json` + `.credential-cache.json`.
  - `skills/{slug}/SKILL.md`.
  - `statuses/` - custom status workflow.

Each feature package (`sessions`, `sources`, `skills`, `automations`) exposes a `getWorkspace*Path(workspaceRoot)` helper and NEVER walks out of its subtree. That means moving a workspace folder = works. Deleting = atomic.

## Example
```ts
// Each feature gets its own subtree helper:
export const getWorkspaceSkillsPath = (root: string) => join(root, 'skills');
export const getWorkspaceSourcesPath = (root: string) => join(root, 'sources');
export const getWorkspaceSessionsPath = (root: string) => join(root, 'sessions');
export const getSessionPath = (root: string, id: string) => join(root, 'sessions', id);

// Anywhere that handles workspace lifecycle:
export async function deleteWorkspace(id: string) {
  await rm(join(config.workspacesRoot, id), { recursive: true, force: true });
}
```

## Gotchas
- Don't let ONE feature's code write outside its subtree - the portability guarantee only holds if it's actually enforced.
- Credentials stay at the APP level (`~/.craft-agent/credentials.enc`) because they cross workspace boundaries - users don't want to re-auth per workspace.
- When a user zips a workspace for sharing, remind them to NOT include `.credential-cache.json` - those are decrypted reconstructions of secrets.
- Workspace IDs should be GUIDs, not slugs - renaming a workspace shouldn't move its folder.
- A default-workspaces dir helper (`getDefaultWorkspacesDir()`) per-OS (macOS `~/Library/Application Support/...`, Linux `~/.config/...`, Windows `%APPDATA%\...`) keeps the layout OS-native.
