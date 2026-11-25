---
name: project-structuring
description: Transforma mandatos amplos ou entregáveis soltos em plano estruturado — produtos com critério de aceitação, atividades decompostas, cronograma ancorado em marcos reais, planejamento de capacidade humana e aquisições. Para OSCs, governos e parcerias.
---

# Estruturação de Projeto

## Quando usar esta skill

Esta skill apoia o trabalho de traduzir intenções programáticas em um plano executável — produtos entregáveis, atividades, cronograma, capacidade humana e aquisições — com rastreabilidade de decisões e lente de equidade operacional.

- Receber **mandato programático amplo** ("fortalecer a rede de atenção básica", "melhorar a formação docente") e precisar transformá-lo em plano
- Ter **termo de referência ou edital aprovado** com entregáveis pré-definidos e precisar completar o plano (cronograma + capacidade + aquisições)
- Passar de uma **teoria da mudança** (insumos → atividades → resultados → impactos) já construída para o plano de execução
- Preparar **insumo estruturado para captação de recursos** — um plano consolidado alimenta propostas, concept notes e narrativas de orçamento
- Precisar verificar se o projeto **cabe na equipe real** antes de assinar compromissos com financiadores ou parceiros

Sinais típicos na conversa do usuário:

- "Ganhamos o edital, mas agora tenho que fazer o cronograma e não sei por onde começar"
- "Meu TR diz X, Y, Z — me ajuda a transformar isso em atividades e prazos?"
- "A gente tem essa ideia de projeto mas não organizou nada ainda"
- "Preciso saber se cabe na equipe que a gente tem"
- "O financiador quer ver cronograma com marcos"
- "Tenho a ToC, agora preciso do plano de execução"

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Insumos mínimos carregados** — pelo menos uma das opções: mandato programático textual, teoria da mudança existente, termo de referência aprovado, ou rascunho de entregáveis. Sem nenhum desses, a skill não tem base para trabalhar.

2. **Noção de âncoras reais** — prazos mandatórios (edital, marco legal, data de evento externo) declarados explicitamente, OU declaração de que não há âncoras. "Acho que deve ser rápido" não é âncora; "A entrega é em 30/06/2026 pelo termo de parceria" é.

3. **Dimensionamento de equipe** — para rodar a Etapa 6 (Capacidade humana), lista das pessoas/funções disponíveis com percentual real de dedicação ao projeto, considerando cumulatividade com outros compromissos.

4. **Tempo para validação humana** — a skill tem dois checkpoints obrigatórios (após Etapa 3 e após Etapa 8). Sem humano revisando nesses pontos, a saída é rascunho interno, não plano apresentável.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar entregáveis, atividades ou requisitos.** Se uma informação não está nos insumos fornecidos, escreva "não encontrado" ou marque como `[suposição]` com justificativa. Não preencha lacunas com padrões genéricos do setor.

2. **Datas absolutas só existem quando há âncora real.** Duração estimada por default em unidades relativas (dias úteis, semanas, "T+Nd" do início). Datas absolutas só aparecem quando o usuário declarou explicitamente uma âncora (prazo de edital, marco legal, compromisso contratual) e a data é calculada em volta dela.

3. **Critério de aceitação é mensurável ou não existe.** "Manual validado" não é critério — "manual de 20-30 páginas validado por 3 leitores externos com comentários tratados e versão final em PDF acessível" é. Linhas sem critério mensurável são rejeitadas ou marcadas como `[suposição]`.

4. **Distinguir fato de inferência.** Toda inferência (duração estimada sem base explícita, dependência implícita, custo projetado) é marcada como `[suposição]` com justificativa de uma frase. Isso torna explícito o que é derivação do modelo, não do usuário.

5. **Plano que oculta trabalho ou capacidade é plano falso.** Se a análise de capacidade humana (Etapa 6) revelar que a equipe não cabe, que há trabalho invisível não-atribuído, ou que a demanda supera a disponibilidade real, isso vai para o output sem suavização. Plano honesto é plano útil.

6. **Lente de equidade e justiça social em todas as etapas críticas.** Quem são os beneficiários concretos de cada entregável? Quais ritmos externos (safras, festividades, calendários comunitários) foram considerados? Que trabalhos estão invisíveis no plano (cuidado, mediação cultural, tradução)? A distribuição de carga concentra trabalho em frontline feminilizada/terceirizada? As especificações de aquisição excluem fornecedores pequenos ou periféricos? Ver `docs/equity-lens.md` do repo para o framework geral. **Esta não é uma regra opcional** — skills de impacto social sem lente de equidade reproduzem desigualdades.

## O workflow (8 etapas)

O trabalho de estruturação é organizado em 8 etapas sequenciais. Cada etapa tem um **objetivo**, um **prompt sugerido** pronto para copiar, e um **output esperado** que serve de insumo para a etapa seguinte. Os prompts usam tags XML (`<escopo>`, `<principios>`, `<insumos>`, `<entregaveis>`, `<atividades>`, `<cronograma>`, etc.) — prática recomendada pela Anthropic para entradas estruturadas e saídas mais confiáveis.

**Estrutura do fluxo:**

- **Etapas 1-2** sempre rodam (configuração + insumos)
- **Etapa 3** roda em dois modos: **Modo A** (mandato amplo → produz entregáveis) ou **Modo B** (entregáveis prontos → revisão crítica). O modo é declarado na Etapa 1.
- **Etapas 4-5** sempre rodam (decomposição em atividades + sequenciamento)
- **Etapa 6 (Capacidade humana)** é opcional, **ligada por default**. Pode ser pulada quando o usuário declara trabalho individual ou equipe já dimensionada externamente.
- **Etapa 7 (Aquisições)** é opcional, **desligada por default**. Ligada quando há compras com janelas críticas, especificações técnicas ou valores relevantes.
- **Etapa 8** sempre roda (consolidação + autoverificação + handoff humano)

Usuário típico roda 6-7 etapas efetivamente. Não pule etapas — a qualidade do plano final depende da disciplina de ir uma por uma, validando nos checkpoints.

### Etapa 1 — Configuração, princípios e modo de entrada

**Objetivo:** Estabelecer as regras do trabalho com o modelo, injetar os princípios invioláveis, e capturar: modo de entrada, flags dos módulos opcionais, pergunta-alvo, público do plano final. Sem esse alinhamento, o trabalho posterior parte desfocado.

**Prompt sugerido:**

```
Você é especialista em gestão de projetos de impacto social, com
experiência em OSCs, políticas públicas e parcerias. Vou te enviar, nas
próximas mensagens, insumos para estruturar um projeto. Antes de
começar, leia e concorde com os princípios abaixo — eles valem para
todas as respostas desta conversa.

<principios>
1. Nunca inventar entregáveis, atividades ou requisitos. Se uma
   informação não está nos insumos fornecidos, escreva "não encontrado"
   ou marque como [suposição] com justificativa.
2. Datas absolutas só existem quando há âncora real declarada.
   Duração por default em unidades relativas (dias úteis, semanas,
   "T+Nd"). Absolutas só em volta de âncoras do usuário.
3. Critério de aceitação é mensurável ou não existe. Linhas vagas
   são marcadas como [suposição] e sinalizadas para refinamento.
4. Distinguir fato de inferência. Toda inferência vira [suposição]
   com justificativa de uma frase.
5. Plano que oculta trabalho ou capacidade é plano falso. Gaps
   descobertos vão para o output sem suavização.
6. Lente de equidade em todas as etapas críticas: beneficiários
   nomeados, ritmos externos respeitados, trabalhos invisíveis
   incluídos, capacidade realista, aquisições não-excludentes.
</principios>

Agora, antes dos insumos, preciso que você confirme o escopo do trabalho
preenchendo o bloco abaixo com base no que eu já te contei. Se algum
campo estiver indefinido, pergunte.

<escopo>
  <modo_entrada>A | B</modo_entrada>
  <!-- A = mandato amplo (produz entregáveis do zero)
       B = entregáveis prontos (revisão crítica + completar plano) -->
  <pergunta_alvo>...</pergunta_alvo>
  <publico_plano>...</publico_plano>
  <!-- ex.: governança interna, conselho da OSC, financiador,
       secretaria municipal, equipe de execução -->
  <modulo_capacidade_humana>ligado | desligado</modulo_capacidade_humana>
  <!-- default: ligado. Desligado só se trabalho individual
       ou equipe já dimensionada externamente -->
  <modulo_aquisicoes>ligado | desligado</modulo_aquisicoes>
  <!-- default: desligado. Ligado quando há compras com janelas
       críticas, especificações técnicas ou valores relevantes -->
</escopo>

Se concordar com as regras, responda "OK – regras definidas" e aguarde
os insumos.
```

**Output esperado:** Confirmação verbal ("OK – regras definidas") + bloco `<escopo>` preenchido, pronto para ser referenciado nas etapas seguintes.

### Etapa 2 — Insumos e contexto institucional

**Objetivo:** Catalogar o que o usuário já tem — teoria da mudança, termo de referência, plano de trabalho, prazos mandatórios, restrições legais/orçamentárias, atores envolvidos, datas-âncora — e nomear lacunas críticas antes de começar a produzir conteúdo.

**Prompt sugerido:**

```
Antes de produzir entregáveis, preciso que você catalogue os insumos que
recebeu. Produza uma tabela Markdown com estas colunas:

| Insumo_ID | Tipo | Nome/Descrição curta | Conteúdo relevante para o plano | Marco/Prazo extraído (se houver) | Observações |

Regras:
- Use Insumo_IDs sequenciais: INS001, INS002, INS003...
- "Tipo" é um destes: mandato programático, teoria da mudança,
  termo de referência, plano de trabalho, restrição legal, restrição
  orçamentária, ator externo, marco temporal, documento técnico,
  diagnóstico prévio, outro (justificar).
- "Conteúdo relevante para o plano" é uma frase curta resumindo
  o que esse insumo traz que alimenta a estruturação (não é resumo
  geral do documento).
- "Marco/Prazo extraído" só preenchido se o insumo contiver data
  explícita, marco oficial ou janela mandatória. Caso contrário,
  "não encontrado".
- Se algum insumo contradiz outro, sinalize em "Observações"
  explicitando o conflito.

Depois da tabela, escreva uma <nota_lacunas> cobrindo explicitamente:

<nota_lacunas>
  (a) Lacunas críticas que IMPEDEM avanço (ex.: "sem qualquer
      informação sobre equipe disponível, a Etapa 6 não pode rodar").
  (b) Lacunas que podem ser tratadas como [suposição] na continuação
      do fluxo (ex.: "o edital não declara data de início, vou assumir
      T+15d do aceite da proposta como [suposição]").
  (c) Contradições entre insumos a resolver na próxima etapa.
</nota_lacunas>

Seja específico. Nomear lacunas é mais útil do que generalizar.
```

**Output esperado:** Tabela completa de insumos classificados + nota de lacunas diferenciando bloqueadores de suposições viáveis + contradições sinalizadas.

### Etapa 3 — Entregáveis com critérios de aceitação

**Objetivo:** Produzir a lista de entregáveis do projeto com critério de aceitação mensurável, evidência de conclusão verificável, e beneficiários impactados nomeados concretamente. Esta etapa tem **comportamento condicional** baseado no modo de entrada declarado na Etapa 1.

**Prompt sugerido (Modo A — mandato amplo, produz entregáveis do zero):**

```
Com base nos insumos catalogados na Etapa 2 e no mandato declarado no
escopo, proponha a lista de entregáveis do projeto. Use esta tabela
Markdown:

<entregaveis>
| Entregável_ID | Produto | Descrição | Critério de aceitação | Evidência de conclusão | Beneficiários impactados | [suposição?] | Observações |
</entregaveis>

Regras:
- Use Entregável_IDs sequenciais: ENT001, ENT002, ENT003...
- "Produto" é um rótulo curto e objetivo (ex.: "Manual formativo",
  "Ciclo de oficinas regionais", "Relatório de avaliação").
- "Descrição" é uma frase explicando o que o produto é.
- "Critério de aceitação" PRECISA ser mensurável: formato, tamanho,
  quantidade, qualidade mínima, quem valida. Exemplo ruim:
  "Manual validado". Exemplo bom: "Manual de 20-30 páginas, validado
  por 3 leitores externos, com comentários tratados, versão final
  em PDF acessível (WCAG 2.1 AA)".
- "Evidência de conclusão" é um artefato objetivo: arquivo entregue,
  ata assinada, link público, nota fiscal, registro em sistema.
- "Beneficiários impactados" é OBRIGATÓRIO nomear grupos concretos.
  Exemplo ruim: "população atendida", "usuários". Exemplo bom:
  "educadores populares de OSCs nos 4 territórios-sede, com perfil
  majoritariamente feminino e atuação com crianças em situação de
  vulnerabilidade social".
- "[suposição?]" = "sim" quando o entregável foi inferido do mandato
  sem confirmação explícita nos insumos; "não" quando há referência
  direta.

Depois da tabela, escreva um parágrafo curto (3-5 linhas) explicando:
- Quais entregáveis foram propostos como [suposição] e por quê
- Quais critérios de aceitação precisaram ser inferidos
- Se algum beneficiário foi abstrato por falta de dado, e qual dado
  falta para nomear concretamente
```

**Prompt sugerido (Modo B — entregáveis prontos, revisão crítica):**

```
Na Etapa 1 você declarou que já tem entregáveis definidos num documento
(termo de referência, plano de trabalho, proposta aprovada). Sua tarefa
agora é revisá-los criticamente contra os princípios invioláveis. NÃO
produza entregáveis novos — avalie os existentes.

Para cada entregável do documento fornecido, produza uma linha na tabela:

<revisao_entregaveis>
| Entregável_ID | Produto (como está no doc) | Descrição | Critério de aceitação atual | Critério passou no teste de mensurabilidade? | Evidência de conclusão | Beneficiários nomeados concretamente? | Ação sugerida | [suposição?] |
</revisao_entregaveis>

Regras:
- "Critério passou no teste de mensurabilidade?" = "sim" apenas se o
  critério explicita formato/tamanho/quantidade/quem valida. Caso
  contrário "não" e aponte o que falta.
- "Beneficiários nomeados concretamente?" = "sim" se o documento nomeia
  grupos com qualificadores; "não" se usa abstrações ("usuários",
  "beneficiários", "comunidade").
- "Ação sugerida" tem três valores possíveis:
  (1) "manter como está" — entregável passou em todos os testes
  (2) "refinar: [o que refinar]" — entregável válido mas precisa
      de ajuste específico
  (3) "rejeitar: [motivo]" — entregável vago demais, duplicado,
      sobreposto, ou fora de escopo

Depois da tabela, escreva uma nota de consolidação apontando:
- Entregáveis que merecem ser fundidos (sobreposição)
- Lacunas no conjunto (entregáveis que o mandato implica mas o doc
  não cobre)
- Critérios de aceitação que o doc apresenta como prontos mas não são
```

**Output esperado:** (Modo A) Tabela `<entregaveis>` completa + parágrafo de suposições; (Modo B) Tabela `<revisao_entregaveis>` completa + nota de consolidação.

**Checkpoint humano obrigatório após esta etapa.** Ver seção "Checkpoints de validação humana".

### Etapa 4 — Decomposição em atividades

**Objetivo:** Transformar cada entregável (produzido na Etapa 3 ou validado na revisão crítica) em uma sequência de 3-8 atividades de escopo limitado, com dependências explícitas e duração estimada em unidades relativas. Sem datas absolutas nesta etapa.

**Prompt sugerido:**

```
A partir dos entregáveis validados, decomponha cada um em atividades.
Produza esta tabela Markdown:

<atividades>
| Atividade_ID | Entregável_ID | Descrição (1 frase) | Duração estimada | Unidade | Dependências (Atividade_IDs) | Marco associado | [suposição?] |
</atividades>

Regras:
- Use Atividade_IDs sequenciais: ATV001, ATV002, ATV003...
- Cada entregável vira 3-8 atividades. Se um entregável gerar menos
  de 3 ou mais de 8, reavalie — pode estar mal dimensionado.
- "Descrição" é uma frase objetiva, no infinitivo ("validar conteúdo
  pedagógico com leitores externos"), não substantivada.
- "Duração estimada" é um número inteiro ou intervalo (ex.: "5",
  "3-5", "10-14"). NUNCA data absoluta nesta etapa.
- "Unidade" é uma destas: "dias úteis", "semanas", "T+Nd do início".
- "Dependências" lista Atividade_IDs que precisam estar concluídas
  antes. Para atividades sem predecessoras, "nenhuma".
- "Marco associado" = âncora declarada pelo usuário à qual a atividade
  se vincula (ex.: "entrega final ao financiador", "data do evento
  público", "prazo legal de prestação de contas"). Vazio se não há
  marco direto.
- "[suposição?]" = "sim" quando a duração foi inferida sem base
  explícita, "não" quando há referência no insumo (ex.: "o termo de
  parceria estipula 30 dias para validação").

Depois da tabela, escreva uma <nota_decomposicao> apontando:
- Entregáveis que exigiram mais inferência (onde o mandato estava
  vago sobre o "como")
- Atividades que você marcou como [suposição] e que precisam de
  confirmação humana antes do cronograma
- Dependências cruzadas entre entregáveis (atividade de ENT001
  depende de atividade de ENT003, etc.)
```

**Output esperado:** Tabela `<atividades>` completa + nota de decomposição identificando suposições e dependências cruzadas.

### Etapa 5 — Sequenciamento com âncoras e caminho crítico qualitativo

**Objetivo:** Ordenar as atividades respeitando dependências e **datas-âncora declaradas**. Onde há âncora, calcular janelas absolutas em volta; onde não há, manter tempo relativo. Identificar caminho crítico **qualitativamente** — a cadeia mais longa de dependências bloqueantes — e apontar riscos de atraso. Considerar ritmos externos (calendários comunitários, festividades, safras, janelas escolares).

**Prompt sugerido:**

```
Com a lista de atividades da Etapa 4, produza o cronograma. Use esta
tabela Markdown:

<cronograma>
| Atividade_ID | Janela de execução | Tipo de janela | Dependências resolvidas | No caminho crítico? | Risco de atraso | [suposição?] |
</cronograma>

Regras:
- "Janela de execução" tem dois formatos possíveis, escolhidos por
  linha:
  (a) ABSOLUTA: quando a atividade está ancorada em data declarada
      pelo usuário ou tem dependência direta com atividade ancorada.
      Formato: "DD/MM/YYYY a DD/MM/YYYY" ou "semana de DD/MM a DD/MM".
  (b) RELATIVA: quando não há âncora. Formato: "T+Nd a T+Nd",
      "semanas 3-5 do projeto", "após ATV007".
- "Tipo de janela" = "absoluta" ou "relativa".
- NÃO INVENTE DATAS ABSOLUTAS ONDE NÃO HÁ ÂNCORA. Se o usuário não
  declarou data de início, relativa é a única opção honesta.
- "Dependências resolvidas" = lista dos Atividade_IDs predecessores
  (deve bater com a coluna de dependências da Etapa 4).
- "No caminho crítico?" = "sim" se a atividade está na cadeia mais
  longa de dependências bloqueantes (aquela cujo atraso move o prazo
  final). Caso contrário "não". Sempre acompanhar de uma frase de
  justificativa.
- "Risco de atraso" = "alto | médio | baixo" + 1 frase nomeando o
  fator de risco (dependência externa, recurso crítico, validação
  institucional).
- "[suposição?]" = "sim" quando a janela, a duração, ou a dependência
  foi inferida.

Depois da tabela, escreva dois blocos obrigatórios:

<cadeia_critica>
Parágrafo de 5-8 linhas explicando a cadeia crítica identificada, os
pontos de fragilidade, e quaisquer [suposições] usadas para preencher
janelas. Se houver mais de uma cadeia concorrente (ex.: projeto com
múltiplas âncoras), explicite as duas e qual é a dominante.
</cadeia_critica>

<ritmos_externos_respeitados>
Lista dos ritmos externos aplicáveis ao projeto que foram considerados
no sequenciamento. Nomeie especificamente: calendários comunitários,
festividades (carnaval, festas juninas, natal), safras, calendário
escolar (início/fim de semestre, férias, provas), períodos eleitorais,
recessos legislativos, Ramadã ou outros ciclos religiosos, janelas
de enchente/seca. Se nenhum se aplica ao contexto do projeto,
declarar explicitamente: "nenhum ritmo externo aplicável ao contexto
deste projeto — justificativa: [frase]". NÃO deixe essa seção vazia.
</ritmos_externos_respeitados>
```

**Nota de design (divergência consciente do livro original):** O Caso 13 do livro *Inteligência Artificial para Impacto Social* pede um cronograma textual estilo Gantt com datas absolutas, duração em dias úteis e caminho crítico algorítmico. Esta skill diverge intencionalmente: datas absolutas só em volta de âncoras declaradas, caminho crítico identificado por raciocínio sobre dependências (não por cálculo PERT/CPM). Motivo: LLMs produzem *fake precision* quando forçados a fazer aritmética de datas e análise de caminho crítico sem base real — exatamente o tipo de work slop que esta skill combate. Ver `references/variantes.md` para adaptação quando há múltiplas âncoras externas concorrentes.

**Output esperado:** Tabela `<cronograma>` completa + bloco `<cadeia_critica>` de 5-8 linhas + bloco `<ritmos_externos_respeitados>` nomeando especificamente o que foi considerado.

### Etapa 6 — Capacidade humana *(opcional, default ligado)*

**Objetivo:** Distribuir as atividades entre a equipe declarada, identificar meses/períodos de pressão, apontar gaps de capacidade, e — criticamente — nomear trabalhos invisíveis que o plano não estava considerando (cuidado, mediação comunitária, tradução cultural, articulação política, facilitação em reuniões).

**Quando pular esta etapa:** se `<modulo_capacidade_humana>desligado</modulo_capacidade_humana>` foi declarado na Etapa 1. Casos típicos: trabalho individual, consultoria solo, equipe já dimensionada externamente por financiador ou parceiro. Se pulada, mencione explicitamente no output da Etapa 8 que a capacidade humana não foi analisada e é responsabilidade externa.

**Prompt sugerido:**

```
Com o cronograma da Etapa 5 e a lista de pessoas/funções que eu te
passei nos insumos, distribua as atividades e produza a análise de
capacidade humana. Use esta tabela Markdown:

<capacidade_humana>
| Pessoa/Função | % dedicação declarada | Atividades atribuídas (Atividade_IDs) | Período de pico | Cumulatividade com outros compromissos | Gap de capacidade? | [suposição?] |
</capacidade_humana>

Regras:
- Uma linha por pessoa nomeada ou função (ex.: "Maria Silva -
  Coordenação Pedagógica (40%)", "Assistente Técnico 1 (20%)",
  "Consultor Externo - M&E (pontual)").
- "% dedicação declarada" = percentual que o usuário declarou no
  início, NÃO um valor inventado.
- "Atividades atribuídas" = lista dos Atividade_IDs que essa pessoa
  executa ou lidera. Se a pessoa não tem atividades atribuídas, ela
  NÃO deve estar na tabela (questione por que foi listada como equipe).
- "Período de pico" = semana/mês em que a carga é maior para essa
  pessoa, considerando o cronograma da Etapa 5.
- "Cumulatividade com outros compromissos" = se o usuário declarou
  que a pessoa acumula outros projetos, qual é o impacto. Se não
  houve declaração, marque [suposição] e assuma que há cumulatividade.
- "Gap de capacidade?" = "sim | não". "Sim" quando a demanda do plano
  supera a dedicação declarada, considerando cumulatividade. Acompanhar
  de 1 frase explicando o gap (ex.: "40% declarado não cobre 60h de
  oficinas + 20h de sistematização no mês 3").
- "[suposição?]" = "sim" quando a atribuição foi inferida sem base
  explícita.

Depois da tabela, escreva uma <nota_capacidade_honesta> obrigatória
cobrindo os TRÊS pontos abaixo, cada um em parágrafo próprio:

<nota_capacidade_honesta>
(a) TRABALHOS INVISÍVEIS: Quais trabalhos o plano vai exigir mas que
    não estão nomeados na tabela? Exemplos: cuidado de crianças durante
    oficinas em territórios, mediação cultural com lideranças locais,
    tradução (linguística ou cultural) entre equipe técnica e
    comunidade, articulação política com atores externos, facilitação
    e moderação de reuniões, documentação fotográfica, comunicação em
    redes, hospedagem de participantes. Nomeie os que se aplicam E
    aponte se vão ficar invisíveis no plano ou se precisam ser
    atribuídos/terceirizados.

(b) CONCENTRAÇÃO DESPROPORCIONAL: Há concentração de trabalho em
    frontline, geralmente feminilizada, racializada ou terceirizada?
    Se sim, nomeie qual é o trabalho e quem carrega. Se não, declarar
    explicitamente: "nenhuma concentração desproporcional identificada".

(c) GAPS REAIS (NÃO A FULL-TIME FICTÍCIA): Quais gaps emergiram da
    análise considerando disponibilidade real (meio período,
    cuidadoras, cumulatividade com outros projetos), não uma fantasia
    de equipe 100% dedicada? Liste cada gap e proponha uma opção
    (redistribuição, redução de escopo, contratação adicional,
    renegociação de prazo).
</nota_capacidade_honesta>

Não suavize. Se o plano não cabe, o output diz isso.
```

**Output esperado:** Tabela `<capacidade_humana>` completa + `<nota_capacidade_honesta>` cobrindo os 3 pontos (trabalhos invisíveis, concentração desproporcional, gaps reais) em parágrafos separados.

### Etapa 7 — Aquisições *(opcional, default desligado)*

**Objetivo:** Derivar a lista de necessidades materiais a partir dos entregáveis, especificar requisitos mínimos, definir critério de aceite, mapear janelas de compra e entrega, e flagrar especificações que excluem fornecedores pequenos ou periféricos.

**Quando rodar esta etapa:** apenas se `<modulo_aquisicoes>ligado</modulo_aquisicoes>` foi declarado na Etapa 1. Casos típicos: projeto com compras de equipamento, materiais didáticos/insumos para oficinas, contratação de serviços técnicos externos, obras menores, aquisição de tecnologia.

**Prompt sugerido:**

```
Com base nos entregáveis (Etapa 3) e nas atividades (Etapa 4), derive
a lista de necessidades de aquisição. Use esta tabela Markdown:

<aquisicoes>
| Necessidade_ID | Entregável_ID | Item/Serviço | Tipo | Especificação mínima | Critério de aceite | Janela de compra sugerida | Janela de entrega necessária | Risco logístico | Flag de equidade | [suposição?] |
</aquisicoes>

Regras:
- Use Necessidade_IDs sequenciais: AQ001, AQ002, AQ003...
- "Tipo" = "bem" ou "serviço".
- "Especificação mínima" descreve o que o item/serviço precisa
  atender em até 3 frases. Inclui requisitos de desempenho,
  compatibilidade, normas. EVITE marcas específicas. Cite normas
  (NBR, ISO, regulamentações setoriais) apenas quando existirem e
  forem realmente aplicáveis.
- "Critério de aceite" é uma frase explicando como saber que a entrega
  atendeu a especificação.
- "Janela de compra sugerida" e "Janela de entrega necessária" seguem
  a mesma regra da Etapa 5: absoluta só em volta de âncoras, relativa
  caso contrário. Formato: "DD/MM/YYYY a DD/MM/YYYY" ou "T+Nd a T+Nd".
- "Risco logístico" identifica o principal risco (fornecedor único,
  prazo curto, certificação difícil, transporte complexo, sazonalidade).
- "Flag de equidade" é OBRIGATÓRIO e tem 3 valores possíveis:
  (1) "ok: [justificativa]" — a especificação não exclui fornecedores
      pequenos/periféricos; justifique em 1 frase por que.
  (2) "atenção: [risco específico]" — a especificação impõe exigência
      que PODE excluir fornecedores pequenos (certificação cara, volume
      mínimo alto, prazo apertado); especifique qual.
  (3) "excluidor: [motivo]" — a especificação claramente exclui
      fornecedores pequenos/periféricos; proponha mitigação.
  NUNCA deixar como "n/a".
- "[suposição?]" = "sim" quando a especificação ou janela foi inferida
  sem base nos insumos.

Depois da tabela, escreva um parágrafo curto (3-5 linhas) destacando:
- Necessidades críticas para o caminho crítico do cronograma
- Flags de equidade "excluidor" com mitigações propostas
- Necessidades marcadas como [suposição] que precisam de confirmação
  humana (quantidade, especificação, fornecedor disponível)
```

**Nota de design:** Se o projeto tem um número muito grande de itens de aquisição (mais de ~20), sugira ao usuário agrupar por categoria (ex.: "kit pedagógico da oficina", "infraestrutura tecnológica") e detalhar a especificação de categorias críticas — em vez de uma linha por item individual. A ideia é não inflar o output em detrimento da usabilidade.

**Output esperado:** Tabela `<aquisicoes>` completa com flag de equidade em todas as linhas + parágrafo de destaque para o que entra no caminho crítico e o que foi sinalizado como suposição.

### Etapa 8 — Consolidação, autoverificação e handoff

**Objetivo:** Produzir um documento consolidado único — **Plano de Estruturação do Projeto** — que junta os outputs das etapas anteriores em um artefato apresentável para governança interna, financiador ou conselho. Seguido de autoverificação estruturada contra os 6 princípios invioláveis e handoff explícito para validação humana.

**Prompt sugerido:**

```
Agora produza dois artefatos separados, claramente delimitados. Use
todas as saídas das Etapas 2 a 7. NÃO invente dados novos.

<artefato tipo="plano_consolidado">
# Plano de Estruturação do Projeto

## 1. Contexto e pergunta-alvo
[Retome o contexto capturado na Etapa 1. 1 parágrafo curto.]

## 2. Entregáveis
[Tabela consolidada da Etapa 3 — apenas linhas validadas, sem
observações de suposição soltas. Mantenha coluna "Beneficiários
impactados".]

## 3. Atividades e dependências
[Tabela consolidada da Etapa 4.]

## 4. Cronograma
[Tabela da Etapa 5. Mantenha tipo de janela (absoluta/relativa) em
cada linha para evitar confusão.]

### 4.1 Caminho crítico e riscos
[Parágrafo da Etapa 5 descrevendo a cadeia crítica.]

### 4.2 Ritmos externos respeitados
[Lista da Etapa 5.]

## 5. Plano de capacidade humana
[SOMENTE se a Etapa 6 rodou. Tabela + nota de capacidade honesta
consolidada em texto corrido.]
[Se a Etapa 6 NÃO rodou: uma frase declarando "capacidade humana
não analisada — responsabilidade externa" + nome do responsável
externo se aplicável.]

## 6. Plano de aquisições
[SOMENTE se a Etapa 7 rodou. Tabela consolidada + destaques de
equidade e caminho crítico.]
[Se a Etapa 7 NÃO rodou: "sem aquisições significativas no escopo
deste projeto".]

## 7. O que NÃO foi resolvido aqui (OBRIGATÓRIO)
[Seção de transparência. Lista, em bullets, de:
- Decisões pendentes que precisam de validação humana
- [suposições] não resolvidas e o que falta para resolvê-las
- Consultas externas necessárias (atores, normas, orçamento)
- Gaps de capacidade ou aquisições sinalizados e ainda não
  endereçados
- Riscos residuais que precisam ser monitorados na execução]

## 8. Nota de método
[3-5 linhas explicando quais etapas rodaram, quais foram puladas, e
a justificativa. Inclui ponto de entrada declarado (A ou B) e
módulos opcionais acionados.]
</artefato>

<artefato tipo="autoverificacao">
# Autoverificação contra princípios invioláveis

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência da verificação | Ajustes necessários |
|---|---|---|---|
| 1. Nunca inventar entregáveis, atividades ou requisitos | ... | ... | ... |
| 2. Datas absolutas só com âncoras reais | ... | ... | ... |
| 3. Critério de aceitação mensurável | ... | ... | ... |
| 4. Distinguir fato de inferência ([suposição]) | ... | ... | ... |
| 5. Plano honesto sobre trabalho e capacidade | ... | ... | ... |
| 6. Lente de equidade aplicada (beneficiários, ritmos, trabalhos invisíveis, capacidade real, aquisições não-excludentes) | ... | ... | ... |

Regras de preenchimento:
- "Cumprido?" = "Sim" apenas se você pode citar evidência concreta do
  próprio plano consolidado. "Parcial" = cumprido em parte com gap
  identificado. "Não" = violação real.
- "Evidência da verificação" cita seção/tabela/linha específica do
  plano que sustenta o "Sim" ou aponta onde está a falha.
- "Ajustes necessários" lista correções concretas. Deixar vazio só
  quando "Cumprido?" = "Sim" sem ressalvas.

Ao final da tabela, mensagem curta lembrando o humano de rodar o
checklist em `references/checklist.md` antes de publicar o plano.
</artefato>
```

**Checkpoint humano obrigatório antes de qualquer publicação/aprovação formal.** Ver seção "Checkpoints de validação humana".

**Output esperado:** (1) Documento "Plano de Estruturação do Projeto" com 8 seções numeradas, incluindo a seção 7 "O que NÃO foi resolvido aqui" obrigatória. (2) Tabela de autoverificação cobrindo os 6 princípios, cada linha com evidência concreta. (3) Apontamento explícito para `references/checklist.md`.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar para a próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop** — planos bonitos que desmoronam na execução.

- **Após Etapa 3 (Entregáveis).** Verifique:
  - Os entregáveis propostos (Modo A) ou validados (Modo B) refletem a intenção programática do projeto?
  - Os critérios de aceitação são de fato mensuráveis? Você consegue, lendo só o critério, saber quando o produto está pronto?
  - Os beneficiários nomeados são os grupos certos, ou há ausências estruturais (PCDs, pessoas em situação de rua, comunidades rurais, pessoas sem internet)?
  - As linhas marcadas com `[suposição]` são aceitáveis como suposição, ou precisam virar pergunta para outro ator antes de continuar?

- **Após Etapa 8 (Consolidação).** Verifique:
  - O plano consolidado bate com a realidade institucional (equipe, orçamento, capacidade de articulação)?
  - A seção "O que NÃO foi resolvido aqui" é honesta e específica, ou está minimizando gaps?
  - As decisões pendentes listadas têm dono e prazo para serem resolvidas?
  - Você rodou o checklist em `references/checklist.md` — seção técnica E seção de equidade — e está pronto(a) para assinar embaixo?

**Regra geral:** Se você não teve tempo de validar nesses dois pontos, o plano é rascunho interno. Não mande para financiador, conselho, parceiro ou secretaria até a validação ser feita.

## Falhas comuns

Anti-patterns que o modelo (ou o humano confiando no modelo sem checar) pode cometer:

1. **Cronograma de datas fake.** O modelo preenche "15/03/2026" e "22/05/2026" quando o usuário nunca declarou âncora. Resultado: plano parece preciso, mas é ficção apresentada como fato. *Mitigação:* Etapa 5 exige declaração explícita de âncoras antes de produzir qualquer data absoluta. Se você leu uma data absoluta no output e não se lembra de ter declarado a âncora, está errado — volte e corrija.

2. **Entregáveis genéricos sem critério mensurável.** "Relatório", "Oficinas", "Material de apoio". Sem formato, sem quantidade, sem qualidade mínima, sem quem valida. *Mitigação:* Etapa 3 rejeita linhas com critério vago e força reformulação. O teste simples: "se eu ler só o critério, eu sei quando o produto está pronto?". Se não, o critério não serve.

3. **Plano baseado em equipe full-time fictícia.** O modelo assume que todos os atores declarados estão disponíveis 40 horas por semana sem compromissos concorrentes. *Mitigação:* Etapa 6 exige declaração de percentual real e cumulatividade. Pergunte na entrada: "a Maria dedica 40% a este projeto, mas ela está em outros dois que também consomem 30% e 20% cada. A soma passa de 100%."

4. **Beneficiários abstratos.** "População atendida", "usuários", "comunidade", "jovens". Sem qualificador, sem geografia, sem recorte. A skill reproduz a abstração sem questionar. *Mitigação:* coluna "Beneficiários impactados" na Etapa 3 é obrigatória e exige grupos concretos. Rejeitar linhas com abstrações como primeiro passo antes do checkpoint humano.

5. **Aquisições com especificação que exclui fornecedores periféricos.** Certificações caras que só 3 empresas têm, volume mínimo que cooperativa pequena não consegue entregar, prazo de entrega que só fornecedor nacional atende. *Mitigação:* flag de equidade obrigatório na Etapa 7. Não aceita "n/a" — ou é "ok" com justificativa, ou é "atenção/excluidor" com mitigação proposta.

6. **Plano suavizado pra não brigar com a realidade.** Gaps de capacidade que ficam implícitos, riscos que somem na consolidação, dependências externas tratadas como certas. O modelo quer produzir um artefato "pronto" e por isso minimiza problemas. *Mitigação:* seção "O que NÃO foi resolvido aqui" na Etapa 8 é obrigatória e tem que ser específica. Autoverificação da Etapa 8 força revisão contra o Princípio 5 (plano honesto). Humano no checkpoint rejeita versões "limpas" demais.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa da skill num caso realista: OSC pequena nordestina recebendo edital federal para formação de 120 educadores populares em 4 territórios, Modo A (mandato amplo), com módulos de capacidade humana e aquisições ativados. Mostra input, saídas intermediárias de cada etapa, e o plano final consolidado.

- **`references/variantes.md`** — Adaptações do workflow base para contextos diferentes:
  1. **Modo B** (entregáveis pré-definidos em termo de referência aprovado)
  2. **Projeto só de trabalho humano** (advocacy, pesquisa, articulação política — Etapa 7 desligada)
  3. **Projeto aquisição-pesada** (governo municipal adquirindo infraestrutura — Etapa 6 mais leve)
  4. **Encadeamento com `theory-of-change`** (como passar output da ToC direto para a Etapa 2)
  5. **Encadeamento com `fundraising-pitch`** (como usar o plano consolidado como insumo de captação)
  6. **Múltiplas âncoras concorrentes** (projeto com ciclo eleitoral + calendário escolar + edital)

- **`references/checklist.md`** — Checklist pro humano validar o plano antes de publicar/apresentar. Seção técnica (critérios mensuráveis, dependências coerentes, âncoras reais, autoverificação honesta) + seção de equidade (beneficiários nomeados, ritmos externos, trabalhos invisíveis, equipe realista, aquisições não-excludentes).

---

*Baseada nos casos de uso 12 ("Entregáveis e Produtos"), 13 ("Detalhamento de Atividades e Cronograma") e 14 ("Planejamento de Recursos") do livro* Inteligência Artificial para Impacto Social *(Castro, 2025), fundidos em um único fluxo e modernizados com práticas atuais de prompting (XML tags, autoverificação estruturada, lente de equidade operacional, manejo explícito de "não sei", datas absolutas só em volta de âncoras reais — divergência consciente do formato original do livro, detalhada em `references/variantes.md`).*
