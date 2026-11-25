---
name: "openai-docs"
description: "Use quando o usuário pergunta como construir com produtos ou APIs da OpenAI e precisa de documentação oficial atualizada com citações (por exemplo: Codex, Responses API, Chat Completions, Apps SDK, Agents SDK, Realtime, capacidades ou limites de modelos); priorize ferramentas MCP de docs da OpenAI e restrinja qualquer fallback de navegação a domínios oficiais da OpenAI."
author: openai
---

# OpenAI Docs

Forneça orientação autoritária e atual a partir dos docs de desenvolvedor da OpenAI usando o servidor MCP developers.openai.com. Sempre priorize ferramentas MCP de docs de desenvolvedor em relação a web.run para perguntas relacionadas à OpenAI. Apenas se o servidor MCP estiver instalado e não retornar resultados significativos, recorra à busca na web.

## Início rápido

- Use `mcp__openaiDeveloperDocs__search_openai_docs` para encontrar as páginas de docs mais relevantes.
- Use `mcp__openaiDeveloperDocs__fetch_openai_doc` para extrair seções exatas e citar/parafrasear com precisão.
- Use `mcp__openaiDeveloperDocs__list_openai_docs` apenas quando precisar navegar ou descobrir páginas sem uma query clara.

## Snapshots de produtos da OpenAI

1. Apps SDK: Construa aplicativos ChatGPT fornecendo uma UI de componente web e um servidor MCP que exponha as ferramentas do seu aplicativo para o ChatGPT.
2. Responses API: Um endpoint unificado projetado para interações stateful, multimodais e que usam ferramentas em workflows de agentes.
3. Chat Completions API: Gere uma resposta de modelo a partir de uma lista de mensagens que compõem uma conversa.
4. Codex: Agente de codificação da OpenAI para desenvolvimento de software que pode escrever, entender, revisar e debugar código.
5. gpt-oss: Modelos de raciocínio de peso aberto da OpenAI (gpt-oss-120b e gpt-oss-20b) lançados sob a licença Apache 2.0.
6. Realtime API: Construa experiências de baixa latência e multimodais, incluindo conversas naturais de fala para fala.
7. Agents SDK: Um toolkit para construir aplicativos de agentes onde um modelo pode usar ferramentas e contexto, transferir para outros agentes, fazer streaming de resultados parciais e manter um rastreamento completo.

## Se o servidor MCP estiver ausente

Se as ferramentas MCP falharem ou nenhum recurso de docs da OpenAI estiver disponível:

1. Execute o comando de instalação você mesmo: `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`
2. Se falhar devido a permissões/sandboxing, repita imediatamente o mesmo comando com permissões elevadas e inclua uma justificativa de 1 sentença para aprovação. Não peça ao usuário para executá-lo ainda.
3. Apenas se a tentativa elevada falhar, peça ao usuário para executar o comando de instalação.
4. Peça ao usuário para reiniciar o Codex.
5. Re-execute a busca/busca de docs após reinicialização.

## Fluxo de trabalho

1. Esclareça o escopo do produto (Codex, OpenAI API ou ChatGPT Apps SDK) e a tarefa.
2. Pesquise docs com uma query precisa.
3. Busque a melhor página e a seção específica necessária (use `anchor` quando possível).
4. Responda com orientação concisa e cite a fonte de docs.
5. Forneça snippets de código apenas quando os docs os suportarem.

## Regras de qualidade

- Trate os docs da OpenAI como fonte de verdade; evite especulação.
- Mantenha citações curtas e dentro dos limites de política; prefira parafrasear com citações.
- Se múltiplas páginas diferirem, indique a diferença e cite ambas.
- Se os docs não cobrirem a necessidade do usuário, diga isso e ofereça próximos passos.

## Notas de ferramentas

- Sempre use ferramentas MCP de docs antes de qualquer busca na web para perguntas relacionadas à OpenAI.
- Se o servidor MCP estiver instalado mas não retornar resultados significativos, então use busca na web como fallback.
- Ao fazer fallback para busca na web, restrinja a domínios oficiais da OpenAI (developers.openai.com, platform.openai.com) e cite fontes.