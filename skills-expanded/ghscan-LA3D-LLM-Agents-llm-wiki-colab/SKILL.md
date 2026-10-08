---
name: wiki-enroll
description: Prepare or update this project's federation agent card and register its discovery topic. Use when the user wants to enroll this project or maintain its published card.
---

Run from the host project using the installed helper:

```bash
bash "$SKILL_DIRECTORY/scripts/enroll.sh" --help
```

For an automated draft, supply `--non-interactive --dry-run` with a description
and at least one `--capability`, or supply `--card-json` containing the reviewed
structured card. Add `--update` to migrate or edit an existing card. Review the
candidate, then rerun without `--dry-run` within the user's authorized scope.
See [the helper contract](references/enrollment.md) for examples, dependencies,
existing-card updates and publication checks.

The helper derives repository identity from its GitHub origin, not the logged-in
account or local folder name. Use `--repo OWNER/REPO` when an alias or inaccessible
origin prevents detection, and `--wiki-dir PATH` for a nonstandard attachment.
Existing agent and skill IDs remain stable. The filename is always
`Card_<repository-name>.md`, independently of the agent ID. Existing prose and
unrelated frontmatter are preserved. Do not replace a whole existing card with a
new template to resolve a validation error.

The default operation prepares a local card only. `--add-topic` explicitly
requests GitHub topic registration; `--check-remote` checks wiki-origin access.
Neither proves that a card has been published or indexed. The helper prints
commands to stage and commit only the card, then push the wiki. Execute those
publication steps when requested or already authorized. Verify the public index
before reporting the agent as discoverable; adding a topic alone is insufficient
for owners outside the index's allowlist.

During the structured-card rollout, deploy compatible index/fabric readers and
connector clients before publishing new cards. Enrollment source changes do not
upgrade those services. Do not advertise A2A or MCP invocation merely because a
wiki or discovery service exists; retain only reviewed explicit interfaces.
