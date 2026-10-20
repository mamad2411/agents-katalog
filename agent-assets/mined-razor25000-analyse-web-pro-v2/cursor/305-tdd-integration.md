---
description: 
globs: 
alwaysApply: false
---
## Context:

-  Create a component following TDD principles.
-  Create components with full integration tests.
-  You need to FIRST create the integration tests file, sucec.ts, and then generate the code.

## Workflow

0. Search the file and read the code that need to be edited.
0. Plan what you will do, like where the components will be created, the name of the component, etc.
1. Create a test file in the `e2e` folder.
2. Create the component and the page in the correct fo-routes.mdc and all the project's rules.
3. Run the tests with `pnpm test:e2c:ci -g "name-of-the-test"`.
4. Correct the component until the tests pass.

## Debug

* You can use `page.evaluate` to test the content.
* You can use `console.log` inside the page to understand the issues.
* You CAN'T use screenshots.
* You CAN'T use `page.pause()`.

## Important information

* Most of the table is Organization-related and must be created inside /orgs/[orgSlug] folder