---
name: symfony-yoandev-console
description: >-
  Write Symfony console commands as thin translation layers over a service: one class
  per command family with method-level #[AsCommand] on Symfony 8.1, invokable commands
  with #[Argument] and #[Option] before that, SymfonyStyle output, dry run by default
  with --force on anything destructive, mandatory locking on long or scheduled commands,
  clean shutdown on SIGTERM, and a smoke test with runCommand or CommandTester. Use this
  skill whenever someone asks to add a command, write a script, make something runnable
  from the terminal, build an import or an export or a batch job, clean up or purge or
  delete old data, backfill a column, send a digest, "run this once", "I need a CLI for
  this", "make:command", says a command times out or eats all the memory or deleted more
  than it should, or asks how to test a command. For scheduling that command to run every
  night, and for Messenger workers, use symfony-yoandev-async instead.
---

# Console commands

> **Tier: core when writing a command** — and within it, dry-run by default and the lock are not optional on a destructive or scheduled command. Everything else is a command like any other.

A command is a translation layer, exactly like a controller. It parses input, calls **one**
service, formats output. That is the whole job.

The reason is not tidiness. A rule that lives inside `__invoke()` can only be exercised by
booting a console, building an input and reading text back out of a buffer; the same rule
in a service is tested by calling a method and asserting on the return value. Every
business decision left in a command is a decision you will only ever test through a string.

```php
#[AsCommand(name: 'app:shelf:purge', description: 'Remove abandoned shelves')]
public function purge(
    SymfonyStyle $io,
    #[Option(description: 'Actually delete, instead of reporting')] bool $force = false,
): int {
    $report = $this->shelfPurger->purge(dryRun: !$force);   // the only call

    $io->table(['Shelf', 'Books'], $report->rows());
    $io->success(\sprintf('%d shelves %s.', $report->count, $force ? 'deleted' : 'concerned'));

    return Command::SUCCESS;
}
```

## The shape, by version

`vendor/` is the source of truth over anything written here — check which forms exist
before choosing.

| Symfony | Write this |
|---|---|
| **8.1+** | One class per command **family**, one public method per command, `#[AsCommand]` on each method |
| **7.3 – 8.0** | One **invokable** class per command, `#[AsCommand]` on the class, `__invoke()` with `#[Argument]` / `#[Option]` |
| **6.4 – 7.2** | One class per command extending `Command`, `#[AsCommand]` on the class, `configure()` + `execute()` |

The family form is the goal: `app:user:create` and `app:user:delete` share a constructor,
share their input conventions, and are read together.

```php
final class UserCommands
{
    public function __construct(private readonly UserRegistrar $registrar) {}

    #[AsCommand(name: 'app:user:create', description: 'Create a user')]
    public function create(SymfonyStyle $io, #[Argument] string $email): int { /* … */ }

    #[AsCommand(name: 'app:user:delete', description: 'Delete a user')]
    public function delete(SymfonyStyle $io, #[Argument] string $email): int { /* … */ }
}
```

Autoconfiguration tags the service once per attributed method and the container builds one
`Command` per method. The class must **not** extend `Command` — mixing the two throws at
compile time — and the methods must be public and non-static.

**`extends Command` is not deprecated.** It still works in 8.1, and `configure()` /
`execute()` are not marked for removal. It is simply no longer what you write for new
code — and it remains the right answer for the one thing invokable commands cannot do
(signals, below). All three forms side by side, plus the full input inference table:
`references/writing-commands.md`.

## Input is inferred from the signature

Argument and option definitions come from parameter types and defaults. Two surprises:

- **Names are kebab-cased.** `int $bookId` is `<book-id>` on the command line, and
  `?string $olderThan` is `--older-than`. Nothing warns you.
- **An option parameter must have a default**, otherwise the container throws. That is
  what makes it an option rather than an argument.

```php
#[Argument] array $shelves = [],            // <shelves>...  (variadic)
#[Option] ?string $olderThan = null,        // --older-than=OLDER-THAN
#[Option] int $batchSize = 500,             // --batch-size=BATCH-SIZE [default: 500]
#[Option] bool $force = false,              // --force
#[Option] bool $report = true,              // --report|--no-report   (negatable)
```

`SymfonyStyle`, `InputInterface`, `OutputInterface`, `Application` and `Cursor` are
injected by type — do not declare them as arguments, and do not build a `SymfonyStyle` by
hand. Return an `int`, always: `Command::SUCCESS` (0), `Command::FAILURE` (1),
`Command::INVALID` (2). Anything else raises a `TypeError`.

## Destructive commands: dry run by default

**A command that deletes, truncates, anonymises or overwrites reports by default and only
acts with `--force`.** Without `--force` it prints what it would do and exits `SUCCESS` —
a dry run that succeeded is a success.

This is deliberately *not* an interactive confirmation. `$io->confirm()` is skipped the
moment `--no-interaction` is passed, which is exactly how CI, deploy scripts and schedulers
run everything. A prompt protects a human at a terminal and nobody else; `--force` protects
both, because the safe path is the default one.

**Print counts before and after, from two separate queries.** A gap between
`Shelves concerned: 1240` and `Shelves deleted: 1240` is the only thing that reveals a
silent partial delete — a foreign key that swallowed rows, a batch that stopped early, a
filter that moved between the count and the delete. Printing the same variable twice
proves nothing.

The complete pattern — service signature, command, and the tests covering both branches —
is in `references/destructive-and-scheduled.md`.

## Locking is mandatory on long or scheduled commands

A task that takes six minutes and is scheduled every five stacks. By the end of the day
hundreds of copies compete for the same rows, and the symptom is a server that dies rather
than a command that fails.

`LockableTrait` ships with `symfony/console`, but the lock component does not —
`composer require symfony/lock`. Without it the trait throws *"To enable the locking
feature you must install the symfony/lock component."* at runtime, on the first execution,
in production.

```php
if (!$this->lock('app:digest:send')) {
    $io->warning('Already running, skipping this run.');

    return Command::SUCCESS;      // not FAILURE — a skipped run is the design working
}

try {
    // …
    return Command::SUCCESS;
} finally {
    $this->release();
}
```

Three things that bite. **`finally`, not a trailing `release()`** — an escaping exception
leaves the lock held, and while flock frees it when the process dies, a database store
does not, so the next run is blocked until its TTL expires. **Name the lock explicitly in
a command family**, because `$this->lock()` with no argument reads the `#[AsCommand]`
attribute *on the class*, which a family class does not have, and throws `Lock name
missing`. And **`LockableTrait` ignores `LOCK_DSN`**: it builds its own semaphore or flock
store, both local to one machine, which on more than one server is not a lock — assign the
autowired `LockFactory` to `$this->lockFactory` in the constructor.

Scheduling the command itself (`#[AsCronTask]`, `#[AsPeriodicTask]`, workers) belongs to
**symfony-yoandev-async**. The lock belongs here because it is a property of the command.

## Long-running commands and memory

Doctrine's unit of work keeps a reference to every entity it hydrates, so a command
walking 500 000 rows holds 500 000 objects until it exits. It does not leak slowly: it
grows linearly, then hits `memory_limit`.

```php
foreach ($this->repository->iterateStaleReviews() as $i => $review) {   // toIterable()
    $this->archiver->archive($review);

    if (0 === $i % 500) {
        $em->flush();
        $em->clear();       // drop everything hydrated so far
    }
}
```

`$em->clear()` detaches **everything**, including entities you were still holding — so
re-fetch after clearing, never keep a reference across the boundary. The query belongs in
the repository (`toIterable()` on a `QueryBuilder` result), the batching in the service.
Fetch-join caveats and the rest: `references/destructive-and-scheduled.md`.

## Output that survives being redirected to a file

`SymfonyStyle` gives you `title()`, `section()`, `success()`, `warning()`, `error()`,
`table()`, `progressIterate()`. Use them; do not hand-roll `writeln()` with dashes.

The rule that matters: **a scheduled command's output is read in a log file, weeks later,
by someone who does not know what it does.** Print the parameters it ran with, print
counts rather than adjectives, put diagnostics behind verbosity:

```php
$io->writeln(\sprintf('Purging shelves older than %s (batch %d)', $olderThan, $batchSize));

if ($io->isVerbose()) {
    $io->writeln(\sprintf('  · shelf #%d (%d books)', $shelf->getId(), $count));
}
```

A progress bar in a log file is a wall of control characters: guard it, or run scheduled
invocations with `--no-ansi`. Errors go to stderr via `$io->getErrorStyle()`, which is
what lets a caller separate a report from a failure.

## Testing: unit test the service, smoke test the command

The command holds no rule, so there is nothing in it worth a thorough test. What a smoke
test proves is that the wiring holds: the service id resolves, the arguments bind, the
exit code is right.

```php
final class ShelfCommandsTest extends KernelTestCase
{
    #[Test]
    public function it_reports_without_deleting_by_default(): void
    {
        $result = self::runCommand('app:shelf:purge');           // Symfony 8.1+

        $this->assertCommandIsSuccessful($result);
        self::assertStringContainsString('1240 shelves concerned', $result->getDisplay());
    }
}
```

`runCommand()` comes from `ConsoleCommandAssertionsTrait`, which `KernelTestCase` already
uses, and it boots the kernel for you. Before 8.1, build a
`Symfony\Bundle\FrameworkBundle\Console\Application` and use `CommandTester::execute()`;
both forms are in `references/writing-commands.md`.

**Destructive commands are the exception and get real coverage**: dry run does not touch
the database, `--force` does, and the exit codes are asserted. A command is often the only
entry point to an irreversible operation, and "we thought it was in dry run" is a sentence
people say afterwards.

## When something goes wrong

| Symptom | Cause |
|---|---|
| Command not listed by `bin/console list` | The class extends `Command` *and* uses method-level `#[AsCommand]`, or the method is private or static |
| `The option ... must declare a default value` | An `#[Option]` parameter with no default. Options are optional by definition |
| `--my-option` not recognised, `--my-option` in code | Names are kebab-cased from the parameter: `$myOption` → `--my-option` |
| Missing argument exits `1`, not `2` | Input binding failures are `FAILURE`. `INVALID` is for *your* validation of a value that parsed fine |
| `LogicException: To enable the locking feature…` | `symfony/lock` is not installed |
| `Lock name missing` | `$this->lock()` with no name in a method-level command family. Pass the name |
| Two copies running despite the lock | `LockableTrait`'s default store is per-machine. Inject the configured `LockFactory` |
| `Allowed memory size exhausted` after N rows | Doctrine's identity map. `toIterable()` plus a periodic `clear()` |
| SIGTERM kills the command mid-write | `SignalableCommandInterface` does not fire on invokable commands (see the reference); use `extends Command` for that one command |
| Deleted more rows than reported | Counted and deleted in one query, or the filter differs between the two. Count, act, count again |

## Reference files

| File | When to read it |
|---|---|
| `references/writing-commands.md` | Writing any command: the three version-specific forms, the full input inference table, output and verbosity, signals, both testing APIs |
| `references/destructive-and-scheduled.md` | Anything that deletes or overwrites, anything scheduled or long-running: the dry-run/`--force` pattern end to end, locking stores and pitfalls, Doctrine memory in batches, testing an irreversible command |
