---
name: speckit-install
description: Install the Specify CLI on the host machine (uv tool install or uvx one-time); supports multiple OS, persistent or one-time install, and corporate or restricted-network environments. Use when the user says "install Spec Kit", "install Specify CLI", or "specify command not found".
---

# Spec Kit Install Skill

Install the [Specify CLI](https://github.com/github/spec-kit) so that `specify` is available in PATH (or use one-time `uvx`). This skill covers only **installing the CLI**; it does not run `specify init`. For project initialization after install, use **speckit-initial**.

## When to Use

- First-time Spec Kit setup ("install Spec Kit", "install Specify CLI").
- CI or scripts that need to pre-install the CLI.
- Upgrading the CLI (`uv tool install --force`).
- User reports "specify command not found" or "specify: command not found".

## Prerequisites

- **uv**: [Astral uv](https://docs.astral.sh/uv/) for installing the CLI. If uv is not installed, guide the user to install it first (e.g. `curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS, or see uv docs for Windows).
- **Python 3.11+** when using uv (uv typically bundles or uses system Python).
- **Git** (optional for install; required later for `specify init` with git).

## Workflow

1. **Check if already installed**
   - Suggest running `specify --version` or `specify check`. If the command succeeds, the CLI is already installed; suggest **speckit-initial** for project init or **speckit-check** for environment verification.

2. **Persistent install (recommended)**
   - Run: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
   - This makes `specify` available in PATH for all projects.
   - **Upgrade**: `uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git`

3. **One-time usage (no PATH install)**
   - Run: `uvx --from git+https://github.com/github/spec-kit.git specify init <project_name_or_.> --ai <agent>`
   - Use when the user does not want to install the tool permanently (e.g. quick try, CI one-off). Document that subsequent `specify init` or `specify check` in the same session can reuse the same `uvx` prefix or require re-running with full `uvx --from ...` if not installed.

4. **Corporate or restricted network**
   - Set `GH_TOKEN` or `GITHUB_TOKEN` for GitHub API access if needed.
   - For `specify init` (handled in **speckit-initial**): `--github-token <token>` or env var. For install, uv may need network access to clone the repo; if TLS issues occur, document that uv/spec-kit may support `--skip-tls` or similar only where explicitly documented (avoid recommending insecure options unless user is in a controlled environment).

## Outputs

- **Persistent install**: `specify` is available in PATH; user can run `specify init`, `specify check` in any directory.
- **One-time**: No change to PATH; user runs `uvx --from git+https://github.com/github/spec-kit.git specify ...` for each use.

## Next Steps

- After install: use **speckit-initial** to run `specify init` in a project, or **speckit-check** to verify the environment.

## Different Environments

| Environment | Notes |
|-------------|--------|
| **Linux** | Install uv if needed; then `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`. WSL: same as Linux. |
| **macOS** | Same as Linux; ensure Python 3.11+ available for uv if required. |
| **Windows** | Install uv (see uv docs); use PowerShell or cmd. For project init, **speckit-initial** will use `--script ps` when needed. |
| **Corporate / proxy** | Use GH_TOKEN/GITHUB_TOKEN if GitHub API is restricted; ensure uv can reach GitHub. |
| **CI** | Prefer persistent install in a cacheable step: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`; then run `specify init` or `specify check` in the same runner. |

## Troubleshooting

- **uv not found**: Direct user to install [uv](https://docs.astral.sh/uv/).
- **Python version**: uv usually manages Python; if errors mention Python, ensure 3.11+ is available.
- **Network / SSL**: Check firewall, proxy, and GitHub access; avoid disabling TLS unless necessary and documented.
- **Permission errors**: On Linux/macOS, user install with uv typically does not need sudo; if using system Python, consider user-level uv install.

## References

- [GitHub spec-kit](https://github.com/github/spec-kit) — Get Started: Install Specify CLI
- [uv documentation](https://docs.astral.sh/uv/)

## 国内适配

- 支持中文文档和中文注释
- 示例代码兼容国内开发环境
- 提供中文 FAQ 和常见问题解答

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
