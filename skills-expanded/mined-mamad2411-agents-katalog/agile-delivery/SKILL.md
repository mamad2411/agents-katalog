---
name: agile-delivery
description: Entrega ágil do ponto de vista do PM — Scrum e Kanban na prática, planejamento por capacidade, forecast por vazão (Monte Carlo), métricas de fluxo, bugs e interrupções, dependências, retrospectiva e acordo PM ↔ tech lead. Use quando planejar sprint ou fluxo, responder pedidos de data sem prometer, ou diagnosticar um processo travado.
---

Antes de aplicar este pattern, leia também [`../user-stories/SKILL.md`](../user-stories/SKILL.md) (histórias, DoR/DoD, three amigos), [`../prioritization/SKILL.md`](../prioritization/SKILL.md), [`../product-roadmap/SKILL.md`](../product-roadmap/SKILL.md) e [`../stakeholder-communication/SKILL.md`](../stakeholder-communication/SKILL.md). O planejamento técnico e a estimativa são do agent `tech-lead`; a definição de pronto do pacote está em `user-stories`.

# Entrega ágil

**Agilidade** é a capacidade de **entregar valor em pequenos incrementos, aprender com o resultado e ajustar o rumo** — não um conjunto de cerimônias. Scrum e Kanban são **ferramentas** para isso. O papel do PM é manter o time apontado para o **resultado certo** (o quê e por quê) e **remover obstáculos**, deixando para a engenharia o **como**.

## 1. Valores práticos (o que importa de verdade)

- **Entregar valor em fatias pequenas e frequentes** (`user-stories`), não grandes lançamentos raros.
- **Feedback rápido**: ciclo curto entre ideia, uso real e aprendizado (`product-metrics`).
- **Time autônomo e responsável**: o time **decide como** cumprir o objetivo; o PM define **o problema e a prioridade**.
- **Transparência**: trabalho, bloqueios e riscos visíveis para todos.
- **Melhoria contínua**: inspecionar e adaptar o **próprio processo** (retrospectivas).
- **Sustentabilidade**: ritmo constante e **qualidade embutida** (testes, revisão — `testing`, `code-reviewer`); cortar qualidade para "ir mais rápido" cobra juros logo adiante.

## 2. Scrum em uma página

**Papéis:** **Product Owner (PO)** — dono do **backlog** e da **priorização** (o PM frequentemente exerce esse papel ou o acompanha de perto); **Scrum Master** — facilita o processo e remove impedimentos; **Developers** — o time (engenharia, QA, design) que **entrega o incremento**. O **`tech-lead`** orienta tecnicamente; **PM/PO ≠ tech lead**: um decide **o quê/por quê**, o outro **como/quando é viável**.

**Eventos** (sprint de 1–2 semanas costuma ser o melhor equilíbrio):
| Evento | Propósito | O PM faz |
|---|---|---|
| **Sprint Planning** | Escolher **o que** entra e **como** começar; definir o **Sprint Goal** | Traz **prioridade e objetivo**; esclarece dúvidas; **não impõe** a quantidade |
| **Daily** (15 min) | O **time** sincroniza o progresso rumo ao Sprint Goal e destrava impedimentos | Ouve; **não é reunião de status para o PM** |
| **Sprint Review** | **Demonstrar o resultado** a stakeholders e **coletar feedback** | Conduz a conversa de valor; ajusta o backlog com o que ouviu |
| **Retrospectiva** | O time **melhora o próprio processo** | Participa como membro, abre-se a feedback |
| **Backlog Refinement** (contínuo) | Deixar histórias **prontas para entrar** (DoR) | **Presente**: prioriza, explica o problema, ajuda a fatiar |

**Sprint Goal:** **uma frase** com o **objetivo de valor** da sprint ("**Sócios conseguem renovar um empréstimo simples pela web**") — não uma lista de tarefas. Ele dá **foco e flexibilidade**: se um item atrasar, o time negocia **escopo** para preservar o objetivo.

**O incremento** ao fim da sprint é **usável e "pronto"** conforme a **DoD** (`user-stories`) — **potencialmente lançável**, mesmo que a decisão de lançar seja separada (`release-management`).

## 3. Kanban — fluxo contínuo

Ideal para trabalho **de fluxo contínuo e imprevisível** (suporte, plataforma, manutenção) ou times que **não** funcionam bem em sprints:
- **Quadro** com colunas do **fluxo real** (Backlog → Refinado → Em desenvolvimento → Em revisão → Em teste → Pronto → Em produção).
- **Limite de trabalho em andamento (WIP)** por coluna: **pare de começar, comece a terminar.** Muito trabalho simultâneo **aumenta o tempo de entrega** e esconde gargalos.
- **Políticas explícitas** (o que significa "pronto" para sair de cada coluna).
- **Puxe** trabalho quando há capacidade, em vez de empurrar.
- **Gerencie o fluxo** com as métricas da seção 5.
Muitos times usam **Scrumban** (cadência de planejamento do Scrum + WIP/fluxo do Kanban). Escolha pelo **tipo de trabalho**, não por moda.

## 4. Refinamento e planejamento

**Refinamento** (30–60 min/semana, contínuo): PM + `tech-lead` + QA (+ design) **preparam o backlog** — **esclarecem o problema, escrevem critérios de aceite, fatiam** as grandes e **identificam dependências e riscos** (`user-stories`). Mantenha **2 sprints de histórias prontas** à frente (nem mais — muito refinamento antecipado envelhece e é desperdício).

**Planejamento por capacidade (não por desejo):**
1. Sabe-se a **capacidade** real (pessoas disponíveis, férias, reuniões, **reserva para bugs/incidentes e dívida técnica** — `prioritization`).
2. O **time puxa** os itens de maior prioridade **que cabem**; o PM **não aumenta a carga** na sprint em andamento ("só mais um item").
3. Defina o **Sprint Goal** e **o que NÃO entra**.
4. **Dependências** externas travadas **antes** de a história entrar.

### Estimar sem se enganar

- **Estimativa é previsão, não compromisso**, e **incerta**: use **intervalos** ou tamanhos relativos (**P/M/G**, ou pontos) e declare a incerteza (`tech-lead` entrega "G, ±50%, depende do spike X").
- **Story points** medem **tamanho/complexidade relativos**, **não tempo**; servem **para o time** planejar a sprint — **não** para comparar times, medir produtividade ou virar meta (**lei de Goodhart**: quando a medida vira meta, deixa de ser boa medida).
- **Forecast baseado em dados é melhor que estimativa por opinião**: com o **histórico de vazão** (throughput: itens concluídos por semana) calcule **probabilidades**. Ex.: *"nas últimas 12 semanas o time concluiu entre 4 e 9 itens/semana; para 30 itens restantes, **85% de chance de terminar em ≤ 8 semanas**"* — via **simulação de Monte Carlo** (simula milhares de futuros a partir do histórico). Entregue **faixas e probabilidades**, **não** uma data única (`product-roadmap`: pedidos de data).
- **Itens menores e de tamanho parecido** tornam o forecast **muito mais previsível** que estimar cada um: **fatie pequeno** (`user-stories`) e "contar itens" já funciona bem (*no estimates* por contagem).
- **Estimar não é negociar**: o PM não "espreme" a estimativa; negocia **escopo**.

## 5. Métricas de fluxo (saúde do processo, não "produtividade")

| Métrica | O que é | Para que serve |
|---|---|---|
| **Lead time** | Da **ideia/pedido** até **em produção** | O tempo que o **cliente** espera |
| **Cycle time** | Do **início do trabalho** até **pronto** | A **velocidade do time**; use **percentis** (ex.: **85% dos itens em ≤ 6 dias**) |
| **Throughput** | Itens concluídos por período | Base do **forecast** |
| **WIP** | Itens **em andamento** | Excesso = fila e atraso |
| **Idade do item (aging)** | Há quanto tempo está em andamento | Detecta itens **travados** antes de estourar |
| **Taxa de defeitos / retrabalho** | Bugs escapados, itens que voltam | Qualidade embutida |

**Lei de Little:** `Cycle time médio ≈ WIP / Throughput` — **reduzir o WIP reduz o tempo de entrega** (sem trabalhar mais rápido). **Use métricas para melhorar o sistema, nunca para avaliar pessoas.** Medir indivíduos gera manipulação e destrói a colaboração. Complemente com as métricas **DORA** de entrega (frequência de deploy, lead time de mudança, taxa de falha de mudança, tempo de restauração — `github-actions-aws`, `argocd`, `observability`): times que entregam **pequeno e frequente** com **qualidade** têm menos falhas, não mais.

## 6. Dupla trilha: descoberta e entrega

(`product-discovery`) Enquanto a engenharia **entrega o que já foi validado**, PM + design + um engenheiro **descobrem o próximo**:
```
Trilha de DESCOBERTA:  entrevistas → hipóteses → protótipos/experimentos → decisão (seguir/ajustar/parar)
                                                                │ (só o que foi validado entra)
Trilha de ENTREGA:    refinamento → desenvolvimento → teste → lançamento gradual → medição
```
**O backlog de entrega só recebe itens com hipótese validada e critérios claros.** Reserve **capacidade** para descoberta (`prioritization`) — sem isso o time vira *feature factory*.

## 7. Bugs, interrupções e trabalho não planejado

Interrupções **sempre existem** (bugs de produção, incidentes, pedidos urgentes). **Planeje-as**, não as ignore:
- **Reserve capacidade** (buffer) para o imprevisto.
- **Classifique por severidade** com critérios **claros e acordados** (`P1` = produção fora/perda de dados → **para tudo**; `P2` = impacto relevante, na sprint; `P3` = backlog priorizado). **Nem todo bug é urgente.**
- **Um canal único de entrada** (sem pedidos "por fora" direto ao desenvolvedor); o PM **triage**.
- **Rotação de "plantão/suporte"** no time para proteger o foco dos demais.
- **Incidentes** têm processo próprio (comunicação, post-mortem — `stakeholder-communication`, `observability`); as **ações do post-mortem** viram itens **priorizados** no backlog (senão se repete).
- **Meça o volume** de trabalho não planejado: se passa de ~20–30% consistentemente, é **sinal** (qualidade, dívida técnica, estabilidade) a tratar — e a conversa de capacidade (`technical-product-management`).

## 8. Dependências

Em arquiteturas de vários serviços/times (`microservices`), **dependências** são a causa nº 1 de atraso:
- **Mapeie cedo** (no refinamento e no planejamento trimestral — `product-roadmap`): de quem dependemos, de quê, para quando.
- **Reduza-as pelo design**: **contratos explícitos** (`contract-testing`), **fatias verticais** que o time entrega sozinho, **fronteiras alinhadas aos times** (`microservices`).
- **Combine contratos antes de codar**: com o time vizinho, defina a API/evento e use **stub/mock** até o real existir.
- **Faça o risco visível** (quadro de dependências, "bloqueado por X", **idade** do bloqueio) e **escale cedo** (`stakeholder-communication`).

## 9. Retrospectiva

O motor da melhoria. Formato simples (60 min): **o que foi bem · o que não foi · o que tentaremos** → **1–3 ações** com **dono e prazo**, **revisadas na retro seguinte**. Regras: **segurança psicológica** (sem culpa), **foco no processo/sistema**, **ações concretas e poucas**, **acompanhamento** (retro sem follow-up vira reclamação). Varie o formato quando cansar; use **dados** (métricas de fluxo, incidentes) como insumo. O PM **participa como membro**, aceita feedback sobre a **qualidade do seu refinamento** e do **contexto** que entrega.

## 10. Acordo de trabalho PM ↔ Tech Lead (a parceria central)

| PM | Tech Lead |
|---|---|
| **O quê e por quê**: problema, valor, prioridade, critérios de aceite | **Como e quão difícil**: arquitetura, riscos técnicos, estimativa, qualidade |
| Dono do **backlog** e do **resultado** | Dono da **saúde técnica** e do **plano de entrega** |
| Traz **contexto de negócio e do usuário** | Traz **restrições técnicas e alternativas mais baratas** |
| Negocia **escopo** com stakeholders | **Protege a qualidade** e a sustentabilidade do ritmo |

**Combinem explicitamente:** como as **prioridades** mudam (e quem pode mudar durante a sprint — idealmente ninguém, salvo P1), a **DoR/DoD**, a **reserva de capacidade** para dívida técnica, como tratam **estimativas** (intervalos, sem pressão), como **decidem escopo vs prazo**, e a **cadência de conversa** (um 1:1 curto semanal). **Quando discordam**, levam **evidência** e, se preciso, escalam **juntos** com as opções. O PM **não** decide solução técnica; o tech lead **não** decide o valor.

## 11. Anti-patterns

- **Scrum-but**: cerimônias sem os princípios (daily como status ao chefe, retro sem ação, sprint goal inexistente).
- **Velocity/pontos como meta ou comparação entre times** (Goodhart); **medir pessoas** com métricas de fluxo.
- **PM empurrando itens para dentro da sprint** ("só mais um"); **mudar o escopo no meio** sem negociação.
- **Mini-waterfall**: design numa sprint, dev na outra, teste na seguinte (fatias horizontais — `user-stories`).
- **Backlog gigante e velho**; **refinamento só no dia do planejamento**.
- **WIP alto** ("todo mundo em tudo") e itens parados por semanas sem ninguém notar.
- **Estimar como compromisso**, ou pressionar para "encaixar".
- **Ignorar capacidade** para dívida técnica, bugs e incidentes (a velocidade cai até parar).
- **Sem Sprint Goal** (só uma lista de tarefas); **sem demonstração** (review vira slide).
- **Descoberta e entrega misturadas** (construir antes de validar).
- **Dependências descobertas na sprint** (não mapeadas no refinamento).

---

## Regras principais

- **Agilidade = pequenos incrementos de valor + feedback + ajuste**; Scrum/Kanban são ferramentas — escolha pelo **tipo de trabalho** (Scrum para entrega de produto; Kanban para fluxo contínuo; Scrumban misto).
- **Sprint Goal** é uma frase de **valor**, não lista de tarefas; **o time puxa** o que cabe na **capacidade real** (com buffer para bugs/dívida); **o PM não empurra** itens.
- **Refinamento contínuo** com PM + tech lead + QA: histórias **prontas (DoR)**, critérios de aceite, fatiadas, dependências mapeadas; ~2 sprints à frente.
- **Estimativa é previsão incerta**: intervalos/P-M-G, **pontos não medem produtividade nem são meta**; prefira **forecast por vazão (Monte Carlo)** com **faixas e probabilidades**; itens **pequenos** tornam tudo mais previsível; **negocie escopo, não estimativa**.
- **Métricas de fluxo** (lead/cycle time com percentis, throughput, WIP, aging, defeitos) para melhorar **o sistema**, **nunca avaliar pessoas**; **reduzir WIP** reduz o tempo de entrega (Lei de Little); acompanhe também **DORA**.
- **Dupla trilha**: só entra no backlog de entrega o que foi **validado** (`product-discovery`); reserve capacidade para descoberta.
- **Interrupções existem**: buffer, severidade clara (P1/P2/P3), canal único, rotação de suporte, **ações de post-mortem priorizadas**.
- **Dependências**: mapear cedo, reduzir por design (contratos, fatias verticais), combinar contrato antes de codar, escalar cedo.
- **Retrospectiva** com 1–3 ações (dono e prazo) **acompanhadas**; segurança psicológica; foco no sistema.
- **Parceria PM ↔ tech lead**: o PM define **o quê/por quê**, o tech lead **como/viabilidade e saúde técnica**; acordos explícitos de prioridade, DoR/DoD, capacidade para dívida e estimativa.
- **Sem Lombok** — deliberado (skill de produto, sem código).
