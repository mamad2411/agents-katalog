---
name: symfony-security
description: Symfony / PHP webapp security review — Security Component (firewalls, voters, access_control, role hierarchies), Doctrine ORM injection patterns (raw DQL, QueryBuilder, expr()), Twig auto-escape and |raw, CSRF + session, PHP-specific RCE classes (unserialize, include/require, system/exec, eval, type juggling), configuration discipline (.env, secrets vault, profiler in prod), and recent Symfony CVE patterns. Covers Symfony-based CMSes (Sulu, Ibexa, Bolt) and custom Symfony webapps.
---

# Symfony Security

## When to use

This skill is the Symfony/PHP-specific layer on top of `secure-coding`. Symfony has a sophisticated Security Component but plenty of foot-guns: firewall ordering, missing voters, Doctrine string-interpolation, Twig opt-outs, and PHP's enduring RCE classes (unserialize gadget chains, dynamic includes, type juggling).

Triggers on:

- A question like "review this Symfony app for security", "is our security.yaml correct", "Doctrine SQLi check", "Twig |raw on user input", "PHP unserialize on request body", "Symfony Profiler in prod".
- Presence of `composer.json` with `symfony/*` packages, `config/packages/security.yaml`, `config/services.yaml`, `src/Controller/`, `src/Entity/`, `templates/*.twig`, `bin/console`.
- A PR that touches `security.yaml`, voter classes, Doctrine repositories with raw SQL or DQL, Twig templates with `|raw`, or any controller that calls `unserialize()`, `include $var`, `system()`, or `eval()`.
- Symfony version bumps or security advisories from the Symfony blog.
- A handoff from `security-review` or `api-security` when Symfony is in the stack.
- A Symfony-based CMS (Sulu, Ibexa, Bolt) review.

### When NOT (handoff)

- General PHP secure-coding (not Symfony-specific) → `secure-coding`.
- API design and OWASP API Top 10 → `api-security`. Use this skill for the Symfony-specific implementation; that skill for the conceptual API layer.
- SAST tooling (Psalm, PHPStan, Phan with security rules, Semgrep `p/php`) → `sast-orchestrator`.
- Dependency vulns in `composer.lock` → `cve-triage`.
- Container/host hardening for the PHP-FPM + nginx/Apache stack → `container-hardening`.
- Secrets in `.env`, `parameters.yaml`, or external vault → `secrets-scanner`.
- Drupal specifically — uses many Symfony components but has fundamentally different architecture (services, hooks, routing). Out of scope here; warrants its own skill in a future round.
- WordPress, Laravel — different framework families; this skill stays focused on Symfony and Symfony-based CMSes.

## Approach

Eight phases. Phase 1 (security.yaml) is where most production bugs sit; phase 5 (PHP RCE classes) is where Symfony skill diverges most from the other framework-specific skills.

### 1. Security Component: security.yaml

Symfony's Security Component is configured in `config/packages/security.yaml`. The structure:

```yaml
security:
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'

    providers:
        app_user_provider:
            entity: { class: App\Entity\User, property: email }

    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            lazy: true
            provider: app_user_provider
            entry_point: form_login
            form_login: { ... }
            logout: { ... }

    access_control:
        - { path: ^/admin, roles: ROLE_ADMIN }
        - { path: ^/api, roles: IS_AUTHENTICATED_FULLY }

    role_hierarchy:
        ROLE_ADMIN: [ROLE_USER]
        ROLE_SUPER_ADMIN: [ROLE_ADMIN, ROLE_ALLOWED_TO_SWITCH]
```

Common foot-guns:

- **Firewall order matters**. Symfony walks the `firewalls` map top-down and applies the first match. A broad pattern early (e.g. `pattern: ^/`) eats subsequent firewalls. Specific patterns first, generic last.
- **`dev` firewall in production**. The `dev` firewall has `security: false` for the profiler/asset paths. If somehow `dev` patterns leak into prod (mistyped pattern, copy-paste), parts of the site become unauthenticated. Cross-check the prod environment loads `security.yaml` without dev overrides.
- **`access_control` is order-sensitive too**. First matching rule wins; the rest is ignored. A `path: ^/api` rule above a `path: ^/api/admin, roles: ROLE_ADMIN` rule means admin endpoints are only IS_AUTHENTICATED, not ROLE_ADMIN.
- **`IS_AUTHENTICATED` levels**: `IS_AUTHENTICATED_REMEMBERED` < `IS_AUTHENTICATED_FULLY` < `IS_AUTHENTICATED_ANONYMOUSLY`. For sensitive actions use FULLY; remembered tokens are weaker (cookie-based, can be stolen without re-auth).
- **`role_hierarchy`** uses arrays of "roles inherited by this role". A common bug: `ROLE_ADMIN: ROLE_USER` (string instead of `[ROLE_USER]`) silently fails for ROLE_USER inheritance. Always use array notation.
- **Anonymous auth**: in newer Symfony (5.3+) anonymous is gone; access is implicit when no firewall matches. Pre-5.3, an `anonymous: ~` line in firewall config is intentional but worth flagging.

### 2. Voters and method-level authorization

Route-level `access_control` is coarse. Sensitive actions need voters.

```php
final class PostVoter extends Voter
{
    public const EDIT = 'POST_EDIT';

    protected function supports(string $attribute, $subject): bool
    {
        return $attribute === self::EDIT && $subject instanceof Post;
    }

    protected function voteOnAttribute($attribute, $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        if (!$user instanceof User) return false;
        return $subject->getAuthor() === $user;
    }
}
```

Then in the controller:

```php
#[IsGranted('POST_EDIT', subject: 'post')]
public function edit(Post $post): Response { ... }
```

- IDOR fix is exactly the voter pattern — check ownership against the authenticated user, not just authentication.
- Without voters, controllers tend to do `if ($post->getAuthor() === $user)` inline. Works, but easy to forget on a new endpoint. The voter centralizes the rule.
- `#[IsGranted]` attribute (PHP 8+) or `$this->denyAccessUnlessGranted()` in older code. Pick one style and apply consistently.

### 3. Doctrine ORM and SQL injection

Doctrine parameterizes by default through DQL placeholders and QueryBuilder parameters. SQLi arises where you step out.

Safe:

```php
$qb->where('u.email = :email')->setParameter('email', $email);
$conn->executeQuery('SELECT * FROM users WHERE email = ?', [$email]);
```

Unsafe:

```php
$qb->where("u.email = '{$email}'");                    // string interpolation
$conn->executeQuery("SELECT * FROM users WHERE email = '$email'");
$qb->orderBy($request->query->get('sort'));            // user-controlled column
```

Specific patterns:

- **`orderBy` / `addOrderBy` with user input**: same risk as Django `.order_by(request.GET.get('sort'))`. Allowlist column names.
- **`expr()->literal($var)`**: uses the platform's quote function, not parameter binding. Better than string concatenation but parameter binding via `setParameter` is preferred.
- **`Connection::executeQuery` / `executeStatement` with raw SQL**: always use `?` or `:name` placeholders + parameter array.
- **Native SQL via `EntityManager::createNativeQuery`**: same parameter discipline.
- **Doctrine annotations/attributes do not protect against query-time injection**; they only define schema. The query itself must be parameterized.

### 4. Twig templates and XSS

Twig auto-escapes for the active context (HTML, JS, CSS, URL). XSS arises where you opt out.

- **`{{ var|raw }}`** — opt-out of escaping. Treat every `|raw` filter on user input as XSS.
- **`{% autoescape false %}` block** — disables escaping for the entire block. Rare, review every use.
- **`{{ var }}` in JS context**: Twig auto-detects `<script>` blocks and applies JS escaping. But `<script>var x = {{ data|json_encode|raw }}</script>` is the safer pattern (JSON serializer escapes correctly, `|raw` here is intentional because `json_encode` already produced safe output).
- **HTML attribute context**: Twig handles `<a href="{{ url }}">` correctly by default for HTML quoting, but `javascript:` URLs in `href` bypass HTML escaping. Validate `url` server-side (allowlist `http:`, `https:`, `mailto:`).
- **Custom Twig functions/filters**: code that returns `new \Twig\Markup($value, 'UTF-8')` marks content as already-safe. If `$value` includes user input, that is XSS. Audit `Twig\Markup` instantiation.
- **Symfony UX components / Twig live components**: user-controlled props that flow into rendered output need the same escape discipline as classic templates.

### 5. PHP-specific RCE and dangerous primitives

This is the phase where Symfony skill diverges most from the Java/Python/Ruby framework skills. PHP has several features that turn user input into code execution if mishandled.

**`unserialize()` on user input** — RCE via gadget chains:

- PHP class instantiation invokes `__wakeup`, `__destruct`, `__toString`, etc. magic methods.
- A POP (Property-Oriented Programming) chain across classes already in the codebase can produce arbitrary effect from controlled `unserialize()` input.
- **Never call `unserialize()` on user input**. If you must deserialize untrusted data, use `json_decode` (returns scalars/arrays only, no class instantiation) or a strictly-validated JSON schema.
- The `allowed_classes` parameter (`unserialize($data, ['allowed_classes' => false])`) blocks class instantiation but is a brittle defense — `json_decode` is cleaner.
- Common attack surface: cookies, request parameters, cached data with controllable inputs, message-queue payloads. Search the codebase for `unserialize(`.

**`include` / `require` with user input** — LFI/RFI:

```php
include $_GET['template'];           // LFI/RFI vector
include $base . $request->get('p');  // path traversal if 'p' contains ../
```

- Validate against an allowlist of known templates. Never resolve user-controlled path fragments into file system paths.
- `allow_url_include` should be `Off` in `php.ini` — historic mitigation against RFI but never the only defense.

**`system`, `exec`, `passthru`, `shell_exec`, backticks** — command injection:

- Use `Process` component (`Symfony\Component\Process\Process`) which escapes arguments correctly:
  ```php
  $process = new Process(['ls', '-la', $userPath]);  // arguments are NOT shell-interpreted
  $process->run();
  ```
- Avoid the string-form constructor (`new Process('ls -la ' . $userPath)`) — that re-introduces shell interpretation.
- `escapeshellarg()` / `escapeshellcmd()` are platform-dependent and have edge cases; prefer the Process component's array form.

**`eval()`** — direct code execution:

- Never on user input.
- In legacy code, sometimes used for simple template engines or expression evaluation. Replace with Symfony's Expression Language component (`ExpressionLanguage`) — sandboxed, no PHP code execution.

**Type juggling and loose comparisons**:

- `==` does type coercion: `'0' == false` is true, `'abc' == 0` is true (in PHP <8), `'1abc' == 1` is true.
- For auth/comparison logic, always use `===` (strict).
- `in_array($needle, $haystack)` defaults to loose comparison — pass `true` as third argument for strict.
- **`hash_equals($known, $user_supplied)`** for timing-safe comparison of hashes/tokens.

### 6. CSRF, session, and password handling

- **CSRF on forms**: Symfony Form Component injects a `_token` field automatically. Validate via `$this->isCsrfTokenValid('intention', $token)` for forms not built with the Form Component (e.g. AJAX endpoints).
- **API stateless endpoints** typically skip CSRF (token-auth or JWT). Make this explicit per firewall — `stateless: true` in the firewall config.
- **Session config** (`config/packages/framework.yaml`):
  - `cookie_secure: auto` or `true` for HTTPS-only
  - `cookie_httponly: true`
  - `cookie_samesite: lax` or `strict`
  - `gc_maxlifetime` reasonable (e.g. 1 hour)
  - `name_strict_mode: true` to prevent session-fixation via attacker-supplied session ID
- **Password hashing**: use `auto` algorithm (Symfony picks bcrypt or argon2id based on what's available). Cost factor configurable; argon2id with memory-cost 65536+ is the current default.
- **Remember-me tokens**: signed via secret; rotate the secret on suspected compromise. Token storage in DB > cookie-only (allows revocation).

### 7. Configuration discipline

- **`.env` / `.env.local` / `.env.local.php`**: `.env` is the public default, `.env.local` is gitignored secrets, `.env.local.php` is the compiled production cache (run `composer dump-env prod`).
- **Symfony Secrets vault** (`bin/console secrets:set`): encrypts secrets per-environment with separate decryption keys. Production decryption key stored outside the repo.
- **`parameters.yaml`** (legacy, pre-Flex): hardcoded secrets in here are an anti-pattern. Migrate to `.env` or secrets vault.
- **Web Profiler in production**: `WebProfilerBundle` exposes `/_profiler` with full request internals (DB queries, log entries, env vars). MUST be disabled in prod (`framework.profiler.enabled: false` and remove from `bundles.php` for prod env).
- **`app_dev.php` legacy** (Symfony 2/3 era): the dev front controller exposing the profiler. Modern Symfony (4+) uses environment-based switching, but legacy apps may still ship `app_dev.php` to production by mistake. Should not be reachable.
- **Debug mode**: `APP_ENV=prod APP_DEBUG=0` in production. Debug mode shows stack traces with secrets and code paths.
- **Trusted proxies and trusted hosts**: `framework.trusted_proxies` and `framework.trusted_hosts` lock down which proxies and hosts the app trusts. Misconfig = host-header injection vector.

### 8. CVE patterns and Symfony-based CMSes

**Symfony CVE feed**: [https://symfony.com/blog/category/security-advisories](https://symfony.com/blog/category/security-advisories) is the canonical source. Always `[verify]` against the current advisory list before citing in a finding — Symfony patches in minor-release windows and the advisory list moves.

Recent CVE classes worth grepping for:

- Cache-poisoning and session-fixation patterns from late 2022 — `[verify against the advisory feed]`.
- HTTP-cache + ESI-related disclosure issues — `[verify]`.
- Environment-mode override via query parameters in development — `[verify]`.

Practical defense: stay within 1 minor release of latest. Track the security-advisories blog category; subscribe to the RSS feed.

**Symfony-based CMSes** (this skill applies, with CMS-specific overlays):

- **Sulu** — REST-API-first CMS, security via security.yaml + Sulu's role/permission system. Permissions are per-content-locale and per-section. Common review targets: webspace configuration, custom controllers extending Sulu's base, REST-API endpoint exposure.
- **Ibexa Platform** (formerly eZ Platform / eZ Publish) — has its own role/policy system on top of Symfony's, plus content-tree permissions. Custom field-types and view-handlers are common attack-surface entry points. Older eZ Publish (pre-Ibexa) had a string of CVEs; Ibexa modernized but legacy patterns persist in long-running deployments.
- **Bolt CMS** — lighter Symfony-based CMS. Smaller attack surface but the same Symfony-component patterns apply.
- **Drupal 9+** — explicitly out of scope here. Uses Symfony components but its security model (hooks, services, render arrays, FormAPI) is its own world. Drupal has a dedicated Security Team and SA advisory feed; treat as a separate skill.
- **Custom Symfony webapps** — the bulk of real-world cases. The discipline here applies directly.

### Verification-loop

Layer 1: scope (security.yaml, all controllers with `#[IsGranted]` or auth checks, all Doctrine repositories with custom queries, all Twig templates using `|raw`, all calls to `unserialize`/`include`/`system`/`eval` walked through?), assumptions (firewall order verified, voter coverage on resource-modifying endpoints?), gaps (Profiler disabled in prod, debug off, secrets in vault?). Layer 2: Symfony CVE-IDs verified against [https://symfony.com/blog/category/security-advisories](https://symfony.com/blog/category/security-advisories) (no fabricated IDs), Doctrine and Twig API names current for the version in use, CMS-specific role-system claims (Sulu, Ibexa) backed by their own docs.

## Output

```
Symfony security review — <app/module>
Symfony: <x.y.z> | PHP: <x.y> | CMS: <Sulu | Ibexa | Bolt | none (custom)>

security.yaml:
  Firewall count:           N
  Firewall order audit:     <clean | finding: pattern X eats Y>
  access_control rules:     N, ordered specific→generic? <yes/no>
  role_hierarchy:           <correct array notation | finding>
  IS_AUTHENTICATED_FULLY on sensitive routes: <yes/no>

Voters and authorization:
  Voter classes:            N
  Coverage on resource endpoints: <% with #[IsGranted] or denyAccessUnlessGranted>
  Inline ownership checks (no voter): <list — refactor candidates>

Doctrine:
  Raw DQL/SQL with string interpolation: <list>
  orderBy with user input:                <list, allowlist applied?>
  expr()->literal usage:                  <count, replacement plan>

Twig:
  |raw on user input:       <list>
  autoescape false blocks:  <list>
  Twig\Markup wrappers:     <audit>

PHP RCE primitives:
  unserialize() calls:      <list, source of input>
  include/require with $var: <list>
  system/exec/passthru:     <list, Process component used?>
  eval():                   <should be 0; if not, FINDING>
  Strict comparison (===):  <audit auth/token comparisons>

CSRF + session:
  CSRF token validation on non-Form endpoints: <yes/no>
  cookie_secure / httponly / samesite:         <yes/no per setting>
  Password algorithm:                          <auto | argon2id | bcrypt | weak>

Configuration:
  Profiler in prod:         <disabled | FINDING if enabled>
  APP_DEBUG in prod:        <0 | FINDING if 1>
  Secrets in .env vs vault: <distribution>
  Trusted proxies/hosts:    <set | not set — header-injection risk>

Version + CVE check:
  Symfony version:          <on latest minor + N | drift>
  Recent advisories:        <0 unresolved | N pending — handoff to cve-triage>

CMS-specific (if applicable):
  Sulu role system:         <reviewed>
  Ibexa policies:           <reviewed>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- **Symfony Security docs** — [https://symfony.com/doc/current/security.html](https://symfony.com/doc/current/security.html). Canonical reference for security.yaml, voters, password hashing.
- **Symfony Security Advisories** — [https://symfony.com/blog/category/security-advisories](https://symfony.com/blog/category/security-advisories). Primary CVE source; verify any specific CVE claim against this feed.
- **Symfony Voters** — [https://symfony.com/doc/current/security/voters.html](https://symfony.com/doc/current/security/voters.html). Method-level authorization patterns.
- **Doctrine ORM Security** — [https://www.doctrine-project.org/projects/doctrine-orm/en/current/](https://www.doctrine-project.org/projects/doctrine-orm/en/current/) and DQL parameter-binding docs.
- **Twig Security** — [https://twig.symfony.com/doc/3.x/api.html#environment-options](https://twig.symfony.com/doc/3.x/api.html#environment-options). Auto-escape behavior.
- **OWASP PHP Security Cheat Sheet** — [https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html).
- **OWASP PHP Object Injection** — [https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection). The unserialize gadget-chain class.
- **PHPGGC** (PHP Generic Gadget Chains) — [https://github.com/ambionics/phpggc](https://github.com/ambionics/phpggc). Catalog of known POP gadget chains across PHP libraries; awareness reference, not for offensive use here.
- **Symfony Process Component** — [https://symfony.com/doc/current/components/process.html](https://symfony.com/doc/current/components/process.html). Safe command execution.
- **Symfony Secrets** — [https://symfony.com/doc/current/configuration/secrets.html](https://symfony.com/doc/current/configuration/secrets.html). Encrypted secrets management.
- **Sulu** — [https://docs.sulu.io/](https://docs.sulu.io/). For CMS-specific role/permission overlay.
- **Ibexa Platform** — [https://doc.ibexa.co/](https://doc.ibexa.co/). For Ibexa-specific security model.
- **Bolt CMS** — [https://docs.boltcms.io/](https://docs.boltcms.io/).

## Categories

- appsec
