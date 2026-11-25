---
name: hooks-and-guardrails
description: Candados como código para Claude Code — hooks que bloquean acciones (PreToolUse), stop-gates que impiden cerrar sin evidencia (Stop), guardas de recursos, inyección de contexto (SessionStart, UserPromptSubmit), contrato de entrada/salida por stdin/stdout/exit code, fallar cerrado vs abierto, portabilidad en Windows y cómo probar y depurar un hook. Usar al convertir una regla que "el agente a veces se salta" en una barrera determinista, al escribir o revisar un script en .claude/hooks/, o cuando un hook no dispara, bloquea de más o rompe todas las sesiones.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Hooks y candados

CLAUDE.md y skills son **contexto**: el modelo los sigue casi siempre. Un hook es **código**: se
ejecuta siempre. Todo lo que no puede fallar nunca (no commitear sobre la rama de integración, no
tocar la base productiva, no cerrar un carril sin evidencia) va en un hook. Lo que admite criterio
va en un prompt (`prompt-engineering`). Los candados de seguridad de la aplicación son otro tema:
`security-guardrails`.

## 1. Contrato de un hook de comando

Entrada: JSON por **stdin**. Salida: **exit code** + stdout (JSON opcional) + stderr.

Campos comunes de entrada: `session_id`, `cwd`, `hook_event_name`, `permission_mode`,
`transcript_path`; los de herramienta agregan `tool_name`, `tool_input` y `tool_use_id`;
`PostToolUse` agrega `tool_result`; `Stop` agrega `stop_hook_active` y `last_assistant_message`;
`SubagentStop` suma además `agent_id` y `agent_type`.

> [!warning] Leé stdin como bytes y decodificá `utf-8-sig`
> En Windows, PowerShell antepone un BOM UTF-8 al pipe y `json.load(sys.stdin)` muere con
> `Unexpected UTF-8 BOM`. Si ese error lo traga un `except: sys.exit(0)`, el candado queda
> **inerte y silencioso**: exit 0 y stdout vacío es indistinguible de "permitido". Usá
> `json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))` y mandá todo fallo de parseo a stderr.

| Exit | Efecto |
|---|---|
| `0` | Continúa. stdout se interpreta como JSON si empieza con `{` y termina con `}`; en `UserPromptSubmit` y `SessionStart` el texto plano de stdout entra al contexto del modelo |
| `2` | **Bloquea** (en los eventos que admiten bloqueo). Escribí la razón en stderr: el modelo la recibe y ajusta |
| otro | Error **no bloqueante**: la acción sigue. Solo se ve la primera línea de stderr |

Regla de la guía oficial: si el hook impone una política, **usá `exit 2`**; el `exit 1` no bloquea.
Salida JSON válida manda sobre el código de salida; elegí un mecanismo por hook.

## 2. Eventos que la casa usa

| Evento | Bloquea con exit 2 | Para qué |
|---|---|---|
| `PreToolUse` (matcher por herramienta) | Sí: cancela la llamada | Vetar comandos, rutas, ramas; limitar subagentes; exigir precondiciones |
| `PostToolUse` | No (ya corrió); el modelo ve stderr | Formatear, registrar, avisar "esto rompió el typecheck" |
| `Stop` | Sí: el modelo sigue trabajando | Stop-gate: no cerrar sin evidencia |
| `SubagentStop` | Sí | Exigir formato de retorno o evidencia al subagente |
| `UserPromptSubmit` | Sí: bloquea y borra el prompt | Inyectar estado (carril activo, claim actual); frenar pedidos prohibidos |
| `SessionStart` | No | Cargar contexto vivo: rama, estado de progreso, avisos |
| `PostToolUseFailure` | No | Liberar candados de recursos cuando una herramienta falla |

`PreToolUse` corre **antes** de cualquier chequeo de permisos y en todos los modos: un `deny` desde
un hook bloquea incluso con permisos salteados. Al revés no: un `allow` no levanta reglas de `deny`
de la configuración. Los hooks pueden apretar, nunca aflojar.

Salida estructurada de `PreToolUse` (dentro de `hookSpecificOutput`, no en el nivel superior):

```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason": "Prohibido commitear sobre la rama de integración; creá una rama."}}
```

Valores: `allow` (salta el prompt de permiso), `deny` (cancela y devuelve la razón al modelo),
`ask` (prompt normal). `Stop` y `PostToolUse` usan `decision: "block"` + `reason` en el nivel
superior; `PermissionRequest` usa `hookSpecificOutput.decision.behavior`. Ante la duda, consultá la
tabla de decisión por evento en la doc oficial: los formatos difieren entre eventos.

## 3. Configuración

Van en `hooks` de un archivo de settings: `~/.claude/settings.json` (usuario),
`.claude/settings.json` (proyecto, versionado), `.claude/settings.local.json` (personal, fuera de git),
settings gestionados (organización), `hooks/hooks.json` de un plugin, o el frontmatter de una skill o
subagente. Los hooks de todos los niveles **se suman**. Los candados del equipo van en
`.claude/settings.json` para que viajen con el repo.

```json
{"hooks": {"PreToolUse": [{"matcher": "Bash|PowerShell",
  "hooks": [{"type": "command",
             "command": "python \"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.py\"",
             "timeout": 20}]}]}}
```

Matcher: nombre exacto o lista con `|`; cualquier otro carácter lo vuelve regex. Es sensible a
mayúsculas. `${CLAUDE_PROJECT_DIR}` apunta a la raíz del proyecto: usalo siempre, nunca rutas
relativas al cwd. Timeout por defecto de un hook de comando: 10 minutos; ponelo explícito y corto.
Además de `command` existen `prompt` (un modelo evalúa y decide), `agent`, `http` y `mcp_tool`;
para políticas usá `command`: determinista y auditable.

## 4. Stop-gate: no cerrar sin evidencia

Patrón de la casa: un archivo de estado de progreso (`progress-reporting`) con el claim vigente
(`evidence-and-verification`). El hook `Stop` lee el estado; si hay trabajo activo sin claim de
cierre, sale con `2` y explica qué falta.

```python
import json, sys
data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))  # utf-8-sig: PowerShell antepone BOM
if data.get("stop_hook_active"):      # ya hay un Stop hook corriendo
    sys.exit(0)                       # nunca bloquear dos veces seguidas sin progreso
intentos = contar_y_registrar(data.get("session_id"))  # contador propio, persistido
if intentos > 2:
    print("Gate cede tras 2 bloqueos sin progreso.", file=sys.stderr)
    sys.exit(0)
state = load_state()
if state and state["phase"] != "done":
    print(f"Trabajo en {state['phase']}; registrá evidencia o marcá BLOCKED antes de cerrar.",
          file=sys.stderr)
    sys.exit(2)
sys.exit(0)
```

`stop_hook_active` está documentado: es `true` mientras un hook `Stop` ya se está ejecutando,
precisamente para que el hook evite dispararse a sí mismo de forma recursiva. **No alcanza solo.**
Protege contra la recursión inmediata, pero no contra el ciclo *bloqueo → el modelo responde de
nuevo → bloqueo*, donde cada vuelta trae el campo en `false`. Por eso el ejemplo suma un **contador
propio por sesión persistido en disco** que cede tras N bloqueos sin progreso: es la única defensa
que no depende de un campo ajeno. No hay ningún límite documentado de bloqueos consecutivos, así
que no supongas que algo te va a frenar el ciclo.

`Stop` dispara **cada vez** que el modelo termina de responder, no solo al final de la tarea: el
gate debe leer estado real, no suponer "el trabajo terminó".

Riesgo conocido: si el estado queda "activo" por una sesión que murió, **todas** las sesiones
futuras quedan bloqueadas al cerrar. Diseñá la salida: un comando para marcar `done`/`abandoned`,
caducidad del estado, y un mensaje de error que diga cómo destrabar.

## 5. Guardas de recursos y candados de proceso

- `PreToolUse` sobre `Agent`: contar subagentes activos y negar por encima del tope; liberar el contador en `PostToolUse` **y** `PostToolUseFailure` del mismo matcher, o el candado queda tomado.
- `PreToolUse` sobre `Bash|PowerShell`: vetar `--workers>1`, `git push --force`, `git commit` en ramas protegidas, `DROP`/`TRUNCATE` fuera de test, `rm -rf` sobre rutas fuera del proyecto. Parseá `tool_input.command`; ante un comando que no podés interpretar, decidí por política (§6).
- Estado del candado en archivo con nombre por sesión y caducidad; nunca en memoria del proceso (cada hook es un proceso nuevo).
- Ver `agent-resource-control` para los topes que la casa aplica.

## 6. Fallar cerrado vs abierto

| Candado | Ante error interno del hook |
|---|---|
| Seguridad y datos (ramas protegidas, base productiva, borrado) | **Cerrado**: `exit 2` con "hook falló, acción denegada por precaución" |
| Calidad y proceso (formato, avisos, contexto) | **Abierto**: `exit 0`, registrar el error |
| Stop-gate | Cerrado, pero con vía de escape documentada (§4) |

Un bypass (`variable de entorno que desactiva el guard`) es aceptable **solo** si deja rastro:
registrá quién, cuándo y por qué en un log que se revisa. Un bypass silencioso convierte el candado
en decoración. Recordá que `PreToolUse` no puede bloquear lo que corre fuera de una herramienta:
una terminal del usuario no pasa por hooks.

## 7. Portabilidad (Windows incluido)

- Forma shell sin `args`: en Windows corre en Git Bash, o PowerShell si no está. Preferí `python script.py` como comando, o la **forma exec** (`"args": []`) que lanza el ejecutable sin shell y evita problemas de comillas.
- Intérprete: `python`, no `python3` (en muchas máquinas Windows no existe). Sin `#!/usr/bin/env`, sin `chmod`, sin `jq`: parseá JSON con Python o Node.
- No asumas `/proc`, `os.getloadavg`, `fork` ni señales POSIX. Si una guarda depende de eso, en Windows queda **inerte**: detectalo y decilo en el log, no simules que protege.
- Rutas con `pathlib`; comparaciones de rutas normalizadas y sin distinguir mayúsculas.
- Perfiles de shell que imprimen texto (un `echo` en `.bashrc`) contaminan stdout y rompen el JSON: envolvé esas salidas en `if [[ $- == *i* ]]`.
- Escribí a stdout solo JSON o nada; todo lo humano a stderr.

## 8. Probar y depurar

1. A mano: `echo '{"tool_name":"Bash","tool_input":{"command":"git push --force"}}' | python .claude/hooks/guard.py; echo $?` — verificá exit y stderr por cada rama de la lógica.
2. Un caso por rama: permitido, denegado, entrada malformada, estado ausente, bypass.
3. En sesión: `/hooks` lista los registrados por evento; `claude --debug` (o `/debug`) muestra ejecuciones, stdout completo y errores de parseo. Los hooks se leen al iniciar la sesión: tras editar settings, reiniciá.
4. Versioná los scripts con sus tests; un hook es código de producción del equipo.

## Anti-patrones

- `exit 1` para bloquear.
- Política en un `prompt` hook cuando alcanzaba un `if` determinista.
- Stop-gate sin `stop_hook_active`, sin contador propio, sin caducidad y sin comando de salida.
- Candado que solo funciona en Linux y nadie sabe que en Windows no hace nada.
- Dar por bueno un hook porque su self-test de funciones puras pasa: hay que ejercitar el
  contrato real, alimentándolo por stdin desde **cada shell** que lo vaya a invocar.
- Bypass por variable de entorno sin registro.
- Hooks personales en `settings.local.json` que el equipo cree que existen.
- Mezclar JSON en stdout con texto humano.
- Un hook que tarda 30 s en cada `Edit`.

## Checklist

- [ ] La regla realmente no admite criterio; si admite, va a un prompt.
- [ ] Evento y matcher correctos; `${CLAUDE_PROJECT_DIR}`; timeout explícito.
- [ ] Bloquea con `exit 2` + razón en stderr, o con JSON válido; no ambos.
- [ ] Política de fallo (cerrado/abierto) decidida y escrita en el script.
- [ ] Bypass, si existe, deja rastro.
- [ ] `Stop`: lee estado real, respeta `stop_hook_active`, **además** lleva contador propio por
      sesión que cede tras N bloqueos, y tiene vía de escape documentada.
- [ ] stdin leído como bytes con `utf-8-sig`; probado por pipe desde PowerShell **y** desde bash.
- [ ] Candados con contador se liberan también en `PostToolUseFailure`.
- [ ] Corre en Windows con `python` y sin dependencias POSIX; lo que no puede, lo declara.
- [ ] Probado a mano con JSON por stdin en cada rama; scripts versionados en el repo.
