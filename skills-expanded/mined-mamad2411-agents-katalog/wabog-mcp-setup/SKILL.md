---
name: wabog-mcp-setup
description: Configura el conector oficial de Wabog (servidor MCP) en el entorno de IA donde se ejecuta este agente. Úsala cuando el usuario pida conectar Wabog, su asistente legal, a su herramienta de IA (Claude Code, Claude, ChatGPT, Codex, Antigravity, OpenCode u otro cliente MCP).
---

# Configurar el MCP de Wabog

Eres un agente de IA y tu tarea es dejar funcionando el conector de Wabog en el entorno donde te estás ejecutando, con la menor fricción posible para el usuario.

## Datos del servidor

- **Nombre sugerido:** `wabog`
- **URL:** `https://mcp.wabog.com` (también responde en `https://mcp.wabog.com/mcp`)
- **Transporte:** MCP Streamable HTTP
- **Autenticación:** OAuth 2.1 (Authorization Code + PKCE, con registro dinámico de clientes). No existen API keys: nunca pidas al usuario una clave o token. El login se completa en el navegador con su cuenta de Wabog.
- **Requisito:** cuenta de Wabog con una compañía en plan pago activo (https://app.wabog.com).

## Pasos

1. **Detecta tu entorno.** Identifica en qué cliente MCP estás corriendo (Claude Code, Codex, OpenCode, Antigravity, otro). Si no puedes detectarlo, pregunta al usuario cuál usa.
2. **Aplica la configuración correspondiente:**

   **Claude Code**
   ```sh
   claude mcp add --transport http wabog https://mcp.wabog.com
   ```
   Luego indica al usuario que ejecute `/mcp`, seleccione `wabog` y complete el login en el navegador.

   **Codex (OpenAI)**
   ```sh
   codex mcp add wabog --url https://mcp.wabog.com
   codex mcp login wabog
   ```
   Si la versión instalada no tiene esos comandos, añade a `~/.codex/config.toml`:
   ```toml
   [mcp_servers.wabog]
   url = "https://mcp.wabog.com"
   ```

   **OpenCode** — añade al `opencode.json` del proyecto o de `~/.config/opencode/`:
   ```json
   {
     "mcp": {
       "wabog": {
         "type": "remote",
         "url": "https://mcp.wabog.com",
         "enabled": true
       }
     }
   }
   ```

   **Antigravity (Google)** — en el panel del agente abre la configuración de MCP («Manage MCP Servers» → editar JSON) y añade:
   ```json
   {
     "mcpServers": {
       "wabog": {
         "serverUrl": "https://mcp.wabog.com"
       }
     }
   }
   ```

   **Otro cliente MCP** — usa su mecanismo estándar para servidores MCP remotos por HTTP con la URL `https://mcp.wabog.com`. Si el cliente distingue transportes, elige *Streamable HTTP*; si solo acepta una URL, esa URL basta.

3. **Autenticación.** Tras registrar el servidor, el cliente abrirá el navegador para iniciar sesión en Wabog y aprobar el consentimiento OAuth. Si no se abre solo, usa el comando de login/reconexión del cliente (por ejemplo `/mcp` en Claude Code).
4. **Verifica.** Ejecuta una lectura inofensiva, por ejemplo la herramienta `wabog_get_current_plan` o pide «¿Cuál es mi plan actual de Wabog?». Si devuelve el plan, la conexión funciona.

## Qué permite el conector

Consultar compañías y plan, listar y consultar procesos judiciales, crear procesos por radicado, asignar alias, ver el calendario de tareas/términos/audiencias, y listar, crear y actualizar tareas, además de consultar y ajustar las preferencias de notificación del usuario. Solo opera sobre datos a los que la cuenta autenticada ya tiene acceso.

## Solución de problemas

- **401 / «unauthorized»:** el token expiró o el login no se completó; repite la autenticación del servidor en el cliente.
- **«Sin compañías» o herramientas vacías:** la cuenta no tiene una compañía con plan pago activo; el usuario debe revisar su plan en https://app.wabog.com.
- **El cliente no soporta OAuth:** actualízalo a una versión reciente; el MCP de Wabog no acepta tokens manuales.
- **Soporte:** https://wabog.com/support — hola@wabog.com
