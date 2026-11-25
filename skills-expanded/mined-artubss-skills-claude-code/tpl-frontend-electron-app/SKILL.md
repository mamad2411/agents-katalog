---
name: tpl-frontend-electron-app
description: Template do pack (frontend/12-electron-app.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/12-electron-app.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/12-electron-app.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Electron 30 + TypeScript + React
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Desktop Runtime | Electron | 30+ |
| UI Framework | React | 19+ |
| Linguagem | TypeScript | 5.x (strict) |
| Bundler (renderer) | Vite | 5.x |
| Bundler (main/preload) | electron-builder + tsc | — |
| Estilização | Tailwind CSS | v4 |
| State (renderer) | Zustand | 4.x |
| Packaging | electron-builder | 24+ |
| Testes | Vitest + Playwright (E2E) | latest |

---

## ARQUITETURA: TRÊS PROCESSOS

```
┌─────────────────────────────────────────────────────┐
│  MAIN PROCESS (Node.js)                              │
│  src/main/                                           │
│  • Acesso ao sistema de arquivos                     │
│  • Janelas (BrowserWindow)                           │
│  • Menu, tray, notificações                          │
│  • Chamadas nativas do OS                            │
│  • ipcMain.handle() — responde chamadas do renderer  │
└──────────────────┬──────────────────────────────────┘
                   │ IPC (seguro, via preload)
┌──────────────────▼──────────────────────────────────┐
│  PRELOAD SCRIPT (Node.js + browser context)          │
│  src/preload/                                        │
│  • ÚNICO ponto de comunicação entre main e renderer  │
│  • contextBridge.exposeInMainWorld()                 │
│  • Expõe APENAS a API necessária — não o Node.js     │
└──────────────────┬──────────────────────────────────┘
                   │ window.api.*
┌──────────────────▼──────────────────────────────────┐
│  RENDERER PROCESS (Chromium + React)                 │
│  src/renderer/                                       │
│  • React app normal — sem acesso ao Node.js          │
│  • Chama window.api.xxx() para operações nativas     │
│  • Bundled pelo Vite                                 │
└─────────────────────────────────────────────────────┘
```

---

## PROJECT STRUCTURE

```
├── electron-builder.config.ts      # Configuração de packaging
├── vite.config.ts                  # Config do renderer (React)
├── tsconfig.json                   # Base tsconfig
├── tsconfig.main.json              # TypeScript para main + preload
├── tsconfig.renderer.json          # TypeScript para renderer (React)
├── src/
│   ├── main/                       # Main process — Node.js APENAS
│   │   ├── index.ts                # Entry point — cria BrowserWindow
│   │   ├── ipc/
│   │   │   ├── fs-handlers.ts      # ipcMain.handle para filesystem
│   │   │   ├── app-handlers.ts     # app.getVersion(), dialog, etc.
│   │   │   └── index.ts            # Registra todos os handlers
│   │   ├── windows/
│   │   │   ├── main-window.ts      # Configuração da janela principal
│   │   │   └── splash-window.ts    # Splash screen opcional
│   │   ├── services/
│   │   │   ├── auto-updater.ts     # electron-updater
│   │   │   ├── store.ts            # electron-store (persistência nativa)
│   │   │   └── logger.ts           # electron-log
│   │   └── utils/
│   │       └── is-dev.ts           # app.isPackaged check
│   ├── preload/
│   │   ├── index.ts                # contextBridge.exposeInMainWorld
│   │   └── api.d.ts                # TypeScript types para window.api
│   └── renderer/                   # React app — browser APENAS
│       ├── index.html
│       ├── src/
│       │   ├── main.tsx            # ReactDOM.createRoot
│       │   ├── App.tsx
│       │   ├── components/
│       │   │   ├── ui/
│       │   │   └── features/
│       │   ├── hooks/
│       │   │   └── useElectronApi.ts  # Wrapper para window.api
│       │   ├── stores/
│       │   │   └── app.store.ts    # Zustand store
│       │   ├── pages/
│       │   └── types/
│       │       └── electron.d.ts   # Redeclara window.api
├── resources/
│   ├── icon.icns                   # macOS
│   ├── icon.ico                    # Windows
│   └── icon.png                    # Linux
├── dist/                           # Output do build
└── release/                        # Output do packaging
```

---

## SEPARAÇÃO DE AMBIENTES — REGRA OURO

```
MAIN PROCESS pode:
  ✅ Importar módulos Node.js (fs, path, child_process)
  ✅ Acessar electron (app, BrowserWindow, ipcMain, dialog, shell)
  ✅ Usar electron-store, electron-log, electron-updater
  ❌ NUNCA importar código de src/renderer/

PRELOAD pode:
  ✅ Importar tipos do renderer (apenas types)
  ✅ Chamar ipcRenderer.invoke()
  ✅ Usar contextBridge
  ❌ NUNCA expor objetos Node.js inteiros (require, process, fs)
  ❌ NUNCA colocar lógica de negócio aqui

RENDERER pode:
  ✅ Importar qualquer pacote NPM puro (React, Zustand, etc.)
  ✅ Acessar window.api (o que o preload expôs)
  ❌ NUNCA importar electron, fs, path ou qualquer módulo Node.js
  ❌ NUNCA usar require() — apenas import (ESM)
```

---

## IPC COMMUNICATION

### 1. Definir a API no Preload

```typescript
// src/preload/index.ts
import { contextBridge, ipcRenderer } from 'electron';

// Definir o tipo da API
export type ElectronAPI = {
  fs: {
    readFile: (path: string) => Promise<string>;
    writeFile: (path: string, content: string) => Promise<void>;
    openDialog: (options: Electron.OpenDialogOptions) => Promise<string[]>;
  };
  app: {
    getVersion: () => Promise<string>;
    quit: () => void;
    minimize: () => void;
    maximize: () => void;
  };
  updater: {
    checkForUpdates: () => Promise<void>;
    onUpdateAvailable: (cb: (info: UpdateInfo) => void) => () => void;
  };
};

contextBridge.exposeInMainWorld('api', {
  fs: {
    readFile: (path: string) => ipcRenderer.invoke('fs:readFile', path),
    writeFile: (path: string, content: string) =>
      ipcRenderer.invoke('fs:writeFile', path, content),
    openDialog: (options: Electron.OpenDialogOptions) =>
      ipcRenderer.invoke('fs:openDialog', options),
  },
  app: {
    getVersion: () => ipcRenderer.invoke('app:getVersion'),
    quit: () => ipcRenderer.send('app:quit'),
    minimize: () => ipcRenderer.send('app:minimize'),
    maximize: () => ipcRenderer.send('app:maximize'),
  },
  updater: {
    checkForUpdates: () => ipcRenderer.invoke('updater:checkForUpdates'),
    onUpdateAvailable: (cb) => {
      const listener = (_: unknown, info: UpdateInfo) => cb(info);
      ipcRenderer.on('updater:updateAvailable', listener);
      // Retorna função de cleanup (remover listener)
      return () => ipcRenderer.removeListener('updater:updateAvailable', listener);
    },
  },
} satisfies ElectronAPI);
```

### 2. Registrar Handlers no Main

```typescript
// src/main/ipc/fs-handlers.ts
import { ipcMain, dialog } from 'electron';
import { readFile, writeFile } from 'fs/promises';

export function registerFsHandlers() {
  ipcMain.handle('fs:readFile', async (_event, path: string) => {
    // Validar path — nunca confiar cegamente no input do renderer
    if (!path || typeof path !== 'string') {
      throw new Error('Path inválido');
    }
    return readFile(path, 'utf-8');
  });

  ipcMain.handle('fs:writeFile', async (_event, path: string, content: string) => {
    await writeFile(path, content, 'utf-8');
  });

  ipcMain.handle('fs:openDialog', async (_event, options: Electron.OpenDialogOptions) => {
    const result = await dialog.showOpenDialog(options);
    return result.filePaths;
  });
}

// src/main/ipc/index.ts
export function registerAllHandlers() {
  registerFsHandlers();
  registerAppHandlers();
  registerUpdaterHandlers();
}
```

### 3. Usar no Renderer

```typescript
// src/renderer/src/hooks/useElectronApi.ts
// Wrapper seguro — verifica se window.api existe (dev vs. web?)
export function useElectronApi() {
  const api = (window as Window & { api?: ElectronAPI }).api;
  if (!api) throw new Error('Electron API não disponível — não é um ambiente Electron');
  return api;
}

// Em componente React:
export function FileEditor() {
  const api = useElectronApi();
  const [content, setContent] = useState('');

  async function handleOpen() {
    const [path] = await api.fs.openDialog({
      properties: ['openFile'],
      filters: [{ name: 'Text', extensions: ['txt', 'md'] }],
    });
    if (path) {
      const text = await api.fs.readFile(path);
      setContent(text);
    }
  }

  return (
    <div>
      <button onClick={handleOpen}>Abrir Arquivo</button>
      <textarea value={content} onChange={e => setContent(e.target.value)} />
    </div>
  );
}
```

---

## SECURITY RULES — OBRIGATÓRIAS

```typescript
// src/main/windows/main-window.ts
export function createMainWindow(): BrowserWindow {
  return new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      contextIsolation: true,          // ✅ OBRIGATÓRIO — isola contextos
      nodeIntegration: false,          // ✅ OBRIGATÓRIO — renderer não acessa Node.js
      sandbox: true,                   // ✅ Recomendado — isola ainda mais o renderer
      webSecurity: true,               // ✅ NUNCA desabilitar em produção
      allowRunningInsecureContent: false, // ✅ NUNCA true
    },
  });
}
```

**Por que estas configurações são críticas:**
- `contextIsolation: true` — sem isso, uma XSS no renderer pode executar código Node.js.
- `nodeIntegration: false` — sem isso, `require('fs')` funciona no renderer (crítico).
- `sandbox: true` — bloqueia acesso a APIs Chromium nativas não expostas.

**Validação de IPC navegação:**
```typescript
// src/main/index.ts — bloquear navegação para URLs externas
app.on('web-contents-created', (_event, contents) => {
  contents.on('will-navigate', (event, url) => {
    const allowedOrigins = ['http://localhost:5173', 'app://'];
    if (!allowedOrigins.some(origin => url.startsWith(origin))) {
      event.preventDefault();
    }
  });

  contents.setWindowOpenHandler(({ url }) => {
    // Abrir links externos no browser do OS, não no Electron
    if (url.startsWith('https://')) {
      shell.openExternal(url);
    }
    return { action: 'deny' };
  });
});
```

---

## ROUTING TABLE

| Trigger | Onde Corre | Mecanismo | Descrição |
|---------|-----------|-----------|-----------|
| App inicia | Main | `app.whenReady()` | Cria BrowserWindow, carrega renderer |
| Renderer pronto | Main | `did-finish-load` | Esconde splash, mostra main window |
| Usuário clica "Abrir arquivo" | Renderer → Main | `window.api.fs.openDialog()` → `ipcMain.handle('fs:openDialog')` | Dialog nativo |
| Usuário salva arquivo | Renderer → Main | `window.api.fs.writeFile()` → `ipcMain.handle('fs:writeFile')` | Escrita em disco |
| Atualização disponível | Main → Renderer | `ipcRenderer.on('updater:updateAvailable')` | Evento push do main ao renderer |
| Usuário clica "Atualizar" | Renderer → Main | `window.api.updater.installUpdate()` | Reinicia e instala |
| Usuário fecha janela | Main | `BrowserWindow.on('close')` | Salvar estado antes de fechar |
| Link externo clicado | Main | `setWindowOpenHandler` | Abrir no browser nativo |
| Menu nativo > Fechar | Main | `ipcMain.on('app:quit')` | `app.quit()` |

---

## ELECTRON-BUILDER CONFIG

```typescript
// electron-builder.config.ts
import { Configuration } from 'electron-builder';

const config: Configuration = {
  appId: 'com.minhaempresa.meuapp',
  productName: 'Meu App',
  directories: {
    output: 'release',
    buildResources: 'resources',
  },
  files: [
    'dist/**/*',        // renderer build (Vite output)
    'dist-main/**/*',   // main + preload build (tsc output)
    'resources/**/*',
  ],
  win: {
    target: ['nsis', 'portable'],
    icon: 'resources/icon.ico',
    signingHashAlgorithms: ['sha256'],
  },
  mac: {
    target: ['dmg', 'zip'],
    icon: 'resources/icon.icns',
    category: 'public.app-category.productivity',
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: 'resources/entitlements.mac.plist',
    entitlementsInherit: 'resources/entitlements.mac.plist',
  },
  linux: {
    target: ['AppImage', 'deb'],
    icon: 'resources/icon.png',
    category: 'Utility',
  },
  publish: {
    provider: 'github',
    owner: 'minha-org',
    repo: 'meu-app',
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
  },
};

export default config;
```

---

## AUTO-UPDATER

```typescript
// src/main/services/auto-updater.ts
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';

export function setupAutoUpdater(mainWindow: BrowserWindow) {
  autoUpdater.logger = log;
  autoUpdater.autoDownload = false; // pedir confirmação antes de baixar

  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('updater:updateAvailable', info);
  });

  autoUpdater.on('update-downloaded', () => {
    mainWindow.webContents.send('updater:updateReady');
  });

  autoUpdater.on('error', (err) => {
    log.error('Auto-updater error:', err);
  });

  // Verificar após 3 segundos de inicialização
  setTimeout(() => autoUpdater.checkForUpdates(), 3000);
}
```

---

## PERSISTÊNCIA (electron-store)

```typescript
// src/main/services/store.ts
import Store from 'electron-store';

interface AppStore {
  windowBounds: { width: number; height: number; x: number; y: number };
  recentFiles: string[];
  theme: 'light' | 'dark' | 'system';
  lastOpenedPath: string | null;
}

export const store = new Store<AppStore>({
  defaults: {
    windowBounds: { width: 1200, height: 800, x: 0, y: 0 },
    recentFiles: [],
    theme: 'system',
    lastOpenedPath: null,
  },
});

// Salvar posição e tamanho da janela ao fechar
export function persistWindowBounds(window: BrowserWindow) {
  window.on('close', () => {
    store.set('windowBounds', window.getBounds());
  });
}
```

---

## TESTES

```typescript
// src/renderer/src/components/FileEditor.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import { FileEditor } from './FileEditor';

// Mock da window.api
vi.stubGlobal('api', {
  fs: {
    openDialog: vi.fn().mockResolvedValue(['/mock/file.txt']),
    readFile: vi.fn().mockResolvedValue('conteúdo do arquivo'),
    writeFile: vi.fn().mockResolvedValue(undefined),
  },
});

describe('FileEditor', () => {
  it('abre arquivo e exibe conteúdo', async () => {
    render(<FileEditor />);
    fireEvent.click(screen.getByText('Abrir Arquivo'));
    expect(await screen.findByDisplayValue('conteúdo do arquivo')).toBeTruthy();
  });
});
```

```typescript
// tests/e2e/app.spec.ts (Playwright com Electron)
import { test, expect, _electron as electron } from '@playwright/test';

test('app abre a janela principal', async () => {
  const app = await electron.launch({ args: ['dist-main/main/index.js'] });
  const window = await app.firstWindow();
  await expect(window).toHaveTitle('Meu App');
  await app.close();
});
```

---

## QUALITY GATES

- [ ] `npx tsc -p tsconfig.main.json --noEmit` — main + preload sem erros
- [ ] `npx tsc -p tsconfig.renderer.json --noEmit` — renderer sem erros
- [ ] `npx vitest run` — testes unitários passando
- [ ] `npx playwright test` — testes e2e passando
- [ ] `contextIsolation: true` e `nodeIntegration: false` em TODAS as janelas
- [ ] Nenhum import de `electron`, `fs`, `path` em `src/renderer/`
- [ ] Nenhum módulo Node.js exposto diretamente via `contextBridge`
- [ ] IPC handlers validam e sanitizam todos os inputs
- [ ] Links externos abertos via `shell.openExternal()`, nunca no renderer
- [ ] `will-navigate` bloqueado para URLs não-autorizadas
- [ ] `electron-builder` gera instalador funcional: `npm run make`
- [ ] `auto-updater` configurado para produção antes do release

---

## FORBIDDEN

```
❌ NUNCA usar nodeIntegration: true — risco crítico de segurança
❌ NUNCA usar contextIsolation: false — idem
❌ NUNCA expor `require`, `process`, `fs` via contextBridge
❌ NUNCA importar módulos Node.js (fs, path, child_process) em src/renderer/
❌ NUNCA importar módulos do renderer em src/main/
❌ NUNCA usar webSecurity: false em produção
❌ NUNCA confiar cegamente em dados vindos do renderer — sempre validar no handler
❌ NUNCA usar eval() ou new Function() no renderer
❌ NUNCA abrir URLs externas diretamente no BrowserWindow — usar shell.openExternal()
❌ NUNCA hardcodar paths absolutos — usar path.join(__dirname, ...)
❌ NUNCA usar any em TypeScript — sempre tipar ElectronAPI explicitamente
❌ NUNCA commitar arquivos de resources/keys ou certificados de code signing
❌ NUNCA commit sem rodar quality gates
```

---

## COMMANDS

```bash
# Dev (main + renderer simultaneamente)
npm run dev

# Build separado
npm run build:main      # tsc -p tsconfig.main.json
npm run build:renderer  # vite build

# Build completo
npm run build

# Packaging por plataforma
npm run make:win    # electron-builder --win
npm run make:mac    # electron-builder --mac
npm run make:linux  # electron-builder --linux

# Testes
npx vitest run
npx vitest --ui
npx playwright test
npx playwright test --ui

# Lint
npx eslint . --fix
npx tsc -p tsconfig.main.json --noEmit
npx tsc -p tsconfig.renderer.json --noEmit
```

---

## TSCONFIG.MAIN.JSON

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "moduleResolution": "node",
    "outDir": "dist-main",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src/main/**/*", "src/preload/**/*"],
  "exclude": ["src/renderer/**/*", "node_modules"]
}
```

## TSCONFIG.RENDERER.JSON

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["vite/client"]
  },
  "include": ["src/renderer/**/*"],
  "exclude": ["src/main/**/*", "src/preload/**/*", "node_modules"]
}
```
