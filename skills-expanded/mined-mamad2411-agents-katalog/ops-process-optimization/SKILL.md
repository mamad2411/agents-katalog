---
name: ops-process-optimization
description: Analisar e melhorar processos de negócio. Use quando o processo está lento, como podemos melhorar, simplificar esse workflow, muitos passos, gargalo, ou quando o usuário descreve um processo ineficiente que quer corrigir. Agente Clawdia.
argument-hint: "<nome ou descrição do processo a otimizar>"
---

# /ops-process-optimization

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Analisa processos existentes e recomenda melhorias. Adaptado para o contexto da Evolution API: time pequeno, startup de ops, remoto-first.

## Agente

Clawdia — hub operacional, calendário, emails, tarefas, decisões.

## Framework de Análise

### 1. Mapear Estado Atual
- Documentar cada etapa, ponto de decisão e handoff
- Identificar quem faz o quê e quanto tempo cada etapa leva
- Anotar etapas manuais, aprovações e tempos de espera

### 2. Identificar Desperdício

Nas operações da Evolution, os desperdícios mais comuns são:

| Tipo | Descrição | Exemplos Evolution |
|------|-----------|-------------------|
| **Espera** | Tempo em filas ou aguardando aprovações | Aprovações presas com Davidson, espera por review de PR |
| **Retrabalho** | Etapas que falham e precisam ser refeitas | Bug reportado após deploy, issue mal especificada |
| **Handoffs** | Cada handoff é ponto potencial de falha/delay | Danilo → Guilherme → Davidson → Cliente |
| **Superprocessamento** | Etapas que não agregam valor | Reuniões que poderiam ser mensagem no Discord |
| **Trabalho manual** | Tarefas que poderiam ser automatizadas | Rotinas já automatizadas via `make scheduler` |
| **Sincronização forçada** | Bloquear progresso desnecessariamente | Esperar todo o time para tomar uma decisão |

### 3. Desenhar Estado Futuro
- Eliminar etapas desnecessárias
- Automatizar onde possível (ver rotinas em `ADWs/`)
- Reduzir handoffs
- Paralelizar etapas independentes
- Adicionar checkpoints (não gates)
- Delegar mais decisões para o time sem precisar passar por Davidson

### 4. Medir Impacto
- Tempo economizado por ciclo
- Redução de taxa de erros
- Economia de custo
- Melhoria de satisfação do time

## Análise de Automação

Para o contexto Evolution, avaliar sempre se a melhoria pode ser:

| Nível | Opção | Exemplo |
|-------|-------|---------|
| **Já existe** | Usar rotina existente em `ADWs/` | `make sync`, `make morning` |
| **Novo skill** | Criar skill dedicado | `/create-routine` |
| **Linear** | Criar issue/workflow no Linear | Templates de issues recorrentes |
| **Manual otimizado** | Checklist / SOP documentado | `ops-runbook` ou `ops-process-doc` |

## Output

Produzir comparação antes/depois do processo com recomendações específicas de melhoria, impacto estimado e plano de implementação.

```markdown
## Otimização de Processo: [Nome do Processo]

### Estado Atual
[Descrever como o processo funciona hoje — etapas, tempos, responsáveis]

**Tempo total do ciclo:** [X horas/dias]
**Pontos de dor identificados:**
- [Ponto de dor 1]
- [Ponto de dor 2]

### Desperdícios Identificados
| Tipo | Descrição | Impacto Estimado |
|------|-----------|-----------------|
| [Tipo] | [O que está errado] | [Horas/semana perdidas] |

### Estado Futuro Proposto
[Descrever o processo otimizado]

**Tempo total do ciclo projetado:** [X horas/dias] ([Y]% de redução)

### Recomendações de Melhoria
| Mudança | Impacto | Esforço | Prioridade |
|---------|---------|---------|-----------|
| [Mudança] | [Alto/Médio/Baixo] | [Alto/Médio/Baixo] | [1/2/3] |

### Plano de Implementação
1. [Primeiro passo — quick win de baixo esforço]
2. [Segundo passo]
3. [Terceiro passo]

### Métricas de Sucesso
| Métrica | Baseline | Meta | Como Medir |
|---------|---------|------|-----------|
| [Métrica] | [Atual] | [Alvo] | [Método] |
```

## Dicas para Equipes Remotas e Pequenas (Evolution)

1. **Assíncrono por padrão** — Se pode ser Discord/Linear, não precisa ser reunião.
2. **Documente decisões** — Decisões tomadas no chat desaparecem. Colocar no Notion ou Linear.
3. **Quick wins primeiro** — Melhorias de 30% com esforço mínimo valem mais do que 100% que nunca saem do papel.
4. **Meça antes e depois** — Sem métrica, não tem como saber se melhorou.
