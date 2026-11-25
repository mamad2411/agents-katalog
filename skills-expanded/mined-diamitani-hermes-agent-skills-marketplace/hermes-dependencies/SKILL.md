---
name: hermes-dependencies
description: Install and manage Python packages in the Hermes Agent virtual environment. Covers uv pip workflows, namespace-conflict recovery, disk space cleanup, and common packaging pitfalls.
version: 1.0.0
created_by: agent
metadata:
  hermes:
    tags: [hermes, python, dependencies, venv, pip, uv, disk-space, troubleshooting]
---

# Hermes Dependencies

Manage Python packages inside the Hermes Agent virtual environment. Hermes runs in its own venv at `~/.hermes/hermes-agent/venv/` with a modern Python (3.11+). Use `uv` for all package operations — the system `pip` often points at an older Python and will pick up wrong dependencies.

## Quick Reference

```bash
# Install a package
uv pip install <package> --python ~/.hermes/hermes-agent/venv/bin/python

# Uninstall
uv pip uninstall <package> --python ~/.hermes/hermes-agent/venv/bin/python

# List installed packages
uv pip list --python ~/.hermes/hermes-agent/venv/bin/python

# Show package details
uv pip show <package> --python ~/.hermes/hermes-agent/venv/bin/python

# Check what would be installed (dry run)
uv pip install <package> --dry-run --python ~/.hermes/hermes-agent/venv/bin/python
```

## Disk Space Management

The Hermes venv shares disk with the rest of the system. When `uv pip install` fails with "No space left on device" (errno 28), clear these in order of impact:

1. **Failed Playwright browser cache** (~500MB): `rm -rf ~/Library/Caches/ms-playwright`
2. **npm cache**: `npm cache clean --force`
3. **OpenAI/Codex caches**: `rm -rf ~/Library/Caches/com.openai.{codex,atlas}`
4. **Build artifacts in /tmp**: check `du -sh /tmp/* | sort -rh | head -10`

Use `df -h /` to check available space before large installs.

## Namespace Package Conflicts

Some packages (notably `composio`) ship as namespace packages where multiple distributions (`composio-core`, `composio-client`, `composio`) try to own the same `composio/` directory. When you uninstall one, it may remove `__init__.py` but leave the directory — breaking all other composio packages.

**Symptoms:**
- `import composio` succeeds but has no attributes
- `composio.__path__` shows as `_NamespacePath`, not a real path
- `composio.__file__` is `None`

**Fix — clean reinstall:**
```bash
# 1. Remove all conflicting packages
uv pip uninstall composio composio-client composio-core --python ~/.hermes/hermes-agent/venv/bin/python

# 2. Delete the leftover namespace directory
rm -rf ~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/composio

# 3. Reinstall only what you need
uv pip install composio-core --python ~/.hermes/hermes-agent/venv/bin/python
```

**Composio-specific:** Install only `composio-core`. The full `composio` CLI package (0.18.0) and `composio-client` (1.42.0) are version-incompatible with each other and with `composio-core` (0.7.21). `composio-core` alone provides the complete Python API including `Composio`, `ComposioToolSet`, `Action`, `Trigger`, etc.

## Pitfalls

- **Wrong Python**: Using bare `pip3 install` may target the system Python 3.9, which then picks up Hermes venv packages from `sys.path` and crashes with `TypeError` on `|` union syntax. Always use `uv pip install --python <venv-path>`.
- **Missing `__init__.py` after uninstall**: If a package worked before an uninstall/reinstall cycle, check for leftover namespace directories (see Namespace Package Conflicts above).
- **Disk-full errors mid-install**: `uv` downloads wheels to `~/.cache/uv/`. If disk fills during extraction, clear both the target cache and `~/.cache/uv/`, then retry.
- **PEP 668 externally-managed environment**: The system Python on macOS is PEP 668-protected. Never `pip install` into it. Always use the Hermes venv.
