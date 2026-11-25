---
name: playwright-e2e-builder
description: Planeje e construa suítes de testes E2E abrangentes com Playwright usando Page Object Model, persistência de estado de autenticação, fixtures customizados, regressão visual e integração com CI. Usa planejamento orientado por entrevista para esclarecer fluxos críticos de usuário, estratégia de auth, abordagem de dados de teste e paralelização antes de escrever testes.
tags: [playwright, e2e, testing, automation, typescript, ci, visual-regression]
---

# Gerador de Suíte de Testes E2E com Playwright

## Quando usar

Use esta skill quando você precisar:

- Configurar Playwright do zero em um projeto existente
- Construir testes E2E para fluxos críticos de usuário (signup, checkout, dashboards)
- Implementar Page Object Model para arquitetura de testes mantível
- Configurar persistência de estado de autenticação entre testes
- Configurar testes de regressão visual com screenshots
- Integrar Playwright em CI/CD com sharding e retries

## Fase 1: Exploração (Modo Plano)

Entre no modo de plano. Antes de escrever qualquer teste, explore o projeto existente:

### Estrutura do projeto
- Encontre o tech stack: é React, Next.js, Vue, SvelteKit ou outro framework?
- Verifique se Playwright já está instalado (`playwright.config.ts`, `@playwright/test` em package.json)
- Procure por diretórios de testes existentes (`e2e/`, `tests/`, `__tests__/`)
- Verifique se há testes E2E existentes em Cypress, Selenium ou outros frameworks (contexto de migração)
- Encontre o comando do dev server e porta (`npm run dev`, `next dev`, etc.)

### Estrutura da aplicação
- Identifique as principais rotas/páginas (procure na config do router, diretório pages ou arquivos de rotas)
- Encontre fluxo de autenticação (URL da página de login, endpoints de API de auth, armazenamento de token)
- Procure por test IDs em componentes (atributos `data-testid`, `data-test`, `data-cy`)
- Procure por rotas de API que os testes possam usar para semear dados
- Verifique arquivos `.env` para variáveis de ambiente específicas de teste

### CI/CD
- Verifique a config de CI existente (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
- Procure por setup Docker ou docker-compose (útil para ambientes de teste consistentes)
- Verifique se existe padrão de URL de ambiente staging/preview

## Fase 2: Entrevista (AskUserQuestion)

Use AskUserQuestion para esclarecer requisitos. Pergunte em rodadas.

### Rodada 1: Escopo e fluxos críticos

```
Pergunta: "Quais são os fluxos de usuário críticos para testar?"
Cabeçalho: "Fluxos"
multiSelect: true
Opções:
  - "Autenticação (signup, login, logout, reset de senha)" — Fluxos de auth principais
  - "CRUD principal (criar, ler, atualizar, deletar recursos principais)" — Operações de dados primários
  - "Checkout/pagamentos (carrinho, cobrança, confirmação)" — Fluxos de e-commerce ou pagamento
  - "Dashboard/admin (visualizações de dados, filtros, exports)" — Interações do painel administrativo
```

```
Pergunta: "Quantas páginas/rotas a aplicação tem aproximadamente?"
Cabeçalho: "Tamanho da app"
Opções:
  - "Pequena (< 10 rotas)" — Landing page, auth, algumas páginas de feature
  - "Média (10-30 rotas)" — Múltiplas áreas de feature, settings, profiles
  - "Grande (30+ rotas)" — App complexa com muitas seções e papéis de usuário
```

### Rodada 2: Estratégia de autenticação para testes

```
Pergunta: "Como sua app lida com autenticação?"
Cabeçalho: "Tipo de auth"
Opções:
  - "Cookie/session (Recomendado)" — Server configura httpOnly cookies após login
  - "JWT em localStorage" — Token armazenado em localStorage do navegador
  - "OAuth/SSO (Google, GitHub, etc.)" — Fluxo de redirecionamento de provedor de auth terceirizado
  - "Sem auth (app pública)" — Sem login necessário

Pergunta: "Como os testes devem autenticar?"
Cabeçalho: "Auth de teste"
Opções:
  - "Login via UI uma vez, reutilizar estado (Recomendado)" — Padrão storageState: login em setup, compartilhar cookies entre testes
  - "API login em beforeEach" — Chamar API de auth diretamente antes de cada teste, pular UI login
  - "Semear auth token em fixtures" — Injetar tokens pré-gerados, sem necessidade de fluxo de login
  - "Testar UI de login sempre" — Testar o formulário de login em cada suíte de testes
```

### Rodada 3: Dados de teste e ambiente

```
Pergunta: "Como os dados de teste devem ser gerenciados?"
Cabeçalho: "Dados de teste"
Opções:
  - "Seeding via API em fixtures (Recomendado)" — Chamar endpoints de API para criar/limpar dados de teste antes de cada teste
  - "Seeding de banco de dados (SQL direto)" — Executar scripts SQL ou comandos ORM para popular banco de dados de teste
  - "Ambiente de teste compartilhado (pré-populado)" — Testes rodam contra um ambiente staging persistente com dados existentes
  - "Mock de respostas de API" — Interceptar requisições de rede e retornar dados mockados

Pergunta: "Em qual ambiente os testes E2E rodam?"
Cabeçalho: "Ambiente"
Opções:
  - "Dev server local (Recomendado)" — Iniciar dev server antes dos testes, rodar contra localhost
  - "URL de preview/staging" — Rodar contra um ambiente de preview ou staging deployado
  - "Stack Docker Compose" — Stack completo em containers, testes rodam fora ou dentro
```

### Rodada 4: CI e paralelização

```
Pergunta: "Como os testes devem rodar em CI?"
Cabeçalho: "CI"
Opções:
  - "GitHub Actions (Recomendado)" — Suporte nativo ao Playwright com sharding
  - "GitLab CI" — Runners baseados em Docker com imagem Playwright
  - "Apenas local (sem CI ainda)" — Apenas execuções de teste locais por enquanto
  - "Outro CI (Jenkins, CircleCI)" — Configuração customizada de CI

Pergunta: "Você precisa de testes de regressão visual?"
Cabeçalho: "Visual"
Opções:
  - "Não — apenas testes funcionais (Recomendado)" — Assert comportamento, não pixels
  - "Sim — comparações de screenshot" — Capturar e comparar screenshots de página
  - "Sim — screenshots de componentes" — Capturar componentes específicos, não páginas inteiras
```

## Fase 3: Plano (ExitPlanMode)

Escreva um plano de implementação concreto cobrindo:

1. **Estrutura de diretórios** — arquivos de teste, page objects, fixtures, config
2. **Config do Playwright** — projects (navegadores), base URL, retries, workers
3. **Setup de auth** — global setup para storageState ou auth baseada em API
4. **Page objects** — classes para cada página com locators e actions
5. **Test fixtures** — fixtures customizados para seeding de dados, auth, API client
6. **Suítes de testes** — arquivos de teste para cada fluxo crítico da entrevista
7. **Config de CI** — arquivo de workflow com sharding, upload de artefatos, reporting

Apresente via ExitPlanMode para aprovação do usuário.

## Fase 4: Executar

Após aprovação, implemente seguindo esta ordem:

### Passo 1: Config do Playwright

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI
    ? [['html', { open: 'never' }], ['github']]
    : [['html', { open: 'on-failure' }]],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  projects: [
    // Auth setup — runs before all tests
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'e2e/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'e2e/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'mobile',
      use: {
        ...devices['iPhone 14'],
        storageState: 'e2e/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

### Passo 2: Setup de auth (global)

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'e2e/.auth/user.json';

setup('authenticate', async ({ page }) => {
  // Navigate to login page
  await page.goto('/login');

  // Fill login form
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL || 'test@example.com');
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD || 'testpassword');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for auth to complete — adjust selector to your app
  await page.waitForURL('/dashboard');
  await expect(page.getByRole('navigation')).toBeVisible();

  // Save signed-in state
  await page.context().storageState({ path: authFile });
});
```

### Passo 3: Fixtures customizados

```typescript
// e2e/fixtures.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from './pages/login-page';
import { DashboardPage } from './pages/dashboard-page';

// API client for test data seeding
class ApiClient {
  constructor(private baseURL: string, private token?: string) {}

  async createResource(data: Record<string, unknown>) {
    const response = await fetch(`${this.baseURL}/api/resources`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`Seed failed: ${response.status}`);
    return response.json();
  }

  async deleteResource(id: string) {
    await fetch(`${this.baseURL}/api/resources/${id}`, {
      method: 'DELETE',
      headers: this.token ? { Authorization: `Bearer ${this.token}` } : {},
    });
  }
}

type Fixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  api: ApiClient;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  api: async ({ baseURL }, use) => {
    const client = new ApiClient(baseURL!);
    await use(client);
  },
});

export { expect };
```

### Passo 4: Page Object Model

```typescript
// e2e/pages/login-page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private page: Page) {
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// e2e/pages/dashboard-page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class DashboardPage {
  readonly heading: Locator;
  readonly createButton: Locator;
  readonly searchInput: Locator;
  readonly resourceList: Locator;

  constructor(private page: Page) {
    this.heading = page.getByRole('heading', { level: 1 });
    this.createButton = page.getByRole('button', { name: 'Create' });
    this.searchInput = page.getByPlaceholder('Search');
    this.resourceList = page.getByTestId('resource-list');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async createResource(name: string) {
    await this.createButton.click();
    await this.page.getByLabel('Name').fill(name);
    await this.page.getByRole('button', { name: 'Save' }).click();
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    // Wait for debounced search to trigger
    await this.page.waitForResponse(resp =>
      resp.url().includes('/api/resources') && resp.status() === 200
    );
  }

  async expectResourceVisible(name: string) {
    await expect(this.resourceList.getByText(name)).toBeVisible();
  }

  async expectResourceCount(count: number) {
    await expect(this.resourceList.getByRole('listitem')).toHaveCount(count);
  }
}
```

### Passo 5: Suítes de testes

```typescript
// e2e/auth.spec.ts
import { test, expect } from './fixtures';

test.describe('Authentication', () => {
  // These tests run WITHOUT storageState (unauthenticated)
  test.use({ storageState: { cookies: [], origins: [] } });

  test('successful login redirects to dashboard', async ({ loginPage, page }) => {
    await loginPage.goto();
    await loginPage.login('test@example.com', 'testpassword');
    await expect(page).toHaveURL('/dashboard');
  });

  test('invalid credentials shows error', async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login('test@example.com', 'wrongpassword');
    await loginPage.expectError('Invalid credentials');
  });

  test('logout clears session', async ({ page }) => {
    // Login first
    await page.goto('/login');
    // ... login steps ...

    // Logout
    await page.getByRole('button', { name: 'Logout' }).click();
    await expect(page).toHaveURL('/login');

    // Verify can't access protected route
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});

// e2e/dashboard.spec.ts
import { test, expect } from './fixtures';

test.describe('Dashboard', () => {
  test('displays resource list', async ({ dashboardPage }) => {
    await dashboardPage.goto();
    await expect(dashboardPage.heading).toHaveText('Dashboard');
    await expect(dashboardPage.resourceList).toBeVisible();
  });

  test('create new resource', async ({ dashboardPage, page }) => {
    await dashboardPage.goto();
    await dashboardPage.createResource('New E2E Resource');

    // Verify resource appears in list
    await dashboardPage.expectResourceVisible('New E2E Resource');
  });

  test('search filters results', async ({ dashboardPage, api }) => {
    // Seed test data via API
    await api.createResource({ name: 'Alpha Item' });
    await api.createResource({ name: 'Beta Item' });

    await dashboardPage.goto();
    await dashboardPage.search('Alpha');
    await dashboardPage.expectResourceVisible('Alpha Item');
  });

  test('empty state shown when no resources', async ({ dashboardPage, page }) => {
    await dashboardPage.goto();
    await dashboardPage.search('nonexistent-query-xyz');
    await expect(page.getByText('No results found')).toBeVisible();
  });
});

// e2e/crud.spec.ts
import { test, expect } from './fixtures';

test.describe('Resource CRUD', () => {
  let resourceId: string;

  test.beforeEach(async ({ api }) => {
    // Seed a resource for tests that need one
    const resource = await api.createResource({ name: 'Test Resource' });
    resourceId = resource.id;
  });

  test.afterEach(async ({ api }) => {
    // Clean up seeded data
    if (resourceId) {
      await api.deleteResource(resourceId).catch(() => {});
    }
  });

  test('edit resource name', async ({ page }) => {
    await page.goto(`/resources/${resourceId}`);
    await page.getByRole('button', { name: 'Edit' }).click();
    await page.getByLabel('Name').clear();
    await page.getByLabel('Name').fill('Updated Resource');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByRole('heading')).toHaveText('Updated Resource');
  });

  test('delete resource with confirmation', async ({ page }) => {
    await page.goto(`/resources/${resourceId}`);
    await page.getByRole('button', { name: 'Delete' }).click();

    // Confirm deletion dialog
    await expect(page.getByRole('dialog')).toBeVisible();
    await page.getByRole('button', { name: 'Confirm' }).click();

    // Should redirect to list
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### Passo 6: Regressão visual (se selecionado)

```typescript
// e2e/visual.spec.ts
import { test, expect } from './fixtures';

test.describe('Visual regression', () => {
  test('dashboard matches snapshot', async ({ dashboardPage, page }) => {
    await dashboardPage.goto();
    // Wait for dynamic content to stabilize
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('dashboard.png', {
      maxDiffPixelRatio: 0.01,
    });
  });

  test('login page matches snapshot', async ({ loginPage, page }) => {
    test.use({ storageState: { cookies: [], origins: [] } });
    await loginPage.goto();
    await expect(page).toHaveScreenshot('login.png', {
      maxDiffPixelRatio: 0.01,
    });
  });

  // Component-level screenshots
  test('navigation component matches snapshot', async ({ page }) => {
    await page.goto('/dashboard');
    const nav = page.getByRole('navigation');
    await expect(nav).toHaveScreenshot('navigation.png');
  });
});
```

### Passo 7: GitHub Actions CI

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npx playwright test --shard=${{ matrix.shard }}
        env:
          BASE_URL: http://localhost:3000
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}

      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report-${{ strategy.job-index }}
          path: playwright-report/
          retention-days: 14

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: test-results-${{ strategy.job-index }}
          path: test-results/
          retention-days: 7
```

## Referência de estrutura de diretórios

```
e2e/
├── .auth/
│   └── user.json            # Saved auth state (gitignored)
├── fixtures.ts              # Custom test fixtures and API client
├── pages/
│   ├── login-page.ts        # Login page object
│   ├── dashboard-page.ts    # Dashboard page object
│   └── resource-page.ts     # Resource detail page object
├── auth.setup.ts            # Global auth setup (runs once)
├── auth.spec.ts             # Authentication tests
├── dashboard.spec.ts        # Dashboard tests
├── crud.spec.ts             # CRUD operation tests
└── visual.spec.ts           # Visual regression tests (optional)
playwright.config.ts         # Playwright configuration
```

## Melhores práticas

### Use locators baseados em role primeiro
Prefira `getByRole()`, `getByLabel()`, `getByText()` em vez de seletores CSS ou test IDs. Esses locators refletem como usuários interagem com a página e detectam problemas de acessibilidade:

```typescript
// Preferido — acessível e resiliente
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByLabel('Email').fill('user@test.com');

// Fallback — quando baseado em role não funciona
await page.getByTestId('custom-widget').click();

// Evite — frágil, quebra em refatorações
await page.locator('.btn-primary').click();
await page.locator('#email-input').fill('user@test.com');
```

### Aguarde por rede, não por timers
Nunca use `page.waitForTimeout()`. Aguarde por condições específicas:

```typescript
// Wait for API response
await page.waitForResponse(resp => resp.url().includes('/api/data'));

// Wait for element state
await expect(page.getByText('Saved')).toBeVisible();

// Wait for navigation
await expect(page).toHaveURL('/dashboard');

// Wait for loading to finish
await expect(page.getByTestId('spinner')).toBeHidden();
```

### Isole dados de teste
Cada teste deve criar seus próprios dados e limpar depois:

```typescript
test('edit resource', async ({ api, page }) => {
  // Arrange — seed via API
  const resource = await api.createResource({ name: 'Test' });

  // Act
  await page.goto(`/resources/${resource.id}`);
  // ... test logic ...

  // Cleanup (also runs on failure via afterEach)
});
```

### Marque testes para execuções seletivas

```typescript
test('checkout flow @slow @checkout', async ({ page }) => {
  // Long test tagged for selective execution
});

// Run only: npx playwright test --grep @checkout
// Skip slow: npx playwright test --grep-invert @slow
```

### Adições a .gitignore

```
# Playwright
e2e/.auth/
test-results/
playwright-report/
blob-report/
```

## Checklist antes de finalizar

- [ ] `playwright.config.ts` tem webServer configurado para iniciar o dev server
- [ ] Auth setup salva storageState e todos os test projects dependem dele
- [ ] Page objects usam locators baseados em role (`getByRole`, `getByLabel`, `getByText`)
- [ ] Sem chamadas `waitForTimeout()` — apenas aguardar por elementos, URLs ou respostas
- [ ] Testes criam e limpam seus próprios dados (sem estado mutável compartilhado)
- [ ] Config de CI tem sharding para execução paralela
- [ ] Trace, screenshot e vídeo são capturados em falhas para debug
- [ ] Diretório `.auth/` está em `.gitignore`
- [ ] `npx playwright test` passa localmente antes de fazer push