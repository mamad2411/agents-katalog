# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| intellij-dependency-analytics | Kotlin/Java IntelliJ plugin | serena-intellij-dependency-analytics | ${TRUSTIFY_WS_DIR}/redhat-developer/intellij-dependency-analytics |
| trustify-da-java-client | Java client library | serena-trustify-da-java-client | ${TRUSTIFY_WS_DIR}/guacsec/trustify-da-java-client |
| trustify-da-api-spec | OpenAPI specification | serena-trustify-da-api-spec | ${TRUSTIFY_WS_DIR}/guacsec/trustify-da-api-spec |
| fabric8-analytics-vscode-extension | TypeScript VS Code extension | serena-fabric8-analytics-vscode-extension | ${TRUSTIFY_WS_DIR}/fabric8-analytics/fabric8-analytics-vscode-extension |
| trustify-da-javascript-client | JavaScript/TypeScript client library | serena-trustify-da-javascript-client | ${TRUSTIFY_WS_DIR}/guacsec/trustify-da-javascript-client |
| trustify-dependency-analytics | Java/Quarkus backend service | serena-trustify-dependency-analytics | ${TRUSTIFY_WS_DIR}/guacsec/trustify-dependency-analytics |
| trustify | Rust backend | serena-trustify | ${TRUSTIFY_WS_DIR}/guacsec/trustify |
| trustify-scale-testing | Goose load/performance tests | serena-trustify-scale-testing | ${TRUSTIFY_WS_DIR}/guacsec/trustify-scale-testing |
| trustify-ui | React/TypeScript frontend | serena-trustify-ui | ${TRUSTIFY_WS_DIR}/guacsec/trustify-ui |
| rhtpa-konflux-release.0.3.z | Konflux release repo (0.3.z stream) | — | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.3.z |
| rhtpa-konflux-release.0.4.z | Konflux release repo (0.4.z stream) | — | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.4.z |
| rhtpa-konflux-release.0.5.z | Konflux release repo (0.5.z stream) | — | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.5.z |
| rhtpa-konflux-release.0.6.z | Konflux release repo (0.6.z stream) | — | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.6.z |
| trusted-profile-analyzer-operator | Go/Helm operator | — | ${TRUSTIFY_WS_DIR}/trustification/trusted-profile-analyzer-operator |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747
- Default component: DA

### Jira Field Defaults

- Default priority: Normal
- fixVersion scope: both
- Prompt for priority: true
- Prompt for fixVersion: true

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in the trustify-dependency-analytics repository:

    mcp__serena-trustify-dependency-analytics__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

No known limitations.

## Hierarchy Configuration

- Default epic grouping strategy: by-repository

## Bug Configuration

- Bug issue type ID: 10016
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Security Configuration

### Product Lifecycle

- Product pages URL: https://access.redhat.com/support/policy/updates/rhta
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10172
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_10483
- Upstream Affected Component custom field: customfield_10632
- PS Component custom field: customfield_10669
- Stream custom field: customfield_10832
- ProdSec contact email:
- ProdSec Jira account ID:
- Embargo policy URL: https://prodsec.pages.redhat.com/prodsec-docs/incident-response/Embargo_Process/

### Version Streams

| Stream | Lifecycle | Konflux Release Repo | Local Path | Security Matrix Path | Operator Version |
|---|---|---|---|---|---|
| 2.1.x | EOL | gitlab.cee.redhat.com/trustification/rhtpa-konflux-release.0.3.z | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.3.z | docs/security-matrix-2.1.x.md | — |
| 2.2.x | Full Support | gitlab.cee.redhat.com/trustification/rhtpa-konflux-release.0.4.z | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.4.z | docs/security-matrix-2.2.x.md | 1.1.z |
| 3.0.x | Full Support | gitlab.cee.redhat.com/trustification/rhtpa-konflux-release.0.5.z | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.5.z | docs/security-matrix-3.0.x.md | 3.y.z |
| 3.1.x | Full Support | gitlab.cee.redhat.com/trustification/rhtpa-konflux-release.0.6.z | ${TRUSTIFY_GL_DIR}/trustification/rhtpa-konflux-release.0.6.z | docs/security-matrix-3.1.x.md | 3.y.z |

### Source Repositories

| Repository | URL | Deployment Context |
|---|---|---|
| trustify | https://github.com/guacsec/trustify | customer-shipped |
| trustify-ui | https://github.com/guacsec/trustify-ui | customer-shipped |
| trusted-profile-analyzer-operator | https://github.com/trustification/trusted-profile-analyzer-operator | customer-shipped |

## Cross-Project Conventions

### Feature Parity Protocol (Dependency Analytics)

The DA ecosystem has paired repositories that must maintain functional parity:
- **Client libraries:** trustify-da-java-client ↔ trustify-da-javascript-client
- **IDE extensions:** intellij-dependency-analytics ↔ fabric8-analytics-vscode-extension

When implementing a feature in any of these repositories, follow this workflow:

1. **Before implementation:** Use the `da-parity` agent to analyze how similar features are implemented in the counterpart repository. If an implementation spec doesn't already exist in `.claude/agent-memory/_shared/`, generate one.

2. **During implementation:** The implementing agent must reference the counterpart's code via its Serena instance and follow any existing spec in `.claude/agent-memory/_shared/`.

3. **After implementation:** 
   - Use the `da-parity` agent to update the parity matrix at `.claude/agent-memory/_shared/parity-matrix.md`
   - Write implementation notes to `.claude/agent-memory/_shared/impl-<project>-<feature>.md`
   - If the counterpart does not yet have the feature, create an implementation spec at `.claude/agent-memory/_shared/spec-<feature>.md` for the other side

4. **API spec changes:** If the feature requires API contract changes, use the `da-api-spec` agent first, then propagate to backend and clients. Use `api-contract-review` to verify compliance after implementation.

### Shared Knowledge

Agents share cross-cutting knowledge through `.claude/agent-memory/_shared/`. This directory holds **living knowledge** that agents actively reference.

**Persistent files** (stay until superseded):
- `spec-<feature>.md` — Language-neutral implementation specs (written by da-parity)
- `impl-<project>-<feature>.md` — Implementation notes (written by client/IDE agents)
- `parity-matrix.md` — Running feature parity status (maintained by da-parity)
- `parity-report-*.md` — Detailed parity analysis reports
- `contract-<topic>.md` — API contract notes (written by api-contract-review)

**Issue investigations** go on the issue itself (Jira/GitHub comment), not as files in this directory. This keeps the repo clean and makes findings visible to the whole team.

**Guardrail:** Agents must NEVER post comments to Jira or GitHub without explicit user consent. The workflow is: investigate → present findings to the user → ask permission before posting.

### Keeping Shared Knowledge Current

Any agent that investigates or modifies code in the DA ecosystem must update shared docs when it discovers cross-cutting information. This applies during investigations, code reviews, bug fixes, and feature implementations — not just planned parity work.

**What to update:**
- **Parity-relevant findings** — New gaps, resolved gaps, or behavioral differences between paired repositories. Update the relevant `parity-report-*.md` or flag for `da-parity` follow-up.
- **Architecture patterns** — Patterns discovered in one repository that the counterpart should follow (e.g., "Java uses centralized `IgnorePatternDetector`, JS should adopt a similar pattern").
- **Feature status changes** — If a feature was added, removed, or broken, note it so counterpart agents are aware.
- **API contract observations** — Mismatches between spec and implementation, undocumented behavior, or deprecations.

**What NOT to update:**
- Routine debugging traces or dead-end investigations
- Information that's already in the code or git history
- Ephemeral state (build failures, test flakiness) unless it reveals a systemic issue

**How to update:**
- Append to existing reports rather than creating new files when the topic is already covered
- If a finding doesn't fit an existing file, create one following the naming conventions above
- Keep entries concise: what was found, where (file:line), and what it means for the counterpart

### Quality Checks

Build, format, and test requirements live in each repository's `CONVENTIONS.md` file.
Agents have PostToolUse hooks that auto-format on every edit. The sdlc-workflow skills
handle CONVENTIONS.md discovery and CI verification automatically during implementation.
