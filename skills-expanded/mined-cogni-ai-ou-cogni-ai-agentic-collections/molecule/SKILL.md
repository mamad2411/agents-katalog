---
name: molecule
description: >-
  How to run and manage Molecule tests for Ansible roles and playbooks.
  You MUST load this skill when running or managing Molecule tests for Ansible.
license: MIT
---
<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->
# Molecule Testing

## WHEN TO USE

- Agent needs to execute syntax/lint/test checks for Ansible playbooks locally.
- Troubleshooting configuration logic inside devcontainers or codespaces.
- User needs to run or debug Ansible role testing frameworks using Molecule.

## Commands

```bash
# Run Molecule tests
molecule test

# Syntax check
molecule syntax
```

## Devcontainer Guidance

When running Molecule inside GitHub Codespaces or a repository's VS Code devcontainer:

- Treat the repository devcontainer as the default controller environment for local development and testing.
- Keep controller dependency installation in the devcontainer configuration so Molecule scenarios can assume those tools
are already available.
- Do not install controller-side Python dependencies during Molecule runs when the agent is already operating inside
Codespaces or the repo devcontainer.
- Do not create additional Python virtual environments such as `.venv` or `venv`; use the existing container Python
environment, which should already provide the required dependencies.
- If dependencies are missing in a Codespace or devcontainer, update `.devcontainer/requirements.txt` or
`.devcontainer/devcontainer.json` instead of introducing a per-run Molecule install step or a separate virtual
environment.

## Troubleshooting

### Molecule Testing issues

If you encounter problems or hangs during `molecule test`:

- Run molecule using separate commands (e.g., `molecule create`, `molecule converge`, `molecule destroy`)
  to isolate the issue.
- Always use a timeout prefix command when running separate commands to prevent indefinite hangs
  (e.g., `timeout 600s molecule create` for a max of 5-10 minutes).
- If dealing with upstream plugins that have broken conditionals, you may need to temporarily use
  the `ANSIBLE_ALLOW_BROKEN_CONDITIONALS=1` environment variable
  (e.g., `timeout 600s env ANSIBLE_ALLOW_BROKEN_CONDITIONALS=1 molecule create`).

### Ansible Environment issues

- **Ansible missing Python modules:** If a module such as `requests` or `docker` is installed for the main container
  Python but Ansible still cannot import it, check `ansible --version` to identify the interpreter in use. In
  Codespaces/devcontainers, Ansible may run from a pipx-managed environment, so install controller-side libraries there as
  well, for example with `pipx inject ansible -r .devcontainer/requirements-ansible.txt`.
