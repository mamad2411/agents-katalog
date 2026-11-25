---
name: configure-agent-skills
description: Creates and manages the agentskills.io manifest index at `/.well-known/agent-skills/index.json`, exposing structured API capabilities for agent orchestrators and capability-routing infrastructure to auto-discover and invoke. Use when registering, updating, or validating the skill manifest after adding or deprecating API endpoints on a service.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Configure Agent Skills

Use this skill when exposing API capabilities or developer instructions through the Agent Skills manifest at `/.well-known/agent-skills/index.json`. This makes structured skill metadata discoverable by agent orchestrators, SDK clients, and capability-routing infrastructure that reads the agentskills.io schema.

## Core Rules

- The manifest MUST be placed at `/.well-known/agent-skills/index.json` at the domain root (RFC 8615).
- The manifest envelope MUST conform to agentskills.io 0.2.0: declare `$schema: "https://schemas.agentskills.io/discovery/0.2.0/schema.json"` and a non-empty `skills` array.
- Each skill entry MUST declare:
  - `name`: stable kebab-case identifier (`^[a-z0-9]+(-[a-z0-9]+)*$`) matching directory and SKILL.md slug.
  - `type`: packaging type enum `["skill-md", "archive"]` (`skill-md` for standalone Markdown, `archive` for bundled tools).
  - `description`: 20 to 1024 characters with an explicit "Use when..." operational trigger clause.
  - `url`: relative or absolute URI reference to the full SKILL.md or archive package.
  - `digest`: lowercase hexadecimal SHA-256 digest prefixed with `sha256:` (`^sha256:[a-f0-9]{64}$`).
- **Progressive Disclosure**: Expose capabilities in two tiers:
  - *Tier 1 (Passive Discovery Index & Startup Slice)*: Keep active startup prompt skill metadata strictly $\le 5\text{ KB}$ (role-scoped slice, ~40–100 tokens/skill) without instruction bodies; keep full catalog discovery (`/.well-known/agent-skills/index.json` or `INDEX_TIER1.json`) stripped of markdown bodies with `sha256:` digests.
  - *Tier 2 (JIT Asset Retrieval)*: Full `SKILL.md` instructions or unpacked tool archives fetched Just-In-Time (JIT) into the execution sandbox only when an active intent matches the skill trigger.
- **Canonical Cryptographic Verification**: Compute SHA-256 digests using RFC 8785 JSON Canonicalization Scheme (JCS) or raw asset bytes; verify fetched asset digest before loading to prevent supply-chain tampering (OWASP AST02).
- **Discovery Headers & CORS**: Manifest HTTP response MUST set `Content-Type: application/json` and `Access-Control-Allow-Origin: *` (with 204 response on CORS `OPTIONS` preflight).
- **Passive Link Discovery**: The server MUST advertise the manifest via RFC 8288 Link header on the domain root: `Link: </.well-known/agent-skills/index.json>; rel="agent-skills"`.
- **Cache Freshness**: Serve `ETag` and `Last-Modified` headers to enable conditional HTTP requests (`If-None-Match`), preventing stale contract execution (OWASP ASI01).
- **Identity Triad Parity**: Enforce strict parity: $\text{Directory Slug} \equiv \text{Frontmatter Name} \equiv \text{Manifest Name}$.

## When to Use

- Exposing agent skills and tool capabilities via the agentskills.io 0.2.0 discovery standard
- Updating the capability manifest after adding, modifying, or deprecating skill endpoints
- Implementing two-tier progressive disclosure (Tier 1 passive index vs Tier 2 JIT asset loading)
- Verifying SHA-256 asset digests and cross-origin CORS/Link headers for orchestrator discovery

## Suggested Process

1. **Inventory Capabilities & Calibrate Triggers**: Define skill `name` (kebab-case), select packaging `type` (`skill-md` for standalone markdown, `archive` for bundled assets), author an operational `description` with an explicit `Use when...` trigger clause, and assign stable `url`.
2. **Compute Canonical SHA-256 Digest**: Calculate the SHA-256 hash across canonical asset bytes (RFC 8785 JCS canonicalization for JSON or raw byte stream for Markdown/tar archives) and format as `sha256:<64-hex-chars>`.
3. **Build agentskills.io 0.2.0 Manifest**: Wrap capability descriptors in the normative 0.2.0 envelope:
   ```json
   {
     "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
     "skills": [
       {
         "name": "pdf-processing",
         "type": "skill-md",
         "description": "Extract text, tables, and form fields from PDF files. Use when extracting data from invoices, forms, or documents.",
         "url": "/.well-known/agent-skills/pdf-processing/SKILL.md",
         "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
       }
     ]
   }
   ```
4. **Deploy at Well-Known Path**: Place the manifest at `/.well-known/agent-skills/index.json`. For Cloudflare Pages, publish under `public/.well-known/agent-skills/index.json`; for Workers, handle on router.
5. **Configure Response & Discovery Headers**: Set `Content-Type: application/json`, `Access-Control-Allow-Origin: *`, `ETag`, `Last-Modified`, and add `Link: </.well-known/agent-skills/index.json>; rel="agent-skills"` on the domain root.
6. **Validate Progressive Disclosure**: Verify active startup prompt slices stay $\le 5\text{ KB}$ without instruction bodies; verify full manifest (`index.json` / `INDEX_TIER1.json`) strips bodies, computes valid digests, and passes `contracts/schemas/agent-skills-discovery.json`.

## Checklist

- [ ] Manifest envelope specifies `$schema: "https://schemas.agentskills.io/discovery/0.2.0/schema.json"`.
- [ ] Every skill declares `name`, `type` (`skill-md` or `archive`), `description`, `url`, and `digest`.
- [ ] Skill descriptions include explicit "Use when..." or "Use for..." trigger clauses.
- [ ] Canonical SHA-256 digests computed and formatted with `sha256:` prefix.
- [ ] Startup active prompt slice stays $\le 5\text{ KB}$ and full discovery index omits embedded instruction bodies.
- [ ] Manifest endpoint served with `Content-Type: application/json` and `Access-Control-Allow-Origin: *`.
- [ ] RFC 8288 Link header pointing to discovery manifest configured on domain root.
- [ ] Manifest validated against `contracts/schemas/agent-skills-discovery.json`.

## Related Skills

- **configure-mcp**: Expose model context server capability endpoint — co-deployed with agent skills manifest.
- **manage-api-catalog**: Wire up RFC 9727 API catalog linkset — complementary discovery mechanism.
- **agent-a2a-protocol**: Implement full A2A 1.0 task lifecycle across discovered agent endpoints.
- **configure-agent-headers**: Expose well-known discovery paths via HTTP Link headers for passive discovery.

## Output Contracts

The manifest itself is the primary discovery contract. When communicating manifest changes:

- **`contracts/schemas/agent-skills-discovery.json`**: Primary schema contract for `/.well-known/agent-skills/index.json`, enforcing agentskills.io 0.2.0 structure, packaging types, and SHA-256 digests.
- **`contracts/schemas/api-contract-spec.json`**: Emitted when communicating service endpoint shape changes across agent boundaries.

## Failure Modes

- **Schema Drift**: Manifest deployed without valid 0.2.0 `$schema` or missing mandatory fields. Mitigation: CI gate validates against `agent-skills-discovery.json`.
- **Digest Mismatch**: Skill asset modified without updating `digest`. Mitigation: Runtime aborts with `E_DIGEST_MISMATCH` to prevent supply chain poisoning (AST02).
- **Context Bloat**: Ingesting full markdown instruction bodies into `index.json`. Mitigation: Enforce role-scoped startup slices $\le 5\text{ KB}$ and strip markdown bodies from discovery manifests; fetch full `SKILL.md` assets JIT.
- **CORS Blockade**: Browser orchestrator blocked from reading manifest. Mitigation: Return `Access-Control-Allow-Origin: *` and 204 on preflight `OPTIONS`.
- **Stale Cache Execution**: Agent client executing cached manifest after capability changes. Mitigation: Set `ETag` and `Last-Modified` for conditional HTTP revalidation.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: Malicious manifest redirecting agents to untrusted endpoints. Validate `url` against trusted domain allowlist.
- **ASI03 Identity & Privilege Abuse**: Declared skills must align with role policy profile and action boundaries; do not infer authority from URLs.
- **ASI04 Supply Chain**: Enforce SHA-256 cryptographic verification before loading any JIT skill asset into the execution sandbox.
- **ASI07 Inter-Agent Communication**: Treat manifest as a signed public contract; validate all changes in CI prior to deployment.
- **ASI09 Human-Agent Trust Exploitation**: Surface validator output in deploy records; never claim compliance without passing validation.
