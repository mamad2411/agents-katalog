---
name: angular-guards
description: "ALWAYS use when working with Angular Route Guards, CanActivate, CanDeactivate, CanLoad, or route protection in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Route Guards

**Version:** Angular 21 (2025)
**Tags:** Guards, Routing, Auth, CanActivate

**References:** [Guards Guide](https://angular.dev/guide/routing/router-tutorial#protecting-routes) • [CanActivate](https://angular.io/api/router/CanActivate)

## API Changes

This section documents recent version-specific API changes.

- NEW: Functional guards — Use `CanActivateFn` instead of class-based

- NEW: CanMatch guard — Prevent lazy loading of unauthorized code

- NEW: provideRouter with guards — Modern guard registration

- DEPRECATED: Class-based guards — Migrate to functional

## Best Practices

- Create functional guard

```ts
export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  return router.createUrlTree(['/login']);
};
```

- Use CanActivate for route protection

```ts
const routes: Routes = [
  {
    path: 'dashboard',
    canActivate: [authGuard],
    component: DashboardComponent
  }
];
```

- Use CanActivateChild for child routes

```ts
export const adminGuard: CanActivateChildFn = () => {
  const auth = inject(AuthService);
  return auth.isAdmin() || inject(Router).createUrlTree(['/unauthorized']);
};

const routes: Routes = [
  {
    path: 'admin',
    canActivateChild: [adminGuard],
    children: [...]
  }
];
```

- Use CanMatch for lazy loading

```ts
const routes: Routes = [
  {
    path: 'admin',
    canMatch: [authGuard],
    loadComponent: () => import('./admin/admin.component')
  }
];
```

- Use CanDeactivate for unsaved changes

```ts
export const canDeactivateGuard: CanDeactivateFn<CanComponentDeactivate> = (component) => {
  if (component.hasUnsavedChanges?.()) {
    return confirm('You have unsaved changes. Are you sure?');
  }
  return true;
};
```

- Use withComponentInputBinding

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding())
  ]
};
```

- Use multiple guards

```ts
const routes: Routes = [
  {
    path: 'admin',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./admin/admin.component')
  }
];
```

- Pass data to guards

```ts
const routes: Routes = [
  {
    path: 'user/:id',
    canActivate: [userGuard],
    data: { requiredRole: 'admin' }
  }
];

export const userGuard: CanActivateFn = (route, state) => {
  const requiredRole = route.data['requiredRole'];
  // Check role
};
```
