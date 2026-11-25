# Algotiqa GUI — OpenCode instructions

## Quick start

```bash
npm install
npm start              # ng serve --host algotiqa-server --port 8444
npm run build          # ng build → dist/gui/   (default config: production)
npm run watch          # ng build --watch --configuration development
npm test               # ng test  (Karma + Jasmine + ChromeHeadless)
```

- The dev server binds **`algotiqa-server:8444`** (not `localhost:4200`). `README.md` is the unmodified Angular CLI template and is stale — trust `package.json`/`angular.json`.
- No `lint`/`typecheck` scripts and no CI workflow exist. The closest thing to typechecking is `ng build` (strict templates are on).

## Architecture

- **Angular 21**, standalone components, **`bootstrapApplication`** in `src/main.ts` (no `AppModule`).
- `src/routes.ts` — flat route table; URL constants in `src/app/model/urls.ts`.
- **Named `right` router outlet**: create/edit/view panels render in `outlet: 'right'` (see `routes.ts` and `AbstractPanel.openRightPanel()`). Add new edit panels there, not to the primary outlet.
- **Layout**: `src/app/layout/header-panel` and `src/app/layout/main-panel` (which contains `left-panel`, `right-panel`, `work-panel`). Feature panels nest under `work-panel/{admin,inventory,portfolio,tool,home,unknown}` and `src/app/module/{doc-editor,performance-metrics,quality-analyzer,simulator,trade-analyzer}` (routed under `Url.Module_*`).
- **OIDC auth** via `angular-auth-oidc-client`; config in `src/authentication.ts` — Keycloak authority `https://algotiqa-server:8443/auth/realms/algotiqa`, clientId `algotiqa-frontend`, `secureRoutes: 'https://algotiqa-server:8443/'`.
- **Localization**: `src/assets/lang/application-{en,it}.yaml` loaded by `LabelService`.
- **Global scripts/styles** (declared in `angular.json`, not imported): `apexcharts`, `jquery`, `trumbowyg` (+ its CSS). `ng-apexcharts`/`trumbowyg` rely on these globals.
- ~18 services registered in `main.ts`; `src/app/service/abstract-subscriber.ts` is the base class (not itself a service).

## Conventions

- 2-space indent, single quotes in TS (`.editorconfig`); SCSS for component styles (configured via `angular.json` schematics).
- **ELv2 license header** on every source file — preserve it on new files (copy the header block from any existing `.ts`).
- Panels extend `AbstractPanel` (`src/app/component/abstract.panel.ts`): it calls `this.init()` from `ngOnInit` and `this.destroy()`/`this.viewInit()` hooks. Localization helpers on it: `loc()`, `mod()`, `button()`, `menu()`, `map()`, `labelMap()` — all take YAML keys prefixed by `page.<pageCode>.*`, `model.*`, `button.*`, `menu-button.*`, `map.*`.
- tsconfig is **strict**: `strict`, `strictTemplates`, `noPropertyAccessFromIndexSignature`, `noImplicitReturns`. Index-signature access needs bracket notation; templates must be type-correct.
- Icons: `<mat-icon>` uses the **Material Icons** font (default). Some templates use Material Symbols via `<span class="material-symbols-outlined">`. **Both** fonts are loaded in `src/index.html` — do not remove either.

## Reusable components

- **Buttons** (`src/app/component/button/`, 15 of them: back, chart, connect, create, data, delete, disconnect, edit, optimize, playground, reload, run, save, upload, view) — each wraps `<flat-button>` with icon+label. Bind `(click)` on the custom element (native event bubbling): `<create-button (click)="onCreateClick()" [disabled]="disCreate"></create-button>`.
- **Form controls** (`src/app/component/form/`): `select-required`, `select-optional`, `input-number`, `input-text-required`/`-optional`, `date-picker`, `time-picker`, `*-selector` (broker/data/instrument/preset/root/period/timeframe), `file-uploader`, `confirmation-dialog`, `chip-text-set`, `check-button`, `toggle-button`, `flag`, `round-box`, plus `flat-button` and `error-state-matcher`/`drag-n-drop.directive`.
- **List/table panels** (`src/app/component/panel/`): `list-panel` (with `<list-panel>`/`<list-buttons>`/`<list-left>`/`<list-content>` slots), `flex-table` (sort/filter/selection), `simple-table` (read-only).

## Known bugs & gotchas

- **`app.component.spec.ts` is broken**: it uses `declarations: [AppComponent]`, but `AppComponent` is standalone — should be `imports: [AppComponent]`. It is the only spec file. Expect `npm test` to fail on it.
- **`select-required` binding-order issue**: Angular binds `[key]` before `[list]`/`[map]`, so the `set key()` setter calls `formControl.setValue()` before options exist — an initial value may not render. The setter currently does **not** defer to `ngOnInit` (there is no deferral). If you touch this component, be aware options may not be populated when `key` is set.
- **`@HostBinding('style.pointer-events')` hack** is on `flat-button` **and all 15 button wrappers** (sets `pointer-events: none` on the host when `disabled`). Prefer native `<button disabled>` for new components rather than replicating the hack.
- **ViewEncapsulation is Emulated** (default): a component's SCSS cannot reach into Angular Material internals — use `:host ::ng-deep` for those overrides.
- **Custom-element components** (`<list-content>`, `<flex-table>`, `<list-buttons>`, …) are `display: inline` by default; without an explicit `:host { display: flex|block }` they break the flex layout chain (height constraints and scrollbars won't propagate).
- **`SidebarMenuModule`** (`src/app/component/sidebar-menu/sidebar.module.ts`) is the **only `@NgModule`** in the repo; its 4 declared components (`SidebarMenuComponent`, `AnchorComponent`, `ItemComponent`, `NodeComponent`) are `standalone: false`. Everything else is standalone.

## Tests

- Single spec: `src/app/layout/app.component.spec.ts` (broken — see above).
- Test builder is `@angular/build:karma` (esbuild-based). No `karma.conf.js` — config is implicit via the Angular CLI; browser defaults to ChromeHeadless.
- Run a focused spec with: `npx ng test --include='**/app.component.spec.ts'` (single run: add `--watch=false`).
