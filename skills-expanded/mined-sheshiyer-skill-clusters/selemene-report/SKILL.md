---
name: selemene-report
description: "Generate Selemene Engine reports from a slash-command. Routes deterministic birth/compatibility/transit reports through the existing @selemene/bridge CLI and narrative witness readings through the packages/witness-pipeline. USE WHEN the user says /selemene-report, selemene report, generate selemene report, birth chart report, compatibility report, transit report, or witness reading. NOT for building new engines, not for replacing the bridge CLI, not for human web UI intake."
origin: project
cluster: selemene
version: 1.0.0
---

# Selemene Report — `/selemene-report`

Generate Selemene Engine reports from a coding-agent context.

This skill is a thin orchestrator over surfaces that already exist in the repo:

- **Deterministic reports** — birth chart, compatibility, transit — via the Rust `noesis-vedic-api` report generator, reached through the `@selemene/bridge` CLI.
- **Narrative witness readings** — solo or dyadic — via `packages/witness-pipeline/src/orchestrator/integrated.ts`.

The skill does not reimplement report logic. It asks for missing inputs, invokes the right existing path, writes a manifest + artifact, and returns the artifact path plus a non-prescriptive witness prompt.

---

## Triggers

Invoke this skill when the user says any of the following, or asks for a Selemene report without specifying a surface:

- `/selemene-report`
- `selemene report`
- `generate selemene report`
- `birth chart report`
- `compatibility report`
- `transit report`
- `witness reading`
- `selemene reading`

## Non-triggers (route elsewhere)

- Building or modifying a Selemene engine → `rust-orchestrator` or `backend-architecture-orchestrator`
- Changing the bridge CLI itself → `createcli` or work directly in `bridges/cli/src/`
- Human-facing web intake → the existing `apps/noesis-web` app; this skill is for agent/terminal use
- PDF/DOCX layout/rendering → `documents` cluster (`docx`, `pdf`, `notebooklm`)

---

## Inputs

The skill accepts a command string and resolves the report type from the first positional argument.

### Deterministic reports

```bash
/selemene-report birth "Name" "1990-01-15T10:30:00+05:30" "Bangalore" \
  [--output-dir ./selemene-reports] [--format text|html|json|pdf]

/selemene-report compatibility \
  --person1 "Name A" "1990-01-15T10:30:00+05:30" "Bangalore" \
  --person2 "Name B" "1992-03-20T14:00:00+05:30" "Mumbai" \
  [--output-dir ./selemene-reports]

/selemene-report transit "Name" "1990-01-15T10:30:00+05:30" "Bangalore" \
  --from 2026-01-01 --to 2026-12-31 \
  [--output-dir ./selemene-reports]
```

### Narrative witness reading

```bash
/selemene-report witness --mode solo --subjects subjects.json \
  [--level L1|L2|L3|L4|L5] [--output-dir ./selemene-reports]
```

`subjects.json` matches the rich `ReportSubjectInput` shape from `packages/witness-pipeline/src/intake/types.ts`. The live Rust endpoint requires every subject to carry a `normalized_location`:

```json
[
  {
    "role": "primary",
    "name": "Name",
    "birth_date": "1990-01-15",
    "birth_time": "10:30",
    "birth_time_confidence": "exact",
    "birth_location_query": "Bangalore",
    "normalized_location": {
      "display_name": "Bengaluru, Karnataka, India",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "timezone": "Asia/Kolkata",
      "provider": "manual",
      "confidence": "manual"
    }
  }
]
```

### Environment

The skill reads the same environment the bridge CLI uses:

- `SELEMENE_RUST_URL` (default: `http://localhost:8080`)
- `SELEMENE_TS_URL` (default: `http://localhost:3001`)
- `SELEMENE_API_KEY` (optional)
- `CF_DEV_BYPASS_TOKEN` (optional, sent as `x-noesis-dev-auth` for local development bypass)
- `SELEMENE_OUTPUT_DIR` (default: `./selemene-reports`)

It also respects a local `.selemenerc.json` if present, reusing the bridge config file format.

---

## Execution flow

1. **Parse intent** — first positional argument chooses one of `birth`, `compatibility`, `transit`, `witness`.
2. **Validate inputs** — require birth datetime + location for deterministic reports; require `--subjects` JSON for witness.
3. **Resolve backend**
   - Deterministic: `POST {rustUrl}/api/v1/workflows/{workflow_id}/execute` with an `EngineInput` body. There are no dedicated `/api/reports/*` routes. The skill maps the CLI report type to an existing workflow ID:
     - `birth` → `birth-blueprint`
     - `compatibility` → `full-spectrum` (carries a second subject in `options.partner_birth_data` + `relationship_context`)
     - `transit` → `daily-practice` (sets `current_time` to `--from` and `options.transit_window_end` to `--to`)
   - Witness: the `packages/witness-pipeline` package is a TypeScript library (not an HTTP server). The running `ts-engines` server exposes generic engine endpoints (`/engines/:id/calculate`), not a dedicated witness endpoint. The live equivalent for assembled witness readings is the Rust `POST /api/v1/assets/generate` endpoint. The CLI maps `--mode solo` to mode `"integrated-reading"` and `--mode dyadic` to mode `"composite-dyad"`.
4. **Write artifacts** — always emit:
   - `{output_dir}/manifest.json`
   - `{output_dir}/{report_type}-{slug}-{timestamp}.{ext}`
5. **Return result** — absolute artifact path + a one-line witness prompt.

---

## Output contract

Every run produces a manifest next to the artifact:

```json
{
  "report_type": "birth|compatibility|transit|witness",
  "created_at": "2026-07-06T13:45:00Z",
  "subject_count": 1,
  "engines_used": ["vedic"],
  "artifact_path": "/abs/path/to/selemene-reports/birth-name-20260706-134500.md",
  "witness_prompt": "What is the one thing from this report that feels most alive right now?"
}
```

For deterministic reports the artifact format is set by `--format`. For witness readings the artifact is markdown by default, matching the source-pack factory output in `packages/witness-pipeline/src/assets/factory.ts`.

---

## Tool reference

The skill ships a thin wrapper in `Tools/` that performs the parse → validate → invoke → write flow.

- `Tools/Report.ts` — main entry, called as `bun run Tools/Report.ts <subcommand> <args>`
- `Tools/lib/resolve-config.ts` — reads `.selemenerc.json` and env vars
- `Tools/lib/write-manifest.ts` — writes the manifest.json contract
- `Tools/lib/prompts.ts` — returns a witness prompt per report type

Do not edit `Tools/` to add new report math. If a report type is missing, extend the backend (Rust or witness-pipeline) first, then add a sub-command mapping here.

---

## Verification checklist

Before claiming a report was generated:

- [ ] The manifest file exists next to the artifact and is valid JSON.
- [ ] The artifact file exists and is non-empty.
- [ ] The backend endpoint or witness-pipeline script returned a success status.
- [ ] The returned path is absolute and readable.

---

### Running the backend

Start the Rust API server from the Selemene Engine repo:

```bash
cd /Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Selemene-engine
export RUST_ENV=development
export CF_DEV_BYPASS_TOKEN=selemene-local-test
export ENABLE_SWAGGER_UI=true
cargo run -p noesis-api --bin noesis-server
```

Notes:
- The crate is `noesis-api` and the binary name is `noesis-server` (`cargo run -p noesis-api` alone is ambiguous because the crate also ships helper binaries).
- Default bind address is `0.0.0.0:8080`.
- `CF_DEV_BYPASS_TOKEN` + `x-noesis-dev-auth` header bypasses auth in development only; production requires a valid JWT or `X-API-Key`.
- `ENABLE_SWAGGER_UI=true` exposes `/api/openapi.json` and `/api/docs`.
- Without `DATABASE_URL`, auth endpoints are unavailable but health checks and workflow execution via dev bypass still work.

Verify health:

```bash
curl -i http://localhost:8080/health/live
```

Expected: `HTTP/1.1 200 OK` with JSON body containing `status`, `version`, `uptime_seconds`, `engines_loaded`, and `workflows_loaded`.

### TypeScript engines server

Start the TypeScript engine server from the Selemene Engine repo:

```bash
cd /Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Selemene-engine/ts-engines
bun run dev
```

Notes:
- Default bind address is `0.0.0.0:3001`.
- This is a generic Elysia API for the TS consciousness engines (`tarot`, `i-ching`, `enneagram`, `sacred-geometry`, `sigil-forge`, `raaga`).
- It does **not** expose `/witness/generate`; witness-pipeline is a local library.

Verify health:

```bash
curl -i http://localhost:3001/health
```

Expected: `HTTP/1.1 200 OK` with JSON body containing `status`, `engines`, `uptime_ms`, and `version`.

## Endpoint assumptions

- Rust deterministic reports: `POST {rustUrl}/api/v1/workflows/{workflow_id}/execute` with an `EngineInput` body.
  - The actual running server exposes these workflow IDs: `birth-blueprint`, `daily-practice`, `decision-support`, `self-inquiry`, `creative-expression`, `full-spectrum`.
  - There is **no** `birth-report`, `compatibility-report`, or `transit-report` workflow; the repo also does not expose dedicated `/api/reports/*` routes.
  - The CLI maps report types to workflows:
    - `birth` → `birth-blueprint`
    - `compatibility` → `full-spectrum`
    - `transit` → `daily-practice`
  - Request body shape is `EngineInput`:
    ```json
    {
      "birth_data": {
        "name": "Ada",
        "date": "1815-12-10",
        "time": "15:00",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London"
      },
      "options": {}
    }
    ```
    - `current_time` and `precision` are optional (defaults apply).
    - `location` may be used for geo-only engines but chart workflows primarily read `birth_data`.
    - For `compatibility`, `options.partner_birth_data` carries the second person and `options.relationship_context.type` is `"compatibility"`.
    - For `transit`, `current_time` is set to `--from` and `options.transit_window_end` is set to `--to`.
- Generic workflow execution: `POST {rustUrl}/api/v1/workflows/{workflow_id}/execute` with the same `EngineInput` body.
- TS witness pipeline: there is no `POST {tsUrl}/witness/generate` on the running `ts-engines` server. The only TS HTTP surface is `ts-engines`, which exposes `GET /health`, `/engines`, `/engines/:id/info`, and `POST /engines/:id/calculate`. The witness-pipeline package is a library (`IntegratedReadingOrchestrator`).
- Live witness / premium-asset endpoint: `POST {rustUrl}/api/v1/assets/generate` returns an `AssetGenerateResponse` with `assembled` text. Request body:
  ```json
  {
    "mode": "integrated-reading",
    "report_level": "L3",
    "subjects": [
      {
        "role": "primary",
        "name": "Name",
        "birth_date": "1990-01-15",
        "birth_time": "10:30",
        "birth_time_confidence": "exact",
        "birth_location_query": "Bangalore",
        "normalized_location": {
          "display_name": "Bengaluru, Karnataka, India",
          "latitude": 12.9716,
          "longitude": 77.5946,
          "timezone": "Asia/Kolkata",
          "provider": "manual",
          "confidence": "manual"
        }
      }
    ]
  }
  ```
- Dev auth: when `CF_DEV_BYPASS_TOKEN` is set, the CLI sends it as the `x-noesis-dev-auth` header. In production, use `SELEMENE_API_KEY` (sent as `Authorization: Bearer ...`) or an `X-API-Key` header configured in your deployment.

If your Selemene deployment uses different routes, update `Tools/Report.ts` before using.

## Testing

Run the unit-test suite from the skill directory:

```bash
cd ~/.agents/skill-clusters/skills/selemene-report
bun test
```

Run a live smoke test against the Rust server after starting it:

```bash
SELEMENE_RUST_URL=http://localhost:8080 \
  CF_DEV_BYPASS_TOKEN=selemene-local-test \
  bun run report birth "Ada" "1815-12-10T15:00:00+00:00" "London" \
  --output-dir ./tmp-reports
```

Run a dry-run to validate CLI parsing without contacting any backend:

```bash
bun run report birth "Ada" "1990-01-15T10:30:00+05:30" "Bangalore" --dry-run
```

### Endpoint assumptions

Final wired paths after Tasks 8-13:

- Rust deterministic workflows: `POST {rustUrl}/api/v1/workflows/{workflow_id}/execute`
  - `birth` → `birth-blueprint`
  - `compatibility` → `full-spectrum`
  - `transit` → `daily-practice`
- Rust witness / premium-asset endpoint: `POST {rustUrl}/api/v1/assets/generate`

No dedicated `/api/reports/*` routes or `POST {tsUrl}/witness/generate` HTTP route exist in the running Selemene Engine; the witness-pipeline package is a local TypeScript library and the live assembled reading is produced by the Rust assets endpoint.

### Authentication

The CLI supports two authentication paths:

- `CF_DEV_BYPASS_TOKEN` environment variable → sent as `x-noesis-dev-auth` header. Use this for local development only; it is enabled by the Rust server in development mode when `CF_DEV_BYPASS_TOKEN` is set.
- `SELEMENE_API_KEY` environment variable → sent as `Authorization: Bearer {SELEMENE_API_KEY}`. Use this for production or any deployment that expects API-key auth.

`Tools/lib/resolve-config.ts` reads `SELEMENE_API_KEY` from env or `.selemenerc.json`. `Tools/Report.ts` reads `CF_DEV_BYPASS_TOKEN` directly from the environment because it is a dev-mode bypass, not a persistent config value.

## Design notes

- **Hub-and-spoke citizenship.** This skill is an `active-spoke` under the `selemene` cluster. It is enumerated only if the cluster is active; otherwise it resolves on demand via `~/.agents/skill-clusters/skills/selemene-report/SKILL.md`.
- **No duplicate logic.** The skill invokes `@selemene/bridge` and `packages/witness-pipeline`; it does not contain copies of `mergeSpecs`, `generateClaudeTools`, `IntegratedReadingOrchestrator`, or `ReportSection` logic.
- **Non-prescriptive framing.** All returned prompts are mirrors, not advice. This matches the existing witness-pipeline tone.
