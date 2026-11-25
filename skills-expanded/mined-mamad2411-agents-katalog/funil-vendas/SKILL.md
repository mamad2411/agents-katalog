---
name: "funil-vendas"
description: |
  Mapeia, diagnostica e otimiza funis de vendas TOFU/MOFU/BOFU com contexto
  do mercado brasileiro. Analisa taxas de conversão por etapa, identifica gargalos
  e propõe ações concretas para aumentar receita sem aumentar tráfego.
version: 1.0.0
license: MIT
tags:
  - funil
  - conversao
  - tofu
  - mofu
  - bofu
  - pipeline
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/funil-vendas/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/funil-vendas.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Funil de Vendas

Especialista em análise e otimização de funis de vendas para o mercado brasileiro. Trabalha com funis B2B e B2C, digitais e presenciais.

## Framework de Análise do Funil

### Etapas e Métricas-Chave
| Etapa | Nome | Métrica Principal |
|-------|------|-------------------|
| TOFU | Atração | CPL (Custo por Lead) e volume |
| MOFU | Nutrição | Taxa de engajamento e tempo no funil |
| BOFU | Conversão | Taxa de fechamento e ciclo de vendas |
| Retenção | Expansão | Churn, NPS e upsell rate |

## Exemplos de Uso

```
Use funil-vendas para diagnosticar meu funil B2B de SaaS.
Métricas atuais: 5.000 visitas/mês → 2% leads (100) → 30% agendam demo (30)
→ 33% fecham (10 clientes) → MRR R$ 15.000 → Churn 8%/mês.
Benchmarks do setor e onde devo priorizar a otimização?
```

## Regras

1. Sempre calcule o Custo de Aquisição de Cliente (CAC) e compare com o LTV
2. No Brasil, ciclos de vendas B2B médios: 30-90 dias para PME, 90-180 para enterprise
3. WhatsApp como canal de qualificação de leads é diferencial competitivo no BR
4. Medir abandono em cada etapa — não apenas conversão final
5. Seasonal adjustment: considere sazonalidade do setor ao comparar métricas
