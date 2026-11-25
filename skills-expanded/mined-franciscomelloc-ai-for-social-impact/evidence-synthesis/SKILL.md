---
name: evidence-synthesis
description: Sintetiza múltiplos documentos em matriz comparativa com citações rastreáveis, divergências explícitas e análise de representatividade. Para briefings, revisões de literatura e análise comparativa de políticas públicas.
---

# Síntese de Evidências

## Quando usar esta skill

Esta skill apoia o trabalho de leitura crítica, comparação e síntese de múltiplos documentos quando a decisão precisa estar ancorada em evidência rastreável.

- Ler e comparar **múltiplos documentos** (3 ou mais) sobre um mesmo tema
- Produzir um **briefing executivo** ou nota para tomada de decisão baseada em evidência
- Mapear **convergências e divergências** entre diferentes fontes
- Preparar **revisão de literatura rápida** sobre política pública, programa ou intervenção
- Elaborar **análise comparativa** de experiências nacionais ou internacionais

Sinais típicos na conversa do usuário:

- "Tenho vários relatórios sobre X, preciso resumir"
- "Quais são os achados comuns entre esses estudos?"
- "Preciso de um briefing para o secretário sobre..."
- "O que essas fontes dizem sobre [tema]?"
- "Como [país/estado] implementou [política]? Tenho aqui 5 relatórios..."

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Acesso aos documentos** — PDFs carregados, links, ou textos colados no chat
2. **Pergunta-alvo clara** — pode ser refinada na Etapa 1, mas alguma ideia inicial é necessária
3. **Noção do público final** — a saída vai para uma dirigência executiva? Equipe técnica? Ambos? Isso muda o formato do produto final
4. **Tempo para validação humana** — a skill produz rascunhos; a qualidade final depende de revisão por especialista

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar evidência.** Se uma informação não está no material fornecido, escreva "não encontrado". Não preencha lacunas com conhecimento geral do modelo.

2. **Toda afirmação carrega citação.** Use autor-ano + página/seção quando disponível. Afirmação sem citação é afirmação frágil — não entra na saída final.

3. **Trechos literais entre aspas** para evidências decisivas. Paráfrase não substitui citação quando a formulação original importa (dados, definições, recomendações).

4. **Distinguir fato de inferência.** Marque toda inferência como `[suposição]` e explique em uma frase por que a inferência é razoável. Isso torna explícito o que é derivação sua, não das fontes.

5. **Divergências são tão importantes quanto convergências.** Não suavize conflitos para produzir uma narrativa coerente. Se as fontes discordam, a saída tem que mostrar isso.

6. **Lente de equidade e justiça social em todas as etapas.** Quais vozes estão representadas nas fontes? Quais estão ausentes? A análise captura impactos diferenciais sobre grupos marginalizados ou vulnerabilizados? A linguagem é inclusiva e não-estigmatizante? Ver `docs/equity-lens.md` para critérios operacionais. **Esta não é uma regra opcional** — skills de impacto social sem lente de equidade reproduzem desigualdades.

## O workflow (6 etapas)

O trabalho de síntese é organizado em 6 etapas sequenciais. Cada etapa tem um **objetivo** específico, um **prompt sugerido** pronto para copiar e um **output esperado** que serve de insumo para a etapa seguinte. Os prompts usam tags XML (`<escopo>`, `<documento>`, `<evidencia>`, `<analise>` etc.) para reduzir ambiguidade e ajudar o modelo a estruturar as respostas — é uma prática recomendada pela Anthropic para entradas estruturadas e saídas mais confiáveis. Não pule etapas: a qualidade da síntese final depende da disciplina de ir uma por uma, validando com humano nos checkpoints indicados.

### Etapa 1 — Configuração e escopo

**Objetivo:** Estabelecer as regras do trabalho com o modelo e alinhar o escopo da síntese (pergunta-alvo, recorte temporal, população de interesse, público da saída). Sem esse alinhamento, a coleta de evidências parte desfocada.

**Prompt sugerido:**

```
Você é pesquisador especialista em políticas públicas, com experiência em
síntese de evidências e revisão de literatura. Vou te enviar, nas próximas
mensagens, um conjunto de documentos para análise. Antes de começar, leia
e concorde com os princípios abaixo — eles valem para todas as respostas
desta conversa.

<principios>
1. Nunca inventar evidência. Se uma informação não está no material
   fornecido, escreva "não encontrado". Não preencha lacunas com
   conhecimento geral.
2. Toda afirmação carrega citação (autor-ano + página/seção quando
   disponível).
3. Trechos literais entre aspas para evidências decisivas. Paráfrase
   não substitui citação quando a formulação original importa.
4. Distinga fato de inferência. Marque toda inferência como
   [suposição] e explique em uma frase por que é razoável.
5. Divergências são tão importantes quanto convergências. Não suavize
   conflitos para produzir narrativa coerente.
6. Lente de equidade em todas as etapas: quem está representado, quem
   está ausente, linguagem inclusiva, impactos diferenciais.
</principios>

Agora, antes dos documentos, preciso que você confirme o escopo do
trabalho preenchendo o bloco abaixo com base no que eu já te contei.
Se algum campo estiver indefinido, pergunte.

<escopo>
  <pergunta_alvo>...</pergunta_alvo>
  <recorte_temporal>...</recorte_temporal>
  <populacao_interesse>...</populacao_interesse>
  <publico_saida>...</publico_saida>
</escopo>

Se concordar com as regras, responda "OK – regras definidas" e aguarde
os documentos.
```

**Output esperado:** Confirmação verbal ("OK – regras definidas") + bloco `<escopo>` preenchido, pronto para ser usado como referência nas etapas seguintes.

### Etapa 2 — Catalogação e representatividade

**Objetivo:** Inventariar os documentos recebidos e fazer uma primeira passada de análise de representatividade — quem são os autores, de onde vêm, que tipos de fonte estão presentes e quais lacunas já aparecem no conjunto.

**Prompt sugerido:**

```
Antes de extrair evidências, preciso de uma catalogação estruturada dos
documentos que você recebeu. Produza uma tabela Markdown com estas colunas:

| Doc_ID | Título | Autor(es) | Afiliação | Geografia | Ano | Tipo | Link/Arquivo | Observações |

Regras:
- Use Doc_IDs únicos e sequenciais: DOC001, DOC002, DOC003... Esses IDs
  serão usados em todas as etapas seguintes para rastreabilidade.
- "Tipo" pode ser: artigo científico, relatório técnico, nota de política,
  avaliação de impacto, documento governamental, estudo de caso etc.
- Se algum metadado não estiver disponível no documento, escreva
  "não encontrado" naquela célula. Não invente.

Depois da tabela, escreva uma nota de lacunas cobrindo explicitamente:

<analise>
  (a) Duplicatas ou documentos desatualizados que devam ser sinalizados.
  (b) Lacunas de representatividade percebidas no conjunto — por exemplo:
      "todas as fontes são do Sudeste brasileiro", "nenhuma perspectiva
      de usuárias do serviço", "ausência total de literatura pós-2020",
      "só há vozes acadêmicas, nenhuma de movimento social".
</analise>

Seja específico nas lacunas: nomear é mais útil do que generalizar.
```

**Output esperado:** Tabela Markdown completa de catalogação + nota de lacunas com duplicatas sinalizadas e ausências explicitamente nomeadas.

### Etapa 3 — Extração de evidências com citação literal

**Objetivo:** Extrair achados estruturados de cada documento, com citação verificável e flag explícito de generalização indevida. É a etapa que mais consome atenção — a qualidade da síntese final depende do rigor aqui.

**Prompt sugerido:**

```
Agora vamos extrair as evidências de cada documento. Processe UM DOCUMENTO
por resposta (se o conjunto for grande, agrupe em lotes de no máximo 5, um
por seção). Para cada documento, produza uma tabela Markdown assim:

<documento id="DOC00X">
Título: ...
Autor(es): ...
</documento>

| Achado (1-2 frases) | Categoria | Indicador | Trecho literal entre aspas | Citação (autor-ano, p./seção) | Flag_overgeneralização |

Regras:
- "Categoria" deve ser uma destas quatro: Contexto / Solução / Resultado /
  Recomendação. Se um achado não se encaixa, escolha a mais próxima e
  justifique entre parênteses.
- "Indicador" só preenchido quando houver número, métrica ou meta
  quantificada no documento. Caso contrário, "não encontrado".
- "Trecho literal entre aspas" é obrigatório para achados decisivos
  (dados, definições, recomendações). Copie textualmente do documento.
- "Citação" precisa carregar autor-ano e a página ou seção. Se não houver
  paginação, use "seção X", "cap. Y" ou "não encontrado".
- "Flag_overgeneralização" é "sim" quando o próprio documento generaliza
  de uma amostra limitada para afirmações amplas sobre uma população
  maior. Exemplo: pesquisa com 50 jovens em uma cidade concluindo sobre
  "a juventude brasileira". Nesse caso, explique em uma frase.
  Caso contrário, "não".

Ao final de cada documento, consolide os achados mais relevantes em uma
lista curta (máx. 5 bullets) com seus respectivos Doc_IDs.
```

**Output esperado:** Uma tabela de evidências por documento, cada uma com citações literais verificáveis e flags de overgeneralização; ao final da etapa, um conjunto consolidado pronto para ser cruzado na Etapa 4.

### Etapa 4 — Matriz comparativa e análise de lacunas

**Objetivo:** Consolidar as evidências das etapas anteriores em uma matriz que torne explícitas as convergências (quando 2 ou mais fontes concordam), as divergências (quando fontes discordam) e — crucialmente — quem está ausente da base de evidências.

**Prompt sugerido:**

```
Com base nas tabelas de extração da Etapa 3, produza agora uma matriz
comparativa consolidada. Use este formato Markdown:

| Categoria | Convergências (2+ fontes) | Divergências | Evidências (Doc_IDs com autor-ano) | O que falta saber | Quem está ausente |

Regras de preenchimento:
- "Categoria" usa as mesmas quatro categorias da Etapa 3
  (Contexto / Solução / Resultado / Recomendação).
- "Convergências" só lista pontos sustentados por pelo menos 2 fontes
  independentes. Se só uma fonte afirma algo, isso NÃO é convergência —
  vai para "O que falta saber" ou fica na tabela de origem.
- "Divergências" descreve explicitamente o conflito. Não suavize. Se as
  fontes discordam sobre eficácia, número, público-alvo ou recomendação,
  escreva exatamente qual é o desacordo.
- "Evidências" referencia os Doc_IDs mais autor-ano, nunca só o ID solto.
- "O que falta saber" lista perguntas abertas pela base atual — onde os
  dados são insuficientes, desatualizados ou inconclusivos.
- "Quem está ausente" é COLUNA OBRIGATÓRIA. Liste grupos, perspectivas
  ou contextos que não estão capturados no conjunto de fontes: por
  exemplo, "usuárias do serviço público", "pessoas com deficiência",
  "comunidades rurais", "gestão municipal", "avaliações independentes
  pós-2022". Se uma categoria não tem ausências evidentes, escreva
  "nenhuma lacuna aparente" e justifique.

Ao final da matriz, escreva um parágrafo de 5-8 linhas sintetizando os
padrões principais encontrados e as lacunas mais críticas para a
pergunta-alvo da Etapa 1.
```

**Output esperado:** Matriz Markdown completa, com a coluna "Quem está ausente" preenchida de forma específica, seguida de um parágrafo de síntese dos padrões e das lacunas mais críticas.

### Etapa 5 — Produtos por público

**Objetivo:** Traduzir a análise das etapas anteriores em dois produtos adaptados a públicos distintos — dirigência executiva (precisa decidir rápido) e equipe técnica (precisa implementar e justificar).

**Prompt sugerido:**

```
Agora produza DOIS documentos separados, claramente delimitados por
cabeçalhos. Use a matriz e as evidências das Etapas 3 e 4. Não invente
dados novos.

<produto tipo="resumo_executivo">
# Resumo executivo (1 página)

- **Objetivo:** 1 parágrafo curto (contexto + pergunta-alvo).
- **Mensagens-chave:** 5 a 7 bullets, cada um ancorado em evidência
  (autor-ano entre parênteses).
- **Riscos:** 3 riscos concretos da decisão, com fonte.
- **Decisões sugeridas:** 3 opções de caminho, com trade-offs
  explícitos (o que se ganha, o que se abre mão).
- **Nota de método:** 3 linhas dizendo quantos documentos foram
  analisados, de que tipo, e qual foi o recorte.
- **Limitações e representatividade (OBRIGATÓRIO):** seção nomeando
  quem está ausente da base, o que os dados não capturam, e em que
  medida a recomendação é generalizável. Sem esta seção, o resumo
  está incompleto.
</produto>

<produto tipo="anexo_tecnico">
# Anexo técnico (2-4 páginas)

- **Método:** como os documentos foram selecionados, catalogados e
  analisados (referencie as 6 etapas da skill).
- **Tabela das 10 evidências mais relevantes:** achado, categoria,
  trecho literal entre aspas, citação completa.
- **Matriz de convergências e divergências:** reutilize a matriz da
  Etapa 4, sem cortar a coluna "Quem está ausente".
- **Limitações expandidas:** discussão mais detalhada das lacunas,
  vieses do conjunto e riscos de overgeneralização sinalizados na
  Etapa 3.
- **Próximos passos:** dados a coletar, atores a consultar, perguntas
  de pesquisa abertas.
- **Referências:** lista completa em norma ABNT.
</produto>

Mantenha os dois produtos autocontidos — cada um deve ser legível
independentemente.
```

**Output esperado:** Dois documentos Markdown claramente delimitados — um resumo executivo de 1 página com seção obrigatória de limitações e um anexo técnico de 2-4 páginas com método, evidências, matriz e referências ABNT.

### Etapa 6 — Autoverificação e handoff humano

**Objetivo:** Revisar a saída contra os 6 princípios invioláveis antes de entregar ao humano para validação final. A autoverificação não substitui o humano — prepara o material para a revisão dele.

**Prompt sugerido:**

```
Antes de entregar os produtos da Etapa 5, faça uma autoverificação
estruturada contra os 6 princípios invioláveis definidos na Etapa 1.
Produza uma tabela Markdown nesse formato:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência da verificação | Ajustes necessários |

Cubra EXPLICITAMENTE os 6 princípios, um por linha:

1. Nunca inventar evidência
2. Toda afirmação carrega citação
3. Trechos literais entre aspas para evidências decisivas
4. Distinguir fato de inferência (uso de [suposição])
5. Divergências tratadas, não suavizadas
6. Lente de equidade aplicada (representação, ausência, linguagem,
   impactos diferenciais)

Regras:
- Para cada linha, cite pelo menos um trecho concreto do produto final
  que sustenta o "cumprido" — ou aponte exatamente onde está a falha.
- "Parcial" é resposta válida e até desejável: indique o que está ok
  e o que ainda precisa de ajuste.
- Se detectar que algum princípio foi violado, proponha a correção
  específica (em qual etapa, qual parágrafo, qual ajuste).

Feche com uma mensagem curta lembrando o humano de rodar o checklist
de validação em `references/checklist.md` antes de publicar a síntese.
```

**Output esperado:** Relatório de autoverificação em tabela Markdown cobrindo os 6 princípios, com evidências concretas e ajustes sugeridos, mais um apontamento explícito para o checklist humano em `references/checklist.md`.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar para a próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop**.

- **Após Etapa 2 (Catalogação)** — Verifique: a catalogação cobre todos os documentos que você enviou? Os metadados estão corretos? As lacunas de representatividade que o modelo identificou batem com sua percepção do conjunto?

- **Após Etapa 4 (Matriz comparativa)** — Verifique: as convergências e divergências refletem fielmente o que as fontes dizem? As citações foram abertas e conferidas contra os originais? A coluna "Quem está ausente" captura os grupos relevantes?

- **Após Etapa 6 (Autoverificação)** — Verifique: o relatório de autoverificação aponta pontos reais de fragilidade? Antes de publicar, rode o checklist em `references/checklist.md`.

**Regra geral:** Se você não teve tempo de validar, não publique. Use a saída como rascunho interno até a validação ser feita.

## Falhas comuns

Anti-patterns que o modelo (ou o humano confiando no modelo sem checar) pode cometer:

1. **Paráfrase travestida de citação** — o modelo escreve "segundo Silva (2023)..." mas o Silva não disse exatamente aquilo. *Mitigação:* exigir trechos literais entre aspas para evidências decisivas.

2. **Síntese sem divergências** — todas as fontes parecem concordar magicamente. Em política pública real, isso quase nunca acontece. *Mitigação:* se a Etapa 4 não produziu divergências, questione — provavelmente a comparação foi superficial.

3. **Alucinação de número de página** — o modelo inventa `p. 23` para uma citação em um documento que nem tem paginação. *Mitigação:* quando não houver página, exigir "seção" ou "artigo" ou "não encontrado".

4. **Generalização indevida reproduzida** — o documento diz "em uma amostra de 50 jovens em Belo Horizonte", e a síntese escreve "os jovens brasileiros pensam X". *Mitigação:* flag de overgeneralização na Etapa 3 + revisão humana.

5. **Invisibilização de grupos ausentes** — as fontes não falam sobre pessoas com deficiência, e a síntese também não menciona. Ausência vira silêncio. *Mitigação:* coluna "Quem está ausente" na Etapa 4 é obrigatória.

6. **Confusão entre fonte e análise** — o modelo atribui às fontes conclusões que são interpretação do próprio modelo. *Mitigação:* marcar inferências como `[suposição]` consistentemente.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa desta skill em um caso realista (5 documentos sobre Educação Profissional e Tecnológica). Mostra input, saídas intermediárias de cada etapa e produtos finais.

- **`references/variantes.md`** — Adaptações do workflow base para contextos diferentes: conjuntos grandes (30+ documentos), documentos em inglês, poucos documentos (≤3), documentos com qualidade de OCR ruim.

- **`references/checklist.md`** — Checklist pro humano validar a saída antes de publicar. Inclui seção técnica (citações, aspas, divergências) e seção de equidade (ausência, linguagem, generalização, impactos diferenciais).

---

*Baseada no caso de uso 1 ("Síntese de Evidências") do livro* Inteligência Artificial para Impacto Social *(Castro, 2025), modernizada com práticas atuais de prompting (XML tags, autoverificação estruturada, lente de equidade operacional, manejo explícito de "não sei").*
