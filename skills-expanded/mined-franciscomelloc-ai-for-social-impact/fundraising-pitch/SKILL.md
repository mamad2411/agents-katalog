---
name: fundraising-pitch
description: Transforma programa estruturado (ToC, dados, orçamento, equipe) em kit de captação — concept note, roteiro de deck, proposta, história, orçamento narrado — com framing adaptado ao funder e auditoria anti-deficit framing.
---

# Captação de Recursos — Kit de Peças

## Quando usar esta skill

Esta skill transforma **um programa estruturado** (teoria da mudança, dados de impacto, orçamento, equipe) em **kit de peças de captação** — concept note, roteiro de pitch deck, narrativa de proposta, história de impacto, narrativa de orçamento — com framing adaptado ao funder específico e auditoria anti-deficit framing em três momentos estruturais.

A skill é **tradutora pura**: empacota o que já existe, não constrói projeto do zero. Se você não tem um programa estruturado, primeiro use `theory-of-change`, `project-structuring` ou `evidence-synthesis` — ou aceite o diálogo ToC-lite de 5–7 perguntas que esta skill faz na Etapa 3.

Use quando o usuário:

- Precisa escrever uma concept note para um funder específico (foundation internacional, edital público, filantropia corporativa, doador individual)
- Vai submeter proposta a edital público brasileiro (BNDES, CGU, fundos estaduais, BID, Banco Mundial) e precisa da narrativa completa
- Vai pitchar pro conselho de uma foundation e precisa do roteiro do deck (não do design)
- Tem projeto pronto em PT e precisa traduzir pra EN para funder internacional
- Recebeu pedido explícito do funder: "nos mande uma narrativa de orçamento justificando cada rubrica"
- Precisa de história de impacto com protagonista real pra campanha de doação individual
- Já rodou `theory-of-change` e quer transformar a cadeia causal em peça de captação

Sinais típicos na conversa do usuário:

- "Preciso escrever uma concept note pro Ford / Mott / Open Society / BMGF"
- "Tem um edital do BNDES / CGU / ITAÚ / BID abrindo, preciso submeter proposta"
- "Vou pitchar pro conselho de uma foundation, preciso do deck"
- "A campanha de doação individual precisa de história pra rede social — com dados"
- "O funder pediu narrativa de orçamento justificando cada rubrica"
- "Já tenho minha ToC pronta, preciso transformar em proposta de captação"
- "Preciso escrever em inglês uma proposta pra funder internacional"

Relação com outras skills do repositório (upstream):

- **`theory-of-change` → fundraising-pitch** — ToC formal absorvida como insumo; a skill pula o diálogo ToC-lite e usa a cadeia causal diretamente (variante V5)
- **`project-structuring` → fundraising-pitch** — orçamento + cronograma + equipe absorvidos; a skill preenche os campos que faltam no briefing via diálogo curto (variante V6)
- **`evidence-synthesis` → fundraising-pitch** — matriz sintetizada vira `<indice_dados>` diretamente; a skill aproveita a rastreabilidade já construída upstream (variante V7)
- **`strategic-planning` → fundraising-pitch** — KPIs/OPIs entram como métricas de M&E na base canônica
- **Documento próprio da OSC** — relatório de atividades, proposta antiga, plano estratégico interno, site institucional (variante V8)
- **Diálogo ToC-lite (5–7 perguntas)** — quando OSC não tem nada formal; a skill constrói a versão mínima necessária SEM reimplementar `theory-of-change`

Downstream: nenhum. Esta skill é **ponto de saída** da cadeia interna → funder. O que vem depois é design gráfico do deck, submissão ao funder, relacionamento, e — para peças em EN — revisão humana por falante nativo antes de submeter. Fora do escopo desta skill.

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Programa estruturado** — via output de skill upstream (`theory-of-change`, `project-structuring`, `evidence-synthesis`, `strategic-planning`), documento próprio da OSC (relatório, proposta antiga, plano), OU disposição para responder ao diálogo ToC-lite de 5–7 perguntas na Etapa 3. A skill **não constrói ToC do zero** — constrói a versão mínima necessária pra escrever a peça. Se o usuário não tem programa algum, a skill o redireciona para `theory-of-change` primeiro.

2. **Pelo menos um dado concreto rastreável** — número com fonte, resultado com método de medição, ou testemunho com autor e data. "Atendemos muita gente" não é dado. "Atendemos 412 pessoas em 2024 — fonte: SIA-SUS consolidado anual" é dado. Sem fato concreto, captação vira adjetivo inflado, e a skill recusa.

3. **Ask mensurável com rubricas grossas** — o valor solicitado, o prazo, o uso dos recursos em pelo menos 3 rubricas (pessoal, operação, M&E). "US$ 180.000 em 18 meses para expandir o programa X de 240 para 640 jovens atendidos — 60% pessoal, 25% operação, 15% M&E" é válido. "Precisamos de apoio para fortalecer a rede" não é. Sem ask mensurável, peça vira declaração de intenções.

4. **Tipo ou identidade do funder** — um dos 4 tipos default (foundation internacional, edital público brasileiro, filantropia corporativa, doador individual) OU, melhor, dossiê do funder específico (nome, prioridades declaradas, peças já financiadas, critérios publicados, restrições). Se só tipo, a skill cai nos defaults por tipo e marca `[suposição]` em toda adaptação de framing.

5. **Idioma-alvo da saída** — PT ou EN. Um idioma por execução. Se a OSC precisa dos dois, roda duas vezes — a base canônica do primeiro run vira insumo do segundo.

6. **Disposição pra auditar o funder (CH0) e reframar deficit framing (CH1)** — se o usuário quer só "escrever bonitinho sem questionar nada", a skill avisa que não é essa skill. A auditoria do funder na Etapa 2 **pode recomendar não aplicar**; o reframe de deficit framing na Etapa 4 **é decisão política** que o usuário precisa assumir. Quem só quer cópia obediente de concept note antiga, procure outra ferramenta.

Se algum desses elementos não está pronto, a skill **pergunta antes de avançar** — não inventa silenciosamente.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Dados concretos são literais.** Números, prazos, valores do ask, nomes de programas, unidades de escala — nunca parafrasear, arredondar, "melhorar a fluência". Se faltar, escrever `não encontrado` literal. "US$ 180.000 em 18 meses" nunca vira "cerca de 180 mil". "412 mulheres atendidas em 2024" nunca vira "centenas de mulheres". Captação com número errado é **dano reputacional** (o funder checa) e **dano ético** (promessa falsa). Este é o princípio mais protegido da skill: a revisão na Etapa 7 tem um eixo factual dedicado.

2. **Nome antes de adjetivo, causa estrutural nomeada, protagonismo da comunidade.** Deficit framing e poverty porn são **proibidos**. O baseline (`references/fundraising-style-baseline.md`) define operacionalmente o que isso significa: nome do grupo antes de "vulnerável" ou "carente"; causa estrutural (política, econômica, histórica) nomeada junto com o indicador; comunidade como sujeito gramatical de verbos de ação, não objeto de intervenção. Passivização dos atendidos ("beneficiários receberão treinamento") é sinal vermelho da revisão. Este princípio é a razão da skill existir — relaxá-lo é reproduzir exatamente o anti-pattern que a skill combate.

3. **Ask mensurável não é opcional.** Toda peça gerada contém "quanto, em quanto tempo, pra quê, com que custo marginal por unidade-alvo". "Precisamos de apoio pra expandir" é **inválido** como ask. "US$ 180.000 em 18 meses expandem de 240 para 640 jovens atendidos — custo marginal US$ 280 por jovem, 3 unidades novas" é **válido**. Sem ask mensurável, a skill recusa de saída na Etapa 1. É o contrato que distingue captação profissional de declaração de intenções.

4. **Lente de equidade é upstream (funder + briefing) + downstream (peça) — 3 etapas estruturais, não checklist final.** Auditoria do funder (Etapa 2 + CH0 — "vale aplicar?"), auditoria do briefing (Etapa 4 + CH1 — "como nomeamos?"), auditoria das peças (Etapa 7 eixo 4 + CH2 — "aceitamos as correções?"). Equidade no final é disclaimer — equidade distribuída em três etapas estruturais é infraestrutura. Ver `docs/equity-lens.md` para o framework compartilhado do repositório.

5. **Adaptação ao funder é disciplinada, não submissa.** A skill ajusta **framing** (tom, linguagem, ordem dos argumentos, ênfase), mas **nunca distorce** o projeto pra caber num funder. Se o funder prioriza educação infantil e a OSC trabalha com adolescentes, a skill **não** reescreve o projeto como se fosse educação infantil — o humano decide em CH0 se desiste da aplicação ou assume a distorção explicitamente. "Torcer o projeto pra parecer o que o funder quer" é exatamente o anti-pattern que mata OSCs pequenas (Falha Comum nº 3).

6. **Anti-hallucination: `não encontrado` + `[suposição]` explícitos.** Quando um dado não existe no input, escrever `não encontrado` literal. Quando a skill propõe adaptação sem base (ex: framing sem dossiê do funder, tom sem diretriz de marca), marcar `[suposição]` + justificativa curta. Especialmente crítico em adaptação ao funder — inventar "o Ford prioriza X" sem fonte é alucinação. Sem essas marcas, a suposição vira "fato" na cabeça de quem lê e aparece na peça como se fosse afirmação sustentada.

**Estas não são regras opcionais.** A skill existe porque captação institucional tradicional normalizou deficit framing, adjetivos inflados e projetos torcidos em troca de dinheiro. Relaxar os princípios é reproduzir exatamente o que a skill se propõe a combater.

## O workflow (8 etapas)

O trabalho é organizado em 8 etapas sequenciais com 3 checkpoints humanos. **Etapa 1** configura o trabalho, declara idioma e funder, carrega o baseline e marca peças a produzir. **Etapa 2** audita o funder (equity upstream #1) — primeiro checkpoint humano, decisão política de aplicar ou não. **Etapa 3** monta o briefing estruturado (absorvendo upstream, extraindo de documento próprio, ou via diálogo ToC-lite) e indexa dados rastreáveis. **Etapa 4** audita o briefing por deficit framing herdado (equity upstream #2) — segundo checkpoint humano, decisão política de reframe. **Etapa 5** escreve a base canônica única da qual todas as peças derivam. **Etapa 6** deriva as peças selecionadas. **Etapa 7** faz revisão 4 eixos (equity downstream) — terceiro checkpoint humano, aceitação técnica item a item. **Etapa 8** é autoverificação final contra os princípios.

Cada etapa tem **objetivo** específico, **prompt sugerido** pronto para copiar (com tags XML `<principios>`, `<config>`, `<auditoria_funder>`, `<briefing>`, `<indice_dados>`, `<auditoria_briefing>`, `<base_canonica>`, `<peca_concept_note>` (e variantes por peça), `<revisao>`, `<autoverificacao>` — prática recomendada pela Anthropic), e **output esperado** que alimenta a etapa seguinte. **Não pule etapas**, especialmente E2, E4 e E7 — as duas primeiras contêm decisões políticas obrigatórias, a terceira é o instrumento que impede captação performática.

### Etapa 1 — Configuração, seleção de peças e carga do baseline

**Objetivo:** declarar idioma-alvo (PT ou EN), tipo do funder (ou dossiê específico se existe), peças a produzir, e **carregar `references/fundraising-style-baseline.md`** como contexto ativo para toda a execução. Também verificar pré-requisitos duros (programa estruturado disponível, pelo menos um dado concreto, ask mensurável com rubricas grossas). Se qualquer pré-requisito falhar, a skill recusa avançar e pede o que falta.

**Prompt sugerido:**

````
Você vai me ajudar a construir um kit de captação a partir de um programa estruturado, seguindo a skill fundraising-pitch. Antes de começar, confirme que entendeu as regras.

<principios>
1. Dados concretos são literais — nunca parafrasear número, prazo, valor, nome. "Não encontrado" quando faltar.
2. Nome antes de adjetivo, causa estrutural nomeada, protagonismo da comunidade. Deficit framing e poverty porn proibidos.
3. Ask mensurável obrigatório — valor, prazo, uso, custo marginal. Sem isso, recusar.
4. Equity lens é upstream (funder + briefing) + downstream (peça) — 3 etapas, não checklist final.
5. Adaptação ao funder é disciplinada, não submissa. Nunca torcer o projeto pra caber num funder.
6. Toda adaptação sem base marcada [suposição] + justificativa.
</principios>

<config>
- Idioma-alvo da saída: [PT | EN] — um só por execução
- Tipo do funder: [foundation_internacional | edital_publico | filantropia_corporativa | doador_individual]
- Dossiê do funder específico (opcional, mas preferível):
  - Nome: [ex: Ford Foundation, Edital FAPESP 2026/01, Instituto Itaú Social]
  - Prioridades declaradas: [cole do site/edital literal]
  - Peças que já financiou em temas próximos: [liste com fontes]
  - Critérios publicados: [cole literal]
  - Restrições: [overhead máximo, uso restrito, contrapartida]
- Se não houver dossiê: skill usa defaults por tipo + marca TODAS as adaptações de framing como [suposição].

<pecas_selecionadas>
O usuário marca quais peças produzir. A skill produz APENAS as marcadas. A base canônica (Etapa 5) é produzida sempre como insumo interno, mesmo que não esteja marcada — é o documento mestre do qual tudo deriva.

[ ] concept note (2–4 páginas, foundation-standard)
[ ] roteiro de pitch deck (8–12 slides, texto + notas do apresentador — NÃO gera design)
[ ] narrativa de proposta (seções longas para edital ou foundation formal)
[ ] história de impacto (1–2 páginas, protagonista real identificado)
[ ] narrativa de orçamento (texto que justifica rubricas grossas — não é a planilha)
</pecas_selecionadas>

<pre_requisitos_duros>
Confirme que estes 3 estão disponíveis. Se qualquer um falhar, PARE e peça o que falta.

1. Programa estruturado: output de skill upstream OU documento próprio OU disposição para diálogo ToC-lite de 5–7 perguntas na Etapa 3.
2. Pelo menos UM dado concreto rastreável: número com fonte, resultado com método, testemunho com autor/data.
3. Ask mensurável: valor + prazo + uso em pelo menos 3 rubricas grossas (pessoal, operação, M&E).
</pre_requisitos_duros>
</config>

<linha_base>
Carregue references/fundraising-style-baseline.md como contexto ativo. Aplique a disciplina de prosa do fundraising profissional (Candid / Chronicle of Philanthropy) + framing de protagonismo do Community-Centric Fundraising, sem deficit framing. As 10 regras operacionais orientam TODA a geração a partir da Etapa 5.
</linha_base>

Ao terminar, responda literalmente:
"OK — regras aceitas. Idioma [PT|EN], funder [tipo] [com|sem] dossiê específico, [N] peças marcadas. Pré-requisitos duros: [OK | FALTA X]. Linha de base carregada. Pronto para Etapa 2 (auditoria do funder)."
````

**Output esperado:** handshake explícito + config bloco completo + pré-requisitos confirmados + confirmação de carga da linha de base. Se a skill pular direto para a Etapa 2 sem o handshake, o usuário volta e exige — é função do prompt forçar o aceite.

### Etapa 2 — Auditoria do funder (equity upstream #1)

**Objetivo:** auditar se os termos publicados ou o histórico do funder excluem estruturalmente OSCs pequenas, periféricas ou de base comunitária. Esta é a **única etapa do repo inteiro** que audita o polo com mais poder numa relação assimétrica — e ela existe porque captação **é** uma relação assimétrica. O output é um veredicto VERDE / AMARELO / VERMELHO, com recomendação acionável. O CH0 que fecha a etapa é decisão política de ir/não ir — a skill pode recomendar não aplicar, e o humano decide.

**Prompt sugerido:**

````
Agora audite o funder antes de começar qualquer escrita. O objetivo é identificar se os termos do funder excluem OSCs pequenas, periféricas ou de base comunitária — não "como agradar ao funder", mas "vale aplicar?".

<auditoria_funder>
Analise o funder em 8 critérios objetivos. Para cada um, marque VERDE / AMARELO / VERMELHO e justifique em 1 frase com citação literal do dossiê ou [suposição] se não houver base.

1. ELEGIBILIDADE FORMAL — Exige CNPJ com N anos mínimos? Exige auditoria formal externa? Exige certificações específicas (OSCIP, utilidade pública, etc.)? Se a OSC não tem, é VERMELHO.

2. MATCHING FUND / CONTRAPARTIDA — Exige contrapartida financeira da OSC? Em que percentual? OSCs pequenas raramente têm caixa pra matching fund — se exigido e alto, é VERMELHO ou AMARELO.

3. IDIOMA E REPORTES — Exige staff com inglês nativo? Exige reportes trimestrais formais em inglês? Exige narrative reports em padrão foundation anglo? Se a OSC não tem capacidade instalada, é AMARELO (aplicável com suporte) ou VERMELHO.

4. TRACK RECORD — Exige histórico de grants internacionais anteriores? Exige prestação de contas auditada de grants anteriores? Se OSC está aplicando pela primeira vez a funder internacional, é AMARELO.

5. TEMA E TERRITÓRIO — O tema e território do funder são compatíveis com o da OSC? Se não, é VERMELHO (não torcer o projeto). Se parcialmente, AMARELO.

6. VALOR MÍNIMO — O valor mínimo do ask do funder é viável para o tamanho da OSC? Grant de US$ 2M para OSC com orçamento anual de US$ 150k é estruturalmente inviável — a OSC não tem capacidade de absorver. VERMELHO.

7. RESTRIÇÕES DE USO — Overhead máximo permitido (muitos funders limitam a 10–15%). Uso restrito (só atividade direta, não pessoal fixo, não estrutura). Se as restrições inviabilizam a execução realista, é AMARELO ou VERMELHO.

8. HISTÓRICO DE QUEM JÁ FINANCIOU — Quem o funder já financiou em temas próximos? Se só financiou OSCs grandes de capitais, é AMARELO (sinal de exclusão estrutural de OSCs periféricas). Se financiou diversidade geográfica e de tamanho, é VERDE.

Saída:
Tabela com 8 linhas (uma por critério):
Critério | Verdict (VERDE|AMARELO|VERMELHO) | Justificativa (1 frase + citação literal ou [suposição]) | Acionável
</auditoria_funder>

<veredicto_final>
Agregue os 8 critérios em um veredicto final:
- VERDE: 0 VERMELHO e ≤2 AMARELO. Funder estruturalmente acessível. Recomendação: aplicar.
- AMARELO: 0 VERMELHO e 3+ AMARELO, OU 1 VERMELHO reversível. Funder aplicável com ressalvas. Recomendação: aplicar com nota explícita de riscos estruturais, o humano decide.
- VERMELHO: 2+ VERMELHO, OU 1 VERMELHO estrutural (ex: valor mínimo inviável). Funder estruturalmente inacessível. Recomendação: não aplicar. Humano decide se quer forçar mesmo assim — SEM torcer o projeto.
</veredicto_final>

Ao terminar, pare e aguarde decisão humana explícita (CH0). NÃO avance para Etapa 3 antes do humano registrar "CH0: vou aplicar" ou "CH0: vou desistir".
````

**Output esperado:** tabela de 8 critérios com veredict por linha + veredicto final agregado + recomendação acionável. Mínimo de 8 linhas auditadas — auditoria parcial invalida o output.

---

### CHECKPOINT HUMANO CH0 — pós-E2 (bloqueia E3)

**Pergunta obrigatória ao humano:**

> Revise a auditoria do funder. Você tem três caminhos:
>
> - **Aplicar** — os termos do funder são acessíveis à OSC (veredicto VERDE ou AMARELO aceito). Registre por escrito "CH0: vou aplicar".
> - **Desistir** — os termos do funder excluem estruturalmente a OSC (veredicto VERMELHO) e não vale a pena distorcer o projeto. Registre "CH0: vou desistir". A skill para aqui.
> - **Aplicar apesar do vermelho** — você quer forçar a aplicação mesmo sabendo que o funder estruturalmente não cabe. Registre "CH0: vou aplicar com risco estrutural — [sua razão]". A skill segue, mas **sem torcer o projeto** (Princípio 5). Se o projeto não cabe, a peça vai dizer isso honestamente.
>
> A skill não avança para a Etapa 3 sem esse registro. Decisão implícita não conta.

Esta é a decisão mais consequente da skill inteira. É o ponto onde a OSC pode decidir **não aplicar** a um funder que a estruturalmente exclui — e ganhar de volta o tempo que gastaria numa aplicação destinada a falhar. É também o ponto onde o modelo **não pode decidir sozinho**: captação é decisão política, não técnica.

### Etapa 3 — Construção do briefing estruturado

**Objetivo:** montar ou absorver o briefing mínimo que a peça precisa — 7 campos fixos (problema, ToC curta, solução, evidência, equipe, ask, M&E) — e indexar os dados rastreáveis em tabela com IDs tipados. A skill tem **três caminhos condicionais** baseados no tipo de input:

- **(a) Chain-in de skill upstream** — absorve output de `theory-of-change`, `project-structuring`, `evidence-synthesis`, `strategic-planning`. Mapeamento campo-a-campo, depois preenche o que falta via diálogo curto.
- **(b) Documento próprio da OSC** — relatório de atividades, proposta antiga, plano estratégico interno, site institucional. A skill extrai os campos que consegue e diálogo preenche o resto.
- **(c) Diálogo ToC-lite (5–7 perguntas)** — quando OSC não tem nada formal. A skill **não reimplementa `theory-of-change`** — constrói só a versão mínima necessária pra escrever a peça.

**Prompt sugerido:**

````
Vamos montar o briefing estruturado. A estrutura é fixa em 7 campos. Identifique primeiro qual caminho de input se aplica (a, b ou c) e siga o sub-fluxo correspondente.

<briefing>
Estrutura obrigatória (7 campos):

1. PROBLEMA — qual problema, pra quem, onde, com que magnitude. Dado concreto obrigatório.
2. TEORIA DA MUDANÇA CURTA — cadeia causal em 3–5 nós: insumos → atividades → resultados → impactos. Não é ToC completa, é a versão mínima pra justificar o desenho.
3. SOLUÇÃO — o que a OSC faz na prática, concretamente, no dia a dia. Verbos de ação específicos, não "fortalecimento" ou "empoderamento".
4. EVIDÊNCIA DE IMPACTO — dado concreto rastreável de que o desenho funciona (resultado medido, testemunho com autor/data, avaliação externa se houver).
5. EQUIPE — quem faz, quanto tempo, qualificação relevante, anos de operação da OSC.
6. ASK — valor + prazo + uso em ≥3 rubricas grossas + custo marginal por unidade-alvo.
7. M&E — como a OSC sabe que está funcionando. Indicadores específicos, fontes de dado, periodicidade.
</briefing>

<caminho_a_chain_upstream>
Se o input é output de skill upstream:
- theory-of-change → mapeie ToC para os campos 1, 2, 3, 7. Pergunte os que faltam (evidência, equipe, ask).
- project-structuring → mapeie para campos 3, 5, 6. Pergunte o que falta (problema, ToC curta, evidência, M&E).
- evidence-synthesis → a matriz vira o campo 4 (evidência) diretamente, e o <indice_dados> herda IDs da matriz. Pergunte o resto.
- strategic-planning → KPIs/OPIs viram o campo 7 (M&E). Pergunte o resto.
Confirme campo a campo com o usuário antes de avançar.
</caminho_a_chain_upstream>

<caminho_b_documento_proprio>
Se o input é documento próprio da OSC:
Extraia do texto o que conseguir preencher nos 7 campos. Marque com [extraído de: nome do documento, trecho literal] cada campo preenchido. Para cada campo que não conseguir preencher, pergunte ao usuário diretamente.
</caminho_b_documento_proprio>

<caminho_c_toc_lite>
Se o input é diálogo ToC-lite, faça estas 5–7 perguntas, uma por vez. Não passe pra próxima sem resposta.

1. Qual é o problema que sua OSC ataca? Para quem é esse problema (quem é a comunidade)? Onde (município, território, escala)? Tenha coragem de ser específico — "jovens em situação de vulnerabilidade" não serve, "240 jovens de 16 a 24 anos da comunidade do Barreiro buscando primeiro emprego formal" serve.

2. O que a sua OSC faz concretamente para atacar esse problema? Me dê a descrição no nível da ação, não da retórica. "Fortalece competências" não serve, "oferece 5 oficinas semanais de 3h em panificação, costura e instalação elétrica, em parceria com 2 escolas técnicas" serve.

3. Qual é o resultado concreto que você já mediu — um número, com fonte e método. Se você não tem, diga "não encontrado" e a skill vai sinalizar na peça como lacuna. Captação sem dado é adjetivo inflado.

4. Por que este desenho funciona? (cadeia causal curta, 3–5 nós) — qual é a lógica que liga insumos → atividades → resultados → impactos?

5. Quem é a equipe? Quantas pessoas, há quanto tempo, com que qualificação relevante? Há quanto tempo a OSC existe?

6. Qual é o ask? Valor + prazo + uso em ≥3 rubricas grossas. Se o usuário não sabe dizer, pare e peça — sem ask mensurável, a skill recusa por Princípio 3.

7. (Opcional) Tem um testemunho ou história concreta com autor identificado? Nome + data + contexto + autorização para uso público. Se sim, pode virar base para a história de impacto. Se não, a história de impacto não poderá ser gerada — a skill avisa.
</caminho_c_toc_lite>

<indice_dados>
Indexe todo dado concreto mencionado em uma tabela com IDs tipados:
DAT_ID | Tipo | Valor literal | Fonte | Data | Onde aparece no briefing

Tipos obrigatórios a varrer:
- numero_resultado (métricas de impacto, atendimentos, resultados medidos)
- valor_financeiro (orçamento, ask, custo marginal, matching)
- prazo (datas, janelas, cronogramas)
- testemunho (citação direta com autor)
- referencia_externa (avaliação, pesquisa, dado oficial citado)
- nome_proprio (nome de programa, comunidade, parceiro, autoridade)

Regra: valor literal exatamente como está no briefing. Não normalize formato de data. Não arredonde valores. Se um dado parece estar no briefing mas você não consegue citar trecho literal, marque "não encontrado" e peça ao usuário.
</indice_dados>

Ao terminar, responda literalmente:
"Briefing montado com [N] campos preenchidos de 7. [M] dados indexados. Caminho usado: [a|b|c]. Pronto para Etapa 4 (auditoria do briefing)."
````

**Output esperado:** briefing estruturado com 7 campos (ou marcações explícitas de "não encontrado" para campos vazios) + índice de dados tipados. Mínimo de 3 dados rastreáveis indexados — menos que isso não sustenta peça de captação.

### Etapa 4 — Auditoria upstream do briefing (equity #2)

**Objetivo:** auditar o **próprio briefing** contra as 10 regras do baseline, **antes** de escrever qualquer peça. Se o briefing já traz "jovens vulneráveis sem perspectiva" (porque foi assim que a OSC aprendeu a falar de si mesma), esse framing vai vazar para a concept note, o deck, a proposta, a história — corrigir em 5 lugares depois é trabalho em 5 lugares; decidir aqui é trabalho em 1 lugar, uma vez. Para cada violação, a skill propõe **reframe concreto** com duas opções (mais conservadora / mais assertiva) e registra a decisão do humano em tabela.

**Prompt sugerido:**

````
Agora audite o próprio briefing contra as 10 regras do fundraising-style-baseline.md, ANTES de qualquer geração. Foco: deficit framing herdado, adjetivos sem número, passivização da comunidade, falta de causa estrutural.

<auditoria_briefing>
Analise o briefing em 4 dimensões:

1. NOMEAÇÃO DA COMUNIDADE
Como o briefing chama quem a OSC atende? Liste os termos textuais entre aspas.
Há deficit framing? ("jovens vulneráveis sem perspectiva", "mulheres em situação de risco", "crianças carentes", "famílias necessitadas", "beneficiários", "assistidos", "público em situação de vulnerabilidade" sem qualificador específico)

Regra 1 do baseline: Nome do grupo antes do adjetivo demográfico.
- Errado: "Jovens negros vulneráveis em situação de risco social."
- Certo: "Os 240 jovens da comunidade do Barreiro — 18 a 24 anos, em busca do primeiro emprego formal — participam do programa X desde 2023."

2. ADJETIVOS INFLADOS SEM NÚMERO
Há palavras como "significativo", "massivo", "transformador", "inovador", "robusto", "consistente" sem número que sustente?

Regra 2/7 do baseline: Adjetivo custa número. Se a prosa usa adjetivo inflado, a revisão pede o número. Sem número, corta o adjetivo.

3. CAUSA ESTRUTURAL
O problema aparece como "característica do grupo" (evasão alta, desemprego alto, baixa escolaridade) ou como consequência de causa estrutural nomeada (acesso desigual, distância até escola, histórico de exclusão, política pública ausente)?

Regra 3 do baseline: Causa estrutural nomeada junto com o indicador.
- Errado: "A evasão escolar na região é alta."
- Certo: "A evasão no ensino médio na região é 34% — 12 pontos acima da média estadual —, concentrada em escolas com 3+ horas de deslocamento."

4. PASSIVIZAÇÃO DA COMUNIDADE
A comunidade aparece como sujeito gramatical de verbos de ação (conduz, decide, avalia, forma) ou como objeto de intervenção (receberá, será beneficiado, será capacitado)?

Regra 5/10 do baseline: Protagonismo da comunidade é sujeito da frase. Sem "beneficiários" como sujeito passivo.

Para CADA violação identificada, proponha DUAS opções de reframe:
- CONSERVADOR — reformulação mínima, mantém estrutura do briefing, troca só os termos mais problemáticos.
- ASSERTIVO — reformulação estrutural, nomeia causas, coloca comunidade como protagonista, puxa dado do <indice_dados>.

Marque qual recomenda em cada linha.

Produza tabela de notas de framing:
Dimensão | Termo/frase original (literal) | Opção conservadora | Opção assertiva | Recomendação | Decisão humana (a preencher em CH1)
</auditoria_briefing>

Ao terminar, pare e aguarde decisão humana por linha (CH1). Decisão implícita não conta.
````

**Output esperado:** tabela de notas de framing com uma linha por violação identificada. Mínimo de 2 linhas — se a auditoria encontra zero violações, a skill reitera a análise pois é implausível que um briefing real não tenha nenhum framing a ajustar (a menos que o briefing tenha vindo de chain-in de `theory-of-change` já auditada, caso em que a etapa é curta).

---

### CHECKPOINT HUMANO CH1 — pós-E4 (bloqueia E5)

**Pergunta obrigatória ao humano:**

> Revise a tabela de notas de framing. Para cada violação, escolha uma decisão:
>
> - **Reframe conservador** — aplica a reformulação mínima. Mais seguro, menos transformador.
> - **Reframe assertivo** — aplica a reformulação estrutural, nomeia causas, coloca comunidade como protagonista. Mais alinhado com o baseline, mais arriscado se o funder é conservador.
> - **Manter original** — preserva o termo literal, com justificativa explícita (ex: "é a linguagem exata do edital, não reescrevível", "é termo juridicamente definido", "é citação direta de dado oficial"). Só permitido com justificativa.
>
> Registre por escrito sua decisão linha a linha. A skill não avança para a Etapa 5 sem esse registro. **Decisão implícita = decisão do modelo = violação do Princípio 4** (equity upstream).

Esta é a segunda decisão política da skill. O reframe aqui trava o que vai virar linguagem padrão em 5 peças derivadas. Errar aqui contamina o kit inteiro. É também o ponto onde a OSC escolhe **como vai falar de si mesma** — uma escolha que extrapola o uso nesta aplicação específica.

### Etapa 5 — Base canônica

**Objetivo:** escrever **uma única base canônica** (~800–1500 palavras) que contém todos os elementos que qualquer peça do kit vai precisar, na ordem do baseline (regra 6): **problema → evidência → ToC curta → solução → equipe → ask → M&E → equidade**. Esta base é o "documento mestre" do qual todas as peças derivam. Todo dado numérico ancorado inline ao ID do `<indice_dados>` (ex: `412 mulheres [DAT03]`). Todo framing respeitando as decisões de CH1.

A base canônica **não é entregue diretamente ao funder** — é um artefato interno de consistência. Mas ela é longa e estruturada o suficiente para, com adaptações de formato, virar qualquer uma das 5 peças selecionáveis.

**Prompt sugerido:**

````
Agora escreva a base canônica do kit — documento interno único de ~800–1500 palavras, do qual todas as peças vão derivar. Use a estrutura fixa de 8 seções e aplique literal as decisões de CH1.

<base_canonica>
Estrutura obrigatória (8 seções na ordem):

1. PROBLEMA (1–2 parágrafos)
Abre com o dado concreto do problema, não com adjetivo. Nomeia a comunidade (nome/localização/tamanho específico) antes de qualquer adjetivo demográfico. Nomeia causa estrutural junto com o indicador — não "a evasão é alta" mas "a evasão é X%, concentrada em Y por causa de Z".

2. EVIDÊNCIA DE QUE ESTE DESENHO FUNCIONA (1–2 parágrafos)
Apresenta o dado concreto de resultado, com fonte e método. Se há testemunho, inclui com autor identificado (nome, data, contexto). Evidência aparece ANTES da descrição da solução — funder precisa saber que funciona antes de entender como.

3. TEORIA DA MUDANÇA CURTA (1 parágrafo)
Cadeia causal em 3–5 nós: insumos → atividades → resultados → impactos. Usa linguagem da TdC mas em forma narrativa, não bullet. "Quando a OSC X oferece Y em condição Z, a comunidade W passa a K, e isso leva a M em 18 meses."

4. SOLUÇÃO NO NÍVEL DA AÇÃO (1–2 parágrafos)
Descreve o que a OSC faz na prática, no nível da ação concreta. Verbos específicos, frequência, parcerias operacionais. NÃO "fortalecimento de competências"; SIM "5 oficinas semanais de 3h em panificação, costura e instalação elétrica em parceria com escolas técnicas locais".

5. EQUIPE E TRACK RECORD (1 parágrafo)
Quem faz, há quanto tempo, qualificação relevante, anos de operação da OSC, grants anteriores se relevantes. Nomeia parceiros institucionais se existem.

6. ASK (1 parágrafo)
Valor + prazo + uso em ≥3 rubricas grossas + custo marginal por unidade-alvo + escala resultante. "US$ 180.000 em 18 meses [DAT07] expandem de 240 para 640 jovens atendidos [DAT05] — custo marginal US$ 280 por jovem, 3 unidades novas, 60% pessoal, 25% operação, 15% M&E."

7. M&E (1 parágrafo)
Como a OSC sabe que está funcionando. Indicadores específicos (não "métricas a serem definidas"), fontes de dado, periodicidade de coleta, quem avalia.

8. EQUIDADE OPERACIONAL (1 parágrafo)
Como o desenho nomeia e atua sobre assimetrias de poder. Quem decide sobre o que, como a comunidade participa do desenho e da avaliação, como o programa protege contra dano não intencional (ex: estigmatização, dependência, captura). Evita "empoderamento" se não houver mecanismo concreto.
</base_canonica>

<ancoragem_dados>
Cada dado numérico aparece inline ancorado ao DAT_ID correspondente. Exemplo: "412 mulheres atendidas em 2024 [DAT03]". Se um dado está no briefing mas não no <indice_dados>, volte para Etapa 3 e indexe. Não invente dado que não está no índice.
</ancoragem_dados>

<framing_ch1>
Aplique literalmente as decisões do CH1. Se CH1 decidiu "assertivo" para um termo, use a formulação assertiva. Se CH1 decidiu "manter original", use o termo literal. A base canônica é o primeiro teste do reframe — se o reframe não funciona aqui, volta pra E4 e ajusta.
</framing_ch1>

Ao terminar, responda literalmente:
"Base canônica produzida. [N] palavras, 8 seções, [M] dados ancorados inline. Pronto para Etapa 6 (derivação das peças)."
````

**Output esperado:** base canônica ~800–1500 palavras com 8 seções fixas, todos os dados ancorados inline aos DAT_IDs. Se a base excede 2000 palavras, provavelmente está escrevendo a concept note em vez da base — a skill reitera a instrução.

### Etapa 6 — Derivação das peças selecionadas

**Objetivo:** gerar **cada peça marcada na Etapa 1** a partir da base canônica. **Nenhuma peça inventa dado que não está na base canônica.** Se uma peça precisa de dado que a base não tem, a skill marca `não encontrado` e flag para o humano. Cada peça tem regras de formato próprias — a skill não escreve "concept note longa" nem "pitch deck curto"; aplica o formato específico.

**Prompt sugerido:**

````
Gere cada peça marcada na Etapa 1, usando a base canônica como fonte única. Nenhuma peça pode conter dado que não esteja na base canônica ou no <indice_dados>.

<peca_concept_note>
Se marcada: concept note 2–4 páginas, estrutura foundation-standard:

- Summary / resumo (1 parágrafo, ≤150 palavras) — problema + solução + ask + por que vale + equipe — versão mais comprimida da base canônica, sem adjetivo inflado.
- Problem / problema (1 parágrafo) — dado concreto do problema + causa estrutural nomeada.
- Approach / abordagem (1–2 parágrafos) — solução no nível da ação + ToC curta + como se diferencia.
- Evidence / evidência (1 parágrafo) — dado de resultado + testemunho com autor + avaliação externa se houver.
- Outcomes expected / resultados esperados (1 parágrafo) — o que vai mudar, em quanto tempo, medido como.
- Budget summary / resumo orçamentário (1 parágrafo) — ask + rubricas grossas + custo marginal por unidade-alvo.
- Organization / organização (1 parágrafo) — equipe + anos + track record + parceiros.
- Ask / pedido (1 parágrafo final explícito) — valor + prazo + uso + o que a OSC quer do funder além do dinheiro (networking, validação, introduções).

Regras:
- Passa nas 10 regras do baseline — verifica nome antes de adjetivo, número em vez de adjetivo, causa estrutural nomeada, protagonismo da comunidade.
- Todo dado ancorado inline ao DAT_ID.
- Respeita decisões de CH1 linha a linha.
- Se o funder tem dossiê, aplica framing do dossiê. Se não tem, usa default do tipo + marca [suposição] quando há adaptação sem base.
</peca_concept_note>

<peca_roteiro_deck>
Se marcada: roteiro de pitch deck 8–12 slides, formato lista numerada:

Slide 1: Capa — Nome do programa + 1 frase de posicionamento (≤15 palavras). Nota do apresentador: contexto de abertura, quem está na sala.

Slide 2: Problema — dado concreto do problema + causa estrutural. Nota: como contar sem dramatizar.

Slide 3: Comunidade — nome do grupo, tamanho específico, localização. NÃO foto de rosto sem consentimento.

Slide 4: Solução — o que a OSC faz, no nível da ação. Não retórica.

Slide 5: Evidência — dado de resultado com fonte. Gráfico simples se possível.

Slide 6: Teoria da mudança — cadeia causal visual em 3–5 nós.

Slide 7: Equipe — quem, há quanto tempo, qualificação relevante.

Slide 8: Ask — valor + prazo + uso + escala resultante.

Slide 9: M&E — como vamos saber que funcionou.

Slide 10: Sustentabilidade — o que acontece depois do grant.

Slide 11 (opcional): Perguntas frequentes antecipadas.

Slide 12 (opcional): Contato + obrigado.

Regras:
- Texto de CADA slide: ≤40 palavras. Notas do apresentador: 2–3 frases por slide.
- Este é ROTEIRO TEXTUAL. A skill NÃO gera imagens, NÃO abre PowerPoint, Canva, Figma, Slides. O humano monta o design depois.
- Se a peça "história de impacto" também foi marcada, o slide 3 puxa o protagonista identificado da história.
- Aplica framing de CH1 e dossiê do funder.
</peca_roteiro_deck>

<peca_narrativa_proposta>
Se marcada: narrativa de proposta para edital ou foundation formal, seções longas. Estrutura:

- Problem Statement / Apresentação do problema (2–4 parágrafos) — diagnóstico com múltiplos dados, causas estruturais, urgência, quem é afetado, contexto histórico curto.
- Methodology / Metodologia (2–3 parágrafos) — solução no nível da ação, como se chegou a este desenho, referências a práticas similares se houver.
- Workplan / Plano de trabalho (estrutura: atividade → produto → prazo → responsável) — detalha execução em etapas.
- Monitoring & Evaluation / M&E (2 parágrafos) — indicadores específicos, fontes de dado, periodicidade, quem avalia, aprendizado iterativo.
- Risk & Mitigation / Riscos (1 parágrafo) — 3–5 riscos reais com mitigação específica. NÃO riscos genéricos ("pandemia", "mudança política").
- Sustainability / Sustentabilidade (1 parágrafo) — o que acontece depois do grant, possibilidade de scale, possibilidade de continuidade sem o funder.
- Budget Narrative / Narrativa de orçamento (referência à peça própria se marcada, ou parágrafo curto).
- Team / Equipe (1 parágrafo).

Regras:
- Versão longa da base canônica, preserva estrutura foundation-standard.
- Todo dado ancorado inline.
- Se for para edital público brasileiro, usa formato brasileiro (plano de trabalho com metas, etapas, recursos — pode virar anexo estruturado no final).
</peca_narrativa_proposta>

<peca_historia_impacto>
Se marcada: história de impacto 1–2 páginas, arco narrativo curto, protagonista real identificado.

Estrutura:
- Contexto (1 parágrafo) — quem é o protagonista (NOME real ou flag explícito "pedir autorização antes de publicar"), de onde, qual era a situação específica. Não adjetivo de vulnerabilidade — descrição concreta.
- Virada (1–2 parágrafos) — o que mudou quando o protagonista encontrou o programa da OSC, o que o protagonista fez (sujeito ativo), o que aconteceu como resultado concreto.
- Resultado (1 parágrafo) — onde o protagonista está hoje, com dado concreto de onde chegou. Cita fonte/data.
- Voz direta (pelo menos uma citação) — uma fala do protagonista em discurso direto, com autorização explícita. Se não há autorização, a skill flaga.
- Conexão com o programa (1 parágrafo) — como este caso específico se conecta a N outros atendidos, com o dado agregado do <indice_dados>.

Regras:
- SE O BRIEFING NÃO TEM PROTAGONISTA REAL IDENTIFICADO, a skill RECUSA gerar esta peça. Não inventa protagonista. Não usa "Maria*" com asterisco. Não usa "beneficiária fictícia para ilustrar".
- Sem sentimentalismo. Sem adjetivo dramático. Dado concreto no lugar de emoção.
- Protagonista é sujeito gramatical ativo das frases centrais, não objeto de intervenção.
- Autorização explícita é pré-condição. Se não há, a peça sai com flag "PENDENTE: obter autorização do protagonista antes de publicar esta peça."
</peca_historia_impacto>

<peca_narrativa_orcamento>
Se marcada: narrativa de orçamento — texto que JUSTIFICA cada rubrica grossa. NÃO é a planilha.

Estrutura:
- Abertura (1 parágrafo) — ask total + prazo + o que o valor total conquista em termos de escala.
- Uma seção por rubrica grossa (~1 parágrafo cada):
  - Pessoal — quantas pessoas, que papéis, por que este custo por papel. Atado a resultado concreto.
  - Operação — quais custos operacionais (deslocamento, material, locação, contrapartida, comunicação), por que cada um é necessário para a execução, com ordem de grandeza.
  - M&E — quanto do total vai para monitoramento e avaliação (padrão foundation é 5–10%), o que especificamente vai ser feito com esse valor.
  - Overhead / estrutura — se o funder permite, quanto e para quê. Se o funder limita, a skill calcula e sinaliza se o limite inviabiliza.
- Encerramento (1 parágrafo) — custo marginal por unidade-alvo, comparação com projetos similares se houver dado.

Regras:
- Cada rubrica tem 1 frase que explica POR QUÊ este valor, atada a um resultado concreto. Sem justificativa, a rubrica vira "pede dinheiro".
- Não inventa rubrica que não está no briefing. Se o briefing não tem a divisão, pede antes de gerar.
- Respeita restrições do funder se conhecidas. Se o funder limita overhead a 10% e o projeto precisa de 18%, a skill sinaliza e pergunta como resolver.
</peca_narrativa_orcamento>

Ao terminar, responda literalmente:
"Peças geradas: [lista das marcadas]. Dados ancorados: [M]. Framing de CH1 aplicado. Pronto para Etapa 7 (revisão 4 eixos)."
````

**Output esperado:** bloco `<pecas>` com uma entrada por peça marcada, cada uma completa e ancorada em dados. Se alguma peça marcada recebeu recusa estruturada (ex: história de impacto sem protagonista real), o output inclui a recusa explícita com motivo.

### Etapa 7 — Revisão 4 eixos (equity downstream #3)

**Objetivo:** revisar cada peça gerada contra 4 eixos fixos, em tabela item-a-item. Cada achado vira linha. Eixos: **(1) factual**, **(2) normativa**, **(3) estilo/baseline**, **(4) equidade downstream**. Esta revisão é a contraparte downstream da equity lens — captura violações que escaparam da base canônica e da derivação.

**Prompt sugerido:**

````
Agora revise CADA peça gerada contra 4 eixos. Para cada achado, crie uma linha na tabela. Não há achado zero: se uma peça parece perfeita, tente 3 vezes mais; é implausível que não haja nenhum ajuste.

<revisao>
Para cada peça, examine os 4 eixos:

1. FACTUAL — rastreabilidade e precisão de dados.
- Todo dado numérico é rastreável ao <indice_dados>? Nenhum número órfão?
- Nomes de programas, locais, autoridades escritos literalmente como no briefing?
- Datas e prazos literais, não parafraseados?
- Testemunhos com autor identificado, data, contexto?
- Valor do ask consistente entre todas as peças?
Achados típicos: número aparece sem DAT_ID, prazo foi arredondado, nome do programa escrito de duas formas diferentes.

2. NORMATIVA — respeito às decisões de CH0 e CH1.
- A peça respeita o resultado do CH0? (ex: se CH0 foi VERMELHO + "aplicar com risco", a peça nomeia o risco honestamente ou tenta mascarar?)
- A peça aplica as decisões de CH1 linha a linha? (ex: se CH1 decidiu "assertivo" para um termo, a peça usa a formulação assertiva?)
- A peça distorce o projeto pra caber no funder? (viola Princípio 5)
Achados típicos: peça adiciona "inclui crianças" num programa de adolescentes pra parecer mais amplo; peça omite risco estrutural que CH0 identificou.

3. ESTILO / BASELINE — as 10 regras do fundraising-style-baseline.md.
- Regra 1: nome antes do adjetivo demográfico?
- Regra 2: número no lugar do adjetivo?
- Regra 3: causa estrutural junto com o indicador?
- Regra 4: ask mensurável presente?
- Regra 5: sem "beneficiários" como sujeito passivo?
- Regra 6: ordem problema → evidência → solução → ask preservada?
- Regra 7: adjetivo custa número? "significativo", "massivo", "transformador" acompanhados de número?
- Regra 8: M&E como parte da narrativa?
- Regra 9: orçamento narrado justifica?
- Regra 10: protagonismo da comunidade como sujeito ativo?
Achados típicos: "impacto transformador" sem número; "os beneficiários receberão treinamento" em vez de "as participantes conduzem as oficinas".

4. EQUIDADE DOWNSTREAM — deficit framing, poverty porn, invisibilização.
- Deficit framing residual escapou? (ex: "jovens em situação de vulnerabilidade" sem qualificador específico)
- Poverty porn em história de impacto? (protagonista como objeto de compaixão, sem voz direta, sem dados)
- Causa estrutural silenciada? (problema aparece como característica do grupo)
- Voz da comunidade? (citação direta com autor, ou fala atribuída genericamente?)
- "Empoderamento" ou "fortalecimento" usado sem mecanismo concreto?
Achados típicos: história de impacto sem voz direta; problema descrito como "alta evasão dos jovens" sem nomear causa estrutural.

Tabela de revisão:
Peça | Eixo | Trecho citado (literal) | Problema identificado | Correção proposta | Recomendação (aceitar | revisar | manter com justificativa)
</revisao>

Ao terminar, pare. Aguarde decisão humana linha a linha (CH2). Não aplique correções automaticamente.
````

**Output esperado:** tabela de revisão com pelo menos 3 linhas por peça (mínimo heurístico — menos que isso sugere revisão superficial, a skill reitera). Versão corrigida das peças só é produzida **depois** do CH2, não antes.

---

### CHECKPOINT HUMANO CH2 — pós-E7 (bloqueia E8)

**Pergunta obrigatória ao humano:**

> Revise a tabela de achados linha a linha. Para cada linha, escolha:
>
> - **Aceitar** — aplicar a correção proposta exatamente como está.
> - **Revisar** — a correção é na direção certa mas precisa de ajuste; proponha ajuste.
> - **Manter com justificativa** — preservar o trecho original por razão explícita (ex: "é citação literal do edital", "é termo juridicamente definido", "o funder específico usa essa linguagem e vamos espelhar").
>
> A skill aplica as correções aceitas e revisadas na versão final das peças. Decisão implícita não conta. Este é um checkpoint **técnico** — as decisões políticas maiores já foram tomadas em CH0 e CH1; aqui é aceitação de ajustes finos.
>
> Depois do CH2, a skill gera as versões finais das peças e avança para a Etapa 8 (autoverificação).

O CH2 é menos pesado que CH0 e CH1 — é item-a-item, não decisão política macro. Mas é o ponto onde o humano **ganha ou perde** qualidade final. Humano apressado aceita tudo sem ler, perde controle sobre as peças. Humano cauteloso lê linha a linha, ganha peça defensável.

### Etapa 8 — Autoverificação

**Objetivo:** a skill revisa seu próprio output contra os **6 princípios invioláveis**, declara onde cumpriu e onde ficou em dívida, lista as decisões humanas tomadas (log de CH0, CH1, CH2) com timestamp, anexa o `<indice_dados>` final, e — se a peça saiu em EN — nomeia a "revisão humana por falante nativo" como obrigação pendente.

**Prompt sugerido:**

````
Última etapa. Revise seu próprio output contra os 6 princípios invioláveis. Seja honesto — se um princípio foi violado, declare a violação em vez de mascará-la. Esta autoverificação vai para o usuário como parte do entregável.

<autoverificacao>
Para cada princípio, declare: CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO, com justificativa de 1–2 frases e evidência literal quando relevante.

Princípio 1 — Dados concretos são literais
Todo número, prazo, valor, nome rastreável ao <indice_dados>? Nenhuma paráfrase?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:

Princípio 2 — Nome antes de adjetivo, causa estrutural nomeada, protagonismo da comunidade
Nenhuma peça contém deficit framing? Passivização da comunidade eliminada?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:

Princípio 3 — Ask mensurável não é opcional
Toda peça contém ask mensurável com valor + prazo + uso + custo marginal?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:

Princípio 4 — Lente de equidade é 3 etapas, não checklist final
CH0 + CH1 + CH2 foram executados e registrados?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:

Princípio 5 — Adaptação ao funder é disciplinada, não submissa
O projeto foi preservado sem distorção? Adaptação de framing com ou sem [suposição]?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:

Princípio 6 — Anti-hallucination: não encontrado + [suposição] literais
Toda adaptação sem base marcada? Todo dado ausente marcado "não encontrado"?
Status: [CUMPRIDO | CUMPRIDO COM RESSALVA | VIOLADO]
Justificativa:
</autoverificacao>

<log_checkpoints>
Registre as 3 decisões humanas com resumo curto:
CH0 (auditoria do funder) — Decisão: [aplicar | desistir | aplicar com risco]. Razão:
CH1 (reframe do briefing) — N violações auditadas, decisões: [X conservador, Y assertivo, Z manter]. Razão curta para os "manter":
CH2 (revisão 4 eixos) — N achados, decisões: [X aceitar, Y revisar, Z manter com justificativa]. Razão curta para os "manter":
</log_checkpoints>

<indice_dados_final>
Anexe o <indice_dados> final — a tabela completa com todos os DAT_IDs citados nas peças, cada um com tipo, valor literal, fonte, data. Este é o anexo de rastreabilidade do kit.
</indice_dados_final>

<pendencia_humana_en>
Se peça gerada em EN para funder internacional:
"ATENÇÃO: as peças em EN deste kit precisam de REVISÃO HUMANA por falante nativo de inglês antes de serem submetidas ao funder. A skill fez revisão 4 eixos mas NÃO substitui revisão nativa de qualidade profissional. Não submeter sem essa revisão. Princípio 6 e consistência com a skill accessible-communication."
Se peça em PT, omita este bloco.
</pendencia_humana_en>

Ao terminar, responda:
"Autoverificação completa. [N] princípios cumpridos, [M] com ressalva, [K] violados. Kit finalizado. [se EN] Revisão nativa humana pendente."
````

**Output esperado:** autoverificação honesta contra os 6 princípios (declarar violações se houver, não mascarar), log das 3 decisões humanas, índice de dados final, aviso EN se aplicável.

## Checkpoints de validação humana

A skill tem 3 checkpoints humanos obrigatórios, com natureza distinta:

**CH0 — Pós-Etapa 2 (Auditoria do funder).** Decisão política de **aplicar ou não**. O humano revê a tabela de 8 critérios da auditoria do funder e decide: aplicar (VERDE ou AMARELO aceito), desistir (VERMELHO, a skill para aqui), ou aplicar apesar do risco (VERMELHO forçado, a skill segue sem torcer o projeto). Esta é a decisão mais consequente da skill — é o ponto onde OSC pequena pode ganhar de volta o tempo que gastaria numa aplicação destinada a falhar.

**CH1 — Pós-Etapa 4 (Auditoria do briefing).** Decisão política de **reframe**. Para cada violação identificada no briefing (deficit framing, adjetivo sem número, passivização, causa estrutural omitida), o humano escolhe: reframe conservador (reformulação mínima), reframe assertivo (reformulação estrutural), ou manter original com justificativa. A decisão trava o que vai virar linguagem padrão em 5 peças derivadas. Errar aqui contamina o kit inteiro.

**CH2 — Pós-Etapa 7 (Revisão 4 eixos).** Aceitação **técnica** item a item. Para cada achado da tabela de revisão (factual, normativa, estilo, equidade), o humano escolhe: aceitar a correção, revisar (ajustar a correção proposta), ou manter com justificativa. Menos pesado que CH0 e CH1 — mas é o ponto onde o humano **ganha ou perde** qualidade final.

**Por que 3 checkpoints e não menos?** Porque captação entrelaça três tipos de decisão distintos: (1) "vale aplicar?" (vai/não vai — política), (2) "como nomeamos?" (framing — política), e (3) "aceito as correções?" (aceitação técnica). Colapsar qualquer uma em outra borra a natureza da decisão e transfere poder político para o modelo. O mesmo princípio que a skill `stakeholder-negotiation` aplica com 3 CHs em 10 etapas.

**Regra comum aos 3:** decisão implícita ou "pode avançar" sem registro por item é **violação do Princípio 4** (equity como infraestrutura). A skill reitera o pedido de decisão explícita até receber resposta registrada.

## Falhas comuns

Seis anti-patterns comuns em captação e o contra-movimento de cada um na skill.

**1. Deficit framing reproduzido do próprio input da OSC.**

A OSC escreve seu briefing com "jovens vulneráveis sem oportunidade" porque foi assim que aprendeu a falar de si pra funders. Uma skill ingênua reproduz, e o deficit framing vaza para as 5 peças derivadas. **Contra-movimento:** Etapa 4 + CH1 — auditoria do briefing antes de escrever qualquer peça, reframe proposto com opções conservadora/assertiva, decisão política explícita. O sinal vermelho da revisão é adjetivo demográfico aparecendo antes do nome da comunidade.

**2. Ask performático.**

"Precisamos de apoio pra expandir" ou "US$ 500k pra fortalecer a rede" — sem decomposição, sem custo marginal, sem rubricas, sem timeline. Captação vira pedido genérico que funders descartam. **Contra-movimento:** pré-requisito 3 é obrigatório (ask mensurável) na Etapa 1; a regra 4 do baseline é um eixo fixo da revisão na Etapa 7; a "narrativa de orçamento" é peça própria do kit em vez de parágrafo lateral.

**3. Projeto torcido pro funder.**

O funder prioriza educação infantil; a OSC trabalha com adolescentes; a skill ingênua "ajuda" a OSC a reescrever o projeto como se fosse educação infantil. Resultado: peça boa que descreve programa que não existe. **Contra-movimento:** Princípio 5 (adaptação disciplinada, não submissa) + CH0 é decisão de ir/não ir, não de quanto torcer. Se o funder não cabe estruturalmente, a skill diz e para. Se o humano força, a peça não mente — nomeia o descompasso.

**4. História de impacto como poverty porn.**

Protagonista sem nome, "Maria*" com asterisco, descrita como objeto de compaixão, sem voz direta, sem dados concretos do resultado, sem autorização explícita de uso da imagem/história. **Contra-movimento:** a peça "história de impacto" tem regras próprias na Etapa 6 — protagonista com nome real (ou flag explícito "pedir autorização antes de publicar"), voz direta em discurso direto com autor/data, ancoragem em dado concreto do `<indice_dados>`, arco narrativo sem sentimentalismo. Se o briefing não tem protagonista real identificado, a skill **recusa gerar a peça** e explica.

**5. Pitch deck como entregável visual.**

Usuário pede "o PPT pronto" e se frustra quando recebe texto. A skill que promete "gerar o deck" e tenta honrar com Markdown vira ferramenta errada. **Contra-movimento:** a Etapa 1 nomeia explicitamente que a peça "roteiro de pitch deck" é texto + notas do apresentador, não design; a skill não abre PowerPoint, Canva, Figma, Slides; na revisão da Etapa 7, a peça é checada como texto (não como layout). O humano monta o design depois na ferramenta visual de escolha.

**6. Concept note genérica reutilizada.**

A OSC tem uma concept note que funcionou uma vez, copia pra todos os funders, só troca o cabeçalho. Resultado: zero adaptação de framing, mesma peça pra Ford e BNDES, rejeição nos dois. **Contra-movimento:** Etapa 2 força o dossiê ou pelo menos o tipo do funder no início; Etapa 6 aplica o framing decidido na geração de cada peça; Etapa 7 eixo normativo verifica aderência ao framing decidido. Skill não aceita "qualquer funder" como input — exige identificação.

## Arquivos complementares

Esta skill traz 4 arquivos em `references/` (um a mais que o padrão de 3, porque inclui linha de base de estilo própria paralela a `style-guide.md` do `technical-note-writing` e `plain-language-baseline.md` do `accessible-communication`).

1. **[`fundraising-style-baseline.md`](references/fundraising-style-baseline.md)** — 10 regras operacionais com exemplos errado/certo + seção `## Aplicação em EN`. Linha de base: "disciplina de prosa do fundraising profissional (Candid / Chronicle of Philanthropy) + framing de protagonismo do Community-Centric Fundraising, sem deficit framing". Carregada como contexto ativo na Etapa 1 e aplicada durante toda a geração a partir da Etapa 5.

2. **[`exemplos.md`](references/exemplos.md)** — execução completa de 1 caso realista ponta a ponta. Percorre as 8 etapas com 3 checkpoints humanos — da configuração à autoverificação final. Mostra a textura operacional: como preencher `<auditoria_funder>`, como fazer o diálogo ToC-lite, como ancorar dados inline no `<indice_dados>`, como o CH1 fica quando há violações reais, como uma concept note em EN sai estruturada.

3. **[`variantes.md`](references/variantes.md)** — 8 variações do workflow base em duas dimensões: (a) **por tipo de funder** — V1 foundation internacional, V2 edital público brasileiro, V3 filantropia corporativa, V4 doador individual; cada variante documenta o que muda em E2 (critérios de auditoria), E5 (ênfase da base canônica) e E6 (quais peças fazem sentido); e (b) **por chain-in** — V5 chain de `theory-of-change`, V6 de `project-structuring`, V7 de `evidence-synthesis`, V8 input solto (documento próprio ou diálogo ToC-lite).

4. **[`checklist.md`](references/checklist.md)** — checklist pro humano validar, com seção técnica (pré-requisitos cumpridos, dados rastreáveis, ask mensurável, baseline aplicado, 3 CHs registrados, peça EN marcada para revisão nativa) e seção equidade (auditoria do funder com veredicto explícito, reframe de CH1 decidido por linha, eixo 4 da revisão aplicado, história de impacto com protagonista identificado ou flag de autorização, narrativa de orçamento justifica sem inventar).

---

> **Lente de equidade compartilhada:** esta skill herda o framework de `docs/equity-lens.md` do repositório. A operacionalização específica desta skill em 3 etapas (auditoria do funder, reframe do briefing, revisão downstream) é uma aplicação dos princípios do equity-lens, não uma substituição.
