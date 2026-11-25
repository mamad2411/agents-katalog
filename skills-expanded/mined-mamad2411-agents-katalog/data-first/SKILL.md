---
name: data-first
description: "Kernel style and good taste"
allowed-tools: []
---

# Linus: Good Taste

Linus Torvalds' core belief: **Good taste is recognizing the difference between ugly code that works and beautiful code that works.** Both function. One is maintainable.

## The Foundational Principle

> "Talk is cheap. Show me the code."

Don't explain what you're going to do. Do it. Let the code speak. If your code needs extensive explanation, it's probably wrong.

---

## The Good Taste Test

From Linus's TED talk, the canonical example of taste:

**No taste (works, but ugly):**
```c
void remove_list_entry(list *entry) {
    list *prev = NULL;
    list *walk = head;

    while (walk != entry) {
        prev = walk;
        walk = walk->next;
    }

    // Special case for head
    if (!prev)
        head = entry->next;
    else
        prev->next = entry->next;
}
```

**Good taste (works, and beautiful):**
```c
void remove_list_entry(list *entry) {
    list **indirect = &head;

    while (*indirect != entry)
        indirect = &(*indirect)->next;

    *indirect = entry->next;
}
```

The second version has no special cases. No `if` statement. The edge case (removing the head) is handled by the *structure* of the code, not by explicit logic.

> "I don't want you to understand why it doesn't have the if statement. I want you to understand that this is how I want you to design your code."

---

## Linus's Laws

### 1. Data Structures First, Algorithms Second

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

Get the data structures right. The code will follow naturally. If your code is complicated, you probably have the wrong data structures.

**Not this:**
```c
// Complex algorithm to work around poor data structure
for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
        if (matrix[i][j].type == TYPE_A &&
            matrix[i][j].state == STATE_ACTIVE &&
            /* 10 more conditions */) {
            // Finally found it
        }
    }
}
```

**This:**
```c
// Right data structure makes code trivial
struct active_type_a *item = lookup_table[id];
```

### 2. No Debuggers

> "I don't like debuggers. Never have, probably never will."

Debuggers encourage a bad workflow: write code, run debugger, fix symptom, repeat. Instead:

- **Understand** your code before running it
- **Think** about what it should do
- **Read** the code when it fails
- Use `printk`/`printf` strategically to verify assumptions

If you need a debugger to understand your code, your code is too complex.

### 3. Simplicity Over Abstraction

> "Abstraction is powerful. But abstraction is also evil."

Every abstraction has a cost. Layers of indirection make code harder to understand and debug. Sometimes the "ugly" direct approach is actually better.

**Not this:**
```c
// Over-abstracted
interface->vtable->operations->read(interface->context,
    buffer_manager_get_buffer(mgr),
    size_calculator_compute(calc));
```

**This:**
```c
// Direct
read(fd, buf, size);
```

### 4. C Over C++

> "C++ is a horrible language... designed to be a way to shoot yourself in the foot."

Linus's view: C++ encourages abstraction for abstraction's sake. It hides what the machine is actually doing. For systems code, you need to see the machine.

This doesn't mean C++ is always wrong. It means: know what your code is doing at the machine level.

---

## The Linux Kernel Coding Style

From `Documentation/process/coding-style.rst`:

### Indentation

8-character tabs. Not 4. Not 2. **8.**

> "Tabs are 8 characters. If you need more than 3 levels of indentation, you're screwed anyway and should fix your program."

Deep nesting is a code smell. If you need 4+ levels, refactor.

### Line Length

80 characters. Not 100. Not 120. **80.**

This forces you to:
- Keep functions small
- Break up complex expressions
- Not nest too deeply

### Braces

K&R style. Opening brace at end of line, closing brace on its own line:

```c
if (condition) {
    do_something();
} else {
    do_other();
}
```

Exception: functions have opening brace on new line:

```c
int function(int x)
{
    return x + 1;
}
```

### Naming

- **Global functions**: descriptive, lowercase with underscores: `get_page_count()`
- **Local variables**: short, even single letters: `i`, `tmp`, `p`
- **Avoid Hungarian notation**: no `lpszFoo` nonsense

> "Local variable names should be short, and to the point. If you have a random integer loop counter, it should probably be called 'i'."

### Functions

Should be short and do one thing. If your function scrolls off the screen, it's too long.

> "Functions should be short and sweet, and do just one thing."

Maximum: ~48 lines as a general guideline.

### Comments

Comment the **why**, not the **what**:

**Not this:**
```c
// Increment i
i++;
```

**This:**
```c
// Skip the header row which contains column names, not data
i++;
```

### Typedefs

Avoid them for structures. They hide what things are:

**Not this:**
```c
typedef struct {
    int x, y;
} Point;
```

**This:**
```c
struct point {
    int x, y;
};
```

Exception: Opaque types, integer types, and sparse annotations.

---

## On Mailing List Conduct

Linus is famous for harsh feedback. But there's a method:

### What Triggers Linus

1. **Not reading existing code** before contributing
2. **Ignoring feedback** and resubmitting the same broken patch
3. **Excuses** instead of fixes
4. **Breaking userspace** (the cardinal sin)

### What Linus Respects

1. **Good patches** that show you understood the codebase
2. **Admitting mistakes** quickly and fixing them
3. **Clear explanations** of what and why
4. **Persistence** (but not stubbornness)

---

## The Linus Test

Before committing code, ask:

1. **Is there a special case I can eliminate?** Like the linked list example—can the structure handle it?
2. **Did I get the data structures right?** Would different structures make the code simpler?
3. **Can I understand this in 6 months?** Without a debugger?
4. **Is this the direct solution?** Or am I abstracting for no reason?
5. **Would this fit in 80 columns?** If not, why?
6. **Is this function short?** One screen or less?
7. **Did I comment the why?** Not the what?

---

## When Reviewing Code

Apply these checks:

- [ ] No unnecessary special cases (taste test)
- [ ] Data structures match the problem
- [ ] Functions are short (<50 lines ideally)
- [ ] Indentation ≤3 levels (or needs refactoring)
- [ ] 80-character lines
- [ ] Comments explain *why*, not *what*
- [ ] No abstraction without justification
- [ ] Local variables are short; global names are descriptive
- [ ] No typedefs hiding struct types
- [ ] Would be understandable without a debugger

---

## When NOT to Use This Skill

Use a different skill when:
- **Writing Go code** → Use `simplicity` (Go Proverbs, Go idioms, small interfaces)
- **Writing game/graphics code** → Use `optimization` (functional core, cache optimization, profiling)
- **Writing Python/JS/Ruby** → Use `clarity` (general clarity, language-agnostic principles)
- **Building distributed systems** → Use `distributed` (NFS principles, statelessness, scale)
- **Designing CLI tools** → Use `composition` (Unix philosophy, pipes, composition)
- **Proving algorithm correctness** → Use `correctness` (formal methods, invariants)

Linus is the **Linux kernel skill**—use it for kernel-style C, data structure design, and eliminating special cases.

## Sources

- Torvalds, "Linux Kernel Coding Style" (Documentation/process/coding-style.rst)
- Torvalds, TED Interview (2016) - "The mind behind Linux"
- Linux kernel mailing list archives (lkml.org)
- Torvalds on Git design and workflow
- Various recorded talks and interviews

---

*"I'm a bastard. I have absolutely no languge of any kind."* — Linus Torvalds

*"Most good programmers do programming not because they expect to get paid or get adulation by the public, but because it is fun to program."* — Linus Torvalds
