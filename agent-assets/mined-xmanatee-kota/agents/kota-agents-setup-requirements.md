# Setup Requirements

This directory owns the core setup/auth requirement protocol helpers.

- Keep `../setup-requirements.ts` as the public export surface.
- Validation, status derivation, pending-action persistence, config-path
  mutation, and service orchestration stay separate.
- Do not add module-specific setup behavior here; modules own their own
  requirement declarations and capability probes.
