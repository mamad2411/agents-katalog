---
name: technical-product-management
description: PM técnico para APIs e plataformas — NFRs com números, SLI/SLO/SLA e error budget, API como produto, dívida técnica como decisão de produto, build × buy, FinOps e custo por transação, leitura de ADRs e a fronteira entre PM e engenharia. Use quando definir requisitos não funcionais ou negociar confiabilidade × funcionalidades.
---

Antes de aplicar este pattern, leia também [`../prd-writing/SKILL.md`](../prd-writing/SKILL.md), [`../prioritization/SKILL.md`](../prioritization/SKILL.md), [`../product-metrics/SKILL.md`](../product-metrics/SKILL.md), [`../release-management/SKILL.md`](../release-management/SKILL.md) e as skills técnicas citadas ao longo do texto — o PM **não precisa dominá-las**, mas precisa **entender o suficiente** para fazer as perguntas certas: `microservices`, `observability`, `resilience`, `idempotency`, `service-communication`, `aws-observability`.

# PM técnico

Em produtos de **backend, APIs e plataforma**, grande parte do valor (e do risco) está no que o usuário **não vê**: **confiabilidade, desempenho, segurança, custo, contratos entre serviços**. O PM técnico **não escreve o código nem decide a arquitetura** (`tech-lead`/`architect`), mas **traduz requisitos de negócio em requisitos técnicos mensuráveis**, **entende os trade-offs** e **prioriza trabalho invisível** com a mesma seriedade do visível.

> **Papéis:** o PM define **o quê, por quê e quão bom** (requisitos, metas, prioridade); a engenharia define **como** (arquitetura, tecnologia). **Pergunte e questione, não decida a solução técnica.** E **nunca invente números**: SLOs, custos e capacidade vêm de **medição ou de decisão explícita**, não de chute.

## 1. Requisitos não funcionais (NFRs) são requisitos de produto

"Rápido", "seguro", "disponível" **não são requisitos**; **números e condições** são. Para **cada** funcionalidade crítica, o PRD deve trazer (`prd-writing`, seção 6) — **conversando com o `tech-lead`** sobre o que é viável e a que custo:
| Categoria | Pergunta de negócio | Como expressar (exemplo) |
|---|---|---|
| **Desempenho** | Quanto o usuário **tolera esperar**? | "p95 < 300 ms com 200 req/s" (percentil, carga, condição) |
| **Disponibilidade** | Quanto custa **ficar fora do ar**? | "99,9% mensal" (≈ 43 min de indisponibilidade/mês) |
| **Capacidade/escala** | Qual **pico** esperamos e **crescimento**? | "2.000 renovações/hora no pico; 3× em 12 meses" |
| **Durabilidade/dados** | Quanto de dado podemos perder / quanto tempo para restaurar? | **RPO** (perda máxima: "≤ 5 min") e **RTO** (recuperação: "≤ 1 h") |
| **Segurança** | Que dados e quem acessa? Qual a regulação? | "Só o titular acessa seus dados; autenticação forte para admin; logs de auditoria 1 ano" |
| **Privacidade** | Que dados pessoais, base legal, retenção? | Veja `privacy-lgpd` |
| **Observabilidade** | Como saberemos que **quebrou**? | "Alerta em 5xx > 1% por 5 min; dashboard por serviço" (`observability`) |
| **Compatibilidade** | Quem **não pode quebrar**? | "APIs `v1` mantidas por 12 meses" (`release-management`) |
| **Acessibilidade/i18n** | Para quem e em que idiomas? | "WCAG 2.1 AA; pt-BR e en" |

**A conta da disponibilidade (importa para negociar):**
| SLO | Indisponibilidade/mês (~30 dias) | Custo típico |
|---|---|---|
| 99% | ~7 h 12 min | Baixo |
| 99,9% | ~43 min | Médio (multi-AZ, redundância) |
| 99,99% | ~4 min | **Alto** (multi-região, automação, on-call forte) |

Cada **"9" a mais custa muito mais** e pode exigir **mudar a arquitetura**. **Não peça 99,99% por reflexo**: pergunte **quanto realmente custa uma hora fora do ar** e escolha o **nível suficiente**. Cadeias síncronas **multiplicam** disponibilidade (`microservices`: 4 serviços a 99,9% ≈ 99,6%).

## 2. SLI, SLO, SLA e error budget

- **SLI** (indicador): a métrica medida (ex.: proporção de requisições com sucesso e < 500 ms).
- **SLO** (objetivo): a **meta interna** do SLI (99,9% em 30 dias).
- **SLA** (acordo): o **compromisso contratual** com o cliente, **com consequências** (créditos) — **mais frouxo** que o SLO interno.
- **Error budget** (orçamento de erro) = `100% − SLO`: **quanto de falha é aceitável** no período (99,9% → 0,1% ≈ 43 min). **É uma ferramenta de decisão de produto:**
  - **Orçamento sobrando** → o time pode **lançar mais rápido e correr riscos**.
  - **Orçamento esgotado** → **congela features novas** e prioriza **confiabilidade** até recuperar.
  Isso transforma a eterna disputa "features × estabilidade" em uma **regra objetiva e acordada** entre PM e engenharia, em vez de uma briga de opinião (`prioritization`). **Combine a política antes** do primeiro incidente.
Os SLIs vêm do que o **usuário percebe** (disponibilidade e latência no ponto de entrada — `observability`, `aws-observability`), não do uso de CPU. O PM **olha o mesmo dashboard de SLO** que a engenharia.

## 3. API como produto

Quando o "cliente" é **outro time ou um parceiro** que consome sua API/serviço (`service-communication`), **trate a API como um produto**:
| Prática | Em concreto |
|---|---|
| **Conheça os consumidores** | Quem usa? Para quê? Quanto? (métricas de uso **por consumidor**; contratos — `contract-testing`) |
| **Experiência do desenvolvedor (DX)** | **Documentação** clara e atual (`swagger`/OpenAPI), exemplos, **ambiente de teste/sandbox**, mensagens de erro úteis (`exception-handling`), tempo até a **primeira chamada** com sucesso |
| **Contrato estável** | **Mudanças aditivas**; quebra = **nova versão** com convivência; **política de deprecação publicada** (`release-management`, seção 8) |
| **Qualidade prometida** | **SLO/SLA** documentados (latência, disponibilidade, limites de taxa — `api-gateway`) |
| **Suporte e comunicação** | Canal para consumidores, **changelog**, avisos de manutenção/incidente |
| **Governança leve** | Padrões comuns (erros, paginação, autenticação, idempotência — `idempotency`) para APIs **consistentes** |
| **Métricas do produto-API** | Adoção (consumidores ativos), **tempo até a 1ª chamada**, taxa de erro por consumidor, uso por endpoint, **tickets de suporte** |

Uma API **difícil de usar, mal documentada ou que quebra sem aviso** gera **custo de suporte** e **perda de confiança**, mesmo "funcionando".

## 4. Dívida técnica é uma decisão de produto

**Dívida técnica** (atalhos que aceleram hoje e **cobram juros** amanhã — código difícil de mudar, testes ausentes, plataformas desatualizadas, arquitetura que não acompanha) **não é "capricho de engenheiro"**: é **dinheiro e velocidade**. Ignorá-la **desacelera** cada entrega futura até o time parar; pagá-la sem critério vira **refatoração infinita**. Trate-a como **qualquer outra aposta de produto**:
- **Torne-a visível e quantificada** pelo `tech-lead`: *"O módulo X faz cada mudança levar 3× mais; 40% dos bugs vêm dele"* — o **custo atual (juros)** e o **custo de pagar**. Use **dados** (cycle time por área, taxa de defeitos, incidentes — `agile-delivery`).
- **Priorize pelo retorno**: *(juros evitados + risco reduzido) ÷ custo de pagar* (`prioritization`: custo de atraso). **Atualização de segurança, plataformas fora de suporte e riscos de incidente** têm **prazo** (custo de atraso alto) e **entram como obrigação**.
- **Reserve capacidade fixa** (`prioritization`, seção 3) em vez de brigar a cada sprint; e **pague em fatias pequenas junto das features** ("deixe a trilha mais limpa do que encontrou") quando possível.
- **Não esconda** dívida **deliberada**: quando se escolhe um atalho para **lançar no prazo**, **registre** (item de backlog, com dono) — dívida **consciente e registrada** é ferramenta; **inconsciente** é risco.
- **Evite a falsa dicotomia** "feature **ou** qualidade": qualidade **embutida** (testes, revisão — `testing`, `code-reviewer`) é o que **mantém** a velocidade (`agile-delivery`).

## 5. Build × Buy × Open source

Decisão **de produto e de engenharia** juntas (`architect` — ADR):
| Opção | Quando | Custos ocultos |
|---|---|---|
| **Build** (construir) | É **diferencial competitivo**/núcleo do negócio; nada pronto atende | Manutenção **para sempre**, equipe, *time-to-market* mais lento |
| **Buy** (comprar SaaS/serviço gerenciado) | **Não** é diferencial (e-mail, pagamento, identidade — `aws-ses`, `aws-cognito`); rapidez importa | **Custo recorrente** (cresce com o uso), **lock-in**, limites de customização, dependência do fornecedor |
| **Open source** | Há solução madura e a equipe sabe operá-la | **Operação, segurança, atualizações** por sua conta; *bus factor* |

**Pergunte:** isto é **diferencial**? **TCO** (custo total em 3 anos: licença + operação + pessoas)? **Quão difícil sair** (lock-in)? **Risco** (fornecedor some/muda preço)? **Segurança/LGPD** (onde ficam os dados — `privacy-lgpd`)? **Regra:** **construa o que diferencia, compre o que é commodity**. Prefira **serviços gerenciados** (RDS, SQS, Cognito) a operar infraestrutura própria **quando não é seu negócio** — com os olhos abertos para o **custo** e o **lock-in**.

## 6. Custo de nuvem (FinOps) como métrica de produto

Em nuvem, **cada decisão de produto tem custo recorrente variável**. O PM precisa **enxergar** isso:
- **Custo por unidade de valor**: **custo por transação / por usuário ativo / por cliente** — a métrica que diz se o **negócio escala com lucro** (`aws-observability`, tags de custo — `aws-terraform`).
- **Funcionalidades têm custo operacional**: notificação por SMS, armazenamento de arquivos, chamadas a APIs pagas, **logs retidos** (`aws-observability`), consultas pesadas. Pergunte **"quanto custa isto por 1.000 usos?"** antes de aprovar (e **inclua no business case** — `product-strategy`).
- **Tags de custo** por produto/ambiente/time (a engenharia faz — `aws-terraform`) para **atribuir** custo; **alertas de orçamento** (AWS Budgets).
- **Trade-offs reais**: disponibilidade (multi-AZ/região), latência (cache), retenção de dados e **desempenho** custam dinheiro — **escolha o nível suficiente** para o requisito do usuário (seção 1), **não o máximo**.
- **Otimização é trabalho priorizado** (rightsizing, Spot, retenção de log, desligar ambientes ociosos — `aws-eks`, `aws-ecs-fargate`) com **retorno medido** — e não "quando sobrar tempo".

## 7. Ler e participar de decisões de arquitetura

O PM **não decide** a arquitetura, mas **deve entender o suficiente para opinar sobre o impacto no produto**:
- **ADR** (`architect`): leia o **contexto, as alternativas e as consequências**. Pergunte: **"qual o impacto para o usuário e para o prazo?"**, **"o que isso nos impede de fazer?"**, **"como revertemos se errarmos?"**, **"qual o custo recorrente?"**.
- **Aprenda o vocabulário e os trade-offs essenciais** (as skills `microservices`, `messaging`, `resilience`, `saga-pattern`… explicam cada um): **consistência eventual** (o usuário vê um estado intermediário — impacta UX e requisitos), **acoplamento** (mudança num serviço quebra outros?), **escala × custo**, **segurança × atrito**.
- **Entenda a complexidade escondida** de pedidos "simples": "só adicionar um campo" pode atravessar **3 serviços, contratos e migrações** (`contract-testing`, `flyway-migrations`) — **respeite a estimativa** e **negocie escopo**, não a pressione.
- **Peça opções, não soluções**: "preciso que o aviso chegue em até 1 h; o que você sugere e a que custo?" — deixa a engenharia propor **a mais simples que atende**.
- **Preste atenção em decisões irreversíveis ("one-way doors")** (banco de dados, provedor de identidade, contratos públicos): vale **mais tempo e evidência**; as **reversíveis ("two-way doors")** pedem **velocidade**.

## 8. Dependências entre times e a lei de Conway

Em arquiteturas distribuídas, **a estrutura dos times molda a dos sistemas** (e vice-versa — `microservices`). O PM técnico:
- **Alinha fronteiras de produto com fronteiras de serviço/time** (um time **dono** de uma capacidade, de ponta a ponta) para **reduzir dependências**.
- **Mapeia dependências** cedo (`agile-delivery`, `product-roadmap`) e **negocia contratos** entre times **antes** de construir.
- **Evita ser o "roteador" de pedidos** entre times: promove **interfaces claras** (APIs, contratos) e **donos explícitos**.
- **Reconhece trabalho de plataforma** (a "golden path" que acelera todos os times — `scaffold`, `kubernetes`) como **produto interno**, com **clientes internos**, métricas (tempo para o primeiro deploy) e roadmap.

## 9. Incidentes e confiabilidade

- **Participe dos post-mortems** (sem culpa): entenda **causas sistêmicas** e **priorize as ações** resultantes no backlog (`agile-delivery`) — post-mortem sem ação priorizada **se repete**.
- **Comunicação com clientes** durante incidentes é **papel do PM com suporte** (`stakeholder-communication`): honesta, frequente, sem especulação.
- **Defina severidade e impacto de negócio** com a engenharia (o que é P1?), para **priorizar** corretamente a resposta.
- **Use o error budget** (seção 2) para **decidir** entre features e confiabilidade.

## 10. Perguntas que o PM técnico faz (cola rápida)

**Ao receber uma proposta técnica:** Qual o **problema do usuário/negócio** que resolve? Quais as **alternativas** (incluindo "não fazer" e "a mais simples")? **Quanto custa** (construir **e** operar)? **Como medimos** que funcionou? **E se der errado**, como revertemos? O que **fica mais difícil** depois?
**Ao definir um requisito:** Qual o **número** (latência, disponibilidade, volume)? **Quanto custa** um nível acima? **Quem consome** e o que acontece a eles se quebrar? **Que dados pessoais** estão envolvidos?
**Ao priorizar trabalho invisível:** Qual o **custo de atraso**? Qual o **risco** se não fizermos? **Que dado** mostra o impacto (incidentes, tempo de ciclo, custo)?

## 11. Anti-patterns

- **Requisitos "rápido/seguro/disponível"** sem número; pedir **99,99%** sem custo de oportunidade.
- **Decidir a solução técnica** (invadir o papel do tech lead/architect) — ou o inverso, a engenharia decidir o valor.
- **Tratar dívida técnica como "capricho"** (ou como "tudo urgente"); **esconder** atalhos deliberados.
- **Ignorar custo de nuvem** até a fatura chegar; aprovar funcionalidades sem estimar custo por uso.
- **API sem documentação/versionamento/deprecação**; desligar versão sem avisar consumidores.
- **Pressionar estimativas** em vez de negociar escopo; subestimar a complexidade "escondida".
- **Features × confiabilidade como disputa de opinião** (sem error budget acordado).
- **Build por vaidade** (o que é commodity) ou **buy sem considerar lock-in e custo recorrente**.
- **PM roteador** entre times, sem contratos nem donos claros.
- **Post-mortem sem ações priorizadas**.
- **Inventar números técnicos** (SLO, capacidade, custo) em vez de medir/decidir.

---

## Regras principais

- **NFRs são requisitos de produto**: **números e condições** (p95, SLO, RPO/RTO, pico, retenção), negociados com o tech lead **sabendo o custo** de cada nível; **cada "9" custa muito mais** — peça o **suficiente**, não o máximo.
- **SLI/SLO/SLA e error budget**: o orçamento de erro **decide features × confiabilidade** com regra acordada **antes** do incidente; SLIs do que o **usuário percebe**.
- **API é produto**: conheça os consumidores, **DX e documentação**, contrato **estável e versionado**, **SLO/SLA publicados**, **deprecação com aviso**, métricas de adoção e suporte.
- **Dívida técnica é decisão de produto**: **visível e quantificada**, priorizada por **retorno e custo de atraso**, com **capacidade reservada**; atalhos deliberados **registrados**; qualidade embutida mantém a velocidade.
- **Build × buy × open source**: construa o **diferencial**, compre a **commodity**; considere **TCO, lock-in, segurança/LGPD** e a **operação** de cada opção.
- **Custo de nuvem é métrica de produto**: **custo por transação/usuário**, estimar **custo por uso** de cada feature, tags e alertas de orçamento, otimização priorizada.
- **Leia ADRs** e pergunte pelo **impacto no usuário, no prazo, no custo e na reversibilidade**; peça **opções, não soluções**; respeite a complexidade escondida; **one-way vs two-way doors**.
- **Alinhe fronteiras de produto, serviço e time** (Conway); contratos e donos claros; plataforma como **produto interno**.
- **Post-mortem sem culpa com ações priorizadas**; comunicação de incidente honesta.
- **Nunca invente números técnicos**; **o PM define o quê/por quê/quão bom, a engenharia define o como**.
- **Sem Lombok** — deliberado (skill de produto, sem código).
