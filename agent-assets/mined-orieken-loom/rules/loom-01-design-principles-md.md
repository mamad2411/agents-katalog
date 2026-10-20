# Design Principles

## 1. Simple Design (Kent Beck)
In priority order:
1. **Passes the tests**: If it doesn't work, nothing else matters.
2. **Reveals intention**: Code should explain *why* it exists.
   *Example*: `const isEligibleForDiscount = user.age > 65;` instead of `if (user.age > 65)`.
3. **No duplication**: DRY — Don't Repeat Yourself.
4. **Fewest elements**: Once the above are met, remove anything unneeded.

## 2. Refactoring Operations (Martin Fowler)
1. **Extract Function**: Code block is too long or intent is unclear.
2. **Inline Function**: Function body is as clear as its name.
3. **Extract Variable**: Expression is too complex to read.
4. **Rename Variable**: Name doesn't reveal intention.
5. **Move Method/Field**: Feature Envy — method uses fields of another class more than its own.
6. **Replace Conditional with Polymorphism**: Repeated `switch/if` statements checking the same type codes.
7. **Introduce Parameter Object**: Data Clumps — parameters always travel together.
8. **Remove Dead Code**: Code is no longer reachable.
9. **Separate Query from Modifier**: A method both returns a value and changes state.
10. **Preserve Whole Object**: Passing 5 fields from an object instead of the object itself.

## 3. Sandi Metz Hard Limits
- Classes $\le$ 100 lines.
- Methods $\le$ 5 lines (10 ceiling for exceptional cases).
- Max 4 parameters per method.
- No more than one dot per line (except chained fluent interfaces like `array.map().filter()`).

## 4. The Boy Scout Rule
**Leave the camp better than you found it.**
If you touch a file that has structural issues, complexity $\ge$ 7, or functions $>$ 25 lines, extract and clean them up *within the same commit*. Do not leave messes for the next person.

## 5. Naming Standards
- **Intention-Revealing Names**: Stop using `process`, `handle`, `manage`, `data`, `info`. Be specific.
- **Boolean Prefixes**: Booleans must start with `is`, `has`, `can`, or `should`.
- **No Abbreviations**: `calculateTotal` not `calcTot`.

## 6. Ubiquitous Language (Eric Evans)
All class names, variable names, and domain concepts MUST match the terms exactly as defined in `DOMAIN_DICTIONARY.md`.

## 7. Anti-Pattern Radar
- **Distributed Monolith**: Microservices that communicate synchronously and break together. The same shape
  can appear at the team level — see `TEAM_TOPOLOGY.md` and the `team-topology-check` skill for a
  Conway's-Law-flavored version of this check.
- **Anemic Domain Model**: Domain entities have only getters/setters; all logic is in "Service" classes.
- **God Object**: A class that knows too much or does too much.
- **Shotgun Surgery**: Making a simple change requires editing many different files.
- **Leaky Abstraction**: A generic-sounding interface that forces callers to understand its implementation details.
- **Premature Generalization**: Building an abstract framework for a use case that might "one day" exist.

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
