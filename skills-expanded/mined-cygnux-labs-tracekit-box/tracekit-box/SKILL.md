---
name: tracekit-box
description: >
  Run an AI agent's job or untrusted code in a Tracekit Box micro-VM on Linux: no network card, an allowlist for
  every connection, secrets that never enter the VM, changes returned as a patch, and a signed record of everything
  that crossed. USE WHEN: running untrusted code, an agent job or a CI task that needs real credentials, network access
  or repository changes, where you must contain it and prove afterwards what it did. NOT FOR: macOS or Windows hosts
  without a Linux VM, or jobs that need a full network.
---

# Run a job in Tracekit Box

1. **Check the host.** `test -r /dev/kvm -a -w /dev/kvm` must succeed (Linux with KVM). `tkbox version` and
   `tracekit --version` (1.4.2 to 1.5.3 tested) must work. If the signer isn't running:
   `tracekit init --dev --v2 --no-hooks && tracekit up --wait`. If `tkbox ls` fails, no daemon is answering: start
   `tkbox daemon` in the background and wait until `tkbox ls` works.
2. **Create the box with the least it needs.** Name the image, only the hosts or presets the job needs (`--allow`),
   and each secret bound to the one host that should receive it:
   `tkbox run --name JOB --image IMAGE --allow PRESETS --workspace . --secret NAME=env:VAR@HOST`.
   Never put a secret's value on the command line or in the workspace: `--secret` takes only an `env:` or `file:`
   source, a command that holds a value is refused, and so is a box whose workspace has a file holding one.
3. **Run commands** with `tkbox exec JOB -- CMD`. A host off the allowlist is held (or, with `inspect: all`, refused at
   once): tell the person to run `tkbox approvals` and `tkbox approve <id>` on the host. Don't try to route around a
   hold or a refusal; each one says what to do.
4. **Bring the changes back.** `tkbox stop JOB`, then `tkbox diff JOB` to review, then `tkbox apply JOB` (before
   export), which decides each file before writing it. Sensitive paths such as `.github/workflows/**` need the person's
   `--allow-sensitive`.
5. **Prove it.** `tkbox export JOB -o JOB.tkb`, then `tracekit verify JOB.tkb --trust JOB.trust.json`. Report its
   `Integrity:`, `Assurance:` and `isolation:` lines as printed: a dev signer (no witness) gives `Assurance: dev`.

Limits: a secret value under 6 bytes is not redacted from responses, blocked in requests or looked for in workspace
files. The full list is in https://github.com/Cygnux-Labs/tracekit-box/blob/main/docs/limits.md.
