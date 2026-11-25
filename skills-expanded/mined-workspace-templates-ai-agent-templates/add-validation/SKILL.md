---
name: add-validation
description: Adds request validation to a handler using the validation library your project already uses, with tests for bad input.
disable-model-invocation: true
---

Add request validation to: $ARGUMENTS

1. Read the handler and list every value it takes from the body, query, params and headers, with the type and limits the code assumes.
2. Find the validation library already in the dependencies and copy how an already validated handler uses it (where the schema lives, how errors are mapped). Never add a second library.
3. Write the schema: required versus optional, string length caps, numeric ranges, enums, email or UUID formats, and reject unknown keys when the project does so elsewhere.
4. Run it before any logic, and return the project's standard 400 shape with the field name in each message.
5. Use the parsed value afterwards, not the raw request.
6. Add tests: valid input, each missing required field, wrong types, boundary values, and an extra unknown field.
7. Run tests and lint.

Report each rule you added and why, and mark any limit you had to guess so I can confirm it. Do not change what valid requests return.
