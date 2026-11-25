---
name: symfony-yoandev-http
description: >-
  Write the HTTP layer of a Symfony application: controllers, routes, request input
  mapping, JSON and HTML responses, forms and Twig templates. One controller class per
  resource, a class-level route prefix, input DTOs hydrated by #[MapRequestPayload] or a
  FormType, output through #[Serialize] for JSON and #[Template] for HTML, RFC 7807
  Problem Details for API errors, and an items + meta envelope for lists. Use this skill
  whenever someone asks to add a page, add a route or an endpoint, expose something as
  JSON, build an API, make a CRUD, build or wire up a form, map an uploaded file off the
  request, read a query parameter, paginate a list, return a 404 or a 422, protect an
  action with a CSRF token, render or restructure a Twig template, or says their endpoint
  returns a 500, their form never validates, their JSON has the wrong shape, or their
  route matches the wrong action. For what then happens to that uploaded file — where it
  is stored, how it is served back, who may read it — use `symfony-yoandev-storage` instead.
---

# HTTP layer

> **Tier: core** — with the simplifications `symfony-yoandev-standards` lists under *What the rules do not require* — no Input DTO for a plain GET, one Output DTO per shape.

Controllers, routing, request input, responses, forms, templates.

A controller is a translation layer: HTTP in, a service call, a representation out. It
holds no rule. That is not tidiness — it is what makes the rule testable without a
kernel, and what lets the same service serve an HTML page and a JSON endpoint without
either one being a special case.

## The shape of a controller

One class per resource, class-level route prefix, one action per use case.

```php
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Service\ShelfReader;
use Symfony\Bridge\Twig\Attribute\Template;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/books', name: 'book_')]
final class BookController extends AbstractController
{
    public function __construct(private readonly ShelfReader $shelf)
    {
    }

    #[Route('', name: 'index', methods: ['GET'])]
    #[Template('book/index.html.twig')]
    public function index(): array
    {
        return ['books' => $this->shelf->shelf()];        // list<BookView>
    }

    #[Route('/{id}', name: 'show', methods: ['GET'], requirements: ['id' => '\d+'])]
    #[Template('book/show.html.twig')]
    public function show(int $id): array
    {
        return ['book' => $this->shelf->book($id)];       // BookView, not a Book entity
    }
}
```

**The template receives an output DTO, never the entity.** And the controller does not
load entities as a habit: the service takes an id and owns the 404 (`BookNotFound`,
`symfony-yoandev-architecture`). The EntityValueResolver (`Book $book`) has one job — resolving
the subject a `#[IsGranted]` voter needs before the action runs — and even then the
action passes `$book->getId()` on; the service's `find()` is answered by the identity
map. Letting a resolved entity reach Twig is how `book.author.name` in a loop becomes an
N+1 that appears in no PHP file.

`#[Route('/books', name: 'book_')]` on the class plus `name: 'index'` on the action
gives the route name `book_index`. Rejected alternative: one invokable class per action.
It reads well in isolation and badly in aggregate — the shared prefix, the shared
dependencies and the shared security rules get copied into every file, and a resource's
surface is no longer visible in one place.

### What never goes in a controller

| Found in a controller | Where it belongs | Why |
|---|---|---|
| `if` on a business condition | a service | The rule needs a unit test, not an HTTP request |
| `EntityManagerInterface`, `flush()` | a service (which calls the repository) | `flush()` is one call per use case, owned by the service |
| `QueryBuilder`, DQL, `findBy` with criteria | a repository method named after the intent | Rule 3; deptrac enforces it when adopted. See `symfony-yoandev-doctrine` |
| An entity in a JSON response **or a template** | an output DTO in `src/Dto/Output/` | An entity is a mapping, not an API contract; it leaks on every column you add, and lazy-loads from inside rendering |
| `$request->request->get('title')` | an input DTO + `#[MapRequestPayload]` | Untyped, unvalidated, invisible to PHPStan |
| `try { … } catch (\Throwable)` around a service call | `#[WithHttpStatus]` on the exception | The status belongs to the exception, once, not to every caller |
| A `<script>` or a business rule in the template | a Stimulus controller (see `symfony-yoandev-frontend`) | |

An action that is more than about ten lines is almost always holding something that
belongs elsewhere.

## Routing

Attributes only, on the action. Three things earn their keep:

- **`requirements:`** — `['id' => '\d+']` stops `/books/new` from matching `/books/{id}`
  and turns a junk id into a clean 404. Symfony 8.1 also coerces and validates typed
  route parameters before calling the controller (a non-numeric value for an `int $id`
  becomes a 404); on 6.4–8.0 the same request raises a `TypeError` and returns 500, so
  the requirement is what protects you.
- **`methods:`** — an action that only handles POST should say so, otherwise a GET
  reaches it and fails somewhere less obvious.
- **`priority:`** — only when two patterns genuinely overlap. Needing it usually means a
  requirement is missing.

**JSON routes are prefixed `api_` and live in a separate controller from their HTML
equivalent.** `BookController` and `ApiBookController`: same resource, same service, two
translations. They diverge in everything the framework treats differently — response
format, error rendering, statelessness, authentication, caching — and merging them ends
in `if ($request->getPreferredFormat() === 'json')` in every action.

## Getting the request in

Never read `$request` by hand when an attribute can do it. The attribute types the
value, validates it, and turns a bad request into a proper status code before your code
runs.

```php
#[Route('/reviews', name: 'create', methods: ['POST'])]
public function create(#[MapRequestPayload] CreateReviewInput $input): Response
```

| Attribute | Reads | Since | Failure status |
|---|---|---|---|
| `#[MapRequestPayload]` | body (JSON, XML, form) → DTO | 6.3 | 422 |
| `#[MapQueryString]` | whole query string → DTO | 6.3 | **404** |
| `#[MapQueryParameter]` | one query parameter | 6.3 | **404** |
| `#[MapRequestHeader]` | one header | 8.1 | 400 |
| `#[MapUploadedFile]` | one uploaded file | 7.1 | 422 |
| `#[MapEntity]` | an entity by something other than its id | 6.2 | 404 |

The 404 defaults surprise people: an invalid `?page=abc` reads as "no such page", which
is defensible for an HTML listing and wrong for an API. Pass
`validationFailedStatusCode: 422` on API routes.

Input DTOs live in `src/Dto/Input/` and carry the validation constraints. **Not every
action has one:** a GET whose only input is a route parameter takes `int $id` and stops
there — the DTO exists for a payload or a query string that must be validated, and
`symfony-yoandev-standards` lists the other simplifications the rules allow. Details,
version fallbacks, uploaded files inside a DTO, variadic payloads, dynamic validation
groups, and why `#[MapEntity(expr:)]` is rejected: `references/input-mapping.md`.

## Getting the response out

The action returns data; an attribute decides the representation.

```php
#[Route('/books/{id}', name: 'api_book_show', methods: ['GET'], requirements: ['id' => '\d+'])]
#[Serialize]                                   // Symfony 8.1+
public function show(int $id): BookView        // an output DTO, never an entity
{
    return $this->shelf->book($id);
}
```

```php
#[Route('/books/new', name: 'book_new', methods: ['GET', 'POST'])]
#[Template('book/new.html.twig')]
public function new(Request $request): array|Response
{
    // array → rendered; Response → returned as-is
}
```

`array|Response` is the whole idiom: `#[Template]` renders the array, and a redirect
short-circuits it because Symfony only dispatches the view event when the controller
did not return a `Response`.

Two behaviours verified in
`vendor/symfony/twig-bridge/EventListener/TemplateAttributeListener.php`: a
`FormInterface` in the returned array is converted to a `FormView` for you (pass `$form`,
not `$form->createView()`), and if that form is submitted and invalid the status becomes
**422** — what Turbo needs to re-render the page with its errors instead of ignoring the
reply.

Output DTOs live in `src/Dto/Output/`. `#[Serialize]`, serializer attributes, the list
envelope and the float trap below: `references/json-api.md`.

## The float trap

`json_encode(4.0)` produces `4`. A client that parsed `averageRating` as a float
yesterday gets an integer today, purely because the average landed on a round number.
Verified against this vendor tree:

```
new JsonResponse(['average' => 4.0])   {"average":4}
$this->json($dto)                      {"average":4}     ← forces the JsonResponse flags
#[Serialize] on the action             {"average":4.0}   ← JsonEncode preserves it
```

`AbstractController::json()` overrides the serializer's context with
`JsonResponse::DEFAULT_ENCODING_OPTIONS`, which omits `JSON_PRESERVE_ZERO_FRACTION`.
`#[Serialize]` passes only its own context, so the default survives. Two fixes, in
`references/json-api.md`.

## Errors

API errors are RFC 7807 Problem Details. Symfony's `ProblemNormalizer` already produces
the `type` / `title` / `status` / `detail` body, with a `violations` list for validation
failures — but a client sending `Accept: application/problem+json` gets an **HTML error
page**, because no encoder is registered for the `problem` format and the error renderer
silently falls back. A six-line encoder fixes it, ready to copy:
**`assets/ProblemJsonEncoder.php` → `src/Serializer/`**. The reasoning is in
`references/json-api.md`.

Business exceptions carry their own status:

```php
#[WithHttpStatus(409)]
final class ShelfIsFull extends \RuntimeException
{
}
```

Thrown anywhere, it becomes a 409 with no `catch` in the controller and no kernel
listener. It is inherited by subclasses, and ignored if the exception already implements
`HttpExceptionInterface`.

## Where this skill stops: API Platform

Everything above builds a JSON API by hand — input DTOs, `#[Serialize]`, Problem Details,
the pagination envelope. That is deliberate and it works well for a handful of endpoints
you control end to end.

It stops being the right call at a point worth naming, because past it you are
reimplementing [API Platform](https://api-platform.com) badly. **Redirect to it when any
of these is true:**

- the API has more than a handful of resources, each needing list, filter, sort and
  paginate — you would be writing the same four things again per resource;
- it is consumed by clients you do not control, or by generated clients;
- **you need a documented contract** — OpenAPI, a schema, anything a consumer can read.
  This suite has no answer for that, and needing one is itself the signal;
- you need several formats, or content negotiation beyond JSON;
- filtering and sorting are becoming a query language.

API Platform gives all of it natively, including RFC 7807 errors — the encoder this
skill ships exists precisely because the hand-written path does not get them for free.

**This suite does not cover API Platform.** It is a different stack, not a library you
add: it brings its own resource model, its own pagination shape (Hydra by default, not
the `items` + `meta` envelope decided here), its own filters. Adopting it overrides
several decisions made here, and that is fine — it is the right trade at that scale.

Say so plainly rather than quietly building a worse version. And do not mix the two on
one project: two ways of exposing a resource is worse than either.

## Forms

A FormType lives in `src/Form/`, and its `data_class` is an **input DTO, never an
entity**. Binding a form to an entity means the request writes to a managed object before
anything validates it, and any `flush()` in the same request persists it.

Three rules with the same root — the FormType describes fields, nothing else: **no
buttons** (they belong to the template, which knows the context), **no constraints**
(they are on the DTO, which is also what `#[MapRequestPayload]` validates — one source of
truth for both entry points), and **one action renders and processes**, GET and POST on
the same route.

That last rule has one extra branch worth knowing: an action can answer the POST with a
**Turbo Stream** (`$request->setRequestFormat(TurboBundle::STREAM_FORMAT)`, then render)
when the submission has to refresh several disjoint zones instead of navigating — keeping
the 422 on the invalid path and a 303 fallback for requests that did not ask for a
stream. `references/forms-and-twig.md` has it; **`symfony-yoandev-frontend` arbitrates** whether
the interaction should be a stream response, a Live Component or a pushed stream.

`empty_data`, readonly DTOs, `#[UniqueEntity]` on the input DTO, `#[IsCsrfTokenValid]`
and the Twig conventions: `references/forms-and-twig.md`.

## When it does not do what you expect

| Symptom | Cause |
|---|---|
| 500 instead of 404 on a bad `{id}` | Missing `requirements: ['id' => '\d+']` (and Symfony < 8.1) |
| 404 on an invalid query parameter | The default for `#[MapQueryString]` / `#[MapQueryParameter]`; set `validationFailedStatusCode: 422` |
| 415 Unsupported Media Type on POST | No `Content-Type` on the request, so `#[MapRequestPayload]` cannot pick a format |
| The DTO argument is `null` | The body was empty and the argument is nullable or has a default; use `mapWhenEmpty: true` |
| `Could not resolve the "$x" controller argument` | The argument is untyped |
| An HTML error page on an API route | `Accept: application/problem+json` with no encoder for the `problem` format |
| `4.0` serialised as `4` | `$this->json()` or `JsonResponse`; use `#[Serialize]` or pass the flag |
| The form is always invalid, no message | Constraints are on the entity, not on the DTO the form is bound to |
| `#[UniqueEntity]` never fires | It is on the entity; it must be on the validated input DTO |
| Form submits but the DTO is unchanged | The DTO is readonly with no `empty_data` callable |
| `#[IsGranted]` seems to run after mapping | It does not — gate attributes run first, by design |

## Reference files

| File | When to read it |
|---|---|
| `references/input-mapping.md` | Mapping anything from the request: payloads, query strings, headers, uploads, entities, validation groups |
| `references/json-api.md` | Writing or fixing a JSON endpoint: `#[Serialize]`, serializer attributes, floats, Problem Details, list envelopes |
| `references/forms-and-twig.md` | Building a form, answering a submission with a Turbo Stream, or writing/restructuring templates |
| `assets/ProblemJsonEncoder.php` | Copy to `src/Serializer/` on any project exposing a JSON API — without it, `Accept: application/problem+json` returns HTML |

Adjacent skills: `symfony-yoandev-doctrine` (entities, repositories, queries), `symfony-yoandev-security`
(authentication, voters, `#[IsGranted]`), `symfony-yoandev-frontend` (Stimulus, Turbo, Twig
components), `symfony-yoandev-performance` (when `#[Cache]` is justified), `symfony-yoandev-testing`, and
`symfony-yoandev-storage` — this skill stops at the valid `UploadedFile`; where it is written,
how it is served back and what deletes it are that skill's.
