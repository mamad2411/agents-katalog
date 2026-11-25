---
name: git
description: This skill should be used when the user asks to "clone a repo", "git clone", "check out this repo", "install this tool from GitHub", "try this open source project", or mentions cloning, checking out, or installing any Git repository. Automatically gates public repo clones with a security assessment before execution.
metadata:
  version: 2.0.0
---

# Git (Secure Clone)

Gate every `git clone` of a public repository with an automatic security assessment. Private/org repos clone immediately with no added friction.

## Trigger

Any user request that involves cloning, checking out, or installing a Git repository.

## Workflow

### 1. Parse the repo URL

Extract `<host>`, `<owner>`, and `<repo>` from the URL or shorthand the user provided.

Accept common forms: `https://github.com/org/repo`, `git@github.com:org/repo.git`, `org/repo` (assume GitHub when no host). Normalize to an HTTPS URL.

### 2. Probe: public or private?

Run this host-agnostic check (no API key needed):

```bash
GIT_TERMINAL_PROMPT=0 \
GIT_ASKPASS=/bin/false \
git -c credential.helper= -c http.extraheader= \
  ls-remote --heads <normalized-https-url> 2>&1
```

| Outcome | Meaning | Action |
|---------|---------|--------|
| Succeeds (exits 0, prints refs) | Repo is publicly readable | **Run the security gate (Step 3)** |
| Fails (auth error / 404) | Repo is private or restricted | **Clone directly** — skip the gate |
| Fails (network / DNS error) | URL is invalid or unreachable | **Report the error**, do not clone |

When in doubt (rate-limited, ambiguous result), treat as public and run the gate.

### 3. Security gate (public repos only)

Read and execute the full assessment defined in the `oss-security-check` skill (`../oss-security-check/SKILL.md`).

Pass it:
- `<url>` — the normalized HTTPS URL
- `<owner>/<repo>` — extracted from the URL
- `<host>` — the git host
- Context: "This is a git repository the user wants to clone"

Wait for the assessment to complete. Present the results to the user.

### 4. User decision

After presenting the assessment, ask the user:

- **Clone** — proceed with the clone to the requested location
- **Clone to sandbox** — clone to a temporary/isolated directory instead
- **Abort** — do not clone

### 5. Execute the clone

If approved, run the clone. If the recommendation was "medium" or "high" risk, remind the user:

- Use read-only / scoped tokens if the tool needs credentials
- Prefer a throwaway repo for first use
- Look for a `--dry-run` mode before running with real data

### 6. Cleanup

The `oss-security-check` skill handles cleanup of its temporary shallow clone.

## Customization

The public/private probe in Step 2 is generic. Teams should replace it with a check specific to their environment. For example:

- **GitHub org allowlist:** skip the gate for repos in your org
- **Internal registry:** skip for packages from your private registry
- **Domain allowlist:** skip for repos hosted on your company's GitLab instance

Ask your AI agent: *"Modify the git skill so that repos in the `<your-org>` GitHub organization skip the security gate, and all other public repos are scanned before cloning."*

## Notes

- Private repo clones are unaffected — zero added latency.
- Public repo gate adds ~30-60 seconds (web search + code scan).
- This skill does NOT replace thorough security review for production dependencies. It is a fast first pass.
