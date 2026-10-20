# GraphQL API Design

## Summary

**One-sentence:** Design GraphQL schemas (SDL first) where every mutation returns a typed MutationNamePayload with userErrors and authorization lives in directives.

**One-paragraph:** Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed `MutationNamePayload { data, userErrors }`. Authorization is declared as schema directives (e.g. @auth(scope: ADMIN)); resolvers do not embed authorization checks ad-hoc. Naming conventions are nailed down (Connection/Edge for paginated lists, Input for mutation arguments, Result-shape unions for errors). Output is the schema spec + auth model + naming guide.

**Ефективно для:**

- Authoring or refactoring GraphQL schemas where shape consistency matters.
- Aligning multiple teams on naming and mutation patterns.
- Designing authorization that survives schema growth.
- Documenting decisions before implementation lands.

## Applies If (ALL must hold)

- GraphQL is the chosen protocol (see graphql-api).
- Schema spans multiple aggregates (>=5 types with relations).
- Mutations are non-trivial (validation, partial-success cases).
- Authorization beyond 'logged in' is needed (per-resource scopes).

## Skip If (ANY kills it)

- Schema is a thin facade over one resource — design overhead exceeds value.
- Authorization is one global flag (logged in / not) — directives are over-engineering.
- Protocol is REST or gRPC — this methodology does not apply.
- Schema is consumer-defined (federation subgraph generated from clients).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model: aggregates + relations + lifecycle states | doc or ERD | tech-lead |
| Mutation list: create/update/delete per aggregate + custom verbs | table | tech-lead |
| Authorization model: scopes, roles, ownership rules | policy | security |
| Naming policy: Connection/Edge, Input, Payload, error union shape | ADR | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[graphql-api]] | Implementation conventions for resolvers + DataLoader. |
| [[api-versioning]] | Schema diff gates align with this design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (mutation payload type, userErrors array, auth via directives, naming conventions, no scalar primitives for IDs) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for GraphQL design spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: aggregates → types → mutations → auth model → naming check | 800 |
| `content/05-examples.xml` | essential | Worked example: Payment mutation with userErrors + @auth | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `type_modeling` | opus | Aggregate-to-type mapping needs deep synthesis. |
| `mutation_payload_design` | sonnet | Mechanical payload type emission with userErrors. |
| `auth_directive_set` | opus | Authorization model encoded as directives. |
| `naming_audit` | sonnet | Walk types, enforce naming convention. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | Reference SDL with Payload + userErrors + @auth directives |
| `templates/dataloader.py` | DataLoader factory for Python servers (Ariadne/Strawberry) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api-design.py` | Validate GraphQL design spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[graphql-api]]
- [[api-versioning]]
- [[rest-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps schema complexity, authorization needs, and mutation shape to a rule from `01-core-rules.xml`, telling the agent whether to apply the design rules or skip when the schema is too small for the conventions. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/schema.graphql`

```graphql
scalar DateTime
scalar UUID
scalar Email

interface Node { id: ID! }
interface Timestamped { createdAt: DateTime!  updatedAt: DateTime! }

enum UserRole { ADMIN  MODERATOR  MEMBER }
enum OrderStatus { DRAFT  PLACED  PAID  SHIPPED  DELIVERED  CANCELLED }

type User implements Node & Timestamped {
  id: ID!
  email: Email!
  name: String!
  role: UserRole!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
  orders(first: Int, after: String, status: OrderStatus): OrderConnection!
}

type Order implements Node & Timestamped {
  id: ID!
  status: OrderStatus!
  items: [OrderItem!]!
  totalAmount: Float!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OrderItem {
  id: ID!
  quantity: Int!
  unitPrice: Float!
  totalPrice: Float!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge { node: Order!  cursor: String! }

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input CreateUserInput { email: Email!  name: String!  role: UserRole }
input UpdateUserInput { email: Email  name: String  role: UserRole }

type CreateUserPayload { user: User  errors: [Error!]! }
type UpdateUserPayload { user: User  errors: [Error!]! }
type Error { field: String  message: String!  code: String! }

type Query {
  user(id: ID!): User
  users(first: Int, after: String): OrderConnection!
  me: User
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  orderStatusChanged(orderId: ID!): Order!
}
```

### `templates/dataloader.py`

```python
"""
Strawberry DataLoader batch functions.
Input: list of keys (UUIDs)
Output: list of entities in same order as keys (None for missing)
"""
from strawberry.dataloader import DataLoader
from typing import List
from uuid import UUID


class OrganizationLoader(DataLoader[UUID, "Organization"]):
    async def batch_load_fn(self, keys: List[UUID]) -> List["Organization"]:
        organizations = await self.repository.find_by_ids(keys)
        org_map = {org.id: org for org in organizations}
        # CRITICAL: return in same order as keys; None for missing
        return [org_map.get(key) for key in keys]


class UserLoader(DataLoader[UUID, "User"]):
    async def batch_load_fn(self, keys: List[UUID]) -> List["User"]:
        users = await self.repository.find_by_ids(keys)
        user_map = {u.id: u for u in users}
        return [user_map.get(key) for key in keys]


# 1:N grouping: orders keyed by user_id
class OrdersByUserLoader(DataLoader[UUID, List["Order"]]):
    async def batch_load_fn(self, user_ids: List[UUID]) -> List[List["Order"]]:
        orders = await self.repository.find_by_user_ids(user_ids)
        grouped: dict[UUID, list] = {uid: [] for uid in user_ids}
        for order in orders:
            grouped[order.user_id].append(order)
        return [grouped[uid] for uid in user_ids]


# Context factory — call once per request, never at module level
def create_loaders(repository_factory) -> dict:
    return {
        "organization": OrganizationLoader(repository_factory.organization),
        "user": UserLoader(repository_factory.user),
        "orders_by_user": OrdersByUserLoader(repository_factory.order),
    }
```
