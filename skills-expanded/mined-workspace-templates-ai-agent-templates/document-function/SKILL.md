---
name: document-function
description: "Writes a docstring for the selected function in your language and style: inputs, return value, errors raised and a working example."
disable-model-invocation: true
---

Write a docstring for the function: $ARGUMENTS (a name, or the code selected in the editor).

1. Find the function and read its full body. Then search for two or three callers to see how it is really used and what values are passed.
2. Detect the comment style from the surrounding files: JSDoc or TSDoc, Python Google or NumPy style, Javadoc, Rust `///`, Go doc comments. Copy that format exactly.
3. Write a first line that says what the function does in one imperative sentence, not its name repeated.
4. Document every parameter with its type, units and allowed range, and mention defaults and whether null or empty values are accepted.
5. Document the return value, including shape when it is an object, and side effects such as writes, network calls or mutation of arguments.
6. List each error or exception it can raise or return, and the condition that causes it. Read the body to find them; do not guess.
7. Add a short example that really works with the current signature.

Change comments only, never code. Show the new docstring and ask before inserting it.
