---
name: sputnik-excel
description: Toma una estimación generada por sputnik-core (o issues desde Jira vía Atlassian MCP) y genera una cotización en Excel siguiendo el formato de la plantilla "Cotización - Validacion Ingresos Smartket.xlsx". Convierte puntos a horas de desarrollo y produce un .xlsx con membrete, tabla de tareas (cliente), hoja de resumen técnico (equipo), subtotal, IVA y total. Úsala cuando tras una estimación con sputnik-core el usuario pida el archivo Excel, o cuando comparta issues de Jira y pida cotizarlos a Excel.
disable-model-invocation: true
---

# Sputnik Excel — Cotización a .xlsx

Obtiene issues directamente desde Jira, los estima con la metodología `sputnik-core`, y genera un archivo Excel de cotización de servicios usando el formato de la plantilla **"Cotización - Validacion Ingresos Smartket.xlsx"**.

También acepta input manual: una tabla ya estimada por `cotizador-sputnik` o una lista de historias/tareas pegadas en el chat.

## Requisitos

- **Atlassian MCP** (Rovo u otro conector de Atlassian): necesario para obtener issues desde Jira. Si no está disponible, la skill solo funciona con input manual (tabla pegada).
- **openpyxl**: para generar el Excel (instalación: `pip install openpyxl`).

## Stack y metodología de estimación

Se hereda de `sputnik-core`. Si los issues de Jira no tienen puntos asignados, se aplica la misma escala Fibonacci (0/1/2/3) y reglas de división (máx. 3 puntos). Consulta la skill `sputnik-core` para los detalles completos.

## Conversión de puntos a horas

Cada punto Fibonacci se traduce a horas de desarrollo con esta tabla fija:

| Puntos | Horas |
|--------|-------|
| 0 | 0 |
| 1 | 2 |
| 2 | 4 |
| 3 | 6 |

Las tareas divididas (`[DIVISION]`) se suman como tareas independientes. El total de horas se calcula automáticamente en el Excel.

## Estructura del Excel generado

El archivo debe replicar fielmente la hoja **"Factura de servicio"** de la plantilla. Se usa `openpyxl` para generarlo.

### Hoja: "Cotización"

| Celda(s) | Contenido | Formato |
|----------|-----------|---------|
| **E2:F2** (merge) | `COTIZACIÓN` | Century Gothic, 28pt, bold, white (theme 1), alineación right+center |
| **C3:D3** (merge) | Nombre de la empresa (preguntar al usuario, default: `OCTANE SYSTEMS, SA DE CV`) | Century Gothic, 11pt, bold |
| **E3** | `Fecha:` | Century Gothic, 8pt, bold |
| **F3** | `=TODAY()` | Century Gothic, 8pt |
| **E4** | `N.° de Cotización:` | Century Gothic, 10pt, bold, alineación right |
| **F4** | Número de cotización (preguntar al usuario) | Century Gothic, 8pt |
| **E5** | `Id. del cliente:` | Century Gothic, 10pt, bold |
| **F5** | ID del cliente (preguntar al usuario) | Century Gothic, 8pt |
| **C6** | `Para:` | |
| **D6** | Nombre del cliente | |
| **E6** | `Autoriza:` | |
| **F6** | Nombre de quien autoriza | |
| **C12** | `Responsable` | Header azul (theme 8 solid fill), bold, white text, center |
| **D12** | `Trabajo` | Header azul |
| **E12** | `Días Hábiles` | Header azul |
| **F12** | `Fecha de vencimiento` | Header azul |
| **C13** | Responsable del proyecto (preguntar) | |
| **D13** | Nombre/descripción del trabajo (preguntar) | |
| **E13** | Días hábiles estimados (horas totales / 8) | |
| **F13** | `=TODAY() + N` donde N son los días hábiles | |
| **C14** | `Horas de desarrollo` | Header tabla de tareas, bold, center |
| **D14** | `Descripción` | Header tabla de tareas, bold, center |
| **E14** | `Precio por hora` | Header tabla de tareas, bold, center |
| **F14** | `Total de línea` | Header tabla de tareas, bold, center |

### Tabla de tareas (desde fila 15 en adelante)

Cada fila de la estimación (omitiendo SUBTOTAL/TOTAL GENERAL) genera una fila:

| Col C (Horas) | Col D (Descripción) | Col E (Precio/hr) | Col F (Total línea) |
|---|---|---|---|
| Horas según tabla de conversión | **Descripción Cliente** (humanizada, sin jerga técnica, **sin prefijo de capa**) | Precio por hora configurable (default: 25) | `=IF(C{r}>0, C{r}*E{r}, "")` |

- **La descripción usa la columna "Descripción Cliente"** de la estimación (lenguaje de negocio, NO la estructura descriptiva técnica).
- **NO se incluye el prefijo de capa** (`[SQL]`, `[Backend]`, `[Frontend]`) — el Excel es para el cliente, no necesita ver la categoría técnica.
- Si hay justificación relevante para el cliente (<15 palabras), se añade al final entre paréntesis.
- Las tareas `[DIVISION]` se listan secuencialmente como filas normales.
- Fuente: Century Gothic, 8pt. Horas y precios alineados a la derecha.

### Totales

Tras la última fila de tareas (dejar 1 fila vacía):

| Fila | Col E | Col F |
|------|-------|-------|
| Subtotal | `Subtotal` (bold, theme 6, fill gris claro) | `=SUM(F15:F{last_data_row})` |
| (vacía) | | |
| IVA | `IVA` | `=F{subtotal_row}*0.16` |
| Total | `Total` (bold, theme 6, fill gris claro) | `=F{subtotal_row}+F{iva_row}` (el total es subtotal + IVA, asumiendo descuento 0) |

Formato de totales: bordes finos superior, borde grueso inferior en la fila Total.

### Pie de página

| Celda | Contenido |
|-------|-----------|
| **C33:D33** (merge) | `de ser aceptada la cotización se generará su factura en los 3 días hábiles siguientes. Con un plazo de 15 días para pagar` |
| **C34:F34** (merge) | `Favor de confirmar con un correo si se acepta la cotización` |

### Formato general

- Fuente base: Century Gothic, 8pt para datos
- Ancho de columnas: C=14, D=90, E=27, F=24
- Alto de fila de datos: 15
- Sin bordes en celdas de datos (solo en headers y totales)

## Workflow

### Paso 0: Conectar a Jira (si el input viene de Jira)

Si el usuario pide cotizar issues directamente desde Jira:

1. Confirma que tienes acceso a las herramientas de Jira (`search_jira_issues`, `get_visible_jira_projects`, `get_jira_issue`). Si no están disponibles, pide al usuario que instale la extensión Atlassian MCP y configure las variables de entorno (`ATLASSIAN_BASE_URL`, `ATLASSIAN_USERNAME`, `ATLASSIAN_API_TOKEN`).
2. Pregunta al usuario en un solo mensaje:
   - **Project key** (ej. `SPK`, `ITSEG`). Si no lo sabe, usa `get_visible_jira_projects` para listarlos.
   - **Filtro**: ¿todos los issues del proyecto? ¿un sprint específico? ¿un JQL? (default: issues sin resolver del proyecto, o los de un sprint activo).
   - **¿Los issues ya tienen story points?** Si sí, se usan directamente y solo se convierten a horas. Si no, se estiman con `cotizador-sputnik`.
3. Obtén los issues con `search_jira_issues` usando JQL. Extrae de cada uno: key, summary, description, story points (si existen), labels, issue type.

### Paso 1: Estimar (si aplica)

- Si los issues ya tienen story points: úsalos tal cual. Cada punto se convierte a horas según la tabla de conversión.
- Si no tienen puntos: aplica `sputnik-core`. Para cada issue, analiza summary + description, infiere capa (SQL/Backend/Frontend) y tipo de actividad, asigna puntos Fibonacci, divide si >3.
- Muestra la tabla resultante al usuario para validación antes de continuar.

Si el input es manual (tabla pegada o historias en texto), omite el Paso 0 y ve directo al Paso 1 con el input proporcionado.

### Paso 2: Recolectar datos de la cotización

Pregunta al usuario en un solo mensaje (no uno por uno):

1. **Nombre de la empresa** (default: `OCTANE SYSTEMS, SA DE CV`)
2. **N.° de cotización** (ej. `N.° 21129`)
3. **ID del cliente** y **nombre del cliente** (`Para:`)
4. **Nombre de quien autoriza** (`Autoriza:`)
5. **Responsable** del proyecto
6. **Nombre del trabajo** (descripción general, ej. `Validación de Ingresos en Smartket`)
7. **Precio por hora** (default: 25 USD). Stack sugerido: .NET + SQL Server → 30 USD/hr; Node.js/React → 25 USD/hr; Python → 25 USD/hr. El precio se ajusta según el dev-kit del proyecto si está identificado.
8. **Nombre del archivo de salida** (default: `Cotización - {Nombre del trabajo}.xlsx`)

Si el usuario ya proporcionó alguno de estos datos en el contexto, no lo preguntes de nuevo.

### Paso 3: Validar antes de generar

Muestra un resumen ANTES de generar el Excel:

```
📊 Resumen de cotización:
- Empresa: [nombre]
- Trabajo: [descripción]
- Total de tareas: N
- Total de puntos: X → Total de horas: Y
- Días hábiles: Z (Y/8)
- Precio por hora: $W
- Subtotal: $S | IVA (16%): $I | Total: $T

¿Genero el archivo Excel?
```

Espera confirmación explícita.

Si los issues ya existen en Jira con story points, compara la suma de puntos/horas del Excel contra los puntos en Jira. Si hay divergencia >10%, alerta: "⚠️ La suma de puntos en Jira (42 pts) difiere de la estimación actual (38 pts). Revisa antes de generar."

### Paso 4: Generar el Excel

Usa `openpyxl` para crear el archivo. La implementación debe:

1. Crear un workbook con una hoja llamada `Cotización`
2. Escribir todos los datos siguiendo la estructura de celdas definida arriba
3. Aplicar fórmulas (TODAY, SUM, multiplicación, IVA, total)
4. Aplicar formatos (fuentes, colores, alineación, bordes, anchos de columna, altos de fila)
5. Guardar el archivo en la ruta indicada por el usuario (default: directorio de trabajo actual)

### Paso 5: Confirmar entrega

Al terminar:

```
✅ Cotización generada: [ruta del archivo]
📄 [N] tareas | [Y] horas totales | Total: $[T]
```

## Manejo de tareas divididas `[DIVISION]`

Aparecen como filas independientes en el Excel, igual que en la tabla original. Conservan el prefijo `[DIVISION]` en la descripción para trazabilidad.

## Mapeo de capa a descripción en Excel

Las capas se usan internamente para agrupar y estimar, pero **NO se muestran en el Excel**. La columna "Descripción" del Excel contiene únicamente la **Descripción Cliente** humanizada, sin prefijos.

| Capa (interno) | Descripción en Excel (cliente) |
|---|---|
| SQL | `Creación de motor de base de datos para consulta de identificadores de clase` |
| Backend | `Desarrollo de servicio de consulta para el reporte de capas de costo` |
| Frontend | `Desarrollo de pantalla de visualización del reporte de capas de costo` |

**La descripción siempre debe ser humanizada** (ver `sputnik-core` → "Descripción para cliente"). Nada de `usp_`, `dbo.`, nombres de endpoints, rutas técnicas, ni prefijos `[SQL]`, `[Backend]`, `[Frontend]`.

## Lo que NO debes hacer

- No intentes conectar a Jira si no tienes las herramientas `search_jira_issues` y `get_visible_jira_projects` disponibles; pide al usuario que instale la extensión o que pegue los issues manualmente.
- No generes el Excel sin confirmación del usuario.
- No modifiques los puntos ni las horas — respeta los valores exactos de la tabla o del issue de Jira.
- No incluyas filas de SUBTOTAL o TOTAL GENERAL de la tabla original como tareas en el Excel.
- No uses otras fuentes que no sean Century Gothic.
- No generes hojas adicionales (solo `Cotización` y `Resumen Técnico`).

### Hoja: "Resumen Técnico" (interna del equipo)

Además de la hoja "Cotización" (cliente), genera una segunda hoja para uso interno del equipo con la tabla original de estimación:

| Col A (Capa) | Col B (Req.) | Col C (Actividad) | Col D (Estructura Descriptiva) | Col E (Puntos) | Col F (Justificación) |
|---|---|---|---|---|---|
| SQL | Req. 00001 | Se realiza SP | MiDB.ins.usp_AltaOrden | 3 | Lógica de negocio con transacción |

- Incluye todas las filas de la estimación original (incluyendo `[DIVISION]`).
- **No incluye** filas de SUBTOTAL ni TOTAL GENERAL.
- Fuente: Consolas, 9pt (estilo técnico, legible).
- Esta hoja es para que el equipo sepa exactamente qué construir sin la traducción humanizada.
- No omitas el IVA ni las fórmulas — el Excel debe ser funcional, no solo valores planos.
