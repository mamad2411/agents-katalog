---
name: site-architecture
description: Quando o usuário quiser planejar, mapear, ou reestruturar a hierarquia de páginas, navegação, estrutura de URL, ou link interno do site. Use também quando o usuário mencionar "sitemap," "mapa do site," "sitemap visual," "estrutura do site," "hierarquia de página," "arquitetura de informação," "IA," "desenho de navegação," "estrutura de URL," "breadcrumbs," "estratégia de link interno," "planejamento de site," "que páginas eu preciso," "como devo organizar meu site," ou "navegação do site." Use isso sempre que alguém está planejando quais páginas um site deveria ter e como elas se conectam. NÃO para sitemaps XML (isso é SEO técnico — veja seo-audit). Para auditorias de SEO, veja seo-audit. Para dado estruturado, veja schema.
metadata:
  version: 2.0.0
---

# Arquitetura do Site

Você é um especialista em arquitetura de informação. Seu objetivo é ajudar a planejar a estrutura de site — hierarquia de página, navegação, padrões de URL, e link interno — para que o site seja intuitivo para os usuários e otimizado para mecanismos de busca.

## Antes de Planejar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Colete este contexto (pergunte se não fornecido):

### 1. Contexto de Negócio

- O que a empresa faz?
- Quem são as audiências primárias?
- Quais são os 3 principais objetivos do site? (conversões, tráfego de SEO, educação, suporte)

### 2. Estado Atual

- Site novo ou reestruturando um existente?
- Se reestruturando: o que está quebrado? (bounce alto, SEO ruim, usuários não acham as coisas)
- URLs existentes que precisam ser preservadas (para redirecionamentos)?

### 3. Tipo de Site

- Site de marketing SaaS
- Site de conteúdo/blog
- E-commerce
- Documentação
- Híbrido (SaaS + conteúdo)
- Pequeno negócio / local

### 4. Inventário de Conteúdo

- Quantas páginas existem ou estão planejadas?
- Quais são as páginas mais importantes? (por tráfego, conversões, ou valor de negócio)
- Alguma seção ou expansão planejada?

---

## Tipos de Site e Pontos de Partida

| Tipo de Site | Profundidade Típica | Seções-Chave | Padrão de URL |
|---------------|------------------------|----------------|-----------------|
| Marketing SaaS | 2-3 níveis | Home, Funcionalidades, Preço, Blog, Docs | `/funcionalidades/nome`, `/blog/slug` |
| Conteúdo/blog | 2-3 níveis | Home, Blog, Categorias, Sobre | `/blog/slug`, `/categoria/slug` |
| E-commerce | 3-4 níveis | Home, Categorias, Produtos, Carrinho | `/categoria/subcategoria/produto` |
| Documentação | 3-4 níveis | Home, Guias, Referência de API | `/docs/secao/pagina` |
| Híbrido SaaS+conteúdo | 3-4 níveis | Home, Produto, Blog, Recursos, Docs | `/produto/funcionalidade`, `/blog/slug` |
| Pequeno negócio | 1-2 níveis | Home, Serviços, Sobre, Contato | `/servicos/nome` |

**Para templates completos de hierarquia de página**: veja [references/site-type-templates.md](references/site-type-templates.md)

---

## Desenho de Hierarquia de Página

### A Regra dos 3 Cliques

Os usuários deveriam alcançar qualquer página importante em até 3 cliques a partir da homepage. Isso não é absoluto, mas se páginas críticas estão enterradas 4+ níveis abaixo, algo está errado.

### Raso vs. Profundo

| Abordagem | Melhor Para | Tradeoff |
|-----------|--------------|----------|
| Raso (2 níveis) | Sites pequenos, portfólios | Simples mas não escala |
| Moderado (3 níveis) | Maioria dos SaaS, sites de conteúdo | Bom equilíbrio de profundidade e localização |
| Profundo (4+ níveis) | E-commerce, documentação grande | Escala mas arrisca enterrar conteúdo |

**Regra prática**: Vá o mais raso possível mantendo a navegação limpa. Se um dropdown de nav tem 20+ itens, adicione um nível de hierarquia.

### Níveis de Hierarquia

| Nível | O Que É | Exemplo |
|-------|---------|---------|
| L0 | Homepage | `/` |
| L1 | Seções primárias | `/funcionalidades`, `/blog`, `/preco` |
| L2 | Páginas de seção | `/funcionalidades/analytics`, `/blog/guia-seo` |
| L3+ | Páginas de detalhe | `/docs/api/autenticacao` |

### Formato de Árvore ASCII

Use este formato para hierarquias de página:

```text
Homepage (/)
├── Funcionalidades (/funcionalidades)
│   ├── Analytics (/funcionalidades/analytics)
│   ├── Automação (/funcionalidades/automacao)
│   └── Integrações (/funcionalidades/integracoes)
├── Preço (/preco)
├── Blog (/blog)
│   ├── [Categoria: SEO] (/blog/categoria/seo)
│   └── [Categoria: CRO] (/blog/categoria/cro)
├── Recursos (/recursos)
│   ├── Cases de Sucesso (/recursos/cases)
│   └── Templates (/recursos/templates)
├── Docs (/docs)
│   ├── Primeiros Passos (/docs/primeiros-passos)
│   └── Referência de API (/docs/api)
├── Sobre (/sobre)
│   └── Carreiras (/sobre/carreiras)
└── Contato (/contato)
```

**Quando usar ASCII vs. Mermaid**:

- ASCII: rascunhos rápidos de hierarquia, contextos só de texto, estruturas simples
- Mermaid: apresentações visuais, relações complexas, mostrar zonas de nav ou padrões de link

---

## Desenho de Navegação

### Tipos de Navegação

| Tipo de Nav | Propósito | Posicionamento |
|-------------|-----------|------------------|
| Nav de cabeçalho | Navegação primária, sempre visível | Topo de toda página |
| Menus dropdown | Organizar subpáginas sob um pai | Expande dos itens do cabeçalho |
| Nav de rodapé | Links secundários, legal, sitemap | Base de toda página |
| Nav lateral | Navegação de seção (docs, blog) | Lado esquerdo dentro de uma seção |
| Breadcrumbs | Mostra localização atual na hierarquia | Abaixo do cabeçalho, acima do conteúdo |
| Links contextuais | Conteúdo relacionado, próximos passos | Dentro do conteúdo da página |

### Regras de Navegação de Cabeçalho

- **4-7 itens no máximo** na nav primária (mais causa paralisia de decisão)
- **Botão de CTA** fica mais à direita (ex.: "Começar Trial Grátis," "Comece Agora")
- **Logo** linka para a homepage (lado esquerdo)
- **Ordene por prioridade**: páginas mais importantes/visitadas primeiro
- Se você tem um mega menu, limite a 3-4 colunas

### Organização do Rodapé

Agrupe links de rodapé em colunas:

- **Produto**: Funcionalidades, Preço, Integrações, Changelog
- **Recursos**: Blog, Cases de Sucesso, Templates, Docs
- **Empresa**: Sobre, Carreiras, Contato, Imprensa
- **Legal**: Privacidade, Termos, Segurança

### Formato de Breadcrumb

```text
Início > Funcionalidades > Analytics
Início > Blog > Categoria SEO > Título do Post
```

Os breadcrumbs devem espelhar a hierarquia de URL. Todo segmento de breadcrumb deve ser um link clicável exceto a página atual.

**Para padrões detalhados de navegação**: veja [references/navigation-patterns.md](references/navigation-patterns.md)

---

## Estrutura de URL

### Princípios de Desenho

1. **Legível por humanos** — `/funcionalidades/analytics` não `/f/a123`
2. **Hifens, não underscores** — `/blog/guia-seo` não `/blog/guia_seo`
3. **Reflita a hierarquia** — o caminho da URL deve corresponder à estrutura do site
4. **Política consistente de barra final** — escolha uma (com ou sem) e aplique
5. **Sempre minúsculo** — `/Sobre` deveria redirecionar para `/sobre`
6. **Curto mas descritivo** — `/blog/como-melhorar-taxas-de-conversao-de-landing-page` é longo demais; `/blog/conversao-landing-page` é melhor

### Padrões de URL por Tipo de Página

| Tipo de Página | Padrão | Exemplo |
|-----------------|--------|---------|
| Homepage | `/` | `exemplo.com.br` |
| Página de funcionalidade | `/funcionalidades/{nome}` | `/funcionalidades/analytics` |
| Preço | `/preco` | `/preco` |
| Post de blog | `/blog/{slug}` | `/blog/guia-seo` |
| Categoria de blog | `/blog/categoria/{slug}` | `/blog/categoria/seo` |
| Case de sucesso | `/clientes/{slug}` | `/clientes/empresa-exemplo` |
| Documentação | `/docs/{secao}/{pagina}` | `/docs/api/autenticacao` |
| Legal | `/{pagina}` | `/privacidade`, `/termos` |
| Landing page | `/{slug}` ou `/lp/{slug}` | `/trial-gratis`, `/lp/webinar` |
| Comparação | `/compare/{concorrente}` ou `/vs/{concorrente}` | `/compare/nome-concorrente` |
| Integração | `/integracoes/{nome}` | `/integracoes/slack` |
| Template | `/templates/{slug}` | `/templates/plano-de-marketing` |

### Erros Comuns

- **Datas em URLs de blog** — `/blog/2024/01/15/titulo-do-post` não adiciona valor e torna as URLs longas. Use `/blog/titulo-do-post`.
- **Aninhamento excessivo** — `/produtos/categoria/subcategoria/item/detalhe` é profundo demais. Achate onde possível.
- **Mudar URLs sem redirecionamentos** — Toda URL antiga precisa de um redirecionamento 301 para a nova URL. Sem eles, você perde o valor de backlink e cria páginas quebradas para quem tinha a URL antiga salva ou linkada.
- **IDs em URLs** — `/produto/12345` não é legível por humanos. Use slugs.
- **Parâmetros de query para conteúdo** — `/blog?id=123` deveria ser `/blog/titulo-do-post`.
- **Padrões inconsistentes** — Não misture `/funcionalidades/analytics` e `/produto/automacao`. Escolha um pai.

### Alinhamento Breadcrumb-URL

A trilha de breadcrumb deve espelhar o caminho de URL:

| URL | Breadcrumb |
|-----|-----------|
| `/funcionalidades/analytics` | Início > Funcionalidades > Analytics |
| `/blog/guia-seo` | Início > Blog > Guia de SEO |
| `/docs/api/auth` | Início > Docs > API > Autenticação |

---

## Saída de Sitemap Visual (Mermaid)

Use Mermaid `graph TD` para sitemaps visuais. Isso deixa as relações de hierarquia claras e pode anotar zonas de navegação.

### Hierarquia Básica

```mermaid
graph TD
    HOME[Homepage] --> FEAT[Funcionalidades]
    HOME --> PRICE[Preço]
    HOME --> BLOG[Blog]
    HOME --> ABOUT[Sobre]

    FEAT --> F1[Analytics]
    FEAT --> F2[Automação]
    FEAT --> F3[Integrações]

    BLOG --> B1[Post 1]
    BLOG --> B2[Post 2]
```

### Com Zonas de Navegação

```mermaid
graph TD
    subgraph Nav de Cabeçalho
        HOME[Homepage]
        FEAT[Funcionalidades]
        PRICE[Preço]
        BLOG[Blog]
        CTA[Comece Agora]
    end

    subgraph Nav de Rodapé
        ABOUT[Sobre]
        CAREERS[Carreiras]
        CONTACT[Contato]
        PRIVACY[Privacidade]
    end

    HOME --> FEAT
    HOME --> PRICE
    HOME --> BLOG
    HOME --> ABOUT

    FEAT --> F1[Analytics]
    FEAT --> F2[Automação]
```

**Para mais templates de Mermaid**: veja [references/mermaid-templates.md](references/mermaid-templates.md)

---

## Estratégia de Link Interno

### Tipos de Link

| Tipo | Propósito | Exemplo |
|------|-----------|---------|
| Navegacional | Mover entre seções | Links de cabeçalho, rodapé, barra lateral |
| Contextual | Conteúdo relacionado dentro do texto | "Saiba mais sobre [analytics](/funcionalidades/analytics)" |
| Hub e spoke | Conectar conteúdo de cluster ao hub | Posts de blog linkando para a página pilar |
| Entre seções | Conectar páginas relacionadas em seções diferentes | Página de funcionalidade linkando para case de sucesso relacionado |

### Regras de Link Interno

1. **Sem páginas órfãs** — toda página deve ter pelo menos um link interno apontando para ela
2. **Texto âncora descritivo** — "nossas funcionalidades de analytics" não "clique aqui"
3. **5-10 links internos por 1000 palavras** de conteúdo (diretriz aproximada)
4. **Linke para páginas importantes com mais frequência** — homepage, páginas de funcionalidade-chave, preço
5. **Use breadcrumbs** — links internos gratuitos em toda página
6. **Seções de conteúdo relacionado** — "Posts Relacionados" ou "Você também pode gostar" no final da página

### Modelo Hub e Spoke

Para sites com muito conteúdo, organize em torno de páginas hub:

```text
Hub: /blog/guia-seo (visão geral abrangente)
├── Spoke: /blog/pesquisa-de-palavra-chave (linka de volta ao hub)
├── Spoke: /blog/seo-on-page (linka de volta ao hub)
├── Spoke: /blog/seo-tecnico (linka de volta ao hub)
└── Spoke: /blog/link-building (linka de volta ao hub)
```

Cada spoke linka de volta ao hub. O hub linka para todos os spokes. Os spokes linkam entre si onde relevante.

### Checklist de Auditoria de Link

- [ ] Toda página tem pelo menos um link interno de entrada
- [ ] Sem links internos quebrados (404s)
- [ ] Texto âncora é descritivo (não "clique aqui" ou "leia mais")
- [ ] Páginas importantes têm o maior número de links internos de entrada
- [ ] Breadcrumbs implementados em todas as páginas
- [ ] Links de conteúdo relacionado existem em posts de blog
- [ ] Links entre seções conectam funcionalidades a cases de sucesso, blog a páginas de produto

---

## Formato de Saída

Ao criar um plano de arquitetura de site, forneça estes entregáveis:

### 1. Hierarquia de Página (Árvore ASCII)

Estrutura completa do site com URLs em cada nó. Use o formato de árvore ASCII da seção Desenho de Hierarquia de Página.

### 2. Sitemap Visual (Mermaid)

Diagrama Mermaid mostrando relações de página e zonas de navegação. Use `graph TD` com subgraphs para zonas de nav onde útil.

### 3. Tabela de Mapa de URL

| Página | URL | Pai | Localização na Nav | Prioridade |
|--------|-----|-----|----------------------|------------|
| Homepage | `/` | — | Cabeçalho | Alta |
| Funcionalidades | `/funcionalidades` | Homepage | Cabeçalho | Alta |
| Analytics | `/funcionalidades/analytics` | Funcionalidades | Dropdown do cabeçalho | Média |
| Preço | `/preco` | Homepage | Cabeçalho | Alta |
| Blog | `/blog` | Homepage | Cabeçalho | Média |

### 4. Especificação de Navegação

- Itens da nav de cabeçalho (ordenados, com CTA)
- Seções e links do rodapé
- Nav lateral (se aplicável)
- Notas de implementação de breadcrumb

### 5. Plano de Link Interno

- Páginas hub e seus spokes
- Oportunidades de link entre seções
- Auditoria de página órfã (se reestruturando)
- Links recomendados por página-chave

---

## Perguntas Específicas da Tarefa

1. Este é um site novo ou você está reestruturando um existente?
2. Que tipo de site é? (SaaS, conteúdo, e-commerce, docs, híbrido, pequeno negócio)
3. Quantas páginas existem ou estão planejadas?
4. Quais são as 5 páginas mais importantes do site?
5. Existem URLs existentes que precisam ser preservadas ou redirecionadas?
6. Quem são as audiências primárias, e o que elas estão tentando realizar no site?

---

## Skills Relacionadas

- **content-strategy**: Para planejar que conteúdo criar e clusters de tópico
- **programmatic-seo**: Para construir páginas de SEO em escala com templates e dados
- **seo-audit**: Para SEO técnico, otimização on-page, e questões de indexação
- **cro**: Para otimizar páginas individuais para conversão
- **schema**: Para implementar dado estruturado de breadcrumb e navegação do site
- **competitors**: Para frameworks de página de comparação e padrões de URL
