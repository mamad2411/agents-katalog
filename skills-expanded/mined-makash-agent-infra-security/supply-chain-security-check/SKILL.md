---
name: supply-chain-security-check
description: Investigate whether a project, environment, container, or CI pipeline is affected by a dependency supply chain incident across any ecosystem. Use this skill when the user mentions a compromised package and the ecosystem is NOT npm/Node.js, NOT Python/PyPI, and NOT GitHub Actions — those have dedicated skills (npm-supply-chain-response, pypi-supply-chain-response, github-actions-supply-chain-response). Use this skill for Go, Rust, Ruby, Java/Maven, .NET/NuGet, Docker, or when the ecosystem is unknown or spans multiple ecosystems. Also use when the user asks a general "am I affected?" question without specifying an ecosystem.
license: MIT
compatibility: Requires Bash. Optional per ecosystem — see command reference table.
---

# Supply Chain Security Check

Generic incident response for supply chain compromises across any package ecosystem.

**Routing note:** If the compromised package is from npm/Node.js, Python/PyPI, or GitHub Actions, use the dedicated ecosystem skill instead — they have deeper IOC libraries, ecosystem-specific forensics, and tailored detection commands. This skill covers Go, Rust, Ruby, Java, .NET, Docker, multi-ecosystem incidents, and any ecosystem without a dedicated skill.

## When to use

- A package on crates.io, RubyGems, Maven Central, NuGet, Go modules, Docker Hub, or any other registry is reported compromised
- A transitive dependency may have pulled in a bad version
- You need a fast answer on "do we use this anywhere?"
- The incident spans multiple ecosystems (e.g., a compromised CI action that published malicious packages to both npm and PyPI)
- The ecosystem is unknown and you need to identify it first
- You need a clean incident note for engineering or security

## Inputs

Collect from the user before starting. Don't re-ask for information already provided.

**Required:**
- Package name
- Ecosystem (python, node, go, rust, ruby, java, dotnet, docker — or "unknown")
- Known bad versions

**Helpful but not required:**
- Known safe version or mitigation
- Attack window (UTC)
- Indicators of compromise (C2 domains, persistence paths, process names)
- Repos, folders, images, or runners to inspect
- Build logs, lockfiles, SBOMs, image digests, CI logs

## Workflow

### Phase 1: Confirm incident facts

Collect:
- Bad versions and attack window
- Package manager and registry affected
- Official advisory or source
- Indicators of compromise
- Whether pinned containers, vendored dependencies, or source installs were unaffected

### Phase 2: Find direct references in source

Search lockfiles and dependency manifests using the ecosystem-appropriate files:

| Ecosystem | Manifest files | Lockfiles |
|-----------|---------------|-----------|
| Go | `go.mod` | `go.sum` |
| Rust | `Cargo.toml` | `Cargo.lock` |
| Ruby | `Gemfile` | `Gemfile.lock` |
| Java | `pom.xml`, `build.gradle`, `build.gradle.kts` | — |
| .NET | `*.csproj`, `*.fsproj`, `packages.config` | `packages.lock.json` |
| Docker | `Dockerfile`, `docker-compose.yml` | — |
| Python | `requirements*.txt`, `pyproject.toml`, `Pipfile` | `poetry.lock`, `uv.lock`, `Pipfile.lock` |
| Node | `package.json` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |

Also search:
- CI workflows (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
- Install scripts, bootstrap scripts
- Docs or examples with install commands

```bash
# Generic search across all file types
rg -n "<PACKAGE>" .
find . -name "*.lock" -o -name "*.toml" -o -name "*.mod" -o -name "Gemfile*" -o -name "pom.xml" -o -name "*.gradle" -o -name "*.csproj" | xargs grep -l "<PACKAGE>" 2>/dev/null
```

### Phase 3: Find transitive use in built environments

Check the actual installed environment, not just source files.

| Ecosystem | Check installed version | Show dependency tree |
|-----------|----------------------|---------------------|
| Go | `go list -m <PACKAGE>` | `go mod graph \| grep <PACKAGE>` |
| Rust | `cargo tree -p <PACKAGE>` | `cargo tree -i <PACKAGE>` |
| Ruby | `bundle show <PACKAGE>` | `bundle exec gem dependency <PACKAGE> --reverse-dependencies` |
| Java (Maven) | `mvn dependency:tree \| grep <PACKAGE>` | `mvn dependency:tree` |
| Java (Gradle) | `gradle dependencies \| grep <PACKAGE>` | `gradle dependencies` |
| .NET | `dotnet list package` | `dotnet list package --include-transitive` |
| Docker | `docker run --rm <IMAGE> <pkg_cmd>` | Inspect image layers: `docker history <IMAGE>` |
| Python | `pip show <PACKAGE>` | `pipdeptree -r -p <PACKAGE>` |
| Node | `npm ls <PACKAGE>` | `npm ls <PACKAGE>` / `yarn why <PACKAGE>` |

Determine:
- Whether the package was installed
- Which top-level package pulled it in (transitive exposure)
- Whether the resolved version matches a known bad version
- Whether install timing overlaps the incident window

### Phase 4: Hunt for indicators of compromise

Look for:
- Suspicious files in package install directories
- Outbound connections to unknown domains
- Unusual subprocess creation or process spawning
- Secrets access patterns (recent access times on credential files)
- Ecosystem-specific hooks (Python `.pth` files, npm `postinstall`, Ruby `extconf.rb`)
- Package versions installed during the incident window

**Credential access evidence:**
```bash
find ~/.ssh ~/.aws ~/.config/gcloud ~/.kube -atime -1 2>/dev/null
stat ~/.ssh/id_rsa 2>/dev/null | grep Access
```

**Process inspection:**
```bash
ps aux | grep -v grep | grep -iE "<SUSPICIOUS_PATTERN>"
```

**Network indicators:**
```bash
ss -tnp 2>/dev/null | grep -i "<C2_DOMAIN>"
grep -rF "<C2_DOMAIN>" /var/log/ 2>/dev/null
```

**Persistence checks:**
```bash
# systemd user services
find ~/.config/systemd/user/ -name "*.service" -mtime -7 2>/dev/null
# Cron jobs
crontab -l 2>/dev/null
# Scripts in config directories
find ~/.config -name "*.py" -o -name "*.sh" -o -name "*.rb" | xargs ls -lt 2>/dev/null | head -20
```

**Kubernetes (if applicable):**
```bash
kubectl get pods -n kube-system --sort-by=.metadata.creationTimestamp
kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged == true) | .metadata.name'
kubectl get secrets --all-namespaces --sort-by=.metadata.creationTimestamp | tail -20
```

### Phase 5: Classify impact

Classify each finding as:
- **Not present** — package not found anywhere
- **Present, safe version** — installed but not a compromised version
- **Present, likely affected** — compromised version was installed
- **Present, insufficient evidence** — package found but version or install timing unclear
- **Confirmed compromise** — compromised version installed AND IOC indicators found

### Phase 6: Recommend actions

If affected:
- Isolate host, runner, or container
- Remove malicious artifacts
- Rebuild from known-good base
- Pin or block bad versions
- Audit transitive constraints
- Review CI/CD and dependency caches
- Add registry and dependency monitoring

**Credential rotation:** Hand off to the `credential-exfiltration-response` skill for systematic rotation. Scope what credentials were accessible on the compromised system first:
```bash
# List credential files present
ls ~/.ssh/id_* ~/.aws/credentials ~/.config/gcloud/application_default_credentials.json ~/.kube/config ~/.npmrc ~/.pypirc ~/.docker/config.json 2>/dev/null

# Find .env secrets to rotate
find . -name ".env*" -exec grep -h "KEY\|SECRET\|TOKEN\|PASSWORD\|CREDENTIAL" {} \; | cut -d= -f1 | sort -u
```

Tell the credential skill which types were accessible, the attack window, and whether IOCs suggest active credential use.

### Phase 7: Prevention

**Pin exact versions** in dependency files — never use range specifiers for critical dependencies.

| Ecosystem | Pin syntax | Lockfile with hashes |
|-----------|-----------|---------------------|
| Go | `go get <PACKAGE>@v1.2.3` | `go.sum` (automatic) |
| Rust | `<PACKAGE> = "=1.2.3"` in Cargo.toml | `Cargo.lock` (automatic) |
| Ruby | `gem '<PACKAGE>', '1.2.3'` | `Gemfile.lock` (automatic) |
| Java | `<version>1.2.3</version>` (no ranges) | — |
| .NET | `Version="1.2.3"` (no wildcards) | `packages.lock.json` |
| Python | `<PACKAGE>==1.2.3` | `pip-compile --generate-hashes` |
| Node | `npm install --save-exact` | `npm ci` (lockfile-only) |

**Generate an SBOM** so you can answer "am I affected?" in seconds next time.

**Scope secrets in CI/CD** — pass secrets only to the specific step that needs them.

## Output template

### Executive summary
State whether the project, image, runner, or host appears affected.

### Findings
For each repo, environment, image, or host:
- Package present or absent
- Direct or transitive
- Resolved version
- Evidence
- Risk level

### Immediate actions
- Containment
- Credential rotation scope (hand off to `credential-exfiltration-response`)
- Rebuild scope
- Pinning or blocking recommendation

### Unknowns
List what still cannot be proven from available evidence.

## Important notes

- Never tell the user they're "definitely safe" — supply chain attacks can have delayed or stealthy payloads. Use language like "no indicators found in the checks we ran."
- Transitive dependency exposure is the most common way developers are affected. Most people don't realize a compromised package was pulled in by something they explicitly installed.
- If the ecosystem is npm, Python/PyPI, or GitHub Actions, redirect to the dedicated skill — they have deeper IOC libraries and ecosystem-specific forensics that this generic skill cannot match.
- Credential rotation is non-negotiable if the compromised version was installed. Use the `credential-exfiltration-response` skill for the full detect/rotate/verify lifecycle.
- For multi-ecosystem incidents (e.g., a compromised CI action that published malicious packages to multiple registries), run this skill once per ecosystem and coordinate credential rotation across all of them.
