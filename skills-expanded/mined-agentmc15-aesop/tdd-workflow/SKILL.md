---
name: tdd-workflow
description: Write a failing test first, then the minimum code to pass it. Use for any bug fix or new behavior.
---

1. Write a test that reproduces the bug or specifies the behavior. Run it; confirm it FAILS.
2. Commit the failing test.
3. Implement the minimum change to make it pass. Run the full suite.
4. Have a separate reviewer check the implementation is not overfitting the test.
