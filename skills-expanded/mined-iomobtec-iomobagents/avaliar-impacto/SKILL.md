---
name: avaliar-impacto
description: "Estima o impacto e o esforço de uma mudança técnica em sistemas existentes. Use quando o arquiteto ou o tech-lead precisa dimensionar uma alteração antes de planejá-la."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: avaliar-impacto

Estima o **efeito de uma mudança técnica** sobre serviços, consumidores, contratos e dados existentes antes que a mudança seja implementada. Produz um mapa de impacto que permite ao time decidir com informação completa.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `dados.md`

---

## Quando usar

- Antes de alterar contrato de API existente (endpoint, campo, código de status)
- Antes de renomear ou remover entidade, tabela ou coluna com dados em produção
- Antes de atualizar dependência com breaking changes
- Antes de mudar padrão arquitetural usado por múltiplos serviços
- Quando o time não tem certeza se uma mudança é segura para fazer agora

---

## Entrada esperada

- Descrição da mudança proposta
- Serviço ou módulo onde a mudança ocorre
- Tipo de mudança: API, schema de banco, evento, dependência, padrão
- Ambiente de destino: DEV, STG ou PRD

---

## Processo de execução

### Passo 1 — Classificar a mudança

| Tipo | Exemplos | Risco base |
|---|---|---|
| Contrato de API | Remover campo, mudar tipo, novo campo obrigatório | Alto |
| Schema de banco | DROP COLUMN, renomear tabela, mudar tipo de coluna (`dados.md §2`, `seguranca.md §3`) | Crítico |
| Evento | Remover campo do payload, mudar tópico | Alto |
| Dependência | Major version bump, troca de biblioteca | Médio-Alto |
| Padrão de código | Mudar pattern usado em N serviços | Médio |
| Refatoração interna | Sem mudança de contrato ou schema | Baixo |

### Passo 2 — Mapear consumidores diretos

Para mudança de API ou evento:
- Quais serviços chamam o endpoint ou consomem o tópico?
- Quais ambientes (DEV, STG, PRD) têm consumidores ativos?
- Há consumidores externos (parceiros, mobile, integrações)?

Para mudança de schema:
- Quais serviços executam queries na tabela/coluna afetada?
- Há views, procedures ou triggers que dependem dessa estrutura?
- Há relatórios ou exports que leem diretamente?

### Passo 3 — Classificar cada impacto

| Impacto | Classificação | Ação necessária |
|---|---|---|
| Consumidor quebra imediatamente | Breaking — bloqueante | Não pode ir agora sem coordenação |
| Consumidor degradado mas funcional | Risco — deve ser tratado | Pode ir com janela de correção |
| Consumidor não afetado | Nenhum | Pode prosseguir |
| Consumidor beneficiado | Positivo | Comunicar melhoria |

### Passo 4 — Calcular blast radius

Quantificar:
- Número de serviços impactados
- Volume de tráfego na operação afetada (se disponível)
- Criticidade de negócio (caminho crítico vs secundário)
- Disponibilidade de rollback (é reversível se der errado?)

### Passo 5 — Recomendar estratégia de migração

| Situação | Estratégia |
|---|---|
| Breaking change em API pública | Versionar API; manter versão antiga por período definido |
| Breaking change em schema | Expandir-contrair (expand-contract): adicionar novo estado, migrar, remover antigo (`dados.md §2`) |
| Dependência com breaking change | Isolar atrás de adapter; testar em STG antes de PRD |
| Mudança sem consumidores | Pode ser feita diretamente |

---

## Saída produzida

```markdown
## Avaliação de Impacto: <descrição da mudança>

**Tipo:** Contrato de API | Schema | Evento | Dependência | Padrão  
**Serviço afetado:** <nome>  
**Ambiente(s):** DEV | STG | PRD  
**Risco global:** 🟢 Baixo | 🟡 Médio | 🔴 Alto | ⛔ Crítico

---

### Mapa de consumidores

| Consumidor | Tipo de impacto | Breaking? | Ação necessária |
|---|---|---|---|
| <serviço-a> | Campo removido da response | Sim | Atualizar antes do deploy |
| <serviço-b> | Novo campo opcional | Não | Nenhuma ação |
| <app-mobile> | Breaking change | Sim | Coordenar com time mobile |

---

### Blast radius

- Serviços impactados: N
- Volume estimado na operação: <N req/min ou N eventos/hora>
- Caminho crítico: Sim | Não
- Rollback possível: Sim | Não (e por quê)

---

### Estratégia de migração recomendada

1. <passo 1>
2. <passo 2>
3. <passo 3>

**Janela recomendada:** <imediato | próxima sprint | coordenar com stakeholders>

---

### Decisão necessária

⚠️ Esta mudança requer confirmação do time antes de prosseguir:
- <ponto de decisão 1>
- <ponto de decisão 2>
```
