# VistA RPC Reference — Mandatory Lookup Before Coding

## Rule

Before writing ANY VistA RPC call, DDR query, or broker interaction:

1. **Check the frozen repo first.** The `VistA-Evolved` repo (sibling in workspace) has
   the richest RPC reference data. Do NOT guess at parameter formats.
2. **Read the reference doc:** `docs/reference/vista-rpc-reference-data.md` in this repo.

## Quick Reference Paths (in frozen VistA-Evolved repo)

| Need | File |
|------|------|
| RPC exists? | `data/vista/vivian/rpc_index.json` (3,747 RPCs) |
| RPC params? | `data/vista/rpcs/rpc-catalog.json` (full File 8994 with params) |
| Domain RPCs? | `data/vista/admin-specs/<domain>.json` (15 domain files) |
| RPC in VEHU? | `data/vista/vista_instance/rpc_present.json` (2,508 RPCs) |
| CPRS RPCs? | `design/contracts/cprs/v1/rpc_catalog.json` (975 RPCs) |
| RPC contexts? | `data/vista/rpcs/rpc-contexts.json` |

## DDR LISTER — Authoritative Spec

Source: `LISTC^DDR` in `WorldVistA/VistA-M` on GitHub.

- **1 parameter**, type REFERENCE (LIST in XWB)
- **Keys:** FILE (required), FIELDS (required), FLAGS, IENS, MAX (default "*"), FROM, PART, XREF, SCREEN, ID, OPTIONS
- **Response:** GLOBAL ARRAY with `[BEGIN_diDATA]`/`[END_diDATA]` markers. Parse only lines between these markers that have `^` delimiters and numeric IEN in first position.

## Never Allowed

- Guessing at RPC parameter formats without checking reference data
- Assuming an RPC exists without checking `rpc_present.json` or `rpc_index.json`
- Using LITERAL params for DDR family RPCs (they use LIST/REFERENCE params)
- Ignoring `[BEGIN_diDATA]`/`[END_diDATA]` markers in DDR LISTER responses
