---
name: angular-skills
description: Angular framework patterns, best practices, and enterprise patterns
category: stacks/frontend/angular
applies_to: angular
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Angular Skills

Platform for building mobile and desktop web applications.

## Sub-Skills

### Architecture
- [module-structure.md](architecture/module-structure.md) - Module organization
- [component-patterns.md](architecture/component-patterns.md) - Component design
- [service-patterns.md](architecture/service-patterns.md) - Service patterns
- [state-management.md](architecture/state-management.md) - NgRx patterns

### Components
- [smart-dumb.md](components/smart-dumb.md) - Smart/Dumb patterns
- [lifecycle-hooks.md](components/lifecycle-hooks.md) - Lifecycle hooks
- [change-detection.md](components/change-detection.md) - Change detection
- [content-projection.md](components/content-projection.md) - Content projection

### RxJS
- [observables.md](rxjs/observables.md) - Observable patterns
- [operators.md](rxjs/operators.md) - Operator patterns
- [subjects.md](rxjs/subjects.md) - Subject patterns
- [error-handling.md](rxjs/error-handling.md) - Error handling

### Forms
- [reactive-forms.md](forms/reactive-forms.md) - Reactive forms
- [template-forms.md](forms/template-forms.md) - Template forms
- [validation.md](forms/validation.md) - Form validation

### Performance
- [lazy-loading.md](performance/lazy-loading.md) - Lazy loading
- [change-detection.md](performance/change-detection.md) - OnPush strategy
- [trackby.md](performance/trackby.md) - TrackBy optimization

### Testing
- [unit-testing.md](testing/unit-testing.md) - Jasmine/Karma
- [component-testing.md](testing/component-testing.md) - Component tests
- [service-testing.md](testing/service-testing.md) - Service tests
- [e2e-testing.md](testing/e2e-testing.md) - E2E with Protractor

## Detection
Auto-detected when project contains:
- `angular.json` file
- `*.component.ts` files
- `@angular/core` package
