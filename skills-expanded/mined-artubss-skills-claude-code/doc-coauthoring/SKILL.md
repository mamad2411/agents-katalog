---
name: doc-coauthoring
description: Orienta usuários através de um fluxo de trabalho estruturado para coautoria de documentação. Use quando o usuário quer escrever documentação, propostas, especificações técnicas, decision docs ou conteúdo estruturado similar. Este fluxo ajuda usuários a transferir contexto de forma eficiente, refinar conteúdo através de iterações e verificar se o doc funciona para leitores. Dispare quando o usuário menciona escrever docs, criar propostas, elaborar specs, ou tarefas de documentação similares.
---

# Fluxo de Trabalho de Coautoria de Documentação

Esta skill fornece um fluxo de trabalho estruturado para orientar usuários através da criação de documentos colaborativos. Atue como um guia ativo, conduzindo usuários através de três etapas: Coleta de Contexto, Refinamento & Estrutura, e Teste com Leitores.

## Quando Oferecer Este Fluxo

**Condições de disparo:**
- Usuário menciona escrever documentação: "escrever um doc", "elaborar uma proposta", "criar um spec", "documentar"
- Usuário menciona tipos específicos de doc: "PRD", "design doc", "decision doc", "RFC"
- Usuário parece estar iniciando uma tarefa de escrita substancial

**Oferta inicial:**
Ofereça ao usuário um fluxo de trabalho estruturado para coautoria do documento. Explique as três etapas:

1. **Coleta de Contexto**: Usuário fornece todo o contexto relevante enquanto Claude faz perguntas de esclarecimento
2. **Refinamento & Estrutura**: Construir iterativamente cada seção através de brainstorming e edição
3. **Teste com Leitores**: Testar o doc com um novo Claude (sem contexto) para identificar pontos cegos antes de outros lerem

Explique que essa abordagem ajuda a garantir que o doc funcione bem quando outras pessoas o lerem (inclusive quando colarem no Claude). Perguntaé se querem tentar esse fluxo ou preferem trabalhar de forma livre.

Se o usuário recusar, trabalhe de forma livre. Se aceitar, prossiga para a Etapa 1.

## Etapa 1: Coleta de Contexto

**Objetivo:** Fechar a lacuna entre o que o usuário sabe e o que Claude sabe, permitindo orientação inteligente depois.

### Perguntas Iniciais

Comece perguntando ao usuário sobre metacontexto do documento:

1. Que tipo de documento é este? (ex: especificação técnica, decision doc, proposta)
2. Qual é o público-alvo principal?
3. Qual é o impacto desejado quando alguém lê isto?
4. Existe um template ou formato específico a seguir?
5. Há outras restrições ou contexto que eu deva saber?

Informe que podem responder de forma breve ou despejar informações da forma que funcionar melhor para eles.

**Se o usuário fornece um template ou menciona um tipo de doc:**
- Pergunte se têm um documento template para compartilhar
- Se fornecerem um link a um documento compartilhado, use a integração apropriada para recuperá-lo
- Se fornecerem um arquivo, leia-o

**Se o usuário menciona editar um documento compartilhado existente:**
- Use a integração apropriada para ler o estado atual
- Verifique se há imagens sem texto alternativo
- Se houver imagens sem alt-text, explique que quando outros usarem Claude para entender o doc, Claude não conseguirá vê-las. Perguntaé se querem gerar alt-text. Se sim, solicite que colem cada imagem no chat para geração de alt-text descritivo.

### Despejo de Informações

Uma vez respondidas as perguntas iniciais, incentive o usuário a despejar todo o contexto que tem. Solicite informações como:
- Background do projeto/problema
- Discussões relacionadas da equipe ou documentos compartilhados
- Por que soluções alternativas não estão sendo usadas
- Contexto organizacional (dinâmica da equipe, incidentes passados, política)
- Pressões de timeline ou restrições
- Arquitetura técnica ou dependências
- Preocupações dos stakeholders

Aconselhe-os a não se preocupar em organizá-lo - apenas colocar tudo para fora. Ofereça múltiplas formas de fornecer contexto:
- Despejo de informações stream-of-consciousness
- Apontar para canais da equipe ou threads para ler
- Ligar para documentos compartilhados

**Se integrações estão disponíveis** (ex: Slack, Teams, Google Drive, SharePoint, ou outros servidores MCP), mencione que podem ser usadas para puxar contexto diretamente.

**Se nenhuma integração for detectada e em Claude.ai ou app Claude:** Sugira que podem habilitar conectores nas configurações do Claude para permitir puxar contexto de apps de mensageria e armazenamento de documentos diretamente.

Informe que perguntas de esclarecimento serão feitas uma vez que tenham feito seu despejo inicial.

**Durante a coleta de contexto:**

- Se o usuário menciona canais de equipe ou documentos compartilhados:
  - Se integrações disponíveis: Informe que o conteúdo será lido agora, então use a integração apropriada
  - Se integrações não disponíveis: Explique falta de acesso. Sugira habilitar conectores nas configurações do Claude, ou colar o conteúdo relevante diretamente.

- Se o usuário menciona entidades/projetos desconhecidos:
  - Perguntaé se ferramentas conectadas devem ser pesquisadas para aprender mais
  - Aguarde confirmação do usuário antes de pesquisar

- Conforme o usuário fornece contexto, rastreie o que está sendo aprendido e o que ainda não está claro

**Fazendo perguntas de esclarecimento:**

Quando o usuário sinalizar que terminou seu despejo inicial (ou após contexto substancial fornecido), faça perguntas de esclarecimento para garantir compreensão:

Gere 5-10 perguntas numeradas baseadas em lacunas no contexto.

Informe que podem usar abreviações para responder (ex: "1: sim, 2: veja #canal, 3: não porque compatibilidade retroativa"), ligar para mais docs, apontar para canais para ler, ou apenas continuar despejando informações. O que for mais eficiente para eles.

**Condição de saída:**
Contexto suficiente foi coletado quando as perguntas mostram compreensão - quando casos extremos e trade-offs podem ser perguntados sem precisar explicar o básico.

**Transição:**
Perguntaé se há mais contexto que querem fornecer nesta etapa, ou se é hora de passar para o rascunho do documento.

Se o usuário quer adicionar mais, deixe. Quando estiver pronto, prossiga para a Etapa 2.

## Etapa 2: Refinamento & Estrutura

**Objetivo:** Construir o documento seção por seção através de brainstorming, curadoria e refinamento iterativo.

**Instruções para o usuário:**
Explique que o documento será construído seção por seção. Para cada seção:
1. Perguntas de esclarecimento serão feitas sobre o que incluir
2. 5-20 opções serão brainstormadas
3. Usuário indicará o que manter/remover/combinar
4. A seção será rascunhada
5. Será refinada através de edições cirúrgicas

Comece com a seção que tem mais incógnitas (geralmente a decisão/proposta central), depois trabalhe através do resto.

**Ordenação de seções:**

Se a estrutura do documento é clara:
Perguntaé qual seção eles gostariam de começar.

Sugira começar com qualquer seção que tenha o máximo de incógnitas. Para decision docs, essa é geralmente a proposta central. Para specs, é tipicamente a abordagem técnica. Seções de resumo são melhores deixadas para o final.

Se o usuário não sabe que seções precisa:
Baseado no tipo de documento e template, sugira 3-5 seções apropriadas para o tipo de doc.

Perguntaé se essa estrutura funciona, ou se querem ajustá-la.

**Uma vez que a estrutura é acordada:**

Crie a estrutura inicial do documento com texto placeholder para todas as seções.

**Se acesso a artifacts está disponível:**
Use `create_file` para criar um artifact. Isso dá tanto ao Claude quanto ao usuário um scaffold para trabalhar.

Informe que a estrutura inicial com placeholders para todas as seções será criada.

Crie artifact com todos os headers de seção e texto placeholder breve como "[A ser escrito]" ou "[Conteúdo aqui]".

Forneça o link do scaffold e indique que é hora de preencher cada seção.

**Se nenhum acesso a artifacts:**
Crie um arquivo markdown no diretório de trabalho. Nomeie apropriadamente (ex: `decision-doc.md`, `technical-spec.md`).

Informe que a estrutura inicial com placeholders para todas as seções será criada.

Crie arquivo com todos os headers de seção e texto placeholder.

Confirme que o arquivo foi criado e indique que é hora de preencher cada seção.

**Para cada seção:**

### Passo 1: Perguntas de Esclarecimento

Anuncie que o trabalho começará na seção [NOME DA SEÇÃO]. Faça 5-10 perguntas de esclarecimento sobre o que deve ser incluído:

Gere 5-10 perguntas específicas baseadas em contexto e propósito da seção.

Informe que podem responder de forma breve ou apenas indicar o que é importante cobrir.

### Passo 2: Brainstorming

Para a seção [NOME DA SEÇÃO], brainstorme [5-20] coisas que podem ser incluídas, dependendo da complexidade da seção. Procure por:
- Contexto compartilhado que pode ter sido esquecido
- Ângulos ou considerações ainda não mencionadas

Gere 5-20 opções numeradas baseadas na complexidade da seção. No final, ofereça brainstorm de mais se querem opções adicionais.

### Passo 3: Curadoria

Perguntaé quais pontos devem ser mantidos, removidos, ou combinados. Solicite breves justificativas para ajudar a aprender prioridades para as próximas seções.

Forneça exemplos:
- "Manter 1,4,7,9"
- "Remover 3 (duplica 1)"
- "Remover 6 (público já sabe disso)"
- "Combinar 11 e 12"

**Se o usuário der feedback freeform** (ex: "parece bom" ou "eu gosto de mais ou menos disso") em vez de seleções numeradas, extraia suas preferências e prossiga. Parse o que querem manter/remover/mudar e aplique.

### Passo 4: Verificação de Lacunas

Baseado no que selecionaram, perguntaé se há algo importante faltando para a seção [NOME DA SEÇÃO].

### Passo 5: Rascunho

Use `str_replace` para substituir o texto placeholder desta seção com o conteúdo rascunhado real.

Anuncie que a seção [NOME DA SEÇÃO] será rascunhada agora baseado no que selecionaram.

**Se usando artifacts:**
Depois de rascunhar, forneça um link para o artifact.

Peça que leiam e indiquem o que mudar. Note que ser específico ajuda o aprendizado para as próximas seções.

**Se usando um arquivo (sem artifacts):**
Depois de rascunhar, confirme conclusão.

Informe que a seção [NOME DA SEÇÃO] foi rascunhada em [filename]. Peça que leiam e indiquem o que mudar. Note que ser específico ajuda o aprendizado para as próximas seções.

**Instrução-chave para o usuário (inclua ao rascunhar a primeira seção):**
Forneça uma nota: Em vez de editar o doc diretamente, peça para indicarem o que mudar. Isso ajuda o aprendizado do seu estilo para seções futuras. Por exemplo: "Remova o bullet X - já coberto por Y" ou "Torne o terceiro parágrafo mais conciso".

### Passo 6: Refinamento Iterativo

Conforme o usuário fornece feedback:
- Use `str_replace` para fazer edições (nunca reimprima o doc inteiro)
- **Se usando artifacts:** Forneça link para artifact depois de cada edição
- **Se usando arquivos:** Apenas confirme que edições estão completas
- Se o usuário edita o doc diretamente e pede para ler: note mentalmente as mudanças que fizeram e mantenha-as em mente para seções futuras (isso mostra suas preferências)

**Continue iterando** até o usuário estar satisfeito com a seção.

### Verificação de Qualidade

Depois de 3 iterações consecutivas sem mudanças substanciais, perguntaé se algo pode ser removido sem perder informação importante.

Quando a seção está pronta, confirme que [NOME DA SEÇÃO] está completa. Perguntaé se estão prontos para a próxima seção.

**Repita para todas as seções.**

### Próximo à Conclusão

Ao se aproximar da conclusão (80%+ das seções feitas), anuncie a intenção de reler o documento inteiro e verificar:
- Fluxo e consistência entre seções
- Redundância ou contradições
- Qualquer coisa que pareça "entulho" ou preenchimento genérico
- Se toda frase carrega peso

Leia o documento inteiro e forneça feedback.

**Quando todas as seções foram rascunhadas e refinadas:**
Anuncie que todas as seções foram rascunhadas. Indique a intenção de revisar o documento completo mais uma vez.

Revise para coerência geral, fluxo, completude.

Forneça quaisquer sugestões finais.

Perguntaé se estão prontos para passar para o Teste com Leitores, ou se querem refinar qualquer coisa mais.

## Etapa 3: Teste com Leitores

**Objetivo:** Testar o documento com um novo Claude (sem vazamento de contexto) para verificar se funciona para leitores.

**Instruções para o usuário:**
Explique que o teste ocorrerá agora para ver se o documento realmente funciona para leitores. Isso identifica pontos cegos - coisas que fazem sentido para os autores mas podem confundir outros.

### Abordagem de Teste

**Se acesso a sub-agentes está disponível (ex: em Claude Code):**

Realize o teste diretamente sem envolvimento do usuário.

### Passo 1: Prever Perguntas de Leitores

Anuncie a intenção de prever que perguntas os leitores podem fazer quando tentam descobrir este documento.

Gere 5-10 perguntas que os leitores fariam realisticamente.

### Passo 2: Testar com Sub-Agente

Anuncie que essas perguntas serão testadas com uma instância fresca de Claude (sem contexto desta conversa).

Para cada pergunta, invoque um sub-agente com apenas o conteúdo do documento e a pergunta.

Resuma o que Reader Claude acertou/errou para cada pergunta.

### Passo 3: Executar Verificações Adicionais

Anuncie que verificações adicionais serão realizadas.

Invoque sub-agente para verificar ambiguidade, falsas suposições, contradições.

Resuma quaisquer problemas encontrados.

### Passo 4: Relatar e Corrigir

Se problemas encontrados:
Relate que Reader Claude teve dificuldade com problemas específicos.

Liste os problemas específicos.

Indique a intenção de corrigir essas lacunas.

Volte ao refinamento para seções problemáticas.

---

**Se nenhum acesso a sub-agentes (ex: interface web claude.ai):**

O usuário precisará fazer o teste manualmente.

### Passo 1: Prever Perguntas de Leitores

Perguntaé que perguntas as pessoas podem fazer quando tentam descobrir este documento. O que elas digitariam no Claude.ai?

Gere 5-10 perguntas que os leitores fariam realisticamente.

### Passo 2: Configurar Teste

Forneça instruções de teste:
1. Abra uma conversa fresca do Claude: https://claude.ai
2. Cole ou compartilhe o conteúdo do documento (se usar plataforma de doc compartilhado com conectores ativados, forneça o link)
3. Faça ao Reader Claude as perguntas geradas

Para cada pergunta, instrua Reader Claude a fornecer:
- A resposta
- Se algo era ambíguo ou pouco claro
- Que conhecimento/contexto o doc assume que já é conhecido

Verifique se Reader Claude dá respostas corretas ou mal-interpreta algo.

### Passo 3: Verificações Adicionais

Também pergunte ao Reader Claude:
- "O que neste doc pode ser ambíguo ou pouco claro para leitores?"
- "Que conhecimento ou contexto este doc assume que os leitores já têm?"
- "Há alguma contradição interna ou inconsistência?"

### Passo 4: Iterar Baseado em Resultados

Perguntaé o que Reader Claude errou ou teve dificuldade. Indique a intenção de corrigir essas lacunas.

Volte ao refinamento para qualquer seção problemática.

---

### Condição de Saída (Ambas as Abordagens)

Quando Reader Claude consistentemente responde perguntas corretamente e não expõe novas lacunas ou ambiguidades, o doc está pronto.

## Revisão Final

Quando Reader Testing passa:
Anuncie que o doc passou no teste de Reader Claude. Antes da conclusão:

1. Recomende fazer uma leitura final si mesmos - eles possuem este documento e são responsáveis por sua qualidade
2. Sugira double-check de qualquer fato, links, ou detalhes técnicos
3. Peça que verifiquem se alcança o impacto que queriam

Perguntaé se querem uma revisão mais, ou se o trabalho está pronto.

**Se o usuário quer revisão final, forneça-a. Caso contrário:**
Anuncie conclusão do documento. Forneça algumas dicas finais:
- Considere ligar esta conversa em um apêndice para que leitores vejam como o doc foi desenvolvido
- Use apêndices para fornecer profundidade sem inchar o doc principal
- Atualize o doc conforme feedback é recebido de leitores reais

## Dicas para Orientação Efetiva

**Tom:**
- Seja direto e procedural
- Explique rationale brevemente quando afetar comportamento do usuário
- Não tente "vender" a abordagem - apenas execute-a

**Tratando Desvios:**
- Se usuário quer pular uma etapa: Perguntaé se quer pular isto e escrever de forma livre
- Se usuário parece frustrado: Reconheça que isto está levando mais tempo que esperado. Sugira formas de se mover mais rápido
- Sempre dê ao usuário agência para ajustar o processo

**Gerenciamento de Contexto:**
- Ao longo, se contexto está faltando em algo mencionado, pergunte proativamente
- Não deixe lacunas acumularem - aborde-as conforme surgem

**Gerenciamento de Artifacts:**
- Use `create_file` para rascunhar seções completas
- Use `str_replace` para todas as edições
- Forneça link de artifact depois de cada mudança
- Nunca use artifacts para listas de brainstorming - isso é apenas conversa

**Qualidade sobre Velocidade:**
- Não se apresse através das etapas
- Cada iteração deve fazer melhorias significativas
- O objetivo é um documento que realmente funciona para leitores