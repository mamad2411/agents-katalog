---
name: tpl-dominio-plataforma-conteudo
description: Template do pack (dominio/06-plataforma-conteudo.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/06-plataforma-conteudo.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Plataforma de Conteúdo / Blog / CMS

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/06-plataforma-conteudo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
CMS parece simples mas esconde armadilhas de SEO (URL canonical errada = duplicate content penalty),
performance (N+1 em listagem de posts com categorias) e consistência (draft publicado acidentalmente
por race condition). Rich text storage é frequentemente subestimado — escolhas erradas de formato
bloqueiam migration futura.

## STACK ASSUMPTIONS
- Editor: Tiptap (ProseMirror) ou Slate.js para rich text
- Backend: Node.js / Laravel / Django
- DB: PostgreSQL para conteúdo estruturado
- Storage: S3/GCS para imagens e attachments
- CDN: CloudFront / Cloudflare para assets + cache de páginas
- Search: Algolia ou Elasticsearch para pesquisa de conteúdo
- Queue: BullMQ / Sidekiq para CDN invalidation + indexação de busca assíncrona

## CORE CONCEPTS
- **Slug**: identificador URL do conteúdo — único, imutável após publicação
- **Draft/Publish Workflow**: separação entre rascunho (editável) e publicado (imutável no histórico)
- **Content Versioning**: snapshot de cada publicação para rollback
- **Canonical URL**: href canonical evita duplicate content com paginação/filtros
- **Sitemap.xml**: gerado dinamicamente, excluir noindex pages, submeter ao Google Search Console
- **CDN Invalidation**: limpar cache ao publicar/editar conteúdo
- **Rich Text Storage**: JSON (Tiptap) ou Markdown — nunca HTML puro no banco
- **Author Permissions**: owner pode publicar, editor precisa de revisão

## ARCHITECTURE RULES

### Content Model
```
Post
  ├── id (uuid)
  ├── slug (unique, indexed)
  ├── status (draft | review | scheduled | published | archived)
  ├── published_at (nullable)
  ├── current_version_id (fk → PostVersion)
  └── PostVersions (histórico imutável)
        ├── title, excerpt, content_json, meta_title, meta_description
        ├── featured_image_url
        └── created_at, created_by
```

### Draft/Publish Flow
- Draft: pode ser editado livremente, sem versão histórica até publicar
- Publicar: criar PostVersion snapshot → atualizar `current_version_id` → invalidar CDN
- Rollback: mudar `current_version_id` para versão anterior → invalidar CDN
- Scheduled: job agendado para publicar em `scheduled_at` → mesmo flow de publicação
- Nunca editar conteúdo de uma versão publicada — criar nova versão sempre

### Slug Management
- Gerar slug a partir do título no create (sanitize: lowercase, remove special chars, hifenize)
- Slug é editável apenas antes da primeira publicação
- Após publicado: criar `SlugRedirect` se mudar slug (301 para novo slug)
- Slug único global — checar collision antes de salvar

### SEO Fields
- Cada post: `meta_title` (max 60 chars), `meta_description` (max 160 chars), `canonical_url`
- `canonical_url` default: URL canônica do post (para não deixar em branco)
- `noindex` flag para drafts, arquivos e páginas paginadas futuras
- Sitemap.xml: incluir apenas posts publicados, com `lastmod` = `published_at`
- Open Graph: `og:title`, `og:description`, `og:image` separados dos meta tags SEO

### Rich Text Storage
- Armazenar como JSON nativo do editor (Tiptap JSON schema)
- Nunca armazenar HTML gerado — regenerar no render
- Assets embutidos no conteúdo: usar referências por ID (não URL direta)
- Sanitizar HTML no render (XSS — mesmo JSON pode ter link malicioso)

### CDN Invalidation
- Invalidar no publish: `/{slug}`, `/`, `/sitemap.xml`, `/feed.xml`
- Invalidar no unpublish: mesmos paths
- Usar wildcard com cuidado — `/*` invalida cache inteiro (caro e lento)
- Queue invalidation: não bloquear request de publicação, executar em background

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /posts | Criar post draft → gerar slug → validar unique |
| PATCH /posts/:id | Atualizar draft (se not published) ou criar novo draft pending |
| POST /posts/:id/publish | Snapshot → publicar → CDN invalidation → reindex busca |
| POST /posts/:id/unpublish | Retirar do ar → CDN invalidation → remover do sitemap |
| POST /posts/:id/schedule | Agendar publicação → criar job na queue |
| POST /posts/:id/rollback/:versionId | Restaurar versão anterior como current |
| GET /posts/:slug | Servir conteúdo publicado (CDN-cached) |
| GET /admin/posts?status=draft | Listar com paginação, filtro por status/author |
| POST /media/upload | Upload para S3 via signed URL → retornar media record |
| DELETE /media/:id | Soft delete → verificar referências antes → cleanup job |
| GET /sitemap.xml | Gerar dinamicamente (ou servir do cache com TTL 1h) |
| POST /comments | Criar comentário → status: pending (moderation) |
| PATCH /admin/comments/:id/approve | Aprovar comentário → publicar → notificar autor do post |

## CRITICAL RULES
1. Slug nunca muda após publicação sem criar redirecionamento 301
2. Conteúdo publicado é imutável no histórico — nova edição = nova versão
3. CDN invalidation sempre assíncrona — nunca bloquear request de publicação
4. HTML nunca armazenado no banco — apenas JSON do editor
5. `canonical_url` preenchido em 100% dos posts publicados
6. Deletar imagem só se não referenciada em nenhum conteúdo publicado
7. Scheduled posts: checar no job se ainda está `scheduled` antes de publicar (pode ter sido cancelado)
8. Comentários com moderação ativa antes de aparecer publicamente
9. Author sem permissão de publish deve criar post com status `review`
10. Media upload: validar tipo MIME no servidor (não apenas extensão)

## COMMON PITFALLS

### ❌ Slug mutável após publicação
```javascript
// ERRADO: SEO / links externos quebram
await post.update({ slug: newSlug }); // 404 para URLs indexadas

// CORRETO: criar redirect antes
await SlugRedirect.create({ from: post.slug, to: newSlug, postId: post.id });
await post.update({ slug: newSlug });
await invalidateCDN(post.slug); // invalidar URL antiga também
```

### ❌ HTML raw no banco
```sql
-- ERRADO: impossível migrar editor futuramente, XSS risk
UPDATE posts SET content = '<h1>Título</h1><p>Conteúdo com <script>evil()</script></p>';

-- CORRETO: JSON do editor
UPDATE posts SET content_json = '{"type":"doc","content":[{"type":"heading","content":[...]}]}';
-- HTML é gerado no render server-side com sanitização
```

### ❌ CDN invalidation síncrona
```javascript
// ERRADO: publicação demora 3s esperando CloudFront
await post.publish();
await cloudfront.createInvalidation({ paths: ['/*'] }); // bloqueia response

// CORRETO: async
await post.publish();
await queue.add('cdn-invalidate', { paths: [`/${post.slug}`, '/', '/sitemap.xml'] });
res.json({ ok: true }); // responde imediatamente
```

## QUALITY GATES
- [ ] 100% dos posts publicados com `canonical_url` preenchido
- [ ] Slug nunca alterado sem criar `SlugRedirect`
- [ ] Conteúdo armazenado como JSON (não HTML)
- [ ] CDN invalidation assíncrona via queue
- [ ] Sitemap.xml inclui apenas posts publicados com `noindex: false`
- [ ] Comentários passam por moderação antes de publicar
- [ ] Imagens não deletadas se referenciadas em conteúdo ativo
- [ ] Versioning funcional com rollback testado
- [ ] Meta tags SEO validadas (tamanho, campos obrigatórios)
- [ ] Scheduled posts verificam estado antes de publicar

## FORBIDDEN
- Armazenar HTML gerado pelo editor diretamente no banco de dados
- Alterar slug de post publicado sem criar redirecionamento
- CDN invalidation síncrona bloqueando requests de publicação
- Publicar imediatamente sem validar meta SEO obrigatórios
- Deletar mídia sem verificar referências em conteúdo publicado
- Comentários sem fluxo de moderação em plataformas abertas
