---
name: tpl-frontend-angular-ngrx
description: Template do pack (frontend/10-angular-ngrx.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/10-angular-ngrx.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/10-angular-ngrx.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Angular 17+ + NgRx
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Angular | 17+ |
| Linguagem | TypeScript | 5.x (strict) |
| State Management | NgRx | 17+ |
| Reatividade | RxJS | 7.x |
| UI Components | Angular Material | 17+ |
| Testes unitários | Jest + Testing Library | latest |
| Testes e2e | Playwright | latest |
| Node.js | Node.js | 20 LTS |
| Build | Angular CLI / Nx | — |

---

## PROJECT STRUCTURE

```
src/
├── app/
│   ├── core/                        # Singleton services, guards, interceptors
│   │   ├── auth/
│   │   │   ├── auth.guard.ts
│   │   │   ├── auth.service.ts
│   │   │   └── auth.interceptor.ts
│   │   ├── http/
│   │   │   └── error.interceptor.ts
│   │   └── core.providers.ts        # provideCore() function
│   ├── shared/
│   │   ├── components/              # Componentes reutilizáveis standalone
│   │   ├── directives/
│   │   ├── pipes/
│   │   └── utils/
│   ├── features/
│   │   ├── dashboard/
│   │   │   ├── data-access/         # Store, effects, selectors, actions
│   │   │   │   ├── +state/
│   │   │   │   │   ├── dashboard.actions.ts
│   │   │   │   │   ├── dashboard.effects.ts
│   │   │   │   │   ├── dashboard.reducer.ts
│   │   │   │   │   ├── dashboard.selectors.ts
│   │   │   │   │   └── dashboard.state.ts
│   │   │   │   └── dashboard.service.ts
│   │   │   ├── ui/
│   │   │   │   ├── dashboard-card/
│   │   │   │   └── dashboard-chart/
│   │   │   ├── dashboard.component.ts
│   │   │   ├── dashboard.component.html
│   │   │   ├── dashboard.routes.ts
│   │   │   └── index.ts             # public API do feature
│   │   └── users/
│   │       └── (mesma estrutura)
│   ├── app.component.ts
│   ├── app.config.ts                # provideRouter, provideStore, etc.
│   └── app.routes.ts
├── environments/
│   ├── environment.ts
│   └── environment.prod.ts
└── main.ts
```

---

## STANDALONE COMPONENTS — REGRAS

**Angular 17+ usa standalone por padrão. Sem NgModules.**

```typescript
// ✅ CORRETO — standalone component
@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule, MatCardModule, RouterModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <mat-card>
      <h2>{{ user().name }}</h2>
      <p>{{ user().email }}</p>
    </mat-card>
  `,
})
export class UserCardComponent {
  user = input.required<User>();
  userSelected = output<User>();
}
```

**Regras de componentes:**
1. Todo componente é `standalone: true`.
2. Todo componente usa `ChangeDetectionStrategy.OnPush` — sem exceção.
3. Componentes são "dumb" (apresentação) ou "smart" (container) — nunca misturar.
4. Smart components: injetam Store, services; Dumb components: apenas `input()`/`output()`.
5. Nenhum componente tem lógica de negócio — delegar para services ou effects.

---

## SIGNALS VS OBSERVABLES — DECISION TABLE

| Situação | Usar | Motivo |
|---------|------|--------|
| State local do componente | `signal()` | Simples, síncrono, sem overhead RxJS |
| Propriedade derivada de state | `computed()` | Memoizado, reativo |
| Side effect por mudança de signal | `effect()` | Não usar para mutations de state |
| Stream de eventos HTTP | `Observable` | Async, cancelável, pipe operators |
| State global da aplicação | NgRx Store (Observable) | Previsível, debuggável, testável |
| Formulários reativos | `FormControl` (Observable) | Já é RxJS |
| Dados da Store no template | `store.select()` com `async` pipe | Desinscrição automática |
| Combinação de múltiplos streams | `combineLatest`, `switchMap` etc. | Poder do RxJS |
| Timer / polling | `interval()` + `takeUntilDestroyed` | Gerenciamento de lifecycle |

```typescript
// Signal local — estado simples do componente
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
  }
}

// Observable da store — dados globais
export class UserListComponent {
  private store = inject(Store);
  users$ = this.store.select(selectAllUsers);
  loading$ = this.store.select(selectUsersLoading);
}
```

---

## NGRX STORE PATTERN

### State

```typescript
// features/users/data-access/+state/users.state.ts
export interface UsersState {
  users: User[];
  selectedUserId: string | null;
  loading: boolean;
  error: string | null;
}

export const initialUsersState: UsersState = {
  users: [],
  selectedUserId: null,
  loading: false,
  error: null,
};
```

### Actions

```typescript
// features/users/data-access/+state/users.actions.ts
import { createActionGroup, emptyProps, props } from '@ngrx/store';

export const UsersActions = createActionGroup({
  source: 'Users',
  events: {
    'Load Users': emptyProps(),
    'Load Users Success': props<{ users: User[] }>(),
    'Load Users Failure': props<{ error: string }>(),
    'Select User': props<{ userId: string }>(),
    'Create User': props<{ user: CreateUserDto }>(),
    'Create User Success': props<{ user: User }>(),
    'Create User Failure': props<{ error: string }>(),
    'Delete User': props<{ userId: string }>(),
    'Delete User Success': props<{ userId: string }>(),
  },
});
```

### Reducer

```typescript
// features/users/data-access/+state/users.reducer.ts
import { createReducer, on } from '@ngrx/store';
import { UsersActions } from './users.actions';

export const usersReducer = createReducer(
  initialUsersState,

  on(UsersActions.loadUsers, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(UsersActions.loadUsersSuccess, (state, { users }) => ({
    ...state,
    users,
    loading: false,
  })),

  on(UsersActions.loadUsersFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error,
  })),

  on(UsersActions.deleteUserSuccess, (state, { userId }) => ({
    ...state,
    users: state.users.filter((u) => u.id !== userId),
  }))
);
```

### Selectors

```typescript
// features/users/data-access/+state/users.selectors.ts
import { createFeatureSelector, createSelector } from '@ngrx/store';

export const selectUsersState = createFeatureSelector<UsersState>('users');

export const selectAllUsers = createSelector(
  selectUsersState,
  (state) => state.users
);

export const selectUsersLoading = createSelector(
  selectUsersState,
  (state) => state.loading
);

export const selectSelectedUser = createSelector(
  selectUsersState,
  (state) => state.users.find((u) => u.id === state.selectedUserId) ?? null
);

// Memoized com argumentos
export const selectUserById = (userId: string) =>
  createSelector(selectAllUsers, (users) => users.find((u) => u.id === userId));
```

### Effects

```typescript
// features/users/data-access/+state/users.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, exhaustMap, map, of } from 'rxjs';

@Injectable()
export class UsersEffects {
  private actions$ = inject(Actions);
  private usersService = inject(UsersService);

  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.loadUsers),
      exhaustMap(() =>
        this.usersService.getAll().pipe(
          map((users) => UsersActions.loadUsersSuccess({ users })),
          catchError((err) =>
            of(UsersActions.loadUsersFailure({ error: err.message }))
          )
        )
      )
    )
  );

  createUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.createUser),
      exhaustMap(({ user }) =>
        this.usersService.create(user).pipe(
          map((created) => UsersActions.createUserSuccess({ user: created })),
          catchError((err) =>
            of(UsersActions.createUserFailure({ error: err.message }))
          )
        )
      )
    )
  );
}
```

---

## DEPENDENCY INJECTION — REGRAS

```typescript
// ✅ CORRETO — usar inject() em vez de constructor injection para componentes standalone
@Component({ standalone: true })
export class UserListComponent {
  private store = inject(Store);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.store.dispatch(UsersActions.loadUsers());
  }
}

// ✅ CORRETO — provideIn: 'root' para singleton global
@Injectable({ providedIn: 'root' })
export class AuthService { }

// ✅ CORRETO — scoped service em feature-level provider
// No routes do feature:
{
  providers: [{ provide: UsersService, useClass: UsersService }]
}
```

**Regras DI:**
1. Usar `inject()` em standalone (não constructor injection).
2. `providedIn: 'root'` apenas para services verdadeiramente singleton.
3. Services de feature ficam em `providers` da rota lazy.
4. Interceptors: registrar em `app.config.ts` via `withInterceptors([...])`.
5. Guards: usar functional guards `() => inject(AuthGuard).canActivate()`.

---

## ROUTING TABLE

| Trigger | Rota | Componente | Guard | Descrição |
|---------|------|-----------|-------|-----------|
| Acessa `/` | `''` | `HomeComponent` | — | Landing page |
| Acessa `/login` | `'login'` | `LoginComponent` | `noAuthGuard` | Redireciona se já logado |
| Acessa `/dashboard` | `'dashboard'` | `DashboardComponent` | `authGuard` | Lazy loaded |
| Acessa `/users` | `'users'` | `UserListComponent` | `authGuard` | Dispara LoadUsers |
| Acessa `/users/:id` | `'users/:id'` | `UserDetailComponent` | `authGuard` | Resolve com selectUserById |
| Clica "Criar usuário" | — | Dispatch `CreateUser` action | — | Effect faz chamada HTTP |
| Clica "Deletar" | — | Dispatch `DeleteUser` action | — | Dialog de confirmação primeiro |
| Erro 404 | `'**'` | `NotFoundComponent` | — | Catch-all |

---

## APP.CONFIG.TS

```typescript
// app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter, withComponentInputBinding, withViewTransitions } from '@angular/router';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { isDevMode } from '@angular/core';
import { routes } from './app.routes';
import { authInterceptor } from './core/http/auth.interceptor';
import { errorInterceptor } from './core/http/error.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding(), withViewTransitions()),
    provideHttpClient(withInterceptors([authInterceptor, errorInterceptor])),
    provideStore(), // providers de feature ficam nas rotas lazy
    provideEffects(),
    provideStoreDevtools({ maxAge: 25, logOnly: !isDevMode() }),
  ],
};
```

---

## TESTES

```typescript
// spec do componente
import { render, screen } from '@testing-library/angular';
import { MockStore, provideMockStore } from '@ngrx/store/testing';
import { UserListComponent } from './user-list.component';
import { selectAllUsers } from '../data-access/+state/users.selectors';

describe('UserListComponent', () => {
  it('exibe lista de usuários', async () => {
    const initialState = { users: { users: [{ id: '1', name: 'Alice' }], loading: false, error: null } };

    await render(UserListComponent, {
      providers: [provideMockStore({ initialState })],
    });

    expect(screen.getByText('Alice')).toBeTruthy();
  });
});

// spec do reducer
describe('usersReducer', () => {
  it('set loading=true em loadUsers', () => {
    const action = UsersActions.loadUsers();
    const state = usersReducer(initialUsersState, action);
    expect(state.loading).toBe(true);
  });
});
```

---

## QUALITY GATES

- [ ] `npx ng build --configuration production` — sem erros de build
- [ ] `npx jest --coverage` — cobertura > 80% em branches
- [ ] `npx tsc --noEmit` — sem erros TypeScript
- [ ] `npx eslint . --max-warnings 0` — sem warnings
- [ ] Todos os componentes têm `ChangeDetectionStrategy.OnPush`
- [ ] Nenhum subscribe sem `takeUntilDestroyed` ou `async` pipe
- [ ] Actions seguem convenção `createActionGroup`
- [ ] Efeitos têm tratamento de erro com `catchError` → action failure
- [ ] Nenhum componente acessa diretamente o HTTP service — apenas via Store/effects
- [ ] `standalone: true` em todos os componentes, pipes e directives

---

## FORBIDDEN

```
❌ NUNCA usar NgModules — projeto é 100% standalone
❌ NUNCA usar ChangeDetectionStrategy.Default — sempre OnPush
❌ NUNCA chamar HTTP diretamente do componente — usar effects
❌ NUNCA manipular o DOM diretamente — usar Renderer2 ou ng-template
❌ NUNCA usar `document.getElementById` ou similar
❌ NUNCA colocar lógica de negócio em componentes — mover para services/effects
❌ NUNCA criar subscription sem gerenciar o ciclo de vida
❌ NUNCA usar `any` em TypeScript — sempre tipar explicitamente
❌ NUNCA mutar o state diretamente no reducer — sempre spread operator
❌ NUNCA acessar o Store de dentro de um service — apenas componentes e effects
❌ NUNCA usar `effect()` para mutar outros signals (causa loops)
❌ NUNCA commit sem rodar quality gates
```

---

## COMMANDS

```bash
# Dev
ng serve

# Build produção
ng build --configuration production

# Gerar componente standalone
ng generate component features/users/ui/user-card --standalone --change-detection OnPush

# Gerar feature store
ng generate @ngrx/schematics:feature features/users/data-access/+state/users --module app --creators

# Testes
npx jest
npx jest --coverage
npx jest --watch

# E2E
npx playwright test

# Lint
ng lint --fix
```
