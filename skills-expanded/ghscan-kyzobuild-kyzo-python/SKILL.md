---
name: python-state-success
description: Build the two live-node constructs — consistency model and binding — the only places mutable state and transport clients are allowed to converge. Fires before holding a socket, database, bus, or client; before declaring a mutable field; before writing a manager, an engine, or a second unfrozen model in a context; or before writing a connect/setup/wiring class.
---

# State

The live-node constructs: where mutable state and transport clients are allowed to exist at all. Everything in `python-values-success` is frozen; the consistency model is the one deliberate exception, and the binding is what wires clients into it.

## Consistency Model

### Definition

The single unfrozen `BaseModel` of a context, the one node where live clients and mutable state converge. Every state it holds is a proven fact, and state evolution is a field re-pointing to a newer proven value.

### Required Form

```python
PositionState = Annotated[Position | Flat, Field(discriminator="kind")]


class PositionConsistencyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    bus: BusClient
    ledger: LedgerClient
    latest: PositionState

    def book(self, report: VenueFill) -> None:
        self.latest = Position(prior=self.latest, fill=report)
        self.bus.publish(self.latest)
        self.ledger.append(self.latest)
```

`PositionState` is the state union: `Position` and `Flat` are the concept models declared in their own sections, each carrying the same-named `exposure` derivation, so exposure reads off `latest` with no branch. Clients are fields, state fields are declared types, and every method is a verb. `arbitrary_types_allowed` is legal on this class and nowhere else.

### Sorting Rules

A second unfrozen model means the context is two contexts: stop and report it. Client binding belongs to the binding; the consistency model receives constructed clients as fields. A fact the state implies is a derivation on the state's model, not a method here. A frozen domain composite is a concept model.

### Replaced Forms

A manager or engine is domain logic with a technology name and no proof obligation. A module-level client is the live edge escaped from the one node that may hold it. A second unfrozen model is a second convergence point for state, which is two contexts fused into one.

### Construct-Specific Doctrine

State evolution is reassignment of proofs, never mutation of their contents: construct the newer proven fact and re-point the field to it. The consistency model never holds an unproven value, not even for one statement. Every non-client field is a declared type; no bare primitives, no `T | None`, no `bool` gates. Selection never happens here: construction selected the variant, the checker narrows it, and what differs by variant is read from the union value.

### Allowed Patterns

- one unfrozen `BaseModel` per context with `arbitrary_types_allowed=True`, clients as fields
- every non-client field a declared type holding a proven value
- state evolution by re-pointing a field to a newly constructed fact
- verbs as the only methods

### Forbidden

- a second unfrozen model in one context
- a module-level client
- `match`, `if`/`elif`, or `isinstance` anywhere in the class
- a hand-assembled dict where a constructed type belongs
- an unproven or unmodeled value held in any field
- `arbitrary_types_allowed` on any other class

### Halt Rule

Halt when a context needs a second unfrozen model, when a client no verb reaches is demanded, or when a state field has no declared row. Report the row and the field or client: the context is mis-factored or the meaning is unmodeled, and the table is not finished.

## Binding

### Definition

The class whose `connect` method binds transport clients to the consistency model. Its entire meaning is the binding it performs: it owns no domain type, holds no domain logic, and makes no domain decision.

### Required Form

```python
class PositionBinding:
    def connect(self, bus: BusClient, ledger: LedgerClient, opening: PositionState) -> PositionConsistencyModel:
        return PositionConsistencyModel(bus=bus, ledger=ledger, latest=opening)
```

### Sorting Rules

Domain state and domain transitions belong to the consistency model; the binding only constructs it. Client instantiation and configuration belong to the composition root; the binding receives constructed clients. Transport ingress belongs to the route; the binding handles no request.

### Replaced Forms

A repository is a fetch surface given a class name; consumers read facts the consistency model's transitions establish. A computing service is domain logic that escaped the consistency model. A manager is sequencing the construction graph already owns.

### Construct-Specific Doctrine

`connect` may perform transport setup whose signal has no domain meaning: connection, authentication, subscription, and the idempotent create-or-bind that binds the same client either way. If the domain reacts to a transport signal, the signal is modeled through the ordered union (`python-adapters-success`), never caught here.

### Allowed Patterns

- one class whose `connect` accepts constructed transport clients and any opening state, and returns the constructed consistency model
- connection, authentication, and subscription setup inside `connect`

### Forbidden

- a method that computes a domain fact
- a catch that converts a transport signal into a domain answer
- a domain type defined in the binding's file
- a repository, manager, or computing service

### Halt Rule

Halt when `connect` would need a domain decision, a domain computation, or a catch the domain reacts to. Report the row and the signal as a modeling gap: the meaning belongs in the consistency model or the ordered union, and the table is not finished.
