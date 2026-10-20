---
description: global guideline for next js implementation
globs: 
---
**Code Implementation Guidelines**

- **Simple Components**: Keep components always simple and focused on a single responsibility. Delegate any complex logic to custom hooks.
- **Use Hooks for Complexity**: Manage state, side effects, and business logic in custom hooks under the `hooks/` directory instead of bloating your components.
- **Folder Structure**:
  - `actions/`: Server Actions for Next.js (e.g., form submissions, mutations)
  - `app/`: Entry point and global configuration (layouts, providers)
    - `app/constants/`: Application-wide constants (environment flags, static values)
  - `hooks/`: Reusable custom hooks for state and logic
  - `services/`: Backend orchestration (controllers, services, repository usage)
  - `repository/`: Data access layer (database queries, ORM interfaces)
  - `types/`: Shared TypeScript types and interfaces
  - `utils/`: Pure utility functions and helpers
  - `components/`: Reusable, atomic UI components
- **Imports & Naming**: Always include required imports. Use descriptive file and function names.
- **DRY Principle**: Don’t Repeat Yourself. Extract shared logic into hooks or utilities.
- **Early Returns**: Favor early returns (`if (!data) return null;`) to improve readability.
- **Tailwind Styling**: Use only Tailwind CSS classes (`className="..."`). Avoid separate CSS files.
- **`class:` Syntax**: Prefer `class:` directives over ternary operators in `className` where possible.
- **Descriptive Identifiers**: Name variables and functions clearly. Event handlers should start with `handle` (e.g., `handleClick`).
- **Accessibility**: Add `tabIndex="0"`, `aria-label`, `onClick`, and `onKeyDown` on interactive elements.
- **Arrow Functions**: Declare functions as constants (`const toggle = () => {}`) and type them when possible.
- **TypeScript Types**: Never use `any`. Define interfaces or types in `types/`.
- **Button**: use @/components/Button for the button, when the button is not inside a form set the type="button"
- **fetch data**: Use swr to fetch data 


