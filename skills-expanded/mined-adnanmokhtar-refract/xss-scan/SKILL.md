---
name: xss-scan
description: Browser-side injection and client exposure — raw-HTML sinks in every frontend framework, URL-scheme sinks, DOM sinks, postMessage, CSP and frame-ancestors, CSRF, tokens in web storage, secrets and source maps shipped in the client bundle.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: xss-scan

## Premise

Everything an attacker does **through the victim's browser**: run script in the app's origin (XSS — reflected, stored, DOM), ride the victim's cookies (CSRF), frame the app under a decoy (clickjacking), read what the app left in web storage, or read what the build shipped (keys, internal URLs, source). XSS is **A05:2025 Injection**; the rest spread across A01 / A02 / A04 / A07 / A08, and each detector names its class. The security pack has no frontend reviewer agent — on a repo with a web client, this skill **is** `/security-audit`'s client coverage.

**Every finding cites the sink at `<file:line>` + the tainted source (or, for a config detector, the failing condition) + the concrete fix + a severity** (critical / high / medium / low). A grep hit is never a finding: `dangerouslySetInnerHTML` over a constant is a hit; over `comment.body` from the API it is stored XSS.

**Taint, here:** anything an attacker can write that a browser later renders — request params reflected by the server; **API fields another user wrote** (comments, names, bios, filenames, CMS content, a partner API's data, model output); the URL (`location.*`, router params); `document.referrer`; `window.name`; `postMessage` data; web storage (any earlier XSS could have written it). Developer-authored constants are not taint.

When `llm-trust-scan` ran first, its `completion-sources.txt` (§3s, `<file:line>` of every completion, tool-call argument and model message read) is a source list: trace each one forward to this skill's sinks, and grade the sink here (OH-1, HTML and Markdown sinks); `llm-trust-scan` lists the count only.

## Adapt to the codebase

Most repos have two lanes — the client framework, and whatever renders HTML on the server. Detect both and phrase each fix in the lane's own primitive.

**Client lane**

| Lane | Escapes by default | Raw-HTML / trust-bypass sinks | URL attributes | CSP / framing primitive | CSRF primitive | What ships to the browser |
|---|---|---|---|---|---|---|
| **React / Next.js** | JSX text + attributes | `dangerouslySetInnerHTML`, `srcDoc`, `ref.current.innerHTML` | React 19 blocks `javascript:` in `href`/`src`/`action`/`formAction`; ≤ 18 only warns — read the lockfile's major. Never covered: `data:` (browsers block it top-level; an `<iframe src="data:…">` loads with an opaque origin), `window.open`, `location` | `headers()` in `next.config.*`; nonce CSP in `middleware.ts` / `proxy.ts` | Server Actions compare `Origin` to `Host`; route handlers have none | `NEXT_PUBLIC_*`, `env:` in `next.config.*`, anything a `'use client'` file imports |
| **Vue / Nuxt** | `{{ }}` + bindings | `v-html`, `innerHTML` in render functions / `useHead` | `:href` never scheme-checked | `nuxt-security` module; SPA: host config or `<meta>` | none built in — `nuxt-security` / `nuxt-csurf` | `NUXT_PUBLIC_*`, `runtimeConfig.public`, `VITE_*`, `VUE_APP_*` |
| **Angular** | interpolation + bindings via `DomSanitizer` | `bypassSecurityTrust{Html,Url,ResourceUrl,Script,Style}`, `nativeElement.innerHTML`, `Renderer2.setProperty(el, 'innerHTML', …)` | `[href]` sanitised (`unsafe:` prefix) unless bypassed | `autoCsp` in `angular.json`; `CSP_NONCE` / `ngCspNonce` | `HttpClient` XSRF cookie→header (`withNoXsrfProtection` disables); the server must still validate | every value in `environment*.ts` |
| **Svelte / SvelteKit** | `{expr}` | `{@html …}` | `href={…}` never scheme-checked | `kit.csp` in `svelte.config.js` (nonce / hash, auto-applied) | `kit.csrf` origin check, on by default | `PUBLIC_*` via `$env/*/public`; `$env/*/private` in client code is a build error |
| **Other client code** | — | Solid `innerHTML`, Lit `unsafeHTML`, Alpine `x-html`, jQuery `.html()` / `.append(str)` / `$(str)`, DOM `innerHTML` / `outerHTML` / `insertAdjacentHTML` / `document.write` / `createContextualFragment` / `setHTMLUnsafe` | — | host config or `<meta>` | — | whatever the bundler inlines (`define`, `DefinePlugin`, `envPrefix`) |

**Server-rendered lane**

| Stack | Escaped output | Raw-output hatch (the sink) | Sanitiser for real HTML | CSP / framing | CSRF | Session-cookie flags |
|---|---|---|---|---|---|---|
| **Node** (Express / NestJS / Fastify) | EJS `<%= %>`, Handlebars `{{ }}`, Nunjucks, Pug `#{}` | EJS `<%- %>`, Handlebars `{{{ }}}` / `SafeString`, Nunjucks `\|safe` / `autoescape: false`, Pug `!=` / `!{}`, a template literal passed to `res.send` / `reply.send`, any handler that sets `text/html` (`res.type('text/html').send(buildPage())`, `@Header('Content-Type', 'text/html')`) | DOMPurify + jsdom, `sanitize-html` | `helmet()` / `@fastify/helmet` — defaults set CSP + `frame-ancestors` | `csrf-csrf` (signed double-submit) / `csrf-sync`, `@fastify/csrf-protection`; `csurf` is deprecated | `res.cookie(n, v, { httpOnly, secure, sameSite })`; Fastify `reply.setCookie(n, v, opts)` (`@fastify/cookie`) |
| **Python** (Django / FastAPI / Flask) | Django templates; Jinja2 **only** where autoescape is on (Flask `render_template`: `.html .htm .xml .xhtml .svg`) | `\|safe`, `mark_safe`, `Markup()`, `{% autoescape off %}` / `false`, a bare `jinja2.Environment()` (autoescape defaults off), an f-string into `HttpResponse` / `HTMLResponse` | `nh3` (`bleach` is deprecated) | Django `SECURE_CSP` (6.0+) or `django-csp`, `XFrameOptionsMiddleware`; Flask `flask-talisman`; FastAPI a middleware | Django `CsrfViewMiddleware` (default on); Flask-WTF `CSRFProtect`; FastAPI none | `SESSION_COOKIE_SECURE / _HTTPONLY / _SAMESITE`; `set_cookie(…, secure=, httponly=, samesite=)` |
| **Go** | `html/template` (contextual) | `text/template` used for HTML, `template.HTML/JS/URL/HTMLAttr(x)`, `fmt.Fprintf(w, "<…%s")` | `bluemonday` | header middleware (`unrolled/secure`) or by hand | `http.CrossOriginProtection` (Go 1.25+), `gorilla/csrf` | `http.Cookie{HttpOnly, Secure, SameSite}` |
| **Java / Kotlin Spring** | Thymeleaf `th:text`, JSP `<c:out>` | `th:utext`, JSP `<%= %>` / bare `${}` | OWASP Java HTML Sanitizer | Spring Security `headers()` — frame `DENY` by default, **no CSP by default** | Spring Security CSRF (default on) | `server.servlet.session.cookie.*` |
| **Ruby / Rails** | ERB `<%= %>` | `raw`, `.html_safe`, `<%== %>` | `sanitize` helper (allow-list) | `content_security_policy` initializer; `X-Frame-Options: SAMEORIGIN` default | `protect_from_forgery` (default on) | `session_store … secure:, same_site:`; `cookies[:k] = { httponly:, secure: }` |
| **PHP / Laravel** | Blade `{{ }}`, Twig | Blade `{!! !!}`, Twig `\|raw`, plain `echo` / `<?=` | HTML Purifier | `spatie/laravel-csp`; no framing header by default | `@csrf` + `VerifyCsrfToken` / `validateCsrfTokens` | `config/session.php` — `secure` is env-driven, **unset means off** |

## Pre-flight greps

Run these first; they produce the candidate set the detectors judge. Grep **N** feeds detector **§ N**. Every command names its path (`.`, a directory, `"${B[@]}" .`): with none and a non-terminal stdin (an agent shell, a hook, CI), `rg` reads stdin and hangs or returns nothing. `X` keeps the sweep on code that ships. It drops vendored and built code, prose (`*.md`), the setup's own `ai/` artifact tree (audits and design canvases quote the very sinks they discuss), tests, stories, mocks and i18n catalogs. 12d and 13b search the build output on purpose. Drop the stories glob when a Storybook is deployed publicly, and drop `!ai/**` when the repo's `ai/` holds application code. `rg` with PCRE2 is assumed.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/out/**'
   -g '!**/.next/**' -g '!**/.nuxt/**' -g '!**/.output/**' -g '!**/.svelte-kit/**' -g '!**/coverage/**'
   -g '!**/*.min.js' -g '!**/*.map' -g '!.git/**' -g '!**/*.md' -g '!ai/**'
   -g '!**/*.{test,spec,stories,mock}.*' -g '!**/{__tests__,__mocks__,__snapshots__,test,tests,e2e,cypress,fixtures,mocks}/**'
   -g '!**/{locales,i18n,translations}/**/*.json')

# 1. Raw-HTML sinks, every framework — document writers under any receiver name (doc.write, contentDocument.write).
#    Then jQuery's HTML-parsing methods — only when it is a dependency.
rg -n --pcre2 'dangerouslySetInnerHTML|\bv-html\b|\[innerHTML\]|bypassSecurityTrust(Html|Script|Style|Url|ResourceUrl)\b|\{@html\s|\b(inner|outer)HTML\s*(\+?=|:)(?!=)|insertAdjacentHTML\s*\(|\b\w*[dD]oc(ument)?\.write(ln)?\s*\(|createContextualFragment\s*\(|\bsrc[dD]oc\s*=|(set|parse)HTMLUnsafe\s*\(|\bx-html\b|\bunsafeHTML\s*\(' "${X[@]}" .
rg -q -g 'package.json' -g '!**/node_modules/**' '"jquery"' . && rg -n --pcre2 '\.(html|append|prepend|after|before|replaceWith|wrap(All|Inner)?)\s*\(\s*[^)\s\x22\x27]|(\$|jQuery)\s*\(\s*(location|window\.location|document\.(URL|referrer)|decodeURI\w*\s*\(|[\w.\]\[]+\s*\+)' "${X[@]}" .

# 2. Markdown / rich-text renderers in files that import NO sanitiser (file-level set difference).
comm -23 <(rg -l --pcre2 'from\s+[\x22\x27](marked|markdown-it|showdown|rehype-raw|remark-html|micromark|@mdx-js/\w+|next-mdx-remote)[\x22\x27]|require\(\s*[\x22\x27](marked|markdown-it|showdown)[\x22\x27]|\bmarked(\.parse)?\(|allowDangerousHtml|\bhtml\s*:\s*true\b|^\s*(import|from)\s+(markdown|mistune|markdown2)\b|Redcarpet|Commonmarker|Kramdown|Parsedown|CommonMarkConverter|goldmark|blackfriday|Markdig|flexmark' "${X[@]}" . | sort) \
        <(rg -l --pcre2 'DOMPurify|dompurify|sanitize-html|sanitizeHtml|rehype-sanitize|rehypeSanitize|\bnh3\b|\bbleach\b|bluemonday|HtmlSanitizer|HtmlPolicyBuilder|HTMLPurifier|setSafeMode\s*\(\s*true|html_input|escape_html|filter_html' "${X[@]}" . | sort)

# 3. URL attributes bound to a variable (a JSX `action={<Button/>}` is a component prop, not a form action), then
#    navigation sinks fed from one (`const location = useLocation()` is a declaration, not a navigation).
rg -n --pcre2 '\b(href|xlink:href)=\{(?!\s*[\x22\x27\x60][/#])|\b(action|formAction|formaction)=\{(?!\s*($|<|\{|\(|[\x22\x27\x60][/#]))|(:|v-bind:)(href|action|formaction)=\x22|\[(href|action|formaction|attr\.href)\]=\x22|\b(href|action|formaction)=\x22\s*(\{\{|\{!!|<%[=-]|\$\{|#\{)|th:(href|action)=\x22\$\{|<(iframe|embed|object|frame)\b[^>]*[\s:\[](src|data)\b' "${X[@]}" .
rg -n --pcre2 '(?<!const\s|\blet\s|\bvar\s)\blocation(\.href)?\s*=(?!=)|\blocation\.(assign|replace)\s*\(|\bwindow\.open\s*\(|\b(router|\$router|history)\.(push|replace|navigateByUrl)\s*\((?!\s*[\x22\x27\x60]/)|\b(navigate|navigateTo|goto)\s*\((?!\s*[\x22\x27\x60]/)' "${X[@]}" .

# 4. DOM-based XSS: files holding BOTH a client-side source and a script/HTML sink — read each flow.
comm -12 <(rg -l --pcre2 'location\.(hash|search|href)|document\.(URL|documentURI|referrer|baseURI|cookie)|window\.name|URLSearchParams|useSearchParams|searchParams\.get|route\.(query|params|hash)|queryParamMap|queryParams|(local|session)Storage\.getItem' "${X[@]}" . | sort) \
        <(rg -l --pcre2 '\beval\s*\(|\bnew\s+Function\s*\(|\bset(Timeout|Interval)\s*\(\s*([\x22\x27\x60]|\w+\s*\+)|\b(inner|outer)HTML\s*(\+?=|:)(?!=)|insertAdjacentHTML|[dD]oc(ument)?\.write|dangerouslySetInnerHTML|v-html|\{@html|\.html\s*\(|\$\(\s*location|(?<!const\s|\blet\s|\bvar\s)\blocation(\.href)?\s*=(?!=)|location\.(assign|replace)\s*\(' "${X[@]}" . | sort)

# 5. postMessage: every listener with the head of its body (the origin check must come first); wildcard sends.
rg -n -A6 --pcre2 'addEventListener\s*\(\s*[\x22\x27]message[\x22\x27]|\bonmessage\s*=' "${X[@]}" .
rg -nU --pcre2 '\.postMessage\s*\((?:[^()]|\([^()]*\))*?,\s*[\x22\x27]\*[\x22\x27]' "${X[@]}" .

# 6. Server-rendered raw output: every engine's escape hatch (a JS `|| raw` and a JSX `{!!x}` are not hatches); HTML built
#    in a handler; every handler that serves text/html; state serialised into <script>; Jinja2 with autoescape off; Pug and
#    JSP, whose unescaped forms need their own file types; then HTML documents built in the BROWSER (print pipelines, popups).
rg -n --pcre2 '<%-|<%==|<%=\s*raw\b|\.html_safe\b|\{!![^}]*!!\}|(?<!\|)\|\s*(safe|raw)\b|autoescape\s*[=:]\s*(False|false)|\{%-?\s*autoescape\s+(false|off)|\bmark_safe\s*\(|\bMarkup\s*\(|\bSafeString\s*\(|th:utext|\{\{\{|\btemplate\.(HTML|JS|JSStr|URL|HTMLAttr|CSS)\s*\(|\x22text/template\x22|Html\.Raw\s*\(' "${X[@]}" .
rg -n --pcre2 '\b(res|reply)\.(send|write|end)\s*\(\s*\x60[^\x60]*<\w[^\x60]*\$\{|\b(HttpResponse|HTMLResponse|Response|make_response)\s*\(\s*f[\x22\x27][^\x22\x27]*<\w|fmt\.Fprint(f|ln)?\s*\(\s*w\s*,\s*[\x22\x60][^\x22\x60]*<\w|\becho\s+[^;]*\$_(GET|POST|REQUEST|COOKIE)|<\?=\s*\$_(GET|POST|REQUEST|COOKIE)' "${X[@]}" .
rg -n -i --pcre2 '\.type\(\s*[\x22\x27]text/html|[\x22\x27]Content-Type[\x22\x27]\s*,\s*[\x22\x27]text/html|\b(reply|res|response)\.(header|set|setHeader)\([^)]*text/html|@Header\(\s*[\x22\x27]Content-Type[\x22\x27]\s*,\s*[\x22\x27]text/html|(content_type|media_type|mimetype)\s*=\s*[\x22\x27]text/html|\bHTMLResponse\b' "${X[@]}" .
rg -n --pcre2 '<script[^>]*>[^<]*(JSON\.stringify|json\.dumps|json_encode|to_json)\s*\(|__\w*STATE\w*__\s*=\s*\$?\{?\s*JSON\.stringify|(__html|innerHTML)\s*:\s*JSON\.stringify' "${X[@]}" .
rg -n --pcre2 '\bEnvironment\s*\(|render_template\s*\(\s*[\x22\x27][^\x22\x27]+\.(j2|jinja2?|txt|tpl)[\x22\x27]' -g '*.py' "${X[@]}" .
rg -n --pcre2 '^\s*[\w.#:-]*(\([^)]*\))?\s*!=|!\{' -g '*.pug' -g '*.jade' "${X[@]}" .
rg -n --pcre2 '<%=|\$\{' -g '*.jsp' -g '*.jspx' "${X[@]}" . | rg -v 'c:out|fn:escapeXml'
rg -n -i --pcre2 '\x60\s*<!doctype\s+html|\x60\s*<html\b[^\x60]*<(head|body)\b|new\s+Blob\s*\([^)]*text/html' "${X[@]}" .

# 7–8. CSP and framing: where each is set (app, framework config, <meta>, reverse proxy) — zero hits on a repo that
#      serves HTML means no policy anywhere; then weak or disabled values; then HTML-serving configs that set neither.
rg -n -i --pcre2 'content-security-policy|contentSecurityPolicy|\bhelmet\s*\(|\bcsp\s*[:=(]|SECURE_CSP|\bCSP_\w+\s*=|content_security_policy|x-frame-options|frameguard|frame-ancestors|X_FRAME_OPTIONS|xframe_options|frameOptions|nuxt-security|autoCsp' "${X[@]}" .
rg -n --pcre2 "'unsafe-(inline|eval|hashes)'|script-src[^;\n]*?\s(\*|https?:|data:|blob:)(?![^\s;\x22\x27\x60,])|contentSecurityPolicy\s*:\s*false|frameguard\s*:\s*false|xframe_options_exempt|frameOptions\s*\(\s*(\)\s*\.\s*disable|\w+\s*->\s*\w+\.disable)|ALLOW-FROM|reportOnly\s*:\s*true|Content-Security-Policy-Report-Only" "${X[@]}" .
comm -23 <(rg -l --pcre2 'try_files[^;]*index\.html|^\s*index\s+index\.html|\bfile_server\b|DocumentRoot|express\.static|useStaticAssets|serveStatic|ServeStaticModule|sendFile\([^)]*index\.html|StaticFiles\(|http\.FileServer' "${X[@]}" . | sort) \
        <(rg -l -i --pcre2 'content-security-policy|contentSecurityPolicy|frame-ancestors|x-frame-options|\bhelmet\s*\(|frameguard' "${X[@]}" . | sort)

# 9. CSRF: is auth cookie-borne at all (no hits → § 9 is N/A); does any CSRF control exist; protection switched off;
#    GETs that mutate; every mutating route; server-rendered POST forms with no token field; then the handlers that
#    READ a cookie — on a hybrid app (bearer everywhere, one path-scoped refresh cookie) they are the whole surface.
#    The GET-that-mutates verb must END a path segment: `:id/cancel` and `logout`, never `cancellations` or `payout-accounts`.
rg -n --pcre2 'express-session|cookie-session|iron-session|next-auth|@auth/core|lucia|SessionMiddleware|SESSION_ENGINE|session_store|req\.session\b|request\.session\b|withCredentials\s*:\s*true|credentials\s*:\s*[\x22\x27]include|\b(res|reply|response)\.cookie\s*\(|\.setCookie\s*\(|cookies\(\)\.set\s*\(' "${X[@]}" .
rg -l -i --pcre2 'csrf|xsrf|lusca|CrossOriginProtection|sec-fetch-site|forgery' "${X[@]}" .
rg -n --pcre2 'csrf_exempt|csrf\s*\(\s*\)\s*\.\s*disable|\.csrf\s*\(\s*(AbstractHttpConfigurer::disable|\w+\s*->\s*\w+\.disable)|skip_before_action\s+:verify_authenticity_token|skip_forgery_protection|protect_from_forgery\s+with:\s*:null_session|validateCsrfTokens\s*\(\s*except|protected\s+\$except|WTF_CSRF_ENABLED\s*=\s*False|WTF_CSRF_CHECK_DEFAULT\s*=\s*False|checkOrigin\s*:\s*false|withNoXsrfProtection' "${X[@]}" .
rg -n -i --pcre2 '(\b(app|router|r|e|api|route|server|fastify)\.get|@(Get|GetMapping|RequestMapping)|Route::get|^\s*get|@(app|router|bp|blueprint)\.(get|route)|\bpath)\s*\(?\s*[\x22\x27]([^\x22\x27]*[/_-])?(delete|remove|destroy|logout|log-?out|sign-?out|approve|reject|cancel|confirm|transfer|pay|refund|unsubscribe|toggle|activate|deactivate|reset|grant|revoke)(?=[/\x22\x27?.]|$)' "${X[@]}" .
rg -n -i --pcre2 '@(Post|Put|Patch|Delete)(Mapping)?\s*\(|\b(app|router|r|e|api|route|server|fastify)\.(post|put|patch|delete)\s*\(|Route::(post|put|patch|delete)\s*\(|@(app|router|bp|blueprint)\.(post|put|patch|delete)\s*\(|^\s*(post|put|patch|delete)\s+[\x22\x27]' "${X[@]}" .
comm -23 <(rg -l -i --pcre2 '<form\b[^>]*method=[\x22\x27]?post' "${X[@]}" . | sort) <(rg -l -i --pcre2 'csrf|authenticity_token|_token|xsrf|hidden_tag|form_with|form_for|form_tag|th:action' "${X[@]}" . | sort)
rg -n --pcre2 '\b(req|request|ctx)\.cookies\b|@Cookies?\s*\(|\.unsignCookie\s*\(|\bcookies\(\)\.get\s*\(|\$_COOKIE\b|request\.COOKIES|\bgetCookie\s*\(' "${X[@]}" .

# 10. Auth material in web storage, or in a cookie written by script.
rg -n -i --pcre2 '(local|session)Storage\s*(\.\s*(setItem|getItem)\s*\(|\[|\.\w+\s*=(?!=))[^\n]*(token|jwt|auth|session|bearer|credential|refresh|access)|cacheLocation\s*:\s*[\x22\x27]localstorage|storage\s*:\s*(window\.)?(local|session)Storage|persistSession\s*:\s*true|document\.cookie\s*=[^;\n]*(token|jwt|auth|session)' "${X[@]}" .

# 11. Every cookie write (Fastify's is reply.setCookie) and session-cookie config; then explicit downgrades.
rg -n --pcre2 '\b(res|reply|response)\.cookie\s*\(|\.setCookie\s*\(|CookieSerializeOptions|\bhttpOnly\s*:|\bcookies\(\)\.set\s*\(|\bcookies\.set\s*\(|\bset_cookie\s*\(|\bsetcookie\s*\(|\bSetCookie\s*\(|Set-Cookie|\bnew\s+Cookie\s*\(|http\.Cookie\s*\{|ResponseCookie\.from|\bcookies(\.signed|\.encrypted|\.permanent)?\[\s*:|\bcookie\s*:\s*\{|session_store|SESSION_COOKIE_\w+|server\.servlet\.session\.cookie|[\x22\x27](secure|http_only|same_site)[\x22\x27]\s*=>' "${X[@]}" .
rg -n -i --pcre2 '\b(http_?only|secure)\s*[:=]\s*(false|0)\b|same_?site\s*[:=]\s*[\x22\x27:]?none|SESSION_COOKIE_(SECURE|HTTPONLY)\s*=\s*False|CSRF_COOKIE_SECURE\s*=\s*False|cookie\.(secure|http-only)\s*=\s*false|[\x22\x27]secure[\x22\x27]\s*=>\s*(false|env\()' "${X[@]}" .

# 12. What the client bundle carries.
#  a. Public-prefixed vars with a secret-shaped name. .env* is often git-ignored AND still read by the build.
rg -n --hidden --no-ignore --pcre2 '\b(NEXT_PUBLIC|VITE|REACT_APP|NUXT_PUBLIC|NUXT_ENV|PUBLIC|EXPO_PUBLIC|GATSBY|VUE_APP|STORYBOOK)_\w*(SECRET|PRIVATE|SERVICE_?ROLE|SERVICE_?KEY|ADMIN|PASSWORD|PASSWD|TOKEN|ACCESS_?KEY|DATABASE_URL|DB_|WEBHOOK|SIGNING|CLIENT_SECRET)\w*' "${X[@]}" .
#  b. Build config that inlines non-public env or widens the public prefix.
rg -n --pcre2 'envPrefix\s*:|[\x22\x27]process\.env[\x22\x27]\s*:|:\s*process\.env\s*[,}]|\b(DefinePlugin|EnvironmentPlugin)\b|^\s*env\s*:\s*\{|runtimeConfig\s*:' -g '*.config.*' -g '**/environments/*.ts' -g '!**/node_modules/**' .
#  c. Server-only modules imported by client code: Next.js marks it 'use client'; a Vite SPA ships its whole src/, so
#     look there for the server workspace's package or source, and for process.env (undefined unless `define` inlines it).
rg -l -0 --pcre2 '^\s*[\x22\x27]use client[\x22\x27]' "${X[@]}" . | xargs -0 -r rg -Hn --pcre2 'from\s+[\x22\x27][^\x22\x27]*(/server\b|/db\b|prisma|firebase-admin|supabase-admin|service-?role|/admin\b)|SERVICE_?ROLE'
rg --files . -g 'vite.config.*' -g '!**/node_modules/**' | xargs -r -n1 dirname | sort -u | while IFS= read -r d; do [ -d "$d/src" ] && \
  rg -Hn --pcre2 'from\s+[\x22\x27](@[\w-]+/(api|server|backend|db)\b|(\.\./)+(apps/)?(api|server|backend)/src/)|\bprocess\.env\.\w+' "${X[@]}" "$d/src"; done
#  d. The proof — secret prefixes in the built output, at any depth. Needs a production build: on a read-only target,
#     build in a throwaway worktree (`git worktree add <tmp> HEAD`, install, build) or read CI's build artifact.
#     "No files were searched" here means no build output — blocked, not clean.
B=(-uu -g '**/dist/**' -g '**/build/**' -g '**/out/**' -g '**/.next/static/**' -g '**/.output/public/**' -g '!**/node_modules/**')
rg -n --pcre2 '\b(sk_live_|rk_live_|sk-ant-|sk-proj-|AKIA[0-9A-Z]{16}|ghp_|github_pat_|xox[baprs]-|service_role|-----BEGIN [A-Z ]*PRIVATE KEY)' "${B[@]}" .

# 13. Source maps: (a) a production config that emits them, (b) maps actually present in the build output.
rg -n --hidden --pcre2 'productionBrowserSourceMaps\s*:\s*true|\bsourcemap\s*:\s*(true|[\x22\x27](inline|hidden)[\x22\x27]|\{[^}]*client\s*:\s*true)|devtool\s*:\s*[\x22\x27][\w-]*source-map|GENERATE_SOURCEMAP\s*=\s*true|[\x22\x27]sourceMap[\x22\x27]\s*:\s*(true|\{)' "${X[@]}" -g '!**/tsconfig*.json' .
rg -l 'sourceMappingURL=' "${B[@]}" .; rg --files "${B[@]}" . | rg '\.map$'

# 14. Cross-origin <script> / stylesheet with no integrity attribute (multi-line tags); scripts injected at runtime;
#     then tag managers, pixels and "custom head code" settings — whatever a runtime injector loads or writes.
rg -nU --pcre2 '<[sS]cript\b(?:(?!integrity)[^>])*\bsrc=[\x22\x27]?(https?:)?//(?:(?!integrity)[^>])*>|<link\b(?=[^>]*stylesheet)(?:(?!integrity)[^>])*\bhref=[\x22\x27]?(https?:)?//(?:(?!integrity)[^>])*>' "${X[@]}" .
rg -n --pcre2 'createElement\s*\(\s*[\x22\x27]script[\x22\x27]' "${X[@]}" .
rg -n -i --pcre2 'googletagmanager\.com|\bgtm\.js|\bgtag\s*\(|\bfbq\s*\(|connect\.facebook\.net|static\.hotjar\.com|clarity\.ms/tag|cdn\.segment\.com|snap\.licdn\.com|analytics\.tiktok\.com|\b(custom|extra|additional)_?(head(er)?|body|footer)?_?(code|scripts?|snippets?)\b' "${X[@]}" .

# 15. New-window links with no rel (multi-line tags), and window.open with no noopener (balanced parens, multi-line calls).
rg -nU --pcre2 '<a\b(?:(?!\brel=)[^>])*\btarget=\{?[\x22\x27]_blank[\x22\x27]\}?(?:(?!\brel=)[^>])*>' "${X[@]}" .
rg -nU --pcre2 '\bwindow\.open\s*\((?!(?:[^()]|\([^()]*\))*noopener)' "${X[@]}" .

# 16. Client-side authorization gates — map each to the API call it guards (§ 16 has the shortcut for large counts).
rg -n --pcre2 '\b(canActivate|canMatch|CanActivateFn|beforeEach|beforeEnter|beforeLoad|ProtectedRoute|PrivateRoute|RequireAuth|AuthGuard|withAuth|isAdmin|hasRole|hasPermission|hasAuthority|usePermissions?|useAbility|v-can|v-permission)\b|<Can\b' "${X[@]}" .
```

A finding is a grep hit **plus** a read of the enclosing component or handler that traces the value back to its source (prop → parent → fetch → the API field another user writes). The greps narrow; they do not decide. Two limits to carry into the read: a JSX tag whose attributes hold an arrow function (`=>`) can end grep 14/15's `[^>]` early, so read the tag when the file renders user links; and `No files were searched` from a file-type-scoped grep (Pug, JSP, Jinja) means that engine is absent, while from 12d / 13b it means no build output.

**Bulk triage.** A grep with more than ~50 hits (3b, 9e and 16 reach hundreds on a large app) is ranked by file before any line is read: `<grep> | cut -d: -f1 | sort | uniq -c | sort -rn`. Dismiss a whole file or directory that never reaches a browser bundle (Playwright drivers, probes, build scripts) with one read, and say so in the coverage block. Then read every remaining hit.

**Measured on a real repo** (a NestJS-on-Fastify API with a React 19 + Vite SPA, 2026-10): the old scope returned 109 grep-1 hits, and 95 of them were design canvases and audit prose. With `X` it returns 9, and that set now includes the shared print pipeline's `doc.write(html)`, which the old `document\.write` missed. Grep 3a went from 142 to 51 (about 70 were `action={<Button/>}` props), 6a from 86 to 0 (`|| raw`, `{!!x}`), 15b from 20 to 7, and 16 from 1,650 to 353. Grep 11a went from 0 source hits to 4, because it now sees `reply.setCookie`. Every seeded browser-side defect in `benchmarks/fixtures/vuln-fullstack` is still hit. Re-measured 2026-10-15 on a real NestJS + React monorepo: grep 9's GET-that-mutates line printed 35 read-only routes (`cancellations`, `confirm-attempts`, `payout-methods`) and no mutating GET; anchored to a segment end it prints 0 there, and 4 of 11 on the fixtures — `logout`, `:id/cancel`, `approve/`, `deactivate`, each a mutating GET, while the 7 read routes it dropped were noise.

## Scans for

### 1. Raw-HTML sink fed from API data or the URL

`A05:2025 · CWE-79`

```
BAD:   <div dangerouslySetInnerHTML={{ __html: comment.body }} />        // another user wrote comment.body
       <div v-html="profile.bio">   {@html post.body}   this.s.bypassSecurityTrustHtml(post.body)   $('#out').html(data.name)
GOOD:  <div>{comment.body}</div>                                          // text — the framework escapes it
       <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(comment.body, { USE_PROFILES: { html: true } }) }} />
```
A hit is a finding when the value reaches the sink from an API field, the URL or web storage with no sanitiser **at the sink**. Fix order: render as text (`{}`, `{{ }}`, `textContent`); only when the product needs rich HTML, the lane's sanitiser as the last step before the sink, with a strict config — no `ADD_TAGS` of `script`/`iframe`, no `on*` in `ADD_ATTR`, no `ALLOW_UNKNOWN_PROTOCOLS`, and no string mutation after sanitising (mutation XSS). Angular: a `bypassSecurityTrust*` over anything that is not a compile-time constant is the finding — drop the bypass and let `DomSanitizer` run. `srcdoc` with user HTML runs in the parent's origin unless the iframe carries `sandbox` without `allow-same-origin`. The same holds for a document writer under any name (`doc.write(html)`, `frame.contentDocument.write`). A same-origin, unsandboxed `about:blank` popup or frame is the app's origin. Read the HTML string it writes the way § 6 reads a client-built document. Severity: **critical** stored (one user's input renders in another's — above all an admin's — session); **high** reflected from the URL; **medium** when only a trusted admin can write the field.

### 2. Markdown / rich text rendered with HTML enabled and no sanitiser

`A05:2025 · CWE-79`

```
BAD:   const html = marked.parse(comment.md);  <div v-html="html">       <ReactMarkdown rehypePlugins={[rehypeRaw]}>
GOOD:  const html = DOMPurify.sanitize(marked.parse(comment.md));          // render THEN sanitise, never the reverse
       <ReactMarkdown rehypePlugins={[rehypeRaw, rehypeSanitize]}>
```
Renderer defaults decide it: `marked` and `showdown` pass raw HTML through — always pair with a sanitiser; `markdown-it` is safe at `html: false` and the finding is `html: true`; `react-markdown` is safe until `rehype-raw` (then `rehype-sanitize` must follow it); `allowDangerousHtml` in the remark/rehype chain; **MDX compiled from user input is code execution — critical, never a sanitiser fix**. Server-side: python-markdown → `nh3`; Redcarpet `filter_html` / `escape_html`; Parsedown `setSafeMode(true)`; league/commonmark `html_input: 'escape'` + `allow_unsafe_links: false`; goldmark without `html.WithUnsafe()`; Markdig `DisableHtml()`. **Model output is taint** — a chat UI rendering LLM markdown with HTML on is this detector; the prompt-injection chain that feeds it is `@llm-security-reviewer`'s. A sanitiser in a shared wrapper counts only if every call site goes through it. Severity as § 1.

### 3. URL-scheme sink fed from user data (`javascript:` / `data:`)

`A05:2025 · CWE-79`

Auto-escaping does not help: `javascript:alert(document.cookie)` has no character to escape, so `href="{{ user.website }}"` in Jinja, Blade, ERB or Handlebars is as live as a JSX `href={user.website}`.
```
BAD:   <a href={user.website}>    <a href="{{ user.website }}">    location.href = params.get('return')    window.open(link)
GOOD:  const safeUrl = (u) => { try { const p = new URL(u, location.origin);
         return ['https:', 'http:', 'mailto:'].includes(p.protocol) ? p.href : '#'; } catch { return '#'; } };
       <a href={safeUrl(user.website)}>                 // and validate the scheme where the URL is first stored
```
Sinks: `href`, `action`, `formaction`, `xlink:href`, `iframe`/`embed`/`object` `src`/`data`, `location` assignment / `assign` / `replace`, `window.open`, router navigation. Fix: a scheme **allow-list** after parsing — never `startsWith('javascript:')` (beaten by `JaVaScRiPt:`, leading control characters, entity encoding). Framework cover is partial. Angular sanitises `[href]`. React 19 rewrites `javascript:` in `src`/`href`/`action`/`formAction` (react-dom's `sanitizeURL`), so a JSX attribute hit on React 19 is a dismissal that cites the lockfile line. React does not block `data:`: browsers refuse top-level `data:` navigation, and an `<iframe src="data:…">` gets an opaque origin. Neither framework covers `location` or `window.open`, so those are always read. **Boundary with `ssrf-scan` § 7:** a navigation sink that takes an absolute URL is also an open redirect. One finding per sink — credited here when `javascript:` reaches it (script execution outranks a redirect), with § 7 listed as corroboration; a relative-path-only fix closes both. Severity: **high** (a `javascript:` link needs one click; an automatic `location =` needs none — critical when stored).

### 4. DOM-based XSS — URL, referrer, window name or storage into a script sink

`A05:2025 · CWE-79 (CWE-95 for the eval family)`

```
BAD:   el.innerHTML = new URLSearchParams(location.search).get('q')
       eval(location.hash.slice(1))          setTimeout('render(' + q + ')', 0)          $(location.hash)
GOOD:  el.textContent = new URLSearchParams(location.search).get('q') ?? ''
       setTimeout(() => render(q), 0)        // a function, never a string; no eval of anything from the page
```
The payload often never reaches the server (`#fragment`), so no server log, WAF or server-side review sees it. Grep 4 intersects files that read a source with files that hold a sink; read the flow inside each. jQuery `$(str)` parses HTML when the string starts with `<`. The structural fix for a large legacy DOM codebase is **Trusted Types** (`require-trusted-types-for 'script'` in the CSP), which turns every remaining string-to-sink assignment into a thrown error. Browser-side `eval` is this detector's; server-side `eval` is `injection-scan`'s. Severity: **high**.

### 5. postMessage — listener with no origin check, sender with `'*'`

`A01:2025 · CWE-346 (listener) / CWE-201 (wildcard send); A05:2025 when the data reaches an HTML sink`

```
BAD:   window.addEventListener('message', (e) => { el.innerHTML = e.data.html })   // any window may post
       parent.postMessage({ token }, '*')                                           // any embedder may read
GOOD:  window.addEventListener('message', (e) => {
         if (e.origin !== 'https://app.example.com') return;    // exact match
         render(schema.parse(e.data));                             // then validate the shape
       });
       parent.postMessage({ token }, 'https://app.example.com');
```
A check that exists can still be the finding: `e.origin.includes('example.com')`, `indexOf`, `endsWith('example.com')` (passes `evilexample.com`), an unanchored regex with unescaped dots, or a check on `e.source` alone. Not cross-window, dismiss: `Worker`, `WebSocket` and `BroadcastChannel` `onmessage`. Severity: **high** when the data reaches an HTML/code sink or triggers a state change, or a wildcard send carries a token or PII; **low** for a wildcard send of a non-sensitive UI signal (an iframe height).

### 6. Server-rendered XSS — raw template output, HTML built in a handler, state serialised into `<script>`

`A05:2025 · CWE-79`

```
BAD:   <%- user.bio %>   {{ bio|safe }}   {!! $post->body !!}   <%= raw @post.body %>   th:utext="${post.body}"   {{{ body }}}
       res.send(`<h1>Results for ${req.query.q}</h1>`)       fmt.Fprintf(w, "<p>%s</p>", q)
       <script>window.__STATE__ = ${JSON.stringify(state)}</script>     // "</script><script>…" in any field breaks out
GOOD:  <%= user.bio %>   {{ bio }}   {{ $post->body }}   <%= @post.body %>   th:text="${post.body}"   {{ body }}
       render an escaped template, not a string; Go: html/template, never text/template, for HTML
       serialise with an HTML-safe encoder (serialize-javascript, devalue) or JSON.stringify(x).replace(/</g, '\\u003c')
```
A hit is a finding when the raw expression's value derives from request or stored user data. A raw hatch over a value the server's own sanitiser produced (`sanitize`, `nh3.clean`, `format_html`) is a dismissal — cite the sanitiser line. Two traps the hatch grep cannot see: a bare `jinja2.Environment(...)` with no `autoescape=select_autoescape()` renders everything raw, and Flask's `render_template('mail.j2')` is not auto-escaped (only `.html .htm .xml .xhtml .svg` are). JSON-LD through `dangerouslySetInnerHTML` with `JSON.stringify` alone is the same breakout once any field is user-controlled — Next.js's own JSON-LD guide escapes `<` as `\u003c`. A handler that builds its HTML in a domain function and sends it with `res.type('text/html').send(buildPage(dto))` never matches the template-literal grep. Grep 6's `text/html` command lists every handler that serves HTML. Read each builder it reaches for an escape on every interpolated value. **HTML documents built in the browser are this detector too.** Waybill, receipt and label print pipelines, and popup shells, are template literals starting `<!doctype html>`. They are written into a same-origin frame or popup (`doc.write`, `srcdoc`, a `Blob` of `text/html`), so they run in the app's origin. The last grep-6 command lists them. Read every `${…}`: each one is escaped by the builder's own `esc()` / `escapeHtml()`, or is provably numeric or constant. Any other interpolation of tenant- or customer-entered text is stored XSS. **Boundary with `injection-scan`:** user input becoming the template **source** (`render_template_string(req.body)`, `ejs.render(userString)`) is SSTI, CWE-1336 — that skill's. This detector is user input as a template **value** rendered unescaped. Severity: **critical/high** stored; **high** reflected.

### 7. Content-Security-Policy missing or bypassable

`A02:2025 · CWE-693`

§ 1–6 are the fix; CSP is the second layer under them. Flag, on any origin that serves HTML:
- no enforced policy — none set, only `Content-Security-Policy-Report-Only`, or `helmet({ contentSecurityPolicy: false })`;
- `script-src` (or `default-src` when `script-src` is absent) with `'unsafe-inline'` and **no** nonce or hash, `'unsafe-eval'`, `*`, `https:`, `http:`, `data:`, or a broad CDN host that serves user-uploadable or JSONP content;
- no `object-src 'none'`; no `base-uri 'none'` / `'self'` (an injected `<base href>` re-points every relative script).

```
BAD:   script-src 'self' 'unsafe-inline' 'unsafe-eval' https:
GOOD:  script-src 'nonce-{per-response}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
       (+ require-trusted-types-for 'script' where the codebase can adopt it)
```
**Not a finding:** `'unsafe-inline'` and `https:` placed **alongside** a nonce and `'strict-dynamic'` — the deliberate backward-compatible strict policy; CSP2+ browsers ignore both. **What `'strict-dynamic'` hands over.** Any script that trusted code creates with `createElement('script')` runs inside the policy. That covers a tag manager, a pixel, and an operator's "custom head code". The CSP is therefore no control over what those injectors load. List every grep-14 injector whose URL or body comes from config or the database, and the route tree that mounts it. Mounted on authenticated or admin routes, it is a finding (§ 14). Read every place a policy can be set — app middleware, framework config, `<meta http-equiv>`, the reverse proxy's `add_header`. An nginx `add_header` inside a `location` block replaces every server-level one and covers only responses served from that block. Check every location that serves HTML, including the `try_files … /index.html` fallback; grep 7–8's file-level difference cannot tell. The common SPA miss is what grep 7–8's third command lists: `helmet()` on the API while the proxy serves `index.html` with no policy of its own — the API's headers never reach the page. The response as served is the truth: when a `/security-live-scan` report exists its header capture wins over the code read; without one, a policy read only in code is UNVERIFIED and the output says so. Severity: **medium**; **high** when the same origin carries a § 1–6 finding (no second layer under a live XSS); **low** for `'unsafe-inline'` in `style-src` only.

### 8. Clickjacking — authenticated pages frameable

`A02:2025 · CWE-1021`

```
BAD:   (no framing header)     X-Frame-Options: ALLOW-FROM https://partner.example     frameguard: false
       <meta http-equiv="Content-Security-Policy" content="frame-ancestors 'none'">       // ignored in <meta>
GOOD:  Content-Security-Policy: frame-ancestors 'none'   (or 'self' / an explicit partner list)
       + X-Frame-Options: DENY for older browsers
```
Flag an origin serving authenticated or state-changing pages that sends neither `frame-ancestors` nor `X-Frame-Options: DENY|SAMEORIGIN`, or switches it off (`frameguard: false`, `frameOptions().disable()`, `@xframe_options_exempt`). `ALLOW-FROM` is obsolete and ignored — it is no protection. `frame-ancestors` in a `<meta>` CSP is ignored. Sent by default: helmet, Django `XFrameOptionsMiddleware`, Rails, Spring Security. Not by default: bare Express, Next.js, Nuxt, SvelteKit, Laravel, FastAPI, Flask, Go `net/http`. A widget meant to be framed with no authenticated action → dismiss. Severity: **medium** on pages with one-click state changes (delete, transfer, change email, OAuth consent); **low** on read-only pages.

### 9. CSRF on cookie-authenticated state-changing routes

`A01:2025 · CWE-352`

Decide applicability first (grep 9, first command): a bearer token the browser never attaches on its own → `N/A (bearer-token API, no ambient credential)`. Cookie-borne auth → every non-idempotent route needs a token or an origin check. `credentials: 'include'` in the client is not proof of cookie auth on the API. The surface is **the routes that read the cookie** (grep 9's last command), bounded by the cookie's `Path`. A refresh cookie scoped to `/api/v1/auth` reaches only that path's handlers. On a hybrid app (bearer everywhere, one path-scoped refresh cookie), those few handlers are the whole § 9 surface. Grep 9's mutating-route list (hundreds on a large API) is then read only for routes under that path.
```
BAD:   app.get('/account/delete', requireSession, del)              // a top-level navigation fires it, Lax cookie attached
       http.csrf(AbstractHttpConfigurer::disable)                    // "it's a REST API" — while the SPA logs in with JSESSIONID
GOOD:  app.post('/account/delete', requireSession, csrfProtection, del)   // synchronizer token or signed double-submit
       + SameSite=Lax on the session cookie and an Origin check as defence-in-depth
```
Findings: protection switched off on a cookie-authenticated app (`csrf_exempt`, `.csrf().disable()`, `skip_before_action :verify_authenticity_token`, a `validateCsrfTokens(except: […])` covering cookie routes, `WTF_CSRF_ENABLED = False`, `checkOrigin: false`, `withNoXsrfProtection`); a framework with no built-in control and no middleware added (grep 9's control check lists no files — then every mutating route it lists is a candidate); a GET that mutates (`SameSite=Lax` still sends the cookie on a top-level GET); a server-rendered POST form with no token field. The control's design — synchronizer vs **signed** double-submit, why a naive double-submit fails, why `SameSite` is defence-in-depth only — is `ai-patterns/auth-flow.md` § CSRF; phrase the fix in it. Login / logout / OAuth-`state` CSRF goes to `@auth-reviewer` § CSRF. A CORS policy reflecting any `Origin` with credentials is `@api-security-reviewer`'s API8 row — cross-link it, it makes a token readable cross-origin. Severity: **critical** when it reaches takeover (change email or password with no re-auth); **high** on money, role or account mutations; **medium** on low-value ones.

### 10. Auth tokens in `localStorage` / `sessionStorage`

`A07:2025 · CWE-922`

```
BAD:   localStorage.setItem('access_token', t)     createAuth0Client({ cacheLocation: 'localstorage' })     document.cookie = `token=${t}`
GOOD:  refresh token in an HttpOnly; Secure; SameSite cookie the SERVER sets; access token in memory only — or a BFF holding both
```
Any script on the origin reads web storage, so one XSS anywhere — § 1–6, or a compromised third-party script (§ 14) — exfiltrates every token in it. A cookie written by `document.cookie` cannot be HttpOnly, so it is the same exposure. Moving tokens into cookies creates the CSRF surface: the fix names § 9's control too. The trade (XSS blast radius vs CSRF surface vs SSR) and the single-owner session module are the frontend pack's `frontend/ai-patterns/auth-session-client.md` § Where the token lives (the trade, not a verdict) — **when the frontend pack is installed**, phrase the fix in it; without it, give the GOOD line above plus § 9's control. Severity: **high** for refresh or long-lived tokens; **medium** for short-lived access tokens. The precondition is script on the origin, so on its own a § 10 row cannot pass `finding-verification.md` gate 4 (real impact). It is **Hardening** unless it chains to a § 1–6 or § 14 finding on the same origin. Chained, it takes that finding's severity and cites it.

### 11. Cookies missing `Secure` / `HttpOnly` / `SameSite`

`A02:2025 · CWE-614 / CWE-1004 / CWE-1275`

```
BAD:   res.cookie('sid', id)        SESSION_COOKIE_SECURE = False        'secure' => env('SESSION_SECURE_COOKIE')   // unset → off
GOOD:  res.cookie('__Host-sid', id, { httpOnly: true, secure: true, sameSite: 'lax', path: '/' })
```
Every cookie carrying a session, auth token, CSRF secret or PII needs `Secure`, `HttpOnly` (a double-submit CSRF cookie that JS must read is the one legitimate exception) and `SameSite=Lax|Strict` (`None` only for a deliberate cross-site embed, and then `Secure` is mandatory). Prefer the `__Host-` prefix for the session cookie: it forces `Secure`, `Path=/` and no `Domain`, which blocks sibling-subdomain cookie tossing. Read the framework's session config, not only explicit setters — the session cookie is usually configured, not set. Fastify writes with `reply.setCookie(name, value, opts)`, and the options often live in a helper returning `CookieSerializeOptions`. Grep 11 lists both, and the read goes to the helper. A `secure: false` gated on a non-production environment is a dismissal once the production branch is shown. Do not lean on browsers' Lax-by-default — it is not universal. Severity: **high** for a session cookie without `HttpOnly` or without `Secure` on an HTTPS site; **medium** for `SameSite` missing or `None` on it; **low** on non-sensitive cookies.

### 12. Secrets and internal URLs shipped in the client bundle

`A04:2025 · CWE-798 / CWE-200`

```
BAD:   NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=…          define: { 'process.env': process.env }          'use client' + import { db } from '@/server/db'
GOOD:  the key stays server-side (route handler, server action, BFF) and the browser calls that;
       only publishable keys carry a public prefix; server modules start with import 'server-only' so a client import fails the build
```
Everything the bundler inlines is public — minification is not protection. Flag a public-prefixed var holding a secret-shaped value (12a); build config that inlines non-public env or widens the prefix (12b: `env:` in `next.config.*`, Vite `define` over `process.env`, `envPrefix` set to `''` or a private prefix, `DefinePlugin` / `EnvironmentPlugin` over all env, a secret in Angular's `environment.prod.ts`); a server-only module imported by client code (12c). In Next.js that is a `'use client'` file. A Vite SPA has no such marker and ships all of `src/`, so the second 12c command reads it for the server workspace's package or source and for `process.env`. The last item is the proof: a secret prefix found in the built output (12d). A read-only target with no `dist/` and no `node_modules` blocks 12d and 13b unless the build is run in a throwaway worktree or the CI artifact is read. The output names which. Internal hostnames, staging/admin URLs and unreleased-feature flags in the bundle are **low** (reconnaissance). Publishable by design, not findings: Stripe `pk_`, Firebase web `apiKey`, Supabase `anon` key (safe only while RLS holds — say that claim is unproven here), Sentry DSN, analytics write keys, a Maps key restricted by HTTP referrer. **Boundary with `secret-scan-method`:** it owns committed secrets across tree and history, and rotation. This detector owns **client exposure** — a key in a never-committed `.env.local` still ships, which is why 12a reads ignored files. One finding per key: when it is also committed, credit `secret-scan-method` and add "also shipped to the browser". Rotate first; a rebuild does not recall bundles already cached by CDNs and users. Severity: **critical** for a server or admin credential (service-role key, secret API key, DB URL).

### 13. Production source maps published

`A02:2025 · CWE-540`

```
BAD:   build: { sourcemap: true }              // dist/assets/*.js.map deployed beside the bundle
GOOD:  build: { sourcemap: 'hidden' }  + upload to the error tracker, then delete the .map files before deploy
```
Flag production config that emits public maps — `productionBrowserSourceMaps: true`, Vite `build.sourcemap: true | 'inline'`, webpack `devtool: '…source-map'` in the production config, Angular's production `"sourceMap": true`, Nuxt `sourcemap.client: true`, Create React App without `GENERATE_SOURCEMAP=false` (it emits maps by default) — or `.map` files / `sourceMappingURL` comments in the deploy output. `'hidden'` maps that the deploy step deletes → dismiss once that step is shown. A local analysis build (the frontend pack's `bundle-analyze` builds with `--sourcemap` for its treemap) is not a deploy → dismiss. Severity: **low** (source reconnaissance); **medium** when the maps expose what § 12 looks for.

### 14. Third-party script or stylesheet without Subresource Integrity

`A08:2025 · CWE-353 / CWE-829`

```
BAD:   <script src="https://cdn.example.com/lib@1.2.3/lib.min.js"></script>
GOOD:  <script src="https://cdn.example.com/lib@1.2.3/lib.min.js" integrity="sha384-…" crossorigin="anonymous"></script>
       — or install it, so the lockfile pins it and the bundler serves it first-party
```
A cross-origin script runs with the page's full authority; a compromised CDN compromises every page that loads it. SRI is impossible for URLs whose content changes by design (Google Tag Manager, Stripe.js, Google Fonts CSS, a vendor loader) — for those, drop the SRI ask and require the vendor on the CSP allow-list (§ 7) plus a vendor inventory. Scripts injected at runtime (`createElement('script')`) are the same surface and usually cannot carry SRI.

**Runtime injectors on signed-in routes.** Under `'strict-dynamic'` an allow-list is moot (§ 7), so the control is **which routes mount the injector**. Trace each grep-14 injector (tag-manager container id, pixel id, "custom head code" body) back to where its value is written. That may be a settings endpoint, a seed, or a vendor console such as the tag manager's own workspace. Then find the provider or layout that mounts it. Mounted on the login page, the authenticated app shell or an admin console, it is a **finding**. Whoever publishes to that container or edits that field runs script in every signed-in session. That publisher sits outside the app's RBAC, MFA and audit log, can read passwords typed at login, and can act with an admin session's authority. Fix: mount injectors only in the public, signed-out route tree, or run them in a sandboxed iframe on a separate origin. While one stays live on signed-in routes, put a step-up (MFA re-auth) on the endpoint that writes it. Severity: **medium**; **high** when it covers admin routes and the container or field is editable by anyone outside the platform team. Probe: read the public config endpoint the injector loads to see whether each one is active. Otherwise: **medium** on pages that handle auth or payment; **low** elsewhere.

### 15. `target="_blank"` / `window.open` without `noopener` on user-supplied links

`CWE-1022 — hardening, no Top-10 class`

```
BAD:   window.open(user.link)                          <a href={user.website} target="_blank">
GOOD:  window.open(user.link, '_blank', 'noopener,noreferrer')      <a … target="_blank" rel="noopener noreferrer">
```
Reverse tabnabbing: the opened page gets `window.opener` and can navigate the app's tab to a phishing clone. **Current Chrome, Firefox and Safari already treat `target="_blank"` on `<a>` / `<area>` / `<form>` as `rel="noopener"`**, so on anchors this is low — add `rel` for older clients. `window.open` is **not** covered by that default, and `rel="opener"` opts back in — flag both. Only user-supplied or third-party targets; first-party static links → dismiss. Severity: **low** (anchors); **medium** (`window.open` of a user URL on an authenticated page).

### 16. Authorization enforced only in the client

`A01:2025 · CWE-602`

```
BAD:   <Can action="users.delete"><button onClick={() => api.del(`/users/${id}`)}>…    // DELETE /users/:id checks login, not role
GOOD:  the server route carries the role / permission guard; <Can> stays as UX
```
A route guard (`canActivate`, `beforeEach`, `<ProtectedRoute>`), a `<Can>` / `v-if="isAdmin"` wrapper or a hidden button is UX, not access control — the attacker calls the API directly. For each gated action, find the API call it fires and prove the server route enforces the same permission; the finding cites **both** ends. At hundreds of hits, do not map them one by one. When the server publishes a route→permission manifest or a spec asserting every route declares one (with an explicit unguarded list), verify that manifest's completeness once. Then spot-check the destructive and admin gates against it, and say so in the coverage block. API source outside this repo → the server half is `blocked (API in another repo)` and goes to the output as a PROVE item (call the endpoint with a lower-role token; expect 403). The server-side audit is `@api-security-reviewer` § API5 — Broken Function Level Authorization (BFLA), and the per-role matrix is `logic-race-scan`'s — hand both there rather than re-deriving them. Admin route tables and role names shipped to every user's bundle are **low** (reconnaissance, not access). Severity: inherits the server finding — **critical/high** for a mutating admin function any role can call.

**Open redirect is not a detector here.** A redirect target read from input — server `Location` or client navigation to any external origin — is `ssrf-scan` § 7. § 3 above takes only the `javascript:` half of a shared sink.

## Output

```
xss-scan — <scope>   lanes: React/Next (client) · Express + EJS (server-rendered)

Findings: 5

1. src/components/Comment.tsx:10                         critical  [report-with-fix]
   dangerouslySetInnerHTML={{ __html: comment.body }} — comment.body is another user's input
   (GET /api/comments → Comment.body; no sanitiser on the path). A05:2025 · CWE-79 · stored XSS.
   Fix: render {comment.body} as text; if rich text is required, DOMPurify.sanitize(…, { USE_PROFILES: { html: true } }) at this line.

2. src/lib/nav.ts:6                                      high      [report-with-fix]
   window.location.href = params.get('return') — ?return=javascript:… executes. Also an open redirect
   (ssrf-scan § 7, corroboration). Fix: relative path only (reject any scheme or leading //), else '/'.

3. .env.production:1                                     critical  [report-with-fix]
   NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY — service-role key inlined into the client bundle
   (confirmed by 12d in .next/static/chunks/). Fix: rotate first (secret-scan-method), move the calls behind a
   route handler, drop the public prefix.

4. next.config.js:4                                      medium    [report-with-fix]
   CSP script-src 'self' 'unsafe-inline' 'unsafe-eval' https: — no nonce, so 'unsafe-inline' is live; no
   object-src, no base-uri. No /security-live-scan report — the served header is UNVERIFIED.
   Fix: nonce + 'strict-dynamic' policy from middleware.ts; object-src 'none'; base-uri 'none'.

5. src/components/Admin.tsx:2                            high      [report-flagged]
   <Can action="users.delete"> is the only gate on DELETE /users/:id visible here; the API lives in another repo.
   PROVE: DELETE /users/1 with a member-role token must return 403.

Class coverage:
   1 raw-HTML sinks               checked (9 hits → 1 finding)
   2 markdown / rich text         checked (1 hit → 0 findings — rehype-sanitize follows rehype-raw)
   3 URL-scheme sinks             checked (6 hits → 1 finding)
   4 DOM-based XSS                checked (2 files → 0 findings)
   5 postMessage                  N/A (no message listener or postMessage call in repo)
   6 server-rendered XSS          checked (3 hits → 0 findings — all <%= %>, escaped)
   7 CSP                          checked (1 policy → 1 finding)
   8 clickjacking                 checked (frame-ancestors 'none' in middleware.ts → 0 findings)
   9 CSRF                         N/A (bearer-token API; no session or auth cookie)
  10 tokens in web storage        checked (0 hits → 0 findings)
  11 cookie flags                 checked (1 setter → 0 findings)
  12 client-bundle secrets        checked (2 hits → 1 finding; 12d ran on .next/static)
  13 source maps                  checked (0 config hits, 0 .map files in .next/static → 0 findings)
  14 SRI                          checked (1 hit → 0 findings — Stripe.js, CSP-allow-listed instead)
  15 noopener                     checked (2 hits → 0 findings — first-party static links)
  16 client-only authorization    blocked (API source not in repo — 1 PROVE item)
```

## False positives / gotchas

- **Constants are not taint.** In-repo i18n strings carrying markup, icon SVG strings, a JSON-LD object built only from server constants. Translation strings editable outside the repo (a CMS, a translation vendor) are stored input.
- **Sanitised at the sink is the fix, not a finding** — unless the config re-allows script vectors, the output is mutated afterwards, or sanitising happens before a markdown render or a concatenation.
- `innerHTML = ''` and `textContent` / `innerText` are safe. DOM `Element.append(string)` inserts text; only jQuery's `.append(string)` parses HTML.
- **A framework-escaped binding is not a finding** even over user data — `{user.name}`, `{{ name }}`, `<%= x %>`. Only the raw hatches and URL attributes are.
- **Tests, stories, fixtures, examples** — dismiss unless shipped (a publicly deployed Storybook is shipped). `X` already drops them; widen it back only for a shipped Storybook.
- **Bearer-token APIs have no CSRF surface** — flagging one is noise (§ 9 reports `N/A`).
- **A header set in code can be stripped or overridden at the edge.** `iac-scan` owns the proxy and edge config; `/security-live-scan` captures what is actually served.
- **No build output is `blocked`, never clean.** 12d and 13b read `dist/` / `.next/` / `.output/`. With none present, say which build to run, or run it in a throwaway worktree.
- **An accepted risk covers only what its rationale covers.** Before filing a sink, search the repo's audit and decision log for it (`rg -n -F '<sink file or setting key>' . -g '*.md'`). Re-report only the part the recorded reasoning does not address, and cite the decision. Example: "only the platform owner writes the head code" says nothing about who publishes to the tag-manager container, or about which routes mount it.

## When to run

- On any diff touching frontend code (components, templates, markdown rendering), server-rendered HTML, cookie or session config, CSP or framing headers, client-side env vars or bundler config — the signal `/security-audit` dispatches this skill on.
- Always on a whole-repo `/security-audit`: a detector whose sink does not exist reports `N/A (<reason>)`, it is not skipped.
- Before launching any public web client; after adding rich text or markdown, an embed or iframe integration, a third-party script, or a change to where auth state is stored.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the sink `<file:line>` + the source or failing condition + the fix + a severity.
- Do not report a grep hit as a finding. Every row is a hit **plus** a read of the enclosing component or handler that establishes the taint path.
- Do not end without the class-coverage block: all sixteen detectors, each `checked (k hits → m findings)` / `N/A (<reason>)` / `blocked (<reason>)`. A detector that is absent from it reads as "did not look".
- Do not propose a deny-list (`replace(/<script>/g, '')`, `startsWith('javascript:')`) or a hand-written escape function as the fix — escape through the framework, sanitise with a maintained sanitiser, allow-list schemes.
- Do not mark a CSP, framing or cookie control VERIFIED from code alone when the app has a deployed URL — it stays UNVERIFIED until the served header is seen.
- Do not re-derive another owner's finding: SSTI → `injection-scan`; open redirect → `ssrf-scan` § 7; committed-secret rotation → `secret-scan-method`; the server half of § 16 → `@api-security-reviewer`.

## Related

- `/security-audit` — dispatches this skill on its frontend / template / cookie / CSP / client-env signal and on every whole-repo run; this skill's class-coverage block feeds its XSS / CSRF / clickjacking / token-storage / client-bundle ledger row.
- `/security-fix` — consumes these findings and closes them.
- `@security-auditor` — its A05 XSS bullet and A02 CSP / framing bullets are the detectors; this skill is the executor behind them.
- `@auth-reviewer` — § CSRF and § Sessions (cookie-based) own the auth-surface slice; this skill sweeps every other cookie-authenticated route.
- `@api-security-reviewer` — the server half of § 16 (API5) and CORS with credentials (API8).
- `@llm-security-reviewer` — prompt injection that turns model output into § 2's stored input.
- `ssrf-scan` § 7 — open redirect. `injection-scan` — SSTI, server-side eval, prototype pollution (including client-side query-string parsers). `secret-scan-method` — committed secrets and rotation; § 12 here is what shipped. `data-exposure-scan` — exposed internal files and fingerprinting headers; source maps are § 13 here. `file-access-scan` — SVG / HTML uploads served inline (stored XSS through an upload). `iac-scan` — headers set at the edge.
- `ai-patterns/auth-flow.md` § CSRF; `rules/security-principles.md` — the output-encoding, session-cookie, CSP and CSRF rules.
- **Frontend pack, when installed:** `frontend/rules/frontend-principles.md` § Must not (raw HTML without a sanitiser); `frontend/ai-patterns/auth-session-client.md` § Where the token lives (the trade, not a verdict) for § 10's fix; `@ui-reviewer`, which blocks XSS-shaped raw HTML and client-side secrets at review time — this skill is the repo-wide sweep behind it; `ssr-audit` for hydration, where § 6's state serialisation is the security half. Without the frontend pack, phrase fixes against `rules/security-principles.md` and the GOOD lines above.
