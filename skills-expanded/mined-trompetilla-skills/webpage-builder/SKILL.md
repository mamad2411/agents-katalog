# Webpage Builder Skill

This skill allows agents to build, test, and deploy single-page applications (SPAs) using vanilla JavaScript, HTML, and CSS. It prioritizes simplicity, testability, and stability without relying on heavy build tools or frameworks.

## 1. Process: The "Spec-First" Loop

To ensure quality and prevent regressions, follow this strict loop:

1.  **Spec**: Define the requirements in `benchmarks/apps/<app-name>/spec.md`. List features, UI states, and data models.
2.  **Test**: Write a headless logic test in `apps/<app-name>/test.js` using Node.js's native test runner. Mock browser APIs (like `localStorage`).
3.  **Code**: Implement the logic in `apps/<app-name>/js/store.js` until the test passes.
4.  **UI**: Build the UI in `apps/<app-name>/index.html` and `apps/<app-name>/js/app.js`, connecting it to the tested Store.
5.  **Verify**: Open the app in a browser (or use `browser` tool) to verify the UI.

## 2. Architecture: Vanilla MVC

We use a lightweight "Vanilla MVC" pattern:

### The Store (`store.js`)
*   **Role**: Manages data state and business logic.
*   **Dependencies**: Zero DOM dependencies. Uses `localStorage` for persistence.
*   **Interface**: Exposes methods like `getItems()`, `addItem()`, `updateItem()`.
*   **Testing**: Can be tested in Node.js by mocking `localStorage`.

### The Router (`app.js`)
*   **Role**: Handles navigation via URL hashes (e.g., `#list`, `#detail:123`).
*   **Mechanism**: Listens to `hashchange` events and calls the appropriate render function.

### The App (`app.js`)
*   **Role**: Renders UI based on the current route and Store data.
*   **Mechanism**: Clears a main container (e.g., `<div id="view">`) and injects HTML strings.
*   **Interactivity**: Binds event listeners to DOM elements after rendering.

## 3. Testing: Headless Logic

Since the Store has no DOM dependencies, we can test it using `node --test`.

**Example Test Setup (`test.js`):**

```javascript
const test = require('node:test');
const assert = require('node:assert');
const Store = require('./js/store.js');

// Mock localStorage
class MockStorage {
    constructor() { this.store = {}; }
    getItem(key) { return this.store[key] || null; }
    setItem(key, value) { this.store[key] = value.toString(); }
    clear() { this.store = {}; }
}
global.localStorage = new MockStorage();

test('Store adds an item', (t) => {
    const store = new Store('test_key');
    store.addItem('New Item');
    assert.strictEqual(store.getItems().length, 1);
});
```

To run: `node apps/<app-name>/test.js`

## 4. Gatekeeping: EVAL.md

Before marking a task as complete, create or update `EVAL.md` in the app's directory. This file should contain a checklist of manual verification steps for the UI, as automated tests only cover logic.

**Example `EVAL.md`:**
```markdown
# Evaluation Checklist

- [ ] App loads without console errors.
- [ ] Creating an item updates the list immediately.
- [ ] Refreshing the page persists the data.
- [ ] Clicking "Delete" removes the item.
```

## 5. Templates

Use the template in `skills/webpage_builder/templates/vanilla-app/` to bootstrap new projects. It includes the directory structure and boilerplate code for the Store, Router, and App.
