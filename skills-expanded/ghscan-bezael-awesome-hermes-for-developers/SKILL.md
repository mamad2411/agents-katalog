---
name: mcp-server-wireup
description: Connect a new MCP (Model Context Protocol) server to a running Hermes Agent instance safely — add the right entry under `mcp_servers:` in `~/.hermes/config.yaml`, scope its environment variables correctly, and verify both that the server's tools actually load and that Hermes's credential-filtering is doing what the docs claim. Use when the user has an MCP server (official, community, or self-built) and needs it working inside Hermes, is migrating an `mcp.json`-style config from Claude Desktop/Cursor into Hermes, or is debugging why an MCP server's tools aren't showing up or a tool call is failing with what looks like an auth error.
version: 0.1.0
platforms:
  - hermes
metadata:
  hermes:
    tags: [mcp, config, security, wireup, integrations]
    category: integrations
---

# MCP Server Wireup

> **Estado:** skill ilustrativa, escrita a partir del mecanismo de `mcp_servers` documentado en
> `hermes-agent.nousresearch.com/docs` y en la chuleta de Dominicode — **no ejecutada aún contra
> una instancia real de Hermes**. Los pasos de "Verification" están diseñados para que tú (o quien
> la instale) confirmes el comportamiento en tu propia instancia antes de confiar en ella para producción.

Esta skill **no** enseña a construir un servidor MCP desde cero (diseño de tools/resources/prompts,
elegir transporte, auth del propio servidor, deployment). Para eso usa una skill de autoría de
servidores (ej. `build-mcp-server`). Esta skill asume que el servidor ya existe — oficial, de un
repo de la comunidad, o hecho por ti — y se enfoca exclusivamente en la parte del lado de Hermes:
conectarlo, no romper nada al hacerlo, y comprobar que de verdad quedó conectado.

## When to Use

- Tienes un servidor MCP (comando `npx`, binario local, o wrapper Docker) y necesitas que Hermes
  lo vea y pueda llamar sus tools.
- Estás migrando una entrada de `mcp.json`/`.mcp.json` (formato usado por Claude Desktop, Cursor,
  Claude Code) hacia el `~/.hermes/config.yaml` de Hermes — los campos no son 1:1.
- Las tools de un servidor MCP no aparecen al pedirle a Hermes que las liste, o una tool call falla
  con un error que huele a autenticación pero el servidor "debería" tener sus credenciales.
- Quieres auditar si las credenciales que declaraste para un servidor MCP realmente quedan
  aisladas al subproceso de ese servidor, o si el subproceso está heredando más de tu shell de lo
  que debería.
- **No** uses esta skill si lo que necesitas es diseñar el servidor MCP en sí (herramientas,
  transporte, esquema de auth propio) — eso es un problema de autoría de servidor, no de wireup.

## Procedure

### 1. Verifica el servidor de forma aislada, antes de tocar Hermes

Corre el comando exacto que vas a poner en `command`/`args` directamente en tu shell, sin Hermes de
por medio:

```bash
npx -y @modelcontextprotocol/server-github
```

Si no arranca aquí (falta un binario, falta una env var, versión incompatible de Node), tampoco va
a arrancar dentro de Hermes — pero afuera es mucho más fácil de diagnosticar porque ves el stderr
completo, no el que Hermes decida repetir.

### 2. Localiza y respalda `~/.hermes/config.yaml`

```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%s)
```

Este archivo también contiene `terminal.backend`, `approvals` y (potencialmente, ver paso 4) 
secretos — trátalo como un archivo sensible desde este punto, no como un dotfile cualquiera.

### 3. Agrega la entrada bajo `mcp_servers:` — como clave de nivel raíz

`mcp_servers` va al mismo nivel que `terminal:` y `approvals:`, **no** anidado dentro de ninguno de
los dos. Usa `templates/mcp-server-entry.yaml` como punto de partida. Forma mínima documentada:

```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

- La clave (`github` en el ejemplo) es el alias que vas a ver en Hermes — puede ser cualquier
  string, pero mantenlo estable si documentas el setup para un equipo.
- `command` + `args` son exactamente lo que probaste en el paso 1.
- `env` es una lista explícita — ver el paso 4, es la parte que más se rompe.
- Campos que **no** están confirmados en la documentación de Hermes (aunque existen en otros
  clientes MCP como Claude Desktop: `disabled`, `alwaysAllow`, `cwd` por servidor) — no asumas que
  Hermes los soporta solo porque otro cliente MCP los tiene. Confirma en el changelog de tu versión
  instalada (`hermes --version`, `hermes doctor`) antes de depender de ellos.

### 4. Declara el `env` explícitamente — no asumas herencia del shell

Por diseño documentado, los subprocesos de servidores MCP **no** heredan tu entorno completo — solo
reciben una base mínima (`PATH`, `HOME`, `USER`, `LANG`) más lo que declares en el bloque `env` de
ese servidor. Si el servidor necesita `GITHUB_PERSONAL_ACCESS_TOKEN`, `OPENAI_API_KEY`, o cualquier
otra credencial, tiene que estar en ese `env:` — exportarla en tu `.bashrc`/`.zshrc` no es suficiente.

Aquí hay una tensión real en la documentación que vale la pena señalar en vez de esconder: el
checklist general de seguridad de Hermes dice *"guarda secretos en `~/.hermes/.env`, nunca en
`config.yaml`"*, pero el único mecanismo documentado para pasarle credenciales a un servidor MCP es
justamente escribirlas dentro de `config.yaml`, bajo `mcp_servers.<nombre>.env`. No hay (que
sepamos, a la fecha de esta skill) una sintaxis de interpolación tipo `${GITHUB_TOKEN}` confirmada
en los docs de Hermes para este bloque — si tu versión sí la soporta, es algo que debes confirmar
tú mismo antes de asumirlo, no algo que esta skill puede prometer.

Mitigación práctica mientras esa tensión no se resuelve en la documentación oficial:

```bash
chmod 600 ~/.hermes/config.yaml
```

Y trata cualquier `config.yaml` con un `mcp_servers.*.env` poblado como un archivo con secretos:
no lo subas a git, no lo sincronices por dotfile managers a máquinas menos confiables, no lo
adjuntes en un issue de soporte sin redactar los valores primero.

### 5. Valida sintaxis antes de arrancar una sesión

```bash
hermes doctor
```

`doctor` está documentado como el comando para diagnosticar problemas de configuración — córrelo
después de cualquier edición manual de `config.yaml`, antes de asumir que el YAML quedó bien
indentado.

### 6. Confirma que las tools del servidor cargaron

Arranca (o reinicia) `hermes` y, en una conversación nueva, pide explícitamente que liste las
tools/skills disponibles, o usa `/skills`. El servidor nuevo debe aparecer con sus tools nombradas.
Si no aparece: revisa `hermes doctor` de nuevo y confirma que el comando del paso 1 sigue arrancando
limpio de forma aislada.

### 7. Haz una tool call real — "aparece en la lista" no es lo mismo que "funciona"

Pide a Hermes que use una tool concreta del servidor nuevo (ej. "lista mis repos de GitHub"). Un
servidor puede aparecer listado y aun así fallar en la primera llamada real si el token es inválido,
expiró, o le faltan permisos/scopes.

### 8. Verifica el filtrado de credenciales con una prueba canario (no confíes solo en el doc)

Ver `scripts/dump-mcp-subprocess-env.sh` y la sección Verification — reemplaza temporalmente
`command`/`args` de tu entrada por el script canario, confirma qué variables de entorno *realmente*
recibió el subproceso, y luego restaura tu entrada real.

## Pitfalls

- **Indentación incorrecta de `mcp_servers`.** El ejemplo oficial lo muestra comentado justo debajo
  del bloque `approvals` en las plantillas de hardening — es fácil pegarlo indentado *dentro* de
  `approvals` o `terminal` por accidente. Debe ser una clave de nivel raíz.
- **Asumir que el `env:` hereda tu shell.** No lo hace. El síntoma es engañoso: la tool call falla
  con algo que parece un error de auth del servicio externo (401, "bad credentials"), cuando la
  causa real es que la env var nunca llegó al subproceso.
- **Sincronizar `config.yaml` sin darte cuenta de que ahora tiene un secreto adentro.** Si usas
  chezmoi, un repo de dotfiles, o backups automáticos, un `mcp_servers.*.env` poblado convierte ese
  archivo en material sensible sin que el nombre del archivo lo delate.
- **"Funciona en mi shell pero no en Hermes" por PATH filtrado.** Si tu `command` depende de un
  shim de un version manager (`nvm`, `volta`, `asdf`) que solo existe en el PATH de tu shell
  interactivo, el subproceso de Hermes (con PATH mínimo) puede no encontrarlo aunque `npx -y ...`
  te funcione perfecto cuando lo pruebas manualmente. Prueba con el entorno filtrado, no con tu
  shell completo (ver Verification).
- **Confundir esto con `hermes tools`.** Ese comando configura las herramientas *nativas* de
  Hermes (las que ya trae el agente), no servidores MCP. No hay (documentado) un subcomando CLI
  para agregar servidores MCP — se editan directamente en `config.yaml`.
- **Confundir `hermes gateway status` con salud del servidor MCP.** Ese comando reporta el estado
  de conexiones de mensajería (Telegram, Discord, etc.), no si tus servidores MCP están sanos.

## Verification

- [ ] `hermes doctor` no reporta errores relacionados al bloque `mcp_servers` nuevo.
- [ ] El servidor nuevo aparece al listar tools/skills en una sesión nueva de `hermes` (o vía
      `/skills`).
- [ ] Una tool call real contra ese servidor completa exitosamente — no solo "aparece listado".
- [ ] `ls -l ~/.hermes/config.yaml` muestra permisos no legibles por otros usuarios si el archivo
      ahora contiene algún secreto (`chmod 600` aplicado).
- [ ] Prueba canario de entorno (`scripts/dump-mcp-subprocess-env.sh`): sustituyes temporalmente el
      `command` real por el script canario, confirmas que el subproceso solo recibió `PATH`,
      `HOME`, `USER`, `LANG` y las variables que declaraste explícitamente en `env:` — ninguna otra
      variable de tu shell (API keys de otros proyectos, tokens de otras herramientas, etc.) — y
      luego restauras la entrada real. Este es el paso que convierte "la documentación dice que
      Hermes filtra credenciales" en "yo confirmé que Hermes filtra credenciales en mi instalación".

## Reference files

- `references/config-yaml-mcp-schema.md` — campos confirmados vs. no confirmados del bloque
  `mcp_servers`, y cómo se compara con `mcp.json` de otros clientes.
- `references/credential-filtering.md` — el mecanismo de filtrado de entorno documentado y la
  tensión con el checklist general de secretos.
- `templates/mcp-server-entry.yaml` — plantilla comentada para copiar/pegar bajo `mcp_servers:`.
- `templates/hermes-env.example` — plantilla de `~/.hermes/.env` como bitácora aparte de tus
  secretos (copia manual hacia `config.yaml`, no interpolación automática confirmada).
- `scripts/dump-mcp-subprocess-env.sh` — servidor MCP "falso" de un solo uso para el paso 8 de
  Verification.
- `scripts/verify-mcp-wireup.sh` — corre `hermes doctor`, revisa permisos de `config.yaml`, y
  valida la sintaxis YAML del bloque `mcp_servers` antes de darlo por bueno.
