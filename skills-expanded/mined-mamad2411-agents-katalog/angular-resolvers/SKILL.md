---
name: angular-resolvers
description: "ALWAYS use when working with Angular Route Resolvers, data pre-fetching, or loading data before route activation."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Route Resolvers

**Version:** Angular 21 (2025)
**Tags:** Resolvers, Routing, Data Loading

**References:** [Resolvers Guide](https://angular.dev/guide/routing/router-tutorial#pre-fetching-data-with-a-resolver)

## Best Practices

- Create functional resolver

```ts
export const userResolver: ResolveFn<User> = (route, state) => {
  const userService = inject(UserService);
  const userId = route.paramMap.get('id');
  return userService.getUser(userId!);
};
```

- Use resolver in route

```ts
const routes: Routes = [
  {
    path: 'user/:id',
    resolve: { user: userResolver },
    component: UserComponent
  }
];
```

- Get resolved data in component

```ts
@Component({})
export class UserComponent {
  private route = inject(ActivatedRoute);
  
  user = this.route.snapshot.data['user'];
  
  // Or with input binding (Angular 17+)
  userId = input<string>();
}
```

- Handle resolver errors

```ts
export const dataResolver: ResolveFn<Data> = (route, state) => {
  const service = inject(DataService);
  return service.getData().pipe(
    catchError(() => of(null))
  );
};
```

- Use multiple resolvers

```ts
const routes: Routes = [
  {
    path: 'dashboard',
    resolve: {
      user: userResolver,
      settings: settingsResolver
    },
    component: DashboardComponent
  }
];
```
