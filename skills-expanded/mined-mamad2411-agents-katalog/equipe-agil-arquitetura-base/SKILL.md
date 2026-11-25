---
name: equipe-agil-arquitetura-base
description: Fundamentos de arquitetura de software compartilhados pelos dois Arquitetos da Equipe Backend Ágil Kanban+XP (Arquiteto App e Arquiteto Sis). Invoque sempre que precisar fundamentar decisões arquiteturais transversais — quality attributes/-ilities (Bass), Architecturally Significant Requirements (ASRs), ADR (Nygard), fitness functions automatizadas (Ford), risk-driven design (Fairbanks), modelo C4, evolutionary architecture, views & beyond (Clements), trade-off de atributos de qualidade ou raciocínio sobre estilo arquitetural. Não cobre design intra-aplicação específico (vive em arquiteto-app-knowledge) nem sistemas distribuídos específicos (vive em arquiteto-sis-knowledge). Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Fundamentos de Arquitetura — Base compartilhada entre Arquitetos

Skill carregada **pelos dois Arquitetos** (Arquiteto App e Arquiteto Sis) da Equipe Backend Ágil Kanban+XP, depois dos baselines `equipe-agil-xp-baseline` e `equipe-agil-kanban-method` e antes das skills de conhecimento específico de cada um.

## 1. Conceitos centrais

### 1.1 O que é arquitetura — definições operacionais

- **Richards & Ford**: arquitetura é composta por *structure, characteristics, decisions, design principles*.
- **Bass et al.**: arquitetura é o conjunto de estruturas (de componentes, de runtime, de alocação) **mais** as decisões que constrangem mudanças futuras.
- **Fowler**: "architecture is the things that are hard to change later."
- **Heurística operacional**: se é caro/lento mudar depois, é arquitetura.

### 1.2 Quality Attributes / -ilities (Bass — *Software Architecture in Practice*)

- **Definição**: propriedade mensurável de um sistema que indica quão bem ele satisfaz necessidades além das funcionais.
- **Lista canônica priorizada para backend/APIs**: performance, scalability, availability, reliability, security, maintainability, modifiability, deployability, testability, observability, interoperability, usability (API DX), portability, cost.
- ***Quality Attribute Scenarios*** (Bass) — formato testável de ASR:
  `source · stimulus · environment · artifact · response · response measure`
  Ex.: "Sob 2× carga normal, o serviço responde em < 500 ms p95 por ≥ 10 min sem degradar disponibilidade abaixo de 99,9%".
- **Trade-offs são inevitáveis**: alta consistência ↔ alta disponibilidade (CAP); alta segurança ↔ alta usabilidade; baixo acoplamento ↔ alta performance. Tornar trade-offs **explícitos** no ADR.

### 1.3 Architecturally Significant Requirements (ASRs)

- Subconjunto de requisitos que **moldam** a arquitetura: alto impacto estrutural, alto custo de mudança ou definem o estilo.
- **Caça aos ASRs no Replenishment**: para cada item, perguntar — esse requisito muda topologia, contratos, performance budget, modelo de dados, modelo de segurança ou modelo de falha? Se sim, é ASR.
- ASR vira **ADR** + atualização de **fitness function** quando confirmado.

### 1.4 ADR — Architecture Decision Records (Nygard)

- Decisões arquiteturais devem ser **registradas no momento em que são tomadas**, não reconstruídas depois.
- **Formato leve** (uma página): `Title · Status (Proposed/Accepted/Deprecated/Superseded) · Context · Decision · Consequences · Alternatives consideradas · Links`.
- **Onde vivem**: dentro do projeto, em `/<projeto>/arquitetura/adr/NNNN-<slug>.md` (princípio 11 + seção 2.A do prompt).
- **Imutabilidade**: ADR é imutável após *Accepted*; mudança = nova ADR que *supersedes* a anterior.

### 1.5 Fitness Functions (Ford — *Building Evolutionary Architectures*)

- **Definição**: teste objetivo que mede se uma característica arquitetural (uma "-ility") está sendo preservada.
- **Categorias**:
  - *Atomic vs holistic* — verifica uma característica vs várias juntas.
  - *Triggered vs continuous* — roda em CI/release vs em produção (monitoring).
  - *Static vs dynamic* — limite fixo vs limite que evolui (ex.: budget de complexidade ciclomática).
  - *Manual vs automated* — preferir automated; manual aceitável como ponte temporária.
- **Exemplos executáveis em projeto Java/Quarkus**:
  - Testes de dependência entre pacotes via **ArchUnit** (aprofundado em `arquiteto-app-knowledge`).
  - Limite de tempo de build (Ten-Minute Build do XP).
  - Latência p95 abaixo de X ms em smoke de perf (Gatling/JMeter no pipeline).
  - Score de cobertura de mutação acima de N% (PIT).
  - Zero CVE críticos via SCA (OWASP Dependency-Check / Trivy).
- Toda fitness function relevante **roda em pipeline** e falha o build se violada.

### 1.6 Risk-Driven Architecture (Fairbanks — *Just Enough Software Architecture*)

- **Princípio**: "Architectural effort should be proportional to risk."
- **Processo**:
  1. **Identificar riscos** (técnicos, organizacionais, de domínio).
  2. **Selecionar técnica** apropriada a cada risco (modeling, prototipagem, benchmark, threat modeling, etc.).
  3. **Aplicar** até reduzir o risco a um nível aceitável.
  4. **Parar** — não fazer mais arquitetura do que o risco justifica.
- **Anti-padrão**: *gold-plated architecture* (decisão arquitetural sem risco que a justifique) ou *cowboy* (zero arquitetura com riscos altos).

### 1.7 Modelo C4 (Simon Brown — sintetizado em Richards & Ford)

4 níveis de zoom para diagramas:

- **C1 — Context**: o sistema como caixa preta + usuários + sistemas externos.
- **C2 — Container**: deployables (apps, bancos, brokers) dentro do sistema; tecnologias citadas.
- **C3 — Component**: componentes internos de um container (módulos, agregados, adapters).
- **C4 — Code** (opcional): classes/funções — geralmente gerado, raramente desenhado à mão.

**Regra**: cada diagrama declara seu nível e tem uma **legenda explícita**; sem legenda = diagrama inválido. Diagramas vivem em `/<projeto>/arquitetura/diagramas/`.

### 1.8 Documenting Software Architectures — Views & Beyond (Clements et al.)

Arquitetura é multi-vista; nenhuma vista única captura tudo.

**Três categorias de visão**:
- *Module views* — como o sistema é dividido em unidades de implementação (decomposição, uso, layer).
- *Component-and-connector (C&C) views* — comportamento em runtime (pipe-and-filter, client-server, publish-subscribe).
- *Allocation views* — mapeamento para ambiente (deployment, work assignment, implementation).

**Regra**: documente apenas as vistas que respondem a perguntas de stakeholders concretos. Documentar tudo = documentar nada.

### 1.9 Evolutionary Architecture (Ford, Parsons, Kua & Sadalage)

- **Definição**: arquitetura projetada para suportar **mudança guiada e incremental** em múltiplas dimensões (técnica, dados, domínio, operacional).
- **Três princípios**:
  1. **Fitness functions** como guarda-corpos automatizados.
  2. **Mudança incremental** habilitada por baixo acoplamento e deploy automatizado.
  3. **Múltiplas dimensões de mudança** consideradas explicitamente.
- ***Last responsible moment***: decida quando o custo de adiar passa a ser maior que o custo de errar. Antes disso, mantenha opções abertas.

### 1.10 Estilos arquiteturais — vocabulário comum

- ***Monolithic*** (layered, modular, vertical slice, microkernel, pipeline) → escopo intra-aplicação (**Arquiteto App** aprofunda).
- ***Distributed*** (service-based, microservices, event-driven, space-based, serverless) → escopo inter-aplicação (**Arquiteto Sis** aprofunda).
- A escolha do estilo é a decisão arquitetural de **maior impacto** — deve nascer **ASR-driven + risk-driven**, registrada em ADR top-level.

## 2. Práticas e heurísticas operacionais

### 2.1 Caça aos ASRs no Replenishment

Para cada item entrando na ready queue, os Arquitetos perguntam (rápido — 30 s por item):

- Muda contrato externo?
- Muda performance budget (p95, throughput, custo)?
- Muda modelo de dados (esquema, dono, consistência)?
- Muda topologia (novo serviço, broker, dependência)?
- Muda modelo de segurança (autz, dado sensível, fronteira de confiança)?
- Muda modelo de falha (resiliência, blast radius)?

Qualquer "sim" = item entra com flag de ASR e **tarefa de ADR vinculada** antes do *done*.

### 2.2 Escrevendo um ADR útil

- **Context** descreve a **tensão**, não a solução; deixe claro qual ASR ou risco motivou.
- **Decision** é uma frase **imperativa**: "Adotaremos X."
- **Consequences** lista o **bom e o ruim** explicitamente — sem isso, vira propaganda.
- **Alternatives considered** mostra que outras opções foram avaliadas (mesmo que rejeitadas em parágrafo curto).
- ADR sem trade-off explícito = ADR fraca; revise.

### 2.3 Escolhendo fitness functions com economia

- Comece pela -ility mais cara para o time hoje (a que mais quebra ou que mais consome tempo de revisão manual).
- Prefira fitness functions **executáveis no CI** sobre auditorias manuais.
- Cada fitness function deve falhar **rápido e claro**, com mensagem que aponta para o ADR que ela protege.
- Evite fitness functions **redundantes** — vira ruído e dessensibiliza o time.

### 2.4 Quando NÃO fazer arquitetura (risk-driven aplicado)

- Sem risco identificado + sem ASR = **não** escreva ADR, **não** desenhe diagrama, **codifique**.
- Excesso de arquitetura up-front é desperdício (Reinertsen — fila de decisões não validadas).
- Reserve esforço arquitetural para o que mover o ponteiro de risco.

### 2.5 Anti-padrões arquiteturais comuns

- ❌ **Arquitetura cerimonial** — ADRs e diagramas que ninguém consulta porque não amarram a decisão.
- ❌ **Gold plating** — generalização sem ASR (especulação).
- ❌ **Cowboy** — código importante sem ADR, sem fitness function, "todo mundo sabe".
- ❌ **Documentação após o fato** — ADR escrita depois que o código mergeu vira histórico, não decisão.
- ❌ **Big Architecture Up Front** sem feedback empírico.
- ❌ **Fitness function teatral** — verifica algo trivial e cria sensação falsa de cobertura.

### 2.6 Como Arquiteto App e Arquiteto Sis colaboram

- **Arquiteto App**: dono das decisões **dentro** de um deployable (módulos, agregados, adapters, persistência local, ArchUnit, design tático DDD).
- **Arquiteto Sis**: dono das decisões **entre** deployables (granularidade de serviço, integração, mensageria, sagas, contratos inter-serviço, dados distribuídos, resiliência).
- **Sobreposição**: contratos de API (API Designer A/R com C de ambos), fronteiras de bounded context que viram serviço, decisão *monolith vs split*.
- **Quando discordam**: vencer com dados (ASR + fitness function), não opinião — escalar ao Eng Coach se persistir.

## 3. Templates e checklists

### 3.1 Template de ADR (uma página)

```markdown
# ADR-NNNN: <Título curto, declarativo>

- **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- **Data**: YYYY-MM-DD
- **Autores**: <pair de arquitetos>
- **ASR vinculado**: <ID/link>
- **Risco que motivou**: <bullet curto>

## Contexto
<A tensão / força em jogo. Sem solução aqui.>

## Decisão
<Frase imperativa: "Adotaremos X.">

## Consequências
**Positivas**:
- ...

**Negativas / custos**:
- ...

## Alternativas consideradas
- **X** — rejeitada porque ...
- **Y** — rejeitada porque ...

## Fitness functions associadas
- <link para teste/check no pipeline>

## Links
- ADR-MMMM (relacionada)
- Diagrama Cn correspondente
```

### 3.2 Template de Quality Attribute Scenario (ASR testável)

```
Source:            <quem/o quê dispara — usuário, sistema externo, evento>
Stimulus:          <o que acontece — pico de carga, falha de dependência, requisição>
Environment:       <estado do sistema — normal, degradado, em manutenção>
Artifact:          <componente afetado — serviço X, banco Y>
Response:          <comportamento esperado — retorna 503 com Retry-After, ativa circuit breaker>
Response measure:  <métrica concreta — < 500 ms p95, ≥ 99.9% availability por 30d>
```

### 3.3 Checklist "essa decisão precisa de ADR?"

- [ ] Afeta contrato externo (API/evento) consumido por outro time?
- [ ] Muda performance/scalability/availability budget?
- [ ] Muda modelo de dados (dono, esquema, consistência)?
- [ ] Muda fronteira de segurança ou modelo de autz?
- [ ] Cria ou remove dependência inter-serviço?
- [ ] Escolhe tecnologia/biblioteca com custo de troca alto?
- [ ] Define padrão que outros componentes deverão seguir?

≥ 1 marcado = **escreva ADR antes do código**.

### 3.4 Checklist de qualidade de ADR

- [ ] Status explícito.
- [ ] Contexto descreve a tensão, não a solução.
- [ ] Decisão é uma frase imperativa.
- [ ] Consequências negativas listadas (não só positivas).
- [ ] ≥ 1 alternativa considerada com justificativa de rejeição.
- [ ] Fitness function associada (quando aplicável) com link para o pipeline.
- [ ] Diagrama Cn referenciado (quando aplicável).

### 3.5 Estrutura de pastas de arquitetura (consistente com seção 2.A do prompt)

```
/<projeto>/arquitetura/
├── adr/
│   ├── 0001-adocao-clean-architecture.md
│   ├── 0002-event-driven-para-notificacoes.md
│   └── ...
├── diagramas/
│   ├── c1-context.png + c1-context.md
│   ├── c2-container.png + c2-container.md
│   ├── c3-component-pagamentos.png + ...md
│   └── fitness-functions.md
└── asrs/
    └── asr-<id>-<slug>.md
```

## 4. Como esta skill é usada pelos agentes

Skill compartilhada **apenas pelos dois Arquitetos** (`equipe-agil-arquiteto-app` e `equipe-agil-arquiteto-sis`). Eles a carregam **depois** de `equipe-agil-xp-baseline` e `equipe-agil-kanban-method` e **antes** de sua skill de conhecimento específico.

- **Arquiteto App** usa esta skill para fundamentar decisões intra-aplicação (depois aprofunda em Clean Architecture, DDD tático, GoF, ArchUnit na sua skill própria).
- **Arquiteto Sis** usa esta skill para fundamentar decisões inter-aplicação (depois aprofunda em microservices, EIP, sagas, Kleppmann na sua skill própria).
- Ambos produzem **ADRs** vinculadas a **ASRs** com **fitness functions** automatizadas no pipeline da equipe (commit stage / acceptance stage da `feature/*`).
- **Tech Lead, Eng Coach, AppSec, SRE, DevOps, API Designer** consomem ADRs e diagramas, mas **não carregam** esta skill — interagem com os Arquitetos.

## References

Bibliografia da seção 3.3a do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Fundamentals of Software Architecture* — Richards & Ford
- *Software Architecture in Practice* (4ª ed.) — Bass, Clements & Kazman
- *Just Enough Software Architecture: A Risk-Driven Approach* — Fairbanks
- *Documenting Software Architectures: Views and Beyond* (2ª ed.) — Clements et al.
- *Building Evolutionary Architectures* (2ª ed.) — Ford, Parsons, Kua & Sadalage
- *Documenting Architecture Decisions* — Michael Nygard *(artigo seminal sobre ADR — complementar)*
