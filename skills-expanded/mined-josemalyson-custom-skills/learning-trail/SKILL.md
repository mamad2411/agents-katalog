---
name: learning-trail
description: Use esta skill SEMPRE que o usuário mencionar que deseja estudar, aprender, explorar, entender ou pedir uma trilha, aula ou roadmap sobre qualquer assunto, mesmo que não cite explicitamente "trilha de aprendizado". A skill cria um guia linear (coluna vertebral) suportado por recursos avaliados rigorosamente (nervos). O usuário pode escolher entre saída Markdown ou 4 templates HTML diferentes (completo, minimalista, timeline, feed mobile). Evite usá-la apenas para tarefas de código ou dúvidas pontuais, mas para qualquer jornada de aprendizado, acione-a imediatamente!
version: 3.1
---

# Learning Trail Generator

Bem-vindo à skill Learning Trail Generator. O seu objetivo aqui é ajudar o usuário a aprender um tema aprofundadamente. Para isso, você gerará um arquivo `.md` no padrão **spine + nerves** (espinha e nervos), no qual a maior força está em você validar e inspecionar cada recurso sugerido.

## Arquitetura de Confiança (Trust by Inspection)

A essência desta skill é construir confiança através da inspeção do conteúdo real, e não apenas por reputação ou intuição. Por isso:
- Nós não filtramos fontes usando whitelists estáticas. Qualquer fonte pode ser ótima se o conteúdo for bom.
- Inspecionamos ativamente cada candidato a recurso (lendo o texto, transcrições ou PDFs) antes de incluí-lo na trilha. 
- Cada recomendação é incluída apenas se puder ser validada como cobrindo o tema específico exigido, com o nível de profundidade correto.
- Isso evita que o usuário receba links quebrados ou desatualizados, garantindo uma trilha sólida.

A reputação da fonte serve apenas como desempate, mas o conteúdo vem em primeiro lugar.

## O Modelo Mental

Pense na trilha como um jogo de tabuleiro:
- **Tabuleiro:** O mapa da trilha, apresentado antes de começar.
- **Casas (Estações):** A espinha dorsal do conhecimento (idealmente de 4 a 10 estações breves, ~5-10 min de leitura cada).
- **Caminhos Laterais (Nervos):** Recursos validados para aprofundamento.
- **Desafio Final:** Perguntas socráticas para auto-avaliação (sem gabaritos!).

## Como conduzir a sessão (Workflow)

Siga estas fases passo a passo.

### Fase 1 — Captura e Clarificação (Perguntas Iterativas)

Ao receber a solicitação de aprendizado, identifique o idioma do usuário.
Antes de começar a pesquisa, **faça perguntas iterativas até entender totalmente o que o usuário deseja**. As perguntas devem cobrir:

1. **Plano:** Ele prefere que você monte o plano automaticamente ou quer customizar (tamanho, foco teórico vs prático)?
2. **Materiais:** Ele possui algum link, PDF ou material específico que gostaria de incluir na trilha?
3. **Nível:** Qual o nível de profundidade desejado? (iniciante, intermediário, avançado)
4. **Foco:** Prefere uma trilha mais teórica (conceitos, papers), prática (ferramentas, código) ou balanceada?
5. **Extensão:** Quantas estações (tópicos) ele idealiza? (curta: 3-4, média: 5-7, longa: 8-10)

**Importante:** Não pergunte tudo de uma vez. Vá em sequência, adaptando as perguntas com base nas respostas anteriores. O objetivo é extrair o máximo de contexto ANTES de começar a pesquisar.

### Fase 2 — Busca Exploratória

Realize uma busca ampla pelo assunto para entender o contexto geral e encontrar os melhores candidatos a materiais. 
- Procure os conceitos fundamentais, pré-requisitos e tópicos mais avançados para montar a ordem da trilha (a espinha).
- Colete vários candidatos de leitura e vídeo (papers, vídeos do YouTube, artigos, livros). Colete um número razoável (por exemplo, 6-8 de cada), pois alguns falharão na validação.

**Fontes prioritárias de busca:**

Direcione a busca exploratória para estes quatro tipos de fonte, sempre nesta ordem de prioridade quando o tema permitir:

1. **YouTube** — palestras, aulas e talks de canais técnicos e conference talks (ex: conferências da área, canais de universidades, canais de profissionais reconhecidos). Priorize vídeos com transcrição disponível para validação na Fase 4.
2. **Artigos científicos / papers** — arXiv, ACM, IEEE, journals da área, papers seminais e surveys recentes. Para temas de GenAI/ML, priorize papers com citações relevantes e/ou de labs reconhecidos.
3. **Blogs de especialistas** — apenas blogs de autoria de profissionais/pesquisadores com histórico comprovado na área (ex: engenheiros de empresas referência no tema, pesquisadores publicados, mantenedores de projetos open source relevantes). Evite agregadores genéricos, listicles ou blogs sem autoria identificável — a autoridade do autor é parte do critério de inclusão, não só o conteúdo.
4. **X (Twitter)** — threads técnicas e posts de especialistas reconhecidos na área (pesquisadores, engenheiros de referência, contas oficiais de projetos/labs). Use apenas quando a thread tiver profundidade técnica real (não notícia rasa ou hype); trate como material complementar, não como espinha principal da trilha.

Isso não substitui outras fontes de qualidade (livros, documentação oficial) quando forem os melhores candidatos — é uma priorização de busca, não uma whitelist exclusiva (mantém-se o princípio de "conteúdo vem em primeiro lugar" da seção de Arquitetura de Confiança).

### Fase 3 — Desenho da Espinha (Estações)

Determine a sequência lógica do aprendizado. 
Se for uma ferramenta prática, talvez 4-5 estações sejam suficientes. Se for um conceito complexo, 7-10. Mais que 10 pode ser exaustivo; sugira quebrar em sub-trilhas.
Cada estação precisa de uma narrativa: introduza o problema, desenvolva a ideia, mostre limitações e conclua.

### Fase 4 — Validação Atômica de Recursos (O Coração da Skill)

Esta é a etapa mais crítica. Para que a trilha seja incrivelmente útil, precisamos ter certeza de que o que recomendamos é excelente. 

Para cada tópico a ser aprofundado (slot de nervo):
1. **Busque o conteúdo:** Use ferramentas de fetch para ler a URL do artigo/paper ou obter a transcrição de um vídeo.
2. **Avalie o conteúdo:** Ele cobre especificamente o subtópico da estação? A profundidade está adequada para o nível da trilha? É atual (especialmente em tecnologia)? 
3. **Avalie a autoridade do autor (para blogs e X):** Quando o recurso for um blog post ou uma thread/post do X, confirme quem é o autor e qual sua credencial na área (pesquisador publicado, engenheiro de empresa referência, mantenedor de projeto relevante etc.). Se não for possível identificar um autor com autoridade comprovada no tema, descarte o recurso — mesmo que o conteúdo pareça bom.
4. Se a resposta for "sim" para todos, o recurso é aprovado.
5. **Extraia a prova:** Separe 1 ou 2 frases do próprio conteúdo que evidenciam a relevância dele para o subtópico. Isso será exibido na trilha para dar contexto ao usuário.
6. Seja resiliente. Tente validar vários materiais até ter algumas boas opções por estação (em média 1 a 3 recursos por estação).

**Dica para uso de Sub-agentes:**
Se o seu ambiente suportar agentes paralelos (como Claude Code usando a tool de Task), você pode gerar sub-agentes para lerem e avaliarem os recursos paralelamente, o que acelera bastante o processo. Peça a eles para retornarem o veredicto (aprovado/reprovado) e o trecho de evidência (excerpt).

### Fase 5 — Escolha do Formato de Saída

Com a espinha montada e os nervos validados, **apresente ao usuário as opções de formato de saída** e peça que ele escolha:

**Opção A — Markdown (`.md`)**
- Arquivo leve, portátil, editável em qualquer editor.
- Template: `assets/trail_template.md`

**Opção B — HTML Web Aprimorado (`TEMPLATE.html` / `TEMPLATE_ENHANCED.html`) — recomendado**
- Experiência reading-first baseada no `DESIGN.md`: sidebar, sumário contextual, progresso persistente, busca, dark mode e impressão.
- Usa progressive enhancement: Inter + Geist Mono, Mermaid, Shiki e KaTeX são carregados sob demanda, sempre com fallback local.
- Ideal para publicação web, trilhas técnicas extensas, diagramas, código e conteúdo matemático.

**Opção C — HTML Offline Autocontido (`TEMPLATE_OFFLINE.html`)**
- Mesma arquitetura visual, navegação e contrato de placeholders da versão Enhanced, sem qualquer dependência externa.
- Ideal para download, abertura local, LMS restrito, impressão, arquivamento e ambientes sem rede.

**Opção D — HTML Minimalista para Leitura (`TEMPLATE_MINIMAL.html`)**
- Design limpo, tipografia serifada para leitura focada, dark mode automático.
- Ideal para impressão ou leitura prolongada.

**Opção E — HTML Linha do Tempo (`TEMPLATE_TIMELINE.html`)**
- Visual em timeline vertical, cards de nervos em grid, dark mode automático.
- Ideal para progressão visual do aprendizado.

**Opção F — HTML Feed Mobile-First (`TEMPLATE_FEED.html`)**
- Estilo feed de rede social, navegação inferior, otimizado para celular.
- Ideal para consumo em dispositivos móveis.

**IMPORTANTE:** Apresente todas as 6 opções com uma breve descrição de cada (como acima) e aguarde a escolha.

### Fase 6 — Geração do Arquivo

Com o formato escolhido pelo usuário:

- Se **Markdown**: gere `./trilhas/{slug}.md` usando `assets/trail_template.md` como referência estrutural.
- Se **HTML**: preencha o template escolhido (`TEMPLATE.html`, `TEMPLATE_ENHANCED.html`, `TEMPLATE_OFFLINE.html`, `TEMPLATE_MINIMAL.html`, `TEMPLATE_TIMELINE.html` ou `TEMPLATE_FEED.html`) com todo o conteúdo da trilha (estações, nervos, checks, boss final, recursos adicionais, auditoria) e salve em `./trilhas/{slug}.html`.

Certifique-se de substituir **todos** os placeholders `{...}` do template pelos valores reais da trilha.

### Fase 7 — Fechamento

Avise ao usuário que a trilha foi gerada e forneça estatísticas curtas: número de estações, de nervos validados, estimativa de leitura e o formato escolhido.
Pergunte se ele deseja gerar em outro formato também, ou se está satisfeito.
Deixe o usuário guiar os próximos passos, sugerindo se ele gostaria de conversar mais, criar um projeto prático para fixar ou avançar para um próximo tema, mas não imponha as etapas automaticamente.

## Pontos Importantes para a Interação

- Procure não gerar conceitos inteiros "de cabeça"; busque validação, para garantir que as informações são frescas e exatas.
- Se o usuário não gostar de alguma seção, adapte-a iterativamente.
- Faça o processo ser transparente: mostre brevemente ao usuário quando você estiver descartando um link por ele ser inadequado, pois isso demonstra o valor da curadoria que você está fazendo.
