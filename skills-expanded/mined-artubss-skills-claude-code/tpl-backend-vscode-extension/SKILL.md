---
name: tpl-backend-vscode-extension
description: Template do pack (backend/13-vscode-extension.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/13-vscode-extension.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: VS Code Extension

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/13-vscode-extension.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Platform:** VS Code Extension API 1.90+
- **Language:** TypeScript 5.x (strict)
- **Bundler:** esbuild (via npm script)
- **Testing:** Mocha + @vscode/test-electron
- **UI Patterns:** TreeDataProvider, WebviewPanel, StatusBarItem
- **Publishing:** @vscode/vsce

---

## PROJECT STRUCTURE
```
src/
├── extension.ts              # activate() / deactivate() - entry point
├── commands/
│   ├── index.ts              # All command registrations
│   ├── openPanel.ts
│   └── refreshTree.ts
├── providers/
│   ├── MyTreeProvider.ts     # TreeDataProvider implementation
│   └── MyWebviewProvider.ts  # WebviewViewProvider implementation
├── views/
│   └── webview/
│       ├── index.html        # Webview HTML template
│       └── main.ts           # Webview-side script (compiled separately)
├── services/
│   └── config.ts             # WorkspaceConfiguration helpers
└── utils/
    └── logger.ts             # OutputChannel wrapper
test/
├── suite/
│   ├── index.ts              # Mocha runner
│   └── tree-provider.test.ts
└── runTests.ts               # Test entry
.vscode/
└── launch.json               # "Run Extension" + "Extension Tests" configs
package.json                  # contributes: commands, views, menus
tsconfig.json
esbuild.js                    # Build script
```

---

## ARCHITECTURE RULES
1. **`activate()` registers disposables** — every `vscode.commands.registerCommand`, event listener, and provider must be pushed to `context.subscriptions`.
2. **Activation events are specific** — never use `"*"` activationEvent in `package.json`; use `onCommand`, `onView`, `onLanguage`, etc.
3. **WebviewPanel uses nonce + CSP** — every webview HTML sets `Content-Security-Policy` with a unique nonce for `<script>` tags.
4. **Messages are typed** — define `ExtensionMessage` and `WebviewMessage` discriminated unions; never send untyped objects.
5. **Heavy work is async** — never block the extension host thread; use `vscode.window.withProgress` for long operations.
6. **WorkspaceFolder handling** — always check `vscode.workspace.workspaceFolders` before accessing files; handle multi-root.
7. **No bundled node_modules in VSIX** — mark all `vscode.*` as `external` in esbuild; dependencies must be bundled.

---

## ACTIVATION + COMMAND REGISTRATION

```typescript
// src/extension.ts
import * as vscode from 'vscode'
import { registerCommands }  from './commands/index.js'
import { MyTreeProvider }    from './providers/MyTreeProvider.js'
import { Logger }            from './utils/logger.js'

export function activate(context: vscode.ExtensionContext): void {
  const logger = new Logger('MyExtension')
  logger.info('Extension activated')

  // Register tree view
  const treeProvider = new MyTreeProvider(context)
  const treeView = vscode.window.createTreeView('myExtension.treeView', {
    treeDataProvider: treeProvider,
    showCollapseAll: true,
  })

  // All registrations pushed to subscriptions
  context.subscriptions.push(
    treeView,
    ...registerCommands(context, treeProvider, logger),
  )
}

export function deactivate(): void {
  // Cleanup handled by context.subscriptions dispose chain
}

// src/commands/index.ts
import * as vscode from 'vscode'
import type { MyTreeProvider } from '../providers/MyTreeProvider.js'
import type { Logger }         from '../utils/logger.js'

export function registerCommands(
  context: vscode.ExtensionContext,
  tree:    MyTreeProvider,
  logger:  Logger,
): vscode.Disposable[] {
  return [
    vscode.commands.registerCommand('myExtension.refresh', () => {
      tree.refresh()
      logger.info('Tree refreshed')
    }),
    vscode.commands.registerCommand('myExtension.openPanel', (item?: MyTreeItem) => {
      // Opens webview panel
      openWebviewPanel(context, item)
    }),
  ]
}
```

---

## TREEDATAPROVIDER PATTERN

```typescript
// src/providers/MyTreeProvider.ts
import * as vscode from 'vscode'

export class MyTreeItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly type:  'group' | 'item',
    public readonly data?: unknown,
  ) {
    super(
      label,
      type === 'group'
        ? vscode.TreeItemCollapsibleState.Collapsed
        : vscode.TreeItemCollapsibleState.None,
    )
    this.tooltip     = this.label
    this.contextValue = type
    if (type === 'item') {
      this.command = {
        command:   'myExtension.openPanel',
        title:     'Open',
        arguments: [this],
      }
    }
  }
}

export class MyTreeProvider implements vscode.TreeDataProvider<MyTreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<MyTreeItem | undefined>()
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event

  constructor(private readonly context: vscode.ExtensionContext) {}

  refresh(item?: MyTreeItem): void {
    this._onDidChangeTreeData.fire(item)
  }

  getTreeItem(element: MyTreeItem): MyTreeItem { return element }

  async getChildren(element?: MyTreeItem): Promise<MyTreeItem[]> {
    const folders = vscode.workspace.workspaceFolders
    if (!folders) return []
    if (!element) {
      return folders.map(f => new MyTreeItem(f.name, 'group'))
    }
    // Return items under the group
    return this.loadItems(element.label as string)
  }

  private async loadItems(folderName: string): Promise<MyTreeItem[]> {
    // Load data for this folder
    return [new MyTreeItem(`${folderName}/item-1`, 'item')]
  }
}
```

---

## WEBVIEW PANEL WITH CSP + NONCE

```typescript
// src/commands/openPanel.ts
import * as vscode from 'vscode'
import * as crypto from 'node:crypto'
import * as path   from 'node:path'
import * as fs     from 'node:fs'

export function openWebviewPanel(
  context: vscode.ExtensionContext,
  item?:   unknown,
): void {
  const panel = vscode.window.createWebviewPanel(
    'myExtension.panel',
    'My Panel',
    vscode.ViewColumn.Beside,
    {
      enableScripts:       true,
      localResourceRoots:  [vscode.Uri.joinPath(context.extensionUri, 'dist', 'webview')],
      retainContextWhenHidden: true,
    },
  )

  const nonce    = crypto.randomBytes(16).toString('base64')
  const scriptUri = panel.webview.asWebviewUri(
    vscode.Uri.joinPath(context.extensionUri, 'dist', 'webview', 'main.js')
  )

  panel.webview.html = getHtml(nonce, scriptUri, panel.webview)

  // Typed message passing
  panel.webview.onDidReceiveMessage((msg: WebviewMessage) => {
    if (msg.type === 'READY') {
      panel.webview.postMessage({ type: 'INIT', data: item } satisfies ExtensionMessage)
    }
  }, undefined, context.subscriptions)
}

type WebviewMessage = { type: 'READY' } | { type: 'UPDATE'; value: string }
type ExtensionMessage = { type: 'INIT'; data: unknown } | { type: 'ERROR'; message: string }

function getHtml(nonce: string, scriptUri: vscode.Uri, webview: vscode.Webview): string {
  const csp = `default-src 'none'; script-src 'nonce-${nonce}'; style-src ${webview.cspSource} 'unsafe-inline';`
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="${csp}">
  <title>My Panel</title>
</head>
<body>
  <div id="root"></div>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`
}
```

---

## ROUTING TABLE (Command → Handler)

| Command ID | Trigger | Handler | Action |
|-----------|---------|---------|--------|
| `myExtension.refresh` | Context menu / button | `registerCommands` | Refresh tree view |
| `myExtension.openPanel` | Tree item click | `openWebviewPanel` | Open WebviewPanel |
| `myExtension.configSet` | Command palette | `configCommand` | Update workspace config |
| `myExtension.showOutput` | Status bar click | `logger.show()` | Show output channel |
| `myExtension.runTask` | Command palette | `taskRunner` | `vscode.tasks.executeTask` |
| `onDidSaveTextDocument` | File save event | auto-handler | Re-analyze on save |
| `onDidChangeWorkspaceFolders` | Workspace change | `treeProvider.refresh()` | Refresh tree |
| `onDidChangeConfiguration` | Settings change | `configWatcher` | Apply new config |
| `myExtension.openSettings` | Command palette | — | `workbench.action.openSettings` |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] `vsce package` — VSIX builds without warnings
- [ ] All commands/views declared in `package.json` `contributes`
- [ ] No `activationEvents: ["*"]`
- [ ] Every `registerCommand` disposable in `context.subscriptions`
- [ ] Webview HTML has valid CSP with nonce
- [ ] `npm test` via `@vscode/test-electron` passes
- [ ] Extension size < 5 MB (check `vsce ls`)
- [ ] No `console.log` in activated code — use `OutputChannel`

---

## FORBIDDEN
- ❌ `activationEvents: ["*"]` — lazy activation only
- ❌ `setTimeout`/`setInterval` without cleanup on `deactivate`
- ❌ Webview `enableScripts: true` without CSP + nonce
- ❌ Accessing `vscode.workspace.rootPath` (deprecated) — use `workspaceFolders`
- ❌ Storing secrets in `context.globalState` — use `context.secrets` API
- ❌ Synchronous file I/O in event handlers — always `async`/`await`
- ❌ Registering disposables without adding to `context.subscriptions`
- ❌ Direct DOM calls from extension host code — all DOM work goes in the webview
