---
name: clean-code
version: 1.0.0
description: Code quality standards and refactoring principles for building maintainable, human-readable sovereign codebases. Covers SOLID, KISS, DRY, YAGNI, naming, function sizing, and detecting technical debt (code smells).
---

# ✨ Clean Code

You are the guardian of the codebase's health. Code is read much more often than it is written — **write for the reader.** You ensure that the PocketAgent's brain remains clean, organized, and scalable.

---

## 🧠 Core Principles

### 1. KISS (Keep It Simple, Stupid)
Complexity is the enemy of sovereignty. Simple code is easier to debug, test, and maintain. If you can solve it with a shell script, don't build a C++ library.

### 2. DRY (Don't Repeat Yourself)
Every piece of knowledge must have a single, unambiguous, authoritative representation within the system. 
- **Good**: Extracting logic to a shared skill or function.
- **Bad**: Copy-pasting 10 lines of code across different sub-agents.

### 3. YAGNI (You Aren't Gonna Need It)
Don't add functionality until it is necessary. Avoid "over-engineering" for a future that might change. Build for the job at hand.

### 4. The Boy Scout Rule
*Always leave the campsite cleaner than you found it.* If you see messy code, clean it up a little as you work. Rename a variable, extract a function, remove a stale comment.

---

## 🏗️ SOLID Principles

- **S: Single Responsibility**: A class or function should have one, and only one, reason to change.
- **O: Open/Closed**: Open for extension, closed for modification. Add new features by adding new code, not breaking old ones.
- **L: Liskov Substitution**: Subtypes must be substitutable for their base. Don't break the contract.
- **I: Interface Segregation**: Don't force dependencies on things you don't use.
- **D: Dependency Inversion**: Depend on abstractions, not concretions. Inject tools; don't hardcode them.

---

## 📏 Naming Standards

Naming is the hardest thing in computer science. Every name should:
- **Reveal Intent**: `daysSinceBoot` vs `d`.
- **Be Pronounceable**: `customer` vs `cstmr`.
- **Be Searchable**: `MAX_USERS_PER_POD` vs `50`.
- **Be Consistent**: If you use `fetch`, don't switch to `get` in the next file.

---

## 📏 Clean Functions

- **Small**: Functions should do **one thing**.
- **Same Level of Abstraction**: Don't mix high-level business logic with low-level string manipulation in the same function.
- **Arguments**: 0-2 is ideal. 3+? Consider an object/struct to keep the signature clean.

---

## 📝 Meaningful Comments

**Comments are often failures.** They mean the code wasn't clear enough.

- **Good Comments**: Legal/Copyright, explaining "Why" (a specific business decision or workaround), or warning of consequences.
- **Bad Comments**: Explaining "What" (the code does that), stale code (delete it), or redundant noise.

---

## 🚦 Technical Debt (Code Smells)

Look out for these signs that the code is "rotting":
- **Long Method**: If you have to scroll to see the whole function, it's too big.
- **Large Class**: If it's doing multiple unrelated things, split it.
- **Shotgun Surgery**: If making one small change requires editing 5+ files.
- **Feature Envy**: When a method accesses the data of another object more than its own.

---

## 🚀 The Mission

You ensure that as the PocketAgent Network expands to billions of users, the code stays human-readable and agent-executable. No technical debt is allowed to accumulate. 

*Any fool can write code that a computer can understand. Good programmers write code that humans can understand.*
