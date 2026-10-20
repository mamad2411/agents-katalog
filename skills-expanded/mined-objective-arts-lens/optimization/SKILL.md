---
name: optimization
description: "Performance optimization"
allowed-tools: []
---

# Carmack: Functional Core, Performance Shell

John Carmack's core belief: **Loaded loaded loaded. Every cycle counts, but only after you understand what you're doing.** Write code that's easy to reason about, then optimize the hell out of it.

## The Foundational Principle

> "If you want to do something really well, you have to understand it deeply. You can't just learn the API."

Don't just use libraries and frameworks. Understand what they're doing at the machine level. The programmers who make breakthroughs are the ones who understand the whole stack.

---

## Functional Thinking

Carmack famously advocated for functional programming principles in C++:

### Pure Functions

> "No matter what language you work in, programming in a functional style provides benefits. You should do it whenever it is convenient, and you should think hard about the decision when it isn't convenient."

**Not this:**
```c
int globalCounter = 0;

void processItem(Item* item) {
    item->value = compute(item->value);
    globalCounter++;  // Side effect
    log(item);        // Side effect
}
```

**This:**
```c
Item processItem(Item item) {
    return (Item){
        .value = compute(item.value),
        .processed = true
    };
}

// Side effects at the edges
int main() {
    Item result = processItem(input);
    counter++;
    log(result);
}
```

### Benefits of Purity

1. **Easy to test** - No setup, no mocking, no state
2. **Easy to reason about** - Output depends only on input
3. **Parallelizable** - No shared mutable state
4. **Cacheable** - Same input always gives same output

### Const Correctness

Use `const` aggressively. If it doesn't need to change, mark it const:

```c
const char* getMessage(const Config* config) {
    // Can't accidentally modify config
    return config->message;
}
```

Carmack: "Use const everywhere you possibly can."

---

## Deep Optimization

When performance matters (games, graphics, systems), optimize methodically:

### Understand the Hardware

> "I can't stress this enough: understand what the machine is doing."

Know:
- **Cache behavior** - L1/L2/L3 sizes, cache line size
- **Branch prediction** - How mispredicts cost cycles
- **Memory access patterns** - Sequential vs. random
- **SIMD opportunities** - Vector operations

### Data-Oriented Design

Carmack moved toward data-oriented design in later work:

**Not this (Array of Structures):**
```c
struct Entity {
    Vector3 position;
    Vector3 velocity;
    int health;
    char name[32];
    Texture* sprite;
    // ... more fields
};
Entity entities[1000];

// Process positions - cache misses everywhere
for (int i = 0; i < 1000; i++) {
    entities[i].position += entities[i].velocity;
}
```

**This (Structure of Arrays):**
```c
struct Entities {
    Vector3 positions[1000];
    Vector3 velocities[1000];
    int health[1000];
    // ... arrays for each property
};

// Process positions - cache-friendly sequential access
for (int i = 0; i < 1000; i++) {
    positions[i] += velocities[i];
}
```

### Measure, Don't Guess

> "The first rule of optimization is: measure."

Profile before optimizing. The bottleneck is never where you think.

---

## Static Analysis

Carmack became a strong advocate for static analysis:

> "Anything that can be done by static analysis to catch a bug before it happens is a win."

Use every tool available:
- **Compiler warnings**: Enable all warnings, treat as errors (`-Wall -Werror`)
- **Static analyzers**: Coverity, PVS-Studio, clang-analyzer
- **Sanitizers**: ASan, UBSan, TSan
- **Formal methods**: Where critical

### The Cost of Bugs

> "The cost of fixing a bug goes up by an order of magnitude at every stage: design, code, test, ship."

Catch bugs at compile time. Then at startup. Then in tests. Never in production.

---

## Code Style

From Carmack's practices and .plan files:

### Locality of Behavior

Keep related code together. Don't spread logic across files for "organization":

```c
// Prefer: All player physics in one place, even if long
void UpdatePlayer(Player* p) {
    // Movement
    p->velocity += gravity * dt;
    p->position += p->velocity * dt;

    // Collision
    if (CheckCollision(p->position)) {
        ResolveCollision(p);
    }

    // Animation
    UpdateAnimation(p, p->velocity);
}
```

### Avoid Premature Abstraction

> "Premature abstraction is just as bad as premature optimization."

Don't create class hierarchies until you have three concrete examples. Don't add parameters until you need them.

**Not this:**
```cpp
class AbstractEntityFactory {
    virtual Entity* create(const EntityParams& params) = 0;
};

class ConcretePlayerFactory : public AbstractEntityFactory {
    // ... 200 lines later, creates a Player
};
```

**This:**
```cpp
Player* createPlayer(int x, int y) {
    return new Player(x, y);
}
```

### Comments for Future Self

Carmack's code has strategic comments explaining *why*, especially for non-obvious optimizations:

```c
// OPTIMIZATION: Using integer math here because the FPU pipeline
// would stall waiting for the divide. Measured 15% faster on target
// hardware (Pentium 166).
int approxDist = (dx > dy) ? dx + (dy >> 1) : dy + (dx >> 1);
```

---

## The Carmack Test

Before committing code, ask:

1. **Is this function pure?** If not, can I make it pure?
2. **Is const used everywhere possible?** Could any parameter or return be const?
3. **Do I understand the hardware impact?** Cache behavior, branch prediction, memory access?
4. **Have I measured before optimizing?** Or am I guessing?
5. **Is this the simplest solution?** Or am I abstracting prematurely?
6. **Would static analysis catch any bugs?** Have I run the tools?
7. **Could this be tested in isolation?** Without mocking half the system?

---

## When Reviewing Code

Apply these checks:

- [ ] Functions are as pure as possible (side effects at edges)
- [ ] const used aggressively
- [ ] No premature abstraction (concrete before abstract)
- [ ] Data layout considered for cache behavior (if performance-critical)
- [ ] Optimizations are measured, not assumed
- [ ] Compiler warnings enabled and clean
- [ ] Static analysis tools would pass
- [ ] Complex optimizations are commented with *why*
- [ ] Code locality is preserved (related logic together)

---

## When NOT to Use This Skill

Use a different skill when:
- **Writing Linux kernel code** → Use `data-first` (kernel style, data structures, taste)
- **Writing Go code** → Use `simplicity` (Go Proverbs, interface design)
- **Writing application code** → Use `clarity` (general clarity, readability)
- **Building distributed systems** → Use `distributed` (statelessness, fault tolerance)
- **Performance isn't measured yet** → Measure first. Carmack says: "Don't optimize without data."

Carmack is the **performance-critical skill**—use it when profiling has identified bottlenecks or you're writing game/graphics/real-time code.

## Sources

- Carmack, ".plan" files (1990s-2000s, archived at github.com/ESWAT/john-carmack-plan-archive)
- Carmack, "Functional Programming in C++" (QuakeCon 2013)
- Carmack, Various GDC talks and keynotes
- Carmack, Twitter/X threads on programming practices
- Masters of Doom (Kushner, 2003) - historical context

---

*"Focused, hard work is the real key to success. Keep your eyes on the goal, and just keep taking the next step towards completing it."* — John Carmack
