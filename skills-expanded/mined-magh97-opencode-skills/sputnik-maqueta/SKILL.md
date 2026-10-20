---
name: sputnik-maqueta
description: "Analiza maquetas (Figma, PDF, imagen, ClaudeAI Design) y extrae componentes UI + endpoints + tablas, generando la tabla de estimación de sputnik-core. Úsala cuando suban una maqueta y pidan 'estimar esta pantalla' o 'desglosar este diseño'."
disable-model-invocation: true
metadata:
  requires-devkits: auto-detect
---

# Sputnik Maqueta — Diseño a Estimación

Analiza una maqueta (imagen, PDF, Figma, ClaudeAI Design) y genera la tabla de estimación de `sputnik-core` automáticamente.

---

## Workflow

### Paso 1: Recibir la maqueta

Formatos soportados:
- **Imagen**: PNG, JPG, WebP → usar la tool `Read` directamente sobre el archivo de imagen (es multimodal) para análisis detallado
- **PDF**: usar la tool `Read` sobre el archivo, indicando el parámetro `pages` para analizar cada página (o rango de páginas)
- **Figma**: si el usuario comparte link, pedir export o screenshot
- **ClaudeAI Design**: link a `https://claude.ai/design/p/{uuid}` → ver sección específica abajo
- **Video/screenshare**: si el usuario muestra una UI en video, extraer frames

Preguntar en un solo mensaje:
1. **Nombre del proyecto** (ej: `SSA`, `Smartket`)
2. **Req.** asociado (ej: `Req. 00042`)
3. **Stack objetivo**: Web (.NET + React + Ant Design) o Móvil (Flutter). Default: Web.
4. **¿La maqueta muestra un flujo completo o pantallas sueltas?**

### ClaudeAI Design — instrucciones específicas

**Formato**: ClaudeAI genera diseños como páginas HTML interactivas con mockups de UI, componentes visuales, tablas de datos, formularios, flujos de pantalla y especificaciones técnicas embebidas en el HTML.

**Procedimiento de extracción**:

1. **Cargar la skill `claude-in-chrome` primero** (es prerequisito antes de usar cualquier tool `mcp__claude-in-chrome__*`), y luego usar sus tools MCP reales para abrir y capturar el diseño:
   ```
   mcp__claude-in-chrome__tabs_create_mcp   # abrir una pestaña nueva
   mcp__claude-in-chrome__navigate          # navegar a "https://claude.ai/design/p/{uuid}"
   mcp__claude-in-chrome__read_page         # capturar el estado/estructura interactiva de la página
   mcp__claude-in-chrome__computer          # tomar screenshot y/o interactuar (clicks, scroll) con la página
   ```

2. **Navegar el diseño**: Si el diseño tiene tabs, secciones colapsables, o múltiples pantallas, identificarlas con `read_page` y navegar cada vista:
   - Buscar elementos clickeables en la lectura de la página (tabs, botones, enlaces internos)
   - Usar `mcp__claude-in-chrome__computer` para hacer clic en tabs/secciones y volver a leer/capturar
   - Tomar screenshot de cada pantalla/variante del diseño con `mcp__claude-in-chrome__computer`

3. **Analizar componentes visibles**: Una vez capturadas todas las vistas, aplicar el mismo análisis que para Figma:
   - Tablas de datos → `Se crea Tabla FrontEnd`
   - Formularios → `Se crea Alta/Cambio FrontEnd`
   - Filtros/búsqueda → `Se crea/modifica submenu`
   - Botones de acción (alta, cambio, baja) → inferir endpoints correspondientes

4. **Si el link requiere autenticación**:
   - Pedir al usuario que tome screenshots del diseño o copie el contenido al chat
   - Alternativamente, pedir que exporte el diseño como PDF/imagen
   - No asumir contenido que no se pueda verificar

5. **Si el diseño incluye especificaciones técnicas** (tablas de BD, endpoints sugeridos, reglas de negocio en texto): el HTML suele contener `<pre>`, `<code>`, o tablas con esta información. Extraerla con `mcp__claude-in-chrome__read_page` (o `mcp__claude-in-chrome__javascript_tool` si se necesita evaluar JS en la página).

### Paso 2: Analizar la maqueta

Para cada pantalla/componente visible, identificar:

#### Capa Frontend — Componentes visibles

| Elemento UI | Componente React | Tipo de actividad |
|-------------|-----------------|-------------------|
| Tabla con datos | `<ProTable>` o `<Table>` | `Se crea Tabla FrontEnd` |
| Formulario de creación | `<ProForm>` / `<Form>` + `<Modal>` | `Se crea Alta FrontEnd` |
| Formulario de edición | `<Drawer>` con `<ProForm>` | `Se crea Cambio FrontEnd` |
| Filtros / Búsqueda | `<Select>` con búsqueda remota, `<Input.Search>` | `Se crea/modifica submenu` |
| Pantalla completa nueva | Layout con sidebar, breadcrumb, contenido | `Se crea Pantalla FrontEnd` |
| Botón de eliminar con confirmación | `<Button danger>` + `<Modal>` | `Se crea Baja FrontEnd` |
| Gráficos / Charts | `<Chart>` (ECharts/Recharts) | `Se crea/modifica submenu` |
| Subida de archivos | `<Upload>` | `Se crea/modifica submenu` |

#### Capa Backend — Endpoints inferidos

Para cada operación CRUD visible en la UI:

| Acción UI | Endpoint inferido | Tipo de actividad |
|-----------|-------------------|-------------------|
| Tabla que carga datos | `GET /api/{recurso}` | `Se crea Consulta BackEnd` |
| Formulario de creación | `POST /api/{recurso}` | `Se crea Alta BackEnd` |
| Formulario de edición | `PUT /api/{recurso}/{id}` | `Se crea Cambio BackEnd` |
| Botón eliminar | `DELETE /api/{recurso}/{id}` | `Se crea Baja BackEnd` |
| Dropdowns que cargan opciones | `GET /api/{recurso}/lookup` | `Se crea Consulta BackEnd` |
| Exportar/Descargar | `GET /api/{recurso}/export` | `Se crea Consulta BackEnd` |

#### Capa SQL — Tablas y SPs inferidos

| Dato visible en UI | Objeto SQL inferido | Tipo de actividad |
|--------------------|---------------------|-------------------|
| Tabla con columnas X, Y, Z | `usp_Obtener{Recurso}` — SELECT con JOINs de las tablas dueñas de esas columnas | `Se realiza SP` |
| Formulario con campos A, B, C | `usp_Alta{Recurso}` — INSERT con validaciones | `Se realiza SP` |
| Formulario de edición | `usp_Cambio{Recurso}` — UPDATE con WHERE | `Se realiza SP` |
| Dropdown de catálogo | `usp_Obtener{Catalogo}Lookup` — SELECT Id, Nombre | `Se realiza SP` |
| Badges de estado (colores) | Tabla de catálogo: `CREATE TABLE Cat_Estados` | `Se crea tabla SQL` |

### Paso 3: Detectar complejidad implícita

Elementos en la maqueta que suben el puntaje:

| Señal visual | Implicación | Efecto en puntos |
|--------------|-------------|-----------------|
| Estados con colores (badges) | Catálogo + lógica de transición de estados | +1pt |
| Validaciones inline (mensajes rojos) | Reglas de negocio en backend + SP | +1pt |
| Loader/spinner en dropdown | Búsqueda remota → endpoint adicional + índices | +1pt |
| Filtros múltiples combinables | SP con WHERE dinámico + índices compuestos | +1pt |
| Paginación con total | COUNT(*) + paginación en SP | +1pt |
| Subida de archivos | Azure Blob / manejo de archivos + endpoint | +2pt |
| Exportar a Excel/PDF | Generación server-side + endpoint descarga | +2pt |
| Múltiples tabs/secciones | Varias queries independientes en misma pantalla | +1pt por tab extra |

### Paso 4: Generar tabla de estimación

Aplica las reglas de `sputnik-core`:
- Escala Fibonacci 0/1/2/3
- División si >3 puntos
- Estructura descriptiva inferida
- Descripción cliente humanizada
- Subtotales por capa + total general

### Paso 5: Mostrar y preguntar

Muestra la tabla generada y pregunta:
1. "¿Faltan pantallas o funcionalidades no visibles en la maqueta?"
2. "¿Hay integraciones externas (Azure, correo, APIs) que la maqueta no muestra?"
3. "¿El flujo incluye validaciones de negocio no evidentes (ej: exclusividad, límites)?"

Si el usuario agrega información, actualiza la estimación.

### Paso 6: Ofrecer pipeline

```
✅ Estimación generada:
- SQL: 8 tareas (14 pts)
- Backend: 6 tareas (10 pts)
- Frontend: 9 tareas (15 pts)
TOTAL: 23 tareas, 39 puntos, 78 horas

¿Quieres...?
1. Exportar a Excel → sputnik-excel
2. Subir issues a Jira → sputnik-jira
3. Refinar algún punto
```

---

## Lo que NO debe hacer

- No inventar elementos que no están en la maqueta. Si un botón dice "Exportar" → inferir endpoint. Si no hay botón de exportar → no inferirlo.
- No asumir reglas de negocio invisibles. Preguntar si hay validaciones cross-field, exclusividad, límites.
- No estimar SPs que no tienen representación visual (ej: jobs nocturnos, migraciones). Preguntar al usuario.
