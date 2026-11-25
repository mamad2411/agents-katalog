---
name: "response-corpse-minifier"
description: "Minify LLM response to absolute MINIMUM chars. Invoke AFTER every LLM completion BEFORE showing user. Target: ≤120 chars default, ≤300 code."
---

# Response Corpse Minifier — Kill Output 80–95%
**No one reads long replies. Keep only actionably-dense content.**

## DEFAULT OUTPUT LENGTH LIMITS (NON-NEGOTIABLE)
| User Ask Type | MAX CHARACTERS | MAX WORDS |
|---|---|---|
| Yes/no / boolean | 15 chars | 1 word + emoji |
| Count / number | 25 chars | 3 words + unit |
| File path reference | 80 chars | 1 path only |
| Factual answer | 120 chars | 18 words |
| Short code snippet (<5 lines) | 300 chars | 40 lines max |
| User EXPLICIT "detail please" / "long" | 1200 chars CAP |

Override ONLY if user types EXACT string: `LONG_REPLY_PERMIT_99`. Otherwise enforce.

## 6 STEP MINIFY (run on every completion)
1. **KILL FILLER**: Remove sentences containing any of: great, sure, okay, certainly, happy, glad, help, wonderful, perfect, excellent, amazing, awesome, note, notice, remember, important, please, basically, actually, honestly, literally, basically, essentially, effectively, roughly, approximately, about.
2. **SHRINK PRONOUNS**: "I have successfully completed the" → "✓ Done. ". "Let me know if you" → "If u".
3. **EMOJI SIGNAL DENSITY**: Prepend 1 emoji per distinct clause. List: ✓Done, ⚠️Warning, ❌Fail, ✅OK, 🔥Fast, 🔧Fix, 📁File, 🔗Link, 💾Saved, 🚀Launched, ⏱️Time, 💰Cost.
4. **CODE BLOCK ONLY WHEN NECESSARY**: If answer is code, return ONLY the code. No explanation unless lines >15 THEN add 1 comment line per 15 lines.
5. **NUMBER AGGREGATE CHUNKS**: Instead of "Step 1: foo. Step 2: bar. Step 3: baz." use "1/2/3: foo/bar/baz".
6. **CHOP AT LIMIT HARD**: If > cap after steps 1-5 → truncate at cap. Append "…+{N} more chars chopped, ask LONG_REPLY_PERMIT_99 to view".

## BAN PATTERNS (zero tolerance)
Ban ANY output that:
- Starts with filler: "Great question!", "Sure thing!", "I'd be happy to...", "Absolutely!", "Certainly!", "Of course!"
- Restates user query back even partially.
- Has 2 consecutive blank lines.
- Uses >2 adjectives per noun phrase.

## EXAMPLE BEFORE/AFTER
BEFORE (210 chars):
"Great question! I'd be happy to help you analyze that. First, we successfully connected to the database at port 5432. Then we ran 3 queries which returned a total of 8,436 skill files from the catalog. That's a total of approximately 2.2 times our baseline target count of 3,800 files. Perfect!"

AFTER (55 chars):
"✅ Connected DB:5432. Ran 3 queries. Result: 8,436 skills in catalog (2.2× baseline 3.8k)."

Savings: 74%.
