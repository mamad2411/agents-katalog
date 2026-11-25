# service-harness

Harness packages model context from material supplied by the runtime and keeps
explicit agent-authored memory. It provides inspection evidence for what was
included in an inference context.

## Service Functions

- `harness_ComposeContext`: pass resolved plugin material, runtime facts, and
  session history to construct a bounded context package and store its report.
- `harness_GetContextReport`: inspect a context package by report ID.
- `harness_StreamContextReports`: inspect recent reports for a session.
- `harness_PutMemory`: store only a memory the agent explicitly decided to
  retain, including provenance.
- `harness_GetMemory`, `harness_SearchMemory`, `harness_DeleteMemory`: read,
  find, or remove explicit memory records.

## Boundary

- Pass prompt material sourced from installed agent, tool, or service plugins.
- Runtime facts may report active work or approved policy state; they are not
  service-authored instructions.
- Harness does not invoke models, tools, or other services.
- Memory is explicit state, not a hidden copy of chat history or documents.
