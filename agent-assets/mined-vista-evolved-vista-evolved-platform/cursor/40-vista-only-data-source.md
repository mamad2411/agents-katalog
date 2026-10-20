# VistA-Only Data Source and Runtime Truth Policy (NON-NEGOTIABLE)

## Core Rule

Every tenant-admin route MUST read from and write to the live VistA system.
There are NO fixture files, NO JSON fallbacks, NO alternate data sources.
Every route MUST be verified against the running VistA Docker container.
Code that was never tested against the live system is NOT done.

If VistA is unreachable, routes MUST return:
```json
{ "ok": false, "source": "error", "error": "VistA unreachable" }
```

## Prohibited patterns

These patterns are FORBIDDEN in any tenant-admin code:

1. **No `readFile` for JSON data.** Never load JSON files as data sources.
2. **No `source: 'fixture'`.** This label must never appear in any API response.
3. **No fixture fallback logic.** Never write `if (!vistaResult.ok) { return fixtureData }`.
4. **No `fixtures/` directory.** This directory was deleted and must never be recreated.
5. **No hardcoded data arrays.** Never embed user/facility/role data directly in code.
6. **No degraded-mode data.** If VistA is down, show an error, not stale data.
7. **No claiming a route works without live proof.** "Should work" or "looks correct" is never acceptable.
8. **No skipping runtime verification.** Every new or changed route must be tested against the running Docker.

## Required patterns

1. Every route starts with VistA connectivity check or RPC call.
2. If VistA returns data, return it with `source: 'vista'`.
3. If VistA fails, return `{ ok: false, source: 'error', error: '<specific message>' }`.
4. The UI shows a red ERROR badge when source is 'error'.
5. DDR family RPCs (DDR LISTER, DDR GETS, DDR FILER, DDR VALIDATOR) are the primary
   mechanism for reading/writing VistA FileMan data.
6. Custom ZVE* overlay RPCs handle operations DDR cannot (cross-file, business logic).

## Runtime truth verification (MANDATORY)

Before marking ANY route as done, the following MUST be proven against the live
VistA Docker container (`local-vista-utf8` on port 9434 or equivalent):

### For read routes:
- Call the route via curl/fetch
- Confirm the response has `ok: true, source: 'vista'`
- Confirm the data matches what exists in VistA (spot-check against direct MUMPS global inspection)
- Confirm the response does NOT contain "fixture", hardcoded data, or stale JSON

### For write routes (create/update/delete):
- Call the write route with valid data
- Confirm the route returns success with `ok: true`
- **READ BACK** the written data via a separate read route or DDR GETS
- Confirm the read-back matches what was written
- Confirm the data actually changed in VistA (inspect the global if needed)

### For edit/update routes:
- Read the current value
- Write a new value
- Read back the value and confirm it changed
- Restore the original value (if appropriate for test data)

### For delete routes:
- Confirm the record exists before delete
- Call the delete route
- Confirm the record no longer exists via read-back

### What "done" means for ANY route:
1. VistA Docker is running and reachable
2. Route returns `ok: true` with real VistA data (reads) or success confirmation (writes)
3. Response includes `source: 'vista'` — never 'fixture', 'catalog', or 'error'
4. Write operations are proven with read-back verification
5. No MUMPS errors (`%YDB-E-*`) in the response
6. The test was run against the LIVE Docker, not assumed or simulated
7. The UI correctly displays the VistA data and all actions (buttons, forms, links) work

### What is NEVER acceptable:
- "Should work" or "looks correct" without live test output
- Marking a route done without showing the actual HTTP response
- Saying "verification deferred" or "will test later"
- Testing with non-existent data (e.g. IEN=0 or IEN=999999)
- Writing code that compiles but was never executed against VistA
- Building UI that renders but does not actually communicate with VistA
- Any data display that does not come from a live VistA RPC call

## Why this exists

Fixtures and untested code created a false sense of functionality. Routes appeared
to "work" but returned stale JSON data or were never actually tested against VistA.
This masked integration gaps and prevented detection of broken communication paths.
Users could not tell if their changes were actually reaching VistA. AI coding agents
repeatedly wrote hundreds of routes that compiled but returned MUMPS errors when
actually called. This was a patient safety and data integrity risk.

All fixture files and fallback logic were permanently removed on 2026-03-21.
Runtime truth verification was made mandatory on the same date.
