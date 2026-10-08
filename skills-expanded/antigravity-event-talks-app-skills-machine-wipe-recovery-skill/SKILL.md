---
name: machine-wipe-recovery
description: Standard operating runbook for rapid environment restoration after an OS wipe or new hardware setup. Restores git credentials, clones repositories via HTTPS/gh, cleans cache debt, boots local Sentinel daemons, and verifies zero-cost global deployments.
---

# Machine-Wipe Recovery Runbook (Sovereign Rebuild)

This skill operationalizes the exact recovery sequence used to reconstruct an agentic engineering workspace after a fresh machine wipe, storage restore, or clean macOS installation.

---

## 1. Identity & Toolchain Verification

On a fresh machine, never assume tools or credentials exist. Verify the foundational bus:

```bash
# 1. Check native toolchains
git --version
python3 --version

# 2. Configure Git global identity (prevents local username leakage)
git config --global user.name "Timothy Wheels"
git config --global user.email "timothywheelspro@users.noreply.github.com"
git config --global credential.helper osxkeychain
```

---

## 2. GitHub CLI Rapid Deployment & Auth

If Homebrew is absent, download the pre-compiled binary directly to `~/.local/bin/` (zero root / zero package-manager dependency):

```bash
# 1. Fetch latest macOS Apple Silicon binary
mkdir -p ~/.local/bin /tmp/gh-install
curl -sL https://github.com/cli/cli/releases/download/v2.101.0/gh_2.101.0_macOS_arm64.zip -o /tmp/gh-install/gh.zip
unzip -q /tmp/gh-install/gh.zip -d /tmp/gh-install/
cp /tmp/gh-install/gh_*/bin/gh ~/.local/bin/gh && chmod +x ~/.local/bin/gh
rm -rf /tmp/gh-install

# 2. Authenticate GitHub CLI via web flow
gh auth login --web -p https
```

---

## 3. Clone Repositories via HTTPS (Bypassing SSH Lockouts)

When SSH keys are not yet registered, clone public repositories immediately via HTTPS:

```bash
mkdir -p ~/Documents/GitHub && cd ~/Documents/GitHub
git clone https://github.com/timothywheelspro/antigravity-event-talks-app.git
git clone https://github.com/timothywheelspro/AssetDesk.git
cd antigravity-event-talks-app
```

---

## 3a. .NET 8 SDK (User-Scoped, No sudo, No Homebrew)

AssetDesk (SIS250) targets `net8.0`. Install with Microsoft's script into `~/.dotnet`
so no admin password is needed and the runbook stays reproducible:

```bash
curl -sSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 8.0 --install-dir ~/.dotnet

# Persist for every shell
cat >> ~/.zshrc <<'ZSH'
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$HOME/.dotnet:$HOME/.dotnet/tools:$PATH"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
ZSH
source ~/.zshrc

# Canary: baseline must print row counts for all three CSVs
cd ~/Documents/GitHub/AssetDesk && dotnet run
```

---

## 4. Purge Cache Debt & Guard Git Tracking

Ensure heavy framework cache folders (VitePress, Node, Python) do not bloat git:

```bash
# Untrack committed cache without deleting local files
git rm -r --cached docs/.vitepress/cache 2>/dev/null || true

# Enforce clean .gitignore
cat << 'EOF' >> .gitignore
.vitepress/cache
.vitepress/dist
docs/.vitepress/cache
docs/.vitepress/dist
__pycache__/
*.py[cod]
.DS_Store
EOF
```

---

## 5. Boot Local Sentinel Daemons

Re-establish local machine autonomy and verification services:

```bash
# Runtime/log dir (NOT versioned). The scripts themselves live in the repo under sentinel/.
mkdir -p ~/sentinel-core && cd ~/sentinel-core
REPO=~/Documents/GitHub/antigravity-event-talks-app

# Boot Origin Server (Port 8080)
nohup python3 -m http.server 8080 > origin.log 2>&1 &

# Boot Edge Drop Webhook (Port 8081) from the versioned copy
nohup python3 "$REPO/sentinel/edge-drop.py" > edge-drop.log 2>&1 &

# Verify active listeners + health
lsof -i :8080 -i :8081
curl -s http://localhost:8081/health

# Arm the git pre-push gate (once per clone)
git -C "$REPO" config core.hooksPath sentinel/hooks
```

---

## 6. Zero-Cost Global Deployment (GitHub Pages via API)

If third-party platforms (e.g. Vercel) are suspended, activate native GitHub Pages via `gh api`:

```bash
gh api -X POST /repos/timothywheelspro/antigravity-event-talks-app/pages \
  -f source='{"branch":"main","path":"/"}'

# Monitor build status until "status: built"
gh api /repos/timothywheelspro/antigravity-event-talks-app/pages/builds/latest
```
Live URL structure: `https://<owner>.github.io/<repo>/`
