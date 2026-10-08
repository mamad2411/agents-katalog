# Agentes y Skills instalados — Claude Code

> Documento de referencia. Actualizado: 2026-05-07.

---

## Skills del plugin oficial (Anthropic)

Instalados vía `npx skills add` en:  
`C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\`

| Skill | Invocación | Descripción |
|---|---|---|
| `docx` | `/docx` | Editar y crear archivos Word (.docx). Scripts en `skills/docx/scripts/office/` |
| `pdf` | `/pdf` | Leer y manipular archivos PDF |
| `pptx` | `/pptx` | Editar presentaciones PowerPoint |
| `xlsx` | `/xlsx` | Editar hojas de cálculo Excel |
| `schedule` | `/schedule` | Crear tareas programadas (cron) en agentes remotos |
| `consolidate-memory` | `/consolidate-memory` | Consolidar y limpiar memorias del proyecto |
| `skill-creator` | `/skill-creator` | Crear nuevos skills personalizados |
| `setup-cowork` | `/setup-cowork` | Configurar entornos de trabajo colaborativo |

### Scripts del skill `docx` (Windows)

| Script | Comando |
|---|---|
| Desempaquetar | `python unpack.py doc.docx tmp_dir/` |
| Empaquetar | `python pack.py tmp_dir/ out.docx --original doc.docx --validate false` |
| Validar | `python validate.py doc.docx` |
| Convertir a PDF | `python soffice.py --headless --convert-to pdf doc.docx` |
| Aceptar cambios | `python accept_changes.py in.docx out.docx` |

> **Nota crítica:** Usar siempre `--validate false` en Windows (error cp1252 con `→`).

---

## Skills del marketplace (invocables con `/`)

Disponibles desde la sesión actual de Claude Code:

### Diseño y Frontend

| Skill | Descripción |
|---|---|
| `design-taste-frontend` | Senior UI/UX Engineer. Reglas métricas, CSS hardware acceleration, arquitectura de componentes |
| `gpt-taste` | Elite UX/UI + GSAP Motion Engineer. Tipografía editorial, bento grids, ScrollTriggers |
| `high-end-visual-design` | Diseño de agencia premium. Define fuentes, sombras, cards y animaciones de nivel alto |
| `minimalist-ui` | Interfaces editoriales limpias. Monocromo cálido, tipografía contrastada, sin gradientes |
| `industrial-brutalist-ui` | Interfaces mecánicas brutalistas. Grids rígidos, escala tipográfica extrema |
| `emil-design-eng` | Filosofía de UI polish de Emil Kowalski: animaciones, detalles invisibles, componentes |
| `stitch-design-taste` | DESIGN.md para Google Stitch. Tipografía anti-genérica, micro-animaciones |
| `redesign-existing-projects` | Actualiza proyectos existentes a estándares premium |

### Generación de imágenes / mockups

| Skill | Descripción |
|---|---|
| `brandkit` | Branding premium: logos, identidad visual, paletas, mockups |
| `image-to-code` | Genera imagen de diseño y luego la implementa como código |
| `imagegen-frontend-web` | Imágenes de referencia de diseño web (una imagen por sección) |
| `imagegen-frontend-mobile` | Conceptos de pantallas de apps móviles (iOS/Android) |

### Código y API

| Skill | Descripción |
|---|---|
| `claude-api` | Build, debug y optimización de apps con Anthropic SDK. Prompt caching incluido |
| `full-output-enforcement` | Fuerza código completo sin truncar ni usar placeholders |
| `simplify` | Revisa código cambiado por calidad, reutilización y eficiencia |

### Configuración y productividad

| Skill | Descripción |
|---|---|
| `update-config` | Configura `settings.json` del harness: hooks, permisos, env vars |
| `keybindings-help` | Personalizar atajos de teclado en `~/.claude/keybindings.json` |
| `fewer-permission-prompts` | Analiza transcripts y añade allowlist para reducir prompts de permisos |
| `loop` | Ejecuta un prompt o slash command en intervalo recurrente |
| `find-skills` | Descubre e instala skills disponibles según la necesidad |
| `init` | Inicializa un CLAUDE.md nuevo con documentación del proyecto |
| `review` | Revisa un pull request |
| `security-review` | Revisión de seguridad de los cambios en la rama actual |

### Context y memoria

| Skill | Descripción |
|---|---|
| `lean-ctx` | Context Runtime para agentes IA. 48 herramientas MCP, 10 modos de lectura, compresión 99% |

---

## MCP Servers activos (globales)

| Servidor | Herramientas clave |
|---|---|
| **Google Calendar** | `create_event`, `list_events`, `suggest_time`, `update_event` |
| **Supabase** | `execute_sql`, `apply_migration`, `deploy_edge_function`, `get_logs` |
| **Vercel** | `deploy_to_vercel`, `get_runtime_logs`, `list_deployments`, `get_project` |
| **Canva** | `generate_design`, `export_design`, `get_assets`, `start_editing_transaction` |
| **Miro/Coda** | `doc_create`, `doc_update`, `diagram_create`, `table_sync_rows` |
| **lean-ctx** | `ctx_read`, `ctx_shell`, `ctx_search`, `ctx_tree`, `ctx_knowledge`, `ctx_session` |
| **Semantic Search** | `semanticSearch` |
| **Scheduled Tasks** | `create_scheduled_task`, `list_scheduled_tasks` |

---

## Permisos globales (settings.json)

Ubicación: `C:\Users\User\.claude\settings.json`

Comandos preaprobados:
- `Bash(python *)` — ejecución de scripts Python
- `Bash(npx skills *)` — gestión de skills
- `Bash(git add *)`, `Bash(git commit -m ' *)` — operaciones git básicas
- MCP lean-ctx: `ctx_shell`, `ctx_read`, `ctx_search`, `ctx_discover_tools`, `ctx_session`, `ctx_tree`, `ctx_knowledge`
- MCP Supabase: `apply_migration`, `execute_sql`, `get_logs`
- MCP Vercel: `list_teams`

---

## Hooks activos (globales)

| Evento | Matcher | Acción |
|---|---|---|
| `PreToolUse` | `Bash\|bash` | `lean-ctx hook rewrite` — optimiza comandos Bash |
| `PreToolUse` | `Read\|Grep\|Search\|ListFiles\|...` | `lean-ctx hook redirect` — redirige lecturas a ctx_read |
