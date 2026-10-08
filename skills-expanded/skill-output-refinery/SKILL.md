---
name: "skill-output-refinery"
description: "Runs 4-stage quality pass on ANY skill's raw output: completeness audit, error checks, user-intent alignment, and polish/actionability injection. Invoke AFTER every skill execution for guaranteed +15-50% output value."
---

# Skill Output Refinery — 4-Stage Quality Pass

Run AFTER ANY skill returns output. Target: +15% to +50% measurable output quality/user-satisfaction increase. Zero extra skill executions; purely transformation layer (except stage-3 micro-correction LLM call ≤60t).

## 4 Stages — Non-Negotiable Order

### Stage 1 — Completeness Audit (0 tokens, structural)
INPUT: raw skill output
ACTION: Diff against output contract checklist for the skill type:
- **Code output**: valid syntax, imports present, all referenced vars defined, test coverage block, edge-case comments, error handling paths, copy-pasteable block delimiters
- **Writing output**: clear structure (intro/body/conclusion or sections), call-to-action if marketing, specific numbers not vague, links verified, transition phrases, no orphan sentences
- **Config output**: valid YAML/TOML/JSON parse, required keys present, values in documented range, comments explain non-obvious keys, ENV VAR patterns for secrets
- **Plan output**: ordered steps, deadlines/owners where applicable, dependencies mapped explicitly, success criteria testable, rollback plan for risky steps, risk register top 3
ACTION 2: Tag ANY missing checkboxes with `[REFINERY-STAGE1: MISSING=<name>]`
OUTPUT: (audited_output, missing_list [])

### Stage 2 — Correctness Verification (0 or minimal tokens)
INPUT: Stage1 audited output + missing list
ACTION: Run verifier appropriate to output type:
- Code: static syntax (parse tree regex for 5 common langs), type check patterns
- Config: parse check with Python/Ruby/YAML lib (std lib only, no external deps)
- Numbers: math regex check on 2+2, %, currency totals, date sanity (month≤12, dom≤31)
- Links: structural valid URL pattern (no network ping by default, add if `full_verify=true` env flag)
ACTION 2: Tag any verifier failures with `[REFINERY-STAGE2: ERROR=<type> LINE=<#>]` with micro-suggested fix 1-line.
OUTPUT: (verified_output, error_list [])

### Stage 3 — User-Intent Alignment (micro LLM call ≤60 tokens)
INPUT: Stage2 verified_output + original user request
ACTION: LLM ask = "Rate output 0-10 on 1=fully off-topic to 10=fully answered, max 3 bullet fixes". Parse bullets, auto-apply fixes that are 1-line edits (swap sentence, add 1-liner section title, insert missing 1-5 word phrase).
RULE: If LLM score ≤5 → flag and re-run the original skill WITH the intent-alignment bullets as amendment (NOT new skill invocation, reuse existing context)
RULE: If LLM score ≥6 and ≤8 → apply 1-line fixes inline.
RULE: If LLM score ≥9 → pass through unchanged.
COST: ≤60 tokens total per run. 95% sessions adds 10-30 tokens only.
OUTPUT: (aligned_output, intent_score 0-10, fixes_applied N)

### Stage 4 — Polish & Actionability Injection (0 tokens, rule-based)
INPUT: Stage3 aligned_output
ACTION: Apply output-class polish rules:
- Code: add header block with copy/paste command (or install command)
- Long writing: add TL;DR at TOP (3 sentences max, first 3 body SVO triples)
- Plan: add `[NEXT ACTION]` footer line = the 1 step user does RIGHT NOW after reading
- Config: add `[VALIDATED]` footer + parse method 1-liner (e.g., "`python3 -c 'import yaml; yaml.safe_load(open("f"))'`")
- List: add sorting by priority/impact when list is ≥5 items and unordered
RULE: Never add adjective/adverb fluff. Never add emojis to technical output. Never add marketing to technical docs.
OUTPUT: polished_final_output

## Output Wrapper Line
Prepend AFTER [SWEPT ...] if present, else first line:
```
[REFINED STAGES=<1|2|3|4> INTENT_SCORE=<0-10> FIXES_APPLIED=<N> MISSING_ITEMS=<M>]
```

## Integration with Core Stack
- Runs AFTER skill-efficacy-evaluator if score <70 (re-refine after evaluator suggests improvements)
- Runs BEFORE output-minifier (refinery adds structure THEN minifier removes waste)
- Runs AFTER quantum fold observe (refine expanded superposed turn)
- Cross-platform share: stage 1+2 checklists versioned in shared_state so all 21 platforms apply same audit

## Disable String
`SKILL_OUTPUT_REFINERY_DISABLE_FULL_CONFIRM_44444`
