---
name: vscode-settings
description: VS Code configuration, extensions, keybindings, and workspace optimization. Use when user mentions "vscode", "vs code", "vscode settings", "vscode extensions", "keybindings", "code editor", "workspace settings", "settings.json", "launch.json", "tasks.json", "vscode snippets", "devcontainer", "remote development", or customizing their VS Code setup.
---

# VS Code Settings

## Settings Hierarchy

Settings resolve in this order (later overrides earlier):

1. **Default settings** - built-in VS Code defaults
2. **User settings** - `~/.config/Code/User/settings.json` (Linux), `~/Library/Application Support/Code/User/settings.json` (macOS), `%APPDATA%\Code\User\settings.json` (Windows)
3. **Workspace settings** - `.vscode/settings.json` in workspace root
4. **Folder settings** - per-folder overrides in multi-root workspaces

Commit `.vscode/settings.json`, `extensions.json`, `tasks.json`, and `launch.json` to version control. Add user-specific paths to `.gitignore` if needed.

## Essential settings.json Configurations

### Editor

```jsonc
{
  "editor.fontSize": 14,
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active",
  "editor.inlineSuggest.enabled": true,
  "editor.stickyScroll.enabled": true,
  "editor.linkedEditing": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.cursorBlinking": "smooth",
  "editor.cursorSmoothCaretAnimation": "on",
  "editor.renderWhitespace": "boundary"
}
```

### Files and Search

```jsonc
{
  "files.autoSave": "onFocusChange",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/__pycache__": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/coverage": true,
    "**/.next": true,
    "**/build": true
  },
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true
  }
}
```

### Terminal

```jsonc
{
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.fontFamily": "'JetBrains Mono', monospace",
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.defaultProfile.linux": "bash",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.scrollback": 10000,
  "terminal.integrated.env.osx": {
    "FIG_NEW_SESSION": "1"
  },
  "terminal.integrated.shellArgs.osx": ["-l"],
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.copyOnSelection": true
}
```

## Keybinding Customization

Keybindings live in `keybindings.json`. Open with `Cmd+K Cmd+S` (macOS) or `Ctrl+K Ctrl+S` (Windows/Linux).

### Structure

```jsonc
[
  {
    "key": "ctrl+shift+d",
    "command": "editor.action.duplicateSelection"
  },
  {
    "key": "ctrl+shift+k",
    "command": "editor.action.deleteLines",
    "when": "editorTextFocus && !editorReadonly"
  }
]
```

### When Clauses

Common context keys for conditional bindings:

- `editorTextFocus` - cursor is in an editor
- `editorHasSelection` - text is selected
- `editorLangId == 'typescript'` - specific language
- `resourceExtname == '.json'` - specific file extension
- `inDebugMode` - debugger is active
- `sideBarVisible` - sidebar is open
- `terminalFocus` - terminal has focus

Combine with `&&`, `||`, `!`:

```jsonc
{
  "key": "ctrl+enter",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "\n" },
  "when": "terminalFocus && !terminalTextSelected"
}
```

### Key Chords

Two-part shortcuts:

```jsonc
{
  "key": "ctrl+k ctrl+c",
  "command": "editor.action.addCommentLine"
}
```

## Must-Have Extensions

### Recommended Extensions File

Create `.vscode/extensions.json` in your project:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-python.python"
  ],
  "unwantedRecommendations": []
}
```

### By Category

**Languages & Frameworks**: `ms-python.python`, `ms-python.vscode-pylance`, `golang.go`, `rust-lang.rust-analyzer`, `bradlc.vscode-tailwindcss`, `prisma.prisma`, `svelte.svelte-vscode`, `vue.volar`

**Git**: `eamodio.gitlens`, `mhutchie.git-graph`, `github.vscode-pull-request-github`

**Testing**: `vitest.explorer`, `ms-vscode.test-adapter-converter`, `hbenl.vscode-test-explorer`

**Productivity**: `usernamehw.errorlens`, `christian-kohler.path-intellisense`, `streetsidesoftware.code-spell-checker`, `mikestead.dotenv`, `yzhang.markdown-all-in-one`, `gruntfuggly.todo-tree`

**AI**: `github.copilot`, `github.copilot-chat`, `continue.continue`

**Formatting & Linting**: `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`, `stylelint.vscode-stylelint`, `editorconfig.editorconfig`

## Custom Snippets

### User Snippets

Open via `Cmd+Shift+P` > "Snippets: Configure Snippets". Choose a language or global scope.

`~/.config/Code/User/snippets/typescript.json`:

```json
{
  "Arrow Function": {
    "prefix": "af",
    "body": ["const ${1:name} = (${2:params}) => {", "  $0", "};"],
    "description": "Arrow function"
  },
  "Console Log Variable": {
    "prefix": "clv",
    "body": "console.log('${1:var}:', $1);",
    "description": "Log variable with label"
  },
  "Try Catch": {
    "prefix": "tc",
    "body": [
      "try {",
      "  $1",
      "} catch (error) {",
      "  ${2:console.error(error);}",
      "}"
    ]
  }
}
```

### Tabstops and Variables

- `$1`, `$2` - tab stops (cursor positions in order)
- `$0` - final cursor position
- `${1:default}` - placeholder with default text
- `${1|one,two,three|}` - choice list
- `$TM_FILENAME`, `$TM_DIRECTORY`, `$CURRENT_YEAR` - built-in variables
- `${TM_FILENAME_BASE/(.*)/${1:/pascalcase}/}` - variable transforms

### Project Snippets

Place in `.vscode/*.code-snippets` for project-scoped snippets:

```json
{
  "Component Template": {
    "scope": "typescriptreact",
    "prefix": "comp",
    "body": [
      "interface ${1:Component}Props {",
      "  $2",
      "}",
      "",
      "export function ${1:Component}({ $3 }: ${1:Component}Props) {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  );",
      "}"
    ]
  }
}
```

## tasks.json

### Build Tasks

```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "npm",
      "script": "build",
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "lint",
      "type": "shell",
      "command": "npx eslint . --ext .ts,.tsx",
      "problemMatcher": ["$eslint-stylish"]
    },
    {
      "label": "test",
      "type": "shell",
      "command": "npx vitest run",
      "group": { "kind": "test", "isDefault": true }
    }
  ]
}
```

### Problem Matchers

Define custom problem matchers for non-standard output:

```jsonc
{
  "label": "custom-build",
  "type": "shell",
  "command": "make build",
  "problemMatcher": {
    "owner": "custom",
    "fileLocation": ["relative", "${workspaceFolder}"],
    "pattern": {
      "regexp": "^(.+):(\\d+):(\\d+):\\s+(error|warning):\\s+(.+)$",
      "file": 1, "line": 2, "column": 3, "severity": 4, "message": 5
    }
  }
}
```

### Compound Tasks

Run multiple tasks together:

```jsonc
{
  "label": "build-and-test",
  "dependsOn": ["build", "test"],
  "dependsOrder": "sequence",
  "problemMatcher": []
}
```

## launch.json

### Node.js

```jsonc
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Node: Current File",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Node: Attach",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true
    }
  ]
}
```

### Python

```jsonc
{
  "name": "Python: Current File",
  "type": "debugpy",
  "request": "launch",
  "program": "${file}",
  "console": "integratedTerminal",
  "justMyCode": true,
  "env": { "PYTHONDONTWRITEBYTECODE": "1" }
}
```

### Go

```jsonc
{
  "name": "Go: Launch Package",
  "type": "go",
  "request": "launch",
  "mode": "auto",
  "program": "${workspaceFolder}",
  "env": {},
  "args": []
}
```

### Browser (Chrome)

```jsonc
{
  "name": "Chrome: Launch",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:3000",
  "webRoot": "${workspaceFolder}/src",
  "sourceMaps": true
}
```

## Multi-Root Workspaces

Create a `.code-workspace` file:

```json
{
  "folders": [
    { "name": "Frontend", "path": "./packages/frontend" },
    { "name": "Backend", "path": "./packages/backend" },
    { "name": "Shared", "path": "./packages/shared" }
  ],
  "settings": {
    "files.exclude": { "**/node_modules": true }
  },
  "extensions": {
    "recommendations": ["dbaeumer.vscode-eslint"]
  }
}
```

Per-folder settings override workspace settings. Open with `code project.code-workspace`.

## Dev Containers

### devcontainer.json

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Node.js Dev",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [3000, 5432],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  }
}
```

### With Dockerfile

```jsonc
{
  "name": "Custom Dev",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": { "NODE_VERSION": "20" }
  },
  "remoteUser": "node",
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,type=bind,readonly"
  ]
}
```

### Docker Compose

```jsonc
{
  "name": "Full Stack",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "shutdownAction": "stopCompose"
}
```

## Remote Development

**SSH**: Install "Remote - SSH" extension. Configure `~/.ssh/config`, then `Cmd+Shift+P` > "Remote-SSH: Connect to Host". VS Code installs its server on the remote automatically.

**WSL**: Install "WSL" extension. Run `code .` from a WSL terminal, or use `Cmd+Shift+P` > "WSL: Connect to WSL".

**Tunnels**: Run `code tunnel` on a remote machine to create a persistent tunnel. Connect from any browser at `vscode.dev` or from the desktop app via "Remote - Tunnels" extension. No SSH required.

## Extension Authoring Basics

Scaffold a new extension:

```bash
npm install -g yo generator-code
yo code
```

Minimal `package.json` contribution points:

```json
{
  "contributes": {
    "commands": [{
      "command": "myext.helloWorld",
      "title": "Hello World"
    }],
    "keybindings": [{
      "command": "myext.helloWorld",
      "key": "ctrl+shift+h"
    }],
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myext.enable": { "type": "boolean", "default": true }
      }
    }
  }
}
```

Register in `src/extension.ts`:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('myext.helloWorld', () => {
    vscode.window.showInformationMessage('Hello World!');
  });
  context.subscriptions.push(disposable);
}

export function deactivate() {}
```

Debug with `F5` (launches Extension Development Host). Publish with `vsce publish`.

## Profiles

Create profiles for different workflows: `Cmd+Shift+P` > "Profiles: Create Profile".

Use cases:
- **Frontend** - Tailwind, ESLint, Prettier, browser debug configs
- **Python** - Pylance, Ruff, Jupyter, Python debug configs
- **Writing** - Markdown extensions, zen mode defaults, spell checker
- **Minimal** - No extensions, clean UI for demos/screencasts

Export/import profiles as `.code-profile` files or share via GitHub Gist.

Switch profiles via the gear icon in the bottom-left or `Cmd+Shift+P` > "Profiles: Switch Profile".

## Settings Sync

Enable via `Cmd+Shift+P` > "Settings Sync: Turn On". Syncs:

- Settings, keybindings, snippets, extensions, UI state, profiles

Sign in with GitHub or Microsoft account. Choose what to sync in Settings Sync preferences.

For teams, commit `.vscode/settings.json` and `.vscode/extensions.json` instead of relying on sync. Keep personal preferences (theme, font size) in user settings only.

## Productivity Tips

**Multi-cursor**: `Alt+Click` to add cursors. `Cmd+D` to select next occurrence. `Cmd+Shift+L` to select all occurrences. `Cmd+Alt+Up/Down` to add cursors above/below.

**Emmet**: Type abbreviations and press `Tab` in HTML/JSX. `div.container>ul>li*3` expands to full markup. Works in JSX with `"emmet.includeLanguages": { "javascriptreact": "html" }`.

**Breadcrumbs**: Enable with `"breadcrumbs.enabled": true`. Navigate file path and symbol hierarchy at the top of the editor.

**Zen Mode**: `Cmd+K Z` to enter. Hides all UI chrome for focused editing. Configure with `"zenMode.hideLineNumbers"`, `"zenMode.centerLayout"`.

**Quick Open**: `Cmd+P` to open files by name. Add `:` for go-to-line, `@` for go-to-symbol, `#` for workspace symbol search.

**Command Palette**: `Cmd+Shift+P` for all commands. Type partial matches.

**Side-by-side editing**: `Cmd+\` to split. Drag tabs between groups. `Cmd+1/2/3` to focus groups.

**Timeline view**: Built-in local file history in the Explorer sidebar. Compare previous versions without Git.

**Sticky scroll**: Shows nested scope context at the top of the editor. Enable with `"editor.stickyScroll.enabled": true`.

## Project-Specific Formatter/Linter Configuration

### Per-Language Formatters

```jsonc
// .vscode/settings.json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.tabSize": 4,
    "editor.formatOnSave": true
  },
  "[go]": {
    "editor.defaultFormatter": "golang.go",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "files.trimTrailingWhitespace": false
  }
}
```

### ESLint + Prettier Coexistence

```jsonc
{
  "eslint.validate": ["javascript", "typescript", "javascriptreact", "typescriptreact"],
  "prettier.requireConfig": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

Order matters: Prettier formats first (on save), then ESLint fixes remaining issues (code action on save). Use `eslint-config-prettier` to disable ESLint rules that conflict with Prettier.

### Ruff for Python

```jsonc
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  }
}
```
