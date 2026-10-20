---
name: equipe-agil-engineering-coach-knowledge
description: Conhecimento específico do Engineering Coach (XP + Flow Steward) da Equipe Backend Ágil Kanban+XP. Cobre GOOS (Freeman & Pryce), Clean Code (Martin), Pragmatic Programmer, legacy code (Feathers — seams, characterization tests), xUnit Test Patterns (Meszaros — test doubles), Refactoring to Patterns (Kerievsky), Mikado Method, Philosophy of Software Design (Ousterhout — deep modules), mutation testing (PIT em Java) e property-based testing (jqwik). Invoque quando precisar coachar TDD/pair/mob, diagnosticar code smells, planejar trabalho em legado, escolher test doubles, melhorar mutation score, ou facilitar Service Delivery Review. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Engineering Coach (XP + Flow Steward) — Conhecimento específico

Skill carregada pelo agente `equipe-agil-engineering-coach` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento técnico de craft e coaching que o Eng Coach precisa para ser **owner explícito das práticas XP** e **owner das métricas de fluxo Kanban**.

## 1. Conceitos centrais

### 1.1 Mandato do Engineering Coach na equipe

- **Owner explícito das práticas XP**: TDD, pair/mob, refactoring, simple design, CI na hierarquia `pr-*` → `feature/*` (vide `equipe-agil-xp-baseline`).
- **Owner das métricas de fluxo Kanban**: lead time, cycle time, throughput, CFD, aging WIP; **coacha o time a interpretar e agir** sobre os números (vide `equipe-agil-kanban-method`).
- **Facilita as 7 cadências Kanban**, especialmente Daily, SDR e Risk Review.
- Coacha o time em técnicas avançadas (mutation testing, test doubles, property-based, strangler fig).
- **Não decide arquitetura** (Arquitetos) nem **priorização** (PO); **garante que code craft e fluxo sejam realidade**.
- RACI: A/R em Cadências Kanban, Métricas de Fluxo, Práticas de Engenharia.

### 1.2 GOOS — Growing Object-Oriented Software, Guided by Tests (Freeman & Pryce)

- **Double loop TDD**:
  - *Outer loop*: acceptance test falhando (end-to-end pelo *walking skeleton*).
  - *Inner loop*: red-green-refactor de unidade até o acceptance passar.
- **Walking skeleton**: menor implementação end-to-end que exercita toda a infra (deploy, build, persistência, contratos) — antes de implementar regra de negócio.
- **Mock roles, not objects**: testes dirigem a descoberta de **papéis** (interfaces de colaboração), não imitam classes concretas.
- **Listen to the tests**: testes difíceis de escrever sinalizam design fraco (acoplamento, responsabilidade mal posta) — refactor antes de continuar.

### 1.3 Clean Code (Martin) — heurísticas operacionais

- **Funções pequenas** (≤ 20 linhas; idealmente ≤ 5); **fazem uma coisa**; **um nível de abstração** por função.
- **Nomes revelam intenção**; sem abreviações sem contexto; sem prefixos húngaros.
- **Sem comentários que descrevem o quê** (o código diz); comentários só para **por quê** não-óbvio (vide CLAUDE.md desta equipe).
- **Classes pequenas, coesas**: SRP (Single Responsibility) operacionalizado como "uma razão para mudar".
- **Boy Scout Rule**: deixe o código melhor do que encontrou.

### 1.4 Pragmatic Programmer (Hunt & Thomas, ed. 20º aniversário)

- **DRY** — Don't Repeat Yourself, mas no nível de **conhecimento**, não de texto.
- **Orthogonality** — componentes independentes; mudança em um não cascateia em outros.
- **Tracer bullets** — implementar fim-a-fim cedo, ajustar mira (similar ao walking skeleton).
- **Broken Windows** — degradação começa pequena; corrija já.
- **Programming by coincidence** — code que funciona "porque sim" é dívida.

### 1.5 Legacy Code (Feathers — *Working Effectively with Legacy Code*)

- **Definição operacional de legado**: código **sem testes**.
- ***Seams***: pontos do código onde se pode alterar comportamento **sem editar o código original** (object seam, link seam, preprocessing seam). Usar seams para injetar fakes/mocks em código não testável.
- ***Characterization tests***: testes que capturam o comportamento **atual** (mesmo que não-intencional) antes de mudar — proteção contra regressão.
- **Estratégia em legado**:
  1. Encontrar pontos de mudança.
  2. Encontrar seams próximos.
  3. Quebrar dependências mínimas (sprout method/class, extract interface).
  4. Escrever characterization tests.
  5. Mudar com confiança.
- **Sprout Method**: novo comportamento em método novo (testável), código antigo chama-o.
- **Sprout Class**: idem para classes inteiras quando o legado é grande.

### 1.6 xUnit Test Patterns (Meszaros) — taxonomia de test doubles

- **Dummy** — passado mas nunca usado (preencher assinatura).
- **Stub** — devolve respostas pré-programadas para inputs.
- **Spy** — stub que **registra** chamadas para verificação posterior.
- **Mock** — pré-programado com **expectativas** (falha se chamadas esperadas não acontecem).
- **Fake** — implementação real simplificada (ex.: in-memory repository).

**Heurística**:
- Prefira **fake** (in-memory) quando o colaborador tem comportamento interno relevante.
- Use **stub** para dependências externas determinísticas.
- Use **mock** com parcimônia — testes acoplados a interação são frágeis.
- Use **Testcontainers** (Java) para integrar contra serviço real quando viável (banco, broker) — vive em `quality-engineer-knowledge`.

### 1.7 Refactoring to Patterns (Kerievsky)

- Refactoring **rumo a** um padrão (não aplicar padrão de cara).
- Catálogo: *Move Accumulation to Collecting Parameter*, *Compose Method*, *Replace Conditional Dispatcher with Command*, *Move Embellishment to Decorator*, etc.
- **Padrão emerge da pressão** (duplicação, divergent change, shotgun surgery) — não da especulação.
- Caminhos *toward*, *through* e *away from* patterns — padrões podem ser **removidos** quando deixaram de fazer sentido.

### 1.8 Mikado Method (Ellnestam & Brolund)

Técnica para **mudanças grandes em código complexo** sem perder o verde do CI:

1. Defina **goal** (Mikado).
2. Tente fazer a mudança ingenuamente.
3. Anote tudo que quebrou; **desfaça** e crie pré-requisitos.
4. Para cada pré-requisito, recurse.
5. Quando uma folha é alcançável e segura, faça-a, commit verde.
6. Vá subindo a árvore.

Resultado: refactor grande feito em passos pequenos, com main verde a cada passo (compatível com `pr-*` → `feature/*`).

### 1.9 Philosophy of Software Design (Ousterhout)

- **Complexity is incremental** — pequenas decisões ruins acumulam.
- **Deep modules**: interface estreita, implementação rica.
- **Information hiding** > information leakage; um módulo que precisa expor seu detalhe interno é raso.
- **Define errors out of existence** (ex.: substring que nunca falha em vez de exception).
- **Pull complexity downwards** — vale a pena complicar a implementação para simplificar interface usada por muitos.
- **Comments should describe things that are not obvious from the code** (alinhado com instruções desta equipe).

### 1.10 Mutation Testing (PIT para Java)

- **Princípio**: gerar **mutantes** (versões do código com pequenas mudanças); rodar a suite; se nenhum teste **mata** o mutante, a suite tem buracos.
- **Mutation Score**: % de mutantes mortos pela suite.
- Heurística: mutation score > 80% indica suite robusta; abaixo de 60% indica testes confirmatórios (existem mas não validam comportamento).
- **PIT** é a ferramenta padrão Java; integra com Maven/Gradle e CI.
- Anti-padrão: usar **line coverage** como métrica de qualidade — coverage 100% pode ter mutation 20%.

### 1.11 Property-Based Testing (jqwik para Java)

- **Princípio**: declarar uma **propriedade** que deve valer para qualquer input; framework gera centenas de inputs aleatórios + *shrinking* para encontrar caso mínimo falho.
- Complementa example-based tests (não substitui): casos representativos via Gherkin/JUnit + propriedades para invariantes (ex.: *idempotência*, *comutatividade*, *roundtrip serialize-deserialize*).
- **jqwik** é a biblioteca padrão Java; integra com JUnit 5.

### 1.12 Code as Crime Scene / Software Design X-Rays (Tornhill)

- Análise **comportamental** de código: cruzar git log com hotspots para encontrar **arquivos que mudam muito + complexos** = candidatos prioritários a refactor.
- **Coupling temporal**: arquivos que mudam **juntos** ao longo do tempo revelam acoplamento implícito (Shotgun Surgery em formato historiado).
- Ferramentas: CodeScene, code-maat.
- Útil para Risk Review (vide cadências).

## 2. Práticas e heurísticas operacionais

### 2.1 Coaching de TDD — diagnósticos comuns

| Sintoma observado | Diagnóstico | Intervenção |
|-------------------|-------------|-------------|
| Teste passa de primeira | Não houve Red — não é TDD | Pedir para reverter implementação e ver vermelho |
| Teste muito grande / setup imenso | Design acoplado | *Listen to the tests* — extrair colaborador |
| Mock everything | Testes de interação frágeis | Migrar para fake / teste de comportamento |
| Cobertura alta, mutation baixa | Testes confirmatórios | Sessão de mutation testing |
| Refactor sem teste verde antes/depois | Risco escondido | Parar; voltar ao verde; recomeçar |

### 2.2 Coaching de pair/mob

- Rotação a cada 25–50 min (pair) ou 5–10 min (mob) — vide `equipe-agil-xp-baseline`.
- **Silent pair** = não é pair: facilitar por perguntas (*"o que faríamos a seguir?"*).
- *Driver autônomo* + navigator passivo: chamar o navigator a verbalizar.
- Em mob, **strong-style pairing** (Falco): *"if you have an idea, you must take the keyboard"*.

### 2.3 Service Delivery Review — pauta padrão

1. **CFD da última quinzena** — bandas estáveis? engordando?
2. **Cycle time scatter** — p85/p95 deslocando?
3. **Aging WIP** — itens estagnados há > p85 histórico → discutir caso a caso.
4. **Throughput** — variabilidade aumentou?
5. **Bloqueios crônicos** (Risk Review feed).
6. **Mutation score / DORA** — tendência.
7. **Experimentos a propor** (kaizen) — uma mudança de política por SDR.

### 2.4 Conduzindo um Risk Review

- Lista os bloqueios (idade × frequência).
- Lista a dívida técnica catalogada (com link para hotspots — Tornhill).
- Lista falhas em fitness functions recentes.
- Lista incidentes (de Ops Review) com vínculo a item Intangible.
- Saída: itens *Intangible* para entrar na ready queue + acordos de política.

### 2.5 Quando aplicar Mikado vs refactor direto

- **Refactor direto** (boy scout): mudança ≤ 1 commit, sem cascata.
- **Mikado**: mudança que quebra o build ao tentar ingenuamente, com cascata > 1 dia. Conjugar com Branch by Abstraction + Feature Flag dentro da `feature/*`.

### 2.6 Coaching anti-padrões a evitar

- ❌ **Coach que escreve o código**: o time fica passivo.
- ❌ **Coach que vira gerente**: confunde mandato com Tech Lead/PO.
- ❌ **Métrica como vara**: usar lead time/throughput para cobrar indivíduo destrói a coleta.
- ❌ **Ritual sem propósito**: SDR sem ação concreta = teatro.
- ❌ **Doutrina sem contexto**: "fazemos sempre X" sem checar se X resolve o problema do time.

## 3. Templates e checklists

### 3.1 Pauta padrão do Service Delivery Review (15 itens, 60 min)

1. Bem-vindas + outcomes do SDR anterior — 5 min.
2. CFD comentado — 10 min.
3. Cycle Time scatter + percentis — 10 min.
4. Aging WIP — casos individuais — 10 min.
5. Throughput run chart — 5 min.
6. Mutation score & DORA — 5 min.
7. 1 experimento de política para a próxima quinzena — 10 min.
8. Action items + owners + data — 5 min.

### 3.2 Checklist "essa intervenção é coaching ou comando?"

- [ ] Pergunta antes de afirmar?
- [ ] Devolve a decisão ao time?
- [ ] Aponta para princípio ou padrão, não para "minha preferência"?
- [ ] Mensura efeito da intervenção em ≥ 1 métrica?
- [ ] Permite ao time errar e aprender quando o custo é baixo?

≥ 4 marcados = coaching. ≤ 2 = comando — recuar.

### 3.3 Receita de characterization test (Feathers)

```
1. Identifique o módulo legado a tocar.
2. Encontre um seam (object/link/preprocessing).
3. Escreva um teste que invoca o código com input plausível.
4. Capture a saída **observada** (não a esperada).
5. Faça o teste asseverar essa saída observada exatamente.
6. Rode N vezes — se determinístico, é o golden master.
7. Agora você tem rede. Refatore.
```

### 3.4 Template de plano Mikado

```
Goal (Mikado): <mudança desejada>

Tentativa ingênua: <data> — falhou em:
  - <quebra 1>
  - <quebra 2>

Pré-requisitos (folhas a baixo são feitas primeiro):
  └─ Pré-requisito A
      └─ Pré-requisito A.1
      └─ Pré-requisito A.2
  └─ Pré-requisito B
      └─ ...

Estado atual: <folha sendo trabalhada>
```

### 3.5 Brown bag — calendário sugerido (rotação trimestral)

| Semana | Tema sugerido |
|--------|---------------|
| 1 | Walking skeleton de feature nova (GOOS) |
| 2 | Test doubles na prática (Meszaros) |
| 3 | Mutation testing — workshop com PIT |
| 4 | Hotspots do repositório (Tornhill) |
| 5 | Property-based testing com jqwik |
| 6 | Mikado em refactor real do backlog |
| 7 | Refactoring to Patterns aplicado |
| 8 | Discussão de CFD/aging WIP do mês |
| 9 | Philosophy of Software Design — deep modules |
| 10 | Working Effectively with Legacy Code — sessão prática |
| 11 | DORA: o que nossos números estão dizendo |
| 12 | Retrospectiva técnica do trimestre |

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-engineering-coach`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O Eng Coach:
- **Não escreve código de feature**; codifica para ensinar (workshops, dojos, kata).
- **Não decide arquitetura nem prioriza**: encaminha ao Arquiteto/PO.
- **É o RACI A/R** das práticas e métricas; tem autoridade para interromper o fluxo (stop-the-line) quando uma prática inegociável é violada.

## References

Bibliografia das seções 3.2 (Fundamental + Avançada) do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Growing Object-Oriented Software, Guided by Tests* — Freeman & Pryce
- *Clean Code* — Martin
- *The Pragmatic Programmer* (20º aniv.) — Hunt & Thomas
- *Working Effectively with Legacy Code* — Feathers
- *xUnit Test Patterns* — Meszaros
- *Refactoring to Patterns* — Kerievsky
- *A Philosophy of Software Design* — Ousterhout
- *When Will It Be Done?* — Vacanti
- *Rethinking Agile* — Leopold
- *Flow Engineering* — Phillips & Kersten
- *Implementation Patterns* — Beck
- *Smalltalk Best Practice Patterns* — Beck
- *Effective Software Testing* — Aniche
- *Specification by Example* — Adzic
- *The Mikado Method* — Ellnestam & Brolund
- *Software Design X-Rays* — Tornhill
- *Your Code as a Crime Scene* — Tornhill
