# AGENTS — Workspace

## Escopo
- Monorepo com backend em `api/` e frontend em `frontend/`.
- Este arquivo define diretrizes gerais para qualquer agente na raiz.

## Regras gerais
- Preserve separacao de responsabilidades entre `api/` e `frontend/`.
- Priorize mudancas pequenas, seguras e testaveis.
- Nao altere contratos publicos sem atualizar ambos os lados (API e UI).
- Respeite as regras de negocio descritas em `docs/tasks.md`.

## Validacao minima
- Backend: validar inicializacao da API e rotas afetadas.
- Frontend: validar build/lint e fluxo principal impactado.
- Sempre listar arquivos alterados e riscos pendentes.

## Diretrizes da API

### Escopo
- Backend FastAPI em `api/`.

### Regras de implementacao
- Centralize regras de negocio em `services/`.
- Mantenha `routers/` enxutos (validacao de entrada e delegacao).
- Preserve consistencia entre `models/`, `schemas.py` e migracoes.
- Garanta operacoes criticas com transacao quando aplicavel.

### Regras de dominio prioritarias
- Um funcionario so pode ter 1 tarefa em andamento.
- Um vinculo por tarefa por vez.
- Roubo de vinculo apenas quando tarefa estiver pausada.
- Finalizacao apenas na ultima etapa.

### Validacao minima
- Testar endpoints afetados e cenarios de pre-condicao.
- Verificar regressao nas rotas existentes relacionadas.
- Reportar arquivos alterados, testes executados e riscos.

## Diretrizes do Frontend

### Objetivo
- Interface tecnica, densa e clara, com visual industrial-refinado.
- Sidebar escura fixa como ancora visual.
- Timer verde sempre visivel quando houver sessao ativa.
- Animacoes curtas e funcionais, sem excesso decorativo.

### Design System
- Tema claro como padrao; dark mode opcional com persistencia em `localStorage`.
- Paleta principal: verdes da marca, cinzas neutros, cores semanticas de status e feedback.
- Tipografia:
	- `Barlow Condensed`: titulos e labels.
	- `DM Sans`: corpo, tabelas e formularios.
	- `JetBrains Mono`: timer, duracao e timestamps.
- Espacamento em multiplos de 4px.

### Layout Base
- Sidebar fixa: 240px.
- Header de pagina: 56px.
- Conteudo com padding lateral de 32px e largura util maxima de 1200px.

### Componentes obrigatorios
- Sidebar com navegacao por papel (Funcionario/Admin).
- Header com titulo, breadcrumb e ate 2 acoes.
- Botoes: primario, secundario, destrutivo e icon-only.
- Badge de status com variantes e pulso no status ativo.
- Card de atividade com destaque de sessao ativa e timer.
- TimerBanner sticky no topo da area de conteudo.
- Inputs e tabelas consistentes com o design system.
- Modal com overlay e foco controlado.
- Toast no canto inferior direito com auto-dismiss.
- Arvore no admin: Edificio > Lajes > Atividades, com expand/collapse.

### Fluxos principais
1. Selecao de usuario no primeiro acesso (salva no `localStorage`).
2. Funcionario: iniciar/finalizar sessao em Minhas atividades.
3. Historico: filtros por periodo + resumo + tabela.
4. Admin Dashboard: atividades ativas, progresso por edificio e graficos.
5. Admin Edificios: arvore, busca e criacao com preview de lajes.
6. Admin Usuarios: listagem, criacao e ativacao/inativacao.

### Interacoes e movimento
- Transicoes entre 150ms e 300ms para estados de UI.
- Suporte obrigatorio a `prefers-reduced-motion`.
- Feedback imediato em hover, focus e clique.

### Acessibilidade minima
- `focus-visible` em todos os elementos interativos.
- `aria-label` em botoes icon-only e badges de status.
- Modal com focus trap e retorno de foco ao elemento de origem.
- Timer com `aria-live="polite"`, evitando atualizacao a cada segundo para leitor de tela.
- Contraste minimo WCAG AA.

### Checklist de implementacao
1. Definir variaveis globais e fontes.
2. Implementar estado de sessao ativa via Context + timer com cleanup.
3. Entregar Badge, TimerBanner, CardAtividade, Modal e Toast.
4. Entregar arvore expansivel com animacao e suporte a multiplas aberturas.
5. Cobrir estados vazios nas listas.
6. Integrar WebSocket no dashboard admin.
7. Implementar dark mode com persistencia.
8. Validar acessibilidade basica em toda a UI.


## vexp <!-- vexp v1.3.11 -->

**MANDATORY: use `run_pipeline` — do NOT grep or glob the codebase.**
vexp returns pre-indexed, graph-ranked context in a single call.

### Workflow
1. `run_pipeline` with your task description — ALWAYS FIRST (replaces all other tools)
2. Make targeted changes based on the context returned
3. `run_pipeline` again only if you need more context

### Available MCP tools
- `run_pipeline` — **PRIMARY TOOL**. Runs capsule + impact + memory in 1 call.
  Auto-detects intent. Includes file content. Example: `run_pipeline({ "task": "fix auth bug" })`
- `get_context_capsule` — lightweight, for simple questions only
- `get_impact_graph` — impact analysis of a specific symbol
- `search_logic_flow` — execution paths between functions
- `get_skeleton` — compact file structure
- `index_status` — indexing status
- `get_session_context` — recall observations from sessions
- `search_memory` — cross-session search
- `save_observation` — persist insights (prefer run_pipeline's observation param)

### Agentic search
- Do NOT use built-in file search, grep, or codebase indexing — always call `run_pipeline` first
- If you spawn sub-agents or background tasks, pass them the context from `run_pipeline`
  rather than letting them search the codebase independently

### Smart Features
Intent auto-detection, hybrid ranking, session memory, auto-expanding budget.

### Multi-Repo
`run_pipeline` auto-queries all indexed repos. Use `repos: ["alias"]` to scope. Run `index_status` to see aliases.
<!-- /vexp -->