---
name: component-architecture-solid
description: Cómo el diseño de un componente de UI Angular encarna SOLID — una responsabilidad por componente (SRP), extensible por inputs/slots/composición sin editarlo (OCP), variantes que respetan el contrato base (LSP), inputs mínimos y cerrados en vez de un mega-componente (ISP) y dependencia de abstracciones inyectadas (DIP). Usar al diseñar un componente, al revisar uno que creció con demasiados inputs o un `@switch` de negocio, o al decidir si partirlo, extenderlo por projection o inyectarle una dependencia.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Arquitectura de componentes con SOLID

SOLID no es solo para clases de backend: un componente Angular **es** una clase con un
contrato público (inputs/outputs/slots). Los mismos cinco principios deciden si ese
contrato envejece bien o se pudre. Este es el nivel de diseño; el nivel de nombres y
funciones lo cubre `clean-code`, el catálogo de principios puros `solid-principles`, y la
ubicación por nivel `atomic-design-components`.

## Cada nivel atómico tiene su responsabilidad (mapa SOLID)

| Nivel | Responsabilidad única (SRP) | De qué NO debe saber |
|---|---|---|
| Átomo | Renderizar un elemento con sus estados y accesibilidad | Datos, dominio, otros componentes |
| Molécula | Componer pocos átomos para un propósito | De dónde vienen los datos |
| Organismo | Armar una sección con sentido, recibiendo datos por input | Cómo se obtienen/mutan los datos |
| Contenedor (smart) | Orquestar estado, datos y efectos | Detalles de presentación |

Si un componente sabe de dos filas de esta tabla, tiene dos razones para cambiar → SRP roto.

## 1. SRP — una responsabilidad, una razón para cambiar

Un componente hace **una** cosa. Señales de que hace más de una: mezcla traer datos con
pintarlos; tiene un bloque de presentación y otro de lógica de negocio; el nombre lleva
"y" ("tarjeta-y-editor"); el archivo pasa de ~150 líneas de template sin ser una página.

```ts
// ❌ el mismo componente trae datos, filtra, pagina y pinta
@Component({ selector: 'app-patient-list' })
export class PatientList {
  private readonly api = inject(PatientApi);
  readonly patients = signal<Patient[]>([]);
  // ...fetch, filtro, orden, paginado Y markup de la tabla
}
```
```ts
// ✅ contenedor orquesta; presentacional pinta
@Component({ selector: 'app-patient-list-page' })          // smart
export class PatientListPage {
  private readonly api = inject(PatientApi);
  protected readonly patients = this.api.list;             // resource/httpResource
}
// template: <app-patient-table [rows]="patients.value()" (sort)="..."/>  // dumb
```

## 2. OCP — abierto a extensión, cerrado a modificación

Un componente estable (un átomo del design system, un organismo reusado) se **extiende sin
tocarlo**. Las tres palancas de extensión en Angular:

- **Inputs de variante** (unión cerrada): `tone`, `size`, `layout`.
- **Content projection**: `<ng-content>` con `select` para slots; el consumidor inyecta
  contenido sin que el componente sepa qué.
- **Plantillas configurables**: `contentChild(TemplateRef)` + `NgTemplateOutlet` para
  piezas como una celda custom de tabla.

```ts
// ❌ cada caso nuevo edita el componente: crece un @switch infinito
readonly kind = input<'doctor' | 'clinic' | 'insurer' | 'pharmacy' | ...>();
// template: @switch (kind()) { @case ('doctor') {...} @case ('clinic') {...} ... }
```
```ts
// ✅ cerrado a modificación: el consumidor proyecta su cuerpo
@Component({
  selector: 'app-entity-card',
  template: `<article><header><ng-content select="[card-title]"/></header>
             <ng-content/></article>`,
})
export class EntityCard {}
```

Regla: si agregar un caso de uso obliga a editar un componente compartido, OCP está roto.
Agregar una **variante nueva a la unión** sí es legítimo; agregar una **rama de negocio**
adentro no.

## 3. LSP — una variante no rompe el contrato

Toda variante de un componente debe ser usable donde se espera el componente, sin
sorpresas. Un `size="sm"` no puede dejar de emitir el output que emite `size="md"`; un
`variant="ghost"` de botón sigue siendo enfocable y activable por teclado.

- No condiciones el contrato a un input: `(picked)` se emite en **todas** las variantes o
  en ninguna. Un output que aparece y desaparece según otro input es una trampa.
- Nada de "esta prop solo funciona si esa otra vale X" sin que el tipo lo exprese. Si dos
  inputs son mutuamente excluyentes, modelalos como una sola unión discriminada.
- Preferí **composición a herencia** de componentes: extender una clase de componente para
  cambiar comportamiento suele violar LSP. Componé átomos, no heredes organismos
  (`solid-principles` desarrolla composición sobre herencia).

## 4. ISP — inputs mínimos y cohesivos

Nadie debería depender de inputs que no usa. Un componente con 20 inputs opcionales obliga
a cada consumidor a entender los 20 y multiplica los estados imposibles.

```ts
// ❌ mega-input: banderas sueltas, combinaciones inválidas posibles
readonly showHeader = input(false); readonly showFooter = input(false);
readonly compact = input(false); readonly bordered = input(false);
readonly elevated = input(false); readonly danger = input(false); // ...
```
```ts
// ✅ agrupá lo que viaja junto; cerrá las variantes
readonly variant = input<'flat' | 'bordered' | 'elevated'>('flat');
readonly tone = input<'neutral' | 'danger'>('neutral');
// slots para header/footer en vez de banderas: <ng-content select="[card-header]"/>
```

Síntoma de ISP roto: más de ~6 inputs, banderas booleanas que eligen apariencia (eso es una
variante), o combinaciones de inputs que no tienen sentido juntas. Partí el componente o
agrupá los inputs relacionados en un objeto/variante.

## 5. DIP — depender de abstracciones, no de concretos

Cuando un componente **necesita** una dependencia (un contenedor que trae datos), que
dependa de una **abstracción inyectada**, no de una implementación concreta. Así se testea
con un doble y se cambia la fuente sin tocar el componente.

```ts
// ❌ acoplado a la implementación concreta y a HttpClient
export class AppointmentsPage {
  private readonly http = inject(HttpClient);
  load() { return this.http.get('/api/appointments'); } // URL y transporte adentro
}
```
```ts
// ✅ depende de un puerto; la implementación se provee por DI
export abstract class AppointmentsGateway { abstract list(): Observable<Appointment[]>; }

@Component({ /* ... */ })
export class AppointmentsPage {
  private readonly gateway = inject(AppointmentsGateway);  // abstracción
}
```

Los componentes **presentacionales** llevan DIP al extremo: no inyectan nada de datos;
reciben todo por props. DIP aplica sobre todo a los contenedores.

## Tabla de decisión: síntoma → principio → movida

| Síntoma | Principio | Movida |
|---|---|---|
| Trae datos y además pinta | SRP | Partir en contenedor (smart) + presentacional (dumb) |
| Un `@switch` por caso de negocio crece con cada feature | OCP | Content projection / TemplateRef |
| Un output existe solo con cierto input | LSP | Contrato uniforme o unión discriminada |
| Más de ~6 inputs, banderas de apariencia | ISP | Variantes cerradas, agrupar, partir |
| Inyecta `HttpClient`/servicio concreto en algo reusable | DIP | Puerto inyectado, o subir la dependencia al contenedor |
| Se hereda una clase de componente para variar | LSP/OCP | Composición de átomos |

## Anti-patrones

- Un componente "hace todo" de una feature (God component).
- Herencia de componentes para compartir markup (usá composición y projection).
- Inputs que activan/desactivan otros inputs sin que el tipo lo modele.
- Servicio de datos o `Router` dentro de un átomo/molécula/organismo compartido.
- Agregar una rama `@if`/`@switch` de negocio a un componente del design system.

## Checklist

- [ ] El componente tiene una sola responsabilidad y una sola razón para cambiar (SRP).
- [ ] Se extiende por inputs/slots/plantillas, sin editar el componente estable (OCP).
- [ ] Toda variante respeta el mismo contrato de inputs/outputs (LSP).
- [ ] Inputs mínimos, cohesivos y con variantes cerradas; nada de banderas de apariencia (ISP).
- [ ] Las dependencias reales entran por abstracción inyectada; lo presentacional no inyecta datos (DIP).
- [ ] La responsabilidad vive en el nivel atómico correcto (`atomic-design-components`).
- [ ] La división estado/presentación es explícita: el contenedor trae datos y orquesta; el
      presentacional solo recibe props y emite eventos.
