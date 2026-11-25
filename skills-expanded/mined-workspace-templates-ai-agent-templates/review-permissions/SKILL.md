---
name: review-permissions
description: Reviews roles, scopes and access lists in a config or manifest and proposes a trimmed version that keeps only what is used.
disable-model-invocation: true
---

Review the permissions in: $ARGUMENTS

1. Read the file and list every grant: IAM actions and resources, Kubernetes verbs and resources, OAuth scopes, GitHub Actions `permissions:`, Android or extension manifest permissions, database roles.
2. Flag wildcards (`*`), admin-level grants, broad resources, long-lived tokens, and anything that allows writing where reading would do.
3. Search the code and scripts for what each grant is used for. Mark each as used, unused or unclear.
4. Propose a minimal replacement: narrower actions, specific resources, read-only where possible, short-lived credentials. Keep the original format.
5. For every removal, state what could break and how to test it.
6. Do not apply anything, and never run commands that change live cloud or cluster state.

Report a table: grant, used, risk, proposed change. Show the trimmed file as a diff. Then ask whether to write it to disk.
