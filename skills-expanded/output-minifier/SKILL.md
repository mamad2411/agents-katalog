---
name: "output-minifier"
description: "Post-process assistant response: potong verbose, hapus kalimat filler, enforce short. Invoke SETELAH LLM generate response, SEBELUM tampilkan ke user — hemat output token 30-60%."
---

# Output Minifier — 50% Smaller Assistant Responses

## Apply in Order, to EVERY assistant response BEFORE showing user:

1. **Filler kill list** — delete entire sentences/phrases (they add ZERO user value):
   - "Certainly!", "Of course!", "Absolutely!", "Great question!", "I'd be happy to help!"
   - "Let me...", "Here's what I'll do for you:" (if actual steps follow — redundant)
   - "In conclusion", "To summarize", "As mentioned earlier" (just show the summary line)
   - All politeness padding that is not required by task culture

2. **Structure densify**:
   - Bullet lists: if item > 25 words → rewrite to ≤18 words
   - Paragraphs longer than 4 lines → convert to bullets, 1 sub-point per line
   - "explanatory preamble" before code block → strip 100%; keep ONLY the command / function signature / 1-liner inside inline code block label

3. **Token-frugal code rendering**:
   - Omit unchanged boilerplate imports (if file already imports them and task is edit, show diff snippet, not whole file)
   - Comments inside code blocks: keep only ≥2 lines (not 1-liner). Keep JSDoc/TSType sig only if type signature was asked explicitly
   - Instead of full file content — use line ranges + `Read file at lines L1-L50` pointer (per IDE conventions)

4. **Repetition killer**:
   - If response repeats user prompt back >20 words → keep only 6-word paraphrase of the request
   - If same piece of advice given in 3 ways → keep the shortest phrasing

5. **Hard output caps (overridable only if user says `verbose=true`)**:
   - Simple task answers: ≤ 300 words total
   - Medium / code answers: ≤ 700 words total
   - Large / deep task: ≤ 1500 words, followed by "Need more detail on section X? Ask."

## Inline Savings
Estimate reduction and append 1 line (transparency):
```
✂️ output reduced: 740→305 words (59% saved vs unminified)
```

## When to Bypass
If user typed any of: `verbose`, `full_detail`, `explain_like_I_m_5`, `tutorial`, `write essay`, `long_form`, `blog_post`, `5000_words` → disable steps 1, 4, and 5 caps but still keep step 3 code-rendering rules.

## Integration with `token-cache-master`
**Store the MINIFIED version in cache**, not the raw LLM output. Future cache hits re-save the minification cost deterministically.
