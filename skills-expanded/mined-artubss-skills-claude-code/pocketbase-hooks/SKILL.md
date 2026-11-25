---
name: "PocketBase Hooks"
description: "Hooks JavaScript do lado do servidor para PocketBase (pb_hooks). Use ao escrever rotas customizadas, event hooks, cron jobs, envio de emails, requisições HTTP, consultas ao banco de dados ou estender PocketBase com lógica do lado do servidor. Abrange o runtime goja ES5, roteamento, middleware, todos os event hooks, consultas de DB, operações de registros e APIs globais."
---

# JavaScript do Lado do Servidor do PocketBase (pb_hooks)

## Fundamentos do Runtime

- Arquivos vão em `pb_hooks/*.pb.js` (devem terminar com `.pb.js`)
- Engine: **goja** — ES5.1 + alguns ES6. **Sem módulos ES6** (`import`/`export`), **sem async/await**, **sem arrow functions em versões antigas**. Use `function(){}` e CommonJS `require()`.
- Cada arquivo é carregado ao iniciar a app e em hot-reload
- `__hooks` — caminho absoluto para o diretório pb_hooks
- Declarações TypeScript: `pb_data/types.d.ts` (auto-geradas, úteis para suporte de IDE)
- Flag `--hooksPool=25` controla goroutines JS concorrentes (padrão: 25)
- Cada handler roda em um contexto isolado — sem estado mutável compartilhado entre requisições

## Roteamento

### Adicionando rotas

```js
routerAdd("GET", "/api/hello/{name}", function(e) {
    var name = e.request.pathValue("name")
    return e.json(200, { "message": "Hello " + name })
}, /* optional middleware */)
```

### Padrões de caminho
- `{name}` — parâmetro de caminho nomeado
- `{path...}` — wildcard (corresponde ao resto do caminho)
- `{$}` — correspondência exata (sem barra final)

### Métodos de resposta

| Método | Uso |
|--------|-----|
| `e.json(status, data)` | Resposta JSON |
| `e.string(status, text)` | Texto simples |
| `e.html(status, html)` | Resposta HTML |
| `e.redirect(status, url)` | Redirecionamento (301/302) |
| `e.blob(status, contentType, bytes)` | Dados binários |
| `e.stream(status, contentType, reader)` | Resposta com streaming |
| `e.noContent(status)` | Sem corpo (204) |

### Lendo dados da requisição

```js
// Corpo (JSON)
var body = new DynamicModel({ name: "", age: 0 })
e.bindBody(body)

// Query params
var page = e.request.url.query().get("page")

// Headers
var token = e.request.header.get("Authorization")

// Arquivos enviados
var files = e.findUploadedFiles("document")  // retorna array de *filesystem.File

// Estado de autenticação
var user = e.auth          // registro de auth atual ou null
var isSuper = e.hasSuperuserAuth()
```

## Middleware

### Middleware built-in

```js
routerAdd("GET", "/api/protected", handler,
    $apis.requireAuth(),                // qualquer usuário autenticado
    // OU
    $apis.requireAuth("users"),         // apenas coleção "users"
    // OU
    $apis.requireSuperuserAuth(),       // apenas superusers
    // OU
    $apis.requireGuestOnly(),           // apenas não autenticado
    // OU
    $apis.bodyLimit(5 * 1024 * 1024),   // limite de corpo 5MB
    // OU
    $apis.gzip()                        // compressão gzip
)
```

### Middleware global

```js
routerUse(function(e) {
    // roda antes de toda requisição
    console.log(e.request.method, e.request.url.path)
    return e.next()  // DEVE chamar e.next() para continuar
})
```

### Middleware de rota customizada

```js
function myMiddleware(e) {
    // pré-processamento
    var result = e.next()  // chama o próximo handler
    // pós-processamento
    return result
}

routerAdd("GET", "/api/test", handler, myMiddleware)
```

Prioridade: middleware roda em ordem — primeira registrada, primeira executada.

## Event Hooks

### Ciclo de vida do registro

Cada evento de registro tem 3 variantes:
- `onRecord*Execute` — envolve a ação padrão. Chame `e.next()` para continuar.
- `onRecord*AfterSuccess` — roda após execução bem-sucedida
- `onRecord*AfterError` — roda após erro de execução

```js
// Antes/durante criação
onRecordCreateExecute(function(e) {
    // e.record — o registro sendo criado
    e.record.set("status", "pending")
    return e.next()  // continua com a criação
}, "posts")  // filtro de coleção opcional

// Após criação bem-sucedida
onRecordAfterCreateSuccess(function(e) {
    // e.record — o registro criado (tem ID agora)
    console.log("Criado:", e.record.id)
}, "posts")

// Após falha na criação
onRecordAfterCreateError(function(e) {
    // e.error — o erro
    console.log("Falhou:", e.error)
}, "posts")
```

### Todos os hooks de registro

| Hook | Campos do objeto evento |
|------|------------------------|
| `onRecordCreateExecute` | `e.record` |
| `onRecordUpdateExecute` | `e.record` |
| `onRecordDeleteExecute` | `e.record` |
| `onRecordAfterCreateSuccess` | `e.record` — após criação bem-sucedida |
| `onRecordAfterUpdateSuccess` | `e.record` — após atualização bem-sucedida |
| `onRecordAfterDeleteSuccess` | `e.record` — após exclusão bem-sucedida |
| `onRecordAfterCreateError` | `e.record`, `e.error` — após falha na criação |
| `onRecordAfterUpdateError` | `e.record`, `e.error` — após falha na atualização |
| `onRecordAfterDeleteError` | `e.record`, `e.error` — após falha na exclusão |
| `onRecordValidate` | `e.record` — adiciona erros de validação customizados |
| `onRecordEnrich` | `e.record` — modifica resposta da API (oculta/adiciona campos) |
| `onRecordsListRequest` | `e.records`, `e.result` — modifica resposta da lista |
| `onRecordRequestCreate` | `e.record` — durante requisição de criação da API |
| `onRecordRequestUpdate` | `e.record` — durante requisição de atualização da API |
| `onRecordRequestDelete` | `e.record` — durante requisição de exclusão da API |

### Auth hooks

```js
onRecordAuthWithPasswordRequest(function(e) {
    // e.record — o registro de auth
    // e.password — a senha fornecida
    return e.next()
}, "users")

onRecordAuthWithOAuth2Request(function(e) {
    // e.record — o registro de auth (pode ser novo)
    // e.oAuth2User — dados do usuário OAuth2
    // e.isNewRecord — true se primeiro login OAuth2
    return e.next()
}, "users")

onRecordAuthWithOTPRequest(function(e) {
    // e.record — o registro de auth
    return e.next()
}, "users")

onRecordAuthRefreshRequest(function(e) {
    return e.next()
}, "users")
```

### Hooks de realtime

```js
onRealtimeConnectRequest(function(e) {
    // e.client — o cliente SSE
    // e.idleTimeout — timeout da conexão
    return e.next()
})

onRealtimeSubscribeRequest(function(e) {
    // e.client
    // e.subscriptions — subscriptions solicitadas
    return e.next()
})
```

### Outros hooks

```js
onFileDownloadRequest(function(e) {
    // e.record, e.fileField, e.servedPath, e.servedName
    return e.next()
}, "documents")

onBatchRequest(function(e) {
    // e.batch — array de sub-requisições
    return e.next()
})

onCollectionCreateExecute(function(e) {
    // e.collection
    return e.next()
})

// Ciclo de vida da app
onBootstrap(function(e) {
    // roda uma vez ao iniciar a app (após DB estar pronto)
    return e.next()
})

onTerminate(function(e) {
    // roda no encerramento gracioso
    return e.next()
})
```

### Hook de validação

```js
onRecordValidate(function(e) {
    if (e.record.getString("title").length < 3) {
        e.error = new ValidationError("title", "Title must be at least 3 characters")
    }
    return e.next()
}, "posts")
```

### Hook de enrich (modifica resposta da API)

```js
onRecordEnrich(function(e) {
    // Oculta campo de não-proprietários
    if (!e.requestInfo.auth || e.requestInfo.auth.id !== e.record.getString("author")) {
        e.record.hide("private_notes")
    }
    // Adiciona campo computado
    e.record.withCustomData(true)
    e.record.set("displayName", e.record.getString("first") + " " + e.record.getString("last"))
    return e.next()
}, "users")
```

## Banco de Dados

### Query builder

```js
var results = arrayOf(new DynamicModel({ id: "", title: "", count: 0 }))

$app.db()
    .select("id", "title", "COUNT(comments) as count")
    .from("posts")
    .where($dbx.hashExp({ status: "active" }))
    .andWhere($dbx.like("title", "hello"))
    .orderBy("created DESC")
    .limit(10)
    .offset(0)
    .all(results)  // popula array results
```

### Métodos de execução

| Método | Retorno |
|--------|---------|
| `.all(results)` | Popula array |
| `.one(result)` | Registro único |
| `.execute()` | Para INSERT/UPDATE/DELETE |

### Queries brutas

```js
$app.db().newQuery("SELECT * FROM posts WHERE status = {:status}")
    .bind({ status: "active" })
    .all(results)
```

**Sempre use parâmetros nomeados `{:param}`** — nunca concatene strings SQL.

### Expressões $dbx

```js
$dbx.hashExp({ field: "value" })           // field = "value"
$dbx.hashExp({ field: ["a", "b"] })        // field IN ("a", "b")
$dbx.not($dbx.hashExp({ field: "value" })) // NOT (field = "value")
$dbx.and(expr1, expr2)                     // expr1 AND expr2
$dbx.or(expr1, expr2)                      // expr1 OR expr2
$dbx.like("field", "val")                  // field LIKE "%val%"
$dbx.orLike("field", "a", "b")            // field LIKE "%a%" OR field LIKE "%b%"
$dbx.notLike("field", "val")              // field NOT LIKE "%val%"
$dbx.in("field", "a", "b", "c")           // field IN ("a", "b", "c")
$dbx.notIn("field", "a", "b")             // field NOT IN ("a", "b")
$dbx.between("field", 1, 10)              // field BETWEEN 1 AND 10
$dbx.exists($dbx.exp("SELECT 1 FROM t WHERE ..."))
$dbx.exp("raw SQL expression", optionalParams)
```

### Transações

```js
$app.runInTransaction(function(txApp) {
    // use txApp em vez de $app dentro da transação
    var record = txApp.findRecordById("posts", "RECORD_ID")
    record.set("views", record.getInt("views") + 1)
    txApp.save(record)
})
```

## Operações de Registro

### Encontrando registros

```js
// Por ID
var record = $app.findRecordById("posts", "RECORD_ID")

// Por valor de campo
var record = $app.findFirstRecordByData("users", "email", "user@example.com")

// Por expressão de filtro (mesma sintaxe das regras da API)
var record = $app.findFirstRecordByFilter("posts", "slug = {:slug}", { slug: "my-post" })

// Múltiplos registros com filtro
var records = $app.findRecordsByFilter(
    "posts",                    // coleção
    "status = 'active'",        // filtro
    "-created",                 // ordenação
    10,                         // limite
    0                           // offset
)

// Todos os registros (sem limite)
var records = $app.findAllRecords("posts", $dbx.hashExp({ status: "active" }))

// Contagem
var total = $app.countRecords("posts", $dbx.hashExp({ status: "active" }))
```

### Criando registros

```js
var collection = $app.findCollectionByNameOrId("posts")
var record = new Record(collection)
record.set("title", "My Post")
record.set("author", "USER_ID")
record.set("tags", ["tag1", "tag2"])  // multi-relação
$app.save(record)
// record.id agora está definido
```

### Atualizando registros

```js
var record = $app.findRecordById("posts", "RECORD_ID")
record.set("title", "Updated Title")
$app.save(record)
```

### Deletando registros

```js
var record = $app.findRecordById("posts", "RECORD_ID")
$app.delete(record)
```

### Getters de registro

```js
record.id
record.getString("title")
record.getInt("count")
record.getFloat("price")
record.getBool("active")
record.getStringSlice("tags")  // para campos com múltiplos valores
record.getDateTime("created")  // retorna objeto DateTime
record.get("field")            // valor bruto interface{}
```

### Expandindo relações

```js
$app.expandRecord(record, ["author", "tags"], null)
var author = record.expandedOne("author")   // relação única
var tags = record.expandedAll("tags")        // relação múltipla
```

### Operações de arquivo

```js
// Atribui arquivo de caminho
var file = $filesystem.fileFromPath("/path/to/file.pdf")
record.set("document", file)

// Atribui arquivo de bytes
var file = $filesystem.fileFromBytes(byteArray, "report.pdf")
record.set("document", file)

// Atribui arquivo de URL
var file = $filesystem.fileFromURL("https://example.com/file.pdf")
record.set("document", file)

$app.save(record)
```

## Cron Jobs

```js
cronAdd("daily_cleanup", "0 3 * * *", function() {
    // roda todo dia às 3:00 AM
    var old = $app.findRecordsByFilter("temp", "created < @now - 30d", "", 0, 0)
    for (var i = 0; i < old.length; i++) {
        $app.delete(old[i])
    }
})

cronRemove("daily_cleanup")  // remove um job registrado anteriormente
```

Expressões cron: `minuto hora dia mês dia_da_semana`
Preview de crons registrados: Dashboard > Settings > Crons

## Email

```js
var message = new MailerMessage()
message.from = { address: $app.settings().meta.senderAddress, name: $app.settings().meta.senderName }
message.to = [{ address: "user@example.com", name: "User" }]
message.subject = "Hello"
message.html = "<h1>Hello World</h1>"
// message.bcc, message.cc — arrays opcionais
// message.attachments — opcional

$app.newMailClient().send(message)
```

### Customizando emails do sistema

```js
onMailerRecordVerificationSend(function(e) {
    // e.record, e.message
    e.message.subject = "Custom verification subject"
    e.message.html = "<p>Custom HTML with token: " + e.meta.token + "</p>"
    return e.next()
}, "users")

// Hooks similares: onMailerRecordResetPasswordSend, onMailerRecordEmailChangeSend, onMailerRecordOTPSend
```

## HTTP Client

```js
var res = $http.send({
    url: "https://api.example.com/data",
    method: "POST",
    body: JSON.stringify({ key: "value" }),
    headers: { "Content-Type": "application/json", "Authorization": "Bearer TOKEN" },
    timeout: 30  // segundos
})

// Resposta
res.statusCode  // número
res.json         // JSON parseado (se aplicável)
res.headers      // objeto
res.cookies      // objeto
res.body         // string bruta

// Upload multipart
var formData = new FormData()
formData.append("file", $filesystem.fileFromPath("/path/to/file.pdf"))
formData.append("name", "test")

var res = $http.send({
    url: "https://api.example.com/upload",
    method: "POST",
    body: formData
})
```

**Sem suporte a streaming** em `$http.send()`.

## Tipos de Erro

```js
throw new BadRequestError("message", optionalData)     // 400
throw new UnauthorizedError("message", optionalData)    // 401
throw new ForbiddenError("message", optionalData)       // 403
throw new NotFoundError("message", optionalData)        // 404
throw new TooManyRequestsError("message", optionalData) // 429
throw new InternalServerError("message", optionalData)  // 500
throw new ApiError(statusCode, "message", optionalData) // status customizado

// Erros de validação (para onRecordValidate)
new ValidationError("field_name", "error message")
```

## Objetos Globais

| Objeto | Propósito |
|--------|-----------|
| `$app` | Instância principal da app — DB, registros, coleções, settings |
| `$apis` | Helpers de middleware da API |
| `$security` | JWT, encriptação, geração de string aleatória |
| `$os` | Operações de SO: `$os.exec()`, `$os.readDir()`, `$os.tempDir()` |
| `$http` | HTTP client |
| `$filesystem` | Helpers de arquivo (`fileFromPath`, `fileFromBytes`, `fileFromURL`) |
| `$dbx` | SQL expression builders |

### Exemplos de $security

```js
var token = $security.randomString(32)
var hash = $security.hs256("data", "secret")
var encrypted = $security.encrypt("data", "encryptionKey")
var decrypted = $security.decrypt(encrypted, "encryptionKey")
```

### Exemplos de $os

```js
var result = $os.exec("ls", ["-la", "/tmp"])  // retorna { code, output }
var files = $os.readDir("/path")
var tmp = $os.tempDir("prefix")
```

## Padrões Comuns

### Auto-atribuir autor na criação

```js
onRecordCreateExecute(function(e) {
    if (e.auth) {
        e.record.set("author", e.auth.id)
    }
    return e.next()
}, "posts")
```

### Cascata de lógica customizada na deleção

```js
onRecordDeleteExecute(function(e) {
    // Limpa dados relacionados não gerenciados por cascadeDelete
    var comments = $app.findRecordsByFilter("comments", "post = {:id}", "-created", 0, 0, { id: e.record.id })
    for (var i = 0; i < comments.length; i++) {
        $app.delete(comments[i])
    }
    return e.next()
}, "posts")
```

### Rate limiting por usuário

```js
routerAdd("POST", "/api/expensive-action", function(e) {
    var recent = $app.countRecords("actions",
        $dbx.hashExp({ user: e.auth.id }),
        $dbx.exp("created > {:cutoff}", { cutoff: new DateTime().sub(1 * 60) })  // último minuto
    )
    if (recent >= 5) {
        throw new TooManyRequestsError("Rate limit exceeded")
    }
    // prossegue com ação
    return e.json(200, { ok: true })
}, $apis.requireAuth())
```

### Webhook na mudança de registro

```js
onRecordCreateAfterSuccessExecute(function(e) {
    try {
        $http.send({
            url: "https://hooks.example.com/webhook",
            method: "POST",
            body: JSON.stringify({
                event: "record.create",
                collection: e.record.collection().name,
                record: e.record
            }),
            headers: { "Content-Type": "application/json" },
            timeout: 10
        })
    } catch (err) {
        console.log("Webhook failed:", err)
    }
})
```