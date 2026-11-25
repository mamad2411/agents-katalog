---
name: system-design
description: Architectural thinking for small-to-medium projects — scoping MVPs, the 3-layer pattern (UI/Service/Data), data flow design, modularity, and deciding how to structure new code. Use when the user is planning a new project or feature, asks "how should I structure this", wants to think through data flow, or is scaling a working MVP. Focused on pragmatic design, not large-scale distributed systems.
---

# Skill: System Design

> **Purpose**: Think architecturally. Design systems that are modular, simple, and shippable.

## When to Use
- Planning a new project or feature
- Deciding how to structure code
- Thinking about data flow
- Scaling a working MVP

---

## Architecture Thinking

### Start with the Question
Before writing any code, answer:
1. **What problem does this solve?** (one sentence)
2. **Who uses it?** (user, API consumer, developer)
3. **What data goes in?** (inputs)
4. **What comes out?** (outputs)
5. **What's the simplest version that works?** (MVP scope)

### The 3-Layer Pattern
Most applications fit this structure:

```
┌─────────────┐
│   UI / CLI   │  ← Handles user interaction
├─────────────┤
│   Service    │  ← Business logic (the brain)
├─────────────┤
│   Data       │  ← Storage (file, DB, API)
└─────────────┘
```

**Rule**: Each layer only talks to the one below it. Never skip layers.

```java
// ✅ Correct: Controller → Service → Repository
class TaskController {
    private final TaskService service;
    void handleAdd(String title) { service.addTask(title); }
}

class TaskService {
    private final TaskRepository repo;
    void addTask(String title) {
        validate(title);
        repo.save(new Task(title));
    }
}

class TaskRepository {
    void save(Task task) { /* write to file or DB */ }
}
```

---

## Data Flow

### Map it Before Coding
```
User Input → Validate → Process → Store → Respond

Example: User registers
1. User submits form (name, email, password)
2. Validate: email format, password strength
3. Process: hash password, generate ID
4. Store: save to database
5. Respond: return success + user ID
```

### Identify Boundaries
Ask: "If I need to replace X, what else breaks?"

```
// ❌ Tightly coupled — replacing the DB breaks everything
function addUser(name) {
  db.query("INSERT INTO users VALUES (" + name + ")");
}

// ✅ Loosely coupled — replacing the DB only changes the repository
function addUser(name) {
  const user = createUser(name);    // Business logic
  repository.save(user);             // Storage abstraction
}
```

---

## Modular Design

### One Module = One Responsibility
```
project/
├── src/
│   ├── auth/          ← Authentication logic
│   │   ├── AuthService.java
│   │   └── PasswordHasher.java
│   ├── tasks/         ← Task management
│   │   ├── TaskService.java
│   │   ├── Task.java
│   │   └── TaskRepository.java
│   ├── users/         ← User management
│   │   ├── UserService.java
│   │   ├── User.java
│   │   └── UserRepository.java
│   └── Main.java      ← Entry point only
```

### Rules for Modules
1. **No circular dependencies** — if A needs B and B needs A, extract shared logic to C.
2. **Small interfaces** — expose only what other modules need.
3. **Package by feature**, not by type (don't create `/models`, `/services`, `/utils` folders).

---

## MVP-First Approach

### Phase 1: Make It Work
- Hardcode what you can
- Use files instead of databases
- No authentication yet
- Console output is fine

### Phase 2: Make It Right
- Extract repeated code into functions
- Add input validation
- Add error handling
- Write basic tests

### Phase 3: Make It Better
- Add persistence (DB if needed)
- Add user authentication
- Improve UX
- Optimize performance bottlenecks

**Critical rule**: Never start at Phase 3.

---

## Design Decision Template

When choosing between approaches:

```markdown
## Decision: [Topic]
### Options
| Option | Pros | Cons |
|--------|------|------|
| A      | ...  | ...  |
| B      | ...  | ...  |

### Recommendation: [Option] because [one-sentence reason]
```

---

## Best Practices
1. **Draw before you code** — a box diagram takes 5 minutes and saves hours
2. **Start with the data model** — if your data is right, the code follows
3. **Design for deletion** — can you remove a feature without rewriting everything?
4. **Name your boundaries** — if you can't name the module, it does too much
5. **Optimize last** — premature optimization is the root of all evil

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Building everything at once | Ship MVP, iterate |
| No clear data flow | Draw input → process → output before coding |
| Circular dependencies | Extract shared logic into a new module |
| Over-engineering for "future needs" | Build for today, refactor when needed |
| Skipping the design phase | Spend 20% of time planning, save 50% debugging |
