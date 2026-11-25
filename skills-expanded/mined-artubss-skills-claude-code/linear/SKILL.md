---
name: linear
description: Gerencie issues, projetos e workflows de equipe no Linear. Use quando o usuário deseja ler, criar ou atualizar tickets no Linear.
metadata:
  short-description: Gerencie issues do Linear no Codex
---

# Linear

## Visão Geral

Esta skill oferece um workflow estruturado para gerenciar issues, projetos e workflows de equipe no Linear. Ela garante integração consistente com o servidor Linear MCP, que fornece gerenciamento de projetos em linguagem natural para issues, projetos, documentação e colaboração em equipe.

## Pré-requisitos
- O servidor Linear MCP deve estar conectado e acessível via OAuth
- Confirme o acesso ao workspace, equipes e projetos relevantes do Linear

## Workflow Obrigatório

**Siga estas etapas na ordem. Não pule etapas.**

### Etapa 0: Configurar Linear MCP (se ainda não estiver configurado)

Se qualquer chamada MCP falhar porque Linear MCP não está conectado, pause e configure:

1. Adicione o Linear MCP:
   - `codex mcp add linear --url https://mcp.linear.app/mcp`
2. Ative o cliente MCP remoto:
   - Defina `[features] rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login linear`

Após o login bem-sucedido, o usuário terá que reiniciar o codex. Você deve finalizar sua resposta e informá-lo que quando tentar novamente poderá prosseguir com a Etapa 1.

**Nota para Windows/WSL:** Se você ver erros de conexão no Windows, tente configurar o Linear MCP para ser executado via WSL:
```json
{"mcpServers": {"linear": {"command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/sse", "--transport", "sse-only"]}}}
```

### Etapa 1
Esclareça o objetivo e escopo do usuário (ex: triagem de issues, planejamento de sprint, auditoria de documentação, balanceamento de carga de trabalho). Confirme equipe/projeto, prioridade, labels, ciclo e datas de vencimento conforme necessário.

### Etapa 2
Selecione o workflow apropriado (veja Workflows Práticos abaixo) e identifique as ferramentas Linear MCP que você precisará. Confirme os identificadores necessários (ID do issue, ID do projeto, chave da equipe) antes de chamar as ferramentas.

### Etapa 3
Execute chamadas de ferramentas Linear MCP em lotes lógicos:
- Leia primeiro (list/get/search) para construir contexto.
- Crie ou atualize em seguida (issues, projetos, labels, comentários) com todos os campos obrigatórios.
- Para operações em massa, explique a lógica de agrupamento antes de aplicar mudanças.

### Etapa 4
Resuma os resultados, destaque lacunas ou bloqueadores restantes e proponha próximas ações (issues adicionais, mudanças de labels, atribuições ou comentários de acompanhamento).

## Ferramentas Disponíveis

Gerenciamento de Issues: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_my_issues`, `list_issue_statuses`, `list_issue_labels`, `create_issue_label`

Projeto & Equipe: `list_projects`, `get_project`, `create_project`, `update_project`, `list_teams`, `get_team`, `list_users`

Documentação & Colaboração: `list_documents`, `get_document`, `search_documentation`, `list_comments`, `create_comment`, `list_cycles`

## Workflows Práticos

- Planejamento de Sprint: Revise issues abertos para uma equipe alvo, escolha os principais itens por prioridade e crie um novo ciclo (ex: "Sprint de Performance Q1") com atribuições.
- Triagem de Bugs: Liste bugs críticos/de alta prioridade, classifique por impacto do usuário e mova os principais itens para "In Progress".
- Auditoria de Documentação: Pesquise documentação (ex: autenticação de API), depois abra issues marcadas com "documentation" para lacunas ou seções desatualizadas com correções detalhadas.
- Balanceamento de Carga de Trabalho da Equipe: Agrupe issues ativas por responsável, sinalize qualquer um com carga alta e sugira ou aplique redistribuições.
- Planejamento de Release: Crie um projeto (ex: "Release v2.0") com milestones (congelamento de funcionalidades, beta, docs, lançamento) e gere issues com estimativas.
- Dependências Entre Projetos: Encontre todos os issues "bloqueados", identifique os bloqueadores e crie issues vinculados se faltarem.
- Atualizações de Status Automatizadas: Encontre seus issues com atualizações antigas e adicione comentários de status baseados no estado atual/bloqueadores.
- Etiquetagem Inteligente: Analise issues sem label, sugira/aplique labels e crie categorias de labels faltantes.
- Retrospectivas de Sprint: Gere um relatório do último ciclo concluído, observe trabalho concluído vs. adiado e abra issues de discussão para padrões.

## Dicas para Produtividade Máxima

- Agrupe operações por mudanças relacionadas; considere templates inteligentes para estruturas de issues recorrentes.
- Use queries em linguagem natural quando possível ("Mostre-me o que João está trabalhando esta semana").
- Aproveite o contexto: referencie issues anteriores em novas solicitações.
- Quebre grandes atualizações em lotes menores para evitar limites de taxa; armazene em cache ou reutilize filtros ao listar com frequência.

## Solução de Problemas

- Autenticação: Limpe cookies do navegador, execute novamente OAuth, verifique permissões de workspace, garanta que o acesso à API esteja habilitado.
- Erros ao Chamar Ferramentas: Confirme que o modelo suporta múltiplas chamadas de ferramentas, forneça todos os campos obrigatórios e divida solicitações complexas.
- Dados Faltando: Atualize o token, verifique o acesso ao workspace, procure por projetos arquivados e confirme a seleção correta de equipe.
- Performance: Lembre-se dos limites de taxa da API Linear; agrupe operações em massa, use filtros específicos ou armazene consultas frequentes em cache.