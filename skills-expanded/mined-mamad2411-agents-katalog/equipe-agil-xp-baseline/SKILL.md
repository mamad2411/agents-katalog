---
name: equipe-agil-xp-baseline
description: Base de Extreme Programming + Continuous Delivery + DORA compartilhada por todos os papéis técnicos da Equipe Backend Ágil Kanban+XP. Invoque sempre que precisar fundamentar decisões de TDD, pair/mob, simple design, refactoring, Continuous Integration, hierarquia de branches da equipe (pr-* dentro de feature/<funcionalidade>), feature flags, build pipeline, métricas DORA ou trunk-based development. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Baseline XP + Continuous Delivery + DORA

Conhecimento técnico inegociável compartilhado por todos os papéis técnicos da Equipe Backend Ágil Kanban+XP: Engineering Coach, Arquiteto App, Arquiteto Sis, Tech Lead, Quality Engineer, Data Engineer, AppSec, DevOps, SRE e API Designer.

## 1. Conceitos centrais

### 1.1 Valores e princípios XP (Beck — *XP Explained*, 2ª ed.)

- **Valores**: Communication, Simplicity, Feedback, Courage, Respect.
- **Princípios secundários**: Humanity, Economics, Mutual Benefit, Self-Similarity, Improvement, Diversity, Reflection, Flow, Opportunity, Redundancy, Failure, Quality, Baby Steps, Accepted Responsibility.

Valores guiam a postura; princípios traduzem a postura em escolhas concretas.

### 1.2 As 12 práticas primárias XP

1. Sit Together
2. Whole Team
3. Informative Workspace
4. Energized Work (*sustainable pace*)
5. Pair Programming
6. Stories (slim, customer-visible)
7. Weekly Cycle
8. Quarterly Cycle
9. Slack
10. Ten-Minute Build
11. Continuous Integration
12. Test-First Programming

**Práticas corolárias (segundo Beck)**: Real Customer Involvement, Incremental Deployment, Team Continuity, Shrinking Teams, Root-Cause Analysis, Shared Code, Code and Tests, Single Code Base, Daily Deployment, Negotiated Scope Contract, Pay-Per-Use.

### 1.3 TDD — ciclo Red / Green / Refactor (Beck — *TDD by Example*)

- **Red**: escreva um teste que falha por uma razão clara (e somente uma).
- **Green**: faça passar com o **menor código possível** (até *fake it 'til you make it* / triangulação).
- **Refactor**: melhore o design sem alterar comportamento; remova duplicação; nomeie melhor.

**Regras de Beck**:
- Nunca escreva código de produção sem um teste vermelho.
- Nunca escreva mais teste do que o necessário para falhar.
- Nunca escreva mais produção do que o necessário para passar.

### 1.4 Simple Design — 4 regras (Beck, em ordem decrescente de prioridade)

1. Passa em todos os testes.
2. Revela intenção (nomes claros, estrutura óbvia).
3. Sem duplicação (DRY).
4. Mínimo de elementos (sem código morto, sem abstração especulativa).

Quando 2 e 3 conflitam, 2 vence: clareza > brevidade.

### 1.5 Pair & Mob Programming (Shore & Warden — *Art of Agile* 2ª ed.)

- **Pair**: driver (foca no "como") + navigator (foca no "o quê / próximo passo / qualidade"). Troca a cada 25–50 min ou commit. *Ping-pong pairing* funciona muito bem com TDD (um escreve o teste, o outro implementa).
- **Mob**: a equipe inteira no mesmo problema; um teclado de cada vez; rotação a cada 5–10 min (Llewellyn Falco). Reduz hand-off, acelera difusão de conhecimento.
- **Benefícios**: revisão contínua, *knowledge sharing*, menor *bus factor*, qualidade embutida.
- **Anti-padrão**: *silent pair* (duas pessoas lendo em silêncio) — não é pair.

### 1.6 Continuous Integration (Humble & Farley — *CD*; Hammant — *Trunk-Based*, com variação local em dois níveis)

- **Definição de Fowler**: todos integram pelo menos diariamente; CI verde antes do próximo commit.
- **Convenção da equipe (variação ao trunk-based estrito)** — hierarquia de branches que a equipe **possui** e **mantém**:
  - **`feature/<nome-da-funcionalidade>`**: *uma* branch por funcionalidade, criada pela equipe; vive enquanto a funcionalidade está em desenvolvimento. É o **ponto de integração contínua do time**.
  - **`pr-<id>-<slug>`** (ex.: `pr-1234-ajuste-validacao-cota`): **efêmera** (vida ≤ 1 dia), aberta a partir da `feature/<funcionalidade>` correspondente; recebe o commit pequeno e atômico do desenvolvedor; integrada de volta à `feature/*` via PR assim que o CI verde permitir; deletada após o merge.

- **Fronteira de responsabilidade (regra inegociável)**: a equipe **só toca em branches que ela criou** — suas `feature/*` e suas `pr-*`. Nenhum agente da equipe está autorizado a:
  - Fazer commit, rebase, push ou merge em `develop`, `main`, `master`, `release/*`, `hotfix/*` ou em `feature/*` de outras equipes.
  - Resolver conflitos em branches alheias (escalar ao owner externo).
  - Mover a `feature/*` da equipe para `develop` — esse passo está em **outro fluxo / outra equipe / outro gate**, fora do escopo desta equipe.

- **Justificativa**: preserva o espírito do trunk-based (integração contínua, branch curtíssima, sem *long-lived* dentro do escopo do time) e simultaneamente cria um ponto de gate por PR (CI + code review). O mandato do Quality Engineer (estabilidade pós-merge **nas branches da equipe**) permanece inegociável.

- **Pré-commit hook + build local de 10 min máx** (Ten-Minute Build) executa **antes** do push para `pr-*`.

- **Pipeline (escopo do time)**: commit stage na `pr-*` (compile + unit + lint + SCA fast) → ao mergear em `feature/<funcionalidade>`, acceptance stage (component, integration, e2e, contract) → quality stages (perf smoke, security DAST, mutation) → deploy progressivo em ambiente de feature/preview com feature flags. **A integração `feature/*` → `develop` é um pipeline separado fora do escopo do time.**

### 1.7 Feature Flags como mecanismo de *dark launch*

- **Tipos**: release toggles (curtos, deletados após o release), experiment toggles (A/B), ops toggles (kill switch), permission toggles (entitlement).
- **Regras**:
  - Cada flag tem owner + data prevista de remoção.
  - Flag morta = dívida técnica; remover assim que possível.
  - Release toggles cobertos por teste de **ambos** os caminhos (on/off).
- **Ferramentas no ecossistema Java/Quarkus**: Unleash, Togglz, FF4j, LaunchDarkly.

### 1.8 Refactoring — catálogo essencial (Fowler 2ª ed.)

**Composição**: Extract Function, Inline Function, Extract Variable, Inline Variable, Change Function Declaration.

**Encapsulamento**: Encapsulate Record, Encapsulate Collection, Replace Primitive with Object, Replace Temp with Query.

**Hierarquia**: Pull Up Method/Field, Push Down, Replace Conditional with Polymorphism, Replace Type Code with Subclasses.

**Bad smells → refactoring** (lista curta): Long Method, Large Class, Long Parameter List, Divergent Change, Shotgun Surgery, Feature Envy, Data Clumps, Primitive Obsession, Switch Statements, Speculative Generality, Refused Bequest, Comments (que escondem código ruim).

**Regra-mãe**: mude o código em passos pequenos com testes verdes entre cada passo.

### 1.9 Modern Software Engineering (Farley)

Engenharia de software = **aprendizado** (científico, iterativo, empírico) + **gestão de complexidade** (modularidade, coesão, separação de concerns, abstração, baixo acoplamento).

- **5 técnicas de aprendizado**: iteração, feedback rápido, incremento, experimentação, empirismo.
- **5 técnicas de gestão de complexidade**: modularidade, coesão, separação de concerns (SoC), abstração, baixo acoplamento.

CD não é "ferramenta de deploy"; é a manifestação operacional dessas dez técnicas.

### 1.10 Métricas DORA (Forsgren, Humble & Kim — *Accelerate*)

**Throughput**:
- *Deployment Frequency* — com que frequência o time entrega em produção.
- *Lead Time for Changes* — do commit ao deploy em produção.

**Estabilidade**:
- *Change Failure Rate* (CFR) — % de mudanças que causam falha em produção.
- *Mean Time to Restore* (MTTR) — tempo para restaurar serviço após incidente.

**Bandas de performance** (referência):
| Banda  | Deploy Freq        | Lead Time | CFR     | MTTR   |
|--------|--------------------|-----------|---------|--------|
| Elite  | On-demand          | < 1h      | 0–15%   | < 1h   |
| High   | Diário–semanal     | < 1 dia   | 0–15%   | < 1 dia|
| Medium | Semanal–mensal     | 1d–1 mês  | 0–15%   | < 1 dia|
| Low    | Mensal–bimestral   | > 1 mês   | 16–30%  | > 1 dia|

**Quinta métrica** (DORA 2021+): *Reliability* (operacional — disponibilidade vs SLO).

**Capabilities que predizem performance** (resumo): trunk-based, continuous testing, deployment automation, monitoring/observability, security shifted left, lean management, *generative culture* (Westrum).

## 2. Práticas e heurísticas operacionais

### 2.1 Disciplina de commit via branch `pr-*` (integrada na `feature/*` do time)

- Commit pequeno e atômico (uma intenção); mensagem no imperativo curto; vincula a item Kanban.
- **Nascimento da `feature/*`**: criada **uma vez** pela equipe ao iniciar a funcionalidade, a partir do ponto que o processo externo definir (tipicamente um snapshot estável de `develop`). A partir daí, a `feature/*` é território exclusivo do time.
- **Nascimento da `pr-*`**: `git switch -c pr-<id-item>-<slug-curto>` a partir da `feature/<funcionalidade>` recém-puxada.
- **Nunca push com teste vermelho ou build local quebrado.**
- **Sequência obrigatória**: pull `feature/<funcionalidade>` → criar `pr-*` (se ainda não existe) → build local → testes → commit → push → CI verde na `pr-*` → abrir/atualizar PR (`pr-*` → `feature/*`) → merge em `feature/*` no mesmo dia.
- **Quebra no CI da `feature/*` após merge** = parar o mundo (*stop-the-line*): primeira prioridade do time é restaurar verde, com revert preferível a fix-forward quando demora > 10 min.
- Vida útil máxima de uma `pr-*`: 1 dia. Se passar disso, usar Branch by Abstraction + Feature Flag dentro da `feature/*` para integrar o que já existe e continuar incrementalmente.
- **Proibido**: qualquer operação (commit, push, rebase, merge) em branches que a equipe **não criou** — `develop`, `main`, `release/*`, `feature/*` de outras equipes. Escalar ao owner externo se a sincronização for necessária.

### 2.2 TDD na prática — anti-padrões comuns

- ❌ Escrever todos os testes antes de qualquer produção (não é TDD, é *test-first* em batch).
- ❌ *Test-after* pintado de TDD: implementação primeiro, teste depois.
- ❌ *Mock everything*: testes que só verificam que o mock foi chamado não validam comportamento.
- ❌ Asserts vagos (`assertTrue(result != null)`) — verifique o valor exato esperado.
- ✅ *Take small steps*: se está difícil escrever o teste, simplifique o design antes.
- ✅ Triangulação: dois ou três testes que forcem a generalização do código.

### 2.3 Pair / Mob — regras operacionais

- Driver foca no "como" (digitação, sintaxe); navigator no "o quê / próximo passo / qualidade do design".
- Rotação **compulsória** em pair (Pomodoro-like a cada 25–50 min ou a cada commit verde).
- Mob: rotação a cada 5–10 min (regra de Llewellyn Falco — *"if you have an idea, you must take the keyboard"*).
- Anti-padrão: *silent pair* — dois lendo em silêncio não é pair.
- Anti-padrão: *driver autônomo* — navigator vira espectador passivo.

### 2.4 CI + hierarquia `pr-*` → `feature/*` — regras de ouro

- "If integrating is hard, do it more often" — Beck. Dentro do escopo do time: integrar `pr-*` em `feature/*` no **mesmo dia**.
- Build de 10 min ou menos no commit stage da `pr-*`; se passar disso, paralelize ou divida.
- *Branch by Abstraction* + Feature Flags em vez de manter `pr-*` aberta por mais de 1 dia.
- **Pré-commit hooks**: format + lint + testes rápidos.
- **Merge de `pr-*` em `feature/*`** preferencialmente via *squash + rebase linear* (histórico limpo, 1 commit por unidade de valor); merge commit aceitável quando preserva contexto útil.
- Após merge, **deletar imediatamente** a branch `pr-*` (local + remoto).
- A `feature/*` em si **não é deletada pelo time**; sua entrega para `develop` está fora do escopo do time.

### 2.5 Refactoring contínuo

- *Boy Scout Rule*: deixe o código melhor do que encontrou.
- *Refactor first* antes de adicionar feature em código difícil (Mikado Method para mudanças grandes que exigem várias dependências).
- Refactor sempre com **testes verdes antes e depois**.
- **Nunca misturar refactor + feature no mesmo commit** — separa o sinal de revisão.

### 2.6 Métricas DORA — uso correto

- Ferramenta de **conversa**, não de gerência por números.
- Coletar por **time / serviço**, não por indivíduo.
- Tendência > valor pontual; comparar o time a si mesmo, não a outros times.
- Quando uma métrica piora, investigue a *capability* subjacente (ex.: lead time longo → falta de deployment automation? testes lentos? aprovação humana intermediária?).

## 3. Templates e checklists

### 3.1 Definition of Done (DoD) compatível com CI via `pr-*` → `feature/*`

- [ ] Funcionalidade coberta por testes próprios (unit + um nível acima quando aplicável).
- [ ] Build local de 10 min verde.
- [ ] Code review por pair (in-process) ou async no PR da branch `pr-*`.
- [ ] Sem regressão observável dentro da `feature/*` (smoke + fitness functions verdes).
- [ ] Feature flag presente se a `feature/*` puder ser promovida a `develop` antes do release.
- [ ] DMV atualizada (contrato OpenAPI/AsyncAPI, spec executável BDD, ADR leve ou Glossário) se mudou comportamento.
- [ ] Observabilidade instrumentada (log estruturado, métrica, trace OpenTelemetry).
- [ ] Pipeline CI verde na `pr-*` **e** verde na `feature/*` após o merge.
- [ ] Branch `pr-*` excluída pós-merge.
- [ ] Nenhuma mudança feita fora do escopo do time (nada em `develop`, `release/*` ou `feature/*` de terceiros).

### 3.2 Pre-push checklist (na branch `pr-*`)

1. Pull da `feature/<funcionalidade>`: `git pull --rebase origin feature/<funcionalidade>`.
2. Build + testes rápidos locais.
3. Lint / format.
4. Inspeção de diff: `git diff origin/feature/<funcionalidade>...HEAD`.
5. Commit + push para `pr-*`.
6. Aguardar CI verde na `pr-*` → revisão → merge em `feature/*` → confirmar CI verde na `feature/*` antes de abrir o próximo ciclo.

### 3.3 Pipeline anatomy — escopo do time

```
[commit em pr-*] ──► commit stage na pr-*  (compile + unit + lint + SCA fast)   ≤ 10 min
                    │
                    ▼ (PR merge: pr-* → feature/<funcionalidade>)
              acceptance stage na feature/*  (component + integration + e2e + contract)
                    │
                    ▼
              quality stages em paralelo na feature/*  (perf smoke, security DAST, mutation)
                    │
                    ▼
              deploy em ambiente de feature/preview com feature flags
                    │
                    ▼
              observability gates (golden signals, SLO budget)
                    │
                    ▼  ╔═══════════════════════════════════════════════╗
                       ║  feature/* → develop está FORA do escopo     ║
                       ║  do time (outro fluxo, outro owner, outro    ║
                       ║  gate). Equipe não toca.                     ║
                       ╚═══════════════════════════════════════════════╝
```

### 3.4 Template de mensagem de commit

```
<verbo no imperativo curto> <objeto> <[#item-kanban]>

<corpo opcional: por que, não o que — o diff mostra o que>
```

Exemplos:
- `Valida CPF na contratacao de cota [#1234]`
- `Adiciona feature flag fl-novo-rateio [#1240]`
- `Refatora ContratacaoService para Extract Function [#1212]`

## 4. Como esta skill é usada pelos agentes

Todos os papéis técnicos da equipe carregam esta skill **antes** das skills específicas para garantir vocabulário e disciplina de engenharia comuns.

- **Engineering Coach** é o owner explícito destas práticas (RACI A/R em "Práticas de Engenharia").
- **Quality Engineer** apoia-se no DoD daqui para o mandato de estabilidade pós-merge **nas branches da equipe** (`pr-*` e `feature/*`).
- **DevOps** materializa o pipeline em dois níveis (commit stage na `pr-*` + acceptance/quality/deploy stages na `feature/*`), respeitando que **nenhum job dispara em branches alheias**.
- **SRE** consome as métricas DORA junto com SLOs, medindo lead/throughput dentro do escopo do time (até o merge em `feature/*`).
- **Tech Lead, Arquitetos, Data Engineer, AppSec, API Designer** seguem a disciplina de `pr-*` → `feature/*` em todo trabalho técnico no código.

## References

Bibliografia da seção 3.0a do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Extreme Programming Explained* (2ª ed.) — Beck & Andres
- *The Art of Agile Development* (2ª ed.) — Shore & Warden
- *Modern Software Engineering* — Farley
- *Continuous Delivery* — Humble & Farley
- *Test-Driven Development by Example* — Beck
- *Refactoring* (2ª ed.) — Fowler
- *Accelerate* — Forsgren, Humble & Kim
- *Trunk-Based Development* — Hammant *(complementar para a variação de branches da equipe)*
