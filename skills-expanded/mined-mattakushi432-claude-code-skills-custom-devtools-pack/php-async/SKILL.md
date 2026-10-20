---
name: php-async
description: "When to activate: PHP concurrency, ReactPHP, Swoole coroutines, PHP Fibers, async PHP, queued jobs, Laravel queues, Symfony Messenger, non-blocking I/O, event loop"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: php
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# PHP Async & Concurrency Patterns

## When to Use

Deciding how to handle concurrent or long-running work in PHP: background jobs, high-throughput I/O-bound services, or evaluating whether async PHP is even the right tool for the problem.

## Core Patterns

### Default to Queued Jobs, Not Async I/O

For the vast majority of PHP apps (Laravel, Symfony), the pragmatic concurrency model is: handle the HTTP request synchronously and push slow work onto a queue.

```php
// Laravel
final class SendInvoiceEmail implements ShouldQueue
{
    public function __construct(private readonly int $invoiceId)
    {
    }

    public function handle(InvoiceMailer $mailer): void
    {
        $mailer->send(Invoice::findOrFail($this->invoiceId));
    }
}

SendInvoiceEmail::dispatch($invoice->id);
```

```php
// Symfony Messenger
final class SendInvoiceEmailHandler
{
    public function __invoke(SendInvoiceEmail $message): void
    {
        $this->mailer->send($message->invoiceId);
    }
}
```

This scales horizontally (more workers), survives process crashes (the job stays in the queue), and needs no exotic runtime.

### Fibers (PHP 8.1+)

Fibers give you cooperative, pausable execution without an external extension — the primitive that libraries like ReactPHP/Amp build on.

```php
$fiber = new Fiber(function (): void {
    $value = Fiber::suspend('paused');
    echo "Resumed with: {$value}\n";
});

$paused = $fiber->start();   // runs until suspend(), returns 'paused'
$fiber->resume('hello');     // resumes, prints "Resumed with: hello"
```

Most application code should not touch Fibers directly — they're the foundation async libraries use internally.

### ReactPHP: Event-Loop Based Async I/O

```php
$loop = React\EventLoop\Loop::get();

$client = new React\Http\Browser($loop);
$client->get('https://api.example.com/status')
    ->then(function (Psr\Http\Message\ResponseInterface $response) {
        echo $response->getBody();
    });

$loop->run();
```

Useful for long-running daemons (webhooks relay, WebSocket server) that need many concurrent non-blocking connections without spawning a process per connection.

### Swoole Coroutines

```php
Swoole\Coroutine\run(function () {
    [$a, $b] = Swoole\Coroutine\Barrier::wait(
        Swoole\Coroutine::create(fn () => Http\get('https://api.a.com')),
        Swoole\Coroutine::create(fn () => Http\get('https://api.b.com')),
    );
});
```

Swoole rewrites the runtime (its own coroutine-aware sockets, `Co\run`), replacing PHP-FPM entirely. This buys much higher throughput for I/O-bound workloads but is a bigger operational commitment — a different deployment model, different debugging tools, and libraries must be coroutine-safe.

## When NOT to Reach for Async PHP

- A typical CRUD web app with normal request volume — PHP-FPM's process-per-request model is simpler to reason about and debug
- CPU-bound work (image processing, PDF generation) — async doesn't help; use queued workers or a separate service
- When the team has no operational experience running Swoole/RoadRunner in production — the debugging story is meaningfully different from stock PHP-FPM
- Anything achievable by "dispatch to a queue and return 202" — simpler, more resilient, and easier to scale than in-process concurrency

## Checklist

- [ ] Slow/external work (email, PDF generation, third-party API calls) is queued, not done inline in the request
- [ ] Jobs are idempotent — safe to retry after a crash mid-execution
- [ ] If using Fibers/ReactPHP/Swoole directly, the team has a debugging and monitoring story for it
- [ ] Swoole/RoadRunner code avoids storing per-request state in static properties (leaks across requests in a long-running worker)

## Quick Reference

| Need | Tool |
|---|---|
| Offload slow work from the request cycle | Laravel Queues / Symfony Messenger |
| Low-level pausable execution primitive | Fibers (PHP 8.1+) |
| Event-loop async I/O in userland PHP | ReactPHP / Amp |
| Maximum throughput, coroutine-native runtime | Swoole / OpenSwoole |
| "Just handle more requests" | Scale PHP-FPM workers horizontally first |

## See Also

- `skills/php-ecosystem/laravel-patterns.md`
- `skills/php-ecosystem/php-performance.md`
