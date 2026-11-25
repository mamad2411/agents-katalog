---
name: github-project-backlog
description: Procedimiento del Product Owner para armar de punta a punta un backlog profesional en un GitHub Project v2 (de organizacion o de usuario) a partir de una propuesta, plan o lista de pendientes - issues REALES en lenguaje de negocio (nunca borradores), epicas por categoria con sub-issues, etiquetas por proyecto/fase/categoria/tipo, milestones por fase con condicion de salida, campos del Project (Fase, Categoria, Prioridad, Tipo y el Status integrado con Backlog/Sprint actual/En progreso/En QA/Bloqueado/Hecho), vistas, verificacion y espejo local en .coordination/backlog.md. Incluye el script idempotente project_backlog.py (un solo spec JSON, modo prueba, reanudable). Cargala para /dev-team:project (crear, agregar, verificar, espejo) o cuando el usuario pida "armar un Project organizado por fases".
---

# Backlog completo en un GitHub Project v2 — dev-team

Lo ejecuta el **product-owner**. Convierte una propuesta/plan/lista en un Project ordenado:
fases con condicion de salida, categorias como epicas, historias de negocio con Gherkin,
campos llenos, vistas y un espejo local. Todo con UN spec JSON y el script
`scripts/project_backlog.py`, que crea o reutiliza cada pieza sin duplicar.

## Reglas duras
1. **Nunca borradores.** Cada item del Project es un **issue real**. Si los repos del tema aun
   no existen, los issues viven en el repo transversal del proyecto (el que diga
   `.coordination/config.json` → `tracker.github.repo`) con la etiqueta del proyecto. Nunca se
   crean repos sin autorizacion. `gh project item-create` crea borradores: **no usarlo**.
2. **Redaccion 100% de negocio** (regla de oro del PO): titulo claro desde el titulo
   ("Poder abrir la plataforma y ver un modulo de ejemplo"), sin endpoints, tablas, nombres de
   clases, ramas ni jerga. Test de lectura: lo entiende QA o gerencia a la primera. El script
   avisa si detecta palabras tecnicas o historias sin Gherkin, pero el responsable es el PO.
3. **Escribir en GitHub solo si el usuario lo pidio explicitamente.** Siempre se muestra
   primero el plan (`--dry-run`) y se espera su confirmacion. Si `gh` no esta autenticado o no
   tiene scope `project` (`gh auth status`), decirlo y parar: el usuario corre
   `gh auth refresh -s project`; no se hace auth interactivo desde el agente.
4. **No se toca ningun ambiente.** Crear el backlog no despliega, no ejecuta scripts ni
   cambia parametros en ningun lado.
5. **Reutilizar antes de crear**: Project con el mismo nombre exacto, campos, opciones,
   etiquetas, milestones, epicas e issues (titulo exacto + etiqueta del proyecto). Si hay dos
   Projects con el mismo nombre, preguntar cual.
6. **Acentos**: se conservan en titulos, cuerpos y descripciones. Los **nombres** de campos,
   opciones y etiquetas van **sin acentos** (`Categoria`, `Decision`, `cat: Documentacion y gobierno`)
   para evitar problemas de filtros y busquedas. El script los normaliza solo.
7. En re-ejecuciones el script **solo llena campos vacios**: no pisa el Status que el equipo ya
   movio ni la prioridad que alguien ajusto.

## De donde salen org, repo y Project
De `.coordination/config.json` → `tracker` (`provider: "github"`, `github.org`,
`github.repo` = repo de issues, `github.project` = nombre exacto). Si falta algo, preguntarlo
**una sola vez** al usuario y, despues de crear, el script lo registra en `config.json`
(`org`, `repo`, `project`, `projectNumber`, `projectUrl`, `projectLabel`) sin pisar lo demas.
Si `tracker.provider` es `azure`, esta skill no aplica (el Project es de GitHub): avisar.

## Entradas que el PO deriva de la fuente
- **Fases** (`Fase 0`, `Fase 1`, ...) con titulo, objetivo y **condicion de salida** verificable.
- **Categorias** con su descripcion (seran las epicas). Sugeridas: Entorno de pruebas,
  Experiencia de uso, Modulos y crecimiento, Multi-cliente, Seguridad y acceso, Calidad y
  pruebas, Rendimiento y accesibilidad, Publicacion y operacion, Documentacion y gobierno,
  Decisiones abiertas. Usar solo las que la fuente justifica.
- **Items**: historias, decisiones, riesgos y tareas de negocio; lo ya hecho va con estado `Hecho`.
- Riesgos y decisiones abiertas detectadas en la fuente (tambien son items).

## Redaccion de cada item (cuerpo en Markdown)
- **Historia**: Contexto · Historia de usuario (Como / Quiero / Para) · Criterios de
  aceptacion en **Gherkin** (Dado / Cuando / Entonces; no repetir "entonces" dentro del texto
  del criterio) · Alcance (incluye / no incluye) · Dependencias (salida de la fase anterior; OK
  del usuario si toca ambientes) · Clasificacion.
- **Decision**: Contexto · Opciones · **Quien decide** · **Criterio de cierre**.
- **Riesgo**: Contexto · Impacto · **Como lo reducimos**.
- **Tarea de negocio**: que se hace y como se sabe que esta hecho.
- **Salida de la Fase N**: cada fase termina con este item (tarea de negocio, prioridad Alta)
  que repite la condicion de salida en Gherkin. Si el spec no lo trae, el script lo genera
  (`generar_salidas: true`); si ya existe uno con otro titulo ("Salida de la Fase 1: ..."),
  lo reutiliza.
- **Lo ya hecho**: se crea, se comenta (`comentario_hecho` o "Ya realizado; se registra como
  Hecho.") y se cierra con `state_reason: completed`; Status `Hecho`.

## El spec (un solo JSON de alto nivel)
Ejemplo completo en `assets/spec-ejemplo.json`; el formato exacto esta en el docstring del
script (`project_backlog.py --help`). Campos: `org`, `repo`, `project`, `project_label`
(opcional), `fases[]` (`nombre`, `titulo`, `objetivo`, `condicion_salida`, opcional
`milestone` y `cat_salida`), `categorias[]` (`nombre`, `descripcion`), `items[]` (`titulo`,
`body`, `fase`, `cat`, `prio`, `tipo`, `estado`, opcional `etiquetas` y `comentario_hecho`).
Sin IDs: el script resuelve todo.

Guardar el spec junto al estado (fuera de cualquier repo): `.coordination/project-state/<nombre>.spec.json`
en la carpeta paraguas, o `~/.dev-team/project-state/<nombre>.spec.json` si no hay una
`.coordination` fuera de git (topologia mono). El archivo de estado guarda ademas una copia
del spec bajo la clave `spec`, util para `agregar`.

**Proyecto existente con milestones propios**: poner en cada fase `"milestone": "<titulo exacto>"`
para reutilizarlos (por defecto el script usa `"<etiqueta> · Fase N: <titulo>"` para no chocar
con milestones de otros proyectos del mismo repo).

## El script
```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/github-project-backlog/scripts/project_backlog.py"
python3 "$S" aplicar SPEC --dry-run            # plan con lecturas de GitHub (sin escribir)
python3 "$S" aplicar SPEC --dry-run --offline  # plan sin llamar a gh (spec recien redactado)
python3 "$S" aplicar SPEC                      # ejecutar (solo con OK del usuario)
python3 "$S" verificar SPEC [--corregir]       # revisar / arreglar
python3 "$S" espejo SPEC [--dry-run]           # regenerar la seccion del backlog local
```
Que hace `aplicar`, en orden (cada paso reutiliza lo existente):
1. Project (lo crea si no existe y lo enlaza al repo de issues).
2. Campos single-select `Fase`, `Categoria`, `Prioridad` (Alta/Media/Baja), `Tipo` (Historia,
   Decision, Riesgo, Tarea de negocio, Epica) y las opciones del **Status integrado** (su
   nombre no se puede cambiar; sus opciones si): Backlog, Sprint actual, En progreso, En QA,
   Bloqueado, Hecho. Las opciones por defecto de GitHub se **renombran conservando su id**
   (Todo → Backlog, In Progress → En progreso, Done → Hecho), asi no se pierden valores; las
   opciones extra que el equipo haya agregado se conservan.
3. Etiquetas: la del proyecto, `fase-N`, `cat: <Categoria>`, y por tipo `historia`, `decision`,
   `riesgo`, `tarea de negocio`, `epica`.
4. Milestones por fase con objetivo y **CONDICION DE SALIDA** en la descripcion.
5. Epicas "Épica: <Categoria>" (una por categoria).
6. Items: issue real con etiquetas y milestone → **sub-issue** de su epica → item del Project
   → campos (solo los vacios) → cierre si es `Hecho`.
7. Reescribe en cada epica SOLO la seccion marcada `<!-- historias:inicio/fin -->` con la
   lista de historias por fase (lo demas del cuerpo no se toca).
8. Vistas: "Tablero por Estado" (renombrando la vista por defecto), "Tabla por Fase",
   "Tabla por Categoria", "Roadmap por Fase". Si la API las rechaza, avisa sin abortar.
9. Verificacion final con correccion (re-llena items sin campos, agrega issues que quedaron
   fuera, enlaza sub-issues faltantes) y conteos por Fase / Categoria / Status / Tipo.
10. Espejo en `.coordination/backlog.md` y registro en `config.json` → `tracker.github`.

Garantias del script: GraphQL siempre con **variables** (nunca interpola titulos ni cuerpos en
la consulta); reintentos con espera creciente ante rate limit y errores transitorios (la
creacion de issues NO se reintenta a ciegas: antes de repetir busca si se creo); lotes de
maximo 5 alias por mutacion; archivo de estado para reanudar (si se corta, re-ejecutar el
mismo comando continua sin duplicar).

**Archivo de estado/resultado**: nunca en el directorio actual ni dentro de un repo git.
Se usa la `.coordination/` canonica (la primera con `config.json` subiendo desde el cwd cuya
carpeta padre NO esta dentro de un repo git, comprobado con
`git -C <padre> rev-parse --is-inside-work-tree`) → `.coordination/project-state/<nombre>.json`;
si no hay (mono-repo), `~/.dev-team/project-state/<nombre>.json`. `--estado RUTA` lo fija a
mano y tambien se rechaza si cae dentro de un repo.

## Espejo local
Seccion al PRINCIPIO de `.coordination/backlog.md` (despues del titulo `#` si existe), entre
`<!-- project-backlog:inicio <etiqueta> -->` y `<!-- project-backlog:fin <etiqueta> -->`; al
regenerar solo se reemplaza esa seccion y nunca se borra lo demas. Contiene link al Project,
repo y etiqueta, conteo por fase (items / hechos) y por categoria, condicion de salida por
fase y la lista de issues con link, categoria, tipo, prioridad y estado.

## Verificacion (que se revisa)
- Borradores en el Project → se convierten en issues del repo (`--corregir`).
- Items sin campos (el caso "Content already exists": `addProjectV2ItemById` responde eso bajo
  ritmo rapido y el item queda vacio) → se re-llenan desde el spec o, si no estan en el spec,
  desde sus etiquetas (`fase-N`, `cat: X`, tipo) y su estado (cerrado → Hecho). La prioridad
  sin dato queda para que la defina el PO.
- Issues con la etiqueta del proyecto que no estan en el Project → se agregan.
- Historias que no cuelgan de la epica de su categoria → se enlazan.
- Issues cerrados cuyo Status no es Hecho → solo se reportan (decide el equipo).
- Reporte final: conteos por Fase / Categoria / Status / Tipo.

## Trampas conocidas
- **Sub-issues**: REST `POST repos/{repo}/issues/{epica}/sub_issues` con `sub_issue_id` = **id
  numerico** del issue (campo `id` del REST), no el numero ni el `node_id`. Un issue solo puede
  tener una epica padre: si ya tiene otra, GitHub rechaza (el script lo avisa, no lo mueve).
- **"Content already exists"** al agregar items a ritmo rapido: el item queda sin campos. Por
  eso la verificacion final recorre todo y re-llena.
- **"Resource limits exceeded"** con mutaciones de muchos alias (p. ej. `deleteProjectV2Item`
  en lotes de mas de ~8): lotes chicos. Un item huerfano de un issue borrado puede no poder
  eliminarse por permisos: mencionarlo.
- Borrar un issue creado por error: GraphQL `deleteIssue` (requiere admin) — solo con pedido
  explicito del usuario; el script nunca borra nada.
- **Vistas**: la API permite crear y renombrar vistas y cambiar su layout, pero **NO fijar
  agrupamiento ni orden** (son de solo lectura). Avisar al usuario que el "Group by" de cada
  vista se marca **una vez a mano en la interfaz** (Tablero por Status; Tabla por Fase; Tabla
  por Categoria; Roadmap por Fase).
- `gh api -f body=@archivo` no expande archivos: los cuerpos se envian como JSON por
  `--input -` (el script ya lo hace).
- Etiquetas con ":" y espacios funcionan (`cat: Calidad y pruebas`).
- Para esperar un proceso en segundo plano no encadenar `sleep` largos: usar un bucle
  `until [ -f archivo ]`.

## Entrega al usuario
URL del Project, conteo por fase y categoria, 5 titulos de ejemplo, avisos del script, y lo
que queda pendiente: agrupamiento de vistas a mano, repos por crear, decisiones abiertas.
Handoff `po-to-lead-{fecha}.md` con el link al Project y el orden recomendado por fase.
