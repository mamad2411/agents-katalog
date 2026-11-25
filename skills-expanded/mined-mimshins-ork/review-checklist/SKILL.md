---
name: review-checklist
description: The checklist reviewers in the software-factory example go through before they report. Use when reviewing a branch for security, user experience or code quality.
---

# Review checklist

Go through the parts that match your role, then report.

## Every review

- Read the spec first; review the branch against it, not against what you
  would have built.
- Run the project's own checks (tests, lint, types) and say whether they pass.
- Report `pass` only when you would merge it as is. Otherwise report
  `changes_requested` with each change as one concrete line: the file, what is
  wrong, and what to do instead.

## Security

- Input from users, files or the network is validated before use.
- No secret, token or personal data is written to code, logs or commits.
- New dependencies are pinned and needed.

## User experience

- Every new message, label and error says what happened and what to do next.
- The change works with the keyboard and at narrow widths, where it has a UI.

## Code

- The change is the smallest one that meets the spec, and reads like the code
  around it.
- New behaviour has a test that fails without it.
