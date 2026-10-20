---
name: reactivity
description: "Compile-time JS philosophy"
---

# Rich Harris JavaScript Philosophy

Applying Rich Harris' "compile-time over runtime" philosophy from Svelte and Rollup. The best runtime code is no runtime code.

---

## Core Philosophy

### Shift Work to Compile Time

> "Frameworks are not tools for organizing your code. They're tools for organizing your mind."

The virtual DOM was a necessary hack, not a permanent solution. Compile-time analysis can eliminate runtime overhead entirely.

```javascript
// Runtime framework (React)
// Ships entire diffing algorithm to browser
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// Compile-time framework (Svelte)
// Compiles to surgical DOM updates - no diffing needed
<script>
  let count = 0;
</script>
<button on:click={() => count++}>{count}</button>

// Svelte output: direct DOM manipulation
// button.textContent = count;
```

### Ship Less JavaScript

Every byte of JavaScript has a cost:
1. Download time
2. Parse time
3. Compile time
4. Execute time

The fastest JavaScript is JavaScript you don't ship.

### Reactivity Should Be Automatic

```javascript
// Manual reactivity (React) - you track dependencies
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);  // You must remember to add count

// Automatic reactivity (Svelte) - compiler tracks dependencies
$: document.title = `Count: ${count}`;
// Compiler knows count is a dependency
```

---

## Bundling Philosophy (Rollup)

### Tree Shaking Done Right

```javascript
// utils.js
export function used() { return 'used'; }
export function unused() { return 'unused'; }

// main.js
import { used } from './utils.js';
console.log(used());

// Rollup output: unused() is completely eliminated
// Other bundlers often can't remove it
```

**Why Rollup is better at tree-shaking:**
- ES modules only (no CommonJS ambiguity)
- Static analysis of imports/exports
- No side-effect assumptions unless marked

### Code Splitting Philosophy

```javascript
// Split on routes, not components
// Users load what they need when they need it

// Dynamic imports at route boundaries
const routes = {
  '/dashboard': () => import('./routes/Dashboard.svelte'),
  '/settings': () => import('./routes/Settings.svelte'),
};
```

---

## Framework Trade-offs

### Virtual DOM Costs

| Operation | Virtual DOM | Compiled (Svelte) |
|-----------|-------------|-------------------|
| Create element | Create VDOM node + diff + create real | Create real element |
| Update text | Create VDOM + diff + update real | Update real element |
| Memory | VDOM tree + real DOM | Real DOM only |
| Bundle size | Framework runtime + app | App only |

### When Virtual DOM Makes Sense

- Highly dynamic UIs where everything changes constantly
- When developer experience outweighs performance
- When team already knows React/Vue

### When Compile-Time Wins

- Performance-critical applications
- Bandwidth-constrained environments
- Simple to moderate interactivity
- When bundle size matters

---

## Svelte Patterns

### Component Design

```svelte
<!-- Props with defaults -->
<script>
  export let name = 'World';
  export let count = 0;
</script>

<!-- Reactive declarations -->
<script>
  let a = 1;
  let b = 2;
  $: sum = a + b;  // Automatically updates
  $: console.log(`Sum is ${sum}`);  // Reactive statement
</script>

<!-- Direct DOM binding -->
<input bind:value={name}>
<input type="number" bind:value={count}>
```

### Stores for Shared State

```javascript
// stores.js
import { writable, derived } from 'svelte/store';

export const count = writable(0);
export const doubled = derived(count, $count => $count * 2);

// Component usage - $ prefix auto-subscribes
<script>
  import { count, doubled } from './stores.js';
</script>

<button on:click={() => $count++}>
  {$count} × 2 = {$doubled}
</button>
```

---

## Build Optimization Rules

### 1. Analyze Before Optimizing

```bash
# Visualize bundle
npx rollup-plugin-visualizer
npx source-map-explorer bundle.js
```

### 2. Question Every Dependency

```javascript
// Before adding lodash for one function:
import { debounce } from 'lodash';  // 70KB

// Consider:
function debounce(fn, ms) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
}  // 200 bytes
```

### 3. Prefer Native Over Polyfill

```javascript
// Check browser support before polyfilling
// Modern browsers have:
// - fetch, Promise, async/await
// - Array methods (map, filter, find)
// - Object methods (entries, values, assign)
// - Template literals, destructuring, spread
```

---

## When to Apply

| Scenario | Apply Harris Philosophy |
|----------|------------------------|
| New project, performance matters | Yes - consider Svelte |
| Bundle size optimization | Yes - tree-shaking analysis |
| Framework selection | Yes - evaluate compile-time options |
| Existing React codebase | Partially - bundling insights |
| Server-side rendering | Yes - SvelteKit considerations |

---

## Source Material

- "Rethinking Reactivity" (talk)
- "The Truth About Virtual DOM" (blog)
- Svelte documentation and tutorials
- Rollup documentation
- Rich Harris on Twitter/talks
