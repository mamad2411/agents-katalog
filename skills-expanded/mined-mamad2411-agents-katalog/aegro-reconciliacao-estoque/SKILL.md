---
name: aegro-reconciliacao-estoque
description: Identificar e explicar divergencias entre estoque fisico, atividades e financeiro
version: 0.5.1
---

# Reconciliacao de Estoque

## Objetivo

Identificar e explicar divergencias entre o estoque registrado no sistema,
o consumo em atividades de campo e os lancamentos financeiros. Essencial
para auditoria, controle de insumos e fechamento de safra.

## Quando Usar

- Cliente reclama "estoque nao bate"
- Antes de fechamento de safra
- Auditoria periodica de insumos
- Compra registrada mas estoque nao aumentou
- Aplicacao feita mas estoque nao baixou

## Pre-requisitos de Conhecimento

Para detalhes dos comandos e regras de negocio:
- `/aegro-estoquista` -- locais, itens, movimentacoes, entradas, saidas
- `/aegro-agronomo` -- atividades, realizacoes (consumo de insumos)

## Formula de Reconciliacao

```
Estoque Teorico = Estoque Inicial
                  + Entradas (compras, devolucoes)
                  + Transferencias recebidas
                  - Consumo em atividades (realizacoes)
                  - Transferencias enviadas
                  - Saidas manuais (perdas, ajustes)

DIVERGENCIA = Estoque Atual (sistema) - Estoque Teorico
```

Se divergencia = 0, estoque esta conciliado.
Se divergencia != 0, investigar causas.

## Sequencia de Passos

### 1. Mapear locais de estoque

Listar armazens/depositos e guardar location_keys.

### 2. Identificar insumo alvo

Listar elementos por categoria (DEFENSIVE, FERTILIZER, SEED).
Se usuario especificou insumo, filtrar por nome.
Priorizar insumos criticos (alto valor ou uso frequente).

### 3. Verificar posicao atual

Buscar itens em estoque para o elemento selecionado.
Registrar quantidade atual por local e unidade de medida.

**Sinal de alerta:** Quantidade negativa indica problema de registro.

### 4. Levantar historico de movimentacoes

Buscar logs de estoque no periodo da safra e classificar:

| Tipo de movimentacao | Direcao |
|----------------------|---------|
| MANUAL_ENTRY | Entrada (compras) |
| MANUAL_REMOVAL | Saida (perdas, ajustes) |
| TRANSFER | Entrada ou saida (entre locais) |
| ACTIVITY_CONSUMPTION | Saida (uso em campo) |

Calcular totais de entrada e saida.

### 5. Cruzar com consumo em atividades

Buscar realizacoes no periodo e filtrar as que usaram o elemento.
Calcular total consumido em atividades.
Comparar com ACTIVITY_CONSUMPTION dos logs.

### 6. Calcular divergencia

Aplicar a formula de reconciliacao e quantificar a divergencia.

### 7. Investigar causas (se divergencia != 0)

Listar atividades que consomem o insumo (APPLICATION, FERTILIZATION, SOWING).
Verificar:
- Atividade planejada mas sem realizacao
- Realizacao registrada mas sem baixa de estoque
- Quantidade aplicada vs quantidade baixada

## Como Identificar Divergencias

| Divergencia | Significado | Causa mais provavel | Onde investigar |
|-------------|-------------|---------------------|-----------------|
| Atual > Teorico | Estoque "sobrando" | Entrada nao registrada | NFs de compra pendentes |
| Atual < Teorico | Estoque "faltando" | Saida nao registrada | Realizacoes sem baixa |
| Diverge por local | Deslocamento fisico | Transferencia nao feita | Movimentacoes entre locais |
| Quantidade negativa | Erro de registro | Saida antes da entrada | Ordem cronologica dos lancamentos |

**Diagnostico rapido:**
- Se diferenca corresponde a uma realizacao especifica, provavelmente e baixa nao registrada
- Se diferenca corresponde a um valor de NF, provavelmente e entrada nao registrada
- Se diferenca e pequena e difusa, pode ser arredondamento ou perda natural

## Formato de Resposta

```markdown
## Reconciliacao de Estoque: {{nome_insumo}}

### Posicao Atual
| Local | Quantidade | Unidade |
|-------|------------|---------|
| Armazem Central | 150 | L |
| Deposito Campo | 30 | L |
| **Total** | **180 L** | |

### Movimentacoes ({{inicio}} a {{fim}})
| Tipo | Quantidade |
|------|------------|
| Entradas (compras) | +500 L |
| Consumo em aplicacoes | -280 L |
| Ajustes/perdas | -20 L |
| **Saldo movimentado** | **+200 L** |

### Reconciliacao
| Item | Valor |
|------|-------|
| Estoque inicial | 50 L |
| + Movimentacoes | +200 L |
| = **Estoque teorico** | **250 L** |
| Estoque atual | 180 L |
| **DIVERGENCIA** | **-70 L** |

### Causa Provavel
- Aplicacao em 15/03 consumiu 50L sem baixa de estoque

### Acoes Recomendadas
1. Verificar realizacao de 15/03
2. Conferir fisicamente o estoque
3. Registrar ajuste se confirmado
```

## Proximos Workflows

| Situacao | Proximo workflow |
|----------|------------------|
| Corrigir lancamentos financeiros | `/aegro-lancamento-financeiro` |
| Verificar aplicacoes | `/aegro-monitoramento-pragas` |
| Visao geral da fazenda | `/aegro-visao-geral` |
| Fechar safra | `/aegro-fechamento-safra` |
