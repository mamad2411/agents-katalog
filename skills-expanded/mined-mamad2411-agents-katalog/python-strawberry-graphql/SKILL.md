---
name: python-strawberry-graphql
description: Use when building GraphQL APIs with Strawberry — code-first schema, Django integration, N+1 avoidance, subscriptions, federation note.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-django, python-essentials, python-testing, graphql-essentials, security]
---

# Strawberry GraphQL

**Iron Law: code-first — Python types ARE the schema; never hand-write SDL. Every resolver that touches a related object MUST use a DataLoader (or `select_related`/`prefetch_related` upstream). One unbatched FK in a list query = N+1 across the entire response.**

**Versions:** Current `0.245.x` · `strawberry-graphql-django` `0.50.x` — _Strawberry is fast-moving (weekly releases) — pin in `pyproject.toml`. Code-first means the schema is generated from your Python types via `@strawberry.type`; export SDL for codegen on the client side with `strawberry export-schema`._

## When Strawberry beats Graphene

Strawberry uses native type hints throughout, has first-class async resolvers, ships Federation 2 + subscriptions out of the box, and `strawberry-graphql-django` is more actively maintained than `graphene-django`. Pydantic v2 conversion is built in via `strawberry.experimental.pydantic`. Graphene is still common in legacy code; for new code, **Strawberry is the default**.

## Code-first schema

```python
import strawberry
from typing import Annotated

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    full_name: str | None = None

@strawberry.type
class Order:
    id: strawberry.ID
    sku: str
    qty: int
    user: "User"                                          # forward ref OK

@strawberry.type
class Query:
    @strawberry.field
    async def order(self, id: strawberry.ID) -> Order | None:
        return await Order.objects.aget(pk=id)

    @strawberry.field
    async def orders(self, info: strawberry.Info) -> list[Order]:
        # Always eager-load FKs you know the resolver chain will hit
        return [o async for o in Order.objects.select_related("user").aiterator()]

schema = strawberry.Schema(query=Query)
```

Use `strawberry.ID` (not `str`) for identifiers — surfaces as `ID` in SDL, matches GraphQL spec. Use `strawberry.lazy("yourapp.types")` for circular references across modules.

## Django integration — `strawberry-graphql-django`

```python
# urls.py
from strawberry.django.views import AsyncGraphQLView
urlpatterns = [
    path("graphql/", AsyncGraphQLView.as_view(schema=schema, graphql_ide="graphiql")),
]
# Disable graphql_ide in production: graphql_ide=None
```

```python
import strawberry_django
from .models import Order as OrderModel

@strawberry_django.type(OrderModel, fields=["id", "sku", "qty", "user"])
class Order:
    pass                                                  # type maps from Django model

@strawberry_django.type(OrderModel)
class OrderWithCustom:
    id: strawberry.ID
    sku: str
    qty: int
    @strawberry_django.field(only=["user__email"])        # tells optimizer what to fetch
    def user_email(self, root: OrderModel) -> str:
        return root.user.email
```

The `strawberry-django` `DjangoOptimizerExtension` analyzes the query AST and rewrites your `QuerySet` with `select_related`/`prefetch_related` automatically. **Enable it in `Schema(extensions=[DjangoOptimizerExtension])`** — without it, the manual `select_related` calls in every resolver are your only N+1 defense.

## DataLoader — the N+1 killer

Even with the optimizer, custom resolvers that escape the ORM (calling external APIs, denormalized lookups) need explicit batching:

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User | None]:
    users = {u.id: u for u in await User.objects.filter(id__in=keys).aall()}
    return [users.get(k) for k in keys]                   # preserve order

# Per-request loader (do NOT module-scope — leaks state across requests)
async def get_context(request) -> dict:
    return {"user_loader": DataLoader(load_fn=load_users)}

@strawberry.field
async def author(self, info: strawberry.Info) -> User | None:
    return await info.context["user_loader"].load(self.author_id)
```

**One DataLoader per request, not per server.** Module-scoped loaders cache across requests → stale data + memory leak. Pass via `context` (per-request) or via `info.context` factory in your view.

## Permissions

```python
import strawberry
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "auth required"
    async def has_permission(self, source, info, **kwargs) -> bool:
        return info.context["request"].user.is_authenticated

@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def cancel_order(self, info, id: strawberry.ID) -> Order:
        ...
```

**Field-level authz is the GraphQL way.** Don't gate at the schema root — different fields have different visibility (`User.email` is public, `User.internal_notes` is staff-only). Apply `permission_classes` per `@strawberry.field` / `@strawberry.mutation` (and pair with row-level filtering inside the resolver).

## Subscriptions

```python
import asyncio
import strawberry

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def order_updates(self, order_id: strawberry.ID) -> AsyncGenerator[Order, None]:
        async for order in pubsub.subscribe(f"order:{order_id}"):
            yield order
```

Requires an ASGI server (`uvicorn`/`daphne`) and a pub/sub backbone (Redis, Postgres LISTEN/NOTIFY, channels-layer). Wire it to your existing job-queue/notification layer rather than inventing a new transport.

## Federation — quick note

Strawberry supports Apollo Federation 2 (`@strawberry.federation.type(keys=["id"])`). **Don't reach for federation unless multiple teams own separate subgraphs.** Single-service apps are simpler as a monolithic schema. Re-evaluate at 3+ services with overlapping types.

## Pagination — Relay-style connections

```python
@strawberry.type
class Query:
    @strawberry_django.connection(strawberry_django.relay.ListConnection[Order])
    async def orders(self) -> list[Order]:
        return Order.objects.all()                        # the connection wraps with edges/pageInfo/cursor
```

Cursor pagination (encoded `{id, sort_key}` cursor) is the Relay default and matches what most GraphQL clients expect. Don't roll your own offset pagination — clients (Apollo, urql, Relay) all support cursor by default.

## Schema export for codegen

`strawberry export-schema myproject.schema:schema > schema.graphql`. Run in CI; fail if `schema.graphql` differs from the committed copy. Frontend codegen (Apollo CLI, graphql-codegen) consumes this. Treat SDL like OpenAPI: PR-reviewed, lockstep with releases.

## Query depth / complexity limits

Public GraphQL endpoints are DOS targets — deeply nested `{ users { friends { friends ... } } }` fans out exponentially.

```python
from strawberry.extensions import QueryDepthLimiter, MaxAliasesLimiter
schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        MaxAliasesLimiter(max_alias_count=15),
        DjangoOptimizerExtension,
    ],
)
```

Add a complexity budget (`strawberry-graphql-django` has `ComplexityExtension`) for production. Combine with per-user rate limiting upstream.

## Anti-patterns

- Custom resolvers calling `.filter()` per-row without a DataLoader — N+1 across the response
- Module-scoped DataLoader — cross-request cache poisoning + memory leak
- Skipping `DjangoOptimizerExtension` and trusting manual `select_related` — one missed resolver degrades the whole query
- Hand-writing SDL alongside `@strawberry.type` — duplication that drifts
- `graphql_ide` enabled in production — introspection leaks your entire API surface
- Permissions stacked at the schema root — apply per-field
- Returning `None` for "not found" without explicit `Order | None` — clients can't tell error from missing
- No depth/complexity limit — first malicious client takes down the DB
- Subscriptions over plain HTTP — fails behind a 60s proxy timeout; use WebSocket transport
- Storing user-scoped data on `info.context` without per-request init — stale state

## Hand-off

For GraphQL fundamentals (DataLoader theory, federation, field-level authz, cursor pagination): `Skill(devkit:graphql-essentials)`. For Django ORM/migrations the resolvers sit on top of: `Skill(devkit:python-django)`. For testing patterns (async pytest, factory_boy): `Skill(devkit:python-testing)`. For authn/authz patterns feeding `permission_classes`: `Skill(devkit:security)`.
