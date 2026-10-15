---
name: al-test
description: Creates AL test codeunits for Business Central extensions. Use when the user wants to generate tests for new or existing BC AL functionality.
argument-hint: "[description of functionality to test, acceptance criteria, or test cases]"
---

Create AL tests for the following context: $ARGUMENTS

## Steps

1. **Read the project config** — read `app/app.json` to get the mandatory affix and app object ID range, and `test/app.json` to get the test app object ID range. If either file does not exist, stop and tell the user.

2. **Explore the test directory** — list all `.al` files in `test/`. For each test codeunit found, read it and note:
   - The codeunit name and number
   - The `// [FEATURE]` tag in `OnRun()` to understand what feature area it covers
   - Existing test procedure names to avoid duplication

3. **Decide where to add the tests** — based on the feature area described in `$ARGUMENTS`, determine whether the new tests belong in an existing test codeunit or require a new one:
   - If an existing codeunit covers the same feature area, add the new test procedures to it
   - If no existing codeunit fits, create a new one using the next available ID from the test app's object ID range

4. **Generate the tests** following these conventions:
   - `Subtype = Test; TestPermissions = Disabled;`
   - `OnRun()` contains a single `// [FEATURE] <feature name>` comment
   - Each test procedure has the `[Test]` attribute (and `[HandlerFunctions('...')]` if UI modal handlers are needed)
   - Test procedure names are descriptive and written in plain English (e.g. `PaymentMethodFilterExcludesNonMatchingEntries`)
   - Each test body starts with a `// [SCENARIO]` comment summarising what is being tested
   - Use `// [GIVEN]`, `// [WHEN]`, `// [THEN]` comments to structure the body
   - Extract setup and teardown into `local procedure` helpers — keep test procedure bodies concise
   - Declare variables inside the procedure body, not at codeunit level
   - Use `Assert` codeunit for assertions
   - Use Microsoft Test Library codeunits where appropriate (e.g. `Library - Purchase`, `Library - ERM`, `Library - Variable Storage`) — if a library is used that isn't already a dependency in `test/app.json`, flag it to the user
   - All custom object/field/procedure names must end with the mandatory affix (e.g. `OOO`)
   - Object names must not exceed 30 characters including the affix
   - Captions omit the affix
   - Include `[MessageHandler]` / `[ConfirmHandler]` / `[PageHandler]` stubs at the bottom when needed
   - Preserve the `#region Test References` and `#region Test Stages` comment blocks at the bottom of the file if they exist

5. **Write the output** — use the Edit tool to add to an existing file, or the Write tool to create a new file. New files should follow the naming convention `<FeatureArea>Tests.Codeunit.al` in the `test/` directory.

6. **Summarise** what was created or modified, and list the test procedure names added.
