---
name: claude-code-sessions
description: Procure, analise e gerencie o histórico de sessões do Claude Code. Use quando o usuário quer encontrar sessões passadas, verificar uso de tokens, revisar análise de ferramentas, retomar trabalho anterior ou gerenciar tarefas entre sessões. Fornece 11 skills e um dashboard web.
---

# Claude Code Sessions

Plugin de inteligência de sessão para Claude Code. Lê os arquivos de sessão em JSONL que Claude Code gera em `~/.claude/projects/` e os torna pesquisáveis e analisáveis.

## O Que Faz

Claude Code registra cada sessão em um arquivo JSONL — mensagens, chamadas de ferramentas, contagens de tokens, diffs, tarefas. Este plugin lê esses arquivos e oferece duas interfaces. A maioria das operações é somente leitura; skills de exclusão e limpeza podem remover arquivos de sessão quando explicitamente invocados.

**11 skills** usáveis diretamente no Claude Code:

| Skill | Propósito |
|-------|---------|
| `/session-search "query"` | Busca de texto completo em todas as sessões |
| `/session-stats` | Uso de tokens, distribuição de modelos, análise de ferramentas |
| `/session-list` | Lista sessões ordenadas por recência, tamanho ou duração |
| `/session-detail` | Análise profunda de uma sessão específica |
| `/session-diff` | Compare duas sessões — arquivos, ferramentas, tópicos |
| `/session-timeline` | Visualização cronológica de sessões em um projeto |
| `/session-resume` | Gere um prompt de recuperação de contexto a partir de qualquer sessão |
| `/session-tasks` | Encontre tarefas pendentes e órfãs em todas as sessões |
| `/session-export` | Exporte uma sessão como markdown limpo |
| `/session-cleanup` | Encontre sessões vazias, minúsculas ou desatualizadas |
| `/session-delete` | Delete sessões e suas tarefas associadas |

**Dashboard web** em `localhost:3000` com quatro visualizações: Dashboard (estatísticas resumidas), Sessions (tabela ordenável com operações em massa), Search (busca de texto completo com snippets de contexto), Tasks (agrupadas por status com detecção de órfãs).

## Instalação

```bash
/plugin marketplace add apappascs/claude-code-sessions
/plugin install claude-code-sessions@claude-code-sessions
```

Sem chaves de API. Sem configuração. Sem dependências de runtime. Lê o que já está no disco.

Para o dashboard:

```bash
bun run ui
# → http://localhost:3000
```

## Arquitetura

Os mesmos módulos TypeScript alimentam skills, dashboard e CLI:

```
lib/formatters.ts      — utilitários puros, sem I/O
lib/session-parser.ts  — analisa um arquivo JSONL em dados estruturados
lib/session-store.ts   — verifica todas as sessões, agrega, pesquisa
ui/server.ts           — endpoints HTTP + entrega de arquivos estáticos
```

Cada arquivo lib funciona como um CLI autônomo:

```bash
bun run lib/session-store.ts list --sort recency --limit 10
bun run lib/session-store.ts search "database migration" --since 2025-01-01
bun run lib/session-parser.ts stats path/to/session.jsonl
```

## Casos de Uso

- Encontre a sessão onde você resolveu um problema específico semanas atrás
- Veja quais projetos consomem mais tokens
- Acompanhe tarefas pendentes em todas as sessões e projetos
- Retome uma sessão anterior com contexto completo
- Compare como duas sessões abordaram o mesmo problema
- Exporte transcrições de sessão para documentação

## Links

- **GitHub**: [github.com/apappascs/claude-code-sessions](https://github.com/apappascs/claude-code-sessions)
- **Licença**: MIT