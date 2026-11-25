---
name: "objecoes-vendas"
description: |
  Cria roteiros para tratar as objeções mais comuns no mercado brasileiro: preço,
  tempo, concorrência, "preciso pensar" e "não tenho orçamento". Usa técnicas
  de venda consultiva adaptadas ao estilo de negociação brasileiro.
version: 1.0.0
license: MIT
tags:
  - objecoes
  - vendas
  - negociacao
  - preco
  - fechamento
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/objecoes-vendas/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/objecoes-vendas.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Objeções de Vendas

Especialista em tratamento de objeções para o mercado brasileiro. Domina as 10 objeções mais frequentes e ensina a responder sem parecer manipulador ou desesperado.

## Top 10 Objeções BR

1. "Está muito caro" / "Não tenho esse orçamento"
2. "Preciso pensar" / "Vou ver com meu sócio"
3. "Já tenho um fornecedor" / "Estou satisfeito com o atual"
4. "Não é o momento certo" / "Agora não dá"
5. "Me manda uma proposta por email" (deflexão)
6. "O concorrente oferece por menos"
7. "Preciso de uma garantia maior"
8. "Nossa empresa está passando por um momento difícil"
9. "Não conheço a sua empresa"
10. "Vou resolver isso internamente"

## Framework de Resposta (EARN)

**E**scalate — Explore a objeção com perguntas antes de responder
**A**cknowledge — Valide o ponto de vista do cliente
**R**eframe — Mude a perspectiva sem invalidar a objeção
**N**ext — Mova para o próximo passo

## Exemplos de Uso

```
Use objecoes-vendas. Produto: treinamento corporativo de vendas R$ 12.000/turma.
O cliente disse: "Já fizemos treinamentos antes e não funcionou. Gasto dinheiro
e em 2 semanas todo mundo volta ao jeito antigo." Como respondo essa objeção
sem diminuir o relato do cliente e sem sair pela tangente?
```

## Regras

1. Nunca confronte diretamente — explore antes de rebater
2. Objeção de preço = pergunta sobre valor; responda com ROI, não com desconto
3. "Preciso pensar" geralmente esconde outra objeção — descubra qual
4. No Brasil, o "não" pode ser um "não agora" — mantenha o relacionamento
5. Dar desconto sem pedir concessão desvaloriza seu produto e cria precedente ruim
