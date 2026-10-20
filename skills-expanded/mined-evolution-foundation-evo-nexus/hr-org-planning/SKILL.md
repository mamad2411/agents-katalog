---
name: hr-org-planning
description: Planejamento de headcount, design organizacional e otimização de estrutura de times. Use quando precisar de planejamento de org, plano de headcount, estrutura de times, reorganização, próximas contratações prioritárias, ou ao pensar em tamanho de time, linhas de reporte e design organizacional.
argument-hint: "<time, cargo ou contexto de planejamento>"
---

# HR — Org Planning

Ajude a planejar a estrutura organizacional, headcount e design de times.

## Dimensões do Planejamento

- **Headcount**: Quantas pessoas precisamos, em quais cargos, até quando?
- **Estrutura**: Linhas de reporte, span of control, fronteiras de time
- **Sequenciamento**: Quais contratações são mais críticas? Qual é a ordem certa?
- **Budget**: Modelagem de custo de headcount e trade-offs

## Benchmarks de Org Saudável

| Métrica | Faixa Saudável | Sinal de Alerta |
|---------|---------------|-----------------|
| Span of control | 3-7 reports diretos | < 2 ou > 10 |
| Camadas de gestão | 2-3 para times ≤ 15 | Muitas = decisões lentas |
| IC : manager ratio | 4:1 a 8:1 | < 3:1 = top-heavy |
| Tamanho de time | 4-8 pessoas | < 3 = isolado, > 10 = difícil de alinhar |

> Nota: benchmarks ajustados para startup small team (~10 pessoas). Os valores clássicos de orgs maiores não se aplicam diretamente.

## Estrutura Atual — Evolution API (referência)

```
Davidson (CEO)
├── Danilo (Tech/PM)
│   ├── Guilherme / Gui (Dev Backend - Brius)
│   ├── Nickolas / Nick (Dev - Brius)
│   └── Wanderson (Brius)
├── Marcelo (Etus)
├── Matheus (Etus)
├── Samara (Financeiro Etus)
├── Thaís (Jurídico Brius/Etus)
├── Vitor (Jurídico Etus)
└── William (Freelancer - OrionDesign)
```

> Atualize conforme a estrutura real mudar.

## Output — Plano de Headcount

```markdown
## Plano de Headcount: [Time / Período]
**Data:** [Data] | **Horizonte:** [ex: H2 2025]

### Estado Atual
| Cargo | Regime | Nível | Time | Status |
|-------|--------|-------|------|--------|
| [Cargo] | CLT/PJ | [Nível] | [Time] | Ativo |

### Novas Vagas Planejadas
| Cargo | Prioridade | Regime | Nível | Justificativa | Início Desejado |
|-------|-----------|--------|-------|---------------|----------------|
| [Cargo] | Alta/Média/Baixa | CLT/PJ | [Nível] | [Por quê agora] | [Mês/Trimestre] |

### Sequência Recomendada de Contratações

**Round 1 (imediato — preenche gargalo crítico):**
1. [Cargo] — [Razão: bottleneck específico]

**Round 2 (3-6 meses — escala capacidade):**
2. [Cargo] — [Razão]
3. [Cargo] — [Razão]

**Round 3 (6-12 meses — estrutura de gestão):**
4. [Cargo] — [Razão]

### Modelagem de Custo
| Cargo | Regime | Custo Mensal Estimado | Custo Anual |
|-------|--------|-----------------------|-------------|
| [Cargo] | CLT | R$ [X] (base + encargos) | R$ [X] |
| [Cargo] | PJ | R$ [X] (NF) | R$ [X] |
| **Total Headcount Adicional** | | R$ [X]/mês | R$ [X]/ano |

### Riscos
- [Single point of failure identificado — ex: só 1 pessoa sabe X]
- [Sobrecargas identificadas — ex: Danilo fazendo PM + tech lead]
- [Dependências críticas em freelancers ou contratados externos]
```

## Output — Org Chart (texto)

```markdown
## Estrutura Organizacional: [Time] — [Data]

[Davidson] (CEO)
├── [Nome] ([Cargo]) — CLT/PJ
│   ├── [Nome] ([Cargo]) — CLT/PJ
│   └── [Nome] ([Cargo]) — CLT/PJ
└── [Nome] ([Cargo]) — CLT/PJ

**Vagas Abertas:**
└── 🔍 [Cargo Aberto] — [Estimativa de início]
```

## Frameworks de Decisão

### Quando Contratar vs. Terceirizar

| Critério | Contratar (CLT/PJ long-term) | Terceirizar / Freelancer |
|----------|------------------------------|--------------------------|
| Atividade | Core do produto | Periférica / pontual |
| Frequência | Recorrente e contínua | Esporádica ou por projeto |
| Conhecimento | Estratégico, não pode vazar | Operacional, documentável |
| Budget | Capacidade de arcar com CLT | Prefere flexibilidade de custo |

### Quando Criar um Novo Nível de Gestão

- Time cresceu para 7+ pessoas reportando a um único gestor
- Gestor está gastando >30% do tempo em alinhamento operacional
- Existem 2+ domínios técnicos distintos sem liderança dedicada
- Velocidade de decisão está caindo por falta de autonomia local

### Sequenciamento de Contratações — Critérios

Priorize contratar quando:
1. **Gargalo de receita**: A ausência do cargo está bloqueando crescimento de MRR
2. **Single point of failure**: Uma pessoa concentra conhecimento crítico único
3. **Overload recorrente**: Time-chave está constantemente em sobrecarga há 2+ sprints
4. **Oportunidade de mercado**: Tem uma janela de mercado e falta capacidade de executar

## Dicas para a Evolution

1. **Time pequeno = cada hire importa mais** — Erros de contratação custam proporcionalmente mais em times de 10 do que em times de 100.
2. **Brius vs. Etus** — Mantenha clareza sobre qual entidade legal cada colaborador está vinculado. Impacto contratual, fiscal e de gestão.
3. **Freelancer → PJ → CLT** — Caminho natural para testar fit antes de internalizar. Use para reduzir risco.
4. **Documentar antes de contratar** — Se o conhecimento está só na cabeça de uma pessoa, documente primeiro. Isso revela o que você realmente precisa contratar.
5. **Growthspace antes de headcount** — Para times pequenos, crescer capacidade de pessoas existentes costuma ser mais rápido e barato que contratar.
