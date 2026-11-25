---
name: correctness
description: "Formal methods"
allowed-tools: []
---

# Dijkstra: The Humble Programmer

Edsger Dijkstra's core belief: **Programming is a branch of applied mathematics.** Programs should be derived from specifications through rigorous reasoning, not hacked together and tested until they seem to work.

## The Foundational Principle

> "Program testing can be used to show the presence of bugs, but never to show their absence."

Testing finds bugs. It doesn't prove correctness. For critical software, you need mathematical reasoning, not just passing tests.

---

## The Humble Programmer

From his Turing Award lecture (1972):

> "We shall do a much better programming job, provided that we approach the task with a full appreciation of its tremendous difficulty, provided that we stick to modest and elegant programming languages, provided that we respect the intrinsic limitations of the human mind and approach the task as Very Humble Programmers."

### Intellectual Humility

Our brains are limited. We can only hold so much in working memory. Therefore:

1. **Keep programs simple** - so we can understand them
2. **Use abstraction wisely** - to manage complexity
3. **Prove correctness** - don't trust intuition
4. **Be skeptical of cleverness** - including your own

### The Competent Programmer

> "The competent programmer is fully aware of the strictly limited size of his own skull; therefore he approaches the programming task in full humility."

You are not smart enough to write correct complex programs by intuition. No one is. Use discipline instead.

---

## Structured Programming

Dijkstra, with Dahl and Hoare, established structured programming.

### Go To Considered Harmful

> "The go to statement as it stands is just too primitive; it is too much an invitation to make a mess of one's program."

The problem with `goto`: it makes program flow impossible to reason about. You can't look at a statement and know how you got there.

**Not this:**
```
    start:
        read(x)
        if x < 0 goto negative
        if x > 100 goto toolarge
        process(x)
        goto start
    negative:
        print("negative!")
        goto start
    toolarge:
        print("too large!")
        goto start
```

**This:**
```
    while true:
        read(x)
        if x < 0:
            print("negative!")
        elif x > 100:
            print("too large!")
        else:
            process(x)
```

### The Three Structures

All programs can be written with only:

1. **Sequence** - statements execute in order
2. **Selection** - if/then/else
3. **Iteration** - while loops

No `goto` needed. Ever.

### Why It Matters

Structured code has **one entry, one exit** per block. This makes reasoning possible:

- You know how control reaches each statement
- You can reason about what's true at each point
- You can prove properties about the code

---

## Program Derivation

From "A Discipline of Programming":

### Don't Write, Derive

> "We should not ask 'How do we write this program?' but 'How do we derive this program from its specification?'"

The process:
1. Start with a specification (what should be true)
2. Derive the program through mathematical reasoning
3. The program is correct by construction

### Weakest Preconditions

For any statement S and postcondition R, the weakest precondition `wp(S, R)` is the weakest condition that guarantees R after S executes.

**Example:**
```
Statement: x := x + 1
Postcondition: x > 5

wp(x := x + 1, x > 5) = x > 4
```

If x > 4 before, then x > 5 after.

### Loop Invariants

To prove a loop correct:
1. **Establish invariant** - true before loop starts
2. **Maintain invariant** - if true before iteration, true after
3. **Use invariant + termination** - proves postcondition

**Example:**
```
// Invariant: sum = a[0] + a[1] + ... + a[i-1]
sum := 0
i := 0
while i < n:
    sum := sum + a[i]
    i := i + 1
// Postcondition: sum = a[0] + ... + a[n-1]
```

The invariant plus `i = n` (termination) proves the postcondition.

---

## On Simplicity

### Simplicity Is Not Optional

> "Simplicity is prerequisite for reliability."

Complex programs cannot be understood. Programs that cannot be understood cannot be trusted. Therefore: simplicity is mandatory.

### Elegance

> "Elegance is not a dispensable luxury but a quality that decides between success and failure."

Elegant solutions are:
- Easier to understand
- Easier to prove correct
- Easier to modify
- Less likely to hide bugs

### The Role of Beauty

> "In their capacity as a tool, computers will be but a ripple on the surface of our culture. In their capacity as intellectual challenge, they are without precedent in the cultural history of mankind."

Programming is an intellectual discipline. Beauty and elegance are not decorations—they are signs that you've found the right solution.

---

## On Separation of Concerns

### Divide and Conquer

> "The separation of concerns... even if not perfectly possible, is the only available technique for ordering one's thoughts."

Break problems into independent pieces. Solve each piece. Combine solutions.

### Abstraction Layers

Each layer should be:
- Complete (handles all cases at its level)
- Consistent (behaves uniformly)
- Independent (doesn't leak details to other layers)

### Why Modularity Matters

> "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."

Abstraction isn't hiding complexity. It's creating a level where complexity doesn't exist.

---

## On Education and Practice

### Against BASIC

> "It is practically impossible to teach good programming to students that have had a prior exposure to BASIC: as potential programmers they are mentally mutilated beyond hope of regeneration."

(Harsh, but his point: bad habits learned early are nearly impossible to unlearn.)

### The Tools We Use

> "The tools we use have a profound and devious influence on our thinking habits, and therefore on our thinking abilities."

Choose languages, tools, and practices that encourage rigorous thinking.

### On Natural Language

> "Besides a mathematical inclination, an exceptionally good mastery of one's native tongue is the most vital asset of a competent programmer."

Clarity of thought requires clarity of expression. If you can't explain it clearly, you don't understand it.

---

## Dijkstra's Aphorisms

From his EWDs (numbered manuscripts):

> "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

> "Computer Science is no more about computers than astronomy is about telescopes."

> "Perfecting oneself is as much unlearning as it is learning."

> "Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it. And to make matters worse: complexity sells better."

> "If debugging is the process of removing software bugs, then programming must be the process of putting them in."

---

## The Dijkstra Test

Before committing code, ask:

1. **Is this simple?** Can I understand the entire thing at once?
2. **Is it structured?** One entry, one exit per block? No goto-like jumps?
3. **Could I prove this correct?** Do I know the invariants?
4. **Have I separated concerns?** Are independent things independent?
5. **Is it elegant?** Would Dijkstra approve of the solution?
6. **Am I being humble?** Or trusting my cleverness too much?
7. **Could I explain this clearly?** In precise natural language?

---

## When Reviewing Code

Apply these checks:

- [ ] Code is structured (sequence, selection, iteration only)
- [ ] No goto-like patterns (early returns that obscure flow, deeply nested breaks)
- [ ] Each function has clear pre/postconditions
- [ ] Loops have identifiable invariants
- [ ] Complexity is minimized (not just managed)
- [ ] Abstractions are precise, not vague
- [ ] Concerns are separated (independent things independent)
- [ ] Could be proven correct (even if informal proof)
- [ ] Simple enough to hold in one's head

---

## On Formal Methods

Dijkstra championed formal methods—mathematical proof of program correctness.

### When to Use Formal Methods

- Safety-critical systems (medical, aviation, nuclear)
- Security-critical systems (cryptography, access control)
- When testing cannot provide adequate confidence
- When the cost of bugs exceeds cost of proof

### Practical Application

Even without full formal proof:
1. **Write specifications** - what should be true?
2. **State invariants** - what's always true?
3. **Reason about edge cases** - prove they're handled
4. **Document pre/postconditions** - make contracts explicit

---

## When NOT to Use This Skill

Use a different skill when:
- **Documenting algorithms as prose** → Use `algorithms` (literate programming)
- **Applying OO design patterns** → Use `design-patterns` (23 patterns catalog)
- **Writing Java/Kotlin** → Use `java` (Effective Java idioms)
- **Optimizing performance** → Use `optimization` (profiling, data-oriented)
- **General code clarity** → Use `clarity` (readability, naming)

Dijkstra is the **formal methods skill**—use it when correctness must be proven, not just tested.

## Sources

- Dijkstra, "A Discipline of Programming" (1976)
- Dijkstra, "Go To Statement Considered Harmful" (1968)
- Dijkstra, "The Humble Programmer" (Turing Award lecture, 1972)
- Dijkstra, EWD manuscripts (cs.utexas.edu/~EWD/)
- Dijkstra, Dahl, Hoare, "Structured Programming" (1972)

---

*"How do we convince people that in programming simplicity and clarity—in short: what mathematicians call 'elegance'—are not a dispensable luxury, but a crucial matter that decides between success and failure?"* — Edsger W. Dijkstra
