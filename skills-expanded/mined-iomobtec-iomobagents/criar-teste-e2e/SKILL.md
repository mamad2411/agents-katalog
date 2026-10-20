---
name: criar-teste-e2e
description: "Escreve testes end-to-end com Playwright para fluxos completos do usuário. Use quando o dev-qa vai automatizar um fluxo de ponta a ponta."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-teste-e2e

Escreve **testes de ponta a ponta (E2E)** que validam fluxos completos de usuário percorrendo frontend, BFF e serviços backend. Usa Playwright como ferramenta principal: navega na UI real, interage como usuário e verifica resultados visíveis.

**Agente:** dev-qa  
**Guardrails aplicáveis:** `00-core.md`, `testes.md`, `seguranca.md`, `processo.md`  
**Referências rápidas:** `References/testing-patterns.md`

---

## Quando usar

- Para validar o caminho feliz (happy path) de um fluxo de negócio de ponta a ponta
- Quando uma história de usuário tem critérios de aceite que abrangem múltiplas telas ou serviços
- Para cobrir regressão em fluxos críticos após mudança de comportamento
- Nunca como substituto de testes unitários e de integração — E2E complementa, não substitui

---

## Princípio fundamental

**E2E testa fluxo de usuário — não implementação.** O teste interage com a UI da mesma forma que o usuário: clica, digita, navega e verifica o que está visível. Nunca acessa banco de dados diretamente nem chama APIs internas para verificar resultado.

---

## Processo de execução

### Passo 1 — Configurar Playwright

```bash
npm init playwright@latest
# ou adicionar ao projeto existente:
npm install --save-dev @playwright/test
npx playwright install chromium
```

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['list']],
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### Passo 2 — Estrutura de arquivos

```
e2e/
├── fixtures/
│   └── auth.fixture.ts      # login reutilizável entre testes
├── pages/
│   ├── login.page.ts        # Page Object: seletores + ações da tela de login
│   └── checkout.page.ts
├── flows/
│   ├── checkout.spec.ts     # Teste do fluxo de checkout
│   └── user-registration.spec.ts
└── support/
    └── test-data.ts         # Dados sintéticos de teste — sem CPF/email real
```

### Passo 3 — Implementar Page Object

Encapsula seletores e ações de uma tela — impede que mudança de seletor quebre múltiplos testes:

```typescript
// e2e/pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private readonly page: Page) {
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Senha');
    this.submitButton = page.getByRole('button', { name: /entrar/i });
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
}
```

### Passo 4 — Escrever o teste de fluxo

```typescript
// e2e/flows/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { CheckoutPage } from '../pages/checkout.page';
import { TEST_USER } from '../support/test-data';

test.describe('Checkout flow', () => {
  test.beforeEach(async ({ page }) => {
    // Autenticar antes de cada teste — não reutilizar sessão entre testes
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(TEST_USER.email, TEST_USER.password);
    await expect(page).toHaveURL('/home');
  });

  test('should complete purchase when payment is approved', async ({ page }) => {
    const checkout = new CheckoutPage(page);

    await checkout.goto();
    await checkout.selectProduct('product-test-1');
    await checkout.fillPaymentDetails({ cardNumber: '4111 1111 1111 1111', expiry: '12/30', cvv: '123' });
    await checkout.submitOrder();

    await expect(page.getByRole('heading', { name: /pedido confirmado/i })).toBeVisible();
    await expect(page.getByText(/número do pedido/i)).toBeVisible();
  });

  test('should show error when card is declined', async ({ page }) => {
    const checkout = new CheckoutPage(page);

    await checkout.goto();
    await checkout.selectProduct('product-test-1');
    // Cartão de teste que simula recusa — definido na documentação do gateway fake do ambiente de teste
    await checkout.fillPaymentDetails({ cardNumber: '4000 0000 0000 0002', expiry: '12/30', cvv: '123' });
    await checkout.submitOrder();

    await expect(page.getByRole('alert')).toContainText(/cartão recusado/i);
    await expect(page).toHaveURL('/checkout'); // usuário permanece na tela
  });

  test('should show empty cart message when cart is empty', async ({ page }) => {
    const checkout = new CheckoutPage(page);

    await checkout.goto();

    await expect(page.getByText(/seu carrinho está vazio/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /finalizar compra/i })).not.toBeVisible();
  });
});
```

### Passo 5 — Fixture de autenticação reutilizável

```typescript
// e2e/fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { TEST_USER } from '../support/test-data';

// Fixture que injeta uma página já autenticada
export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(TEST_USER.email, TEST_USER.password);
    await expect(page).toHaveURL('/home');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### Passo 6 — Dados de teste

```typescript
// e2e/support/test-data.ts
// Dados sintéticos fixos — sem dado real de produção (testes.md §7)
export const TEST_USER = {
  email: 'e2e-test-user@example-test.com', // conta de teste no ambiente
  password: process.env.E2E_TEST_PASSWORD ?? 'TestPassword@2024',
};

export const TEST_PRODUCTS = {
  standard: { id: 'product-test-1', name: 'Produto de Teste A' },
  premium: { id: 'product-test-2', name: 'Produto de Teste B' },
};
```

### Passo 7 — Seletores por prioridade

Usar seletores resistentes a mudança de layout (mesma prioridade que RTL — `testes.md §2`):

| Prioridade | Seletor | Exemplo |
|---|---|---|
| 1 | `getByRole` | `page.getByRole('button', { name: /confirmar/i })` |
| 2 | `getByLabel` | `page.getByLabel('CPF')` |
| 3 | `getByText` | `page.getByText('Pedido confirmado')` |
| 4 | `getByPlaceholder` | `page.getByPlaceholder('Digite seu e-mail')` |
| 5 | `data-testid` | `page.getByTestId('order-summary')` — último recurso |

```typescript
// ⛔ seletor por CSS/XPath — frágil, quebra com refatoração de estilo
page.locator('.checkout-btn');
page.locator('//button[contains(@class, "submit")]');

// ✅ seletor por role — resistente a refatoração
page.getByRole('button', { name: /finalizar compra/i });
```

---

## Escopo do E2E: o que testar e o que não testar

| Testar com E2E | Não testar com E2E |
|---|---|
| Happy path dos fluxos críticos de negócio | Lógica de validação (testar com unitário) |
| Mensagens de erro visíveis ao usuário | Todos os casos de borda (testar com integração) |
| Navegação e redirecionamento | Comportamento de componente isolado |
| Integração entre frontend e BFF | Regras de negócio internas de um serviço |

---

## Checklist de conclusão

- [ ] Page Objects para cada tela coberta — sem seletores duplicados no teste
- [ ] Seletores por role/label — sem CSS class ou XPath
- [ ] Dados sintéticos — sem email, CPF ou cartão real (`testes.md §7`)
- [ ] Cada teste independente — `beforeEach` reseta estado, nenhum teste depende de outro (`testes.md §3`)
- [ ] Casos cobertos: happy path + ao menos um caminho de erro por fluxo
- [ ] Nome dos testes: `should <comportamento> when <condição>` (`testes.md §1`)
- [ ] Credenciais de teste via variável de ambiente — nunca hardcoded (`seguranca.md §2`)
