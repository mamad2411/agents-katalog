---
name: pre-output-review
description: "ALWAYS apply before delivering: code, explanations, plans, analyses, documents, commands, designs, reviews, or any artifact the user will act on or read. Review the planned output against a quality checklist; revise until all items pass; deliver only the final approved content. Do NOT trigger for: single-word acknowledgements, yes/no answers, clarifying questions, or echoing back what the user said. When in doubt whether a response warrants review, apply the checklist — the overhead is negligible."
metadata:
  category: meta
  version: "1.0"
---

# Pre-Output Review

Gates every substantive response through a quality checklist; fixes any failures silently before delivering the final output.

## Purpose

Ensure every substantive response is complete, correct, scoped, and secure before it reaches the user by running a mandatory self-review loop.

## Trigger

Apply before delivering any:
- Code (new files, edits, snippets, commands)
- Explanations, analyses, or technical answers
- Plans, designs, architectures, schemas
- Documents, reports, reviews, checklists
- Any artifact the user will act on or read

Do NOT trigger for:
- Single-word or one-line confirmations ("Done", "Sure", "OK")
- Yes/no answers to direct questions
- Asking the user a clarifying question
- Echoing back what the user said

## Prerequisites

None — no tools or environment required.

## Steps

1. **Draft the response** — compose the full response mentally before outputting anything; do not stream partial output during the review phase

2. **Run the quality checklist** — check every item in the Checklist below against the draft; mark each as Pass or Fail

3. **Fix all failures** — revise the draft to address every failed item; do not skip or defer any

4. **Re-run the checklist** — repeat Step 2 on the revised draft; continue the fix → re-check loop until every item passes

5. **Deliver the final output** — output only the reviewed and approved content; never show the checklist or review process to the user unless they explicitly ask to see it

## Checklist

### Completeness
- [ ] Every part of the user's request is addressed — nothing silently skipped
- [ ] If the request had sub-questions, each is answered

### Correctness
- [ ] No invented APIs, libraries, function signatures, or CLI flags that don't exist
- [ ] No factual claims made without basis in the conversation or known knowledge
- [ ] Code: syntactically valid for the target language
- [ ] Commands: flags and arguments are valid for the tool version in context

### Scope
- [ ] No features, refactors, or improvements added beyond what was asked
- [ ] No unnecessary files created or existing files modified beyond the request
- [ ] If the task was ambiguous, one interpretation was chosen and stated — not both implemented silently

### Format
- [ ] Code is inside a fenced code block with the correct language tag
- [ ] File paths are correct relative to the workspace
- [ ] Markdown is valid and renders cleanly (no unclosed backticks, no broken tables)
- [ ] Response length matches the complexity of the request — not padded, not truncated

### Security
- [ ] No hardcoded credentials, API keys, tokens, or passwords in any output
- [ ] No shell commands constructed from unvalidated user input
- [ ] No SQL or code that introduces injection vulnerabilities
- [ ] File operations are scoped to the intended directory

### Consistency
- [ ] Output is consistent with earlier decisions and context in this conversation
- [ ] Variable names, function names, and terminology match the existing codebase style
- [ ] No contradictions introduced relative to a previous response in the same session

## Output Format

File path: none (the reviewed output is delivered inline to the user)

The final output is the response itself — no review artifacts, no checklist output, no "I have reviewed this and...". The user sees only the finished, approved result.

```
<the final approved response — clean, complete, and passing all checklist items>
```

## Rules

### Must
- Run the full checklist on every substantive output — no items may be skipped
- Fix every failed item before delivering — never deliver with known failures
- Repeat the fix → re-check loop until all items pass
- Deliver only the final approved output — the review process is internal
- If a Completeness or Correctness item cannot be resolved (e.g. information is genuinely unknown), state the limitation explicitly in the response rather than guessing
- When uncertain whether a response is substantive enough to warrant review, apply the checklist anyway — the cost is negligible and the risk of skipping is not

### Never
- Never output partial or unreviewed content to the user
- Never invent facts, APIs, or library functions to fill a gap — state the uncertainty instead
- Never add scope beyond what was asked even if the addition seems helpful
- Never show the checklist or review loop output to the user unless explicitly asked
- Never treat checklist items as optional — all must pass before delivery

## Examples

### Good Example

User asks: "Write a Python function to read a JSON file."

Internal review (not shown to user):
```
Completeness: ✓ function requested → provided
Correctness:  ✓ json.load() is valid Python stdlib; try/except is correct
Scope:        ✓ only the function, no extra utilities added
Format:       ✓ code block with python tag
Security:     ✓ no credentials; file path from argument, not hardcoded
Consistency:  ✓ no prior context to contradict
→ ALL PASS
```

Output to user:
```python
import json

def read_json(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
```

### Bad Example

User asks: "Write a Python function to read a JSON file."

Output to user:
```python
import json

def read_json(file_path):
    data = json.loads(file_path)  # BUG: loads() parses a string, not a file
    return data

# I also added a write_json helper you might find useful:
def write_json(data, path):
    ...
```

> Why this is bad: `json.loads()` is wrong (parses a string, not a file path) — Correctness failed. `write_json` was not asked for — Scope failed. Neither failure was caught before delivery because no review was run.
