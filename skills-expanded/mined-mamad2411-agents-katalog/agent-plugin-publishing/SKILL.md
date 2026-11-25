---
name: agent-plugin-publishing
description: Package and publish VS Code agent plugins to Marketplace, GitHub Releases, or private registries with versioning, release notes, and update monitoring.
---

# Agent Plugin Publishing

## Specialization

Prepare agent plugins for distribution through VS Code Marketplace, GitHub Releases, or private registries. Manage versioning, VSIX packaging, release documentation, and post-release monitoring.

## Supporting Activities

- Validate plugin manifest (plugin.json schema compliance).
- Bump semantic version and update changelog.
- Generate VSIX package (single and multi-platform).
- Create release notes with scope, known issues, rollback reference, and approval evidence.
- Publish to chosen distribution channel.
- Configure marketplace metadata (tags, logo, repository link).
- Monitor telemetry and respond to issues.

## Workflow

1. **Pre-publish validation**:
   - Confirm `plugin.json` exists and is valid JSON.
   - Verify `name` field uses only lowercase, numbers, hyphens (no slashes or namespace prefixes).
   - Check `version` field follows semver (MAJOR.MINOR.PATCH; e.g., 1.2.3).
   - Confirm all referenced paths exist (`skills/`, `agents/`, `.mcp.json`, etc.).
   - Run security scan: `npm audit` (zero high/critical vulnerabilities).
   - Test plugin locally: `Chat: Install Plugin From Source` → verify all components load.
   - Confirm README.md is present and clear.

2. **Update version and changelog**:
   - Decide version bump: patch (bug fix), minor (new feature), major (breaking change).
   - Update `plugin.json`:
     ```json
     {
       "version": "1.2.0"
     }
     ```
   - Update `marketplace.json` (if publishing to marketplace):
     ```json
     {
       "plugins": [
         {
           "name": "my-plugin",
           "version": "1.2.0",
           ...
         }
       ]
     }
     ```
   - Create or update `CHANGELOG.md`:
     ```markdown
     ## [1.2.0] - 2026-05-18

     ### Added
     - New test-runner agent for batch testing

     ### Fixed
     - SSRF prevention for web tool
     - Secret handling in MCP config

     ### Security
     - Added sandbox constraints for MCP servers
     - Input validation for file paths

     ### Breaking Changes
     None

     ### Known Issues
     - MCP servers do not support Windows (Linux/macOS only)
     ```

3. **Create release notes** (governance requirement):
   - Release notes MUST include:
     - **Scope**: Features added, bugs fixed, security patches.
     - **Breaking Changes**: What existing integrations are affected?
     - **Known Issues**: Limitations or workarounds (none = "None").
     - **Rollback Reference**: How to downgrade if needed.
     - **Approval Evidence**: Link to PR review, security sign-off, smoke test results.
   - Example:
     ```markdown
     # Release: my-plugin 1.2.0

     ## Scope Delivered
     - Feature: Test runner agent with parallel test execution
     - Bug fix: SSRF prevention for web tool
     - Security: Sandbox constraints for MCP servers

     ## Scope Deferred
     - Feature: Windows support for MCP servers (defer to 1.3.0)

     ## Known Issues
     - MCP servers do not start on Windows (use Linux/macOS or wait for 1.3.0)

     ## Rollback Procedure
     1. Disable plugin in Extensions view or Agent Customizations editor
     2. Uninstall from Extensions view (right-click → Uninstall)
     3. Reinstall previous version: Chat: Install Plugin From Source → previous release tag
     4. Verify: Chat: List Plugins shows previous version

     ## Release Evidence
     - PR Review: https://github.com/my-org/my-plugin/pull/42 (approved by @reviewer)
     - Security Sign-off: security-team@example.com (no vulns)
     - Smoke Tests: All tests pass (pytest output in CI)
     - E2E Tests: Agent behaves as documented (manual verification)
     ```

4. **Package plugin**:
   - Install vsce (VS Code Extension CLI):
     ```bash
     npm install -g @vscode/vsce
     ```
   - Login to marketplace (if publishing to VS Code Marketplace):
     ```bash
     vsce login <publisher-id>
     ```
   - Generate VSIX package:
     ```bash
     vsce package  # Single-platform package
     vsce package --target win32-x64 linux-x64 darwin-arm64  # Multi-platform
     # Output: my-plugin-1.2.0.vsix (or my-plugin-win32-x64-1.2.0.vsix, etc.)
     ```
   - Verify package contents:
     ```bash
     unzip -l my-plugin-1.2.0.vsix | head -20
     # Should include: plugin.json, skills/, agents/, .mcp.json, README.md, etc.
     ```

5. **Publish to distribution channel**:

   **Option A: VS Code Marketplace (recommended for public plugins)**
   - Requires: Microsoft account, publisher ID, VSIX package.
   - Steps:
     ```bash
     vsce publish minor  # Auto-bump version, create VSIX, publish
     # OR
     vsce publish --packagePath ./my-plugin-1.2.0.vsix
     ```
   - Marketplace metadata:
     - Display name: "My Testing Plugin" (max 128 chars)
     - Description: "Batch test runner for JavaScript projects" (max 1024 chars)
     - Category: "Other" or "Agent Extensions"
     - Tags: testing, agent, automation
     - Repository: https://github.com/my-org/my-plugin
     - Icon: 128x128 PNG
     - README: Rendered on Marketplace
     - License: MIT, Apache-2.0, GPL-3.0, etc.

   **Option B: GitHub Releases (for open-source plugins)**
   - Steps:
     ```bash
     # Tag release
     git tag -a v1.2.0 -m "Release version 1.2.0"
     git push origin v1.2.0

     # Create GitHub Release
     # Upload VSIX as binary attachment
     # Include release notes (see step 3)
     ```
   - Users install via: `Chat: Install Plugin From Source` → paste repo URL.

   **Option C: Private Registry (enterprise plugins)**
   - Host VSIX on private server or artifact store.
   - Configure registry URL in team workspace settings:
     ```jsonc
     {
       "chat.plugins.marketplaces": [
         "https://internal-registry.example.com/plugins"
       ]
     }
     ```

6. **Post-publish verification**:
   - **Marketplace availability**: Search for plugin in VS Code Extensions (`@agentPlugins` filter).
   - **Version visibility**: Confirm correct version appears (may take 5-10 min for sync).
   - **Installation test**: Install the published plugin and verify components load.
   - **Telemetry**: Enable telemetry and monitor first week of usage.

7. **Monitor and respond**:
   - **Daily checks (first week)**:
     - Monitor GitHub issues for bug reports.
     - Check Marketplace rating and feedback.
     - Review telemetry: crash rates, tool latency, error frequency.
   - **Update frequency**:
     - Hotfix (critical bugs): publish within 24 hours.
     - Minor updates (new features): publish on regular cadence (weekly/biweekly).
     - Patch updates (non-critical bugs): batch into minor or hotfix releases.
   - **Communication**:
     - Document known issues in README or plugin marketplace page.
     - Link to GitHub Issues for user feedback.
     - Post release announcements in team channels or community forums.

8. **Handle updates and rollbacks**:
   - **User update flow**: VS Code checks for updates every 24 hours (if `extensions.autoUpdate` enabled).
   - **Rolling back a release**:
     - Immediately disable plugin on Marketplace (if critical issue found).
     - Publish hotfix (bump patch version, fix issue).
     - Announce rollback and hotfix timeline to users.
     - Document incident and resolution.

## Inputs

- Validated agent plugin (all components tested and security-hardened).
- Release checklist completed (security, functional, performance tests pass).
- Changelog with version bump decision (patch, minor, major).
- Release notes with scope, known issues, rollback procedure, approval evidence.
- Distribution channel choice (Marketplace, GitHub, private registry).
- Marketplace metadata (if publishing to Marketplace): description, tags, icon, category.

## Required Outputs

- Updated `plugin.json` with bumped version.
- Updated `marketplace.json` (if applicable) with new version.
- CHANGELOG.md with clear entry for this release.
- RELEASE_NOTES.md or GitHub Release with scope, known issues, rollback reference, approval evidence.
- VSIX package (single or multi-platform).
- Published plugin (available on chosen distribution channel).
- Post-publish validation: plugin is discoverable and installable.
- Telemetry baseline recorded for monitoring.

## Done Criteria

- `plugin.json` version matches CHANGELOG and release notes.
- VSIX package contains all expected components (plugin.json, skills/, agents/, .mcp.json, README.md).
- Release notes include scope, known issues, rollback procedure, and approval evidence.
- Plugin is published and discoverable on chosen distribution channel.
- Installation test succeeds: plugin installs, components load, agent is available in Chat.
- First-week telemetry collected: usage patterns and error rates monitored.
- Update monitoring process is in place (daily checks first week, then weekly).

## Validation Checklist

- [ ] `plugin.json` version field updated (semver, matches CHANGELOG).
- [ ] `marketplace.json` version field updated (if applicable).
- [ ] CHANGELOG.md entry exists for this version with features, fixes, breaking changes, known issues.
- [ ] RELEASE_NOTES.md includes scope, deferred items, known issues, rollback procedure, approval evidence.
- [ ] VSIX package generated successfully (`vsce package` output without errors).
- [ ] VSIX contains plugin.json, README.md, all referenced directories (skills/, agents/, etc.).
- [ ] Plugin published to distribution channel (Marketplace, GitHub Release, or private registry).
- [ ] Plugin is discoverable in VS Code Extensions (`@agentPlugins` filter) or distribution URL.
- [ ] Installation test passes: plugin installs, components load, agent appears in Chat.
- [ ] Telemetry monitoring is configured (crash rates, tool latency, error frequency tracked).

## References

- [VS Code Extension Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [vsce Command Reference](https://github.com/microsoft/vscode-vsce)
- [Semantic Versioning](https://semver.org/)
- [GitHub Release Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Marketplace Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

## Trigger Conditions

Invoke this skill when any of the following is true:

- A plugin is ready for release (implementation, testing, security review complete).
- Versioning and changelog updates are needed.
- Release notes must be created with evidence and rollback procedures.
- A plugin needs to be published to Marketplace, GitHub, or private registry.
- Post-release monitoring and update management is required.
