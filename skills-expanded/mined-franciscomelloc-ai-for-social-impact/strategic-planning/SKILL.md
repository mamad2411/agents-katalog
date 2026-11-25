---
name: strategic-planning
description: Facilita planejamento estratégico multi-horizonte (H1/H2/H3) e derivação de KPIs/OPIs com árvore de valor e plano de governança. Para OSCs e governos com objetivos amplos a aterrissar em indicadores rastreáveis.
---

# Planejamento Estratégico e Indicadores

## Quando usar esta skill

Esta skill apoia o trabalho de planejamento estratégico e definição de indicadores em organizações de impacto social — OSCs, governos, coletivos organizados — quando a decisão precisa ser ancorada em critérios transparentes e monitorada por indicadores rastreáveis, não em intuição.

- **Construir ou revisar planejamento estratégico** de 12/24/36 meses com método de 3 horizontes (H1/H2/H3)
- **Priorizar iniciativas** por critério único transparente e ponderado, com equidade embutida
- **Definir KPIs estratégicos e OPIs operacionais** a partir de objetivos aprovados
- **Construir árvore de valor** mostrando drivers controláveis, influenciáveis e observáveis de cada objetivo
- **Produzir plano de mensuração e governança** (fontes, frequência, responsáveis, riscos de viés, mitigação)
- **Traduzir resultados esperados de uma teoria da mudança** em indicadores rastreáveis

Sinais típicos na conversa do usuário:

- "Nosso plano estratégico acabou, precisamos definir o próximo ciclo"
- "Temos 8 ideias novas e não sabemos quais priorizar"
- "Preciso reportar KPIs pro financiador e não sei o que medir"
- "Como transformar objetivos amplos em indicadores rastreáveis?"
- "Quero montar um Mapa H1–H2–H3 pro próximo ciclo"
- "Tenho o planejamento aprovado, falta definir os indicadores"
- "Preciso de uma árvore de valor pra cada objetivo"

A skill tem **dois pontos de entrada**:

- **Modo full (9 etapas)** — equipe começa do zero ou revisa planejamento; executa planejamento (Etapas 1–4) e depois derivação de indicadores (Etapas 5–9)
- **Modo só-indicadores (5 etapas)** — equipe já tem 3–5 objetivos estratégicos aprovados e quer derivar KPIs/OPIs; pula as Etapas 1–4 e entra direto na Etapa 5 com uma Etapa 1' reduzida

Relação com outras skills do repositório:

- Use `theory-of-change` antes desta skill quando você precisa construir a teoria da mudança primeiro; depois invoque `strategic-planning` no modo só-indicadores passando os resultados finais da ToC como objetivos aprovados
- Use `evidence-synthesis` ou `evidence-gathering` antes desta skill quando você precisa consolidar o diagnóstico que alimenta o inventário da Etapa 2
- Use `project-structuring` **depois** desta skill pra transformar iniciativas priorizadas em entregáveis, cronograma e recursos
- `qualitative-analysis` pode alimentar a Etapa 1 (compreensão qualitativa de necessidades dos grupos vulneráveis) e a Etapa 8 (fontes qualitativas de dados pra indicadores)

## Pré-requisitos

Antes de começar, o usuário precisa ter:

**Para qualquer modo:**

1. **Missão ou mandato institucional** — 1 parágrafo claro. Se a organização não tem missão escrita, escrever uma versão de trabalho antes de invocar a skill.
2. **Público prioritário específico** — quem a organização serve, com quem trabalha. **Não** usar "beneficiários" genérico; nomear o público com especificidade ("mulheres em situação de violência doméstica nos territórios X", "jovens de 15–24 anos fora da escola no quilombo Y", "servidores da atenção básica de municípios até 50 mil habitantes").
3. **Grupos vulneráveis concretos** — lista de grupos em situação de vulnerabilidade relevantes ao contexto, com nomes concretos ("jovens negros fora da escola", "mães adolescentes", "pessoas com deficiência visual", "usuárias da ESF em bairros sem agente comunitário"). Não "vozes diversas" nem "grupos minoritários" genérico.
4. **Restrições inegociáveis** — legais (marco regulatório aplicável), orçamentárias (teto, limites), éticas (princípios do conselho ou missão).
5. **Tempo para validação humana** — a skill produz rascunhos; a qualidade final depende de revisão humana em **3 a 4 checkpoints obrigatórios** durante o workflow, dependendo do modo.

**Modo full (9 etapas) adicionalmente:**

6. **Lista inicial de iniciativas** — até 12 iniciativas candidatas (nomes curtos) OU, se não houver iniciativas ainda, descrição de 3 problemas/oportunidades prioritários
7. **Ordem de grandeza do orçamento** — não precisa ser o orçamento final, só a magnitude (ex: "~R$ 500 mil/ano", "~R$ 5 milhões/ano")
8. **Janela do próximo ciclo de planejamento** — quando começa o próximo exercício / plano plurianual / ciclo programático

**Modo só-indicadores (5 etapas) adicionalmente:**

6. **3 a 5 objetivos estratégicos já aprovados** pela equipe, liderança ou conselho
7. **Fonte dos objetivos** — planejamento anterior, resultados finais de uma `theory-of-change`, deliberação de conselho, edital aprovado, etc. A skill aceita objetivos de qualquer fonte mas exige saber de onde vieram

Se algum desses elementos não está pronto, a skill **pergunta antes de avançar** — não inventa silenciosamente.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas da skill, nos dois modos. Não negocie.

1. **A skill facilita, não decide.** Priorização final, validação de KPIs, aprovação do Mapa H1–H2–H3 e validação da árvore de valor são responsabilidades humanas explícitas. A IA acelera preparação e sistematização; a deliberação é da equipe/liderança. A skill nunca produz plano "pronto pra aprovar automaticamente".

2. **Equidade é critério ponderado de priorização, não disclaimer.** Na Etapa 1, a skill propõe default com Equidade 20% no critério único de priorização. **Piso recomendado: 15%.** O usuário pode ajustar o peso, mas qualquer valor abaixo de 15% (ou "Equidade = 0%") gera alerta explícito da skill (não bloqueia — a responsabilidade é humana, mas a decisão precisa ser registrada com justificativa). Grupos vulneráveis são nomeados **antes** de qualquer discussão de horizontes. **Este princípio é específico desta skill.**

3. **"Não encontrado" e `[suposição]` explícitos.** Quando faltar evidência pra classificar iniciativa ou sustentar indicador, marcar literalmente "não encontrado". Quando precisar prosseguir com inferência, marcar `[suposição]` com justificativa curta (1 frase). Padrão do repositório.

4. **Toda iniciativa descartada gera pergunta "quem deixa de ser atendido?".** Registro obrigatório no log de decisões da sub-etapa 3c. Impede descartes que aumentam desigualdades silenciosamente. Cada linha do log identifica a iniciativa descartada, quem fica sem serviço, e o risco de aumento de desigualdade (sim/não/incerto). **Este princípio é específico desta skill.**

5. **Indicadores desagregados por grupo vulnerável sempre que o dado permitir.** Quando o dado não permitir, a lacuna vira item explícito do plano de governança da Etapa 8 — nomeada como `LACUNA DE MENSURAÇÃO` com estratégia concreta de enfrentamento. Nunca é esquecida nem mascarada. **Este princípio é específico desta skill.**

6. **Checkpoints humanos obrigatórios nas transições críticas.** A skill **interrompe** o fluxo e aguarda confirmação humana; não avança silenciosamente. **Modo full:** 4 checkpoints (fim da Etapa 1, fim da Etapa 4, fim da Etapa 6, fim da Etapa 9). **Modo só-indicadores:** 3 checkpoints (fim da Etapa 1', fim da Etapa 6, fim da Etapa 9). Ver `docs/equity-lens.md` para o framework de equidade do repositório.

## O workflow — Modo full (9 etapas)

O trabalho é organizado em 9 etapas sequenciais. Cada etapa tem **objetivo**, **prompt sugerido** pronto pra copiar, e **output esperado** que alimenta a etapa seguinte. Os prompts usam tags XML (`<principios>`, `<escopo>`, etc.) pra reduzir ambiguidade — prática recomendada pela Anthropic. Não pule etapas; a qualidade final depende da disciplina de validar humanamente nos checkpoints indicados.

Se você já tem 3–5 objetivos estratégicos aprovados e quer apenas derivar KPIs/OPIs, vá direto para a seção "Modo só-indicadores (5 etapas)" abaixo.

### Etapa 1 — Fundamentos e regras de classificação

**Objetivo:** Estabelecer princípios de trabalho com o modelo + capturar escopo rico + travar regras de H1/H2/H3 + travar critério único de priorização + nomear público prioritário e grupos vulneráveis **antes** de qualquer discussão de iniciativas. Sem esse alinhamento inicial, as etapas seguintes acumulam desvios invisíveis.

**Prompt sugerido:**

```
Você é especialista em portfólio de inovação e monitoramento de
resultados, apoiando equipes de impacto social em planejamento
estratégico. Trabalhe em português claro e inclusivo.

Antes de começar, leia e concorde com os princípios abaixo — eles valem
para toda a conversa desta análise.

<principios>
1. Facilitar, não decidir. Priorização, validação de KPIs e aprovação do
   Mapa H1-H2-H3 são responsabilidades humanas. Você acelera preparação
   e sistematização.
2. Equidade é critério ponderado de priorização, não disclaimer. Grupos
   vulneráveis são nomeados antes de qualquer discussão de horizontes.
3. "Não encontrado" quando faltar base; "[suposição]" com justificativa
   de 1 frase quando precisar inferir.
4. Toda iniciativa descartada na priorização gera a pergunta "quem deixa
   de ser atendido?" — registro obrigatório.
5. Indicadores desagregados por grupo vulnerável quando o dado permitir;
   quando não, marcar LACUNA DE MENSURAÇÃO com estratégia de
   enfrentamento.
6. Interromper o fluxo e aguardar confirmação humana nos 4 checkpoints
   obrigatórios (fim da Etapa 1, Etapa 4, Etapa 6 e Etapa 9).
</principios>

Agora preencha o escopo comigo. Pergunte sobre os campos que eu não
preencher; não invente nem preencha silenciosamente.

<escopo>
  <missao_mandato>[1 parágrafo — missão ou mandato institucional]</missao_mandato>
  <publico_prioritario>[quem a organização serve — específico, não "beneficiários"]</publico_prioritario>
  <grupos_vulneraveis>[lista de grupos concretos em situação de vulnerabilidade — nomes reais, não "populações vulneráveis"]</grupos_vulneraveis>
  <restricoes_inegociaveis>[legais, orçamentárias, éticas]</restricoes_inegociaveis>
  <orcamento_ordem>[ordem de grandeza do orçamento disponível]</orcamento_ordem>
  <horizonte_ciclo>[quando começa o próximo ciclo de planejamento — data ou janela]</horizonte_ciclo>
  <regras_H1_H2_H3>
    H1 (até 12 meses): melhorias do core e continuidade; baixa novidade;
    incerteza operacional.
    H2 (12-24 meses): adjacências/novas ofertas relacionadas ao core;
    média novidade; incerteza de adoção.
    H3 (24-36+ meses): apostas transformacionais; alta novidade;
    incerteza tecnológica/de modelo.
    [Usuário: confirme ou ajuste. Ajustes só com motivo explícito.]
  </regras_H1_H2_H3>
  <criterio_priorizacao>
    Default proposto: Impacto 30% + Equidade 20% + Viabilidade 25% +
    Alinhamento 15% + Risco 10% (pesos somam 100%).
    [Usuário: confirme ou ajuste. Alerta: "Equidade = 0%" ou ausente
    gera nota explícita da skill mas não bloqueia — responsabilidade
    humana.]
  </criterio_priorizacao>
  <modo>full</modo>
</escopo>

Use a regra dos 3 critérios (tempo, novidade, incerteza) pra classificar
iniciativas nas etapas seguintes: se 2 de 3 critérios apontam pro mesmo
horizonte, classifique nele.

CHECKPOINT HUMANO OBRIGATÓRIO: antes de avançar, confirme comigo que os
fundamentos e critérios acima refletem o que a equipe/liderança aprova.
Responda apenas com "OK — fundamentos confirmados" quando estiver pronto,
OU com ajustes específicos pra qualquer campo.
```

**Output esperado:** Bloco `<escopo>` preenchido e confirmado pelo usuário. A skill aguarda "OK — fundamentos confirmados" antes de avançar. Se algum campo crítico (`missao_mandato`, `publico_prioritario`, `grupos_vulneraveis`, `criterio_priorizacao`) não foi preenchido, a skill pergunta antes de seguir.

### Etapa 2 — Inventário focado e lacunas

**Objetivo:** Levantar iniciativas candidatas (ou problemas/oportunidades se ainda não houver iniciativas claras) + normalizar e deduplicar via IA + identificar lacunas na distribuição H1/H2/H3 *antes* de classificar.

**Orientação para humanos:** Liste até 12 iniciativas (nomes curtos); se não houver, descreva 3 problemas ou oportunidades prioritários. Para cada iniciativa responda em 1 linha:
- Objetivo ("o que muda para quem")
- Prazo-alvo
- Grau de novidade (baixo/médio/alto)
- Principal incerteza
- Evidência citada (se houver — fonte, dado, precedente)

**Prompt sugerido:**

```
Recebi a lista de iniciativas abaixo. Agora:

1. Remova duplicatas e normalize os títulos pra que iniciativas similares
   fiquem juntas (mas não as funda silenciosamente — mostre o que foi
   normalizado pra eu confirmar).

2. Preencha o quadro de trabalho em Markdown:
   | Iniciativa | Objetivo (1 frase) | Prazo-alvo | Novidade | Incerteza | Evidência |

3. Identifique lacunas na distribuição esperada H1/H2/H3 — por exemplo,
   excesso em H1 (continuidade só), vazio em H3 (nenhuma aposta
   transformacional). Nomeie as lacunas explicitamente.

4. Faça ao grupo a seguinte pergunta literal:
   "O que precisa existir em H2/H3 para que a visão de 24-36 meses seja
   plausível?"

   Aguarde resposta do humano e registre novas ideias **apenas se a
   equipe aprovar** explicitamente.

Não avance para a classificação (Etapa 3) sem passar por essa pergunta.

Lista de iniciativas:
[colar aqui a lista levantada pelo humano]
```

**Output esperado:** Tabela normalizada + nota explícita de lacunas + pergunta feita à equipe + (opcionalmente) novas iniciativas aprovadas pela equipe, prontas pra entrar na Etapa 3.

### Etapa 3 — Classificação profunda + priorização por critério único + log de descarte

**Objetivo:** Classificar cada iniciativa em horizonte usando a regra dos 3 critérios + priorizar pelo critério único travado na Etapa 1 + gerar log obrigatório de descarte ("quem deixa de ser atendido?" pra cada iniciativa cortada).

Esta etapa tem 3 sub-etapas que rodam em sequência: **3a** classificação, **3b** priorização, **3c** log de descarte.

**Prompt sugerido (Sub-etapa 3a — Classificação por horizonte):**

```
Para cada iniciativa do inventário da Etapa 2, aplique a regra dos 3
critérios (tempo, novidade, incerteza): se 2 de 3 apontarem para o mesmo
horizonte, classifique nela. Para cada iniciativa:

- Horizonte sugerido (H1/H2/H3)
- Justificativa em 1 frase citando qual o critério dominante
- Evidência mínima pra sustentar a escolha (métrica interna, custo/ordem
  de grandeza, precedente) — se faltar base, marcar "não encontrado" e,
  se precisar seguir, rotular como [suposição] com justificativa curta

Produza a tabela:
| Iniciativa | Horizonte | Justificativa | Evidência / "não encontrado" / [suposição] |
```

**Prompt sugerido (Sub-etapa 3b — Priorização por critério único):**

```
Agora aplique o critério único travado na Etapa 1. Para cada iniciativa:

- Nota qualitativa justificada (ex: "Impacto: médio — atinge ~400
  jovens no primeiro ciclo, justificativa em dado do SIGA interno")
  pra cada dimensão do critério
- Score final calculado usando os pesos da Etapa 1
- Justificativa de 1 frase
- Evidência citada ou "não encontrado"
- [suposição] quando aplicável

Produza a tabela:
| Iniciativa | Horizonte | [Dimensão 1] | [Dimensão 2] | [...] | Score | Justificativa | Evidência |

Importante: mostre as notas qualitativas justificadas, não só o score
final. Score sem justificativa esconde a lógica.
```

**Prompt sugerido (Sub-etapa 3c — Log de descarte, OBRIGATÓRIA):**

```
Para cada iniciativa que ficou fora do top-N (iniciativas descartadas),
preencha obrigatoriamente o log de descarte:

| Iniciativa descartada | Quem deixa de ser atendido? | Risco de aumento de desigualdade (sim / não / incerto) | Observação |

Esta etapa é OBRIGATÓRIA. Não pode ser pulada nem resumida.

Para cada linha do log:
- "Quem deixa de ser atendido" deve nomear grupos ou pessoas concretas,
  não "beneficiários"
- O risco de desigualdade deve ser avaliado explicitamente: sim, não ou
  incerto; quando incerto, justificar o que dependeria da resposta
- Observação: qual alternativa aparece no lugar? O que a equipe pode
  fazer pra compensar a ausência?

CHECKPOINT HUMANO OBRIGATÓRIO: peça confirmação linha por linha do log
de descarte + confirmação do top-N (ou top-X) que segue adiante. Não
avance para a Etapa 4 sem as duas confirmações.
```

**Output esperado:** 3 tabelas (classificação + priorização + log de descarte) + top-N confirmado + log de descarte validado pelo humano.

### Etapa 4 — Montagem do Mapa H1–H2–H3 e validação

**Objetivo:** Consolidar o produto do Caso 26 do livro — o Mapa H1–H2–H3 com narrativa por horizonte, log de decisões e log de descarte consolidado. Este é o **artefato comunicável** pra equipe, conselho e financiadores.

**Prompt sugerido:**

```
Gere o Mapa H1-H2-H3 em três colunas (uma por horizonte) com a estrutura:

| Nome | Objetivo (1 frase) | Justificativa do horizonte | Evidência / "não encontrado" | Dependência crítica | Confiança |

Inclua abaixo do mapa:

1. **Narrativa por horizonte (3 parágrafos — um por horizonte):**
   - Tese (o que esse horizonte aposta)
   - Riscos e assunções principais
   - Sinais de avanço (o que indica que o horizonte está se cumprindo)

2. **Log de decisões e pendências:** bullets com data, dono, próximo
   passo. Pra cada decisão estratégica tomada, quem assumiu
   responsabilidade e qual o próximo movimento esperado.

3. **Log de descarte consolidado:** copiar a tabela da sub-etapa 3c,
   preservando a coluna "quem deixa de ser atendido?" em cada linha.

CHECKPOINT HUMANO OBRIGATÓRIO: apresente o mapa completo e pergunte
literalmente: "Este é o Mapa H1-H2-H3 que você aprova? Responda com
'OK — mapa aprovado' ou com os ajustes pontuais que precisa fazer."

Não avance para a Etapa 5 sem a aprovação explícita.
```

**Output esperado (fim do Caso 26):** Mapa H1–H2–H3 aprovado pelo humano + narrativa por horizonte + log de decisões + log de descarte consolidado. Este artefato é reutilizado na síntese final da Etapa 9.

### Etapa 5 — Enquadrar objetivos como resultados

**Objetivo:** Para cada objetivo (vindos do Mapa da Etapa 4 no modo full, ou dos objetivos aprovados na Etapa 1' no modo só-indicadores), reescrever em linguagem de resultado, classificar como atividade/output/resultado estratégico, propor KPIs e OPIs iniciais, e sugerir uma métrica-norte.

**Orientação para humanos (modo só-indicadores):** Descreva de forma breve: (a) 3 a 5 objetivos estratégicos para os próximos 12–24 meses; (b) o público ou território prioritário; (c) restrições inegociáveis — legais, orçamentárias ou éticas. Se usou `theory-of-change`, passe os resultados finais da ToC como objetivos.

**Prompt sugerido:**

```
Você é especialista em monitoramento e avaliação. Trabalhe em português
claro e inclusivo. Não invente dados — escreva "não encontrado" quando
faltar base e use [suposição] para hipóteses, explicando em uma frase.

A partir dos objetivos abaixo:

1. Reescreva cada objetivo em linguagem de resultado ("o que muda para
   quem"), removendo verbos de atividade ("fazer", "realizar",
   "promover") e focando em mudança observável.

2. Classifique cada um como:
   - atividade (o que a organização faz)
   - output (o produto direto da atividade)
   - resultado estratégico (a mudança observável no público prioritário)

   Defina cada termo em até duas linhas na primeira vez que aparecer.

3. Para cada objetivo, proponha:
   - Até 3 KPIs (Key Performance Indicators — resultados estratégicos)
   - Até 2 OPIs (Operational Performance Indicators — execução
     operacional sob controle direto da equipe) relacionados a cada KPI

   Para cada indicador (KPI ou OPI), especifique:
   - Nome
   - Tipo (KPI / OPI)
   - Definição curta (1-2 linhas)
   - Fonte de dados
   - Periodicidade (mensal / trimestral / semestral / anual)
   - Explicação de como informa decisões

4. Sugira uma **métrica-norte** (KPI principal — aquele que melhor
   representa o avanço estratégico) e uma **alternativa B**, justificando
   a escolha em 1 frase.

5. Peça ao humano: "Qual métrica-norte a equipe/liderança escolhe — A
   ou B? A escolha tem consequências pras etapas seguintes."

Produza a tabela final:
| Objetivo reescrito | Classificação | KPIs propostos | OPIs propostos | Métrica-norte (A) | Alternativa (B) | Justificativa |

Objetivos:
[colar objetivos aprovados da Etapa 4 ou da Etapa 1']
```

**Output esperado:** Tabela com objetivos reescritos + classificação + KPIs/OPIs iniciais + métrica-norte escolhida pelo humano.

### Etapa 6 — Árvore de valor e hipóteses

**Objetivo:** Pra cada objetivo, construir árvore de valor textual mostrando drivers e ligações causais; marcar o que é [controlável], [influenciável] ou [observável]; nomear ligações frágeis e confundidores antes de refinar os indicadores.

**Orientação para humanos:** Revise os KPIs propostos na Etapa 5 e confirme quais fazem sentido. Informe à skill quais são controláveis pela equipe e quais dependem de fatores externos — esse input alimenta a árvore de valor.

**Prompt sugerido:**

```
Construa uma árvore de valor em formato textual para cada objetivo,
partindo da métrica-norte (KPI) e detalhando os principais fatores que
a influenciam — primeiro os drivers operacionais diretos (OPIs) e depois
os drivers secundários e terciários.

Use a notação:
- [controlável]: a equipe tem autoridade direta sobre o fator
- [influenciável]: a equipe pode afetar mas não controla totalmente
  (depende de parceiros, contexto, etc.)
- [observável]: a equipe só pode monitorar; o fator depende de forças
  externas (macroeconomia, contexto político, clima)

Estrutura da árvore (uma por objetivo):

Métrica-norte: [Nome do KPI]
  └ Driver primário 1 [controlável]: [descrição]
       └ Sub-driver 1a [controlável/influenciável]: [descrição]
       └ Sub-driver 1b [controlável/influenciável]: [descrição]
  └ Driver primário 2 [influenciável]: [descrição]
       └ Sub-driver 2a [influenciável]: [descrição]
  └ Driver primário 3 [observável]: [descrição]

Para cada ligação entre pai e filho na árvore, explique em 1 frase:
- Qual é a relação causal esperada
- Se a ligação é **frágil** (pouca evidência, muitos confundidores,
  depende de pressupostos fortes) — e por quê

Finalize com 3-5 perguntas para a equipe que ajudem a refinar o modelo
antes da validação (ex: "Driver X depende de Y estar estável — isso é
razoável pro próximo ciclo?").

CHECKPOINT HUMANO OBRIGATÓRIO: apresente a árvore de valor e pergunte:
"A equipe valida esta árvore de valor antes de eu refinar os
indicadores? Responda com 'OK — árvore validada' ou com os ajustes
necessários."

Não avance para a Etapa 7 sem a validação explícita.
```

**Output esperado:** Uma árvore de valor textual por objetivo + ligações frágeis nomeadas + perguntas pra equipe + validação humana explícita.

### Etapa 7 — Refinar indicadores estratégicos e operacionais

**Objetivo:** A partir da árvore validada, produzir a **especificação final** dos indicadores, com desagregação obrigatória por grupo vulnerável sempre que o dado permitir. Quando não permitir, cada lacuna vira item do plano de governança da Etapa 8.

**Prompt sugerido:**

```
A partir da árvore de valor validada, descreva os indicadores essenciais
para cada objetivo, agrupando-os em dois blocos textuais:

1. OPIs — medem execução e processos sob controle direto da equipe
2. KPIs — representam resultados estratégicos ou impactos esperados

Para cada indicador (KPI ou OPI), apresente:

- Nome
- Tipo (KPI / OPI)
- Definição curta (1-2 linhas)
- Fonte de dados
- Periodicidade (mensal / trimestral / semestral / anual)
- Decisão que o indicador orienta
- DESAGREGAÇÃO POR GRUPO VULNERÁVEL (obrigatória, específica desta
  skill): usando a lista de grupos vulneráveis da Etapa 1, especifique:
  * Quais quebras de análise são possíveis com o dado existente
    (ex: "desagregar por bairro, gênero e faixa etária")
  * Se o dado **não permite** desagregação relevante, marcar
    explicitamente:
    LACUNA DE MENSURAÇÃO: [descrição do que falta — ex: "raça/cor não
    é coletada no cadastro"]
    Essa lacuna será tratada na Etapa 8 (plano de governança).

Regras de preenchimento:
- Indique lacunas com "não encontrado" quando faltar base
- Marque [suposição] com justificativa curta quando precisar inferir
- Toda LACUNA DE MENSURAÇÃO flagada aqui precisa reaparecer na Etapa 8
  com estratégia de enfrentamento

Produza duas tabelas:

Tabela OPIs:
| Nome | Definição | Fonte | Periodicidade | Decisão orientada | Desagregação | Lacunas |

Tabela KPIs:
| Nome | Definição | Fonte | Periodicidade | Decisão orientada | Desagregação | Lacunas |

Ao final, liste todas as LACUNAS DE MENSURAÇÃO identificadas, numeradas,
pra que a Etapa 8 possa tratar cada uma.
```

**Output esperado:** Duas tabelas (OPIs + KPIs) completas + lista numerada de lacunas de mensuração que alimenta a Etapa 8.

### Etapa 8 — Plano de mensuração e governança

**Objetivo:** Especificar como cada indicador será coletado, atualizado e revisado ao longo do tempo; especificar fontes, frequência, responsáveis, riscos de viés e mitigação; **tratar cada LACUNA DE MENSURAÇÃO da Etapa 7 com estratégia concreta de enfrentamento**.

**Prompt sugerido:**

```
Descreva em texto corrido como cada indicador será coletado, atualizado
e revisado ao longo do tempo. Use este formato:

1. **Plano por indicador (tabela):**

| Indicador | Fonte primária | Frequência | Responsável sugerido | Risco de viés | Mitigação proposta |

   - Fonte primária: sistema, pesquisa, registro administrativo, etc.
     Se a fonte exige coleta nova, nomear o instrumento.
   - Frequência: mensal / trimestral / semestral / anual — coerente com
     a periodicidade declarada na Etapa 7.
   - Responsável sugerido: função/papel (ex: "Coordenação de
     programas"), não nome próprio.
   - Risco de viés: 1-2 frases descrevendo o principal viés esperado
     (seleção, memória, desejabilidade social, cobertura parcial, etc.).
   - Mitigação: 1-2 frases de estratégia concreta.

2. **Lacunas de mensuração e estratégia de enfrentamento:**

Pra cada LACUNA DE MENSURAÇÃO listada na Etapa 7, proponha estratégia
concreta:

| Lacuna | Estratégia de enfrentamento | Prazo | Responsável sugerido |

Exemplos de estratégias aceitáveis:
- "Coletar dado de raça/cor no próximo ciclo de cadastro (Q2 2026)"
- "Triangular com pesquisa amostral trimestral até cobrir 80% dos
  casos"
- "Aceitar como não mensurável nesta rodada e registrar em log de
  limitações; revisar em 12 meses"
- "Substituir por proxy qualitativo (entrevistas semi-estruturadas)
  documentado em anexo"

Cada lacuna PRECISA de estratégia concreta — "vamos pensar a respeito"
não é aceitável.

3. **Cronograma de revisão do plano:** Em que momentos do ciclo os
   indicadores e o plano serão revisados formalmente? (Ex: revisão
   semestral de OPIs + revisão anual de KPIs + revisão extraordinária
   quando crises ou mudanças materiais ocorrerem.)
```

**Output esperado:** Tabela-plano por indicador + tabela de lacunas com estratégia de enfrentamento + cronograma de revisão. Este documento é o handoff operacional pra equipe de M&E.

### Etapa 9 — Checagem de consistência e síntese final

**Objetivo:** Rodar autoverificação estruturada contra os 6 princípios invioláveis + produzir síntese narrativa final + lembrete explícito de que a decisão final é humana.

Esta etapa tem 3 sub-etapas: **9a** checagem de consistência, **9b** relatório de autoverificação, **9c** síntese narrativa.

**Prompt sugerido (Sub-etapa 9a — Checagem de consistência):**

```
Revise o conjunto completo do trabalho (Mapa H1-H2-H3, árvore de valor,
indicadores e plano de mensuração) e confirme explicitamente:

(i) Os OPIs descrevem processos controláveis pela equipe (não medem
    fatores externos)
(ii) Os KPIs traduzem resultados estratégicos ou impactos esperados
     (não são outputs nem atividades disfarçadas)
(iii) A periodicidade declarada é coerente com as fontes de dados
      (ex: não pedir dado mensal de uma pesquisa anual)
(iv) As fórmulas sugeridas são viáveis (a equipe consegue calcular com
     o dado disponível)
(v) Cada iniciativa priorizada tem ao menos 1 KPI e 2 OPIs
(vi) Toda LACUNA DE MENSURAÇÃO tem estratégia de enfrentamento

Pra cada item acima, produza a linha:
| Item | Cumprido? (Sim/Parcial/Não) | Evidência ou ajuste proposto |

Se algum item é "Não" ou "Parcial", descreva o ajuste necessário antes
de fechar a síntese final.
```

**Prompt sugerido (Sub-etapa 9b — Relatório de autoverificação):**

```
Produza o relatório de autoverificação contra os 6 princípios invioláveis
da skill. Formato:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência | Ajustes |

Cubra os 6 princípios, um por linha:

1. A skill facilita, não decide (checkpoints humanos respeitados?)
2. Equidade é critério ponderado (peso da Equidade no critério único?
   respeitado o piso ≥15% recomendado?)
3. "Não encontrado" + [suposição] explícitos
4. Log de descarte com pergunta "quem deixa de ser atendido?"
5. Desagregação por grupo vulnerável ou LACUNA DE MENSURAÇÃO
6. Checkpoints humanos obrigatórios respeitados em todas as transições

Cada linha deve citar trecho concreto do produto (mapa, tabela,
indicador, plano) que sustenta o "cumprido" ou aponta a falha.
```

**Prompt sugerido (Sub-etapa 9c — Síntese narrativa final):**

```
Produza a síntese narrativa final em no máximo 1 página (400-500
palavras). Estrutura:

1. **Mapa H1-H2-H3** — 1 frase por horizonte, nomeando a tese de cada um
2. **Top-3 KPIs** — a métrica-norte + 2 outras KPIs de maior peso
   estratégico, com definição curta e quem é responsável
3. **Lacunas críticas de mensuração** — 3-5 lacunas mais importantes e
   prazo de enfrentamento
4. **Recomendações ao usuário** — o que vale validar com
   conselho/liderança antes de operacionalizar; onde buscar segunda
   opinião; qual o próximo ciclo de revisão

NOTA FINAL OBRIGATÓRIA: inclua literalmente o parágrafo final:

"Lembrete: este plano é um rascunho estruturado pra facilitar a
deliberação humana. A decisão sobre qual caminho seguir é
responsabilidade exclusiva da liderança, que deve avaliar impactos
políticos, sociais e éticos antes de validar o plano. Antes de publicar,
rode o checklist em references/checklist.md."

CHECKPOINT HUMANO OBRIGATÓRIO: apresente a síntese final e pergunte:
"A síntese final está pronta pra handoff? Responda 'OK — síntese
aprovada' ou aponte ajustes."
```

**Output esperado:** Relatório de consistência + relatório de autoverificação dos 6 princípios + síntese narrativa de 1 página com nota final obrigatória + aprovação humana explícita.

## O workflow — Modo só-indicadores (5 etapas)

Use este modo quando a equipe **já tem 3 a 5 objetivos estratégicos aprovados** por liderança/conselho/edital e quer derivar KPIs/OPIs sem refazer o planejamento estratégico inteiro.

O modo só-indicadores pula as Etapas 1–4 do modo full (levantamento, priorização, Mapa H1–H2–H3) e entra direto na Etapa 5. A Etapa 1 é substituída por uma **Etapa 1' reduzida** que captura apenas os fundamentos essenciais e recebe os objetivos já aprovados.

### Etapa 1' — Fundamentos reduzidos + objetivos aprovados

**Objetivo:** Capturar os 6 campos mínimos pra rodar os indicadores + receber os objetivos já aprovados + registrar a fonte dos objetivos.

**Prompt sugerido:**

```
Você é especialista em monitoramento e avaliação. Trabalhe em português
claro e inclusivo.

Antes de começar, leia e concorde com os princípios abaixo:

<principios>
1. Facilitar, não decidir. Validação de KPIs é responsabilidade humana.
2. Equidade é infraestrutura — indicadores desagregados por grupo
   vulnerável quando o dado permitir; quando não, LACUNA DE MENSURAÇÃO
   com estratégia de enfrentamento.
3. "Não encontrado" quando faltar base; "[suposição]" com justificativa
   quando precisar inferir.
4. Interromper o fluxo e aguardar confirmação humana em 3 checkpoints
   obrigatórios (fim da Etapa 1', Etapa 6 e Etapa 9).
</principios>

Agora preencha o escopo reduzido:

<escopo>
  <missao_mandato>[1 parágrafo]</missao_mandato>
  <publico_prioritario>[quem a organização serve — específico]</publico_prioritario>
  <grupos_vulneraveis>[lista concreta, com nomes reais]</grupos_vulneraveis>
  <restricoes_inegociaveis>[legais, orçamentárias, éticas]</restricoes_inegociaveis>
  <objetivos_aprovados>
    [3 a 5 objetivos estratégicos já aprovados pela equipe ou
    liderança]
  </objetivos_aprovados>
  <fonte_dos_objetivos>[planejamento estratégico anterior | theory-of-change | deliberação de conselho | edital aprovado | outro]</fonte_dos_objetivos>
  <modo>so_indicadores</modo>
</escopo>

CHECKPOINT HUMANO OBRIGATÓRIO: antes de avançar, confirme comigo que
os fundamentos reduzidos e objetivos acima estão corretos. Responda
"OK — fundamentos e objetivos confirmados" OU com ajustes pontuais.
```

**Output esperado:** Bloco `<escopo>` reduzido preenchido + confirmação humana explícita.

### Etapas 5 a 9 — Idênticas ao modo full

Após a Etapa 1', o workflow segue exatamente igual ao modo full, começando na Etapa 5 (Enquadrar objetivos como resultados) e indo até a Etapa 9 (Checagem de consistência e síntese final). Volte à seção "Modo full" acima para os prompts dessas etapas — eles funcionam sem modificação.

**Nota sobre o modo só-indicadores:** você não passa pela priorização (Etapa 3) e nem gera log de descarte (sub-etapa 3c). Isso **não** significa que o Princípio 4 está dispensado — significa que a priorização já foi feita fora da skill. Se a fonte dos objetivos é um planejamento anterior, confirme que o descarte de iniciativas foi discutido lá; se não foi, a skill **alerta o usuário** de que há um risco de viés estrutural herdado (sem bloquear).

## Checkpoints de validação humana

A skill **interrompe** o fluxo e aguarda confirmação humana explícita nos checkpoints abaixo. Não avance silenciosamente em nenhum deles.

**Modo full — 4 checkpoints obrigatórios:**

1. **Fim da Etapa 1** — confirmar fundamentos, especialmente `grupos_vulneraveis` e `criterio_priorizacao`. Resposta esperada: "OK — fundamentos confirmados" ou ajustes pontuais.

2. **Fim da Etapa 4** — aprovar o Mapa H1–H2–H3 consolidado (três colunas + narrativa por horizonte + log de decisões + log de descarte). Resposta esperada: "OK — mapa aprovado" ou ajustes pontuais. O log de descarte precisa ser revisado linha a linha.

3. **Fim da Etapa 6** — validar a árvore de valor antes de refinar os indicadores. Resposta esperada: "OK — árvore validada" ou ajustes pontuais.

4. **Fim da Etapa 9** — validar a síntese final (relatório de consistência + relatório de autoverificação + síntese narrativa de 1 página). Resposta esperada: "OK — síntese aprovada" ou ajustes pontuais.

**Modo só-indicadores — 3 checkpoints obrigatórios:**

1. **Fim da Etapa 1'** — confirmar fundamentos reduzidos e objetivos aprovados (combina os dois primeiros checkpoints do modo full).

2. **Fim da Etapa 6** — validar a árvore de valor.

3. **Fim da Etapa 9** — validar a síntese final.

**Regra geral:** a skill nunca avança com "silêncio = consentimento". O humano tem que responder literalmente com a frase de confirmação ou apontar ajustes. Isso não é formalidade — é a tradução operacional do Princípio 1 ("a skill facilita, não decide").

## Falhas comuns

Anti-patterns recorrentes na aplicação desta skill. Se você reconhecer algum deles no seu processo, volte à etapa anterior e corrija antes de avançar.

1. **Planejamento só-H1 disfarçado de multi-horizonte.** A equipe lista 10 iniciativas, classifica 8 em H1, 2 em H2, 0 em H3, e chama de "Mapa H1–H2–H3". O resultado é apenas continuidade do que já existe. **Mitigação:** a Etapa 2 identifica lacunas explicitamente e a sub-etapa 3a pergunta ao grupo "o que precisa existir em H2/H3 pra visão de 24–36 meses ser plausível?". Se a resposta é "nada", a equipe precisa reconhecer que não está fazendo planejamento estratégico — está fazendo plano operacional.

2. **Score de priorização travestido de objetividade.** Modelo gera números sem justificativa qualitativa, equipe assume que "o score diz o que fazer". Priorização vira cerimônia de matemática. **Mitigação:** a sub-etapa 3b exige notas qualitativas justificadas por dimensão + frase de justificativa em cada linha; o checkpoint humano da Etapa 4 confirma top-N, não aceita score cego. Score sem justificativa escrita é um sinal de alerta.

3. **Descarte sem nomeação de quem fica de fora.** Iniciativa "Curso de audiovisual" é descartada porque score é baixo; ninguém pergunta quem já participava e vai perder o serviço; o corte aumenta desigualdade silenciosamente. **Mitigação:** Princípio 4 + sub-etapa 3c com log de descarte obrigatório. **Cada linha** do log precisa nomear grupos concretos, não "beneficiários" genérico.

4. **KPI que mede atividade disfarçado de resultado estratégico.** "Número de oficinas realizadas" listado como KPI quando é output, não resultado. "Horas de formação oferecidas" listado como KPI quando é atividade. O indicador parece bom mas não mede mudança. **Mitigação:** a Etapa 5 exige classificação explícita (atividade / output / resultado estratégico); a Etapa 9 sub-etapa (i) tem item de checagem específico pra separar OPIs de KPIs.

5. **Indicador sem desagregação mascarando desigualdade.** "Taxa de conclusão do curso = 70%" é reportada sem mostrar que jovens negros têm 50% e jovens brancos têm 90%. A média agregada esconde a desigualdade estrutural e pode até ser usada pra justificar continuidade do que não funciona. **Mitigação:** Princípio 5 + Etapa 7 exige desagregação por grupo vulnerável; quando o dado não existe, a LACUNA DE MENSURAÇÃO é flagada e tratada na Etapa 8, nunca omitida.

6. **Plano "pronto" sem validação humana real.** A skill produz o plano completo e o usuário copia/cola sem os checkpoints. Princípio 1 vira enfeite. **Mitigação:** Princípios 1 e 6 + 4 checkpoints no modo full (3 no modo só-indicadores) onde a skill interrompe e aguarda confirmação explícita; a nota final obrigatória da Etapa 9 reforça ("a decisão sobre qual caminho seguir é responsabilidade exclusiva da liderança").

## Arquivos complementares

- `references/exemplos.md` — execução completa fictícia no modo full, usando o cenário "Rede Jovem Território" (OSC juvenil em município médio). Mostra os dois modos em contexto.
- `references/variantes.md` — 5 variantes do workflow: modo só-indicadores, planejamento em governo (secretaria municipal), integração soft com `theory-of-change`, handoff para `project-structuring` e critério de priorização customizado.
- `references/checklist.md` — checklist de validação humana em duas seções (técnica + equidade) + regra de ouro final.
- `../../docs/equity-lens.md` — framework de equidade do repositório, herdado por todas as skills.
