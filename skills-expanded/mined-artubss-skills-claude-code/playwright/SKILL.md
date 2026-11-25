---
name: playwright-skill
description: Automação completa de navegador com Playwright. Detecta automaticamente servidores de desenvolvimento, escreve scripts de teste limpos em /tmp. Testa páginas, preenche formulários, captura telas, verifica design responsivo, valida UX, testa fluxos de login, verifica links, automatiza qualquer tarefa de navegador. Use quando você quiser testar sites, automatizar interações de navegador, validar funcionalidade web ou realizar qualquer teste baseado em navegador.
---

**IMPORTANTE - Resolução de Caminho:**
Esta skill pode ser instalada em diferentes locais (sistema de plugins, instalação manual, global ou específica do projeto). Antes de executar qualquer comando, determine o diretório da skill com base em onde você carregou este arquivo SKILL.md e use esse caminho em todos os comandos abaixo. Substitua `$SKILL_DIR` pelo caminho real descoberto.

Caminhos de instalação comuns:

- Sistema de plugins: `~/.claude/plugins/marketplaces/playwright-skill/skills/playwright-skill`
- Global manual: `~/.claude/skills/playwright-skill`
- Específico do projeto: `<projeto>/.claude/skills/playwright-skill`

# Automação de Navegador Playwright

Skill de automação de navegador para fins gerais. Vou escrever código Playwright personalizado para qualquer tarefa de automação que você solicitar e executá-lo via executor universal.

**FLUXO DE TRABALHO CRÍTICO - Siga estas etapas em ordem:**

1. **Auto-detectar servidores de desenvolvimento** - Para testes em localhost, SEMPRE execute a detecção de servidor PRIMEIRO:

   ```bash
   cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(servers => console.log(JSON.stringify(servers)))"
   ```

   - Se **1 servidor encontrado**: Use-o automaticamente, informe o usuário
   - Se **múltiplos servidores encontrados**: Pergunte ao usuário qual testar
   - Se **nenhum servidor encontrado**: Peça uma URL ou ofereça ajuda para iniciar servidor de desenvolvimento

2. **Escrever scripts em /tmp** - NUNCA escreva arquivos de teste no diretório da skill; sempre use `/tmp/playwright-test-*.js`

3. **Usar navegador visível por padrão** - Sempre use `headless: false` a menos que o usuário solicite especificamente modo headless

4. **Parameterizar URLs** - Sempre torne URLs configuráveis via variável de ambiente ou constante no topo do script

## Como Funciona

1. Você descreve o que quer testar/automatizar
2. Detecto automaticamente servidores em execução (ou peço uma URL se testando site externo)
3. Escrevo código Playwright personalizado em `/tmp/playwright-test-*.js` (não bagunça seu projeto)
4. Executo via: `cd $SKILL_DIR && node run.js /tmp/playwright-test-*.js`
5. Resultados exibidos em tempo real, janela do navegador visível para debug
6. Arquivos de teste auto-limpos de /tmp pelo seu SO

## Configuração (Primeira Vez)

```bash
cd $SKILL_DIR
npm run setup
```

Isto instala Playwright e navegador Chromium. Necessário apenas uma vez.

## Padrão de Execução

**Etapa 1: Detectar servidores de desenvolvimento (para testes em localhost)**

```bash
cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```

**Etapa 2: Escrever script de teste em /tmp com parâmetro de URL**

```javascript
// /tmp/playwright-test-page.js
const { chromium } = require('playwright');

// URL parametrizada (detectada ou fornecida pelo usuário)
const TARGET_URL = 'http://localhost:3001'; // <-- Auto-detectada ou do usuário

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(TARGET_URL);
  console.log('Página carregada:', await page.title());

  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  console.log('📸 Captura de tela salva em /tmp/screenshot.png');

  await browser.close();
})();
```

**Etapa 3: Executar a partir do diretório da skill**

```bash
cd $SKILL_DIR && node run.js /tmp/playwright-test-page.js
```

## Padrões Comuns

### Testar uma Página (Múltiplos Viewports)

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detectada

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();

  // Teste desktop
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(TARGET_URL);
  console.log('Desktop - Título:', await page.title());
  await page.screenshot({ path: '/tmp/desktop.png', fullPage: true });

  // Teste mobile
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({ path: '/tmp/mobile.png', fullPage: true });

  await browser.close();
})();
```

### Testar Fluxo de Login

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detectada

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/login`);

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Aguardar redirecionamento
  await page.waitForURL('**/dashboard');
  console.log('✅ Login bem-sucedido, redirecionado para dashboard');

  await browser.close();
})();
```

### Preencher e Enviar Formulário

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detectada

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/contact`);

  await page.fill('input[name="name"]', 'João Silva');
  await page.fill('input[name="email"]', 'joao@example.com');
  await page.fill('textarea[name="message"]', 'Mensagem de teste');
  await page.click('button[type="submit"]');

  // Verificar envio
  await page.waitForSelector('.success-message');
  console.log('✅ Formulário enviado com sucesso');

  await browser.close();
})();
```

### Verificar Links Quebrados

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000');

  const links = await page.locator('a[href^="http"]').all();
  const results = { working: 0, broken: [] };

  for (const link of links) {
    const href = await link.getAttribute('href');
    try {
      const response = await page.request.head(href);
      if (response.ok()) {
        results.working++;
      } else {
        results.broken.push({ url: href, status: response.status() });
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message });
    }
  }

  console.log(`✅ Links funcionando: ${results.working}`);
  console.log(`❌ Links quebrados:`, results.broken);

  await browser.close();
})();
```

### Capturar Tela com Tratamento de Erro

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle',
      timeout: 10000,
    });

    await page.screenshot({
      path: '/tmp/screenshot.png',
      fullPage: true,
    });

    console.log('📸 Captura de tela salva em /tmp/screenshot.png');
  } catch (error) {
    console.error('❌ Erro:', error.message);
  } finally {
    await browser.close();
  }
})();
```

### Testar Design Responsivo

```javascript
// /tmp/playwright-test-responsive-full.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detectada

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ];

  for (const viewport of viewports) {
    console.log(
      `Testando ${viewport.name} (${viewport.width}x${viewport.height})`,
    );

    await page.setViewportSize({
      width: viewport.width,
      height: viewport.height,
    });

    await page.goto(TARGET_URL);
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    });
  }

  console.log('✅ Todos os viewports testados');
  await browser.close();
})();
```

## Execução Inline (Tarefas Simples)

Para tarefas rápidas e únicas, você pode executar código inline sem criar arquivos:

```bash
# Capturar uma tela rápida
cd $SKILL_DIR && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3001');
await page.screenshot({ path: '/tmp/quick-screenshot.png', fullPage: true });
console.log('Captura de tela salva');
await browser.close();
"
```

**Quando usar inline vs arquivos:**

- **Inline**: Tarefas rápidas e únicas (captura de tela, verificar se elemento existe, obter título da página)
- **Arquivos**: Testes complexos, verificações de design responsivo, qualquer coisa que o usuário possa querer re-executar

## Helpers Disponíveis

Funções utilitárias opcionais em `lib/helpers.js`:

```javascript
const helpers = require('./lib/helpers');

// Detectar servidores de desenvolvimento em execução (CRÍTICO - use isto primeiro!)
const servers = await helpers.detectDevServers();
console.log('Servidores encontrados:', servers);

// Clique seguro com retry
await helpers.safeClick(page, 'button.submit', { retries: 3 });

// Digite com segurança e limpeza
await helpers.safeType(page, '#username', 'testuser');

// Capturar tela com timestamp
await helpers.takeScreenshot(page, 'test-result');

// Lidar com banners de cookie
await helpers.handleCookieBanner(page);

// Extrair dados de tabela
const data = await helpers.extractTableData(page, 'table.results');
```

Veja `lib/helpers.js` para lista completa.

## Headers HTTP Personalizados

Configure headers HTTP personalizados para todas as requisições via variáveis de ambiente. Útil para:

- Identificar tráfego automatizado para seu backend
- Obter respostas otimizadas para LLM (ex: erros em texto simples em vez de HTML estilizado)
- Adicionar tokens de autenticação globalmente

### Configuração

**Header único (caso comum):**

```bash
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

**Múltiplos headers (formato JSON):**

```bash
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

### Como Funciona

Headers são aplicados automaticamente ao usar `helpers.createContext()`:

```javascript
const context = await helpers.createContext(browser);
const page = await context.newPage();
// Todas as requisições desta página incluem seus headers personalizados
```

Para scripts usando API raw do Playwright, use o `getContextOptionsWithHeaders()` injetado:

```javascript
const context = await browser.newContext(
  getContextOptionsWithHeaders({ viewport: { width: 1920, height: 1080 } }),
);
```

## Uso Avançado

Para documentação abrangente da API do Playwright, veja [API_REFERENCE.md](API_REFERENCE.md):

- Seletores & Locators melhores práticas
- Network interception & API mocking
- Autenticação & gerenciamento de sessão
- Teste de regressão visual
- Emulação de dispositivo mobile
- Teste de performance
- Técnicas de debug
- Integração CI/CD

## Dicas

- **CRÍTICO: Detectar servidores PRIMEIRO** - Sempre execute `detectDevServers()` antes de escrever código de teste para testes em localhost
- **Headers personalizados** - Use variáveis de ambiente `PW_HEADER_NAME`/`PW_HEADER_VALUE` para identificar tráfego automatizado para seu backend
- **Use /tmp para arquivos de teste** - Escreva em `/tmp/playwright-test-*.js`, nunca no diretório da skill ou projeto do usuário
- **Parameterize URLs** - Coloque URL detectada/fornecida em uma constante `TARGET_URL` no topo de cada script
- **PADRÃO: Navegador visível** - Sempre use `headless: false` a menos que o usuário peça explicitamente modo "headless" ou "background"
- **Modo headless** - Use `headless: true` apenas quando o usuário especificamente solicitar execução "headless" ou "background"
- **Desacelerar:** Use `slowMo: 100` para tornar ações visíveis e mais fáceis de acompanhar
- **Estratégias de espera:** Use `waitForURL`, `waitForSelector`, `waitForLoadState` em vez de timeouts fixos
- **Tratamento de erro:** Sempre use try-catch para automação robusta
- **Saída de console:** Use `console.log()` para rastrear progresso e mostrar o que está acontecendo

## Resolução de Problemas

**Playwright não instalado:**

```bash
cd $SKILL_DIR && npm run setup
```

**Módulo não encontrado:**
Garanta execução a partir do diretório da skill via wrapper `run.js`

**Navegador não abre:**
Verifique `headless: false` e garanta que display está disponível

**Elemento não encontrado:**
Adicione espera: `await page.waitForSelector('.element', { timeout: 10000 })`

## Exemplo de Uso

```
Usuário: "Teste se a página de marketing se parece bem"

Claude: Vou testar a página de marketing em múltiplos viewports. Deixe-me detectar primeiro servidores em execução...
[Executa: detectDevServers()]
[Saída: Servidor encontrado na porta 3001]
Encontrei seu servidor de desenvolvimento rodando em http://localhost:3001

[Escreve script de automação personalizado em /tmp/playwright-test-marketing.js com URL parametrizada]
[Executa: cd $SKILL_DIR && node run.js /tmp/playwright-test-marketing.js]
[Mostra resultados com capturas de tela de /tmp/]
```

```
Usuário: "Verifique se o login redireciona corretamente"

Claude: Vou testar o fluxo de login. Primeiro, deixe-me verificar servidores em execução...
[Executa: detectDevServers()]
[Saída: Servidores encontrados nas portas 3000 e 3001]
Encontrei 2 servidores de desenvolvimento. Qual eu deveria testar?
- http://localhost:3000
- http://localhost:3001

Usuário: "Use 3001"

[Escreve automação de login em /tmp/playwright-test-login.js]
[Executa: cd $SKILL_DIR && node run.js /tmp/playwright-test-login.js]
[Reporta: ✅ Login bem-sucedido, redirecionado para /dashboard]
```

## Notas

- Cada automação é escrita sob medida para sua solicitação específica
- Não limitado a scripts pré-construídos - qualquer tarefa de navegador é possível
- Auto-detecta servidores de desenvolvimento em execução para eliminar URLs hardcoded
- Scripts de teste escritos em `/tmp` para limpeza automática (sem bagunça)
- Código executa de forma confiável com resolução adequada de módulos via `run.js`
- Divulgação progressiva - API_REFERENCE.md carregado apenas quando recursos avançados são necessários