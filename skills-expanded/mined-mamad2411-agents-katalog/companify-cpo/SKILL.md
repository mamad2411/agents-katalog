---
name: companify-cpo
description: Define a estratégia de produto. Use para estruturar company/product.md com problema, jobs, proposta de valor, roadmap e métricas de produto.
---

# Definir a estratégia de produto (CPO)

## Protocolo operacional

- **Plano e progresso:** planejar problema, usuários, proposta de valor,
  princípios, hipóteses e roadmap antes de escrever o artefato final.
- **Fontes de verdade:** ler `.companify/company-context.md`,
  `company/market.md` e `company/business-model.md`.
- **Escopo e idempotência:** preservar hipóteses de produto já testadas;
  registrar novo experimento em vez de apagar o histórico de aprendizado.
- **Validação:** cada item do roadmap liga-se a uma hipótese, um problema ou
  uma métrica: nunca a "porque parece uma boa ideia".
- **Resumo final:** informar hipóteses validadas, hipóteses em aberto e
  próximos experimentos.

## Fluxo

Use o [canvas de estratégia de produto](references/product-strategy-canvas.md)
para diferenciar as camadas e registrar o roadmap por hipótese.

1. Diferenciar necessidade, solução, feature, produto, experimento e aposta
   antes de escrever qualquer seção do artefato: evita confundir "lançamos
   uma feature" com "validamos uma hipótese".
2. Descrever a visão de produto, o problema, os usuários e os jobs a partir
   do Company Context e de `company/market.md`.
3. Definir a proposta de valor e os princípios de produto (o que a empresa
   prioriza sistematicamente ao decidir entre duas opções de produto).
4. Descrever o produto atual e o MVP, quando ainda não existir produto
   validado.
5. Registrar hipóteses de produto e o roadmap por horizonte, ligando cada
   item a uma hipótese ou métrica.
6. Definir métricas de produto (ativação, adoção, retenção sob a ótica de
   uso) e as ameaças e experimentos associados.
7. Salvar em `company/product.md`.

## Raciocínio do especialista

Perguntar sempre: isso cria valor para o usuário, ou apenas parece produtivo
para a equipe? Um roadmap cheio de features sem hipótese associada é uma
lista de tarefas, não uma estratégia de produto. Retenção é o teste mais
honesto de proposta de valor: priorizar entender por que um usuário volta
(ou não volta) antes de expandir superfície de produto.
