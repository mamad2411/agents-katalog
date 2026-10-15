---
name: nsutil-mcp
description: >-
  (NS) Build and extend MCP servers with NsUtil (`NsUtil\MCP` on `NsUtil\Api`):
  Tool, Prompt, Server classes, attributes, HTTP endpoint wiring, JSON-RPC methods,
  Docker PHPUnit tests. Use whenever the user creates or extends MCP servers, tools,
  prompts, MCP endpoints, JSON-RPC dispatch, or MCP tests in apps that depend on
  nextstage-brasil/ns-util — even if they do not name this skill. Do NOT invent
  fluent addTool APIs or run PHPUnit on the host.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.1"
depends:
  - ns-harness
---

# NsUtil MCP Server

Build MCP servers via `NsUtil\MCP` on `NsUtil\Api`.

## Context (read first)

See `../ns-harness/references/harness-discovery.md`.

1. `{harness_root}/rules/nsutil-architecture-rules.md` when present — read **MCP Server** section. Also `{harness_root}/rules/architecture-rules.md` when present.
2. **Legacy only** if `{harness_root}/` absent: `.cursor/rules/nsutil-architecture-rules.mdc` (prefer `harness init` then `npx @nextstage-brasil/harness sync` — absorbs orphans).
3. Package docs when available: `vendor/nextstage-brasil/ns-util/src/MCP/README.md`.

## Workflow

```
- [ ] 1. Tool class(es) — suffix `Tool`, `#[Description]`, `handle()`
- [ ] 2. Prompt class(es) — optional; suffix `Prompt`, `#[Description]`
- [ ] 3. Server class — `#[Name]`, `#[Version]`, register `$tools` / `$prompts`
- [ ] 4. HTTP endpoint — `new MyServer($api); $server->run();`
- [ ] 5. Tests in Docker — `tests/Units/MCP/` pattern
```

## Tool

```php
use NsUtil\MCP\Attributes\Description;
use NsUtil\MCP\Tool;

#[Description('What this tool does')]
class GetCurrentWeatherTool extends Tool
{
    public function handle(array $params): array
    {
        return ['temperature' => 25, 'location' => $params['location'] ?? ''];
    }

    public function schema(): ?array
    {
        return ['location' => ['type' => 'string', 'description' => 'City name']];
    }
}
```

| Field | Rule |
| --- | --- |
| **name** | Inferred: class minus `Tool` → snake_case (`GetCurrentWeatherTool` → `get_current_weather`). `#[Name]` only to override. |
| **description** | **Required** `#[Description('...')]` on class. |
| **schema** | Optional; becomes `inputSchema` in `tools/list`. |

## Prompt

```php
use NsUtil\MCP\Attributes\Description;
use NsUtil\MCP\Prompt;

#[Description('Summarize weather for a city')]
class SummarizeWeatherPrompt extends Prompt
{
    public function handle(array $params): array
    {
        return [
            'description' => 'Weather summary prompt',
            'messages' => [
                ['role' => 'user', 'content' => ['type' => 'text', 'text' => $params['location'] ?? '']],
            ],
        ];
    }

    public function arguments(): ?array
    {
        return ['location' => ['type' => 'string', 'description' => 'City name']];
    }
}
```

| Field | Rule |
| --- | --- |
| **name** | Inferred: class minus `Prompt` → snake_case (`SummarizeWeatherPrompt` → `summarize_weather`). `#[Name]` only to override. |
| **description** | **Required** `#[Description('...')]` on class. |
| **arguments** | Optional; prompt argument schema for `prompts/list` / `prompts/get`. |

Register class strings on Server `$prompts` (same pattern as `$tools`).

## Server

```php
use NsUtil\MCP\Attributes\Instructions;
use NsUtil\MCP\Attributes\Name;
use NsUtil\MCP\Attributes\Version;
use NsUtil\MCP\Server;

#[Name('Weather Server')]
#[Version('1.0.0')]
#[Instructions('Weather lookup tools')]
class WeatherServer extends Server
{
    protected array $tools = [
        GetCurrentWeatherTool::class,
    ];

    protected array $prompts = [
        SummarizeWeatherPrompt::class,
    ];
}
```

Wire: `$server = new WeatherServer($api); $server->run();` — or `new WeatherServer()` (uses `Request::getInstance()`).

## JSON-RPC methods

`initialize`, `ping`, `tools/list`, `tools/call`, `prompts/list`, `prompts/get`.

Body via `$api->getBody()` only. Response via `PrepareOutputRFC` — no hand-rolled JSON-RPC envelope.

## Do not

- Do not alter NsUtil package classes for MCP behavior — extend via Server/Tool/Prompt in consuming app.
- Use fluent `addTool()` — register class strings in `$tools` / `$prompts`.
- Use HTTP 404 for unknown tool/method in Server (use 400; Api strips metadata when `responseCode > 401`).
- Run PHPUnit on host — Docker only (`NS_UTIL_TEST_MODE=1` in `phpunit.xml`).

## Tests

Run inside Docker. Prefer runner from `{harness_root}/rules/nsutil-architecture-rules.md` when present. Common pattern:

```bash
bash docker/scripts/phpunit-runner.sh tests/Units/MCP/
```

Path layout: `tests/Units/MCP/` (fixtures: `tests/Units/MCP/Fixtures/` in ns-util).
