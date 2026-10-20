---
name: angular-signals-state
description: Estado con signals en Angular — `signal`/`computed`/`effect` (y cuándo NO usar `effect`), `linkedSignal`, `resource`/`httpResource`/`rxResource` y su estabilidad, interop con RxJS (`toSignal`/`toObservable`), niveles de estado (local, feature, global, URL), stores con signals, estado de servidor vs cliente e inmutabilidad. Usar al decidir dónde vive un dato, al traer datos async a una vista, al escribir un store, o cuando un `effect` setea otro signal.
---

# Estado con signals

Regla base: **una sola fuente de verdad por dato, todo lo demás se deriva**. Si podés
calcularlo, no lo guardes. Verificá cada API contra angular.dev en la versión instalada:
varias de esta skill cambiaron de estabilidad entre versiones.

## 1. Primitivas

| Primitiva | Para qué | Regla |
|---|---|---|
| `signal(v)` | Estado escribible | Privado en el dueño; hacia afuera `asReadonly()` |
| `computed(fn)` | Estado derivado | Puro: sin efectos, sin escribir signals, sin async |
| `linkedSignal(fn)` | Derivado que el usuario puede pisar y que se resetea cuando cambia la fuente | Selección por defecto, página actual al cambiar un filtro |
| `effect(fn)` | Sincronizar con algo que **no es** un signal | Último recurso (§2) |

```ts
readonly options = input.required<ShippingMethod[]>();
// se reinicia al primer ítem cada vez que cambian las opciones; el usuario puede pisarlo
readonly selected = linkedSignal(() => this.options()[0]);
```

## 2. `effect`: cuándo sí y cuándo no

Sí: escribir en `localStorage`, loguear/analítica, sincronizar con una librería de DOM
imperativa (mapa, gráfico), llamar una API no reactiva.

No:
- Copiar o transformar un signal en otro → `computed`.
- "Cuando cambia A, reseteá B" → `linkedSignal`.
- Traer datos cuando cambia un parámetro → `resource`/`httpResource` (§3).
- Lógica de negocio. Un effect corre cuando Angular decide, no cuando vos querés.

```ts
// ❌ estado derivado mantenido a mano: se desincroniza y dispara renders extra
effect(() => this.total.set(this.items().reduce((s, i) => s + i.price, 0)));
// ✅
readonly total = computed(() => this.items().reduce((s, i) => s + i.price, 0));
```

Dentro de un effect, leé con `untracked()` lo que no debe re-dispararlo. Un effect se
crea en contexto de inyección y se destruye con su dueño; si toca APIs de navegador,
ojo con SSR (`angular-ssr-hydration`).

## 3. Datos asíncronos: `resource`, `httpResource`, `rxResource`

Estabilidad: en Angular v21 `resource` figura como **experimental** en la doc oficial
("might change before it is stable"). Verificá el estado de `resource`, `httpResource` y
`rxResource` en la versión instalada antes de adoptarlos de forma transversal, y
encapsulalos detrás de la capa de datos del proyecto (`frontend-data-access`) para que
un cambio de API se absorba en un solo lugar.

```ts
readonly patientId = input.required<string>();

readonly patient = resource({
  params: () => ({ id: this.patientId() }),
  loader: ({ params, abortSignal }) => this.api.getPatient(params.id, abortSignal),
});
```

- `params` es reactivo: cuando cambia, el loader vuelve a correr y el pedido anterior se
  aborta vía `abortSignal` — propagalo al `fetch`/cliente.
- `params` que devuelve `undefined` deja el recurso en `idle` (no hay pedido).
- Estado expuesto como signals: `value`, `hasValue()`, `error`, `isLoading`, `status`
  (`'idle' | 'loading' | 'reloading' | 'resolved' | 'error' | 'local'`), más `reload()`.
- Leé `value()` detrás de `hasValue()`: es type guard y evita la lectura que lanza
  cuando el recurso está en error.
- `value.set()/update()` deja el recurso en `'local'`: sirve para UI optimista
  (`frontend-ux-states`).
- `httpResource(() => url)` hace GET por `HttpClient` (pasa por interceptors) y es solo
  para **lecturas**. Las mutaciones (POST/PUT/DELETE) son llamadas explícitas.
- `rxResource({ params, stream })` cuando la fuente ya es un Observable.

| `status` | Tratamiento en la vista |
|---|---|
| `loading` | skeleton |
| `reloading` | contenido previo + indicador discreto |
| `error` | mensaje + reintentar (`reload()`) |
| `resolved` con lista vacía | estado vacío |

## 4. Interop con RxJS

- `toSignal(obs$, { initialValue })`: se suscribe una sola vez y se desuscribe con el
  contexto. Creala como campo, nunca dentro de un `computed`, un template o un método
  que se llama repetido. Sin `initialValue` el tipo incluye `undefined`; `requireSync`
  solo para fuentes que emiten al suscribirse. Si el Observable falla, el signal lanza.
- `toObservable(sig)`: requiere contexto de inyección. Útil para `debounceTime`,
  `switchMap` y otros operadores de tiempo que los signals no tienen.
- Signals para **estado**; RxJS para **eventos en el tiempo** (debounce, websockets,
  reintentos con backoff). No reescribas streams complejos con effects.
- Suscripción manual inevitable → `takeUntilDestroyed()`.

## 5. Dónde vive cada dato

| Nivel | Ejemplos | Dónde |
|---|---|---|
| Local de UI | abierto/cerrado, tab activo, borrador de un input | `signal` en el componente |
| De feature | filtros + resultados de una pantalla, wizard de varios pasos | servicio provisto en la ruta de la feature |
| Global de cliente | sesión, tenant activo, tema, idioma | servicio `providedIn: 'root'` |
| Del servidor | entidades que viven en la API | `resource` o capa de datos; **no** copiar a un store global "por las dudas" |
| De la URL | página, orden, filtros compartibles, id seleccionado | query/route params: la URL es la fuente de verdad |

Subí de nivel solo cuando dos consumidores reales lo necesitan. El estado de servidor es
un caché con fecha de vencimiento: definí cuándo se invalida (tras una mutación, al
volver a la vista), no lo trates como verdad local.

## 6. Store con signals

```ts
@Injectable()
export class AppointmentFiltersStore {
  private readonly state = signal<Filters>({ status: null, from: null, cursor: null });

  readonly filters = this.state.asReadonly();
  readonly hasActiveFilters = computed(() => this.state().status !== null || this.state().from !== null);

  setStatus(status: StatusId | null): void {
    this.state.update((s) => ({ ...s, status, cursor: null }));   // reset del cursor al filtrar
  }
}
```

- Signals privados y escribibles; hacia afuera `asReadonly()` + `computed`. Los
  consumidores cambian estado **solo** por métodos con nombre de intención.
- Un store no conoce componentes ni el router. Sin lógica de presentación adentro.
- Antes de sumar una librería de estado, verificá si el proyecto ya eligió una.

## 7. Inmutabilidad

Un signal notifica cuando cambia la **referencia**. Mutar en el lugar no dispara nada.

```ts
this.items().push(item);                          // ❌ misma referencia: la vista no se entera
this.items.update((list) => [...list, item]);     // ✅
```

Objetos y arrays siempre por copia (`{ ...s }`, `[...l]`, `map`, `filter`). Tipá el
estado como `readonly` para que el compilador lo imponga (`typescript-standards`).

## 8. Anti-patrones

- El mismo dato en dos signals sincronizados a mano.
- `effect` que hace `set()` de otro signal; cadenas de effects.
- Store global con todo "por si acaso"; copiar la respuesta de la API a un store y no
  invalidarla nunca.
- `toSignal()` llamado en cada ejecución de un método o `computed`.
- Exponer el `WritableSignal` para que cualquiera escriba.
- Filtros o paginación en memoria cuando deberían estar en la URL.
- Async dentro de `computed`.

## Checklist

- [ ] Cada dato tiene una única fuente de verdad; lo derivable está en `computed`.
- [ ] Ningún `effect` escribe signals ni contiene lógica de negocio.
- [ ] Datos async con estados `loading`/`error`/vacío resueltos en la vista.
- [ ] Verificado el estado (experimental/estable) de `resource`/`httpResource` en la versión instalada.
- [ ] `abortSignal` propagado; mutaciones fuera de `httpResource`.
- [ ] `toSignal` creado una sola vez, con `initialValue` cuando corresponde.
- [ ] Estado en el nivel más bajo que alcanza; lo compartible por link, en la URL.
- [ ] Updates inmutables; signals escribibles no expuestos.
