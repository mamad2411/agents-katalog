---
name: ops-status-report
description: Gerar relatório de status com KPIs, riscos e action items. Use quando escrever update semanal ou mensal para liderança, resumir saúde do projeto com status verde/amarelo/vermelho, surfacing riscos e decisões que precisam de atenção dos stakeholders, ou transformar atividade do Linear em narrativa legível. Agente Atlas.
argument-hint: "[semanal | mensal | trimestral] [projeto ou equipe]"
---

# /ops-status-report

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Gera relatório de status polido para liderança ou stakeholders. Ver skill **ops-risk-assessment** para frameworks de matriz de risco e definições de severidade.

## Agente

Atlas — projetos, status, milestones, blockers, Linear, GitHub.

## Output

```markdown
## Status Report: [Projeto/Equipe] — [Período]
**Autor:** [Nome] | **Data:** [Data]

### Executive Summary
[3-4 frases de visão geral — o que está no prazo, o que precisa de atenção, vitórias principais]

### Status Geral: 🟢 No Prazo / 🟡 Em Risco / 🔴 Fora do Prazo

### Métricas-Chave
| Métrica | Meta | Real | Tendência | Status |
|---------|------|------|-----------|--------|
| [KPI] | [Meta] | [Real] | [subindo/caindo/estável] | 🟢/🟡/🔴 |

### Conquistas do Período
- [Vitória 1]
- [Vitória 2]

### Em Progresso
| Item | Responsável | Status | ETA | Notas |
|------|------------|--------|-----|-------|
| [Item] | [Pessoa] | [Status] | [Data] | [Contexto] |

### Riscos e Issues
| Risco/Issue | Impacto | Mitigação | Responsável |
|-------------|---------|-----------|------------|
| [Risco] | [Impacto] | [O que estamos fazendo] | [Quem] |

### Decisões Necessárias
| Decisão | Contexto | Deadline | Ação Recomendada |
|---------|----------|----------|-----------------|
| [Decisão] | [Por que importa] | [Quando] | [O que recomendo] |

### Prioridades do Próximo Período
1. [Prioridade 1]
2. [Prioridade 2]
3. [Prioridade 3]
```

## Se Conectores Disponíveis

Se **Linear MCP** estiver conectado (via `int-linear-review`):
- Puxar status do projeto, itens concluídos e milestones futuros automaticamente
- Identificar itens em risco e tarefas atrasadas

Se **Discord** estiver disponível:
- Escanear discussões recentes para decisões e blockers a incluir
- Oferecer para postar o relatório finalizado em canal relevante

Se **Google Calendar MCP** estiver conectado:
- Referenciar reuniões e decisões-chave do período reportado

## Dicas

1. **Comece pela headline** — Líderes ocupados leem as 3 primeiras linhas. Faça-as contar.
2. **Seja honesto sobre riscos** — Surfacing issues cedo constrói confiança. Surpresas destroem.
3. **Facilite as decisões** — Para cada decisão necessária, forneça contexto e uma recomendação.
