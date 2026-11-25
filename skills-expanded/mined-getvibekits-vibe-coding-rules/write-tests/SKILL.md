---
name: write-tests
description: Write simple tests for one file or function and run them.
argument-hint: [file or function]
disable-model-invocation: true
---

Write tests for: $ARGUMENTS

1. Look at how tests are already written in this project and match that style.
   If there are no tests yet, tell me which test tool you'd use and why, and wait for my OK.
2. Cover the normal case, one empty or missing input, and one bad input.
3. Run the tests and show me the result.
4. If a test fails because of a real bug, tell me. Don't change the code under test without asking.
