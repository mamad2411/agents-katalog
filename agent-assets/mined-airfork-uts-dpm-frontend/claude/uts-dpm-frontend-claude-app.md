# Application Root

Main Angular application code with feature modules, shared components, and services.

## Files

| File                 | What                              | When to read                        |
| -------------------- | --------------------------------- | ----------------------------------- |
| `app.component.ts`   | Root component with router outlet | Modifying app shell, global layout  |
| `app.component.html` | Root template with router outlet  | Changing app structure              |
| `app.routes.ts`      | Top-level routing configuration   | Adding routes, modifying navigation |

## Directories

| Directory         | What                                                   | When to read                    |
| ----------------- | ------------------------------------------------------ | ------------------------------- |
| `auth/`           | Authentication module (login, guards, password change) | Auth flow, login issues, guards |
| `dpms/`           | DPM management features (create, edit, approve, home)  | DPM functionality               |
| `users/`          | User management (list, detail, create, edit)           | User CRUD operations            |
| `ui/`             | Reusable UI component library                          | Building UI, component issues   |
| `services/`       | API services and business logic                        | Data fetching, API integration  |
| `models/`         | TypeScript interfaces and DTOs                         | Type definitions                |
| `shared/`         | Shared utilities, pipes, directives                    | Cross-cutting concerns          |
| `error-pages/`    | Error page components (404, 403)                       | Error handling UI               |
| `design-preview/` | Design preview component                               | Testing design system           |
