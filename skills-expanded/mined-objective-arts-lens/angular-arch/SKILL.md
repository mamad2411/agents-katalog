---
name: angular-arch
description: "Angular architecture and organization patterns"
allowed-tools: []
---

# Deborah Kurata: Angular Architecture

Deborah Kurata's core belief: **Well-organized code is maintainable code.** Architecture decisions made early compound over the life of a project.

## The Foundational Principle

> "Structure your Angular application so that you can locate code quickly, identify what the code does at a glance, keep the flattest structure possible, and stay DRY."

The LIFT principle:
- **L**ocate code quickly
- **I**dentify code at a glance
- **F**lattest structure possible
- **T**ry to stay DRY

## Core Principles

### 1. Feature Module Organization

Organize by feature, not by type.

**Not this (organize by type):**
```
src/app/
├── components/
│   ├── user-list.component.ts
│   ├── product-list.component.ts
│   └── order-list.component.ts
├── services/
│   ├── user.service.ts
│   ├── product.service.ts
│   └── order.service.ts
└── models/
    ├── user.model.ts
    ├── product.model.ts
    └── order.model.ts
```

**This (organize by feature):**
```
src/app/
├── users/
│   ├── user-list.component.ts
│   ├── user-detail.component.ts
│   ├── user.service.ts
│   ├── user.model.ts
│   └── users.module.ts
├── products/
│   ├── product-list.component.ts
│   ├── product.service.ts
│   └── products.module.ts
└── shared/
    ├── components/
    ├── pipes/
    └── shared.module.ts
```

### 2. Module Types and Responsibilities

**Five types of modules:**

| Module Type | Purpose | Loads |
|-------------|---------|-------|
| Root (App) | Bootstrap | Once at startup |
| Feature | Business feature | Lazy loaded |
| Shared | Reusable components | Imported by features |
| Core | Singleton services | Once in AppModule |
| Routing | Route configuration | With parent module |

```typescript
// Core module - singleton services, guards
@NgModule({
  providers: [AuthService, LoggingService]
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parent: CoreModule) {
    if (parent) {
      throw new Error('CoreModule already loaded. Import only in AppModule.');
    }
  }
}

// Shared module - reusable, no singletons
@NgModule({
  declarations: [SpinnerComponent, TruncatePipe],
  exports: [SpinnerComponent, TruncatePipe, CommonModule]
})
export class SharedModule {}
```

### 3. Smart vs Presentational Components

Clear separation of concerns.

```
CONTAINER (Smart)              PRESENTATIONAL (Dumb)
─────────────────              ─────────────────────
user-shell.component           user-list.component
                               user-detail.component
                               user-form.component

Responsibilities:              Responsibilities:
- Fetch data                   - Display data
- Handle state                 - Emit events
- Coordinate children          - No service injection
- Route handling               - Pure @Input/@Output
```

**Naming convention:**
```
feature/
├── feature-shell.component.ts      # Smart container
├── feature-list.component.ts       # Presentational
├── feature-detail.component.ts     # Presentational
├── feature-edit.component.ts       # Presentational
└── feature.service.ts
```

### 4. Barrel Files (index.ts)

Export public API, hide internals.

```typescript
// users/index.ts
export * from './users.module';
export * from './user.model';
export * from './user.service';
// Don't export internal components

// Importing from outside the feature:
import { UserService, User } from '@app/users';
```

### 5. Path Aliases

Use TypeScript path aliases for clean imports.

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "paths": {
      "@app/*": ["src/app/*"],
      "@core/*": ["src/app/core/*"],
      "@shared/*": ["src/app/shared/*"],
      "@env/*": ["src/environments/*"]
    }
  }
}
```

**Usage:**
```typescript
// Instead of: import { UserService } from '../../../core/services/user.service';
import { UserService } from '@core/services/user.service';
```

### 6. State Management Patterns

Choose complexity appropriate to your app.

```
COMPLEXITY LEVEL           SOLUTION
────────────────           ────────
Simple                     Services + BehaviorSubject
Medium                     Component Store (@ngrx/component-store)
Complex                    Global Store (@ngrx/store)
```

**Simple state (service-based):**
```typescript
@Injectable({ providedIn: 'root' })
export class UserStateService {
  private usersSubject = new BehaviorSubject<User[]>([]);
  users$ = this.usersSubject.asObservable();

  setUsers(users: User[]) {
    this.usersSubject.next(users);
  }
}
```

**Medium state (component store):**
```typescript
interface UserState {
  users: User[];
  loading: boolean;
}

@Injectable()
export class UserStore extends ComponentStore<UserState> {
  readonly users$ = this.select(state => state.users);
  readonly loading$ = this.select(state => state.loading);

  readonly loadUsers = this.effect<void>(trigger$ =>
    trigger$.pipe(
      tap(() => this.patchState({ loading: true })),
      switchMap(() => this.userService.getAll().pipe(
        tapResponse(
          users => this.patchState({ users, loading: false }),
          error => this.patchState({ loading: false })
        )
      ))
    )
  );
}
```

### 7. Route Organization

One routing module per feature, lazy loaded.

```typescript
// app-routing.module.ts
const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  {
    path: 'users',
    loadChildren: () => import('./users/users.module').then(m => m.UsersModule)
  },
  {
    path: 'products',
    loadChildren: () => import('./products/products.module').then(m => m.ProductsModule)
  },
  { path: '**', component: PageNotFoundComponent }
];

// users/users-routing.module.ts
const routes: Routes = [
  {
    path: '',
    component: UserShellComponent,
    children: [
      { path: '', component: UserListComponent },
      { path: ':id', component: UserDetailComponent },
      { path: ':id/edit', component: UserEditComponent }
    ]
  }
];
```

### 8. Service Design Patterns

Services should be focused and testable.

```typescript
// Data service - HTTP operations
@Injectable({ providedIn: 'root' })
export class UserDataService {
  private url = '/api/users';

  constructor(private http: HttpClient) {}

  getAll(): Observable<User[]> {
    return this.http.get<User[]>(this.url);
  }

  getById(id: number): Observable<User> {
    return this.http.get<User>(`${this.url}/${id}`);
  }
}

// Facade service - coordinates multiple data services
@Injectable({ providedIn: 'root' })
export class UserFacadeService {
  constructor(
    private userData: UserDataService,
    private userState: UserStateService
  ) {}

  loadUsers() {
    this.userData.getAll().subscribe(users => {
      this.userState.setUsers(users);
    });
  }
}
```

### 9. Interface Segregation

Small, focused interfaces over large ones.

```typescript
// Not this - one big interface
interface User {
  id: number;
  name: string;
  email: string;
  address: Address;
  orders: Order[];
  preferences: Preferences;
  // ... 20 more properties
}

// This - focused interfaces
interface UserBasic {
  id: number;
  name: string;
  email: string;
}

interface UserWithAddress extends UserBasic {
  address: Address;
}

interface UserWithOrders extends UserBasic {
  orders: Order[];
}
```

### 10. Consistent Naming Conventions

```
ELEMENT                    NAMING CONVENTION
───────                    ─────────────────
Feature module             users.module.ts
Routing module             users-routing.module.ts
Component                  user-list.component.ts
Service                    user.service.ts
Directive                  highlight.directive.ts
Pipe                       truncate.pipe.ts
Guard                      auth.guard.ts
Resolver                   user.resolver.ts
Interceptor                logging.interceptor.ts
Model/Interface            user.model.ts
```

## The Kurata Test

Before committing architecture decisions, ask:

1. **Can I locate this code quickly?** By feature, not by type?
2. **Can I identify what this does at a glance?** Clear naming?
3. **Is the structure as flat as possible?** No unnecessary nesting?
4. **Am I repeating myself?** Should this be in SharedModule?
5. **Is this module focused?** One responsibility?
6. **Is state management appropriate?** Not over-engineered?

## When Reviewing Code

Apply these checks:

- [ ] Features organized in feature modules
- [ ] Core services in CoreModule (imported once)
- [ ] Shared components in SharedModule
- [ ] Smart/presentational component separation
- [ ] Lazy loading for feature modules
- [ ] Path aliases for clean imports
- [ ] Barrel files for public API
- [ ] Consistent naming conventions
- [ ] Appropriate state management complexity

## When NOT to Use This Skill

Use a different skill when:
- **Designing DI and testability** → Use `angular-core`
- **Optimizing performance** → Use `angular-perf`
- **Working with RxJS** → Use `rxjs`
- **Applying design patterns** → Use `design-patterns`

Kurata is the **Angular organization skill**—use it for project structure, module design, and architecture patterns.

## Sources

- Kurata, "Angular Architecture: Best Practices" (Pluralsight)
- Kurata, "RxJS and Reactive Forms in Angular" (Pluralsight)
- Angular Style Guide (influenced by Kurata's work)
- Kurata's conference talks and blog posts

---

*"Good architecture is not about choosing the right technology—it's about organizing code so your team can work effectively."* — Deborah Kurata
