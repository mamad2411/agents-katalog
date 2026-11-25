---
name: good-test-skill
version: 1.0.0
author: test
license: MIT
description: Mock good skill for testing the evaluator. Has clear trigger, iron laws, and verification steps.
metadata:
  type: process
---

# Good Test Skill

A skill that does one thing well.

## Trigger

Use when user asks to do X. NOT for Y or Z.

## Iron Law

Never write code without a failing test first. Write code before test? Delete it.

## Process

1. Write test
2. Watch it fail
3. Write minimal code
4. Verify it passes
   ```bash
   npm test
   ```
5. Refactor

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple" | Simple breaks. Test takes 30s. |
| "I'll test after" | Tests after prove nothing. |

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know | Ask |
