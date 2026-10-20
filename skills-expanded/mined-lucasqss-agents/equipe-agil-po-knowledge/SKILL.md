---
name: equipe-agil-po-knowledge
description: Conhecimento específico do Product Owner da Equipe Backend Ágil Kanban+XP. Cobre product discovery contínuo (Cagan, Torres), user story mapping (Patton), impact mapping (Adzic), specification by example (Adzic), Linguagem Ubíqua (Evans) como base do Glossário, regras de domínio executáveis (von Halle), priorização por valor (MoSCoW/WSJF complementar ao Kanban), INVEST, Definition of Ready, e a regra de referência inegociável entre Stories → Regras → Glossário. Invoque quando precisar planejar descoberta, escrever stories/critérios de aceite, definir DoR, decidir entrada na ready queue, ou modelar vocabulário ubíquo. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Product Owner — Conhecimento específico

Skill carregada pelo agente `equipe-agil-po` depois de `equipe-agil-kanban-method`. Cobre o que **só o PO** precisa dominar; práticas Kanban (Replenishment, classes of service, WSJF) e baseline de fluxo vivem em `equipe-agil-kanban-method`.

## 1. Conceitos centrais

### 1.1 Escopo do PO nesta equipe

- Absorve as responsabilidades do antigo **Analista de Requisitos/Negócios**.
- Owner do **backlog** e da entrega de **valor**; decisões de priorização e *trade-offs* de escopo.
- Conduz **Replenishment Meeting** (input cadence do Kanban) movendo trabalho de *options* para *ready queue*.
- Mantém os **três artefatos vivos** do produto (formato leve, herdados da tradição requirements com mesma regra de referência).
- **Pré-requisito explícito**: conhecimento básico de arquitetura de software, OO e padrões de projeto (GoF e enterprise), para dialogar com Arquitetos, identificar ASRs e modelar o domínio consistentemente.

### 1.2 Os três artefatos vivos do produto

1. **Linguagem Ubíqua / Glossário** — vocabulário compartilhado com o domínio. **Folha do grafo**: nada referencia para fora dele.
2. **Regras de Domínio** — invariantes e políticas; idealmente **especificações executáveis** (BDD) ou regras de domínio em código (von Halle).
3. **User Stories + Critérios de Aceite** — formato Gherkin/BDD; **topo do grafo**.

### 1.3 Regra de referência (direção permitida) — INEGOCIÁVEL

```
Stories     ──►  Regras       (permitido)
Stories     ──►  Glossário    (permitido)
Regras      ──►  Glossário    (permitido)
Regras      ──►  Stories      (PROIBIDO)
Glossário   ──►  qualquer     (PROIBIDO — folha do grafo)
```

**Justificativa**:
- O **Glossário** é folha imutável de vocabulário; termos não conhecem o produto.
- As **Regras** descrevem invariantes do domínio que existem **independentemente** do produto.
- As **Stories** estão no topo e podem invocar tanto regras quanto termos.

Violação típica: regra de domínio referenciando uma story específica = acoplamento errado. Refatorar a regra para descrever a invariante de domínio, não o caso de uso.

### 1.4 Continuous Discovery (Torres — *Continuous Discovery Habits*)

- Discovery **semanal**, não fase preliminar.
- *Opportunity Solution Tree* (OST): outcome → opportunities (problemas de usuário) → solutions → experiments.
- Trio de discovery: PO + designer + engenheiro (no nosso caso: PO + Arquiteto App + Tech Lead).
- ≥ 1 entrevista/semana com usuário/cliente; *assumption testing* antes de construir.
- **Anti-padrão**: "discovery sprint" no início e depois só delivery — vira waterfall disfarçado.

### 1.5 Empowered product teams (Cagan — *Inspired*, *Empowered*)

- Time de produto é responsável pelo **outcome**, não pelo output (feature entregue).
- Quatro grandes riscos a mitigar antes de construir: **value, usability, feasibility, business viability**.
- PO **não é tomador de pedidos** do stakeholder; é negociador de outcome.
- *Coach the team* > tell the team — alinha com Eng Coach.

### 1.6 User Story Mapping (Patton)

- Mapa em **2 dimensões**: eixo horizontal = jornada do usuário (backbone); eixo vertical = profundidade de funcionalidades para cada passo.
- Permite **slice MVP** horizontal (1ª linha = mínimo viável por jornada), depois fatias subsequentes de valor.
- Substitui backlog plano por mapa narrativo — facilita conversas com stakeholders.

### 1.7 Impact Mapping (Adzic)

Mapa visual em 4 níveis:

```
Goal (por quê)
 └─ Actor (quem)
     └─ Impact (como o comportamento muda)
         └─ Deliverable (o que entregamos)
```

Usa para garantir que cada deliverable está vinculado a uma mudança de comportamento mensurável de um ator, em direção a um goal de negócio.

### 1.8 Specification by Example / BDD (Adzic — *Specification by Example*)

- Critérios de aceite escritos como **exemplos concretos**, executáveis quando possível.
- Formato Gherkin: `Given · When · Then`.
- **Single source of truth**: a especificação é o teste é a documentação.
- Exemplos vivem ao lado do código (`/src/test/resources/features/*.feature`) e são executados no pipeline.
- **Three Amigos**: PO + dev + QE refinam exemplos juntos antes de virar story pronta.

### 1.9 Linguagem Ubíqua (Evans — *Domain-Driven Design*)

- **Mesma palavra, mesmo significado** — em conversas, código, banco, telas.
- Glossário **vive no projeto**, evolui com o código, é versionado.
- Termo novo no domínio → entrada no Glossário **antes** de virar story.
- Termo ambíguo entre subdomínios → bounded context separado (escalar para Arquiteto App).

### 1.10 Regras de Domínio como código executável (von Halle — *Business Rules Applied*)

- Regras de negócio são **artefatos de primeira classe**, separáveis das stories.
- Catálogo de tipos de regra: *definitional* (sempre verdade), *behavioral* (devem ser respeitadas), *derivation* (computações), *constraint* (limites).
- Quando viável, regras são implementadas como código de domínio puro (testável isoladamente), não como `if` espalhados.
- Glossário cita regras; regras citam glossário; stories citam ambos.

### 1.11 INVEST — qualidade de user story

Toda story na ready queue deve ser:

- **I**ndependent — sem dependência forte de outras stories da mesma janela.
- **N**egotiable — escopo conversável até começar.
- **V**aluable — entrega valor a um usuário ou stakeholder real.
- **E**stimable — time consegue dimensionar (ainda que probabilisticamente via throughput).
- **S**mall — cabe no ciclo de uma `pr-*` (≤ 1 dia) ou em poucos commits dentro da `feature/*`.
- **T**estable — critério de aceite concreto, idealmente Gherkin.

### 1.12 Priorização — quando usar o quê

- **WSJF** (default — vive em `equipe-agil-kanban-method`): sequenciamento dentro da ready queue.
- **MoSCoW** (Must / Should / Could / Won't): comunicação com stakeholders sobre escopo de release/quarter.
- **Outcomes Over Output** (Seiden): comprometer-se com outcome (métrica de negócio), entregar output flexível.
- Evitar estimativa por *story points* — usar throughput histórico + Monte Carlo (vive em `equipe-agil-kanban-method`).

## 2. Práticas e heurísticas operacionais

### 2.1 Rotina semanal do PO

| Dia típico | Ritual |
|------------|--------|
| Diário | Daily standup (Kanban, focado em itens) |
| Diário | ≤ 30 min em descoberta (entrevistas, dados, hipóteses) |
| Semanal | **Replenishment Meeting** (PO + Tech Lead + Eng Coach) |
| Semanal | Refinamento com Three Amigos (PO + dev + QE) |
| Quinzenal | Participa do **Service Delivery Review** (consultado) |
| Mensal | **Ops Review** (consumir dados de SLO/incidentes que afetam roadmap) |
| Trimestral | **Strategy Review** + revisão da OST |

### 2.2 Conduzindo um Replenishment Meeting eficaz

1. **Limpar a ready queue**: remover itens obsoletos (mais que N semanas sem pull).
2. **Capacidade**: olhar throughput médio da equipe (vem do Eng Coach).
3. **Candidatos**: top da *options column* + itens *Fixed Date* aproximando.
4. **Cada candidato passa pelo DoR** (3.1 abaixo); falhou DoR = volta para *options* com tarefa de readiness.
5. **Arquitetos** fazem caça aos ASRs (perguntas em `equipe-agil-arquitetura-base` §2.1).
6. **AppSec** consultado se item toca dado sensível ou fronteira de confiança.
7. **Atribuir classe of service** (Expedite/Fixed Date/Standard/Intangible) — vive em `equipe-agil-kanban-method`.
8. **Comprometer** — itens entram na ready queue ordenados por WSJF dentro de cada classe.

### 2.3 Three Amigos — refinamento de story

- **PO**: traz o "porquê" e o exemplo concreto.
- **Dev (Tech Lead ou par)**: testa a viabilidade técnica, pergunta sobre edge cases.
- **Quality Engineer**: pergunta "como vou saber que está pronto?" — força critérios testáveis.
- Output: story com Gherkin claro + glossário/regras atualizados se necessário.

### 2.4 Anti-padrões comuns do PO

- ❌ **PO como secretário de stakeholder**: backlog vira lista de pedidos, sem outcome.
- ❌ **Story = task técnica** (ex.: "criar tabela X"): tarefa técnica não é story; é parte da decomposição interna.
- ❌ **Critério de aceite vago** ("deve funcionar bem"): não é testável.
- ❌ **Regra de domínio dentro da story**: viola a regra de referência; extrair para o documento de Regras.
- ❌ **Glossário com termos de implementação** (ex.: "DTO", "endpoint"): glossário é vocabulário de **domínio**, não técnico.
- ❌ **"Vou perguntar depois"** na Replenishment: item não entra na ready queue sem DoR.
- ❌ **Discovery delegada para depois** ("primeiro entrega isso, depois pensamos"): viola continuous discovery.

### 2.5 Quando escalar para outros agentes

- **Para Arquiteto App**: dúvida sobre bounded context, modelagem de agregado, impacto intra-aplicação.
- **Para Arquiteto Sis**: item que cria/muda dependência inter-serviço, evento novo, fluxo distribuído.
- **Para AppSec**: dado pessoal, autenticação, autorização, fronteira de confiança nova.
- **Para SRE**: item com requisito de disponibilidade/latência atípico.
- **Para API Designer**: mudança em contrato público de API.
- **Para Eng Coach**: tensão com práticas (item pede atalho em XP/Kanban) ou conflito no time.

## 3. Templates e checklists

### 3.1 Definition of Ready (DoR) do PO — entrada na ready queue

Complementa a DoR genérica de `equipe-agil-kanban-method`:

- [ ] Story no formato Gherkin com ≥ 1 critério de aceite concreto.
- [ ] Outcome esperado declarado (métrica de negócio quando aplicável).
- [ ] Termos novos do domínio adicionados ao Glossário.
- [ ] Regras de domínio invocadas referenciadas (ou criadas se inexistentes).
- [ ] ASRs identificados (com Arquitetos no Replenishment) e flag setada.
- [ ] Classe of service atribuída.
- [ ] Riscos de segurança (AppSec) e operação (SRE) consultados quando relevantes.
- [ ] Dependências externas mapeadas (e cronograma de chegada confirmado).
- [ ] Tamanho ≤ 1 ciclo de `pr-*` ou ≤ poucos commits dentro da `feature/*`; se maior, **decompor**.

### 3.2 Template de User Story (Gherkin)

```gherkin
# story-NNN-<slug>.feature
Funcionalidade: <título — frase curta de outcome>
  Como         <ator>
  Eu quero     <ação>
  Para         <benefício / outcome de negócio>

  Contexto:
    Dado que <pré-condição de domínio>

  Cenário: <caso principal / golden path>
    Dado <estado inicial>
    Quando <ação do ator>
    Então <resultado observável>
    E <invariante de domínio confirmada>

  Cenário: <caso alternativo / edge>
    ...

  # Glossário referenciado: [termo1], [termo2]
  # Regras invocadas:        [regra-X], [regra-Y]
```

### 3.3 Template de entrada do Glossário

```markdown
## <Termo do Domínio>

**Definição**: <uma frase curta, em linguagem de negócio, sem jargão técnico>.

**Sinônimos aceitos**: <se houver>
**Termos relacionados**: <links internos>

**Exemplos**:
- <exemplo concreto>
- <contraexemplo — o que NÃO é>

**Observações**:
- <ambiguidade resolvida, decisão de nomenclatura, etc.>
```

### 3.4 Template de Regra de Domínio

```markdown
## Regra <ID>: <título imperativo>

**Tipo**: definitional | behavioral | derivation | constraint

**Invariante**: <enunciado da regra, em vocabulário do Glossário>

**Justificativa**: <por que essa regra existe no domínio>

**Exemplos**:
| Entrada | Saída esperada | Observação |
|---------|----------------|------------|
| ...     | ...            | ...        |

**Implementação executável**: <link para teste/spec/código de domínio>

**Glossário referenciado**: [termo1], [termo2]
```

### 3.5 Checklist de impact map antes da Strategy Review

- [ ] Goal claro, mensurável e datado.
- [ ] Atores priorizados (quem mais move o ponteiro).
- [ ] Impactos descritos como **mudança de comportamento** de cada ator.
- [ ] Deliverables ligados a ≥ 1 impacto (sem órfão).
- [ ] Pelo menos 1 hipótese de aprendizagem por deliverable (não só de entrega).

### 3.6 Outcomes vs Output — declaração de comprometimento

```
Outcome (o que muda no mundo):       <métrica mensurável + meta + janela>
Output (o que entregamos):           <flexível — feature, MVP, experimento>
Hipótese (por que acreditamos):      <belief que vamos validar>
Sinal de falha rápida:               <métrica/observação que abandona a aposta>
```

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-po`, **depois** de `equipe-agil-kanban-method`.

O PO usa esta skill para:
- Conduzir Replenishment com critério (DoR + caça aos ASRs).
- Escrever stories INVEST + Gherkin.
- Manter os três artefatos vivos respeitando a regra de referência.
- Operar continuous discovery sem reverter para waterfall.
- Comunicar trade-offs de escopo com stakeholders (MoSCoW, outcomes over output).

Outros papéis **consomem** os artefatos (Glossário, Regras, Stories) mas **não carregam** esta skill.

## References

Bibliografia das seções 3.1 (Fundamental + Avançada) do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Inspired: How to Create Tech Products Customers Love* — Cagan
- *Empowered* — Cagan & Jones
- *User Story Mapping* — Patton
- *Impact Mapping* — Adzic
- *Specification by Example* — Adzic
- *Domain-Driven Design* — Evans *(linguagem ubíqua, base do Glossário)*
- *Continuous Discovery Habits* — Torres
- *The Lean Startup* — Ries
- *Lean UX* (3ª ed.) — Gothelf & Seiden
- *Escaping the Build Trap* — Perri
- *Outcomes Over Output* — Seiden
- *The Lean Product Playbook* — Olsen
- *Business Rules Applied* — von Halle
- *Bridging the Communication Gap* — Adzic
- *Software Requirements* (3ª ed.) — Wiegers & Beatty
- *Mastering the Requirements Process* (3ª ed.) — Robertson & Robertson
- *Discovery Discipline* — Bonnet & Cossette
