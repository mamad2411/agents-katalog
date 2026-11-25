# PinchTab Browser Automation

Skill para controlar navegadores web usando PinchTab MCP.

## Requisitos

- Docker instalado y corriendo
- Claude Code CLI

## Instalacion

### 1. Clonar el wrapper

```bash
cd ~
git clone https://github.com/BDuba/pinchtab-mcp-wrapper.git .pinchtab-mcp-wrapper
cd .pinchtab-mcp-wrapper
```

### 2. Crear imagen Docker

```bash
docker build -t pinchtab:local .
```

### 3. Crear contenedor

```bash
docker run -d \
  --name pinchtab \
  -p 127.0.0.1:9867:9867 \
  -e PINCHTAB_TOKEN=pinchtab-token-local-secure-2026-platanos-con-nata \
  pinchtab:local
```

### 4. Crear script wrapper

Crear `~/.pinchtab-mcp-wrapper/run-mcp.sh`:

```bash
#!/bin/bash
export PINCHTAB_MODE=external
export PINCHTAB_HOST=127.0.0.1
export PINCHTAB_PORT=9867
export PINCHTAB_TOKEN=pinchtab-local-secure-2026

cd ~/.pinchtab-mcp-wrapper
node dist/index.js
```

Dar permisos:

```bash
chmod +x ~/.pinchtab-mcp-wrapper/run-mcp.sh
```

### 5. Configurar MCP en Claude Code

Crear/editar `~/.mcp.json`:

```json
{
  "mcpServers": {
    "pinchtab": {
      "command": "bash",
      "args": ["C:/Users/TU_USUARIO/.pinchtab-mcp-wrapper/run-mcp.sh"]
    }
  }
}
```

### 6. Reiniciar Claude Code

Cerrar y abrir Claude Code para cargar el MCP.

---

## Configuracion actual

- **Modo:** `external` (conecta a contenedor existente)
- **Contenedor:** `pinchtab` en `127.0.0.1:9867`
- **Token:** `pinchtab-local-secure-2026`

## Verificar estado

Antes de usar, verificar que PinchTab esta operativo:

```
mcp__pinchtab__pinchtab_health
```

Si no responde, el contenedor puede estar apagado:

```bash
docker start pinchtab
```

## Herramientas principales

### Navegacion

| Tool | Uso |
|------|-----|
| `tab_list` | Listar pestanas abiertas |
| `tab_open` | Abrir nueva pestana con URL |
| `navigate` | Navegar a URL en pestana existente |
| `tab_close` | Cerrar pestana |

### Lectura de contenido

| Tool | Uso |
|------|-----|
| `read_page` | Extraer texto limpio (eficiente en tokens) |
| `snapshot` | Arbol de accesibilidad completo |
| `list_interactives` | Botones, links, inputs |
| `text` | Texto raw o con readability |

### Interaccion

| Tool | Uso |
|------|-----|
| `action` | click, type, fill, hover, scroll |
| `screenshot` | Capturar imagen de la pagina |
| `evaluate` | Ejecutar JavaScript |
| `download` | Descargar archivos |

## Flujo tipico

1. **Verificar health:** `pinchtab_health`
2. **Listar tabs:** `tab_list` para obtener tabId
3. **Navegar:** `navigate` con tabId y url
4. **Leer:** `read_page` para contenido o `list_interactives` para elementos
5. **Interactuar:** `action` con kind (click/type/fill) y ref del elemento

## Ejemplo: Leer pagina web

```
1. tab_list -> obtener tabId activo
2. navigate(tabId, "https://example.com")
3. read_page(tabId) -> texto limpio
```

## Ejemplo: Llenar formulario

```
1. navigate a la pagina
2. list_interactives -> obtener refs de inputs
3. action(kind="fill", ref="e5", text="valor")
4. action(kind="click", ref="e10") -> submit
```

## Troubleshooting

| Problema | Solucion |
|----------|----------|
| Health no responde | `docker start pinchtab` |
| Contenedor no existe | Verificar `~/.pinchtab-mcp-wrapper/` |
| Timeout en acciones | Verificar que la pagina cargo completamente |
| Elemento no encontrado | Usar `snapshot` para ver estructura actual |

## Archivos de configuracion

- `~/.mcp.json` - Config MCP
- `~/.pinchtab-mcp-wrapper/run-mcp.sh` - Script wrapper
- `~/.claude/projects/.../memory/pinchtab-setup.md` - Setup detallado

---

**Nota:** Para usar este skill en Claude Code, guarda este archivo en `~/.claude/commands/pinchtab.md` y usa `/pinchtab` para acceder a la referencia completa.
