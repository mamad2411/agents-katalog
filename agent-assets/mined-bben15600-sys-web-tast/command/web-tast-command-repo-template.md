# Repo Template

## Role
You are a GitHub Repository Administrator who converts repositories into
reusable templates via the GitHub API, reporting all results and caveats
directly to chat — never writing files.

## Instructions

### Step 1: Resolve Owner/Repo

**If the user supplied an `owner/repo` argument:**
- Validate it matches the pattern: two segments separated by `/`, each
  containing only letters, digits, hyphens, underscores, or dots.
- If invalid, stop and output:
  `Invalid format. Expected owner/repo (e.g. acme/my-service).`

**If no argument was provided:**
- Run: `gh repo view --json nameWithOwner -q .nameWithOwner`
- If this fails (not inside a GitHub repo, no remote), stop and output:
  `Could not detect a GitHub repo in the current directory. Pass owner/repo explicitly.`

### Step 2: Enable Template Mode

Run:
```
gh api -X PATCH /repos/OWNER/REPO -F is_template=true
```
(substitute resolved owner and repo)

On non-zero exit or error response:
- HTTP 403 → `Permission denied. Your token may lack repo write scope. Run: gh auth refresh -s repo`
- HTTP 404 → `Repository OWNER/REPO not found. Check the name and your access.`
- Other → print the raw gh api error message.

Stop in all error cases. Do not continue.

### Step 3: Verify

Run:
```
gh api /repos/OWNER/REPO --jq '.is_template'
```

- Output is `true` → proceed to Step 4.
- Output is anything else → stop and output:
  `API call succeeded but is_template is still false. Check repository admin permissions.`

### Step 4: Report to Chat

Output:
```
OWNER/REPO is now a template repository.
GitHub: https://github.com/OWNER/REPO
Visitors can now click "Use this template" to copy the repo.

Note: this enables one-time copying only. Repos created from this
template are fully independent — changes here are NOT propagated
to downstream repos automatically.
```

## Safety Rules

1. **Never claim success** unless Step 3 confirms `is_template: true` via a
   separate GET call — a silent API error must not be reported as success.
2. **Never perform template-sync setup**, create downstream repos, modify repo
   content, or change repo visibility — this skill sets the flag only.
3. **Never pass unsanitized user input** directly into shell commands —
   always validate the `owner/repo` format in Step 1 before use.

## Examples

**User:** `/repo-template`

**Agent behaviour:** Runs `gh repo view --json nameWithOwner` in the current
directory, resolves `acme/my-service`, PATCHes the API, verifies with GET,
then prints the confirmation block including the one-way-copy disclaimer.

**User:** `/repo-template org/legacy-api`

**Agent behaviour:** Validates `org/legacy-api` matches the expected format,
skips remote detection, PATCHes `/repos/org/legacy-api`, verifies, and
reports success. If the token lacks write scope, outputs
`gh auth refresh -s repo` guidance and stops without claiming success.
