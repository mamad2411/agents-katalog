---
name: unit-test-methodology
description: >
  Systematically generate unit tests by enforcing testing methodology for complete coverage.
  Trigger when the user says: "write unit tests", "add tests", "generate test cases",
  "test coverage", "how do I test this", "write tests for", "补充测试",
  "帮我写单元测试", "生成测试用例", "这个函数怎么测", "测试覆盖率不够",
  "写 test", "给这个方法加测试", "单测".
  Unlike ad-hoc test generation, this Skill enforces analyze-then-derive:
  systematically partition equivalence classes per parameter, apply boundary values
  for ranged inputs, use Pairwise to compress combinations for 4+ parameters,
  and use decision tables for multi-condition branches.
  Every test case must be annotated with its source technique to guarantee
  systematic coverage without missing critical boundary scenarios.
  Supports Go / Python / Java / TypeScript / Rust. Trigger even when the user just says "write a test".
---

# Unit Test Methodology Skill

Internalize testing design methodology into code generation — think like a senior test engineer, not a random generator.

## Core principle

> **Analyze first, derive second, write code last. Never skip a step.**

Jumping straight to test code without analysis is the most common mistake — avoid it.

---

## Step 1: Identify language

Identify the language and load the corresponding reference:

| Language | Reference file |
|----------|---------------|
| Go | `references/go.md` |
| Python | `references/python.md` |
| Java | `references/java.md` |
| TypeScript / JavaScript | `references/typescript.md` |
| Rust | `references/rust.md` |

If the language is unclear, ask the user or infer from code style.

---

## Step 2: Analyze the function (required)

Read the function/method code and explicitly list the following in your response — **do not skip**:

### Parameter dimension
- Type and **implicit business constraints** for each parameter (not just type, but business rules)
- Dependencies between parameters (if A exists, must B be non-null?)
- Special values: `nil` / `null` / `zero` / `empty` / `negative` / max value
- Enum/state types: does each value behave differently?

### Behavior dimension
- What is the **happy path**?
- Under what conditions does it return `error` / `false` / `null` / throw an exception?
- Are there **side effects** (write to DB / send message / modify external state)?
- Do mock call counts/arguments need verification?

### Dependency dimension
- Which interfaces/external services are depended on? Which need mocking?
- Do different behaviors of external dependencies (success/failure/timeout) affect the result?

---

## Step 3: Select techniques

Choose from the table below based on analysis — **multiple selections, usually combined**:

| Function characteristic | Technique | Notes |
|------------------------|-----------|-------|
| Any parameter | **Equivalence Partitioning** | Always apply |
| Numeric parameter with range | **Boundary Value Analysis** | Add on top of EP |
| Parameter with enum/state values | **EP** (one class per value) | One valid class per legal value |
| Multiple if/else condition branches | **Decision Table** | Cover condition combinations |
| 4+ independent parameters | **Pairwise Combinatorial** | Compress full combinations |
| Object with state field | **State Transition Testing** | One valid + one invalid transition each |
| Write operation callable multiple times | **Idempotency Testing** | Verify repeated-call behavior |

---

## Step 4: Derive test cases systematically

### Equivalence partitioning rules
- Valid class: at least 1 (normal input scenario)
- Invalid classes: **each failure case is its own test case, never merge**
- Annotation format: `// [EP·valid]` / `// [EP·invalid·1: email is empty]`

### Boundary value rules
Take 6 points for each parameter with a range constraint:

```
[min-1]  [min]  [min+1]  ...  [max-1]  [max]  [max+1]
 outer   inner  inner         inner   inner   outer
(expect err) (ok) (ok)        (ok)    (ok)  (expect err)
```

`minLength` / `maxLength` for strings apply the same way.
Annotation format: `// [BV·min]` / `// [BV·max+1]`

### Decision table rules
- List all condition variables that affect the output
- Generate one test case per meaningful condition combination
- Focus on mutually exclusive and dependent conditions

### Pairwise rules (for 4+ parameters)
When there are many parameters, inform the user they can compute the minimum combination set (if caseforge is installed):

```bash
caseforge pairwise \
  --var "role:admin,user,guest" \
  --var "status:active,inactive,pending" \
  --var "is_owner:true,false" \
  --var "region:cn,us,eu"
# Full combinations 3×3×2×3=54 → Pairwise ≈ 12
```

For 6 or fewer parameters, you can also compute Pairwise combinations directly in reasoning.

---

## Step 5: Test data

Prefer generating **realistic data with business meaning** — avoid placeholders like `"test"` / `"foo"` / `1`.

For bulk data:

```bash
caseforge fake \
  --field "id:uuid" \
  --field "name:person_name" \
  --field "email:email" \
  --field "age:int:18:65" \
  --field "role:enum:admin,user,guest" \
  --count 3 \
  --seed 42    # Fixed seed, reproducible in CI
```

---

## Step 6: Generate test code

Based on the language identified in Step 1, generate code following the conventions in `references/<lang>.md`.

**Every test case must include**:
1. **A name describing the scenario** (not `test1` / `case2`)
2. **Technique annotation** (comment, see format above)
3. **Input data with business meaning**
4. **Explicit expected result**
5. **Complete assertions** (including side-effect verification, not just return value)

---

## Notes

- Invalid equivalence classes **must each be their own test case** — merging is an error
- Functions with side effects (write DB / send message) **must verify mock calls**, not just assert the return value
- When business constraints are uncertain, mark the test name with `[needs confirmation]` and provide assumption notes
- When parameters ≥ 4, **proactively suggest** using `caseforge pairwise`
- Test code must be **directly runnable** — no TODOs or placeholders

---

## Test case count reference

```
Function with 3 parameters, typical case count:
  EP happy path:              1
  Invalid classes per param:  2-3 × 3 params = 6-9
  Boundary values (if ranged): 4-6
  Key cross-parameter combos: 2-4
  Dependency failure scenarios: 1-3
  Total:                      ~15-25 test cases
```

Fewer than 5 cases usually means insufficient analysis — revisit the function.
