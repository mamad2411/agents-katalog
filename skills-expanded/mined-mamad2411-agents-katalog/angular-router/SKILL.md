---
name: angular-router
description: "ALWAYS use when working with Angular Router, routing configuration, guards, resolvers, lazy loading, or navigation in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/router

**Version:** Angular 21 (2025)
**Tags:** Routing, Navigation, Guards, Lazy Loading, SPA

**References:** [Docs](https://angular.dev/guide/routing) — official routing guide • [API](https://angular.io/api/router) • [GitHub](https://github.com/angular/angular/tree/main/packages/router)

## API Changes

This section documents recent version-specific API changes.

- NEW: Functional guards and resolvers — Prefer functional approach over class-based guards [source](https://angular.dev/guide/routing/router-tutorial#functional-guards)

- NEW: Router inputs — New way to pass data to components via route inputs [source](https://angular.dev/guide/routing/router-tutorial#router-inputs)

- NEW: withComponentInputBinding — Enable component input binding from route params

- NEW: Router snapshots improvement — Better type safety for route parameters

- NEW: provideRouter() — Modern router configuration with functional providers

- DEPRECATED: RouterModule.forRoot() — Use provideRouter() in modern applications

## Best Practices

- Use lazy loading for feature modules — Reduce initial bundle size by 50-70%

```ts
const routes: Routes = [
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/dashboard.routes').then(m => m.DASHBOARD_ROUTES)
  }
];
```

- Use functional guards over class-based guards

```ts
// ✅ Modern functional guard
const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  return router.createUrlTree(['/login']);
};

// ❌ Avoid class-based guards for new code
// @Injectable() export class AuthGuard implements CanActivate { ... }
```

- Use CanMatch guard for lazy-loaded routes — Prevents unauthorized code downloads

```ts
{
  path: 'admin',
  canMatch: [authGuard],
  loadComponent: () => import('./admin/admin.component').then(m => m.AdminComponent)
}
```

- Use resolvers for pre-fetching data — Eliminates loading spinners

```ts
{
  path: 'user/:id',
  resolve: { user: userResolver }
}

// In component
@Component({})
export class UserComponent {
  private route = inject(ActivatedRoute);
  
  // Modern way
  user = input.required<User>();
  
  // Legacy way
  ngOnInit() {
    this.route.data.subscribe(data => {
      this.user = data['user'];
    });
  }
}
```

- Use router inputs for better type safety

```ts
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding())
  ]
};

// Component receives route params as inputs
@Component({})
export class UserComponent {
  @Input() id!: string;
}
```

- Use wildcard routes for 404 pages

```ts
{
  path: '**',
  component: NotFoundComponent
}
```

- Use PreloadAllModules for background loading

```ts
provideRouter(routes, withPreloading(PreloadAllModules))
```

- Use routerLink for navigation — Maintains SPA behavior

```ts
// ✅ Correct
<a routerLink="/dashboard">Dashboard</a>

// ❌ Wrong - causes full page reload
<a href="/dashboard">Dashboard</a>
```

- Use kebab-case for URL paths — Consistent naming convention

```ts
// ✅ Good
{ path: 'user-profile', ... }

// ❌ Avoid
{ path: 'userProfile', ... }
```
