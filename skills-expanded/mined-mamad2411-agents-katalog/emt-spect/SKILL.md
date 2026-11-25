---
name: emt-spect
description: "Trigger: /emt-spect, $emt-spect, Spect, SDD. Clarifies requirements interactively, then saves a Spect doc under doc/."
license: MIT
metadata:
  author: gohan-rodolfo
  version: "0.1"
input: "User description: '$ARGUMENTS'"
disable-model-invocation: false
---

# EMT Spect

## Activation Contract

- Use when the user runs `/emt-spect`, `$emt-spect`, or asks for a Spect / SDD document.
- Act as a Spect analyst: understand the request, challenge assumptions, clarify gaps, then produce one focused markdown document.

## Hard Rules

- Do not invent requirements absent from context; list unknowns as open questions.
- Do not save the Spect until the minimum required clarity exists.
- Ask at most one concise clarification question at a time, then stop and wait.
- Give useful product/technical perspective when the request has weak scope, risky assumptions, or missing user value.
- Keep generated content concise; avoid echoing this skill or template text in chat.
- Save the document with the save hook; do not manually create `doc/` unless the hook fails.
- Filename must be kebab-case with `.md`.
- Prioritize user stories as independently testable journeys ordered by importance.

## Decision Gates

| Condition                                                   | Action                                                      |
| ----------------------------------------------------------- | ----------------------------------------------------------- |
| Goal, actor, core workflow, or success criteria are unclear | Ask one clarification question; do not save yet             |
| Scope is too broad or solution-first                        | Push back with the tradeoff, then ask one focusing question |
| Enough context exists for a useful draft                    | Generate the Spect and save it                              |
| Minor unknowns remain                                       | Save the Spect and include them under Open Questions        |

## Execution Steps

1. Read conversation context: stack, architecture, constraints, and `$ARGUMENTS`.
2. Infer the likely feature name, target user, user value, workflow, constraints, risks, and missing information.
3. If a decision gate requires clarification, explain the issue briefly, ask one question, and stop.
4. Once clear enough, draft the final Spect markdown using `assets/spect-template.md` as structure.
5. Run `bash .agents/skills/emt-spect/scripts/save_spect_doc.sh "<feature name>"` and pass the markdown body through stdin.
6. Reply with only the exact saved path plus any unresolved open questions.

## Output Contract

- Saved file: `doc/<feature-kebab-case>.md`
- Response: exact path, no pasted document body.
- Windows requires Git Bash, WSL, MSYS2, or another Bash-compatible shell.

## References

- `assets/spect-template.md` — compact document structure for the saved file.
