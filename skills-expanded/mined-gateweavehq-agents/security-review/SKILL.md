---
name: security-review
description: Look for security problems in a change, such as unvalidated input, missing authorization checks and leaked secrets. Use when asked for a security review or when a change touches authentication, permissions or untrusted input.
---

# Security review

Go through the change with these questions, and read the surrounding code, not only the diff.

- **Input.** Where does untrusted data enter? Is it validated at that boundary, and is it ever
  used in a query, a shell command, a file path, a URL or HTML without escaping?
- **Authorization.** Does every new route, function or message check who is asking and whether
  they may? Can one user reach another user's data by changing an id?
- **Secrets.** Are tokens, keys or passwords written to files, logs, error messages, or
  returned to the client? Are they read from the environment?
- **Data.** Is personal or sensitive data stored, sent or logged that did not need to be?
- **Dependencies.** Is a new dependency needed, maintained and pinned?
- **Failure.** What happens on bad input or a failing service? Does it fail closed?

Report each finding with the file and line, how it could be abused, and a fix, most serious
first. If you find nothing, say what you checked.
