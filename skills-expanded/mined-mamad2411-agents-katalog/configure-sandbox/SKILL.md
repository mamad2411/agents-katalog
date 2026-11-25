---
name: configure-sandbox
description: Guide users through configuring local sandboxing in workspace and/or global settings YAML. Use when users ask to enable sandboxing, configure sandboxing, choose read-only vs read-write sandboxing, set network policy, inspect sandbox settings, or update .poolside/settings.local.yaml or global settings.
metadata:
  version: "0.2.0"
  language: en
  optimized: true
  quick-reference: true
  icon: "📦"
  tags:
    - sandbox
    - config
    - poolside
    - yaml
    - security
    - network
  github: "https://github.com/sirisakboy/sell/tree/main/skills/configure-sandbox/"
  import-mode: read-only
  sync: auto-from-source
---
    - sandbox
    - config
    - poolside
    - yaml
    - security
    - network
---
# Configure Sandboxing (Optimized v0.2.0)
Guide the user through configuring local sandboxing for pool — fast and accurately.
---
## 🎯 Quick Reference (TL;DR)
| Scenario | YAML Snippet |
|----------|-------------|
| **Filesystem sandbox (read-only)** | `sandbox.filesystem.workspaces.access: read-only` |
| **Shell sandbox (read-write)** | `sandbox.filesystem.workspaces.access: read-write` |
| **Custom image** | Add `sandbox.image: <tag>` |
| **Block network** | `sandbox.network.policy: off` |
| **Allow-list networks** | `sandbox.network.policy: allow-list` + egress lists |
| **Expose env var** | `sandbox.env_vars.KEY: value` |
| **Mount host path** | `sandbox.filesystem.mounts` entry |
---
## 💡 Goal
Write a `sandbox:` configuration to one or both of:
- **Workspace-local**: `<workspace>/.poolside/settings.local.yaml`
- **Shared workspace**: `<workspace>/.poolside/settings.yaml`
- **Global user settings**: the Poolside user config `settings.yaml`
> **Default recommendation**: Use workspace-local for project-specific choices. Use global for defaults across many workspaces.
---
## ❓ Use Questions (When Available)
If the `question` tool is available, ask concise questions:
1. **Scope**: This workspace only, global defaults, or both?
2. **Sandbox mode**:
   - **Filesystem sandboxing** (`read-only`): workspace mounted read-only; agent changes staged for review
   - **Shell sandboxing** (`read-write`): tools run in a container; workspace writes apply directly
3. **Image**: default (`ubuntu:22.04`) or custom tag?
4. **Network policy**: unrestricted, block all, allow-list only, or leave unchanged?
5. **Environment/secrets/mounts**: any env vars, named secrets, or extra host paths?
If `question` is unavailable, explain choices and ask the user to pick before editing files.
---
## ⚙️ Configuration Model
Pool enables local sandboxing when a loaded settings file contains a top-level `sandbox:` object. Settings are merged from **lowest to highest** priority:
1. Global user settings → 2. Shared workspace settings → 3. Local workspace settings
4. Higher-priority scalar fields override lower-priority values
5. `env_vars` are merged by key; `network` and `filesystem` are **replacement-style** at higher priority
### Important Defaults
- `sandbox:` absent everywhere → sandbox **disabled**
- `sandbox:` present but `filesystem.workspaces.access` omitted → defaults to `read-write` (shell sandboxing)
- `image` omitted → `ubuntu:22.04`
- `network` omitted or `policy: unsafe-allow-all` → network **unrestricted**
---
## 📄 YAML Reference
### Minimal Configurations
**Filesystem sandboxing (read-only):**
```yaml
sandbox:
  filesystem:
    workspaces:
      access: read-only
```
**Shell sandboxing (read-write):**
```yaml
sandbox:
  filesystem:
    workspaces:
      access: read-write
```
**With custom image:**
```yaml
sandbox:
  image: ubuntu:24.04
  filesystem:
    workspaces:
      access: read-only
```
### Network Policies
**Unrestricted (explicit):**
```yaml
sandbox:
  network:
    policy: unsafe-allow-all
```
**Block all egress:**
```yaml
sandbox:
  network:
    policy: off
```
**Allow-list domains + CIDRs:**
```yaml
sandbox:
  network:
    policy: allow-list
    egress:
      allowed_domains:
        - github.com
        - api.example.com
      allowed_cidrs:
        - 10.0.0.0/8
```
### Environment Variables, Secrets, and Mounts
```yaml
sandbox:
  env_vars:
    NODE_ENV: development
  secrets:
    - GITHUB_TOKEN
  filesystem:
    workspaces:
      access: read-only
    mounts:
      - host: /absolute/host/path
        sandbox: /mnt/data
        access: read-only
```
> **Notes**:
> - `env_vars` values are literal strings — **never** store secret values here
> - `secrets` names must match pool's secret store — do **not** ask user to reveal secret values
> - `filesystem.mounts[].host` and `sandbox` must be absolute paths
> - Mount access: `read-only` or `read-write`
---
## 🔧 Editing Workflow (Step-by-Step)
1. **Inspect** existing settings files:
   - `<workspace>/.poolside/settings.local.yaml`
   - `<workspace>/.poolside/settings.yaml`
   - global `settings.yaml` (if configuring global defaults)
2. **Create** `.poolside/` directory if it doesn't exist
3. **Merge or update** only the `sandbox:` section — never overwrite unrelated settings
4. **Avoid duplicate keys** in YAML
5. **Never overwrite wholesale** unless the file only contains obsolete sandbox content and user agreed
6. **After editing**, summarize:
   - Which file(s) changed
   - Effective sandbox mode
   - Image choice
   - Network policy
   - Secrets, env vars, or mounts configured
---
## ✅ Verification
1. Start a **new session** (`/new`) — sandbox config loads at session creation
2. Run in the new session:
   ```
   /sandbox
   ```
3. `/sandbox` reports: effective state, selected image, network policy, and configuration sources
> ⚠️ Running `/sandbox` in an **old** session may still show the previous state — sandbox was already initialized.
---
## 🛠️ Optimizations Applied (v0.2.0)
- **Quick Reference table**: Instant lookup for common scenarios
- **Inline scope guidance**: Clear recommendation on when to use workspace-local vs global
- **Config model summary**: Priority order + merge rules in one list
- **Validation checklist**: 6-step editing workflow with explicit preservation rules
- **Verification shortcut**: Exact command to run (`/sandbox`) + warning about old sessions