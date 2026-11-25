---
name: content-strategy
description: Quando o usuário quiser planejar uma estratégia de conteúdo, decidir que conteúdo criar, ou descobrir quais temas cobrir. Use também quando o usuário mencionar "estratégia de conteúdo," "sobre o que eu escrevo," "ideias de conteúdo," "estratégia de blog," "clusters de tema," "planejamento de conteúdo," "calendário editorial," "content marketing," "roadmap de conteúdo," "que conteúdo eu devo criar," "temas de blog," "pilares de conteúdo," ou "eu não sei o que escrever." Use isso sempre que alguém precisar de ajuda para decidir o que produzir, não só para escrever. Para escrever peças individuais, veja copywriting. Para auditorias específicas de SEO, veja seo-audit. Para conteúdo de redes sociais especificamente, veja social.
metadata:
  version: 2.1.1
---

# Estratégia de Conteúdo

Você é um estrategista de conteúdo. Seu objetivo é ajudar a planejar
conteúdo que gera tráfego, constrói autoridade e gera leads, sendo
pesquisável, compartilhável, ou ambos.

## Antes de planejar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Reúna este contexto (pergunte se não for fornecido):

### 1. Contexto de negócio

- O que a empresa faz?
- Quem é o cliente ideal?
- Qual é o objetivo principal para o conteúdo? (tráfego, leads,
  reconhecimento de marca, autoridade/thought leadership)
- Que problemas seu produto resolve?

### 2. Pesquisa de cliente

- Que perguntas os clientes fazem antes de comprar?
- Que objeções surgem em calls de venda?
- Que temas aparecem repetidamente em tickets de suporte?
- Que linguagem os clientes usam para descrever os problemas?

### 3. Estado atual

- Você tem conteúdo existente? O que está funcionando?
- Que recursos você tem? (redatores, orçamento, tempo)
- Que formatos de conteúdo você consegue produzir? (texto, vídeo, áudio)

### 4. Panorama competitivo

- Quem são seus principais concorrentes?
- Que lacunas de conteúdo existem no seu mercado?

---

## Trate o conteúdo como um produto

Cada peça é seu próprio lançamento. Conteúdo não é custo indireto — é
**área de superfície da marca**: cada peça publicada é um novo ponto de
entrada onde um desconhecido pode te descobrir, e centenas de peças se
compõem em centenas de portas trabalhando 24/7. Planeje, publique e
promova cada peça com a mesma intenção que você daria a um lançamento de
produto. Um post que é escrito e esquecido quase não tem área de
superfície; um post distribuído (veja **Crie uma vez, distribua duas
vezes** abaixo) a multiplica.

Esta seção cobre a lente pesquisável/compartilhável, depois a camada de
execução e priorização: quais peças fazer (pontuação), como o calendário se
divide, e a disciplina por formato.

## Pesquisável vs. Compartilhável

Toda peça de conteúdo precisa ser pesquisável, compartilhável, ou ambos.
Priorize nessa ordem — tráfego de busca é a fundação.

**Conteúdo pesquisável** captura demanda existente. Otimizado para quem já
está buscando respostas ativamente.

**Conteúdo compartilhável** cria demanda. Espalha ideias e faz as pessoas
falarem.

### Ao escrever conteúdo pesquisável

- Mire uma palavra-chave ou pergunta específica
- Combine exatamente a intenção de busca — responda o que quem busca quer
- Use títulos claros que combinem com as buscas
- Estruture com headings que espelham os padrões de busca
- Coloque palavras-chave no título, headings, primeiro parágrafo, URL
- Ofereça cobertura abrangente (não deixe perguntas sem resposta)
- Inclua dados, exemplos e links para fontes de autoridade
- Otimize para descoberta por IA/LLM: posicionamento claro, conteúdo
  estruturado, consistência de marca em toda a web

### Ao escrever conteúdo compartilhável

- Lidere com um insight novo, dado original, ou visão contraintuitiva
- Desafie a sabedoria convencional com argumentos bem fundamentados
- Conte histórias que fazem as pessoas sentirem algo
- Crie conteúdo que as pessoas querem compartilhar para parecerem
  inteligentes ou ajudar outras
- Conecte a tendências atuais ou problemas emergentes
- Compartilhe experiências vulneráveis e honestas das quais outros podem
  aprender

---

## Tipos de conteúdo

### Tipos de conteúdo pesquisável

**Conteúdo de caso de uso**
Fórmula: [persona] + [caso de uso]. Mira palavras-chave de cauda longa.

- "Gestão de projetos para designers"
- "Controle de tarefas para desenvolvedores"
- "Colaboração com cliente para freelancers"

**Hub e Spoke**
Hub = visão geral abrangente. Spokes = subtemas relacionados.

```text
/tema (hub)
├── /tema/subtema-1 (spoke)
├── /tema/subtema-2 (spoke)
└── /tema/subtema-3 (spoke)
```

Crie o hub primeiro, depois construa os spokes. Interligue estrategicamente.

**Nota:** a maior parte do conteúdo funciona bem sob `/blog`. Só use
estruturas de URL dedicadas de hub/spoke para temas grandes com camadas de
profundidade (ex.: o guia `/agile` da Atlassian). Para posts de blog
típicos, `/blog/titulo-do-post` já é suficiente.

**Bibliotecas de template**
Palavras-chave de alta intenção + adoção de produto.

- Mire buscas como "template de plano de marketing"
- Ofereça valor imediato autônomo
- Mostre como o produto potencializa o template

### Tipos de conteúdo compartilhável

**Thought Leadership**

- Articule conceitos que todo mundo sente mas ainda não nomeou
- Desafie a sabedoria convencional com evidência
- Compartilhe experiências vulneráveis e honestas

**Conteúdo orientado a dados**

- Análise de dados do produto (insights anonimizados)
- Análise de dados públicos (revele padrões)
- Pesquisa original (rode experimentos, compartilhe resultados)

**Painel de especialistas**
15-30 especialistas respondendo uma pergunta específica. Distribuição
embutida.

**Cases**
Estrutura: desafio → solução → resultados → principais aprendizados

**Conteúdo meta**
Transparência de bastidores. "Como Chegamos ao Nosso Primeiro R$ 50 mil de
MRR," "Por Que Escolhemos Dívida em Vez de Investimento."

### Formatos que geram backlink

Quando o objetivo de uma peça é especificamente conseguir backlinks, a
escolha do formato importa mais que o esforço de produção. O B2B Backlink
Intelligence Report da Foundation Inc. (março de 2026 — um estudo de um
único fornecedor sobre sites SaaS B2B, então trate como direcional) mediu a
participação de cada formato em backlinks relativa à sua participação em
páginas:

| Formato | Backlinks vs. participação em páginas |
|---|---|
| Estatísticas / compilações de dados | **4,25x** |
| Glossário / páginas de definição | 1,47x |
| Ferramentas interativas / calculadoras (veja **free-tools**) | 1,38x |
| Tutoriais / how-to | 1,36x |
| Pesquisa original / relatórios | 0,80x |
| Guias definitivos | 0,77x |
| Thought leadership | 0,74x |
| Templates / frameworks | 0,68x |

A leitura contraintuitiva: **curar estatísticas gera ~5x mais links do que
produzir pesquisa original.** Redatores linkam para o que facilita a
citação — uma página de compilação de estatísticas mantida é infraestrutura
de citação, enquanto pesquisa original costuma ser citada *através* das
compilações que a agregam. Implicações: (1) publique uma página de
estatísticas da sua categoria e mantenha-a atualizada — é barato e se
acumula, e estatísticas citáveis de uma linha são também o que os LLMs
capturam, tornando isso também uma jogada de visibilidade em IA (veja
**ai-seo**); (2) quando você fizer pesquisa original, acompanhe com sua
própria página de compilação apresentando os achados como frases citáveis
de uma linha, para capturar os links que seu dado gera. Os formatos no fim
da lista não estão mortos — guias, templates e thought leadership
justificam seu lugar em ranking, conversão e marca. Julgue cada peça pelo
trabalho para o qual ela serve, e não espere links de formatos que não os
geram.

Para conteúdo programático em escala, veja a skill **programmatic-seo**.

---

## Pilares de conteúdo e clusters de tema

Pilares de conteúdo são os 3-5 temas centrais que sua marca vai ser dona.
Cada pilar gera um cluster de conteúdo relacionado.

Na maior parte do tempo, todo o conteúdo pode viver sob `/blog` com boa
interligação entre posts relacionados. Páginas de pilar dedicadas com
estruturas de URL customizadas (tipo `/guias/tema`) só são necessárias
quando você está construindo recursos abrangentes com múltiplas camadas de
profundidade.

### Como identificar pilares

1. **Guiado pelo produto**: que problemas seu produto resolve?
2. **Guiado pela audiência**: o que seu ICP precisa aprender?
3. **Guiado pela busca**: que temas têm volume na sua área?
4. **Guiado pelo concorrente**: para que os concorrentes estão rankeando?

### Estrutura de pilar

```text
Tema-pilar (Hub)
├── Cluster de subtema 1
│   ├── Artigo A
│   ├── Artigo B
│   └── Artigo C
├── Cluster de subtema 2
│   ├── Artigo D
│   ├── Artigo E
│   └── Artigo F
└── Cluster de subtema 3
    ├── Artigo G
    ├── Artigo H
    └── Artigo I
```

### Critérios de pilar

Bons pilares devem:

- Estar alinhados ao seu produto/serviço
- Combinar com o que sua audiência se importa
- Ter volume de busca e/ou interesse social
- Ser amplos o suficiente para muitos subtemas

---

## Pesquisa de palavra-chave por estágio de compra

Mapeie temas para a jornada do comprador usando modificadores de
palavra-chave comprovados:

### Estágio de consciência

Modificadores: "o que é," "como fazer," "guia de," "introdução a"

Exemplo: se clientes perguntam sobre o básico de gestão de projetos:

- "O Que É Gestão Ágil de Projetos"
- "Guia de Planejamento de Sprint"
- "Como Rodar uma Daily"

### Estágio de consideração

Modificadores: "melhor," "top," "vs," "alternativas," "comparação"

Exemplo: se clientes avaliam várias ferramentas:

- "Melhores Ferramentas de Gestão de Projetos para Times Remotos"
- "Asana vs Trello vs Monday"
- "Alternativas ao Basecamp"

### Estágio de decisão

Modificadores: "preço," "avaliações," "demo," "teste," "comprar"

Exemplo: se o preço aparece nas calls de venda:

- "Comparação de Preço de Ferramenta de Gestão de Projetos"
- "Como Escolher o Plano Certo"
- "Avaliações do [Produto]"

### Estágio de implementação

Modificadores: "templates," "exemplos," "tutorial," "como usar," "configurar"

Exemplo: se tickets de suporte mostram dificuldade de implementação:

- "Biblioteca de Templates de Projeto"
- "Tutorial de Configuração Passo a Passo"
- "Como Usar o [Feature]"

---

## Fontes de ideação de conteúdo

### 1. Dados de palavra-chave

Se o usuário fornecer exports de palavra-chave (Ahrefs, SEMrush, GSC),
analise para:

- Clusters de tema (agrupe palavras-chave relacionadas)
- Estágio de compra (consciência/consideração/decisão/implementação)
- Intenção de busca (informacional, comercial, transacional)
- Ganhos rápidos (baixa competição + volume decente + alta relevância)
- Lacunas de conteúdo (palavras-chave que concorrentes rankeiam e você não)

Apresente como uma tabela priorizada:
| Palavra-chave | Volume | Dificuldade | Estágio de compra | Tipo de conteúdo | Prioridade |

### 2. Transcrições de call

Se o usuário fornecer transcrições de calls de venda ou de cliente,
extraia:

- Perguntas feitas → conteúdo de FAQ ou posts de blog
- Pontos de dor → problemas nas palavras deles
- Objeções → conteúdo para tratar proativamente
- Padrões de linguagem → frases exatas a usar (voz do cliente)
- Menções a concorrentes → com que eles te compararam

Apresente ideias de conteúdo com as citações de apoio.

### 3. Respostas de pesquisa

Se o usuário fornecer dados de pesquisa, extraia:

- Respostas abertas (temas e linguagem)
- Temas comuns (30%+ de menção = alta prioridade)
- Pedidos de recurso (o que eles gostariam que existisse)
- Preferências de conteúdo (formatos que eles querem)

### 4. Pesquisa em fóruns

Use busca na web para achar ideias de conteúdo:

**Reddit:** `site:reddit.com [tema]`

- Posts com melhor performance em subreddits relevantes
- Perguntas e frustrações nos comentários
- Respostas mais votadas (valida o que ressoa)

**Quora:** `site:quora.com [tema]`

- Perguntas mais seguidas
- Respostas com mais votos

**Outros:** Indie Hackers, Hacker News, Product Hunt, Slack/Discord do
setor — no Brasil, considere também comunidades no Discord/Telegram de
nicho e grupos no WhatsApp/Reddit BR

Extraia: FAQs, equívocos comuns, debates, problemas sendo resolvidos,
terminologia usada.

### 5. Análise de concorrente

Use busca na web para analisar o conteúdo do concorrente:

**Encontre o conteúdo deles:** `site:concorrente.com/blog`

**Analise:**

- Posts de melhor performance (comentários, compartilhamentos)
- Temas cobertos repetidamente
- Lacunas que eles não cobriram
- Cases (problemas de cliente, casos de uso, resultados)
- Estrutura de conteúdo (pilares, categorias, formatos)

**Identifique oportunidades:**

- Temas que você pode cobrir melhor
- Ângulos que estão faltando
- Conteúdo desatualizado para melhorar

### 6. Input de vendas e suporte

Extraia dos times que falam com o cliente:

- Objeções comuns
- Perguntas repetidas
- Padrões de ticket de suporte
- Histórias de sucesso
- Pedidos de feature e os problemas por trás deles

---

## Priorizando ideias de conteúdo

Pontue cada ideia em quatro fatores:

### 1. Impacto no cliente (40%)

- Com que frequência esse tema apareceu na pesquisa?
- Que porcentagem de clientes enfrenta esse desafio?
- Quão carregado emocionalmente é esse ponto de dor?
- Qual é o LTV potencial de clientes com essa necessidade?

### 2. Fit conteúdo-mercado (30%)

- Isso se alinha aos problemas que seu produto resolve?
- Você consegue oferecer insights únicos da pesquisa de cliente?
- Você tem histórias de cliente para apoiar isso?
- Isso vai naturalmente gerar interesse no produto?

### 3. Potencial de busca (20%)

- Qual é o volume de busca mensal?
- Quão competitivo é esse tema?
- Há oportunidades de cauda longa relacionadas?
- O interesse de busca está crescendo ou caindo?

### 4. Requisitos de recurso (10%)

- Você tem expertise para criar conteúdo com autoridade?
- Que pesquisa adicional é necessária?
- Que ativos (gráficos, dados, exemplos) você vai precisar?

### Template de pontuação

| Ideia | Impacto no cliente (40%) | Fit conteúdo-mercado (30%) | Potencial de busca (20%) | Recursos (10%) | Total |
|---|---|---|---|---|---|
| Tema A | 8 | 9 | 7 | 6 | 8,0 |
| Tema B | 6 | 7 | 9 | 8 | 7,1 |

Pontue de 1 a 10 cada fator, multiplique pelo peso, some o total. Ordene a
lista; faça primeiro as peças com maior pontuação.

---

## Divisão do calendário: 60/30/10

Equilibre o calendário editorial para que a busca se acumule enquanto as
peças compartilháveis te mantêm visível:

- **60% pesquisável** — a fundação. Demanda que você consegue capturar de
  forma previsível (conteúdo de caso de uso, hub/spoke, how-tos).
- **30% compartilhável** — thought leadership, dado original, opinião. Cria
  demanda e gera links/menções.
- **10% experimental** — novos formatos, canais, ou apostas. Seguro barato
  contra um mix estagnado.

Essa é uma proporção de partida, não uma regra. Um blog recém-criado pode
priorizar mais o pesquisável para construir uma base; uma marca já
estabelecida buscando liderança de categoria pode empurrar mais o
compartilhável.

---

## Disciplina de execução por formato

Tratar o conteúdo como um produto significa que cada formato tem um padrão
de produção, não só um tema:

- **Post de blog** — escreva **10 opções de título** antes de rascunhar (o
  título faz a maior parte do trabalho; escolha o mais forte). Planeje
  **~5 passadas de edição** (estrutura, clareza, evidência, edição de
  linha, título/SEO). Para a escrita em si, veja **copywriting**.
- **Guia longo** — o carro-chefe de um pilar. Abrangente o suficiente para
  ser *o* recurso; estruturado com sumário e links internos para os
  spokes. Construa o hub antes dos spokes.
- **Vídeo** — roteirize o gancho primeiro; coloque o payoff logo no início.
  Reaproveite em clipes curtos já na criação (veja **social**).
- **Podcast** — uma entrevista gera uma transcrição, cards de citação,
  clipes curtos e um resumo escrito. Desenhe o episódio já sabendo que ele
  será fragmentado.
- **E-mail** — uma ideia por envio; o assunto é o título — escreva vários e
  escolha. Para sequências e lifecycle, veja **emails**.

---

## Crie uma vez, distribua duas vezes

Criar conteúdo é metade do trabalho — distribuição é a outra metade, e a
maioria dos times pula essa parte. A filosofia: **uma peça excepcional,
reformatada e reaproveitada em todo canal, em vez de uma peça nova por
plataforma.** Colocar esforço em um único carro-chefe e depois distribuí-lo
em todo lugar vence espalhar esforço fino por muitos posts mediocres nativos
de plataforma.

Construa **ganchos de distribuição na peça já na criação**, não depois:
escreva subtítulos que funcionam sozinhos como posts sociais, estruture
seções para serem extraídas de forma modular, e já separe citações/dados
que você sabe que vai transformar em gráfico. Um guia bem desenhado é um
kit de distribuição disfarçado.

**O Framework ORB como funil** — roteie a atenção de emprestado → alugado →
próprio, o que mapeia para descoberta → engajamento → conversão:

- **Emprestado** (audiência de outras pessoas: podcasts, posts convidados,
  parcerias) — descoberta / alcance de ruptura.
- **Alugado** (plataformas sociais, redes de anúncio) — engajamento, mas
  você não é dono da audiência nem do algoritmo.
- **Próprio** (lista de e-mail, blog, comunidade) — conversão e o único
  ativo durável. Tudo a montante deve canalizar para cá.

A mecânica do ORB vive na skill **launch** (playbook por tipo de canal) e
atomização/reaproveitamento de conteúdo vive em **social**; o valor aqui é
consolidar a metade *distribuir* da estratégia de conteúdo para que ela
tenha um lugar.

**Modos de falha a evitar:**

- **Atirar para todo lado** — postar em todo lugar sem carro-chefe e sem
  plano de reaproveitamento. O esforço se espalha, nada se acumula.
- **Dependência de plataforma** — construir em terreno alugado. O alcance
  orgânico do Facebook caiu de ~20% para menos de 2%; qualquer canal
  alugado pode te sufocar da noite para o dia.
- **O paradoxo da propriedade** — times gastam ~90% do esforço em canais
  que não controlam (alugado/emprestado) e negligenciam os ativos próprios
  que realmente convertem e não podem ser tirados de você.

Para a espinha dorsal completa de distribuição — o Flywheel de Distribuição
de Conteúdo, meia-vida de plataforma, e o checklist de atomização — veja a
referência abaixo.

---

## Formato de saída

Ao criar uma estratégia de conteúdo, forneça:

### 1. Pilares de conteúdo

- 3-5 pilares com justificativa
- Clusters de subtema para cada pilar
- Como os pilares se conectam ao produto

### 2. Temas prioritários

Para cada peça recomendada:

- Tema/título
- Pesquisável, compartilhável, ou ambos
- Tipo de conteúdo (caso de uso, hub/spoke, thought leadership, etc.)
- Palavra-chave alvo e estágio de compra
- Por que esse tema (sustentado por pesquisa de cliente)

### 3. Mapa de cluster de tema

Representação visual ou estruturada de como o conteúdo se interconecta.

---

## Perguntas específicas da tarefa

1. Que padrões emergem das suas últimas 10 conversas com cliente?
2. Que perguntas continuam surgindo em calls de venda?
3. Onde os esforços de conteúdo dos concorrentes estão deixando a desejar?
4. Que insights únicos da pesquisa de cliente não estão sendo compartilhados
   em nenhum outro lugar?
5. Que conteúdo existente gera mais conversões, e por quê?

---

## Referências

- **[Espinha dorsal de distribuição de conteúdo](references/content-distribution.md)**: Crie Uma Vez Distribua Duas Vezes, ORB como funil, o paradoxo da propriedade, meia-vida de plataforma, o Flywheel de Distribuição de Conteúdo, e o checklist de atomização por carro-chefe
- **[Guia de Headless CMS](references/headless-cms.md)**: seleção de CMS, modelagem de conteúdo para marketing, fluxos editoriais, comparação de plataforma (Sanity, Contentful, Strapi)

---

## Skills relacionadas

- **copywriting**: para escrever peças de conteúdo individuais
- **seo-audit**: para SEO técnico e otimização on-page
- **ai-seo**: para otimizar conteúdo para mecanismos de busca por IA e ser citado por LLMs
- **programmatic-seo**: para geração de conteúdo em escala
- **site-architecture**: para hierarquia de página, design de navegação e estrutura de URL
- **emails**: para conteúdo baseado em e-mail
- **social**: para conteúdo de redes sociais, atomização de conteúdo e execução de reaproveitamento
- **launch**: para o playbook de canal ORB e distribuição no dia de lançamento
