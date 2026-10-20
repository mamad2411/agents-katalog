---
name: clean-soc
description: Use when writing, fixing, editing, or refactoring code where responsibilities are mixed, functions or classes do too much, or concerns overlap in any programming language. Enforces the Single Responsibility Principle and separation of concerns—one reason to change per module.
---

# Clean SoC

## When to Use

Use this skill when writing, fixing, editing, or refactoring code in any programming language.

Also trigger on: functions doing UI + business logic + I/O together, god classes, services that also validate and persist and send email, controllers with business rules, mixed levels of abstraction in one function, or asks like "this function does too much", "split this up", "separate concerns".

## Instructions

### S1: One Reason to Change

Each function, class, or module should have exactly one responsibility—one actor or reason that would cause it to change. If you can name two different things it does, split it.

```text
# Bad - three reasons to change
function processOrder(order):
  validateStock(order)            # inventory rules
  saveToDatabase(order)           # persistence
  sendConfirmationEmail(order)    # notifications

# Good - three modules, each with one reason
function validateOrder(order): ...
function persistOrder(order): ...
function notifyCustomer(order): ...
```

### S2: One Level of Abstraction per Function

A function should read at a single level of abstraction. Mixing high-level intent with low-level implementation forces readers to context-switch.

```text
# Bad - mixed abstraction
function renderDashboard(metrics):
  header = "<html><head><style>" + buildStyles(theme) + "</style></head>"
  data = query("SELECT * FROM metrics WHERE date = '" + today + "'")
  return header + "<h1>Dashboard</h1>" + formatRows(data)

# Good - high-level steps
function renderDashboard(metrics):
  page = buildPage()
  data = loadMetrics()
  return page.render(data)
```

### S3: Separate Input, Processing, Output

Push I/O to the edges. Pure processing in the middle is testable and reusable; I/O at the edges is easy to swap.

```text
# Bad - parsing, computing, and rendering fused
function report(rows):
  parsed = [parse(r) for r in rows]
  totals = [sum(r.items) for r in parsed]
  printTable(totals)

# Good - separated
function parseRows(rows): ...
function computeTotals(parsed): ...
function renderTable(totals): ...
```

### S4: Split God Objects

When a class accumulates unrelated responsibilities (state, formatting, persistence, logging), extract cohesive groups into their own classes and compose them.

```text
# Bad - god class
class OrderService:
  method validate(order): ...
  method save(order): ...
  method toXml(order): ...
  method email(order): ...
  method log(order): ...

# Good - composed responsibilities
class OrderValidator: ...
class OrderRepository: ...
class OrderFormatter: ...
class OrderNotifier: ...
class OrderService:  # composes the above
```

### S5: Keep Related Changes Together (Cohesion)

Separating concerns does not mean scattering. Code that changes together should live together—a business rule and its data shape belong in the same module, not spread across layers. Cohesion is the counterweight to separation.

```text
# Bad - rule separated from its data
// orders.js
if order.total > 100: discount = 0.1   # rule
// user.js
const order = { total: 120 }           # data

# Good - rule and shape co-located
// order.js
class Order:
  fields: total
  method discountRate():
    return 0.1 if this.total > 100 else 0
```

### Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| S1 | One reason to change | Split validate / persist / notify |
| S2 | One abstraction level | High-level steps, not inline SQL + HTML |
| S3 | Input / processing / output | Parse, compute, render as separate steps |
| S4 | Split god objects | Extract validator, repository, formatter |
| S5 | Keep related changes together | Rule and its data co-located |