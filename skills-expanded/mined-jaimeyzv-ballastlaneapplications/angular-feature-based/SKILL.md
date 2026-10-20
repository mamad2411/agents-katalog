---
name: angular-feature-based
description: Frontend architecture + coding style + packages for the Angular frontend — feature folder conventions, standalone components, feature independence/boundaries, kebab-case naming, signals vs constructor injection, session-as-boolean AuthService, guard pair, Tailwind usage, and npm/Angular CLI package management. Read when scaffolding or editing any Angular feature, component, service, model, or route. Confirmed from jaimeyzv/angular-feture-based-architecture and jaimeyzv/online-loan-management-system-api's real auth feature.
---

# Angular Feature-Based Architecture

This is the single skill for how the Angular frontend is structured, styled, and packaged. For error handling and security specifics, see the `error-handling-frontend` and `security-frontend` skills.

## Feature Independence (boundary rules)

- **Each feature is self-contained** — `tasks` and `auth` don't reach into each other's internals directly. High cohesion inside a feature, low coupling between features. Share only through a feature service's public surface (e.g. `tasks` reads auth state via `AuthService`'s `isAuthenticated`/`isAuthenticated$`, never by importing auth internals).
- **Ask before extracting shared code** into a `core`/`shared` folder — confirm something is genuinely cross-cutting first.
- **Dependency of `tasks` on `auth`** goes only through `AuthService`'s public API. Session state is a **derived boolean** (`BehaviorSubject<boolean>`), not a stored token — see the `security-frontend` skill.

## Two Confirmed Real Shapes — Use the Right One

This codebase actually has two slightly different feature-internal layouts, both legitimate:

**"CRUD feature" shape** (`tasks`, `loans`, `installments` in the reference repos) — components live under a `components/` subfolder:
```
features/tasks/
  components/
    task-list/
      task-list.component.ts
      task-list.component.html
      task-list.component.scss
      task-list.component.spec.ts
    task-create/
    task-edit/
  models/
    task.model.ts
  services/
    task-service.ts
    task-service.spec.ts
```

**"Auth feature" shape** — top-level pages sit directly under the feature, no `components/` nesting:
```
features/auth/
  login/
    login.component.ts
    login.component.html
    login.component.scss
  register/
    register.component.ts
    register.component.html
    register.component.scss
  services/
    auth.service.ts
    login.service.ts
    logout.service.ts
    interceptor.service.ts
  guards/
    auth.guard.ts
```

**When scaffolding a new feature, match whichever shape the feature is actually closer to** — a feature with several interchangeable CRUD views (list/create/edit) fits the `components/` nesting; a feature that's really a small number of distinct pages/flows (like auth) doesn't need the extra nesting level. Don't force one shape onto the other for consistency's sake — the real codebase doesn't.

## Scaffolding a New Component

```bash
ng generate component features/tasks/components/task-detail --standalone
```

- **Always `--standalone`.** Never generate into an NgModule.
- **kebab-case is automatic** via the CLI — don't hand-roll file names.

## Component Shape — Two Valid Injection Styles, Match the File

Confirmed real: the codebase mixes `inject()` (newer style) and constructor injection (used throughout the real `LoginComponent`/`RegisterComponent`/`AuthService`). Both are valid Angular; **match whichever style the file you're editing already uses** rather than converting on sight.

```typescript
// Constructor injection — confirmed real style in auth components
export class LoginComponent {
  constructor(
    private fb: FormBuilder,
    private loginService: LoginService,
    private router: Router,
    private route: ActivatedRoute,
    private authService: AuthService
  ) {}
}

// inject() — equally valid for new components, especially with signals
export class TaskListComponent {
  private taskService = inject(TaskService);
  tasks = signal<Task[]>([]);
}
```

## Component Responsibilities

- **Local UI state as class fields or signals** (`loading`, `showError`, `errorMessage` — confirmed real pattern in `LoginComponent`/`RegisterComponent`), never in the service.
- **Forms via `ReactiveFormsModule`**, confirmed real (`FormBuilder`, `FormGroup`, `Validators`) — build the form in the constructor or as a class field, validate with Angular's built-in validators for shape (`required`, `email`, `maxLength`), leave business validation to the backend.

```typescript
this.form = this.fb.group({
  username: ['', [Validators.required, Validators.maxLength(50)]],
  email: ['', [Validators.required, Validators.email]],
  password: ['', [Validators.required]],
});
```

## Services

- **State-holding services use `BehaviorSubject`**, confirmed real (`AuthService.isAuthenticatedSubject`) — exposed as `<name>$` observable plus a synchronous getter when consumers need both reactive and immediate reads.
- **Action-only services (no state) are plain injectable classes** — `LoginService` (HTTP calls), `LogoutService` (logout flow + navigation) — don't merge these into `AuthService` just because they're auth-related; split by responsibility (state vs. action), matching the real codebase.
- **`providedIn: 'root'`** on every feature service — no feature-level providers array, no lazy-provided services in this codebase's pattern.

```typescript
@Injectable({ providedIn: 'root' })
export class TaskService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/tasks`;
  constructor(private http: HttpClient) {}

  getAll(): Observable<Task[]> {
    return this.http.get<Task[]>(this.apiUrl);
  }
}
```

## Tailwind Usage

- **Utility classes directly in templates**, no separate `.scss` rules for anything Tailwind can express — the reference repo's `.postcssrc.json` + Tailwind setup is the standard; a component's `.scss` file exists for the rare case Tailwind genuinely can't cover (complex animations, pseudo-element tricks), not as a dumping ground for spacing/color that a utility class would handle.

```html
<!-- DO -->
<button class="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:opacity-50"
        [disabled]="loading">
  {{ loading ? 'Signing in…' : 'Sign in' }}
</button>
```

## Routing Composition

Features are wired together at the app level, referencing feature-level guards — not each feature managing its own routing module.

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent), canActivate: [noAuthGuard] },
  { path: 'register', loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent), canActivate: [noAuthGuard] },
  { path: 'tasks', loadComponent: () => import('./features/tasks/components/task-list/task-list.component').then(m => m.TaskListComponent), canActivate: [authGuard] },
];
```

- **`loadComponent` for standalone lazy loading** — matches the standalone-only convention, no route-level NgModules.

## Coding Style (TypeScript/Angular)

- **kebab-case for all files:** `task-list.component.ts`, `task-service.ts`, `task.model.ts`. One component per folder, co-located with its `.html`, `.scss`, `.spec.ts`.
- **PascalCase** for classes/interfaces/types; **camelCase** for variables/functions/properties; **kebab-case** for selectors (`app-task-list`).
- **Prefer signals for local component state** (`signal`, `computed`). Use RxJS/`Observable` where the data is inherently a stream (HTTP responses, router events) — that stays in the service layer.
- **Typed `Observable<T>` from every HTTP call — no `any`.**

```typescript
getAll(): Observable<Task[]> {
  return this.http.get<Task[]>(`${this.apiUrl}/tasks`);
}
```

- **One service per feature owns its `apiUrl`**, built from `environment.apiBaseUrl` (never a hardcoded `https://localhost:XXXX` string). Split a service only when responsibilities genuinely diverge (state vs. one-off actions) — the way `auth` splits into `AuthService`/`LoginService`/`LogoutService` — not preemptively.
- **Tailwind utility classes in templates**, no separate custom CSS unless Tailwind genuinely can't express it.

## Packages (npm / Angular CLI)

- **Never hardcode versions from memory** — Angular and Tailwind move fast. `npm install <package>` without pinning unless a specific version is required for toolchain compatibility.
- **Scaffold via the CLI** (`ng generate component features/<feature>/components/<name> --standalone`) rather than hand-writing boilerplate — keeps files consistent with current conventions and avoids accidentally generating NgModule-based code.
- **Core set:** `@angular/core|common|router|forms` (Angular 20+, standalone), built-in `HttpClient`, `tailwindcss`/`postcss`/`autoprefixer`, CLI's default Jasmine + Karma. Run `ng update` to check versions rather than assuming from memory. Keep `package-lock.json` committed.
