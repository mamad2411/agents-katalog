---
name: page-object-model
description: Apply Page Object Model (and the modern Screenplay/Component-Object variants) to keep UI tests readable, refactor-safe, and DRY. Use when structuring Playwright/Cypress/Selenium suites or rescuing brittle ones.
source: self
date_added: 2026-05-01
---

# Page Object Model

POM encapsulates **what a page exposes to a test** (selectors + actions) so test bodies read like user intent, not DOM scraping. This skill covers the modern shape (component objects, fixtures, Screenplay) plus the rules that prevent POM from rotting into a god-object.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Frameworks | Playwright 1.50 (preferred), Cypress 14, WebdriverIO 9, Selenium 4 |
| Locator strategy | Roles + accessible names (`getByRole`), `data-testid` as fallback |
| Patterns | Component Object Model (per UI component), Screenplay (Tasks + Questions + Abilities), Playwright fixtures |
| Linting | ESLint Playwright plugin, Cypress ESLint, Sonar rules `S2699` |

## When to Use

- E2E suite has duplicated selectors and copy-pasted flows.
- Non-engineers need to read tests.
- Test maintenance cost spikes after each UI refactor.
- Onboarding new engineers who keep copying selectors from old tests.

## Rules

1. **Page object exposes intent, not selectors.** `await login.signIn(user)` — never `await page.click('#btn-2')` in a test.
2. **No assertions inside the page object** beyond preconditions ("the form is visible"). Assertions belong in tests.
3. **Component objects > monolithic pages.** A `CheckoutPage` composes `AddressForm`, `PaymentForm`, `OrderSummary`.
4. **Locate by role + name first**, then `data-testid`. Never CSS selectors that mirror styling.
5. **Methods return the *next* page object** (or `void`) so flows compose.
6. **No `sleep`/manual waits.** Use auto-waiting locators or assertions on real state.
7. **Construct via fixtures**, not `new` in every test. Centralizes wiring and auth.

## Playwright — Component Objects + Fixtures

```ts
// pages/login.page.ts
import { Page, Locator } from '@playwright/test';
import { DashboardPage } from './dashboard.page';

export class LoginPage {
  private readonly email: Locator;
  private readonly password: Locator;
  private readonly submit: Locator;

  constructor(private readonly page: Page) {
    this.email    = page.getByRole('textbox', { name: 'Email' });
    this.password = page.getByRole('textbox', { name: 'Password' });
    this.submit   = page.getByRole('button',  { name: 'Sign in' });
  }

  async goto() { await this.page.goto('/login'); }

  async signIn(creds: { email: string; password: string }) {
    await this.email.fill(creds.email);
    await this.password.fill(creds.password);
    await this.submit.click();
    return new DashboardPage(this.page);
  }
}
```

```ts
// fixtures.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

export const test = base.extend<{ login: LoginPage }>({
  login: async ({ page }, use) => use(new LoginPage(page)),
});
export { expect };
```

```ts
// tests/login.spec.ts
import { test, expect } from '../fixtures';

test('valid user reaches dashboard', async ({ login }) => {
  await login.goto();
  const dash = await login.signIn({ email: 'a@b.co', password: 'pw' });
  await expect(dash.welcome).toBeVisible();
});
```

## Component Object Pattern

```ts
// components/address-form.ts
export class AddressForm {
  constructor(private readonly root: Locator) {}
  async fill(addr: Address) {
    await this.root.getByRole('textbox', { name: 'Street' }).fill(addr.street);
    await this.root.getByRole('combobox', { name: 'Country' }).selectOption(addr.country);
    await this.root.getByRole('textbox', { name: 'Postal code' }).fill(addr.postcode);
  }
}

// pages/checkout.page.ts
export class CheckoutPage {
  readonly shipping: AddressForm;
  readonly billing: AddressForm;
  constructor(page: Page) {
    this.shipping = new AddressForm(page.getByTestId('shipping'));
    this.billing  = new AddressForm(page.getByTestId('billing'));
  }
}
```

## Screenplay (advanced)

Use when tests describe roles & multi-actor scenarios:

```ts
await actorCalled('Alex')
  .whoCan(BrowseTheWeb.using(page))
  .attemptsTo(
    Login.as('alex@acme.com'),
    Add.toCart('SKU-42'),
    Checkout.placingOrder(),
  );
await ensure(actorCalled('Alex'), Order.confirmation()).isVisible();
```

Libraries: Serenity/JS, Playwright-bdd-screenplay.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| 5,000-line `HomePage` god object | Split into Component Objects per region |
| Assertions inside page methods | Move to tests; methods describe interactions only |
| Returning raw locators | Return next page object or void; encapsulate locators |
| CSS selectors mirroring styling | Use roles + names; only use `data-testid` when role is impossible |
| `await page.waitForTimeout(2000)` | Use locator auto-wait or poll on real state |
| Page object mutates test data | Page objects are stateless drivers; test owns data |
| Duplicated login per test | Use `storageState` or auth fixture once per worker |

## Output Format (review)

```
Suite: ui-e2e (Playwright)
Pages: 14   Components: 22
Test bodies avg lines: 7   (target ≤ 10)
Selector strategy: 78% getByRole, 18% data-testid, 4% CSS (action: replace)
Assertions in page objects: 0 ✅
Auth: storageState (1 setup test, reused) ✅
```

## References

- Martin Fowler — Page Object: <https://martinfowler.com/bliki/PageObject.html>
- Playwright — POM guide: <https://playwright.dev/docs/pom>
- Selenium docs — POM: <https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/>
- Serenity/JS — Screenplay: <https://serenity-js.org/handbook/design/screenplay-pattern/>
- Kent C. Dodds — Testing Library queries hierarchy: <https://testing-library.com/docs/queries/about/#priority>
