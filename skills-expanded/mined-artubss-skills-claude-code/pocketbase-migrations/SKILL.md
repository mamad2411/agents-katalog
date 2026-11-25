---
name: "PocketBase Migrations"
description: "Migrações de schema e versionamento para PocketBase. Use ao criar migrações, gerenciar versões de schema, sincronizar collections entre ambientes, usar automigrate ou criar collections programaticamente. Aborda comandos migrate, formato de arquivo de migração, importação de snapshots e a tabela _migrations de rastreamento."
---

# PocketBase Migrações & Versionamento de Schema

## Visão Geral

PocketBase suporta duas abordagens para gerenciamento de schema:

1. **Auto-migrate** (padrão em dev) — Alterações no Dashboard geram automaticamente arquivos de migração em `pb_migrations/`
2. **Migrações manuais** — escreva arquivos de migração manualmente para controle total

## Comandos CLI

```bash
# Criar um novo arquivo de migração vazio
./pocketbase migrate create "add_posts_collection"
# Cria: pb_migrations/1234567890_add_posts_collection.js

# Aplicar todas as migrações pendentes
./pocketbase migrate up

# Reverter a última migração aplicada
./pocketbase migrate down

# Gerar um snapshot completo de todas as collections atuais
./pocketbase migrate collections
# Cria um arquivo de migração que recria todas as collections do zero

# Sincronizar histórico de migrações com estado real do BD (marcar todas como aplicadas)
./pocketbase migrate history-sync
```

## Modo Auto-migrate

Ativado por padrão. Quando você altera collections no Dashboard, PocketBase gera automaticamente arquivos de migração em `pb_migrations/`.

```bash
# Iniciar com auto-migrate (padrão)
./pocketbase serve

# Desativar auto-migrate (produção)
./pocketbase serve --automigrate=0
```

**Fluxo de trabalho**:
1. Desenvolva com auto-migrate LIGADO — use o Dashboard para projetar schema
2. Arquivos de migração são gerados automaticamente em `pb_migrations/`
3. Faça commit desses arquivos no git
4. Deploy: migrações rodam automaticamente ao iniciar `serve`
5. Em produção: use `--automigrate=0` para evitar que alterações no Dashboard gerem novas migrações

## Formato de Arquivo de Migração

```js
// pb_migrations/1234567890_add_posts_collection.js

migrate(
    // UP — aplicar migração
    function(app) {
        var collection = new Collection({
            name: "posts",
            type: "base",
            fields: [
                { name: "title", type: "text", required: true },
                { name: "body", type: "editor" },
                { name: "author", type: "relation", collectionId: "USERS_COLLECTION_ID", cascadeDelete: false, maxSelect: 1, required: true },
                { name: "status", type: "select", values: ["draft", "published", "archived"] },
                { name: "published_at", type: "date" },
                { name: "tags", type: "relation", collectionId: "TAGS_COLLECTION_ID", maxSelect: 0 }
            ],
            indexes: [
                "CREATE INDEX idx_posts_author ON posts (author)",
                "CREATE INDEX idx_posts_status ON posts (status)",
                "CREATE UNIQUE INDEX idx_posts_title ON posts (title)"
            ],
            listRule: "",   // AVISO: "" significa acesso público — use um filtro ou null para restringir
            viewRule: "",   // AVISO: "" significa acesso público — use um filtro ou null para restringir
            createRule: "@request.auth.id != ''",
            updateRule: "author = @request.auth.id",
            deleteRule: "author = @request.auth.id"
        })
        app.save(collection)
    },
    // DOWN — reverter migração
    function(app) {
        var collection = app.findCollectionByNameOrId("posts")
        app.delete(collection)
    }
)
```

**Importante**: o `app` dentro de migrações é uma instância transacional. Se algum erro ocorrer, toda a migração é revertida.

## Criando Collections Programaticamente

### Collection base

```js
var collection = new Collection({
    name: "posts",
    type: "base",
    fields: [
        { name: "title", type: "text", required: true, min: 3, max: 200 },
        { name: "slug", type: "text", required: true, autogenerate: { pattern: "slugify(title)" } },
        { name: "body", type: "editor" },
        { name: "cover", type: "file", maxSelect: 1, maxSize: 5242880, mimeTypes: ["image/jpeg", "image/png", "image/webp"] },
        { name: "views", type: "number", min: 0 },
        { name: "metadata", type: "json", maxSize: 2000000 },
        { name: "featured", type: "bool" },
        { name: "published_at", type: "date" }
    ]
})
app.save(collection)
```

### Collection auth

```js
var collection = new Collection({
    name: "users",
    type: "auth",
    fields: [
        { name: "name", type: "text", required: true },
        { name: "avatar", type: "file", maxSelect: 1, maxSize: 5242880 },
        { name: "role", type: "select", values: ["user", "editor", "admin"], required: true }
    ],
    passwordAuth: { enabled: true, identityFields: ["email", "username"] },
    oauth2: { enabled: true },
    otp: { enabled: false },
    mfa: { enabled: false },
    authToken: { duration: 604800 }  // 7 dias
})
app.save(collection)
```

### Collection view

```js
var collection = new Collection({
    name: "posts_stats",
    type: "view",
    viewQuery: "SELECT p.id, p.title, COUNT(c.id) as comments_count, p.views FROM posts p LEFT JOIN comments c ON c.post = p.id GROUP BY p.id",
    listRule: "",
    viewRule: ""
})
app.save(collection)
```

## Modificando Collections Existentes

```js
migrate(function(app) {
    var collection = app.findCollectionByNameOrId("posts")

    // Adicionar um novo campo
    collection.fields.add({
        name: "subtitle",
        type: "text",
        max: 500
    })

    // Remover um campo
    collection.fields.removeByName("old_field")

    // Atualizar regras de API
    collection.listRule = "@request.auth.id != ''"
    collection.viewRule = ""

    // Adicionar índice
    collection.indexes.push("CREATE INDEX idx_posts_subtitle ON posts (subtitle)")

    app.save(collection)
}, function(app) {
    var collection = app.findCollectionByNameOrId("posts")
    collection.fields.removeByName("subtitle")
    app.save(collection)
})
```

## SQL Bruto em Migrações

```js
migrate(function(app) {
    app.db().newQuery("ALTER TABLE posts ADD COLUMN legacy_id TEXT DEFAULT ''").execute()
    app.db().newQuery("UPDATE posts SET legacy_id = id WHERE legacy_id = ''").execute()
}, function(app) {
    app.db().newQuery("ALTER TABLE posts DROP COLUMN legacy_id").execute()
})
```

**Aviso**: SQL bruto contorna o cache de schema do PocketBase. Execute `migrate collections` posteriormente para re-sincronizar se necessário.

## Configurações & Superuser em Migrações

### Inicializar configurações de app

```js
onBootstrap(function(e) {
    var settings = e.app.settings()
    settings.meta.appName = "My App"
    settings.meta.appURL = "https://myapp.com"
    settings.meta.senderName = "My App"
    settings.meta.senderAddress = "noreply@myapp.com"
    settings.smtp.enabled = true
    settings.smtp.host = "smtp.example.com"
    settings.smtp.port = 587
    settings.smtp.username = $os.getenv("SMTP_USER")
    settings.smtp.password = $os.getenv("SMTP_PASS")
    e.app.save(settings)
    return e.next()
})
```

### Criar superuser em migração

```js
migrate(function(app) {
    var superusers = app.findCollectionByNameOrId("_superusers")
    var record = new Record(superusers)
    // IMPORTANTE: sempre defina as variáveis de ambiente PB_ADMIN_EMAIL e PB_ADMIN_PASSWORD
    var email = $os.getenv("PB_ADMIN_EMAIL")
    var password = $os.getenv("PB_ADMIN_PASSWORD")
    if (!email || !password) {
        throw new Error("PB_ADMIN_EMAIL and PB_ADMIN_PASSWORD env vars are required")
    }
    record.set("email", email)
    record.set("password", password)
    app.save(record)
})
```

## Migrações de Snapshot

`./pocketbase migrate collections` gera um snapshot completo — útil para:
- Bootstrap de um novo ambiente
- Resetar histórico de migrações
- Revisar schema completo em um arquivo

O arquivo gerado usa `app.importCollections(collections)` que suporta dois modos:
- **Padrão (merge/extend)**: adiciona novas collections e campos, atualiza as existentes, não deleta nada
- **Deletar faltantes**: `app.importCollections(collections, true)` — deleta collections/campos que não estão no snapshot

## Tabela `_migrations`

PocketBase rastreia migrações aplicadas na tabela interna `_migrations`:
- `id` — auto-gerado
- `file` — nome do arquivo de migração
- `applied` — timestamp

`migrate history-sync` marca todos os arquivos de migração existentes como aplicados sem executá-los — útil ao importar um banco de dados existente.

## Melhores Práticas

1. **Dev**: use auto-migrate + Dashboard para projetar schema, faça commit dos arquivos gerados
2. **Staging/Prod**: deploy com `--automigrate=0`, migrações rodam ao iniciar
3. **Sempre escreva migrações DOWN** — reversibilidade economiza você quando algo dá errado
4. **Uma preocupação por migração** — não misture alterações de schema não relacionadas
5. **Teste migrações**: aplique em uma cópia de dados de produção antes de fazer deploy
6. **Use `migrate collections`** periodicamente para fazer snapshot do estado atual para documentação
7. **Nunca edite migrações aplicadas** — crie uma nova migração para corrigir problemas
8. **Dados de seed**: prefira uma migração dedicada para dados iniciais únicos; se usar `onBootstrap`, faça a lógica de seed idempotente (verificações de existência/upserts) porque bootstrap executa a cada inicialização do app