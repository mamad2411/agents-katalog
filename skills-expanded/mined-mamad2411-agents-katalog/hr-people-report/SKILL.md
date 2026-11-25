---
name: hr-people-report
description: Gera relatórios de headcount, attrition, diversidade ou saúde organizacional. Use ao preparar snapshot de headcount para liderança, analisar tendências de turnover por time, preparar métricas de representatividade, ou avaliar span of control e flight risk no time.
argument-hint: "<tipo de relatório: headcount, attrition, diversidade, saúde-org>"
---

# HR — People Report

Gere relatórios de people analytics a partir dos dados do time. Analise dados da força de trabalho para identificar tendências, riscos e oportunidades.

## Tipos de Relatório

- **Headcount**: Snapshot atual do time — por função, localidade, nível, tempo de casa
- **Attrition**: Análise de turnover — voluntário/involuntário, por área, tendências
- **Diversidade**: Métricas de representatividade — por nível, função, pipeline
- **Saúde Org**: Span of control, camadas de gestão, tamanhos de time, flight risk

## Métricas-Chave

### Retenção
- Taxa geral de attrition (voluntária + involuntária)
- Taxa de attrition lamentável (perda de pessoas-chave)
- Tempo médio de casa
- Indicadores de flight risk

### Diversidade
- Representatividade por nível, time e função
- Diversidade no pipeline de contratação
- Taxas de promoção por grupo
- Análise de equidade de remuneração

### Engajamento
- Resultados de pesquisas de clima e tendências
- eNPS (Employee Net Promoter Score)
- Taxas de participação
- Temas recorrentes em feedback aberto
- Nível de atividade no Discord / WhatsApp do time (proxy qualitativo)

### Produtividade
- Receita por colaborador (MRR / headcount)
- Eficiência do span of control
- Tempo para produtividade de novos colaboradores

## Abordagem

1. Entender que pergunta a pessoa está tentando responder
2. Identificar os dados corretos (upload, colar ou buscar no Notion MCP)
3. Analisar com métodos estatísticos apropriados para o tamanho da amostra
4. Apresentar achados com contexto e ressalvas
5. Recomendar ações específicas baseadas nos dados

## O Que Preciso Saber

Cole um CSV ou descreva seus dados. Campos úteis:
- Nome/ID do colaborador, departamento, time
- Cargo, nível, localidade
- Data de entrada, data de saída (se aplicável)
- Gestor, remuneração (se relevante)
- Regime (CLT/PJ)

## Output

```markdown
## People Report: [Tipo] — [Data]
**Referência:** [Período] | **Time:** [Escopo]

### Executive Summary
[2-3 principais conclusões]

### Métricas-Chave
| Métrica | Valor | Tendência |
|---------|-------|-----------|
| Headcount total | [X] | [↑/↓/—] |
| CLT | [X] ([X]%) | |
| PJ / Freelancer | [X] ([X]%) | |
| Attrition 12 meses | [X]% | [↑/↓/—] |
| Attrition lamentável | [X]% | |
| Tempo médio de casa | [X] meses | |
| Time-to-productivity novos hires | [X] semanas | |

---

### HEADCOUNT

#### Por Função
| Função | Qtde | % do Time |
|--------|------|-----------|
| Engenharia | [X] | [X]% |
| Produto / PM | [X] | [X]% |
| Financeiro | [X] | [X]% |
| Jurídico | [X] | [X]% |
| Design | [X] | [X]% |

#### Por Regime
| Regime | Qtde | % |
|--------|------|---|
| CLT | [X] | [X]% |
| PJ (long-term) | [X] | [X]% |
| Freelancer / Pontual | [X] | [X]% |

#### Por Tempo de Casa
| Faixa | Qtde |
|-------|------|
| < 6 meses | [X] |
| 6-12 meses | [X] |
| 1-2 anos | [X] |
| 2+ anos | [X] |

---

### ATTRITION

#### Saídas no Período
| Nome | Cargo | Regime | Tipo | Motivo | Data |
|------|-------|--------|------|--------|------|
| [Nome] | [Cargo] | CLT/PJ | Voluntária/Involuntária | [Motivo] | [Data] |

#### Análise
- **Lamentável vs. não-lamentável:** [X]% das saídas foram lamentáveis
- **Padrões identificados:** [ex: 2 saídas de devs sênior por oportunidade de salário melhor]
- **Recomendação:** [ação específica]

---

### SAÚDE ORG

#### Span of Control
| Gestor | Reports Diretos | Avaliação |
|--------|----------------|-----------|
| Davidson | [X] | [OK / Alto — avaliar] |
| Danilo | [X] | [OK / Alto — avaliar] |

#### Single Points of Failure
| Conhecimento Crítico | Única Pessoa | Risco |
|---------------------|-------------|-------|
| [ex: arquitetura Evolution Go] | [Nome] | Alto |

#### Flight Risk (baseado em indicadores qualitativos)
| Colaborador | Indicadores | Risco | Ação Sugerida |
|-------------|------------|-------|---------------|
| [Nome] | [ex: sem promoção há X meses, baixo engajamento] | Alto/Médio | [ex: 1:1 de desenvolvimento] |

---

### Recomendações
- [Recomendação baseada em dados]
- [Item de ação com responsável e prazo]

### Metodologia
[Como os números foram calculados, ressalvas sobre tamanho de amostra, fontes de dados]
```

## Integrações Disponíveis

**Notion MCP** (substitui HRIS):
- Buscar dados de colaboradores cadastrados em databases Notion
- Gerar relatórios sem necessidade de upload de CSV

**Discord** (proxy qualitativo de engajamento):
- Atividade nos canais do time como sinal complementar de engajamento
- Não substitui pesquisa de clima, mas pode indicar tendências

## Notas sobre Contexto Evolution

- **Time pequeno (~10)**: Métricas percentuais têm alta variância com amostras pequenas. Prefira análise qualitativa + quantitativa combinadas.
- **Mix CLT/PJ**: Distinção importante — PJs têm menos proteções de retenção, monitorar flight risk com mais atenção.
- **Comunidade open source como fonte de talento**: Contribuidores ativos no GitHub são pipeline natural. Rastrear engajamento da comunidade pode ser um leading indicator de futuras contratações.
- **Diversidade**: Explicitamente rastrear — times de tech BR têm viés histórico de homogeneidade. Começar a medir é o primeiro passo.
