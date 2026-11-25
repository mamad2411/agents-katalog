---
name: tailwind-cleanup
description: Removes unused Tailwind classes, extracts repeated class patterns into components
argument-hint: [directory]
user-invocable: true
allowed-tools: Bash Read Grep Glob Edit
effort: medium
---

## Tailwind CSS Cleanup

Target: **$1** (or `src/` if not specified)

### 1. Find Unused Classes
```bash
npx tailwindcss --content "./src/**/*.{ts,tsx}" --input ./src/styles/globals.css --dry-run 2>/dev/null | grep "Removing"
```

### 2. Find Repeated Class Combinations
```bash
grep -rn 'className="' ${1:-src/} --include="*.tsx" | grep -oP 'className="[^"]+"' | sort | uniq -c | sort -rn | head -20
```

### 3. Extract Repeated Patterns
When the same 5+ class combination appears 3+ times, it should become:
- A component (if it's a complete UI element)
- A `cn()` variant (if it's a style pattern)
- A `@apply` in CSS (sparingly)

### 4. Check for Anti-Patterns
- `!important` overrides (`!text-red-500`)
- Arbitrary values where a design token exists (`text-[#FF0000]` → use color from theme)
- Mixing Tailwind with raw CSS in the same element

### 5. Verify PurgeCSS config covers all dynamic class patterns:
```ts
// ❌ Dynamic classes get purged
const color = isError ? 'red' : 'green'
<div className={`text-${color}-500`} />

// ✅ Full class names are safe
const className = isError ? 'text-red-500' : 'text-green-500'
```

Report: N unused classes removed, N patterns extracted.
