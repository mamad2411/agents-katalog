---
name: supply-chain-git-platforms
description: Git platform security posture review — examines GitHub, GitLab, Gitea, Bitbucket organization and repository settings for access control misconfigurations, exposed .git directories, unprotected branches, stale collaborator access, webhook integrity, default-branch permissions, and secret scanning enablement. Operates on user-supplied exports and read-only API queries. No repository creation, branch push, webhook creation, access modification, or secret reading.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat, forensic]
authorization-required: conditional
evidence-outputs: [command-log, redacted-evidence, finding-draft, platform-risk-matrix, access-review-report]
---

# Git platform security review — access control, exposed repos, and configuration hygiene

Use this skill to review the security configuration of Git hosting platforms: GitHub (cloud and Enterprise Server), GitLab (cloud and self-managed), Gitea, Bitbucket, and Azure DevOps. The review covers organization-level settings (member access, default permissions, OAuth app restrictions), repository-level settings (branch protection, visibility, deploy keys, webhooks, secret scanning), and exposed repository content (.git directories on production servers). All analysis is read-only: read configuration exports, perform read-only API queries, analyze exposed directories. Never create repos, modify access, push code, trigger webhooks, or read live secret values.

## Required inputs

- Platform type and organization/user name. Confirm whether the review targets a specific organization, a set of repositories, or all repositories the supplied API token can access.
- Repository access: read-only API token OR user-provided exports of organization/repository settings. If neither is available, the review is limited to publicly accessible information and user-supplied config dumps.
- Scope file: which repositories, organizations, and settings are in scope. Which access changes, push operations, or webhook creations are prohibited.
- Confirmation that no repository settings will be modified, no webhooks created, no access changed, and no secrets read.

## Required gates

1. `pentest_agent_load_config` to verify storage and redaction policy.
2. `pentest_agent_parse_scope` to confirm platform scope, allowed repositories, and prohibited actions.
3. `pentest_agent_check_authorization` before any read-only API call.
4. `pentest_agent_build_command` for dry-run command preview.
5. `pentest_agent_append_evidence` for redacted findings.

## Workflow

### Phase 1 — organization-level security review

Assess the platform-wide settings that affect all repositories.

1. **Member access and roles** (GitHub):
   - List organization members by role: Owner, Admin, Member.
   - Count owners: > 3 owners is excessive (increases attack surface); = 1 owner is a bus-factor risk.
   - Check for members without 2FA enabled (GitHub: `/orgs/{org}/members?filter=2fa_disabled`).
   - Check for stale members (no activity in 90+ days).
   - Finding: members without 2FA → HIGH in organizations with access to production code or secrets.
   - Finding: former employees with active membership → CRITICAL. Immediate removal required.
2. **OAuth app restrictions** (GitHub):
   - Are third-party application access restrictions enabled?
   - Which OAuth apps have organization access? Are any unknown or unnecessary?
   - Finding: no OAuth app restrictions → MEDIUM. Any user can authorize a malicious OAuth app that reads private repos.
3. **Default repository permissions**:
   - What is the base permission for organization members on new repos? (None, Read, Write, Admin).
   - GitHub default is "Read" — check if it's been changed to "Write" or "Admin".
   - Finding: default permission is Write or Admin → HIGH. Any member can modify any new repository.
4. **Repository forking policy**:
   - Can members fork private repositories? Forks may leak source code to personal accounts with weaker security.
   - Can members fork internal repositories to external organizations?
   - Finding: private/internal repo forking enabled → MEDIUM. Intellectual property risk.
5. **Webhook configuration**:
   - Are webhooks configured at the organization level?
   - What URLs do they point to? Are they HTTPS?
   - Is the webhook secret configured? (Can only verify presence, not secret value.)
   - Finding: webhook without secret → HIGH. Anyone who discovers the webhook URL can send forged payloads.

### Phase 2 — repository-level access control

For each in-scope repository, examine who has what access.

1. **Repository visibility**: public, private, or internal (GitHub). Document for each repo.
   - Public repos: intended to be public? Contains secrets accidentally?
   - Internal repos: visible to all organization members — wider exposure than many realize.
2. **Direct collaborator access**: list every user with direct access to the repository (not through team membership).
   - Finding: direct collaborator access when team-based access is the organization policy → LOW but worth flagging (bypasses team management).
3. **Team access audit**: for each team with repository access, document: team name, permission level (read/triage/write/maintain/admin), number of members.
   - Finding: team with admin access that has > 10 members → MEDIUM. Too many admins.
4. **Deploy keys audit**:
   - List deploy keys: title, SHA256 fingerprint, read-only or read-write, creation date, last used date.
   - Finding: deploy key with write access → MEDIUM (may be necessary, but document and verify).
   - Finding: deploy key unused for > 90 days → LOW. Remove stale keys.
5. **Outside collaborators**: users with repository access who are not organization members.
   - Finding: outside collaborators with write or admin access → HIGH. Verify business need and review access quarterly.

### Phase 3 — branch protection and merge controls

For each in-scope repository's default branch and any protected branches, assess the protection rules.

1. **Branch protection status**: is the default branch (main/master) protected?
   - Finding: unprotected default branch → HIGH. Anyone with push access can force-push or delete the branch.
2. **Protection rule details**:
   - **Required reviews**: minimum count, whether stale reviews are dismissed, whether code owners must approve.
   - **Required status checks**: which CI checks must pass before merging.
   - **Require conversation resolution**: are all review threads required to be resolved?
   - **Force push**: blocked? Allowed?
   - **Branch deletion**: blocked? Allowed?
   - **Restrict pushes to specific teams/apps**: who can bypass the rules? If administrators can bypass: documented and approved?
   - Finding: required reviews < 2 for a production-critical repo → MEDIUM.
   - Finding: administrators can bypass branch protection → MEDIUM if not audited.
3. **Push rules (GitLab)**: are push rules configured? (commit message regex, branch name regex, file size limits, prevent secret push).
4. **Signed commits required?**:
   - Does the platform require signed commits?
   - Finding: no signed-commit requirement → LOW. Commits can be forged.

### Phase 4 — secret scanning and push protection

Evaluate whether the platform's native secret-scanning features are enabled.

1. **GitHub secret scanning**:
   - Is secret scanning enabled for the repository? (Settings → Security → Secret scanning).
   - Is push protection enabled? (Blocks pushes that contain known secret patterns).
   - Finding: secret scanning disabled → MEDIUM. Low-cost, high-value control.
   - Finding: push protection disabled → HIGH if secret scanning is also disabled. A developer accidentally pushing a secret to a public repo has minutes before it's scraped.
2. **GitLab secret detection**:
   - Is secret detection enabled in CI/CD? (`Secret-Detection.gitlab-ci.yml` template).
   - Are push rules configured to reject secrets?
3. **Custom secret patterns**: has the organization defined custom patterns for internal secret formats (connection strings, internal API tokens, internal key formats)?
   - Finding: custom patterns not defined → MEDIUM. Standard scanning misses org-specific secrets.

### Phase 5 — exposed .git directory detection

Check whether production servers are exposing `.git` directories that would leak the entire repository history.

1. **Passive check** (read-only, target only with authorization and user approval):
   - For each in-scope web target, check: `curl -s -o /dev/null -w "%{http_code}" https://TARGET/.git/HEAD`.
   - HTTP 200 → the `.git` directory is publicly accessible.
   - HTTP 403 → `.git` exists but access is denied (still confirm — some servers return 403 but allow specific files within `.git`).
   - HTTP 404 → `.git` not present at that path (but could exist on a different virtual host or port).
2. **What can be leaked** (documentation for finding impact):
   - Source code (entire history).
   - Hardcoded secrets, API keys, database passwords from old commits.
   - `.env`, `config/database.yml`, `wp-config.php` backups.
   - Developer email addresses (for social engineering).
   - Commit messages revealing security issues ("fixed XSS, TODOs: remove debug endpoint").
3. **Finding**: exposed `.git` → CRITICAL. Immediate remediation required. Document the path, response status, and any accessible files confirmed via HEAD/config. Do NOT use `git-dumper` or any tool that reconstructs the repository without explicit, separate approval — that constitutes active source-code exfiltration.

### Phase 6 — stale resources and cleanup recommendations

Identify resources that increase the attack surface unnecessarily.

1. **Stale repositories**: no commits in > 12 months, no active maintainers. Archive or delete.
2. **Stale branches**: branches merged months ago but never deleted. Clean up.
3. **Unused deploy keys and webhooks**: remove if not needed.
4. **Forked repositories**: are forks maintained independently? If abandoned, they may contain vulnerabilities patched in the upstream repo.
5. **Repository templates**: are templates kept up to date? A stale template creates insecure new repos.

## Decision points

- **API token has limited scope and cannot read certain settings**: document what could not be assessed. "Branch protection status could not be verified — API token lacked `repo:admin` scope."
- **Organization is on a free plan without certain features** (e.g., required reviewers on private repos requires GitHub Team): document as "Platform tier limitation." Note that upgrading would enable the missing controls.
- **Repository is archived/read-only**: still review — archived repos can contain secrets that were valid when the repo was active.
- **Finding requires reaching out to a former employee for access removal**: handle with organizational process, not within this skill. Flag and move on.
- **Exposed .git directory is confirmed but remediation would require deploying a web-server config change**: route to the appropriate team. Document the finding with specific URL, path, and impact.

## Prohibited behavior

- Creating, modifying, or deleting repositories, branches, tags, releases, or webhooks.
- Modifying user or team access (adding, removing, changing permissions).
- Reading secret values, deploy key private keys, webhook secrets, or API tokens.
- Using a discovered API token to access resources beyond what the user explicitly approved.
- Running `git-dumper`, `git clone`, or any tool that reconstructs an exposed `.git` directory without explicit, separate approval.
- Posting issues, pull requests, or comments on the target platform.
- Triggering CI/CD pipelines or deployment workflows.

## Stop conditions

- API token is invalid or expired → stop and request a valid read-only token.
- API token has write or admin scopes beyond what is needed → warn the user. Use with extreme caution. Never use write/admin tokens for any action beyond read-only queries.
- Exposed `.git` directory is detected → flag as CRITICAL but do NOT proceed to dump the repository without separate approval.
- A finding would require modifying a setting to validate → stop. Document the finding and recommend validation in a non-production environment.

## Evidence

For each finding, record: platform, repository/organization name (redacted to example name if sensitive), setting or resource, current value, risk, recommended value, and a brief justification. Evidence template:

```text
Git platform security review for: [ORG_NAME / REPO_NAME]
Platform: [GitHub.com / GitHub Enterprise / GitLab.com / GitLab self-managed / Bitbucket]
Review date: [DATE]
Repositories in scope: [N] ([N] public, [N] private, [N] internal)
Data source: [read-only API token / user-provided exports / public data only]

Organization-level findings:
  2FA enforcement: [enabled/disabled] across [N]/[N] members
  OAuth app restrictions: [enabled/disabled]
  Default repo permissions: [None / Read / Write / Admin]
  Outside collaborators: [N] across [N] repos

Repository-level findings summary:
  Unprotected default branches: [N] repos
  Deploy keys with write access: [N]
  Outside collaborators with write/admin: [N]
  Secret scanning disabled: [N] repos
  Push protection disabled: [N] repos

Exposed .git directory scan:
  Hosts scanned: [N]
  Exposed .git found: [N] hosts
  CRITICAL findings: [list URLs redacted to hostname]

Access hygiene:
  Stale members (>90 days inactive): [N]
  Stale repositories (>12 months no commit): [N]
  Stale deploy keys (>90 days unused): [N]

Redaction notes:
  - Repository and organization names redacted to example identifiers.
  - No secret values, private keys, or API tokens accessed or recorded.
  - Deploy key fingerprints recorded for audit; private keys never accessed.
  - Exposed .git URLs documented; no repository data dumped or cloned.
```

## Report handoff

1. `pentest_agent_record_finding` for each confirmed finding, with: platform, repository/org context, finding category, current configuration, risk, recommended configuration, and redacted evidence.
2. Priority matrix: CRITICAL (exposed .git), HIGH (unprotected branches, 2FA gaps, outside collaborators with admin), MEDIUM (secret scanning disabled, push protection disabled), LOW (stale resources, cleanup items).
3. If requested, provide an access review spreadsheet (CSV) mapping users/teams to repositories and permission levels.
4. Explicitly note: no repository settings were modified, no access was changed, no webhooks were created, no secrets were read, and no `.git` repositories were dumped.
