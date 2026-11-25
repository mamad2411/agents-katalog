---
name: npm-supply-chain-response
description: Respond to npm supply chain attacks and compromised package incidents. Use this skill whenever a user mentions a compromised npm package, an npm supply chain attack, a malicious dependency in node_modules, credential-stealing malware from npm install, or asks how to check if they're affected by a package compromise on npm. Also trigger when the user asks about postinstall script backdoors, typosquatted npm packages, hunting for IOCs after an npm install, auditing node environments for malicious packages, or generating an incident response checklist for an npm compromise. Trigger even if the user just names a package and says it was "hacked", "backdoored", "compromised", or "pwned" and the package is from npm, yarn, or pnpm. Covers axios, plain-crypto-js, and any future npm supply chain incident.
license: MIT
compatibility: Requires Bash and Node.js/npm. Optional: yarn, pnpm, jq, docker, kubectl.
---

# npm Supply Chain Attack Response

Help developers triage, investigate, contain, and recover from a compromised npm package.

This skill produces one of three outputs depending on what the user asks for:

1. **Interactive triage checklist** — step-by-step walkthrough, one phase at a time, asking the user to run commands and report back before proceeding.
2. **Full incident response runbook** — a complete markdown document covering all six phases that the user can save and share with their team.
3. **Shell script** — a `check_npm_compromise.sh` script that automates detection, reports findings, and prompts before any remediation action.

If the user doesn't specify which format, default to the interactive triage checklist. If the user says something like "just give me everything" or "runbook", produce the full markdown document. If they say "script" or "automate", generate the shell script.

## Gathering context

Before producing any output, collect the following from the user. If they've already provided some of this in the conversation, don't re-ask.

**Required:**
- **Package name** — the compromised package (e.g., `axios`)
- **Compromised versions** — which versions contain the malicious payload (e.g., `1.14.1`, `0.30.4`)

**Helpful but not required (use defaults or skip if the user doesn't know):**
- **Known safe version** — the last clean version to pin to (e.g., `1.14.0`)
- **Attack window** — UTC time range when the bad versions were available on npm
- **Known IOCs** — domains, filenames, persistence paths, process names. If the user doesn't have these, use the built-in IOC pattern library (see `references/ioc-patterns.md`).
- **Payload behavior** — what the malware does (credential theft, persistence, lateral movement). If unknown, assume credential theft as the baseline.
- **Malicious dependency** — some attacks inject the payload via a typosquatted dependency rather than the main package (e.g., `plain-crypto-js` in the Axios attack). If known, collect this too.

## The six phases

Every output format follows these six phases in order. The depth and format change based on the output type, but the sequence is always the same.

### Phase 1: Exposure check — "Am I even affected?"

The goal is to determine whether the compromised package exists anywhere in the user's environments, including as a transitive dependency they never directly installed.

**Commands to guide the user through:**

Check if the package is installed and what version:
```
npm ls <PACKAGE> 2>/dev/null
yarn why <PACKAGE> 2>/dev/null
pnpm why <PACKAGE> 2>/dev/null
```

Search lockfiles for the compromised package or its malicious dependency:
```
grep -n "<PACKAGE>" package-lock.json 2>/dev/null
grep -n "<PACKAGE>" yarn.lock 2>/dev/null
grep -n "<PACKAGE>" pnpm-lock.yaml 2>/dev/null
grep -n "<MALICIOUS_DEP>" package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null
```

Hunt across ALL environments on the machine — developers often have multiple projects, global installs, and package manager caches:
```
find / -path "*/node_modules/<PACKAGE>/package.json" -type f 2>/dev/null
find / -path "*/node_modules/<MALICIOUS_DEP>" -type d 2>/dev/null
npm ls -g --depth=0 2>/dev/null | grep "<PACKAGE>"
```

**Monorepo support:** For workspaces, run checks from the workspace root AND individual packages. Lockfiles may exist at multiple levels.
```
find . -name "package-lock.json" -o -name "yarn.lock" -o -name "pnpm-lock.yaml" | while read f; do
  echo "=== $f ===" && grep -n "<PACKAGE>" "$f" 2>/dev/null
done
```

Check npm cache (note: `npm cache ls` was removed in npm 7+):
```
grep -r '<PACKAGE>' ~/.npm/_cacache/index-v5/ 2>/dev/null
grep -r '<MALICIOUS_DEP>' ~/.npm/_cacache/index-v5/ 2>/dev/null
```

Check Docker images built during the attack window:
```
docker images --format "{{.Repository}}:{{.Tag}} {{.CreatedAt}}" | sort -k2
docker run --rm <IMAGE> npm ls <PACKAGE> 2>/dev/null
```

Search for unpinned or loosely pinned references in package.json:
```
grep -n "<PACKAGE>" package.json 2>/dev/null
```
Flag dangerous patterns: `^`, `~`, `*`, `>=`, or no version pin at all. Only exact versions (`"1.14.0"` without prefix) are safe.

Check CI/CD logs for the package version string during the attack window:
```
grep -r "<PACKAGE>@" /path/to/ci/logs/ 2>/dev/null
```

### Phase 2: Version confirmation — "Did I get the bad version?"

If Phase 1 found the package, confirm whether the installed version matches a compromised version.

```
cat node_modules/<PACKAGE>/package.json | grep '"version"'
```

Check if the malicious dependency was pulled in:
```
ls node_modules/<MALICIOUS_DEP>/ 2>/dev/null
cat node_modules/<MALICIOUS_DEP>/package.json 2>/dev/null | grep '"version"'
```

Check file timestamps to estimate when the package was installed:
```
stat node_modules/<PACKAGE>/package.json 2>/dev/null
```

For npm, check the lockfile resolved URLs and integrity hashes — these are more reliable than the version field if the attacker tampered with package.json post-install:
```
grep -A5 '"<PACKAGE>"' package-lock.json | grep -E '"version"|"resolved"|"integrity"'
```

After confirming the version, classify the finding into one of these five categories:

- **Not present** — package not found anywhere
- **Present, safe version** — installed but not a compromised version
- **Present, likely affected** — compromised version was installed
- **Present, insufficient evidence** — package found but version or install timing unclear
- **Confirmed compromise** — compromised version installed AND IOC indicators found

### Phase 3: IOC hunting — "Did the malware execute?"

If the user confirmed they had a compromised version, look for evidence that the payload ran. Read `references/ioc-patterns.md` for the built-in pattern library. Combine those patterns with any attack-specific IOCs the user provides.

**Postinstall script detection — scan ALL installed packages:**
```
npm query ':attr(scripts, [postinstall])' 2>/dev/null | jq '.[].name'
```

If `npm query` is not available (older npm), use:
```
find node_modules -maxdepth 2 -name package.json \
  -exec grep -l '"preinstall\|postinstall\|preuninstall"' {} \;
```

**Anti-forensics detection:**

Some attacks swap `package.json` with a clean copy after the postinstall runs to hide evidence. Check for:
```
# The Axios attack swaps package.md → package.json after execution
ls node_modules/<MALICIOUS_DEP>/package.md 2>/dev/null

# Check if the postinstall script file still exists (payload self-deletes)
ls node_modules/<MALICIOUS_DEP>/setup.js 2>/dev/null
```

If `package.md` exists alongside `package.json`, the package.json was likely swapped post-execution to remove the postinstall evidence. The original malicious package.json is gone.

**Filesystem IOCs — check platform-specific persistence locations:**

macOS:
```
ls -la /Library/Caches/com.apple.act.mond 2>/dev/null
find ~/Library/Caches -name "*.mond" -mtime -7 2>/dev/null
```

Linux:
```
ls -la /tmp/ld.py 2>/dev/null
find /tmp -name "*.py" -mtime -3 2>/dev/null
find ~/.config/systemd/user/ -name "*.service" -mtime -7 2>/dev/null
crontab -l 2>/dev/null
```

Windows:
```
dir %PROGRAMDATA%\wt.exe 2>nul
dir %TEMP%\*.vbs %TEMP%\*.ps1 2>nul
```

**Network indicators:**
```
# Check for connections to known C2 domains
ss -tnp 2>/dev/null | grep -i "<C2_DOMAIN>"
netstat -tn 2>/dev/null | grep -i "<C2_DOMAIN>"

# Search logs for C2 communication
grep -rF "<C2_DOMAIN>" /var/log/ 2>/dev/null
```

**Process inspection:**
```
# Look for background processes spawned by the payload
ps aux | grep -E "ld\.py|com\.apple\.act|wt\.exe" | grep -v grep
```

**Credential access evidence:**
```
find ~/.ssh ~/.aws ~/.config/gcloud ~/.kube ~/.npmrc ~/.docker -atime -1 2>/dev/null
stat ~/.ssh/id_rsa 2>/dev/null | grep Access
stat ~/.npmrc 2>/dev/null | grep Access
```

**Kubernetes (if applicable):**
```
kubectl get pods -n kube-system --sort-by=.metadata.creationTimestamp
kubectl get secrets --all-namespaces -o json | jq '.items[] | select(.metadata.creationTimestamp > "<ATTACK_DATE>")'
```

### Phase 4: Containment — "Stop the bleeding"

Before removing anything, preserve evidence if your organization may need forensic analysis.

```
# Preserve evidence before cleanup
npm ls --all > npm-ls-evidence-$(date +%Y%m%d-%H%M%S).txt 2>&1
cp package-lock.json package-lock-evidence-$(date +%Y%m%d-%H%M%S).json 2>/dev/null
cp -r node_modules/<MALICIOUS_DEP> malicious-dep-evidence-$(date +%Y%m%d-%H%M%S)/ 2>/dev/null
ss -tnp > network-connections-$(date +%Y%m%d-%H%M%S).txt 2>/dev/null
```

Remove the compromised package and malicious dependency, purge caches:
```
rm -rf node_modules/<MALICIOUS_DEP>
npm cache clean --force
```

Pin to a known-safe version:
```
npm install <PACKAGE>@<SAFE_VERSION> --save-exact
```

For yarn/pnpm:
```
yarn add <PACKAGE>@<SAFE_VERSION> --exact
pnpm add <PACKAGE>@<SAFE_VERSION> --save-exact
```

If persistence artifacts were found in Phase 3, remove them. In the interactive checklist, describe each artifact and ask the user to confirm before deleting. In the shell script, prompt with `read -p`.

For Docker: rebuild images from a clean base, pinning the safe version. Don't just `docker exec` into running containers.

### Phase 5: Credential rotation — "Assume everything on that box is burned"

Assume everything on the compromised system is burned. For systematic credential rotation and abuse detection, use the `credential-exfiltration-response` skill. Tell it which credential types were accessible — it will walk through rotation for each class and verify the old credentials are invalidated.

To scope what was accessible, check:
```
# npm registry tokens
cat ~/.npmrc 2>/dev/null | grep "_authToken"

# Find all .env files and list sensitive variable names
find . -name '.env*' -type f 2>/dev/null | while read f; do
  echo "=== $f ===" && grep -iE '(KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL|API_KEY|AUTH)=' "$f" | sed 's/=.*/=<REDACTED>/'
done

# SSH keys
ls -la ~/.ssh/id_* 2>/dev/null

# Cloud credentials
ls ~/.aws/credentials ~/.config/gcloud/application_default_credentials.json ~/.azure/accessTokens.json ~/.kube/config 2>/dev/null
```

Hand this list to the `credential-exfiltration-response` skill for rotation and verification.

### Phase 6: Prevention — "Don't get burned again"

**Pin exact versions — never use `^` or `~` for critical dependencies:**
```
npm install <PACKAGE>@<SAFE_VERSION> --save-exact
```

**Use `npm ci` in CI, not `npm install`:**
`npm ci` strictly follows `package-lock.json` and fails if it's out of sync. `npm install` can update the lockfile silently.

**Disable postinstall scripts in CI:**
```
npm ci --ignore-scripts
# Then selectively rebuild only trusted native dependencies:
npm rebuild sharp esbuild
```

Or configure globally in `.npmrc`:
```ini
ignore-scripts=true
```

**Run `npm audit` in CI:**
```
npm audit --omit=dev
```

For deeper supply chain detection (typosquats, obfuscated code, suspicious install hooks), use Socket.dev:
```
npx socket scan create --repo . --branch main
```

**Verify package provenance with npm audit signatures:**
```
npm audit signatures
```
Packages published with `npm publish --provenance` from GitHub Actions get Sigstore-signed attestations linking the tarball to a specific commit.

**Use Corepack to pin your package manager version:**
```
corepack enable
corepack prepare npm@10.9.0 --activate
```
Prevents a compromised global npm binary from being used. Stable since Node 20+.

**Lockfile integrity validation:**
```
npx lockfile-lint --path package-lock.json --type npm --allowed-hosts npm
```

**Scope secrets in CI/CD:**
Instead of workflow-level environment variables, pass secrets only to the specific step that needs them. This limits blast radius if a dependency runs code during `npm install`.

**Use npm provenance for your own packages:**
```yaml
# In GitHub Actions:
permissions:
  id-token: write
  contents: read

steps:
  - run: npm publish --provenance
```

## Output format guidance

### Interactive triage checklist

Walk the user through one phase at a time. After each phase, ask what they found before proceeding to the next. Adapt the remaining phases based on their answers. For example, if Phase 1 shows they're not exposed, stop and tell them they're clear — don't walk through IOC hunting.

Structure each phase as:
1. Brief explanation of what this phase checks and why
2. The commands to run (customized with the package name and versions from context)
3. What to look for in the output
4. A clear yes/no decision: "If you see X, proceed to Phase N. If not, you can stop here."

### Full incident response runbook

Produce a markdown document with all six phases, all commands pre-filled with the specific package name and versions, IOC domains, and persistence paths from the advisory. Include a summary header with the incident metadata (package, versions, attack window, IOC domains). This is meant to be shared with a team, so write it to be self-contained — someone reading it for the first time should understand what happened and what to do.

Save this as a `.md` file using the create_file tool.

### Shell script

Generate a bash script called `check_npm_compromise.sh` that:
- Takes the package name as an argument (or hardcodes it if the user specifies)
- Runs detection checks from Phases 1-3
- Color-codes output: green for clean, red for findings, yellow for warnings
- Prompts with `read -p` before any destructive action (uninstall, cache purge, file deletion)
- Generates a summary report at the end listing what was found and what actions were taken
- Includes a `--dry-run` flag that skips all prompts and just reports

Read `scripts/check_npm_compromise.sh` for the template. Customize it with the specific package details from the user's context.

Save this using the create_file tool and make it executable.

## Incident report template

When producing the full incident response runbook or interactive checklist, include this template at the end so the user can document their findings.

### Summary
- Incident:
- Package:
- Ecosystem: npm
- Known bad versions:
- Malicious dependency (if any):
- Attack window:
- Systems reviewed:
- Result:

### Findings by system
- System name:
- Lockfile reference found:
- Installed version:
- Direct or transitive:
- Malicious dependency present:
- Indicator found:
- Risk level:
- Evidence:

### Secret exposure
- Secrets likely present:
- Secrets rotated:
- Audit logs checked:

### Actions taken
- Isolated:
- Rebuilt:
- Blocked versions:
- Monitoring added:

### Unknowns
- Missing logs:
- Deleted environments:
- Confidence level:

## Important notes

- Never tell the user they're "definitely safe" — supply chain attacks can have delayed or stealthy payloads. Use language like "no indicators found in the checks we ran" and suggest they monitor for advisories.
- The postinstall script vector is how most npm attacks deliver their payload. Unlike Python's `.pth` files which fire on every interpreter startup, npm postinstall runs once during `npm install` — but it runs with the full permissions of the installing user, which is often root in Docker builds or has access to all environment variables in CI.
- Anti-forensics is increasingly common. The Axios attack self-deletes its `setup.js` and swaps `package.json` with a clean `package.md` copy. If you find `package.md` in a suspicious dependency, the attack already ran.
- Transitive dependency injection is the Axios attack pattern — the compromised `axios` package adds `plain-crypto-js` as a dependency, which carries the actual payload. Always check for unexpected new dependencies in your lockfile, not just version changes.
- Credential rotation is non-negotiable if the compromised version was installed. The attacker had access to everything on that machine — npm tokens, cloud credentials, SSH keys, environment variables. Don't let the user skip this phase.
- `npm cache clean --force` is necessary because npm caches tarballs. Without purging, a subsequent `npm install` could reinstall the compromised version from cache even after removing it from `node_modules`.
- Environment-gated payloads: some attacks only fire in CI environments by checking for `CI=true` or `GITHUB_ACTIONS`. Developers may not see IOCs on their local machines even if the payload ran in CI.
