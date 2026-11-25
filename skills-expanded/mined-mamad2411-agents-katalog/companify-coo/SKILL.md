---
name: companify-coo
description: Transforma estratégia em capacidade operacional. Use para estruturar company/operations.md com processos críticos, capacidade e gargalos.
---

# Estruturar a operação (COO)

## Protocolo operacional

- **Plano e progresso:** planejar processos, capacidade, fornecedores e
  qualidade antes de escrever o artefato final.
- **Fontes de verdade:** ler `company/product.md`, `company/technology.md` e
  `company/finance.md` quando já produzidos.
- **Escopo e idempotência:** não redesenhar um processo já validado sem
  comprovação de que ele deixou de funcionar.
- **Validação:** cada processo crítico tem um dono, uma capacidade estimada
  e um sinal observável de gargalo.
- **Resumo final:** informar processos críticos, gargalos identificados e o
  que deve ser automatizado versus permanecer humano.

## Fluxo

Use a [checklist de operação](references/operations-checklist.md) para
mapear o fluxo de entrega, os processos críticos e os fornecedores.

1. Mapear como a empresa entrega sua promessa hoje, do pedido à entrega.
2. Identificar processos críticos, fornecedores, parceiros e recursos
   necessários.
3. Definir padrões de qualidade, atendimento, implantação, suporte e SLAs
   aplicáveis.
4. Identificar o que deve ser automatizado e o que precisa continuar humano,
   com o motivo de cada escolha.
5. Identificar gargalos e as capacidades que limitam o crescimento no
   estágio atual.
6. Salvar em `company/operations.md`, respondendo: como a empresa entrega sua
   promessa? Quais processos são críticos? Quais capacidades limitam o
   crescimento? Que partes devem ser automatizadas? Que partes precisam
   continuar humanas? Onde existem gargalos?

## Raciocínio do especialista

A pergunta central é: conseguimos entregar isso repetidamente, não apenas uma
vez? Um processo que funciona para o décimo cliente pode quebrar no
centésimo: testar cada processo contra o volume que o CRO e o CMO estão
projetando, não contra o volume atual. Automação sem processo estável documentado
apenas move o gargalo, não o resolve.
