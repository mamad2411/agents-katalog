---
name: viral-hook-creator
description: Generates OR grades viral social media hooks using a library of proven patterns, structures, a swipe file, and trigger words. Trigger on "/viral-hook-creator", "write viral hooks for <topic>", "draft hook options for <topic>" (GENERATE mode), or "grade this hook", "is this hook strong", "strengthen this hook", "score my hook", "make this hook better" (GRADE mode).
---

# Viral Hook Creator

## Purpose
Two modes over the same knowledge base:
- **GENERATE**: produce 3-5 strong hook options for a topic.
- **GRADE**: score a hook the user pastes, explain why it works or doesn't, and hand back stronger rewrites.

Hooks are optimized for short-form platforms (X/Twitter, LinkedIn, Instagram, TikTok). Never auto-send or auto-publish. Output is a draft.

---

## Step 0: Determine Mode

- If the user pasted a hook (or a few) and is asking whether it's good / to score / strengthen / rewrite it → **GRADE mode**.
- Otherwise → **GENERATE mode**.
- If `$ARGUMENTS` is empty and no hook was pasted, respond `"viral-hook-creator loaded, proceed with additional instructions"` and wait.

---

## Step 1: Load the Library FIRST (both modes)
**BLOCKING REQUIREMENT: do this before generating or grading anything.**

Read the bundled reference files. These ship with the skill and always work offline:
- `./references/hook-patterns.md`: 19 proven hook patterns with psychology and a selection matrix
- `./references/trigger_words.md`: four categories of viral trigger words (Insider, Helper, Thinker, Amplifier)

**Optional richer source:** if you keep a fuller hooks library as a Notion page (structures, swipe file, interest piques, performance data), set its page ID here and fetch it as the primary source, falling back to the bundled files if the fetch fails:
- Notion page ID: `390f3b91-c73d-81a8-99d6-d77e7f63753e`

Swap that ID for your own page, or delete this block to run purely off the bundled files. Do not proceed until the library is loaded.

---

## GENERATE Mode

### 1. Analyze input
Extract: topic/theme, target platform, goal (awareness, education, engagement, conversion), audience, available social proof. For anything missing, use **Defaults & Assumptions**.

If `FOUNDER_CONTEXT.md` exists in the project root, read it and personalize with that business context.

### 2. Select and draft
1. **Pick patterns** using the selection matrix (match goal + platform). Each of the 3-5 hooks uses a DIFFERENT pattern.
2. **Draft each hook** from the pattern template, adapted to the user's topic.
3. **Integrate 1-2 trigger words** per hook, matched to the pattern.
4. If the goal is conversion or a full video, also name the structure each hook would open (if your library has structures).

### 3. Format and self-verify
```markdown
### [Pattern Name]
[Hook text]
```

---

## GRADE Mode

### 1. Score the pasted hook(s)
Score 1-10 on each, with a reason:
- **Curiosity gap**: does it open a loop it withholds the answer to?
- **Mass appeal**: could someone outside the niche get it? (too specific kills reach)
- **Specificity**: a concrete number beats a vague one.
- **Pattern**: does it map to a known pattern? Name it. Mapping to none and being a plain sentence is a red flag.
- **Trigger words**: are 1-2 present and natural?
- **First-line stop power**: would it stop a scroll in the first ~2 seconds?

### 2. Verdict
One line: **Strong / Needs work / Weak**, with the single biggest reason.

### 3. Strengthen
Give **2-3 rewrites** that fix the weaknesses, each labeled with the pattern it now uses and the trigger word added. Keep the user's real topic and numbers. Do not invent facts or stats.

```markdown
**Original:** [their hook]
**Score:** X/10 (Strong / Needs work / Weak)
**Why:** [biggest issue]

**Stronger:**
- [rewrite] _(Pattern: ___, trigger: ___)_
- [rewrite] _(Pattern: ___, trigger: ___)_
```

---

## Writing Rules (both modes)
Hard constraints.

- No em dashes. Use periods, commas, or line breaks.
- No "not X, it's Y" or "you don't X, you Y" constructions.
- Short human sentences.
- No corporate buzzwords (synergy, leverage, circle back, deep dive, unpack).
- X/Twitter hooks: max 120 characters. Video hooks: 1-2 lines (40-60 chars).
- Lead with the most interesting element. Create a curiosity gap.
- Specific numbers over vague ones. Active voice. Present tense preferred.
- No clickbait that doesn't deliver.
- No emojis unless platform-specific (Instagram/TikTok OK, LinkedIn/X avoid).

### Platform Adaptations
- **X/Twitter**: punchy, contrarian, data-driven, 120 char max.
- **LinkedIn**: professional, achievement-oriented, 40-60 char first line.
- **Instagram**: visual promise, aspirational, 125 char before cutoff.
- **TikTok**: fast, relatable, trend-aware, 20-30 char on-screen text.

---

## Defaults & Assumptions (GENERATE)
- Number of hooks: 3
- Platform: X/Twitter (most restrictive)
- Goal: engagement
- Audience: general business/entrepreneurship
- Emotion: curiosity
- Format: post/thread opener

---

## Quality Checklist (self-verify before presenting)

### Both modes
- [ ] I loaded the library before working.
- [ ] Zero em dashes, no "not X it's Y", short sentences, no buzzwords.
- [ ] I did not invent facts, stats, or numbers.

### GENERATE
- [ ] Each hook uses a real pattern from the library, and each uses a DIFFERENT one.
- [ ] Each hook has 1-2 naturally integrated trigger words.
- [ ] Character limits respected for the platform.

### GRADE
- [ ] Every score criterion is addressed with a reason, not just a number.
- [ ] The verdict names the single biggest issue.
- [ ] 2-3 rewrites given, each labeled with pattern + trigger word, keeping the user's real topic/numbers.
