# Cursor AI Rules for Playwright Test Automation Framework
# Author: Pramod Dutta | The Testing Academy

## Project Overview
This is an enterprise-grade Playwright test automation framework using TypeScript.
It follows a 3-layer architecture: Pages → Modules → Tests.

## Architecture Rules

### Layer 1: Pages (src/pages/)
- Define locators as arrow functions: `submitButton = () => this.page.locator('#submit')`
- Keep actions simple (single UI interaction)
- NO business logic or conditionals
- Use private page property in constructor

### Layer 2: Modules (src/modules/)
- Orchestrate multiple Page actions
- Contain business logic and workflows
- Use Logger for step tracking
- NO direct locator access - use Page methods only

### Layer 3: Tests (src/tests/)
- Use test.describe() for grouping
- Use test.step() for important actions
- Add tags: @P0, @P1, @P2, @Smoke, @Regression
- Use fixtures for page objects

## Code Style
- Use TypeScript strict mode
- Arrow functions for locators
- Async/await for all Playwright operations
- JSDoc comments for public methods
- No console.log (use Logger utility)

## File Naming
- Pages: `{Feature}Page.ts` (e.g., LoginPage.ts)
- Modules: `{Feature}Module.ts` (e.g., LoginModule.ts)
- Tests: `{feature}.spec.ts` (e.g., login.spec.ts)

## Import Paths
Use path aliases:
- `@pages/*` → `src/pages/*`
- `@modules/*` → `src/modules/*`
- `@utils/*` → `src/utils/*`

## Test Tags
- @P0: Critical priority
- @P1: High priority
- @P2: Medium priority
- @Smoke: Smoke tests
- @Regression: Full regression

## Common Patterns

### Page Object Example
```typescript
export class LoginPage {
    constructor(private page: Page) {}
    
    usernameInput = () => this.page.locator('#username');
    
    async fillUsername(value: string): Promise<void> {
        await this.usernameInput().fill(value);
    }
}
```

### Module Example
```typescript
export class LoginModule {
    private loginPage: LoginPage;
    
    constructor(page: Page) {
        this.loginPage = new LoginPage(page);
    }
    
    async doLogin(username: string, password: string): Promise<void> {
        await this.loginPage.fillUsername(username);
        await this.loginPage.fillPassword(password);
        await this.loginPage.clickLogin();
    }
}
```

### Test Example
```typescript
test.describe('@P0 @Login Login Tests', () => {
    test('should login successfully', async ({ page }) => {
        const loginModule = new LoginModule(page);
        
        await test.step('Login with valid credentials', async () => {
            await loginModule.doLogin('user', 'pass');
        });
    });
});
```

