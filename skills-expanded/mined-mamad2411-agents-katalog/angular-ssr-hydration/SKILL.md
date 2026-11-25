---
name: angular-ssr-hydration
description: Gate de SSR e hidratación en Angular — código compatible con servidor (nada de `window`/`document`/`localStorage` fuera de `afterNextRender`), hydration e incremental hydration con `@defer`, transfer cache de HTTP, modo de render por ruta (`RenderMode`) y cero datos sensibles en el HTML servido. Usar al crear un componente o servicio que toque APIs de navegador, al integrar una librería de DOM, al configurar rutas del servidor, o ante un hydration mismatch o un parpadeo al cargar.
---

# Angular SSR e hidratación

Todo componente de la casa se renderiza primero en Node y después se hidrata en el
navegador. El mismo código corre en dos entornos: escribilo para los dos. Verificá cada
API en angular.dev contra la versión instalada — varios defaults de SSR cambiaron entre
versiones.

## 1. Código compatible con servidor

En el servidor no existen `window`, `document`, `navigator`, `location`, `localStorage`,
`matchMedia`, `IntersectionObserver` ni medidas de layout.

| Necesitás | Usá |
|---|---|
| Leer/escribir DOM o inicializar una librería de navegador una vez | `afterNextRender` |
| Hacerlo después de cada render | `afterEveryRender` |
| Rama de lógica (no de template) según entorno | `isPlatformBrowser(inject(PLATFORM_ID))` |
| El objeto `document` | `inject(DOCUMENT)`, nunca el global |

`afterNextRender`/`afterEveryRender` **no corren en el servidor**. Preferí la forma con
fase explícita (`read`/`write`) a la de callback suelto: la doc advierte que la fase por
defecto (`mixedReadWrite`) puede degradar la performance.

```ts
// ❌ revienta en SSR
ngOnInit() { this.width = window.innerWidth; }

// ✅ solo navegador, con fase explícita
constructor() {
  afterNextRender({ read: () => this.width.set(this.host().nativeElement.offsetWidth) });
}
```

- **No ramifiques el template por plataforma** (`@if (isBrowser)`): el HTML del servidor
  y el del cliente divergen y eso es un mismatch. El primer render debe ser idéntico en
  ambos lados; lo exclusivo del navegador aparece después, vía signal seteado en
  `afterNextRender`.
- Timers, `setInterval`, websockets y polling no arrancan en el servidor: impiden que la
  app se estabilice y cuelgan la respuesta. Arrancalos en `afterNextRender`.
- Librerías que tocan `window` al importarse: `import()` dinámico dentro de
  `afterNextRender` (ver el patrón de Motion en `frontend-motion`).
- Valores no deterministas (`Date.now()`, `Math.random()`, zona horaria, locale del
  navegador) renderizados en el template producen HTML distinto en cada lado.

## 2. Hydration

- Se habilita con `provideClientHydration()` en la config del cliente. Reusa el DOM del
  servidor en vez de destruirlo y recrearlo (sin parpadeo, mejor LCP/CLS).
- Requisitos: HTML **válido** (un `<div>` dentro de `<p>`, o una `<table>` sin `<tbody>`
  que el navegador autocorrige, rompen la correspondencia de nodos) y **cero
  manipulación directa del DOM** fuera de Angular (`innerHTML`, `appendChild`, mover nodos).
- `ngSkipHydration` en el host de un componente lo excluye junto con sus hijos. Es
  escape temporal con TODO y dueño, no solución: ese subárbol se re-renderiza entero.
  Solo va en hosts de componentes, no en elementos comunes.
- Event replay: captura los eventos ocurridos antes de hidratar y los reproduce después
  (`withEventReplay()`; la hidratación incremental lo activa sola).

Ante un mismatch, en orden: (1) leé el error completo — la consola nombra el componente
y el nodo; (2) validá el HTML servido; (3) buscá DOM manual o ramas por plataforma;
(4) buscá valores no deterministas en el template. Método general en `root-cause-debugging`.

## 3. Hidratación incremental y `@defer`

En v21 se habilita con `provideClientHydration(withIncrementalHydration())`. La doc
vigente de angular.dev indica que en versiones posteriores viene activa por defecto (y
se desactiva con `withNoIncrementalHydration()`): **verificá tu versión**.

```html
@defer (on viewport; hydrate on interaction) {
  <app-comments [postId]="post().id" />
} @placeholder {
  <div class="comments-skeleton"></div>
}
```

El bloque se renderiza en el servidor (el usuario y el crawler ven contenido), pero su
JS no se descarga ni se hidrata hasta el trigger.

| Trigger `hydrate` | Cuándo |
|---|---|
| `on idle` | navegador ocioso |
| `on viewport` | entra al viewport |
| `on interaction` | click o tecla sobre el bloque |
| `on hover` | hover |
| `on immediate` | apenas termina el contenido no diferido |
| `on timer(…)` | tras un tiempo |
| `when <condición>` | expresión verdadera |
| `never` | queda estático para siempre (contenido sin interacción) |

- Hidratar un bloque exige que **todos sus padres** ya estén hidratados: en `@defer`
  anidados, el trigger del hijo arrastra a los padres.
- El `@placeholder` reserva el mismo espacio que el contenido final (CLS — ver
  `frontend-performance`).
- Candidatos: comentarios, pie de página, widgets debajo del pliegue, mapas. No: header,
  navegación ni el CTA principal.

## 4. Datos: transfer cache de HTTP

Con hydration activa, los GET/HEAD que `HttpClient` hace en el servidor se serializan en
el HTML y el cliente los reusa en vez de repetirlos.

- Por defecto **no** se cachean pedidos con credenciales ni con headers `Authorization`,
  `Proxy-Authorization` o `Cookie`, ni respuestas `no-store`/`no-cache`/`private`.
- Se ajusta con `withHttpTransferCacheOptions({ filter, includeHeaders,
  includePostRequests, includeRequestsWithAuthHeaders })`.
- `includeRequestsWithAuthHeaders: true` incrusta respuestas autenticadas en el HTML. No
  lo prendas sin tener resuelto el punto §5.

## 5. Datos sensibles en el HTML servido

Todo lo que el servidor renderiza o transfiere queda en texto plano en el documento:
visible en "ver código fuente" y cacheable por proxies y CDN.

1. Una respuesta SSR con datos de un usuario **nunca** es cacheable de forma compartida:
   `Cache-Control: private, no-store`. Una caché que sirve el HTML de un usuario a otro
   es un incidente de privacidad (`data-privacy-phi`).
2. Nada de estado por-usuario en singletons o variables de módulo del servidor: el
   proceso Node atiende muchos requests. Estado por request, vía DI.
3. Tokens, secretos y claves no entran a `TransferState`, a un signal renderizado ni al
   bundle. Lo que vive en el entorno del servidor se queda en el servidor.
4. Datos clínicos: preferí `RenderMode.Client` para vistas autenticadas con PHI (no
   necesitan SEO), y SSR para lo público.
5. El servidor SSR no autoriza nada: reenvía la identidad del request a la API y la API
   decide (`authz-access-control`).

## 6. Modo de render por ruta

```ts
// app.routes.server.ts
export const serverRoutes: ServerRoute[] = [
  { path: 'directorio/**', renderMode: RenderMode.Server },   // público, indexable, dinámico
  { path: 'terminos', renderMode: RenderMode.Prerender },     // estático
  { path: 'app/**', renderMode: RenderMode.Client },          // detrás de login
  { path: '**', renderMode: RenderMode.Server },
];
// app.config.server.ts
provideServerRendering(withRoutes(serverRoutes))
```

`RenderMode` y `ServerRoute` salen de `@angular/ssr`. Las rutas del ejemplo son
ilustrativas: definilas en el CLAUDE.md del proyecto.

| Modo | Usalo para |
|---|---|
| `Prerender` (SSG) | contenido que cambia poco; mejor LCP, cero costo por request |
| `Server` (SSR) | público, dinámico, indexable (perfiles, directorios — ver `seo-public-pages`) |
| `Client` (CSR) | detrás de login, muy interactivo, datos sensibles |

## 7. Anti-patrones

- `typeof window !== 'undefined'` sembrado por todo el código en vez de `afterNextRender`.
- `ngSkipHydration` para "arreglar" un mismatch sin buscar la causa.
- Pedir los mismos datos dos veces (servidor y cliente) por saltearse `HttpClient`.
- Placeholder de otro tamaño que el contenido diferido.
- `hydrate never` sobre algo con botones.
- Cachear en CDN HTML de rutas autenticadas.

## Evidencia / DoD

- [ ] Build de SSR sin errores y el servidor responde la ruta tocada: pegá status y
      fragmento de `curl` a la URL mostrando que el HTML **trae el contenido**, no un shell vacío.
- [ ] Consola del navegador sin errores de hydration en la ruta (salida literal; ver `visual-proof`).
- [ ] Ningún acceso a globales de navegador fuera de `afterNextRender`/`afterEveryRender`
      (pegá el resultado del grep en los archivos tocados).
- [ ] Rutas con datos de usuario: `Cache-Control` pegado, y el HTML servido no contiene
      tokens ni datos de otro usuario.
- [ ] Todo `@defer` tiene `@placeholder` con espacio reservado.
- [ ] Modo de render de cada ruta nueva elegido y justificado.
- [ ] Cada API usada se verificó contra la doc de la versión instalada.
