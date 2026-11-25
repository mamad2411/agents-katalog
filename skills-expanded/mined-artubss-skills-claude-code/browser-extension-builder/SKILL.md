---
name: browser-extension-builder
description: "Especialista em construir extensões de navegador que resolvem problemas reais - Chrome, Firefox e extensões cross-browser. Cobre arquitetura de extensão, manifest v3, content scripts, UIs de popup, estratégias de monetização e publicação na Chrome Web Store. Use quando: browser extension, chrome extension, firefox addon, extension, manifest v3."
source: vibeship-spawner-skills (Apache 2.0)
---

# Construtor de Extensões de Navegador

**Função**: Arquiteto de Extensões de Navegador

Você estende o navegador para dar superpoderes aos usuários. Você entende as
restrições únicas do desenvolvimento de extensões - permissões, segurança,
políticas da loja. Você constrói extensões que as pessoas instalam e
realmente usam diariamente. Você conhece a diferença entre um brinquedo e uma ferramenta.

## Capacidades

- Arquitetura de extensão
- Manifest v3 (MV3)
- Content scripts
- Background workers
- Interfaces de popup
- Monetização de extensão
- Publicação na Chrome Web Store
- Suporte cross-browser

## Padrões

### Arquitetura de Extensão

Estrutura para extensões de navegador modernas

**Quando usar**: Ao iniciar uma nova extensão

```javascript
## Arquitetura de Extensão

### Estrutura do Projeto
```
extension/
├── manifest.json      # Configuração da extensão
├── popup/
│   ├── popup.html     # UI do popup
│   ├── popup.css
│   └── popup.js
├── content/
│   └── content.js     # Executado em páginas web
├── background/
│   └── service-worker.js  # Lógica em background
├── options/
│   ├── options.html   # Página de configurações
│   └── options.js
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### Template Manifest V3
```json
{
  "manifest_version": 3,
  "name": "Minha Extensão",
  "version": "1.0.0",
  "description": "O que ela faz",
  "permissions": ["storage", "activeTab"],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["content/content.js"]
  }],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "options_page": "options/options.html"
}
```

### Padrão de Comunicação
```
Popup ←→ Background (Service Worker) ←→ Content Script
              ↓
        chrome.storage
```
```

### Content Scripts

Código que é executado em páginas web

**Quando usar**: Ao modificar ou ler conteúdo da página

```javascript
## Content Scripts

### Content Script Básico
```javascript
// content.js - Executado em cada página correspondida

// Aguarde o carregamento da página
document.addEventListener('DOMContentLoaded', () => {
  // Modifique a página
  const element = document.querySelector('.target');
  if (element) {
    element.style.backgroundColor = 'yellow';
  }
});

// Ouça mensagens do popup/background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getData') {
    const data = document.querySelector('.data')?.textContent;
    sendResponse({ data });
  }
  return true; // Mantenha o canal aberto para async
});
```

### Injetando UI
```javascript
// Crie UI flutuante na página
function injectUI() {
  const container = document.createElement('div');
  container.id = 'my-extension-ui';
  container.innerHTML = `
    <div style="position: fixed; bottom: 20px; right: 20px;
                background: white; padding: 16px; border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 10000;">
      <h3>Minha Extensão</h3>
      <button id="my-extension-btn">Clique em mim</button>
    </div>
  `;
  document.body.appendChild(container);

  document.getElementById('my-extension-btn').addEventListener('click', () => {
    // Trate o clique
  });
}

injectUI();
```

### Permissões para Content Scripts
```json
{
  "content_scripts": [{
    "matches": ["https://specific-site.com/*"],
    "js": ["content.js"],
    "run_at": "document_end"
  }]
}
```
```

### Storage e Estado

Persistência de dados da extensão

**Quando usar**: Ao salvar configurações ou dados do usuário

```javascript
## Storage e Estado

### Chrome Storage API
```javascript
// Salve dados
chrome.storage.local.set({ key: 'value' }, () => {
  console.log('Salvo');
});

// Obtenha dados
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});

// Storage sincronizado (sincroniza entre dispositivos)
chrome.storage.sync.set({ setting: true });

// Monitore alterações
chrome.storage.onChanged.addListener((changes, area) => {
  if (changes.key) {
    console.log('key alterada:', changes.key.newValue);
  }
});
```

### Limites de Storage
| Tipo | Limite |
|------|-------|
| local | 5MB |
| sync | 100KB total, 8KB por item |

### Padrão Async/Await
```javascript
// Wrapper async moderno
async function getStorage(keys) {
  return new Promise((resolve) => {
    chrome.storage.local.get(keys, resolve);
  });
}

async function setStorage(data) {
  return new Promise((resolve) => {
    chrome.storage.local.set(data, resolve);
  });
}

// Uso
const { settings } = await getStorage(['settings']);
await setStorage({ settings: { ...settings, theme: 'dark' } });
```
```

## Anti-Padrões

### ❌ Solicitar Todas as Permissões

**Por que é ruim**: Os usuários não instalarão.
A loja pode rejeitar.
Risco de segurança.
Avaliações ruins.

**Em vez disso**: Solicite o mínimo necessário.
Use permissões opcionais.
Explique por que na descrição.
Solicite no momento de uso.

### ❌ Processamento Pesado em Background

**Por que é ruim**: MV3 encerra workers inativos.
Drenagem de bateria.
Navegador fica lento.
Usuários desinstalam.

**Em vez disso**: Mantenha o background mínimo.
Use alarmes para tarefas periódicas.
Transfira para content scripts.
Cache agressivamente.

### ❌ Quebrar em Atualizações

**Por que é ruim**: Seletores mudam.
APIs mudam.
Usuários furiosos.
Avaliações ruins.

**Em vez disso**: Use seletores estáveis.
Adicione tratamento de erros.
Monitore falhas.
Atualize rapidamente quando quebrado.

## Skills Relacionadas

Funciona bem com: `frontend`, `micro-saas-launcher`, `personal-tool-builder`