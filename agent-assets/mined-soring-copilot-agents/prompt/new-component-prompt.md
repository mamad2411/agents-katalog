---
name: new-component
description: Scaffold a new Vue 3 or React component with types, composable, and tests
agent: implementer
model: GPT-5.1-Codex
tools:
  - editFiles
  - createFile
  - codebase
  - search
  - problems
  - usages
  - runInTerminal
  - runTests
---

# Create New Frontend Component

## Component: ${input:componentName:Component name (e.g., "UserProfileCard")}
## Framework: ${input:framework:vue or react}

Create a complete frontend component following project conventions.

### For Vue 3 Components

1. **Component** (`frontend/src/components/`)
   - `<script setup lang="ts">` with typed props and emits
   - Responsive template with semantic HTML
   - `<style scoped>` with CSS custom properties

2. **Composable** (`frontend/src/composables/`) — if data fetching or complex logic needed
   - Reactive state management with `ref()` / `computed()`
   - Error and loading state handling
   - Cleanup on component unmount

3. **Types** (`frontend/src/types/`)
   - Interface for component props
   - Interface for API response data (if applicable)
   - Export from barrel file

4. **Tests** (`frontend/src/components/__tests__/`)
   - Render with default props
   - Render with various prop combinations
   - User interaction tests (click, input, submit)
   - Emitted event assertions

### For React Components

1. **Component** (`frontend/src/components/`)
   - Typed functional component with `interface Props`
   - Hooks for state and side effects
   - Clean JSX with semantic HTML

2. **Custom Hook** (`frontend/src/hooks/`) — if reusable logic
   - TanStack Query for server state
   - Proper cleanup and error handling

3. **Types** (`frontend/src/types/`)
   - Component prop types
   - API response types

4. **Tests** (`frontend/src/components/__tests__/`)
   - Testing Library queries by role/label
   - User interaction with `userEvent`
   - Async state assertions

### Verify after creation
- Run `#runTests` to ensure all tests pass
- Check `#problems` for type errors
