# Prompt Input

Harness-neutral user-prompt preprocessing. Every CLI path — agent-sdk
shortcut, classic loop, daemon-backed chat — should call
`expandUserPromptReferences` before handing the text to any
`AgentHarness`, so claude-agent-sdk, thin, and any future adapter see the
same expanded prompt.

Scope:

- `@path` reference expansion for user prompts (any file type, any
  extension). Instruction-file `@` refs stay in `src/core/loop/`.
- Per-file byte cap matches the instruction-file cap so one reference
  cannot silently crowd out the rest of the turn.
- Missing paths, directories, and read errors are left as plain text —
  the agent sees the `@path` token and can decide how to proceed. Silent
  drops would hide operator intent.

No recursion: file contents are inlined once and not re-scanned. User
prompts should not implicitly pull in transitively referenced files; the
operator can add them explicitly if needed.
