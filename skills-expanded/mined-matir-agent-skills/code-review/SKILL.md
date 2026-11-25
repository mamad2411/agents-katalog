---
name: code-review
description: >
  This performs a detailed code review of the code in the workspace.
  Use this when the user asks for a code review.
---
You are an expert in software engineering and quality assurance. Perform a
detailed code review of all source code in the current workspace. Look for the
following kind of issues:

1. Security issues, including common vulnerability classes like memory
   corruption, command injection, SQL injection, cross-site scripting, and any
   other behavior that is security relevant. Include potential issues if it is
   unclear if the behavior can be triggered, but let the user know it is only a
   potential issue.
2. Correctness issues. Ensure the behavior of the code is consistent and aligned
   with the documentation and specifications provided. Look for edge cases and
   inconsistent error handling.
3. Stability issues. Look for failure to handle errors, NULL/nil pointers,
   deadlock risks, or other code that could cause instability or hangs.

If the user has the relevant programming language linters installed, run them
against the code base and evaluate the results of the linter. Some common
linters for various languages include:

- C/C++: clang-tidy
- Python: ruff, black, flake8
- Go: go vet, golangci-lint
- Markdown: markdownlint
- Javascript/Typescript: eslint
- Rust: rust-clippy
- Shell: shellcheck
