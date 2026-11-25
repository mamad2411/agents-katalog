---
name: markdown-math
description: Use when writing KaTeX math. Pitfalls, format, style.
---

# Markdown Math — Writing Mathematical Content

## When to use

Use this skill when writing mathematical derivations, assignment solutions, lecture notes, or any document heavy with LaTeX math in markdown. Covers **what to do** and **what to avoid** with KaTeX in markdown.

---

## KaTeX Pitfalls (必读)

### 1. Inline math `$...$` — avoid bare `*` inside

**Wrong:** `$f^*(\cdot)$` — the `*` is parsed by markdown as emphasis before KaTeX sees it.

**Right:** `$f^\ast(\cdot)$` — use `\ast` instead of bare `*` inside inline math.

Also applies to `$x^*$` → `$x^\ast$`.

### 2. Markdown italic around inline math

**Wrong:** `*[P.S. $f^*(\cdot)$]*` — the `*...*` italic wrapper interferes with `$...$` delimiters.

**Right:** Use `_..._` for italic when it wraps math: `_[P.S. $f^\ast(\cdot)$]_`, or just omit italic.

### 3. `\text{}` inside `\boxed{}`

**Wrong:** `\boxed{G = \text{const} \times \sigma \sqrt{Q/V}}` — `\text` inside `\boxed` causes KaTeX parse error in some renderers.

**Right:** Use a simple constant `c` instead: `\boxed{G = c \,\sigma\sqrt{Q/V}}`.

Or use `\mathrm{const}` if `c` is too terse.

### 4. Numbered lists wrapping display math

**Wrong:**
```markdown
1. $$
   G = \sigma \frac{Q}{V}
   $$
```

The `1. ` list marker on the same line as `$$` breaks many markdown renderers.

**Right:** Keep `$$` blocks at top level (not nested in lists). Use headings or `**(N)**` labels instead:

```markdown
**(1)**

$$
G = \sigma \frac{Q}{V}
$$
```

### 5. `\!` (negative thin space) is fine in KaTeX

`\!\left(` works in KaTeX — no need to avoid it.

### 6. `\boxed` inside `\begin{aligned}`

**Wrong:** 
```markdown
$$
\begin{aligned}
G &= c \times \frac{C}{QP} \times z^{1/2} \\
&= c \times Q^{1/2}\sigma V^{-1/2}
= \boxed{c \times \sigma\sqrt{Q/V}}
$$
```

KaTeX's `aligned` environment expects `&` alignment markers and `\\` line breaks. A `\boxed` on the last line breaks parsing: _"Expected & or \\ or \cr or \end at end of input"_.

**Right:** Split into two blocks — one plain `$$` for the derivation chain, one standalone `$$` with just the box:
```markdown
$$
G = c \times \frac{C}{QP} \times z^{1/2}
= c \times Q^{1/2}\sigma V^{-1/2}
$$

$$
\boxed{G = c\;\sigma\sqrt{Q/V}}
```

### 7. Display math separator

Always put a blank line before and after `$$` blocks. No exceptions.

---

## Solution Format Preferences

For quant assignment solutions:

- **Concise, equations-forward.** Lead with the math, not prose. Derivation steps in equation blocks, brief inline comments between them.
- **No narrative paragraphs.** A line of explanation between equation blocks is fine. A paragraph-length explanation is too much.
- **Every question gets its own section** with a clear heading.
- **Box the final answer** with `\boxed{}`.
- **Use `c` for arbitrary constants** (not `\text{const}`).
- **Language:** match the assignment's language (English or Chinese).

---

## Folder Conventions

| Content | Location |
|---------|----------|
| Problem statement | `assignments/assignment-N/Assignment N.md` |
| Task checklist | `assignments/assignment-N/task.md` |
| Solved work | `assignments/assignment-N/solution.md` |
| PDF original | `assignments/assignment-N/Assignment N.pdf` (gitignored) |

The `tasks/task-N/` directory is for separate **coding tasks** (C++, Python, etc.), not for assignment problem briefs.

---

## References

- [dimensional-analysis.md](references/dimensional-analysis.md) — Buckingham Pi workflow for quantitative assignments (Q3 pattern).
