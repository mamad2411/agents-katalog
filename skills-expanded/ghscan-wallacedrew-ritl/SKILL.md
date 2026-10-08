---
name: encapsulate-record
description: Apply Encapsulate Record when you see Data Class, Primitive Obsession. The record is a class with accessors; the agent reasons about its shape, invariants, and behavior in one definition.
---

# Apply: 53 — Encapsulate Record

**Announce first:** name the smell you see and that you're applying Encapsulate Record before any edit. The user reads the announcement as your contract.

**Or decline first:** if you don't apply Encapsulate Record, name the decline type — catalog miss, taste call, cost-benefit, constraint-blocked, or insufficient context — so the user knows which counterargument applies.

**Symptom:** A plain object passed across the codebase; the agent reading any consumer must inspect every other consumer to learn what shape the record actually has.

**Goal:** The record is a class with accessors; the agent reasons about its shape, invariants, and behavior in one definition.

```js
// Avoid:
const org = { name: 'Acme', country: 'US' };
console.log(org.name);

// Prefer:
class Org {
  constructor({ name, country }) { this._name = name; this._country = country; }
  name()    { return this._name; }
  country() { return this._country; }
}
console.log(new Org(org).name());
```

**Pressure:** Field changes ripple through every consumer; the agent must coordinate updates and verify each consumer respects the (implicit) contract.

**Tradeoff:** Wrapping every record adds construction ceremony at every entry; for records without invariants or behavior to attract, the agent gains nothing for the per-call cost.

**Relief:** Field accesses run through named methods; a field rename touches one class definition without changing any caller, and invariants enforced in those methods catch invalid combinations the field-level access would otherwise let through.

**Trap:** Wrapping records on principle without invariants or behavior to add creates classes the agent must instantiate everywhere with no encapsulation gain.

**Removes smells:** Data Class, Primitive Obsession
