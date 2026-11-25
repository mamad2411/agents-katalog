---
name: symfony-yoandev-observability
description: >-
  Make a Symfony application say what it is doing in production: Monolog channels
  separating application logs from Doctrine and Messenger, processors attaching a
  correlation id and the current user, fingers_crossed explained, redaction of
  passwords and personal data, an alert when a message reaches the Messenger failure
  transport, a worker heartbeat, and a health check that actually tests the database.
  Use this skill whenever someone asks how to know if something broke in production,
  add logging, add a logger to a service, set up log channels, add error tracking or
  Sentry, get alerted when something fails, add a health check or readiness probe, find
  out why nothing appears in the logs, or says "we did not notice the queue was stuck",
  "nobody saw the error", "the logs are unreadable", "did that email actually send",
  "is the worker still alive", "how do I trace one user's request", or "there are
  passwords in our logs".
---

# Observability

> **Tier: on demand** — channels and redaction matter from the first production deploy; correlation ids, the worker heartbeat and health probes are switched on by a real worker, a real orchestrator, a real incident.

An application that reaches production and then goes silent is not finished. This skill
covers **what the application emits and how it is structured**: channels, levels,
processors, redaction, alerts, health. **Where logs go is infrastructure and out of
scope** — a file, stdout, a managed aggregator, a Grafana stack. The prod handler
configuration (`php://stderr`, JSON) is already `symfony-yoandev-deployment`'s; profiling and
Stopwatch are `symfony-yoandev-performance`'s; the dev server's log stream is
`symfony-yoandev-local-dev`'s.

## The pact this suite already made

The standard mandates `#[WithLogLevel]` on expected business exceptions so they stop
drowning real failures. That only pays off if something watches what remains. The ladder
Symfony applies, from `ErrorListener::resolveLogLevel()`:

| Exception | Level |
|---|---|
| Not an `HttpExceptionInterface`, or status ≥ 500 | `critical` |
| `HttpExceptionInterface` with a 4xx status (a plain 404 included) | `error` |
| Carries `#[WithLogLevel]` | whatever the attribute says |
| Listed in `framework.exceptions` with a `log_level` | that — **the config wins over the attribute** |

So **`critical` means "a request or a message died on something nobody planned for"**,
and that is the level an alert handler subscribes to; `error` is not a useful threshold,
because every 404 that `excluded_http_codes` does not filter lands there.
`framework.exceptions` also takes a `log_channel`, moving a whole family of expected
exceptions off the `request` channel entirely — `log_channel: business` with
`log_level: info` produces `business.INFO`, verified on 8.1 (check
`config:dump-reference framework exceptions` on an older version).

## Channels

A single log stream stops being readable at the size where you would actually need it:
on any real page Doctrine alone emits one record per statement, Messenger one per
dispatch, the cache one per miss, and the ten lines your own code wrote are a rounding
error. Channels are how you filter *before* the data leaves the process. Symfony ships
them already — `doctrine`, `messenger`, `request`, `security`, `cache`,
`http_client`, `mailer`, `console`, `router`, `event`, `php`, `deprecation` — so add
your own with `monolog.channels: ['deprecation', 'business', 'alert']` for anything
worth watching separately, then inject that channel's logger. Four ways work, verified
on monolog-bundle 4.0:

| How | Notes |
|---|---|
| `#[WithMonologChannel('business')]` on the class | Clearest. Monolog 3.5 + monolog-bundle 3.9 |
| `#[Target('business')]` on the `LoggerInterface` argument | Argument-level, when one class needs two channels |
| Name the argument `$businessLogger` | Works, invisible. Rename the variable and the channel silently changes |
| `#[Autowire(service: 'monolog.logger.business')]` | The escape hatch when the alias does not exist |

**One trap, measured.** `#[Target]` and `#[Autowire(service:)]` fail at compile time on a
typo, listing every channel that does exist. `#[WithMonologChannel]` does not: a misspelt
channel is silently *created*, escapes every handler filter, and nothing warns you.
`debug:container --tag=monolog.channel_logger` lists them; a name you do not recognise
is a typo.

## fingers_crossed, and why a working request logs nothing

The prod recipe wraps the stream handler in `fingers_crossed`. It **buffers everything
and writes nothing** until one record reaches `action_level` (`error` by default), then
flushes the entire buffer — the debug trail that led to the failure — and keeps passing
records through for the rest of the process. Two consequences people report as bugs:
a successful request writes **zero lines** (so
`info` calls tracing a happy path never appear in production), and a failing one dumps
up to `buffer_size` (50 in the recipe) records at once, including every Doctrine
statement **with its bound parameter values** — the point of the mechanism, and the
biggest single source of secrets in logs.

In a Messenger worker the handler is reset between messages (`kernel.reset`, via
Messenger's `ResetServicesListener`), so a failing message flushes its own trail and a
successful one stays silent, exactly as in a request. `passthru_level` and
`excluded_http_codes`: `references/monolog.md`.

## One user action, several processes

A correlation id is what makes a request and the workers it spawned readable as one
story. Three pieces: a holder service resolving the id from an `X-Request-Id` header or
generating one (implementing `ResetInterface`, so a long-running worker does not reuse
it); a Monolog processor putting it on every record; a Messenger middleware stamping
outgoing envelopes and restoring the id in the worker.

```php
#[AsMonologProcessor]
final readonly class CorrelationIdProcessor
{
    public function __construct(private CorrelationId $correlationId) {}

    public function __invoke(LogRecord $record): LogRecord
    {
        $record->extra['correlation_id'] = $this->correlationId->get();

        return $record;
    }
}
```

Measured end to end: an id generated in the dispatching process appeared on all 29
records the worker wrote while handling that message, including the framework's own
`messenger.CRITICAL`. This needs **no kernel listener** — the holder reads
`RequestStack`, which keeps it inside the "kernel listeners are a last resort" rule.
Full code, plus the user/token processor: `references/monolog.md`. `#[AsMonologProcessor]`
is monolog-bundle 3.8+ (`priority:`, Monolog 3.4 and monolog-bundle 3.11); below that,
tag `monolog.processor` in YAML.

## What must never be logged

A log ends up in a backup, in a third-party aggregator, and in a support screenshot.
Passwords, tokens, API keys, session ids, card and bank numbers, and personal data
beyond what you need to identify the actor do not belong there.

The mechanism is a redacting processor at low priority — it runs before the handlers'
own PSR-3 interpolation, so `{password}` in a message string is redacted too (verified).
The trap it cannot fix is a value you concatenated into the message yourself: **put data
in the context array, never in the message string.** The leak to check first is
`doctrine.dbal.logging` — it defaults to `%kernel.debug%`, so it is off in production,
but anyone who switches it on to chase a slow query starts writing every bound parameter
at `debug`, and `fingers_crossed` flushes those on the next error. Sinks and the
processor code: `references/sensitive-data.md`.

## The Messenger failure alert

`symfony-yoandev-async` states the rule — a message reaching the failure transport must raise an
alert — without the mechanism. Here it is: what the framework already does, what a
listener adds, and the sink that decides whether any of it is an alert.

**The framework already logs it.** `SendFailedMessageForRetryListener` writes
`messenger.CRITICAL: Error thrown while handling message … Removing from transport
after N retries` the moment retries are exhausted, before
`SendFailedMessageToFailureTransportListener` (priority -100) moves the envelope. If
`critical` already reaches a human, you are done.

**A listener adds the structure** — `#[AsEventListener]` on `WorkerMessageFailedEvent`,
guarded on `willRetry()` so the three retries stay quiet:

```php
// The canonical copy is references/alerting.md; this one is identical to it.
#[AsEventListener]
#[WithMonologChannel('alert')]
final readonly class AlertOnMessageSentToFailureTransport
{
    public function __construct(private LoggerInterface $logger) {}

    public function __invoke(WorkerMessageFailedEvent $event): void
    {
        if ($event->willRetry()) {
            return;
        }

        $envelope = $event->getEnvelope();

        $this->logger->critical('Message moved to the failure transport', [
            'message_class' => $envelope->getMessage()::class,
            'transport' => $event->getReceiverName(),
            'retries' => RedeliveryStamp::getRetryCountFromEnvelope($envelope),
            'exception' => $event->getThrowable(),
        ]);
    }
}
```

**The sink is the part that decides whether it is an alert.** And here is the finding
that matters: **do not send it by email.** Verified — with `SendEmailMessage` routed to
`async` as this standard requires, a `symfony_mailer` Monolog handler produces
`messenger.INFO: Sending message SendEmailMessage with async sender`. The alert about
the broken queue is queued *on the broken queue*. Use a sink that does not re-enter
Messenger — a `slackwebhook` handler, `error_log`, Sentry, or `critical` on stderr with
the platform's own alerting rule — and wrap a third-party sink in a `fallbackgroup`
handler: an unreachable webhook throws, and Monolog lets that exception turn a logged
error into a 500 (measured).

**A listener cannot fire if no worker is running**, which is the most common reason a
queue rots. That needs the second mechanism: a worker heartbeat written on
`WorkerRunningEvent`, plus a probe on queue depth — both in `references/alerting.md`,
with the console commands (`messenger:stats --format=json`, `messenger:failed:show
--stats`) for the shell-script version.

## Health checks

A route returning 200 unconditionally tells the orchestrator the container has booted,
not that the application works. Test the dependencies:

```php
public function run(): bool
{
    return 1 === (int) $this->connection
        ->executeQuery($this->connection->getDatabasePlatform()->getDummySelectSQL())
        ->fetchOne();
}
```

**Two deliberate exceptions to the standard live in this endpoint, and both are exceptions
rather than oversights.** The first is here: this is SQL outside a repository. It is
allowed because it is not a query about the domain — there is no intent to name and no
result to map, it is a connectivity probe — so it stays in a dedicated `Health\` service
where the exception remains visible instead of spreading. The second is below.

`getDummySelectSQL()` is portable where a literal `SELECT 1` is not (Oracle needs
`FROM DUAL`). Collect the checks with `#[AutoconfigureTag]` on a `HealthCheck` interface
and **`#[AutowireLocator]`** in the controller — with an iterator each check is built by
the `foreach`, outside any `try`, and one unbuildable check 500s the whole endpoint
(measured). Return **503 when any check fails**; a probe that always answers 200 is
decorative.

That is the second exception: the standard says an action returns data and `#[Serialize]`
decides the representation, but `#[Serialize]`'s `code` is fixed at attribute level, so it
cannot express a status that depends on the result. A bare `JsonResponse` is therefore
correct *here* — because the attribute genuinely cannot do it, not because it was more
convenient — and nowhere else.

Verified running: `{"status":"degraded","checks":{"database":"ok","failure_queue":"failed","worker":"ok"}}`
with HTTP 503. Full implementation, and which checks belong on a liveness versus a
readiness probe: `references/alerting.md`.

## Error tracking

Sentry or an equivalent adds what a log line cannot: the same exception grouped across
occurrences, a release marker, the request and user attached, and a notification the
first time a fingerprint appears. It replaces nothing — the logs are still the trail
that led there. On monolog-bundle 4.0 the built-in `sentry` and `raven` handler **types
were removed**; integrate through `sentry/sentry-symfony` and a `service`-type handler.

The one thing that matters when wiring it: **do not send the exceptions
`#[WithLogLevel]` already marked as expected.** The log-level route does this for free —
an SDK integrated as a Monolog handler at `level: critical` never sees the `info` the
attribute produced. The SDK's own ignore list is the second lever; read its current
config key with `debug:config` rather than copying one from a blog post.

## When nothing shows up

| Symptom | Cause |
|---|---|
| Nothing in the prod log for a working request | `fingers_crossed` — that is correct behaviour, not a broken handler |
| `info` calls never appear in production | Same. They are buffered and discarded unless the request errors |
| A whole exception family drowns the log | Missing `#[WithLogLevel]`, or a 4xx logged at `error` — add `excluded_http_codes` |
| The alert handler never fires | Its `level` is above what the record carries, or a `channels:` filter excludes it |
| Alert emails never arrive when the queue breaks | They are queued on the queue that broke. Use a sink outside Messenger |
| A channel filter has no effect | The channel name is a typo — `debug:container --tag=monolog.channel_logger` |
| A processor's field is missing from some records | It is scoped to a channel or a handler — `debug:container --tag=monolog.processor` |
| Logs full of SQL parameters | `doctrine.dbal.logging` was turned on, and `fingers_crossed` flushed the buffer |
| Health check returns 200 while the app is broken | It tests nothing. Give it a real dependency check |
| The health endpoint 500s | One check could not even be constructed — use `#[AutowireLocator]`, not `#[AutowireIterator]` |
| The correlation id changes mid-worker | The holder is not `ResetInterface`, or the middleware is not registered on the bus |

## Reference files

| File | When to read it |
|---|---|
| `references/monolog.md` | Configuring channels and handlers, writing a processor, `fingers_crossed` options, per-environment setup, asserting in a test that something was logged |
| `references/sensitive-data.md` | Before logging anything derived from user input, or when a log review turns up a secret |
| `references/alerting.md` | Wiring the Messenger failure alert and its sink, the worker heartbeat, the queue-depth watchdog, health check endpoints |
