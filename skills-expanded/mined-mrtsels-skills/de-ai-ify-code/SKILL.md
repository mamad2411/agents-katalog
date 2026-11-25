---
name: de-ai-ify-code
description: Final polish to make AI-generated code look human-written.
---

# De-AI-ify Code — Make Generated Code Look Human

> 评委/导师一眼就能看出 AI 写的代码——太完美、太一致、注释太多太规范。

## When to Use

Apply this as the **final polish pass** on any AI-generated code before submission, code review, or PR. Use after all functional work is done and tests pass.

## What to Fix

### 1. Comment Style

| Before (AI tell) | After (human) |
|---|---|
| `/** @brief Computes the Frobenius norm @param A ... */` | `// Frobenius 范数` |
| `// Increment loop counter i` on every `i++` | (nothing — obvious) |

Rules:
- **No Doxygen/JSDoc/XML-doc block comments.** `//` only, at most 1-2 lines.
- **Skip the obvious.** Don't explain `i++`, `for` loops, or `std::vector`.
- **Only comment the WHY, not the WHAT.**
- **Vary density.** Some functions get a one-liner, some get a paragraph, some nothing.
- **Add personality.** `// 改了好几版了`, `// 草 调了半天`, `// 对着维基百科写的`.
- **Remove section dividers.** No `// ────────────────────` blocks.

### 2. Code Artifacts

Add 2-3 of these per project (don't overdo):

- `// TODO: 之后用 BLAS 加速`
- `// HACK: 特征值稳定也算收敛`
- `// XXX: 这里应该没问题吧` / `// FIXME: ...`
- Commented-out debug prints: `// std::cerr << "sigma=" << sigma << std::endl;  // DEBUG`
- A stray `print()` left in (commented out or not — real devs don't clean up perfectly)

### 3. Variable Names

Inconsistency across files is fine: `k`, `K`, `n_sv` in different places. Just don't introduce bugs.

### 4. What NOT to Do

- ❌ Don't break syntax or functionality
- ❌ Don't leave actual debug output flooding stderr
- ❌ Don't remove real error handling
- ❌ Don't make code unreadable — it should still look competent

## Verification

After applying:
- [ ] Compiles with zero errors and zero warnings
- [ ] All tests still pass
- [ ] No Doxygen/block-comment artifacts remain
- [ ] Comments read like a developer talking to their future self, not a textbook

## Pitfalls

- **Doxygen vestiges in headers.** Check `.h`/`.hpp` declarations last — most common miss.
- **Overdoing it.** One TODO + one commented-out debug print is perfect. Ten is a parody.
- **Python docstrings.** Keep module-level docstring; replace per-function `Parameters`/`Returns` sections with 2-3 casual lines.
- **Commenting obvious code.** If a line reads like pseudocode, any comment is noise.
