---
name: angular-cypress
description: "ALWAYS use when testing Angular applications with Cypress, E2E testing, or component testing in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular + Cypress

**Version:** Cypress 13.x (2025)
**Tags:** Cypress, E2E, Testing, Component Tests

**References:** [Cypress](https://www.cypress.io/) • [Cypress Angular](https://docs.cypress.io/guides/component-testing/angular/overview)

## Best Practices

- Install Cypress

```bash
npm install -D cypress @cypress/angular cypress-visual-regression
npx cypress open
```

- Write E2E test

```ts
describe('My First Test', () => {
  it('visits the kitchen sink', () => {
    cy.visit('/');
    cy.contains('type').click();
    cy.get('.action-email').type('fake@email.com');
    cy.get('.action-email').should('have.value', 'fake@email.com');
  });
});
```

- Write component test

```ts
import { mount } from 'cypress/angular';
import { ButtonComponent } from './button.component';

describe('ButtonComponent', () => {
  it('renders button with text', () => {
    mount(ButtonComponent, { 
      componentProperties: { 
        label: 'Click me' 
      } 
    });
    cy.get('button').should('contain.text', 'Click me');
  });
});
```
