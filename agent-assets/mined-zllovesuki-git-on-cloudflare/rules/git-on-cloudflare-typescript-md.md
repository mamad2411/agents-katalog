---
trigger: always_on
---

1. Avoid using `as any`, `unknown`, or unnecessary type casting unless absolute necessary. Always use types correctly in TypeScript.
2. Whenever the bahavior/signature of a function/class/etc changes, be sure to update the associated JSDoc/comments, README, and/or markdown documentations to reflect the change.
3. When an existing behavior/signature of a function/class/etc changes, the tests should be updated to avoid breaking changes, or introduce new tests if the behavior is newly introduced.
