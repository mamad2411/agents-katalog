---
name: clean-code
description: >-
  Use when a clean/*, purity/* or language/* rule is reported, or when asked to clean,
  simplify, rename or make code more readable: business names, small functions, stepdown
  order, comments only for what code cannot say, no escape hatches, Clock, IdGenerator.
allowed-tools:
  - Read
  - Edit
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit explain *)
  - Bash(npm run lint *)
---

# Clean code

The checker holds these rules (`npx ddd-ts-kit check`); this skill says how to satisfy them
without fighting them. Reference: `docs/ARCHITECTURE.md` section 6.

## Names

- Take the word from the context's glossary (`CONTEXT.md`). If it is not there, the concept
  is not understood yet: add the term with its meaning first (skill `ddd-ts-kit:glossary`), or ask.
- Class: a noun of the domain. Method: what the business says happens (`order.cancel(reason)`),
  never `setStatus`, `update`, `process`, `handle`, `manage`, `doX`.
- No `Manager`, `Helper`, `Util`, `Data`, `Info`, `Processor`, `Wrapper`, `Impl`, `Base`,
  `Abstract`, `Dto`, `Entity`, `Model` in a name of the domain or of a use case
  (`language/no-technical-name`). A technical suffix is allowed only where it names the architectural role outside the
  domain (`OrderRepository`, `PlaceOrderHandler`), or where the business itself says the word:
  a term of the glossary holds it (`Scoring model` lets `ScoringModel` through, `Copy of data`
  lets `CopyOfData` through). Add that row only when a domain expert uses the term, never to
  silence the rule; without it the generator and the checker refuse the name.
- A variable, a parameter, a property, a destructured name and a loop variable name the concept
  they hold, from the glossary: `const appointment = await this.appointmentRepository.findById(id)`,
  `for (const reminder of due)`. Never `target`, `data`, `item`, `obj`, `info`, `element`, `tmp`
  and the like in `domain/` and `application/` (`naming/business-name`): they hide which concept a
  line handles. `npx eslint --fix` renames a binding built by `X.create(..)`, `new X(..)` or read
  from a repository; rename a loop variable and the others yourself, after the message.
- One word per concept in a context: not `fetch` here and `retrieve` there.
- A boolean reads as a predicate (`isOverdue`), a collection as a plural, a function that
  answers as a question, a function that acts as a verb.
- A refusal reads as a sentence: `throw SlotTaken.forCalendar(calendar.id, slot.startsAt)`, a
  class named after what is refused, in terms of the glossary and the qualifiers `invalid`,
  `unknown`, `already`, `too`, `no`, `missing`, `required` (`BookingTooLate`), never `...Error`, and a static factory named after what the
  refusal is about, `for`, `with`, `because`, `on` or `at` then a capital letter (`forCalendar`,
  `withNotice`, `becauseOf`). The class reads its code from the closed list of its context,
  `readonly code = SchedulingCodes.SlotTaken` in `<context>.codes.ts`. Never
  `new SlotTaken(...)`, never a factory named `create` or `slotTaken` (`errors/through-factory`,
  `errors/factory-name`, `errors/code-listed`). Add one with
  `npx ddd-ts-kit generate error <context> <Refusal> <factory>`. Under
  `"stack.refusals": "factories"`, the factory sits on the error class of the concept and its code
  says the same words: `AppointmentError.slotTaken(..)` sets `SLOT_TAKEN`.
- No magic string: a status, a kind, a role is a vocabulary declared once
  (`npx ddd-ts-kit generate vocabulary <context> <Name> --value <value>...`, an object `as const`
  and its union type) and read by its key, `AppointmentStatus.NoShow`; a permission is read from
  its set, `billingPermissions['invoice.issue']`, never by its id (`language/declared-vocabulary`).
  A word of another language that spells the same string stays its word, typed by it outside
  `domain/`: `Record<ProductListedV1Payload['state'], InvoiceStatus>`, `'issued' satisfies TheirType`.
- No magic number in `domain/` and `application/`: 0, 1, -1 and an index only; a duration, a
  limit or a rate is a constant of the module, `const MINUTES_PER_HOUR = 60;`, or a value object
  of the business (`clean/no-magic-number`). Both rules hold under `"stack.literals": "named"`,
  which `init` writes; a project whose config does not say keeps them silent.
- A domain event declares its name once, `static readonly eventName = '<context>.<aggregate>.<fact>'`,
  and its `readonly name` reads it (`events/name-declared-once`); a reaction reads it too, `@DomainEventHandler(InvoiceIssued)`, and an integration event handler reads
  the type it handles from the contract, `invoiceIssuedV1.type`.

## Functions

- One thing, one level of abstraction. If a blank line separates "steps", each step is a
  function whose name replaces the comment you were about to write.
- Three parameters at most. More means a missing value object or command.
- A function of `domain/` that answers a plain object of data, `({ amount, currency })`, is a value
  object written as a function: make it a class, `npx ddd-ts-kit generate value-object <context> <Name>`,
  with its rules in the static factory and its operations as methods (`domain/value-object-class`,
  under `"stack.values": "classes"`, which `init` writes). A function that answers value objects
  it builds, a record derived by a spread, a specification and a state machine stay functions; a
  decision answered as `{ kind: 'refused', reason }` is a refusal thrown by a factory.
- No boolean parameter: `publish(draft)` and `schedule(draft, date)`, not `publish(draft, true)`.
- Either changes state or returns an answer.
- Guard clauses first, happy path unindented. No `else` after a `return` or `throw`.

## Order of a file: stepdown

Read top to bottom like an article: what, then how.

```ts
export class Invoice extends AggregateRoot {
  static issue(...)            // 1. factories
  static rehydrate(...)
  pay(payment: Payment)        // 2. public intentions, most important first
  cancel(reason: Reason)
  private assertPayable()      // 3. each private helper below its first caller
  private remainingAmount()
}
```

In a module: the exported function first, then its helpers in call order. Constants and types
a reader needs to understand the first function go above it; everything else below.

## Comments

Default: none. Clear code with good names is the documentation. Write a comment only when it
carries what the code cannot:

| Keep | Example |
|---|---|
| why a non-obvious choice | `// Rounded per line, not on the total: required by the tax authority (art. 242)` |
| a warning | `// Order matters: the outbox append must share the transaction of the save` |
| an external reference | RFC, law, vendor bug link |
| the contract of a public API or port | what a method guarantees, units, error raised |

Delete: paraphrases of the next line, banners, section dividers, closing-brace labels,
change history, author, commented-out code, `@param id the id`. If a block needs a comment to
say what it does, extract it and name it.

## Testable by construction

- Time: inject `Clock`, never `new Date()` or `Date.now()` in domain or application. Pass
  `clock.now()` into the aggregate method; aggregates do not hold a clock.
- Identifiers: `IdGenerator`.
- Anything outside the process: a port in `application/ports/`, with a fake.
- Dependencies by constructor, as ports (abstract classes). No singleton import, no static
  state, no `process.env` outside `src/platform/config/`.

## Files and layout

One exported class, interface or function per file, named after it in kebab-case; at most
350 lines, reached by extracting a responsibility (a value object, a domain service, a policy,
a file of its own), never by shortening or deleting a comment, a test or a written rule. A type or a function of the domain with no role directory is a concept not named
yet: its home is in the table "a concept with no role of its own" of `docs/ARCHITECTURE.md`,
never a `types/` or `utils/` folder. Members are `private`, never `#name`. A blank line before a
`return` that is not alone in its block and around `if`, `for`, `try`. Every `if`, `else`, `for`, `while` and `do`
has braces and its body on its own lines, never `if (a) return b;`: a branch is visible at a
glance, and a statement added to it later cannot silently fall outside it. `npm run format`
(Biome, line width 120), then `npm run lint:fix`, settle layout: do not spend tokens on it. A
blank line the lint asks for after the formatter wrapped a long line is expected, and the
second command adds it. With `"formatOnWrite": true` in `ddd-ts-kit.config.json`, the guard runs the project's Biome on each file as it is written (not under the regulated profile). Never Prettier nor a bare `npx biome`: another width, or an unrelated
package of that name.

## Types

No `any` (use `unknown` and narrow), no `!`, no `as` outside mappers, no `@ts-ignore`. Model
alternatives as discriminated unions so that `switch` is exhaustive. Make invalid states
unrepresentable instead of validating them later.

## When a rule is reported

Fix the code, not the rule. Suppressing (`// ddd-ts-kit-disable-next-line <rule> -- reason`),
lowering a severity or raising a limit needs the owner's explicit agreement and a decision
record: skill `ddd-ts-kit:deviation`.
