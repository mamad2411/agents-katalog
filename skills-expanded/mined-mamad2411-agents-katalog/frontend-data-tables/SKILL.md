---
name: frontend-data-tables
description: Diseño e implementación de tablas de datos en la web — densidad legible, orden/filtro/paginación por cursor, columnas responsivas (qué se colapsa o pasa a tarjeta en móvil), selección y acciones masivas, estados por tabla (carga, vacío, error), virtualización de listas grandes y accesibilidad de tabla. Usar al construir cualquier listado tabular (agenda, solicitudes, pacientes, movimientos), al hacerlo responsivo, o al revisar una tabla lenta, ilegible o inutilizable en móvil.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Tablas de datos

Las tablas son donde el usuario pasa el tiempo en una herramienta. Una tabla buena es densa
pero legible, se opera con teclado y no colapsa en móvil ni con 10 000 filas.

## 1. Densidad legible

- Alineá: texto a la izquierda, **números a la derecha** con `font-variant-numeric: tabular-nums`
  para que las cifras se alineen por columna (ver `typography-systems`).
- Padding vertical suficiente para escanear; separadores sutiles (línea fina o zebra tenue), no
  bordes gruesos en cada celda.
- Encabezado fijo (`position: sticky`) en tablas largas; la primera columna identificadora
  también puede fijarse.
- Truncá texto largo con ellipsis + tooltip/expansión, no dejes que rompa la grilla.

## 2. Orden, filtro y paginación por cursor

- Orden por columna con indicador visible de columna y dirección; el orden lo resuelve el
  backend para datos grandes (ver `search-and-filtering`).
- Filtros arriba de la tabla, con chips de lo aplicado y "limpiar"; mostrá el conteo de resultados.
- Paginación por **cursor** (no offset): estable cuando los datos cambian entre páginas. La UI
  ofrece "cargar más"/siguiente; guardá el cursor, no el número de página.

## 3. Responsivo

Una tabla ancha no cabe en móvil. Elegí una estrategia explícita, no dejes scroll horizontal a ciegas:

| Estrategia | Cuándo |
|---|---|
| Colapsar columnas secundarias | Hay 2-3 columnas clave y el resto es detalle |
| Fila → tarjeta (label: valor) | Cada fila es una entidad rica (un paciente, una solicitud) |
| Scroll horizontal con 1ª columna fija | Comparación entre muchas columnas numéricas |

## 4. Selección y acciones masivas

- Checkbox por fila + "seleccionar todo" (con distinción entre "esta página" y "todos los N").
- Barra de acciones masivas que aparece al haber selección; confirmá las destructivas
  (ver `frontend-ux-states`).
- Mostrá cuántos hay seleccionados; permití deseleccionar fácil.

## 5. Estados de la tabla

Toda tabla resuelve sus estados, no solo el caso con datos:
- **Carga**: skeleton de filas (no un spinner que salta el layout).
- **Vacío**: mensaje útil + acción ("No hay solicitudes. Crear una"), distinguí "vacío real"
  de "vacío por filtro" (ofrecé limpiar filtro).
- **Error**: mensaje + reintentar, sin perder los filtros aplicados.

## 6. Virtualización y rendimiento

- Para miles de filas, virtualizá (renderizá solo lo visible) con CDK scrolling u otra
  utilidad de virtual scroll; medí el impacto (ver `frontend-performance`).
- No traigas 10 000 filas al cliente "por las dudas": paginá/filtrá en el servidor.
- `trackBy`/track en `@for` para no re-renderizar filas que no cambiaron.

## 7. Accesibilidad

- Usá `<table>` semántica con `<th scope>`; si construís una grilla con divs, ARIA de grid
  correcto (es más difícil — preferí `<table>`).
- Operable por teclado: foco en controles de orden, filas seleccionables, acciones.
- Encabezados asociados a celdas; no dependas solo del color para estados de fila.

## Anti-patrones

- Números alineados a la izquierda sin `tabular-nums`.
- Paginación por offset que duplica/saltea filas cuando los datos cambian.
- Scroll horizontal en móvil como única respuesta responsiva.
- Traer todo el dataset al cliente y filtrar/paginar en memoria.
- Tabla que solo contempla el caso "con datos".

## Checklist

- [ ] Números a la derecha con `tabular-nums`; encabezado sticky en tablas largas.
- [ ] Orden/filtro en el servidor; paginación por cursor estable.
- [ ] Estrategia responsiva explícita (colapso, tarjeta o scroll con columna fija).
- [ ] Selección con acciones masivas; destructivas confirmadas.
- [ ] Estados carga/vacío/error resueltos; vacío-por-filtro distinguido.
- [ ] Virtualización si hay miles de filas; `track` en el bucle.
- [ ] `<table>` semántica, operable por teclado, sin depender del color.
