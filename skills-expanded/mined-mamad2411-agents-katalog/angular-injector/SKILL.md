---
name: angular-injector
description: "ALWAYS use when working with Angular Injector, inject() function, Provider, or dependency resolution in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Injector

**Version:** Angular 21 (2025)
**Tags:** Injector, DI, Providers

**References:** [Injector API](https://angular.io/api/core/Injector)

## Best Practices

- Use inject()

```ts
@Component({})
export class MyComponent {
  private service = inject(MyService);
}
```

- Use Injector.get

```ts
const injector = Injector.create({
  providers: [{ provide: MyService }]
});
const service = injector.get(MyService);
```

- Use EnvironmentInjector

```ts
const environmentInjector = inject(EnvironmentInjector);
```
