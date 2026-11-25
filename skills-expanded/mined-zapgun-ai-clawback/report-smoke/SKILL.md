---
name: report_smoke
description: End-to-end smoke test for the /<admin-path>/report saved-run viewer. Boots the real clawback binary against the repo's runs/ dir and curls every report route, asserting status + content, prefix mutability, public-read exemption, and that sensitive run-dir siblings stay unreachable. Use after touching src/report.js, src/report_ui/*, or the admin/report wiring.
---

# clawback report viewer smoke test

Run `.skills/report_smoke/scripts/report_smoke.sh` from the project root:

```bash
.skills/report_smoke/scripts/report_smoke.sh
```

Environment variables (optional):

- `CLAWBACK_REPORT_DIR` — runs directory to serve (default `./runs`)

It needs at least one completed run on disk (a subdir with a parseable
`summary.json`). The repo ships `runs/smoke` and `runs/L0-tier1`; the L0-tier1
run also contains the sensitive `proxy.*.log` + `turns.*.ndjson` siblings, which
is exactly what the non-exposure assertions check against.

No upstream and no API key are required — report routes never proxy to
Anthropic. The proxy boots over plain HTTP on a free high port and is torn down
on exit. Exit code is the number of failed assertions (0 = all green).

What the script verifies:

1. **Static + base injection** — `/_proxy/report/` serves index.html with
   `__BASE__` replaced by the real `/_proxy/report/` base href (no literal
   `__BASE__` leaks); `report.js`/`report.css` serve with correct MIME types.
2. **Dynamic routes against real analyzer output** — `/runs` lists the on-disk
   runs newest-first; `/data?run=L0-tier1` returns summary (carrying the
   `tokens` reclaim block) + charts + csvBytes; `/chart/<id>/tokens_saved.svg`
   serves that SVG by name (the same route also serves the bare
   `tokens_saved.bg.svg` share-card background); `/csv/<id>` serves a CSV
   download.
3. **Security (allowlist is the control; traversal guards are depth)** — the
   `proxy.*.log` / `turns.*.ndjson` siblings are unreachable, the data payload
   does not leak their bytes, and `?run=..` / encoded traversal are rejected 400.
4. **Publicly readable** — a GET with a bogus `Host` 421s on a guarded endpoint
   (`/_proxy/metrics`) but the report viewer is exempt and still returns 200.
5. **Dashboard cross-link** — `/_proxy/ui/` exposes the `reportLink`.
6. **Prefix mutability** — a re-boot with `--admin-path ctrl` serves
   `/ctrl/report/...` (base href injected as `/ctrl/report/`) while the old
   `/_proxy/report/` path 404s, proving the admin prefix is not hardcoded.

Complements `test/report.test.js` (unit-level, synthetic run dirs): this
exercises the shipped `bin/clawback.js` boot path against real runs.
