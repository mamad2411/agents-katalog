---
name: symfony-yoandev-async
description: >-
  Move work out of the request with Messenger, send email asynchronously with Mailer and
  TemplatedEmail, and run recurring jobs with Scheduler — Doctrine transport, retry and
  failure policy, prioritised queues, idempotent handlers, and workers under supervisor
  or systemd. Use this skill whenever someone asks to send an email, do something in the
  background, queue a job, run something every night or every five minutes, replace a
  crontab, speed up a slow import or a slow signup, process a big CSV, notify someone
  after an action, set up Messenger or a message handler or a worker, configure retries,
  deal with a message stuck in the failure queue, or says "my emails never arrive",
  "the import times out", "this page is slow because it sends mail", or "how do I
  schedule this".
---

# Asynchronous work

> **Tier: on demand** — nothing in this skill applies until an operation genuinely leaves the request. The first section decides whether it does; if not, close this file.

Messenger, Mailer and Scheduler. One transport, three rules.

## First: does this need to be asynchronous at all?

An operation becomes a message when **the user does not need the result**. That is the
whole test. Not "it is slow": slow work the user is waiting for is still slow when a
worker does it, it has just moved somewhere nobody is watching, and now the user gets a
success page for something that has not happened yet.

| Situation | Verdict |
|---|---|
| Importing 10,000 books from a CSV, mailing the user when it is done | Async |
| Sending the review-published email | Async — the next page does not depend on it |
| Generating a monthly export the user downloads later | Async |
| Recomputing a rating shown on the page rendering next | **Synchronous** |
| Validating a shelf import so the form can show errors | **Synchronous** |
| Anything whose result appears in the response | **Synchronous** |

The failure mode of getting this wrong is specific: the controller returns 200, the
handler throws three hours later, and nobody finds out because nobody reads the failure
transport. Async work needs an operational owner — on a project with no alerting and no
process supervisor, adding a queue makes the system *less* reliable. Say so before
installing anything.

## Messenger is not a command bus

Messenger is used here **only** for work that leaves the request. A controller calls a
service directly — `$this->shelfImporter->import($shelf, $file)` — and reaches for
`$this->bus->dispatch(new ImportShelf($id))` only when nobody is waiting.

Dispatching every action through the bus — the CQRS-flavoured "command bus" — is
deliberately rejected: the call site stops saying what happens, the stack trace goes
through five middlewares, and with a synchronous transport you paid all of that for a
method call. Same reasoning as `symfony-yoandev-architecture`: business consequences are
explicit calls, not dispatched events.

## Transport: Doctrine

`MESSENGER_TRANSPORT_DSN=doctrine://default?auto_setup=0` — the queue lives in the
application's own database: no extra infrastructure, pending messages visible with a
`SELECT`, covered by the backup and restore procedure that already exists. On PostgreSQL
and MySQL 8 the transport reads with `FOR UPDATE SKIP LOCKED`, so several workers are
safe.

`auto_setup=0` means `messenger_messages` is not created at runtime; it comes from a
migration, because Doctrine's schema listener adds the table to the generated schema and
`make:migration` picks it up like any other. No DDL in production.

**The limit, stated plainly.** Past roughly a few thousand messages a day the queue is
write load and vacuum pressure on the business database, on top of the constant polling
`SELECT … FOR UPDATE` from every worker. Escalate to Redis (`symfony/redis-messenger`)
then AMQP (`symfony/amqp-messenger`, for real routing and dead-lettering): a DSN change
plus draining the old transport, handlers unchanged. Do not install RabbitMQ for a
project sending a hundred emails a day.

## The three rules

They prevent the three bugs that actually happen.

### 1. A message carries identifiers, never entities

```php
#[AsMessage('async')]
final readonly class ImportShelf
{
    public function __construct(public int $shelfId, public string $uploadedFilePath) {}
}
```

A serialised entity is a snapshot: by the time the worker deserialises it the row has
moved on, and writing it back silently reverts whatever happened in between. Doctrine
proxies make it worse — what gets serialised is the proxy, not the data. The handler
reloads from the repository and works on current state.

`#[AsMessage]` (`Symfony\Component\Messenger\Attribute\AsMessage`, 7.2+) puts routing
next to the message; on 6.4–7.1 declare it under `routing:` in
`config/packages/messenger.yaml` instead — same rule, different place.

### 2. A handler is idempotent

Messenger retries. A handler that charges a card, sends an email or increments a counter
must survive running twice on the same message, because it will. Guard on checkable
state — `if ($shelf->getImportedAt() !== null) { return; }` — not on hope.

Symfony 7.3 added `DeduplicateMiddleware` / `DeduplicateStamp` (needs `symfony/lock`).
Its own docblock calls it "a best-effort idempotency primitive… not a correctness
primitive against a hostile queue producer": a convenience on top of an idempotent
handler, never a replacement for one.

### 3. A handler is a translation layer

Exactly like a controller: unpack the message, load what the service needs, call the
service, stop. A rule that lives here is unreachable from the synchronous path and
untestable without a transport.

```php
#[AsMessageHandler]
final readonly class ImportShelfHandler
{
    public function __construct(
        private ShelfRepository $shelves,
        private ShelfImporter $importer,
    ) {}

    public function __invoke(ImportShelf $message): void
    {
        $shelf = $this->shelves->find($message->shelfId)
            ?? throw new UnrecoverableMessageHandlingException(
                \sprintf('Shelf "%d" no longer exists.', $message->shelfId),
            );

        $this->importer->import($shelf, $message->uploadedFilePath);
    }
}
```

That one throw is the retry distinction: retrying will never make a deleted shelf exist,
so the message goes straight to the failure transport instead of burning three attempts.
`UnrecoverableMessageHandlingException` for "this will never work"; anything else for
"the network was down".

## Failure policy

```yaml
framework:
    messenger:
        failure_transport: failed
        transports:
            async:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                retry_strategy: { max_retries: 3, delay: 1000, multiplier: 2, jitter: 0.3 }
            failed: 'doctrine://default?queue_name=failed'
```

Three attempts at 1s / 2s / 4s, with jitter so a downed third-party API does not receive
every retry from every worker in the same millisecond (`jitter` defaults to `0.1`;
raising it is free insurance). The message then lands in `failed` — a Doctrine queue, so
persistent, surviving a restart, still there tomorrow morning.

**The rule that matters: a message reaching the failure transport must raise an alert.**
A failure queue nobody reads is a data-loss mechanism with extra steps.

This skill states the rule; **`symfony-yoandev-observability` owns the mechanism** and the code
is written once, in its `references/alerting.md`: a listener on `WorkerMessageFailedEvent`
guarded by `willRetry()`, logging at `critical` on an `alert` channel, and — the part that
decides whether it is an alert at all — a sink that does not re-enter Messenger. The one
fact worth carrying from here: **not `symfony_mailer`.** This standard routes
`SendEmailMessage` to `async`, so an email alert about the broken queue is queued on the
broken queue (measured). Do not copy the listener from memory; read that file.

## Prioritised queues

One transport per priority, so a 10,000-row import does not sit in front of a signup
email:

```yaml
transports:
    async_high: 'doctrine://default?queue_name=high'
    async:      'doctrine://default?queue_name=default'
    async_low:  'doctrine://default?queue_name=low'
```

```bash
php bin/console messenger:consume async_high async async_low
```

The worker drains receivers **in the order given** and only looks at `async` when
`async_high` is empty. `messenger:consume --queues=` does *not* work here — the Doctrine
receiver does not implement `QueueReceiverInterface`, that option belongs to AMQP and
Redis. With Doctrine, separate transports are the mechanism.

## Testing

Nothing here needs a running worker. **The handler** is instantiated and called directly
— `(new ImportShelfHandler($shelves, $importer))(new ImportShelf(12, $path))`. **The
dispatching service** gets a `createMock(MessageBusInterface::class)` with an `expects()`
on `dispatch` and a `self::callback()` checking the message values; the
`->willReturn(new Envelope($message))` is not optional, because `dispatch()` is declared
`: Envelope` and a mock returning `null` fails with a `TypeError` that reads like a bug
in your own code. **Functionally**, route `async` to `'in-memory://'` under `when@test:`
and read the recorded envelopes with `getSent()`. Full patterns:
`references/messenger.md`.

## Email and Scheduler, in two paragraphs

`SendEmailMessage` is routed to `async` by the recipe, and asynchronous is right. Once
the project has the prioritised transports above, **move it to `async_high`** — a signup
confirmation queueing behind a nightly import is the exact problem those transports exist
to solve, and it is a one-line change in `routing:` (`references/messenger.md`). It stays
in `routing:` rather than becoming `#[AsMessage]`, because you cannot put an attribute on
someone else's class. The trap: a
`TemplatedEmail` is rendered **by the worker**, so its context is serialised — put a
Doctrine entity in there and you ship a stale snapshot or a broken proxy. Pass scalars.
In tests the assertion is `assertQueuedEmailCount()`, not `assertEmailCount()`. The
rest: `references/mailer.md`.

`#[AsCronTask('0 3 * * *')]` on a service method beats a crontab: versioned with the code
it runs, and visible in review. **Its condition: it needs a running worker.** A crontab
runs because cron is always there; a schedule runs only while
`messenger:consume scheduler_default` is up — say that before installing it. Details:
`references/scheduler.md`.

## When something does not happen

| Symptom | Cause |
|---|---|
| Nothing happens, no error | No worker is consuming — `messenger:stats` shows the pending count |
| Emails never arrive locally | They are queued: `symfony console messenger:consume async -vv` |
| `Table messenger_messages does not exist` | `auto_setup=0` and the migration was not run |
| Handler runs old code after a deploy | `messenger:stop-workers` was skipped — see `symfony-yoandev-deployment` |
| A message is handled twice | Normal. That is what rule 2 is for |
| `Cannot instantiate proxy` on deserialise | An entity or proxy went into the message or the email context |
| The worker dies around 128 MB | Missing `--memory-limit`; that is a restart trigger, not a bug |
| Retries never stop | `RecoverableMessageHandlingException` defaults to `forceRetry: true`, bypassing `max_retries`. Pass `forceRetry: false` — **8.1+ only**; on 6.4–8.0 the parameter does not exist, the forced retry is unconditional, and the way out is to throw a different exception (`references/messenger.md`) |
| A scheduled task never fires | No worker on `scheduler_default`, or `dragonmantank/cron-expression` is missing |

## Reference files

| File | When to read it |
|---|---|
| `references/messenger.md` | Configuring transports and retries, running workers in production, the console commands, testing dispatch |
| `references/mailer.md` | Anything involving email: templates, CSS inlining, the serialisation trap, dev and test setup |
| `references/scheduler.md` | Recurring tasks, `#[AsSchedule]`, locking, missed runs, replacing a crontab |
