---
name: accessible-communication
description: Transforma um documento institucional (edital, aviso, relatório, nota técnica, normativo) em kit multicanal com linguagem simples, acessibilidade como propriedade obrigatória de toda peça e kit de validação com público-alvo.
---

# Comunicação Acessível e Multicanal

## Quando usar esta skill

Esta skill transforma **um documento institucional** (edital, aviso, relatório, nota técnica, normativo, cartilha) em **kit multicanal de comunicação** — com acessibilidade como propriedade obrigatória de toda peça, não como modo opcional.

Use quando o usuário:

- Precisa transformar edital, aviso, relatório ou normativo em comunicação que chega a quem não lê juridiquês
- Tem uma nota técnica pronta e precisa levar o conteúdo para a sociedade
- Vai publicar informação sobre um programa e precisa de FAQ, SMS, post, release e carrossel ao mesmo tempo
- Precisa produzir peças que atravessem canais com cobertura real no público-alvo, sem assumir smartphone universal
- Tem conteúdo que precisa circular em mais de um idioma (fronteira, línguas indígenas, libras como texto)
- Recebeu pedido de "simplificar" um documento e quer resistir à armadilha de "simplificar = infantilizar"

Sinais típicos na conversa do usuário:

- "Preciso transformar esse edital em post"
- "Tem esse relatório, como faço virar comunicação pra rede social?"
- "Precisamos levar essa informação pro público que não lê juridiquês"
- "Tem um aviso pra publicar, preciso de FAQ, SMS e release ao mesmo tempo"
- "A campanha precisa chegar em populações que falam mais de um idioma"
- "Esse documento está técnico demais, precisa virar linguagem simples"
- "Produzi uma nota técnica com a skill X, agora preciso comunicar pra sociedade"

Relação com outras skills do repositório (upstream):

- **`technical-note-writing` → accessible-communication** — nota técnica pronta vira kit de comunicação da nota, com rastreabilidade preservada (variante V1 em `references/variantes.md`)
- **`theory-of-change` → accessible-communication** — ToC vira peças de comunicação da cadeia causal do programa; os "dados críticos" viram indicadores, marcos e grupos alcançados (variante V4)
- **`evidence-synthesis` → accessible-communication** — matriz sintetizada vira narrativa acessível com rastreabilidade às fontes originais
- **Documento solto** — edital, aviso, normativo, relatório, cartilha (caminho mais comum)

Downstream: nenhum. Esta skill é **ponto de saída** da cadeia institucional → sociedade. O que vem depois é publicação, monitoramento de recepção e validação em campo — fora do escopo desta skill.

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Um documento-fonte** — arquivo, texto colado, URL, ou output de outra skill do repo (`technical-note-writing`, `evidence-synthesis`, `theory-of-change`). Sem documento-fonte, a skill não tem matéria-prima — comunicação sem base vira improviso ou invenção.

2. **Declaração dos públicos-alvo reais** — não "o público em geral"; recortes específicos. Exemplos bons: "estudantes do ensino médio da rede pública de SP", "mães beneficiárias do programa X no município Y", "jornalistas de política urbana em veículos locais", "famílias de pescadores artesanais do litoral norte". Exemplos ruins: "a sociedade", "o cidadão", "todos os interessados". Recorte específico é pré-condição para que a Etapa 6 gere um kit de validação usável.

3. **Declaração dos canais pretendidos** — lista dos canais onde as peças vão circular, com **honestidade sobre cobertura**. "SMS só se o público realmente tem celular ativo" — não invente canal por elegância. A Falha Comum nº 5 é exatamente escolher canal sem validar cobertura real.

4. **Dados críticos imutáveis identificáveis no documento** — prazos, valores, locais, URLs, contatos, nomes oficiais. A skill vai indexar e proteger literalmente. Se o documento tem data errada, a skill vai propagá-la — a responsabilidade pela fonte é humana.

5. **Disposição para auditoria de framing na fonte** — a Etapa 2 força decisão política sobre reframe de linguagem problemática herdada do documento-fonte. Usuários que só querem "copiar o edital bonitinho" sem interrogar como a fonte nomeia o público não serão bem servidos — a saída vai reproduzir o deficit framing original.

6. **Aceitação de que validação real com público é responsabilidade humana.** A skill entrega o kit de validação (Etapa 6), não executa a validação. Não há atalho aqui — "personas simuladas" são proibidas como substituto (Princípio 5).

Se algum desses elementos não está pronto, a skill **pergunta antes de avançar** — não inventa silenciosamente.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Dados críticos são literais.** Prazos, valores, locais, URLs, contatos, nomes oficiais — nunca modificar, parafrasear, arredondar ou "melhorar a fluência". Se faltar, escrever `não encontrado` literal. Comunicação institucional com data errada é **dano material ao público** — pessoa vai à prefeitura no dia errado, perde prazo de inscrição, clica em link que não existe. Este é o princípio mais protegido da skill: toda peça passa por auditoria específica na Etapa 5 eixo factual.

2. **Linguagem simples ≠ linguagem reducionista.** Simplificar **estrutura de frase e vocabulário**, preservar integralmente a **complexidade conceitual**. Frase curta não significa conceito raso. A anti-infantilização é explícita: testar cada parágrafo contra a pergunta "estou falando com adulto ou tratando como criança?". "Você quer participar do edital? Então você precisa mandar papéis! Vamos te explicar!" é o que a skill **não** faz.

3. **Lente de equidade é upstream + downstream, não checklist final.** Auditoria do documento-fonte acontece **antes** de qualquer geração (Etapa 2); auditoria das peças derivadas acontece **durante** a revisão 4 eixos (Etapa 5). Equidade no final é disclaimer — equidade distribuída em duas etapas estruturais é infraestrutura. Ver `docs/equity-lens.md` para o framework compartilhado do repositório.

4. **Acessibilidade é propriedade obrigatória, não modo opcional.** Toda peça gerada passa pelos critérios de acessibilidade, **mesmo a release para imprensa especializada**. Não existe "versão acessível" como peça separada — existe **peça acessível** como única peça. Tratar acessibilidade como modo opcional reproduz o anti-pattern clássico em comunicação institucional: "kit bonito" primeiro e "versão acessível feia" depois.

5. **Validação com público real é responsabilidade humana.** A skill produz o **kit de validação** (Etapa 6), não substitui a coisa real. **Proibido usar "personas simuladas" como substituto.** Colega de OSC com mestrado não é "pessoa em vulnerabilidade social". Simular público em conversa com o modelo é teatro de validação, não validação.

6. **Anti-hallucination: `não encontrado` + `[suposição]` explícitos.** Quando dado ausente do documento-fonte, escrever `não encontrado` literal. Quando a skill propõe adaptação sem base (ex: tom de um post sem diretriz de marca disponível), marcar `[suposição]` + justificativa curta. Sem essas marcas, suposição vira "fato" na cabeça de quem lê.

**Estas não são regras opcionais.** A skill existe porque comunicação institucional inacessível exclui sistematicamente os públicos que mais precisam da informação. Relaxar os princípios é reproduzir exatamente o que a skill se propõe a combater.

## O workflow (7 etapas)

O trabalho é organizado em 7 etapas sequenciais. **Etapa 1** configura o trabalho, indexa dados críticos e carrega a linha de base de linguagem simples. **Etapa 2** audita o documento-fonte (equidade upstream) — primeiro checkpoint humano. **Etapa 3** produz a versão canônica em linguagem simples, da qual todas as outras peças derivam. **Etapa 4** gera as peças selecionadas pelo usuário. **Etapa 5** faz revisão 4 eixos (equidade downstream) — segundo checkpoint humano. **Etapa 6** produz o kit de validação com público-alvo real. **Etapa 7** é autoverificação final contra os princípios.

Cada etapa tem **objetivo** específico, **prompt sugerido** pronto para copiar (com tags XML `<principios>`, `<escopo>`, `<insumos>`, `<dados_criticos>`, `<notas_framing>`, `<linha_base>`, `<peca>`, `<auditoria>`, `<kit_validacao>`, `<autoverificacao>` — prática recomendada pela Anthropic), e **output esperado** que alimenta a etapa seguinte. **Não pule etapas**, especialmente E2, E5 e E6 — as duas primeiras contêm os checkpoints humanos obrigatórios, a terceira é o instrumento que impede acessibilidade performativa.

### Etapa 1 — Configuração, dossiê e indexação de dados críticos

**Objetivo:** declarar tipo de input (documento solto ou chain-in de outra skill), públicos-alvo reais, canais pretendidos, idiomas; carregar insumo; **indexar dados críticos imutáveis** como tabela tipada com IDs (`DC01`, `DC02`, etc.); marcar checklist de peças a produzir; **carregar `references/plain-language-baseline.md`** como contexto ativo para toda a execução.

**Prompt sugerido:**

````
Você vai me ajudar a transformar um documento institucional em kit multicanal de comunicação, seguindo a skill accessible-communication. Antes de começar, confirme que entendeu as regras.

<principios>
1. Dados críticos são literais — nunca modificar prazo, valor, local, URL, contato, nome oficial. "Não encontrado" quando faltar.
2. Linguagem simples ≠ linguagem reducionista. Anti-infantilização explícita.
3. Lente de equidade é upstream (E2) + downstream (E5).
4. Acessibilidade é propriedade obrigatória de toda peça — não modo opcional.
5. Validação com público real é responsabilidade humana. Personas simuladas proibidas como substituto.
6. Toda adaptação sem base marcada [suposição] + justificativa.
</principios>

<escopo>
- Tipo de input: [documento_solto | chain_technical_note | chain_evidence_synthesis | chain_theory_of_change]
- Documento-fonte (texto, arquivo, URL ou output de skill): [COLE AQUI ou anexe]
- Públicos-alvo reais (recortes específicos, NÃO "público geral"):
  - Público 1: [ex: mães beneficiárias do programa Bolsa Cultura do município X]
  - Público 2: [ex: jornalistas de política cultural em veículos locais]
  - Público N: ...
- Canais pretendidos (com cobertura real do público, não aspiracional):
  - Canal 1: [ex: WhatsApp — comprovadamente usado pelo público 1]
  - Canal 2: [ex: site da secretaria — usado por jornalistas]
  - Canal N: ...
- Idiomas: [PT-BR / outros]
</escopo>

<linha_base>
Carregue references/plain-language-baseline.md como contexto ativo. Aplique a disciplina do Plain Language movement + tom inclusivo da Linguagem Cidadã, sem infantilização nem reducionismo. As 10 regras operacionais orientam TODA a geração a partir da Etapa 3.
</linha_base>

<dados_criticos>
Extraia do documento-fonte uma tabela de dados imutáveis. Formato:
DC_ID | Tipo | Valor literal | Onde aparece no documento-fonte

Tipos obrigatórios a varrer:
- prazo (datas, janelas, períodos de inscrição)
- valor (R$, percentuais, limites)
- local (endereço, órgão, plataforma)
- URL (links oficiais)
- contato (telefone, email)
- nome oficial (programa, edital, órgão, autoridade)

Regra: valor literal exatamente como está no documento. Não normalize formato de data. Não arredonde valores. Se um dado parece estar no documento mas você não consegue citar trecho literal, marque "não encontrado" e peça ao usuário para confirmar.
</dados_criticos>

<checklist_de_pecas>
Apresente o menu abaixo. O usuário marca quais peças quer produzir. A skill produz APENAS as marcadas. Exceção: a versão em linguagem simples (Etapa 3) é sempre produzida internamente, mesmo que não esteja marcada — serve como linha de base canônica para derivar as outras.

[ ] linguagem simples (linha de base canônica)
[ ] FAQ (perguntas do ponto de vista do público)
[ ] SMS (≤160 caracteres)
[ ] WhatsApp (≤300 caracteres)
[ ] post redes sociais (título ≤60 chars + copy 100-150 palavras)
[ ] carrossel 5-7 cards
[ ] roteiro de vídeo 2 min
[ ] release imprensa
[ ] newsletter 300-400 palavras
[ ] roteiro de áudio 30-60s
[ ] alt text (para imagens fornecidas ou por descrever)
[ ] versões multi-idioma (declarar quais)
</checklist_de_pecas>

Ao terminar, responda literalmente:
"OK — regras aceitas. Escopo capturado. [N] dados críticos indexados. [M] peças marcadas para produção. Linha de base carregada. Pronto para Etapa 2 (auditoria de framing)."
````

**Output esperado:** handshake explícito + tabela de dados críticos com DC_IDs + checklist de peças marcadas + confirmação de carga da linha de base. Se a skill pular direto para a Etapa 2 sem esse handshake, o usuário volta e exige — é função do prompt forçar o aceite.

### Etapa 2 — Auditoria de equidade upstream (documento-fonte)

**Objetivo:** auditar o documento-fonte em busca de framing problemático **antes de qualquer geração**. Se o edital chama o público de "beneficiários carentes", essa formulação vai vazar para o FAQ, o SMS, o post, o release — corrigir em 6 lugares depois é trabalho em 6 lugares; decidir aqui é trabalho em 1 lugar, uma vez.

A auditoria varre 4 dimensões: nomeação do público, vozes presentes/ausentes, assimetrias institucionais e termos estigmatizantes. Para cada ponto identificado, a skill **propõe duas opções** — reframe (reformulação aplicada nas peças derivadas) ou espelhar (preservar o termo original, com justificativa). O usuário decide explicitamente cada ponto. Esta é uma decisão política, não estética.

**Prompt sugerido:**

````
Agora faça auditoria de equidade do documento-fonte ANTES de qualquer geração.

<auditoria_fonte>
Analise o documento-fonte em 4 dimensões:

1. NOMEAÇÃO DO PÚBLICO
Como a fonte chama quem tenta alcançar? Liste os termos textuais entre aspas.
Há termos de deficit ("beneficiário carente", "público vulnerável", "pessoas em situação de vulnerabilidade" sem qualificador, "minorias", "assistidos")? Liste cada um.

2. VOZES PRESENTES/AUSENTES
Quem fala no documento? (instituição, autoridade, especialistas)
Quem é falado sobre? (público-alvo, "beneficiários", "interessados")
Há alguma voz do próprio público-alvo (testemunho, citação, resultado de escuta)?

3. ASSIMETRIAS INSTITUCIONAIS
O documento posiciona a instituição como "provedora" e o público como "receptor passivo"? Cite frases que sustentam essa leitura (ou afirme o contrário com evidência).

4. TERMOS ESTIGMATIZANTES
Há linguagem que marca grupos de forma problemática? (ex: "idosos", "deficientes", "portadores", "normal" por oposição, "em risco", "carentes")

Para CADA ponto identificado, proponha DUAS opções:
- REFRAME — reformulação que a skill vai aplicar em TODAS as peças derivadas (e registrar nas notas de framing)
- ESPELHA — preservar o termo original literal na peça derivada (com nota de justificativa, tipicamente "termo juridicamente definido no edital, não reescrevível")

Produza uma tabela de notas de framing:
Ponto | Termo original | Decisão (reframe|espelha) | Formulação substituta (se reframe) | Justificativa
</auditoria_fonte>

Ao terminar, pare e peça CONFIRMAÇÃO EXPLÍCITA do usuário para cada linha da tabela. Decisão implícita não conta.
````

**Output esperado:** tabela de notas de framing com uma linha por ponto identificado, cada linha com `(a) termo original / (b) decisão reframe|espelha / (c) formulação substituta se reframe / (d) justificativa`. Mínimo de 3 pontos auditados — menos que isso sugere auditoria superficial, prompt reforça.

---

### CHECKPOINT HUMANO CH1 — pós-E2 (bloqueia E3)

**Pergunta obrigatória ao humano:**

> Revise a tabela de notas de framing. Para cada ponto, confirme a decisão:
>
> - **REFRAME** — a skill vai aplicar a formulação substituta em todas as peças derivadas. Registre por escrito qual é a formulação.
> - **ESPELHA** — o termo original será preservado literal nas peças derivadas. Registre a justificativa (tipicamente: termo juridicamente definido, citação obrigatória, ou nome próprio).
>
> Registre por escrito sua decisão ponto a ponto. A skill não avança para a Etapa 3 sem esse registro.

Se o humano der "ok, avança" sem decisão explícita por linha, o prompt reitera. **Decisão implícita = decisão do modelo = violação do Princípio 3** (equidade upstream). Esta é a decisão política mais consequente da skill inteira — o reframe aqui trava o que vai virar linguagem padrão em 5-10 peças derivadas. Errar aqui contamina o kit inteiro.

### Etapa 3 — Linha de base em linguagem simples

**Objetivo:** produzir a **versão canônica em linguagem simples** do documento-fonte, da qual todas as outras peças serão derivadas. Esta versão é **sempre produzida internamente**, mesmo que o usuário não tenha marcado "linguagem simples" no checklist da Etapa 1. Ela é o filtro estrutural que impede jargão residual de vazar para as peças finais.

A estrutura obrigatória segue a ordem **o que é → para quem → como fazer → quando → onde → quanto**. O documento-fonte pode estar organizado de outra forma; a linha de base reorganiza para o leitor. A Etapa aplica literal as 10 regras de `references/plain-language-baseline.md` e preserva os DC_IDs indexados na Etapa 1 exatamente como estão.

**Prompt sugerido:**

````
Produza a linha de base em linguagem simples do documento-fonte, aplicando a disciplina de plain-language-baseline.md e as notas de framing confirmadas no Checkpoint CH1.

<linha_base>
Estrutura obrigatória do texto (use como esqueleto):

1. O QUE É — uma frase curta explicando o que o documento oferece/anuncia/regula.
2. PARA QUEM — quem pode participar/acessar/usar. Critérios de elegibilidade em ordem de maior para menor excludente.
3. COMO FAZER — instrução operacional, em ordem condição-ação ("Se você já tem cadastro, acesse X. Se ainda não tem, primeiro faça Y").
4. QUANDO — prazos, janelas, datas. Use DC_IDs literal.
5. ONDE — endereço físico, link, telefone. Use DC_IDs literal.
6. QUANTO — valores, gratuidade, contrapartidas. Use DC_IDs literal.
</linha_base>

<regras_operacionais>
Aplique literal as 10 regras de plain-language-baseline.md:
1. Frase direta sujeito-verbo-complemento, ≤20 palavras.
2. Voz ativa por default.
3. Um conceito por parágrafo.
4. Palavra comum substitui sinônimo erudito sem perder precisão.
5. Sigla só após expansão na primeira ocorrência.
6. Dados numéricos com unidade e referência temporal explícitas.
7. Instrução condicional em ordem condição-ação.
8. Segunda pessoa direta ("você") ou terceira impessoal ("a pessoa interessada"); nunca "o beneficiário".
9. Anti-diminutivo, anti-exclamação, anti-emoji como substituto de palavra.
10. Verbos de ação explícitos substituem substantivos processuais ("realização da inscrição" → "se inscrever").
</regras_operacionais>

<preservacao_dc>
Todo dado crítico referenciado precisa ser rastreável ao DC_ID da Etapa 1. Inline: "prazo de inscrição: 30 de maio de 2026 (DC01)". Não parafraseie datas. Não arredonde valores. Se um dado não foi indexado, marque "não encontrado — preciso que o usuário confirme".
</preservacao_dc>

<notas_framing>
Aplique as decisões de reframe confirmadas no CH1. Toda ocorrência do termo original vira a formulação substituta. Termos marcados como "espelhar" permanecem literal.
</notas_framing>

<anti_infantilizacao>
Antes de finalizar, teste cada parágrafo contra a pergunta: "Estou falando com adulto ou tratando como criança?" Se o parágrafo soa como "você precisa mandar seus papéis, olha só como é fácil!", reescreva. Falar simples ≠ falar paternal.
</anti_infantilizacao>
````

**Output esperado:** versão única em linguagem simples, estruturada nas 6 seções obrigatórias, com rastreabilidade inline aos DC_IDs, com notas de framing aplicadas, testada contra infantilização. Esta versão é **artefato interno obrigatório** mesmo que o usuário não tenha pedido — é a âncora de todas as derivações da Etapa 4.

### Etapa 4 — Derivação das peças selecionadas

**Objetivo:** gerar cada peça marcada pelo usuário no checklist da Etapa 1 **a partir da linha de base da Etapa 3**, não do documento-fonte original. A Falha Comum nº 1 é exatamente gerar peças direto do documento original — o jargão residual vaza para todas as derivações.

Cada peça segue o molde do seu formato, preserva literal os DC_IDs, aplica as notas de framing, e respeita a disciplina da linha de base. Peças multi-idioma passam pela Etapa 3 no próprio idioma — não são tradução literal da versão PT.

**Prompt sugerido:**

````
Derive cada peça marcada no checklist, PARTINDO DA LINHA DE BASE DA ETAPA 3, não do documento original.

<peca tipo="FAQ">
Perguntas formuladas do ponto de vista do PÚBLICO, não da instituição.
- ERRADO: "Sobre o processo de inscrição"
- CERTO: "Como me inscrevo?"

Perguntas obrigatórias (nesta ordem):
1. Quem pode participar?
2. Como se inscrever?
3. Quais documentos preciso ter?
4. Quais os prazos e locais?
5. Quanto custa? (ou: É gratuito?)
6. Onde tirar dúvida?

Rodapé obrigatório: "Atualizado em: AAAA-MM-DD".
</peca>

<peca tipo="SMS">
Máximo 160 caracteres. Chamada para ação + link oficial. Sem infantilização. Sem diminutivo. Sem emoji como substituto de palavra.
Exemplo de molde: "[Nome do programa]: inscrições abertas até [DC prazo]. Saiba como participar em [DC URL]. Dúvidas: [DC contato]."
</peca>

<peca tipo="WhatsApp">
Máximo 300 caracteres. Mesmo espírito do SMS, com espaço extra para contexto curto.
</peca>

<peca tipo="post_redes">
Título ≤60 caracteres.
Copy 100-150 palavras.
Sem emojis como substituto de palavra.
Sem hashtags que não foram fornecidas pelo usuário.
CTA claro no final.
</peca>

<peca tipo="carrossel">
5 a 7 cards. Cada card: máximo 2 frases.
Estrutura: abertura (card 1) + 3-5 cards de dados-chave + card final com CTA + card de fontes.
Dados críticos na cara: cada DC_ID relevante aparece literal em pelo menos um card.
</peca>

<peca tipo="roteiro_video">
Duração-alvo: 2 minutos (aprox. 300 palavras faladas).
Estrutura: abertura (5s) + contexto (20s) + achados principais (60s) + implicações (20s) + CTA (15s).
Frases curtas adequadas à fala (não à leitura).
Indicações visuais em colchetes: [imagem: fachada do órgão X] [gráfico: crescimento 2022-2024].
</peca>

<peca tipo="release_imprensa">
Pirâmide invertida. Lead no primeiro parágrafo respondendo o-quê, quem, quando, onde, por-quê. Dois parágrafos de contexto. Seção final de serviço com DC_IDs literal (prazo, local, URL, contato).
Citação só se fornecida pelo usuário — NÃO invente citação de autoridade.
</peca>

<peca tipo="newsletter">
300-400 palavras.
Assunto ≤50 caracteres.
Pré-cabeçalho ≤80 caracteres (aparece na caixa de entrada antes do clique).
3 blocos: "Por que isso importa" + "O que o [programa/edital] mostra" + "O que você pode fazer agora".
</peca>

<peca tipo="roteiro_audio">
30 a 60 segundos (75-150 palavras faladas).
Para quem ouve sem ver. Menciona prazos, elegibilidade, como fazer, contato.
Frases adequadas à fala. Sem siglas não expandidas.
</peca>

<peca tipo="alt_text">
1-2 frases objetivas.
Menciona dados críticos quando aparecem na arte (ex: data no banner, valor destacado).
DECISÃO POLÍTICA EXPLÍCITA: se a imagem tem conteúdo político (foto de protesto, de condição social, de ação comunitária), o alt text NÃO pode neutralizar. Ver Falha Comum nº 4.
</peca>

<peca tipo="multi_idioma">
Cada idioma passa pela Etapa 3 NO SEU PRÓPRIO IDIOMA. Não é tradução literal do PT.
Se o modelo não tem cobertura adequada no idioma alvo, declare como RISCO e pare — não produza versão mal feita.
</peca>

<regras_comuns_todas_as_pecas>
- Toda peça parte da linha de base da Etapa 3, NÃO do documento original.
- Todo DC_ID referenciado aparece literal (prazo, valor, local, URL, contato, nome oficial).
- Toda decisão de reframe do CH1 está aplicada.
- Toda adaptação sem base (tom, voz, estilo de marca) está marcada [suposição] + justificativa.
- Nenhuma peça contém "tratamento infantil" — reler contra a regra 10 da linha de base antes de fechar.
</regras_comuns_todas_as_pecas>
````

**Output esperado:** N peças conforme checklist, cada uma com rastreabilidade inline aos DC_IDs, aplicando notas de framing, seguindo o molde do seu formato, sem jargão residual (porque deriva da Etapa 3, não do original), sem infantilização.

### Etapa 5 — Revisão 4 eixos (equidade downstream)

**Objetivo:** auditoria estruturada das peças derivadas em 4 eixos **independentes**. Esta é a segunda etapa estrutural de equidade (a Etapa 2 foi a auditoria upstream). Aqui o trabalho é verificar que o que saiu da Etapa 4 preserva o que foi decidido no CH1, preserva os DC_IDs literal, aplica consistentemente a linha de base, e é internamente consistente entre peças.

Cada eixo produz **correções propostas** que o humano revisa no CH2 e decide item a item aceitar ou rejeitar. A skill aplica só as aceitas — não é rubber stamp.

**Prompt sugerido:**

````
Audite cada peça produzida na Etapa 4 contra os 4 eixos abaixo. Para cada achado, proponha uma correção concreta que o usuário vai aceitar ou rejeitar no Checkpoint CH2.

<auditoria>

1. EIXO FACTUAL
Para cada peça, verificar:
- Todos os DC_IDs indexados na Etapa 1 aparecem literal onde deveriam?
- Algum dado crítico foi parafraseado? (ex: "final de maio" em vez de "30 de maio")
- Algum dado crítico foi omitido?
- Há afirmação que não está ancorada no documento-fonte nem nos DCs?
- Há "não encontrado" que precisa ser completado pela equipe antes da publicação?

2. EIXO EQUIDADE
Para cada peça, verificar:
- As decisões de reframe do CH1 foram preservadas? Se foi "reframe", a formulação substituta aparece? Se foi "espelhar", o termo original aparece intacto?
- Alguma peça introduziu novo framing problemático QUE NÃO ESTAVA NO ORIGINAL? (ex: post criou diminutivo "criançada" que não estava no edital)
- Alt text estereotipa pessoas ou neutraliza conteúdo político que não deveria ser neutralizado?
- A linguagem é não-estigmatizante em todas as peças?

3. EIXO ACESSIBILIDADE
Para cada peça, verificar:
- A peça aplica consistentemente as 10 regras da linha de base (plain-language-baseline.md)?
- Há resíduo de jargão jurídico/técnico que escapou da Etapa 3?
- A linguagem é simples SEM ser infantilizada? (teste anti-infantilização do parágrafo por parágrafo)
- Alt text é suficiente para quem não vê a imagem?
- O canal escolhido combina com o formato? (ex: SMS realmente cabe em 160 chars; WhatsApp em 300)
- Siglas têm expansão na primeira ocorrência?

4. EIXO CONSISTÊNCIA ENTRE PEÇAS
Verificar a coleção inteira:
- Os dados críticos batem entre todas as peças? (o prazo é o mesmo no FAQ, no SMS, no post, no release?)
- O tom é consistente? (post não está performático enquanto release está burocrático)
- As peças "conversam" entre si? (quem leu o SMS consegue achar o FAQ citado? o release aponta para o mesmo link que o WhatsApp?)
- Se há multi-idioma, as versões são equivalentes em substância (não tradução literal)?

Para CADA achado, escreva uma linha de proposta de correção:
Peça | Eixo | Achado | Correção proposta | Aceitar? (a decidir pelo usuário)
</auditoria>

Ao terminar, pare e aguarde o CH2. NÃO aplique correções silenciosamente.
````

**Output esperado:** tabela única com todas as correções propostas por peça por eixo. Se a tabela está vazia, o prompt avisa: "auditoria sem achados em 0 peças é improvável — releia os 4 eixos com olho crítico e tente de novo".

---

### CHECKPOINT HUMANO CH2 — pós-E5 (bloqueia E6)

**Pergunta obrigatória ao humano:**

> Revise a tabela de correções propostas. Para cada linha, decida:
>
> - **ACEITA** — a skill aplica a correção na peça.
> - **REJEITA** — a skill mantém a peça como está. Registre por que (às vezes a "correção" é falso positivo da auditoria).
> - **AJUSTA** — você propõe formulação alternativa; a skill aplica a sua.
>
> Registre por escrito ponto a ponto. A skill não avança para a Etapa 6 sem esse registro explícito. Rubber stamp ("aceitar tudo") pede confirmação dupla — aceitar sem ler é violação do princípio.

**Por que este checkpoint existe:** a auditoria da Etapa 5 é produção de hipóteses pelo modelo. Aceitar tudo sem revisão reproduz o problema em outra direção — o modelo pode propor correções que "soam certas" mas são inadequadas ao contexto específico (ex: propor reframe de termo que é juridicamente definido e não pode ser mexido).

### Etapa 6 — Kit de validação com público-alvo

**Objetivo:** produzir **instrumento concreto** para o humano validar as peças com 3-5 pessoas do público-alvo real declarado na Etapa 1. A skill **não executa** a validação — executa é responsabilidade humana (Princípio 5). Mas **obriga o artefato a sair** — instrumento pronto na mão torna mais provável que a validação aconteça, e o instrumento nomeia explicitamente o que NÃO conta como validação.

O output é um documento curto (uma página), pronto para uso em campo por uma pessoa que não é pesquisadora de UX — gestor público, voluntário de OSC, estagiário de comunicação.

**Prompt sugerido:**

````
Produza o kit de validação com público-alvo real. O kit é para ser usado em campo por 3-5 entrevistas de 10-15 minutos com pessoas do recorte específico declarado na Etapa 1.

<kit_validacao>

SEÇÃO 1 — ROTEIRO DE ENTREVISTA (10-15 MIN)
- Público a entrevistar: [repetir literal o recorte declarado na Etapa 1]
- Quantas pessoas: 3 a 5 (menos que 3 é amostra insuficiente; mais que 5 não agrega neste estágio)
- NÃO valem como validação: colegas de equipe, proxies demográficos ("é parecido com o público"), familiares, outros profissionais do setor. Ver Falha Comum nº 6.
- Formato: conversa individual, presencial de preferência, ou WhatsApp/telefone se a distância impedir.
- Roteiro de abertura: "Estou testando um material de comunicação sobre [tema]. Queria sua opinião honesta — não é prova nem pesquisa formal. Você pode falar o que quiser, inclusive 'não entendi'."

SEÇÃO 2 — PERGUNTAS DE COMPREENSÃO POR PEÇA
Para CADA peça do kit (FAQ, SMS, post, etc.), faça 4-5 perguntas no formato:
- "O que essa peça está te pedindo pra fazer?"
- "Qual é o prazo mencionado aqui?"
- "Pra quem essa informação é?"
- "Onde você vai tirar dúvida se precisar?"
- "O que te impediria de fazer o que a peça pede?"

IMPORTANTE: não pergunte "você entendeu?" — ninguém responde "não" a essa pergunta. Pergunte o que a pessoa entendeu.

SEÇÃO 3 — PONTOS DE ATENÇÃO POR TIPO DE PÚBLICO
Para o recorte específico declarado, adicione pontos de atenção.
Exemplos (personalize ao caso real):
- Público é idoso rural → perguntar sobre acesso a smartphone ANTES de mostrar QR code; perguntar se aparelho tem plano de dados ativo.
- Público é jovem estudante → perguntar se lê email institucional ou só rede social; perguntar qual rede social usa.
- Público fala língua indígena como primeira língua → perguntar em qual idioma prefere receber; oferecer as duas versões e pedir preferência.
- Público tem pouca leitura formal → perguntar se prefere áudio a texto; ler em voz alta se preciso.

SEÇÃO 4 — CRITÉRIOS DE "QUANDO REGENERAR A PEÇA"
- Se ≥2 de 5 pessoas não identificaram o prazo correto → regenerar SMS/WhatsApp/FAQ.
- Se ≥1 de 5 pessoas entendeu "não é pra mim" quando é pra ela → regenerar o "para quem" (nomeação do público) na linha de base (Etapa 3) e rederivar todas as peças.
- Se o alt text foi lido como "sobre algo diferente" da imagem → regenerar alt text.
- Se 0 de 5 pessoas conseguiu explicar o próximo passo → o problema não é na peça, é na linha de base. Volte à Etapa 3.

SEÇÃO 5 — NOTA EXPLÍCITA: O QUE NÃO É VALIDAÇÃO
"Perguntar para colegas da equipe que se parecem com o público" não é validação. Colega de OSC com mestrado não é "pessoa em vulnerabilidade social". Colega da secretaria que mora no mesmo bairro do público-alvo não é "representante". Personas simuladas em conversa com IA também não contam. Validação com público real é a coisa real, não proxy.

Se o usuário não tem tempo ou condições para rodar a validação em campo, REGISTRE ISSO COMO RISCO DECLARADO na Etapa 7, seção "riscos". Não omita — omissão é dano ao público.
</kit_validacao>
````

**Output esperado:** kit de uma página (400-700 palavras) pronto para uso em campo, estruturado nas 5 seções acima, com o público-alvo nomeado literal no roteiro, perguntas específicas por peça, e nota explícita sobre o que NÃO conta como validação.

### Etapa 7 — Autoverificação

**Objetivo:** checagem final contra os 6 princípios invioláveis. Para cada princípio, declarar explicitamente como foi honrado no trabalho produzido. Listar todos os `não encontrado` remanescentes. Listar todos os `[suposição]` remanescentes. Listar riscos registrados (em especial: "validação em campo não será feita por prazo" — CH implícito da skill não atendido). Concluir com resumo de entrega.

Se a autoverificação é toda "sim" sem hesitação, o prompt pede uma segunda leitura mais crítica — auto-avaliação pro forma é o pior resultado possível desta etapa.

**Prompt sugerido:**

````
Faça a autoverificação final contra os 6 princípios invioláveis.

<autoverificacao>
Para cada princípio, responda EXPLICITAMENTE como foi honrado, citando etapa/peça/linha quando possível:

1. Dados críticos literais — todos os DC_IDs indexados na Etapa 1 aparecem literal nas peças derivadas onde deveriam? Há algum dado parafraseado que escapou da revisão 4 eixos?
2. Linguagem simples ≠ reducionista — a produção passou pelo teste anti-infantilização parágrafo a parágrafo? Onde você teve que reescrever?
3. Lente de equidade upstream + downstream — a Etapa 2 produziu notas de framing que foram aplicadas? A Etapa 5 eixo 2 auditou a preservação dessas notas? Cite as linhas da tabela.
4. Acessibilidade obrigatória em toda peça — nenhuma peça ficou de fora do rigor? (em especial, a release para imprensa especializada)
5. Validação responsabilidade humana — o kit da Etapa 6 nomeia o público real e explicita o que NÃO é validação?
6. Anti-hallucination — todos os "não encontrado" estão listados? Todos os "[suposição]" estão listados?

<nao_encontrado>
Liste todos os "não encontrado" remanescentes. Cada um precisa ser completado pela equipe antes da publicação. Indique quem provavelmente tem a informação (jurídico? autor original? cadastro?).
</nao_encontrado>

<suposicao>
Liste todos os "[suposição]" remanescentes com justificativa. Cada um precisa ser validado internamente antes da publicação.
</suposicao>

<riscos>
Liste riscos declarados. Em especial:
- Validação em campo não será feita (se for o caso) — risco de acessibilidade performativa.
- Canal com cobertura duvidosa no público (se for o caso) — risco de peça que não chega.
- Multi-idioma em idioma com cobertura incerta do modelo (se for o caso) — risco de qualidade desigual.
- Termos "espelhados" que permanecem problemáticos mas não puderam ser alterados — risco de reprodução de framing.
</riscos>

<resumo_entrega>
N peças produzidas: [listar]
Público-alvo declarado: [repetir literal]
Canais declarados: [repetir literal]
Idiomas: [repetir literal]
Kit de validação: entregue / pendente
Próximo passo (humano): [rodar validação em campo + aplicar correções + publicar]
</resumo_entrega>
</autoverificacao>

Se a autoverificação é toda "sim" sem hesitação, RELEIA CRITICAMENTE e declare pelo menos uma dúvida ou tensão. Auto-avaliação pro forma é o pior resultado possível desta etapa.
````

**Output esperado:** relatório de autoverificação estruturado, com as 6 respostas aos princípios, listas de `não encontrado` / `[suposição]` / riscos, e resumo de entrega. Fim da execução da skill.

## Checkpoints de validação humana

A skill tem **2 checkpoints obrigatórios** mais **1 implícito** fora do escopo da skill. Todos os obrigatórios interrompem o fluxo e aguardam registro explícito antes de prosseguir. Decisão implícita = violação.

### Checkpoint CH1 — pós-E2 (bloqueia E3)

O humano confirma, linha a linha, as decisões de reframe/espelhar da auditoria de equidade upstream. Decisão política, não estética, registrada por escrito.

**Por quê:** o reframe aqui trava o que vai virar linguagem padrão em 5-10 peças derivadas. Errar aqui contamina o kit inteiro. Delegar ao modelo é delegar decisão política sobre como nomear o público — o oposto do que a skill existe para fazer.

### Checkpoint CH2 — pós-E5 (bloqueia E6)

O humano revisa as correções propostas pela revisão 4 eixos e decide, item a item, aceitar / rejeitar / ajustar. A skill aplica só o decidido. Não é rubber stamp.

**Por quê:** a revisão 4 eixos é produção de hipóteses pelo modelo. Aceitar tudo sem revisão reproduz o problema — o modelo pode propor correções que parecem certas mas são inadequadas ao contexto (ex: propor reframe de termo juridicamente definido que precisa permanecer literal).

### Checkpoint implícito — entre Etapa 6 e publicação real

A validação em campo com o público-alvo real (3-5 pessoas do recorte declarado) é o terceiro checkpoint **obrigatório em espírito**, mas **fora do escopo operacional da skill**. A skill entrega o kit de validação (Etapa 6), não executa a validação. Se o humano não consegue rodar a validação por prazo ou condições, a Etapa 7 registra explicitamente como **risco declarado** — omissão não conta.

**Por quê está fora do escopo:** a validação em campo é trabalho humano de contato, de escuta, de tempo, de deslocamento. Delegar ao modelo seria permitir "personas simuladas" — o anti-pattern que o Princípio 5 proíbe.

## Falhas comuns

Estes são os anti-patterns mais frequentes observados quando a skill é mal usada. Todos são evitáveis com disciplina nos princípios, nos checkpoints e na linha de base.

1. **Gerar peças direto do documento original em vez de da linha de base em linguagem simples.** Jargão jurídico-técnico residual vaza para TODAS as peças derivadas (FAQ, SMS, post, release), contaminando o kit inteiro. **Causa-raiz:** pular a Etapa 3 ou fazê-la pro forma. **Mitigação:** a Etapa 3 é artefato interno obrigatório, mesmo que o usuário não a tenha marcado no checklist. A Etapa 4 deriva **dela**, não do original.

2. **Tratar linguagem simples como infantilização.** "Você quer participar do edital? Então você precisa mandar papéis! Vamos te explicar direitinho!" — falar com adulto como criança. **Causa-raiz:** confundir "simples" com "fácil de bebê". **Mitigação:** a linha de base `plain-language-baseline.md` tem regra explícita anti-infantilização e anti-diminutivo; o prompt da Etapa 3 exige o teste parágrafo por parágrafo contra a pergunta "estou falando com adulto ou tratando como criança?"; a Etapa 5 eixo 3 tem varredura específica.

3. **Deficit framing herdado da fonte sem auditoria na Etapa 2.** A fonte chama o público de "beneficiários carentes", e a skill vira amplificadora silenciosa da linguagem problemática — a formulação aparece no FAQ, no post, no release. **Causa-raiz:** pular a Etapa 2 ou tratá-la como varredura automática. **Mitigação:** CH1 é obrigatório e bloqueia a Etapa 3 até decisão explícita linha a linha. Decisão política, não estética.

4. **Alt text descritivo neutro quando a imagem tem conteúdo político.** Foto de protesto descrita como "pessoas em frente a um prédio". Foto de ação comunitária descrita como "algumas pessoas em um espaço". Neutralidade aqui é escolha política ativa, não ausência de escolha — e escolhe apagar. **Causa-raiz:** tratar alt text como "descrição objetiva" sem reconhecer que descrição é sempre seleção. **Mitigação:** o prompt da Etapa 4 tipo alt_text tem cláusula explícita sobre decisão política; a Etapa 5 eixo 2 audita especificamente "alt text neutraliza conteúdo político que não deveria ser neutralizado?"

5. **Escolher canal sem validar cobertura real do público.** SMS para quem não tem celular ativo. Instagram para idosos rurais que não usam rede social. QR code para quem não tem smartphone com câmera. E-mail institucional para jovens que só usam WhatsApp. **Causa-raiz:** escolher canal por aspiração institucional, não por uso real. **Mitigação:** pré-requisito 3 da Etapa 1 exige declaração de cobertura real; a Etapa 5 eixo 3 checa combinação canal×formato; a Etapa 6 seção "pontos de atenção por tipo de público" tem exemplos específicos.

6. **"Validação com o público" vira "perguntei para colegas da equipe".** Colega de OSC com mestrado não é "pessoa em vulnerabilidade social". Colega da secretaria que mora perto do território não é "representante do público". Isso é teatro de validação. **Causa-raiz:** pressão de prazo + ilusão de proxy. **Mitigação:** o kit da Etapa 6 nomeia explicitamente o recorte real (repete literal o declarado na Etapa 1) e inclui seção "o que NÃO é validação" que precisa estar no documento entregue, não apenas no prompt.

## Arquivos complementares

Esta skill vem com **quatro** arquivos complementares em `references/` — um a mais do que o padrão de 3, porque ela inclui sua própria linha de base operacional (paralelo ao `style-guide.md` do `technical-note-writing`):

- **[`references/exemplos.md`](references/exemplos.md)** — execução completa em um caso realista (edital público municipal de cultura com linguagem jurídica densa transformado em kit de 5 peças: linguagem simples + FAQ + SMS + carrossel + release). Percorre as 7 etapas + 2 checkpoints, mostrando a decisão de reframe na Etapa 2, a linha de base produzida na Etapa 3, as peças derivadas na Etapa 4 com rastreabilidade inline aos DC_IDs, a revisão 4 eixos na Etapa 5 com correções propostas concretas, e o kit de validação da Etapa 6.

- **[`references/variantes.md`](references/variantes.md)** — cinco variantes do workflow base:
  - **V1: Chain de `technical-note-writing`** — nota técnica pronta vira input; dados críticos já vêm indexados upstream, pula parte da Etapa 1.
  - **V2: Conteúdo multi-idioma** — público inclui falantes de PT + outra(s) língua(s); cada idioma passa pela Etapa 3 no próprio idioma, não é tradução literal.
  - **V3: Urgência/crise sem tempo de validar** — emergência sanitária, desastre climático; execução da skill com risco de acessibilidade performativa declarado explicitamente (CH implícito não atendido).
  - **V4: Chain de `theory-of-change`** — ToC serve como insumo; peças comunicam cadeias causais, não eventos pontuais; os tipos de dados críticos mudam (indicadores, marcos, grupos alcançados).
  - **V5: Documento-fonte com framing problemático imutável** — edital assinado por autoridade não pode ser reescrito; reframe apenas nas peças derivadas, com nota explícita sobre a tensão.

- **[`references/checklist.md`](references/checklist.md)** — checklist humana com duas seções: **Técnica** (dados críticos preservados literal, rastreabilidade inline aos DC_IDs, `não encontrado` listados, `[suposição]` listados, consistência entre peças) e **Equidade** (decisão de reframe registrada por ponto, linguagem não-estigmatizante, alt text não neutraliza político, canais validados contra cobertura real, kit de validação nomeia público real, riscos declarados).

- **[`references/plain-language-baseline.md`](references/plain-language-baseline.md)** — **linha de base operacional desta skill**, paralela ao `style-guide.md` do `technical-note-writing`. Carga obrigatória na Etapa 1. Declara a disciplina do **Plain Language movement (federal.gov / ENAP Linguagem Simples) + tom inclusivo do guia de Linguagem Cidadã, sem infantilização nem reducionismo**. Documenta 10 regras operacionais de prosa com exemplos errado/certo em PT-BR institucional — frase direta, voz ativa, um conceito por parágrafo, palavra comum no lugar de erudito, siglas expandidas, dados numéricos ancorados, ordem condição-ação, segunda pessoa ou terceira impessoal, anti-diminutivo/exclamação/emoji-substituto, verbos de ação no lugar de substantivos processuais.

Para o framework geral de equidade, consulte [`docs/equity-lens.md`](../../docs/equity-lens.md).
