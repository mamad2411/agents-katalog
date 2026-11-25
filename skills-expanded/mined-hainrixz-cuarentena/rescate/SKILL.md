---
name: rescate
description: Para cuando ya abriste o instalaste algo y sospechas que te cambió la compu. Revisa en modo solo lectura la configuración de Claude Code (permisos, hooks, CLAUDE.md, skills, plugins, MCP), el arranque de la terminal, lo que arranca solo y git/npm, marca lo reciente y propone cómo deshacer cada cambio, con respaldo y con tu aprobación. Úsala cuando digan "ya lo instalé", "creo que me cambió la configuración", "abrí un zip raro", "me modificó los permisos", "deshaz lo que instaló" o "revisa mi compu".
argument-hint: "[días hacia atrás, 14 por defecto] [nombre o fecha de lo que abriste]"
allowed-tools: Bash(bash *revisar-compu.sh*), Read, Grep, Glob
---

# Rescate · qué te cambiaron y cómo deshacerlo

Datos de la persona: `$ARGUMENTS`

## Antes de empezar

Pregunta una sola vez, todo junto, lo que falte: **qué abrió o instaló** (nombre del ZIP, link,
lo que recuerde) y **más o menos cuándo**. Si no lo sabe, usa 14 días y sigue.

## Reglas

1. **Primero se mira, después se toca.** Hasta que la persona apruebe un cambio concreto, todo es
   solo lectura.
2. **Nunca imprimes un secreto.** El script tapa lo que parece llave o token. Si al leer un archivo
   ves uno, no lo copies al chat: di "aquí hay una llave" y el archivo.
3. **Nada se borra sin respaldo.** Cada cambio se hace después de copiar el archivo a
   `<archivo>.respaldo-<fecha>`, y se dice dónde quedó.
4. **No asumas que todo lo reciente es malo.** La persona instala cosas a propósito. Pregunta antes
   de proponer quitar algo que tiene pinta de ser suyo.

## Paso 1 · La foto

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/revisar-compu.sh" <días>
```

Si `${CLAUDE_SKILL_DIR}` no se reemplazó por una ruta, usa la carpeta donde está este SKILL.md.
Saca siete bloques: configuración global de Claude, lo instalado en `~/.claude`, servidores MCP,
arranque de la terminal, lo que arranca solo, git/npm/red, y archivos de configuración recientes.

## Paso 2 · Separar lo raro

Para cada cosa marcada como reciente o que encaje con lo que la persona abrió, decide en cuál de
tres grupos va:

- **Sospechoso**: permisos `Bash(*)` o `bypassPermissions` que la persona no puso; hooks que corren
  scripts de una carpeta descargada; un `CLAUDE.md` global con instrucciones que no reconoce;
  líneas en `~/.zshrc` que bajan o evalúan algo; un LaunchAgent nuevo con nombre genérico o que
  corre `curl`; un `core.hooksPath` global; un `registry=` raro en `.npmrc`; llaves nuevas en
  `authorized_keys`; entradas nuevas en `/etc/hosts`.
- **Hay que preguntar**: skills, plugins o servidores MCP nuevos que podrían ser de la persona.
- **Normal**: lo que la persona reconoce y lo que instalan las apps comunes (Google, Adobe, Zoom...).

Abre con Read cada archivo sospechoso para confirmar y cita la línea.

## Paso 3 · El reporte

En el chat, corto:

1. Una frase: encontré N cosas sospechosas, N para confirmar contigo.
2. Una tabla: **Qué · Dónde (archivo:línea) · Desde cuándo · Qué hace · Cómo se deshace**.
3. Las preguntas del grupo "hay que preguntar", juntas.

Si no hay nada sospechoso, dilo claro y di qué revisaste.

## Paso 4 · Deshacer, uno por uno y con su sí

Para cada cambio aprobado: respaldo, cambio, y verificación de que quedó. Las recetas:

- **Permiso o hook en `~/.claude/settings.json`**: respaldo, quitar solo esa regla o ese hook, y
  comprobar que el JSON sigue válido.
- **`~/.claude/CLAUDE.md`**: respaldo y quitar solo las líneas ajenas.
- **Skill, agente o comando**: mover la carpeta a `~/cuarentena/retirados/` en vez de borrarla.
- **Plugin**: `claude plugin uninstall <nombre>` y, si vino de un marketplace desconocido,
  `claude plugin marketplace remove <nombre>`.
- **Servidor MCP**: `claude mcp remove <nombre>` (con `-s user` o `-s project` según dónde esté).
- **Línea en `~/.zshrc` o similar**: respaldo y borrar solo esa línea; pedir abrir una terminal
  nueva para que aplique.
- **LaunchAgent**: `launchctl bootout gui/$(id -u) <ruta del plist>` y mover el `.plist` a
  `~/cuarentena/retirados/`.
- **crontab**: respaldo con `crontab -l > ~/cuarentena/retirados/crontab-<fecha>` y quitar la línea.
- **git o npm**: `git config --global --unset core.hooksPath`, o quitar la línea del `.npmrc`.

## Paso 5 · Si hubo robo de llaves

Si algo leyó llaves y habló con internet (por ejemplo, un script que manda `~/.ssh` o un `.env` a un
servidor), quitarlo no basta: esas llaves hay que **rotarlas**. Di cuáles (SSH, AWS, GitHub, la API
de turno), en qué orden y dónde se hace cada una. Eso lo hace la persona en cada servicio; tú no
tocas cuentas.

Al final, propón revisar la próxima descarga con `/cuarentena:revisar` antes de abrirla.
