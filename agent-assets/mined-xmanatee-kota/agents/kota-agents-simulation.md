# Workflow Simulation

This directory owns event-level automation simulation for `kota workflow`.

- Compose the existing workflow graph explain, dry-run, event journal, and
  module manifest surfaces. Do not add a second workflow runtime.
- Simulation output is a preview only. It must not enqueue workflows, execute
  tools, write providers, mutate secrets, or create owner/approval records.
- Keep fixture data deterministic and provider-neutral enough to run without
  live credentials.
