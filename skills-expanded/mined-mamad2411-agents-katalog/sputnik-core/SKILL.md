---
name: sputnik-core
description: "Estimador de tareas del equipo Sputnik (Fibonacci 0/1/2/3): genera tabla de issues por capa (SQL + Backend + Frontend) para Jira o Excel. Úsala para cotizar, estimar o desglosar un proyecto, sprint o módulo."
metadata:
  requires-devkits: auto-detect
---
 
# Sputnik Core — Estimación Fibonacci
 
Estimador de tareas para el equipo de desarrollo **Sputnik**. Genera una tabla de issues con puntos siguiendo exactamente las reglas del equipo. **No improvises ni uses otras escalas.**
 
## Stack estándar

- **Web**: SQL Server / .NET 10 / React + Vite + Ant Design (ver `react-antdesign`) o shadcn/ui + Tailwind 4.3 (ver `react-components`)
- **Móvil**: SQL Server / .NET 10 / Flutter
En ambos casos las capas son **SQL + Backend + Frontend** (en móvil el Frontend es Flutter).

## Integración con dev-kits

Antes de estimar, carga los dev-kits relevantes para el proyecto:
- **SQL Server** → `sql-server-core`, `sql-server-performance`, `sql-server-procedural`
- **PostgreSQL** → `postgresql-core`, `postgresql-performance`, `postgresql-procedural`
- **Backend .NET** → `dotnet-core`, `dotnet-api`, `dotnet-ef-core`
- **Backend Node.js** → `nodejs-core`, `nodejs-express`, `nodejs-database`
- **Backend Python** → `python-core`, `python-fastapi`, `python-database`
- **Frontend React + Ant Design** → `react-core`, `react-antdesign`
- **Frontend React + Tailwind** → `react-core`, `react-components`

Los dev-kits informan la estimación:
- Saber que un BRIN index en PostgreSQL es 1pt y un GIN particionado es 3pt (`postgresql-performance`)
- Saber que un endpoint GET sin lógica especial es 1pt y un POST con transacción + integración externa es 3pt (`dotnet-api`)
- Saber que un ProTable con filtros remotos es 2pt y una pantalla con formulario + tabla + drawer es 3pt (`react-antdesign`)
 
## Escala de puntos (Fibonacci, máximo 3)
 
| Puntos | Significado | Tiempo |
|---|---|---|
| **0** | Sin código. Tareas administrativas, juntas, seguimientos, configuraciones mínimas, cambios de un parámetro. | — |
| **1** | Tarea simple y bien entendida. SP de consulta directa, endpoint GET sin lógica especial, componente UI básico sin estado. | < 2 horas |
| **2** | Algo de complejidad. Lógica condicional, más de una tabla involucrada, componente con estado o validaciones, integración sencilla con servicio externo. | 2-4 horas |
| **3** | Complejidad media-alta. Lógica de negocio relevante, transacciones, integraciones con efectos secundarios (Azure, correo, etc.), CTE recursivo, componente con múltiples responsabilidades. **MÁXIMO PERMITIDO.** | 4-6 horas |
 
## Regla de división (obligatoria)
 
Si una tarea requeriría **5 o más puntos**, NO se puede estimar así. Debe dividirse en sub-tareas de máximo 3 puntos cada una.
 
- Cada sub-tarea inicia con `[DIVISION]` y especifica qué parte concreta cubre.
- En la justificación indica `División X/Y` y qué cubre esa parte.
- Ejemplo: tarea de 8 pts → `[DIVISION] parte A` (3 pts) + `[DIVISION] parte B` (3 pts) + `[DIVISION] parte C` (2 pts).
## Capas y tipos de actividad
 
### SQL
- `Se crea DB` → Creación de base de datos o schema
- `Se crea tabla SQL` → Creación de una tabla
- `Se realiza SP` → Creación de un stored procedure
### Backend (.NET 10)
- `Se crea archivo BackEnd` → Servicio, infraestructura, clase de utilidad
- `Se crea Consulta BackEnd` → Endpoint GET
- `Se crea Alta BackEnd` → Endpoint POST
- `Se crea Cambio BackEnd` → Endpoint PUT/PATCH
- `Se crea Baja BackEnd` → Endpoint DELETE
### Frontend (React web / Flutter móvil)
- `Se crea Pantalla FrontEnd` → Página o vista principal
- `Se crea Tabla FrontEnd` → Componente tabla/lista con datos
- `Se crea/modifica submenu` → Componente secundario reutilizable
- `Se crea Alta FrontEnd` → Flujo de creación de registro
- `Se crea Cambio FrontEnd` → Flujo de edición de registro
- `Se crea Baja FrontEnd` → Flujo de eliminación
- `Se crea/modifica CSS` → Estilos, temas, configuración visual
## Estructura descriptiva
 
Identificador técnico de la tarea:
 
- **SQL**: `[NombreConexión].[BaseDatos].[Schema].[NombreObjeto]`
- **Backend**: `[NombreProyecto].[Controlador/Servicio].[Método]`
- **Frontend**: `[NombreProyecto].[Componente].[Acción/Función]`
## Criterios para asignar puntos
 
**Suben el puntaje:**
- Lógica de negocio adicional (validaciones, reglas, exclusividad)
- Transacciones (BEGIN TRAN / rollback / COMMIT)
- Integración con servicios externos (Azure Blob, correo, APIs terceros)
- Queries cross-database (`[OtraDB].[dbo].[Tabla]`)
- CTE recursivo o queries complejos con múltiples JOINs
- Manejo de archivos (subida, descarga, conversión)
- Múltiples responsabilidades en un mismo componente
- Efectos secundarios (borrar blob al actualizar, invalidar caché)

**Bajan el puntaje:**
- Es copia/adaptación de algo ya existente en el mismo proyecto
- SP de consulta simple sin lógica especial
- Endpoint que solo delega al SP sin transformación
- Componente UI sin estado ni validaciones
- Configuración sin código (variables de entorno, rutas)

**Auto-detección de división implícita:**
Si una tarea de 3 puntos toca 3+ tablas, 2+ APIs externas, o mezcla múltiples dominios de negocio, sugiere división en sub-tareas aunque el puntaje técnico sea 3. La complejidad implícita prima sobre el puntaje explícito.
## Justificación
 
Cada tarea lleva una justificación breve (**máx. 15 palabras**) que explique por qué merece ese puntaje. Si fue dividida, indica `División X/Y` y qué cubre esa parte.
 
## Descripción para cliente

Además del identificador técnico, cada tarea DEBE incluir una **descripción humanizada** para el cliente, sin jerga técnica. Piensa: ¿qué valor entrega esto al usuario final?

**Reglas para la descripción de cliente:**
- **Nada de nombres técnicos**: nada de `usp_`, `dbo.`, `Controller`, endpoints, nombres de tablas.
- **Lenguaje de negocio**: describe la funcionalidad en términos del problema que resuelve.
- **Una frase clara**: máximo ~20 palabras, que cualquier persona sin background técnico entienda.
- **Empieza con verbo**: "Creación de...", "Desarrollo de...", "Configuración de...", "Integración de..."

**Mapeo de ejemplos:**

| Estructura Descriptiva (técnico) | Descripción Cliente (humanizado) |
|---|---|
| `SSA.ins.usp_ObtenerIdsClase` | Creación de motor de base de datos para consulta de identificadores de clase |
| `SSA.dbo.Universo_RevisionCapasCosto` | Creación de estructura de datos para el análisis de capas de costo |
| `SSA.ReporteController.GetRevisionCapasCosto` | Desarrollo de servicio de consulta para el reporte de revisión de capas de costo |
| `SSA.RevisionCapasCosto.ReportView` | Desarrollo de pantalla de visualización del reporte de revisión de capas de costo |
| `SSA.ClaseDropdown.FiltroIdClase` | Desarrollo de filtro por tipo de clase en el módulo de administración financiera |
| `SSA.ClaseDropdown.OpcionTodos` | Desarrollo de opción de consulta global en el selector de categorías |

## Formato de salida
 
Tabla con estas columnas en orden:
 
| Capa | Nombre Proyecto | Req. | Nombre Actividad | Estructura Descriptiva | Descripción Cliente | Puntos | Justificación |
 
**Reglas de formato:**
- Agrupa las tareas por capa: primero **SQL**, luego **Backend**, luego **Frontend**.
- Al final de cada grupo agrega una fila **SUBTOTAL** con conteo de tareas y suma de puntos.
- Al final de todo agrega una fila **TOTAL GENERAL**.
- Las tareas `[DIVISION]` aparecen justo debajo de donde iría la tarea original.
- El campo Req. se escribe como `Req. NNNNN` (ej. `Req. 00001`).
- No generes Excel salvo que el usuario lo pida explícitamente — la tabla en chat es la salida por defecto.
## Ejemplo de tarea dividida
 
❌ **Mal:**
 
| SQL | MiProyecto | Req. 00001 | Se realiza SP | MiDB.ins.usp_ComplexProc | 8 | SP muy complejo |
 
✅ **Bien:**
 
| SQL | MiProyecto | Req. 00001 | [DIVISION] Se realiza SP - Lógica principal | MiDB.ins.usp_ComplexProc | 3 | División 1/3: lógica de negocio central |
| SQL | MiProyecto | Req. 00001 | [DIVISION] Se realiza SP - Manejo de casos edge | MiDB.ins.usp_ComplexProc | 3 | División 2/3: validaciones y rollback |
| SQL | MiProyecto | Req. 00001 | [DIVISION] Se realiza SP - Integración cross-DB | MiDB.ins.usp_ComplexProc | 2 | División 3/3: JOIN a BD externa |
 
## Cuando el input es una maqueta (Figma/PDF/imagen/ClaudeAI Design)
 
Analiza la maqueta e infiere todas las tareas necesarias:
- Qué tablas y SPs de BD se necesitan
- Qué endpoints del backend los soportan
- Qué componentes del frontend los renderizan
Pide al usuario el **Nombre del proyecto** y **Req.** si no los proporcionó. Si menciona contexto adicional no visible en la maqueta (Azure Blob, cross-DB, reglas de exclusividad, etc.), incorpóralo a la estimación.

### ClaudeAI Design

**Formato**: link a `https://claude.ai/design/p/{uuid}`. ClaudeAI genera diseños como páginas HTML interactivas con mockups de UI, componentes, tablas, formularios, flujos y especificaciones de pantalla.

**Cómo analizarlo**:
1. Abrir el link con `agent_browser` y tomar snapshot + screenshot de la página completa.
2. Si el diseño tiene múltiples vistas/tabs, navegar por cada una y capturar.
3. El contenido HTML suele contener la especificación completa del diseño: componentes, layout, colores, estados.
4. Aplicar el mismo análisis de componentes que para una maqueta de Figma: identificar tablas, formularios, filtros, botones, charts, etc.

**Cuándo pedir credenciales**: Si el diseño requiere autenticación de Claude, pedir al usuario que comparta screenshots o exporte el diseño. Alternativamente, pedir que copie el contenido del diseño al chat.
 
## Workflow
 
1. **Recibe el input** (descripción del módulo, maqueta, lista de requerimientos).
2. **Si falta el nombre del proyecto o el Req., pregúntalo** antes de estimar.
3. **Infiere todas las tareas necesarias** por capa.
4. **Aplica las reglas** de puntuación y división.
5. **Devuelve la tabla** agrupada por capa con subtotales y total general.
6. **Pregunta al final**: "¿Quieres que suba estos issues a Jira?" Si dice que sí, carga la skill `sputnik-jira`. "¿Quieres exportar a Excel?" Si dice que sí, carga la skill `sputnik-excel`.

## Retrospectiva de estimación

Al final de cada sprint que usó esta estimación, sugiere revisar:

1. **¿Qué tareas se subestimaron?** (puntos reales > puntos estimados)
2. **¿Qué tareas se sobreestimaron?** (puntos reales < puntos estimados)
3. **¿Hubo divisiones que pudieron evitarse?** (tareas divididas que en retrospectiva eran una sola)
4. **¿Faltaron tareas?** (actividades que nadie estimó pero igual se hicieron)

Estas métricas alimentan la próxima estimación: si "SPs con transacción" consistentemente se estiman en 2 pero requieren 3, la skill ajusta automáticamente el criterio.
## Lo que NO debes hacer
 
- No uses puntos > 3 bajo ninguna circunstancia.
- No generes Excel automáticamente (solo si el usuario lo pide).
- No subas a Jira sin preguntar explícitamente.
- No improvises tipos de actividad fuera de la lista de cada capa.
- No omitas el subtotal por capa ni el total general.