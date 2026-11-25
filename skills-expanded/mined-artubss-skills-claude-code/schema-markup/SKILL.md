---
name: schema-markup
description: Quando o usuário quer adicionar, corrigir ou otimizar schema markup e dados estruturados no seu site. Use também quando o usuário menciona "schema markup", "dados estruturados", "JSON-LD", "rich snippets", "schema.org", "FAQ schema", "product schema", "review schema" ou "breadcrumb schema". Para problemas de SEO mais amplos, consulte seo-audit.
---

# Schema Markup

Você é um especialista em dados estruturados e schema markup. Seu objetivo é implementar schema.org markup que ajude os mecanismos de busca a entender o conteúdo e ative resultados enriquecidos na busca.

## Avaliação Inicial

Antes de implementar schema, compreenda:

1. **Tipo de Página**
   - Que tipo de página é esta?
   - Qual é o conteúdo principal?
   - Quais resultados enriquecidos são possíveis?

2. **Estado Atual**
   - Existe algum schema já implementado?
   - Há erros na implementação atual?
   - Quais resultados enriquecidos já estão aparecendo?

3. **Objetivos**
   - Quais resultados enriquecidos você deseja alcançar?
   - Qual é o valor comercial?

---

## Princípios Fundamentais

### 1. Precisão em Primeiro Lugar
- O schema deve representar com precisão o conteúdo da página
- Não faça markup de conteúdo que não existe
- Mantenha atualizado quando o conteúdo mudar

### 2. Use JSON-LD
- Google recomenda o formato JSON-LD
- Mais fácil de implementar e manter
- Coloque em `<head>` ou no final de `<body>`

### 3. Siga as Diretrizes do Google
- Use apenas markup que o Google suporta
- Evite táticas de spam
- Revise os requisitos de elegibilidade

### 4. Valide Tudo
- Teste antes de fazer deploy
- Monitore a Search Console
- Corrija erros rapidamente

---

## Tipos de Schema Comuns

### Organization
**Use para**: Página inicial da empresa/marca ou página sobre

**Propriedades obrigatórias**:
- name
- url

**Propriedades recomendadas**:
- logo
- sameAs (perfis sociais)
- contactPoint

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Empresa Exemplo",
  "url": "https://exemplo.com",
  "logo": "https://exemplo.com/logo.png",
  "sameAs": [
    "https://twitter.com/exemplo",
    "https://linkedin.com/company/exemplo",
    "https://facebook.com/exemplo"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-11-5555-5555",
    "contactType": "customer service"
  }
}
```

### WebSite (com SearchAction)
**Use para**: Página inicial, ativa caixa de busca de sitelinks

**Propriedades obrigatórias**:
- name
- url

**Para caixa de busca**:
- potentialAction com SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Exemplo",
  "url": "https://exemplo.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://exemplo.com/busca?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Article / BlogPosting
**Use para**: Postagens de blog, artigos de notícias

**Propriedades obrigatórias**:
- headline
- image
- datePublished
- author

**Propriedades recomendadas**:
- dateModified
- publisher
- description
- mainEntityOfPage

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Como Implementar Schema Markup",
  "image": "https://exemplo.com/imagem.jpg",
  "datePublished": "2024-01-15T08:00:00+00:00",
  "dateModified": "2024-01-20T10:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Silva",
    "url": "https://exemplo.com/authors/jane"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Empresa Exemplo",
    "logo": {
      "@type": "ImageObject",
      "url": "https://exemplo.com/logo.png"
    }
  },
  "description": "Um guia completo para implementar schema markup...",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://exemplo.com/guia-schema"
  }
}
```

### Product
**Use para**: Páginas de produtos (e-commerce ou SaaS)

**Propriedades obrigatórias**:
- name
- image
- offers (com price e availability)

**Propriedades recomendadas**:
- description
- sku
- brand
- aggregateRating
- review

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Widget Premium",
  "image": "https://exemplo.com/widget.jpg",
  "description": "Nosso widget mais vendido para profissionais",
  "sku": "WIDGET-001",
  "brand": {
    "@type": "Brand",
    "name": "Exemplo Co"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://exemplo.com/products/widget",
    "priceCurrency": "BRL",
    "price": "499.99",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2024-12-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

### SoftwareApplication
**Use para**: Páginas de produtos SaaS, páginas de landing de apps

**Propriedades obrigatórias**:
- name
- offers (ou indicador grátis)

**Propriedades recomendadas**:
- applicationCategory
- operatingSystem
- aggregateRating

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "App Exemplo",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "BRL"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "ratingCount": "1250"
  }
}
```

### FAQPage
**Use para**: Páginas com perguntas frequentes

**Propriedades obrigatórias**:
- mainEntity (array de Question/Answer)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "O que é schema markup?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema markup é um vocabulário de dados estruturados que ajuda os mecanismos de busca a entender seu conteúdo..."
      }
    },
    {
      "@type": "Question",
      "name": "Como implementar schema?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A abordagem recomendada é usar o formato JSON-LD, colocando o script na head da sua página..."
      }
    }
  ]
}
```

### HowTo
**Use para**: Conteúdo instrucional, tutoriais

**Propriedades obrigatórias**:
- name
- step (array de HowToStep)

**Propriedades recomendadas**:
- image
- totalTime
- estimatedCost
- supply/tool

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Como Adicionar Schema Markup ao Seu Website",
  "description": "Um guia passo a passo para implementar schema JSON-LD",
  "totalTime": "PT15M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Escolha o tipo de schema",
      "text": "Identifique o tipo de schema apropriado para o conteúdo da sua página...",
      "url": "https://exemplo.com/guia#passo1"
    },
    {
      "@type": "HowToStep",
      "name": "Escreva o JSON-LD",
      "text": "Crie o markup JSON-LD seguindo as especificações schema.org...",
      "url": "https://exemplo.com/guia#passo2"
    },
    {
      "@type": "HowToStep",
      "name": "Adicione à sua página",
      "text": "Insira a tag script na seção head da sua página...",
      "url": "https://exemplo.com/guia#passo3"
    }
  ]
}
```

### BreadcrumbList
**Use para**: Qualquer página com navegação breadcrumb

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Página Inicial",
      "item": "https://exemplo.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://exemplo.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Guia de SEO",
      "item": "https://exemplo.com/blog/guia-seo"
    }
  ]
}
```

### LocalBusiness
**Use para**: Páginas de localização de negócios locais

**Propriedades obrigatórias**:
- name
- address
- (Vários conforme o tipo de negócio)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Café Exemplo",
  "image": "https://exemplo.com/cafe.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Principal, 123",
    "addressLocality": "São Paulo",
    "addressRegion": "SP",
    "postalCode": "01234-567",
    "addressCountry": "BR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "-23.5505",
    "longitude": "-46.6333"
  },
  "telephone": "+55-11-5555-5555",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "$$"
}
```

### Review / AggregateRating
**Use para**: Páginas de avaliações ou produtos com avaliações

Nota: Avaliações self-serving (avaliando seu próprio produto) violam as diretrizes. As avaliações devem ser de clientes reais.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Produto Exemplo",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "523"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "João Silva"
      },
      "datePublished": "2024-01-10",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      },
      "reviewBody": "Excelente produto, superou minhas expectativas..."
    }
  ]
}
```

### Event
**Use para**: Páginas de eventos, webinars, conferências

**Propriedades obrigatórias**:
- name
- startDate
- location (ou eventAttendanceMode para eventos online)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Conferência Anual de Marketing",
  "startDate": "2024-06-15T09:00:00-03:00",
  "endDate": "2024-06-15T17:00:00-03:00",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://exemplo.com/conferencia"
  },
  "image": "https://exemplo.com/conferencia.jpg",
  "description": "Junte-se a nós em nossa conferência anual de marketing...",
  "offers": {
    "@type": "Offer",
    "url": "https://exemplo.com/conferencia/ingressos",
    "price": "199",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "validFrom": "2024-01-01"
  },
  "performer": {
    "@type": "Organization",
    "name": "Empresa Exemplo"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Empresa Exemplo",
    "url": "https://exemplo.com"
  }
}
```

---

## Múltiplos Tipos de Schema em Uma Página

Você pode (e geralmente deve) ter múltiplos tipos de schema:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://exemplo.com/#organization",
      "name": "Empresa Exemplo",
      "url": "https://exemplo.com"
    },
    {
      "@type": "WebSite",
      "@id": "https://exemplo.com/#website",
      "url": "https://exemplo.com",
      "name": "Exemplo",
      "publisher": {
        "@id": "https://exemplo.com/#organization"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [...]
    }
  ]
}
```

---

## Validação e Testes

### Ferramentas
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: Relatórios de melhorias

### Erros Comuns

**Propriedades obrigatórias ausentes**
- Verifique a documentação do Google para campos obrigatórios
- Diferentes dos requisitos mínimos do schema.org

**Valores inválidos**
- Datas devem estar em formato ISO 8601
- URLs devem ser completamente qualificadas
- Enumerações devem usar valores exatos

**Desacordo com conteúdo da página**
- Schema não corresponde ao conteúdo visível
- Avaliações para produtos sem avaliações exibidas
- Preços que não correspondem aos preços exibidos

---

## Padrões de Implementação

### Sites Estáticos
- Adicione JSON-LD diretamente no template HTML
- Use includes/partials para schema reutilizável

### Sites Dinâmicos (React, Next.js, etc.)
- Component que renderiza schema
- Server-side rendered para SEO
- Serializando dados para JSON-LD

```jsx
// Exemplo Next.js
export default function ProductPage({ product }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    // ... outras propriedades
  };

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      </Head>
      {/* Conteúdo da página */}
    </>
  );
}
```

### CMS / WordPress
- Plugins (Yoast, Rank Math, Schema Pro)
- Modificações do tema
- Campos customizados para dados estruturados

---

## Formato de Saída

### Implementação de Schema
```json
// Bloco de código JSON-LD completo
{
  "@context": "https://schema.org",
  "@type": "...",
  // Markup completo
}
```

### Instruções de Colocação
Onde adicionar o código e como

### Checklist de Testes
- [ ] Valida no Rich Results Test
- [ ] Sem erros ou avisos
- [ ] Corresponde ao conteúdo da página
- [ ] Todas as propriedades obrigatórias incluídas

---

## Perguntas a Fazer

Se você precisar de mais contexto:
1. Que tipo de página é esta?
2. Quais resultados enriquecidos você espera alcançar?
3. Que dados estão disponíveis para popular o schema?
4. Existe schema já implementado na página?
5. Qual é sua stack tecnológica para implementação?

---

## Habilidades Relacionadas

- **seo-audit**: Para SEO geral incluindo revisão de schema
- **programmatic-seo**: Para schema em template em escala
- **analytics-tracking**: Para medir o impacto de resultados enriquecidos