---
name: design-patterns
description: >
  Expert guide to GoF (Gang of Four) design patterns based on "Dive Into Design Patterns" by Alexander Shvets.
  Use this skill whenever the user asks about design patterns, OOP principles, SOLID, software architecture,
  or code structure decisions. Trigger for questions like: "how do I implement X pattern", "which pattern
  should I use for Y problem", "explain Factory/Observer/Strategy/etc.", "what's the difference between X
  and Y pattern", "how to apply SOLID", "how to structure this code", "my classes are too coupled",
  "I need to add behavior at runtime", "how to avoid a telescoping constructor", or any question where
  the answer involves object-oriented design. Also trigger when reviewing code for design smells like
  tight coupling, god classes, or switch-case proliferation.
---

# Design Patterns Skill

Based on: *Dive Into Design Patterns* by Alexander Shvets (Refactoring.Guru, 2019)

## Core OOP Pillars (Quick Reference)

| Pillar | Definition |
|--------|-----------|
| **Abstraction** | Model only the attributes/behaviors relevant to the current context — ignore the rest |
| **Encapsulation** | Hide implementation details behind a public interface; protect internals from the outside |
| **Inheritance** | Build new classes on top of existing ones; subclasses inherit state and behavior |
| **Polymorphism** | A program detects the real class of an object at runtime and calls its actual implementation |

**Object Relations (weakest → strongest):**
- **Dependency** — object uses another temporarily (method param / return)
- **Association** — object has a permanent link to another (field)
- **Aggregation** — "has-a" but component can exist independently
- **Composition** — "whole-part"; component only exists inside the container

---

## Software Design Principles

### The Three Core Principles
1. **Encapsulate What Varies** — Identify what changes; isolate it so changes don't ripple everywhere
2. **Program to an Interface, not an Implementation** — Depend on abstractions, not concrete classes
3. **Favor Composition over Inheritance** — Compose behaviors at runtime rather than baking them in via subclasses

### SOLID
See `references/solid.md` for detailed examples and checklist.

| Letter | Principle | One-liner |
|--------|-----------|-----------|
| **S** | Single Responsibility | A class has just one reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subclasses must be substitutable for their superclass |
| **I** | Interface Segregation | Don't force clients to depend on methods they don't use |
| **D** | Dependency Inversion | High-level and low-level modules both depend on abstractions |

---

## Pattern Catalog Overview

Patterns split into three families:

| Family | Purpose | Patterns |
|--------|---------|---------|
| **Creational** | Object creation mechanisms | Factory Method, Abstract Factory, Builder, Prototype, Singleton |
| **Structural** | Assembling objects into larger structures | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **Behavioral** | Communication & responsibility between objects | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor |

**For detailed pattern references, see:**
- `references/creational.md`
- `references/structural.md`
- `references/behavioral.md`

---

## Pattern Selection Guide

Use this when the user describes a problem and needs to pick a pattern:

### "I need to create objects but…"
| Problem | Pattern |
|---------|---------|
| Don't know type until runtime / want subclasses to decide | **Factory Method** |
| Need families of related objects | **Abstract Factory** |
| Constructor has too many params / need step-by-step construction | **Builder** |
| Need to copy complex objects | **Prototype** |
| Need exactly one instance globally | **Singleton** |

### "I need to structure classes but…"
| Problem | Pattern |
|---------|---------|
| Interfaces are incompatible / working with legacy code | **Adapter** |
| Class has multiple independent dimensions of variation | **Bridge** |
| Need to treat individual objects and trees of objects uniformly | **Composite** |
| Need to add behavior to objects at runtime without subclassing | **Decorator** |
| Subsystem is too complex; need a simple entry point | **Facade** |
| Huge number of similar fine-grained objects eating RAM | **Flyweight** |
| Need lazy init, access control, logging, caching around a real object | **Proxy** |

### "I need objects to communicate/behave but…"
| Problem | Pattern |
|---------|---------|
| Requests should pass through a chain of handlers | **Chain of Responsibility** |
| Need to parameterize objects with operations / support undo | **Command** |
| Need to traverse a collection without exposing its structure | **Iterator** |
| Objects are too tightly coupled to each other | **Mediator** |
| Need to save/restore object state (undo/snapshot) | **Memento** |
| Objects need to be notified when another object changes | **Observer** |
| Object behavior depends on state and changes at runtime | **State** |
| Need to switch algorithms/behaviors at runtime | **Strategy** |
| Subclasses should fill in the blanks of an algorithm skeleton | **Template Method** |
| Need to add operations to objects without modifying their classes | **Visitor** |

---

## How to Present a Pattern

When explaining any pattern, always cover:
1. **Intent** — one-sentence definition
2. **Problem** — the design pain it solves
3. **Solution** — the structural approach
4. **Structure** — the roles (Creator, Product, etc.) and how they relate
5. **When to use (Applicability)**
6. **Pros & Cons**
7. **Code example** (use user's language; pseudocode is fine if unknown)
8. **Relations** — similar/complementary patterns to mention

---

## Common Anti-Patterns & Pattern Remedies

| Smell | Remedy |
|-------|--------|
| God class doing too many things | Apply **SRP** + split into collaborators |
| `new ConcreteClass()` hardcoded everywhere | **Factory Method** or **Abstract Factory** |
| Deeply nested if/switch on type | **Strategy** or **State** |
| Subclass explosion (one class per feature combination) | **Decorator** or **Bridge** |
| Global mutable state | **Singleton** (carefully) or dependency injection |
| Tight coupling between subsystems | **Facade** or **Mediator** |
| Duplicate code in similar algorithms | **Template Method** |
| UI button/menu logic scattered | **Command** (for undo queues too) |
| Observers manually wired everywhere | **Observer** / event bus |
| Hard to test because of rigid dependencies | **Dependency Inversion** + interfaces |