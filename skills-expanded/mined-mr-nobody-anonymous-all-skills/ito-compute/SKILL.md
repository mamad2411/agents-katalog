---
name: ito-compute
description: Query live GPU inventory, submit an authenticated Itô fixed-rate RFQ, inspect RFQ or procurement status, revoke device credentials, and run explicitly gated node qualification through the separately installed canonical CLI. Use when a user asks to find H100/H200 capacity, request a fixed compute rate, check Itô compute status, validate GPU nodes, revoke Itô access, or rent or purchase GPU compute and needs the supported boundary explained.
type: procedural
category: ito
domain: ito
version: 1.0.0
author: "All-Skills Canonical Engineering Team"
license: "MIT"
risk: medium
level: intermediate
triggers:
  - "find H100 capacity"
  - "request a fixed compute rate"
  - "check ito compute status"
  - "revoke ito access"
  - "rent GPU compute"
keywords:
  - "ito"
  - "gpu"
  - "compute"
  - "h100"
  - "h200"
  - "rfq"
---

# Itô Compute

Use the canonical Itô compute CLI or MCP server. ECC does not implement a
parallel client, local simulation, reservation, workload runner, or inference
server. ECC itself does no browser automation.

## Install the canonical local package

`ito-compute-cli` is currently unpublished. Build it from its canonical
repository instead of using `npx`, `npm exec`, or an unverified package:

```sh
git clone https://github.com/Ito-Markets/ito-cloud-runtime.git
cd ito-cloud-runtime/cli/ito-compute-cli
npm ci
npm run check
```

Set `ECC_ITO_CLI_EXECUTABLE` to the explicit absolute built entry:

```text
/absolute/path/to/ito-cloud-runtime/cli/ito-compute-cli/dist/bin/ito.js
```

ECC never discovers this credential-bearing client through `PATH`.
`ecc ito login` performs device authorization and never inherits `ITO_API_KEY`.
The validation-only `auth`, plus `find` and `status`, forward `ITO_API_KEY`
directly when configured; `ITO_AUTH_MODE=legacy` is not required. Never put a
key or token in arguments, tracked files, MCP results, logs, or chat.

## CLI workflow

1. Run `ecc ito login` before the first operation. ECC delegates this to the
   canonical CLI's device authorization, which opens the Itô verification page
   by default and persists a device token in macOS Keychain. Use
   `ecc ito login --no-browser` to suppress the page handoff. ECC itself does no
   browser automation. If the originating agent cannot complete the signed-in
   browser step, hand the exact command to the user; after approval finishes,
   return to the originating task and continue with `ecc ito auth`.
   Device tokens use macOS Keychain by default. File-token fallback is explicit
   and its directory and token file must remain owner-only (0700 and 0600).
2. Run `ecc ito auth` to validate existing credentials; it never starts login
   and rejects `--no-browser`.
3. Before `ecc ito find`, obtain explicit buyer authority to submit an RFQ.
   - Require `gpu`, `count`, whole `days`, `max-rate`, `nodes`,
     `gpus-per-node`, `storage-tb`, `start-window`, `form-factor`,
     `contract-type`, `fabric`, `region`, and the split-fill decision.
   - Require `count == nodes * gpus-per-node`; never derive topology.
   - Use `any` only when the buyer explicitly accepts any fabric or region.
   - Omitted `--allow-split` means false.
4. Run the live RFQ command:

   ```sh
   ecc ito find \
     --gpu h200 \
     --count 8 \
     --nodes 1 \
     --gpus-per-node 8 \
     --days 30 \
     --storage-tb 1 \
     --start-window 2099-08-15 \
     --max-rate 3.00 \
     --form-factor bare_metal \
     --contract-type reservation \
     --fabric infiniband \
     --region us-east-1
   ```

5. Run `ecc ito status` to inspect RFQs and procurement orders.
   After an ambiguous transport failure, check status before repeating `find`.
6. When a quote is ready and the buyer explicitly approves, accept it:

   ```sh
   ecc ito accept rfq_<ticket-id>
   ```

   This routes the ticket to the desk for human review. It does not move funds
   or reserve capacity. Do not accept without explicit buyer authority.
7. Run `ecc ito logout` when the user explicitly asks to revoke this device.
   The canonical CLI keeps the local credential when remote revocation fails so
   the operator can retry; never delete the token manually as a substitute.

Inventory prices are indicative. An RFQ is not reserved capacity. Treat a rate
as fixed only when the canonical result contains a non-null firm quote.

## Live node qualification

`ecc ito evals` exposes the canonical CLI's narrow live adapter to a separately
installed `sixtytwo-cli==0.3.33`. It does not expose local fixture execution
through ECC.
Require all of the following before invoking it:

- operator authorization to contact the named nodes;
- `ITO_ENABLE_SIXTYTWO_LIVE=1`;
- `--live-sixtytwo`;
- an explicit node list; and
- an existing absolute config directory containing `sixtytwo.yaml`.

```sh
ecc ito evals \
  --cluster clu_prod_example \
  --live-sixtytwo \
  --nodes gpu-01,gpu-02 \
  --config-dir /absolute/path/to/qualification-config
```

The canonical adapter can run only the pinned version check and
`sixtytwo test --full` against the explicit nodes. It cannot rent, launch,
recover, repair, reset, purchase, or order resources. ECC does not forward
`ITO_API_KEY` or model/cloud credentials into node qualification.

## MCP workflow

Build the canonical package, then configure the stdio server with an absolute
path:

```json
{
  "mcpServers": {
    "ito-compute": {
      "command": "node",
      "args": [
        "/absolute/path/to/ito-cloud-runtime/cli/ito-compute-cli/dist/bin/ito-mcp.js"
      ]
    }
  }
}
```

The server exposes only:

- `ito_auth`
- `ito_find`
- `ito_status`
- `ito_accept`

`ito_auth` validates existing credentials; it does not start device login. Use
`ito_auth`, gather explicit buyer authority and every hard constraint, call
`ito_find`, then poll with `ito_status` when needed. When a quote is ready and
the buyer explicitly approves, call `ito_accept` with the ticket id. Desk
quotes are usually indicative and nonbinding until the desk confirms; the
result carries `quote_class`.

## Rent or purchase semantics

`find` submits an RFQ and may return a firm quote, but it does not rent,
purchase, reserve, provision, or move funds. `accept` routes a quote to the desk
for human review; it does not move funds or reserve capacity. `status` is
read-oriented, though the provider endpoint may reconcile an existing procurement
order. The passive dashboard link in ECC help is a separate user-operated web
route; do not open or operate it as a substitute for a missing CLI capability.

## Unsupported operations

The supported client surface cannot lock quotes, reserve capacity, execute
workloads, or serve inference. `accept` is a desk handoff, not a purchase. The
MCP server does not expose qualification; use the explicit CLI command above. Do
not invent additional tools or a purchase path. Do not substitute a browser or
fixture when the local CLI is missing or a live operation fails. Report the
missing capability and stop.

## Purpose

Query live Itô GPU inventory, submit an authenticated fixed-rate RFQ, inspect
RFQ or procurement status, revoke device credentials, and run explicitly gated
node qualification through the separately installed canonical Itô CLI.

## When to Use

- The user asks to find H100/H200 (or similar) GPU capacity or request a fixed
  compute rate.
- The user asks to check Itô compute status, validate GPU nodes, revoke Itô
  access, or rent or purchase GPU compute and needs the supported boundary
  explained.
- The user wants to log in, validate credentials, or sign out of Itô compute.

## When NOT to Use

- The user wants a parallel client, local simulation, reservation service,
  workload runner, or inference server implemented in this repository.
- The user wants a purchase, reservation, or capacity guarantee outside the
  canonical RFQ flow. RFQs are not reserved capacity.
- The user wants inference serving — use `ito-inference` after a booking.
- The user wants training — use `ito-training` after a booking.

## Capabilities

- Device authorization and credential validation (`ecc ito login`,
  `ecc ito auth`, `ecc ito logout`).
- Live GPU inventory lookup and authenticated RFQ submission (`ecc ito find`).
- RFQ and procurement status inspection (`ecc ito status`).
- Desk handoff for approved quotes (`ecc ito accept <rfq_id>`).
- Explicitly gated live node qualification (`ecc ito evals`).
- MCP bridge: `ito_auth`, `ito_find`, `ito_status`, `ito_accept`.

## Inputs

- GPU type, node count, per-node GPUs, and total count (must satisfy
  `count == nodes * gpus-per-node`).
- Whole days, max rate, storage in TB, start window, form factor, contract
  type, fabric and region constraints, and the split-fill decision.
- For qualification: operator authorization, `ITO_ENABLE_SIXTYTWO_LIVE=1`,
  `--live-sixtytwo`, an explicit node list, and an absolute config directory
  containing `sixtytwo.yaml`.

## Workflow

1. `ecc ito login` (once), then `ecc ito auth` to validate credentials.
2. Gather explicit buyer authority and every hard constraint.
3. `ecc ito find` with the full constraint set; never derive topology.
4. `ecc ito status` before repeating any ambiguous write.
5. `ecc ito accept rfq_<id>` only after explicit buyer approval.
6. `ecc ito logout` on explicit request.

## Tools

- Canonical CLI: `ecc ito {login,auth,logout,find,status,accept,evals}` via
  `ECC_ITO_CLI_EXECUTABLE` (never discovered through `PATH`).
- MCP server (stdio): tools `ito_auth`, `ito_find`, `ito_status`, `ito_accept`.
- No parallel client, simulator, or browser automation is provided or permitted.

## Examples

- "Find 8x H200 for 30 days under $3.00/hr": gather constraints, run
  `ecc ito find --gpu h200 --count 8 --nodes 1 --gpus-per-node 8 --days 30
  --max-rate 3.00 ...`, poll `ecc ito status`.
- "Revoke this device": `ecc ito logout`.

## Safety

- Never put a key or token in arguments, tracked files, MCP results, logs, or
  chat. Device tokens live in macOS Keychain by default; file-token fallback
  must stay owner-only (0700/0600).
- `ecc ito auth` never starts login and rejects `--no-browser`.
- `ITO_API_KEY` is forwarded only for `auth`, `find`, `status`; qualification
  never receives it and no model/cloud credential is forwarded either.
- Do not accept quotes without explicit buyer authority.

## Source

- Canonical upstream CLI: github.com/Ito-Markets/ito-cloud-runtime
  (`cli/ito-compute-cli`). ECC ships no `ito-compute-cli` dependency and
  discovers the executable only via `ECC_ITO_CLI_EXECUTABLE`.

## Notes

- Inventory prices are indicative. An RFQ is not reserved capacity. Treat a
  rate as fixed only for non-null firm quotes in the canonical result.
- The MCP server does not expose qualification; use the explicit CLI command.
