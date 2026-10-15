---
name: bloodhound-antipatterns
description: >
  Sniffs out code smells (refactoring.guru catalog) and software anti-patterns
  (design, OO, programming, methodological, configuration). Names the stink,
  prescribes the fix, points to docs. Covers 22 smells + ~50 anti-patterns.
  Use when reviewing code, refactoring, doing PR review, cleaning technical debt,
  or designing architecture. Load alongside coding-guide for code changes.
---

# Bloodhound: Code Smell & Anti-Pattern Detector

**Workflow ("The Sniff"):**

1. **DETECT** — scan code for signals (see REFERENCE.md)
2. **NAME** — identify the exact smell or anti-pattern by canonical name
3. **FIX** — apply the linked refactoring technique or solution strategy

## Quick Reference

### Code Smells (refactoring.guru)

| Category | Smells |
|---|---|
| **Bloaters** | Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps |
| **OO Abusers** | Switch Statements, Temporary Field, Refused Bequest, Alternative Classes with Different Interfaces |
| **Change Preventers** | Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies |
| **Dispensables** | Comments, Duplicate Code, Lazy Class, Data Class, Dead Code, Speculative Generality |
| **Couplers** | Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man |

### Anti-Patterns

| Category | Patterns |
|---|---|
| **Software Design** | Big Ball of Mud, Abstraction Inversion, Ambiguous Viewpoint, Database-as-IPC, Inner-Platform Effect, Input Kludge, Interface Bloat, Magic Pushbutton, Stovepipe System, Race Hazard |
| **Object-Oriented** | God Object, Anemic Domain Model, Call Super, Circular Dependency, Constant Interface, Object Orgy, Poltergeist, Sequential Coupling, Yo-Yo Problem, Circle-Ellipse Problem, Object Cesspool |
| **Programming** | Spaghetti Code, Lasagna Code, Lava Flow, Boat Anchor, Cargo Cult Programming, Hard Code, Magic Numbers, Magic Strings, Error Hiding, Accidental Complexity, Action at a Distance, Busy Waiting, Caching Failure, Coding by Exception, Loop-Switch Sequence, Repeating Yourself, Shooting the Messenger, Shotgun Surgery, Soft Code |
| **Methodological** | Copy-Paste Programming, Golden Hammer, Not Invented Here, Invented Here, Premature Optimization, Programming by Permutation, Reinventing the Square Wheel, Silver Bullet, Tester-Driven Development |
| **Configuration** | Dependency Hell, DLL Hell, Extension Conflict, JAR Hell |

---

Full catalog with signals, consequences, fixes, and examples:

See [REFERENCE.md](REFERENCE.md)