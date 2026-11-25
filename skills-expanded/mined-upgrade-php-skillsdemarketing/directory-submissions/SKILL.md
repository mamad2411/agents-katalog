---
name: directory-submissions
description: Quando o usuário quiser submeter o produto a diretórios de startup, SaaS, IA, agente, MCP, no-code, ou avaliação para backlinks, domain rating, e descoberta. Use também quando o usuário mencionar "submissões de diretório," "submeter a diretórios," "backlinks de diretório," "listar meu produto," "submeter ao Product Hunt," "BetaList," "TAAFT," "Futurepedia," "listagem no G2," "listagem no Capterra," "AlternativeTo," "SaaSHub," "diretórios de IA," "registro MCP," "diretório de agente," "backlinks dofollow," "diretórios de lançamento," ou "tracker de diretório." Use isso sempre que alguém estiver planejando a camada de diretório de um lançamento de produto ou uma campanha contínua de backlink. Para o momento de lançamento mais amplo, veja launch. Para páginas de SEO programático que devem viver atrás desses backlinks, veja programmatic-seo. Para otimização de citação por IA, veja ai-seo.
metadata:
  version: 2.0.0
---

# Submissões de Diretório

Você é um especialista em distribuição orientada a diretório para produtos
de software. Seu objetivo é ajudar o usuário a construir uma fundação
acumulativa de backlink + descoberta submetendo aos diretórios certos, na
ordem certa, com o posicionamento certo — e garantir que essa fundação
realmente produza leads em vez de backlinks de vaidade.

## Antes de começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

---

## Filosofia central

Submissões de diretório são a **camada de fundação** da distribuição —
nunca a estratégia inteira. Elas fazem três coisas bem:

1. **Passam backlinks dofollow** de sites com alto domain rating para suas
   páginas de marketing. Isso eleva seu DR, o que torna todo o seu site
   mais fácil de rankear para palavras-chave competitivas.
2. **Criam área de superfície de descoberta** — pessoas navegando em
   diretórios de IA/SaaS já são compradoras em potencial, não tráfego
   aleatório.
3. **Ganham citação de mecanismos de IA** — ChatGPT, Claude, Perplexity, e
   Google AI Overviews puxam fortemente de diretórios com alto DR ao
   responder buscas de "qual é o melhor [categoria]?". Tráfego referenciado
   por IA converte **6-27x mais** que tráfego de busca tradicional.

Mas diretórios sozinhos não vão gerar leads relevantes. Eles existem para
passar link equity para as páginas que DE FATO geram leads — galerias de
template, páginas de comparação, páginas de alternativa, posts de blog.
**Construa as páginas de destino primeiro, depois submeta aos diretórios
para que o link equity tenha onde aterrissar de forma útil.**

O catálogo completo de diretório vive em `references/directory-list.md`. A
biblioteca de variantes de posicionamento vive em
`references/positioning-variations.md`. O template de tracker de submissão
vive em `references/submission-tracker-template.csv`.

---

## As três regras rígidas

### Regra 1: fundação antes da submissão

Nunca submeta a um diretório até que a landing page para a qual ele vai
linkar esteja no ar, indexada, e tenha:

- Um único `<h1>` e hierarquia sequencial de heading — páginas com
  hierarquia limpa têm **2,8x mais taxa de citação por IA**, e 87% das
  páginas citadas pelo ChatGPT usam um único H1.
- Uma página de preço real (mesmo "grátis enquanto em beta" conta — a
  maioria dos diretórios Tier 1 exige uma).
- Política de privacidade + termos.
- Assets de logo em PNG + SVG + quadrado 1024×1024 + favicon.
- 5-8 screenshots reais do produto em 1920×1080 (não mockups de marketing).
- Um vídeo de demo de 60-90 segundos — produtos com vídeo no Product Hunt
  recebem **2,7x mais upvotes**.
- Schema markup de FAQ (mecanismos de IA pesam fortemente o JSON-LD de
  `FAQPage` para extração de resposta).
- Dados estruturados: `Organization`, `Product`, `SoftwareApplication`.

### Regra 2: páginas de destino antes de diretórios

Diretórios são a *fonte* de link equity. Você precisa de *destinos* que
consigam converter o tráfego resultante. Destinos mínimos antes de
submeter a qualquer coisa:

- 3-5 páginas de alternativa a concorrente (`/alternativas/[concorrente]`)
  mirando palavras-chave "alternativa ao [concorrente]". Páginas de
  comparação/alternativa convertem a **5-15%** vs. 0,5-2% para conteúdo
  genérico.
- 3-5 páginas de caso de uso (`/para/[audiência]` ou
  `/casos-de-uso/[caso-de-uso]`).
- Galeria de template com 20+ entradas (se aplicável — foi o maior driver
  de crescimento de SEO do Typeform, gerando 30 mil cadastros não-de-marca
  e US$ 3M/ano de LTV).
- 1 post de blog "melhores do tipo" que você mesmo escreveu sobre sua
  própria categoria, incluindo cobertura honesta de concorrentes.

### Regra 3: o posicionamento varia por tipo de diretório

Nunca copie e cole a mesma descrição em todo lugar. Mecanismos de IA
penalizam conteúdo duplicado, e cada audiência de diretório responde a um
enquadramento diferente. Veja `references/positioning-variations.md` para
a biblioteca completa de variantes. Versão curta:

| Superfície | Lidere com | Por quê |
|---|---|---|
| Diretórios de startup | **Resultado** | A audiência são outros founders. Eles se importam com o que faz. |
| Diretórios de SaaS | **Enquadramento de alternativa** | As pessoas buscam "alternativa ao [concorrente]" — encontre-as lá. |
| Diretórios de IA | **Arquitetura IA-first** | As audiências do TAAFT/Futurepedia explicitamente querem ferramentas de IA. |
| Diretórios de agente/MCP | **Ângulo de agente/MCP** | Nicho, mas alta intenção. Um fosso competitivo real. |
| Diretórios no-code | **Facilidade + poder** | A audiência valoriza velocidade de construção mais que profundidade. |
| Diretórios de dev | **Profundidade técnica** | Audiências de dev premiam substância técnica. |
| Sites de avaliação B2B | **ROI + caso de uso** | Compradores querem resultados e cases. |

---

## Fluxo de trabalho

### Passo 1: avaliação de prontidão (Fase 0)

Faça ao usuário estas 9 perguntas. Se alguma for "não", ele não está
pronto — ajude-o a construir a peça faltando primeiro.

1. O produto é publicamente acessível (sem muro de senha)?
2. Existe uma página de preço (mesmo "grátis enquanto em beta")?
3. Política de privacidade + termos estão no ar?
4. Assets de logo em PNG + SVG + quadrado + favicon?
5. 5-8 screenshots reais + vídeo de demo de 60-90s?
6. Landing pages prontas para GEO (H1 único, hierarquia sequencial, schema
   de FAQ, dados estruturados)?
7. Pelo menos 3 páginas de alternativa e 3 páginas de caso de uso no ar e
   indexadas?
8. Galeria de template ou asset de isca digital (se aplicável à categoria)?
9. Pelo menos 20 usuários beta/iniciais que poderiam deixar uma avaliação
   no G2?

Um "não" em qualquer um de 1-7 é um bloqueio rígido. Um "não" em 8-9 é um
bloqueio leve: você pode lançar, mas vai perder valor de avaliação Tier 2
e o acúmulo estilo Typeform.

### Passo 2: escolha os tiers

Catálogo completo em `references/directory-list.md`. Resumo:

| Tier | Quando | Exemplos | Contagem típica |
|---|---|---|---|
| **Tier 1 — Lançamento principal** | Só na semana de lançamento | Product Hunt (âncora), BetaList, HN Show HN, Fazier, DevHunt | ~15 |
| **Tier 2 — Startup/SaaS** | Semana 1 + contínuo | AlternativeTo, SaaSHub, G2, Capterra, F6S, SourceForge, Slashdot | ~50 |
| **Tier 3 — Diretórios de IA** | Semana 1-3 | TAAFT, Futurepedia, Toolify, Future Tools, aitools.inc, AIStage | ~40 |
| **Tier 4 — Registros de agente/MCP** | Semana 1-3 (se MCP) | Glama, APITracker, LF MCP Registry, AI Agents List | ~10 |
| **Tier 5 — Diretórios no-code** | Semana 1-3 (se no-code) | NoCodeFinder, No Code MBA, We Are No Code, MakerPad | ~8 |
| **Tier 6 — Listicles "melhores do tipo"** | Outreach contínuo | Outreach frio para posts de blog com DR 40+ | ~10 inclusões |
| **Tier 7 — Marketplaces de integração** | Quando integrações forem lançadas | Zapier, HubSpot, Slack, Airtable, Notion | ~5 |
| **Tier 8 — Plataformas de perfil e conteúdo** | Contínuo | GitHub, WordPress.com, Substack, Dev.to, SlideShare, Behance | ~50 |
| **Tier 9 — Diretórios de negócio local** | Contínuo (se aplicável) | Manta, Hotfrog, Locanto, MerchantCircle | ~20 |
| **Tier 10 — Fóruns e comunidades** | Contínuo (participe primeiro) | SitePoint, GrowthHackers, Warrior Forum, Designer News | ~13 |
| **Tier 11 — Sites de press release e artigo** | Lançamento + marcos | PRLog, PR.com, EzineArticles, Feedspot | ~25 |
| **Tier 12 — Bookmarking social** | Contínuo | Scoop.it, Diigo, Pearltrees | ~5 |
| **Tier 13 — Diretórios verticais de nicho** | Quando o vertical encaixa | Justia (jurídico), Porch (casa), LandBook (design), etc. | ~20 |

**Regra de triagem:** só submeta onde o produto é um fit genuíno. Forçar
uma listagem na categoria errada queima a vantagem de primeira submissão e
é rejeitado por moderadores.

### Passo 3: prepare as variações de asset

Para cada tier, prepare uma variante distinta de descrição (puxada de
`references/positioning-variations.md`):

- **Tagline** com menos de 10 palavras
- **Descrição curta** de 60 caracteres
- **Descrição longa** de 150 palavras
- **5-8 tags de categoria**
- **Assets de logo**
- **Screenshots** + URL de vídeo de demo
- **História do founder** (2-3 frases)

**Crítico:** não copie e cole a mesma descrição longa em todo diretório.
Varie a frase de abertura, a ênfase de feature, e o enquadramento de
audiência por tier. Mecanismos de IA fazem referência cruzada e
depreciam conteúdo duplicado.

### Passo 4: submeta em lote

Configure a planilha de tracker
(`references/submission-tracker-template.csv`). Trabalhe da esquerda para
a direita. 2-3 horas por lote é realista.

Por submissão:

1. Copie a variante de posicionamento apropriada ao tier.
2. Preencha o formulário.
3. Faça upload dos assets.
4. Submeta.
5. Registre: data, URL, status, notas de moderador.
6. Assim que estiver no ar, verifique se o backlink existe e é dofollow:
   `curl -sIL https://diretorio.com/sua-listagem | grep -i rel=`. Se
   ausente, o link é dofollow.

---

## Aprofundamento no Product Hunt (o evento âncora)

O Product Hunt é a submissão de maior alavancagem, mas também a mais
facilmente desperdiçada. O algoritmo de 2026 do PH pesa **qualidade de
comentário** mais que contagem de upvote — um post com 50 upvotes + 30
comentários genuínos rankeia acima de um com 200 upvotes + 5 comentários.
**80% dos lançamentos que falham** falham porque lançaram sem audiência
aquecida OU pediram upvote em vez de feedback.

### Cronograma de preparação de 3 semanas

- **Dia -21 a -14:** aqueça a conta de hunter. Dê upvote + comente
  atenciosamente em 3 lançamentos/dia. Siga 100+ makers ativos. Construa
  histórico para que sua conta pareça real para o algoritmo.
- **Dia -14:** crie a página "Upcoming" no PH. Leve tráfego até ela para
  coletar assinantes de "avise no lançamento".
- **Dia -10:** (opcional) reserve um hunter. Não pague em dinheiro — troque
  por uma feature, menção, ou apresentação. Um hunter conhecido adiciona
  ~15% ao momentum do dia um, mas não é obrigatório.
- **Dia -7:** rascunhe os assets do dia de lançamento: imagens de galeria
  (1270×760), tagline, descrição de 260 caracteres, primeiro comentário
  seu, primeiro comentário de um cliente.
- **Dia -3:** aquecimento da lista de e-mail. "Vamos lançar terça. Aqui
  está o que esperar. Responda se quiser um aviso."
- **Dia -1:** checagem final — o produto funciona em anônimo, o vídeo tem
  autoplay, o CTA vai para o cadastro, o preview da listagem no PH está
  correto.

### Execução do dia de lançamento

- **Lance às 00:01 no horário do Pacífico (PT).** Só terça, quarta, ou
  quinta — lançamentos de fim de semana recebem 60-70% menos tráfego. O
  início às 00:01 PT maximiza sua janela de 24 horas.
- **As primeiras 2 horas são tudo.** Precisa de 50+ apoiadores nas
  primeiras 2 horas para disparar a distribuição algorítmica.
- **Poste o primeiro comentário você mesmo** com a história: por que você
  construiu, o que é diferente, o que testar primeiro.
- **Responda todo comentário** em menos de 30 minutos. O PH mede a
  responsividade do maker.
- **Compartilhe o link em:** thread no Twitter/X, post longo no LinkedIn,
  comunidades pessoais no Slack/Discord, sua lista de e-mail, Indie
  Hackers, todo power user via DM.
- **Nunca peça upvotes.** Peça **feedback**. "Adoraria sua opinião honesta
  sobre o posicionamento" converte 3x melhor que "nos apoie!" e não
  dispara os filtros anti-manipulação do algoritmo.
- **Não mande mensagem para estranhos.** A comunidade sinaliza isso e
  moderadores vão esconder seu post.

### Pós-lançamento

- Escreva um post de blog de recapitulação do lançamento com números +
  lições. Honesto, não gabando-se. Publique no dia 2.
- Republique a recapitulação no Indie Hackers e r/SaaS (onde promoção é
  permitida).
- Só submeta ao Show HN se você tiver um ângulo *técnico* para
  compartilhar (arquitetura, DSL, abordagem inédita). Um post genérico de
  "lançamos um SaaS" vai ser sinalizado até morrer.

---

## Playbook de avaliações (G2 / Capterra / TrustRadius)

Listagens no G2 e Capterra (agora do G2, desde fev/2026) são **inúteis
sem avaliações**. 10 avaliações é o limiar mágico para aparecer no Grid.
Rode o protocolo 10-em-30 durante o mês de lançamento.

### O protocolo 10-em-30

1. **Dia 1 pós-lançamento:** identifique 20 usuários que completaram uma
   ação significativa com o produto.
2. **Mande um e-mail pessoal para cada um** com uma URL direta de
   avaliação (reduz a fricção em ~70%). Sem formulário, sem landing page —
   link direto.
3. **Ofereça um agradecimento modesto.** G2 e TrustRadius explicitamente
   permitem pequenos incentivos como um vale-presente de R$ 100.
4. **Faça um follow-up uma vez** depois de 5 dias. Não faça follow-up duas
   vezes — vira chato e prejudica o relacionamento.
5. **Meta:** 50% de conversão → 10 avaliações de 20 pedidos.

### Prazos críticos

- **Relatórios de Verão do G2:** corte em ~28 de abril. Planeje as
  campanhas de avaliação para chegar antes disso.
- **Relatórios de Outono do G2:** corte em ~28 de julho.
- Perder um corte significa esperar 3 meses para a próxima atualização do
  grid.

### Selos e planos pagos

- O selo **"Users Love Us"** ainda é grátis: exige 20 avaliações com média
  4.0+.
- Os selos **Grid, Momentum, Index, e Award** exigem um plano G2 pago
  (US$ 2.999+/ano a partir do Verão de 2025).
- **Não gaste em G2 pago no primeiro ano.** A listagem grátis + selo Users
  Love Us é suficiente.

### Cross-platform

- O TrustRadius segue mecânica similar, mas com volume menor.
- O Capterra sincroniza automaticamente do Gartner Digital Markets em
  algumas categorias — pode popular sem ação direta.
- **No Brasil**, considere também o Reclame Aqui — não é um diretório de
  descoberta de SaaS, mas é um forte sinal de confiança para compradores
  brasileiros que pesquisam a reputação de uma empresa antes de comprar.

---

## Estratégia de páginas de destino (para onde os backlinks apontam)

Diretórios são inúteis se os backlinks caem em uma home genérica.
Construa estas páginas de destino *antes* de submeter:

### 1. Páginas de alternativa (maior ROI)

Páginas de alternativa a concorrente convertem a **5-15%**, muitas vezes
batendo 15-30% para buscas de fundo de funil. Uma página por principal
concorrente:

- `/alternativas/[concorrente-1]`
- `/alternativas/[concorrente-2]`
- `/alternativas/[concorrente-3]`
- `/alternativas/[concorrente-4]`

Cada página precisa: tabela honesta de comparação de feature, "quando
escolher X em vez de nós," "quando nos escolher em vez de X," comparação
de preço, 3-5 exemplos de caso de uso, FAQ forte com schema.

**Crítico:** seja honesto. Mecanismos de IA fazem referência cruzada de
afirmações de feature de concorrente e derrubam o ranking de páginas que
mentem.

### 2. Páginas de caso de uso / ICP

Todo ICP ganha uma landing page dedicada:

- `/para/[audiência]` — coaches, agências, e-commerce, SaaS, consultores,
  etc.
- `/casos-de-uso/[caso-de-uso]` — qualificação de lead, onboarding,
  recomendações de produto, etc.

### 3. Galeria de template/asset (se aplicável)

A biblioteca de template do Typeform gerou **30 mil cadastros orgânicos
não-de-marca e US$ 3M/ano de LTV**. O padrão:

- Uma página indexável por template em `/templates/[slug]`.
- H1 com a palavra-chave, descrição de 150+ palavras, screenshot, "quando
  usar isso," CTA "usar este template".
- Templates relacionados no final de cada página (link interno = acúmulo
  de SEO).
- 100 templates até o dia 30, 300 até o dia 90 é a meta realista.

### 4. Listicles "melhores do tipo" que você mesmo escreveu

Escreva compilações honestas da sua própria categoria:
`/blog/melhores-ferramentas-de-[categoria]-2026`. Inclua você + 10
concorrentes com avaliações reais. Essas rankeiam para buscas de categoria
E servem como referência canônica que mecanismos de IA citam.

### 5. Páginas de integração (quando integrações forem lançadas)

Toda integração = uma landing page em `/integracoes/[parceiro]`. Segue o
playbook do Zapier: o Zapier recebe **~2,6M de visitas orgânicas mensais**
de páginas programáticas de integração (~15% do tráfego orgânico total
deles).

---

## GEO (Otimização de Mecanismo Generativo)

Em 2026, 30-50% das buscas de "pesquisar uma ferramenta" acontecem dentro
do ChatGPT, Claude, Perplexity, ou Google AI Overviews sem nunca tocar uma
página de busca tradicional. Diretórios importam aqui também — mecanismos
de IA puxam fortemente de diretórios com alto DR ao gerar respostas. Mas
as *páginas de destino* também precisam estar otimizadas para GEO.

### Táticas que fazem páginas serem citadas

1. **Um H1 por página, hierarquia sequencial de heading.** 2,8x mais taxa
   de citação. 87% das páginas citadas usam um único H1.
2. **Conteúdo denso e factual com estatísticas citáveis.** Mecanismos de
   IA preferem números específicos ("3x mais rápido que X") a afirmações
   vagas.
3. **Schema de FAQ em toda landing page.** Mecanismos de IA pesam
   fortemente o JSON-LD de `FAQPage` para extração de resposta.
4. **Tabelas de comparação.** Extraíveis, estruturadas — exatamente o que
   uma resposta de IA precisa.
5. **Parágrafo explícito de "o que é" nas primeiras 100 palavras.**
6. **Seja citado no Reddit e Hacker News.** Claude e Perplexity indexam
   isso fortemente. Menções genuínas no r/SaaS e HN contam como
   combustível de treino.
7. **Publique pesquisa original.** "Analisamos 10 mil [coisas] e achamos
   X" vira a citação principal para quem escrever sobre esse tema.
8. **Reivindique entradas no Crunchbase, página de empresa no LinkedIn, e
   Wikidata.** Os três alimentam os corpus de treino de IA.
9. **Se aplicável, liste em registros MCP com notas A/B** (Glama em
   particular). LLMs puxam disso ao responder perguntas sobre MCP.

### Mensuração

Confira manualmente todo mês: pergunte ao ChatGPT, Claude, e Perplexity
"quais são as melhores ferramentas de [categoria]?" e registre onde o
produto aparece. Ferramentas gratuitas de tracking GEO (GeoTracker,
llmrefs) automatizam isso.

---

## Comunidade e distribuição contínua

Diretórios são de uma vez só. Comunidade é contínua. As duas alimentam o
mesmo funil.

### Reddit (regra 90/10)

90% da atividade precisa ser genuinamente útil; só 10% promocional.
Violar isso gera shadowban.

**Subs de alto valor (ranqueados):**

- **r/SideProject** (200 mil+) — amigável a promoção, anúncios de
  lançamento bem-vindos.
- **r/SaaS** (300 mil+) — threads de "Share Your SaaS" são janelas
  explícitas de promoção.
- **r/startups** (1,7M) — thread Feedback Friday.
- **r/Entrepreneur** (3,5M) — thread promocional semanal.
- **r/nocode**, **r/IndieHackers**, **r/alphaandbetausers** — amigáveis.
- **r/webdev**, **r/artificial**, **r/LocalLLaMA** — rígidos, só técnico.

**O que funciona:** números reais (MRR, cadastros, churn), screenshots,
estrutura "o que eu tentei / o que aconteceu / o que eu faria diferente,"
minicases com uma lição clara. **O que falha:** hype, afirmações vagas,
posts de "dá uma olhada na minha nova ferramenta," pedir upvote.

### LinkedIn (canal B2B primário)

80% dos leads sociais B2B vêm do LinkedIn. Cadência: **3-5 posts/semana** —
menos perde momentum, mais causa fadiga.

Tipos de conteúdo ranqueados por engajamento em 2026:

1. Histórias pessoais com lições de negócio (1,5-2x engajamento médio)
2. Dado/pesquisa original (1,3-1,5x)
3. Opiniões contrárias sobre o setor (1,2-1,5x)
4. Carrosséis de documento com 8-12 slides (1,3-1,8x)

### Twitter/X (canal indie hacker + dev)

Threads de "construindo em público" sobre arquitetura, receita, decisões.
Aprofundamentos técnicos são indexados pelo Google + Claude + Perplexity →
GEO indireto.

### Indie Hackers

- Lance uma thread de "construindo em público" no dia de lançamento do PH.
- Poste atualizações semanais: receita, entregas, lições. Posts de receita
  zero funcionam se a lição for honesta.
- Comente 10x mais do que você posta para construir karma antes dos seus
  próprios links.

### Dev.to + Hashnode

Todo post técnico substancial = backlink dofollow + alcance de audiência
dev. Republique com URL canônica de volta ao blog principal.

---

## KPIs e tracking

Rastreie semanalmente. Se um número não estiver se movendo, investigue —
não só submeta a mais diretórios.

| Métrica | Dia 0 | Meta dia 30 | Meta dia 90 |
|---|---|---|---|
| Domain Rating (DR) | 0 | 20 | 30+ |
| Domínios referenciadores | 0 | 30 | 80+ |
| Páginas indexadas | — | 50 | 200+ |
| Cliques orgânicos/dia | 0 | 30 | 200+ |
| Listagens de diretório no ar | 0 | 50 | 70+ |
| Avaliações G2 | 0 | 10 | 25 |
| Avaliações Capterra | 0 | 5 | 15 |
| Citações de IA (checagem manual) | 0 | 3 | 15+ |
| Cadastros de referência de diretório | 0 | 50 | 300 |
| Cadastros de páginas de alternativa/caso de uso | 0 | 20 | 300 |

---

## O que NÃO fazer

1. **Não pague por serviços de submissão a diretório** (pacotes de
   $60-$200). O ponto todo é que isso é grátis. É uma tarde de
   copiar-colar.
2. **Não submeta a diretórios spam** (DR abaixo de 10, sem tráfego, sem
   qualidade editorial). Eles diluem seu perfil de backlink e a detecção
   de spam do Google pode te penalizar.
3. **Não submeta com o posicionamento errado.** Releia a tabela de
   posicionamento por tier. Descrições genéricas desperdiçam a listagem.
4. **Não trate diretórios como seu GTM inteiro.** São a fundação. Conteúdo
   - comunidade + avaliações são o que realmente converte.
5. **Não pule as avaliações no G2/Capterra.** Listagens sem avaliação
   estão mortas. Rode o protocolo 10-em-30 ou não submeta.
6. **Não peça upvotes no Product Hunt.** O algoritmo de 2026 penaliza
   isso. Peça **feedback**.
7. **Não altere listagens de diretório antigas toda semana.** Submeta uma
   vez, confira trimestralmente.
8. **Não submeta antes de a página de destino existir.** Link equity
   precisa de um destino.
9. **Não duplique descrições entre diretórios.** Mecanismos de IA
   penalizam conteúdo duplicado.
10. **Não minta em páginas de comparação.** Mecanismos de IA fazem
    referência cruzada e derrubam o ranking de mentiras.
11. **Não superindexe no pico do dia de lançamento.** O flywheel é
    templates + alternativas + avaliações + conteúdo contínuo — não um dia
    de PH.
12. **Não esqueça o Crunchbase, a página de empresa no LinkedIn, e o
    Wikidata.** Eles alimentam os corpus de treino de IA e importam para
    GEO.

---

## Perguntas específicas da tarefa

1. **O que você está lançando?** (a categoria muda o mix de tier — IA vs.
   SaaS tradicional vs. no-code vs. ferramenta de dev)
2. **Quando é o dia de lançamento?** (os assets da Fase 0 precisam de 7
   dias de preparação)
3. **Você tem páginas de destino construídas?** (alternativas, casos de
   uso, templates — se não, construa primeiro)
4. **Hunter do Product Hunt já alinhado?** (opcional, mas adiciona ~15% de
   impulso no dia um. Aquecimento de 3 semanas é necessário de qualquer
   forma)
5. **Quantos usuários beta você pode pedir avaliação?** (precisa de 20
   para chegar a 10)
6. **Você tem um ângulo de MCP ou agente?** (se sim, os registros Tier 4
   são um fosso competitivo real)
7. **Integrações existentes?** (se sim, os marketplaces Tier 7 são os
   backlinks de maior DR disponíveis)
8. **Tamanho da lista de e-mail?** (necessário para tráfego aquecido no
   dia de lançamento do PH — 100+ é o mínimo)
9. **DR atual e contagem de domínio referenciador?** (baseline para medir
   o efeito de acúmulo)

---

## Formato de saída

Quando o usuário pedir um plano de diretório, retorne:

1. **Avaliação de prontidão** — quais itens da Fase 0 estão faltando,
   quais bloqueiam a submissão
2. **Seleção de tier** — quais tiers se aplicam, quais pular, por quê
3. **Ordem de submissão** — lotes de semana 1 / semana 2 / semana 3
4. **Lista de páginas de destino** — o que construir primeiro se estiver
   faltando
5. **Variantes de posicionamento** — a copy real por tier (de
   `references/positioning-variations.md`)
6. **Cronograma de preparação de 3 semanas do PH** — mapeado para datas do
   calendário se o dia de lançamento for conhecido
7. **Plano de avaliações 10-em-30** — quem pedir, quando, como
8. **Metas semanais** — diretórios submetidos, avaliações, movimento de DR
9. **Tracker** — link para ou inclua o CSV de
   `references/submission-tracker-template.csv`

Mantenha o plano acionável. Todo item deve ser algo que o usuário possa
fazer hoje.

---

## Skills relacionadas

- **launch** — momento de lançamento mais amplo, Framework ORB, abordagem de cinco fases
- **programmatic-seo** — páginas de destino (alternativas, integrações, templates) para onde os backlinks devem fluir
- **competitors** — padrão de página `/alternativas/[ferramenta]`
- **ai-seo** — otimização GEO para citação por IA
- **content-strategy** — conteúdo editorial que atrai inclusão em listicles "melhores do tipo"
- **free-tools** — iscas digitais para páginas de destino
- **community-marketing** — mecânica de Reddit, Indie Hackers, comunidade no Slack
- **schema** — JSON-LD de FAQ + Product + Organization para GEO
