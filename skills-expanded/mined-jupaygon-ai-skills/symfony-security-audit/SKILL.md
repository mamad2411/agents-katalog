---
name: symfony-security-audit
description: Read-only security audit for Symfony 6.x/7.x codebases. Covers 10 recurring antipatterns and 4 deep dives (multi-tenant/IDOR, SSRF, EasyAdmin, auth flows) with grep-based scan plans and a strict severity-grouped report. Use when the user asks to audit a Symfony repo, review for OWASP Top 10 issues, or scan for IDOR/SSRF/auth weaknesses. Reports findings with file:line evidence; never auto-fixes.
---

# Symfony Security Audit — Skill for AI Coding Agents

Target: Symfony 6.x / 7.x applications

Some examples use `#[MapQueryParameter]` (Symfony 6.3+). On 6.0–6.2, replace with `filter_var($request->query->get('id'), FILTER_VALIDATE_INT)` and reject non-int values explicitly.

This skill turns your AI coding agent into a Symfony security auditor. It covers 10 recurring antipatterns and 4 deep-dive categories, with grep-based scan plans and a strict report format. Read-only by design — the agent reports, a human decides what to fix.

Sources:
- https://owasp.org/Top10/
- https://symfony.com/doc/current/security.html
- https://symfony.com/doc/current/rate_limiter.html
- https://symfony.com/doc/current/html_sanitizer.html
- https://github.com/nelmio/NelmioSecurityBundle

---

## When to use

- You want a security pass on a Symfony 6/7 project before merging, before release, or as a periodic health check.
- You are starting a new Symfony project and want guardrails before writing the first controller.
- A code review surfaced a suspected security issue and you want a structured sweep of related code paths.

Do NOT use for: non-Symfony codebases, generic security questions, runtime / blackbox pentesting.

---

## Modes

### Mode `pre` — new or early-phase project

Use when the project has few or no controllers. No deep scan needed.

Steps:

1. Confirm Symfony 6 / 7 via `composer.json` (`symfony/framework-bundle` version).
2. Verify baseline configs are present (or flag as TODO). See **Configuration baseline** below.
3. Print the **10 patterns** as a guardrails checklist for the team to build against.
4. Offer to add `docs/security-checklist.md` to the repo (only if the user agrees).

Keep output ≤ 25 lines, in the user's language, telegraphic.

### Mode `existing` — established codebase

Use when the project has a real controller/entity surface. Run the full scan plan below.

If your agent runtime supports isolated sub-agents or background tasks (Claude Code `Agent`, Cursor background agents, etc.), delegate the scan to one so the main conversation context stays clean. Otherwise, run it inline.

Return the report, then surface the top 3 Critical / High findings by impact. Wait for the user to pick which to fix — do not auto-fix, do not open PRs.

---

## Configuration baseline (both modes start here)

Verify these five controls. Any missing → flag as a baseline finding.

| Control | Check | Expected |
|---|---|---|
| `login_throttling` | `config/packages/security.yaml` | Present under `firewalls.main.login_throttling` with `max_attempts` and `interval`. |
| Security headers bundle | `composer.json` | `nelmio/security-bundle` installed (or equivalent CSP / HSTS / clickjacking / nosniff config). |
| Session cookie flags | `config/packages/framework.yaml` | `session.cookie_httponly: true`, `cookie_secure: true`, `cookie_samesite: lax`. |
| Trusted hosts | `config/packages/framework.yaml` or env | `kernel.trusted_hosts` set (not empty). |
| Remember-me server-side revocation | `config/packages/security.yaml` | If `remember_me` is used: `token_provider.doctrine: true` + `rememberme_token` table. |

---

## The 10 patterns

| # | Pattern | Signals to look for | One-line remediation |
|---|---|---|---|
| 1 | SQL / DQL injection | `executeQuery(".*{` interpolating variables; `sort[` without a whitelist in controllers / EasyAdmin; DQL string concatenation. | Typed placeholders (`:id` + `ParameterType::INTEGER`); whitelist `sort[]` against `ClassMetadata::getFieldNames()` in an EventSubscriber. |
| 2 | Command injection | `exec(`, `shell_exec(`, `system(`, `passthru(`, backticks with interpolated variables. | `Symfony\Component\Process\Process` with arguments as an array; for FS use native PHP (`mkdir`, `chmod`). |
| 3 | Missing rate limiting | No `login_throttling` in security.yaml; no `framework.rate_limiter`; signup / password-reset / API endpoints with no consumer. | `security.firewalls.main.login_throttling` + `framework.rate_limiter` with `sliding_window` or `token_bucket`; consume by IP in controllers. |
| 4 | Secrets stored in plaintext | Columns such as `apiKey`, `token`, `secret` queried via `findOneBy(['apiKey' => $raw])` without `hash()`. | For **high-entropy machine-generated tokens** (API keys, session tokens): store only `hash('sha256', $token)`; show the plain value exactly once at creation time; look up by the hash. For **user passwords** (low entropy): never sha256 — use `UserPasswordHasherInterface` (bcrypt / argon2id) via `security.password_hashers`. |
| 5 | Security headers + cookies | `nelmio/security-bundle` missing; no CSP / HSTS / clickjacking / nosniff configured; session without `cookie_httponly` / `cookie_secure` / `cookie_samesite`. | Install `nelmio/security-bundle` with CSP including `frame-ancestors 'none'` (modern) or `X-Frame-Options: DENY` (legacy UA fallback); HSTS (`max_age: 31536000`), nosniff, referrer-policy. Session cookies `httponly + secure + samesite: lax`. |
| 6 | Unsigned webhooks | `POST /webhook/...` endpoints that don't call `hash_equals`, don't validate a DTO with `Validator`, and parse the body via `$request->request->all()`. | `hash_equals(hash_hmac('sha256', $raw, $secret), $sig)` over raw `$request->getContent()`; deserialize to a DTO and validate with `Assert` before processing. |
| 7 | XSS | `\|raw` in Twig over user- or LLM-generated content; values reflected into `<script>` without `\|json_encode`; `.php` / `.phtml` scripts under `public/` interpolating `$_GET` with no escape. | Default Twig escape; for limited HTML use `\|sanitize_html` (html_sanitizer); `\|json_encode` for values inside `<script>`. In `public/*.php` / `*.phtml`: whitelist regex + `htmlspecialchars` with `ENT_QUOTES \| ENT_SUBSTITUTE`. |
| 8 | Missing param whitelist | Variable-keyed reads from the request: `$req->get($k)`, `$req->query->get($k)`, `$req->request->get($k)`, `$req->attributes->get($k)` where `$k` is user-controlled. Filter / session setters accepting arbitrary fields; no `const ALLOWED_*`. Note: `Request::get()` is deprecated in 6+; prefer the specific bag, but the signal is identical. | `const ALLOWED_KEYS = [...]` + `match($key) { ... }` with per-key validation; reject unknown keys with `BadRequestHttpException`. |
| 9 | Path traversal | FS operations taking user input without `realpath()`; regex that only filters `..` or `/`. | `realpath($base . '/' . $input)` + `str_starts_with($resolved, $base . '/')`; throw `NotFoundHttpException` if the resolved path leaves the base directory. |
| 10 | Weak audit logging | `Log::debug` with full `headers` / `body`; no listener for `SwitchUserEvent`; permission changes or admin deletes with no trail. | An `AuditLogger` service that redacts `['password','token','apikey','secret','authorization','cookie']` via `array_walk_recursive`; listeners for switch_user, login fail, admin mutations with `{actor, target, ip, timestamp}`. |

---

## Field-observed sub-patterns

The patterns above are the categories. The sub-patterns below are concrete shapes that recur in production codebases — surface them under the matching pattern number when you find them.

### 8a — Implicit type trust on untrusted input

Two recurring shapes share one root cause: the app validates **what** the user sent (the key, the field name) but not **how** it is typed when later consumed. With `declare(strict_types=1)` enabled, every implicit cast becomes a 500.

**Typed-fallback through session.** A "save-session" or "preferences" endpoint accepts a `(parameter, value)` pair, whitelists the **key** (e.g. `company_id`, `network_id`, `lang`) but stores the **raw value** as `mixed`. Downstream code reads `$session->get('company_id')` and passes it to a typed signature `?int $id`. A user with valid CSRF can poison their own session with a string and turn every subsequent admin request into a 500 with stacktrace — DoS + fingerprinting.

```php
// SessionController — current
$session->set($parameter, $value);            // ← $value is whatever the user POSTed

// MakeFilterDataTrait — downstream read
$companyId = (filter_var($req->get('company_id'), FILTER_VALIDATE_INT) ?: null)
    ?? $session->get('company_id')             // ← string from poisoned session
    ?? $first?->getId();
$service->doStuff($companyId);                 // TypeError: Argument must be ?int
```

**Implicit scalar cast on JSON body field.** Controllers that read `json_decode($request->getContent(), true)` and pass values to a service that does `(string) $value` / `(int) $value`. With `declare(strict_types=1)` and `$value` being an array, `(string) []` triggers `Warning: Array to string conversion` → ErrorException → 500.

```php
$data  = json_decode($request->getContent(), true);
$value = $data['value'] ?? '';
$service->set($user, $field, (string) $value); // (string) array = ErrorException
```

**Remediation (both shapes):** validate type at the trust boundary, not the use site. For session setters: `match` over the key with a per-key validator (`'company_id' => fn($v) => filter_var($v, FILTER_VALIDATE_INT) !== false`). For JSON bodies: a DTO with `Assert\Type` constraints, or `is_scalar` + explicit cast in the controller before calling the service. Defensive cast on read where the writer cannot be fixed.

### 9a — Resource-locator concatenation

Template names, route names, controller FQCNs, and asset paths built by string concatenation with user input.

```php
// Antipattern — case-sensitive FS makes the "whitelist" enumerable
return $this->render(
    'custom/foo/step2-' . $request->get('vendor') . '.html.twig',
    $vars,
);

// Antipattern — forward to a user-named action
return $this->forward('App\\Controller\\' . $request->get('handler') . 'Controller::index');
```

A user-supplied `vendor=fortimanager` (lowercase) bypasses any DB-side case-insensitive lookup and trips Twig's case-sensitive `FilesystemLoader`, leaking the prod `releases/<n>/` path in the stack trace. Worse for `forward()`: it's a controller-injection primitive.

**Remediation:** map the user-supplied fragment to a canonical value before locating the resource. Either render only on a fixed whitelist (`match($vendor) { 'forti' => 'step2-Forti.html.twig', ... }`) or use the canonical attribute of the looked-up entity (`$vendor->getApi()`) — never the raw request string.

### 10a — Sentry / Monolog: silence intentional 4xx

`MapRequestPayload`, rate limiters, EasyAdmin's permission checks and `BadRequestHttpException` validators all throw subclasses of `HttpException`. Symfony returns the right 4xx; Sentry, by default, captures them as errors. A payload-fuzzing probe can pump hundreds of "errors" per minute, drowning the signal of a real intrusion.

```yaml
# config/packages/sentry.yaml
sentry:
    options:
        excluded_exceptions:
            # 422 — DTO failed validation (correct rejection)
            - 'Symfony\Component\HttpKernel\Exception\UnprocessableEntityHttpException'
            # 415 — POST without the right Content-Type (correct rejection)
            - 'Symfony\Component\HttpKernel\Exception\UnsupportedMediaTypeHttpException'
            # 429 — rate limiter triggered (defense working as designed)
            - 'Symfony\Component\HttpKernel\Exception\TooManyRequestsHttpException'
            # 403 — EasyAdmin ACL refused (the ACL is the security control)
            - 'EasyCorp\Bundle\EasyAdminBundle\Exception\ForbiddenActionException'
```

**Audit step:** open `config/packages/sentry.yaml`. If `excluded_exceptions` is missing or only excludes `HttpException` wholesale, list the four above as a finding (Low / operational hygiene). Validate against actual Sentry volume — keeping a 422 visible during early dev is fine; once the endpoint is stable, silencing it is correct so real attacks stay above the noise floor.

---

## The 4 deep dives

These are the most frequent and costly issues in real Symfony projects. Always review them.

### Multi-tenant / IDOR — dominant antipattern

- **Symptom:** controllers call `$repo->find($request->get('id'))` without checking that the entity belongs to the current user's tenant. Roles and listing filters do NOT substitute for an ownership check.
- **Grep:** `->find\(`, `findOneBy\(\['id'` inside `src/**/Controller/**`. For each match, verify the controller / service calls an `assertXxxAccess` helper / Voter / tenant filter in the same flow.
- **Remediation:** a helper on `BaseController` that takes `int` and returns the entity if the user owns it, otherwise throws `AccessDeniedHttpException`. Controllers pass a typed ID via `filter_var + FILTER_VALIDATE_INT` or `#[MapQueryParameter] int`.

Example:

```php
abstract class BaseController extends AbstractController {
    protected function assertCompanyAccess(int $id): Company {
        if ($this->isGranted('ROLE_SUPER_ADMIN')) {
            return $this->companyRepo->find($id) ?? throw new NotFoundHttpException();
        }
        $owned = $this->companyRepo->findOneBy([
            'id'     => $id,
            'tenant' => $this->getUser()->getAllowedTenantIds(),
        ]);
        return $owned ?? throw new AccessDeniedHttpException();
    }
}

public function metrics(#[MapQueryParameter] int $companyId): JsonResponse {
    $company = $this->assertCompanyAccess($companyId);
    return $this->json($this->metrics->build($company));
}
```

### SSRF — user-supplied URLs

- **Symptom:** the project lets a user enter a URL (adapter config, webhook destination, API base) and consumes it with `HttpClient` without validating the destination.
- **Grep:** `HttpClientInterface`, `HttpClient::create`, `->request\(` with a URL originating from a Request or a user-editable entity field.
- **Remediation:** an `ApiUrlValidator` that rejects (a) hostnames in a blocklist (`localhost`, `169.254.169.254`, `metadata.google.internal`, `metadata.amazonaws.com`, `fd00:ec2::254`), (b) IP literals in private / reserved ranges via `FILTER_VALIDATE_IP | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE`. Note: DNS rebinding exists; where possible, resolve the IP up-front and pass it to HttpClient via `resolve` to pin it between validation and request.

Example:

```php
final class ApiUrlValidator {
    public function __construct(private readonly array $blockedHostnames = []) {}

    public function isValid(?string $url): bool {
        if (!$url || !filter_var($url, FILTER_VALIDATE_URL)) return false;
        $parts = parse_url($url);
        if (!in_array($parts['scheme'] ?? '', ['http', 'https'], true)) return false;
        $host = strtolower($parts['host'] ?? '');
        if ($host === '') return false;
        if (in_array($host, $this->blockedHostnames, true)) return false;
        if (filter_var($host, FILTER_VALIDATE_IP)) {
            return filter_var(
                $host,
                FILTER_VALIDATE_IP,
                FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE,
            ) !== false;
        }
        return true;
    }
}
```

### EasyAdmin — mandatory overrides

- **Symptom:** a CRUD controller extends `AbstractCrudController` without overriding `detail / edit / delete`; `disableActions: []` enables deletion with no ownership check.
- **Grep:** `extends AbstractCrudController` in `src/**/Controller/**/*CrudController.php`. Read each one: look for overrides of `detail`, `edit`, `delete` and a call to `assertOwned` or `isGranted('VIEW', $entity)`.
- **Remediation:** a base `HardenedCrudController` that overrides all three actions with `assertOwned(AdminContext)` (SUPER_ADMIN bypass; everyone else checks `$entity->getTenant()->getId() ∈ user->getAllowedTenantIds()`). Add an EventSubscriber validating the `sort[]` query param against `ClassMetadata::getFieldNames()` + direction ∈ {ASC, DESC}.

Example:

```php
abstract class HardenedCrudController extends AbstractCrudController {

    public function createIndexQueryBuilder(SearchDto $s, EntityDto $e, FieldCollection $f, FilterCollection $fi): QueryBuilder {
        $qb = parent::createIndexQueryBuilder($s, $e, $f, $fi);
        if (!$this->isGranted('ROLE_SUPER_ADMIN')) {
            $qb->andWhere('entity.tenant IN (:tenants)')
               ->setParameter('tenants', $this->getUser()->getAllowedTenantIds());
        }
        return $qb;
    }

    public function detail(AdminContext $c): KeyValueStore|Response { $this->assertOwned($c); return parent::detail($c); }
    public function edit(AdminContext $c):   KeyValueStore|Response { $this->assertOwned($c); return parent::edit($c); }
    public function delete(AdminContext $c): KeyValueStore|Response { $this->assertOwned($c); return parent::delete($c); }

    private function assertOwned(AdminContext $c): void {
        if ($this->isGranted('ROLE_SUPER_ADMIN')) return;
        $entity  = $c->getEntity()->getInstance();
        $allowed = $this->getUser()->getAllowedTenantIds();
        if (!$entity || !in_array($entity->getTenant()?->getId(), $allowed, true)) {
            throw $this->createAccessDeniedException();
        }
    }
}
```

### Auth flows — signup, verification, session

- **Symptom (common):** `GET /signup/finalize?hash=abc` validates the hash; `POST /signup/finalize` doesn't revalidate it and accepts creating an account with any POSTed email. Or: remember-me without `token_provider: doctrine` → a cookie stolen via XSS survives logout.
- **Grep:** controllers named `signup`, `register`, `finalize`, `reset` — check token revalidation at every step. `remember_me` in security.yaml — confirm `token_provider.doctrine: true`. Signup — confirm `NotCompromisedPassword` and `PasswordStrength`.
- **Remediation:** in multi-step flows, each POST re-reads the temp record by `(hash, email)` and rejects 403 on mismatch. Remember-me with the doctrine provider + `rememberme_token` table; logout invalidates. Passwords: `Assert\NotCompromisedPassword(skipOnError: true)` + `Assert\PasswordStrength(minScore: STRENGTH_STRONG)` + `Assert\Length(min: 12)`.

Example DTO:

```php
final class SignupDto {
    #[Assert\Email(mode: 'strict')]
    #[Assert\NotBlank]
    public string $email = '';

    #[Assert\NotBlank]
    #[Assert\Length(min: 12)]
    #[Assert\PasswordStrength(minScore: Assert\PasswordStrength::STRENGTH_STRONG)]
    #[Assert\NotCompromisedPassword(skipOnError: true)]
    public string $password = '';

    #[Assert\NotBlank]
    public string $hash = '';  // revalidated against the temp record
}
```

---

## Scan plan

Run the searches in parallel (one `Grep` / `Glob` per signal). Read only files with matches — never the whole tree.

### Block A — Injection (patterns 1, 2, 7)

- `Grep "executeQuery\(.*\{|executeStatement\(.*\{"` — SQL concat.
- `Grep "exec\(|shell_exec\(|system\(|passthru\("` outside `vendor/`.
- `Grep "\|raw"` in `templates/**/*.twig`. For each match, classify: (a) `|raw` applied to a string constant / controller-built HTML → low risk; (b) `|raw` applied to a variable that ultimately traces to user input, request data, DB content of user origin, or LLM output → finding. Only (b) is reported; note the classification in the finding so it can be audited.
- `Glob "public/**/*.php"` and `public/**/*.phtml` — read each; look for `$_GET` / `$_POST` without `htmlspecialchars` / validation.
- `Grep "sort\[" --glob "src/**/Controller/**"` — EasyAdmin or paginator sort without whitelist.

### Block B — Access control / IDOR (deep dive 1 + pattern 8)

- `Grep "->find\(|->findOneBy\(\['id'" --glob "src/**/Controller/**"` — each match is a lookup; open the controller and verify an ownership check in the same method (or a helper called before).
- `Glob "src/**/Controller/**/*CrudController.php"` — EasyAdmin; read each and verify overrides of `detail / edit / delete`.
- `Read config/packages/security.yaml` — list `access_control` and firewalls; flag admin endpoints without a role.
- `Grep "\$session->set\("` followed by a variable argument — potential session poisoning. Cross-reference with every `\$session->get\(` consumed by a typed signature (sub-pattern **8a — typed-fallback**).
- `Grep "(string)|(int)|(float)" --glob "src/**/Controller/**" --glob "src/**/Service/**"` filtered to lines also touching `json_decode` / `request->getContent` / `\$data\[` — implicit scalar casts on JSON bodies (sub-pattern **8a**).
- `Grep "->render\('.*' \. |->forward\('.*' \. " --glob "src/**/Controller/**"` — twig render or controller forward built by concatenating user input (sub-pattern **9a**).

### Block C — Auth / session (patterns 3, 4 + deep dive 4)

- `Read config/packages/security.yaml` — look for `login_throttling`, `remember_me.token_provider.doctrine`.
- `Read config/packages/framework.yaml` — `cookie_httponly`, `cookie_secure`, `cookie_samesite`, `trusted_hosts`, `rate_limiter`.
- `Grep "signup|finalize|reset" --glob "src/**/Controller/**"` — record hash revalidation in POSTs.
- `Grep "NotCompromisedPassword|PasswordStrength" --glob "src/**"`.
- `Grep "findOneBy\(\['apiKey'|findOneBy\(\['token'" --glob "src/**"` — plaintext credentials.

### Block D — SSRF / webhooks (pattern 6 + deep dive 2)

- `Grep "HttpClientInterface|HttpClient::create|->request\(" --glob "src/**"` — HTTP call sites; check if the URL comes from the user.
- `Grep "FILTER_FLAG_NO_PRIV_RANGE|blocked_hostnames|169\.254"` — SSRF validator present or not.
- `Grep "webhook" --glob "src/**/Controller/**"` — each webhook must call `hash_equals`.

### Block E — Observability / headers / secrets (patterns 5, 10)

- `Read composer.json` — `nelmio/security-bundle` present?
- `Grep "Log::(debug|info).*header|json_encode.*\$request->headers"` — possible log leaks.
- `Read .gitignore` — `.env.local`, `.env.*.local`, `.env.*.php` excluded?
- `Grep "SwitchUserListener|SwitchUserEvent"` — is switch_user audited?
- `Grep "exec\(\"mkdir|exec\(\"chmod|exec\(\"rm"` — FS via shell instead of native PHP.
- `Read config/packages/sentry.yaml` (or `monolog.yaml`) — verify `excluded_exceptions` covers Symfony's intentional 4xx (sub-pattern **10a**): `UnprocessableEntityHttpException`, `UnsupportedMediaTypeHttpException`, `TooManyRequestsHttpException`, `EasyCorp\...\ForbiddenActionException`. Missing → noise that masks real attacks.

---

## Output format

The report template below is the exact shape the agent must produce. Translate section names to the user's language at emit time; keep code identifiers and config keys verbatim.

```markdown
# Symfony Security Audit — <repo-name>

**Date:** YYYY-MM-DD
**Symfony:** <version from composer.json>
**Scope:** <n controllers, n entities, n twig, n yaml files read>

## TL;DR

- <top finding 1 with severity>
- <top finding 2>
- <top finding 3>

## Configuration baseline

| Control | Status | Evidence |
|---|---|---|
| login_throttling | ✓ / ✗ / partial | `config/packages/security.yaml:L12` |
| cookie_samesite=lax | ... | ... |
| NelmioSecurityBundle | ... | `composer.json` |
| remember_me token_provider doctrine | ... | ... |
| trusted_hosts | ... | ... |
| .env.local in .gitignore | ... | `.gitignore:L3` |

## Findings

### Critical

#### C-01 · <short title>
- **Pattern:** <1-10 or deep dive 1-4>
- **File:** `src/.../Foo.php:42`
- **Symptom:** <1-2 lines citing the code or the missing control>
- **Remediation:** <1 line, taken from the pattern table / deep dive>

### High
...

### Medium
...

### Low
...

## Suggested actions (by impact)

1. <action> — covers N findings · affects `<category>`
2. <action>
3. ...

## Recommended regression tests

- IDOR: endpoints `<list>` — test that a user in tenant A gets 403 when requesting resources in tenant B.
- CSRF: forms `<list>` — test that POST without token fails.
- SSRF: validator — test with `127.0.0.1`, `localhost`, `169.254.169.254`.

## Methodology notes

<one line if scope was partial or likely false positives>
```

---

## Severity criteria

- **Critical** — exploitable IDOR (entity loaded by ID without ownership), SQL injection, auth bypass, potential RCE.
- **High** — reflected XSS, exploitable SSRF, plaintext credentials, missing rate limit on login / signup.
- **Medium** — missing security headers, weak password policy, incomplete cookie flags, unsigned webhook.
- **Low** — accessible debug routes, theoretical path traversal, verbose metadata logging.
- If undecidable from code alone: **"needs user verification"**.

---

## Rules the agent must follow

- **Read-only.** Never edit, write, run shell that modifies state, or open PRs.
- **Evidence-based.** Every finding cites `file:line`. No evidence → no finding.
- **Honest.** If something cannot be determined from code, say "needs user verification" — never guess.
- **Structured output.** Produce the report in the format above. No preamble, no process narration.
- **No auto-fix.** The user picks which findings become PRs.

---

## Do NOT include in the report

- Your process (what greps you ran, what you read).
- "I suggest you open a PR..." — you report, the user decides.
- Inline code patches. Only the one-line remediation from the pattern table / deep dive.
- Findings without `file:line`.
- Subjective judgments ("smells bad"). Objective code signals only.

---

## Honest limits

If the codebase is large (> 500 PHP files), do a reasoned sample: all controllers, all entities, templates containing `|raw`, configs in full. Document in "Methodology notes" what was left out.

---

## Using this skill

### Claude Code

Copy this skill into your project, or reference it from a central location:

```bash
cp -r skills/symfony-security-audit /your-project/.claude/skills/
```

Invoke it by asking the agent: "audit my Symfony project using the symfony-security-audit skill, in `pre` mode" (or `existing`).

For mode `existing` in large codebases, ask the agent to delegate the scan to a sub-agent via the `Agent` tool so the main conversation stays clean.

### Cursor / Windsurf

Add the `SKILL.md` to your project context (`.cursor/rules/` or `.windsurfrules`). Ask the agent to apply it when auditing a Symfony project.

### Generic agents

Include the file in your system prompt or project documentation. Ask the agent to run the scan plan and return the report in the specified format.

---

## Changelog

- **1.1.0** — added "Field-observed sub-patterns" section after the patterns table:
    - **8a** Implicit type trust on untrusted input — typed-fallback through session, scalar casts on JSON body fields.
    - **9a** Resource-locator concatenation — twig template names and controller forwards built by string concatenation with user input.
    - **10a** Sentry / Monolog config — silence Symfony's intentional 4xx (`UnprocessableEntity`, `UnsupportedMediaType`, `TooManyRequests`, `ForbiddenAction`) so real attacks stay above the noise floor.
  Scan plan extended in Block B (session-poisoning cross-ref, JSON scalar-cast grep, render-concat grep) and Block E (sentry.yaml `excluded_exceptions` check).
- **1.0.0** — initial release. 10 patterns + 4 deep dives + 5-block scan plan + strict report template.
