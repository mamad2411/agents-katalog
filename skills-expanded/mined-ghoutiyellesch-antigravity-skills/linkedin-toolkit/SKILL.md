---
name: linkedin-toolkit
description: Consolidated toolkit for linkedin. Covers linkedin-cli, linkedin-automation
---
# Linkedin Toolkit

## Core Capabilities
# Linkedin Toolkit

## When to Use

Use this skill when you need to automate LinkedIn tasks such as profile fetching, connection management, or post creation via CLI, especially when integrated into automated workflows.

# LinkedIn Skill

You have access to `linkedin` – a CLI tool for LinkedIn automation. Use it to fetch profiles, search people and companies, send messages, manage connections, create posts, react, comment, and more.

Each command sends a request to Linked API, which runs a real cloud browser to perform the action on LinkedIn. Operations are **not instant** – expect 30 seconds to several minutes depending on complexity.

If `linkedin` is not available, install it:

```bash
npm install -g @linkedapi/linkedin-cli
```

## Authentication

If a command fails with exit code 2 (authentication error), ask the user to set up their account:

1. Go to [app.linkedapi.io](https://app.linkedapi.io) and sign up or log in
2. Connect their LinkedIn account
3. Copy the **Linked API Token** and **Identification Token** from the dashboard

Once the user provides the tokens, run:

```bash
linkedin setup --linked-api-token=TOKEN --identification-token=TOKEN
```

## When to Use

Use this skill when you need to **orchestrate LinkedIn actions from scripts or an AI agent** instead of clicking through the web UI:

- Building outreach, research, or recruiting workflows that rely on LinkedIn data and messaging.
- Enriching leads or accounts by fetching people and company profiles in bulk.
- Coordinating multi-step Sales Navigator or workflow runs where JSON output and exit codes are required.

Always respect LinkedIn’s terms of service, local regulations, and your organisation’s compliance policies when using automation against real accounts.

## Global Flags

Always use `--json` and `-q` for machine-readable output:

```bash
linkedin <command> --json -q
```

| Flag                    | Description                             |
| ----------------------- | --------------------------------------- |
| `--json`                | Structured JSON output                  |
| `--quiet` / `-q`        | Suppress stderr progress messages       |
| `--fields name,url,...` | Select specific fields in output        |
| `--no-color`            | Disable colors                          |
| `--account "Name"`      | Use a specific account for this command |

## Output Format

Success:

```json
{ "success": true, "data": { "name": "John Doe", "headline": "Engineer" } }
```

Error:

```json
{
  "success": false,
  "error": { "type": "personNotFound", "message": "Person not found" }
}
```

Exit code 0 means the API call succeeded – always check the `success` field for the action outcome. Non-zero exit codes indicate infrastructure errors:

| Exit Code | Meaning                                                                                     |
| --------- | ------------------------------------------------------------------------------------------- |
| 0         | Success (check `success` field – action may have returned an error like "person not found") |
| 1         | General/unexpected error                                                                    |
| 2         | Missing or invalid tokens                                                                   |
| 3         | Subscription/plan required                                                                  |
| 4         | LinkedIn account issue                                                                      |
| 5         | Invalid arguments                                                                           |
| 6         | Rate limited                                                                                |
| 7         | Network error                                                                               |
| 8         | Workflow timeout (workflowId returned for recovery)                                         |

## Commands

### Fetch a Person Profile

```bash
linkedin person fetch <url> [flags] --json -q
```

Optional flags to include additional data:

- `--experience` – work history
- `--education` – education history
- `--skills` – skills list
- `--languages` – languages
- `--posts` – recent posts (with `--posts-limit N`, `--posts-since TIMESTAMP`)
- `--comments` – recent comments (with `--comments-limit N`, `--comments-since TIMESTAMP`)
- `--reactions` – recent reactions (with `--reactions-limit N`, `--reactions-since TIMESTAMP`)

Only request additional data when needed – each flag increases execution time.

```bash
# Basic profile
linkedin person fetch https://www.linkedin.com/in/username --json -q

# With experience and education
linkedin person fetch https://www.linkedin.com/in/username --experience --education --json -q

# With last 5 posts
linkedin person fetch https://www.linkedin.com/in/username --posts --posts-limit 5 --json -q
```

### Search People

```bash
linkedin person search [flags] --json -q
```

| Flag                   | Description                            |
| ---------------------- | -------------------------------------- |
| `--term`               | Search keyword or phrase               |
| `--limit`              | Max results                            |
| `--first-name`         | Filter by first name                   |
| `--last-name`          | Filter by last name                    |
| `--position`           | Filter by job position                 |
| `--locations`          | Comma-separated locations              |
| `--industries`         | Comma-separated industries             |
| `--current-companies`  | Comma-separated current company names  |
| `--previous-companies` | Comma-separated previous company names |
| `--schools`            | Comma-separated school names           |

```bash
linkedin person search --term "product manager" --locations "San Francisco" --json -q
linkedin person search --current-companies "Google" --position "Engineer" --limit 20 --json -q
```

### Fetch a Company

```bash
linkedin company fetch <url> [flags] --json -q
```

Optional flags:

- `--employees` – include employees
- `--dms` – include decision makers
- `--posts` – include company posts

Employee filters (require `--employees`):

| Flag                     | Description                  |
| ------------------------ | ---------------------------- |
| `--employees-limit`      | Max employees to retrieve    |
| `--employees-first-name` | Filter by first name         |
| `--employees-last-name`  | Filter by last name          |
| `--employees-position`   | Filter by position           |
| `--employees-locations`  | Comma-separated locations    |
| `--employees-industries` | Comma-separated industries   |
| `--employees-schools`    | Comma-separated school names |

| Flag            | Description                                        |
| --------------- | -------------------------------------------------- |
| `--dms-limit`   | Max decision makers to retrieve (requires `--dms`) |
| `--posts-limit` | Max posts to retrieve (requires `--posts`)         |
| `--posts-since` | Posts since ISO timestamp (requires `--posts`)     |

```bash
# Basic company info
linkedin company fetch https://www.linkedin.com/company/name --json -q

# With employees filtered by position
linkedin company fetch https://www.linkedin.com/company/name --employees --employees-position "Engineer" --json -q

# With decision makers and posts
linkedin company fetch https://www.linkedin.com/company/name --dms --posts --posts-limit 10 --json -q
```

### Search Companies

```bash
linkedin company search [flags] --json -q
```

| Flag           | Description                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------ |
| `--term`       | Search keyword                                                                                               |
| `--limit`      | Max results                                                                                                  |
| `--sizes`      | Comma-separated sizes: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+` |
| `--locations`  | Comma-separated locations                                                                                    |
| `--industries` | Comma-separated industries                                                                                   |

```bash
linkedin company search --term "fintech" --sizes "11-50,51-200" --json -q
```

### Send a Message

```bash
linkedin message send <person-url> '<text>' --json -q
```

Text up to 1900 characters. Wrap the message in single quotes to avoid shell interpretation issues.

```bash
linkedin message send https://www.linkedin.com/in/username 'Hey, loved your latest post!' --json -q
```

### Get Conversation

```bash
linkedin message get <person-url> [--since TIMESTAMP] --json -q
```

The first call for a conversation triggers a background sync and may take longer. Subsequent calls are faster.

```bash
linkedin message get https://www.linkedin.com/in/username --json -q
linkedin message get https://www.linkedin.com/in/username --since 2024-01-15T10:30:00Z --json -q
```

### Connection Management

#### Check connection status

```bash
linkedin connection status <url> --json -q
```

#### Send connection request

```bash
linkedin connection send <url> [--note 'text'] [--email user@example.com] --json -q
```

#### List connections

```bash
linkedin connection list [flags] --json -q
```

| Flag                   | Description                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------ |
| `--limit`              | Max connections to return                                                            |
| `--since`              | Only connections made since ISO timestamp (only works when no filter flags are used) |
| `--first-name`         | Filter by first name                                                                 |
| `--last-name`          | Filter by last name                                                                  |
| `--position`           | Filter by job position                                                               |
| `--locations`          | Comma-separated locations                                                            |
| `--industries`         | Comma-separated industries                                                           |
| `--current-companies`  | Comma-separated current company names                                                |
| `--previous-companies` | Comma-separated previous company names                                               |
| `--schools`            | Comma-separated school names                                                         |

```bash
linkedin connection list --limit 50 --json -q
linkedin connection list --current-companies "Google" --position "Engineer" --json -q
linkedin connection list --since 2024-01-01T00:00:00Z --json -q
```

#### List pending outgoing requests

```bash
linkedin connection pending --json -q
```

#### Withdraw a pending request

```bash
linkedin connection withdraw <url> [--no-unfollow] --json -q
```

By default, withdrawing also unfollows the person. Use `--no-unfollow` to keep following.

#### Remove a connection

```bash
linkedin connection remove <url> --json -q
```

### Posts

#### Fetch a post

```bash
linkedin post fetch <url> [flags] --json -q
```

| Flag                 | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `--comments`         | Include comments                                                   |
| `--reactions`        | Include reactions                                                  |
| `--comments-limit`   | Max comments to retrieve (requires `--comments`)                   |
| `--comments-sort`    | Sort order: `mostRelevant` or `mostRecent` (requires `--comments`) |
| `--comments-replies` | Include replies to comments (requires `--comments`)                |
| `--reactions-limit`  | Max reactions to retrieve (requires `--reactions`)                 |

```bash
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 --json -q

# With comments sorted by most recent, including replies
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 \
  --comments --comments-sort mostRecent --comments-replies --json -q
```

#### Create a post

```bash
linkedin post create '<text>' [flags] --json -q
```

| Flag            | Description                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------ |
| `--company-url` | Post on behalf of a company page (requires admin access)                                                           |
| `--attachments` | Attachment as `url:type` or `url:type:name`. Types: `image`, `video`, `document`. Can be specified multiple times. |

Attachment limits: up to 9 images, or 1 video, or 1 document. Cannot mix types.

```bash
linkedin post create 'Excited to share our latest update!' --json -q

# With a document
linkedin post create 'Our Q4 report' \
  --attachments "https://example.com/report.pdf:document:Q4 Report" --json -q

# Post as a company
linkedin post create 'Company announcement' \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### React to a post

```bash
linkedin post react <url> --type <reaction> [--company-url <url>] --json -q
```

Reaction types: `like`, `love`, `support`, `celebrate`, `insightful`, `funny`.

```bash
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type like --json -q

# React on behalf of a company
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type celebrate \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### Comment on a post

```bash
linkedin post comment <url> '<text>' [--company-url <url>] --json -q
```

Text up to 1000 characters.

```bash
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Great insights!' --json -q

# Comment on behalf of a company
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Well said!' \
  --company-url https://www.linkedin.com/company/name --json -q
```

### Statistics

```bash
# Social Selling Index
linkedin stats ssi --json -q

# Performance analytics (profile views, post impressions, search appearances)
linkedin stats performance --json -q

# API usage for a date range
linkedin stats usage --start 2024-01-01T00:00:00Z --end 2024-01-31T00:00:00Z --json -q
```

### Sales Navigator

Requires a LinkedIn Sales Navigator subscription. Uses hashed URLs for person/company lookups.

#### Fetch person

```bash
linkedin navigator person fetch <hashed-url> --json -q
```

#### Search people

```bash
linkedin navigator person search [flags] --json -q
```

| Flag                    | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| `--term`                | Search keyword or phrase                                                                    |
| `--limit`               | Max results                                                                                 |
| `--first-name`          | Filter by first name                                                                        |
| `--last-name`           | Filter by last name                                                                         |
| `--position`            | Filter by job position                                                                      |
| `--locations`           | Comma-separated locations                                                                   |
| `--industries`          | Comma-separated industries                                                                  |
| `--current-companies`   | Comma-separated current company names                                                       |
| `--previous-companies`  | Comma-separated previous company names                                                      |
| `--schools`             | Comma-separated school names                                                                |
| `--years-of-experience` | Comma-separated ranges: `lessThanOne`, `oneToTwo`, `threeToFive`, `sixToTen`, `moreThanTen` |

```bash
linkedin navigator person search --term "VP Marketing" --locations "United States" --json -q
linkedin navigator person search --years-of-experience "moreThanTen" --position "CEO" --json -q
```

#### Fetch company

```bash
linkedin navigator company fetch <hashed-url> [flags] --json -q
```

Optional flags:

- `--employees` – include employees
- `--dms` – include decision makers

Employee filters (require `--employees`):

| Flag                              | Description                                        |
| --------------------------------- | -------------------------------------------------- |
| `--employees-limit`               | Max employees to retrieve                          |
| `--employees-first-name`          | Filter by first name                               |
| `--employees-last-name`           | Filter by last name                                |
| `--employees-positions`           | Comma-separated positions                          |
| `--employees-locations`           | Comma-separated locations                          |
| `--employees-industries`          | Comma-separated industries                         |
| `--employees-schools`             | Comma-separated school names                       |
| `--employees-years-of-experience` | Comma-separated experience ranges                  |
| `--dms-limit`                     | Max decision makers to retrieve (requires `--dms`) |

```bash
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural --employees --dms --json -q
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural \
  --employees --employees-positions "Engineer,Designer" --employees-locations "Europe" --json -q
```

#### Search companies

```bash
linkedin navigator company search [flags] --json -q
```

| Flag            | Description                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| `--term`        | Search keyword                                                                                               |
| `--limit`       | Max results                                                                                                  |
| `--sizes`       | Comma-separated sizes: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+` |
| `--locations`   | Comma-separated locations                                                                                    |
| `--industries`  | Comma-separated industries                                                                                   |
| `--revenue-min` | Min annual revenue in M USD: `0`, `0.5`, `1`, `2.5`, `5`, `10`, `20`, `50`, `100`, `500`, `1000`             |
| `--revenue-max` | Max annual revenue in M USD: `0.5`, `1`, `2.5`, `5`, `10`, `20`, `50`, `100`, `500`, `1000`, `1000+`         |

```bash
linkedin navigator company search --term "fintech" --sizes "11-50,51-200" --json -q
linkedin navigator company search --revenue-min 10 --revenue-max 100 --locations "United States" --json -q
```

#### Send InMail

```bash
linkedin navigator message send <person-url> '<text>' --subject '<subject>' --json -q
```

Text up to 1900 characters. Subject up to 80 characters.

```bash
linkedin navigator message send https://www.linkedin.com/in/username \
  'Would love to chat about API integrations' --subject 'Partnership Opportunity' --json -q
```

#### Get Sales Navigator conversation

```bash
linkedin navigator message get <person-url> [--since TIMESTAMP] --json -q
```

### Custom Workflows

Execute a custom workflow definition from a file, stdin, or inline:

```bash
# From file
linkedin workflow run --file workflow.json --json -q

# From stdin
cat workflow.json | linkedin workflow run --json -q

# Inline
echo '{"actions":[...]}' | linkedin workflow run --json -q
```

Check workflow status or wait for completion:

```bash
linkedin workflow status <id> --json -q
linkedin workflow status <id> --wait --json -q
```

See [Building Workflows](https://linkedapi.io/docs/building-workflows/) for the workflow JSON schema.

### Account Management

```bash
linkedin account list                            # List accounts (* = active)
linkedin account switch "Name"                   # Switch active account
linkedin account rename "Name" --name "New Name" # Rename account
linkedin reset                                   # Remove active account
linkedin reset --all                             # Remove all accounts
```

## Important Behavior

- **Sequential execution.** All operations for an account run one at a time. Multiple requests queue up.
- **Not instant.** A real browser navigates LinkedIn – expect 30 seconds to several minutes per operation.
- **Timestamps in UTC.** All dates and times are in UTC.
- **Single quotes for text arguments.** Use single quotes around message text, post text, and comments to avoid shell interpretation issues with special characters.
- **Action limits.** Per-account limits are configurable on the platform. A `limitExceeded` error means the limit was reached.
- **URL normalization.** All LinkedIn URLs in responses are normalized to `https://www.linkedin.com/...` format without trailing slashes.
- **Null fields.** Fields that are unavailable are returned as `null` or `[]`, not omitted.

---

# LinkedIn Automation via Rube MCP

Automate LinkedIn operations through Composio's LinkedIn toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active LinkedIn connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `linkedin`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `linkedin`
3. If connection is not ACTIVE, follow the returned auth link to complete LinkedIn OAuth
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Create a LinkedIn Post

**When to use**: User wants to publish a text post on LinkedIn

**Tool sequence**:
1. `LINKEDIN_GET_MY_INFO` - Get authenticated user's profile info [Prerequisite]
2. `LINKEDIN_REGISTER_IMAGE_UPLOAD` - Register image upload if post includes an image [Optional]
3. `LINKEDIN_CREATE_LINKED_IN_POST` - Publish the post [Required]

**Key parameters**:
- `text`: Post content text
- `visibility`: 'PUBLIC' or 'CONNECTIONS'
- `media_title`: Title for attached media
- `media_description`: Description for attached media

**Pitfalls**:
- Must retrieve user profile URN via GET_MY_INFO before creating a post
- Image uploads require a two-step process: register upload first, then include the asset in the post
- Post text has character limits enforced by LinkedIn API
- Visibility defaults may vary; always specify explicitly

### 2. Get Profile Information

**When to use**: User wants to retrieve their LinkedIn profile or company details

**Tool sequence**:
1. `LINKEDIN_GET_MY_INFO` - Get authenticated user's profile [Required]
2. `LINKEDIN_GET_COMPANY_INFO` - Get company page details [Optional]

**Key parameters**:
- No parameters needed for GET_MY_INFO (uses authenticated user)
- `organization_id`: Company/organization ID for GET_COMPANY_INFO

**Pitfalls**:
- GET_MY_INFO returns the authenticated user only; cannot look up other users
- Company info requires the numeric organization ID, not the company name or vanity URL
- Some profile fields may be restricted based on OAuth scopes granted

### 3. Manage Post Images

**When to use**: User wants to upload and attach images to LinkedIn posts

**Tool sequence**:
1. `LINKEDIN_REGISTER_IMAGE_UPLOAD` - Register an image upload with LinkedIn [Required]
2. Upload the image binary to the returned upload URL [Required]
3. `LINKEDIN_GET_IMAGES` - Verify uploaded image status [Optional]
4. `LINKEDIN_CREATE_LINKED_IN_POST` - Create post with the image asset [Required]

**Key parameters**:
- `owner`: URN of the image owner (user or organization)
- `image_id`: ID of the uploaded image for GET_IMAGES

**Pitfalls**:
- The upload is a two-phase process: register then upload binary
- Image asset URN from registration must be used when creating the post
- Supported formats typically include JPG, PNG, and GIF
- Large images may take time to process before they are available

### 4. Comment on Posts

**When to use**: User wants to comment on an existing LinkedIn post

**Tool sequence**:
1. `LINKEDIN_CREATE_COMMENT_ON_POST` - Add a comment to a post [Required]

**Key parameters**:
- `post_id`: The URN or ID of the post to comment on
- `text`: Comment content
- `actor`: URN of the commenter (user or organization)

**Pitfalls**:
- Post ID must be a valid LinkedIn URN format
- The actor URN must match the authenticated user or a managed organization
- Rate limits apply to comment creation; avoid rapid-fire comments

### 5. Delete a Post

**When to use**: User wants to remove a previously published LinkedIn post

**Tool sequence**:
1. `LINKEDIN_DELETE_LINKED_IN_POST` - Delete the specified post [Required]

**Key parameters**:
- `post_id`: The URN or ID of the post to delete

**Pitfalls**:
- Deletion is permanent and cannot be undone
- Only the post author or organization admin can delete a post
- The post_id must be the exact URN returned when the post was created

## Common Patterns

### ID Resolution

**User URN from profile**:
```
1. Call LINKEDIN_GET_MY_INFO
2. Extract user URN (e.g., 'urn:li:person:XXXXXXXXXX')
3. Use URN as actor/owner in subsequent calls
```

**Organization ID from company**:
```
1. Call LINKEDIN_GET_COMPANY_INFO with organization_id
2. Extract organization URN for posting as a company page
```

### Image Upload Flow

- Call REGISTER_IMAGE_UPLOAD to get upload URL and asset URN
- Upload the binary image to the provided URL
- Use the asset URN when creating a post with media
- Verify with GET_IMAGES if upload status is uncertain

## Known Pitfalls

**Authentication**:
- LinkedIn OAuth tokens have limited scopes; ensure required permissions are granted
- Tokens expire; re-authenticate if API calls return 401 errors

**URN Formats**:
- LinkedIn uses URN identifiers (e.g., 'urn:li:person:ABC123')
- Always use the full URN format, not just the alphanumeric ID portion
- Organization URNs differ from person URNs

**Rate Limits**:
- LinkedIn API has strict daily rate limits on post creation and comments
- Implement backoff strategies for bulk operations
- Monitor 429 responses and respect Retry-After headers

**Content Restrictions**:
- Posts have character limits enforced by the API
- Some content types (polls, documents) may require additional API features
- HTML markup in post text is not supported

## Quick Reference

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Get my profile | LINKEDIN_GET_MY_INFO | (none) |
| Create post | LINKEDIN_CREATE_LINKED_IN_POST | text, visibility |
| Get company info | LINKEDIN_GET_COMPANY_INFO | organization_id |
| Register image upload | LINKEDIN_REGISTER_IMAGE_UPLOAD | owner |
| Get uploaded images | LINKEDIN_GET_IMAGES | image_id |
| Delete post | LINKEDIN_DELETE_LINKED_IN_POST | post_id |
| Comment on post | LINKEDIN_CREATE_COMMENT_ON_POST | post_id, text, actor |

---
