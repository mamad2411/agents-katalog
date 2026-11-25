---
name: graphql-schema-design
description: Designs a GraphQL schema around the product domain, with honest nullability, input types and mutation payloads that report errors as data.
---

# GraphQL schema design

Design for the client's question, not the table's columns.

## Steps

1. List the screens or use cases the schema serves. Write each as the query a client would send. Model types so those queries are one request.
2. Name by domain meaning (`Order`, `LineItem`), never by table. Use `ID!` for identity. Keep scalars honest: custom `DateTime`, `Money` (amount plus currency, never a float).
3. Decide nullability per field. Non-null only when the server can always produce it. A field that depends on a flaky downstream service must be nullable, because an error on a non-null field nulls the parent.
4. Lists: use connections (`edges`, `node`, `pageInfo`, `first`/`after`) for anything that can grow. Never return an unbounded list.
5. Mutations: one input type and one payload type each, for example `createOrder(input: CreateOrderInput!): CreateOrderPayload!`. The payload holds the changed object and `userErrors: [UserError!]!` with `field` and `message`. Reserve top-level errors for bugs and auth failures.
6. Use enums for closed sets, and unions or interfaces for real polymorphism. Add descriptions to every type and field that is not obvious.
7. Evolve additively. Mark old fields `@deprecated(reason: "...")` and remove them only after usage drops to zero.
8. Lint with graphql-eslint or the schema checker your team uses, and run a client query against the result.

## Rules

- Never expose internal ids, join tables or foreign keys as fields.
- Never add a boolean flag argument where two fields would be clearer.

## Report

The schema in SDL, nullability decisions that were close calls, and the queries you tested.
