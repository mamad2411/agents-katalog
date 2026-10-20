# Web Component Instructions

- Use Lit
- [decorators](https://lit.dev/docs/components/decorators/)
- Extend the `Base` class from `@components/base`.
- Use TypeScript decorators.
- Use the `accessor` keyword for `@property` and `@state`.
- Define styles using `static styles = [globalStyles, css\`...\`]`.
- For icons, export `lit-html` templates from `.ts` files (e.g., `src/icons/my-icon.ts`).
- Do not use React
- Do not use JavaScript
- Use @lit/context for state management
- Use @lit/task for async operations
- Each component should have its own folder with three files:
  - `index.ts`: The main component file.
  - `index.html.ts`: The HTML template.
  - `index.css.ts`: The CSS styles.
- Import the HTML and CSS files into the main component file.

## Routing

- Use `@vaadin/router` for client-side routing.
- Define routes centrally or within a shell component.
- See [Vaadin Instructions](vaadin.instructions.md) for detailed routing patterns.

## Architecture & State Management

### Model Pattern

For complex business logic and data handling, use the **Model Pattern**.

- Create dedicated `Model` classes (e.g., `CustomerModel`, `OrderModel`) to encapsulate API interactions, data parsing, and business rules.
- Models should be framework-agnostic where possible, or loosely coupled to the UI.
- This pattern complements `@lit/task` and `@lit/context`. Use Models for shared/complex data entities, and Tasks for component-specific async operations.

### Base Classes

- Use specialized Base Classes (e.g., `ViewElement` extending `BaseElement`) for shared functionality across similar components.
- Common use cases include handling loading states, error boundaries, or standard layout wrappers for views.

## Examples

index.ts:

```typescript
import { customElement, property, state } from 'lit/decorators.js';
import { html, css } from 'lit';
import { BaseElement, globalStyles } from '@components/base-element';
import { render } from './index.html.ts';
import { styles } from './index.css.ts';

@customElement('my-element')
export class MyElement extends BaseElement {
  static styles = [globalStyles, styles];

  @property({ type: String }) accessor name = 'World';

  @state() private accessor count = 0;

  private increment() {
    this.count++;
  }

  render() {
    return render.call(this);
  }
}
```

index.html.ts:

```typescript
import { html } from 'lit';

export function render() {
  return html`
    <div>
      <h1>Hello, ${this.name}!</h1>
      <p>Count: ${this.count}</p>
      <button @click=${this.increment}>Increment</button>
    </div>
  `;
}
```

index.css.ts:

```typescript
import { css } from 'lit';

export const styles = css`
  div {
    text-align: center;
  }
  button {
    padding: 8px 16px;
    font-size: 16px;
  }
`;
```
