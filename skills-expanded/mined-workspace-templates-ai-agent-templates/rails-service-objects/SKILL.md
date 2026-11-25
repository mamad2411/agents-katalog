---
name: rails-service-objects
description: Extracts business logic out of fat Rails controllers and models into small service and query objects, with specs that prove behavior stays the same.
---

# Rails service objects

Extract only when it makes a flow easier to test. Do not wrap a one-line `save` in a class.

## Steps

1. Pick one fat action or callback. Read it with its model, routes and existing specs. Write the list of side effects it performs, in order.
2. If no spec covers it, write a request spec or model spec for the current behavior first and run it green.
3. Create `app/services/<verb>_<noun>.rb`, for example `PlaceOrder`. One public method, `call`, plus a class method `self.call(...)` that delegates to it. Pass plain arguments, not the controller or params object.
4. Return a result object (`Result.new(success?, record, errors)`) instead of raising for expected failures. Raise only for bugs.
5. Move callbacks that cause side effects (mail, webhooks, charges) into the service. Keep validations and data integrity in the model.
6. For a growing chain of `where` and `joins`, create a query object in `app/queries` that takes a relation and returns a relation, so it can be chained.
7. The controller now parses params, calls the service, and renders by result.

## Rules

- Wrap multi-record writes in `ActiveRecord::Base.transaction` and enqueue jobs after commit.
- Never let a service call another service through a hidden global; pass collaborators as arguments.
- Services must not render, redirect or read `current_user` implicitly.
- Run `bundle exec rspec` after every extraction.

## Report

Name each new class, the lines removed from the old location, and the spec that proves behavior is unchanged.
