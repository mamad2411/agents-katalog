---
name: zephyrus
description: Use when working in a Zephyrus PHP framework project (`zephyrus-framework/core`). Triggers on attribute routing (`#[Get]`, `#[Post]`, `#[Put]`, `#[Patch]`, `#[Delete]`, `#[Root]`, `#[Middleware]`, `#[RequiresEnv]`), `ApplicationBuilder`, `Controller`, `RenderResponses` trait, `Request`/`Response` value objects, `Configuration::fromYamlFile`, `ConfigSection` subclasses, Latte templates in `app/Views/`, Broker/Service/Entity layering, `Zephyrus\Data\Broker` or `Zephyrus\Data\Entity` extensions, controller auto-discovery, and the `config.yml` shape with `application:`/`render:`/`localization:`/`security:`/`database:` sections. Covers attribute routing with MODE-based controller scoping (one codebase, multiple entry points), named middleware registration vs attribute application, raw-SQL Broker pattern with Service/Entity layering, PostgreSQL bytea sanitization, custom controller factory for render-engine injection, `DATABASE_URL` parsing for cloud deploys, DECIMAL-as-string for money precision, fresh-DB-per-test bootstrap with transaction-isolated integration tests, keyset (cursor) pagination, and the no-ORM/no-migration philosophy. Empirical patterns drawn from the production `immunity-app`.
---

# Zephyrus Framework

A PHP 8.4+ framework with attribute routing, immutable HTTP objects,
typed configuration, and security middleware. Test coverage in the core
runs ~98%; the framework intentionally ships a **small surface area**
and pushes the rest to convention.

**Heads-up:** Zephyrus has **no official documentation site yet**
("coming soon"). The framework's GitHub README is light. This skill is
the canonical reference for the empirical patterns, drawn from the
production `immunity-app` (private to ophelios-studio; ask for access).
The framework repos are:

- Core: https://github.com/zephyrus-framework/core
- Application template: https://github.com/zephyrus-framework/framework

## Bootstrap

Applications are built with `ApplicationBuilder`:

```php
$app = ApplicationBuilder::create()
    ->withConfiguration($config, basePath: ROOT_DIR)
    ->withRouter($router)
    ->withControllerFactory(fn(string $class) => /* DI */)
    ->withExceptionHandler(RouteNotFoundException::class, fn($e, $r) => Response::html('404', 404))
    ->build();
```

Configuration is loaded from YAML with typed sections:

```php
$config = Configuration::fromYamlFile(ROOT_DIR . '/config.yml', [
    'render' => RenderConfig::class,
    'leaf'   => LeafConfig::class,   // custom sections register here
]);
```

YAML supports `!env` tags for environment variables with fallback:
`database_host: !env DB_HOST, localhost`.

Production projects extend `Kernel` (or build a custom Application
class), declare their own controller factory, register middlewares,
and run `(new Application())->run();` from `public/index.php`.

## Routing

Routes are declared as PHP 8 attributes on controller methods:

```php
#[Get('/users')]
public function index(): Response { }

#[Get('/users/{id}', constraints: ['id' => '\d+'])]
public function show(int $id): Response { }

#[Post('/users', middlewares: ['auth'])]
public function store(Request $request): Response { }
```

Available verbs: `#[Get]`, `#[Post]`, `#[Put]`, `#[Patch]`, `#[Delete]`,
`#[Head]`, `#[Options]`.

Class-level attributes: `#[Root('/prefix')]`, `#[Middleware('name')]`,
`#[RequiresEnv('VAR', 'value')]`.

Controller discovery (auto-scans the namespace):

```php
$router = (new Router())->discoverControllers(
    namespace: 'App\\Controllers',
    directory: ROOT_DIR . '/app/Controllers',
);
```

Path parameters are auto-injected by name and type-coerced. Type
mismatch returns 404.

### Empirical: MODE-based controller scoping (one codebase, many entry points)

`#[RequiresEnv('MODE', 'WEB')]` on a controller class makes it register
**only when that env var matches**. This is how `immunity-app` ships
one codebase that boots into three different entry points:

```php
namespace App\Controllers\Web;

#[RequiresEnv('MODE', 'WEB')]
abstract class Controller extends BaseController { use RenderResponses; }
```

```php
namespace App\Controllers\Api\Public;

#[Root('/v1')]
#[RequiresEnv('MODE', 'API')]
abstract class Controller extends BaseController {}
```

```php
namespace App\Controllers\Api\Internal;

#[Root('/api/v1')]
#[RequiresEnv('MODE', 'WEB')]   // internal API ships in the WEB process
abstract class Controller extends BaseController {}
```

```php
namespace App\Controllers\Shared;

class HealthController            // No #[RequiresEnv] — registers in EVERY mode
{
    #[Get('/health')]
    public function ping(): Response { return Response::text('ok'); }
}
```

Containerized services set `MODE=API`, `MODE=WEB`, `MODE=INDEXER`
explicitly. **Default to `'WEB'` if unset** (Application bootstrap):

```php
if (!isset($_ENV['MODE']) && getenv('MODE') === false) {
    $_ENV['MODE'] = 'WEB';
    putenv('MODE=WEB');
}
```

**Gotcha:** if you forget to set `MODE` in your container, the WEB
tier's routes register instead of API routes — `/v1/...` returns 404.
Add a `Shared\HealthController` with `#[Get('/health')]` to verify
mode-aware deploys with a probe that works in every tier.

## Controllers

Extend `Controller` for JSON APIs or use the `RenderResponses` trait
for HTML:

```php
final class PageController extends Controller
{
    use RenderResponses;

    #[Get('/')]
    public function index(): Response
    {
        return $this->render('home', ['title' => 'Home']);
    }
}
```

Convenience methods on `Controller`: `json()`, `created()`, `text()`,
`noContent()`, `redirect()`, `abort()`, `validate()`.

Lifecycle hooks: override `before(Request): ?Response` (guard /
short-circuit) and `after(Request, Response): Response` (decorate).

### Empirical: lazy service initialization

`immunity-app` defers expensive service construction until first use
within a request:

```php
final class DashboardController extends Controller
{
    private ?HeartbeatBroker $heartbeats = null;

    #[Get('/dashboard/activity')]
    public function index(Request $request): Response
    {
        $this->heartbeats ??= new HeartbeatBroker();
        $rows = $this->heartbeats->listAllWithStats(60);
        return Response::json($rows);
    }
}
```

The broker constructor opens a DB connection — null-coalescing assignment
defers the connect until a route that needs it actually runs. In tests,
inject a test double via the constructor instead.

### Empirical: custom controller factory for render-engine injection

Plain `new $class()` instantiation does not give controllers the
template engine. Use `withControllerFactory`:

```php
$builder = $builder->withControllerFactory(function (string $class) use ($renderEngine): object {
    $controller = new $class();
    if (method_exists($controller, 'setRenderEngine')) {
        $controller->setRenderEngine($renderEngine);
    }
    return $controller;
});
```

If you add a controller that needs another dependency (a logger, an
event bus), extend this factory. Pure `new()` won't inject it.

## Request & Response

Both are immutable value objects:

```php
// Request
$request->method()                 // GET, POST, ...
$request->uri()->path()            // /users/42
$request->body()->get('name')      // form/JSON body
$request->query()->get('page')     // query string
$request->headers()->bearerToken() // Authorization header
$request->cookies()->get('session')
Request::fromGlobals()             // create from PHP globals

// Response
Response::json(['data' => $items], 200)
Response::html($html, 200)
Response::redirect('/login', 302)
$response->withHeader('X-Custom', 'value')
$response->withStatus(201)
```

### Empirical: cache headers per endpoint

Public, frequently-fetched endpoints layer in revalidation:

```php
return Response::json(['items' => $items])
    ->withHeader('Cache-Control', 'public, max-age=10, stale-while-revalidate=20');
```

Private/user-specific endpoints either skip the header or set
`Cache-Control: no-store`. Don't reach for `no-store` reflexively;
`max-age=0, must-revalidate` lets browsers reuse the response while
revalidating it, which is usually what you want.

## Middleware

Implement `MiddlewareInterface`:

```php
class AuthMiddleware implements MiddlewareInterface
{
    public function process(Request $request, callable $next): Response
    {
        if (!$this->isAuthenticated($request)) {
            return Response::json(['error' => 'Unauthorized'], 401);
        }
        return $next($request);
    }
}
```

### Empirical: named registration vs attribute application (the gotcha)

The `#[Middleware('name')]` attribute *applies* a middleware that was
**registered earlier under that name** in your Kernel/Application
override. Adding the attribute without registering the name fails
silently or crashes at routing time.

```php
// app/Models/Core/Application.php — registration
final class Application extends Kernel
{
    protected function registerMiddleware(ApplicationBuilder $builder): void
    {
        $builder->withMiddleware(new SessionMiddleware(SessionConfig::fromArray([
            'name'     => 'APP_SESSION',
            'lifetime' => 0,
            'sameSite' => 'Lax',
            'secure'   => false,
        ])));

        // Named middlewares are referenced by attribute on controllers
        $builder->registerMiddleware(
            'admin',
            new AuthGuardMiddleware(
                new PredicateAuthGuard(static fn () => Session::hasAdmin()),
            ),
        );
    }
}
```

```php
// app/Controllers/Api/Internal/AdminController.php — application
#[Root('/api/v1')]
#[Middleware('admin')]
final class AdminController extends BaseController
{
    #[Post('/admin/scenario/{name}')]
    public function scenario(string $name): Response { /* ... */ }
}
```

Pattern: register globals via `withMiddleware()` (always run); register
named via `registerMiddleware('name', ...)` (only run when an
attribute references the name).

## Configuration

`config.yml` at project root, loaded via `Configuration::fromYamlFile`:

```yaml
application:
  environment: !env APP_ENV, dev
  debug: !env APP_DEBUG, true

session:
  name: "APP_SESSION"
  lifetime: 0
  http_only: true
  secure: false
  same_site: "Lax"
  cookie_path: "/"

security:
  force_https: false
  allowed_hosts: []
  max_body_size: 10485760
  csrf:
    enabled: true
    auto_html: false
  encryption:
    key: !env ENCRYPTION_KEY

localization:
  locale: "en"
  supported_locales: ["en"]
  locale_path: "locale"
  timezone: !env APP_TIMEZONE, UTC

database:
  host: !env DB_HOST, localhost
  port: !env DB_PORT, 5432
  database: !env DB_NAME, app
  username: !env DB_USERNAME, dev
  password: !env DB_PASSWORD, dev
  charset: "utf8"

render:
  engine: latte
  directory: app/Views
  cache: cache/latte
  mode: always
```

### Custom typed config sections

Subclass `ConfigSection` to add typed sections:

```php
final class MyConfig extends ConfigSection
{
    public readonly string $apiKey;
    public readonly bool   $debugMode;

    public static function fromArray(array $values): static
    {
        $instance = new static($values);
        $instance->apiKey    = $instance->getString('apiKey', '');
        $instance->debugMode = $instance->getBool('debugMode', false);
        return $instance;
    }
}
```

Register when loading:
`Configuration::fromYamlFile($path, ['my_section' => MyConfig::class])`.

YAML keys are normalized: `snake_case` becomes `camelCase` in
`getString()` etc.

### Empirical: `DATABASE_URL` parsing for cloud deploys

`immunity-app` parses Fly/Heroku-style `DATABASE_URL` once at boot and
sets `$_ENV` vars so `config.yml` `!env` directives pick them up:

```php
public static function applyDatabaseUrl(): void
{
    $url = $_ENV['DATABASE_URL'] ?? getenv('DATABASE_URL') ?: null;
    if (!is_string($url) || $url === '') return;

    $parts = parse_url($url);
    $set = static function (string $key, ?string $value): void {
        if ($value !== null && $value !== '' &&
            !isset($_ENV[$key]) && getenv($key) === false) {
            $_ENV[$key] = $value;
            putenv("$key=$value");
        }
    };
    $set('DB_HOST',     $parts['host']    ?? null);
    $set('DB_PORT',     isset($parts['port']) ? (string) $parts['port'] : null);
    $set('DB_USERNAME', $parts['user']    ?? null);
    $set('DB_PASSWORD', $parts['pass']    ?? null);
    $set('DB_NAME',     ltrim($parts['path'] ?? '', '/'));
}
```

Existing `DB_*` vars take precedence — useful for local overrides.

## Database (no ORM, no migrations)

Zephyrus does **raw SQL with parameter binding**. `immunity-app`'s
pattern is **Broker / Service / Entity**.

### Db singleton + connection

```php
final class Db
{
    private static ?Database $current = null;

    public static function current(): Database
    {
        if (self::$current === null) {
            $config = App::getConfiguration()->section('database');
            self::$current = self::fromConfig($config);
            self::registerTypes(self::$current);
        }
        return self::$current;
    }

    private static function registerTypes(Database $db): void
    {
        // DECIMAL columns stay strings — preserves money precision
        $stringPassthrough = static fn (string $v): string => $v;
        $db->registerTypeConversion('NUMERIC',    $stringPassthrough);
        $db->registerTypeConversion('DECIMAL',    $stringPassthrough);
        $db->registerTypeConversion('NEWDECIMAL', $stringPassthrough);
    }
}
```

**`(float)` on a money string loses precision.** Keep DECIMAL as string;
convert only for display via a Formatter helper.

### Broker base class with bytea sanitization

PDO_PGSQL returns `bytea` columns as PHP **stream resources**, not
strings. The framework's type converter doesn't handle resources. Wrap
selects:

```php
abstract class Broker extends ZephyrusBroker
{
    public function __construct(?Database $db = null)
    {
        parent::__construct($db ?? Db::current());
    }

    protected function select(string $sql, array $params = []): array
    {
        $rows = parent::select($sql, $params);
        foreach ($rows as $row) self::sanitize($row);
        return $rows;
    }

    protected function selectOne(string $sql, array $params = []): ?stdClass
    {
        $row = parent::selectOne($sql, $params);
        if ($row !== null) self::sanitize($row);
        return $row;
    }

    private static function sanitize(stdClass $row): void
    {
        foreach ($row as $key => $value) {
            if (is_resource($value)) {
                $contents = stream_get_contents($value);
                $row->$key = $contents === false ? '' : $contents;
            }
        }
    }
}
```

### Broker / Service / Entity layering

```php
// Broker — raw SQL only, returns stdClass
final class EntryBroker extends Broker
{
    public function findByImmId(string $immId): ?stdClass
    {
        return $this->selectOne(
            'SELECT * FROM antibody.entry WHERE imm_id = ?',
            [$immId],
        );
    }
}

// Entity — typed value object, knows its bytea columns
final class Entry extends Entity
{
    public int    $id;
    public string $imm_id;
    public string $keccak_id;     // bytea
    public ?string $flavor = null;

    public static function byteaProperties(): array
    {
        return ['keccak_id', 'context_hash', 'evidence_cid'];
    }
}

// Service — owns a Broker, hydrates to Entity
final readonly class EntryService
{
    public function __construct(
        private EntryBroker $broker = new EntryBroker(),
    ) {}

    public function findByImmId(string $immId): ?Entry
    {
        $row = $this->broker->findByImmId($immId);
        return $row === null ? null : Entry::build($row);
    }
}
```

**Gotcha:** if you add a bytea column to the DB but forget to add it to
`byteaProperties()`, `Entity::build()` may set a PHP resource directly
on a typed property and downstream code breaks.

### Schema as single source of truth

`sql/0-init-database.sql` is the schema. Test bootstrap drops the test
DB and rebuilds from this file fresh per session. **No migrations.**
Add a table → update the SQL → re-run tests. The DDL is the spec.

### Keyset (cursor) pagination

```php
#[Get('/antibodies')]
public function index(Request $request): Response
{
    $beforeId = $request->query('before_id');
    $beforeId = $beforeId === null ? null : (int) $beforeId;

    $items = $this->entries->findFiltered(/* ... */, $limit, $beforeId);

    return Response::json([
        'next_cursor' => $items === [] ? null : end($items)->id,
        'items'       => $items,
    ]);
}
```

```sql
SELECT * FROM entry
WHERE (? IS NULL OR id < ?)
ORDER BY id DESC
LIMIT ?
```

Offset pagination is O(N) on the database. Keyset is O(log N). For any
table that grows beyond a few thousand rows, use keyset.

## Localization

```php
$loader     = new JsonLocaleLoader(ROOT_DIR . '/locale');
$translator = new Translator($loader, 'en');

$translator->trans('welcome', ['name' => 'World'], 'fr');

// Global function (after App::setTranslator)
localize('welcome', ['name' => 'World']);
```

JSON files at `locale/{lang}/strings.json` with nested keys via dots:
`localize('nav.home')`. Missing keys fall back to the key itself.

## Rendering (Latte)

Templates use [Latte](https://latte.nette.org/) (`.latte` files):

```latte
{layout 'layouts/main.latte'}
{block content}
<h1>{$title}</h1>
{/block}
```

Config:

```yaml
render:
  engine: latte
  directory: app/Views
  cache: cache/latte
  mode: always
```

Extensions inject global template variables via `beforeRender()`. Add
custom Latte functions in `Application::__construct()` after the
engine is built (`$engine->addFunction('format', ...)`).

### Empirical: Asset() helper for cache-busting

```php
App::setAsset(new Asset(ROOT_DIR . '/public'));
```

```latte
<link rel="stylesheet" href="{asset('/stylesheets/app.css')}">
{* → /stylesheets/app.css?v=<sha1-of-file-contents> *}
```

Compute SHA-1 of file contents, append as `?v=<hash>` query param.
Browser caches forever; file change auto-invalidates. Pair with
long-lived `Cache-Control` in `.htaccess`/server config.

## Validation

```php
$form = FormValidator::create()
    ->field('email', Rules::required(), Rules::email())
    ->field('age',   Rules::required(), Rules::integer(), Rules::min(18));

$errors = $form->validate($request->body()->all());
if (!$errors->isEmpty()) {
    return $this->json(['errors' => $errors->toArray()], 422);
}
```

## Testing

PHPUnit 11 (`vendor/bin/phpunit`). Two test suites typical:

```xml
<testsuites>
  <testsuite name="unit">
    <directory>tests/Unit</directory>
  </testsuite>
  <testsuite name="integration">
    <directory>tests/Integration</directory>
  </testsuite>
</testsuites>

<php>
  <env name="APP_ENV" value="testing" force="true"/>
  <env name="DB_NAME" value="app_test" force="true"/>
</php>
```

### Empirical: bootstrap rebuilds the DB

```php
// tests/bootstrap.php
$adminPdo = new PDO("pgsql:host=$host;port=$port;dbname=postgres", $user, $pass);
$adminPdo->exec("DROP DATABASE IF EXISTS $testDbName WITH (FORCE)");
$adminPdo->exec("CREATE DATABASE $testDbName");

$testPdo = new PDO("pgsql:host=$host;port=$port;dbname=$testDbName", $user, $pass);
$testPdo->exec(SqlLoader::load(ROOT_DIR . '/sql/0-init-database.sql'));

$GLOBALS['TEST_DATABASE_CONFIG'] = $testConfig;
```

### Empirical: integration tests wrap each test in a transaction

```php
abstract class IntegrationTestCase extends TestCase
{
    protected Database $db;

    protected function setUp(): void
    {
        $config = $GLOBALS['TEST_DATABASE_CONFIG'];
        $this->db = Db::fromConfig($config);
        $this->db->pdo()->beginTransaction();
    }

    protected function tearDown(): void
    {
        if ($this->db->pdo()->inTransaction()) {
            $this->db->pdo()->rollBack();
        }
    }
}
```

Each test is atomic; DB state resets between tests without rebuilding
the schema. Tests run fast, isolated, and order-independent.

## Production patterns from `immunity-app` (cheat sheet)

The decentralized threat-intel SDK at `www/immunity-app` is the
canonical Zephyrus reference. Patterns it codifies:

1. **Three-mode codebase, single Application.** WEB / API / INDEXER all
   share `app/`. `#[RequiresEnv('MODE', 'X')]` on controller classes
   gates which routes register per process.
2. **Default `MODE=WEB`** in single-process local dev. Containers set
   it explicitly.
3. **Named middleware registration** in `Application::registerMiddleware`,
   applied via `#[Middleware('name')]` on controllers.
4. **`Db::current()` singleton** with type conversions for
   NUMERIC/DECIMAL → string (money precision).
5. **`DATABASE_URL` parser** in `Db::applyDatabaseUrl()` for Fly/Heroku
   deploys.
6. **PostgreSQL bytea sanitization** in a custom `Broker` base class.
7. **Broker / Service / Entity layering** with `Entity::byteaProperties()`
   to declare which columns are bytea.
8. **Lazy service init** in controllers via null-coalescing assignment.
9. **Custom controller factory** for render-engine injection (and any
   future cross-cutting deps).
10. **Keyset pagination** with `before_id` cursor in query string and
    `next_cursor` in response.
11. **Cache headers per endpoint** — public/short-TTL on list endpoints,
    `no-store` on private data, none by default.
12. **Tier-aware sessions** (e.g. `Session::hasAdmin()` implies
    `hasJudge()`) with custom helper, gated by middleware OR in-handler
    check when middleware-only granularity isn't enough.
13. **Schema in `sql/0-init-database.sql`** as single source of truth;
    no migrations.
14. **Test bootstrap drops + rebuilds the test DB** fresh per session,
    integration tests wrap in transactions.
15. **`SqlLoader::load(path)`** to ingest large SQL files at boot.

## Conventions

- Controllers in `app/Controllers/` with `App\Controllers` namespace
- Views in `app/Views/` as `.latte` files
- Models / domain logic in `app/Models/{Domain}/{Brokers,Services,Entities}/`
- Config in `config.yml` at project root
- Locale files in `locale/{lang}/*.json`
- SQL schema in `sql/0-init-database.sql`
- Use `ROOT_DIR` constant for absolute paths
- All HTTP objects are immutable; use `with*()` to create modified copies
- Route parameters are type-coerced automatically; mismatch returns 404
- **No ORM, no migrations** — raw SQL + Broker, schema as DDL file
- **Default to PostgreSQL** — bytea sanitization, NUMERIC type
  conversion, and the `DATABASE_URL` parser are PG-specific patterns

## References

- Core repo: https://github.com/zephyrus-framework/core
- Application template: https://github.com/zephyrus-framework/framework
- Latte engine docs: https://latte.nette.org/
- Production reference (and source for empirical patterns):
  `immunity-app` (private; ask Ophelios for access)
- In-repo: `examples/zephyrus/` — minimal Hello-World scaffold
