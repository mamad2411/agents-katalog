---
name: pinrag-release
description: Cut a new pinrag release: bump version, tag, push, and create a GitHub Release (pinrag repo only)
disable-model-invocation: true
---

# Release pinrag

**Scope:** Use this skill only when the user is working in the pinrag repo (this skill lives at `.cursor/skills/pinrag-release/`).

Cut a new pinrag release: bump version, tag, push, and create a GitHub Release (which triggers PyPI publish).

## Steps

1. **Determine version** — If the user provides a version (e.g. `0.7.0`), use it. Otherwise read `pyproject.toml` and suggest the next patch (e.g. `0.6.0` → `0.6.1`) or ask the user.

2. **Bump version** — Set `version = "X.Y.Z"` in **`pyproject.toml`** and the same **`X.Y.Z`** in **`server.json`**: the top-level `"version"` field and `packages[0].version` (MCP Registry metadata for the PyPI package). Keep them in lockstep on every release.

3. **Commit and push** — Run:
   ```bash
   git add pyproject.toml server.json && git commit -m "Bump version to X.Y.Z" && git push origin main
   ```

4. **Tag and push** — Run:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

5. **Create GitHub Release** — Run:
   ```bash
   gh release create vX.Y.Z --notes "Placeholder"
   ```
   Then edit with real notes:
   ```bash
   gh release edit vX.Y.Z --notes "PASTE_NOTES_HERE"
   ```
   Or create with notes in one step if the user provides them.

6. **Release notes format** — Match existing releases. Scan all commits and changes from the previous release to draft notes:
   - Title: `# vX.Y.Z — Short subtitle`
   - Summary: One line describing the release.
   - Sections: `## Section name` (e.g. Configuration, Evaluation, Docs).
   - Bullets: `- **Topic** — Detail.`
   - To draft from diff: `git log vPREV..vX.Y.Z --oneline` and `git diff vPREV..vX.Y.Z --stat`

## Notes

- Publishing the GitHub Release runs the workflow and publishes to PyPI. Tag push alone does not publish.
- If `gh` is not available or the user prefers manual PyPI: `uv build && uv publish` (use PyPI API token when prompted).
- Ensure you are on `main` and have no uncommitted changes before starting.

### MCP Registry (`mcp-publisher`)

The README must include the PyPI ownership line `<!-- mcp-name: io.github.ndjordjevic/pinrag -->` (so the published package description on PyPI contains it). **On each release**, after bumping versions in `pyproject.toml` and `server.json`, ship the release so PyPI is updated.

**Automated (default):** Creating a **GitHub Release** runs `.github/workflows/publish.yml`, which publishes to PyPI and then runs **`mcp-publisher login github-oidc`** + **`mcp-publisher publish`** in CI (OIDC; no extra secrets). A job waits until the new version appears on PyPI before publishing metadata.

**Manual (fallback):** If you skip CI or need to re-publish metadata, run `mcp-publisher login github` and `mcp-publisher publish` from the repo root (with `server.json` present) **after** the matching version is on PyPI.

If you keep the official CLI binary in the **repo root** as `./mcp-publisher` (listed in `.gitignore`, not committed), use `./mcp-publisher login github` and `./mcp-publisher publish` from that directory. Otherwise install via Homebrew (`brew install mcp-publisher`) or download from the [registry releases](https://github.com/modelcontextprotocol/registry/releases) so `mcp-publisher` is on your `PATH`.

The MCP Registry enforces **`server.json` `description` length ≤ 100 characters**; if `publish` returns 422 on `body.description`, shorten the string and try again.

**Verify (search API returns multiple versions):** The registry search endpoint can return **more than one** `servers[]` entry (older + latest). Do not read only `servers[0]`—it may be an older version. To print the **latest** published version:

```bash
curl -fsS "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.ndjordjevic/pinrag" \
  | jq -r '.servers[] | select(._meta["io.modelcontextprotocol.registry/official"].isLatest == true) | .server.version'
```
