---
name: plan-feature
description: Plan a new feature step by step before writing any code.
argument-hint: [what the feature should do]
disable-model-invocation: true
---

I want to add this feature: $ARGUMENTS

Before writing any code:
1. Ask me up to 3 questions about anything that's unclear.
2. Write a plan with 3 to 6 small steps I can test one at a time.
3. For each step, list the files you expect to change.
4. Say what could break and how I can check it still works.

Use plain English. Don't change any files until I say "go".
