# Manifest

This directory owns the declarative module format, its validation and persistence,
and conversion to executable module definitions.

- `module_factory` edits saved declarations. Discovery and loading own trust,
  dependencies, activation and withdrawal; saving does not activate tools.
- Persistence validates paths and stored declarations. Malformed data and failed
  writes are errors, distinct from an absent manifest.
- Shared step-language utilities serve workflows. Automation orchestration
  belongs to the workflow runtime, not the manifest format.
