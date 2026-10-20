---
name: smart-dumb-components
description: Patrón contenedor/presentacional (smart vs dumb) en Angular — dumb = presentacional puro, solo `input()`/`output()`, sin inyectar servicios ni router; smart = contenedor que orquesta estado, datos y efectos casi sin markup propio. Cubre qué va en cada uno, la comunicación datos-abajo/eventos-arriba, dónde vive el estado y cómo se testea cada uno. Usar al crear cualquier componente, al partir uno que trae datos y pinta a la vez, cuando un componente no se puede reusar en otra pantalla ni testear sin levantar media app, o al decidir si algo debe inyectar un servicio.
---

# Componentes smart y dumb (contenedor / presentacional)

Todo componente cae en uno de dos roles. Mezclarlos es la causa número uno de UI que no se
puede reusar ni testear. Este patrón implementa SRP y DIP a nivel de UI
(`component-architecture-solid`) y se apoya en los niveles de `atomic-design-components` y
el estado de `angular-signals-state`.

## 1. Los dos roles

| | Dumb (presentacional) | Smart (contenedor) |
|---|---|---|
| Trabajo | Mostrar lo que recibe, avisar lo que el usuario hace | Traer/mutar datos y coordinar |
| Entrada | `input()` | Servicios inyectados, ruta, params |
| Salida | `output()` | Llama a servicios, navega |
| Inyecta | Nada de datos (a lo sumo utilidades puras) | `HttpClient`/gateways, stores, `Router` |
| Estado | Ninguno propio salvo UI efímera (hover, abierto/cerrado) | Estado de la vista y de servidor |
| Markup | Rico, es su razón de ser | Mínimo: casi solo `<app-dumb .../>` |
| Change detection | `OnPush`, idealmente puro | `OnPush` |
| Reuso | Alto | Casi nulo (atado a un caso) |
| Test | En aislamiento, sin red (`angular-testing`) | Con dobles de servicios / `HttpTestingController` |

Los átomos, moléculas y la mayoría de los organismos compartidos son **dumb**. Las páginas
y las secciones de feature que traen datos son **smart**.

## 2. Comunicación: datos abajo, eventos arriba

Regla única de flujo: el contenedor pasa datos hacia abajo por `input()`; el presentacional
avisa hacia arriba por `output()`. El dumb nunca "busca" nada ni muta estado global.

```ts
// ✅ DUMB: puro, reusable, sin idea de dónde salen los datos
@Component({
  selector: 'app-appointment-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <article>
      <h3>{{ appointment().patientName }}</h3>
      <button (click)="confirm.emit(appointment().id)">Confirmar</button>
    </article>`,
})
export class AppointmentCard {
  readonly appointment = input.required<AppointmentVm>();
  readonly confirm = output<string>();
}
```
```ts
// ✅ SMART: orquesta datos y efectos; delega el pintado al dumb
@Component({
  selector: 'app-agenda-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (a of appointments.value(); track a.id) {
      <app-appointment-card [appointment]="a" (confirm)="onConfirm($event)"/>
    }`,
  imports: [AppointmentCard],
})
export class AgendaPage {
  private readonly gateway = inject(AppointmentsGateway);
  protected readonly appointments = this.gateway.today;   // resource/httpResource
  onConfirm(id: string) { this.gateway.confirm(id); }
}
```

Para inputs de doble vía usá `model()` (p. ej. un control de UI reutilizable), pero el
estado con dueño vive en el smart: `model()` es azúcar de `input()` + `output()`, no una
excusa para que un dumb mute datos de dominio.

## 3. Dónde vive el estado

- **UI efímera** (dropdown abierto, tab activa, hover): puede vivir en el dumb como `signal`
  local. No sale de ahí.
- **Estado de la vista** (filtros, selección, paginado por cursor): en el smart.
- **Estado de servidor** (la lista, el detalle): en el smart, vía `resource`/`httpResource`
  o un store (`angular-signals-state`). El dumb lo recibe ya resuelto.
- **Estados de carga/vacío/error**: el smart los **decide** y se los pasa al dumb como
  input (`state="loading"`); el dumb solo los **muestra** (`frontend-ux-states`).

## 4. Cómo testear cada uno

- **Dumb**: montá el componente con `TestBed`, seteá inputs con `setInput`, disparás la
  interacción y verificás el markup y el output emitido. Sin red, sin mocks de servicios,
  rápido y estable. Candidato ideal para regresión visual (`visual-regression-testing`).
- **Smart**: probá la orquestación con dobles del gateway/store (o `HttpTestingController`),
  verificando que llama a lo correcto y pasa los datos bien; el detalle visual ya está
  cubierto por el test del dumb. Ver `angular-testing`.

## 5. Cómo partir un componente que hace las dos cosas

1. Identificá el markup rico → se va a un dumb nuevo con `input()`/`output()`.
2. Lo que inyecta servicios, trae datos o navega → se queda en el smart.
3. Definí el **view model** (`Vm`): la forma exacta que el dumb necesita, mapeada por el
   smart. El dumb no recibe la entidad de dominio cruda ni el DTO de la API.
4. Conectá: datos por input, eventos por output. Cero referencias del dumb a servicios.

## 6. Anti-patrones

- **Dumb que inyecta** `HttpClient`, un store de datos, `Router` o `ActivatedRoute`: dejó de
  ser reusable y ya no se testea en aislamiento.
- **Smart lleno de estilos y markup**: si tiene CSS y template ricos, escondió un dumb
  adentro. Extraelo.
- **Prop drilling**: pasar un input tres niveles hacia abajo sin usarlo en el medio.
  Composición con content projection o un smart más cercano a la hoja.
- **Dumb que muta lo que recibe**: el input es de solo lectura; para cambiarlo, emití un
  output y que el dueño del estado decida.
- **Dumb que conoce el dominio de negocio**: recibe un `AppointmentVm`, no sabe de reglas de
  agenda ni de permisos.
- **`effect()` en un dumb para sincronizar inputs**: casi siempre es un `computed` o un
  output; ver `angular-signals-state`.

## Relación con los otros ejes

- **Átomo/molécula/organismo** (`atomic-design-components`): describe *qué tan compuesto* es
  el componente. **Smart/dumb** describe *si maneja datos*. Un organismo suele ser dumb; una
  página es smart. Son ejes ortogonales, no sinónimos.
- **SOLID** (`component-architecture-solid`): smart/dumb es la aplicación concreta de SRP
  (una razón para cambiar) y DIP (lo presentacional no depende de servicios concretos).

## Checklist

- [ ] Cada componente tiene rol claro: o presentacional o contenedor, no ambos.
- [ ] El dumb solo usa `input()`/`output()`/`model()`; no inyecta servicios de datos ni router.
- [ ] El dumb recibe un view model, no la entidad de dominio ni el DTO crudo.
- [ ] El estado con dueño vive en el smart; el dumb solo tiene UI efímera.
- [ ] Datos abajo por input, eventos arriba por output; sin prop drilling ni mutación de inputs.
- [ ] Ambos son `OnPush`; el dumb se testea sin red y el smart con dobles.
