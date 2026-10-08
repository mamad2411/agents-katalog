# Savings Analysis Skill

## Goal

Calculate realistic potential savings from verified pricing information.

## Rules

Arithmetic must be performed by deterministic application code.

LLMs may interpret pricing structures but should not be the source of final arithmetic.

## Calculations

Monthly:

current_monthly_cost - alternative_monthly_cost

Annual:

monthly_saving * 12

When billing frequencies differ, normalize them before comparison.

## Conditions

Only calculate savings when:

* current cost is known
* alternative cost is verified
* billing periods are comparable

Otherwise return:

`Savings cannot be reliably calculated.`

## Language

Use:

* potential saving
* estimated saving
* verified price difference

Never use:

* guaranteed saving
* guaranteed refund

unless objectively guaranteed by documented policy.
