---
name: equipe-agil-sre-knowledge
description: Conhecimento específico do SRE da Equipe Backend Ágil Kanban+XP. Cobre SLI/SLO/SLA com error budgets (Beyer, Murphy, Petoff, Ward), golden signals (Beyer), observabilidade vs monitoramento (Majors — high cardinality + structured events), OpenTelemetry (traces, metrics, logs) com Quarkus MicroProfile, USE/RED method (Gregg/Wilkie), chaos engineering (Rosenthal & Jones), capacity planning, incident management (incident commander), blameless postmortem (Lund), toil reduction, runbook como código, on-call humano sustentável. Owner técnico do comportamento em produção e da resposta a incidente da equipe. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# SRE — Conhecimento específico

Skill carregada pelo agente `equipe-agil-sre` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento necessário para operar serviços Java 21 + Quarkus 3 com confiabilidade — definir SLOs, instrumentar observabilidade, responder a incidentes, aprender de falhas, evitar toil.

## 1. Conceitos centrais

### 1.1 Mandato do SRE na equipe

- **Owner técnico do comportamento em produção** dos serviços da equipe (A/R): SLOs, error budgets, observabilidade, incident response, postmortem.
- **Não confunde com DevOps**: DevOps cuida do **fluxo de mudança** (build/integração/deploy até preview). SRE cuida do **comportamento em produção** (SLO, error budget, incidente, capacity, toil).
- **Não confunde com AppSec**: AppSec define controles preventivos; SRE responde quando algo quebra (com AppSec parceiro em incidente de segurança).
- RACI: A/R em SLO/error budget, observabilidade, response a incidente, postmortem; C em arquitetura distribuída, resiliência (Nygard) e capacity.

### 1.2 Stack default

- **Métricas**: Prometheus + Grafana (via MicroProfile Metrics ou Micrometer + Quarkus).
- **Traces**: OpenTelemetry SDK + collector → Jaeger/Tempo (via `quarkus-opentelemetry`).
- **Logs**: estruturados (JSON) com `quarkus-logging-json`; coletados por Loki/Elastic; correlacionados via `traceId`/`spanId`.
- **Alerting**: Alertmanager / PagerDuty / Opsgenie — alerta baseado em **sintoma**, não em causa.
- **SLO tracking**: ferramentas como Nobl9, Sloth, ou dashboards Grafana customizados (burn rate por janela).
- **Chaos engineering**: Litmus, Chaos Mesh, ou scripts pontuais (quando ASR justifica).

### 1.3 SLI, SLO, SLA, Error Budget (Google SRE Book — Beyer, Murphy, Petoff, Ward)

| Termo | Definição | Exemplo |
|-------|-----------|---------|
| **SLI** (Service Level Indicator) | Métrica concreta da qualidade do serviço | `% de requests com status < 500 e latência < 300ms` |
| **SLO** (Service Level Objective) | Meta interna sobre o SLI | `99,9% por janela rolling de 30 dias` |
| **SLA** (Service Level Agreement) | Promessa contratual ao cliente (com penalidade) | `99,5% — se descumprir, crédito de X%` |
| **Error Budget** | `1 - SLO` — quanto de falha é permitido | `0,1% = ~43 min em 30 dias` |

**Princípios**:
- **SLO < SLA**: sempre folga; SLA quebra → cliente reclama; SLO quebra → time aprende cedo.
- **Error budget governa risco**: budget cheio → autoriza experimentar (deploy mais agressivo). Budget zerado → freeze de mudança não-crítica até regenerar.
- **Cada serviço tem ≤ 5 SLOs** — mais que isso é ruído; foque em SLIs que importam para usuário (request success rate, latência, freshness de dado).

### 1.4 Categorias de SLI úteis (escolher 1-3 por serviço)

| Categoria | Quando aplicar | Fórmula típica |
|-----------|----------------|----------------|
| **Availability** | API síncrona | `successes ÷ total` |
| **Latency** | API com SLA de tempo | `% de requests abaixo de threshold` |
| **Throughput** | Worker / pipeline | `eventos processados por minuto` |
| **Freshness** | Dado replicado / CDC | `idade do dado mais antigo não-processado` |
| **Correctness** | Cálculo crítico | `% de saídas verificadas como corretas` |
| **Durability** | Storage | `% de objetos não perdidos por janela` |

### 1.5 Golden Signals (Beyer — capítulo 6 SRE Book)

Quatro métricas que toda API deve ter:
1. **Latency** — distribuição (p50/p95/p99), separar sucessos de erros.
2. **Traffic** — req/s, eventos/s, conexões.
3. **Errors** — taxa de erros (5xx, exceptions, business errors).
4. **Saturation** — quão cheia está a capacidade (CPU, memória, fila, conexões DB).

Complementadas por **USE** (recursos: Utilization, Saturation, Errors — Gregg) e **RED** (requests: Rate, Errors, Duration — Wilkie).

### 1.6 Observabilidade ≠ Monitoramento (Majors et al. — Observability Engineering)

- **Monitoramento**: alarmes em métricas pré-definidas para problemas **conhecidos**.
- **Observabilidade**: capacidade de fazer **perguntas novas** sobre estados internos sem deploy. Requer:
  - **High cardinality**: poder filtrar por qualquer atributo (user_id, request_id, tenant_id, build_sha, region).
  - **High dimensionality**: muitos atributos por evento.
  - **Structured events** (não logs texto puro).
  - **Exploration tooling**: query interativa, não dashboard estático.
- **3 pilares** clássicos: métricas, logs, traces. Mas observabilidade moderna foca em **structured events** com contexto rico (traces + métricas derivadas).

### 1.7 OpenTelemetry com Quarkus

```xml
<dependency>
  <groupId>io.quarkus</groupId>
  <artifactId>quarkus-opentelemetry</artifactId>
</dependency>
<dependency>
  <groupId>io.quarkus</groupId>
  <artifactId>quarkus-micrometer-registry-prometheus</artifactId>
</dependency>
<dependency>
  <groupId>io.quarkus</groupId>
  <artifactId>quarkus-logging-json</artifactId>
</dependency>
```

```properties
quarkus.application.name=aco-pedidos
quarkus.otel.exporter.otlp.endpoint=http://otel-collector:4317
quarkus.otel.resource.attributes=service.name=aco-pedidos,service.version=${quarkus.application.version}
quarkus.log.console.json=true
```

**Instrumentação automática** (REST, JDBC, Kafka) sem código.

**Custom span**:
```java
@Inject Tracer tracer;

Span span = tracer.spanBuilder("calcula-credito").startSpan();
try (Scope s = span.makeCurrent()) {
  span.setAttribute("cliente.id", clienteId.toString());
  return calculadora.calcular(cliente);
} catch (Exception e) {
  span.recordException(e);
  span.setStatus(StatusCode.ERROR);
  throw e;
} finally {
  span.end();
}
```

**Correlação log ↔ trace**: incluir `traceId`/`spanId` no MDC automaticamente (extensão faz).

### 1.8 Alerting — sintoma, não causa

- ❌ Alerta "CPU > 80%" — causa, não sintoma; gera fadiga.
- ✅ Alerta "p99 > SLO de latência por 5 min" — sintoma para usuário.
- ✅ Alerta "error budget burn rate > 14× normal por 1 hora" — multi-window multi-burn-rate (SRE Workbook).
- **Multi-window/multi-burn-rate** (Google SRE Workbook):
  - *Fast burn* — janela curta (1h), burn alta (14× normal) → page imediato.
  - *Slow burn* — janela longa (6h), burn moderada (6×) → ticket / aviso.
- Cada alerta com: link para runbook, dashboard, owner, severidade.

### 1.9 Incident Management (Beyer cap. 14; PagerDuty incident response)

- **Incident Commander (IC)** — coordena, não executa; comunica.
- **Operations Lead** — quem faz hands-on no problema.
- **Comms Lead** — atualiza stakeholders.
- **Scribe** — registra timeline (vira insumo do postmortem).
- **Severities** padrão:
  - SEV-1 — outage total; resposta imediata 24/7.
  - SEV-2 — degradação ampla; resposta em horas.
  - SEV-3 — degradação parcial; resposta em business hours.
- **Resposta em fases**: Detect → Triage → Mitigate → Resolve → Learn.
- **Mitigar > entender**: restaurar serviço primeiro; entender no postmortem.
- **Rollback é mitigação válida** — não esperar root cause antes de reverter.

### 1.10 Blameless postmortem (Lund — SRE Book cap. 15)

- **Hipótese fundamental**: pessoas competentes agiram com a melhor informação disponível. Falha é **sistêmica**.
- **Foco em sistema**, não em pessoas (`alguém deu deploy errado` → `o pipeline permitiu deploy sem confirmação humana`).
- **Estrutura**:
  - Summary (1-2 parágrafos).
  - Impact (usuários afetados, duração, custo estimado).
  - Timeline (eventos com timestamps).
  - Root cause analysis (5-whys ou similar, mas multi-causa preferível).
  - Triggers (o que disparou a falha).
  - Resolução (o que mitigou).
  - Action items (concretos, com owner + data, rastreáveis no Kanban).
  - Lessons learned (positivas e negativas).
- **Distribuição ampla** — postmortem público (dentro da empresa); aprende todo mundo.
- **Action items são primeira-classe**: viram itens Kanban com classe Fixed Date.

### 1.11 Toil reduction (Limoncelli — SRE Book cap. 5)

- **Toil** = trabalho operacional manual, repetitivo, automatizável, sem valor duradouro, escala com tamanho do serviço.
- **Meta**: < 50% do tempo de SRE em toil; resto em projeto/engenharia.
- Para cada toil recorrente, decidir: **automatizar, eliminar (mudar o sistema) ou aceitar (mas medir)**.
- Sinal de alerta: toil crescendo → time vira sysadmin de plantão; engenharia some.

### 1.12 Chaos Engineering (Rosenthal & Jones — Chaos Engineering)

- **Premissa**: sistemas distribuídos falham; descobrir como antes que o cliente descubra.
- **5 princípios**:
  1. Hipótese sobre comportamento em regime estacionário (steady state).
  2. Variável real (failure injection).
  3. Experimento em produção (com escopo limitado).
  4. Automatizar para rodar contínuo.
  5. Minimize blast radius.
- **Game days** — exercício planejado (ex.: matar nó do banco; cortar dependência).
- **Pré-requisitos**: observabilidade boa, error budget, autorização do PO/SRE chefe.
- **Maturidade**: começar em staging → preview → produção controlada.

### 1.13 Capacity planning

- **Demand forecast** — projeção de tráfego (sazonalidade, crescimento, eventos esperados).
- **Headroom**: provisionar para `pico previsto × fator de segurança` (típico 1.5-2×).
- **Cost vs reliability**: planejar gasto contra error budget aceito.
- **Load test** periódico para validar capacity assumida.
- **Autoscaling** (HPA + cluster autoscaler) não substitui capacity planning — apenas absorve flutuação dentro de envelope.

### 1.14 Resiliência (Nygard — Release It!) — perspectiva runtime

Vide `arquiteto-sis-knowledge` §1.6 para padrões; aqui o SRE pensa em:
- **Timeout** em **toda** chamada externa (sem default infinito).
- **Circuit breaker** com half-open + métrica de estado.
- **Bulkhead** isolando pools (DB, HTTP cliente, threads).
- **Retry com backoff exponencial + jitter** apenas para erro transitório.
- **Back-pressure** quando upstream mais rápido que downstream (Kafka consumer group).
- **Graceful degradation** — fallback explícito, não cascata de erro.

### 1.15 On-call humano sustentável

- Rotação ≥ 6 pessoas idealmente.
- Pager **load** monitorado (pages/semana); > 2 noites com page → time queima.
- Compensação clara (folga, financeiro, conforme política).
- Postmortem de qualquer page noturna (mesmo near-miss).
- "Você constrói, você opera" (Werner Vogels) — devs do time entram na rotação com SRE coaching.

## 2. Práticas e heurísticas operacionais

### 2.1 Definindo um SLO útil (workshop curto)

1. **Identifique usuário** (humano ou serviço consumidor).
2. **O que importa para ele?** (latência? sucesso? freshness?)
3. **Defina SLI** mensurável (não invente — alinhe com instrumentação existente).
4. **Meta inicial**: 1 nine abaixo do que parece "óbvio". Aperta se a folga sobra; afrouxa se sangra.
5. **Janela**: 28 ou 30 dias rolling (não calendário).
6. **Document**: serviço, SLI, SLO, janela, owner, política do error budget.

### 2.2 Política de error budget — exemplos de cláusula

- Budget > 50% restante → deploys autorizados normalmente.
- Budget < 25% → freeze de mudança não-crítica até 30 dias regenerar.
- Budget esgotado → freeze obrigatório + postmortem do que consumiu.
- Exceção de freeze: correção de segurança crítica + correção que recupera budget.

### 2.3 Estrutura mínima de dashboard por serviço

- **Header**: SLO target + budget remaining + burn rate atual.
- **Golden signals**: latência (p50/p95/p99 separados por sucesso/erro), traffic, errors, saturation.
- **Dependências**: latência e erro contra cada dependência externa.
- **Recursos**: CPU/mem/conexões DB/heap/GC.
- **Deploy markers**: linha vertical em cada deploy (correlaciona com mudança).

### 2.4 Anti-padrões frequentes

- ❌ **Alerta em causa raiz** (CPU > 80%) — fadiga.
- ❌ **SLO 100%** — sem error budget, sem espaço para experimentar.
- ❌ **Dashboard sem ação** — gráfico bonito que ninguém olha; preferir alerta.
- ❌ **Log texto livre sem estrutura** — não dá para query agregada.
- ❌ **Trace em 1% por amostragem fixa** — perde investigação; usar tail-based sampling para preservar erros.
- ❌ **Métrica de baixa cardinalidade só** — não dá para investigar usuário/tenant específico.
- ❌ **Postmortem que culpa pessoa** — silencia futuras reportagens; cultura morre.
- ❌ **Action items vagos sem owner/data** — postmortem vira teatro.
- ❌ **Retry sem backoff/jitter** — amplifica falha em cascade.
- ❌ **Catch-all sem logging do contexto** — buraco preto.
- ❌ **Mitigation espera entender root cause** — usuário paga.

### 2.5 Como SRE atua no Replenishment

- Item que introduz dependência nova → consultar SRE (timeout, fallback, SLO impacto).
- Item que muda padrão de tráfego → SRE C (capacity, autoscale).
- Item com SLO/latência declarada → SRE owner do SLI.
- Migração de arquitetura → SRE participa do dry-run + plano de rollback.

### 2.6 Como SRE atua no Risk Review e Ops Review

**Risk Review (mensal)**:
- Top-N alertas mais frequentes (atacar fadiga).
- Top-N causas de toil (priorizar automação).
- Error budget burn por serviço.
- Postmortem action items atrasados.
- Capacity heads-up (próximos 90 dias).

**Ops Review (mensal, cross-team)**:
- SLO compliance.
- Incident summary (SEV-1/SEV-2 do mês).
- Dependências externas problemáticas.
- Cross-team blockers operacionais.

### 2.7 Colaboração com outros papéis

- **DevOps** — handoff de readiness; tooling de observabilidade.
- **Tech Lead** — instrumentação OTel; defesa contra Nygard no código.
- **Arquiteto Sis** — design resiliente; padrões de comunicação.
- **AppSec** — incidente de segurança; resposta conjunta.
- **PO** — comunicação durante incidente; priorização de tech debt.
- **Eng Coach** — métricas DORA do escopo do time; aprendizado pós-incidente.
- **Data Engineer** — observabilidade de banco (lag, slot, queries lentas).

## 3. Templates e checklists

### 3.1 Template de SLO doc

```markdown
# SLO — <Serviço> — <SLI name>

- **Owner**: <time/SRE responsável>
- **Status**: Active | Pilot | Deprecated
- **Janela**: 30 dias rolling
- **SLI**: <fórmula precisa — ex.: % de POST /pedidos com status < 500 e duração < 300ms>
- **SLO**: 99.9%
- **Error Budget**: 0.1% (~43 min/30d)
- **Política**: <freeze rules, exception process>
- **Source**: <métrica Prometheus exata, link do dashboard>
- **Alert rules**:
  - Fast burn — 14× por 1h → page
  - Slow burn — 6× por 6h → ticket
- **Histórico**: <compliance dos últimos 3 períodos>
```

### 3.2 Template de runbook

```markdown
# Runbook — <Alerta>

## O que significa
<Sintoma observável + impacto provável ao usuário>

## Primeiras ações (≤ 5 min)
1. Verificar painel: <link>
2. Verificar deploys recentes: <link>
3. Verificar dependências: <link>

## Mitigação
- Se causado por deploy recente → `kubectl rollout undo deployment/<name>` ou bump tag GitOps anterior.
- Se causado por dependência X → desativar feature flag Y.
- Se carga acima do esperado → escalar HPA target.

## Diagnóstico mais profundo
- Trace amostrado: <link Jaeger query>
- Log de erro: <link Loki query>
- Métrica de saturação: <link Grafana>

## Escalonamento
- Após 15 min sem mitigação → IC convoca SEV-2.
- Após 30 min sem mitigação → SEV-1.

## Postmortem obrigatório se
- Incidente > 15 min
- Cliente impactado externamente
- Page noturna
```

### 3.3 Template de postmortem (blameless)

```markdown
# Postmortem — <Título do incidente> — <YYYY-MM-DD>

## Summary
<2 parágrafos: o que aconteceu, impacto, como mitigou>

## Severity
SEV-?

## Impact
- Usuários afetados: <quantidade ou %>
- Duração: <de quando começou a quando mitigou>
- Custo estimado: <financeiro / reputacional>
- Error budget consumido: <% do mês>

## Timeline (UTC)
- HH:MM — primeiro alerta disparado
- HH:MM — IC engajado
- HH:MM — diagnóstico identificou X
- HH:MM — mitigação aplicada
- HH:MM — serviço restaurado

## Root cause(s)
<Multi-causa quando aplicável; não apenas o último gatilho>

## Triggers
<O que disparou a janela de falha agora — deploy, pico, dependência>

## Resolução
<O que efetivamente restaurou o serviço>

## Lessons learned
**O que foi bem**:
- ...

**O que pode melhorar**:
- ...

## Action items
| ID  | Item                                       | Owner | Tipo (mitigate/detect/prevent) | Data alvo |
|-----|--------------------------------------------|-------|--------------------------------|-----------|
| AI1 | Adicionar timeout no cliente HTTP X        | dev1  | Prevent                        | 2026-06-15|
| AI2 | Alerta de burn rate fast no SLO de latência| sre1  | Detect                         | 2026-06-01|
```

### 3.4 Checklist de readiness operacional de um serviço

- [ ] SLO(s) definido(s) e tracked.
- [ ] Dashboard com golden signals + deploy markers.
- [ ] Alertas baseados em sintoma (com runbook).
- [ ] OpenTelemetry instrumentado (traces + metrics + logs estruturados).
- [ ] Logs com `traceId`/`spanId`.
- [ ] Healthcheck `/q/health/*` configurado.
- [ ] Probes K8s apontando para health.
- [ ] Timeout em todas as chamadas externas.
- [ ] Circuit breaker em chamadas críticas.
- [ ] Retry com backoff + jitter quando aplicável.
- [ ] Shutdown gracioso (drena requests).
- [ ] Runbook para alertas top-3.
- [ ] On-call rotação ativa.
- [ ] Capacity headroom validado.

### 3.5 Quando escalar

- **Error budget esgotado e time não freezar mudança** → Eng Coach + PO.
- **Toil > 50% do tempo de SRE** → Eng Coach (replanejamento de slot).
- **Postmortem action items repetidamente atrasados** → Eng Coach + PO.
- **Plataforma corporativa instável afetando SLO** → time de plataforma / SRE corporativo.
- **Incidente SEV-1 ativo** → IC convoca quem precisa, sem cerimônia.

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-sre`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O SRE usa esta skill para:
- Definir SLO/SLI e operar error budget.
- Instrumentar e operar observabilidade (OTel/Prom/Loki/Tempo).
- Conduzir incident response (IC ou Ops Lead).
- Liderar postmortem blameless.
- Reduzir toil ativamente.
- Apoiar capacity planning.
- Defender resiliência no código (parceria com Tech Lead/Arquiteto Sis).

SRE **não decide** estilo arquitetural nem implementação — consulta e influencia. **Em incidente**, autoridade máxima sobre mitigação.

## References

Bibliografia da seção 3.10 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Site Reliability Engineering* — Beyer, Jones, Petoff & Murphy (eds.)
- *The Site Reliability Workbook* — Beyer, Murphy, Rensin, Kawahara & Thorne (eds.)
- *Building Secure & Reliable Systems* — Adkins et al.
- *Observability Engineering* — Majors, Fong-Jones & Miranda
- *Distributed Systems Observability* — Sridharan
- *Implementing Service Level Objectives* — Hidalgo
- *Release It!* (2ª ed.) — Nygard
- *Chaos Engineering* — Rosenthal & Jones
- *Seeking SRE* — Blank-Edelman (ed.)
- *Database Reliability Engineering* — Campbell & Majors
- *The Practice of Cloud System Administration* — Limoncelli, Chalup & Hogan
- *Systems Performance* (2ª ed.) — Gregg
- *Quarkus Observability Guides* — Red Hat
