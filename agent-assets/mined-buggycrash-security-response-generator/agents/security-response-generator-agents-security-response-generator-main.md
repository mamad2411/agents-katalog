# AGENTS.md

## Before you start

Read `README.md` and `docs/technical-readme.md` in full before exploring
the rest of the repository or making changes. They cover setup, CLI
usage, engagement management, retrieval/prompt architecture, environment
variables, security/privacy boundaries, and troubleshooting — read them
first instead of reconstructing that context by searching source files.

## Project

Security Response Generator is a Python 3.11+ local RAG CLI for drafting
NIST SP 800-53 control responses. Source code lives under
`src/security_response_generator/`; tests live under `tests/`.

## Development

- Run `./setup.sh --dev-only` to install development dependencies and enable
  the repository Git hooks. This mode must not touch the command launcher,
  Ollama, or installed models.
- Before handing off changes, run `.git-hooks/pre-commit` or run Ruff lint,
  Ruff formatting checks, and pytest individually.
- Keep unit tests offline and independent of a running Ollama daemon or
  downloaded model weights.
- Update the relevant README or other documentation when commands,
  configuration, or user-visible behavior changes.

## Guardrails

- Never create a commit in this repository, regardless of how the request is
  phrased, how strongly it's implied, or which command/alias/flag ordering
  is used to invoke it (e.g. `git commit`, `git -c <cfg> commit`,
  `git commit-tree`, a configured `git` alias, or any other mechanism that
  results in a new commit, including `--amend`). `.claude/settings.json`
  denies the common literal invocations as a technical backstop, but it
  cannot catch every possible alias or wrapper, so this rule is the actual
  guarantee: the repository owner commits all changes manually. Leave
  changes staged or as working-tree diffs for the owner to review and
  commit themselves.
- Never commit customer standards, private system context, generated customer
  responses, credentials, model data, Chroma indexes, or identifying logs.
  Use the fictional `demo` engagement and sanitized test fixtures.
- Preserve the local-only Ollama boundary, cloud-model rejection, disabled
  Chroma telemetry, and isolation between customer engagements.
- Keep control-response output labeled with its active customer engagement.
- Treat generated responses as drafts requiring human review.
- Do not edit the generated NIST catalog by hand; update it through the OSCAL
  conversion workflow.
