---
name: crear-tests-backend
description: Analiza la testabilidad de un backend .NET de FaaST (cualquier TFM de netcoreapp3.x a net10, cualquier patrón) y crea desde cero su proyecto de tests — mapa de endpoints y dependencias, qué se puede probar sin infraestructura y qué no, tests de caracterización que se escriben ANTES de migrar y deben pasar igual antes y después, unitarios de negocio, integración con WebApplicationFactory + Testcontainers, contrato contra QA en solo lectura, stack y licencias verificadas, plantillas, scaffold, CI con cobertura por riesgo y catálogo de errores. Usala cuando un repo no tenga tests, antes de migrar de TFM, o cuando la suite existente no corra en CI.
---

# Crear tests para un backend .NET de FaaST

> **ESTADO: ACTIVA (estándar de Plataforma FAAST, 2026-09-22).** Validada con los pilotos
> reales de apiback y micro-backoffice. Acompaña a **ADR-018** (stack de tests y licencias)
> y es la **precondición** de la skill hermana **`migrar-dotnet`** (ADR-017): los tests de
> caracterización se escriben en el TFM actual, y la migración no los toca.
>
> **En dev-team:** la carga el agente `backend` (y `qa-backend` la consulta para la suite de
> contrato). Es el detalle .NET de la estrategia de pruebas por capa de la skill
> **`ingenieria-faast`** (que cubre los demás stacks). Las plantillas viven en
> `${CLAUDE_PLUGIN_ROOT}/skills/crear-tests-backend/templates/`. `COORD` es la **ruta
> absoluta de la carpeta de coordinación del proyecto** (fuera de los repos), la que indica
> el coordinador; si no la tenés, se pide — nunca se inventa ni se apunta dentro de un repo.

## El problema que existe

**44 de 61 repos backend de la flota no tienen ningún proyecto de test [V]** (`migrar-dotnet`
`reference/03-plan-de-pruebas` §0). `micro-api-back` es uno de ellos: cero proyectos de
test en `v2.0.33`, y su `CI.yml` de `develop_docker` corre `dotnet test` **en vacío y
pasa** — una señal falsa que es peor que no tener nada [V].

Sin tests, la única red de seguridad de una migración es el snapshot de contrato contra
el ambiente. Funciona, pero es manual, exige el ambiente arriba y no corre en CI.
**Esta skill construye la red que falta.**

## Qué hace

Te lleva de "este repo no tiene un solo test y hay que migrarlo de TFM" a "hay una suite
que corre en CI, en local sin más infraestructura que Docker, que cubre lo que puede
romperse con plata de por medio, y que pasa **idéntica** antes y después de la migración".

## Qué NO hace

- **No escribe en repos de código.** Genera el árbol de tests en la carpeta de salida de
  la coordinación; el ingreso al repo va por el flujo de ramas de ADR-039, como todo.
- **No refactoriza el código para hacerlo testeable.** Un refactor "para poder testear"
  dentro del mismo PR que los tests es exactamente el cambio que los tests deberían estar
  vigilando. Los cambios de testabilidad se listan, se estiman y se deciden aparte (§4).
- **No persigue un porcentaje de cobertura.** Ver `reference/05-ci-cobertura-dod.md`.
- **No reemplaza a QA.** QA valida funcionalmente con capturas; la suite es para el
  desarrollador y para el CI.
- **No toca datos de producción ni de un ambiente de escritura.** Ver regla 5.
- **No decide la política de calidad de la flota.** Eso es ADR-018 + ADR-015 (SonarQube).

---

## Reglas duras

Si una se rompe, se para y se avisa.

1. **Los tests de caracterización se escriben ANTES de tocar el `.csproj`** y deben pasar
   en verde en el TFM **actual**. Un test de caracterización escrito después de migrar
   no caracteriza nada: describe el sistema nuevo.
2. **Durante una migración, los tests no se editan.** Ni el código de test, ni los
   snapshots, ni los `.verified.txt`. Si un test se pone rojo, el veredicto es "la
   migración cambió el comportamiento", no "hay que actualizar el test". Regenerar un
   snapshot durante una migración **borra la evidencia** y anula el trabajo.
3. **Un test que necesita un ambiente de FaaST para pasar no es un test**: es una prueba
   de humo. Vive en su propia categoría (`Contrato`), **no corre en CI por defecto** y
   nunca bloquea un PR.
4. **Cero secretos en el repo de tests.** Ni connection strings, ni JWT reales, ni
   `.env`, ni datos de clientes. Las claves de prueba se generan en el test. Lo que
   necesita un valor real se salta con `Skip` explícito.
5. **Contra un ambiente real: solo lectura, y solo QA.** Prohibido `POST/PUT/DELETE`
   contra cualquier ambiente desde la suite. Prohibido apuntar a Puente, Demo o
   producción de cliente, aunque sea un `GET`.
6. **El test que falla se investiga, no se `[Skip]`.** Un `Skip` sin motivo escrito y sin
   ticket es deuda invisible. El motivo va en el atributo, no en un comentario.
7. **Nada de `DateTime.Now` dentro de un test**, ni del lado del test ni esperando que el
   código lo devuelva. Si el código lo usa, el test lo congela o lo acota (§`T-TIME-01`).
8. **Si el componente hace autenticación, firma o cifra, la suite incluye los tests de
   ese punto** y pasa por el gate de cybersec antes de cerrarse. Los vectores de cifrado
   y los tokens de ejemplo se tratan como evidencia, no como datos de prueba cualquiera.
9. **Un test verde en la máquina y rojo en CI (o al revés) es un bloqueador**, no una
   curiosidad. Casi siempre es cultura, zona horaria o paralelismo (§4).

---

## Procedimiento

### Fase 0 — Encuadre (5 min)

```bash
export COORD="<ruta absoluta de la carpeta de coordinación>"   # la da el coordinador
export REPOS_DIR="<carpeta que contiene los clones de los repos>"
cd "${CLAUDE_PLUGIN_ROOT}/skills/crear-tests-backend"
set -a; . ./templates/parametros-tests.env; set +a
export REPO="micro-api-back"        # el componente (ejemplo)
```

Tres preguntas antes de escribir una línea:

| Pregunta | Por qué importa |
|---|---|
| ¿Para qué son estos tests: **migración**, **regresión** o **desarrollo nuevo**? | Define el orden. Para migración manda la caracterización (§2a) y todo lo demás puede esperar |
| ¿Qué es lo que **si se rompe cuesta plata**? | Es el orden de prioridad real (§`02-estrategia` §1), no "empezar por los controllers" |
| ¿Hay **ventana para cambios de testabilidad** o el código es intocable? | Determina si se puede llegar a integración o si el techo es unitario + contrato |

### Fase 1 — Análisis de testabilidad (solo lectura)

```bash
./templates/analizar-testabilidad.sh "$REPO"            # git grep sobre un ref, no compila
```

Produce el mapa: endpoints por controller, capas, dependencias (EF/HTTP/Hangfire/SMTP/
S3/JWT/reloj/archivos), qué está estático, qué se inyecta, y los bloqueadores conocidos
de `WebApplicationFactory`. Lo que el script **no** puede contestar —y vos sí— está en
**`reference/01-analisis-testabilidad.md`**.

**Salida de fase:** el componente queda clasificado en un carril de testabilidad.

| Carril | Criterio | Techo alcanzable sin tocar código |
|---|---|---|
| **Verde** | DI en todo, `Program` accesible, sin estáticos de configuración, sin conexión en el arranque | Unitarios + integración con `WebApplicationFactory` + Testcontainers |
| **Amarillo** | Config estática, o helpers `static`, o el arranque abre conexión a la BD | Unitarios de lo puro + caracterización por HTTP contra el ambiente. La integración necesita 1-3 cambios chicos listados y aprobados |
| **Rojo** | Todo el negocio vive dentro de los controllers o dentro de SQL crudo que el repo no tiene | Solo caracterización de contrato + unitarios del núcleo puro. **Decir esto de entrada, no descubrirlo en la semana 3** |

### Fase 2 — Elegir la estrategia por objetivo

**`reference/02-estrategia-y-prioridad.md`**. Las cinco familias, cuándo usar cada una y
qué **no** testear:

```
(a) Caracterización / red de seguridad ─ ANTES de migrar. Contrato OpenAPI, golden-file
                                          de respuestas, JSON, fechas/cultura/TZ, JWT,
                                          cifrado, SQL generado por EF
(b) Unitarios de negocio ────────────── cálculos, validaciones, formateo, reglas
(c) Integración ─────────────────────── WebApplicationFactory + Testcontainers (MySQL,
                                          SQL Server) · SQLite/InMemory con sus límites
(d) Contrato contra QA ──────────────── solo lectura, fuera del CI, para lo que no se
                                          puede reproducir localmente
(e) Lo que NO se testea ─────────────── DTOs, Swagger, librerías de terceros, SPs,
                                          y el porcentaje por el porcentaje
```

**El orden de escritura no es el orden de la pirámide: es el orden del riesgo.**
Auth → dinero y cálculos → cifrado → jobs → el resto.

### Fase 3 — Stack

**`reference/03-stack-y-licencias.md`** tiene las versiones y **las licencias
verificadas en nuget.org el 2026-09-21**, con el detalle que más caro sale ignorar:

> **FluentAssertions 8.x es licencia comercial** (`requireLicenseAcceptance=true`,
> `projectUrl` de Xceed) [V]. **7.2.0 es la última Apache-2.0** [V]. Una suite nueva que
> arranque con `FluentAssertions` último **compromete a la empresa con una licencia paga**.
> Por eso el default de esta skill es **Shouldly** (BSD-3) [V].

Misma lógica que la regla 6 de `migrar-dotnet`: **el paquete no se elige por ser el más
nuevo, se elige por versión fijada y licencia leída**.

### Fase 4 — Scaffold

```bash
./templates/scaffold-tests.sh "$REPO"       # escribe en $SALIDA, NUNCA en el repo
```

Genera el árbol, los `.csproj` con las versiones de `parametros-tests.env`, la
`WebApplicationFactory` base con override de configuración **por variables de entorno**
(regla de la casa: todo el `appsettings` a variables), los fixtures de Testcontainers y
los cuatro tests de caracterización que aplican a casi cualquier componente FaaST
(OpenAPI, JWT, cifrado, fechas/cultura).

**Convención, no negociable:**

```
<repo>/
└── tests/                                   ← siempre "tests/", siempre en el repo
    ├── <Proyecto>.Tests.Unit/               sin infra, siempre en CI
    ├── <Proyecto>.Tests.Caracterizacion/    sin infra, siempre en CI, no se edita al migrar
    ├── <Proyecto>.Tests.Integracion/        Docker (Testcontainers), en CI si hay runner
    └── <Proyecto>.Tests.Contrato/           contra QA, NUNCA en CI por defecto
```

Rama de trabajo: la del componente (`develop_docker_net10` en `micro-api-back`).
Nombres de test: `Metodo_Escenario_ResultadoEsperado`, en español, sin abreviar.

### Fase 5 — Escribir, en el orden del riesgo

1. **Núcleo puro primero.** Es el que da tests en minutos y el que más usa el negocio:
   formateo de montos y fechas, cifrado, utilidades. Casi siempre es `static` y casi
   siempre es testeable **hoy**, sin tocar nada.
2. **Auth.** Emisión y validación de token, token expirado, token firmado con otra clave,
   arranque sin clave. Gate de cybersec.
3. **Dinero.** Todo cálculo que termine en un monto, una tasa o un asiento contable.
4. **Contrato.** Snapshot de OpenAPI y golden-file de las respuestas de los endpoints que
   el negocio usa.
5. **El resto**, si sobra tiempo. Casi nunca sobra, y está bien.

### Fase 6 — CI y cierre

**`reference/05-ci-cobertura-dod.md`** + `templates/ci-tests.yml`.

1. `dotnet test` de Unit + Caracterización en cada PR. Sin secretos, sin ambiente.
2. Integración solo si el runner tiene Docker; si no, se marca como gap, no se borra.
3. **Cobertura por riesgo, no por porcentaje global.** El gate es una lista de módulos.
4. Completá `reference/checklist.md`. Cualquier "no" bloquea.
5. Informe desde `templates/informe-testabilidad.md` a `{coordinacion}/inventario/tests/<repo>.md`.
6. Handoff al lead con: carril, qué quedó cubierto, qué **no** y por qué, cambios de
   testabilidad pedidos, y los `Skip` que quedaron con su motivo.

---

## §4 — Los cambios de testabilidad: qué se pide y cómo

Casi ningún componente legado de FaaST arranca bajo `WebApplicationFactory` sin **un**
cambio. Esta skill los trata como una lista corta, explícita y aprobable, nunca como un
refactor silencioso dentro del PR de tests.

| Cambio | Tamaño | Riesgo de comportamiento | Cuándo se pide |
|---|---|---|---|
| `public partial class Program { }` al final de `Program.cs` | 1 línea | **Ninguno** — no cambia el pipeline | Siempre que se quiera integración con minimal hosting |
| `ServerVersion.Parse(...)` en vez de `AutoDetect(...)` cuando hay una variable declarada | 1-3 líneas | Bajo, pero **cambia el arranque**: va con su propio test | Si el arranque abre conexión a MySQL (`T-DB-02`) |
| Inicializar la configuración estática desde `IConfiguration` | 1 archivo | Medio — es el fix que ya existe en Stage para `micro-api-back` | Si hay un `ConfigurationBuilder` privado leyendo el `appsettings` (`T-CFG-01`) |
| Inyectar un reloj (`TimeProvider`) donde hay `DateTime.Now` | N archivos | **Alto, es refactor** | **No se pide dentro de esta skill.** Se acota con caracterización (`T-TIME-01`) |

**Regla:** los dos primeros son aditivos y se proponen junto con la suite. El tercero es
del PR de configuración. El cuarto **no se hace acá**.

---

## §5 — Cómo se coordina con `migrar-dotnet`

Este es el motivo por el que existe la skill, y el orden no es negociable:

```
1. Tests de caracterización, escritos y VERDES en el TFM actual  ← esta skill
2. Commit propio, PR propio, mergeado ANTES de empezar la migración
3. Migración por escalones                                        ← skill migrar-dotnet
4. Los MISMOS tests, sin editar, verdes en el TFM destino         ← el DoD real
5. Dockerización                                                  ← skill dockerizar-componente
```

**Lo que está prohibido:** escribir los tests y migrar en el mismo PR. Un test rojo
después de un cambio combinado no distingue entre "el test estaba mal" y "la migración
rompió algo", que es justo la pregunta que los tests existen para contestar.

**El TFM del proyecto de test sigue al de la app, en el mismo escalón** (es `E-CS-03` del
catálogo de `migrar-dotnet`: `gw-mobile-fintec` tiene app net8 y test net10, y no compila
la solución [V]). El código de los tests no cambia; cambia una propiedad del `.csproj`.

---

## §6 — Archivos de esta skill

```
crear-tests-backend/
├── SKILL.md                              (este archivo — el procedimiento)
├── reference/
│   ├── 01-analisis-testabilidad.md       qué mirar, cómo clasificar, dependencias
│   ├── 02-estrategia-y-prioridad.md      las 5 familias, prioridad por riesgo, qué NO
│   ├── 03-stack-y-licencias.md           versiones y licencias verificadas en nuget.org
│   ├── 04-catalogo-errores-tests.md      error → causa → fix → verificación (códigos T-*)
│   ├── 05-ci-cobertura-dod.md            CI sin secretos, cobertura por riesgo, DoD
│   ├── 06-aplicacion-micro-api-back.md   el plan concreto para apiback v2.0.33
│   └── checklist.md                      se completa por componente
└── templates/
    ├── parametros-tests.env              ← las versiones de paquetes se definen acá
    ├── analizar-testabilidad.sh          Fase 1, solo lectura
    ├── scaffold-tests.sh                 Fase 4, escribe fuera del repo
    ├── Directory.Build.props.tests       TFM + política común de los proyectos de test
    ├── Tests.Unit.csproj                 unitarios y caracterización
    ├── Tests.Integracion.csproj          + Mvc.Testing + Testcontainers
    ├── FaastWebApplicationFactory.cs     override de config por variables de entorno
    ├── TestcontainersFixture.cs          MySQL y SQL Server en Docker
    ├── NucleoPuroTests.cs                unitarios del núcleo estático
    ├── CaracterizacionOpenApiTests.cs    snapshot del contrato
    ├── CaracterizacionRespuestasTests.cs golden-file de respuestas
    ├── JwtCaracterizacionTests.cs        emisión/validación, token de oro
    ├── CifradoGoldenTests.cs             vectores de cifrado
    ├── FechasCulturaTests.cs             cultura, TZ, parseo y formato
    ├── ContratoQaTests.cs                contra ambiente, solo lectura, fuera de CI
    ├── coverage.runsettings              cobertura con exclusiones
    ├── ci-tests.yml                      workflow sin secretos, con gate por riesgo
    └── informe-testabilidad.md           el entregable por componente
```

**Piloto recomendado:** `micro-api-back` (`reference/06-aplicacion-micro-api-back.md`).
Es el único componente con análisis previo completo, va a migrar a net10, y su núcleo
`Cloud.Faast.Core` da tests en verde el primer día sin tocar una línea de producción.

**Leyenda de confianza, igual que en `migrar-dotnet`:**
**[V]** verificado (comando, `git grep` sobre el repo real, o API de nuget.org el
2026-09-21) · **[G]** conocimiento general de la plataforma, a confirmar en el piloto.

**Relacionados:** ADR-018 (este stack) · ADR-017 (destino .NET) · ADR-016 (dockerización) ·
ADR-015 (SonarQube) · skills del plugin `ingenieria-faast` (estrategia de pruebas por capa,
todos los stacks) · `migrar-dotnet` · `dockerizar-componente` · `scalar-api-docs` ·
`{coordinacion}/inventario/analisis-previo-apiback-net10.md` (si existe en el proyecto)
