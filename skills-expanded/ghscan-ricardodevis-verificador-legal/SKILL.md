---
name: instalar-verificador-legal
description: Skill maestro que instala el sistema Verificador de Jurisprudencia y Doctrina de Bilbao.AI en el workspace de Anthropic del despacho cliente y configura el slash command /verificar-legal en Cowork. Activar cuando el usuario teclea /instalar-verificador-legal, o dice "instala el verificador legal", "monta el verificador jurídico", "despliega el sistema de Bilbao.AI", "instalar el verificador de citas", "actualiza el verificador". También activar si el usuario solicita actualización del sistema ("actualiza el sistema legal", "hay nueva versión del verificador"). REQUIERE Cowork escritorio o Claude Code — NO funciona en claude.ai web porque necesita filesystem, shell y red reales. Cubre customización por nombre del despacho, especialidad principal y jurisdicciones autonómicas.
---

# Skill maestro: Instalación del Verificador Legal de Bilbao.AI

## Objetivo

Llevar al despacho cliente desde "no tiene nada" a "/verificar-legal
operativo en Cowork con su API key, su nombre y sus jurisdicciones
configuradas". Sin pedirle que abra terminal, edite ficheros ni
ejecute scripts manualmente.

Además de la instalación inicial, este skill es el plugin de
**mantenimiento** del sistema: actualizar a versiones nuevas,
validar salud, reinstalar desde cero y desinstalar limpiamente.
Por eso permanece instalado tras la primera ejecución.

## Modelo de coexistencia tras la instalación

Tras una instalación exitosa, el usuario tendrá DOS plugins de
Cowork con roles claramente diferenciados:

```
~/.config/claude-cowork/plugins/
├── verificador-legal-installer-bilbao/    ← este plugin (MANTENIMIENTO)
│   └── /instalar-verificador-legal        ← actualizar / validar / reinstalar / desinstalar
│
└── verificador-legal-<despacho-slug>/     ← plugin operativo (USO DIARIO)
    └── /verificar-legal                   ← verificar un escrito
```

Importante:

- **Ambos coexisten** sin solapamiento. Cada uno tiene su rol.
- **Ninguno se autodestruye**. El installer queda disponible para
  ciclo de vida (update/uninstall); el plugin del despacho queda
  como herramienta de trabajo del letrado.
- Si el usuario pregunta "¿puedo borrar el installer ya que ya
  está instalado el sistema?": la respuesta es **NO**. El installer
  es el único camino para actualizar a futuras versiones del
  producto o para desinstalar limpiamente.

## Entorno requerido

Este skill SOLO funciona en:

- **Cowork (aplicación de escritorio)** — porque el sandbox tiene
  Bash, Write, web_fetch y acceso al filesystem del usuario.
- **Claude Code (CLI)** — ídem.

NO funciona en **claude.ai web**: las tools de filesystem y shell
son simuladas y el plugin de Cowork no se puede registrar desde web.

Si te invocan en claude.ai web, detéctalo (no tendrás Bash real
disponible) y avisa al usuario con este mensaje:

> El instalador necesita acceso real a tu disco, terminal y red.
> En claude.ai web esto no es posible. Por favor, abre Cowork (la
> aplicación de escritorio) y reinvócame allí, o utiliza Claude Code
> desde una terminal. Si no tienes Cowork instalado, descárgalo en
> claude.com/desktop.

## Flujo de instalación (9 pasos)

### Paso 0 — Detección de modo

Comprueba si existe `<dir>/.agent-ids.json` (con `<dir>` por defecto
`~/Documents/verificador-juris-bilbao`, o el de
`VERIFICADOR_JURIS_HOME` si está exportada).

| Estado | Flags | Acción |
|---|---|---|
| No existe `.agent-ids.json` | (cualquier flag) | INSTALACIÓN NUEVA — pasos 1–9 |
| Existe `.agent-ids.json` | sin flags | Mostrar **menú** (actualizar / validar / reinstalar / desinstalar / cancelar) y proceder |
| Existe `.agent-ids.json` | `--update` | UPDATE — pasos 3-9 conservando .env y memory store |
| Existe `.agent-ids.json` | `--validate-only` | Solo `despliegue/05_validar_ids.py` y reportar |
| Existe `.agent-ids.json` | `--reinstalar` | Confirmación doble + archivar todos los recursos + INSTALACIÓN NUEVA |
| Existe `.agent-ids.json` | `--uninstall` | Confirmación doble + archivar agentes + borrar plugin del despacho + dejar installer |

Para los modos NO-instalación, ir directo al paso correspondiente.
Para INSTALACIÓN NUEVA y UPDATE: continuar con paso 1.

### Paso 1 — Recogida de datos del despacho

Conversa, una pregunta a la vez:

**1.1 Nombre del despacho**

> ¿Cómo se llama el despacho? Esto aparecerá en el nombre de los
> agentes que crearás en tu workspace de Anthropic, en el title del
> plugin local, y en algunos logs. Ejemplo: "Pérez & Asociados",
> "Bufete García", "AbogadosNorte".

Genera un slug a partir del nombre (lowercase, guiones, sin acentos
ni caracteres especiales). Confirma el slug con el usuario antes de
seguir. Ejemplo: "Pérez & Asociados" → `perez-asociados`.

**1.2 Especialidad principal**

> ¿Cuál es la especialidad principal del despacho?
> - penal
> - civil
> - mercantil
> - administrativo
> - laboral
> - multidisciplinar
>
> Esto afecta a los patrones de extracción de citas y a los prompts
> de los sub-agentes. Si no sabes cuál marcar, elige
> "multidisciplinar" — funciona para todo pero con menos optimización
> específica.

Consulta `reference/customizacion-especialidades.md` para entender
qué cambia con cada especialidad.

**1.3 Jurisdicciones autonómicas**

> ¿Qué jurisdicciones autonómicas son relevantes para vuestro
> trabajo? Habilitar una jurisdicción significa que el sub-agente de
> normativa también validará leyes y decretos publicados en ese
> boletín oficial autonómico.
>
> Boletines disponibles:
> - BOPV (País Vasco)
> - DOGC (Cataluña)
> - BOCM (Madrid)
> - DOGV (Comunidad Valenciana)
> - DOG (Galicia)
> - BOJA (Andalucía)
> - BOA (Aragón)
> - BORM (Región de Murcia)
> - DOCM (Castilla-La Mancha)
> - BON (Navarra)
>
> Puedes habilitar varias separadas por coma. Si trabajáis solo con
> normativa estatal y europea, di "ninguna".

Consulta `reference/customizacion-jurisdicciones.md` para los
detalles de cada boletín.

**1.4 Directorio de instalación**

> ¿Dónde instalo el proyecto?
> - default: `~/Documents/verificador-juris-bilbao`
> - alternativa típica: `~/code/verificador-juris-<despacho-slug>`
>
> Si el directorio existe y NO contiene una instalación previa,
> preguntaré si quieres sobreescribirlo.

**1.5 API key de Anthropic**

> Necesito vuestra API key con permisos sobre Managed Agents.
> Pégala aquí. Te aviso: la voy a guardar solo en el `.env` del
> proyecto (que está en `.gitignore`), nunca en logs ni outputs
> del informe.

Crítico: **NO IMPRIMAS la key** en ningún output. Solo la usarás en
variables de entorno cuando ejecutes los scripts del bootstrap.

### Paso 2 — Validaciones previas

Ejecuta secuencialmente (cada paso con confirmación silenciosa, solo
reporta si algo falla):

1. `python3 --version` → debe ser ≥ 3.10. Si no, ABORT con mensaje.
2. `command -v pip3` → debe existir. Si no, ABORT con mensaje.
3. Conectividad: `curl -s -o /dev/null -w "%{http_code}" https://api.anthropic.com` → debe ser 401 o 200.
4. Auth: con la API key, ejecuta un `models.list(limit=1)`. Si
   AuthenticationError → ABORT con "API key inválida o sin permisos
   de Managed Agents".

### Paso 3 — Volcado del sistema customizado

Copia `assets/system-template/` al directorio elegido. Mientras lo
copias, aplica sustituciones de plantilla en los ficheros que llevan
placeholders `{{DESPACHO_NOMBRE}}`, `{{DESPACHO_SLUG}}`,
`{{ESPECIALIDAD}}`, `{{JURISDICCIONES}}` (lista separada por comas):

- `prompts/coordinator-system.md`
- `prompts/sub-boe-system.md` (sustituir lista de boletines)
- `prompts/sub-cendoj-system.md` (ajustar tonalidad si la especialidad
  es penal/laboral/civil — ver `reference/customizacion-especialidades.md`)
- `skill/verificador-jurisprudencia-es/SKILL.md` (descripción inicial)
- `README.md` (encabezado con nombre del despacho)
- `.env.example` (placeholder de la API key)

Si modo UPDATE: NO sobrescribir `.env`, `.agent-ids.json`, ni
`logs/`. Sobreescribir el resto.

### Paso 4 — `.env` con la API key

Crear `<dir>/.env` con:

```
ANTHROPIC_API_KEY=<la key que el usuario pegó>
DEFAULT_MODEL_OPUS=claude-opus-4-7
DEFAULT_MODEL_SONNET=claude-sonnet-4-6
DEFAULT_MODEL_HAIKU=claude-haiku-4-5-20251001
COORDINATOR_MAX_ITERATIONS=3
```

Permisos: `chmod 600 <dir>/.env`.

### Paso 5 — Ejecutar bootstrap.sh

```bash
cd <dir> && bash bootstrap.sh
```

Captura stdout/stderr. Si el script falla:
- Mostrar las últimas 30 líneas al usuario.
- Consultar `reference/troubleshooting.md` para mapear el error a
  causa probable.
- NO continuar con los pasos siguientes.

Si éxito: capturar el `.agent-ids.json` resultante para usar en el
paso 6.

### Paso 6 — Construir el plugin del cliente

Copia `assets/plugin-cliente-template/` a una carpeta temporal.
Sustituye placeholders:

- `{{DESPACHO_NOMBRE}}` → nombre del despacho
- `{{DESPACHO_SLUG}}` → slug
- `{{PROJECT_HOME}}` → ruta absoluta del directorio donde se ha
  instalado el sistema (paso 3)

NO se inyecta `.agent-ids.json` en el plugin (los IDs viven en el
proyecto, no en el plugin). El plugin solo necesita saber qué
proyecto invocar y bajo qué nombre.

Renombra la carpeta a `verificador-legal-<despacho-slug>`.

### Paso 7 — Instalar el plugin localmente

```bash
mkdir -p ~/.config/claude-cowork/plugins
cp -r <temp>/verificador-legal-<despacho-slug> ~/.config/claude-cowork/plugins/
```

Si modo UPDATE y ya existía un plugin con ese nombre, sobreescribir
(después de confirmación implícita en paso 0).

Recomienda al usuario reiniciar Cowork. **NO lo hagas tú** — el
usuario debe controlar cuándo reiniciar su aplicación.

### Paso 8 — Test E2E rápido (opcional, con confirmación)

> El sistema está montado. ¿Quieres que ejecute un test rápido con
> el escrito de prueba? Tarda 5-10 minutos y consume aproximadamente
> 1-3 USD en tokens. Si tu API key tiene saldo y tienes los 10
> minutos, recomiendo hacerlo: es la mejor garantía de que todo
> funciona end-to-end.

Si el usuario acepta:

```bash
cd <dir> && python3 verificar.py pruebas/escrito-de-prueba.md \
    --fecha-referencia 2010-09-01 --json-only
```

Espera, recoge el resultado, valida que `result=satisfied` y
muestra al usuario:

> Test E2E completado con éxito. El sistema cazó las 4 citas
> críticas correctamente. Informe en
> <dir>/logs/informe-<sid>.md.

Si falla: reportar y consultar troubleshooting.

### Paso 9 — Reporte final al usuario

Salida obligatoria:

```
✓ Sistema instalado en <dir>/
✓ Recursos creados en tu workspace de Anthropic:
  - Skill: skill_XX...
  - Sub-agentes: 5 (cendoj, tc, eurlex, boe, doctrina)
  - Coordinador: agent_XX...
  - Memory store: memstore_XX...
✓ Plugin operativo instalado:
  ~/.config/claude-cowork/plugins/verificador-legal-<slug>/
✓ Reinicia Cowork para activar /verificar-legal.

Configuración aplicada:
  Despacho: <nombre>
  Especialidad: <especialidad>
  Jurisdicciones autonómicas: <lista>

🎯 LOS DOS PLUGINS QUE TIENES INSTALADOS:

  1. verificador-legal-installer-bilbao   ← MANTENIMIENTO
     Comando: /instalar-verificador-legal
     Para: actualizar versiones, validar salud, reinstalar,
            desinstalar. NO LO BORRES.

  2. verificador-legal-<slug>              ← USO DIARIO
     Comando: /verificar-legal
     Para: verificar escritos jurídicos.

Próximos usos:
  Adjunta un escrito en Cowork y teclea /verificar-legal.

Mantenimiento futuro:
  /instalar-verificador-legal --update       (actualizar versión)
  /instalar-verificador-legal --validate-only (auditar salud)
  /instalar-verificador-legal --uninstall    (desinstalación guiada)

Auditoría manual:
  python3 <dir>/despliegue/05_validar_ids.py

Reintentos automáticos de citas en dudosa_por_infraestructura:
  ver <dir>/docs/job-diferido.md

API key guardada solo en <dir>/.env (modo 600). No se envía a
Bilbao.AI ni a terceros. Recordatorio: rotar cada 90 días.
```

## Comportamiento en los modos no-instalación

### Modo `--update`

Pasos 1.4 (directorio) y 1.5 (API key) se LEEN del `.env` y
`.agent-ids.json` existentes (no se vuelven a preguntar).
Datos 1.1-1.3 (nombre, especialidad, jurisdicciones) tampoco se
preguntan: se LEEN del `metadata` del plugin del despacho ya
instalado. Si el usuario quiere cambiar alguno, debe usar
`--reinstalar`.

Paso 3 (volcado) respeta `.env`, `.agent-ids.json`, `logs/`.
Pasos 4, 6, 7 NO se aplican (no se vuelve a crear el .env ni el
plugin del despacho, solo se actualiza el contenido del system).
Paso 5 (bootstrap) se ejecuta — los scripts son idempotentes y
actualizan prompts/skill remota in-place.

### Modo `--validate-only`

Salta a `python3 <dir>/despliegue/05_validar_ids.py` y reporta el
output al usuario sin más. Útil para troubleshooting rápido.

### Modo `--reinstalar`

Pide **confirmación doble** (el usuario debe escribir "REINSTALAR"
literal). Tras confirmación:

1. Llama a `c.beta.agents.archive(id)` para los 6 agentes
   (sub-agentes + coordinador).
2. Llama a `c.beta.skills.delete(id)` o `c.beta.memory_stores.archive(id)`.
3. Borra `<dir>/.agent-ids.json` y `<dir>/logs/`.
4. Borra el plugin del despacho de `~/.config/claude-cowork/plugins/`.
5. Procede con INSTALACIÓN NUEVA estándar.

### Modo `--uninstall`

Pide **confirmación doble** (escribir "DESINSTALAR"). Tras
confirmación:

1. Archiva los 6 agentes en Anthropic (idem reinstalar).
2. Archiva la skill remota y el memory store.
3. Borra el plugin del despacho de `~/.config/claude-cowork/plugins/`.
4. **NO borra el directorio del proyecto** ni el `.env`
   (el usuario decide).
5. **NO se autodesinstala** — el installer queda. El usuario lo
   borra manualmente desde Cowork si quiere.

## Referencias

- `reference/customizacion-especialidades.md` — qué cambia con cada
  especialidad
- `reference/customizacion-jurisdicciones.md` — boletines autonómicos
  disponibles
- `reference/troubleshooting.md` — errores comunes y solución
- `reference/flujo-instalacion.md` — diagrama completo del flujo
