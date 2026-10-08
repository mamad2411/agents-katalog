---
slug: escalation-rca-skill
canonical_slug: escalation-rca-skill
locale: pt-BR
verticals: [customer-success]
title: Redija uma análise de causa raiz de escalação com Claude
artifact_type: claude-skill
tools_used: [claude, zendesk, gong]
roles: [csm, support-lead]
difficulty: intermediate
time_to_setup: "45-60 min"
human_tested: false
last_updated: "2026-06-06"
---

Uma [Claude](/pt-BR/tools/claude/) Skill que transforma uma escalação de cliente em uma análise de causa raiz (RCA) defensável: uma linha do tempo reconstruída de cada toque de ticket e call, uma causa raiz nomeada separada de seus fatores contribuintes, e um plano de ações corretivas com responsáveis e datas. Ela lê a thread do ticket no [Zendesk](/pt-BR/tools/zendesk/) mais qualquer ticket irmão vinculado e as calls do Gong atreladas à conta durante a janela de escalação, e então produz um único RCA em Markdown que o CSM edita e o support lead aprova antes de ir ao cliente ou a um post-incident review interno. O bundle do artifact inclui o SKILL.md mais três arquivos de referência que o time adapta uma vez e reusa em cada escalação.

O bundle do artifact fica em `apps/web/public/artifacts/escalation-rca-skill/`. Ele contém `SKILL.md`, `references/1-rca-template.md` (o esqueleto de output com seções nomeadas), `references/2-cause-taxonomy.md` (a lista fixa de categorias de causa raiz nas quais a Skill deve classificar), e `references/3-sample-rca.md` (um exemplo trabalhado anonimizado que a passada de tone-match imita). Leia os três antes da primeira execução.

## Quando usar

Você é um CSM ou um support lead que acabou de ter uma conta escalando —uma queda sev-1 que deixa o cliente irritado, uma série de tickets mal tratados, uma reclamação que ameaça o renewal— e precisa de um RCA escrito rápido, antes da reunião de postmortem ou da call de desculpas ao cliente. A Skill foi construída para o caso onde a evidência está espalhada entre uma thread do Zendesk, três ou quatro tickets irmãos abertos por pessoas diferentes do lado do cliente, e duas ou três calls do Gong onde a frustração de fato veio à tona. Montar essa linha do tempo na mão são 60 a 120 minutos trocando de aba; a Skill faz a montagem e te entrega um rascunho sobre o qual raciocinar.

Ela produz o output mais útil quando os tickets do Zendesk estão vinculados (via a conta ou um link explícito `problem`/`incident`) e tagueados de forma consistente, e quando ao menos uma call do Gong na janela tem transcrição. Ela é calibrada para um único evento de escalação com uma janela delimitada —tipicamente os 14 a 30 dias ao redor do incidente disparador— não para uma análise de padrão de um trimestre inteiro.

## Quando NÃO usar

Não envie o output da Skill ao cliente sem editar. É um motor de rascunho. A causa raiz é uma hipótese que o CSM e o support lead confirmam contra o próprio conhecimento antes de alguém assinar com o nome. Um RCA enviado a um cliente irritado com uma causa raiz errada faz mais dano do que nenhum RCA.

Não use quando a linha do tempo tem menos de três eventos. Com um ticket e nenhuma call não há nada a reconstruir, e a Skill foi construída para retornar `insufficient data` em vez de fabricar uma narrativa —mas só se você respeitar essa recusa em vez de forçar uma execução. Um RCA confiante construído sobre dois data points se lê com autoridade e engana todos que agem sobre ele.

Não use para disputas legais ou contratuais, postmortems de incidente de segurança, ou qualquer coisa rumo a uma negociação de crédito de SLA onde a redação é adversarial. A Skill escreve um RCA operacional em um registro neutro e responsável; ela não escreve linguagem jurídica defensável e vai subestimar ou superestimar a responsabilidade de formas que importam quando há dinheiro ou termos de contrato em jogo. Roteie esses para o time que os possui.

Não use como preditor de churn ou como health score. Ela explica um evento passado. O workflow de composite health score é a ferramenta calibrada para risco de retenção olhando para frente; ler a classificação de severidade deste RCA como uma probabilidade de churn vai te enganar.

## Setup

Aproximadamente 45 a 60 minutos na primeira vez, a maior parte gasta adaptando a taxonomia de causas em `references/2-cause-taxonomy.md` aos modos de falha reais do seu time.

1. **Instale a Skill.** Coloque o bundle de `apps/web/public/artifacts/escalation-rca-skill/` em `~/.claude/skills/escalation-rca/`. A Skill define um único comando, `draft_rca(account_id, escalation_window, anchor_ticket_id)`, mais helpers internos para o pull do Zendesk, o pull do Gong, o merge de linha do tempo e o pipeline de duas passadas do Claude.
2. **Conecte credenciais.** Configure `ZENDESK_SUBDOMAIN` e `ZENDESK_API_TOKEN` (acesso de leitura em Tickets, Ticket Comments e Ticket Audits —os audits são o que te dá os timestamps de mudança de status), e `GONG_API_KEY` (acesso de leitura em calls e transcrições). A Skill não faz escritas em nenhum dos dois sistemas; é read-only por design para poder rodar contra produção sem um review de controle de mudanças.
3. **Adapte a taxonomia de causas.** Abra `references/2-cause-taxonomy.md` e substitua as categorias placeholder pelas reais do seu time. O set padrão é `product-defect`, `config-error`, `documentation-gap`, `process-breakdown`, `capacity-overload`, `communication-failure` e `third-party-dependency`. A Skill classifica a causa raiz em exatamente uma dessas e lista o resto como fatores contribuintes onde a evidência os suporta; uma causa raiz em texto livre é a razão mais comum de dois RCAs do mesmo incidente discordarem, então a taxonomia fixa é estrutural, não decoração.
4. **Adapte o template e a amostra de voz.** Edite `references/1-rca-template.md` para que os nomes de seção batam com o que seu processo de postmortem espera (alguns times precisam de uma seção `customer-impact` com contagem de usuários afetados; alguns precisam de uma seção `detection`). Substitua o exemplo trabalhado em `references/3-sample-rca.md` por dois ou três RCAs anteriores anonimizados que seu time escreveu, para que a passada de tone-match imite seu estilo de casa em vez da amostra genérica.
5. **Execute para uma escalação.** `draft_rca(account_id="...", escalation_window="2026-05-20:2026-06-03", anchor_ticket_id="48213")`. A Skill escreve um arquivo Markdown: a linha do tempo reconstruída, a seção de causa raiz, a lista de fatores contribuintes, a tabela de ações corretivas e um resumo voltado ao cliente de um parágrafo que o CSM pode aproveitar ou reescrever.

## O que a Skill faz de verdade

A Skill puxa Zendesk e Gong em paralelo porque eles batem em sistemas independentes e o gargalo é a latência da API, não os tokens do Claude. Do Zendesk ela puxa o ticket âncora, cada ticket irmão vinculado à mesma conta ou problema dentro da janela e —criticamente— o audit log de cada ticket, porque os audits carregam os timestamps de mudança de status e de mudança de assignee que a thread de comentários sozinha não tem. Do Gong ela puxa as calls da conta dentro da janela, limitadas às seis mais recentes, com transcrições truncadas em 4,000 caracteres cada. Se qualquer sistema retorna vazio, a Skill registra o gap na linha do tempo em vez de preenchê-lo.

Depois ela funde tudo em uma única linha do tempo cronológica chaveada em timestamps UTC. O merge é um passo determinístico, não um passo do Claude, porque a ordenação de timestamps é exatamente o tipo de coisa que um modelo de linguagem erra sutilmente e um sort não. Cada evento carrega sua fonte (`zendesk-comment`, `zendesk-status-change`, `gong-call`), seu ator e um resumo de uma linha. Essa linha do tempo fundida é a espinha dorsal de todo o RCA, e está no output verbatim para que o leitor possa auditar cada afirmação downstream contra ela.

Então duas passadas do Claude. A passada um é análise causal: o Claude lê a linha do tempo fundida e a taxonomia de causas e produz uma única causa raiz nomeada, uma lista separada de fatores contribuintes e os eventos específicos da linha do tempo que suportam cada um. Separar causa raiz de fatores contribuintes em uma passada dedicada importa porque a falha de RCA mais comum é confundir as duas —chamar de causa o sintoma mais barulhento. A passada é instruída a citar eventos da linha do tempo pelo timestamp em cada afirmação causal e a retornar `insufficient data` se existirem menos de três eventos dentro da janela.

A passada dois é o plano de ações corretivas e o tone-match. O Claude pega a causa raiz confirmada mais os fatores contribuintes e propõe uma tabela de ações corretivas —cada linha uma ação, um papel responsável (não uma pessoa nomeada; o time atribui nomes), um offset de data de vencimento e o fator contribuinte que ela fecha. Depois reescreve todo o RCA na voz do time usando as amostras em `references/3-sample-rca.md`, e escreve o resumo voltado ao cliente de um parágrafo em um registro mais conservador que nomeia impacto e remediação sem admitir responsabilidade que o time não acordou. Separar ações e tom na própria passada mantém o raciocínio causal da passada um sem contaminação pela suavização que o resumo voltado ao cliente exige.

## Realidade de custos

Uma execução completa custa aproximadamente 15,000 a 30,000 tokens de input e 2,000 a 4,000 tokens de output no Claude Sonnet —chame de 6 a 12 centavos por RCA aos preços atuais do Sonnet. A variável de input dominante é o volume de transcrições do Gong; uma conta muito escalada com seis calls registradas na janela aterrissa perto do topo, uma escalação só de tickets sem calls perto do piso. O design de duas passadas compartilha contexto prefixo, então a segunda passada é mais barata que a primeira.

O tempo de relógio é dois a quatro minutos, dominado pelos pulls do audit log do Zendesk (uma chamada de API extra por ticket) e o fetch de transcrições do Gong. As duas passadas do Claude adicionam 40 a 70 segundos depois que o pull paralelo termina.

Um CSM ou support lead escrevendo um RCA do zero tipicamente gasta 60 a 120 minutos —puxando tickets, lendo audits, reescutando calls, reconstruindo a linha do tempo e então escrevendo. A Skill leva isso a 20 a 35 minutos de edição, então a economia é aproximadamente uma hora por escalação. Uma organização de suporte rodando 15 a 25 escalações formais por trimestre recupera 15 a 25 horas de tempo de IC sênior, que é onde o custo é sentido mais porque escalações caem nas pessoas mais experientes.

## Métrica de sucesso

Acompanhe o tempo de "escalação declarada" até "RCA circulado para sign-off interno". A Skill deve puxar a mediana para menos de 90 minutos dentro do primeiro trimestre de uso, contra uma linha de base do zero de meio dia ou mais. Acompanhe também a taxa na qual a causa raiz proposta sobrevive ao review do support lead sem mudança —mire em 60% ou mais. Mais baixo que isso e a taxonomia de causas precisa ser recortada para bater com como seus incidentes de fato falham; mais alto que 85% e o lead provavelmente está carimbando em vez de revisar, o que derrota a guarda de human-in-the-loop.

Um segundo número que vale acompanhar: a parcela de ações corretivas de RCAs passados que de fato foram fechadas na data de vencimento. A Skill não força isso —ela só propõe as ações— mas se essa parcela fica abaixo de 50%, o processo de RCA é teatro e um motor de rascunho mais rápido não vai consertar. A métrica te diz se a organização está agindo sobre as causas raiz ou só documentando-as.

## Versus as alternativas

**Versus um RCA manual em um Google Doc.** O status quo da maioria dos times. RCAs manuais são de maior fidelidade quando o autor esteve pessoalmente no loop do incidente, porque carregam contexto que os sistemas nunca registraram —a thread do Slack, a conversa de corredor, a leitura visceral da reclamação real do cliente. O trade-off é a hora-e-pouco de montagem de linha do tempo, que é puro trabalho mecânico que a Skill elimina. Use manual para a rara escalação de nível de board onde cada palavra é pesada; use a Skill para o volume constante de escalações operacionais onde a restrição é o tempo de IC sênior, não o ofício narrativo. Mesmo para o caso de nível de board a linha do tempo reconstruída da Skill é um artifact de partida útil.

**Versus as funções nativas de merge de tickets e side-conversation do Zendesk.** O Zendesk pode vincular e fundir tickets relacionados e mostrar uma visão unificada, e se tudo que você precisa é o histórico consolidado de tickets isso é menos trabalho que instalar uma Skill. Mas o Zendesk mostra os tickets; ele não reconstrói uma linha do tempo cross-system que inclua calls do Gong, e não nomeia uma causa raiz nem propõe ações corretivas. Ele te dá a matéria-prima; a Skill escreve a análise. Use o linking do Zendesk para manter os tickets irmãos descobríveis —a Skill depende desse linking para encontrá-los— e a Skill para transformar o conjunto vinculado em um RCA.

**Versus uma ferramenta dedicada de incident management (um incident.io ou um FireHydrant).** Essas são excelentes para resposta a incidente liderada por engenharia com rotações on-call, status pages e andaime automatizado de postmortem. Se suas escalações são incidentes de infraestrutura e você já roda uma, use o fluxo de postmortem dela. Mas essas ferramentas são construídas ao redor do ciclo de vida do incidente de engenharia, não do de relacionamento com o cliente; elas não leem suas calls do Gong nem escrevem na voz voltada ao cliente do seu time de CSM. Para uma escalação de posse do CS que é tanto sobre um relacionamento quanto sobre um defeito, esta Skill encaixa na costura que essas ferramentas deixam aberta.

## A vigiar

- **Viés de retrospectiva na passada causal.** Ler uma linha do tempo de trás para frente a partir de um resultado conhecido-ruim faz cada decisão anterior parecer um erro óbvio, e o Claude vai narrar assim se não estiver guardado. Guarda: a passada um é instruída a distinguir o que era conhecível em cada evento do que só é conhecível em retrospectiva, e a marcar qualquer afirmação que dependa da retrospectiva. Ela também retorna `insufficient data` em vez de adivinhar quando existem menos de três eventos de linha do tempo dentro da janela —nenhuma narrativa é construída sobre uma base fina demais para suportar uma.
- **Audit logs faltando colapsam a linha do tempo.** Se o token do Zendesk não tem scope de leitura de audit, a Skill silenciosamente obtém comentários sem timestamps de mudança de status, e a linha do tempo perde os eventos de "o ticket ficou em pending por nove dias" que frequentemente são a verdadeira história. Guarda: a Skill checa o acesso a audit no ticket âncora durante a verificação de setup e recusa rodar com um erro `ZENDESK_AUDIT_SCOPE_MISSING` em vez de produzir uma linha do tempo que omite os eventos mais importantes.
- **Causa raiz confundida com o sintoma mais barulhento.** O evento sobre o qual o cliente mais reclamou raramente é a causa raiz; geralmente é um sintoma downstream. Um modelo sem guarda se ancora no volume. Guarda: a taxonomia de causas em `references/2-cause-taxonomy.md` força uma única categoria classificada, e a passada um deve citar o evento específico da linha do tempo que é o ponto mais cedo em que a causa esteve em jogo —não o mais barulhento, o mais cedo. Sintomas que vieram depois são arquivados como fatores contribuintes.
- **Sentimento do Gong sobre-lido em transcrições finas.** Uma única call curta é superponderada como "o cliente está furioso" quando a transcrição é um voicemail de 90 segundos. Guarda: a Skill limita a influência do Gong na passada causal a evidência corroborante —uma call pode suportar um evento de linha do tempo mas não pode sozinha ser a causa raiz nomeada, porque uma reclamação registrada é um sintoma, não uma causa. Transcrições abaixo de 200 palavras são marcadas como baixa-confiança e excluídas da leitura de sentimento.
- **Resumo voltado ao cliente admitindo responsabilidade que o time não acordou.** A passada dois escreve um resumo que o cliente pode ler, e um LLM deixado ao próprio registro vai pedir desculpas por coisas que a empresa não decidiu assumir. Guarda: o prompt do resumo voltado ao cliente nomeia só impacto e remediação, proíbe explicitamente atribuir culpa ou prometer compensação, e prefixa o parágrafo com um marcador `REVIEW BEFORE SENDING` que o CSM deve remover na mão —não há caminho onde o texto voltado ao cliente sai da Skill sem um toque humano.

## Stack

- **Zendesk** —thread de tickets, tickets irmãos e os audit logs que carregam os timestamps de mudança de status (REST API, read-only)
- **Gong** —transcrições e metadata de calls da conta dentro da janela de escalação (Gong API, read-only)
- **Claude** —análise de duas passadas: análise causal contra a taxonomia, depois plano de ações corretivas mais tone-match (Sonnet recomendado por custo; Opus só se o resumo voltado ao cliente carrega sensibilidade incomum)
