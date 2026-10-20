# Front — Frontend de la Academia

SPA Angular 18 con PrimeNG + NgRx.

**Repo:** `https://github.com/Academia-FireMD/Front`

## Comandos principales

```bash
pnpm start              # ng serve → http://localhost:4200
pnpm build              # Build de produccion
pnpm test               # Tests unitarios (Jest)
pnpm test:ci            # Tests CI con coverage
pnpm e2e                # Playwright E2E completo
pnpm e2e:ui             # Playwright con UI interactiva
pnpm e2e:smoke          # Smoke tests
pnpm test:all           # Unitarios + E2E
```

## Stack

- **Angular 18.1** con standalone components
- **TypeScript 5.5**
- **PrimeNG 17.18** como libreria de UI
- **NgRx 18.1** para state management (store + effects)
- **SCSS** para estilos
- **Jest** para tests unitarios
- **Playwright** para E2E
- **ngx-echarts / chart.js** para graficas
- **toast-ui/editor** para edicion markdown
- **angular-calendar** para calendario

## Arquitectura

La app usa standalone components (sin NgModules). Lazy loading por rutas de feature.

```
src/app/
├── login/              # Autenticacion (local + WordPress redirect)
├── test-de-preguntas/  # Tests y banco de preguntas
├── flashcard/          # Flashcards
├── planificacion/      # Planificacion mensual/semanal
├── examenes/           # Simulacros y examenes
├── perfil/             # Perfil de usuario
├── admin/              # Panel de administracion
├── shared/             # Componentes compartidos
└── store/              # NgRx store, actions, reducers, effects
```

## Convenciones Angular

- **Standalone components**: NO poner `standalone: true` en el decorador (es default desde Angular 19+, pero ya lo usamos asi)
- **Signals** para estado local del componente
- **`input()`/`output()`** en vez de decoradores `@Input`/`@Output`
- **`computed()`** para estado derivado
- **`inject()`** en vez de inyeccion por constructor
- **`ChangeDetectionStrategy.OnPush`** en todos los componentes
- **Control flow nativo**: `@if`, `@for`, `@switch` (NO `*ngIf`, `*ngFor`)
- **Reactive forms** sobre template-driven
- **`class` bindings** en vez de `ngClass`; **`style` bindings** en vez de `ngStyle`
- NO usar `@HostBinding`/`@HostListener` → usar `host` en el decorador
- Logica en el `.ts`, estilos en el `.scss`, template en el `.html` (archivos separados)

## UI/UX

- Usar la paleta de colores definida en variables CSS/SCSS
- Look & feel nativo, consistente con PrimeNG
- Componentes reutilizables siempre que sea posible
- `NgOptimizedImage` para imagenes estaticas

## WordPress

- Login: si WP auth esta habilitado, intenta primero contra WP y luego local
- Recuperar contrasena: detecta si el usuario es `WORDPRESS` y redirige a WP
- Los datos de `authSource` vienen del backend

## Norma: reutilizar antes de crear

Antes de crear cualquier componente, directiva, pipe o service nuevo, audita el repo:

1. `grep -rn "selector.*'app-X'" src/app/shared/` — ¿existe ya algo similar?
2. Inspecciona modulos analogos al tuyo (examen, planificacion, test-de-preguntas).
3. Si existe → reusa. Si va a usarse en >1 lugar → ponlo en `src/app/shared/`. Si es ad-hoc → vive en modulo local pero respetando patrones:
   - `SharedGridComponent` para listas paginadas admin.
   - `<app-async-button>` para acciones con loading state.
   - `<p-confirmDialog>` para confirmaciones destructivas (NO `confirm()` nativo del navegador).
   - `<p-dialog>` para modales (NO modales custom).
   - `<app-tema-select>` para selectores de tema (acepta input `[oposicion]` para filtrar).
   - `<app-woocommerce-product-picker>` para dropdowns de productos WC (ControlValueAccessor).
4. Si vas a romper esta regla, justifica en code review con motivo concreto.
