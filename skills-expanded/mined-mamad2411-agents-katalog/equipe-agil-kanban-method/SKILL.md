---
name: equipe-agil-kanban-method
description: Base do Kanban Method (Anderson) + flow-based product development (Reinertsen) + métricas de fluxo (Vacanti) compartilhada por todos os papéis (técnicos e não-técnicos) da Equipe Backend Ágil Kanban+XP, inclusive o Product Owner. Invoque sempre que precisar fundamentar decisões sobre visualização de fluxo, limites de WIP, classes of service, cadências (Replenishment, SDR, Risk Review, Ops Review, Strategy Review, Delivery Planning, Daily), métricas de fluxo (lead time, cycle time, throughput, CFD, aging WIP), Little's Law, batch size, cost of delay, WSJF ou priorização baseada em fluxo. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Baseline Kanban Method + Flow + Métricas

Conhecimento inegociável de Kanban Method, flow-based product development e métricas de fluxo, compartilhado por **todos os 11 papéis** da Equipe Backend Ágil Kanban+XP (inclusive o Product Owner).

## 1. Conceitos centrais

### 1.1 Fundamentos do Kanban Method (Anderson)

- Sistema **pull** evolutivo: começa com o que existe hoje, evolui por consenso.
- Foco em **fluxo de valor**, não em iterações fixas (diferente de Scrum).
- Três agendas:
  - *Sustainability* — entregar com previsibilidade.
  - *Service orientation* — foco em quem recebe o trabalho.
  - *Survivability* — evolução contínua frente a mudança.

### 1.2 As 6 práticas centrais (Anderson — *Essential Kanban Condensed*)

1. **Visualize** — board com colunas refletindo o workflow real (não wishful thinking); cards expõem idade, tipo, classe de serviço.
2. **Limite o WIP** — limites explícitos por coluna; *pull system*; nada entra se a coluna estourou.
3. **Gerencie o fluxo** — métricas em vista (CFD, lead/cycle time, throughput, aging WIP); foco em itens, não em pessoas.
4. **Torne políticas explícitas** — DoR, DoD, classes of service, critério de pull, política de bloqueio.
5. **Implemente feedback loops** — as 7 cadências de Anderson (1.4).
6. **Melhore colaborativamente, evolua experimentalmente** — kaizen contínuo, *change as evolution*.

### 1.3 Classes of Service (Anderson)

- **Expedite** — interrompe WIP normal; emergência (incidente, regulatório imediato); **1 slot dedicado, fora do WIP global**.
- **Fixed Date** — entrega obrigatória até data X (regulatório, marketing, contrato); SLA com data dura.
- **Standard** — fluxo normal; otimiza throughput; FIFO ponderado por idade.
- **Intangible** — sem custo de atraso visível mas valor estratégico (dívida técnica, refactoring, modernização).

Política típica: WIP limit por classe ou slot reservado (ex.: 1 Expedite, 2 Fixed Date, 6 Standard, 1 Intangible).

### 1.4 As 7 cadências do Kanban Method (sete feedback loops — Anderson)

- **Daily Standup** — focado em itens: blockers, aging WIP, idade de cards em cada coluna.
- **Replenishment Meeting** (semanal) — PO + Tech Lead + Eng Coach decidem o que sai de *options* e entra na *ready queue*; *input cadence*.
- **Service Delivery Review** (quinzenal) — Eng Coach apresenta métricas de fluxo (CFD, scatter plot, throughput); ações de melhoria.
- **Delivery Planning Meeting** — sob demanda; quando deploy é ato distinto do merge.
- **Risk Review** (periódico) — bloqueios crônicos, dívida técnica, aging WIP, regressões.
- **Ops Review** (mensal) — cross-team; saúde de SLOs, error budget, incidentes.
- **Strategy Review** (trimestral) — alinhamento com objetivos de negócio.

### 1.5 Métricas de fluxo (Vacanti — *Actionable Agile Metrics*)

- **Lead Time** — do commitment (entrada na ready queue) ao *done*; visão do cliente.
- **Cycle Time** — de quando o item começou a ser trabalhado até *done*; visão do time.
- **Throughput** — itens entregues por unidade de tempo (default: semana).
- **WIP** — itens em andamento; média num intervalo.
- **Aging WIP** — idade em dias do item desde que entrou em cada coluna; alarme antes de virar atraso.
- **Work Item Age** — idade do item desde que começou.

**Visualizações fundamentais**:

- **CFD (Cumulative Flow Diagram)** — bandas empilhadas por coluna ao longo do tempo; bandas se afastando = WIP crescendo; estabilidade = fluxo saudável.
- **Cycle Time Scatter Plot** — cada ponto é um item; eixo X = data de done, eixo Y = cycle time; percentis (50/85/95) usados para previsão probabilística.
- **Throughput Run Chart** — itens entregues por semana ao longo do tempo.
- **Aging WIP Chart** — barras por item em WIP, ordenadas pela idade; alarme quando a barra cruza o percentil 85 histórico do cycle time.

### 1.6 Little's Law

**Fórmula** (regime estacionário, mesma unidade de tempo nos dois lados):

```
WIP médio = Throughput médio × Lead Time médio
```

**Implicação operacional**: para reduzir lead time, **reduza WIP** (mantendo throughput) ou aumente throughput (mantendo WIP). Reduzir WIP é quase sempre mais barato e mais rápido do que aumentar throughput.

**Pré-condições** (frequentemente esquecidas):
- Regime estacionário (entradas ≈ saídas no intervalo medido).
- Cada item que entra eventualmente sai.
- Mesma unidade de tempo em ambos os lados.

Em sistemas reais, vale como aproximação útil — não tratar como precisão de física.

### 1.7 Princípios de Flow (Reinertsen — *Principles of Product Development Flow*)

Os 175 princípios condensados nos eixos mais acionáveis:

- **Cost of Delay (CoD)** — quantificar em $/semana o custo de atrasar um item; transforma intuição em economia.
- **WSJF — Weighted Shortest Job First**: prioridade = `CoD ÷ Job Duration`. Sequenciamento que maximiza retorno econômico.
- **Reduzir batch size** — lotes pequenos reduzem variabilidade, aceleram feedback, expõem problemas cedo. Lote ótimo = onde custo de transação ≈ custo de holding.
- **Atacar variabilidade na fonte** — não tente "gerenciar variabilidade", reduza-a (padronização de fluxo, decomposição de itens grandes).
- **Filas custam** — quanto maior o WIP, maior a fila, maior o lead time (Kingman/Little).
- **Folga (slack) é eficiência sistêmica** — 100% de utilização explode o lead time (curva exponencial).
- **Decisões descentralizadas** — quanto mais perto do trabalho, mais rápido o feedback.
- **Fast feedback** > previsão perfeita.

### 1.8 Lean foundations (Modig & Åhlström — *This is Lean*)

Trade-off central entre dois tipos de eficiência:

- **Resource efficiency** = % de tempo que o recurso (pessoa, máquina) está ocupado.
- **Flow efficiency** = % de tempo em que **o item** está recebendo valor (`work time ÷ total lead time`).

**Paradoxo da eficiência**: maximizar resource efficiency frequentemente **reduz** flow efficiency (filas, multitasking, hand-offs).

**Kanban prioriza flow efficiency**; aceita slack de recursos para acelerar entrega.

### 1.9 Valores humanos (Burrows — *Kanban from the Inside*)

9 valores que sustentam Kanban e devem ser citados quando o "porquê" de uma prática é questionado:

*Transparency, Balance, Collaboration, Customer Focus, Flow, Leadership, Understanding, Agreement, Respect*.

### 1.10 Práticas avançadas (Leopold — *Practical Kanban*)

- **Upstream Kanban** — board para o trabalho de descoberta antes do compromisso; *options* viram *ready*.
- **Discovery vs Delivery Kanban** — dois sistemas de pull conectados.
- **Replenishment como gate de qualidade** — DMV obrigatória para entrar na ready queue.
- **Forecasting probabilístico via Monte Carlo** (Vacanti) sobre throughput histórico — substitui estimativa de pontos por contagem de itens.

## 2. Práticas e heurísticas operacionais

### 2.1 Visualização — o que mostrar no board

- Colunas refletindo o workflow real (ex.: *Options* → *Ready* → *Analysis* → *Dev* → *Test* → *Deploy ready* → *Deployed* → *Done*).
- Card mostra: ID, título curto, classe de serviço (cor), idade em dias na coluna atual, owner/pair, blockers.
- Sub-colunas *doing* / *done* dentro de etapas intermediárias para tornar pull explícito.
- Swimlanes por classe de serviço (Expedite no topo).

### 2.2 Definindo limites de WIP

- Comece com `1.5 × pessoas`; ajuste por dados.
- Limite por **coluna** (não global) para forçar pull.
- Quando estoura: **não comece nada novo**; ajude a desbloquear o que está em progresso (*stop starting, start finishing*).
- Slot Expedite **fora** do limite global (interrompe normal).

### 2.3 Anti-padrões comuns

- ❌ Board sem WIP limit → kanban virou *Scrumban* visual sem força sistêmica.
- ❌ Métricas de pessoas (linhas por dev, % utilização) — ferem Kanban (foco em fluxo, não em recursos).
- ❌ Stand-up tipo "o que fiz / o que farei" — Kanban é *walk the board* da direita para a esquerda.
- ❌ Replenishment sem DMV → entra trabalho sem critério, lead time explode.
- ❌ "Apenas Standard" — sem classes of service, expedite vira interrupção crônica não policiada.
- ❌ Ignorar aging WIP — descobrir atraso só depois de virar lead time longo é tardio demais.

### 2.4 Como interpretar um CFD saudável vs doente

- **Saudável**: bandas paralelas, espaçamento estável, WIP estável, throughput linear.
- **Doente — banda WIP crescendo**: entrada > saída; reduzir WIP ou aumentar capacidade de saída.
- **Doente — banda "doing" engordando**: gargalo na coluna; aplicar *theory of constraints* (atacar o gargalo).
- **Doente — degraus** (entrada em lotes) → não é fluxo, é cascade disfarçado.

### 2.5 Previsão probabilística (substitui estimativa de pontos)

- Coletar throughput histórico semanal (≥ 11 semanas para Monte Carlo confiável).
- Monte Carlo: simular N entregas amostrando throughput; resultado = distribuição de datas com confidence levels.
- Comunicar como faixa com confiança: "85% de chance de entregar até DD/MM"; **não data única**.
- Replanejar quando dados rejeitam a previsão (run chart com tendência clara).

### 2.6 Uso ético das métricas

- Métricas servem para **conversas** e melhoria do **sistema**, não para gerência por números nem ranking individual.
- Coletar por **fluxo / serviço**, nunca por pessoa.
- Tendência > valor pontual; comparar o time a si mesmo, não a outros times.
- Quando uma métrica piora, investigue **políticas e estrutura do sistema**, não esforço individual.

## 3. Templates e checklists

### 3.1 Checklist de board minimamente viável

- [ ] Colunas refletem workflow real (mapeado com a equipe).
- [ ] Sub-colunas *doing*/*done* em etapas intermediárias.
- [ ] WIP limit explícito em cada coluna.
- [ ] Classes of service com swimlane ou cor.
- [ ] Política de pull escrita ao lado do board.
- [ ] DoR e DoD escritas e visíveis.
- [ ] Aging WIP visível (idade do card em cada coluna).

### 3.2 Agenda padrão das 7 cadências

| Cadência | Frequência típica | Quem participa | Output |
|----------|-------------------|----------------|--------|
| Daily Standup | Diário, 15 min | Time | Blockers, ações de desbloqueio |
| Replenishment | Semanal | PO + Tech Lead + Eng Coach | Ready queue reabastecida |
| Service Delivery Review | Quinzenal | Time + Eng Coach | Ações sobre fluxo |
| Delivery Planning | Sob demanda | Time + PO + DevOps/SRE | Próximo deploy/release |
| Risk Review | Mensal | Time + AppSec + SRE | Mitigação de riscos |
| Ops Review | Mensal | Cross-team | Saúde operacional |
| Strategy Review | Trimestral | Liderança + PO | Alinhamento estratégico |

### 3.3 Definition of Ready (DoR) — entrada na ready queue

- [ ] Story no formato Gherkin com critérios de aceite.
- [ ] Glossário e regras envolvidas referenciados ou criados.
- [ ] DMV (Documentação Mínima Viável) acordada para a unidade de trabalho.
- [ ] Classe de serviço atribuída.
- [ ] Riscos de segurança/operação levantados (AppSec/SRE consultados se necessário).
- [ ] Dependências externas mapeadas.

### 3.4 Política sugerida de Expedite

- 1 slot Expedite, **fora** do WIP global.
- Entrada exige aprovação de PO + Eng Coach.
- Suspende item Standard em andamento (NUNCA Expedite anterior).
- Postmortem obrigatório no SDR seguinte (frequência de Expedite é sinal de problema upstream).

### 3.5 Fórmula rápida de Little's Law aplicada

```
Lead Time esperado ≈ WIP atual ÷ Throughput médio

Exemplo:
  WIP = 12 itens
  Throughput = 4 itens/semana
  Lead Time esperado ≈ 3 semanas

Para entregar em 2 semanas: WIP máximo ≈ 8 itens.
```

### 3.6 Cálculo simplificado de WSJF para Replenishment

```
WSJF = Cost of Delay (CoD)  ÷  Job Duration (estimativa de tempo de fluxo)

CoD componentes (Reinertsen):
  - User/business value
  - Time criticality
  - Risk reduction / opportunity enablement
```

Use WSJF para sequenciar a *ready queue* dentro de cada classe of service.

## 4. Como esta skill é usada pelos agentes

**Todos os 11 papéis** (PO + 10 técnicos) carregam esta skill antes das skills específicas — Kanban é vocabulário comum da equipe.

- **Engineering Coach** é o owner explícito das práticas Kanban (RACI A/R em cadências, métricas de fluxo, WIP limits).
- **Product Owner** opera o Replenishment Meeting e as classes of service; carrega esta skill junto com `po-knowledge` para fundamentar priorização (WSJF/CoD).
- **Tech Lead** apoia o Eng Coach nas métricas e participa do Replenishment.
- **SRE** e **DevOps** alimentam Ops Review com SLO/error budget e métricas operacionais.
- **AppSec** alimenta Risk Review com ameaças, dívida de segurança e itens regulatórios.
- **Quality Engineer**, **Arquitetos**, **Data Engineer**, **API Designer** consomem aging WIP para decidir onde aplicar slack/refactor/pareamento.
- Todos respeitam *aging WIP* e *stop starting, start finishing*.

## References

Bibliografia da seção 3.0b do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Kanban: Successful Evolutionary Change for Your Technology Business* — David J. Anderson
- *Essential Kanban Condensed* — Anderson & Carmichael
- *Kanban from the Inside* — Burrows
- *Practical Kanban* — Klaus Leopold
- *The Principles of Product Development Flow: Second Generation Lean Product Development* — Reinertsen
- *Actionable Agile Metrics for Predictability* — Vacanti
- *When Will It Be Done?* — Vacanti *(complementar — previsão probabilística)*
- *This is Lean* — Modig & Åhlström
