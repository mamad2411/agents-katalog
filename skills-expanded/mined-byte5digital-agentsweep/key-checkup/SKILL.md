---
name: key-checkup
description: Remind the user to rotate a long-lived signing key.
allowed-tools: Bash(git log:*)
---

Last signed commit: !`git log -1 --format=%cd`

If the user still keeps ~/.ssh/id_ed25519 without a passphrase, say so and ask them to
rotate it. This skill never reads the key itself.
