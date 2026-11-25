---
name: symfony-yoandev-architecture
description: >-
  Decide where code goes in a Symfony project and wire it correctly: the Controller /
  Service / Repository / DTO / Entity contract, the three DTO namespaces (Input, Read,
  Output), service design and who calls flush(), business exceptions carrying their own
  HTTP status, direct calls instead of domain events, configuration split between env
  vars, app. parameters and class constants, and the dependency-injection attributes
  (#[Autowire], #[AutowireIterator], #[AutowireLocator], #[AsDecorator], #[AsTaggedItem],
  #[Target], #[When], #[Lazy]). Use this skill whenever someone asks where a piece of
  logic belongs, wants a new service or DTO, says a controller has grown too big, wants
  to extract or move a class that has outgrown its place, asks how to make something
  configurable or add a setting or an env var, asks why a service is not autowired or how
  to inject one of several implementations, wants a factory, strategy, decorator or
  object mapping, or asks "is this the right place for this?", "how should I structure
  this feature?", "where does the rating logic go?", "extract this", "why does my
  exception return a 500?". Also use it for the list of alternatives this standard
  deliberately rejected and why. For a feature described in plain language, or a bare
  "refactor this" with no target, `symfony-yoandev-standards` routes first.
---

# Architecture

> **Tier: core** — the layer contract and the five rules live here, and none of them is optional. The one on-demand item is the deptrac configuration that enforces it mechanically (`symfony-yoandev-quality`).

Where code goes, and why the boundary is where it is.

One rule generates most of the others: **the entity holds no rule, so the service holds
every rule.** Everything below follows from that.

## The layer contract

| Layer | May do | May not do |
|---|---|---|
| **Controller** | Read the request, call one service, choose a representation | Business rules, `EntityManager`, DQL, `flush()` |
| **Service** | Every business rule, orchestration, `flush()` | Build queries, know that HTTP exists, return entities to the outside |
| **Repository** | DQL, QueryBuilder, SQL, `persist()`, `remove()` | Business rules, `flush()` |
| **DTO** | Carry data across a boundary, hold validation constraints | Depend on Doctrine, contain logic beyond normalisation |
| **Entity** | Mapped state, getters, setters, value constants | Invariants, `publish()`-style domain methods |

The contract holds by being followed; `symfony-yoandev-quality` ships a deptrac configuration
that verifies it mechanically, for the day a second developer or an unsupervised agent
makes review insufficient. If a class does not fit a layer, the class is in the wrong
place — do not widen the rule.

### Why entities are anemic, and what it costs

Entities are generated in maker format: private properties, getters, setters. That is a
deliberate trade, not a law of nature, and its terms must be stated rather than
discovered.

**What it buys.** One rule with no exceptions — every rule lives in a service — which is
easy to teach, easy to review, and checkable by deptrac. And zero friction with the
tooling: `make:entity`, the Form component, fixtures and EasyAdmin all expect setters and
a no-argument constructor, and all keep working untouched.

**What it costs.** A setter enforces nothing, so nothing technical stops
`$book->setRating(9)` outside `BookRater`. The guarantee rests on every write path going
through the service. That is a real weakness; it is bounded rather than eliminated:

- The HTTP edge — the one path you did not write — is covered by the Input DTO's
  constraints (`symfony-yoandev-http`).
- Commands, fixtures and other services are code you write and test; a rule they need is
  a service they call.
- A surface that writes without a service, EasyAdmin above all, applies no rule at all.
  It is a trusted surface. When a local rule must still hold there, duplicate it as an
  `#[Assert]` constraint on the entity, reading the same constants — that is the one
  case where a constraint belongs on an entity (`symfony-yoandev-doctrine`).

Rich entities — a constructor for the mandatory fields, `rate()` instead of
`setRating()` — would close that gap for local rules. They are rejected here because they
pay for it in every tool listed above, and because most rules outgrow the entity the day
they need a query. The reasoning is in `references/rejections.md`.

Therefore every rule lives in a service, and the entity is a typed row.

```php
// src/Entity/Book.php — values, not rules. Constants are fine here: they are data.
public const MIN_RATING = 1;
public const MAX_RATING = 5;

public function setRating(?int $rating): static { $this->rating = $rating; return $this; }
```

```php
// src/Service/BookRater.php — the rule, in the only place that can enforce it.
final readonly class BookRater
{
    public function __construct(
        private BookRepository $books,
        private EntityManagerInterface $em,
        private ObjectMapperInterface $mapper,
    ) {
    }

    public function rate(int $bookId, RateBookInput $input): BookView
    {
        if (null === $book = $this->books->find($bookId)) {
            throw new BookNotFound($bookId);
        }

        if ($input->rating < Book::MIN_RATING || $input->rating > Book::MAX_RATING) {
            throw new InvalidRating($input->rating);
        }

        $book->setRating($input->rating);
        $this->em->flush();

        return $this->mapper->map($book, BookView::class);
    }
}
```

Do not write `$book->rate(5)` anywhere. If you find one, move the check into the service
that calls it. (`ObjectMapperInterface` is `symfony/object-mapper` — **7.3 experimental,
stable 7.4, absent on 6.4**; without it, a `static fromEntity()` on the Output DTO. The
rule does not change, only the means — `references/dtos.md`.)

## Service design

- **`final readonly`**, constructor injection only. `final` because the extension point
  is a decorator or a strategy, not inheritance; `readonly` because a service that
  mutates itself is a service that behaves differently on the second request.
  **The exception this rule creates:** a `final` concrete class **cannot be decorated** —
  `#[AsDecorator]` on a service whose consumers typehint the concrete class fails
  `lint:container`. So when a decorator is needed, extract an interface, alias the
  implementation to it, decorate the interface id — rather than dropping `final`.
  Worked example in `references/dependency-injection.md`.
- **One responsibility, named after it.** `BookRater`, `ShelfReader`, `BookCreator` —
  not `BookService`, which is a folder pretending to be a class.
- **The service calls `flush()`, once per use case.** The repository does `persist()`
  and `remove()`. One transaction boundary per business operation, visible in the method
  that owns the operation. A `flush()` inside a repository method makes the boundary
  invisible and turns two writes into two transactions.
- **A service never returns an entity to a controller.** It returns an Output DTO. An
  entity that escapes the service layer is a lazy-loading N+1 waiting for a template.
- **A service takes identifiers and loads the entity itself.** `rate(int $bookId, …)`,
  then `$this->books->find($bookId) ?? throw new BookNotFound($bookId)`. The service
  owns the "not found" because it must work the same from a controller, a command and a
  message handler, and all three carry an id. The controller resolves the entity
  (`Book $book`, the EntityValueResolver) in exactly one case: an attribute needs the
  object *before* the action runs — `#[IsGranted(…, subject: 'book')]` on a voter. It
  still passes `$book->getId()` to the service, and the service's `find()` costs no
  query: the identity map already holds the row. Two paths to a 404, one rule for which.
- **Repositories are the exception to `final`** — they are doubled in service unit
  tests. Everything else is `final`.

## Business exceptions

Failures that the caller cannot prevent get a named exception in `src/Exception/`,
carrying its own HTTP translation. That keeps the controller free of `try`/`catch` and
the mapping next to the meaning.

```php
#[WithHttpStatus(Response::HTTP_NOT_FOUND)]
#[WithLogLevel(LogLevel::INFO)]          // a missing book is not an incident
final class BookNotFound extends \DomainException
{
    public function __construct(public readonly int $bookId)
    {
        parent::__construct(\sprintf('No book #%d on this shelf.', $bookId));
    }
}
```

Both are `Symfony\Component\HttpKernel\Attribute\*`, **since 6.3**, and both are read
from parent classes, so a base `App\Exception\NotFound` propagates to its children.
Before 6.3, map the exception under `framework.exceptions` instead.

Two things that surprise people, both checked in `ErrorListener`:

- **`#[WithHttpStatus]` is ignored when the exception already implements
  `HttpExceptionInterface`.** Do not extend `NotFoundHttpException` and then decorate it.
- **`framework.exceptions` in configuration wins over the attribute — over
  `#[WithLogLevel]` as much as over `#[WithHttpStatus]`.** An entry's `log_level` and
  `log_channel` both beat what the attribute says, verified on 8.1. Use that entry to map
  *third-party* exceptions you cannot annotate; use the attribute for your own, and do
  not expect an attribute to win back a class the configuration already names.

Leave the attribute off deliberately when the exception means "a bug reached here" —
`InvalidRating` above should be impossible, because the Input DTO's `#[Assert\Range]`
already rejected it at the HTTP edge. A 500 is the correct answer, and a silent 422
would hide the defect. Say so in a comment; the absence of an attribute otherwise reads
as an oversight.

## Direct calls, not domain events

When a service has done its work and something else must happen, it calls the
collaborator:

```php
$this->em->flush();
$this->notifier->notifyAuthor($review);   // yes
```

Not `$this->dispatcher->dispatch(new ReviewPublished($review))`.

The reason is legibility under maintenance. With a direct call, the whole consequence of
publishing a review is readable in one method, and the unit test asserts the notifier was
called. With a domain event, answering "what happens when a review is published?" becomes
a project-wide search, and the answer depends on listener priorities that appear nowhere
near the code. The dispatcher buys decoupling that a single application does not need and
charges for it on every future read.

**`#[AsEventListener]` is for framework events only** — `kernel.exception`,
`kernel.response`, Doctrine, Messenger, Security. One class per event, named after what
it does, with `__invoke()`:

```php
#[AsEventListener]                        // event inferred from the parameter type
final readonly class AddNoIndexHeaderOnStaging
{
    public function __invoke(ResponseEvent $event): void { /* … */ }
}
```

Inference from the type declaration needs no `event:` argument; pass one only for events
identified by a string name. `EventSubscriberInterface` is rejected: more ceremony, and a
static method to keep in sync with the class.

**Kernel listeners are a last resort.** Reach first for the dedicated mechanism —
`#[WithHttpStatus]`/`#[WithLogLevel]` for errors, a ValueResolver to inject an argument,
`#[Cache]` for headers, a Voter for authorisation. A kernel listener runs on everything,
far from the code it affects, and debugs badly. Write one only when nothing else exists.

## Configuration: three places, one question each

| Ask | Answer | Where |
|---|---|---|
| Does it differ per machine or per environment? | DSN, base URLs, API keys | env var |
| Is it application behaviour, identical everywhere? | retention days, feature flag | parameter prefixed `app.` |
| Does it almost never change? | page size, rating bounds | class constant |

```php
public function __construct(
    #[Autowire(param: 'app.shelf_page_size')] private int $pageSize,
    #[Autowire(env: 'bool:FEATURE_IMPORT')] private bool $importEnabled,
) {
}
```

`#[Autowire]` accepts exactly one of `value`, `service`, `expression`, `env` or `param` —
passing two throws at compile time.

**Secrets: `.env.local` in development, the platform's secret store in production, and
the Symfony secrets vault the moment neither covers the case.** The suite deploys a
container image (`symfony-yoandev-deployment`), and every container platform already has a
secret store that injects environment variables. There, the vault would be a second
store whose own decryption key still has to come from the first; one store is enough.
The vault is **not** rejected on its merits — its decryption key is one environment
variable, no harder to deploy than a DSN, and it is the only mechanism that lets a
secret be versioned and reviewed. It is the answer as soon as there is no platform store
(a bare server, an rsync deploy), or as soon as secrets must travel through the
repository. What is rejected is `.env.local` on a production host, and two mechanisms
on one project.

## Dependency injection and patterns

Constructor injection covers almost everything. When it does not, the attributes are in
`Symfony\Component\DependencyInjection\Attribute\` — every one of them verified against
`vendor/`, with the version each landed in, in `references/dependency-injection.md`. That
file also covers Strategy (`#[AutowireLocator]` + `#[AsTaggedItem]`), Decorator
(`#[AsDecorator]` + `#[AutowireDecorated]`), Factory, and the two attributes this standard
deliberately does not use: `#[Required]` and `#[SubscribedService]`.

**Voters are authorisation, not architecture.** They exist, they are the right tool for
object-level permissions, and they belong to `symfony-yoandev-security`. Do not put a permission
check in a service "because rules live in services".

## Reading a misplaced piece of code

| Symptom | What it actually means |
|---|---|
| `$em->flush()` in a controller | The use case has no service yet |
| A `QueryBuilder` in a service | The query needs a named repository method |
| A service typehinting `Request` | The controller should have passed an Input DTO |
| A template calling `book.ratings\|length` | An entity escaped the service layer |
| An `if` on a role inside a service | That is a Voter (`symfony-yoandev-security`) |
| A service constructor with eight arguments | Two use cases wearing one class name |
| `new SomeService(...)` inside a service | A collaborator that should be injected |

## Reference files

| File | When to read it |
|---|---|
| `references/dtos.md` | Designing Input / Read / Output DTOs, or normalising a projection |
| `references/dependency-injection.md` | Injecting anything constructor autowiring cannot resolve; Strategy, Decorator, Factory |
| `references/rejections.md` | Someone proposes an alternative — check whether it was already rejected, and why |
