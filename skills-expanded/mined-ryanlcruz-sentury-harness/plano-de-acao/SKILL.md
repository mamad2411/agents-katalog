---
name: plano-de-acao
vitrine:
  grupo: 'Entrega'
  rotulo: 'plano de ação e prioridades'
description: "Organiza ações, responsáveis, prazos e prioridades a partir de evidência."
version: 1.0.0
author: Sentury
license: MIT
metadata:
  gatilhos:
    - 'plano de a[çc][ãa]o'
    - '5w2h|matriz gut|\bgut\b'
    - 'plano (para|pra) (melhorar|resolver|reverter|corrigir)'
  category: cognitive
---

# Plano de ação sobre evidência

Transforma um diagnóstico em algo que alguém executa. A regra que vale para
todos os formatos: **cada número, causa e fato do plano vem de algo que já
está na conversa** — resultado de ferramenta, arquivo lido, dado que a pessoa
colou. O plano organiza a evidência; ele não cria evidência.

## Antes de montar

1. **Tem diagnóstico?** Se ainda não há evidência na conversa, levante primeiro
   (ler o arquivo, rodar o cálculo, pesquisar). Plano sem evidência é opinião
   com formato de documento.
2. **Qual formato?** Se a pessoa nomeou um, use esse. Se não, use o plano
   executivo (abaixo). Não troque o formato pedido por um "melhor".
3. **O que falta?** Dono, prazo e meta só entram se a pessoa disse. Se não
   disse, escreva `a definir` — nunca invente nome, data ou percentual.

## Os formatos

**5W2H** — tabela com O quê, Por quê, Onde, Quando, Quem, Como e Quanto.
Quem e Quanto costumam faltar: `a definir`.

**Matriz GUT** — tabela Gravidade × Urgência × Tendência (1 a 5 cada) por
fator, ordenada pelo produto. Diga de onde saiu cada nota; nota sem base é
chute, marque como "a validar com o time".

**Plano executivo** (padrão) — foco (o problema e a causa em duas linhas),
passo a passo em checklist e critério de aceite de cada passo.

## Registrar e entregar

- Se o plano tem etapas que alguém vai executar depois, grave com
  `criar_plano` (`nome`, `titulo`, `contexto` com o porquê e a evidência,
  `tarefas` com uma linha verificável por item). É o que faz o plano
  sobreviver à conversa e aparecer em Tarefas.
- Se a pessoa quer o documento, escreva o markdown e entregue com
  `entregar_arquivo`. Escrever no disco não entrega nada.
- Sempre diga de onde veio a evidência (arquivo, ferramenta, período).

## Exemplo

Evidência na conversa: a planilha de vendas mostrou queda de 8% no semestre,
concentrada na loja Centro, e as devoluções da loja subiram de 2% para 6%.

```
## Plano de ação
- [ ] Levantar o motivo das devoluções da loja Centro.
      Critério: motivos contados e fonte registrada. Responsável e prazo: a definir.
Fonte: vendas.xlsx, jan–jun.
```

Item bom de checklist: "Levantar o motivo das devoluções da loja Centro".
Item ruim: "Melhorar a satisfação dos clientes" (não dá para marcar feito).
