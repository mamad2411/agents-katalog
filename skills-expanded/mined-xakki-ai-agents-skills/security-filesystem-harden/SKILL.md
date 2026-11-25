---
name: security-filesystem-harden
description: 'Secure filesystem artifacts, bounded reads and lifecycle state against replacement races. Use when local artifacts, archives, markers, locks or runtime state cross a trust boundary. RU: безопасность файловой системы.'
license: MIT
disable-model-invocation: true
---

# Filesystem boundary security

Use when local artifacts, archive inputs, markers, locks or runtime state cross a trust boundary. Define the actual owner, allowed path/source interface, object type, permission and size requirements, concurrency behavior and intended failure result. A pathname is not a stable object identity: a checked path can be replaced before it is reopened or removed.

Where the platform and threat model require it, retain verified directory and file handles, use supported no-follow and handle-relative operations, and validate the opened object rather than relying on a prior path check. Fail closed if a required protection is unavailable. Apply the project’s explicit security contract; do not universally hardcode a single path, exact mode, filesystem type, token format or retention policy.

For [artifact writes and bounded reads](references/artifact-and-input.md), [archive import and evidence](references/archive-import-and-evidence.md), or [local state and ownership](references/lifecycle-state.md), load the applicable reference. Test the actual boundary with synthetic fixtures and safe outside sentinels, proving both rejection and absence of forbidden reads, writes, deletion and downstream actions. Diagnosis does not authorize state cleanup, process termination or takeover.
