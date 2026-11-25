---
name: "PocketBase Collections"
description: "Design de coleções e schemas para PocketBase. Use ao criar coleções, projetar schemas, adicionar campos, configurar relações ou escolher entre tipos de coleção base/auth/view. Previne tipos de campo errados, documenta comportamento padrão zero e aborda cascata de relações."
---

# Design de Coleção & Schema do PocketBase

## Tipos de Coleção

### Coleção Base
Coleção de dados padrão. Campos de sistema: `id`, `created`, `updated`.

### Coleção Auth
Estende a base com autenticação. Campos de sistema adicionais: `email`, `emailVisibility`, `verified`, `password`, `tokenKey`.

Não é possível deletar campos de sistema. Você pode desabilitar autenticação por email/senha nas opções da coleção.

### Coleção View
Somente leitura, apoiada por uma query SELECT SQL. Sem create/update/delete. Campos são auto-detectados da query. Útil para agregações, joins e views computadas.

```sql
-- Exemplo: query de coleção view
SELECT p.id, p.title, COUNT(c.id) as comments_count
FROM posts p LEFT JOIN comments c ON c.post = p.id
GROUP BY p.id
```

Coleções view suportam regras de API (list/view apenas) e podem ser usadas em relações.

## Tipos de Campo

| Tipo | Go type | Padrão zero | Notas |
|------|---------|-------------|-------|
| `text` | `string` | `""` | comprimento min/max, padrão regex |
| `editor` | `string` | `""` | Rich text (HTML sanitizado) |
| `number` | `float64` | `0` | min/max, opção `noDecimal` |
| `bool` | `bool` | `false` | |
| `email` | `string` | `""` | Formato auto-validado |
| `url` | `string` | `""` | Formato auto-validado |
| `date` | `string` | `""` | ISO 8601 (`2024-01-01 00:00:00.000Z`) |
| `select` | `string`/`[]string` | `""`/`[]` | lista de `values`, `maxSelect` |
| `file` | `string`/`[]string` | `""`/`[]` | `maxSelect`, `maxSize`, `mimeTypes` |
| `relation` | `string`/`[]string` | `""`/`[]` | `collectionId`, `cascadeDelete`, `maxSelect` |
| `json` | `any` | `null` | Único tipo que pode ser null! `maxSize` |
| `autodate` | `string` | auto | modificadores `onCreate`/`onUpdate` |
| `password` | `string` | `""` | Armazenado com hash, nunca retornado na API |

**Crítico**: todos os tipos têm padrão de seu valor zero, NÃO null. Apenas campos `json` podem ser null.

## Modificadores de Campo

Use em definições de schema de coleção:

- **`required`** — campo não pode estar vazio/zero
- **`unique`** — restrição de unicidade (composição via índices únicos)
- **`presentable`** — incluído na exibição de relação
- **`hidden`** — excluído de respostas da API a menos que explicitamente solicitado
- **`:autogenerate`** — para campos `text`: auto-gerar valor (ex: slug de outro campo)

## Padrões de Relação

### Um-para-muitos
```
posts.author -> users (maxSelect: 1)
```
Cada post tem um autor. Query posts por autor: `author = "USER_ID"`.

### Muitos-para-muitos
```
posts.tags -> tags (maxSelect: 0, significando ilimitado)
```
Relação multi-select. Filtro: `tags ?= "TAG_ID"` (contém).

### Relações reversas
Nenhum campo de relação reversa explícito necessário. Use `@collection.posts.author` em regras de API ou expanda de qualquer lado:
```
GET /api/collections/users/records/USER_ID?expand=posts_via_author
```

### Deletar em Cascata
Defina `cascadeDelete: true` no campo de relação. Quando o registro referenciado é deletado, todos os registros que apontam para ele também são deletados. O padrão é `false` (define para string vazia).

### Auto-referência
Uma coleção pode referenciar a si mesma:
```
categories.parent -> categories (maxSelect: 1)
```

## Índices

- Criados nas configurações de coleção (não em nível de campo)
- Formato: `CREATE [UNIQUE] INDEX idx_name ON collection (field1, field2)`
- Índices únicos forçam unicidade composta
- Índices parciais: `CREATE INDEX ... WHERE condition`
- Índices em campos de relação melhoram performance de joins

## Especificidades de Coleção Auth

### OAuth2
Habilite por provider nas configurações de coleção. Cada provider precisa de ID do cliente + secret. PocketBase lida com o fluxo OAuth2 completo.

### OTP (Senha De Uma Única Vez)
Habilite nas configurações de coleção auth. Envia código por email. Configure `otp.enabled`, `otp.duration`, `otp.length`.

### MFA (Autenticação Multi-Fator)
Habilite nas configurações de coleção auth. Exige um segundo fator após autenticação primária. `mfa.enabled`, `mfa.duration`, `mfa.rule` (filtro para determinar quais usuários precisam de MFA).

### Autenticação por Senha
Habilitada por padrão. Você pode customizar `minPasswordLength`. Pode desabilitar completamente se usar apenas OAuth2/OTP.

### Opções de Auth
- `authToken.duration` — lifetime do token (segundos)
- `passwordAuth.enabled` — alterna email/senha
- `passwordAuth.identityFields` — campos usados para login (padrão: `email`; pode adicionar `username`)
- `oauth2.enabled` — alterna OAuth2
- `otp.enabled` — alterna OTP

## Boas Práticas

1. **Prefira `select` em vez de `bool`** quando pode haver mais de 2 estados no futuro
2. **Use `relation` e não `text`** para chaves estrangeiras — você obtém cascata, expand e type safety
3. **Campos `json`** são sem schema — use com moderação, prefira campos tipados
4. **Nomeie coleções** em lowercase snake_case (ex: `blog_posts`, `user_profiles`)
5. **Indexe cedo** — adicione índices para qualquer campo usado em filtros ou ordenações
6. **`maxSelect: 1`** em relações retorna um ID string; **`maxSelect: >1` ou `0`** retorna um array