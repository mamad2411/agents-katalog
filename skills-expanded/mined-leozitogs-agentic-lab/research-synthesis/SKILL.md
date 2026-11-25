---
name: research-synthesis
description: Use this skill whenever the user provides multiple sources (papers, articles, transcripts, docs) and asks for a comparative synthesis, briefing, or actionable recommendation. Do NOT use when there is only one source (that's summarization, not synthesis) or when the user wants creative/opinion content.
tipo: skill
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Research Synthesis Skill

## Objetivo

Transformar múltiplas fontes brutas em uma síntese estruturada com fatos separados de hipóteses, comparação cruzada e próximos passos acionáveis.

## Quando usar

- Usuário cola 2+ artigos e pede comparação.
- Usuário pede briefing sobre um tema com fontes anexadas.
- Usuário pede "o que esses textos têm em comum?" ou "onde divergem?".

## Quando NÃO usar

- Só uma fonte → use parafraseamento ou resumo.
- Texto criativo, opinativo ou ficcional.
- Perguntas factuais simples sem fontes.

## Pré-requisitos

- Fontes fornecidas em texto ou anexos legíveis.
- Pergunta de pesquisa explícita (se ausente, perguntar antes).

## Processo

1. Confirme a pergunta de pesquisa. Se ambígua, pergunte uma única clarificação.
2. Liste as fontes recebidas com resumo de uma linha cada.
3. Para cada fonte, extraia: claims, evidence, assumptions, gaps.
4. Separe **fact / hypothesis / opinion**.
5. Compare lado a lado: agreements, disagreements, silences.
6. Marque incertezas com nível de confiança (alta/média/baixa).
7. Produza síntese acionável em **next steps**.

## Recursos auxiliares

- `examples.md` — exemplos com fontes reais.
- `references.md` — fontes metodológicas.
- `tests.md` — casos de teste.

## Saída esperada

Markdown com a seguinte estrutura:

```md
## Question
## Sources considered
## Findings
  ### Agreed across sources
  ### Disagreements
  ### Gaps
## Risks and unknowns
## Recommended next steps
```

## Critérios de qualidade

- Cada claim relevante referencia a fonte.
- Disagreements explicitamente nomeados.
- Next steps no formato verbo + objeto + critério de sucesso.
- Não inventa fontes.
- Marca inferências como tal.

## Testes

Ver `tests.md`. Resumo:

- Caso positivo: 3 papers sobre RAG → síntese com 4 agreements, 2 disagreements, 1 gap.
- Caso negativo: 1 paper sozinho → skill NÃO deve carregar, modelo deve resumir em vez de comparar.
- Caso borda: 2 fontes contraditórias sobre o mesmo número → skill deve marcar como disagreement de alta importância.
