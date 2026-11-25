---
name: evidence-gathering
description: Reúne e cura fontes documentais a partir de URLs ou busca por tópico. Produz catálogo pronto para handoff com evidence-synthesis e análise de lacunas de representatividade. Para revisão de literatura e pesquisa exploratória.
---

# Reunião e Curadoria de Evidências

## Quando usar esta skill

Esta skill apoia a **descoberta e curadoria de fontes** antes da síntese. É o passo anterior ao `evidence-synthesis` no fluxo de pesquisa: você precisa das fontes certas antes de poder sintetizá-las.

Use quando o usuário:

- **Tem um tópico ou pergunta de pesquisa** e não sabe ainda quais fontes consultar
- **Tem uma lista de URLs** e precisa processar, catalogar e curar antes de sintetizar
- **Tem um tópico + algumas URLs iniciais** e quer expandir a base de evidências
- Precisa preparar uma **revisão de literatura** sobre política pública, programa ou intervenção
- Quer produzir um **catálogo pronto pra passar pra `evidence-synthesis`** sem retrabalho

Sinais típicos na conversa do usuário:

- "Preciso de fontes sobre [tema] pra um briefing"
- "Tenho essas 5 URLs, dá pra processar?"
- "Como encontrar evidência sobre [política] no Brasil?"
- "Quais são os principais estudos sobre [tópico]?"
- "Quero preparar uma revisão de literatura rápida sobre X"

**Padrão recomendado:** use esta skill primeiro (gathering), depois passe a saída direto para `evidence-synthesis` (análise comparativa e produção de briefings).

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Pergunta-alvo ou tópico de pesquisa** — pode ser amplo no início, será refinado na Etapa 1
2. **Decidir o modo de operação** — tem URLs específicas? precisa buscar por tópico? os dois?
3. **Critérios mínimos de escopo** — período temporal, idiomas aceitáveis, tipos de fonte preferidos/excluídos, N-alvo aproximado
4. **Acesso à web na plataforma usada** — Claude Code com WebFetch, Claude.ai com browsing, ChatGPT com web search, ou MCPs como Tavily/Brave Search. Se não houver, a skill entra em modo fallback e exige paste manual
5. **Tempo para validação humana** — como em toda skill deste repo, a saída é rascunho; revisão humana é obrigatória antes de publicar

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar fontes ou metadados.** Se uma URL não carrega, escreva "erro de acesso"; se um metadado não existe, escreva "não encontrado". Nunca adivinhe autores, datas, instituições ou URLs. Alucinar fonte é o pior erro desta skill.

2. **Toda afirmação sobre uma fonte carrega a própria fonte.** URL completa + data de acesso registradas explicitamente em cada linha do catálogo. Isso dá rastreabilidade e cobre parcialmente o problema de link rot.

3. **Avaliações de credibilidade são explícitas e justificadas.** Nunca "alta/média/baixa" solto — sempre com justificativa em uma frase citando sinal concreto (ex: "peer reviewed em journal Q1", "opinião publicada sem evidência primária", "governo federal mas sem data recente"). "Confio" não é evidência.

4. **Lacunas de representatividade são nomeadas com grupos concretos.** "Faltam vozes" não serve. Tem que dizer "faltam vozes de usuárias do serviço", "falta perspectiva de municípios rurais do Norte", "nenhuma fonte em espanhol sobre tema latino-americano". Especificidade é obrigatória.

5. **Saída final deve ser diretamente consumível pela Etapa 2 de `evidence-synthesis`.** Formato exato da tabela (Doc_ID, Título, Autor, Afiliação, Geografia, Ano, Tipo, Link/Arquivo, Observações). Sem retrabalho de formato. Este é o princípio específico desta skill e não aparece em outras.

6. **Lente de equidade e justiça social em todas as etapas.** Quais vozes estão sendo buscadas? Quais estão sendo encontradas? A análise agregada de lacunas é substantiva ou cosmética? Ver `docs/equity-lens.md` para critérios operacionais. **Esta não é uma regra opcional** — a Etapa 5 existe especificamente para operacionalizar equidade no conjunto.

## O workflow (6 etapas)

O trabalho de reunião e curadoria é organizado em 6 etapas sequenciais. Cada etapa tem um **objetivo** específico, um **prompt sugerido** pronto para copiar e um **output esperado** que serve de insumo para a etapa seguinte. Os prompts usam tags XML (`<escopo>`, `<modo>`, `<candidato>`, `<analise>` etc.) para reduzir ambiguidade. O modo de operação (URL list / tópico / híbrido) é decidido na Etapa 1 e molda o comportamento da Etapa 2; as Etapas 3-6 são unificadas para os três modos.

### Etapa 1 — Configuração, escopo e modo

**Objetivo:** Estabelecer as regras do trabalho, listar os 6 princípios invioláveis, e decidir o modo de operação junto com o escopo rico.

**Prompt sugerido:**

```
Você é pesquisador especialista em políticas públicas, com experiência em
revisão de literatura e curadoria de fontes. Vou te pedir, nas próximas
mensagens, que reúna e cure um conjunto de fontes documentais. Antes de
começar, leia e concorde com os princípios abaixo — eles valem para todas
as respostas desta conversa.

<principios>
1. Nunca inventar fontes ou metadados. Se uma URL não carrega, escreva
   "erro de acesso"; se um metadado não existe, escreva "não encontrado".
   Nunca adivinhe autores, datas, instituições ou URLs.
2. Toda afirmação sobre uma fonte carrega a própria fonte — URL completa
   + data de acesso em cada linha do catálogo.
3. Avaliações de credibilidade são explícitas e justificadas: nada de
   "alta/média/baixa" solto. Sempre com justificativa em 1 frase citando
   sinal concreto.
4. Lacunas de representatividade são nomeadas com grupos concretos.
   "Faltam vozes" não serve — especifique qual grupo, qual geografia,
   qual idioma, qual tipo de voz.
5. Saída final deve ser diretamente consumível pela Etapa 2 de
   evidence-synthesis (formato exato de tabela, sem retrabalho).
6. Lente de equidade e justiça social em todas as etapas: quem está
   sendo buscado, quem está sendo encontrado, quem está ausente.
</principios>

Agora preciso que você confirme o escopo e o modo de operação preenchendo
o bloco abaixo com base no que eu já te contei. Se algum campo estiver
indefinido, pergunte antes de avançar.

<escopo>
  <modo>url_list | topico | hibrido</modo>
  <pergunta_alvo>...</pergunta_alvo>
  <periodo>...</periodo>
  <idiomas>pt, en, es, ...</idiomas>
  <tipos_desejados>...</tipos_desejados>
  <tipos_excluidos>...</tipos_excluidos>
  <n_alvo>...</n_alvo>
  <repositorios_especificos>(opcional)</repositorios_especificos>
</escopo>

Se concordar com as regras, responda "OK – regras definidas" e aguarde as
URLs (modo url_list/hibrido) ou confirmação para iniciar a busca (modo
topico).
```

**Output esperado:** Confirmação verbal ("OK – regras definidas") + bloco `<escopo>` preenchido com modo e critérios, pronto para orientar a Etapa 2.

### Etapa 2 — Coleta inicial

**Objetivo:** Reunir o pool bruto de candidatos. O comportamento ramifica conforme o modo de operação definido na Etapa 1.

**Prompt sugerido:**

```
Agora vamos coletar o pool bruto de candidatos. Siga o ramo correspondente
ao <modo> definido na Etapa 1:

<modo nome="url_list">
Para cada URL no bloco <urls> abaixo, faça fetch e extraia metadados
básicos: título, autor(es), ano, fonte, URL canônica. Se a URL não
carregar, registre "erro de acesso" na coluna Status_acesso e não
preencha outros campos com palpites.
</modo>

<modo nome="topico">
Busque na web usando termos derivados da <pergunta_alvo> e seus sinônimos
(português e outros idiomas definidos em <idiomas>). Retorne entre 15 e 25
candidatos, priorizando <tipos_desejados> e evitando <tipos_excluidos>.
Se <repositorios_especificos> estiver preenchido, priorize-os.
</modo>

<modo nome="hibrido">
Execute os dois ramos acima. Para os candidatos vindos de URLs
fornecidas, marque Origem="url_fornecida". Para os vindos de busca,
marque Origem="busca_web".
</modo>

FALLBACK OBRIGATÓRIO: Se você não tem acesso à web (WebFetch, browsing,
web search ou MCP), pare esta etapa, explique a limitação ao usuário em
uma frase, e peça que ele cole manualmente o conteúdo bruto dos
candidatos. Não finja ter acessado.

Formate a saída como tabela Markdown com estas colunas:

| Candidato_ID | Título | Autor(es) | Fonte (URL) | Ano | Origem | Status_acesso |

Regras:
- Candidato_IDs sequenciais neste formato: CAND001, CAND002, CAND003...
  (serão promovidos a DOC_IDs na Etapa 6).
- Onde faltar metadado, escreva "não encontrado". Não invente.
- Status_acesso: "ok", "erro de acesso", "paywall", "timeout" etc.
```

**Output esperado:** Pool bruto em tabela Markdown com 15-25 linhas (tipicamente), IDs no formato CAND00X, metadados mínimos e Status_acesso registrado em cada linha.

### Etapa 3 — Avaliação por relevância e qualidade

**Objetivo:** Avaliar cada candidato em 4 dimensões, sem ainda filtrar nada. A filtragem é responsabilidade da Etapa 4.

**Prompt sugerido:**

```
Agora vamos avaliar cada candidato do pool da Etapa 2 em quatro dimensões.
NÃO filtre nada nesta etapa — todos os candidatos continuam na tabela.
A filtragem é responsabilidade da Etapa 4.

Para cada <candidato> avalie:

1. Relevância — alta / média / baixa, SEMPRE acompanhada de justificativa
   em 1 frase. "Alta" solto é proibido. Exemplo válido: "alta: trata
   diretamente do efeito de transferência de renda sobre trabalho
   infantil no Nordeste".

2. Tipo de fonte — duas sub-classificações:
   (a) primária / secundária / terciária
   (b) acadêmica / governamental / imprensa / ONG / blog / outro

3. Sinais de credibilidade — avalie de forma explícita:
   peer review? autoridade institucional? data recente? metodologia
   descrita? conflito de interesse aparente? Resuma em 1 frase citando
   o sinal concreto. Se não houver sinal detectável, escreva
   "não encontrado".

4. Primeira passada de equity — registre: afiliação do(s) autor(es),
   geografia do estudo/objeto, idioma da fonte, e quando possível
   a posição do autor em relação ao tema (pesquisador externo, pessoa
   afetada, gestor público etc.).

Produza uma tabela expandida com as colunas da Etapa 2 mais:

| ... | Relevância | Tipo de fonte | Sinais de credibilidade | Afiliação | Geografia | Idioma |

Regras:
- Nenhuma avaliação "nua". Toda célula de Relevância e Credibilidade
  vem com justificativa curta.
- Use "não encontrado" quando uma dimensão não tem sinal recuperável.
- Mantenha TODOS os candidatos — esta etapa não exclui nada.
```

**Output esperado:** Tabela expandida com as colunas da Etapa 2 somadas às 4 dimensões de avaliação, ainda contendo todos os candidatos do pool bruto.

### Etapa 4 — Deduplicação e filtragem

**Objetivo:** Produzir a shortlist cortando duplicatas, aplicando critérios de exclusão e removendo qualidade fraca. As exclusões ficam VISÍVEIS em uma tabela separada para auditoria.

**Prompt sugerido:**

```
Agora vamos produzir a shortlist. Execute na ordem:

1. Deduplicação:
   - Identifique o mesmo documento aparecendo em URLs diferentes
     (ex: versão no site do autor + versão no repositório institucional).
   - Identifique versões antigas vs. novas (ex: working paper vs. versão
     publicada; preprint vs. peer-reviewed).
   - Mantenha APENAS a versão canônica (preferencialmente a mais recente
     ou a peer-reviewed). Anote os aliases/duplicatas descartados na
     coluna Observações da linha canônica.

2. Aplicação de critérios de escopo:
   - Corte candidatos que caem em <tipos_excluidos>.
   - Corte candidatos fora do <periodo> definido na Etapa 1.

3. Filtros de qualidade:
   - Candidatos com relevância "baixa" E credibilidade fraca = excluir.
   - Candidatos com erro de acesso irrecuperável = excluir (anote na
     coluna Motivo_exclusao).

4. Corte para o <n_alvo> aproximado definido na Etapa 1, priorizando
   relevância alta + credibilidade forte + diversidade de vozes
   (equity lens já aqui).

Produza DUAS tabelas separadas:

**Tabela A — Shortlist final**
Use as colunas da Etapa 3 + adicione `Decisao_final: MANTER`.

**Tabela B — Excluídos**
Use as colunas da Etapa 3 + adicione `Motivo_exclusao` com 1 frase
concreta (ex: "duplicata de CAND007 – versão preprint", "fora do
período 2015-2025", "blog opinativo sem evidência primária",
"erro de acesso irrecuperável após 3 tentativas").

REGRA CRÍTICA: NÃO delete os excluídos da saída. Eles permanecem visíveis
na Tabela B para o usuário auditar suas decisões de curadoria. Exclusão
silenciosa é antipadrão desta skill.
```

**Output esperado:** Duas tabelas Markdown separadas — Tabela A (shortlist final, ~N-alvo linhas) e Tabela B (excluídos com Motivo_exclusao sempre preenchido).

### Etapa 5 — Análise de lacunas de representatividade

**Objetivo:** Olhar a shortlist como um todo (não candidato a candidato) e aplicar a equity lens, nomeando lacunas com grupos concretos.

**Prompt sugerido:**

```
Agora trate a Tabela A (shortlist final) da Etapa 4 como um conjunto.
A pergunta central é: este conjunto responde à pergunta-alvo de forma
representativa, ou reproduz vieses estruturais?

Produza um bloco <analise> cobrindo explicitamente 5 dimensões:

<analise>
  <geografia>
    Qual a distribuição geográfica? Há concentração em uma região,
    país ou centro urbano? Quais geografias estão ausentes? Nomeie.
  </geografia>

  <idioma>
    Há dominância do inglês? Para temas latino-americanos, há fontes
    em português e espanhol? Há ausência crítica de um idioma
    relevante ao recorte?
  </idioma>

  <tipo_de_voz>
    A shortlist é só acadêmica? Só governamental? Há pessoas diretamente
    afetadas, usuárias do serviço, movimentos sociais, gestores locais?
    Quais vozes estão ausentes?
  </tipo_de_voz>

  <temporalidade>
    O período está enviesado (ex: tudo pré-2015)? Há gaps temporais
    relevantes? Há viés de recência excluindo literatura fundacional?
  </temporalidade>

  <interseccionalidade>
    Para o tema específico, quais vieses combinados (gênero + raça +
    classe + território + deficiência etc.) são relevantes e estão
    ausentes ou sub-representados?
  </interseccionalidade>
</analise>

Depois da análise, se alguma lacuna for crítica, produza um bloco de
recomendações de busca adicional:

<recomendacoes>
  - Busca adicional sugerida: termos, repositórios, idiomas
  - Tipo de fonte a incluir que está faltando
  - Vozes específicas a procurar ativamente
</recomendacoes>

REGRA: "faltam vozes" é insuficiente. Nomeie grupos concretos. Exemplos
válidos: "faltam vozes de mulheres rurais do semiárido nordestino",
"falta perspectiva de gestores municipais de municípios <20 mil hab.",
"nenhuma fonte em espanhol sobre programa equivalente no Cone Sul".
Especificidade é obrigatória.
```

**Output esperado:** Bloco `<analise>` com as 5 dimensões preenchidas com especificidade + bloco `<recomendacoes>` com sugestões concretas de busca adicional quando lacunas críticas foram identificadas.

### Etapa 6 — Catálogo final (formato handoff para evidence-synthesis)

**Objetivo:** Produzir a saída final no formato EXATO da Etapa 2 do `evidence-synthesis`, pronta para copy/paste, mais nota de entrega e relatório de autoverificação.

**Prompt sugerido:**

```
Agora produza a saída final em TRÊS partes claramente delimitadas. Esta é
a saída que vai ser passada direto para a Etapa 2 do evidence-synthesis,
então o formato tem que bater exatamente.

**Parte 1 — Catálogo no formato evidence-synthesis Etapa 2**

Tabela Markdown com estas colunas, nesta ordem, exatamente:

| Doc_ID | Título | Autor(es) | Afiliação | Geografia | Ano | Tipo | Link/Arquivo | Observações |

Regras:
- Doc_IDs sequenciais: DOC001, DOC002, DOC003... (promova os CAND_IDs
  mantidos na Tabela A da Etapa 4).
- "Tipo" usa vocabulário compatível com evidence-synthesis: artigo
  científico, relatório técnico, nota de política, avaliação de impacto,
  documento governamental, estudo de caso etc.
- "Observações" é a coluna que carrega informação agregada das etapas
  anteriores: relevância percebida, flags de credibilidade relevantes,
  origem (url_fornecida/busca_web), alertas de equidade específicos
  daquela linha. Mantenha cada Observação em 1-2 frases curtas.
- Onde um metadado não existe no original, escreva "não encontrado".
  Não invente.

**Parte 2 — Nota de entrega**

Um parágrafo de 6-10 linhas cobrindo:
- quantas fontes entraram na shortlist final (Parte 1) vs. quantas foram
  excluídas na Etapa 4 (e os principais motivos de exclusão);
- um resumo muito curto da análise de lacunas da Etapa 5 (as 2-3 lacunas
  mais críticas);
- recomendações acionáveis ao usuário (ex: rodar busca adicional em X
  repositório, considerar fontes em espanhol, validar Doc_IDs Y e Z
  manualmente antes de sintetizar).

**Parte 3 — Relatório de autoverificação**

Tabela Markdown neste formato:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência da verificação | Ajustes necessários |

Cubra EXPLICITAMENTE os 6 princípios invioláveis, um por linha:

1. Nunca inventar fontes ou metadados
2. Toda afirmação sobre uma fonte carrega a própria fonte (URL + data)
3. Avaliações de credibilidade explícitas e justificadas
4. Lacunas de representatividade nomeadas com grupos concretos
5. Saída final no formato exato da Etapa 2 de evidence-synthesis
6. Lente de equidade operacional em todas as etapas

Para cada linha, cite um trecho concreto da saída que sustenta o
"Sim", ou aponte exatamente onde está a falha se for "Parcial" ou "Não".
"Parcial" é resposta válida e até desejável.

Feche com a mensagem: "Antes de publicar ou passar pra evidence-synthesis,
rode o checklist de validação em references/checklist.md."
```

**Output esperado:** Três partes claramente delimitadas — (1) catálogo Markdown com colunas exatas do handoff, (2) nota de entrega de 6-10 linhas, (3) tabela de autoverificação cobrindo os 6 princípios com evidência concreta e lembrete do checklist humano.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar para a próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop**.

- **Após Etapa 2 (Coleta inicial)** — Verifique: todas as URLs fornecidas foram tentadas? Os metadados extraídos batem com os documentos reais? Se foi modo tópico, os candidatos retornados são de fato relevantes (e não spam SEO ou blogs opinativos)?

- **Após Etapa 4 (Deduplicação e filtragem)** — Verifique: os critérios de exclusão foram aplicados consistentemente? Nenhum candidato relevante foi cortado por engano? Os motivos de exclusão são defensáveis? A coluna de excluídos está visível (não deletada)?

- **Após Etapa 6 (Catálogo final + autoverificação)** — Verifique: o catálogo está no formato exato da evidence-synthesis Etapa 2? A nota de entrega nomeia lacunas concretas? O relatório de autoverificação apontou pontos reais de fragilidade? Antes de passar pra evidence-synthesis, rode o checklist em `references/checklist.md`.

**Regra geral:** Se você não teve tempo de validar, não passe pra etapa seguinte. Use a saída como rascunho interno até a validação ser feita.

## Falhas comuns

Anti-patterns específicos desta skill:

1. **URL alucinada ou inventada** — modelo cria URL que parece plausível mas não existe. *Mitigação:* Princípio 1 + verificação de acesso explícita na Etapa 2; se a URL retorna erro, registrar "erro de acesso" em vez de fingir sucesso.

2. **Avaliação de credibilidade sem justificativa** — "fonte confiável" sem dizer por quê. *Mitigação:* Princípio 3 + Etapa 3 exige justificativa em 1 frase para cada avaliação.

3. **Lacunas genéricas** — "faltam vozes diversas" em vez de "falta perspectiva de usuárias do SUS em municípios rurais". *Mitigação:* Princípio 4 + Etapa 5 explicita exigência de especificidade.

4. **Exclusões silenciosas** — cortar candidato sem registrar motivo. *Mitigação:* Etapa 4 mantém tabela de excluídos com coluna `Motivo_exclusao` sempre visível.

5. **Falso sucesso de coleta** — modelo reporta que achou N fontes sem ter acesso à web. *Mitigação:* fallback explícito na Etapa 2 — se não há web access, pare e peça paste manual em vez de fingir.

6. **Over-trust em sinais de autoridade** — "é do governo" = "é bom". *Mitigação:* Etapa 3 avalia em 4 dimensões (relevância, tipo, credibilidade, equity); peer review ≠ autoridade estatal ≠ testemunho comunitário; cada um tem peso em contextos diferentes.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa desta skill em um caso realista (modo tópico, revisão de literatura sobre impactos de gênero de políticas de transferência de renda no Brasil). Mostra input, saídas intermediárias das 6 etapas e produto final pronto pra handoff.

- **`references/variantes.md`** — Adaptações do workflow base para contextos diferentes: plataformas sem acesso à web, temas com muita "sujeira" de SEO/opinião, literatura cinza (governamental/multilateral difícil de indexar), tópicos nichados com poucas fontes.

- **`references/checklist.md`** — Checklist pro humano validar a saída antes de publicar ou passar pra evidence-synthesis. Inclui seção técnica (URLs, metadados, dedup, formato handoff) e seção de equidade (diversidade geográfica, idiomática, de vozes, intersecional).

---

**Próximo passo natural:** depois de rodar esta skill e validar o catálogo com o checklist, passe a saída da Etapa 6 (Parte 1) diretamente como input da Etapa 2 do `evidence-synthesis`. O formato é idêntico por design.

---

*Nova skill do repositório `ai-for-social-impact` (v0.2.0), complementar à `evidence-synthesis`. Baseada em gap identificado durante o desenvolvimento da primeira skill; não tem equivalente direto no livro* Inteligência Artificial para Impacto Social *(Castro, 2025), mas segue o mesmo framework de princípios (equity lens operacional, anti-hallucination, autoverificação estruturada, checkpoints humanos obrigatórios).*
