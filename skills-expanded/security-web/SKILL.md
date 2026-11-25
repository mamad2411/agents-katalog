---
name: security-web
description: "Web application weaknesses and how to find them in code: broken access control and IDOR, injection of every kind, XSS, CSRF, SSRF, path traversal, unsafe uploads, open redirects, insecure deserialisation, mass assignment, XXE, prototype pollution, ReDoS, race conditions and misconfiguration, each with what to look for and the fix. Read before reviewing a web application or an API."
---

# Web application weaknesses

The naive review greps for `eval`, finds nothing and calls the app safe,
while `GET /api/orders/:id` returns any order to any account, checkout trusts
the price in the body, and a coupon applies twice when two requests land
together. Each class below has the code that signals it, how to confirm it
and where the fix lives (method and severity: `security`). Patterns are
regexes for the `grep` tool or `rg -n`: leads, never findings on their own.

## 1. Broken access control and IDOR

The commonest critical finding, invisible to scanners (CWE-862, 863, 639):
routes outside the auth middleware (registered before it, or exempted);
server actions that never read the session; admin actions behind a hidden
button; records loaded by id with no owner or tenant condition (reads,
updates, deletes, downloads, exports, bulk actions, nested routes never
checked against their parent, socket channels, GraphQL `node(id:)`); a role,
user or tenant id taken from the body, a header or an unverified token.

```sh
rg -n 'findById\(|findByPk\(|findUnique\(|findFirst\(|findOne\(|get_object_or_404\(|objects\.get\(|::find(OrFail)?\(|WHERE id = ' .
rg -n -i 'skipAuth|isPublic|AllowAny|permitAll|AllowAnonymous|@Public\(|withoutMiddleware|(body|headers)\.(role|isAdmin|tenantId|orgId)' .
```

Confirm with two accounts in two organisations (a test or a local run): A
asking for B's record gets `404` or `403`, and the query shows why. Fix:
`backend-auth` section 6; review depth in `security-auth`.

## 2. Injection

Input that changes the structure of a query, command or template instead of
filling a slot in it.

- **SQL** (CWE-89): placeholders are safe; identifiers (sort column, table)
  come from an allowed list. A tagged template (the `sql` tag of postgres.js,
  Drizzle or Slonik; Prisma's `$queryRaw` tag) binds values; a plain template
  string given to `query(`, `$queryRawUnsafe(` or `knex.raw(` does not. In
  psycopg `%s` with a second argument is safe; `%` on the string is not.
- **NoSQL** (CWE-943): a JSON field arriving as an object of query operators
  instead of a string; `$where`, `$function`, `$accumulator` run JavaScript.
  Fix: schema types, Mongoose `sanitizeFilter`, keys starting `$` stripped.
- **OS commands** (CWE-78): a shell given a string built from input. An
  argument array avoids the shell, yet a value starting with `-` can become
  an option (git, curl, tar, ssh): `--` before user values.
- **Code and templates** (CWE-94, 1336): `eval`, `new Function`, `setTimeout`
  with a string, Node's `vm` (not a sandbox), Python `exec`, Ruby `send` or
  `constantize` on a parameter, `require()` of a user path; user text used
  as the template itself. Authors of templates get Liquid or Mustache.
- **Others**: LDAP and XPath built by concatenation (use the library's
  escape); CR or LF in a response or mail header (CWE-113); newlines forging
  plain-text logs (CWE-117); Log4j 2 before 2.17.1 running lookups in logged
  text; spreadsheet cells starting `=`, `+`, `-` or `@` run as formulas.

```sh
rg -n -U -i '`\s*(select|insert|update|delete|with)\b[^`]*\$\{|queryRawUnsafe|executeRawUnsafe|\.raw\(|sequelize\.query\(' -t js -t ts .
rg -n 'execute(many)?\(\s*f["\x27]|["\x27]\s*(?i:select|insert|update|delete)\b[^"\x27]*["\x27]\s*(%|\.format\()|text\(\s*f["\x27]|\.extra\(|RawSQL\(' -t py .
rg -n 'fmt\.Sprintf\(\s*"\s*(?i:select|insert|update|delete|with)\b|(query|query_as|execute)\(\s*&?format!|(whereRaw|selectRaw|orderByRaw|DB::raw)\(|(executeQuery|executeUpdate|createQuery|createNativeQuery)\(\s*"[^"]*"\s*\+|(where|order|find_by_sql)\(\s*"[^"]*#\{' .
rg -n '\.(find|findOne|updateOne|deleteMany)\(\s*req\.|\$where|\$function|\$accumulator' .
rg -n 'child_process|shell:\s*true|shell\s*=\s*True|os\.system|os\.popen|exec\.Command\(\s*"(sh|bash)"|getRuntime\(\)\.exec|shell_exec|passthru|proc_open|%x\(' .
rg -n 'eval\(|new Function|runInNewContext|instance_eval|constantize|render_template_string|from_string\(|Handlebars\.compile|renderString\(|createTemplate\(' .
```

## 3. XSS

Input rendered as markup or script in another user's browser (CWE-79):
reflected, stored, or DOM-based (from the URL or `postMessage`).

```sh
rg -n 'innerHTML|outerHTML|insertAdjacentHTML|document\.write|dangerouslySetInnerHTML|v-html|\{@html|bypassSecurityTrust|\.html\(|\|\s*safe\b|autoescape\s+off|mark_safe\(|Markup\(|\{!!|<%-|\{\{\{|html_safe|th:utext|Html\.Raw\(|template\.HTML\(' .
rg -n 'href=\{|:href=|location\.(hash|search)|window\.open\(|addEventListener\(\s*["\x27]message' .
```

- Framework escaping covers text and quoted attributes, not `<script>`,
  event handlers, `style`, unquoted attributes or URLs (`javascript:`).
- Markdown: `marked` does not sanitise, `markdown-it` with `html: true` and
  Python-Markdown pass raw HTML, `react-markdown` is safe until `rehype-raw`.
  Sanitise output: DOMPurify, `sanitize-html`, `nh3` (bleach is deprecated).
- Stored XSS hides in display names, file names, tickets and admin screens;
  SVG uploads on the app's origin run script; server-side HTML-to-PDF turns
  it into file reads and SSRF. `HttpOnly` does not make it minor: the script
  acts as the user. Fix: `frontend-security`.

## 4. CSRF and cross-site WebSockets

Another site makes the victim's browser send a state-changing request with
credentials it attaches by itself: cookies, basic auth, client certificates
(CWE-352). A bearer token that script sets in a header is not exposed.

- Exemptions: `csrf_exempt`, `verify_authenticity_token` skipped,
  `validateCsrfTokens(except:`, `csrf().disable()` (fine for token-only
  APIs), `csurf` (deprecated).
- `SameSite=Lax` stops most of it, but not a state-changing `GET`, not a
  sibling subdomain (same-site is not same-origin), and browsers differ for
  cookies without the attribute: it must be explicit. JSON endpoints resist
  forms only while they refuse other content types. WebSocket upgrades carry
  cookies and ignore CORS: the server checks `Origin`.
- Fix: explicit `SameSite`, the framework's token or an `Origin` or
  `Sec-Fetch-Site` check on unsafe methods, no change of state on `GET`
  (`backend-auth` section 2).

## 5. SSRF

The server fetches a URL the user chose and reaches what the user cannot:
internal services, cloud metadata, admin ports (CWE-918). Link previews,
imports from a URL, webhooks, image proxies, PDF and screenshot renderers,
customer-supplied OIDC issuers, XML and SVG handling.

```sh
rg -n 'fetch\(|axios|got\(|undici|https?\.(get|request)\(|requests\.(get|post|request)\(|httpx\.|urlopen\(|aiohttp|http\.(Get|Post|NewRequest)|reqwest::|Net::HTTP|URI\.open|file_get_contents\(|curl_setopt|RestTemplate|WebClient|page\.goto\(' .
```

- Partial control counts (a chosen path or port on an internal host).
  Checks that fail: string blocklists; the host checked but not the address
  it resolves to; no re-check after redirects; DNS rebinding; parsers that
  disagree about `@`, backslashes or IP notations; `file:` and `gopher:`.
- Rule out loopback, private ranges, link-local with `169.254.169.254` and
  `fd00:ec2::254`, `100.100.100.200` (Alibaba), internal names, Docker's API.
- Fix: an allow-list of hosts, or resolve, refuse private, loopback and
  link-local addresses, connect to the checked address and re-check
  redirects (`backend-security` section 2; `request-filtering-agent` in Node,
  a `net.Dialer` `Control` hook in Go). IMDSv2 limits the damage.

## 6. Paths, archives and uploads

A user value in a path escapes its directory (CWE-22, 98); an upload becomes
code, markup on the app's origin or an outage (CWE-434).

```sh
rg -n 'sendFile\(|createReadStream\(|readFile(Sync)?\(|send_file\(|FileResponse\(|os\.path\.join\(|filepath\.Join\(|http\.ServeFile\(|new File\(|Paths\.get\(|(include|require)(_once)?\s*\(?\s*\$' .
rg -n 'multer|busboy|formidable|UploadFile|request\.FILES|FormFile\(|MultipartFile|move_uploaded_file|originalname|extractall|ZipEntry|zip\.File' .
```

- `os.path.join`, `pathlib`, Rust `Path::join` and Node `path.resolve` drop
  the base when the second part is absolute.
- Zip slip: entries with `..`, absolute names or symlinks land outside the
  target: Python `tarfile` without `filter="data"` (the default only from
  3.14), Java joining `ZipEntry.getName()`, Go joining `zip.File.Name`. Cap
  total size and entry count (zip bombs).
- Uploads: type from the content (magic bytes: `file-type`, `python-magic`,
  `http.DetectContentType`), a size limit while streaming (nginx defaults to
  1 MB), image bombs (Pillow `MAX_IMAGE_PIXELS`), generated names outside
  the web root, never executable (PHP in uploads, `.htaccess`), served from
  another domain or with `Content-Disposition: attachment`.
- Fix: generated names, or resolve and check the result is under the base
  with a trailing separator (Go 1.24 `os.Root`, `filepath.IsLocal`; Java
  `toRealPath().startsWith(base)`) (`backend-security` section 3).

## 7. Open redirects

A redirect target from input (CWE-601): low alone, high in sign-in and OAuth
flows where it carries codes or tokens away (`next`, `returnTo`, `continue`,
`callbackUrl`). A "starts with `/`" check fails: browsers read a leading `//`
or `/\` as another host. Django has `url_has_allowed_host_and_scheme()`;
Rails 7 raises with `raise_on_open_redirects`. Fix: named destinations, or
parse against the app's origin and require it (`frontend-security`).

## 8. Insecure deserialisation and XXE

Native deserialisers can run code while rebuilding objects (CWE-502); XML
parsers resolving external entities read files and make requests (CWE-611).

```sh
rg -n 'pickle\.loads?|dill\.loads?|joblib\.load|torch\.load|jsonpickle|marshal\.loads|yaml\.load\(|unsafe_load|Loader=yaml\.(Loader|UnsafeLoader|FullLoader)|ObjectInputStream|readObject\(|XMLDecoder|XStream|enableDefaultTyping|activateDefaultTyping|JsonTypeInfo\.Id\.CLASS|new Yaml\(' .
rg -n 'unserialize\(|phar://|Marshal\.load|Oj\.load|node-serialize|BinaryFormatter|TypeNameHandling\.(All|Auto|Objects)|DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|LIBXML_NOENT|resolve_entities' .
```

- Safe forms: PyYAML `safe_load`, js-yaml 4 `load`, Psych 4 `YAML.load`,
  `torch.load` with `weights_only=True` (the default from PyTorch 2.6), PHP
  `unserialize` with `allowed_classes` false; .NET 9 removed
  `BinaryFormatter`. A leaked signing key turns signed native formats (some
  Rails cookie and Java view-state formats) into code execution.
- XXE: Java's XML factories resolve entities unless configured; PHP with
  `LIBXML_NOENT`; lxml before 5.0 or with `resolve_entities=True`. SVG, DOCX,
  XLSX, SAML and SOAP are XML too.
- Fix: JSON with a schema; where a native format stays, a signature checked
  first and a class allow-list (Java `ObjectInputFilter`); DTDs off
  (`disallow-doctype-decl` in Java, `defusedxml` in Python).

## 9. Mass assignment and prototype pollution

The body written as it came, so a caller sets `role`, `isAdmin`, `ownerId`,
`tenantId`, `price` or `emailVerified` (CWE-915); or a whole row returned
with the password hash (OWASP API3:2023). In JavaScript a deep merge or path
setter over user keys writes to `Object.prototype` through `__proto__`,
`constructor` or `prototype` (CWE-1321), and every object inherits it.

```sh
rg -n 'Object\.assign\([^)]*req\.body|\.\.\.req\.body|\(req\.body\)|data:\s*req\.body|fields\s*=\s*["\x27]__all__|\*\*request\.(data|POST)|permit!|\$guarded\s*=\s*\[\]|->all\(\)\)|forceFill\(' .
rg -n '__proto__|constructor\[|\bmerge\(|deepmerge|defaultsDeep|extend\(\s*true|_\.set\(|setWith\(|set-value|object-path' -t js -t ts .
```

Fix: a schema per operation for what a caller may set and one for what they
may see (`backend-api` sections 3 and 4); merges that drop unknown keys, `Map`
or `Object.create(null)`, the three keys refused, Node's
`--disable-proto=delete`; old lodash, jQuery `extend` and `set-value` had it.

## 10. ReDoS

A backtracking regex on user input runs for seconds: nested quantifiers like
`(a+)+`, overlapping alternatives, `new RegExp(input)` (CWE-1333).
JavaScript, Python `re`, Java, .NET, PCRE and Ruby backtrack; Go, Rust
`regex` and RE2 do not. Leads: `new RegExp\(|re\.compile\(|Pattern\.compile\(`
and `\([^)]*[+*]\)[+*{]`; `eslint-plugin-regexp` and `recheck` test patterns.
Fix: rewrite, cap input length first, a linear engine (`re2`, .NET
`RegexOptions.NonBacktracking`) or a timeout (Ruby 3.2 `Regexp.timeout`);
escape user text in a pattern (`RegExp.escape`, `re.escape`).

## 11. Race conditions and business logic

Two requests at once pass a check meant for one (CWE-362, 367): a coupon or
balance spent twice, a trial claimed twice, stock below zero, a code guessed
past its limit; READ COMMITTED (PostgreSQL's default) does not stop a read
then a write. Look for a read, a check in code, then a write; uniqueness by
query, not constraint; counters in code; client-sent prices, totals or
currencies; negative quantities; skipped steps; replayed webhooks. Two
parallel runs must leave one effect. Fix: a conditional update whose row
count is checked (`UPDATE ... SET used = true WHERE id = $1 AND NOT used`),
constraints, `SELECT ... FOR UPDATE`, idempotency keys, server-side prices
(`backend-data` section 3).

## 12. Misconfiguration

```sh
rg -n 'DEBUG\s*=\s*True|debug\s*=\s*True|APP_DEBUG=true|display_errors|consider_all_requests_local\s*=\s*true|exposure\.include=\*' .
rg -n -i 'django-insecure-|changeme|your-256-bit-secret|keyboard cat|ALLOWED_HOSTS\s*=\s*\[\s*["\x27]\*|Access-Control-Allow-Origin|origin:\s*(true|["\x27]\*)|allow_origins|CORS_ALLOW_ALL_ORIGINS|allowedOriginPatterns' .
```

- **Debug in production**: Django `DEBUG`, the Werkzeug debugger (a console
  on the server), Laravel `APP_DEBUG`, Actuator exposing `env` or `heapdump`,
  the Symfony profiler, public GraphQL IDEs, stack traces in responses
  (`backend-errors`). **Defaults**: the placeholder secrets above, seeded
  admins, unchanged dashboard passwords.
- **CORS** that echoes the origin with credentials lets any site read
  signed-in responses (high with cookie sessions): Express `origin: true`
  with `credentials: true`, Spring `allowedOriginPatterns("*")` with
  credentials, Starlette or FastAPI `allow_origins=["*"]` with
  `allow_credentials=True` (the origin is echoed when cookies are sent),
  unanchored regexes, suffix checks, `null` allowed.
- **Headers** (HSTS, `nosniff`, CSP, `frame-ancestors`, `Referrer-Policy`)
  missing are low unless they enable a concrete bug. **Served by mistake**:
  `.git/`, `.env`, backups, directory listings. Fixes: `backend-security`
  section 5, `devops-security`.

## 13. Limits and enumeration

No limit on sign-in, one-time codes (six digits fall to a million guesses),
reset, sign-up, email or SMS (each costs money), search, exports or AI calls
(CWE-307, 770); limits keyed on a client-supplied `X-Forwarded-For` (Express
`trust proxy` set to `true`); GraphQL aliases and batching without depth or
cost limits; no cap on page size, body or query time; different answers for
known and unknown accounts (CWE-204). Fix: `backend-security` section 6.

## 14. LLM and agent features

Model output is untrusted input, rendered or put in SQL, shell or a tool
call. Pages and emails the model reads can carry instructions (indirect
prompt injection) that steer it into leaking data, for example through a
markdown image whose URL carries it away. Tools act with the user's
permissions; destructive actions need a confirmation; no secrets in prompts.

## Check it

Every route has an access decision you read and every record lookup an owner
or tenant condition, or a finding; each lead ends as a finding (source, sink,
reach), not reachable (why) or suspected (the open question); framework
defaults were checked in the installed version, not assumed.

## Avoid

Calling an app safe because a grep for `eval` was empty; the IDOR missed
while headers are listed; a sink with no attacker-controlled source; a WAF or
`HttpOnly` as the XSS fix; a "starts with /" redirect check; SSRF checks on
the hostname only; CORS echoing origins; check-then-write on money; payloads.
