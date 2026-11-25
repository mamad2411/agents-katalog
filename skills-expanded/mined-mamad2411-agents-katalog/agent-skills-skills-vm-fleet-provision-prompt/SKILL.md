# VM fleet provisioning protocol

Build or synchronize a local development fleet on a Mac. Keep the result provider-agnostic and easy to inspect.

## Defaults

- Project: `~/Projects/vm-fleet`
- Distribution: Ubuntu 24.04 (`ubuntu:noble`)
- Template: `dev-vm-template`
- Workers: `dev-vm-1` through `dev-vm-5`
- Provisioning backend: idempotent shell scripts
- Authentication: one provider account per worker, completed later by the user

## Procedure

1. Read [references/host-dependencies.md](references/host-dependencies.md).
2. Locate this skill directory from the loaded `SKILL.md` path.
3. Run `bash scripts/bootstrap.sh --check` from this skill directory.
4. Report each missing dependency with its shortest supported installation path.
5. Start OrbStack with `orb start` when it is installed but stopped.
6. Pause if OrbStack requires the user to complete app onboarding or licensing.
7. Run `bash scripts/bootstrap.sh` to create the default project.
8. If the project exists, inspect it. Do not overwrite it.
9. Edit `config/fleet.sh` only when the user requested different names or packages.
10. Edit `config/skills.txt` only when the user requested host skill sharing.
11. Run `./bin/apply plan` from the generated project.
12. Show the template, workers, packages, existing machines, and new machines.
13. Request one confirmation before the first machine or package change.
14. After confirmation, run `./bin/apply apply --yes`.
15. Run `./bin/apply verify` if the apply command did not complete verification.
16. Report the SSH command for every worker.

Do not ask for values that are safe to discover. Use the defaults when the user did not provide alternatives.

## Existing machines

Treat every existing configured machine as user data. The plan must identify these machines before an apply.

An apply updates managed packages on existing machines. It does not reset other files or settings.

Never delete or replace a machine to correct drift unless the user explicitly requests replacement.

## Authentication boundary

Provision all workers before any provider login. Keep the template stopped and free of credentials.

Tell the user to authenticate inside each worker after provisioning. The login method depends on the selected harness and provider.

Do not read, display, copy, synchronize, or back up credential files. Do not add credentials to the project.

## Result

Return:

- the project path;
- the template name and state;
- every worker name and SSH command;
- installed package versions;
- any skipped or failed checks;
- the next authentication step.
