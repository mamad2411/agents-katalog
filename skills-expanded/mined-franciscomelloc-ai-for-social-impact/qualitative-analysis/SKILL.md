---
name: qualitative-analysis
description: Clusteriza respostas abertas, entrevistas e texto livre em temas emergentes com trechos literais rastreáveis, análise opcional de sentimento e estratificação por grupo. Para pesquisas, percepções públicas e diagnósticos qualitativos.
---

# Análise Qualitativa

## Quando usar esta skill

Esta skill apoia o trabalho de codificação temática, análise de sentimento e estratificação por grupo em corpora de texto livre — quando a decisão precisa estar ancorada em trechos literais rastreáveis, não em impressões agregadas.

- Clusterizar **respostas abertas de pesquisa** (survey) em temas com padrões por subgrupo
- Analisar **comentários públicos** em canais institucionais (ouvidoria, redes de atendimento)
- Codificar **transcrições de entrevistas ou grupos focais** com atenção a dinâmicas de poder
- Extrair padrões de **texto livre genérico** (relatórios de campo, diários, registros de atendimento)
- Produzir **diagnósticos qualitativos** que alimentam desenho ou revisão de política

Sinais típicos na conversa do usuário:

- "Tenho 300 respostas abertas de uma pesquisa com usuárias, quais são os temas?"
- "Precisamos entender o que as pessoas estão reclamando na ouvidoria"
- "Rodei 15 entrevistas, preciso codificar antes da reunião"
- "Quais são as queixas mais comuns neste conjunto de comentários?"
- "Preciso de um diagnóstico qualitativo pra embasar a próxima versão do programa"

Relação com outras skills do repositório:

- Use `evidence-synthesis` quando o input são múltiplos documentos estruturados (relatórios, artigos, normativos)
- Use `evidence-gathering` antes de `evidence-synthesis` quando você precisa descobrir as fontes primeiro
- Esta skill (`qualitative-analysis`) é para **texto livre produzido por pessoas** como objeto direto de análise — não documentos institucionais

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Corpus carregado ou colado** — respostas, transcrições, comentários em formato texto (não imagens, não áudio bruto). Se houver áudio, transcrever antes.
2. **Pergunta-alvo clara** — o que você quer entender sobre o corpus. Pode ser refinada na Etapa 1, mas alguma ideia inicial é necessária.
3. **Consciência dos metadados disponíveis** — quais campos demográficos acompanham o corpus (bairro, idade, sexo, etc.) OU reconhecimento explícito de que não há metadados. Declarar "não tenho" é legítimo; fingir que tem é proibido.
4. **Tempo para validação humana** — a skill produz rascunhos codificados; a qualidade final depende de revisão humana em pelo menos **3 checkpoints obrigatórios** durante o workflow.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar trechos, temas ou sentimentos.** Se um tema não aparece no corpus, não crie. Se uma resposta não tem sentimento claro, marque "ambivalente" ou "neutro".

2. **Toda afirmação temática carrega trecho literal rastreável.** Use o formato: `Tema X é ilustrado por R042 ("trecho exato")`. Nunca "alguns respondentes mencionaram..." — rastreabilidade é condição de verdade.

3. **Distinguir tema manifesto de tema latente.** Manifesto = aparece explicitamente no texto. Latente = interpretação analítica. Sempre marcar qual é qual; temas latentes carregam justificativa de 1 frase explicando a inferência.

4. **Nunca inferir demografia a partir de sinais indiretos.** Não usar nome, estilo de linguagem, região, erros ortográficos ou qualquer sinal indireto pra categorizar respondentes em grupos demográficos. Se o dado não existe no dataset, declare explicitamente como lacuna e preserve a declaração até o output final. Inferência demográfica é caminho direto pra viés estrutural. **Este princípio é específico desta skill.**

5. **Divergências dentro de um tema são tão importantes quanto convergências.** Não colapsar opiniões contrárias dentro do mesmo tema — nomear sub-padrões e tensões internas. Consenso falso é mais perigoso que divergência explícita.

6. **Lente de equidade e justiça social em todas as etapas.** Aplicada especificamente na Etapa 1 (escolha da unidade de análise, declaração de lacunas), Etapa 3 (quais vozes dominam os temas emergentes) e Etapa 5 (estratificação por grupo + análise de lacunas). Ver `docs/equity-lens.md` para critérios operacionais. **Esta não é uma regra opcional** — skills de impacto social sem lente de equidade reproduzem desigualdades.

## O workflow (6 etapas)

O trabalho de análise qualitativa é organizado em 6 etapas sequenciais. Cada etapa tem **objetivo**, **prompt sugerido** pronto pra copiar, e **output esperado** que alimenta a etapa seguinte. Os prompts usam tags XML (`<principios>`, `<escopo>`, `<analise>`, `<produto>`, etc.) pra reduzir ambiguidade — prática recomendada pela Anthropic pra entradas estruturadas e saídas confiáveis. Não pule etapas: a qualidade final depende da disciplina de validar humanamente nos checkpoints indicados.

### Etapa 1 — Configuração, escopo e modo

**Objetivo:** Estabelecer princípios de trabalho com o modelo + capturar escopo + escolher modo de clustering + decidir camada de sentimento + declarar metadados demográficos disponíveis e lacunas conhecidas. Sem esse alinhamento inicial, a codificação das etapas seguintes parte desfocada e acumula erros.

**Prompt sugerido:**

```
Você é pesquisador especialista em análise qualitativa aplicada a
políticas públicas e trabalho de impacto social. Vou te enviar, nas
próximas mensagens, um corpus de texto para análise. Antes de começar,
leia e concorde com os princípios abaixo — eles valem para toda a análise
desta conversa.

<principios>
1. Nunca inventar trechos, temas ou sentimentos. Se um tema não aparece
   no corpus, não crie. "Ambivalente" ou "neutro" são respostas válidas
   para sentimento.
2. Toda afirmação temática carrega trecho literal rastreável. Formato:
   Tema X é ilustrado por R042 ("trecho exato"). Nunca generalizações
   como "alguns respondentes mencionaram...".
3. Distinguir tema manifesto (explícito) de tema latente (interpretação
   analítica). Sempre marcar qual é qual; latentes carregam justificativa
   de 1 frase.
4. NUNCA inferir demografia a partir de nome, linguagem, erros
   ortográficos, região ou outros sinais indiretos. Se o dado não existe
   no dataset, declare como lacuna e preserve até o output final.
5. Divergências dentro de um tema são tão importantes quanto
   convergências. Nomear sub-padrões e tensões internas, não colapsar.
6. Lente de equidade em todas as etapas: quem está representado, quem
   está ausente, linguagem inclusiva, impactos diferenciais.
</principios>

Antes do corpus, preciso que você confirme o escopo preenchendo o bloco
abaixo. Se algum campo estiver indefinido, pergunte antes de avançar.

<escopo>
  <tipo_input>survey | comentarios | entrevistas | texto_livre</tipo_input>
  <pergunta_alvo>...</pergunta_alvo>
  <unidade_analise>resposta_inteira | sentenca | trecho_delimitado</unidade_analise>
  <modo_clustering>indutivo | dedutivo | hibrido</modo_clustering>
  <codebook>
    (opcional; preencher APENAS se modo_clustering = dedutivo ou hibrido.
    Lista de temas pré-definidos, cada um com nome + definição curta.)
  </codebook>
  <sentimento_on>false | true</sentimento_on>
  <metadados_demograficos>
    (lista dos campos que acompanham o corpus, ex: "bairro, idade, sexo"
    OU literalmente "nenhum disponível")
  </metadados_demograficos>
  <grupos_ausentes_conhecidos>
    (quando os metadados forem parciais ou ausentes, nomeie com
    especificidade quais grupos provavelmente NÃO estão representados
    no corpus — ex: "usuárias que nunca acessaram o serviço",
    "pessoas com deficiência visual", "moradores de áreas rurais")
  </grupos_ausentes_conhecidos>
  <publico_saida>dirigencia_executiva | equipe_tecnica | ambos</publico_saida>
</escopo>

Defaults quando não especificado: modo_clustering=hibrido,
sentimento_on=false.

Se concordar com as regras e o escopo, responda "OK — regras definidas"
e aguarde o corpus.
```

**Output esperado:** Confirmação ("OK — regras definidas") + bloco `<escopo>` preenchido, pronto pra ser referenciado nas etapas seguintes.

### Etapa 2 — Preparo do corpus

**Objetivo:** Catalogar cada unidade do corpus com ID rastreável, avaliar volume pra decidir chunking, e registrar qualidade e exclusões de forma auditável.

**Prompt sugerido:**

```
Agora vou te enviar o corpus. Antes de qualquer análise temática,
preciso de 3 subetapas de preparo. Entregue cada uma em um subtítulo
separado.

## 2a — Catalogação

Produza uma tabela Markdown com cabeçalho:
| Unidade_ID | Texto | [metadados declarados na Etapa 1] |

Regras:
- Use IDs únicos e sequenciais conforme tipo_input:
  - survey → R001, R002...
  - comentarios → C001, C002...
  - entrevistas → E001, E002... (e sub-IDs E001.T01 para trechos
    quando unidade_analise for "trecho_delimitado")
  - texto_livre → T001, T002...
- Associe os metadados declarados na Etapa 1 (não invente metadados
  que não estão no dataset).
- Se algum metadado estiver ausente para uma unidade específica, escreva
  "não encontrado" naquela célula — nunca infira.

## 2b — Avaliação de volume

- Conte unidades e estime tokens totais (aproximado pelo tamanho agregado).
- Se o corpus tem ≤300 unidades E ≤50k tokens: processar direto, sem
  chunking.
- Se excede qualquer um dos dois limites: proponha esquema de chunking:
  1ª opção: estratificação por grupo demográfico (preserva
    representatividade)
  2ª opção: estratificação temporal (se houver série)
  último recurso: aleatório, COM alerta explícito de que pode mascarar
    padrões diferenciais por grupo
- O usuário decide o esquema; não faça chunking silencioso.

## 2c — Nota de preparo

- Qualidade aparente do corpus (OCR ruim, respostas em branco, spam,
  duplicatas óbvias)
- Normalizações feitas (se houver: maiúscula/minúscula, caracteres
  quebrados, etc.)
- Unidades excluídas do preprocessamento — LISTADAS à parte com motivo
  explícito, NUNCA apagadas silenciosamente

Devolva as 3 subetapas em ordem.
```

**Output esperado:** Tabela catalogada com IDs e metadados + plano de chunking (ou nota "corpus dentro do limite, sem chunking") + nota de preparo com exclusões motivadas.

### Etapa 3 — Codificação/clustering temático

**Objetivo:** Extrair temas + associar cada unidade a tema(s) com trecho literal + marcar manifesto vs. latente. É a etapa mais carregada da skill — a qualidade da síntese final depende do rigor aqui.

**Prompt sugerido:**

```
Agora vamos codificar o corpus em temas. Use o modo escolhido na Etapa 1
(<modo_clustering>). Os 3 modos têm comportamentos distintos:

SE MODO = INDUTIVO (bottom-up):
- Analise o corpus e proponha 5-12 temas emergentes
- Cada tema: nome curto, definição em 1 frase, marcação manifesto/latente,
  2-3 trechos literais ilustrativos com IDs
- Depois, marque cada unidade do corpus com o(s) tema(s) atribuído(s)

SE MODO = DEDUTIVO (top-down):
- Aplique o codebook fornecido na Etapa 1
- Marque cada unidade com tema(s) do codebook
- Unidades que não cabem em NENHUM tema vão para "não classificado (n)"
- Reporte a contagem de "não classificado" e peça decisão ao usuário
  (expandir codebook? aceitar como resíduo?)

SE MODO = HÍBRIDO (default):
- Comece aplicando o codebook fornecido
- Durante a marcação, identifique unidades que não se encaixam
- PROPONHA temas emergentes adicionais pra cobrir o resíduo
- Marque claramente os temas novos como "emergente"
- Output final: codebook original + temas novos identificados

REGRAS COMUNS aos 3 modos:
- Cada tema tem marcação obrigatória: manifesto (aparece explicitamente
  no texto) ou latente (interpretação analítica do modelo)
- Temas latentes carregam justificativa de 1 frase explicando a inferência
- Unidades podem ter múltiplos temas (não forçar exclusividade)
- Se o corpus foi dividido em lotes na Etapa 2, processe lote por lote
  e consolide temas equivalentes ao final (merge de temas que são
  essencialmente o mesmo)

Devolva DUAS tabelas Markdown claramente separadas.

<produto tipo="tabela_temas">
| Tema_ID | Nome | Definição | Tipo (manifesto/latente) | N_unidades | Trechos ilustrativos (IDs + citação literal) | Justificativa (só latente) |
</produto>

<produto tipo="tabela_marcacao">
| Unidade_ID | Temas atribuídos | Observações |
</produto>

Se houver "não classificado", reporte a contagem no final com a pergunta
ao usuário.
```

**Output esperado:** Tabela de temas (com trechos literais obrigatórios) + tabela de marcação de cada unidade. Temas latentes com justificativa. Contagem de "não classificado" quando aplicável.

### Etapa 4 — (Opcional) Camada de sentimento

**Objetivo:** Adicionar polaridade quando `<sentimento_on>` é `true`. Quando `false`, **pular explicitamente** — registrar a decisão, nunca esquecer.

**Prompt sugerido:**

```
Verifique o valor de <sentimento_on> declarado na Etapa 1.

## SE <sentimento_on> FOR FALSE:

Responda EXATAMENTE:
"Pulando Etapa 4 — sentimento desativado na configuração."
E passe direto para a Etapa 5. Não ignore em silêncio — registre a
decisão explicitamente.

## SE <sentimento_on> FOR TRUE:

Para cada unidade já codificada na Etapa 3, atribua polaridade com uma
destas 4 categorias:
- positivo
- neutro
- negativo
- ambivalente
+ justificativa em 1 frase ancorada no próprio trecho da unidade.

REGRAS CRÍTICAS:
- "Ambivalente" é resposta válida — use para unidades com sentimentos
  conflitantes simultâneos (ex: "o médico foi ótimo mas a espera foi
  horrível").
- "Neutro" é resposta válida — use para relatos factuais/descritivos
  sem valência clara (ex: "esperei 2 horas", "o atendimento é no 2º
  andar").
- NÃO FORCE polaridade em texto puramente descritivo. Transformar relato
  em queixa é alucinação de sentimento.

Depois da marcação por unidade, agregue por tema:

<produto tipo="sentimento_por_unidade">
| Unidade_ID | Polaridade | Justificativa |
</produto>

<produto tipo="distribuicao_por_tema">
| Tema_ID | % positivo | % neutro | % negativo | % ambivalente | Tom dominante |
</produto>
```

**Output esperado:** Tabela de sentimento por unidade + tabela de distribuição por tema. OU mensagem explícita de "pulando etapa" quando `<sentimento_on>` for `false`.

### Etapa 5 — Estratificação por grupo e análise de lacunas

**Objetivo:** Aplicar a lente de equidade cruzando (quando possível) temas × grupos demográficos + nomear lacunas com especificidade. Esta é a etapa onde a equity lens se torna operacional, não decorativa.

**Prompt sugerido:**

```
Agora é a análise de equidade e representatividade. Há DOIS caminhos
dependendo dos metadados declarados na Etapa 1.

## CAMINHO A — Metadados demográficos disponíveis

Cruze temas × grupos declarados. Produza uma tabela:

| Grupo | Tema dominante | Temas subrepresentados | Observação |

Identifique padrões diferenciais:
- Tema X é dominante no grupo A mas ausente no grupo B?
- Há sinal de desigualdade estrutural no corpus?
- Há sub-padrões dentro de um mesmo grupo (tensões internas)?

## CAMINHO B — Sem metadados demográficos

Pule o cruzamento e foque integralmente em representatividade + lacunas.
Seja EXPLÍCITO sobre não poder estratificar sem dado — não finja que
consegue.

## EM AMBOS OS CAMINHOS (obrigatório):

1. Análise de representatividade do corpus como um todo:
   - Quem provavelmente NÃO respondeu?
   - Barreiras de acesso à pesquisa/canal
   - Vieses de seleção da amostra

2. Lista nomeada de lacunas com ESPECIFICIDADE (nomes concretos de
   grupos reais, NUNCA "vozes diversas"):
   - Ex: "pessoas com deficiência visual que acessam o serviço via
     ouvidoria"
   - Ex: "usuárias da ESF em bairros sem cobertura de agente comunitário"
   - Ex: "trabalhadoras rurais do semiárido"

3. Riscos de generalização:
   - O que esta análise PODE sustentar
   - O que esta análise NÃO PODE sustentar

## PRINCÍPIO CRÍTICO

Grupos declarados como ausentes na Etapa 1 (<grupos_ausentes_conhecidos>)
devem sobreviver até a Etapa 5. Não os esqueça no caminho. Se foram
declarados, devem aparecer nomeados nesta etapa.

Formato final:

<analise>
  (a) Tabela de cruzamento tema × grupo [apenas no Caminho A]
  (b) Parágrafo de análise diferencial ou de representatividade
  (c) Lista nomeada de lacunas (com especificidade)
  (d) Riscos de generalização
</analise>
```

**Output esperado:** Bloco `<analise>` com (a) tabela de cruzamento quando aplicável, (b) parágrafo de análise, (c) lacunas nomeadas concretamente, (d) riscos de generalização explicitados.

### Etapa 6 — Síntese final e autoverificação

**Objetivo:** Consolidar a análise em matriz temática final + síntese narrativa curta + autoverificação estruturada dos 6 princípios + handoff pro checklist humano. A autoverificação não substitui o humano — prepara o material pra revisão dele.

**Prompt sugerido:**

```
Produza a saída final da análise em três produtos claramente separados
por cabeçalhos.

<produto tipo="matriz_tematica_final">

Matriz temática consolidada em tabela Markdown com cabeçalho:

| Tema_ID | Nome | Tipo | N_unidades | Trechos representativos (ID + literal) | Sub-padrões/divergências | Sentimento (se aplicável) | Distribuição por grupo (se aplicável) |

Regras:
- Preserve os trechos literais entre aspas (Princípio 2 — obrigatório)
- Na coluna "Sub-padrões/divergências", nomeie tensões internas ao
  tema quando existirem (Princípio 5)
- Colunas de sentimento e distribuição por grupo aparecem APENAS se
  as etapas correspondentes foram executadas; caso contrário, omita
  a coluna (não preencha com "n/a" em todas as linhas)

</produto>

<produto tipo="sintese_narrativa">

Máximo 1 página cobrindo:
- Temas dominantes + breve caracterização
- Divergências ou tensões internas relevantes
- Padrões diferenciais por grupo (quando aplicável)
- Lacunas críticas de representatividade (resumo condensado da Etapa 5)
- Recomendações: o que vale validar com o público-alvo antes de
  qualquer decisão substantiva

A síntese narrativa deve ser legível de forma autônoma por quem não
leu as etapas anteriores.

</produto>

<produto tipo="autoverificacao">

Tabela com cabeçalho:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência | Ajustes |

Cubra os 6 princípios invioláveis, um por linha. Para cada um, cite
trecho concreto do produto final que sustenta o "cumprido" — ou aponte
exatamente onde está a falha. "Parcial" é resposta válida e até
desejável: indique o que está ok e o que ainda precisa de ajuste.

Os 6 princípios a verificar:
1. Nunca inventar trechos, temas ou sentimentos
2. Toda afirmação temática carrega trecho literal rastreável
3. Distinguir tema manifesto de tema latente
4. Nunca inferir demografia a partir de sinais indiretos
5. Divergências preservadas dentro dos temas
6. Lente de equidade aplicada nas Etapas 1, 3 e 5

</produto>

Feche com este lembrete verbatim:
"Antes de publicar, rode o checklist em references/checklist.md e
confira manualmente pelo menos 20% dos trechos literais contra o
corpus original. A autoverificação não substitui validação humana."
```

**Output esperado:** 3 produtos delimitados (matriz temática final + síntese narrativa + relatório de autoverificação) + lembrete verbatim ao final.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar pra próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop**.

- **Após Etapa 1 (Configuração)** — Verifique: o escopo captura a pergunta real? A declaração de metadados e lacunas conhecidas está honesta (não esconde ausências, não exagera o que você tem)? O modo de clustering escolhido faz sentido pro tipo de corpus?

- **Após Etapa 3 (Codificação)** — Verifique: os temas propostos refletem fielmente o corpus? Os trechos literais citados foram abertos e conferidos contra o corpus original (pelo menos 20% da amostra)? Sub-padrões e divergências dentro de cada tema foram preservados? Temas latentes têm justificativa razoável?

- **Após Etapa 6 (Síntese final)** — Verifique: a matriz final não perdeu rastreabilidade? A autoverificação aponta fragilidades reais, não é auto-elogio genérico? Nenhuma inferência demográfica indireta escapou? Antes de publicar, rode o checklist em `references/checklist.md`.

**Regra geral:** Se você não teve tempo de validar, não publique. Use a saída como rascunho interno até a validação ser feita.

## Falhas comuns

Anti-patterns que o modelo (ou o humano confiando no modelo sem checar) pode cometer:

1. **Tema inventado sem sustentação no corpus** — modelo cria tema plausível que "faz sentido" mas nenhuma unidade específica o ilustra. *Mitigação:* Princípio 2 + exigência de 2-3 trechos literais por tema + checkpoint humano após Etapa 3.

2. **Citação com aspas que não é literal** — o modelo escreve `R042 ("o atendimento é horrível")` mas R042 escreveu "demorei muito pra ser atendida e me senti mal tratada". Paráfrase travestida de citação. *Mitigação:* Princípio 2 + item de conferência de 20% dos trechos no checklist técnico.

3. **Inferência demográfica silenciosa** — modelo classifica R042 como "provavelmente mulher" por estilo de linguagem, ou "provavelmente baixa escolaridade" por erros ortográficos. Caminho direto pra viés estrutural. *Mitigação:* Princípio 4 + checklist de equidade + recusa explícita da skill em fazer essa atribuição.

4. **Sentimento forçado em texto descritivo** — "esperei 2 horas pra ser atendida" vira "negativo" quando é relato factual sem valência declarada. *Mitigação:* Etapa 4 explicita que "neutro" e "ambivalente" são legítimos; modelo não deve transformar relato em queixa.

5. **Consenso falso dentro de um tema** — duas respostas contrárias agregadas no mesmo tema sem nomear a divergência. "Qualidade do atendimento" cobrindo simultaneamente "o médico foi ótimo" e "o médico foi rude". *Mitigação:* Princípio 5 + coluna "sub-padrões/divergências" obrigatória na matriz final.

6. **Manifesto confundido com latente** — modelo interpreta "na verdade o que ela queria dizer era..." sem marcar como latente, ou marca tema óbvio como latente pra parecer mais analítico. *Mitigação:* Princípio 3 + exigência de marcação explícita + justificativa para todos os temas latentes.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa desta skill em um caso fictício realista (380 respostas abertas de pesquisa com usuárias da atenção básica em município fictício de ~200 mil habitantes, com cruzamento por bairro e idade + lacunas nomeadas). Mostra input, saídas intermediárias e produtos finais das 6 etapas.

- **`references/variantes.md`** — Adaptações do workflow base para contextos diferentes: (1) sem metadados demográficos disponíveis, (2) corpus grande (>300 unidades) com chunking estratificado, (3) entrevistas e grupos focais transcritos, (4) série temporal entre snapshots.

- **`references/checklist.md`** — Checklist pro humano validar a saída antes de publicar. Inclui seção técnica (IDs, citações literais, manifesto/latente, sentimento) e seção de equidade (metadados declarados, inferências proibidas, lacunas nomeadas, consensos falsos).

---

*Baseada nos casos 2 ("Análise Qualitativa") e 18 ("Percepções Públicas") do livro* Inteligência Artificial para Impacto Social *(Castro, 2025), fundidos em uma única skill porque ambos executam clusterização semântica + análise de sentimento — variando apenas o input. Modernizada com práticas atuais de prompting (XML tags, autoverificação estruturada, lente de equidade operacional, princípio anti-inferência demográfica específico desta skill).*
