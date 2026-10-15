---
name: domain-service
description: Identify and encapsulate domain logic that does not belong to any single aggregate into domain services. Use when an agent needs to create, modify, review, or interpret business logic that involves multiple aggregates and does not have a natural owner. A domain service contains pure domain logic — it receives and returns domain types, has no infrastructure dependencies, and does not access repositories, transactions, or external systems. The business-logic entry point orchestrates the domain service by loading the necessary aggregates and passing them in.
---

# Domain Service

## Goal

When domain logic involves multiple aggregates and does not naturally belong to any single one of them, encapsulate that logic in a domain service.

A domain service is a stateless operation expressed in domain terms that enforces business rules spanning multiple aggregates. It receives domain types as input, returns domain types as output, and has no dependencies on infrastructure — no repositories, no transactions, no external systems.

Domain logic that belongs to a single aggregate must stay on that aggregate — in the aggregate root or its child entities. A domain service is only appropriate when no single aggregate can own the logic.

The business-logic entry point (application service) is responsible for loading the aggregates from their repositories, passing them to the domain service, and persisting the results. The domain service never performs these orchestration tasks itself.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- implements domain logic that involves entities or data from multiple aggregates
- places cross-aggregate domain logic directly in a business-logic entry point instead of a domain service
- places cross-aggregate domain logic on one aggregate where it does not naturally belong
- introduces a new business rule that spans multiple aggregates

Do not apply this skill when:

- the logic involves only entities within the same aggregate — that logic belongs on the aggregate root
- the logic is pure orchestration — loading entities, calling save, managing transactions — that belongs in the entry point
- the logic is infrastructure-related — persistence, messaging, external API calls — that belongs in the infrastructure layer

## The Rule

1. Domain logic that spans multiple aggregates belongs in a domain service.
   - If a business rule requires data or entities from two or more aggregates to be evaluated, and no single aggregate can own that rule, create a domain service for it.
   - Do not force the logic onto one aggregate by passing the other aggregate's data as parameters to its methods — if the rule does not naturally belong to that aggregate, it should not be there.

2. A domain service has no infrastructure dependencies.
   - It does not access repositories.
   - It does not manage or participate in transactions.
   - It does not call external systems, APIs, or messaging infrastructure.
   - It receives everything it needs as parameters and returns the result.

3. A domain service operates exclusively on domain types.
   - Parameters must be domain entities, value objects, or domain primitives.
   - Return types must be domain entities, value objects, or domain primitives.
   - Do not pass persistence types, DTOs, or infrastructure types to a domain service.

4. A domain service is stateless.
   - It does not hold mutable state between calls.
   - Each invocation is independent — the result depends only on the inputs.

5. The entry point orchestrates the domain service.
   - The business-logic entry point loads the required aggregates from their repositories.
   - The entry point passes the aggregates or their relevant data to the domain service.
   - The entry point persists any changes returned by the domain service.
   - The domain service is never responsible for loading or persisting data.

6. Do not create a domain service for logic that belongs to a single aggregate.
   - If the logic can be expressed as a method on an aggregate root using only data within that aggregate, it belongs there.
   - A domain service is not a default location for domain logic — it is a specific tool for cross-aggregate rules.

## Detection Workflow

1. Identify domain logic in the code being created or reviewed.
   - Look for business rules, calculations, validations, or decisions that involve domain concepts.

2. Determine which aggregates are involved.
   - If the logic uses data or entities from a single aggregate, it belongs on that aggregate — not in a domain service.
   - If the logic uses data or entities from multiple aggregates, it is a candidate for a domain service.

3. Check where the logic currently lives.
   - If cross-aggregate logic is inside an entry point — mixed with orchestration — extract it into a domain service.
   - If cross-aggregate logic is forced onto one aggregate that does not naturally own it — move it to a domain service.
   - If the logic is already in a domain service, verify it has no infrastructure dependencies.

4. Verify the domain service has no infrastructure dependencies.
   - Check that it does not import or reference repositories, database clients, transaction managers, or external service clients.
   - Check that all inputs and outputs are domain types.

## Writing or Changing Domain Services

1. Identify the cross-aggregate rule.
   - State which aggregates are involved and what business rule spans them.
   - Confirm that no single aggregate can naturally own the rule.

2. Define the domain service as a function or stateless class.
   - Prefer a top-level function when the project conventions support it.
   - Use a stateless class when the project conventions favor it or when grouping related cross-aggregate operations.
   - Name the service after the domain concept it represents — not after a technical pattern.

3. Define parameters and return types using domain types only.
   - Accept the aggregates, entities, or value objects the rule needs.
   - Return the result as domain types — modified entities, value objects, or a domain result.

4. Wire the domain service in the entry point.
   - The entry point loads the necessary aggregates from repositories.
   - The entry point calls the domain service with the loaded data.
   - The entry point persists the result.

## Examples

Domain service for a transfer between two accounts (different aggregates):

```ts
// Domain service — pure domain logic, no infrastructure
const executeTransfer = (
  sourceAccount: Account,
  targetAccount: Account,
  amount: Money,
): { updatedSource: Account; updatedTarget: Account } => {
  if (!sourceAccount.hasSufficientFunds(amount)) {
    throw new InsufficientFundsError()
  }
  return {
    updatedSource: sourceAccount.debit(amount),
    updatedTarget: targetAccount.credit(amount),
  }
}

// Entry point orchestrates
const transferCommandHandler = (
  accountRepository: AccountRepository,
) => (command: TransferCommand) => {
  return withTransaction((transaction) => {
    const source = accountRepository.findById(transaction, command.sourceAccountId)
    const target = accountRepository.findById(transaction, command.targetAccountId)
    const { updatedSource, updatedTarget } = executeTransfer(source, target, command.amount)
    accountRepository.save(transaction, updatedSource)
    accountRepository.save(transaction, updatedTarget)
  })
}
```

```py
# Domain service — pure domain logic, no infrastructure
def execute_transfer(
    source_account: Account,
    target_account: Account,
    amount: Money,
) -> tuple[Account, Account]:
    if not source_account.has_sufficient_funds(amount):
        raise InsufficientFundsError()
    return (
        source_account.debit(amount),
        target_account.credit(amount),
    )

# Entry point orchestrates
def transfer_command_handler(
    account_repository: AccountRepository,
):
    def handler(command: TransferCommand):
        with transaction() as tx:
            source = account_repository.find_by_id(tx, command.source_account_id)
            target = account_repository.find_by_id(tx, command.target_account_id)
            updated_source, updated_target = execute_transfer(source, target, command.amount)
            account_repository.save(tx, updated_source)
            account_repository.save(tx, updated_target)
    return handler
```

```kt
// Domain service — pure domain logic, no infrastructure
fun executeTransfer(
    sourceAccount: Account,
    targetAccount: Account,
    amount: Money,
): Pair<Account, Account> {
    if (!sourceAccount.hasSufficientFunds(amount)) {
        throw InsufficientFundsError()
    }
    return Pair(
        sourceAccount.debit(amount),
        targetAccount.credit(amount),
    )
}

// Entry point orchestrates
fun transferCommandHandler(
    accountRepository: AccountRepository,
) = fun(command: TransferCommand) {
    withTransaction { tx ->
        val source = accountRepository.findById(tx, command.sourceAccountId)
        val target = accountRepository.findById(tx, command.targetAccountId)
        val (updatedSource, updatedTarget) = executeTransfer(source, target, command.amount)
        accountRepository.save(tx, updatedSource)
        accountRepository.save(tx, updatedTarget)
    }
}
```

Not this — cross-aggregate logic embedded in the entry point:

```ts
// Bad: domain logic mixed with orchestration in the entry point
const transferCommandHandler = (
  accountRepository: AccountRepository,
) => (command: TransferCommand) => {
  return withTransaction((transaction) => {
    const source = accountRepository.findById(transaction, command.sourceAccountId)
    const target = accountRepository.findById(transaction, command.targetAccountId)
    // Domain logic should not be here
    if (source.balance < command.amount) {
      throw new InsufficientFundsError()
    }
    const updatedSource = source.debit(command.amount)
    const updatedTarget = target.credit(command.amount)
    accountRepository.save(transaction, updatedSource)
    accountRepository.save(transaction, updatedTarget)
  })
}
```

Not this — cross-aggregate logic forced onto one aggregate:

```ts
// Bad: Account should not know about another Account's transfer logic
class Account {
  transferTo(targetAccount: Account, amount: Money): { source: Account; target: Account } {
    // This rule spans two aggregates — Account should not own it
  }
}
```

## Review Questions

When reading or reviewing code, ask:

- Does this logic involve entities or data from multiple aggregates?
- Is cross-aggregate domain logic placed directly in the entry point mixed with orchestration?
- Is cross-aggregate domain logic forced onto one aggregate that does not naturally own it?
- Does the domain service have any infrastructure dependencies — repositories, transactions, external systems?
- Does the domain service operate exclusively on domain types?
- Is the entry point responsible for loading aggregates, calling the domain service, and persisting the result?

If cross-aggregate domain logic exists outside a domain service, apply this skill.

## Report the Outcome

When finishing the task:

- state which cross-aggregate business rule was identified
- state which aggregates are involved
- state whether a domain service was created or already existed
- state that the domain service has no infrastructure dependencies
- state how the entry point orchestrates the domain service
