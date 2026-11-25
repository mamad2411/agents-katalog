---
name: technical-note-writing
description: Produz rascunhos de notas técnicas e narrativas de dados a partir de dossiê heterogêneo (dados, documentos, diagnósticos, exemplar institucional). Com revisão de conformidade factual, normativa, terminológica e de equidade.
---

# Redação de Notas Técnicas e Narrativas de Dados

## Quando usar esta skill

Esta skill apoia a **redação estruturada de rascunhos** de notas técnicas e narrativas de dados a partir de um dossiê heterogêneo de insumos. É a etapa seguinte ao trabalho de evidência: depois que você tem dados, documentos de referência e diagnósticos, precisa produzir um texto analítico ancorado neles.

Use quando o usuário:

- Precisa **redigir uma nota técnica** para subsidiar decisão de uma dirigência (secretaria, ministério, conselho de OSC, diretoria)
- Tem **uma planilha de dados** e precisa traduzir os números em texto analítico (narrativa de dados)
- Tem um **dossiê misto** (dados + normativos + relatórios prévios + ata de reunião) e precisa consolidar em uma nota única
- Quer **adaptar a voz institucional** de um órgão específico e tem um exemplar de nota anterior pra ancorar o estilo
- Precisa de **revisão estruturada** (factual, normativa, terminológica, equidade) antes de entregar o texto para um decisor

Sinais típicos na conversa do usuário:

- "Preciso escrever uma nota técnica sobre X para a secretária"
- "Tenho essa planilha de dados, dá pra virar texto?"
- "Como transformar esse diagnóstico em nota para decisão?"
- "Preciso de um rascunho de nota técnica seguindo o estilo do nosso órgão"
- "Preciso contar o que esses números significam para um público não-técnico"

**Padrão recomendado (cadeia completa):** use `evidence-gathering` para descoberta de fontes → `evidence-synthesis` para análise comparativa → `technical-note-writing` para redação do produto final. A variante da cadeia está documentada em `references/variantes.md`.

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Dossiê mínimo** — pelo menos um insumo concreto (uma planilha, um documento, um diagnóstico). Nota técnica sem dossiê vira opinião travestida de análise
2. **Pergunta-alvo clara** — pode ser refinada na Etapa 1, mas alguma ideia do que a nota precisa responder é necessária
3. **Noção do decisor final** — quem vai ler e decidir muda tom, tamanho e profundidade técnica do texto
4. **Gênero de saída escolhido** — nota técnica ou narrativa de dados (decidido na Etapa 1; parecer e minuta ficam em variantes)
5. **Exemplar institucional (opcional, recomendado)** — uma nota técnica anterior do mesmo órgão permite à skill mimetizar o estilo sem virar texto genérico de IA
6. **Tempo para validação humana** — a skill produz rascunho; a qualidade final depende de revisão técnica, jurídica quando aplicável, e do checklist em `references/checklist.md`

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar evidência.** Se uma informação não está no dossiê, escreva "não encontrado". Não preencha lacunas com conhecimento geral do modelo. Dossiê é a fronteira do que pode ser afirmado.

2. **Toda afirmação carrega citação.** Use Doc_ID ou linha de planilha + localização específica (página, seção, célula). Afirmação sem âncora não entra no rascunho final — vai pra `[suposição]` ou é cortada.

3. **Trechos literais entre aspas** para citações normativas (artigos de lei, decretos), definições legais e números decisivos. Paráfrase não substitui citação quando a formulação original importa — e quando é lei, costuma importar.

4. **Distinguir fato de inferência.** Marque toda inferência como `[suposição]` e explique em uma frase por que é razoável. Isso torna explícito o que é derivação do modelo, não do dossiê.

5. **Lente de equidade e justiça social operacional em todas as etapas.** Linguagem não-estigmatizante, impactos diferenciais por grupo nomeados, ausências reconhecidas, sem generalização indevida. Aplicada concretamente na Etapa 3 (separação diagnóstico/recomendação) e como eixo obrigatório da Etapa 5. Ver `docs/equity-lens.md`. **Esta não é uma regra opcional.**

6. **[específico desta skill] Rastreabilidade linha-a-linha.** Toda frase do rascunho final é rastreável a um insumo concreto do dossiê (Doc_ID ou linha de planilha). Frases sem âncora ficam marcadas `[suposição]` com justificativa ou são cortadas na Etapa 5. Este princípio ataca o risco nº 1 do gênero: prosa fluente de IA sem base factual.

## O workflow (6 etapas)

O trabalho de redação é organizado em 6 etapas sequenciais. Cada etapa tem um **objetivo** específico, um **prompt sugerido** pronto para copiar e um **output esperado** que serve de insumo para a etapa seguinte. Os prompts usam tags XML (`<escopo>`, `<perfil_estilo>`, `<estrutura>`, `<secao>`, `<revisao>` etc.) para reduzir ambiguidade e estruturar respostas confiáveis. Não pule etapas: o checkpoint humano obrigatório **após a Etapa 3** (pré-redação) é o ponto de maior economia de retrabalho de todo o workflow — aprovar o outline antes de gastar tokens escrevendo o draft evita rascunhos inteiros jogados fora.

### Linha de base de estilo (aplicada SEMPRE)

Antes de qualquer etapa, a skill carrega um **piso de qualidade de prosa** — vale com ou sem exemplar institucional. Fórmula: **estrutura e tom do World Bank, disciplina de frase do The Economist, sem a opinião do Economist.** Quando há exemplar institucional (Etapa 1), o `<perfil_estilo>` ajusta **sobre** este piso; não o substitui.

As 10 regras resumidas:

1. **Primeira frase carrega o ponto** (*bottom line up front*). Abertura de cada seção entrega a conclusão da seção, não o caminho até ela.
2. **Sujeito concreto + verbo ativo.** Diga quem fez o quê. Cortar voz passiva que apaga o agente.
3. **Todo número com ano-base, recorte e unidade.** *Quando*, *onde*, *em que unidade* — os três âncoras.
4. **Parágrafos curtos (≤5 linhas).** Uma ideia por parágrafo, um parágrafo por ideia.
5. **Siglas definidas na primeira ocorrência.** *"Plano Nacional de Educação (PNE)"* uma vez; depois, só "PNE".
6. **Zero filler burocrático.** Cortar "no âmbito de", "no que tange a", "faz-se necessário", "em linhas gerais", "cabe destacar que", "visando a", "tendo em vista que" e similares. Lista completa em `references/style-guide.md`.
7. **Exemplo concreto vence abstração.** Nomear escolas, unidades, valores, datas e pessoas quando o dossiê permite.
8. **Adjetivos avaliativos só com evidência que os sustente.** "Crítico", "urgente", "grave", "preocupante" só depois de a frase anterior estabelecer a régua.
9. **Uma ideia por frase.** Sem ", considerando que, ..., tendo em vista, ..., e visando a, ...".
10. **Cabeçalho → frase-síntese → corpo.** Todo heading é seguido por uma frase (no máximo duas) que sintetiza a seção inteira.

Expansão com exemplos antes/depois, lista completa de filler e tratamento do exemplar institucional: `references/style-guide.md`. Este piso ataca diretamente a **Falha Comum nº 4** ("Estilo genérico de IA") — leia o arquivo inteiro antes de escrever o primeiro rascunho.

### Etapa 1 — Configuração, escopo e estilo institucional

**Objetivo:** Estabelecer as regras, listar os 6 princípios invioláveis, decidir o gênero de saída, capturar escopo rico (pergunta-alvo, decisor, órgão, prazo, extensão) e — se houver — absorver o perfil de estilo do exemplar institucional.

**Prompt sugerido:**

```
Você é redator(a) especialista em nota técnica e análise de dados para
governo e sociedade civil, com experiência em produção de rascunhos para
dirigências executivas e conselhos. Vou te enviar, nas próximas mensagens,
um dossiê de insumos (dados, documentos, diagnósticos) e, opcionalmente,
um exemplar de nota anterior. Antes de começar, leia e concorde com os
princípios abaixo — eles valem para todas as respostas desta conversa.

<principios>
1. Nunca inventar evidência. Se uma informação não está no dossiê, escreva
   "não encontrado". Não preencha lacunas com conhecimento geral.
2. Toda afirmação carrega citação — Doc_ID ou linha de planilha.
3. Trechos literais entre aspas para citações normativas, definições
   legais e números decisivos.
4. Distinguir fato de inferência. Marque toda inferência como [suposição]
   e justifique em uma frase.
5. Lente de equidade em todas as etapas.
6. Rastreabilidade linha-a-linha: toda frase do rascunho final aponta a
   um insumo concreto do dossiê. Frases sem âncora viram [suposição]
   justificada ou são cortadas.
</principios>

Antes do dossiê, confirme o escopo preenchendo o bloco abaixo. Se algum
campo estiver indefinido, pergunte.

<escopo>
  <genero>nota_tecnica | narrativa_de_dados</genero>
  <pergunta_alvo>...</pergunta_alvo>
  <decisor_final>...</decisor_final>
  <orgao_emissor>...</orgao_emissor>
  <prazo>...</prazo>
  <extensao_alvo>... páginas</extensao_alvo>
  <restricoes_especiais>...</restricoes_especiais>
</escopo>

Linha de base de estilo (aplicada SEMPRE, com ou sem exemplar):
estrutura/tom do World Bank + disciplina de frase do Economist, sem
opinião do Economist. As 10 regras resumidas — (1) BLUF primeira frase;
(2) sujeito concreto + verbo ativo; (3) número com ano-base, recorte e
unidade; (4) parágrafos ≤5 linhas; (5) siglas definidas na primeira
ocorrência; (6) zero filler burocrático ("no âmbito de", "no que tange
a", "faz-se necessário", "em linhas gerais", "cabe destacar", "visando
a", "tendo em vista que", "em razão de", "em que pese"); (7) exemplo
concreto > abstração; (8) adjetivo avaliativo só com régua ancorada;
(9) uma ideia por frase; (10) cabeçalho → frase-síntese → corpo.
Expansão e exemplos antes/depois em references/style-guide.md.

Se o usuário forneceu um exemplar institucional, extraia um perfil de
estilo em bullets curtos (estrutura de seções, terminologia recorrente,
tom, convenções de citação, tamanho médio de parágrafo) no bloco
<perfil_estilo>. O perfil ajusta SOBRE a linha de base — não a
substitui. Se o exemplar viola sistematicamente alguma das 10 regras
(ex: usa passiva pesada ou filler), registre no bloco uma linha do
tipo "nota do órgão tem tendência a X; rascunho corrige sem perder tom
institucional". Se não houver exemplar, pule o bloco <perfil_estilo> —
a linha de base sozinha já é o piso.

Se concordar, responda "OK – regras definidas" e aguarde o dossiê.
```

**Output esperado:** Confirmação "OK – regras definidas" + bloco `<escopo>` preenchido + (se houver exemplar) bloco `<perfil_estilo>` em bullets curtos descrevendo o que será mimetizado **acima da linha de base**, mais eventuais correções quando o exemplar viola o piso.

### Etapa 2 — Organização do dossiê

**Objetivo:** Catalogar os insumos heterogêneos do dossiê com IDs rastreáveis tipados (DADO/DOC/DIAG) e fazer uma primeira passada de análise de representatividade.

**Prompt sugerido:**

```
Antes de estruturar o texto, catalogue os insumos do dossiê numa tabela
Markdown única com IDs tipados para rastreabilidade:

- DADO001, DADO002... para planilhas e tabelas (registre colunas principais
  e recorte temporal na coluna Conteúdo-chave)
- DOC001, DOC002... para documentos de referência (normativos, estudos,
  documentos governamentais)
- DIAG001, DIAG002... para diagnósticos narrativos prévios (relatórios,
  atas, despachos, pareceres anteriores)

Formato da tabela:

| ID | Tipo | Título/Descrição | Origem | Ano | Conteúdo-chave | Observações |

Regras:
- Se um metadado não estiver disponível, escreva "não encontrado" na célula.
  Não invente.
- Na coluna Conteúdo-chave, resuma em uma linha o que cada insumo carrega
  (ex: "matrículas e evasão 2023-2025 por escola").

Depois da tabela, escreva uma nota curta de lacunas de representatividade
em <analise>:

<analise>
  (a) Quais vozes/grupos estão ausentes do dossiê?
     (ex: "nenhuma perspectiva de estudantes ou famílias",
      "só dados agregados, sem recorte racial",
      "diagnóstico é todo da gestão, sem campo")
  (b) Vieses estruturais dos insumos (ex: "fontes só do município-sede",
     "diagnósticos refletem prioridades de 2023, já defasados")
  (c) Cobertura temporal e geográfica (gaps explícitos)
</analise>

Seja específico nas lacunas: nomear é mais útil do que generalizar.
```

**Output esperado:** Tabela Markdown de catalogação com IDs tipados + bloco `<analise>` nomeando lacunas concretas de representatividade do dossiê.

### Etapa 3 — Estrutura argumentativa

**Objetivo:** Antes de escrever uma linha do texto final, definir o esqueleto argumentativo da nota (tese, seções, ordem lógica, mapeamento evidência→seção) com **separação estrita entre diagnóstico e recomendação**.

**Prompt sugerido:**

```
Agora, ANTES de redigir, defina a estrutura argumentativa da nota. Não
escreva prosa ainda — só o esqueleto. Use o formato XML abaixo:

<estrutura>
  <tese_central>
    (1 frase: qual é a tese central que a nota sustenta?)
  </tese_central>

  <secao id="1" tipo="diagnostico">
    <titulo>...</titulo>
    <objetivo>(1 frase sobre o que esta seção estabelece)</objetivo>
    <evidencias>DADO001, DOC002, DIAG001</evidencias>
    <pontos>
      - bullet 1 (sem prosa, só o ponto)
      - bullet 2
    </pontos>
  </secao>

  <secao id="2" tipo="diagnostico">...</secao>
  <secao id="3" tipo="analise">...</secao>
  <secao id="4" tipo="recomendacao">
    <titulo>...</titulo>
    <objetivo>...</objetivo>
    <evidencias>DIAG001, DOC001</evidencias>
    <pontos>
      - recomendação 1
      - recomendação 2
    </pontos>
  </secao>
</estrutura>

REGRA CRÍTICA (operacionalização do princípio 5):
- Seções tipo="diagnostico" e tipo="recomendacao" são SEMPRE separadas.
- Uma seção NÃO pode misturar "os dados mostram X" com "o órgão deve
  fazer Y" no mesmo parágrafo. Essas frases vivem em seções diferentes,
  ancoradas em evidências diferentes.
- Se você se pegar misturando, divida a seção em duas.

Depois da estrutura, produza um mapa evidência → seção em tabela:

| ID do insumo | Aparece em | Como contribui |

Aponte onde cada DADO/DOC/DIAG é usado no texto final. Se algum insumo
não aparece em nenhuma seção, sinalize (pode ser sinal de que a estrutura
não aproveita o dossiê, ou de que o insumo não é relevante pra pergunta).

CHECKPOINT HUMANO OBRIGATÓRIO após esta etapa. Peça ao usuário para
revisar e aprovar o outline ANTES de avançar para a Etapa 4.
```

**Output esperado:** Bloco `<estrutura>` em XML com tese central + seções tipadas (diagnóstico/análise/recomendação) + mapa evidência→seção em tabela. Aguarda aprovação humana antes de prosseguir.

### Etapa 4 — Redação do rascunho

**Objetivo:** Produzir o texto completo seguindo o outline aprovado na Etapa 3, com citações inline rastreáveis e marcações `[suposição]` onde aplicável.

**Prompt sugerido:**

```
Com o outline aprovado, agora redija o rascunho completo em Markdown.
Regras do rascunho:

1. Siga EXATAMENTE a estrutura aprovada na Etapa 3 — não invente seções,
   não fusione seções, não reordene sem aprovação.

2. Cada parágrafo referencia explicitamente pelo menos uma âncora inline:
   - Citação de dado: "(DADO001, linha 34)" ou "(DADO001, coluna Evasão_2024)"
   - Citação de documento: "(DOC002, art. 23)" ou "(DOC001, p. 45)"
   - Citação de diagnóstico: "(DIAG001, seção 3.2)"

3. Citações normativas usam trecho literal entre aspas + identificação
   exata do dispositivo:
   "(...)" — Lei Federal 13.005/2014, art. 2º, inciso III

4. Inferências suas vêm marcadas [suposição: explicação curta].
   Ex: "[suposição: a correlação observada entre turno noturno e
   evasão em DIAG001 sugere, mas não prova, causalidade direta]"

5. Estilo do rascunho aplica a LINHA DE BASE (10 regras carregadas na
   Etapa 1) e, se houver exemplar, ESPELHA o <perfil_estilo> acima do
   piso. Não copia frases do exemplar — plágio é proibido, mimetização
   é obrigatória. Se o exemplar viola a linha de base (ex: filler
   burocrático sistemático), o rascunho corrige sem perder tom.

6. Disciplina de frase do Economist aplicada parágrafo a parágrafo:
   - primeira sentença de cada seção carrega a conclusão da seção
     (BLUF — bottom line up front)
   - sujeito concreto + verbo ativo (cortar voz passiva que apaga
     o agente)
   - todo número traz ano-base + recorte + unidade
   - parágrafo nunca passa de 5 linhas (quebre por ideia)
   - zero filler burocrático ("no âmbito de", "no que tange a",
     "faz-se necessário", "em linhas gerais", "cabe destacar",
     "visando a", "tendo em vista que", "em razão de", "em que pese")
   - adjetivo avaliativo ("crítico", "urgente", "grave",
     "preocupante") só depois da frase anterior estabelecer a régua
   - uma ideia por frase — sem orações subordinadas encadeadas

7. Se o gênero escolhido é narrativa_de_dados, o texto dá ênfase a
   descrever padrões, tendências e LIMITAÇÕES dos números, com linguagem
   acessível a não-especialistas. Se é nota_tecnica, adota tom executivo
   e carrega fundamentação normativa mais explícita.

8. NÃO misture diagnóstico com recomendação — respeite a separação
   definida na Etapa 3.

Produza o rascunho completo na resposta.
```

**Output esperado:** Rascunho completo em Markdown seguindo o outline aprovado, com âncoras inline em cada parágrafo e marcações `[suposição]` onde houver inferência.

### Etapa 5 — Revisão de conformidade (4 eixos)

**Objetivo:** Passada única de revisão cobrindo quatro eixos simultaneamente — factual, normativa, terminológica, equidade — antes do handoff humano.

**Prompt sugerido:**

```
Agora faça uma passada de revisão sobre o rascunho da Etapa 4, cobrindo
SIMULTANEAMENTE os quatro eixos abaixo. Não é quatro passadas — é uma
passada só avaliando os quatro ângulos.

<eixos_de_revisao>

EIXO 1 — FACTUAL:
- Toda afirmação numérica bate com o insumo citado?
- Ano, unidade, recorte geográfico e fonte estão corretos?
- Há inferência estatística não autorizada (média, comparação,
  projeção) que não está no dado original?
- Números no rascunho são iguais aos números no DADO_ID citado?

EIXO 2 — NORMATIVA:
- Citações legais conferem com o texto exato da lei/decreto/portaria?
- Artigos, parágrafos e incisos estão corretos?
- Nome do dispositivo está correto (ex: "Lei 13.005/2014" não
  "Lei nº 13.005/14")?
- Há lei revogada sendo citada como vigente?

EIXO 3 — TERMINOLÓGICA E DE ESTILO:
- Terminologia é consistente com o <perfil_estilo> do exemplar
  (se houver)? E com o glossário técnico do setor?
- Siglas definidas na primeira ocorrência?
- Acrônimos institucionais corretos?
- Linha de base de estilo cumprida frase a frase? Varredura
  obrigatória (ver references/style-guide.md):
    * BLUF — primeira frase de cada seção entrega a conclusão?
    * voz ativa dominante, passiva só quando o agente não importa?
    * todo número tem ano-base + recorte + unidade?
    * parágrafos todos ≤5 linhas?
    * filler burocrático cortado ("no âmbito de", "no que tange
      a", "faz-se necessário", "em linhas gerais", "cabe destacar",
      "visando a", "tendo em vista que", "em razão de", "em que
      pese", "no sentido de")?
    * adjetivos avaliativos só depois de régua ancorada?
    * uma ideia por frase?
- Estilo do rascunho soa "IA genérica" ou soa voz institucional
  disciplinada (WB na estrutura, Economist na frase)?

EIXO 4 — EQUIDADE:
- Linguagem é inclusiva e não-estigmatizante? ("grupo vulnerabilizado"
  em vez de "vulnerável"; "estudante em situação de abandono" em vez
  de "evadido")
- Impactos diferenciais por grupo (gênero, raça, renda, território,
  deficiência) são nomeados quando os dados permitem?
- Ausências do dossiê (identificadas na Etapa 2) são reconhecidas
  explicitamente no texto?
- Há generalização indevida? ("a população" vs "a amostra")
- O texto posterga análise de raça, gênero ou classe com "vamos
  resolver o geral primeiro"?
- Recomendações consideram capacidades diferenciais de implementação
  pelos grupos afetados?

</eixos_de_revisao>

Produza a saída em DOIS blocos:

BLOCO A — Diff estruturado em tabela:

| Eixo | Trecho original | Problema identificado | Trecho revisado | Justificativa |

Uma linha por ajuste. Inclua PELO MENOS um ajuste por eixo (se algum
eixo não precisou de ajuste, escreva uma linha "nenhum ajuste
necessário — evidência: ..." com prova concreta).

BLOCO B — Versão revisada completa do rascunho

Aplique todos os ajustes do BLOCO A ao rascunho da Etapa 4. Esta versão
revisada é o insumo da Etapa 6 (autoverificação) — NÃO a versão original.
```

**Output esperado:** Tabela-diff estruturada (Bloco A) + versão revisada completa do rascunho (Bloco B), pronta para a autoverificação final.

### Etapa 6 — Autoverificação e handoff humano

**Objetivo:** Revisar a versão da Etapa 5 contra os 6 princípios invioláveis antes de entregar ao humano. A autoverificação não substitui o humano — prepara o material para a revisão.

**Prompt sugerido:**

```
Antes de entregar a nota, faça uma autoverificação estruturada contra
os 6 princípios invioláveis. Produza uma tabela Markdown:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência da verificação | Ajustes necessários |

Cubra EXPLICITAMENTE os 6 princípios, um por linha:

1. Nunca inventar evidência
2. Toda afirmação carrega citação (Doc_ID + localização)
3. Trechos literais entre aspas para citações normativas
4. Distinguir fato de inferência ([suposição] com justificativa)
5. Lente de equidade aplicada
6. Rastreabilidade linha-a-linha (toda frase aponta a insumo do dossiê)

Regras:
- Para cada linha, cite PELO MENOS UM trecho concreto da versão
  revisada da Etapa 5 que sustenta o "Sim" — OU aponte exatamente
  onde está a falha.
- "Parcial" é resposta válida e até desejável. Indique o que está ok
  e o que ainda precisa de ajuste.
- Se detectar violação de algum princípio, proponha correção
  específica (em qual seção, qual parágrafo, qual ajuste).

Fecha com mensagem curta:

"Autoverificação concluída. Antes de publicar ou entregar ao decisor,
rode o checklist humano em references/checklist.md. A saída é rascunho
até a validação humana passar."
```

**Output esperado:** Relatório de autoverificação em tabela Markdown cobrindo os 6 princípios com evidências concretas + apontamento explícito para o checklist humano.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar para a próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop**.

- **Após Etapa 2 (Organização do dossiê)** — Verifique: todos os insumos que você enviou foram catalogados? Os IDs tipados fazem sentido (DADO/DOC/DIAG)? O conteúdo-chave resume corretamente cada insumo? As lacunas nomeadas em `<analise>` batem com sua percepção do dossiê?

- **Após Etapa 3 (Estrutura argumentativa) — CHECKPOINT MAIS CRÍTICO DO WORKFLOW** — Antes de gastar tokens escrevendo o rascunho, aprove o outline. Verifique: a tese central é defensável com o dossiê? As seções estão bem delimitadas? **Diagnóstico e recomendação estão em seções SEPARADAS?** O mapa evidência→seção cobre todos os insumos relevantes? Este checkpoint sozinho economiza mais retrabalho do que os outros dois juntos — não pule.

- **Após Etapa 6 (Autoverificação)** — Verifique: a versão revisada da Etapa 5 é a que está no relatório? A autoverificação apontou pontos reais de fragilidade (ou ficou só no "Sim" cosmético)? Antes de publicar, rode o checklist em `references/checklist.md`.

**Regra geral:** Se você não teve tempo de validar, não publique. Use a saída como rascunho interno até a validação ser feita.

## Falhas comuns

Anti-patterns específicos de redação de notas técnicas (diferentes dos anti-patterns de síntese e de gathering):

1. **Prosa fluente sem base** — LLM escreve texto com ar autoritativo mas sem âncora concreta a insumo do dossiê. É o risco nº 1 do gênero — texto soa bom, mas não sustenta auditoria. *Mitigação:* Princípio 6 (rastreabilidade linha-a-linha) + eixo factual da Etapa 5 + checklist humano.

2. **Diagnóstico misturado com recomendação** — "os dados mostram X, portanto o órgão deve fazer Y" como se Y fosse derivação automática do dado. Disfarça juízo político como técnico. *Mitigação:* separação estrita de seções por tipo na Etapa 3 + checkpoint humano obrigatório pré-redação.

3. **Citação normativa inventada** — LLM escreve "conforme art. 23 da Lei 8.080/90" quando o artigo fala outra coisa, ou a lei foi revogada, ou o número está errado. *Mitigação:* princípio 3 (trecho literal entre aspas obrigatório para citações legais) + eixo normativo da Etapa 5 exige verificação contra fonte.

4. **Estilo genérico de IA** — texto soa "ChatGPT", perde voz institucional do órgão; frases longas, advérbios vazios, jargão translingual, estruturas "por um lado... por outro lado", parágrafos-bloco, voz passiva pesada, filler burocrático, adjetivos avaliativos sem régua. *Mitigação:* linha de base de estilo (10 regras carregadas na Etapa 1, em `references/style-guide.md`) aplicada SEMPRE — piso de qualidade valendo com ou sem exemplar institucional; perfil de estilo do exemplar ajusta SOBRE o piso na Etapa 1; eixo terminológico expandido da Etapa 5 faz varredura frase a frase contra as 10 regras. O piso é **estrutura/tom do World Bank + disciplina de frase do Economist, sem a opinião do Economist**.

5. **Linguagem estigmatizante herdada das fontes** — documento fonte usa "populações carentes", "evadidos", "analfabetos funcionais", e a skill reproduz sem questionar. Ausência vira silêncio; termo desatualizado vira reprodução. *Mitigação:* eixo equidade da Etapa 5 operacionaliza `docs/equity-lens.md` — revisão ativa de termos, não cópia acrítica.

6. **Números travestidos de certeza** — "a taxa é 12,4%" sem intervalo, ano-base, recorte geográfico ou fonte; média de uma amostra pequena virando afirmação sobre "a população". *Mitigação:* princípio 2 (toda afirmação carrega citação) + eixo factual da Etapa 5 exige ano-base e recorte explícitos em cada número.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa desta skill em um caso realista (nota técnica sobre evasão no ensino médio em um município fictício, com dossiê contendo planilha de matrículas, PNE, plano municipal de educação, diagnóstico interno e exemplar institucional). Mostra input, saídas intermediárias das 6 etapas e rascunho final pronto pro checklist humano.

- **`references/variantes.md`** — Adaptações do workflow base para contextos diferentes: narrativa de dados pura (só planilhas), dossiê vindo da cadeia `evidence-gathering → evidence-synthesis`, parecer (fora do core, com disclaimer jurídico), minuta de ato normativo (fora do core, com disclaimer reforçado) e ausência de exemplar institucional.

- **`references/style-guide.md`** — Linha de base de estilo aplicada SEMPRE: estrutura e tom do World Bank, disciplina de frase do The Economist, sem a opinião do Economist. 10 regras com exemplos antes/depois, tabela de filler burocrático a cortar, tratamento do exemplar institucional como ajuste SOBRE o piso. Ataca diretamente a Falha Comum nº 4 ("Estilo genérico de IA").

- **`references/checklist.md`** — Checklist pro humano validar o rascunho antes de publicar. Três blocos: técnico (rastreabilidade, auditoria factual, separação diagnóstico/recomendação, formato, siglas), estilo (varredura das 10 regras da linha de base) e equidade (linguagem, impactos diferenciais, ausências reconhecidas, generalização, participação). Inclui regra de ouro: itens críticos não marcados = não publique.

---

**Padrão recomendado (cadeia completa):** `evidence-gathering` (descoberta de fontes) → `evidence-synthesis` (matriz comparativa + briefings) → `technical-note-writing` (redação do produto final). As três skills foram desenhadas como padrão ensinável de workflow analítico em trabalho de impacto social.

---

*Baseada nos casos de uso 8 ("Narrativas de Dados") e 9 ("Notas Técnicas e Minutas") do livro* Inteligência Artificial para Impacto Social *(Castro, 2025), modernizados com práticas atuais de prompting (XML tags, autoverificação estruturada, lente de equidade operacional, manejo explícito de "não sei", rastreabilidade linha-a-linha).*
