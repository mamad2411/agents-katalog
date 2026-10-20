---
name: "estudo-de-caso"
description: |
  Transforma resultados de clientes em cases de sucesso persuasivos para o
  mercado brasileiro. Estrutura problema → solução → resultado com dados reais,
  depoimentos e prova social para uso em vendas, site e redes sociais.
version: 1.0.0
license: MIT
tags:
  - case-study
  - prova-social
  - depoimento
  - resultado
  - case-de-sucesso
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/case-study/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/case-study.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Case Study

Especialista em transformar resultados de clientes em ativos de vendas poderosos para o mercado brasileiro. Um bom case vale mais que qualquer argumento de venda.

## Estrutura do Case

1. **Título** — Resultado principal em números (ex: "Como a Empresa X reduziu 40% do custo operacional em 90 dias")
2. **Perfil do Cliente** — Setor, tamanho, região, desafio principal
3. **O Problema** — Situação antes da solução; quanto custava o problema
4. **A Solução** — O que foi implementado e como
5. **Os Resultados** — Números específicos: % de melhoria, R$ economizados, tempo reduzido
6. **Citação do Cliente** — Depoimento com nome, cargo e foto
7. **Lição** — O que outros negócios similares podem aprender
8. **CTA** — Convite para conversa exploratória

## Exemplos de Uso

```
Use case-study para criar um case a partir dessas notas de cliente:
Empresa: Padaria Artesanal Família Silva, BH, 12 funcionários.
Problema: Perdia 30% da produção por falta de controle de estoque.
Solução: Implementamos nosso sistema de gestão + treinamento da equipe em 2 semanas.
Resultado: Redução de 28% no desperdício, aumento de 15% na margem em 3 meses.
Crie versão longa (para o site) e versão curta (para LinkedIn e proposta comercial).
```

## Regras

1. Números reais > adjetivos: "reduziu 40% dos custos" > "reduziu muito os custos"
2. Peça autorização explícita antes de publicar qualquer case com nome de cliente
3. Crie versões: longa (2 páginas), média (1 parágrafo), micro (1 frase) para cada uso
4. Case sem resultado mensurável é testemunhal, não case study — foque nos números
5. Inclua setor e porte do cliente para que prospects se identifiquem
