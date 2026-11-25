---
name: grpc-service-design
description: Designs protobuf services with evolution-safe fields, proper status codes and deadlines, then checks changes with buf for breaking compatibility.
---

# gRPC service design

Write the proto as if two versions will talk to each other for a year.

## Steps

1. Model one RPC per use case with its own request and response message, even when the response is a single field: `GetOrderRequest` and `GetOrderResponse`. Never reuse a request message across methods, because it ties their futures together.
2. Number fields once and never change or reuse them. When removing a field, add `reserved 4; reserved "old_name";`. Use field numbers 1 to 15 for fields that are set often.
3. Add enums with a zero value named `X_UNSPECIFIED`. Use wrapper types or `optional` when you must tell unset from zero.
4. Use `google.protobuf.Timestamp` and `Duration` for time; money as integer minor units with a currency string; never floats for money.
5. For lists, use page tokens: `page_size` and `page_token` in, `next_page_token` out.
6. Return status codes deliberately: `INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`, `PERMISSION_DENIED`, `UNAUTHENTICATED`, `RESOURCE_EXHAUSTED`, `UNAVAILABLE` for retryable faults. Attach details with `errdetails` for field violations.
7. In Go, every client call takes a `context.WithTimeout`; servers pass `ctx` to every downstream call so deadlines propagate and cancelled calls stop work.
8. Run `buf lint` and `buf breaking --against .git#branch=main` before you finish.

## Rules

- Never change a field's type or number in a released message.
- Never use `UNKNOWN` or `INTERNAL` for errors the caller caused.
- Never block a handler without checking `ctx.Done()`.

## Report

The proto diff, status code mapping, deadline defaults and buf results.
