---
name: jira-inlinecard-comment
description: Generic protocol for creating, updating, and verifying Jira inlineCard comments via API v2 wiki markup,
with acli-based ADF verification.
category: Jira Operations
---

# Jira InlineCard Comment Skill

Creates, updates, and verifies Jira comments in **inlineCard** format — rich PR links that render as embedded cards in
the Jira UI — using API v2 wiki markup `[url|url|smart-link]`. Also provides ADF comment verification via `acli` JSON
output parsing.

The `acli` plain-text flags (`--body`, `--body-file`) do not render inlineCards; use this skill's REST API v2 path or
`acli`'s ADF option (`comment update --body-adf <file>`).

***

## 1. Environment & Dependencies

| Tool | Purpose | Verification |
| --- | --- | --- |
| `python3` (3.12+) | Script engine | `python3 --version` |
| `curl` | API calls (fallback / diagnostic) | `curl --version` |
| `acli` | Comment listing for verification | `acli jira workitem comment list --key TEST --limit 1` |

### 1.1 Token Retrieval

Jira API tokens are stored in a local `<key-file>` file. To retrieve a token:

```bash
# By label pattern (returns first matching line's token)
TOKEN=$(grep -A1 "Jira <user>" /path/to/<key-file> | tail -1)

# By line number
TOKEN=$(sed -n '51p' /path/to/<key-file>)
```

The script uses `JIRA_SITE`, `JIRA_EMAIL`, and `JIRA_TOKEN` environment variables. Set them before invocation:

```bash
export JIRA_SITE="<corp-domain>.atlassian.net"
export JIRA_EMAIL="<author>@<corp-domain>.com"
export JIRA_TOKEN="$(grep -A1 'Jira' /path/to/<key-file> | tail -1)"
```

***

## 2. Wiki Markup Format for InlineCard

The Jira API v2 REST endpoint accepts **wiki markup** in the `body` field. To render a URL as an inlineCard (embedded PR
card), use this format:

```text
[{url}|{url}|smart-link]
```

With an optional prefix label and description:

```text
PR{N}: [{url}|{url}|smart-link] - {description}
```

**Example:**

```text
PR<N>: [https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|smart-link] - <DESCRIPTION>
```

This format is Jira Cloud-specific. Do NOT use ADF JSON in the `body` field for API v2 — only wiki markup renders
inlineCard correctly.

***

## 3. Create InlineCard Comment

### 3.1 Using the Script

```bash
python3 scripts/jira-inlinecard.py create \
  --key <TICKET-ID> \
  --url "https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>" \
  --label "PR<N>" \
  --description "<DESCRIPTION>"
```

The script outputs the full API response JSON including the new comment ID.

### 3.2 Using curl Directly

```bash
curl -X POST "https://<corp-domain>.atlassian.net/rest/api/2/issue/<TICKET-ID>/comment" \
  -u "<email>:<token>" \
  -H "Content-Type: application/json" \
  -d '{"body":"PR<N>: [https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|smart-link] - <DESCRIPTION>"}'
```

### 3.3 Response

A successful create returns JSON with the `id` field. Record this ID for future updates:

```json
{
  "id": "14587",
  ...
}
```

***

## 4. Update Existing InlineCard Comment

### 4.1 Using the Script

```bash
python3 scripts/jira-inlinecard.py update \
  --key <TICKET-ID> \
  --id <COMMENT-ID> \
  --url "https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>" \
  --label "PR<N>" \
  --description "<DESCRIPTION>"
```

### 4.2 Using curl Directly

```bash
curl -X PUT "https://<corp-domain>.atlassian.net/rest/api/2/issue/<TICKET-ID>/comment/<COMMENT-ID>" \
  -u "<email>:<token>" \
  -H "Content-Type: application/json" \
  -d '{"body":"PR<N>: [https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>|smart-link]"}'
```

***

## 5. ADF Comment Verification

After creating inlineCard comments, verify they rendered correctly by listing comments and parsing the ADF JSON:

### 5.1 Verify a Single Issue

```bash
python3 scripts/jira-inlinecard.py verify --key <TICKET-ID>
```

This calls `acli jira workitem view <TICKET-ID> --fields comment --json` and parses the `fields.comment.comments[]`
ADF bodies for `type: "inlineCard"` nodes (recursively), returning their URLs.

To check for specific PR numbers:

```bash
python3 scripts/jira-inlinecard.py verify --key <TICKET-ID> --pr-nums <PR-NUMBER>
```

### 5.2 Verify Multiple Issues (Batch)

```bash
python3 scripts/jira-inlinecard.py verify-batch \
  --tickets <TICKET-ID-A>,<TICKET-ID-B>,<TICKET-ID-C> \
  --pr-map "<TICKET-ID-A>=<PR-NUMBER-X>;<TICKET-ID-B>=<PR-NUMBER-Y>,<PR-NUMBER-Z>;<TICKET-ID-C>=<PR-NUMBER-W>"
```

### 5.3 Manual Verification

```bash
acli jira workitem view <TICKET-ID> --fields comment --json
```

The ADF output contains inlineCard nodes like:

```json
{
  "type": "inlineCard",
  "attrs": {
    "url": "https://github.com/<ORG>/<REPO>/pull/<PR-NUMBER>"
  }
}
```

Verify that:

- Each expected PR URL appears as an `inlineCard` node
- No duplicate inlineCard entries for the same PR
- The label text (e.g. `PR3:`) appears as a `text` node immediately before the inlineCard

***

## 6. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| *(none registered)* | |

Composers SHOULD invoke `scripts/jira-inlinecard.py` with appropriate subcommands and pass authentication via
environment variables (`JIRA_SITE`, `JIRA_EMAIL`, `JIRA_TOKEN`).

***

## Related Skills

- [`jira-acli-operations`](../jira-acli-operations/SKILL.md) — CLI-based comment operations (plain text only; does not
produce inlineCard)
- [`jira-automation-rules`](../jira-automation-rules/SKILL.md) — Jira Cloud automation rule construction

***

## Related Conversations & Traceability

- **Session 2026-06-09**: `<TICKET-ID>` inlineCard comment creation and ADF verification. Protocol for converting plain-text
PR links to smart-link inlineCard format via API v2 wiki markup.
- **Session 2026-10-09**: verify/verify-batch fixed for acli 1.3.39 — `comment list` has no `--fields` flag; switched to
`workitem view --fields comment --json` with recursive inlineCard traversal.
