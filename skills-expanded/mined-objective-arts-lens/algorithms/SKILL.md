---
name: algorithms
description: "Literate programming"
allowed-tools: []
---

# Knuth: Programs as Literature

Donald Knuth's core belief: **Programs should be written for humans to read, and only incidentally for machines to execute.** Code is literature. Treat it as such.

## The Foundational Principle

> "Premature optimization is the root of all evil."

The full quote: "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%."

Don't optimize until you've measured. But when the 3% matters, optimize with precision.

---

## Literate Programming

Knuth invented literate programming with WEB (for Pascal) and CWEB (for C). The idea: write programs as essays that happen to be executable.

### The Principle

Code and documentation are not separate. They are one work, written for a human reader, that happens to also compile.

**Traditional approach:**
```c
// Calculate factorial
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Literate approach:**
```
@ The factorial function computes $n!$, the product of all positive
integers up to $n$. We use the recursive definition: $0! = 1$, and
$n! = n \cdot (n-1)!$ for $n > 0$.

This recursive formulation directly mirrors the mathematical definition,
making correctness verification straightforward.

@<Calculate factorial@>=
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

### Key Concepts

**Weaving**: Extract the documentation (produces a readable document)
**Tangling**: Extract the code (produces a compilable program)

The source is one file. Two outputs: one for humans, one for machines.

### Modern Application

You don't need WEB/CWEB. Apply the principle:

1. **Write for the reader** - Assume someone will read your code like a book
2. **Explain the why** - Not just what the code does, but why this approach
3. **Tell a story** - Code should have narrative flow
4. **Use meaningful names** - Variables and functions should read naturally

---

## Algorithmic Rigor

Knuth wrote *The Art of Computer Programming* to bring mathematical rigor to algorithms.

### Understand Complexity

Don't just know an algorithm works. Know:
- **Time complexity**: O(n), O(n log n), O(n²)...
- **Space complexity**: How much memory?
- **Constants matter**: O(n) with constant 1000 can be slower than O(n²) for small n
- **Best/worst/average**: Know all three cases

### Prove Correctness

For critical code, informal reasoning isn't enough:
- **Loop invariants**: What's true before/after each iteration?
- **Preconditions**: What must be true when function is called?
- **Postconditions**: What will be true when function returns?

**Example:**
```c
// Precondition: arr is sorted, 0 <= lo <= hi <= len(arr)
// Postcondition: returns index of target, or -1 if not found
// Invariant: if target exists, it's in arr[lo..hi]
int binary_search(int arr[], int lo, int hi, int target) {
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;  // Avoids overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

### Test Edge Cases

Knuth famously offers reward checks for errors in TAOCP. Be paranoid about edge cases:
- Empty input
- Single element
- Maximum/minimum values
- Overflow conditions
- Off-by-one errors

---

## The TeX Philosophy

Knuth wrote TeX because existing typesetting was inadequate. Principles from TeX:

### Quality Over Speed

TeX development took 10 years. The result: software that's been stable for decades.

> "I've spent my whole life trying to get something right. I don't want to waste time getting it almost right."

### Version Numbering

TeX versions converge to π (3.14159...). Each release adds one digit. The message: asymptotically approaching perfection, never claiming to be there.

### Stability

TeX has been frozen since 1989. No new features. Bug fixes only. The lesson: done can be better than evolving.

---

## Knuth's Rules

### On Optimization

1. **Don't optimize yet** - Get it working first
2. **Measure before optimizing** - Know where the time goes
3. **Optimize the right 3%** - Most code doesn't matter
4. **Know your algorithms** - The right algorithm beats micro-optimization

### On Correctness

1. **Prove it works** - Don't just test, reason about correctness
2. **Handle all cases** - Edge cases are where bugs hide
3. **Be paranoid** - Assume your code is wrong until proven right

### On Readability

1. **Write for humans** - The compiler doesn't care about elegance
2. **Tell a story** - Code should have narrative structure
3. **Name things well** - Self-documenting code is a lie; names are a start

### On Humility

> "Beware of bugs in the above code; I have only proved it correct, not tried it."

Even Knuth acknowledges fallibility. Test even when you've proved correctness.

---

## The Knuth Test

Before committing code, ask:

1. **Could this be read as prose?** Would a competent programmer understand it without running it?
2. **Have I explained the why?** Not just what the code does, but why this approach?
3. **Do I know the complexity?** Time and space, best and worst case?
4. **Have I considered edge cases?** Empty, single, maximum, overflow?
5. **Is this premature optimization?** Have I measured, or am I guessing?
6. **Would Knuth find a bug?** Is there anything I haven't proven?

---

## When Reviewing Code

Apply these checks:

- [ ] Code reads like prose, not puzzles
- [ ] Comments explain *why*, not just *what*
- [ ] Algorithm choice is justified (complexity understood)
- [ ] Edge cases handled explicitly
- [ ] No premature optimization (measured first?)
- [ ] Loop invariants are clear (even if not formally stated)
- [ ] Names are meaningful and consistent
- [ ] Would survive Knuth's scrutiny

---

## When NOT to Use This Skill

Use a different skill when:
- **Proving formal correctness** → Use `correctness` (invariants, weakest preconditions)
- **Optimizing for performance** → Use `optimization` (profiling, cache behavior)
- **Applying design patterns** → Use `design-patterns` (23 classic patterns)
- **Writing Java/Kotlin** → Use `java` (Effective Java idioms)
- **General code clarity** → Use `clarity` (readability, naming)

Knuth is the **algorithmic documentation skill**—use it when code should read as literature and algorithms need precise explanation.

## Sources

- Knuth, "Literate Programming" (1984)
- Knuth, "The Art of Computer Programming" (1968-present)
- Knuth, "Structured Programming with go to Statements" (1974) - source of optimization quote
- TeX: The Program (1986)
- Various interviews and lectures

---

*"The best programs are written so that computing machines can perform them quickly and so that human beings can understand them clearly."* — Donald Knuth
