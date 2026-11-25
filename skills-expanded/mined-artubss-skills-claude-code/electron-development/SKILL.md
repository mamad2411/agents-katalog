---
name: electron-development
description: "Domine desenvolvimento de apps Electron com IPC seguro, contextIsolation, scripts de preload, arquitetura multi-processo, empacotamento com electron-builder, assinatura de código e auto-atualização."
risk: safe
source: community
date_added: "2026-03-12"
---

# Desenvolvimento com Electron

Você é um engenheiro sênior em Electron especializado em arquitetura de aplicações desktop seguras, production-grade. Você possui expertise profunda no modelo multi-processo do Electron, padrões de segurança IPC, integração com SO nativo, empacotamento de aplicações, assinatura de código e estratégias de auto-atualização.

## Use esta skill quando

- Construir novas aplicações Electron desktop do zero
- Proteger um app Electron (contextIsolation, sandbox, CSP, nodeIntegration)
- Configurar comunicação IPC entre processos main, renderer e preload
- Empacotar e distribuir apps Electron com electron-builder ou electron-forge
- Implementar auto-atualização com electron-updater
- Debugar issues do processo principal ou crashes do renderer
- Gerenciar múltiplas janelas e ciclo de vida da aplicação
- Integrar funcionalidades nativas do SO (menus, tray, notificações, diálogos de arquivo)
- Otimizar performance e tamanho do bundle do app Electron

## Não use esta skill quando

- Construir aplicações web-only sem distribuição desktop → use `react-patterns`, `nextjs-best-practices`
- Construir apps Tauri (alternativa desktop baseada em Rust) → use `tauri-development` se disponível
- Construir extensões Chrome → use `chrome-extension-developer`
- Implementar lógica profunda de backend/servidor → use `nodejs-backend-patterns`
- Construir apps mobile → use `react-native-architecture` ou `flutter-expert`

## Instruções

1. Analise a estrutura do projeto e identifique limites entre processos.
2. Enforce padrões de segurança: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`.
3. Design canais IPC com whitelisting explícito no script de preload.
4. Implemente, teste e build com tooling apropriada.
5. Valide contra a Checklist de Segurança para Produção antes de fazer deploy.

---

## Áreas Principais de Expertise

### 1. Estrutura do Projeto & Arquitetura

**Layout de projeto recomendado:**
```
my-electron-app/
├── package.json
├── electron-builder.yml        # ou forge.config.ts
├── src/
│   ├── main/
│   │   ├── main.ts             # Entrada do processo main
│   │   ├── ipc-handlers.ts     # Handlers dos canais IPC
│   │   ├── menu.ts             # Menu da aplicação
│   │   ├── tray.ts             # System tray
│   │   └── updater.ts          # Lógica de auto-atualização
│   ├── preload/
│   │   └── preload.ts          # Bridge entre main ↔ renderer
│   ├── renderer/
│   │   ├── index.html          # HTML de entrada
│   │   ├── App.tsx             # Root da UI (React/Vue/Svelte/vanilla)
│   │   ├── components/
│   │   └── styles/
│   └── shared/
│       ├── constants.ts        # Nomes de canais IPC, enums compartilhados
│       └── types.ts            # Interfaces TypeScript compartilhadas
├── resources/
│   ├── icon.png                # Ícone da app (1024x1024)
│   └── entitlements.mac.plist  # Entitlements do macOS
├── tests/
│   ├── unit/
│   └── e2e/
└── tsconfig.json
```

**Princípios arquiteturais principais:**
- **Pontos de entrada separados**: Main, preload e renderer cada um com sua própria configuração de build.
- **Tipos compartilhados, não módulos compartilhados**: O diretório `shared/` contém apenas tipos, constantes e enums — nunca código executável importado através de limites de processos.
- **Mantenha o processo main enxuto**: Main deve orquestrar janelas, handle IPC e gerenciar ciclo de vida da app. Lógica de negócio pertence ao renderer ou a processos worker dedicados.

---

### 2. Modelo de Processos (Main / Renderer / Preload / Utility)

Electron executa **múltiplos processos** isolados por design:

| Processo | Papel | Acesso Node.js | Acesso DOM |
|----------|-------|----------------|------------|
| **Main** | Ciclo de vida da app, janelas, APIs nativas, hub IPC | ✅ Completo | ❌ Nenhum |
| **Renderer** | Renderização de UI, interação do usuário | ❌ Nenhum (por padrão) | ✅ Completo |
| **Preload** | Bridge seguro entre main e renderer | ✅ Limitado (via contextBridge) | ✅ Antes de carregar página |
| **Utility** | Tarefas CPU-intensivas, trabalho em background | ✅ Completo | ❌ Nenhum |

**BrowserWindow com padrões de segurança (OBRIGATÓRIO):**
```typescript
import { BrowserWindow } from 'electron';
import path from 'node:path';

function createMainWindow(): BrowserWindow {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // ── PADRÕES DE SEGURANÇA (NUNCA MUDE ESTES) ──
      contextIsolation: true,     // Isola preload do contexto renderer
      nodeIntegration: false,     // Previne require() no renderer
      sandbox: true,              // Sandboxing em nível de SO
      
      // ── SCRIPT DE PRELOAD ──
      preload: path.join(__dirname, '../preload/preload.js'),
      
      // ── HARDENING ADICIONAL ──
      webSecurity: true,          // Enforce same-origin policy
      allowRunningInsecureContent: false,
      experimentalFeatures: false,
    },
  });

  // Content Security Policy
  win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
        ],
      },
    });
  });

  return win;
}
```

> ⚠️ **CRÍTICO**: Nunca defina `nodeIntegration: true` ou `contextIsolation: false` em produção. Essas configurações expõem o renderer a ataques de execução remota de código (RCE) através de vulnerabilidades XSS.

---

### 3. Comunicação IPC Segura

IPC é o **único** canal seguro para comunicação entre processos main e renderer. Todo IPC deve fluir através do script de preload.

**Script de preload (contextBridge + whitelisting explícito):**
```typescript
// src/preload/preload.ts
import { contextBridge, ipcRenderer } from 'electron';

// ── WHITELIST: Expose apenas canais específicos ──
const ALLOWED_SEND_CHANNELS = [
  'file:save',
  'file:open',
  'app:get-version',
  'dialog:show-open',
] as const;

const ALLOWED_RECEIVE_CHANNELS = [
  'file:saved',
  'file:opened',
  'app:version',
  'update:available',
  'update:progress',
  'update:downloaded',
  'update:error',
] as const;

type SendChannel = typeof ALLOWED_SEND_CHANNELS[number];
type ReceiveChannel = typeof ALLOWED_RECEIVE_CHANNELS[number];

contextBridge.exposeInMainWorld('electronAPI', {
  // Uma via: renderer → main
  send: (channel: SendChannel, ...args: unknown[]) => {
    if (ALLOWED_SEND_CHANNELS.includes(channel)) {
      ipcRenderer.send(channel, ...args);
    }
  },

  // Duas vias: renderer → main → renderer (request/response)
  invoke: (channel: SendChannel, ...args: unknown[]) => {
    if (ALLOWED_SEND_CHANNELS.includes(channel)) {
      return ipcRenderer.invoke(channel, ...args);
    }
    return Promise.reject(new Error(`Channel "${channel}" is not allowed`));
  },

  // Uma via: main → renderer (subscriptions)
  on: (channel: ReceiveChannel, callback: (...args: unknown[]) => void) => {
    if (ALLOWED_RECEIVE_CHANNELS.includes(channel)) {
      const listener = (_event: Electron.IpcRendererEvent, ...args: unknown[]) => callback(...args);
      ipcRenderer.on(channel, listener);
      return () => ipcRenderer.removeListener(channel, listener);
    }
    return () => {};
  },
});
```

**Handlers IPC no processo main:**
```typescript
// src/main/ipc-handlers.ts
import { ipcMain, dialog, BrowserWindow } from 'electron';
import { readFile, writeFile } from 'node:fs/promises';

export function registerIpcHandlers(): void {
  // invoke() pattern: retorna um valor ao renderer
  ipcMain.handle('file:open', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: 'Text Files', extensions: ['txt', 'md'] }],
    });
    
    if (canceled || filePaths.length === 0) return null;
    
    const content = await readFile(filePaths[0], 'utf-8');
    return { path: filePaths[0], content };
  });

  ipcMain.handle('file:save', async (_event, filePath: string, content: string) => {
    // VALIDATE INPUTS — nunca confie cegamente em dados do renderer
    if (typeof filePath !== 'string' || typeof content !== 'string') {
      throw new Error('Invalid arguments');
    }
    await writeFile(filePath, content, 'utf-8');
    return { success: true };
  });

  ipcMain.handle('app:get-version', () => {
    return process.versions.electron;
  });
}
```

**Uso no renderer (type-safe):**
```typescript
// src/renderer/App.tsx — ou qualquer código renderer
// O electronAPI está globalmente disponível via contextBridge

declare global {
  interface Window {
    electronAPI: {
      send: (channel: string, ...args: unknown[]) => void;
      invoke: (channel: string, ...args: unknown[]) => Promise<unknown>;
      on: (channel: string, callback: (...args: unknown[]) => void) => () => void;
    };
  }
}

// Abrir um arquivo via IPC
async function openFile() {
  const result = await window.electronAPI.invoke('file:open');
  if (result) {
    console.log('File content:', result.content);
  }
}

// Subscrever a atualizações do processo main
const unsubscribe = window.electronAPI.on('update:available', (version) => {
  console.log('Update available:', version);
});

// Cleanup ao desmontar
// unsubscribe();
```

**Resumo de Padrões IPC:**

| Padrão | Método | Caso de Uso |
|--------|--------|------------|
| **Fire-and-forget** | `ipcRenderer.send()` → `ipcMain.on()` | Logging, telemetria, notificações não-críticas |
| **Request/Response** | `ipcRenderer.invoke()` → `ipcMain.handle()` | Operações de arquivo, diálogos, queries de dados |
| **Push ao renderer** | `webContents.send()` → `ipcRenderer.on()` | Atualizações de progresso, status de download, auto-update |

> ⚠️ **Nunca** use `ipcRenderer.sendSync()` em produção — bloqueia o event loop do renderer e congela a UI.

---

### 4. Hardening de Segurança

#### Checklist de Segurança para Produção

```
── OBRIGATÓRIO ──
[ ] contextIsolation: true
[ ] nodeIntegration: false
[ ] sandbox: true
[ ] webSecurity: true
[ ] allowRunningInsecureContent: false

── IPC ──
[ ] Preload usa contextBridge com whitelisting explícito de canais
[ ] Todos os inputs de IPC são validados no processo main
[ ] Nenhum ipcRenderer bruto exposto ao contexto renderer
[ ] Nenhum uso de ipcRenderer.sendSync()

── CONTEÚDO ──
[ ] Headers Content Security Policy (CSP) setados em todas as janelas
[ ] Nenhum uso de eval(), new Function(), ou innerHTML com dados untrusted
[ ] Conteúdo remoto (se houver) carregado em BrowserView separado com permissões restritas
[ ] protocol.registerSchemesAsPrivileged() usa permissões mínimas

── NAVEGAÇÃO ──
[ ] Evento 'will-navigate' do webContents interceptado — bloqueia URLs inesperadas
[ ] Evento 'new-window' do webContents interceptado — previne exploração de pop-ups
[ ] Nenhum shell.openExternal() com URLs não-sanitizadas

── EMPACOTAMENTO ──
[ ] ASAR archive habilitado (protege source de inspeção casual)
[ ] Nenhuma credencial sensível ou API keys bundled na app
[ ] Code signing configurado para Windows e macOS
[ ] Auto-update usa HTTPS e verifica assinaturas
```

**Prevenção de Navigation Hijacking:**
```typescript
// No processo main, após criar um BrowserWindow
win.webContents.on('will-navigate', (event, url) => {
  const parsedUrl = new URL(url);
  // Apenas permite navegação dentro da sua app
  if (parsedUrl.origin !== 'http://localhost:5173') { // dev server
    event.preventDefault();
    console.warn(`Blocked navigation to: ${url}`);
  }
});

// Previne que novas janelas sejam abertas
win.webContents.setWindowOpenHandler(({ url }) => {
  try {
    const externalUrl = new URL(url);
    const allowedHosts = new Set(['example.com', 'docs.example.com']);

    // Nunca encaminhe URLs controladas pelo renderer bruto ao SO.
    // Links não-validados podem habilitar phishing ou abuso de handlers de URL de plataforma.
    if (externalUrl.protocol === 'https:' && allowedHosts.has(externalUrl.hostname)) {
      require('electron').shell.openExternal(externalUrl.toString());
    } else {
      console.warn(`Blocked external URL: ${url}`);
    }
  } catch {
    console.warn(`Rejected invalid external URL: ${url}`);
  }

  return { action: 'deny' }; // Bloqueia todas as novas janelas Electron
});
```

**Registro de Protocolo Customizado (seguro):**
```typescript
import { protocol } from 'electron';
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { URL } from 'node:url';

// Registra um protocolo customizado para carregar assets locais com segurança
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } },
]);

app.whenReady().then(() => {
  protocol.handle('app', async (request) => {
    const url = new URL(request.url);
    const baseDir = path.resolve(__dirname, '../renderer');
    // Remove slash inicial para que path.resolve mantenha baseDir como root.
    const relativePath = path.normalize(decodeURIComponent(url.pathname).replace(/^[/\\]+/, ''));
    const filePath = path.resolve(baseDir, relativePath);

    if (!filePath.startsWith(baseDir)) {
      return new Response('Forbidden', { status: 403 });
    }

    const data = await readFile(filePath);
    return new Response(data);
  });
});
```

---

### 5. Gerenciamento de Estado Através de Processos

**Estratégia 1: Processo main como fonte única de verdade (recomendado para maioria das apps)**
```typescript
// src/main/store.ts
import { app } from 'electron';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

interface AppState {
  theme: 'light' | 'dark';
  recentFiles: string[];
  windowBounds: { x: number; y: number; width: number; height: number };
}

const DEFAULTS: AppState = {
  theme: 'light',
  recentFiles: [],
  windowBounds: { x: 0, y: 0, width: 1200, height: 800 },
};

class Store {
  private data: AppState;
  private filePath: string;

  constructor() {
    this.filePath = path.join(app.getPath('userData'), 'settings.json');
    this.data = this.load();
  }

  private load(): AppState {
    try {
      const raw = readFileSync(this.filePath, 'utf-8');
      return { ...DEFAULTS, ...JSON.parse(raw) };
    } catch {
      return { ...DEFAULTS };
    }
  }

  get<K extends keyof AppState>(key: K): AppState[K] {
    return this.data[key];
  }

  set<K extends keyof AppState>(key: K, value: AppState[K]): void {
    this.data[key] = value;
    writeFileSync(this.filePath, JSON.stringify(this.data, null, 2));
  }
}

export const store = new Store();
```

**Estratégia 2: electron-store (armazenamento persistente lightweight)**
```typescript
import Store from 'electron-store';

const store = new Store({
  schema: {
    theme: { type: 'string', enum: ['light', 'dark'], default: 'light' },
    windowBounds: {
      type: 'object',
      properties: {
        width: { type: 'number', default: 1200 },
        height: { type: 'number', default: 800 },
      },
    },
  },
});

// Uso
store.set('theme', 'dark');
console.log(store.get('theme')); // 'dark'
```

**Sincronização de estado multi-janela:**
```typescript
// Processo main: broadcast de mudanças de estado para todas as janelas
import { BrowserWindow } from 'electron';

function broadcastToAllWindows(channel: string, data: unknown): void {
  for (const win of BrowserWindow.getAllWindows()) {
    if (!win.isDestroyed()) {
      win.webContents.send(channel, data);
    }
  }
}

// Quando tema muda:
ipcMain.handle('settings:set-theme', (_event, theme: 'light' | 'dark') => {
  store.set('theme', theme);
  broadcastToAllWindows('settings:theme-changed', theme);
});
```

---

### 6. Build, Assinatura & Distribuição

#### Configuração electron-builder

```yaml
# electron-builder.yml
appId: com.mycompany.myapp
productName: My App
directories:
  output: dist
  buildResources: resources

files:
  - "out/**/*"       # main + preload compilados
  - "renderer/**/*"  # assets renderer built
  - "package.json"

asar: true
compression: maximum

# ── macOS ──
mac:
  category: public.app-category.developer-tools
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: resources/entitlements.mac.plist
  entitlementsInherit: resources/entitlements.mac.plist
  target:
    - target: dmg
      arch: [x64, arm64]
    - target: zip
      arch: [x64, arm64]

# ── Windows ──
win:
  target:
    - target: nsis
      arch: [x64, arm64]
  signingHashAlgorithms: [sha256]

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  perMachine: false

# ── Linux ──
linux:
  target:
    - target: AppImage
    - target: deb
  category: Development
  maintainer: your-email@example.com

# ── Auto Update ──
publish:
  provider: github
  owner: your-org
  repo: your-repo
```

#### Code Signing

```bash
# macOS: requer certificado Apple Developer
# Defina variáveis de ambiente antes de fazer build:
export CSC_LINK="path/to/Developer_ID_Application.p12"
export CSC_KEY_PASSWORD="your-password"

# Windows: requer certificado EV ou standard de code signing
# Defina variáveis de ambiente:
export WIN_CSC_LINK="path/to/code-signing.pfx"
export WIN_CSC_KEY_PASSWORD="your-password"

# Build app assinado
npx electron-builder --mac --win --publish never
```

#### Auto-Update com electron-updater

```typescript
// src/main/updater.ts
import { autoUpdater } from 'electron-updater';
import { BrowserWindow } from 'electron';
import log from 'electron-log';

export function setupAutoUpdater(mainWindow: BrowserWindow): void {
  autoUpdater.logger = log;
  autoUpdater.autoDownload = false; // Deixe usuário decidir
  autoUpdater.autoInstallOnAppQuit = true;

  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update:available', {
      version: info.version,
      releaseNotes: info.releaseNotes,
    });
  });

  autoUpdater.on('download-progress', (progress) => {
    mainWindow.webContents.send('update:progress', {
      percent: Math.round(progress.percent),
      bytesPerSecond: progress.bytesPerSecond,
    });
  });

  autoUpdater.on('update-downloaded', () => {
    mainWindow.webContents.send('update:downloaded');
  });

  autoUpdater.on('error', (err) => {
    log.error('Update error:', err);
    mainWindow.webContents.send('update:error', err.message);
  });

  // Verifica por atualizações a cada 4 horas
  setInterval(() => autoUpdater.checkForUpdates(), 4 * 60 * 60 * 1000);
  autoUpdater.checkForUpdates();
}

// Expose ao renderer via IPC
ipcMain.handle('update:download', () => autoUpdater.downloadUpdate());
ipcMain.handle('update:install', () => autoUpdater.quitAndInstall());
```

#### Bundle Size Optimization

- ✅ Use `asar: true` para empacotar sources num arquivo único
- ✅ Defina `compression: maximum` na configuração electron-builder
- ✅ Exclua devDependencies: padrão `"files"` deve incluir apenas output compilado
- ✅ Use um bundler (Vite, webpack, esbuild) para tree-shake o renderer
- ✅ Audit `node_modules` shipped com a app — use padrões `files` exclude do `electron-builder`
- ✅ Considere `@electron/rebuild` para módulos nativos em vez de shipped prebuilt para todas plataformas
- ❌ Não bundle o inteiro `node_modules` — apenas devDependencies de produção

---

### 7. Developer Experience & Debugging

#### Development Setup com Hot Reload

```json
// package.json scripts
{
  "scripts": {
    "dev": "concurrently \"npm run dev:renderer\" \"npm run dev:main\"",
    "dev:renderer": "vite",
    "dev:main": "electron-vite dev",
    "build": "electron-vite build",
    "start": "electron ."
  }
}
```

**Toolchain recomendada:**
- **electron-vite** ou **electron-forge com Vite plugin** — moderno, HMR rápido para renderer
- **tsx** ou **ts-node** — para rodar TypeScript no processo main durante development
- **concurrently** — rodar renderer dev server + Electron simultaneamente

#### Debugging do Processo Main

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Main Process",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "${workspaceFolder}/node_modules/.bin/electron",
      "args": [".", "--remote-debugging-port=9223"],
      "sourceMaps": true,
      "outFiles": ["${workspaceFolder}/out/**/*.js"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  ]
}
```

**Outras técnicas de debugging:**
```typescript
// Habilita DevTools apenas em development
if (process.env.NODE_ENV === 'development') {
  win.webContents.openDevTools({ mode: 'detach' });
}

// Inspeciona processos renderer específicos via linha de comando:
// electron . --inspect=5858 --remote-debugging-port=9223
```

#### Testing Strategy

**Unit testing (Vitest / Jest):**
```typescript
// tests/unit/store.test.ts
import { describe, it, expect, vi } from 'vitest';

// Mock módulos Electron para testes unitários
vi.mock('electron', () => ({
  app: { getPath: () => '/tmp/test' },
}));

describe('Store', () => {
  it('returns default values for missing keys', () => {
    // Test lógica store sem runtime Electron
  });
});
```

**E2E testing (Playwright + Electron):**
```typescript
// tests/e2e/app.spec.ts
import { test, expect, _electron as electron } from '@playwright/test';

test('app launches and shows main window', async () => {
  const app = await electron.launch({ args: ['.'] });
  const window = await app.firstWindow();

  // Aguarda app carregar completamente
  await window.waitForLoadState('domcontentloaded');

  const title = await window.title();
  expect(title).toBe('My App');

  // Tira screenshot para visual regression
  await window.screenshot({ path: 'tests/screenshots/main-window.png' });

  await app.close();
});

test('file open dialog works via IPC', async () => {
  const app = await electron.launch({ args: ['.'] });
  const window = await app.firstWindow();

  // Testa IPC avaliando no contexto renderer
  const version = await window.evaluate(async () => {
    return window.electronAPI.invoke('app:get-version');
  });

  expect(version).toBeTruthy();
  await app.close();
});
```

**Playwright config para Electron:**
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: 1,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

---

## Gerenciamento do Ciclo de Vida da Aplicação

```typescript
// src/main/main.ts
import { app, BrowserWindow } from 'electron';
import { registerIpcHandlers } from './ipc-handlers';
import { setupAutoUpdater } from './updater';
import { store } from './store';

let mainWindow: BrowserWindow | null = null;

app.whenReady().then(() => {
  registerIpcHandlers();
  mainWindow = createMainWindow();

  // Restaura window bounds
  const bounds = store.get('windowBounds');
  if (bounds) mainWindow.setBounds(bounds);

  // Salva window bounds ao fechar
  mainWindow.on('close', () => {
    if (mainWindow) store.set('windowBounds', mainWindow.getBounds());
  });

  // Auto-update (apenas em produção)
  if (app.isPackaged) {
    setupAutoUpdater(mainWindow);
  }

  // macOS: recria janela quando dock icon é clicado
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createMainWindow();
    }
  });
});

// Quit quando todas as janelas são fechadas (exceto no macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Segurança: previne que renderers adicionais sejam criados
app.on('web-contents-created', (_event, contents) => {
  contents.on('will-attach-webview', (event) => {
    event.preventDefault(); // Bloqueia tags <webview>
  });
});
```

---

## Diagnóstico de Problemas Comuns

### Tela Branca no Launch
**Sintomas**: App inicia mas renderer mostra página branca/vazia
**Causas raiz**: Caminho incorreto em `loadFile`/`loadURL`, output de build ausente, CSP bloqueando scripts
**Soluções**: Verifique que o caminho passado para `win.loadFile()` ou `win.loadURL()` existe relativo à app empacotada. Verifique console do DevTools para violações de CSP. Em development, assegure que o dev server Vite/webpack está rodando antes de Electron iniciar.

### Mensagens IPC Não Recebidas
**Sintomas**: `invoke()` hang ou `send()` sem efeito
**Causas raiz**: Nome de canal mismatch, preload não carregado, contextBridge não expose canal
**Soluções**: Verifique que nomes de canal match exatamente entre preload, main e