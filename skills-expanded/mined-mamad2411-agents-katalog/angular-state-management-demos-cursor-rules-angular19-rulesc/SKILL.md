---
description: Fora anything related to angular
globs: 
alwaysApply: false
---
# Angular 19 Development Rules

## Component Development

### Imports and Setup

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  // ...
})
export class ExampleComponent {
  // Component logic
}
```

### Input/Output Declarations

Always use the new input syntax:

```typescript
// ✅ DO
readonly input = input<string>();
readonly inputRequired = input.required<string>();
readonly model = model<string>();
readonly output = output<string>();

// ❌ DON'T
@Input() value: string;
@Output() valueChange = new EventEmitter<string>();
```

### Dependency Injection

Always use the `inject()` function instead of constructor injection:

```typescript
// ✅ DO
export class ExampleComponent {
  private service = inject(ExampleService);
}

// ❌ DON'T
export class ExampleComponent {
  constructor(private service: ExampleService) {}
}
```

### Providers

Always use the `providers` field in the component decorator for dependency injection:

```typescript
@Component({
  // ...
  providers: [
    ExampleService,
    {
      provide: EXAMPLE_TOKEN,
      useValue: configValue
    }
  ]
})
```

### Signals

Use signals for reactive state management:

```typescript
// State declaration
readonly count = signal(0);
readonly doubled = computed(() => this.count() * 2);

// State updates
onIncrement() {
  this.count.update(count => count + 1);
}
```

### Component Structure

Follow this order in component files:

1. Imports
2. Component decorator
3. Injected dependencies
4. Input/Output declarations
5. Signals and state
6. Lifecycle hooks
7. Public methods
8. Protected methods
9. Private methods

### Template Syntax

Use modern template syntax:

```html
<!-- Use @if instead of *ngIf -->
@if (condition()) {
<div>Content</div>
} @else {
<div>Alternative</div>
}

<!-- Use @for instead of *ngFor -->
@for (item of items(); track item.id) {
<div>{{ item.name }}</div>
}
```

## Best Practices

1. Always make components standalone
2. Use signals for state management
3. Prefer functional updates for signal mutations
4. Use computed signals for derived state
5. Implement OnDestroy for cleanup when necessary
6. Use effect() for side effects
7. Use defer blocks for lazy loading
8. Use input() and output() instead of decorators
9. Use inject() instead of constructor injection
10. Use providers in component decorator
