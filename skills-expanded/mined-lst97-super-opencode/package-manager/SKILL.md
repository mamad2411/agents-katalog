---
name: package-manager
description: Multi-language package manager detection, selection, and standardization for JavaScript, Python, Go, Rust, Java, Ruby, PHP, .NET, and more.
---

# Package Manager Skill

## Purpose

To eliminate **package manager confusion** across all programming languages and ensure consistent, efficient dependency management. This skill automatically detects, recommends, and configures the optimal package manager for any project—preventing lockfile conflicts, install inconsistencies, and "works on my machine" issues.

**Supported Languages:** JavaScript/TypeScript, Python, Go, Rust, Java, Ruby, PHP, .NET, Elixir, Haskell, C/C++, Swift, Scala, Clojure, Julia, R

**ROI Metric**: Correct package manager selection saves 30-50% on CI build times and prevents entire classes of dependency resolution bugs.

## When to Use

- **Trigger**: **MANDATORY** at project onboarding (`/soc-onboard`).
- **Trigger**: Before any dependency installation in CI/CD pipelines.
- **Trigger**: When contributing to an existing project (detect existing choice).
- **Trigger**: When `devops-agent` sets up build pipelines.
- **Trigger**: When `backend`, `frontend`, `mobile-agent`, `data-agent`, or any other agent installs dependencies.

## Using the Detection Script (RECOMMENDED)

The detection script automates the entire detection process and provides structured output for **all supported languages**:

### Quick Detection

```bash
# Auto-detect all languages in project
.opencode/skills/package-manager/scripts/detect-package-manager.sh

# Detect specific language only
.opencode/skills/package-manager/scripts/detect-package-manager.sh python
.opencode/skills/package-manager/scripts/detect-package-manager.sh javascript
.opencode/skills/package-manager/scripts/detect-package-manager.sh go

# Get just the package manager name
PM=$(.opencode/skills/package-manager/scripts/detect-package-manager.sh --recommend)
echo "Use: $PM"

# For CI/CD or automation
PACKAGE_MANAGER=$(.opencode/skills/package-manager/scripts/detect-package-manager.sh --recommend)
$PACKAGE_MANAGER install
```

### JSON Output for Scripts

```bash
# Get structured data for all detected languages
JSON_OUTPUT=$(.opencode/skills/package-manager/scripts/detect-package-manager.sh --json)

# Extract specific values
echo "$JSON_OUTPUT" | jq -r '.languages[0].package_manager'
echo "$JSON_OUTPUT" | jq -r '.languages[0].commands.install'

# Example output for multi-language project:
{
  "project_root": "/path/to/project",
  "languages": [
    {
      "language": "javascript",
      "package_manager": "pnpm",
      "version": "8.15.0",
      "detection_method": "lockfile",
      "confidence": 95,
      "commands": {
        "install": "pnpm install --frozen-lockfile",
        "add": "pnpm add",
        "add_dev": "pnpm add -D",
        "run": "pnpm",
        "exec": "pnpm dlx"
      }
    },
    {
      "language": "python",
      "package_manager": "poetry",
      "version": "1.7.0",
      "detection_method": "lockfile",
      "confidence": 95,
      "commands": {
        "install": "poetry install",
        "add": "poetry add",
        "add_dev": "poetry add --group dev",
        "run": "poetry run"
      }
    }
  ]
}
```

### Multi-Language Projects

For projects using multiple languages (e.g., full-stack with Python backend and JavaScript frontend):

```bash
# Detect all languages automatically
.opencode/skills/package-manager/scripts/detect-package-manager.sh --all

# This will detect and report package managers for ALL languages found in the project
```

## Supported Languages & Package Managers

### JavaScript/TypeScript

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **pnpm** | pnpm-lock.yaml, pnpm-workspace.yaml | pnpm-lock.yaml |
| **yarn** | yarn.lock | yarn.lock |
| **npm** | package-lock.json, package.json | package-lock.json |
| **bun** | bun.lockb | bun.lockb |

### Python

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **uv** | uv.lock, pyproject.toml [tool.uv] | uv.lock |
| **poetry** | poetry.lock, pyproject.toml [tool.poetry] | poetry.lock |
| **pipenv** | Pipfile.lock | Pipfile.lock |
| **conda** | environment.yml, conda-lock.yml | environment.yml |
| **pip** | requirements.txt, setup.py, setup.cfg | requirements.txt |

### Go

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **go modules** | go.mod, go.sum | go.mod |

### Rust

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **cargo** | Cargo.toml, Cargo.lock | Cargo.toml |

### Java

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **maven** | pom.xml | pom.xml |
| **gradle** | build.gradle, build.gradle.kts | build.gradle |

### Ruby

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **bundler** | Gemfile, Gemfile.lock | Gemfile |

### PHP

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **composer** | composer.json, composer.lock | composer.json |

### .NET

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **nuget** | .csproj, .sln, packages.config | *.csproj |

### Elixir

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **mix** | mix.exs, mix.lock | mix.exs |

### Haskell

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **stack** | stack.yaml | stack.yaml |
| **cabal** | *.cabal | *.cabal |

### C/C++

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **conan** | conanfile.txt, conanfile.py | conanfile.txt |
| **vcpkg** | vcpkg.json | vcpkg.json |

### Swift

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **swift package manager** | Package.swift | Package.swift |

### Scala

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **sbt** | build.sbt | build.sbt |

### Clojure

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **leiningen** | project.clj | project.clj |
| **tools.deps** | deps.edn | deps.edn |

### Julia

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **Pkg** | Project.toml, Manifest.toml | Project.toml |

### R

| Package Manager | Detection Method | Files Checked |
|:----------------|:----------------|:-------------|
| **renv** | renv.lock | renv.lock |
| **packrat** | packrat.lock | packrat.lock |

## The Detection Protocol

### 1. Lockfile Detection (Highest Confidence)

Lockfiles provide the strongest signal of which package manager is in use:

| Lockfile | Package Manager | Confidence |
|:---------|:----------------|:----------:|
| pnpm-lock.yaml | pnpm | 95% |
| bun.lockb | bun | 95% |
| poetry.lock | poetry | 95% |
| uv.lock | uv | 95% |
| yarn.lock | yarn | 90% |
| package-lock.json | npm | 90% |
| Cargo.lock | cargo | 95% |
| Gemfile.lock | bundler | 95% |
| composer.lock | composer | 95% |
| mix.lock | mix | 95% |
| go.sum | go modules | 95% |

### 2. Configuration File Detection

When no lockfile exists, configuration files provide the signal:

| Config File | Package Manager | Confidence |
|:------------|:----------------|:----------:|
| package.json + packageManager field | (as specified) | 100% |
| pyproject.toml [tool.poetry] | poetry | 90% |
| pyproject.toml [tool.uv] | uv | 90% |
| environment.yml | conda | 90% |
| requirements.txt | pip | 85% |
| pom.xml | maven | 95% |
| build.gradle | gradle | 95% |

### 3. Heuristic Detection (Lower Confidence)

When no explicit markers exist:

| Heuristic | Package Manager | Confidence |
|:----------|:----------------|:----------:|
| packages/ directory | pnpm | 80% |
| No indicators | npm (JS) / pip (Python) | 60% |

## Language-Specific Recommendations

### JavaScript/TypeScript Decision Matrix

| Factor | npm | yarn | pnpm | bun |
|:-------|:---:|:----:|:----:|:---:|
| **Disk Space** | High | Medium | Low | Low |
| **Install Speed** | Slow | Medium | Fast | Very Fast |
| **Monorepo Support** | Limited | Workspaces | Excellent | Limited |
| **Strictness** | Lenient | Moderate | Strict | Moderate |
| **CI/CD Compatibility** | Universal | Good | Good | Limited |
| **Recommendation** | Safe default | Reliable | **Preferred** | Experimental |

### Python Decision Matrix

| Factor | pip | poetry | uv | conda | pipenv |
|:-------|:---:|:------:|:--:|:-----:|:------:|
| **Speed** | Slow | Medium | Very Fast | Medium | Slow |
| **Virtual Env** | Manual | Built-in | Built-in | Built-in | Built-in |
| **Lock Files** | No | Yes | Yes | Yes | Yes |
| **Data Science** | Poor | Poor | Poor | **Excellent** | Poor |
| **Recommendation** | Legacy | Good | **Preferred** | Data Science | Avoid |

## CI/CD Integration

### GitHub Actions Example

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect Package Manager
        id: detect
        run: |
          PM=$(./.opencode/skills/package-manager/scripts/detect-package-manager.sh --recommend)
          echo "package_manager=$PM" >> $GITHUB_OUTPUT
          
      - name: Setup Node.js (if JS)
        if: steps.detect.outputs.package_manager == 'npm' || steps.detect.outputs.package_manager == 'yarn' || steps.detect.outputs.package_manager == 'pnpm'
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Setup Python (if Python)
        if: steps.detect.outputs.package_manager == 'poetry' || steps.detect.outputs.package_manager == 'pip'
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install Dependencies
        run: |
          ${{ steps.detect.outputs.package_manager }} install
```

## Command Reference

### JavaScript/TypeScript

```bash
# npm
npm ci                    # Clean install
npm install <package>     # Add dependency
npm install --save-dev <package>  # Add dev dependency
npm run <script>          # Run script
npx <package>             # Execute package

# yarn
yarn install --frozen-lockfile
yarn add <package>
yarn add --dev <package>
yarn <script>
yarn dlx <package>

# pnpm (Recommended)
pnpm install --frozen-lockfile
pnpm add <package>
pnpm add -D <package>
pnpm <script>
pnpm dlx <package>

# bun
bun install
bun add <package>
bun add -d <package>
bun run <script>
bunx <package>
```

### Python

```bash
# pip
pip install -r requirements.txt
pip install <package>
pip install <package> --dev
python <script>

# poetry (Recommended)
poetry install
poetry add <package>
poetry add --group dev <package>
poetry run <command>
poetry run python <script>

# uv (Fastest)
uv sync
uv add <package>
uv add --dev <package>
uv run <command>

# conda (Data Science)
conda env create -f environment.yml
conda install <package>
conda run <command>
```

### Go

```bash
go mod download           # Install dependencies
go get <package>          # Add dependency
go run <file>             # Run script
go build                  # Build
```

### Rust

```bash
cargo fetch               # Download dependencies
cargo add <package>       # Add dependency
cargo add --dev <package> # Add dev dependency
cargo run                 # Run project
cargo build               # Build
```

## Migration Guides

### JavaScript: npm → pnpm

```bash
# 1. Delete old lockfile
rm package-lock.json

# 2. Install with pnpm
pnpm install

# 3. Update package.json
echo '{"packageManager": "pnpm@8.15.0"}' >> package.json

# 4. Update CI/CD to use pnpm
```

### Python: pip → poetry

```bash
# 1. Initialize poetry
poetry init

# 2. Import requirements
poetry add $(cat requirements.txt)

# 3. Install
poetry install
```

## Execution Template

```markdown
## 📦 Package Manager Setup

### 1. Detection
**Script**: `.opencode/skills/package-manager/scripts/detect-package-manager.sh --json`

**Detected Languages**:
| Language | Package Manager | Confidence |
|:---------|:----------------|:----------:|
| JavaScript | pnpm | 95% |
| Python | poetry | 95% |

### 2. Installation Commands
**JavaScript**: `pnpm install --frozen-lockfile`
**Python**: `poetry install`

### 3. CI/CD Setup
- [ ] GitHub Actions workflow updated
- [ ] Cache configured correctly
- [ ] Multi-language support verified

### 4. Team Documentation
- [ ] README updated with setup instructions
- [ ] CONTRIBUTING.md updated
- [ ] Team notified of package manager choices
```

## Integration with Agents

- **`devops-agent`**: Uses this skill for all CI/CD pipeline setups.
- **`backend`**: Detects Python, Go, Rust, Java, etc.
- **`frontend`**: Detects JavaScript/TypeScript package managers.
- **`mobile-agent`**: Detects Swift (iOS), Gradle (Android).
- **`data-agent`**: Detects Python (data science), R, Julia.
- **`pm-agent`**: Ensures package manager consistency across team.

## Anti-Patterns (Avoid)

### ❌ Mixed Package Managers in Same Language

```
Developer A: Uses npm (creates package-lock.json)
Developer B: Uses yarn (creates yarn.lock)
Result: Inconsistent dependencies
```

**Fix**: Enforce single package manager via `packageManager` field.

### ❌ No Lockfiles in Version Control

```
Project: No lockfiles committed
Result: Non-reproducible builds
```

**Fix**: Always commit lockfiles (except for libraries).

### ❌ Wrong Package Manager for Use Case

```
Data Science project: Uses pip instead of conda
Result: Missing scientific libraries
```

**Fix**: Use conda for data science, poetry/uv for general Python.

## Script Files

- **Main Script**: `.opencode/skills/package-manager/scripts/detect-package-manager.sh`
- **Documentation**: `.opencode/skills/package-manager/scripts/README.md`

**Note**: The script is bash 3.2 compatible (macOS default) and requires no external dependencies.
