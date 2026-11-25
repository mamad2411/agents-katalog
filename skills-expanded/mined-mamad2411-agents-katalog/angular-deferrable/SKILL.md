---
name: angular-deferrable
description: "ALWAYS use when working with Angular Deferrable Views, @defer, lazy loading components, or deferred loading in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Deferrable Views

**Version:** Angular 17+ (2025)
**Tags:** @defer, Deferrable, Lazy Loading

**References:** [Deferrable Views](https://angular.dev/guide/defer)

## Best Practices

- Use @defer with on viewport

```ts
@Component({
  template: `
    @defer (on viewport) {
      <heavy-chart />
    } @placeholder {
      <div>Loading...</div>
    }
  `
})
export class DashboardComponent {}
```

- Use @defer with on interaction

```ts
@Component({
  template: `
    <button (click)="showModal = true">Open</button>
    @defer (when showModal) {
      <modal-component />
    }
  `
})
export class MyComponent {}
```

- Use @defer with on hover

```ts
@Component({
  template: `
    @defer (on hover) {
      <tooltip />
    }
  `
})
export class TooltipWrapper {}
```
