---
name: stakeholder-negotiation
description: Mapeia atores por poder × interesse com auditoria de ausências estruturais e prepara materiais de negociação (MANA/ZOPA, argumentário, objeções, roteiro) com checagem de legitimidade da mesa.
---

# Mapeamento de Atores e Preparação para Negociação

## Quando usar esta skill

Esta skill apoia dois momentos do trabalho de articulação política e institucional em projetos de impacto social:

1. **Mapear o ecossistema de atores** de uma política, programa ou campo de atuação — quem tem poder, quem tem interesse, quem está faltando na mesa.
2. **Preparar-se para uma negociação específica** com uma contraparte — entender o terreno, explicitar MANA e ZOPA, antecipar objeções, escrever argumentário e roteiro de reunião.

Os dois momentos são encadeados: o mapa de atores (Sub-arco 1) alimenta a preparação de negociação (Sub-arco 2), mas cada um funciona autonomamente. Quem só precisa do diagnóstico de ecossistema para em E5. Quem já tem um mapa pode entrar direto em E6 (ver `references/variantes.md`).

Use quando o usuário:

- Precisa mapear atores envolvidos numa política, projeto ou iniciativa
- Vai a uma reunião de alto impacto com um financiador, parlamentar, gestor público ou parceiro
- Quer entender quem pode apoiar, bloquear ou vetar uma mudança
- Recebeu pedido de preparação para audiência pública ou reunião de coalizão
- Vai renegociar contrato, convênio, parceria ou edital
- Quer preparar argumentário e antecipação de objeções para pauta difícil

Sinais típicos na conversa do usuário:

- "Preciso mapear quem está envolvido nessa política"
- "Tem uma reunião com o financiador semana que vem, preciso preparar"
- "Quero entender quem pode apoiar ou vetar esse projeto"
- "A secretaria pediu uma preparação pra audiência pública"
- "Tem uma coalizão se formando, quem está dentro e quem está fora?"
- "Queremos renegociar um contrato"
- "Precisamos preparar argumentário pra uma reunião com parlamentares"

Relação com outras skills do repositório:

- **Input opcional:** output de `theory-of-change` (objetivo institucional e indicadores viram âncora para alinhamento de stakeholders) e output de `evidence-synthesis` ou `evidence-gathering` (matriz de evidências vira banco de dados de suporte para o argumentário da Etapa 8).
- **Output opcional:** mapa validado + estratégias de engajamento alimentam `project-structuring` (stakeholders como recurso/dependência) e `strategic-planning` (insumo para diagnóstico multi-horizonte).

Não são contratos rígidos — apenas pontes sugeridas.

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Contexto do tema em uma frase** — a política, programa ou projeto em jogo. Sem isso, a skill não consegue separar atores relevantes de atores adjacentes.

2. **Insumos sobre atores ou sobre a negociação** — dispersos (atas de reunião, trocas de email, relatórios de execução, notícias, posicionamentos públicos) ou estruturados (planilha mínima: nome, setor, cargo, posição), declarado na Etapa 1 como `<modo_input>`.

3. **Para Sub-arco 2 (preparação de negociação):** objetivo institucional claro + autorização interna para discutir limites de negociação. O que a organização aceita ceder e o que não aceita é informação sensível — a skill pergunta, não adivinha. MANA mal dimensionada por falta de alinhamento interno destrói negociações reais.

4. **Disposição para nomear ausências e assimetrias de poder.** As Etapas 4 e 7 forçam isso. Usuários que querem um mapa "otimista" sem lente crítica não serão bem servidos por esta skill — a saída vai soar antipática, é parte do método. Se essa disposição não existe, é melhor usar outra skill ou discutir expectativas antes.

5. **Tempo para os 3 checkpoints humanos obrigatórios.** A skill **interrompe** o fluxo e aguarda confirmação humana nas transições críticas. Não avança silenciosamente. Os checkpoints são decisões políticas e de legitimidade — delegá-las ao modelo é o que a skill existe para impedir.

Se algum desses elementos não está pronto, a skill **pergunta antes de avançar** — não inventa silenciosamente.

## Princípios invioláveis

Estas 5 regras valem em TODAS as etapas, nos dois sub-arcos. Não negocie.

1. **Nunca inventar ator, posição ou evidência.** Se um ator ou uma atribuição (poder, interesse, posição) não está nos insumos, escreva literalmente "não encontrado". A tentação de "preencher" o mapa com conhecimento geral do modelo é o jeito mais rápido de fabricar um ecossistema fictício que depois orienta decisões reais.

2. **Toda inferência marcada como `[suposição]` com justificativa de uma frase.** Vale para poder estimado sem evidência direta, posição provável extrapolada de histórico, MANA da contraparte (quase sempre `[suposição]` — você raramente sabe o que a outra parte fará se não houver acordo), e objeções antecipadas. Sem a marca explícita, suposição vira "fato" na cabeça de quem lê.

3. **Toda classificação rastreável a evidência textual.** A tabela da Etapa 3 traz uma coluna `Evidência` com Ator_ID + trecho literal entre aspas ou referência documental. Sem essa coluna, não há auditoria possível. Evidência literal entre aspas é melhor que paráfrase — resiste a releituras e a terceiros validando o trabalho.

4. **Matriz poder×interesse é diagnóstico do status quo, não descrição neutra do mundo.** Poder é uma relação social construída, não um atributo fixo. Um ator "fraco" hoje pode ser forte amanhã quando se organiza com pares. As Etapas 4 e 7 (auditorias de equidade dedicadas) são **obrigatórias** — não são etapas "extras" nem disclaimers de final. Saltá-las ou fazê-las pro forma é justamente o anti-pattern que a skill existe para impedir.

5. **Lente de equidade e justiça social em todas as etapas**, operacionalizada via:
   - **Duas etapas dedicadas** (E4 — auditoria estrutural do mapa; E7 — auditoria de legitimidade da mesa) que são infraestrutura, não checklists opcionais
   - **Hooks** nas Etapas 2, 3, 5, 6, 8 e 9 (cada uma carrega perguntas rápidas de equidade embutidas no prompt)
   - **Checklist separada** em `references/checklist.md` (seção Equidade)
   - Referencia `docs/equity-lens.md` como framework compartilhado do repositório

**Esta não é uma regra opcional** — skills de impacto social sem lente de equidade operacional reproduzem desigualdades.

## O workflow (10 etapas)

O trabalho é organizado em 10 etapas sequenciais divididas em dois sub-arcos. **Sub-arco 1 — Mapa de Atores (Etapas 1-5)** produz diagnóstico do ecossistema e é standalone útil. **Sub-arco 2 — Preparação de Negociação (Etapas 6-10)** pode ser invocado em sequência ou como ponto de entrada autônomo por quem já tem um mapa. Entre os sub-arcos há um checkpoint humano forte (CP2) que registra a decisão política de com quem negociar e por quê. Há também dois outros checkpoints obrigatórios: CP1 pós-E4 (valida ausências) e CP3 pós-E7 (decisão sobre legitimidade da mesa).

Cada etapa tem **objetivo** específico, **prompt sugerido** pronto para copiar (com tags XML `<principios>`, `<escopo>`, `<insumos>`, `<modo_input>`, `<auditoria>` etc. para reduzir ambiguidade — prática recomendada pela Anthropic), e **output esperado** que alimenta a etapa seguinte. **Não pule etapas**, especialmente E4, CP2 e E7 — todas existem para proteger decisões políticas críticas da delegação silenciosa ao modelo.

---

**Sub-arco 1 — Mapa de Atores (Etapas 1-5)**

### Etapa 1 — Configuração, escopo e modo de input

**Objetivo:** estabelecer regras do trabalho (princípios invioláveis + anti-hallucination), capturar escopo rico (tema, território, horizonte, objetivo institucional de médio prazo, stakeholders-semente), e declarar explicitamente `<modo_input>` como `disperso`, `estruturado` ou `misto`. Esta etapa existe para forçar um handshake antes de qualquer extração — alinha expectativas e evita que a skill parta para a ação com premissas implícitas.

**Prompt sugerido:**

```
Você vai me ajudar a mapear atores e preparar negociação, seguindo a skill stakeholder-negotiation. Antes de começar, confirme que entendeu as regras do trabalho.

<principios>
1. Nunca invente ator, posição ou evidência. "Não encontrado" quando faltar insumo.
2. Toda inferência marcada como [suposição] com justificativa de uma frase.
3. Toda classificação com coluna de evidência (Ator_ID + trecho literal ou referência).
4. A matriz poder×interesse é diagnóstico do status quo — as auditorias de equidade (Etapas 4 e 7) são obrigatórias.
5. Lente de equidade em todas as etapas (ver docs/equity-lens.md).
</principios>

<escopo>
- Tema / política / programa em jogo: [PREENCHER em uma frase]
- Território (escala geográfica): [municipal / estadual / federal / internacional / outra]
- Horizonte temporal: [próximos meses / 1 ano / 2-3 anos]
- Objetivo institucional de médio prazo: [PREENCHER em uma frase]
- Stakeholders-semente (nomes que você já sabe que são relevantes, mesmo sem detalhes): [lista]
</escopo>

<modo_input>
Escolha UM dos três e declare explicitamente:
- disperso — insumos não-estruturados (atas, emails, relatórios, notícias, documentos mistos)
- estruturado — planilha mínima com colunas nome, setor, cargo, posição
- misto — combinação dos dois
</modo_input>

Antes de prosseguir para a Etapa 2, responda literalmente:
"OK — regras definidas. Escopo capturado. Modo de input: [disperso/estruturado/misto]. Pronto para receber os insumos."
```

**Output esperado:** handshake explícito ("OK — regras definidas") + quadro vazio declarando modo de input + pronto para receber insumos. Se a skill pular direto para a Etapa 2 sem esse handshake, o usuário volta e exige — é função do prompt forçar o aceite.

### Etapa 2 — Levantamento e normalização de atores

**Objetivo:** extrair atores dos insumos, bifurcando por `<modo_input>`. No modo `disperso`, a skill faz extração via NER contextual com citação literal (trecho entre aspas que nomeia o ator). No modo `estruturado`, a skill faz ingestão direta com normalização mínima (padroniza grafias, remove duplicatas óbvias). No modo `misto`, a skill faz a união dos dois. A tabela resultante é a base de tudo que vem depois — acurácia aqui evita retrabalho nas Etapas 3, 4 e 5.

**Hook de equidade:** ao consolidar a tabela, a skill pergunta explicitamente: "Os atores extraídos refletem apenas as vozes das fontes institucionais, ou há diversidade de perspectivas? Sinalize qual a proporção de atores governamentais vs OSCs vs comunidades afetadas vs setor privado." Isso prepara o terreno para a Etapa 4, não a substitui.

**Prompt sugerido:**

```
Agora vou te passar os insumos. Modo de input confirmado: [disperso/estruturado/misto].

<insumos>
[COLE AQUI os documentos, atas, emails, planilha, ou combinação]
</insumos>

<instrucoes_extracao>
SE modo = disperso:
- Identifique atores mencionados (pessoas, organizações, coletivos, órgãos)
- Para cada ator extraído, copie um trecho literal entre aspas que o nomeia
- Normalize grafias variantes ("Sec. Saúde" e "Secretaria de Saúde" viram um único Ator_ID)
- Atores mencionados uma vez de passagem entram com nota "menção única"

SE modo = estruturado:
- Ingerir a tabela como-está
- Normalizar apenas: grafias variantes, duplicatas óbvias, campos vazios marcados como "não informado"
- Não inventar setores nem escalas

SE modo = misto:
- Fazer os dois e unir em tabela única, marcando Fonte como "disperso", "estruturado" ou "ambos"

Produza a tabela final com colunas:
Ator_ID | Nome | Setor | Escala de atuação | Descrição curta | Fonte

Ao terminar, responda: "Extraí [N] atores. Diversidade observada: [X governamentais / Y OSCs / Z comunidades afetadas / W setor privado / V outros]. Quer revisar antes de classificar?"
</instrucoes_extracao>
```

**Output esperado:** tabela `Ator_ID | Nome | Setor | Escala de atuação | Descrição curta | Fonte` com pelo menos 5 linhas (menos que isso sugere insumos insuficientes) + parágrafo curto sobre diversidade observada. Esse parágrafo é o hook de equidade — a Etapa 4 vai expandi-lo.

### Etapa 3 — Classificação em interesse, poder e posição

**Objetivo:** para cada ator, atribuir três dimensões com base em evidência:
- **Interesse** (alto/médio/baixo) — envolvimento, agenda declarada, histórico recente de ação no tema
- **Poder de influência** (alto/médio/baixo) — capacidade de veto, recursos, acesso a decisão, legitimidade pública
- **Posição provável** (apoio/oposição/neutro) — postura esperada frente ao que está em jogo, baseada em evidência textual

Cada atribuição carrega uma **Evidência** literal (trecho entre aspas ou referência). Onde não há base direta, marca `[suposição]` com justificativa de uma frase. Onde não há nada, marca "não encontrado" — melhor do que chutar.

**Hook de equidade:** "Sua classificação de poder está reproduzindo o poder formal do ecossistema oficial? Há atores com alto interesse mas baixo poder formal que podem ser subestimados por essa lente?"

**Prompt sugerido:**

```
Classifique cada ator da tabela anterior nas três dimensões.

<instrucoes_classificacao>
Para cada Ator_ID, atribua:
1. Interesse (alto/médio/baixo)
2. Poder (alto/médio/baixo)
3. Posição (apoio/oposição/neutro)
4. Evidência — trecho literal entre aspas OU referência documental OU [suposição] + justificativa curta OU "não encontrado"

Regras:
- Poder considera: veto institucional, recursos financeiros, acesso a decisão, legitimidade pública
- Posição considera: histórico declarado, agenda pública, vinculações conhecidas
- Se a mesma evidência sustenta duas atribuições, cite uma vez só e referencie
- Se não há evidência textual para nenhuma dimensão, o ator fica com "não encontrado" nas 3 colunas e vira candidato a remoção ou a busca ativa de mais insumos

Produza a tabela classificatória completa.

Ao final, responda à pergunta de equidade: "Sua classificação de poder está reproduzindo apenas o poder formal? Há atores com alto interesse e baixo poder formal que esse corte subestima?"
</instrucoes_classificacao>
```

**Output esperado:** tabela classificatória completa com colunas `Ator_ID | Interesse | Poder | Posição | Evidência` + resposta explícita à pergunta de equidade. Se >30% dos atores estão marcados como "não encontrado", o prompt pede para o usuário trazer mais insumos antes de prosseguir.

### Etapa 4 — Auditoria estrutural do mapa (equidade dedicada)

**Objetivo:** auditar o mapa produzido até aqui contra três lentes obrigatórias:

1. **Ausências estruturais** — quem tipicamente não aparece neste tipo de ecossistema e deveria (trabalhadores informais, coletivos sem formalização jurídica, comunidades afetadas diretamente, grupos linguisticamente minoritários, pessoas com deficiência, populações rurais, povos tradicionais, pessoas negras e indígenas em posições de decisão)
2. **Lentes interseccionais** — o mapa reproduz o viés de língua, gênero, raça, território ou classe das fontes originais? (ex: fontes institucionais em PT-BR quase sempre invisibilizam comunidades de pescadores artesanais, quilombolas, povos indígenas; atas de conselhos consultivos tendem a ser brancas, homens, com ensino superior)
3. **Postergação** — há grupos cuja representação foi "adiada" ("vamos começar com esses e depois incluir aqueles") por serem minoritários, difíceis de encontrar nas fontes, ou cuja inclusão parece "complicada"?

A Etapa 4 expande o Caso 10 Etapa 4 do livro (lacunas/ausentes) para um audit de primeira classe. O output inclui uma lista de **atores sugeridos** rotulados como "sugerido — validação humana" e força a distinção entre "mapeado" (está nos insumos) e "sugerido" (inferência do modelo baseada em padrões típicos).

**Prompt sugerido:**

```
Agora faça auditoria estrutural do mapa construído.

<auditoria>
Responda explicitamente às três perguntas:

1. AUSÊNCIAS ESTRUTURAIS
Olhando para a tabela atual, quem tipicamente faz parte deste tipo de ecossistema e NÃO está aqui? Considere: trabalhadores informais, coletivos sem CNPJ, comunidades afetadas diretamente, grupos linguisticamente minoritários, pessoas com deficiência, populações rurais, povos tradicionais (quilombolas, indígenas, ribeirinhos), pessoas negras e indígenas em posições de decisão, mães atípicas, juventude periférica. Liste 3-5 ausências específicas com uma frase de justificativa cada.

2. LENTES INTERSECCIONAIS
O mapa reproduz o viés de língua / gênero / raça / território das fontes? Se suas fontes são todas institucionais em português formal, é quase certo que sim. Nomeie o viés e a direção. Exemplo: "Todas as fontes são atas de reuniões presenciais em horário comercial — isso exclui quem trabalha formalmente, quem não mora perto, e quem não tem recursos para deslocamento. Há viés de classe e de território."

3. POSTERGAÇÃO
Há grupos cuja inclusão parece "complicada" ou "para uma próxima fase"? Nomeie-os. Postergação silenciosa é o mecanismo mais comum de exclusão estrutural — torne-o explícito.

Ao final, produza:
- SEÇÃO "Ausências e lacunas": prosa curta reconhecendo o que o mapa não vê
- TABELA "Atores sugeridos": Nome | Motivo da sugestão | Fonte da inferência (tipicamente "padrão estrutural de ausência neste tipo de ecossistema") | [suposição]
- FLAGUEAMENTO dos vieses reproduzidos pelas fontes

Não aprove a Etapa 5 sem esse pacote.
</auditoria>
```

**Output esperado:** seção "ausências e lacunas" (prosa) + tabela de atores sugeridos com pelo menos 3 linhas + flagueamento explícito dos vieses reproduzidos + prompt de checkpoint para o humano.

---

### Checkpoint humano 1 — pós-E4 (bloqueia E5)

**Pergunta obrigatória ao humano:**

> Revise as ausências listadas e os atores sugeridos. Para cada ator sugerido, decida:
> - **ENTRA** — vira ator real da tabela (com Ator_ID, mesmo que com evidência marcada como [suposição])
> - **ANOTAÇÃO** — fica registrado como ausência reconhecida mas não entra na matriz (ex: comunidade que não quer ser mapeada nesse momento, grupo difícil de localizar que precisa de busca ativa)
> - **DESCARTA** — com justificativa por quê
>
> Registre por escrito sua decisão. A skill não avança para a Etapa 5 sem esse registro.

Se o humano der "ok, avança" sem decisão explícita, o prompt pede novamente. Decisão implícita = decisão do modelo = violação do princípio 4.

### Etapa 5 — Matriz poder×interesse, estratégias diferenciadas e protocolo de atualização

**Objetivo:** distribuir os atores (incluindo os "sugeridos" aprovados no CP1) na matriz 2×2 (alto/baixo para Poder × alto/baixo para Interesse, gerando 4 quadrantes), gerar estratégia de engajamento diferenciada por ator (objetivo do contato + abordagem recomendada em uma linha, sempre citando Ator_ID para rastreabilidade), e definir **protocolo de atualização contínua** — como revisar o mapa a cada ciclo de reunião ou notícia nova sem começar do zero.

**Hook de equidade:** "Para atores nos quadrantes de 'alto interesse + baixo poder' (grupos afetados tipicamente caem aqui), sua estratégia é apenas 'manter informado' ou inclui mecanismos concretos de escuta e compartilhamento de poder?"

**Prompt sugerido:**

```
Distribua os atores na matriz poder×interesse e gere estratégias.

<matriz>
Desenhe a matriz visual 2x2:
- Quadrante 1 (alto poder + alto interesse): GERENCIAR DE PERTO — atores centrais, relação ativa
- Quadrante 2 (alto poder + baixo interesse): MANTER SATISFEITO — atores-gatekeeper, atenção seletiva
- Quadrante 3 (baixo poder + alto interesse): MANTER INFORMADO E ESCUTAR — atenção ao risco de tratar como plateia
- Quadrante 4 (baixo poder + baixo interesse): MONITORAR — revisitar periodicamente

Liste os Ator_IDs em cada quadrante.
</matriz>

<estrategias>
Para cada ator, escreva uma linha de estratégia:
Ator_ID | Objetivo do contato | Abordagem recomendada (1 frase) | Próximo passo concreto

Para os atores do Quadrante 3 (alto interesse + baixo poder — tipicamente grupos afetados), a "abordagem recomendada" deve incluir mecanismo concreto de escuta (não só "manter informado"). Se a abordagem for só comunicação de mão única, o prompt pede para revisar.
</estrategias>

<protocolo_atualizacao>
Defina como o mapa vai ser atualizado ao longo do tempo:
- Quem é o responsável pela curadoria contínua na organização?
- Com que frequência o mapa é revisitado? (sugestão: após cada reunião importante + revisão formal a cada ciclo de planejamento)
- Que tipo de evento dispara uma revisão ad hoc? (mudança de governo, divulgação de edital, crise, notícia relevante)
- Onde mora o mapa? (planilha? wiki? documento versionado?)
</protocolo_atualizacao>

<verificacoes_qualidade>
Antes de fechar a etapa, responda:
1. Todos os 4 quadrantes têm pelo menos 1 ator? (se não, o mapa provavelmente está enviesado)
2. Os atores do Q3 têm estratégia que inclui escuta, não só comunicação?
3. O protocolo de atualização tem responsável nomeado e frequência definida?
</verificacoes_qualidade>
```

**Output esperado:** (a) matriz visual 2×2 com Ator_IDs em cada quadrante; (b) tabela de estratégias `Ator_ID | Objetivo | Abordagem | Próximo passo`; (c) parágrafo de protocolo de atualização; (d) três verificações de qualidade respondidas.

---

### Checkpoint humano 2 — pós-E5 / pré-E6 (transição entre sub-arcos, bloqueia Sub-arco 2)

Este é o checkpoint mais importante da skill. **Decisão política obrigatória.** Humano decide, registra por escrito e confirma:

1. **Com qual(is) contraparte(s) o grupo vai negociar?** Nomeie o Ator_ID ou Ator_IDs. Se são vários, a negociação é multi-parte (consultar `references/variantes.md` variante (a)).
2. **Por quê?** Qual o objetivo institucional que justifica esta negociação agora, neste momento? Uma frase.
3. **Que resultado está em jogo?** Identifique: resultado-alvo (o melhor realisticamente esperado) e resultado mínimo aceitável (abaixo do qual não há acordo).
4. **É bilateral ou multi-parte?** Workflow principal assume bilateral. Multi-parte segue para `variantes.md`.

A skill **não avança** para o Sub-arco 2 sem esse registro explícito. **Decisão implícita é decisão do modelo, e essa decisão é política demais para ser delegada.** Se o humano tentar pular, o prompt reitera a pergunta e cita esta frase como justificativa.

**Por que este checkpoint existe:** o anti-pattern número 1 desta skill é "avançar direto do mapa para a preparação com a 'contraparte óbvia' sem decisão política registrada". A contraparte "óbvia" é quase sempre quem tem mais poder — e escolher negociar com quem tem mais poder sem interrogar essa escolha reproduz exatamente as assimetrias que a skill está tentando tornar visíveis.

---

**Sub-arco 2 — Preparação de Negociação (Etapas 6-10)**

### Etapa 6 — Escopo da negociação, partes, interesses, MANA e ZOPA

**Objetivo:** funde Caso 11 Etapas 2+3 do livro em uma única etapa. Captura o escopo da negociação, identifica partes, resume interesses aparentes com base em evidência, descreve a MANA (Melhor Alternativa à Negociação Acordada) da nossa parte de forma objetiva, estima a MANA da contraparte como `[suposição]` (explícita), e formula a ZOPA (Zona de Possível Acordo) como intervalo qualitativo. Aponta um risco principal e uma oportunidade principal para cada parte.

**Hook de equidade:** "A sua MANA parece 'fraca' em termos absolutos? Nomeie o porquê — é assimetria estrutural de poder, não fato neutro. A Etapa 7 vai expandir isso."

**Prompt sugerido:**

```
Capture o escopo da negociação. Use o registro do Checkpoint 2 como base.

<escopo_negociacao>
Objetivo da negociação (1 parágrafo): [o que queremos ao final deste processo específico]
Resultado-alvo: [o melhor realisticamente esperado]
Resultado mínimo aceitável: [abaixo disso, sem acordo]
Prazos críticos: [datas, janelas]
Restrições jurídicas: [marco regulatório aplicável, impedimentos legais]
Restrições orçamentárias: [teto, limites, compromissos já assumidos]
</escopo_negociacao>

<partes_e_interesses>
Parte 1 (nós):
- Quem somos
- Interesses aparentes (evidência: trecho de ata / missão / plano)
- MANA (o que fazemos se não houver acordo — operacional, não declarativa): [texto objetivo]
- Risco principal nesta negociação
- Oportunidade principal nesta negociação

Parte 2 (contraparte):
- Quem é
- Interesses aparentes (evidência: posicionamento público, histórico, declarações recentes)
- MANA da contraparte: [suposição] + justificativa curta (você raramente sabe o que a outra parte fará)
- Risco principal do nosso ponto de vista (o que eles podem fazer que nos prejudica)
- Oportunidade principal do nosso ponto de vista (o que eles podem querer que nos ajuda)
</partes_e_interesses>

<zopa>
Descreva a Zona de Possível Acordo QUALITATIVAMENTE:
- Em que intervalo de trocas possíveis existe acordo aceitável para as duas partes?
- Há uma dimensão objetiva clara (valor, prazo, escopo)? Descreva o intervalo.
- Há dimensões qualitativas (reputação, precedente, relação continuada)? Nomeie-as.
- Se a ZOPA parece vazia (nenhuma troca possível satisfaz o mínimo das duas partes), declare isso explicitamente — é informação crítica.
</zopa>

<hook_equidade>
Responda: "A nossa MANA é fraca em termos absolutos? Se sim, esse é um dado estrutural sobre nossa posição, não sobre a situação. Nomeie o porquê: somos pequenos, novos, periféricos, desorganizados, carentes de recursos? A Etapa 7 vai auditar isso como assimetria de poder, não como 'fato da vida'."
</hook_equidade>
```

**Output esperado:** briefing estruturado em seções numeradas + MANAs explícitas (nossa operacional, deles `[suposição]`) + ZOPA descrita qualitativamente + resposta ao hook de equidade.

### Etapa 7 — Auditoria de legitimidade da mesa (equidade dedicada)

**Objetivo:** auditar a mesa de negociação contra três perguntas obrigatórias. Esta é a segunda etapa de equidade dedicada da skill — ela existe porque os vieses do Sub-arco 2 são estruturalmente diferentes dos vieses do Sub-arco 1 e exigem tratamento distinto.

**As três perguntas:**

1. **Representação:** quem é mais afetado pela decisão está representado à mesa? Se não, em nome de quem estamos negociando? Há risco de paternalismo (decidir por outros sem sua participação)?

2. **Assimetria de MANA como poder estrutural:** a nossa MANA é fraca porque somos pequenos / periféricos / novos? Nomeie isso como **assimetria de poder**, não como "dado objetivo da situação". Nomeie simetricamente a **força** da MANA da contraparte — também é poder estrutural, não virtude.

3. **Mitigadores possíveis:** há formas de mitigar a ausência de grupos afetados sem interromper a negociação? Por exemplo: envolver terceiros como apoiadores, aplicar escuta prévia com grupos afetados (mesmo que eles não estejam à mesa), adiar a negociação até representação adequada, trazer evidências de voz de pessoas afetadas (testemunhos, dados de escuta).

**Prompt sugerido:**

```
Faça auditoria de legitimidade da mesa.

<auditoria_mesa>
1. REPRESENTAÇÃO
Quem é mais afetado pela decisão que vamos negociar?
Essas pessoas estão representadas à mesa? (sim / não / parcialmente)
Se não: em nome de quem estamos negociando?
Há risco de paternalismo? (decidir o que é melhor para outras pessoas sem consultá-las)

2. ASSIMETRIA DE MANA COMO PODER ESTRUTURAL
Nossa MANA é fraca? Se sim, nomeie o motivo estrutural (não descritivo):
- Somos pequenos? (tamanho organizacional)
- Somos novos? (tempo de existência)
- Somos periféricos? (fora dos círculos de decisão)
- Dependemos financeiramente desta contraparte?

A MANA da contraparte é forte? Se sim, nomeie simetricamente o poder estrutural (recursos, posição histórica, rede de relações, acesso a decisão pública).

A assimetria é um dado da situação, mas não é "neutra" — é poder construído. Nomear isso muda o que conta como acordo aceitável.

3. MITIGADORES POSSÍVEIS
Liste 3 a 5 mitigadores concretos:
- Envolver terceiros como apoiadores na mesa? (quem?)
- Aplicar escuta prévia com grupos afetados? (quando?)
- Adiar a negociação até representação adequada? (até quando? é viável?)
- Trazer evidências de voz de pessoas afetadas mesmo quando elas não estão à mesa? (que evidências?)

4. RECOMENDAÇÃO EXPLÍCITA
Com base nas 3 respostas acima, recomende UMA das opções:
(a) prosseguir como está, assumindo os riscos
(b) prosseguir com mitigadores específicos (liste quais)
(c) adiar até envolver grupos ausentes

Não recomende "depende". A recomendação é uma hipótese forte para o humano aceitar ou rejeitar no Checkpoint 3.
</auditoria_mesa>
```

**Output esperado:** seção "legitimidade da mesa" com as 3 respostas + lista de mitigadores sugeridos + **recomendação explícita** (a/b/c).

---

### Checkpoint humano 3 — pós-E7 (bloqueia E8)

**Pergunta obrigatória ao humano:**

> A auditoria recomendou [a/b/c]. Você aceita a recomendação ou escolhe outra opção?
>
> - (a) prosseguir como está — você assume riscos de legitimidade nomeados e segue direto para E8
> - (b) prosseguir com mitigadores — você nomeia QUAIS mitigadores vão ser implementados antes ou durante a negociação, e a skill incorpora esses mitigadores no roteiro final (E10)
> - (c) adiar — a skill salva o mapa e a preparação parcial, e documenta que a negociação foi adiada até [critério de desbloqueio]
>
> Registre sua escolha por escrito. A skill não gera argumentário ou roteiro sem esse registro.

### Etapa 8 — Mensagens-chave, dados de suporte e precedentes

**Objetivo:** redigir a mensagem principal em uma frase + mensagens de apoio em linguagem simples, cada uma acompanhada por um dado de suporte e um exemplo ou precedente. Entrega também um quadro de referência rápida que pode ser impresso e levado para a reunião.

**Hook de equidade:** "A linguagem do argumentário evita termos estigmatizantes? (ex: 'vulneráveis' em vez de 'em situação de vulnerabilidade'; 'beneficiários' em vez de 'pessoas atendidas'; 'comunidade carente' em qualquer contexto.) Revise ativamente antes de fechar."

**Prompt sugerido:**

```
Redija as mensagens-chave da negociação.

<mensagem_principal>
Em UMA frase, qual é o ponto central que queremos que a contraparte internalize? Deve ser:
- Curta (até 25 palavras)
- Orientada ao interesse da contraparte, não ao nosso (formato "isso te traz X" em vez de "nós precisamos de Y")
- Ancorada em algo concreto (dado, prazo, precedente)
</mensagem_principal>

<mensagens_apoio>
3 a 5 mensagens de apoio, cada uma com:
- Texto da mensagem (1-2 frases, linguagem simples)
- Dado de suporte (com fonte — autor-ano; página/URL quando houver)
- Exemplo ou precedente (situação análoga com desfecho positivo, preferencialmente do próprio ecossistema)
</mensagens_apoio>

<quadro_referencia_rapida>
Tabela pronta para levar para a reunião:
Mensagem | Dado de apoio | Exemplo/Precedente | Fonte

Mantenha citações como trechos literais entre aspas quando forem decisivas. Paráfrase só para encurtar conectivos.
</quadro_referencia_rapida>

<hook_equidade>
Revise a linguagem das mensagens:
- Há termos estigmatizantes? (vulneráveis, beneficiários, carentes, necessitados, público-alvo como coisa)
- As pessoas atendidas aparecem como sujeitos ou como objetos do serviço?
- A narrativa reproduz deficit framing ("essas pessoas não têm X") ou reconhece capacidades?
Se sim para qualquer uma, reescreva.
</hook_equidade>
```

**Output esperado:** (a) mensagem principal em 1 frase; (b) 3-5 mensagens de apoio; (c) quadro de referência rápida em tabela; (d) resposta ao hook de equidade com reescrita se necessário.

### Etapa 9 — Objeções prováveis, respostas preparadas e concessões condicionais

**Objetivo:** listar objeções prováveis em frases curtas, redigir para cada uma uma resposta preparada que traga um dado de suporte e, quando necessário, uma **concessão condicional** amarrada a contrapartidas objetivas. Explicita **gatilhos de recuo** baseados na MANA — os pontos em que dizer "não" é mais protetor do que concordar.

**Princípio:** preparação é antecipação de posições legítimas da contraparte, não ensaio de confronto. Uma objeção bem antecipada permite resposta calma; uma objeção não antecipada vira surpresa em reunião de alto impacto.

**Hook de equidade:** "As objeções que você está antecipando vêm do ponto de vista da contraparte dominante (tipicamente do lado que tem mais poder)? Há objeções que grupos afetados fariam se estivessem à mesa que também precisam ser antecipadas?"

**Prompt sugerido:**

```
Liste objeções prováveis e prepare respostas.

<objecoes>
Para cada objeção, forneça:
1. Objeção (1 frase curta, como a contraparte provavelmente diria)
2. Por que é provável (evidência: histórico, posicionamento público, ou [suposição] + justificativa)
3. Resposta preparada (2-3 frases, com dado de suporte explícito)
4. Concessão condicional (se aplicável) — "posso oferecer X se você oferecer Y"; nunca oferta sem contrapartida
5. Gatilho de recuo — "se a contraparte insiste em [especificação], recuar para [posição]; se insiste mais, [ação]"

Liste 5 a 8 objeções prováveis. Menos que 5 sugere preparação superficial. Mais que 8 sugere que você está listando preocupações, não objeções.
</objecoes>

<gatilhos_de_recuo>
Separadamente, liste os gatilhos de recuo explícitos baseados na MANA:
- Limite 1: [condição] → [ação: adiar, pedir recesso, recuar para MANA]
- Limite 2: [condição] → [ação]
- Limite 3: [condição] → [ação]

Estes são os pontos em que você sabe, antes de entrar na reunião, que "não" é mais seguro do que "sim".
</gatilhos_de_recuo>

<suposicoes_a_validar>
Marque explicitamente os itens que dependem de [suposição]. Estes são os itens que precisam de validação interna antes da reunião — com a liderança, com o jurídico, com a equipe operacional.
</suposicoes_a_validar>

<hook_equidade>
As objeções antecipadas vêm só do lado dominante? Há objeções que grupos afetados fariam? Liste pelo menos 2 "objeções de legitimidade" que podem emergir (ex: "por que vocês estão negociando em nome de comunidades que não foram consultadas?", "essa decisão não deveria passar por escuta comunitária?"). Tenha resposta preparada.
</hook_equidade>
```

**Output esperado:** tabela de defesa preparada + seção separada de gatilhos de recuo explícitos + lista de `[suposição]` a validar + mínimo 2 objeções de legitimidade.

### Etapa 10 — Roteiro de reunião, talk track, kit de materiais e auto-verificação

**Objetivo:** produzir o pacote final que vai para a reunião. Inclui roteiro em texto corrido, talk track de 2-3 minutos para a liderança, lista do kit de materiais, e auto-verificação estruturada contra os princípios invioláveis.

**Prompt sugerido:**

```
Redija o pacote final da preparação.

<roteiro_reuniao>
Escreva o roteiro em texto corrido (não bullet points — prose curta e natural). Estrutura:

1. ABERTURA (2 min)
- Cumprimento + contexto + valor que já geramos na relação (se houver histórico)
- Uma frase que ancora o "por que estamos aqui agora"

2. ANCORAGEM (3 min)
- Pedido objetivo — o que queremos ao final desta reunião especificamente
- Ancorado na mensagem principal da Etapa 8

3. SONDAGEM (10-15 min)
- 2 a 3 perguntas abertas para entender as restrições reais da contraparte
- Não "vender" — escutar. Anotar o que for surpresa.
- Exemplos de perguntas: "Quais são as principais pressões internas que vocês estão lidando neste ciclo?" / "O que seria um acordo ideal para vocês?"

4. ARGUMENTO (10 min)
- Apresentar 2-3 mensagens de apoio da Etapa 8 com dados e precedentes
- Não leia a tabela — internalize, fale natural
- Pare para escutar reação a cada mensagem

5. FECHAMENTO (5 min)
- Próximo passo concreto (data, responsável, entregável)
- Não saia da reunião sem um próximo passo combinado
- Se não for possível fechar, defina data da próxima conversa
</roteiro_reuniao>

<talk_track_lideranca>
Script de 2-3 minutos para a pessoa da liderança que vai abrir a reunião. Em linguagem natural, sem jargão. Deve cobrir: contexto, valor gerado, pedido, convite ao diálogo. A liderança pode adaptar, mas o script existe como piso.
</talk_track_lideranca>

<kit_materiais>
Lista dos materiais que vão para a reunião (impressos ou digitais):
- Briefing (Etapa 6 resumida em 1 página)
- Argumentário (tabela da Etapa 8)
- Dados de apoio (fontes completas com URLs, caso a contraparte peça)
- One-pager do projeto ou tema
- Quaisquer anexos jurídicos ou contratuais relevantes
- Lista de gatilhos de recuo (da Etapa 9) — NÃO vai para a mesa, é leitura interna da equipe pré-reunião
</kit_materiais>

<auto_verificacao>
Responda cada pergunta com sim/não/parcial + justificativa curta:

1. Inventei algum fato, ator ou evidência que não estava nos insumos?
2. Marquei todas as inferências como [suposição] com justificativa?
3. Toda classificação na tabela de atores tem evidência rastreável?
4. Respeitei o escopo declarado na Etapa 1? (ou expandi silenciosamente?)
5. Fiz a auditoria de equidade da Etapa 4 como infraestrutura, não como checklist de final?
6. Fiz a auditoria de legitimidade da Etapa 7 como infraestrutura, não como decoração?
7. Registrei as decisões dos 3 checkpoints humanos por escrito?
8. A linguagem do argumentário foi revisada contra termos estigmatizantes?
9. Os gatilhos de recuo são concretos (não "recuar se preciso")?
10. O roteiro tem próximo passo explícito e responsável nomeado?

Se respondeu "não" ou "parcial" a qualquer item, volte e corrija antes de entregar o pacote.
</auto_verificacao>
```

**Output esperado:** pacote completo = roteiro (texto corrido) + talk track (script curto) + lista de kit + relatório de auto-verificação com 10 perguntas respondidas. Se o relatório de auto-verificação é todo "sim" sem hesitação, o prompt sugere uma segunda leitura mais crítica — auto-avaliação pro forma é o pior resultado possível desta etapa.

## Checkpoints de validação humana

A skill tem **3 checkpoints obrigatórios**. Todos interrompem o fluxo e aguardam registro explícito antes de prosseguir. Decisão implícita = violação. O conteúdo operacional de cada checkpoint está inline no workflow, nas posições onde é invocado. Resumo para orientação:

- **Checkpoint 1 — pós-E4 (bloqueia E5):** humano valida as ausências da auditoria estrutural e decide quais atores sugeridos entram no mapa. **Verifique:** você concorda com a lista de ausências? Alguma sugestão do modelo não faz sentido no contexto específico? O registro da decisão (entra/anotação/descarta) está escrito?

- **Checkpoint 2 — pós-E5 / pré-E6 (bloqueia Sub-arco 2) — CHECKPOINT FORTE:** decisão política de com quem negociar, por quê, o que está em jogo, e se é bilateral ou multi-parte. Não delegável ao modelo. **Verifique:** a contraparte foi escolhida por interrogação consciente, não por ser "óbvia"? O resultado-alvo e o mínimo aceitável estão no papel? Se multi-parte, você consultou `references/variantes.md`?

- **Checkpoint 3 — pós-E7 (bloqueia E8):** decisão sobre legitimidade da mesa (prosseguir / mitigar / adiar) com base na auditoria da Etapa 7. **Verifique:** a recomendação do modelo foi aceita ou modificada com justificativa? Se prosseguiu com mitigadores, eles têm responsável e prazo? Se prosseguiu assumindo riscos, esse é um assumir *consciente*, não um silêncio?

**Regra geral:** se você não teve tempo de validar um checkpoint, não prossiga. Use a saída da etapa anterior como rascunho interno até a validação ser feita. Rode o checklist completo em `references/checklist.md` antes de publicar qualquer material final.

## Falhas comuns

Estes são os anti-patterns mais frequentes observados quando a skill é mal usada. Todos são evitáveis com disciplina nos princípios e nos checkpoints.

1. **Matriz que só replica o ecossistema oficial.** 100% de atores de fontes institucionais, nenhuma voz comunitária, nenhum trabalhador informal, nenhuma organização sem CNPJ. **Causa-raiz:** pular a Etapa 4 ou fazê-la pro forma ("sim, há ausências" sem nomear nenhuma). **Mitigação:** tratar a Etapa 4 como infraestrutura obrigatória e usar o Checkpoint 1 como bloqueio real, não formal.

2. **MANA fantasma.** Declarar uma MANA sem base operacional real — "se não houver acordo, procuramos outro financiador" quando na verdade nenhuma prospecção foi feita. Blefe em negociação é catastrófico quando testado. **Mitigação:** o Princípio 3 (evidência rastreável) vale para a MANA — exija que a MANA seja descrita em termos operacionais concretos, não declarativos. Se não dá para descrever, a MANA é fraca — nomeie isso.

3. **Objeção preparada virando argumentário agressivo.** A Etapa 9 produz tabela de defesa, e a equipe entra na reunião em modo de confronto. **Mitigação:** o prompt da Etapa 9 enfatiza que preparação é antecipação de posições legítimas, não ensaio de combate. Se o tom ficar agressivo na revisão, reescreva.

4. **Pular o Checkpoint 2.** Avançar direto do mapa para a preparação com a "contraparte óbvia" sem decisão política registrada. **Causa-raiz:** pressão de tempo + a contraparte parece óbvia. **Mitigação:** o CP2 está estruturalmente desenhado para interromper — se a skill avança sem ele, é bug.

5. **Equity como disclaimer final.** Rodar o workflow inteiro e enfiar equidade num parágrafo no fim do relatório. As Etapas 4 e 7 existem exatamente para impedir isso. **Mitigação:** tratar as duas etapas como primeira classe — bloquear avanço até que estejam completas.

## Arquivos complementares

Esta skill vem com três arquivos complementares em `references/`:

- **[`references/exemplos.md`](references/exemplos.md)** — execução completa em um caso realista (OSC de educação em território periférico renegociando contrato plurianual com fundação corporativa). Percorre as 10 etapas + 3 checkpoints em modo `disperso`, mostrando ausências estruturais reveladas na Etapa 4, uso do Checkpoint 2 para escolher a contraparte, auditoria de legitimidade na Etapa 7 com mitigadores, MANA da OSC nomeada como fraca por assimetria estrutural, e pacote final (argumentário + objeções + roteiro).

- **[`references/variantes.md`](references/variantes.md)** — quatro variantes do workflow base:
  - (a) **Multi-parte** — mesa tripartite, audiência pública, coalizão; orientações sobre MANAs assimétricas entre as partes
  - (b) **Atualização de mapa existente** — entra direto em E3 com mapa legado como input (pula E1-E2)
  - (c) **Validação coletiva de ToC com stakeholders** — handoff com `theory-of-change`; o mapa vira insumo de facilitação
  - (d) **Preparação de audiência pública** — adaptações ao kit (talk track em linguagem acessível, tempo majoritário de escuta, pré-leitura distribuída antes do evento)

- **[`references/checklist.md`](references/checklist.md)** — checklist humana com duas seções: **Técnica** (rastreabilidade de evidências, cobertura dos 4 quadrantes, MANA fundamentada, gatilhos de recuo explícitos) e **Equidade** (subset operacional de `docs/equity-lens.md` adaptado: ausências estruturais nomeadas, legitimidade da mesa auditada, linguagem revisada, assimetria de MANA explicitada como poder estrutural, mitigadores registrados, grupos afetados com caminho pós-acordo).

Para o framework geral de equidade, consulte [`docs/equity-lens.md`](../../docs/equity-lens.md).
