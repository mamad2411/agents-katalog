---
name: ops-risk-assessment
description: Identificar, avaliar e mitigar riscos operacionais. Use quando precisar de avaliação de riscos, registro de riscos, o que pode dar errado, ou quando avaliando riscos associados a projeto, vendor, processo ou decisão. Agente Lex.
argument-hint: "<projeto, vendor, processo ou decisão a avaliar>"
---

# /ops-risk-assessment

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Identifica, avalia e planeja mitigações para riscos operacionais de forma sistemática.

## Agente

Lex — jurídico, compliance, contratos, LGPD.

## Matriz de Avaliação de Risco

| | Impacto Baixo | Impacto Médio | Impacto Alto |
|---|--------------|---------------|-------------|
| **Alta Probabilidade** | Médio | Alto | Crítico |
| **Média Probabilidade** | Baixo | Médio | Alto |
| **Baixa Probabilidade** | Baixo | Baixo | Médio |

## Categorias de Risco

Para o contexto da Evolution API (startup, open source, remoto-first, operação brasileira):

| Categoria | Descrição | Exemplos Evolution |
|-----------|-----------|-------------------|
| **Operacional** | Falhas de processo, gaps de staffing, outages de sistema | Bot Runtime cair em produção, dev key sobrecarregado |
| **Financeiro** | Estouros de budget, aumento de custo de vendor, impacto em receita | Churn de subscriptions Stripe, custo de infra escalando |
| **Compliance / LGPD** | Violações regulatórias, achados de auditoria, brechas de política | Dados de usuários processados sem base legal LGPD |
| **Jurídico** | Contratos, licenças open source, propriedade intelectual | Uso indevido de licença open source, contrato sem cláusula de saída |
| **Estratégico** | Mudanças de mercado, ameaças competitivas, shifts tecnológicos | Fork agressivo do Evolution API por concorrente |
| **Reputacional** | Impacto em clientes, percepção pública, relacionamento com parceiros | Outage durante demo para prospect grande |
| **Segurança** | Vazamentos de dados, falhas de controle de acesso, vulnerabilidades de terceiros | API key exposta, dependência npm vulnerável |
| **Pessoas** | Time pequeno — concentração de conhecimento, saída de membro-chave | Único dev que conhece Bot Runtime saindo |

## Formato do Registro de Riscos

Para cada risco, documentar:
- **Descrição**: O que pode acontecer
- **Probabilidade**: Alta / Média / Baixa
- **Impacto**: Alto / Médio / Baixo
- **Nível de Risco**: Crítico / Alto / Médio / Baixo
- **Mitigação**: O que estamos fazendo para reduzir probabilidade ou impacto
- **Responsável**: Quem é responsável por gerenciar esse risco
- **Status**: Aberto / Mitigado / Aceito / Fechado

## Output

```markdown
## Registro de Riscos: [Projeto/Processo/Decisão]
**Data:** [Data] | **Escopo:** [O que foi avaliado]

### Resumo Executivo
[2-3 frases — principal exposição de risco e ação recomendada mais urgente]

### Registro de Riscos Priorizado

| # | Risco | Categoria | Probabilidade | Impacto | Nível | Mitigação | Responsável | Status |
|---|-------|-----------|--------------|---------|-------|-----------|------------|--------|
| 1 | [Risco mais crítico] | [Categoria] | Alta | Alto | Crítico | [Mitigação] | [Pessoa] | Aberto |
| 2 | [Segundo mais crítico] | ... | ... | ... | ... | ... | ... | ... |

### Riscos Críticos — Detalhamento

#### Risco 1: [Nome]
- **Descrição**: [O que pode acontecer]
- **Gatilho**: [O que precipitaria esse risco]
- **Impacto**: [Consequências específicas — financeiro, operacional, reputacional]
- **Mitigação**: [Ações concretas para reduzir probabilidade ou impacto]
- **Plano de Contingência**: [O que fazer SE acontecer]
- **Responsável**: [Nome]

### Heat Map de Riscos

```
           IMPACTO
           Baixo    Médio    Alto
Alta   |  Médio  |  Alto  | Crítico |
PROB.  |---------|--------|---------|
Média  |  Baixo  |  Médio |  Alto   |
       |---------|--------|---------|
Baixa  |  Baixo  |  Baixo |  Médio  |
```

Riscos no quadrante:
- **Crítico**: [Lista de riscos]
- **Alto**: [Lista de riscos]
- **Médio**: [Lista de riscos]
- **Baixo/Aceito**: [Lista de riscos]

### Ações Imediatas (Próximas 2 semanas)
1. [Ação urgente 1] — Responsável: [Nome]
2. [Ação urgente 2] — Responsável: [Nome]

### Revisão
**Próxima revisão do registro**: [Data]
**Cadência recomendada**: [Semanal/Mensal — baseado na criticidade]
```

## Dicas

1. **Foque nos controláveis e materiais** — Não tente mitigar todos os riscos. Priorize os que são controláveis e têm impacto real.
2. **Risco de concentração de conhecimento** — Em times pequenos como o da Evolution, sempre verificar: "O que acontece se [pessoa] sair?"
3. **LGPD como risco base** — Toda avaliação deve checar implicações de dados pessoais. Ver `ops-compliance-tracking` para detalhes.
4. **Revisar regularmente** — Riscos mudam com o tempo. Um risco "aceito" hoje pode se tornar crítico amanhã.
