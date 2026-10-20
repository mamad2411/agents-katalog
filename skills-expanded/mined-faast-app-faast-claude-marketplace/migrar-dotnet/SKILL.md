---
name: migrar-dotnet
description: Migra un componente backend .NET de FaaST desde su TargetFramework actual (netcoreapp3.0/3.1, net5, net6, net7, net8) al TFM destino de la flota, definido en templates/parametros.env. Cubre el análisis previo del csproj y sus dependencias, la ruta de saltos con sus breaking changes reales, el plan de pruebas sin tests, el catálogo de errores con su fix verificable, el rollback y la coordinación con la dockerización (ADR-016) y el modelo de ramas (ADR-039). Usala antes de dockerizar un componente EOL, cuando haya que subir de versión de .NET, o cuando una migración ya empezada esté fallando.
---

# Migrar un componente .NET de FaaST

> **ESTADO: ACTIVA (estándar de Plataforma FAAST, 2026-09-22).** Validada con los pilotos
> reales de apiback y micro-backoffice. Acompaña a **ADR-017** (destino de la migración) y
> se coordina con **ADR-016** (dockerización) y la skill hermana **`dockerizar-componente`**.
>
> **En dev-team:** la carga el agente `backend` cuando hay que subir de TFM (siempre a
> pedido: un agente nunca migra de versión por iniciativa propia). Precondición:
> **`crear-tests-backend`** (caracterización en verde en el TFM actual). Paso intermedio:
> **`scalar-api-docs`** (Fase 3.5). Paso siguiente: `dockerizar-componente` / estándar
> `deployment-standard` (lo ejecuta `infra`). Plantillas en
> `${CLAUDE_PLUGIN_ROOT}/skills/migrar-dotnet/templates/`; `COORD` es la ruta absoluta de la
> carpeta de coordinación del proyecto (fuera de los repos) que indica el coordinador.

## El parámetro que manda

**Esta skill no sabe a qué versión migrar. Lo lee de un archivo.**

```bash
set -a; . ./templates/parametros.env; set +a
echo "$TFM_DESTINO"   # net10.0 (recomendación de ADR-017)
```

`templates/parametros.env` es el **único** lugar donde se define el destino. Cambiar
la flota de `net10.0` a `net11.0` en 2027 es editar 5 líneas de ese archivo. Ninguna
plantilla, ningún Dockerfile, ningún workflow y ningún documento de esta skill tiene
un `net9`/`net10` escrito a mano: todos usan `${TFM_DESTINO}` / `${DOTNET_TAG}`.

> **Antes de usar la skill, verificá que `SOPORTE_HASTA` no esté vencido.**
> Si lo está, el destino cambió y hay que actualizar `parametros.env` primero —
> migrar hacia un runtime fuera de soporte es el error que ADR-017 existe para evitar.

## Qué hace

Te lleva de "este componente corre en netcoreapp3.1 y nadie lo toca hace dos años"
a "compila, arranca, responde lo mismo que antes y está en el TFM destino", con
evidencia en cada paso y con un camino de vuelta en todo momento.

## Qué NO hace

- **No despliega.** Deja el componente migrado y verificado; el cutover es de la
  skill `dockerizar-componente` y lo ejecuta infra.
- **No escribe en repos de código desde la coordinación.** Los cambios se proponen,
  se revisan y entran por el flujo de ramas de ADR-039.
- **No moderniza el código.** No activa `nullable`, no activa `ImplicitUsings`, no
  reescribe `Startup.cs` a minimal hosting si no hace falta, no cambia la arquitectura
  interna. Una migración de runtime que además refactoriza es dos cambios a la vez,
  y cuando algo falla no se sabe cuál de los dos fue.
- **No actualiza paquetes "porque hay versión nueva".** Solo los que el salto exige.
  Ver §Regla 6.
- **No decide la política de componentes EOL.** Eso es la decisión (c) de ADR-016.

---

## Reglas duras

Si una se rompe, se para y se avisa. No se sigue "a ver si funciona".

1. **Un componente a la vez, una rama a la vez.** Nunca dos migraciones simultáneas
   en el mismo repo ni un lote de repos en un solo PR.
2. **El TFM destino sale de `parametros.env`.** Nunca de la cabeza, nunca del
   Dockerfile que ya estaba, nunca del `FROM` de un stub de Visual Studio.
3. **Migración y dockerización son dos pasos separados y en este orden**
   (migrar → dockerizar), con una excepción y una prohibición explícitas en §5.
4. **Snapshot del contrato ANTES de tocar nada.** OpenAPI + respuestas reales de los
   endpoints de negocio contra el ambiente actual. Sin la línea base, la migración no
   es verificable y no se puede aprobar. Solo 17 de 61 repos backend tienen proyectos
   de test: el snapshot **es** la red de seguridad, no un complemento.
5. **Cero cambios funcionales en el mismo PR.** Si aparece un bug preexistente,
   se registra y se trata aparte; no se arregla acá.
6. **Se actualiza el paquete mínimo que el salto exige.** `dotnet outdated -u` sobre
   toda la solución está **prohibido**: en esta flota arrastra AutoMapper y MediatR a
   versiones con **licencia comercial** (ver `02-ruta-por-saltos` §6).
7. **Warnings nuevos se leen, no se silencian.** `SYSLIB*`, `CS0618`, `NU1605`,
   `NU1608` son el mecanismo por el que la plataforma avisa lo que va a romper en
   runtime. Un `NoWarn` agregado durante una migración es un incidente diferido.
8. **Si el componente hace autenticación, firma o cifra**, la migración no cierra
   sin review de cybersec. Los saltos 7→8 y 8→9 cambian el manejo de JWT y la carga
   de certificados X.509.
9. **Rollback disponible en todo momento.** La rama anterior existe, el artefacto
   anterior existe y el proceso anterior sigue en disco. Ver `05-rollback-y-coexistencia`.

---

## Procedimiento

### Fase 0 — Encuadre (5 min)

```bash
export COORD="<ruta absoluta de la carpeta de coordinación>"   # la da el coordinador
export REPOS_DIR="<carpeta que contiene los clones de los repos>"
cd "${CLAUDE_PLUGIN_ROOT}/skills/migrar-dotnet"
set -a; . ./templates/parametros.env; set +a
export REPO="micro-banco"        # el componente (ejemplo)
```

Contestá estas tres antes de seguir. Si alguna no tiene respuesta, se pregunta.

| Pregunta | Por qué importa |
|---|---|
| ¿El componente está **vivo**? (commits, tráfico por DNS, dueño de negocio) | Migrar un componente que nadie usa es gastar el presupuesto de riesgo en nada. Decisión (c) de ADR-016 |
| ¿Cuál es su **TFM origen real**? | Lo dice el `.csproj`, no el Dockerfile. 17 repos de la flota tienen el `FROM` desalineado con el `.csproj` |
| ¿Va a **dockerizarse**, y cuándo? | Define el orden (§5) y si el destino es una imagen o un zip |

### Fase 1 — Análisis previo (solo lectura, no se toca nada)

```bash
./templates/analisis-previo.sh "$REPO"
```

Produce el bloque que va al §1 del informe. Lo que el script **no** puede contestar y
vos sí tenés que resolver está en **`reference/01-analisis-previo.md`**: licencias,
dependencias externas vivas, quién consume el componente, y si el `using` sospechoso
es uso real o ruido.

**Salida de fase:** el componente queda clasificado en uno de tres carriles.

| Carril | Criterio | Qué significa |
|---|---|---|
| **Verde** | Sin bloqueadores duros, TFM origen ≥ net6, sin nativas, ≤2 saltos | Migración mecánica. Un día de trabajo |
| **Amarillo** | 3+ saltos, o nativas (Skia/Chromium/GemBox), o Hangfire, o auth | Migración con pruebas dirigidas. Necesita el plan de §3 completo |
| **Rojo** | Bloqueador duro: WCF servidor, EF6, `BinaryFormatter`, GDI+ real, LDAP | **No es una migración, es una reescritura parcial.** Se para y se escala |

### Fase 2 — Ruta de saltos

**`reference/02-ruta-por-saltos.md`** tiene, por cada salto, los breaking changes que
importan en esta flota (no la lista completa de Microsoft), qué herramienta ayuda y
**cuándo la herramienta miente**.

La regla del camino:

```
netcoreapp3.0/3.1 ──▶ net6.0 ──▶ net8.0 ──▶ ${TFM_DESTINO}
net5.0            ──▶ net6.0 ──▶ net8.0 ──▶ ${TFM_DESTINO}
net6.0 / net7.0             ──▶ net8.0 ──▶ ${TFM_DESTINO}
net8.0 / net9.0                        ──▶ ${TFM_DESTINO}
```

**Se pasa por los LTS intermedios**, no se salta directo. Es tentador poner
`${TFM_DESTINO}` en el `.csproj` de un netcoreapp3.1 y ver qué pasa; lo que pasa es
200 errores de compilación mezclados de cuatro saltos distintos, sin forma de saber
cuál viene de dónde. Con escalones, cada tanda de errores tiene un solo origen.

**Excepción:** un componente ya en net8 o net9 va directo. Es un solo salto.

**Cada escalón cierra con build limpio y commit propio.** El commit intermedio no se
despliega, pero es el punto de bisección cuando algo falla tres escalones después.

### Fase 3 — Plan de pruebas

**`reference/03-plan-de-pruebas.md`**. El orden importa: el snapshot del contrato se
toma **antes** del primer escalón, contra el componente corriendo hoy en QA.

```bash
./templates/snapshot-contrato.sh antes     # ANTES de tocar el csproj
# ... migración ...
./templates/snapshot-contrato.sh despues
./templates/comparar-respuestas.sh         # diff de contrato y de respuestas
```

Sin snapshot previo no hay Definition of Done. No es negociable: sin tests, la
comparación contra la versión actual es la **única** evidencia de que el componente
sigue haciendo lo mismo.

### Fase 3.5 — Cambiar la UI de documentación a Scalar

**Requerimiento de Plataforma FAAST (2026-09-22): en la migración a .NET 10 de los
backends legado se deja de usar la UI de Swagger y se usa Scalar.**

Va **después** del snapshot de contrato de la Fase 3 y **antes** del cierre, por una
razón concreta: el snapshot es lo que prueba que cambió la vista y **no** el
contrato. Sin la línea base tomada, este paso no es verificable.

→ **skill `scalar-api-docs`** (plugin dev-team) — el procedimiento completo: árbol de
decisión según qué genera hoy el OpenAPI del componente (Swashbuckle de 1 o N
documentos · generador nativo net9+ · gateway Ocelot/YARP, que muchas veces es
**N/A**), la API real del paquete verificada contra la fuente, el catálogo de
errores `E-SC-01…09` y el checklist.

Tres cosas que valen desde acá, sin entrar a esa skill:

- **Es un PR aparte del salto de TFM.** Misma lógica que §5 (migrar ≠ dockerizar):
  un 500 después de un cambio combinado tiene dos sospechosos en vez de uno.
- **Cambia la vista, no el generador.** `AddSwaggerGen`/`UseSwagger` quedan intactos;
  Scalar apunta a la ruta del documento que ya existe. **El diff de contrato debe dar
  vacío** — se verifica con el `comparar-respuestas.sh` de esta misma skill.
- **La versión sale de `version.txt`**, la misma fuente que `/health`. Ver el §Regla
  de versión de `dockerizar-componente` Paso 4.5.

**Un componente puede adoptar Scalar antes de migrar:** el paquete trae
`net8.0;net9.0;net10.0` en el mismo artefacto y el `PackageReference` no cambia al
saltar de TFM. Si conviene desacoplar los dos trabajos, se puede.

### Fase 4 — Cuando algo falla

**`reference/04-catalogo-errores.md`**: tabla `error → causa → fix → cómo verificar
que el fix funcionó`, con código de error (`E-NU-01`, `E-SQL-01`, `E-CULT-01`…) para
poder citarlo en un handoff sin reexplicarlo.

Está marcado qué entradas **están verificadas contra los repos reales de FaaST** y
cuáles son conocimiento general de la plataforma que hay que confirmar en el piloto.
Leyenda: **[V]** verificado por grep en los repos · **[G]** conocimiento general.

**Regla:** si el error que tenés enfrente no está en el catálogo, se agrega al
catálogo cuando se resuelve. La skill se hace más útil con cada migración.

### Fase 5 — Cierre

1. Completá **`reference/checklist.md`**. Cualquier "no" bloquea.
2. Completá el informe desde **`templates/informe-migracion.md`** y dejalo en
   `{coordinacion}/inventario/migracion/<repo>.md`.
3. Handoff al lead con: carril, saltos hechos, diff de contrato, errores del catálogo
   que aparecieron, y lo que quedó pendiente.
4. Si toca auth/crypto: handoff a cybersec **antes** de proponer el cutover.

---

## §5 — Migrar y dockerizar: en qué orden

Esta es la pregunta que hay que contestar por componente, no una vez para todos.

| Situación | Orden | Por qué |
|---|---|---|
| Componente **EOL** (netcoreapp3.x / net5) que va a dockerizarse | **Migrar primero, dockerizar después** | La imagen base depende del TFM. Dockerizar primero significa construir una imagen `aspnet:3.1` sin parches, validarla, desplegarla, y tirarla a la basura semanas después. Es trabajo hecho dos veces sobre una imagen vulnerable |
| Componente **net6/net7** ya dockerizable | **Migrar primero** | Mismo argumento, con menos urgencia: el `DOTNET_VERSION` del Dockerfile es un `ARG`, pero la validación de QA no lo es. Se valida una vez, no dos |
| Componente **ya en net8/net9** | **Dockerizar primero, migrar después** | Un solo salto, y el contenedor da un ambiente reproducible donde probar el salto. Es el único caso donde dockerizar primero **ayuda** a migrar |
| Componente que **no se va a dockerizar** (baja, cliente inactivo) | **Ninguno de los dos** | Decisión (c) de ADR-016 |

**Lo que está prohibido: migrar y dockerizar en el mismo PR / la misma validación de
QA.** Son dos fuentes de fallo con síntomas idénticos. Un 500 después de un cambio
combinado puede ser el runtime nuevo, la imagen, la variable de entorno que no se
mapeó, el usuario no-root o el binding. Separados, cada síntoma tiene un solo
sospechoso. Esto vale incluso cuando las dos cosas las hace la misma persona el mismo
día: **dos ramas, dos PR, dos validaciones**.

**El puente de vhost de ADR-016 §5 aplica igual.** La migración no cambia el puerto,
no cambia el hostname y no cambia el vhost: un componente migrado y todavía en PM2 se
despliega con el `d.sh` de siempre. Eso es deliberado — permite validar el runtime
nuevo en QA **sin** haber resuelto la dockerización.

---

## §6 — El destino no es opinión, es una fecha

| TFM | Tipo | Fin de soporte | Verificado en |
|---|---|---|---|
| netcoreapp3.1 | LTS | **2022-12-13** | dotnet.microsoft.com |
| net5.0 | STS | **2022-05-10** | dotnet.microsoft.com |
| net6.0 | LTS | **2024-11-12** | dotnet.microsoft.com |
| net7.0 | STS | **2024-05-14** | dotnet.microsoft.com |
| net8.0 | LTS | **2026-11-10** | dotnet.microsoft.com |
| net9.0 | STS | **2026-11-10** | dotnet.microsoft.com |
| net10.0 | **LTS** | **2028-11-14** | dotnet.microsoft.com |
| net11.0 | STS | 2028-11-09 (GA 2026-11-10) | dotnet.microsoft.com |

**net8 y net9 mueren el mismo día.** Consultado el 2026-09-21: faltan **7 semanas**.
Por eso `parametros.env` viene con `net10.0` y por eso ADR-017 existe. El detalle
está en el ADR-017 del proyecto de arquitectura (`decisiones/017-migracion-dotnet-destino.md`
en la carpeta de coordinación, si existe).

---

## Archivos de esta skill

```
migrar-dotnet/
├── SKILL.md                          (este archivo — el procedimiento)
├── reference/
│   ├── 01-analisis-previo.md         qué mirar y cómo interpretarlo
│   ├── 02-ruta-por-saltos.md         breaking changes por salto + herramientas
│   ├── 03-plan-de-pruebas.md         sin tests: contrato, humo, diff, carga
│   ├── 04-catalogo-errores.md        error → causa → fix → verificación
│   ├── 05-rollback-y-coexistencia.md rollback, ADR-039, DoD, gates
│   ├── 06-matriz-componentes.md      los 63 de QA Total, con orden y esfuerzo
│   └── checklist.md                  se completa por componente
└── templates/
    ├── parametros.env                ← EL destino se define acá
    ├── analisis-previo.sh            Fase 1, solo lectura
    ├── snapshot-contrato.sh          línea base y comparación de OpenAPI
    ├── comparar-respuestas.sh        diff de respuestas reales
    ├── Directory.Build.props         TFM + política de warnings, paramétrico
    ├── global.json                   pin de SDK, paramétrico
    ├── informe-migracion.md          el entregable por componente
    └── ci-verify-migracion.yml       build + tests + contrato en CI
```

**Piloto recomendado:** `micro-banco`. El porqué está en `reference/06-matriz-componentes.md` §4.

**Relacionados:** ADR-017 (destino) · ADR-016 (dockerización) · skills del plugin:
`deployment-standard` (estándar de dockerización) · `dockerizar-componente` ·
`scalar-api-docs` (Fase 3.5 — UI de documentación) · `crear-tests-backend` (precondición) ·
`ingenieria-faast` (método y DoD del equipo) · en la coordinación del proyecto, si existen:
`inventario/asis-repos-legado.md` · `inventario/asis-qa-total-apis-micros.md`
