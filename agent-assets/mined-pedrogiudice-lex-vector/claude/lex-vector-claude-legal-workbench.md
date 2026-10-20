# CLAUDE.md - Legal Workbench

Regras para desenvolvimento no Legal Workbench.

---

## Arquitetura Atual (2026-02-27)

**Stack: React SPA (Vite) + FastAPI Services + Traefik + ccui-backend (Rust)**

```
Browser ──> Traefik (:80) ──> React SPA (/)
                │
                ├──> FastAPI Services (/api/*)
                └──> ccui-backend (:8005) ──> tmux ──> Claude Code sessions
```

### Servicos Docker
| Servico | Rota | Porta | Stack |
|---------|------|-------|-------|
| reverse-proxy | - | 80, 8080 | Traefik v3.6.5 |
| frontend-react | `/` | 3000 | Vite + React 18 + nginx |
| api-stj | `/api/stj` | 8000 | FastAPI |
| api-text-extractor | `/api/text` | 8001 | FastAPI + Celery |
| api-doc-assembler | `/api/doc` | 8002 | FastAPI |
| api-ledes-converter | `/api/ledes` | 8003 | FastAPI |
| api-trello | `/api/trello` | 8004 | Bun |
| ccui-backend | `/api/ccui` | 8005 | Rust (axum + tokio + tmux) |
| redis | - | 6379 | Redis 7 Alpine |
| prometheus | - | 9090 | Prometheus v2.47.0 |

### ccui-backend (Wrapper Web para Claude Code)

Backend Rust que gerencia sessoes Claude Code via tmux headless para uso por advogados.

**Endpoints:**
- `GET /health` -- healthcheck
- `GET /api/sessions` -- lista sessoes ativas
- `GET /api/cases` -- lista casos disponiveis com metadados (ready, doc_count)
- `GET /api/sessions/{id}/channels` -- canais ativos de uma sessao (reconexao)
- `GET /ws` -- WebSocket (create_session, input, resize, output, agent_joined/left)

**Funcionalidades Phase 2:**
- Selecao de caso (case_id -> working_dir)
- Auto-start do Claude Code na sessao
- Auto-registro de canal "main" e canais de teammates
- Persistencia de metadados de sessao em disco
- 103 testes, clippy pedantic limpo

**Desenvolvimento:**
```bash
cd legal-workbench/ccui-backend
cargo test -- --test-threads=1
cargo clippy -- -W clippy::pedantic
cargo run  # porta 8005
```

---

## RULE 0: UMA UNICA ARQUITETURA

**NUNCA manter duas arquiteturas concomitantemente.**

- Um `docker-compose.yml`
- Um frontend (React)
- Uma fonte de verdade

> Arquiteturas antigas estao em `_archived/`

---

## Estrutura do Projeto

```
legal-workbench/
├── frontend/                # React SPA (Vite + TypeScript)
│   └── src/
│       ├── pages/           # HubHome, TrelloModule, DocAssembler, STJ
│       ├── components/      # Componentes React
│       │   ├── document/    # TipTapDocumentViewer, FieldList, FieldEditorPanel
│       │   ├── templates/   # TemplateList
│       │   ├── upload/      # DropZone
│       │   └── ui/          # Button, Modal, Input, CollapsibleSection
│       ├── extensions/      # TipTap extensions (FieldAnnotationMark)
│       ├── store/           # Zustand stores (documentStore)
│       ├── services/        # API clients
│       └── types/           # TypeScript types
├── docker/                  # Configuracao Docker
│   ├── services/            # Backends (doc-assembler, stj-api, etc)
│   ├── scripts/             # deploy.sh, health-check.sh
│   └── docker-compose.yml
├── ccui-backend/            # Rust backend (axum+tokio+tmux)
│   ├── src/                 # config, routes, session, tmux, pane_proxy, ws, team_watcher
│   └── tests/               # 103 testes (unit + integration)
├── ferramentas/             # Python tools standalone
│   ├── stj-dados-abertos/   # STJ data pipeline
│   └── legal-text-extractor/# OCR + AI extraction
├── docs/                    # Documentacao
└── _archived/               # POCs e arquiteturas antigas
```

---

## VEDACOES CRITICAS (NUNCA)

### Arquivos de Backup
**NUNCA criar arquivos de backup no repositorio:**
- `.old`, `.bak`, `.backup`, `.orig`, `.tmp`
- `*_antigo`, `*_backup`, `*_old`
- Copias de arquivos para "preservar"

> Use branches Git para preservar codigo. Hook PreToolUse bloqueia automaticamente.

### Separacao Front-Back
**NUNCA modificar frontend ao trabalhar em backend:**
- Tarefas de backend = APENAS arquivos em `ferramentas/` ou `docker/`
- Tarefas de frontend = APENAS arquivos em `frontend/`
- Excecao: alteracoes coordenadas explicitas no prompt

### Granularidade de Tarefas
**NUNCA trabalhar em multiplos modulos simultaneamente:**
- UM modulo por tarefa
- UM commit por mudanca logica
- Se prompt pede multiplos modulos: dividir em tarefas sequenciais

### Regressoes
**NUNCA usar codigo de versoes anteriores:**
- Se precisar de referencia, consulte Git history
- NAO copiar codigo de `_archived/`
- NAO "restaurar" versoes antigas de componentes

---

## Comandos

```bash
# Subir ambiente completo
cd legal-workbench
docker compose up -d

# Ver logs
docker compose logs -f frontend-react

# Rebuild apos mudancas
docker compose build frontend-react && docker compose up -d

# Acessar
http://localhost/           # Hub Home
http://localhost/trello     # Trello Command Center
http://localhost/doc-assembler
http://localhost/stj
```

---

## Definition of Done

1. Backend funcionando (teste via curl ou E2E)
2. Frontend renderiza corretamente
3. Testes E2E com `qa_commander` passam
4. Build Docker funciona

---

## Regras de Frontend

### Sempre Usar Subagente Especializado

| Tarefa | Subagente |
|--------|-----------|
| React/TypeScript | `frontend-developer` |
| UI/Design | `ui-designer` |
| E2E Testing | `qa_commander` |
| Review | `code-reviewer-superpowers` |

### Antes de Implementar

1. Confirmar expectativa de UI
2. Identificar endpoints necessarios
3. Definir estados de erro/loading

---

*Ultima atualizacao: 2026-01-17*
