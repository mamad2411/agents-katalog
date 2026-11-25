---
name: Otimizador de SEO
description: Especialista em Otimização para Mecanismos de Busca para estratégia de conteúdo, SEO técnico, pesquisa de palavras-chave e melhorias de ranqueamento. Use ao otimizar conteúdo do site, melhorar ranqueamentos de busca, realizar análise de palavras-chave ou implementar melhores práticas de SEO. Especialista em SEO on-page, meta tags, schema markup e Core Web Vitals.
---

# Otimizador de SEO

Orientação abrangente para otimização de mecanismos de busca em conteúdo, implementação técnica e planejamento estratégico para melhorar visibilidade e ranqueamentos de busca orgânica.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Otimizar conteúdo do site para mecanismos de busca
- Realizar pesquisa e análise de palavras-chave
- Implementar melhorias de SEO técnico
- Criar meta tags e descrições amigáveis ao SEO
- Auditar sites para problemas de SEO
- Melhorar Core Web Vitals e velocidade de página
- Implementar schema markup (dados estruturados)
- Planejar estratégia de conteúdo para tráfego orgânico

## Fundamentos de SEO

### 1. Pesquisa e Estratégia de Palavras-Chave

**Seleção de Palavra-Chave Primária:**
- Foque em intenção de busca (informacional, navegacional, transacional, comercial)
- Equilibre volume de buscas com competição
- Considere dificuldade de palavra-chave e potencial de ranqueamento
- Alvo em palavras-chave long-tail para vitórias rápidas

**Processo de Pesquisa de Palavras-Chave:**
```
1. Identificar palavras-chave iniciais a partir dos objetivos do negócio
2. Usar ferramentas para expandir lista de palavras-chave (Google Keyword Planner, Ahrefs, SEMrush)
3. Analisar volume de buscas e dificuldade
4. Agrupar palavras-chave por clusters de tópicos
5. Mapear palavras-chave para tipos de conteúdo e páginas
6. Priorizar com base em ROI potencial
```

**Fórmula de Otimização de Conteúdo:**
- Palavra-chave primária: densidade de 1-2% (colocação natural)
- Incluir em: título, H1, primeiro parágrafo, URL, meta descrição
- Usar variações semânticas e termos relacionados
- Manter legibilidade natural (não fazer keyword stuffing)

### 2. SEO On-Page

**Otimização de Title Tag:**
```html
<!-- Bom: Descritivo, inclui palavra-chave, menos de 60 caracteres -->
<title>Guia Completo de React Hooks - Aprenda useEffect & useState</title>

<!-- Ruim: Muito longo, keyword stuffing, genérico -->
<title>React Hooks Guia React Hooks Tutorial React Hooks Exemplos Aprenda React</title>
```

**Melhores Práticas:**
- Manter menos de 60 caracteres (exibido nos SERPs)
- Colocar palavra-chave primária perto do início
- Incluir nome da marca se houver espaço
- Tornar atraente e digno de clique
- Único para cada página

**Meta Descrição:**
```html
<!-- Bom: Atraente, inclui palavras-chave, call-to-action, 150-160 caracteres -->
<meta name="description" content="Domine React Hooks com nosso guia abrangente. Aprenda useState, useEffect e hooks customizados com exemplos práticos. Comece a construir melhores apps React hoje.">

<!-- Ruim: Muito curto, sem proposta de valor -->
<meta name="description" content="Guia e tutorial de React Hooks">
```

**Estrutura de Cabeçalhos:**
```html
<!-- Hierarquia apropriada -->
<h1>Título Principal da Página (Palavra-Chave Primária)</h1>
  <h2>Cabeçalho de Seção (Palavras-Chave Relacionadas)</h2>
    <h3>Subseção</h3>
    <h3>Subseção</h3>
  <h2>Outra Seção</h2>
    <h3>Subseção</h3>
```

**Estrutura de URL:**
```
✅ URLs Boas:
- /blog/guia-react-hooks
- /produtos/tenis-corrida
- /aprenda/javascript-async-await

❌ URLs Ruins:
- /blog?p=12345
- /produtos/cat-1/subcat-2/item-999
- /page.php?id=abc&ref=xyz
```

**Otimização de Imagens:**
```html
<!-- Imagem otimizada -->
<img
  src="/images/diagrama-react-hooks-800w.webp"
  alt="Diagrama de ciclo de vida de React Hooks mostrando useState e useEffect"
  width="800"
  height="600"
  loading="lazy"
/>
```

**Melhores Práticas:**
- Usar texto alternativo descritivo e rico em palavras-chave
- Comprimir imagens (formato WebP preferido)
- Especificar dimensões para evitar deslocamento de layout
- Usar lazy loading para imagens abaixo da dobra
- Incluir legendas quando relevante

### 3. Qualidade de Conteúdo

**Princípios E-E-A-T (Experiência, Expertise, Autoridade, Confiança):**
- Demonstrar expertise do autor com credenciais
- Citar fontes autoritárias
- Manter conteúdo preciso e atualizado
- Mostrar experiência real e insights originais
- Incluir bios de autores e assinaturas

**Estrutura de Conteúdo para SEO:**
```markdown
# Título Principal (H1) - Palavra-Chave Primária

Introdução breve com palavra-chave primária nos primeiros 100 palavras.

## O que é [Tópico]? (H2) - Responda pergunta central

Explicação abrangente com exemplos.

## Por que [Tópico] Importa (H2) - Proposta de valor

Benefícios e casos de uso.

## Como [Ação] (H2) - Guia prático

Instruções passo a passo com visuais.

## Melhores Práticas (H2) - Dicas avançadas

Recomendações de especialistas.

## Erros Comuns a Evitar (H2)

Troubleshooting e armadilhas.

## Conclusão

Resumo e call-to-action.
```

**Diretrizes de Comprimento de Conteúdo:**
- Posts de blog: 1.500-2.500 palavras (tópicos abrangentes)
- Páginas de produto: mínimo 300-500 palavras
- Páginas de categoria: 500-1.000 palavras
- Homepage: 500+ palavras

### 4. SEO Técnico

**Schema Markup (Dados Estruturados):**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Guia Completo de React Hooks",
  "image": "https://example.com/images/react-hooks.jpg",
  "datePublished": "2024-01-15",
  "dateModified": "2024-02-01",
  "author": {
    "@type": "Person",
    "name": "Jane Developer"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Tech Academy",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

**Tipos de Schema Comuns:**
- Article (posts de blog)
- Product (e-commerce)
- FAQ (páginas de perguntas e respostas)
- HowTo (tutoriais e guias)
- Organization (informações de empresa)
- LocalBusiness (negócios baseados em localização)
- BreadcrumbList (caminhos de navegação)
- Review/AggregateRating (avaliações e reviews)

**Configuração de Robots.txt:**
```
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /api/
Allow: /api/public/

Sitemap: https://example.com/sitemap.xml
```

**Estrutura de XML Sitemap:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/blog/guia-react-hooks</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Tags Canônicas:**
```html
<!-- Prevenir problemas de conteúdo duplicado -->
<link rel="canonical" href="https://example.com/pagina-original">

<!-- Lidar com parâmetros de URL -->
<link rel="canonical" href="https://example.com/produtos/sapatos">
<!-- Mesmo se acessado via: /produtos/sapatos?cor=vermelho&tamanho=10 -->
```

### 5. Core Web Vitals

**Largest Contentful Paint (LCP) - Alvo: < 2,5s**
- Otimizar imagens e vídeos
- Usar CDN para ativos estáticos
- Minimizar recursos que bloqueiam renderização
- Implementar lazy loading

**First Input Delay (FID) - Alvo: < 100ms**
- Minimizar tempo de execução de JavaScript
- Dividir tarefas longas
- Usar web workers para computações pesadas
- Diferir JavaScript não crítico

**Cumulative Layout Shift (CLS) - Alvo: < 0,1**
- Definir atributos de tamanho em imagens e vídeos
- Evitar inserir conteúdo acima de conteúdo existente
- Usar animações transform em vez de propriedades que disparam layout
- Reservar espaço para anúncios e embeds

**Otimização de Velocidade de Página:**
```html
<!-- Pré-carregar recursos críticos -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>

<!-- Diferir CSS não crítico -->
<link rel="preload" href="/styles/non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- JavaScript assíncrono/diferido -->
<script src="/js/analytics.js" async></script>
<script src="/js/main.js" defer></script>
```

### 6. SEO Mobile

**Otimização Mobile-First:**
- Design responsivo (teste mobile-friendly aprovado)
- Botões sensíveis ao toque (mínimo 48x48px)
- Tamanhos de fonte legíveis (mínimo 16px)
- Configuração apropriada de viewport
- Velocidade rápida em dispositivos móveis

**Configuração de Viewport:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### 7. Estratégia de Link Interno

**Melhores Práticas:**
- Usar texto âncora descritivo (evitar "clique aqui")
- Vincular a páginas relevantes e contextuais
- Manter hierarquia e fluxo lógicos
- Incluir 3-5 links internos por 1.000 palavras
- Atualizar conteúdo antigo com links para novo conteúdo

**Exemplo:**
```markdown
Saiba mais sobre [padrões avançados de React](/guides/react-patterns)
ou confira nosso [tutorial do hook useState](/tutorials/usestate-guide).
```

## Checklist de Conteúdo SEO

**Antes de Publicar:**
- [ ] Palavra-chave primária em title tag (menos de 60 caracteres)
- [ ] Meta descrição (150-160 caracteres, atraente)
- [ ] Tag H1 com palavra-chave primária
- [ ] Slug de URL otimizado e legível
- [ ] Imagens comprimidas com texto alternativo descritivo
- [ ] 3-5 links internos para conteúdo relevante
- [ ] Links externos para fontes autoritárias
- [ ] Comprimento de conteúdo apropriado para profundidade de tópico
- [ ] Schema markup implementado
- [ ] Mobile-friendly e responsivo
- [ ] Velocidade de página otimizada (< 3s de tempo de carregamento)
- [ ] Nenhum link quebrado
- [ ] Tag canônica definida corretamente
- [ ] Meta tags de compartilhamento social (Open Graph, Twitter Card)

## Estratégias Avançadas de SEO

### Topic Clusters & Pillar Pages

**Estrutura:**
```
Pillar Page: "Guia Completo de React"
  ├── Cluster: "Tutorial de React Hooks"
  ├── Cluster: "Guia de React Context API"
  ├── Cluster: "Otimização de Performance em React"
  └── Cluster: "Melhores Práticas de Testes em React"
```

**Implementação:**
- Criar conteúdo pillar abrangente (3.000+ palavras)
- Desenvolver 8-12 artigos de cluster apoiando o pillar
- Vincular todos os clusters de volta à página pillar
- Vincular página pillar a todos os clusters
- Usar temas de palavras-chave consistentes

### Otimização de Featured Snippet

**Conteúdo Baseado em Perguntas:**
```markdown
## O que é React?

React é uma biblioteca JavaScript para construir interfaces de usuário,
desenvolvida pelo Facebook. Permite que desenvolvedores criem componentes
de UI reutilizáveis e atualizem eficientemente o DOM por meio de uma
implementação virtual do DOM.
```

**Conteúdo Baseado em Listas:**
```markdown
## Top 5 Melhores Práticas de React

1. Usar componentes funcionais com hooks
2. Implementar gerenciamento de estado apropriado
3. Otimizar performance com React.memo
4. Seguir padrões de composição de componentes
5. Escrever testes abrangentes
```

**Conteúdo Baseado em Tabelas:**
| Framework | Performance | Curva de Aprendizado | Ecossistema |
|-----------|-------------|----------------------|------------|
| React     | Excelente   | Moderada             | Extenso    |
| Vue       | Excelente   | Fácil                | Em Crescimento |
| Angular   | Bom         | Íngreme              | Maduro     |

## SEO Local (para negócios com localizações físicas)

**Otimização de Google Business Profile:**
- Preencher todas as informações do negócio
- Posts e atualizações regulares
- Responder a reviews
- Adicionar fotos de alta qualidade
- Verificar horário comercial

**Schema Markup Local:**
```json
{
  "@type": "LocalBusiness",
  "name": "Tech Solutions Inc",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "São Paulo",
    "addressRegion": "SP",
    "postalCode": "01234-567"
  },
  "telephone": "+55-11-5555-0123"
}
```

## Monitoramento & Analytics

**Métricas-Chave para Rastrear:**
- Tendências de tráfego orgânico
- Ranqueamentos de palavras-chave
- Taxa de cliques (CTR)
- Taxa de rejeição e tempo de permanência
- Pontuações de Core Web Vitals
- Crescimento do perfil de backlinks
- Taxas de conversão do tráfego orgânico

**Ferramentas:**
- Google Search Console (performance, problemas de indexação)
- Google Analytics 4 (tráfego, comportamento, conversões)
- PageSpeed Insights (Core Web Vitals)
- Ahrefs/SEMrush (palavras-chave, backlinks, competição)
- Screaming Frog (auditorias técnicas)

Ao otimizar para SEO, priorize experiência do usuário e entrega de valor. Mecanismos de busca cada vez mais recompensam conteúdo que genuinamente ajuda usuários e fornece informações autoritárias e confiáveis.