---
name: angular21
description: Angular 21 coding standards and best practices for any Angular application — new or existing. Covers standalone components, dependency injection with inject(), OnPush change detection, RxJS reactive patterns, signals, routing, reactive forms, Jest testing, naming conventions, and i18n with Transloco. Use this skill whenever working on Angular TypeScript or HTML files, whether creating a new app from scratch, adding features to an existing one, or reviewing Angular code. Also carries MIND CTI company-specific conventions for the MindBill Angular frontends.
paths: "**/*.ts,**/*.html"
---

# Angular 21 — Coding Standards

> General Angular 21 best practices, with MIND CTI company-specific conventions noted where applicable.

## When This Applies

This skill applies to **any Angular application** — both new projects and existing ones. It targets **Angular 21** but the principles apply from Angular 17+ (standalone, signals, `takeUntilDestroyed()`).

MIND CTI currently runs four Angular 21 frontends where this skill is specifically calibrated:
- **MindBill-DrawerManagement-Frontend** (21.2.5) — standalone, Transloco
- **MindBill-DRS-Frontend** (21.2.1) — NgModule, ngx-translate
- **MindBill-Orders-Frontend** (^21.1.2) — NgModule, ngx-translate
- **MindBill-POS-Frontend** (21.1.3) — standalone, Transloco, partial signals

## Core Principles

1. **Standalone-first** — New components, pipes, and directives are standalone. Existing NgModule-based apps migrate incrementally.
2. **`inject()` over constructor injection** — Use the `inject()` function in the class body; never use constructor parameter injection in Angular code.
3. **OnPush everywhere** — Use `ChangeDetectionStrategy.OnPush` on every component. This is the default for new code.
4. **Unsubscribe with `takeUntilDestroyed()`** — Never leave subscriptions dangling; use the `takeUntilDestroyed()` operator.
5. **RxJS for async; signals for local state** — RxJS `Observable`s for HTTP and event streams; Angular signals for local component/service state.
6. **Adapter pattern for API mapping** — Never bind raw JSON to view models. Use `*Adapter` classes/services to map API responses to typed view models.
7. **BL services for business logic** — Components coordinate; `*BlService` services hold complex business rules.

## Quick Reference — Top 15 Rules

1. **`inject()` in class body** — `private http = inject(HttpClient)` — never `constructor(private http: HttpClient)`.
2. **Standalone components** — New components always have `standalone: true` (implicit in Angular 19+) and a self-contained `imports` array.
3. **`ChangeDetectionStrategy.OnPush`** — Required on every component. Use `cdr.detectChanges()` only when imperative updates are needed.
4. **`takeUntilDestroyed()`** — Pipe all subscriptions through `takeUntilDestroyed()` (or `takeUntilDestroyed(this.destroyRef)` in ngOnInit/lifecycle hooks).
5. **`@Injectable({ providedIn: 'root' })`** — Default scope for all services. Use component-level providers only when truly needed.
6. **Adapter pattern** — `SomeAdapter` or `SomeAdapterService` maps raw API JSON → typed model. Keep adapters `providedIn: 'root'` and `@Injectable`.
7. **BL service naming** — Business logic lives in `*-bl.service.ts` files, separate from HTTP services.
8. **Signal-based inputs** — New components use `input()` and `output()` signals, not `@Input()`/`@Output()` decorators.
9. **No subscriptions in templates** — Prefer `async` pipe or `toSignal()` over subscribing inside `ngOnInit`.
10. **Reactive Forms** — Use `ReactiveFormsModule` for all forms. Template-driven forms only for trivial single-field cases.
11. **`async` pipe or `toSignal()`** — Bind observables to templates via `| async` or convert with `toSignal()` — never subscribe just to set a component property.
12. **Jest for testing** — All tests use Jest + `jest-preset-angular`. No Karma/Jasmine.
13. **`@ngneat/spectator`** — Use `createComponentFactory` / `createServiceFactory` for test setup.
14. **ESLint + Prettier** — All `.ts` and `.html` files must pass `ng lint` and `prettier --check`.
15. **`provideHttpClient(withInterceptorsFromDi())`** — Register interceptors via DI providers, not the deprecated `HTTP_INTERCEPTORS` token directly.

## Detailed Reference

- Component design, selectors, change detection, lifecycle hooks → [component-architecture.md](docs/component-architecture.md)
- `inject()`, service scoping, BL pattern, adapter pattern → [services-and-di.md](docs/services-and-di.md)
- Observable patterns, operators, subscription cleanup → [rxjs-patterns.md](docs/rxjs-patterns.md)
- Routing, guards, lazy loading, standalone routes → [routing.md](docs/routing.md)
- Reactive forms, validation, form state → [forms.md](docs/forms.md)
- Jest, spectator, component and service tests → [testing.md](docs/testing.md)
- File naming, selector naming, variable naming → [naming-conventions.md](docs/naming-conventions.md)
- Transloco setup, template/TypeScript usage, key conventions → [i18n.md](docs/i18n.md)

## General Angular Notes

- **Never hardcode API base URLs** — load them from environment configuration or an `AppConfigService` initialized via `APP_INITIALIZER`.
- **HTTP interceptors** — Register via `provideHttpClient(withInterceptorsFromDi())` + DI providers. Keep interceptors in a `providers/` or `interceptors/` directory.
- **TypeScript strict mode** — Always enable `strict: true` in `tsconfig.json`. Avoid `any` — use `unknown` + type guards at API boundaries.
- **Node/npm engines** — Pin compatible Node/npm versions in `package.json` under `"engines"`.
- **New control flow syntax** — Prefer `@if`, `@for`, `@switch` over `*ngIf`, `*ngFor`, `*ngSwitch` in new code.

## MIND CTI Specific Notes

These conventions apply specifically to MIND CTI MindBill Angular projects. For general Angular projects, adapt to your own project's conventions.

- **App selector prefixes**: Each MindBill app uses its own prefix — `dm-` (DrawerManagement), `pos-` (POS), `drs-` (DRS), `ord-` (Orders). The root component is always `app-root`.
- **Adapter pattern**: Hand-written `*Adapter` / `*AdapterService` classes. Do not introduce mapping libraries.
- **BL services**: Multi-step workflows (approval chains, close-of-day flows) live in `*-bl.service.ts`, separate from HTTP data services.
- **i18n**: DrawerManagement and POS use Transloco. DRS and Orders use ngx-translate — keep the library that is already there. Transloco is the standard for new projects.
- **Bootstrap 5 + ng-bootstrap**: Primary UI stack. Do not mix with Angular Material.
- **Logging**: Use the project's `LogService` wrapper (`LogService.getInstance('ClassName')`). Do not call `console.log` directly in production code.
- **Testing stack**: Jest + jest-preset-angular + @ngneat/spectator. Tests run serially (`--runInBand`).
