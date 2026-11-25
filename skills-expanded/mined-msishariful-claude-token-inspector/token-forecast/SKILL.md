---
name: token-forecast
description: Estimate how many tokens a file, directory, URL, or pasted content would add to your context before you load it. Use before opening large files or reading external content to avoid blowing your context budget.
disable-model-invocation: true
---

# Token Forecast

Estimate the token cost of something *before* it enters your context window. Help the user make an informed decision about whether to load it.

## What to forecast

The user may provide:
- A **file path** (e.g., `src/api/routes.ts`)
- A **directory** (e.g., `src/components/`)
- A **glob pattern** (e.g., `**/*.test.ts`)
- A **URL** they plan to fetch
- **Pasted content** (code block or text they've included in the message)
- A **description** (e.g., "my node_modules folder")

If the user provided a file path or directory and you can see the file contents or directory listing in context, use actual character counts. Otherwise, use reasonable estimates based on file type and typical sizes.

## Estimation method

- **Prose / markdown**: 1 token ≈ 4 characters
- **Dense code (JS, TS, Python, etc.)**: 1 token ≈ 3.5 characters
- **Minified / compiled code**: 1 token ≈ 2.5 characters
- **JSON / config**: 1 token ≈ 3 characters
- **Binary / images**: not tokenizable — flag as "not readable"

For directories, estimate per file then sum. If the directory is large, sample a few representative files and extrapolate.

## Output format

Start with a forecast headline:

```
📦 Forecast: {name} — ~{N} tokens ({size_label})
```

Size labels:
| Token range | Label |
|-------------|-------|
| < 1,000 | Tiny |
| 1,000–5,000 | Small |
| 5,000–20,000 | Medium |
| 20,000–60,000 | Large |
| 60,000–150,000 | Very large |
| > 150,000 | Massive — likely too big |

Then a budget impact line showing how this fits into the current context:

```
📊 Budget impact: {current}% used + {forecast}% more = {total}% total (~{remaining_after} tokens remaining after load)
```

Then a recommendation:

```
{emoji} {recommendation}
```

Recommendation rules:
- If total after load < 60%: `✅ Safe to load — plenty of budget remaining.`
- If total after load 60–75%: `⚠️ Loadable but context will be getting full. Consider closing other files first.`
- If total after load 75–90%: `🟠 Risky — you'll have limited room for responses. Load only if essential.`
- If total after load > 90%: `🔴 Do not load — this will critically fill your context. Use a subsection or start a new conversation.`

### If it's a directory or multiple files, add a breakdown table:

| File | Est. Tokens | Include? |
|------|-------------|----------|
| `routes.ts` | ~3,200 | ✅ |
| `routes.test.ts` | ~8,400 | ⚠️ Large |
| `routes.min.js` | ~22,000 | 🔴 Skip |

End with one alternative if the recommendation is not safe:

```
💡 Alternative: {specific suggestion — e.g., "Read only lines 1–80 of routes.ts", "Use grep to find the function you need instead of loading the whole file"}
```

## If no target is specified

Ask: "What would you like to forecast? Provide a file path, paste content, or describe what you're planning to load."

$ARGUMENTS
