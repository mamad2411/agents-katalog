---
name: prestashop_psmcpserver
description: Make any PrestaShop module expose its business logic to AI agents through the official PrestaShop MCP Server (ps_mcp_server). Covers the discovery contract, a Composer-free PSR-4 autoloader, and ready-to-use templates for Tools, Resources, Resource Templates and Prompts.
---

# PrestaShop MCP Server integration (ps_mcp_server)

Use this skill when a module must expose **MCP** elements (Tools / Resources / Prompts) to AI agents (Claude, ChatGPT, Gemini, MCP Inspector) via the official `ps_mcp_server` module. Reference module: `ecom_desestimiento` (its `src/Mcp/` classes follow this skill exactly).

## How ps_mcp_server discovers your module (the contract)

1. Your **main module class** declares compliance:
   ```php
   public function isMcpCompliant() { return true; }
   ```
   On its hooks/discovery, `ps_mcp_server` calls `Module::getInstanceByName(...)` on every installed module, checks `method_exists($m,'isMcpCompliant') && $m->isMcpCompliant()`, and registers compliant module IDs in `ps_mcp_server`'s `mcp_modules_registered` table.
2. For each registered module it scans the directory **`{module}/src`** (recursive, `*.php`, **excludes `index.php`**).
3. For every file it tokenizes the namespace+class, runs **`class_exists($fqcn, true)` (autoload!)**, then `new ReflectionClass(...)` and reads public methods for the attributes:
   `#[PsMcpTool]`, `#[PsMcpResource]`, `#[PsMcpResourceTemplate]`, `#[PsMcpPrompt]`.
4. The **module name is deduced from the file path** `/modules/{name}/...`, not from the namespace. So your namespace can be anything; the files just have to live under `modules/{your_module}/src/`.
5. Technical names are auto-prefixed: `{module}-{toolName}` and must be **≤ 64 chars total** (longer = silently skipped).

Requirements: PrestaShop 8.2+, PHP 8.1+.

## CRITICAL: Composer-free autoloading

The discoverer loads classes by reflection (`class_exists(..., true)`), **not** `require_once`. If your project forbids Composer (manual loading only), register a tiny **SPL autoloader** in the main module constructor. It is active during discovery because `ps_mcp_server` instantiates your module (`getInstanceById`) right before scanning.

```php
public function __construct()
{
    // ... name, version, etc ...
    parent::__construct();
    self::registerMcpAutoload();
    // ... displayName, etc ...
}

public static function registerMcpAutoload()
{
    static $registered = false;
    if ($registered) { return; }
    $registered = true;

    spl_autoload_register(static function ($class) {
        $prefix = 'Vendor\\MyModule\\';                  // your namespace prefix
        $len = strlen($prefix);
        if (strncmp($class, $prefix, $len) !== 0) { return; }
        $relative = substr($class, $len);
        $file = _PS_MODULE_DIR_ . 'my_module/src/' . str_replace('\\', '/', $relative) . '.php';
        if (is_file($file)) { require_once $file; }
    });
}
```

If you DO use Composer, a `composer.json` PSR-4 autoload + committed `vendor/autoload.php` works too — then you can skip the SPL autoloader.

## Attribute reference (exact signatures)

`Ps*` attributes live in `PrestaShop\Module\PsMcpServer\Server\Attributes\` and extend the `mcp/sdk` ones:

- `#[PsMcpTool(?string $name, ?string $title, ?string $description, ?ToolAnnotations $annotations, ?array $icons, ?array $meta, ?array $outputSchema)]`
- `#[PsMcpResource(string $uri, ?string $name, ?string $description, ?string $mimeType, ?int $size, ?Annotations $annotations, ...)]`
- `#[PsMcpResourceTemplate(string $uriTemplate, ?string $name, ?string $description, ?string $mimeType, ...)]`
- `#[PsMcpPrompt(?string $name, ?string $title, ?string $description, ?array $icons, ?array $meta)]`
- `#[PsMcpSchema(?array $properties, ?array $required, ?string $type, ?array $items, ...)]` — describes tool inputs.
- `PsMcpToolAnnotations(?string $title, ?bool $readOnlyHint, ?bool $destructiveHint, ?bool $idempotentHint, ?bool $openWorldHint)`

### GOTCHA: PsMcpToolAnnotations is NOT a standalone attribute
`PsMcpToolAnnotations` extends `ToolAnnotations` (it is **not** marked `#[\Attribute]`). Pass it **inside** the element attribute via the `annotations:` argument, using PHP 8.1 "new in initializers":
```php
#[PsMcpTool(name: 'x', description: '...', annotations: new PsMcpToolAnnotations(readOnlyHint: true, destructiveHint: false))]
```
Do **not** write `#[PsMcpToolAnnotations(...)]` as its own method attribute — it is ignored and risks reflection errors.

## Templates

Put each class in `{module}/src/Mcp/` (or any subfolder of `src/`). Always guard with `_PS_VERSION_` and require your own service classes at the top (loaded when the class is autoloaded inside PrestaShop). The `use PrestaShop\Module\PsMcpServer\...` lines are just aliases — they only resolve when `ps_mcp_server` reflects the class, so the file is safe to autoload even if `ps_mcp_server` is absent (attributes are evaluated only at reflection time).

### Tool (read-only example)
```php
namespace Vendor\MyModule\Mcp;

use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpSchema;
use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpTool;
use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpToolAnnotations;
use PrestaShop\Module\PsMcpServer\Server\Exceptions\PsMcpToolCallException;

if (!defined('_PS_VERSION_')) { exit; }
require_once _PS_MODULE_DIR_ . 'my_module/classes/MyService.php';

class MyTools
{
    #[PsMcpTool(
        name: 'do_something',                       // becomes my_module-do_something
        description: 'Clear, explicit description for the AI. Say what it returns and when to use it.',
        annotations: new PsMcpToolAnnotations(readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false)
    )]
    #[PsMcpSchema(
        properties: [
            'orderId' => ['type' => 'integer', 'description' => 'Numeric order ID.'],
        ],
        required: ['orderId']
    )]
    public function doSomething(int $orderId = 0): array
    {
        if ($orderId <= 0) {
            throw new PsMcpToolCallException('orderId must be a positive integer.', 1);
        }
        $order = new \Order($orderId);
        if (!\Validate::isLoadedObject($order)) {
            throw new PsMcpToolCallException('Order not found.', 1);
        }
        return ['id' => (int) $order->id, 'reference' => (string) $order->reference];
    }
}
```
Rules: method params must match schema property names. Use core classes fully-qualified (`\Order`, `\Configuration`, `\Validate`, `\Db`). Validate inputs; keep results bounded; mark read-only tools `readOnlyHint: true`.

### Resource (markdown or JSON)
```php
use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpResource;
use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpToolAnnotations;
use PrestaShop\Module\PsMcpServer\Server\Exceptions\PsMcpResourceReadException;

class MyResources
{
    #[PsMcpResource(
        uri: 'mymodule://policy',
        name: 'My module policy',
        description: 'Stable knowledge the AI can read.',
        mimeType: 'application/json',
        annotations: new PsMcpToolAnnotations(readOnlyHint: true, destructiveHint: false)
    )]
    public function getPolicy(): array
    {
        try {
            return ['days' => (int) \Configuration::get('MYMODULE_DAYS')];
        } catch (\Throwable $e) {
            throw new PsMcpResourceReadException('Failed: ' . $e->getMessage(), 1);
        }
    }
}
```
Return a `string` for text/markdown resources, an `array` for `application/json`.

### Resource Template (dynamic URI, RFC 6570)
```php
#[PsMcpResourceTemplate(
    uriTemplate: 'mymodule://order/{id}',
    name: 'Order by ID',
    description: 'Returns an order by its numeric ID.',
    mimeType: 'application/json',
    annotations: new PsMcpToolAnnotations(readOnlyHint: true, destructiveHint: false)
)]
public function getOrder(int $id): array { /* ... */ }
```

### Prompt
```php
use PrestaShop\Module\PsMcpServer\Server\Attributes\PsMcpPrompt;
use PrestaShop\Module\PsMcpServer\Server\Exceptions\PsMcpPromptGetException;

class MyPrompts
{
    #[PsMcpPrompt(name: 'assistant', description: 'Prime the AI to use this module tools.')]
    public function assistant(): string
    {
        return "You are an assistant for ... Use the tools 'my_module-do_something' and the resource 'mymodule://policy'.";
    }
}
```
Prompt method parameters become prompt arguments (use the docblock `@param` for their descriptions; required if no default value).

## Error handling

Wrap failures so the AI receives a clean message:
| Element | Exception |
|---|---|
| Tool | `PsMcpToolCallException($message, $exitCode)` |
| Resource / Template | `PsMcpResourceReadException(...)` |
| Prompt | `PsMcpPromptGetException(...)` |

## Activation / testing

1. Install + enable `ps_mcp_server` and your module.
2. Force discovery: open `ps_mcp_server` config, or delete its `.mcp/cache` directory.
3. Verify with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) or a connected AI client (token / OAuth).
4. Tools/resources/prompts appear named `{module}-{name}`.

## Checklist (copy for each module)

- [ ] `isMcpCompliant(): true` in the main module class.
- [ ] SPL autoloader registered in `__construct` (or Composer PSR-4) for your `src/` namespace.
- [ ] MCP classes under `{module}/src/...` with `if (!defined('_PS_VERSION_')) exit;` and `index.php` in every folder (it is excluded from scanning).
- [ ] `#[PsMcpTool]` + `#[PsMcpSchema]` on each tool method; `annotations:` passed INSIDE `#[PsMcpTool(...)]`.
- [ ] Names ≤ 64 chars with the `{module}-` prefix; descriptions explicit and consistent.
- [ ] Inputs validated; outputs bounded; read-only tools flagged.
- [ ] Errors wrapped in the `PsMcp*Exception` classes.
- [ ] Degrades silently when `ps_mcp_server` is absent (nothing loads your `src/Mcp` classes).

## Notes / gotchas learned

- The discoverer reflects classes; if your class can't be autoloaded it is skipped silently — the SPL autoloader is the usual culprit when nothing appears.
- `index.php` files in `src/` are skipped by the scanner (`notName('index.php')`), so they don't break discovery.
- Keep tool logic in your existing service classes and call them from the MCP class — do not duplicate business rules.
