---
name: gh-discussion-replier
description: Professional English replier for GitHub Discussions. Use when a feature request is implemented, a question is answered, or community engagement is needed. Automates replying via the GitHub GraphQL API.
---

# Gh Discussion Replier

## Overview

The `gh-discussion-replier` skill enables posting professional English replies to GitHub Discussions. Unlike issues, discussions use the GraphQL API for both reading and posting. This skill handles the full workflow: fetching context, checking star status, composing a reply, and posting.

## Workflow

1. **Identify the Discussion**: Get the discussion number (e.g., #66) and URL.
2. **Fetch Discussion Content**: Use GraphQL to get the title, body, author, and category.
3. **Check Star Status**: Run the bundled script to check if the author has starred the repo.
   * Command: `bash .github/skills/gh-discussion-replier/scripts/check_discussion_star.sh <discussion_number>`
   * Interpretation:
     * Exit code **0**: User has starred. Use "Already Starred" templates.
     * Exit code **1**: User has NOT starred. Include "Star Request" in the reply.
4. **Select a Template**: Load [references/templates.md](references/templates.md) to choose a suitable response pattern based on the discussion category (Ideas, Q&A, General, Show and tell).
5. **Draft the Reply**: Compose a concise message based on star status and template.
6. **Post the Comment**: Use the GraphQL `addDiscussionComment` mutation (see below).

## Tool Integration

### Fetch Discussion Content

```python
import subprocess, json

def get_discussion(owner, repo, number):
    query = '''
    query($owner:String!, $repo:String!, $number:Int!) {
      repository(owner:$owner, name:$repo) {
        discussion(number:$number) {
          id title body
          author { login }
          category { name }
          comments(first:10) { nodes { body author { login } } }
        }
      }
    }
    '''
    r = subprocess.run(['gh', 'api', 'graphql',
        '-f', f'query={query}',
        '-f', f'owner={owner}',
        '-f', f'repo={repo}',
        '-f', f'number={number}'],
        capture_output=True, text=True)
    return json.loads(r.stdout)['data']['repository']['discussion']
```

### Check Star Status

```bash
bash .github/skills/gh-discussion-replier/scripts/check_discussion_star.sh <discussion_number>
```

### Post Reply Comment

```python
import subprocess, json

def post_discussion_reply(discussion_node_id, body):
    mutation = '''
    mutation($body:String!, $discussionId:ID!) {
      addDiscussionComment(input:{body:$body, discussionId:$discussionId}) {
        comment { id url }
      }
    }
    '''
    r = subprocess.run(['gh', 'api', 'graphql',
        '-f', f'query={mutation}',
        '-f', f'body={body}',
        '-f', f'discussionId={discussion_node_id}'],
        capture_output=True, text=True)
    return json.loads(r.stdout)
```

### Full Workflow Example

```python
import subprocess, json

OWNER = "Fu-Jie"
REPO = "openwebui-extensions"

# 1. Get discussion
disc = get_discussion(OWNER, REPO, 66)
disc_id = disc['id']
author = disc['author']['login']
category = disc['category']['name']
print(f"#{66} [{category}] by @{author}: {disc['title']}")

# 2. Check star
star_result = subprocess.run(
    ['bash', '.github/skills/gh-discussion-replier/scripts/check_discussion_star.sh', '66'],
    capture_output=True, text=True)
has_starred = star_result.returncode == 0

# 3. Compose reply (select template based on category and star status)
body = "Your reply here..."
if not has_starred:
    body += "\n\nIf you find this helpful, a star on [openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions) would be much appreciated! ⭐"

# 4. Post
result = post_discussion_reply(disc_id, body)
print(f"Posted: {result['data']['addDiscussionComment']['comment']['url']}")
```

## Discussion Categories & Tone

| Category | Tone | Typical Action |
|----------|------|---------------|
| **Ideas** | Appreciative, solution-oriented | Acknowledge or announce implementation |
| **Q&A** | Helpful, educational | Answer with technical detail |
| **General** | Warm, conversational | Follow up or redirect |
| **Show and Tell** | Enthusiastic, curious | Acknowledge, ask if feature-worthy |

## Guidelines

- **Language**: ALWAYS use English for the comment body, even if the system prompt or user conversation is in another language.
- **Tone**: Warm, professional, and community-oriented. Discussions are conversations, not tickets.
- **Precision**: When announcing a fix or feature, mention the specific version and briefly describe what was added.
- **Star Request**: Always include a gentle star request if the user has NOT starred the repo. Skip it if they already have.
- **Irreversibility**: Discussion replies cannot be deleted via CLI. **Always confirm the reply content with the user before posting.**
