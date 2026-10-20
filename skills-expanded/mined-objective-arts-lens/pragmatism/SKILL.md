---
name: pragmatism
description: "Pragmatic systems philosophy"
allowed-tools: []
---

# Thompson: When in Doubt, Use Brute Force

Ken Thompson's core belief: **Get it working first. Optimize only if you must.** The elegant solution that doesn't exist is worse than the ugly one that ships.

## The Foundational Principle

> "One of my most productive days was throwing away 1000 lines of code."

Simplicity isn't about writing less code—it's about having less code that matters. Delete ruthlessly. Rewrite when the old approach is fighting you.

---

## Thompson's Rules

### Rule 1: When in Doubt, Use Brute Force

Don't be clever when simple works. A linear scan that's easy to verify beats a complex algorithm that might have bugs.

**Not this:**
```go
// Clever hash-based deduplication with bloom filter pre-check
func dedupe(items []string) []string {
    bloom := newBloomFilter(len(items))
    seen := make(map[uint64]bool)
    // ... 50 lines of clever code
}
```

**This:**
```go
// Brute force: O(n²) but obviously correct
func dedupe(items []string) []string {
    var result []string
    for _, item := range items {
        found := false
        for _, r := range result {
            if r == item {
                found = true
                break
            }
        }
        if !found {
            result = append(result, item)
        }
    }
    return result
}
// When n > 1000, then optimize
```

### Rule 2: Build the Simplest Thing That Could Possibly Work

Don't design for hypothetical futures. Build what you need now. Refactor when requirements change.

**Not this:**
```go
// Anticipating every possible future requirement
type MessageBus interface {
    Publish(topic string, msg Message) error
    Subscribe(topic string, handler Handler) error
    Unsubscribe(topic string, handler Handler) error
    PublishAsync(topic string, msg Message) <-chan error
    SubscribeWithFilter(topic string, filter Filter, handler Handler) error
    // ... 20 more methods for hypothetical use cases
}
```

**This:**
```go
// What we actually need today
type Notifier struct {
    handlers []func(event Event)
}

func (n *Notifier) Notify(e Event) {
    for _, h := range n.handlers {
        h(e)
    }
}
```

### Rule 3: Prototype in the Language of Least Resistance

Use whatever gets you to working code fastest. Rewrite in the "proper" language only after you understand the problem.

Thompson wrote the first Unix in assembly, then rewrote in C once the design was clear. He prototyped in interpreted languages when exploring ideas.

### Rule 4: Trust the Compiler, But Verify

> "I've never been a fan of debugging. I'd rather spend my time writing code that doesn't need debugging."

Write code so simple that bugs have nowhere to hide. When you do debug, add a test so that bug can never return.

### Rule 5: Delete Code Mercilessly

Every line of code is a liability. It must be maintained, understood, and can contain bugs. The best code is no code.

**Ask yourself:**
- Is this feature actually used?
- Could this function be deleted if I changed the caller?
- Is this abstraction earning its complexity?

---

## Unix Philosophy (Thompson's Interpretation)

### Small Sharp Tools

Each program does one thing. Combining them does everything.

**Not this:**
```bash
# Monolithic tool that does everything
supertool --parse-logs --filter-errors --count --format-json input.log
```

**This:**
```bash
# Composition of simple tools
cat input.log | grep ERROR | wc -l
```

### Text as Universal Interface

Text streams connect everything. Binary formats create silos.

**Not this:**
```go
// Custom binary protocol
func encode(data *Record) []byte {
    buf := make([]byte, 256)
    binary.BigEndian.PutUint32(buf[0:4], data.ID)
    // ... complex encoding
}
```

**This:**
```go
// Text-based, debuggable, pipeable
func encode(data *Record) string {
    return fmt.Sprintf("%d\t%s\t%s", data.ID, data.Name, data.Value)
}
```

### Fail Early, Fail Loud

When something goes wrong, stop immediately. Don't try to recover and continue with corrupt state.

**Not this:**
```go
func process(items []Item) []Result {
    var results []Result
    for _, item := range items {
        result, err := transform(item)
        if err != nil {
            // Silently skip bad items
            continue
        }
        results = append(results, result)
    }
    return results
}
```

**This:**
```go
func process(items []Item) ([]Result, error) {
    var results []Result
    for i, item := range items {
        result, err := transform(item)
        if err != nil {
            return nil, fmt.Errorf("item %d: %w", i, err)
        }
        results = append(results, result)
    }
    return results, nil
}
```

---

## Regular Expressions (Thompson's Gift)

Thompson invented the regex implementation used everywhere today. His approach: convert regex to NFA, run in linear time.

### Keep Patterns Simple

**Not this:**
```regex
^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

**This:**
```go
// Separate checks are clearer and more maintainable
func validPassword(s string) bool {
    if len(s) < 8 { return false }
    hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(s)
    hasLower := regexp.MustCompile(`[a-z]`).MatchString(s)
    hasDigit := regexp.MustCompile(`\d`).MatchString(s)
    return hasUpper && hasLower && hasDigit
}
```

---

## Trusting Trust (Security Lesson)

Thompson's 1984 Turing Award lecture revealed you can't fully trust code you didn't write—compilers can hide backdoors invisible in source code.

### Implications for Developers

1. **Minimize dependencies** — Each dependency is code you're trusting
2. **Audit what matters** — Focus security review on authentication, authorization, data handling
3. **Simplicity aids security** — Complex code hides bugs and backdoors
4. **Defense in depth** — Don't trust any single layer

---

## The Thompson Test

Before committing code, ask:

1. **Could brute force work here?** If yes, use it until proven too slow.
2. **Is this the simplest thing that works?** Not the most elegant—the simplest.
3. **Could I delete this?** Code that doesn't exist can't break.
4. **Will this fail loudly?** Silent failures are the worst failures.
5. **Is this text-based where possible?** Text is debuggable and composable.
6. **Am I building for today or a hypothetical future?**

---

## When Reviewing Code

Apply these checks:

- [ ] No premature cleverness (brute force rejected with evidence?)
- [ ] Minimal code (could anything be deleted?)
- [ ] Text interfaces where possible (not unnecessary binary formats)
- [ ] Errors fail fast and loud (no silent continuation)
- [ ] No speculative features (built for actual requirements?)
- [ ] Dependencies justified (each one is trusted code)
- [ ] Simple enough to verify by inspection

---

## Thompson vs Pike

Both emphasize simplicity, but:

| Aspect | Thompson | Pike |
|--------|----------|------|
| Primary focus | Get it working | Get it right |
| On cleverness | Brute force first | Clear over clever |
| On optimization | Only when proven needed | Measure first |
| On prototyping | Prototype fast, rewrite | Design carefully upfront |
| On deletion | Delete aggressively | Simplify through design |

Use **Thompson** when: exploring a problem, prototyping, uncertain about requirements.
Use **Pike** when: building production systems, designing APIs, writing Go.

---

## When NOT to Use This Skill

Use a different skill when:
- **Designing public APIs** → Use `simplicity` or `java` (API design needs more upfront thought)
- **Performance-critical code** → Use `optimization` (brute force won't cut it)
- **Writing production Go** → Use `simplicity` (Go idioms and proverbs)
- **Security-sensitive code** → Use `security-mindset` (security needs paranoid thinking)

Thompson is the **pragmatist's skill**—for getting things working, prototyping, and cutting through complexity.

---

## Sources

- Thompson, "Reflections on Trusting Trust" (Turing Award Lecture, 1984)
- Thompson & Ritchie, "The UNIX Time-Sharing System" (Bell System Technical Journal, 1978)
- Kernighan & Pike interviews with Thompson
- Thompson interviews on Go design decisions
- Coders at Work (Peter Seibel interview with Thompson)

---

*"When in doubt, use brute force."* — Ken Thompson
