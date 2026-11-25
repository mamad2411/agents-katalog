---
description: 
globs: 
alwaysApply: true
---

# Your rule content

### Module-Specific Rules

- Always check the details and requirements mentioned in [README.md](mdc:README.md) file.
- Strictly use JavaScript as the language for frontend and backend.
- Strictly use Kotlin and Jetpack Compose for mobile app.

#### Backend (Node.js, Express, MongoDB)

- Organize code into clear directories: `controllers/`, `routes/`, `models/`, `middlewares/`.
- Implement input validation and standardized error handling.
- Secure protected routes using JWT and role-based guards.
- Add MongoDB indexes on frequently queried fields.
- Use the `dotenv` package to manage environment variables.

#### Web Frontend (React, Next)

- Always follow the reference project structure and code provided in folder path: references/frontend; for writing frontend.
- Always use original documentation of Next JS for creating this project link: https://nextjs.org/docs/app/api-reference/cli/create-next-app .
- Follow a component-based structure, organizing by features or domains.
- Global state should be managed via React Context or Redux Toolkit.
- Use functional components only, with hooks for logic encapsulation.
- Ensure mobile responsiveness using Flexbox, CSS Grid, or Tailwind CSS.
- Create reusable form components for consistency and reduced code duplication.

#### Mobile Frontend (Kotlin + Jetpack Compose)

- Apply MVVM architecture: separate logic into `ui/`, `viewmodel/`, and `repository/`.
- Use Jetpack Navigation for managing screen routes.
- All long-running tasks (e.g., network calls) should use coroutines with proper error states.
- Define themes (colors, typography) centrally for consistent design.
- Persist tokens and session info using DataStore or SharedPreferences.
