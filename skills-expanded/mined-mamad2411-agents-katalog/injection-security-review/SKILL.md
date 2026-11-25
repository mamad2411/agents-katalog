---
name: injection-security-review
version: 1.0.0
description: >
  Revisão de segurança em nível de código-fonte focada exclusivamente em
  vetores de injeção e técnicas de bypass de sanitização.
  Ative ao receber código para auditoria de segurança ou ao investigar
  vulnerabilidades de injeção em qualquer linguagem/framework.
triggers:
  - "revisar segurança"
  - "auditoria de segurança"
  - "revisão de injeção"
  - "bypass de sanitização"
  - "analisar vulnerabilidade"
  - "code review de segurança"
  - "encontrar injection"
  - "SQL injection"
  - "XSS"
  - "command injection"
  - "/security-review"
  - "/audit-injection"
---

# INJECTION SECURITY REVIEW — Caça a vetores de injeção e bypass de sanitização em nível de código

> **Propósito**: Receber código-fonte, executar revisão sistemática por vetores de injeção,
> testar cada sanitização contra técnicas de bypass conhecidas e entregar
> relatório estruturado com severidade, prova de conceito e correção exata.

---

## Filosofia Central

1. **Dado não confiável por padrão** — Toda entrada externa é maliciosa até prova em contrário.
   Na prática: rastrear cada variável desde a entrada (HTTP, DB, arquivo, env) até o sink; se o caminho não tem sanitização parametrizada, é vulnerável.

2. **Sanitização é contexto-dependente** — O que saneia para HTML não saneia para SQL nem para shell.
   Na prática: nunca aceitar uma função "sanitize()" genérica; verificar se o escape corresponde ao sink exato (html_escape para template, parameterized query para SQL, etc.).

3. **Encoding não é sanitização** — Um valor codificado em HTML pode ser decodificado pelo browser; base64 pode ser decodificado pelo parser.
   Na prática: tratar encoding como transformação de representação, não como barreira de segurança.

4. **Bypass é iterativo** — Toda sanitização tem pelo menos um edge case não coberto.
   Na prática: testar sempre com double-encoding, unicode normalization, null bytes, homoglyphs e variações de case.

5. **O sink define o risco** — Dado não sanitizado em um log é risco baixo; o mesmo dado em `eval()` é risco crítico.
   Na prática: classificar severidade pelo par (vetor × sink), não pelo vetor isolado.

6. **Prova ou silêncio** — Nunca relatar vulnerabilidade sem snippet reproduzível.
   Na prática: cada finding deve ter input malicioso → código vulnerável → output inseguro, em sequência demonstrável.

---

## Quando Ativar

### ✅ Ativar para:
- Revisar código-fonte por vulnerabilidades de injeção
- Investigar report de vulnerabilidade recebido (bug bounty, pentest)
- Validar se uma sanitização implementada resiste a bypass
- Code review de PR que toca em parsing, queries dinâmicas, templates ou execução de comando
- Análise de código que recebe input de usuário e o encaminha para sink perigoso
- Revisar library/helper de sanitização interno

### ❌ NÃO ativar para:
- Falhas de autenticação/autorização → use `auth-review`
- Configuração de WAF, CORS, CSP, headers de segurança → use `infra-security`
- Criografia fraca, gestão de chaves, JWT → use `crypto-review`
- Vulnerabilidades de rede (SSRF, CSRF) que não envolvam injeção → responda diretamente
- Análise de dependências (npm audit, SCA) → responda diretamente

---

## Escopo e Limites

### Coberto por esta skill:
| Vetor | Sinks típicos |
|---|---|
| SQL Injection | `query()`, `execute()`, `raw()`, string concatenation em SQL |
| NoSQL Injection | `$where`, `$regex`, `$ne`, `findOne()` com objeto do usuário |
| XSS (Stored/Reflected/DOM) | `innerHTML`, `document.write`, template literals em DOM, `v-html` |
| Command Injection | `exec()`, `spawn()`, `system()`, `popen()`, backticks |
| SSTI | `render()`, `compile()`, `template()` com string do usuário |
| Path Traversal | `fs.readFile()`, `open()`, `include/require` com concatenação |
| LDAP Injection | `search()`, filtros com concatenação de input |
| XPath Injection | `evaluate()`, `selectNodes()` com concatenação |
| HTTP Header Injection | `setHeader()`, `Location:`, `Set-Cookie:` com input |
| Log Injection | `logger.info()`, `console.log()` com input sem newlines |
| Sanitization Bypass | Qualquer função de escape/sanitize/encode como alvo |

### Delegado para outras skills:
| Fora do escopo | Delegar para |
|---|---|
| RBAC/ABAC bypass | `auth-review` |
| TLS, HSTS, cookie flags | `infra-security` |
| Deserialization | `crypto-review` |

---

## Protocolo de Execução

### Fase 1 — Ingestão e Parse

1. **Receber o código-alvo** — Identificar linguagem, framework, versão.
   - Se o usuário enviou arquivos: ler cada um via `file-reading`.
   - Se o usuário enviou snippet inline: usar diretamente.
   - Se o usuário enviou repositório: solicitar os arquivos específicos ou listar estrutura.
   - **Critério de conclusão**: linguagem e framework identificados, todos os arquivos relevantes carregados.

2. **Mapear superfície de entrada (Sources)** — Listar todos os pontos onde dados externos entram.
   - HTTP: `req.body`, `req.query`, `req.params`, `req.headers`, cookies, `formData`
   - Storage: resultados de DB, mensagens de queue, cache
   - Filesystem: `readFile()`, argumentos de CLI, variáveis de ambiente não-controladas
   - **Critério de conclusão**: tabela de sources com localização no código (arquivo:linha).

3. **Mapear superfície de saída (Sinks)** — Listar todos os pontos onde dados fluem para interpretadores.
   - SQL: chamadas a query builders com strings dinâmicas
   - Shell: chamadas a `exec`/`spawn`/`system`
   - HTML: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|raw` em templates
   - Templates: `render_string()`, `Template(user_string).render()`
   - Filesystem: `readFile(path + user_input)`, `include(user_input)`
   - **Critério de conclusão**: tabela de sinks com localização no código (arquivo:linha).

4. **Traçar fluxos source→sink** — Para cada source, seguir o dado até cada sink alcançável.
   - Usar análise estática mental: variável passa por sanitize? Por concatenação? Por template literal?
   - Marcar cada fluxo como: **PARAMETRIZADO** | **SANITIZADO** | **VULNERÁVEL**
   - **Critério de conclusão**: lista de fluxos com classificação.

### Fase 2 — Ataque Sistemático

5. **Classificar cada fluxo VULNERÁVEL por tipo de injeção** — Usar a taxonomia da seção "Padrões".
   - **Critério de conclusão**: cada fluxo vulnerável rotulado com tipo exato (SQLi-Classic, XSS-DOM-Stored, etc.).

6. **Testar cada sanitização contra bypass** — Para cada fluxo marcado SANITIZADO, tentar bypass:
   - Executar os testes da seção "Técnicas de Bypass de Sanitização".
   - Verificar se o escape é contextual (escape HTML usado em contexto SQL = bypass).
   - **Critério de conclusão**: cada sanitização classificada como EFETIVA ou BYPASSÁVEL, com prova.

7. **Montar prova de conceito para cada finding** — Sequência input → código → output.
   - Input: o payload exato que explora a vulnerabilidade
   - Código: o trecho vulnerável com highlight da linha exata
   - Output: o resultado inseguro (query executada, HTML renderizado, comando executado)
   - **Critério de conclusão**: cada finding tem PoC completo e reproduzível.

### Fase 3 — Resiliência e Casos Excepcionais

8. **Testar edge cases de resiliência** — Aplicar os cenários da seção "Casos de Exceção e Resiliência".
   - Input vazio, null, undefined, array em vez de string, objeto aninhado, input extremamente longo
   - Multi-byte characters, BOM, RTL override, zero-width characters
   - **Critério de conclusão**: cada edge case documentado com comportamento observado.

9. **Verificar mitigação de erro** — Se o código tem try/catch, verificar se o erro vaza informação útil.
   - Stack traces expostos contêm nomes de tabela, queries parciais, caminhos de arquivo
   - **Critério de conclusão**: erros classificados como "seguros" ou "information leak".

### Fase 4 — Geração do Artefato

10. **Classificar severidade** — Usar escala fixa:
    - **CRÍTICO**: exploração trivial, impacto imediato (RCE, exfileração de DB inteiro)
    - **ALTO**: exploração requer conhecimento mínimo, impacto significativo
    - **MÉDIO**: exploração requer condições específicas, impacto limitado
    - **BAIXO**: exploração teórica, impacto mínimo (ex: log injection sem consumo downstream)
    - **Critério de conclusão**: cada finding com severidade justificada em 1 frase.

11. **Escrever correção exata** — Para cada finding, fornecer o diff exato (antes → depois).
    - Nunca sugerir "use sanitize" genérico.
    - Sempre especificar a função exata, o contexto e a versão mínima da lib.
    - **Critério de conclusão**: cada finding tem diff aplicável sem interpretação.

12. **Montar relatório final** — Estrutura fixa (ver seção "Formato do Artefato de Saída").
    - **Critério de conclusão**: relatório completo, formatado em markdown, pronto para consumo.

---

## Padrões Específicos

### Padrão 1 — SQL Injection via Concatenação

**Regra**: Nunca interpolar variáveis em string SQL. Use sempre parameterized queries ou query builder com binding.

```javascript
// ✅ PASS — parameterized query
const result = await db.query('SELECT id, name FROM users WHERE email = $1', [userEmail]);

// ❌ FAIL — concatenação direta
const result = await db.query(`SELECT id, name FROM users WHERE email = '${userEmail}'`);

// ❌ FAIL — template literal
const result = await db.query(`SELECT id, name FROM users WHERE email = ${userEmail}`);
```

```python
# ✅ PASS — parameterized
cursor.execute("SELECT id, name FROM users WHERE email = %s", (user_email,))

# ❌ FAIL — f-string
cursor.execute(f"SELECT id, name FROM users WHERE email = {user_email}")

# ❌ FAIL — string format
cursor.execute("SELECT id, name FROM users WHERE email = '%s'" % user_email)
```

```java
// ✅ PASS — PreparedStatement
PreparedStatement stmt = conn.prepareStatement("SELECT id, name FROM users WHERE email = ?");
stmt.setString(1, userEmail);

// ❌ FAIL — concatenação
Statement stmt = conn.createStatement("SELECT id, name FROM users WHERE email = '" + userEmail + "'");
```

**Por que importa**: Concatenação permite que `userEmail = "' OR 1=1 --"` altere a semântica da query. Parameterized queries separam código de dados no protocolo do banco — o driver nunca interpreta o parâmetro como SQL.

---

### Padrão 2 — SQL Injection em Query Builder com String Dinâmica

**Regra**: Query builders protegem apenas quando usados via API tipada. Strings raw dentro de query builder são tão perigosas quanto SQL puro.

```javascript
// ✅ PASS — API tipada do builder
const users = knex('users').where('email', userEmail).select('id', 'name');

// ❌ FAIL — whereRaw com concatenação
const users = knex('users').whereRaw(`email = '${userEmail}'`).select('id', 'name');

// ❌ FAIL — knex.raw com template literal
const users = knex.raw(`SELECT * FROM users WHERE email = '${userEmail}'`);
```

```python
# ✅ PASS — API tipada
users = User.objects.filter(email=user_email)

# ❌ FAIL — extra() com string
users = User.objects.extra(where=[f"email = '{user_email}'"])

# ❌ FAIL — raw()
users = User.objects.raw(f"SELECT * FROM auth_user WHERE email = '{user_email}'")
```

**Por que importa**: `whereRaw`, `knex.raw`, `.extra()`, `.raw()` são escapes que desabilitam a proteção do builder. O dado vira string SQL novamente.

---

### Padrão 3 — SQL Injection em Order By / Column Name Dinâmico

**Regra**: Nomes de coluna e direções de ordenação não podem ser parametrizados — use whitelist.

```javascript
// ✅ PASS — whitelist de colunas válidas
const ALLOWED_COLUMNS = ['name', 'created_at', 'email'];
const ALLOWED_DIRS = ['ASC', 'DESC'];
const col = ALLOWED_COLUMNS.includes(sortCol) ? sortCol : 'created_at';
const dir = ALLOWED_DIRS.includes(sortDir?.toUpperCase()) ? sortDir.toUpperCase() : 'ASC';
const result = await db.query(`SELECT id, name FROM users ORDER BY ${col} ${dir}`);

// ❌ FAIL — interpolação direta
const result = await db.query(`SELECT id, name FROM users ORDER BY ${sortCol} ${sortDir}`);
// Payload: sortCol = "id; DROP TABLE users; --"
```

```python
# ✅ PASS — whitelist
ALLOWED_COLUMNS = {'name', 'created_at', 'email'}
col = sort_col if sort_col in ALLOWED_COLUMNS else 'created_at'
users = User.objects.order_by(col)

# ❌ FAIL — .order_by com input direto
users = User.objects.order_by(sort_col)
```

**Por que importa**: Nenhum driver SQL suporta parameterizar nomes de coluna ou keywords. Placeholder `?` em `ORDER BY ?` resulta em erro ou aspas literais. Whitelist é a única defesa correta.

---

### Padrão 4 — SQL Injection de Segunda Ordem

**Regra**: Dado sanitizado na inserção mas reusado sem sanitização em query posterior é vulnerável.

```javascript
// ❌ FAIL — sanitized no INSERT, mas o valor armazenado é usado raw depois
// Passo 1: INSERT (seguro via parameterized)
await db.query('INSERT INTO users (name, email) VALUES ($1, $2)', [userName, userEmail]);

// Passo 2: SELECT usando o valor armazenado (a coluna contém dado não sanitizado)
const row = await db.query("SELECT * FROM users WHERE name = '" + row.name + "'");
// Se row.name = "admin' --" (armazenado literalmente), a query é injetada
```

```javascript
// ✅ PASS — parameterized em TODOS os usos
const row = await db.query('SELECT * FROM users WHERE name = $1', [row.name]);
```

**Por que importa**: Sanitização no INSERT protege a escrita, mas o valor no banco é o original. Qualquer leitura subsequente que não use parameterized query é vulnerável.

---

### Padrão 5 — NoSQL Injection

**Regra**: Nunca passar objeto construído com input do usuário diretamente como filtro de query.

```javascript
// ❌ FAIL — objeto do usuário como filtro
app.post('/login', (req, res) => {
  // req.body = { "email": {"$ne": ""}, "password": {"$ne": ""} }
  db.users.findOne(req.body); // bypass completo de autenticação
});

// ❌ FAIL — spread do input no filtro
db.users.findOne({ ...req.body, active: true });
// req.body = { "password": { "$gt": "" } } → retorna qualquer senha

// ✅ PASS — campos explícitos com valores escalares
db.users.findOne({
  email: req.body.email,      // string escalar, operadores ignorados
  password: hashedPassword,   // string escalar
  active: true
});
```

```python
# ❌ FAIL — dict do request como filtro
users.find_one(request.json)

# ✅ PASS — campos explícitos
users.find_one({"email": request.json.get("email"), "active": True})
```

**Por que importa**: MongoDB/Mongoose aceitam operadores como `$ne`, `$gt`, `$regex`, `$where` como valores. Se o usuário controla a estrutura do objeto, controla a query.

---

### Padrão 6 — NoSQL Injection via $where / $regex

**Regra**: `$where` executa JavaScript no servidor. `$regex` permite denial of service via backtracking. Bloqueie ambos de input do usuário.

```javascript
// ❌ FAIL — $where permite execução arbitrária
db.users.findOne({ $where: `this.username === '${username}'` });
// Payload: username = "'; sleep(5000); '"

// ❌ FAIL — $regex com input do usuário causa ReDoS
db.users.findOne({ email: { $regex: userInput } });
// Payload: userInput = "(a+)+$" → backtracking catastrófico

// ✅ PASS — usar operadores escalares
db.users.findOne({ username: username }); // sem $where, sem $regex
```

**Por que importa**: `$where` é eval disfarçado de query. `$regex` com input não-validado é vetor de ReDoS que derruba o banco.

---

### Padrão 7 — XSS Refletido via Template Sem Escape

**Regra**: Templates devem escapar por padrão. Escape manual só se o contexto exigir (ex: atributo HTML vs. contexto JavaScript).

```html
<!-- ❌ FAIL — expressão sem escape (varia por framework) -->
<div>{{{ userComment }}}</div>           <!-- Handlebars triple-stache -->
<div v-html="userComment"></div>          <!-- Vue -->
<div dangerouslySetInnerHTML={{comment}} />  <!-- React -->
<div>{{ comment|raw }}</div>              <!-- Twig -->
<%= raw(comment) %>                       <!-- EJS -->
```

```html
<!-- ✅ PASS — escape automático (padrão de cada framework) -->
<div>{{ userComment }}</div>              <!-- Handlebars (double-stache) -->
<div>{{ comment }}</div>                  <!-- Vue (mustache) -->
<div>{comment}</div>                      <!-- React JSX (auto-escape) -->
<div>{{ comment }}</div>                  <!-- Twig (auto-escape) -->
<%= comment %>                            <!-- EJS (escaped) -->
```

**Por que importa**: O escape automático do template engine converte `<script>` em `&lt;script&gt;`, impedindo execução. Desabilitar o escape é equivalente a innerHTML.

---

### Padrão 8 — XSS via Contexto JavaScript no Template

**Regra**: Dado dentro de `<script>` ou atributo `onclick` requer escape diferente de dado dentro de `<div>`.

```html
<!-- ❌ FAIL — HTML escape NÃO protege dentro de <script> -->
<script>
  var username = "{{ username }}";
  // Payload: username = "</script><script>alert(1)</script>"
  // O HTML encoder não escapa aspas e quebra a tag script
</script>

<!-- ❌ FAIL — JSON.stringify sem escape de </script> -->
<script>
  var data = <%= JSON.stringify(userData) %>;
  // Payload: userData contém "</script><script>alert(1)</script>"
</script>

<!-- ✅ PASS — JSON.stringify + escape de </script> -->
<script>
  var data = <%= JSON.stringify(userData).replace(/<\/script/gi, '<\\/script') %>;
</script>

<!-- ✅ PASS — atributo de dados + parse no JS -->
<div id="user-data" data-json='<%= JSON.stringify(userData).replace(/'/g, "&#39;") %>'></div>
<script>
  var data = JSON.parse(document.getElementById('user-data').dataset.json);
</script>
```

**Por que importa**: HTML entities (`&lt;`) são interpretadas literalmente dentro de `<script>`. O parser HTML encontra `</script>` antes do parser JavaScript, quebrando o contexto. É necessário sanitizar para o contexto específico.

---

### Padrão 9 — XSS via DOM (Source: URL hash, Sink: innerHTML)

**Regra**: innerHTML com dado de `location.hash`, `location.search`, `document.referrer` ou `postMessage` é sempre vulnerável.

```javascript
// ❌ FAIL — hash direto em innerHTML
document.getElementById('content').innerHTML = location.hash.slice(1);
// URL: page.html#<img src=x onerror=alert(1)>

// ❌ FAIL — referrer em innerHTML
document.getElementById('welcome').innerHTML = `Bem-vindo, ${document.referrer}`;

// ✅ PASS — textContent (nunca parseia HTML)
document.getElementById('content').textContent = location.hash.slice(1);

// ✅ PASS — DOMPurify se HTML for necessário
document.getElementById('content').innerHTML = DOMPurify.sanitize(location.hash.slice(1));
```

**Por que importa**: DOM XSS não aparece no HTML fonte — ocorre em runtime no browser. `textContent` é a defesa mais simples e infalível quando HTML não é necessário.

---

### Padrão 10 — Command Injection

**Regra**: Nunca interpolar input do usuário em string de comando. Use API com array de argumentos.

```javascript
// ❌ FAIL — exec com string concatenada
const { exec } = require('child_process');
exec(`convert ${userFile} -resize 50% output.jpg`);
// Payload: userFile = "clean.jpg; rm -rf /"

// ❌ FAIL — exec com template literal
exec(`ping -c 3 ${userHost}`);
// Payload: userHost = "8.8.8.8; cat /etc/passwd"

// ✅ PASS — execFile com array de argumentos
const { execFile } = require('child_process');
execFile('convert', [userFile, '-resize', '50%', 'output.jpg'], (err, stdout) => { ... });
// Payload não funciona: userFile é passado como argumento único, não interpretado por shell

// ✅ PASS — spawn (ainda mais seguro, stream-based)
const { spawn } = require('child_process');
const child = spawn('convert', [userFile, '-resize', '50%', 'output.jpg']);
```

```python
# ❌ FAIL — os.system com f-string
os.system(f"convert {user_file} -resize 50% output.jpg")

# ❌ FAIL — subprocess.run com shell=True
subprocess.run(f"convert {user_file} -resize 50% output.jpg", shell=True)

# ✅ PASS — subprocess.run com lista, shell=False (padrão)
subprocess.run(['convert', user_file, '-resize', '50%', 'output.jpg'], check=True)
```

**Por que importa**: `exec()` e `shell=True` invocam `/bin/sh -c "string"`, onde `;`, `|`, `&&`, `$(...)`, backticks são metacaracteres do shell. `execFile`/`spawn`/`subprocess.run(list)` chamam o executável diretamente via `execve()` — sem shell, sem metacaracteres.

---

### Padrão 11 — Command Injection via Argument Injection (sem shell)

**Regra**: Mesmo sem shell, argumentos podem injetar flags perigosas. Valide o formato esperado.

```javascript
// ❌ FAIL — sem shell, mas argumento injeta flag
execFile('curl', [userUrl, '-o', 'output.html']);
// Payload: userUrl = "-o /etc/cron.d/backdoor" → sobrescreve arquivo do sistema

// ✅ PASS — validar que input corresponde ao formato esperado
const urlPattern = /^https?:\/\/[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$/;
if (!urlPattern.test(userUrl)) throw new Error('URL inválida');
execFile('curl', [userUrl, '-o', 'output.html']);
```

```python
# ❌ FAIL — argumento injeta flag no tar
subprocess.run(['tar', '-czf', user_filename, '/data'])
# Payload: user_filename = "--to-command=malicious_script.sh /tmp/x"

# ✅ PASS — validar formato de filename
if not re.match(r'^[a-zA-Z0-9_\-\.]+\.tar\.gz$', user_filename):
    raise ValueError("Nome de arquivo inválido")
subprocess.run(['tar', '-czf', user_filename, '/data'])
```

**Por que importa**: Sem shell, `;` e `|` não funcionam. Mas `-` inicia flags em utilitários Unix. Um atacante pode injetar `--to-command`, `-o`, `--data` dependendo do binário. Validação de formato é essencial.

---

### Padrão 12 — Server-Side Template Injection (SSTI)

**Regra**: Nunca renderizar string do usuário como template. Templates devem ser arquivos estáticos do servidor.

```python
# ❌ FAIL — string do usuário como template Jinja2
from jinja2 import Template
template = Template(user_input)  # user_input = "{{ ''.__class__.__mro__[1].__subclasses__() }}"
template.render()

# ❌ FAIL — render_template_string com input
from flask import render_template_string
render_template_string(user_input)

# ✅ PASS — template como arquivo estático
from flask import render_template
render_template('user_profile.html', username=username)  # username é variável, não template
```

```javascript
// ❌ FAIL — template literal do usuário como template EJS
const ejs = require('ejs');
ejs.render(userInput, data);
// Payload: "<%= process.exit() %>"

// ✅ PASS — arquivo de template
ejs.renderFile('./views/user.ejs', { username });
```

**Por que importa**: Template engines como Jinja2, EJS, Pug, Twig têm acesso ao objeto de contexto e frequentemente ao runtime da linguagem. `{{ ''.__class__ }}` em Jinja2 acessa a hierarquia de classes Python, permitindo RCE.

---

### Padrão 13 — Path Traversal

**Regra**: Nunca concatenar input do usuário em caminho de arquivo. Use `path.resolve` + verificação de prefixo ou whitelist.

```javascript
// ❌ FAIL — concatenação direta
const filePath = `/uploads/${userFilename}`;
fs.readFile(filePath);
// Payload: userFilename = "../../etc/passwd"

// ❌ FAIL — path.join não previne traversal
const filePath = path.join('/uploads', userFilename);
fs.readFile(filePath);
// Payload: userFilename = "../../etc/passwd" → path.join normaliza para "/etc/passwd"

// ✅ PASS — resolve + verificação de prefixo
const basePath = path.resolve('/uploads');
const filePath = path.resolve(path.join(basePath, userFilename));
if (!filePath.startsWith(basePath + path.sep)) {
  throw new Error('Path traversal detectado');
}
fs.readFile(filePath);

// ✅ PASS — whitelist de extensões
const ALLOWED_EXT = ['.jpg', '.png', '.gif', '.pdf'];
const ext = path.extname(userFilename).toLowerCase();
if (!ALLOWED_EXT.includes(ext)) throw new Error('Extensão não permitida');
```

```python
# ❌ FAIL — os.path.join não previne traversal
filepath = os.path.join('/uploads', user_filename)

# ✅ PASS — resolve + startswith
base = os.path.realpath('/uploads')
filepath = os.path.realpath(os.path.join(base, user_filename))
if not filepath.startswith(base + os.sep):
    raise ValueError('Path traversal detectado')
```

**Por que importa**: `path.join` e `os.path.join` resolvem `..` — eles normalizam o caminho. A defesa é verificar se o caminho resultante está dentro do diretório permitido após normalização completa (`realpath`/`resolve`).

---

### Padrão 14 — Path Traversal via Null Byte (Legacy)

**Regra**: Em PHP < 5.3.4 e C APIs antigas, null byte (`%00`) truncava o caminho. Verifique em código legado.

```php
// ❌ FAIL — null byte truncava o caminho em PHP < 5.3.4
$file = "/uploads/" . $_GET['file'];
include($file);
// Payload: ?file=../../etc/passwd%00.jpg → include("/etc/passwd")

// ✅ PASS — verificação antes de usar + versão do PHP atualizada
$file = basename($_GET['file']); // remove path components
$fullPath = '/uploads/' . $file;
if (!file_exists($fullPath)) die('Not found');
include($fullPath);
```

**Por que importa**: Embora corrigido em versões modernas, código legado pode ainda estar rodando em PHP antigo. `basename()` é a defesa mais simples pois remove tudo exceto o nome do arquivo.

---

### Padrão 15 — LDAP Injection

**Regra**: Nunca concatenar input do usuário em filtro LDAP. Escape caracteres especiais LDAP.

```java
// ❌ FAIL — concatenação em filtro
String filter = "(uid=" + username + ")";
ctx.search("ou=users,dc=example,dc=com", filter, controls);
// Payload: username = "admin)(|(password=*))" → retorna todos os usuários

// ✅ PASS — escape de caracteres especiais LDAP
String escapeLDAP(String input) {
    return input.replace("\\", "\\5c")
                .replace("*", "\\2a")
                .replace("(", "\\28")
                .replace(")", "\\29")
                .replace("\u0000", "\\00");
}
String filter = "(uid=" + escapeLDAP(username) + ")";
```

**Por que importa**: Caracteres `*`, `(`, `)` e `\` têm significado especial em filtros LDAP. Sem escape, o atacante modifica a lógica do filtro.

---

### Padrão 16 — HTTP Header Injection

**Regra**: Nunca incluir input do usuário em headers HTTP sem remover CRLF (`\r\n`).

```javascript
// ❌ FAIL — input em header sem sanitização
res.setHeader('X-Custom-Header', userValue);
// Payload: userValue = "test\r\nSet-Cookie: session=stolen"
// Resultado: header extra injetado

// ❌ FAIL — redirect com input
res.redirect(`/callback?next=${userRedirect}`);
// Payload: userRedirect = "https://evil.com\r\nX-Frame-Options: ALLOW-ALL"

// ✅ PASS — remover CRLF
function sanitizeHeader(value) {
  return value.replace(/[\r\n]/g, '');
}
res.setHeader('X-Custom-Header', sanitizeHeader(userValue));

// ✅ PASS — URL whitelist para redirect
const ALLOWED_REDIRECTS = ['/dashboard', '/profile', '/settings'];
const safeRedirect = ALLOWED_REDIRECTS.includes(userRedirect) ? userRedirect : '/dashboard';
res.redirect(safeRedirect);
```

**Por que importa**: CRLF (`\r\n`) é o delimitador de headers HTTP. Injetar CRLF em um header permite ao atacante adicionar headers arbitrários (response splitting) ou, em casos raros, injetar corpo de resposta.

---

### Padrão 17 — Log Injection

**Regra**: Entradas de log com newlines ou sequências de controle podem falsificar entradas ou enganar parsers.

```javascript
// ❌ FAIL — input do usuário em log sem sanitização
logger.info(`Login attempt: username=${username}, ip=${ip}`);
// Payload: username = "admin\n[ERROR] Database connection failed\n[INFO] Admin login successful"
// Resultado: log falsificado parece conter erro de DB + login admin bem-sucedido

// ✅ PASS — remover newlines e caracteres de controle
function sanitizeLog(value) {
  return String(value).replace(/[\r\n\t\x00-\x1f\x7f]/g, ' ');
}
logger.info(`Login attempt: username=${sanitizeLog(username)}, ip=${sanitizeLog(ip)}`);
```

**Por que importa**: Ferramentas de SIEM, ELK e Datadog parseiam newlines como separadores de evento. Log injection pode falsificar alertas de segurança ou mascarar ataques reais.

---

## Técnicas de Bypass de Sanitização

Estas técnicas devem ser aplicadas contra CADA função de sanitização encontrada no código.

### Bypass 1 — Double Encoding

```javascript
// Sanitização: decode once, then validate
function sanitize(input) {
  const decoded = decodeURIComponent(input);
  if (decoded.includes('<script>')) throw new Error('XSS');
  return input;
}

// ❌ Bypass: double-encode → primeiro decode remove uma camada, segundo (no browser) remove a outra
sanitize('%253Cscript%253Ealert(1)%253C/script%253E');
// sanitize() decodifica para: %3Cscript%3Ealert(1)%3C/script%3E (não detecta <script>)
// Browser decodifica para: <script>alert(1)</script> (executa)
```

**Defesa**: Decodificar iterativamente até que o resultado seja estável antes de validar.

```javascript
function fullDecode(input) {
  let prev = '';
  let current = input;
  while (current !== prev) {
    prev = current;
    try { current = decodeURIComponent(current); } catch { break; }
  }
  return current;
}
```

---

### Bypass 2 — Unicode Normalization

```javascript
// Sanitização: verifica por <script>
input.includes('<script>'); // false

// ❌ Bypass: caracteres Unicode que normalizam para ASCII
const payload = '\uFF1Cscript\uFF1Ealert(1)\uFF1C/script\uFF1E';
// ＜ (U+FF1C FULLWIDTH LESS-THAN SIGN) normaliza para <
// ＞ (U+FF1C FULLWIDTH GREATER-THAN SIGN) normaliza para >
payload.normalize('NFC').includes('<script>'); // true — mas o sanitize não normalizou

// ❌ Bypass com combining characters
const payload2 = '<\u0303script>'; // <̃script> → pode ser interpretado como < por alguns parsers
```

**Defesa**: Normalizar para NFC antes de validar.

```javascript
function sanitize(input) {
  const normalized = input.normalize('NFC');
  if (normalized.includes('<script>')) throw new Error('XSS');
  return normalized;
}
```

---

### Bypass 3 — Null Byte Injection

```php
// Sanitização: verifica extensão
if (end(explode('.', $file)) !== 'jpg') die('Invalid');

// ❌ Bypass: null byte trunca em C APIs antigas
$file = "shell.php%00.jpg";
// explode('.', ...) → ['shell', 'php%00', 'jpg'] → end = 'jpg' → passa
// Mas fopen() trunca no null byte → abre "shell.php"
```

**Defesa**: Remover null bytes antes de qualquer validação.

```php
$file = str_replace("\0", '', $file);
```

---

### Bypass 4 — Case Variation + Mixed Encoding

```javascript
// Sanitização: block <script>
input.replace(/<script>/gi, ''); // remove <script> case-insensitive

// ❌ Bypass: misturar encoding
const payload = '<scr\x69pt>alert(1)</scr\x69pt>';
// \x69 é 'i' em hex — o regex não encontra <script> literal

// ❌ Bypass: mixed case já coberto por /gi, mas...
const payload2 = '<ScRiPt>alert(1)</ScRiPt>';
// ...se o regex não tiver 'i' flag, passa
```

**Defesa**: Decodificar TODAS as representações antes de aplicar regex.

---

### Bypass 5 — HTML Parser Diferenças entre Browsers

```html
<!-- Sanitização: remove <script> tags -->

<!-- ❌ Bypass — IE/Edge antigo: backtick em atributo -->
<img src=x onerror=`alert(1)`>

<!-- ❌ Bypass — SVG com script -->
<svg><script>alert(1)</script></svg>
<!-- Sanitizador que só procura <script> no nível top-level falha -->

<!-- ❌ Bypass — event handler sem parênteses em alguns parsers -->
<img src=x onerror=alert(1)>

<!-- ❌ Bypass — mutation XSS (mXSS) -->
<math><mtext><table><mglyph><style><!--</style><img src=x onerror=alert(1)>
<!-- Parser reorganiza o DOM, criando <img> fora do <style> -->
```

**Defesa**: Usar DOMPurify (mantido por Cure53) em vez de regex caseiro. DOMPurify parseia o HTML em uma DOM tree real e remove nós perigosos, resistindo a mXSS.

---

### Bypass 6 — SQLi via Comment Obfuscation

```sql
-- Sanitização: bloqueia palavras como SELECT, UNION, DROP

-- ❌ Bypass — comentários inline (MySQL)
SEL/**/ECT * FROM users
UN/**/ION SELECT password FROM admin

-- ❌ Bypass — comentários de linha (PostgreSQL)
SELECT--
* FROM users

-- ❌ Bypass — case variation + comentários
sElEcT/**/*/**/fRoM/**/users
```

**Defesa**: Parameterized queries tornam isso irrelevante — o dado nunca é parseado como SQL.

---

### Bypass 7 — WAF Bypass via Chunked Encoding / HTTP/2

```
-- Sanitização: WAF bloqueia "UNION SELECT"

-- ❌ Bypass — Transfer-Encoding: chunked (WAF não reconstrói)
POST /search HTTP/1.1
Transfer-Encoding: chunked

7
UNION
6
 SELEC
5
T * F
...
-- WAF vê cada chunk isoladamente, não detecta "UNION SELECT"

-- ❌ Bypass — HTTP/2 com campos pseudo-headers fragmentados
```

**Defesa**: WAF não é sanitização de aplicação. A defesa real é parameterized queries no código.

---

### Bypass 8 — ORM Escape Hatch

```javascript
// Mongoose "escape hatch" — $where permite JS no servidor
const user = await User.find({ $where: `this.username === '${username}'` });

// Sequelize "escape hatch" — raw query
const results = await sequelize.query(`SELECT * FROM users WHERE name = '${name}'`);

// Django "escape hatch" — extra() e raw()
User.objects.extra(where=[f"name = '{name}'"])
User.objects.raw(f"SELECT * FROM auth_user WHERE name = '{name}'")
```

**Defesa**: Auditoria específica para escape hatches. Todo uso de `$where`, `raw()`, `extra()`, `knex.raw()` deve ser sinalizado como finding se contiver input do usuário.

---

## Casos de Exceção e Resiliência

Testar estes cenários em CADA sink identificado:

### Edge Cases de Input

| Input | O que testar | Risco se falhar |
|---|---|---|
| `null` / `undefined` | Sink recebe null? Gera query `WHERE x = null` (nunca match) ou erro? | Logic bug, possível bypass de autenticação |
| `[]` (array vazia) | ORM converte para `IN ()` que gera SQL syntax error? | DoS via erro 500 |
| `[1,2,3]` em campo string | ORM gera `IN (1,2,3)` onde esperava string? | Comportamento inesperado |
| `{}` (objeto vazio) | NoSQL: `findOne({})` retorna primeiro documento? | Bypass de autenticação |
| `{__proto__: {admin: true}}` | Prototype pollution via merge recursivo? | Escalação de privilégio |
| `""` (string vazia) | Query `WHERE x = ''` retorna resultados inesperados? | Information leak |
| `" "` (espaço) | Trim aplicado antes da validação? | Bypass de required validation |
| `NaN` / `Infinity` | Parse de número aceita? SQL `WHERE x = NaN`? | Comportamento indefinido |
| Input de 10MB | Buffer overflow? OOM? Timeout? | DoS |
| String com apenas null bytes `\x00\x00\x00` | Trunca caminho? Bypass validation? | Path traversal |

### Edge Cases de Encoding

| Input | O que testar | Risco se falhar |
|---|---|---|
| `%00` (null byte URL-encoded) | Trunca string em C APIs? | Path traversal, log injection |
| `%0d%0a` (CRLF URL-encoded) | Injeta header? | HTTP response splitting |
| `%2527` (single quote double-encoded) | Bypass de escape de SQL? | SQL injection |
| `\u202E` (RTL override) | Inverte visualmente texto em log/UI? | Phishing via log falsificado |
| `\u200B` (zero-width space) | Bypass de regex que não cobre unicode? | XSS, SQLi |
| `\uFEFF` (BOM) | Corrompe parser XML/JSON? | XML injection, parser crash |
| `&#60;script&#62;` (HTML entity) | Browser decodifica em innerHTML? | XSS |
| `\\u003c` (JS unicode escape) | `eval()` decodifica? | XSS via eval |

### Edge Cases de Multi-Step Flow

| Cenário | O que testar | Risco se falhar |
|---|---|---|
| Input sanitizado → armazenado → reusado | Segunda ordem: dado no DB é usado sem sanitize? | SQLi de segunda ordem |
| Input sanitizado → log → ferramenta de alerta | Log injection dispara alerta falso? | Alert fatigue, ataque mascarado |
| Input sanitizado → email → link com parâmetro | Reflected XSS no email? | XSS em cliente de email |
| Input sanitizado → redirect → URL com hash | DOM XSS na página de destino? | XSS encadeado |
| Input sanitizado → API response → outro serviço consome | Injection propaga para serviço downstream? | Supply chain injection |
| Input validado no frontend → enviado ao backend | Backend re-valida? | Bypass via curl/Postman |

### Edge Cases de Concorrência e Estado

| Cenário | O que testar | Risco se falhar |
|---|---|---|
| Two requests with same input | Race condition na sanitização? | TOCTOU bypass |
| Input modificado entre validação e uso | TOCTOU: filename validado, depois renomeado? | Path traversal |
| Sanitização depende de estado global | Global mutable state afeta resultado? | Inconsistência de sanitização |

---

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa correta |
|---|---|---|
| Usar `escape()` ou `encodeURI()` como sanitização XSS | Não escapa `<`, `>`, `"`, `'` — não é sanitização HTML | Usar `DOMPurify.sanitize()` ou escape do template engine |
| Regex caseiro para bloquear SQL keywords | Bypassável via comentários, encoding, case variation | Parameterized queries |
| Remover palavras "perigosas" da input (blacklist) | Bypass trivial via variação | Whitelist de caracteres permitidos |
| `strip_tags()` do PHP como defesa XSS | Bypass via `<img src=x onerror=alert(1)>` (não precisa tag de fechamento) | `htmlspecialchars($input, ENT_QUOTES, 'UTF-8')` |
| `JSON.stringify` como sanitização para contexto JS | Não escapa `</script>` — quebra contexto HTML | `.replace(/<\/script/gi, '<\\/script')` após stringify |
| Validar input mas não o caminho de uso | Input válido pode se tornar perigoso após transformação | Validar no ponto de uso (sink), não só na entrada |
| Try/catch que retorna erro genérico mas loga o input raw | Log contém payload de injeção que pode ser explorado | Sanitizar antes de logar |
| Sanitização condicional ("se o input parece perigoso") | Atacante controla se a sanitização é aplicada | Sanitizar sempre, independentemente do conteúdo |

---

## Critérios de Qualidade

Antes de entregar o relatório, confirme:

- [ ] Todos os sources mapeados com arquivo:linha
- [ ] Todos os sinks mapeados com arquivo:linha
- [ ] Todos os fluxos source→sink classificados (PARAMETRIZADO / SANITIZADO / VULNERÁVEL)
- [ ] Cada fluxo VULNERÁVEL tem PoC completo (input → código → output)
- [ ] Cada sanitização foi testada contra mínimo 3 técnicas de bypass
- [ ] Edge cases de input testados (null, array, objeto, vazio, longo)
- [ ] Edge cases de encoding testados (null byte, CRLF, double-encode, unicode)
- [ ] Edge cases de segunda ordem verificados
- [ ] Severidade justificada em 1 frase por finding
- [ ] Correção fornecida como diff exato (antes → depois)
- [ ] Nenhum finding sem PoC reproduzível
- [ ] Nenhuma correção genérica ("use sanitize", "validate input")
- [ ] Zero falsos positivos (cada finding é explorável, não teórico)

---

## Formato do Artefato de Saída

```markdown
# Relatório de Revisão de Injeção — [Nome do Projeto/Arquivo]

**Data**: [ISO 8601]
**Linguagem**: [linguagem] | **Framework**: [framework] | **Versão**: [versão]
**Arquivos analisados**: [lista]
**Scope**: [SQLi | NoSQLi | XSS | CMDi | SSTI | Path Traversal | LDAP | XPath | Header | Log]

---

## Resumo Executivo

[3-5 linhas: total de findings por severidade, risco principal, ação prioritária]

| Severidade | Qtd |
|---|---|
| CRÍTICO | X |
| ALTO | X |
| MÉDIO | X |
| BAIXO | X |

---

## Superfície de Ataque

### Sources (Entradas)
| Source | Arquivo:Linha | Tipo |
|---|---|---|
| `req.body.email` | auth.js:42 | HTTP body |
| `req.query.sort` | users.js:18 | Query param |

### Sinks (Saídas)
| Sink | Arquivo:Linha | Tipo | Fluxos |
|---|---|---|---|
| `db.query()` | auth.js:43 | SQL | source→sink: [1] |
| `innerHTML` | dashboard.js:27 | DOM XSS | source→sink: [2,3] |

---

## Findings

### [INJ-001] SQL Injection — Concatenação em Query de Login
**Severidade**: CRÍTICO — exploitação trivial permite autenticação bypass e exfileração de dados.

**Fluxo**: `req.body.email` (auth.js:42) → concatenação (auth.js:43) → `db.query()` (auth.js:43)

**PoC**:
- **Input**: `email = "' OR 1=1 --"`, `password = "qualquer"`
- **Query gerada**: `SELECT * FROM users WHERE email = '' OR 1=1 --' AND password = 'qualquer'`
- **Resultado**: retorna todos os usuários, bypass de autenticação completo

**Correção**:
```diff
- const result = await db.query(`SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`);
+ const result = await db.query('SELECT * FROM users WHERE email = $1 AND password = $2', [email, password]);
```

---

### [INJ-002] XSS Refletido — innerHTML com Hash da URL
**Severidade**: ALTO — exige phishing para explorar, mas executa JS no contexto da origem.

**Fluxo**: `location.hash` (dashboard.js:25) → `innerHTML` (dashboard.js:27)

**PoC**:
- **Input**: URL `https://app.com/dashboard#<img src=x onerror=alert(document.cookie)>`
- **Código**: `document.getElementById('msg').innerHTML = location.hash.slice(1);`
- **Resultado**: cookie de sessão exfiltrado

**Correção**:
```diff
- document.getElementById('msg').innerHTML = location.hash.slice(1);
+ document.getElementById('msg').textContent = location.hash.slice(1);
```

---

## Sanitizações Avaliadas

| Função | Arquivo:Linha | Contexto | Resultado | Bypass |
|---|---|---|---|---|
| `escapeHtml()` | utils.js:12 | HTML output | BYPASSÁVEL | Double-encoding: `%253Cscript%253E` |
| `whitelistFilename()` | upload.js:8 | Path traversal | EFETIVA | Nenhum bypass encontrado |

## Edge Cases Testados

| Cenário | Comportamento | Risco |
|---|---|---|
| `null` em `req.body.email` | Query gera `WHERE email = null` (sem match) | BAIXO — login falha silenciosamente |
| `[]` em `req.body.sort` | `ORDER BY Array` → erro 500 | MÉDIO — DoS |
| `%00` em filename | `path.join` normaliza, mas null byte preservado em legado | ALTO — path traversal em PHP antigo |

---

## Ações Prioritárias

1. **[CRÍTICO]** Corrigir INJ-001 — parameterizar query de login (auth.js:43)
2. **[ALTO]** Corrigir INJ-002 — trocar innerHTML por textContent (dashboard.js:27)
3. **[MÉDIO]** Substituir `escapeHtml()` por DOMPurify ou escape do template engine (utils.js:12)
4. **[MÉDIO]** Adicionar validação de tipo em `req.body.sort` (users.js:18)
```

---

## Referências Cruzadas

| Precisa de... | Use a skill... |
|---|---|
| Revisar autenticação/autorização (IDOR, privilege escalation) | `auth-review` |
| Configurar WAF, CSP, HSTS, CORS | `infra-security` |
| Avaliar criografia, JWT, gestão de sessão | `crypto-review` |
| Analisar dependências com vulnerabilidades conhecidas | responda diretamente com `npm audit`/`pip audit` |
| Ler arquivos de código-fonte enviados | `file-reading` |