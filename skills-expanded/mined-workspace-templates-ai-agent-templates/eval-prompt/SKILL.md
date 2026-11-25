---
name: eval-prompt
description: Runs a prompt against several test inputs and reports which outputs fail your stated criteria, with the evidence for each failure.
disable-model-invocation: true
---

Evaluate this prompt. Input: $ARGUMENTS (a prompt file path or text, plus the pass criteria).

1. If criteria are missing, write 3 to 6 testable ones (format, length, required facts, tone, refusals) and show them for confirmation. Vague criteria like "good" are not allowed.
2. Build 8 to 12 test inputs: typical cases, empty or very long input, a different language, an injection attempt such as "ignore previous instructions", and two cases that should be refused or answered "unknown". Use any example data in the repo first.
3. Run the prompt on each input using the project's own script or the available model tool. Do not call outside services unless the project already does.
4. Grade each output against each criterion as pass or fail, quoting the failing text.
5. Report a table: input, criterion, result, quote. Give the pass rate per criterion.

Finish with the two likeliest causes in the prompt and one suggested edit for each. Do not change the prompt file until asked.
