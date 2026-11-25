---
name: angular-control-flow
description: "ALWAYS use when working with Angular Control Flow syntax, @if, @for, @switch, @defer, or new template syntax in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Control Flow

**Version:** Angular 17+ (2025)
**Tags:** Control Flow, @if, @for, @switch, @defer

**References:** [Control Flow](https://angular.dev/guide/templates/control-flow) • [Deferrable Views](https://angular.dev/guide/defer)

## API Changes

This section documents recent version-specific API changes.

- NEW: @if replaces *ngIf — New control flow syntax

- NEW: @for replaces *ngFor — New loop syntax with track

- NEW: @switch replaces ngSwitch — New switch syntax

- NEW: @defer — Lazy load components

- DEPRECATED: *ngIf, *ngFor, *ngSwitch — Migrate to new syntax

## Best Practices

- Use @if for conditionals

```ts
@Component({
  template: `
    @if (isLoggedIn) {
      <p>Welcome!</p>
    } @else {
      <p>Please login</p>
    }
  `
})
export class MyComponent {
  isLoggedIn = signal(false);
}
```

- Use @else if

```ts
@Component({
  template: `
    @if (user.role === 'admin') {
      <p>Admin panel</p>
    } @else if (user.role === 'user') {
      <p>User dashboard</p>
    } @else {
      <p>Guest view</p>
    }
  `
})
export class MyComponent {}
```

- Use @for for loops

```ts
@Component({
  template: `
    @for (item of items; track item.id) {
      <li>{{ item.name }}</li>
    }
  `
})
export class MyComponent {
  items = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }];
}
```

- Use track for performance

```ts
@for (user of users; track user.id) {
  <li>{{ user.name }}</li>
}
```

- Use @empty for empty lists

```ts
@Component({
  template: `
    @for (item of items; track item.id) {
      {{ item.name }}
    } @empty {
      <p>No items found</p>
    }
  `
})
export class MyComponent {}
```

- Use @switch for conditionals

```ts
@Component({
  template: `
    @switch (status) {
      @case ('loading') {
        <p>Loading...</p>
      }
      @case ('success') {
        <p>Success!</p>
      }
      @case ('error') {
        <p>Error occurred</p>
      }
      @default {
        <p>Unknown status</p>
      }
    }
  `
})
export class MyComponent {
  status = 'loading';
}
```

- Use @defer for lazy loading

```ts
@Component({
  template: `
    @defer (on viewport) {
      <heavy-chart />
    } @placeholder {
      <div>Loading chart...</div>
    }
  `
})
export class DashboardComponent {}
```

- Use @defer with conditions

```ts
@Component({
  template: `
    @defer (on hover) {
      <tooltip />
    }
    
    @defer (when isReady) {
      <ready-component />
    }
  `
})
export class MyComponent {}
```

- Migrate from *ngIf

```bash
ng generate @angular/core:control-flow
```

- Use else with @if

```ts
@if (condition) {
  content
} @else {
  alternative
}
```
