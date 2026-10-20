---
name: scalar-api-docs
description: Reemplaza la UI de Swagger (Swashbuckle SwaggerUI o la UI nativa de Microsoft.AspNetCore.OpenApi) por Scalar como vista interactiva de la API en los backends .NET de FaaST, sin tocar la generación del documento OpenAPI. Cubre el árbol de decisión según qué genera hoy el OpenAPI (Swashbuckle clásico de 1 o N documentos, generador nativo net9+, gateway Ocelot/YARP), la instalación y configuración real del paquete Scalar.AspNetCore, la regla de versión única desde version.txt, el catálogo de errores y el checklist de verificación. Usala durante la migración a .NET 10 de cualquier backend legado, o cuando haya que exponer documentación interactiva de una API nueva.
---

# Scalar como UI de documentación de API

> **ESTADO: ACTIVA (estándar de Plataforma FAAST, 2026-09-22).** Validada con los pilotos
> reales de apiback y micro-backoffice. Es un **paso dentro de** la skill `migrar-dotnet`
> (Fase 3.5), no un proyecto aparte. Se coordina con `dockerizar-componente` (Paso 4.5 —
> versión interna) y con ADR-039.
>
> **En dev-team:** la carga el agente `backend` (en una migración de TFM o al exponer la
> documentación de una API nueva .NET); `tech-writer` y `qa-backend` consumen el mismo
> documento OpenAPI. Plantillas en `${CLAUDE_PLUGIN_ROOT}/skills/scalar-api-docs/templates/`.

**Requerimiento de Plataforma FAAST (2026-09-22):** en la migración a .NET 10 de todos los
backends legado, dejar de usar la UI de Swagger y usar **Scalar** como extensión de
documentación interactiva de la API. En una API nueva (.NET 9+ con el generador nativo
`AddOpenApi()`), Scalar es la UI por defecto (rama B del árbol).

---

## Qué hace

Cambia **la vista**. Nada más.

```
ANTES:  [controllers] → [Swashbuckle genera swagger.json] → [SwaggerUI lo dibuja]
DESPUÉS:[controllers] → [Swashbuckle genera swagger.json] → [Scalar lo dibuja]
                         └──────── INTACTO ────────┘         └── lo único que cambia ──┘
```

## Qué NO hace

- **No cambia el generador de OpenAPI.** No se migra Swashbuckle a
  `Microsoft.AspNetCore.OpenApi` en el mismo paso. Son dos cambios distintos y el
  segundo cambia el **contenido** del documento (el contrato), no solo la vista.
- **No cambia rutas del documento.** `/swagger/{documentName}/swagger.json` se queda
  donde está: lo consumen gateways, colecciones de Postman y el
  `snapshot-contrato.sh` de `migrar-dotnet`. Scalar **apunta** a esa ruta.
- **No toca el contrato.** Los paths, schemas y security schemes salen del mismo
  generador de antes. Si el diff de OpenAPI cambia, algo se hizo mal.
- **No instala Scalar en gateways que no generan OpenAPI propio.** Ver §Árbol, rama C.
- **No habilita la documentación en producción.** La política de exposición por
  ambiente es la decisión abierta D-2 (§Decisiones pendientes).

---

## Reglas duras

1. **Un solo cambio por PR: la UI.** Reemplazar la UI y de paso migrar el generador,
   agregar documentos o retocar el contrato es el error que hace que un diff de
   OpenAPI no se pueda interpretar.
2. **El documento OpenAPI no se regenera ni se mueve.** Scalar consume las rutas que
   ya existen. Si hay que crear una ruta nueva para que Scalar funcione, se paró en
   la rama equivocada del árbol.
3. **La versión que muestra Scalar sale de `version.txt`, la misma fuente que
   `/health`.** Ver §La versión. Es la regla que más se rompe y la más fácil de
   verificar.
4. **`/scalar` es la convención de ruta** para toda la flota. Un componente que la
   cambie lo justifica en su informe.
5. **Nada de credenciales precargadas en la UI fuera de local.** Los
   `AddHttpAuthentication(... auth.Token = "ey...")` quedan **visibles en el
   navegador** — la propia documentación de Scalar lo marca como *CAUTION* [V]. En
   FaaST: prohibido en cualquier ambiente compartido.
6. **Si el componente hace auth, el review de cybersec de `migrar-dotnet` §Regla 8
   incluye esta ruta.** Exponer `/scalar` sin `AllowAnonymous` rompe la
   documentación; exponerla **con** `AllowAnonymous` en un ambiente público expone
   el mapa completo de la API. Se decide, no se hereda.
7. **SwaggerUI y Scalar pueden convivir durante la migración, pero con fecha.** La
   coexistencia es para comparar; se quita SwaggerUI en el mismo PR que cierra la
   migración del componente.

---

## La versión: una sola fuente, `version.txt`

> **REGLA DURA (Plataforma FAAST, 2026-09-22).** Todo endpoint o vista que muestre la versión
> del componente — `/health`, el `Info.Version` del documento OpenAPI que dibuja
> Scalar, y cualquier otra — lee **el mismo `version.txt` del repo**, en runtime,
> idealmente vía un helper compartido cacheado (`VersionInfo.Current`).

- **Nunca** un string hardcodeado (`Version = "1.0.0"` deja la UI congelada en esa
  cadena para siempre).
- **Nunca** `AssemblyInformationalVersion` inyectado por `ARG VERSION`/`-p:` como
  fuente de la app. Un `ARG VERSION` en el Dockerfile, si existe, sirve solo para
  **taguear la imagen** en el registro/CI.
- **Nunca** dos lecturas separadas del mismo archivo. Dos mecanismos se
  desincronizan; uno cacheado, no.

**Por qué es una regla y no una preferencia:** este es exactamente el defecto que se
encontró en apiback el 2026-09-22 — `Info.Version` de los dos `SwaggerDoc(...)` leía
`File.ReadAllText(..., "version.txt")` por su cuenta mientras `/health` leía otra
fuente. Misma palabra "versión", dos números posibles, y el que mira la
documentación no tiene forma de saber cuál de los dos es el desplegado.

Helper de referencia: `templates/VersionInfo.cs`. Precedente real ya en el código:
`Cloud.Faast.Back.Common.VersionInfo.Current` en apiback, y el comentario de
`faast-identidad-y-acceso/src/Identidad.Api/Program.cs` ("un solo punto de lectura de
version.txt, nunca dos mecanismos leyendo el mismo archivo por separado").

**Verificación (obligatoria, en el checklist):** con el contenedor levantado,
`/health` y el `info.version` del documento que sirve Scalar devuelven **la misma
cadena**, y esa cadena es el contenido de `version.txt`. Un solo comando:
`templates/verificar-scalar.sh`.

---

## Árbol de decisión

**La pregunta es una sola: ¿qué genera hoy el documento OpenAPI de este componente?**
Se contesta leyendo `Program.cs`/`Startup.cs`, no suponiendo.

```bash
grep -n "AddSwaggerGen\|UseSwagger\|MapSwagger\|AddOpenApi\|MapOpenApi\|SwaggerForOcelot\|AddOpenApiDocument" \
  $(find . -name Program.cs -o -name Startup.cs | grep -v /obj/)
```

| Lo que encontrás | Rama | Qué aplica |
|---|---|---|
| `AddSwaggerGen` + `UseSwagger` + **un** `SwaggerDoc`/documento por defecto | **A1** | Scalar con `WithOpenApiRoutePattern` apuntando a la ruta que ya sirve Swashbuckle |
| `AddSwaggerGen` + **varios** `SwaggerDoc(name: ...)` | **A2** | Igual que A1 + un `AddDocument(...)` por documento |
| `AddOpenApi()` + `MapOpenApi()` (net9+ nativo) | **B** | El caso simple: `MapScalarApiReference()` casi sin opciones |
| `AddSwaggerForOcelot` / `UseSwaggerForOcelotUI` (Ocelot agregador) | **C1** | Aplica, apuntando a los docs agregados. Decisión abierta D-3 |
| Gateway (Ocelot/YARP) **con** su propio `AddSwaggerGen` de sus controllers | **C2** | Es A1/A2. Ojo con el alcance: documenta el gateway, no lo proxeado |
| Gateway **sin** ningún generador de OpenAPI | **C3** | **N/A — no se instala Scalar.** Parar acá |
| `AddOpenApiDocument` (NSwag) | **D** | Aplica; patrón en `reference/02-api-verificada.md` §6. Ninguno en la flota hoy |

**La rama C3 es una respuesta legítima y frecuente.** Un gateway que solo enruta no
tiene documento propio que dibujar; instalarle Scalar produce una UI vacía o, peor,
una que dice "no hay endpoints" sobre una API que sí existe. En el inventario: los
Ocelot net5 (`gw-crm`, `gw-reporting`, `gw-security`) están en C3 hasta que migren.

Detalle de cada rama, con el código exacto: **`reference/01-arbol-decision.md`**.
Casos reales ya resueltos contra los repos: **`reference/04-casos-reales.md`**.

---

## Procedimiento

### Paso 1 — Clasificar (5 min, solo lectura)

Corré el `grep` de arriba y ubicá el componente en una rama del árbol. Anotá:

| Dato | De dónde sale |
|---|---|
| Generador de OpenAPI | El `grep` |
| **Ruta(s) real(es)** del documento | El `RouteTemplate` de `UseSwagger`, o el default |
| Nombres de los documentos | Los `SwaggerDoc(name: ...)` / `AddOpenApi("v1")` |
| Cómo se lee hoy la versión | `grep -rn "version.txt\|InformationalVersion"` |
| ¿Hay ReDoc u otra UI? | `grep -rn "UseReDoc\|ReDoc"` |
| ¿Hay política de auth global? | `FallbackPolicy`, `RequireAuthenticatedUser` |

**El default de Swashbuckle no es el default de Scalar.** Swashbuckle sirve en
`/swagger/{documentName}/swagger.json`; Scalar busca en
`/openapi/{documentName}.json` [V]. **Si no se corrige esto, la UI carga y queda
vacía** — es el error #1 del catálogo (E-SC-01).

### Paso 2 — Instalar el paquete

```bash
dotnet add <Proyecto>.csproj package Scalar.AspNetCore
```

MIT, sin dependencias transitivas, `net8.0;net9.0;net10.0` en el mismo paquete [V].
**Se pinea la versión** y se anota en el informe. Ver `reference/02-api-verificada.md` §1.

### Paso 3 — Reemplazar SOLO la UI

Tomá la plantilla de la rama que te tocó:

| Rama | Plantilla |
|---|---|
| A1 / A2 | `templates/scalar-swashbuckle.cs` |
| B | `templates/scalar-nativo.cs` |
| C1 | `templates/scalar-ocelot-agregado.cs` |

Se **borra** el bloque `UseSwaggerUI(...)` y se **deja intacto** `UseSwagger()` (es
el que sirve el JSON). Confundir los dos y borrar `UseSwagger()` deja a Scalar sin
documento y rompe además a los consumidores del contrato.

**ReDoc y cualquier otra vista existente se dejan como están** — decisión abierta
D-1, pendiente del responsable de plataforma (si no está registrada en el proyecto, se
pregunta al usuario; no se decide en silencio).

### Paso 4 — Unificar la versión

Aplicá §La versión. En Swashbuckle es el `Version` de cada `OpenApiInfo`; en el
generador nativo es un `AddDocumentTransformer` que setea `document.Info.Version`
(`reference/02-api-verificada.md` §4). Si el componente todavía no tiene el helper,
`templates/VersionInfo.cs`.

### Paso 5 — Verificar

```bash
./templates/verificar-scalar.sh http://localhost:18080 BackOffice GestionCobranza
```

Comprueba las 6 cosas del checklist que se pueden automatizar: build, `/scalar`
devuelve HTML real (no un 302 ni un JSON), cada documento carga, `info.version`
coincide con `/health` y con `version.txt`, y que el contrato **no** cambió.

`curl /scalar` sin `-L` devuelve un **redirect a `/scalar/`** [V] — un "200 OK" que
no llega nunca es el falso negativo más común de esta verificación.

### Paso 6 — Cerrar

1. Completá `reference/checklist.md`. Cualquier "no" bloquea.
2. Diff de contrato (`comparar-respuestas.sh` de `migrar-dotnet`): **debe dar vacío**.
3. Handoff al lead con la rama del árbol, la ruta, la versión verificada en los dos
   lados, y qué se decidió sobre ReDoc/SwaggerUI.
4. Si toca auth: handoff a cybersec **antes** del cutover (Regla 6).

---

## Cuando algo falla

**`reference/03-catalogo-errores.md`**: `síntoma → causa → fix → cómo verificar`, con
código citable (`E-SC-01` … `E-SC-09`). Los cinco que aparecen siempre:

| Código | Síntoma |
|---|---|
| `E-SC-01` | La UI carga pero está vacía / "Failed to fetch the OpenAPI document" |
| `E-SC-02` | La UI queda en blanco y la consola dice `getBasePath is not defined` |
| `E-SC-03` | `/scalar` devuelve 301/302 y el script de verificación lo cuenta como fallo |
| `E-SC-04` | Scalar no muestra ningún botón de autenticación |
| `E-SC-05` | Scalar muestra una versión distinta a `/health` |

`E-SC-02` está **verificado contra un repo de FaaST** (`faast-identidad-y-acceso`,
QA 2026-07-23): la causa raíz y el fix están documentados en el propio `Program.cs`.

---

## Decisiones pendientes (de Plataforma)

Las toma el responsable de plataforma del proyecto. Antes de actuar sobre una de ellas,
mirá si ya quedó registrada (wiki/decisiones del proyecto); si no, registrá
`esperando_usuario` con la pregunta y seguí con el comportamiento por defecto de la skill.

| # | Decisión | Estado |
|---|---|---|
| **D-1** | **¿Se saca también ReDoc** donde exista, o convive con Scalar? La skill hoy **lo deja intacto** | Pendiente |
| **D-2** | **¿En qué ambientes se expone `/scalar`?** Hoy varios componentes tienen la UI solo en `IsDevelopment()`. Si se quiere en QA/Stage, es una decisión de exposición, no técnica | Pendiente |
| **D-3** | **Gateways Ocelot con `SwaggerForOcelot`** (`gw-contabilidad`): ¿se reemplaza la UI agregadora por Scalar, o se deja porque el valor está en la agregación y no en la vista? | Pendiente |
| **D-4** | ¿Se quita SwaggerUI en el mismo PR (Regla 7) o se deja un período de convivencia con fecha de corte? | Pendiente |

---

## Archivos de esta skill

```
scalar-api-docs/
├── SKILL.md                        (este archivo — el procedimiento)
├── reference/
│   ├── 01-arbol-decision.md        cada rama con su código exacto
│   ├── 02-api-verificada.md        API real del paquete, [V] contra la fuente
│   ├── 03-catalogo-errores.md      E-SC-01 … E-SC-09
│   ├── 04-casos-reales.md          apiback · identidad · gw-contabilidad · gw-backoffice
│   └── checklist.md                se completa por componente
└── templates/
    ├── scalar-swashbuckle.cs       ramas A1/A2 (1 o N documentos)
    ├── scalar-nativo.cs            rama B (net9+ nativo)
    ├── scalar-ocelot-agregado.cs   rama C1
    ├── VersionInfo.cs              helper de versión única
    └── verificar-scalar.sh         Paso 5
```

**Leyenda de verificación, usada en todos los archivos:**
**[V]** verificado contra la fuente real (nuget.org, el código de `scalar/scalar`, o
un repo de FaaST — con la cita al lado) · **[G]** conocimiento general sin verificar.

**Relacionados:** skills del plugin `migrar-dotnet` (Fase 3.5) ·
`dockerizar-componente` (Paso 4.5 — versión interna) · `deployment-standard` (versión por
`version.txt`) · `ingenieria-faast` (estándares de API) · en la coordinación del proyecto,
si existe: `inventario/asis-repos-legado.md`
