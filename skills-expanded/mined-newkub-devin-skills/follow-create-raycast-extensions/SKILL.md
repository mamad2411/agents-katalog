---
name: follow-create-raycast-extensions
description: Build Raycast Extensions with TypeScript, React and the Raycast API for macOS productivity
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-vite

---
## Goal

Build Raycast Extensions using TypeScript, React, and the Raycast API to boost productivity on macOS via the command palette and menu bar

## Scope

Use for building Raycast Extensions on macOS with TypeScript, React, and the Raycast API

- Packages: `@raycast/api` 2.x (requires Node >= 22 + React 19 — migrate with `bunx ray migrate`), `@raycast/utils` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-review-codebase` to summarize the tech stack in use
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create raycast extensions)
3. Record the reasons for choosing the stack and libraries for later reference (create raycast extensions)

### 2. Setup Environment

> Goal: Prepare the environment for Raycast extension development

1. Install Raycast on macOS and sign in
2. Check the Raycast CLI: `bunx ray --version` and `bunx ray whoami`
3. Confirm Node.js 22.14+ (`@raycast/api` 2.x requires Node `>=22.22.2`) and that Bun is installed

### 3. Create Extension Project

> Goal: Create the extension project with the CLI

1. Use the `Create Extension` command in Raycast (recommended), or scaffold from the terminal with `bun create raycast-extension -t {template}` (`npm init raycast-extension`)
2. Choose a template: `detail`, `form`, `list`, `menu-bar`, `no-view`, or `ai` (tools) — docs/api/examples at developers.raycast.com
3. Move the project into `desktop-apps/raycast-extensions/{extension-name}/`
4. Check the structure: `package.json`, `src/`, `tsconfig.json`

### 4. Configure Manifest

> Goal: Define the manifest in package.json per the Raycast schema

1. Edit `package.json` per the Raycast schema:

```json
{
  "$schema": "https://www.raycast.com/schemas/extension.json",
  "name": "{extension-name}",
  "title": "Extension Name",
  "description": "What this extension does",
  "icon": "extension-icon.png",
  "author": "your-username",
  "categories": ["Productivity"],
  "commands": [{ "name": "index", "title": "Command", "mode": "view" }],
  "dependencies": {
    "@raycast/api": "^2.3.1",
    "@raycast/utils": "^2.3.1"
  }
}
```

2. Choose `mode`: `view`, `no-view`, or `menu-bar`
3. Run `bun install`

### 5. Develop Commands

> Goal: Develop commands with the Raycast API
1. List Command:

```tsx
import { List, ActionPanel, Action } from "@raycast/api";

export default function Command() {
  return (
    <List>
      <List.Item title="Item" actions={<ActionPanel><Action title="Select" /></ActionPanel>} />
    </List>
  );
}
```

2. Form Command:

```tsx
import { Form, ActionPanel, Action } from "@raycast/api";

export default function Command() {
  return (
    <Form actions={<ActionPanel><Action.SubmitForm title="Create" /></ActionPanel>}>
      <Form.TextField id="title" title="Title" />
    </Form>
  );
}
```

3. Use the Raycast API:
   - Clipboard: `Clipboard.copy()`, `Clipboard.readText()`
   - Cache: `new Cache()`, `cache.set()`, `cache.get()`
   - Storage: `LocalStorage.setItem()`, `LocalStorage.getItem()`
   - Preferences: `getPreferenceValues<Preferences>()`

### 6. Test Extension

> Goal: Test the extension with develop, lint, and build
1. Run `bun install && bun run dev` (or `bunx ray develop`) — dev mode with hot reload
2. Run `bunx ray lint`
3. Run `bunx ray build` (or `bunx ray build -e dist` to validate the build)

### 7. Publish Extension

> Goal: Prepare the extension for publishing to the Raycast Store
1. Create screenshots in `metadata/`
2. Update `CHANGELOG.md`
3. Fork https://github.com/raycast/extensions
4. Copy the extension into `extensions/{extension-name}/`
5. Create a Pull Request
6. For updates: `bunx ray publish`

## Rules

### 1. Structure

```
desktop-apps/raycast-extensions/{extension}/
├── src/
│   ├── index.tsx
│   ├── components/
│   ├── hooks/
│   ├── types/
│   └── utils/
├── assets/
│   └── icon.png (512x512)
├── metadata/
│   └── screenshot-1.png
├── package.json
├── tsconfig.json
├── CHANGELOG.md
└── README.md
```

### 2. Standards

- Use `bunx` for the Raycast CLI (`ray` ships with `@raycast/api`)
- Use Raycast UI: `List`, `Grid`, `Form`, `Detail`, `ActionPanel`
- `CHANGELOG.md` is required — no `version` in the manifest (the Store handles versioning)
- Use `@raycast/eslint-plugin`
- Upgrade the API with `bunx ray migrate` or the codemod `bunx @raycast/migration .`

### 3. Command Modes

| Mode | Use Case |
|------|----------|
| `view` | Show UI |
| `no-view` | Background script |
| `menu-bar` | Menu bar |

- Use /follow-create-sdk if needed
- Use /follow-tool-vite if needed

## Expected Outcome

- Extension created with `bunx create-raycast-extension`
- Manifest is valid
- Commands work
- Raycast API is usable
- Build passes with `bunx ray build`
- Ready to publish to the Raycast Store
