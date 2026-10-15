---
name: tdd-antes-de-codigo
description: Use when implementing any feature or bug fix for a Track task, before writing production code — write a failing test first, watch it fail, then minimal code
---

# TDD Antes de Código

## Visão geral

Roubado do Superpowers `test-driven-development`, adaptado ao loop Track: o teste trava o **acceptance** da task, não um desejo abstrato.

**Anuncie:** "Usando tdd-antes-de-codigo."

**Pré-requisito:** `implementar-task` Fase 0 (MCP) já feita — senão volte e faça o gate de contexto.

## Lei de ferro

```
NENHUM CÓDIGO DE PRODUÇÃO SEM UM TESTE FALHANDO ANTES
```

Escreveu produção antes do teste? **Apague.** Comece de novo.  
Não "adapte" o código antigo enquanto escreve o teste. Delete = delete.

## Quando usar

**Sempre:** nova feature, bug fix, mudança de comportamento, refactor com risco.

**Exceções (pergunte ao humano):** protótipo jogável, código gerado, configs sem comportamento.

Pensou "só dessa vez pulo TDD"? Pare. É racionalização.

## Ciclo Red-Green-Refactor

1. **RED** — Um teste mínimo que descreve o comportamento do acceptance/RF  
2. **Verificar RED** — Rodar e ver falha *pela razão certa* (não erro de setup)  
3. **GREEN** — Código mínimo para passar  
4. **Verificar GREEN** — Suite relevante verde  
5. **REFACTOR** — Limpar mantendo verde  
6. Próximo comportamento → volte ao RED  

## Bom vs ruim

**Bom:** nome claro, um comportamento, assertiva no outcome real da task.  
**Ruim:** teste de mock theater, nome "works", assert só que mock foi chamado.

## Tie-in Track

- Acceptance items do `get_agent_execution_context` = lista de testes a vermelho  
- Não invente critérios fora do escopo MCP  
- Depois do verde: `verificar-antes-de-enviar` (suite + lint/tsc do repo)

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "Já sei que funciona" | Sem RED verificado, você não sabe se o teste testa |
| "Testo depois" | Depois = nunca / teste enviesado pelo código |
| "É só UI" | Ainda há contrato testável ou checklist de acceptance explícito |
| "O repo não tem testes" | Declare a limitação; ainda assim verifique acceptance + gates do repo |
