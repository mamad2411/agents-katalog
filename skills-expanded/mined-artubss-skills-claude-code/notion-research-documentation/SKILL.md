---
name: notion-research-documentation
description: Pesquise em várias páginas Notion e sintetize em documentação estruturada; use quando estiver coletando informações de múltiplas fontes Notion para produzir resumos, comparações ou relatórios com citações.
metadata:
  short-description: Pesquise conteúdo Notion e produza resumos/relatórios
---

# Pesquisa e Documentação

Extraia páginas Notion relevantes, sintetize os achados e publique resumos ou relatórios claros (com citações e links para as fontes).

## Início rápido
1) Encontre fontes com `Notion:notion-search` usando queries direcionadas; confirme o escopo com o usuário.
2) Busque páginas via `Notion:notion-fetch`; anote seções-chave e capture citações (`reference/citations.md`).
3) Escolha o formato de saída (resumo executivo, síntese, comparação, relatório completo) usando `reference/format-selection-guide.md`.
4) Rascunhe em Notion com `Notion:notion-create-pages` usando o template correspondente (resumo executivo, síntese, comparação, completo).
5) Ligue as fontes e adicione uma seção de referências/citações; atualize conforme novas informações chegam com `Notion:notion-update-page`.

## Fluxo de trabalho
### 0) Se alguma chamada MCP falhar porque Notion MCP não está conectado, pause e configure:
1. Adicione o Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Ative o cliente MCP remoto:
   - Configure `[features].rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login notion`

Após o login bem-sucedido, o usuário terá que reiniciar o codex. Você deve finalizar sua resposta e informá-lo para que da próxima vez ele possa continuar com a Etapa 1.

### 1) Colete fontes
- Pesquise primeiro (`Notion:notion-search`); refine queries e peça ao usuário para confirmar se múltiplos resultados aparecerem.
- Busque páginas relevantes (`Notion:notion-fetch`), examine fatos, métricas, afirmações, restrições e datas.
- Rastreie cada URL/ID de fonte para citação posterior; prefira citações diretas para fatos críticos.

### 2) Selecione o formato
- Leitura rápida → resumo executivo rápido.
- Aprofundamento em um tópico → síntese de pesquisa.
- Tradeoffs de opções → comparação.
- Aprofundamento / pronto para executivo → relatório completo.
- Veja `reference/format-selection-guide.md` para quando escolher cada um.

### 3) Sintetize
- Faça um esboço antes de escrever; agrupe achados por temas/questões.
- Anote evidências com IDs de fonte; sinalize lacunas ou contradições.
- Mantenha o objetivo do usuário em vista (decisão, resumo, plano, recomendação).

### 4) Crie o documento
- Escolha o template correspondente em `reference/` (resumo executivo, síntese, comparação, completo) e adapte.
- Crie a página com `Notion:notion-create-pages`; inclua título, sumário, principais achados, evidências de apoio e recomendações/próximos passos quando relevante.
- Adicione citações inline e uma seção de referências; ligue de volta às páginas de fonte.

### 5) Finalize e entregue
- Adicione destaques, riscos e questões em aberto.
- Se o usuário precisar de acompanhamentos, crie tarefas ou uma checklist na página; ligue qualquer entrada de banco de dados de tarefas se aplicável.
- Compartilhe um changelog breve ou status usando `Notion:notion-update-page` ao atualizar.

## Referências e exemplos
- `reference/` — táticas de pesquisa, seleção de formato, templates e regras de citação (ex: `advanced-search.md`, `format-selection-guide.md`, `research-summary-template.md`, `comparison-template.md`, `citations.md`).
- `examples/` — passo-a-passo completos (ex: `competitor-analysis.md`, `technical-investigation.md`, `market-research.md`, `trip-planning.md`).