---
name: companify-interview
description: Conduz a descoberta empresarial progressiva. Use para preencher lacunas do Company Context sem aplicar um questionário fixo.
---

# Conduzir a entrevista empresarial

## Protocolo operacional

- **Plano e progresso:** planejar quais dimensões têm lacuna relevante antes
  de perguntar, e atualizar `.companify/interview.md` a cada resposta.
- **Fontes de verdade:** ler `.companify/config.yaml`,
  `.companify/company-context.md`, `.companify/interview.md` e o contexto
  Brandfy (`brand/strategy.md`, `brand/voice.md`) quando existente.
- **Escopo e idempotência:** nunca substituir uma resposta já confirmada por
  uma inferência. Uma pergunta respondida não é reaberta sem nova comprovação.
- **Validação:** cada resposta é classificada como fato, comprovação,
  declaração do usuário, inferência, hipótese ou premissa antes de entrar no
  Company Context.
- **Resumo final:** informar o que foi preenchido, o que segue como lacuna e
  qual skill deve receber a lacuna a seguir.

## Fluxo

1. Ler o Company Context atual e identificar quais dimensões têm campo em
   branco: origem da ideia, problema, solução, público, cliente, produto,
   diferenciais, concorrência, modelo atual, receita, custos, canais,
   operação, tecnologia, equipe, recursos, objetivos, restrições, ameaças,
   comprovações.
2. Priorizar as perguntas que alteram significativamente o negócio: uma
   lacuna que muda a tese (por exemplo, quem tem o problema) vem antes de uma
   lacuna cosmética (por exemplo, nome fantasia de um fornecedor).
3. Perguntar uma dimensão por vez, sem aplicar as ~70 perguntas possíveis de
   uma vez. Uma empresa em estágio `idea` precisa de profundidade em
   problema/solução/público; uma empresa em `growth` precisa de profundidade
   em tração/aquisição/operação.
4. Classificar cada resposta em [`FATO`, `COMPROVAÇÃO`, `DECLARAÇÃO DO
   USUÁRIO`, `CONTEXTO BRANDFY`, `INFERÊNCIA`, `HIPÓTESE`, `PREMISSA`] e
   registrar em `.companify/interview.md`.
5. Atualizar `.companify/company-context.md` com as respostas confirmadas.
6. Quando uma resposta for uma premissa crítica (alto impacto, ainda não
   verificável), registrar em `.companify/assumptions.md` usando o formato
   [`ASS-NNN`](references/assumption-record.md), com plano de validação e,
   quando fizer sentido, um experimento.
7. Registrar lacunas que exigem especialista de área (mercado, financeiro,
   técnico) como pendência endereçada à skill correspondente, em vez de
   tentar respondê-las genericamente.

Nunca invente uma resposta para "completar" o Company Context. Um campo sem
informação permanece em branco com a pergunta registrada: o Context Gate de
`$companify-builder` depende dessa honestidade para decidir se a esteira pode
avançar.

## Raciocínio do especialista

Tratar a entrevista como descoberta adaptativa: cada resposta pode tornar
duas ou três perguntas seguintes irrelevantes, ou abrir uma pergunta nova que
não estava prevista. Preferir perguntas que testam uma escolha concreta
("quem paga por isso hoje?") a perguntas abstratas ("qual sua visão de
futuro?"). Uma resposta vaga não é preenchida com uma suposição plausível:
vira uma premissa explícita com plano de validação.
