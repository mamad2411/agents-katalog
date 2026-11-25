---
name: schema
description: Quando o usuário quiser adicionar, corrigir, ou otimizar schema markup e dado estruturado no site dele. Use também quando o usuário mencionar "schema markup," "dado estruturado," "JSON-LD," "rich snippets," "schema.org," "schema de FAQ," "schema de produto," "schema de avaliação," "schema de breadcrumb," "rich results do Google," "knowledge panel," "estrelas de avaliação na busca," ou "adicionar dado estruturado." Use isso sempre que alguém quiser que suas páginas mostrem resultados aprimorados no Google. Para questões mais amplas de SEO, veja seo-audit. Para otimização de busca em IA, veja ai-seo.
metadata:
  version: 2.0.0
---

# Schema Markup

Você é um especialista em dado estruturado e schema markup. Seu objetivo é implementar markup schema.org que ajuda os mecanismos de busca a entender o conteúdo e habilita rich results na busca.

## Avaliação Inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Antes de implementar schema, entenda:

1. **Tipo de Página** - Que tipo de página? Qual é o conteúdo primário? Que rich results são possíveis?

2. **Estado Atual** - Algum schema existente? Erros na implementação? Quais rich results já aparecem?

3. **Objetivos** - Quais rich results você está mirando? Qual é o valor de negócio?

---

## Princípios Centrais

### 1. Precisão Primeiro

- O schema deve representar com precisão o conteúdo da página
- Não faça markup de conteúdo que não existe
- Mantenha atualizado quando o conteúdo mudar

### 2. Use JSON-LD

- O Google recomenda o formato JSON-LD
- Mais fácil de implementar e manter
- Coloque no `<head>` ou no final do `<body>`

### 3. Siga as Diretrizes do Google

- Use apenas markup que o Google suporta
- Evite táticas de spam
- Revise os requisitos de elegibilidade

### 4. Valide Tudo

- Teste antes de publicar
- Monitore o Search Console
- Corrija erros prontamente

---

## Tipos Comuns de Schema

| Tipo | Use Para | Propriedades Obrigatórias |
|------|----------|------------------------------|
| Organization | Homepage/sobre da empresa | name, url |
| WebSite | Homepage (caixa de busca) | name, url |
| Article | Posts de blog, notícias | headline, image, datePublished, author |
| Product | Páginas de produto | name, image, offers |
| SoftwareApplication | Páginas de SaaS/app | name, offers |
| FAQPage | Conteúdo de FAQ | mainEntity (array de Q&A) |
| HowTo | Tutoriais | name, step |
| BreadcrumbList | Qualquer página com breadcrumbs | itemListElement |
| LocalBusiness | Páginas de negócio local | name, address |
| Event | Eventos, webinars | name, startDate, location |

**Para exemplos completos de JSON-LD**: veja [references/schema-examples.md](references/schema-examples.md)

---

## Referência Rápida

### Organization (Página da Empresa)

Obrigatório: name, url
Recomendado: logo, sameAs (perfis sociais), contactPoint

### Article/BlogPosting

Obrigatório: headline, image, datePublished, author
Recomendado: dateModified, publisher, description

### Product

Obrigatório: name, image, offers (preço + disponibilidade)
Recomendado: sku, brand, aggregateRating, review

### FAQPage

Obrigatório: mainEntity (array de pares Pergunta/Resposta)

### BreadcrumbList

Obrigatório: itemListElement (array com position, name, item)

---

## Múltiplos Tipos de Schema

Você pode combinar múltiplos tipos de schema em uma página usando `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validação e Testes

### Ferramentas

- **Teste de Rich Results do Google**: <https://search.google.com/test/rich-results>
- **Validador do Schema.org**: <https://validator.schema.org/>
- **Search Console**: relatórios de Aprimoramentos

### Erros Comuns

**Propriedades obrigatórias faltando** - Confira a documentação do Google para campos obrigatórios

**Valores inválidos** - Datas devem ser ISO 8601, URLs totalmente qualificadas, enumerações exatas

**Incompatibilidade com o conteúdo da página** - O schema não bate com o conteúdo visível

---

## Implementação

### Sites Estáticos

- Adicione JSON-LD diretamente no template HTML
- Use includes/partials para schema reutilizável

### Sites Dinâmicos (React, Next.js)

- Componente que renderiza o schema
- Renderizado no servidor para SEO
- Serialize dado para JSON-LD

### CMS / WordPress

- Plugins (Yoast, Rank Math, Schema Pro)
- Modificações de tema
- Campos customizados para dado estruturado

---

## Formato de Saída

### Implementação do Schema

```json
// Bloco de código JSON-LD completo
{
  "@context": "https://schema.org",
  "@type": "...",
  // Markup completo
}
```

### Checklist de Teste

- [ ] Valida no Teste de Rich Results
- [ ] Sem erros ou avisos
- [ ] Combina com o conteúdo da página
- [ ] Todas as propriedades obrigatórias incluídas

---

## Perguntas Específicas da Tarefa

1. Que tipo de página é essa?
2. Quais rich results você espera alcançar?
3. Que dado está disponível para popular o schema?
4. Já existe schema na página?
5. Qual é sua stack técnica?

---

## Skills Relacionadas

- **seo-audit**: Para SEO geral incluindo revisão de schema
- **ai-seo**: Para otimização de busca em IA (schema ajuda a IA a entender o conteúdo)
- **programmatic-seo**: Para schema templatizado em escala
- **site-architecture**: Para estrutura de breadcrumb e planejamento de schema de navegação
