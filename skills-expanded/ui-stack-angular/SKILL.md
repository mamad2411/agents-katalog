---
name: ui-stack-angular
description: "Building interfaces in Angular: standalone components, signals and computed state, the built-in control flow, OnPush change detection, inject, typed reactive forms, the router with lazy routes and guards, HttpClient with interceptors, Angular CDK and Material, SSR with hydration, and testing. Read when the project uses Angular."
---

# Angular

Angular written from old tutorials still looks like 2019: NgModules,
`*ngIf` and `*ngFor`, constructor injection, objects mutated in place,
subscriptions nobody closes, a `BehaviorSubject` store per screen, and
Material in its default violet with Roboto. Current Angular is standalone
components, signals and the built-in control flow. This covers Angular 20
to 22 (22 is current in 2026): keep to what the project's version has.

## 1. Files

- Folders by feature (`features/orders/` with its routes, pages, parts and
  API service), `core/` for interceptors, guards and the shell,
  `shared/ui/` for parts built on the component library. Each feature is
  lazy-loaded and imports no other feature's internals.
- `ng new` in v22 is standalone, zoneless and tested with Vitest. Names
  follow the v20 style guide (`orders-page.ts` holds `OrdersPage`, no
  `.component` suffix); an older project keeps its own.

## 2. Components and templates

```ts
import { Component, inject, input } from "@angular/core";
import { httpResource } from "@angular/common/http";
import { RouterLink } from "@angular/router";
import { OrdersApi, type Order } from "./orders-api";

@Component({
  selector: "app-orders-page",
  imports: [RouterLink],
  template: `
    @if (orders.error()) {
      <p role="alert">Orders could not load. <button type="button" (click)="orders.reload()">Try again</button></p>
    } @else if (orders.hasValue()) {
      <ul>
        @for (order of orders.value(); track order.id) {
          <li><a [routerLink]="['/orders', order.id]">{{ order.number }}</a>
            <button type="button" (click)="api.remind(order.id)">Send reminder</button></li>
        } @empty { <li>No orders with this status.</li> }
      </ul>
    } @else { <p>Loading orders…</p> }
  `,
})
export class OrdersPage {
  readonly status = input<string>(); // ?status=, bound by withComponentInputBinding()
  protected readonly api = inject(OrdersApi);
  protected readonly orders = httpResource<Order[]>(() => `/api/orders?status=${this.status() ?? "open"}`);
}
```

- Standalone only (the default since v19), each listing its template's
  needs in `imports`; `input()`, `input.required()`, `output()`, `model()`,
  `viewChild()`; host bindings in the `host` object; template-only members
  `protected`; derived values `computed`, never template function calls.
- `@if`, `@for` with `track` (a stable id; `$index` only for a list that
  never changes) and `@empty`, `@switch`, `@let`. `*ngIf` and `*ngFor` are
  deprecated since v20 (`ng generate @angular/core:control-flow`).
- `@defer (on viewport)` for heavy parts below the fold, with a
  `@placeholder` (one element: it is what is observed) and `@loading
  (after 100ms; minimum 500ms)` so nothing flickers.

## 3. Signals, change detection, injection

- `signal` for state, `computed` for what follows, `linkedSignal` for
  state that resets with its source (the selected row when the list
  reloads); `effect` only to reach outside Angular (storage, a chart),
  never to copy one signal into another. Update immutably
  (`items.update((list) => [...list, item])`).
- OnPush everywhere: the default from v22 (`ChangeDetectionStrategy.Eager`,
  formerly `Default`, opts out); up to v21, set `changeDetection:
  ChangeDetectionStrategy.OnPush` on every component. New apps are
  zoneless since v21, so whatever the view shows lives in signals.
- `inject()` in field initialisers; `@Service()` (v22) for an app-wide
  singleton (`@Injectable({ providedIn: "root" })` before); shared state in
  a service of signals; RxJS only where streams help (`toSignal()`,
  `takeUntilDestroyed()`).

## 4. Data: resources and interceptors

- `httpResource(() => url)` refetches when a signal in the URL changes:
  `value()`, `isLoading()`, `error()`, `hasValue()`, `reload()`;
  `resource()` wraps a promise, `rxResource()` an Observable. Stable in v22
  (experimental from 19.2 to 21). Mutations are service methods returning
  a promise (`firstValueFrom(http.post(...))`), then `reload()`.
- `provideHttpClient(withInterceptors([sessionInterceptor]))` (fetch is
  the v22 default, no `withFetch()`); this one sends a 401 to sign-in:

```ts
export const sessionInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  return next(req).pipe(catchError((error: unknown) => {
    if (error instanceof HttpErrorResponse && error.status === 401) {
      router.navigate(["/sign-in"], { queryParams: { returnUrl: router.url } });
    }
    return throwError(() => error);
  }));
};
```

## 5. Forms

Signal Forms are stable in v22: use them for new forms. Typed reactive forms
stay right in older versions and existing code (`frontend-forms`).

```ts
import { email, form, FormField, required, submit } from "@angular/forms/signals";
@Component({
  selector: "app-booking-form",
  imports: [FormField],
  template: `
    <form (submit)="send($event)" novalidate>
      @let emailError = booking.email().touched() && booking.email().invalid();
      <label for="email">Email</label>
      <input id="email" type="email" autocomplete="email" [formField]="booking.email"
             [attr.aria-invalid]="emailError" [attr.aria-describedby]="emailError ? 'email-error' : null" />
      @if (emailError) { <p id="email-error">{{ booking.email().errors()[0].message }}</p> }
      <button type="submit" [disabled]="booking().submitting()">Book appointment</button>
    </form>
  `,
})
export class BookingForm {
  private readonly api = inject(BookingApi);
  protected readonly model = signal({ email: "", date: "" });
  protected readonly booking = form(this.model, (path) => {
    required(path.email, { message: "Enter your email address." });
    email(path.email, { message: "Enter an email address like name@example.com." });
  });
  protected async send(event: Event) {
    event.preventDefault();
    await submit(this.booking, {
      action: () => this.api.book(this.model()),
      onInvalid: (f) => f().errorSummary()[0]?.fieldTree().focusBoundControl(),
    });
  }
}
```

`[formField]` binds a native input (value, `required`, `disabled`, touched
on blur); rules sit in the schema (`minLength`, `pattern`, `validate`,
`validateHttp`). `submit()` marks every field touched, runs the action only
when valid and puts the errors it returns on their fields. The reactive
equivalent: `inject(NonNullableFormBuilder).group({ email: ["",
[Validators.required, Validators.email]] })`, `formControlName` on each
input, `markAllAsTouched()` and focus on the first error when invalid.

## 6. The router

- Lazy routes (`loadComponent: () => import("./orders-page").then((m) =>
  m.OrdersPage)`), each with a `title`, a `**` route for not found; guards
  are functions returning `true` or a `UrlTree` (`inject(Router)
  .createUrlTree(["/sign-in"], { queryParams: { returnUrl: state.url } })`).
- `provideRouter(routes, withComponentInputBinding(), withInMemoryScrolling(
  { scrollPositionRestoration: "enabled" }))`. A missing parameter sets its
  input to `undefined`, so defaults live in code (`?? "open"`).
  `withViewTransitions()` (developer preview) keeps its animations inside
  `@media (prefers-reduced-motion: no-preference)`.
- After a navigation, focus moves to the new page's `h1` (a small service
  on `NavigationEnd`); Angular does not do it (`frontend-accessibility`).

## 7. CDK, Aria and Material

- Angular Aria (`@angular/aria`, stable in v22): headless accordion,
  combobox, grid, listbox, menu, tabs, toolbar and tree, styled with your
  tokens. The CDK adds `cdkTrapFocus`, `LiveAnnouncer`, overlays, virtual
  scroll, and drag and drop (with keyboard buttons alongside).
- Material themed from the project's tokens, never its default violet and
  Roboto (`ui-themes`): palettes from the brand colour with
  `ng generate @angular/material:theme-color`, then:

```scss
@use "@angular/material" as mat;
@use "./styles/theme-colors" as brand;
html {
  color-scheme: light dark; /* the system tokens use light-dark() */
  @include mat.theme((
    color: (primary: brand.$primary-palette, tertiary: brand.$tertiary-palette),
    typography: (plain-family: "Plus Jakarta Sans", brand-family: "Fraunces"),
    density: -1,
  ));
}
```

- Your CSS reads `--mat-sys-*` variables; component tweaks go through the
  `*-overrides` mixins, never deep selectors. Spartan is the unstyled option.

## 8. Server rendering and speed

- `ng add @angular/ssr`; `app.routes.server.ts` sets a `RenderMode` per
  route (`Prerender` for public pages, `Server` per request, `Client` for
  the signed-in app); `provideClientHydration(withEventReplay())`, with
  incremental hydration on by default in v22 (`@defer (hydrate on
  viewport)`). Browser-only code (`window`, storage, a chart) runs in
  `afterNextRender()`, or the server render fails.
- `NgOptimizedImage` (`priority` on the largest first-screen image);
  `angular.json` budgets; `@angular/localize` or Transloco (`i18n`).

## Check it

- `ng build` fails on template type errors and over-budget bundles (read
  the lazy chunks); `ng lint` after `ng add angular-eslint`, template
  accessibility rules on; `ng test` (Vitest, or Karma when older). With
  Testing Library: `render(BookingForm, { providers: [provideHttpClient(),
  provideHttpClientTesting()] })`, `userEvent.click(screen.getByRole(
  "button", { name: "Book appointment" }))`, `await screen.findByText(...)`.
- Playwright for journeys; `preview` with `url` `http://localhost:4200/`
  and `start` `npm start -- --port 4200`; then `ui_check`.

## Avoid

NgModules, `*ngIf` and constructor injection in new code; `subscribe` in
components that only render; objects mutated in place; `effect` copying
signals; functions called in templates; `$index` tracking a changing list;
`window` touched during server rendering; Material's default theme; drag
and drop with no keyboard way; a guard that navigates instead of returning
a `UrlTree`; the whole app in one bundle.
