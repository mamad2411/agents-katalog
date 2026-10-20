---
name: frontend-data-access
description: Capa de acceso a datos en Angular — un cliente tipado por recurso en una capa dedicada, interceptors funcionales (auth, errores, correlación, reintento), mapeo del contrato de error del backend a la UI, cancelación y no llamar `HttpClient` desde el componente. Usar al crear el cliente de un endpoint nuevo, al registrar un interceptor, al tipar la respuesta de la API, o cuando un componente traga el error del backend. Si el problema es que el componente no se puede reusar ni testear aislado, el patrón de fondo es `smart-dumb-components`.
---

# Acceso a datos — Angular

La regla madre: **el componente no habla HTTP**. Un componente pide a un servicio; el
servicio de acceso a datos habla con la API. Así el estado (`angular-signals-state`) y la
vista quedan sin acoplarse al transporte, y el contrato se testea en un solo lugar.

## 1. Un cliente por recurso

- Una clase de acceso a datos por recurso del backend (`PatientApi`, `AppointmentApi`),
  en una carpeta dedicada (p.ej. `core/data-access/`), no esparcida por features.
- Cada método devuelve el tipo del contrato, nunca `any`. El tipo es la forma real de la
  respuesta de la API — derivalo del contrato OpenAPI, no lo inventes (ver `api-openapi-docs`).
- El cliente no decide UI: no muestra toasts ni navega. Devuelve datos o lanza un error
  tipado que la capa de estado traduce.

```typescript
// ✅ cliente delgado, tipado, sin lógica de vista
@Injectable({ providedIn: 'root' })
export class AppointmentApi {
  private http = inject(HttpClient);
  private base = inject(API_BASE_URL);

  getPage(cursor?: string): Observable<Page<Appointment>> {
    let params = new HttpParams();
    if (cursor) params = params.set('cursor', cursor);
    return this.http.get<Page<Appointment>>(`${this.base}/appointments`, { params });
  }
}
```

```typescript
// ❌ HttpClient dentro del componente: acopla vista, transporte y errores
@Component({ /* ... */ })
class ListComponent {
  private http = inject(HttpClient);
  items = signal<any[]>([]);        // any + fetch en el componente
  ngOnInit() { this.http.get<any[]>('/appointments').subscribe(x => this.items.set(x)); }
}
```

## 2. Interceptors funcionales (v21)

Registrá interceptors con `provideHttpClient(withInterceptors([...]))`. Un
`HttpInterceptorFn` corre en contexto de inyección, así que puede usar `inject()`. Cloná la
request para modificarla (es inmutable). Orden: el arreglo define el orden de ejecución.

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(TokenStore).access();
  if (!token) return next(req);
  return next(req.clone({ headers: req.headers.set('Authorization', `Bearer ${token}`) }));
};
```

Interceptors que conviene tener, cada uno con una sola responsabilidad:

| Interceptor | Hace |
|---|---|
| auth | Adjunta el token; no lo guarda ni lo renueva (eso es del store) |
| correlation | Agrega un `X-Request-Id`/traceparent para correlacionar con el backend (ver `backend-observability`) |
| error | Traduce la respuesta de error a un error de dominio tipado |
| retry | Reintenta **solo** GET idempotentes ante error de red/5xx, con backoff acotado |

## 3. Mapear el error del backend, no tragarlo

El backend responde errores con un contrato estable (problem details, ver
`error-handling-contract`). El interceptor de error lo convierte en un error de dominio que
la UI sabe distinguir; **nunca** un `catchError(() => of(null))` que borra la falla.

```typescript
export const errorInterceptor: HttpInterceptorFn = (req, next) =>
  next(req).pipe(
    catchError((e: HttpErrorResponse) => throwError(() => toDomainError(e))),
  );

// toDomainError mapea status + body.code → union discriminada { kind: 'not-found' | 'conflict' | ... }
```

- No mostrar el mensaje crudo del backend al usuario; mapear a copy propio (ver `ux-writing-microcopy`).
- El `0` de `HttpErrorResponse.status` es error de red/CORS/cancelación, no del servidor: tratalo aparte.
- Nunca loguear el body del error si puede traer datos de paciente (ver `frontend-error-monitoring`).

## 4. Cancelación y reintento

- Cancelación: al desuscribirse, Angular aborta la request. Para búsquedas que cambian con
  el input, usá `switchMap` (cancela la anterior). En estado con signals, `httpResource`
  cancela solo al cambiar la fuente.
- Reintento: solo peticiones idempotentes (GET), con número de intentos y backoff acotados;
  nunca reintentar un POST que crea algo sin clave de idempotencia (ver `concurrency-and-locking`).

## 5. SSR

Bajo SSR, la primera carga corre en el servidor. Usá la transfer cache de HTTP para no
repetir la request en el cliente y no filtrar datos sensibles en el HTML (ver
`angular-ssr-hydration`). No accedas a `window`/`localStorage` en el cliente de datos.

## Anti-patrones

- `HttpClient` inyectado en un componente o en un `effect`.
- Tipos `any`/`as` sobre la respuesta en vez del tipo del contrato.
- `subscribe` manual en el componente para setear un signal (usá `httpResource`/`toSignal`; ver `angular-signals-state`).
- Interceptor multiuso que hace auth + errores + logging (partilo).
- Reintentar mutaciones sin idempotencia; tragar errores con `of(null)`.

## Checklist

- [ ] Ningún componente inyecta `HttpClient`; todo pasa por un cliente de recurso.
- [ ] Cada método del cliente devuelve el tipo del contrato, sin `any`.
- [ ] Interceptors registrados con `withInterceptors`, uno por responsabilidad, orden pensado.
- [ ] El error del backend se mapea a un error de dominio; la UI no ve el mensaje crudo.
- [ ] GET reintentables con backoff acotado; mutaciones nunca sin idempotencia.
- [ ] Bajo SSR, transfer cache activa y sin datos sensibles en el HTML.
