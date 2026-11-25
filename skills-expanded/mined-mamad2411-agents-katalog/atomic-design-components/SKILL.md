---
name: atomic-design-components
description: Componentes compartidos por atomic design (atoms, molecules, organisms) — criterio de cada nivel, descubrir y REUSAR antes de crear, parametrizar en vez de copiar, API de componente (inputs semánticos, content projection, outputs), presentación vs contenedores, tokens en vez de literales y catálogo vivo. Usar antes de crear cualquier componente de UI, al revisar un PR que agrega uno, al ubicar algo como átomo/molécula/organismo, o al detectar dos componentes que hacen casi lo mismo.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Componentes por atomic design

Regla número uno: **antes de crear, buscá**. La mayoría de los componentes "nuevos" ya
existen con otro nombre o son una variante parametrizable de uno existente. Un PR que
agrega un componente compartido tiene que demostrar que buscó (`native-code-patterns`,
`anti-hallucination-guard`).

## 1. Los niveles

| Nivel | Qué es | Sabe de | Ejemplos |
|---|---|---|---|
| Átomo | Elemento indivisible de UI | Solo tokens y accesibilidad | botón, input, badge, avatar, ícono, spinner |
| Molécula | Pocos átomos con un propósito | Sus átomos; nada de datos ni de dominio | campo con label+error, barra de búsqueda, chip con cierre, ítem de lista |
| Organismo | Sección con sentido propio | Su composición; el dominio solo como **forma** de datos, nunca cómo obtenerlos | header, tarjeta de resultado, tabla paginada, formulario de dirección |
| Página / feature | Orquesta organismos con datos reales | Datos, rutas, permisos | vive en la feature, no en lo compartido |

Criterio para ubicar: ¿podés describir el componente sin nombrar un caso de uso? → átomo
o molécula. ¿Se nombra por lo que muestra ("tarjeta de profesional")? → organismo.
¿Se nombra por dónde vive ("pantalla de agenda")? → feature, no es compartido.

Los átomos no importan moléculas; las moléculas no importan organismos. Las flechas van
para un solo lado.

### Cada nivel es una responsabilidad (puente con SOLID)

El nivel de un componente es su **responsabilidad única** (SRP): un átomo renderiza, un
organismo compone, un contenedor trae datos. Que sepa de dos niveles a la vez (un organismo
que además hace `fetch`) es SRP roto. La extensión por variantes y projection en vez de
editar el componente (OCP), los inputs mínimos y cerrados (ISP) y la dependencia de
abstracciones inyectadas solo en los contenedores (DIP) se desarrollan en
`component-architecture-solid`; el catálogo de principios puros, en `solid-principles`. En §5 está la
separación contenedor/presentacional.

## 2. Antes de crear

1. Listá lo existente: nombres de carpeta + `selector` de cada componente compartido.
2. Buscá por **función**, no por nombre (un "chip" puede llamarse `tag`, `badge`, `pill`).
3. Si existe uno al 80 %: agregale la variante (§4). Copiarlo y cambiarle tres líneas
   crea el segundo del par que después diverge.
4. Si no existe: ¿lo va a usar más de una feature? Si no, vive en la feature. Lo
   compartido se promueve cuando aparece el segundo consumidor real, no antes.
5. Registrá en el PR qué buscaste y por qué no sirvió.

## 3. API de un componente

```ts
@Component({ selector: 'app-badge', /* … */ })
export class Badge {
  readonly tone = input<'neutral' | 'info' | 'success' | 'warning' | 'danger'>('neutral');
  readonly size = input<'sm' | 'md'>('md');
}
// uso: <app-badge tone="success">Confirmada</app-badge>
```

- Inputs mínimos y semánticos: `tone="danger"`, no `color="#c62828"`; `size="sm"`, no
  `padding="4"`. Un input que recibe CSS es un agujero en el sistema.
- Variantes como **unión cerrada** de strings; el compilador rechaza lo que no existe.
- Contenido por `<ng-content>`: el consumidor decide el texto y los hijos; el componente
  decide la forma. Múltiples slots con `select`, y contenido por defecto adentro del
  `<ng-content>` cuando corresponde.
- Un output por intención (`(picked)`, `(dismissed)`), no `(change)` genérico con un
  objeto que hay que inspeccionar.
- Booleans para estados reales (`disabled`, `loading`), no para elegir entre dos
  apariencias (eso es una variante).
- Cuando un organismo necesita piezas configurables (columna custom de una tabla), aceptá
  un `TemplateRef` vía `contentChild` + `NgTemplateOutlet`; no inputs con HTML en string.
- Todo componente compartido sigue las convenciones del framework del repo y se puede montar
  aislado en un test.

## 4. Parametrizar en vez de copiar

Síntoma: dos componentes con el 80 % del template igual. Tratamiento:

- Diferencia de apariencia → nueva **variante** (`tone`, `size`, `layout`).
- Diferencia de contenido → **content projection** con slots.
- Diferencia de comportamiento chico → **input booleano** o **output** nuevo.
- Diferencia grande de comportamiento → dos componentes que comparten los **átomos**,
  no el template.

Límite: si un componente acumula más de ~6 inputs o un `@switch` gigante por variante,
está haciendo dos cosas; partilo (`solid-principles`).

## 5. Presentación vs contenedor

- Los componentes compartidos son de **presentación**: reciben datos por inputs, emiten
  outputs, no inyectan servicios de datos ni el router, no saben de permisos.
- Los contenedores (páginas, secciones de feature) traen datos y los pasan hacia abajo.
- Un organismo compartido que necesita "cargar sus datos" pasa a ser un contenedor de
  feature; deja de ser compartido.
- Los estados de carga/vacío/error los **muestra** el componente compartido por input
  (`state="loading"`), pero los **decide** el contenedor (`frontend-ux-states`).

## 6. Estilos y tokens

- Cero hex, px de espaciado o familia tipográfica literales: solo custom properties del
  sistema (`frontend-design-system`, `css-architecture`).
- El componente no define márgenes externos: el layout se lo da el padre. Un átomo que
  trae `margin-bottom` propio rompe cada segundo contexto donde se usa.
- Variantes por clase del host (`host: { '[class.tone-danger]': …}`) o `data-*`, sin
  `[style]` inline.
- Tema claro/oscuro sale gratis si solo usás tokens semánticos; si necesitás una regla
  específica de tema, es un token que falta.

## 7. Catálogo vivo

- Cada componente compartido tiene: descripción de una línea, tabla de inputs/outputs,
  variantes con ejemplo, estados (hover, focus, disabled, loading, error), notas de
  accesibilidad (roles, nombre accesible, teclado).
- Publicado en el catálogo del proyecto (Storybook u otro que el proyecto defina) o, como
  mínimo, en una página de demo dentro de la app. Lo que no se ve, se duplica.
- Promover, renombrar o borrar un compartido es un cambio de contrato: buscá todos los
  consumidores (grep del selector) y registralo (`technical-docs-and-adr`).

## 8. Anti-patrones

- Componente en la carpeta compartida con un solo consumidor.
- `input()` de color, tamaño en px o clase CSS.
- Componente compartido que inyecta `HttpClient`, un store de datos o `Router`.
- `ButtonPrimary` y `ButtonSecondary` como dos componentes; `Card` y `CardV2`.
- Organismo que importa a otro organismo del mismo nivel para "reusar la mitad".
- Márgenes externos en átomos; estilos globales que dependen del orden de import.
- Nombre por caso de uso en un átomo (`app-save-button`).

## Checklist

- [ ] Se buscó antes de crear y el PR lo documenta.
- [ ] El componente está en el nivel correcto y no importa hacia arriba.
- [ ] Inputs semánticos con variantes cerradas; sin CSS por input.
- [ ] Contenido por projection; outputs por intención.
- [ ] Sin servicios de datos, router ni permisos dentro de un compartido.
- [ ] Solo tokens; sin márgenes externos; tema oscuro sin reglas especiales.
- [ ] Estados (hover/focus/disabled/loading/error) resueltos y accesibles.
- [ ] Entrada en el catálogo + harness + test de contrato.
