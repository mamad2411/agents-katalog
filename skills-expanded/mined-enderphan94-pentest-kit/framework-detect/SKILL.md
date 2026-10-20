---
name: framework-detect
description: >
  Inspects stress-recon outputs (tech_stack.txt, response headers, URL pools) and
  identifies the web frameworks behind the target (FastAPI, Next.js, Express,
  Django, Spring Boot, Keycloak). Writes a structured frameworks.json plus a
  concatenated framework_playbooks.md bundle that stress-scan / front-end-scan /
  browser-scan can read as context, so each downstream skill applies
  framework-specific attack guidance instead of generic OWASP coverage.
  Use when the user invokes "framework-detect", "detect framework", "stack-aware
  scan", or asks to identify the framework / runtime / API stack of a target.
---

# Framework Detect — Stack-Aware Playbook Loader

## Purpose

Pentest-kit's scan skills are generic by default — XSS, SQLi, IDOR, etc. applied
uniformly. But the highest-leverage findings are framework-specific: FastAPI's
`/openapi.json` exposure, Next.js's `/_next/image?url=` SSRF, Spring Boot's
`/actuator/env`, Keycloak's `master` realm reachability. These bugs live in
defaults nobody disabled, not in custom code.

`framework-detect` closes that gap. It reads what stress-recon already
collected, identifies which frameworks are in play, and emits a single
markdown bundle (`framework_playbooks.md`) that the downstream scan skills
include as context. No new network requests; no new dependencies.

## Role

You are an authorized security assessment expert with experience identifying
framework "fingerprints" from minimal signals. You are evidence-driven: a single
weak signal yields a `low` confidence detection; corroborating signals across
tech_stack / headers / URLs upgrade to `high`. You don't pad the output with
false positives.

## Authorization

This skill performs **no live requests** against the target. It reads files
that stress-recon already produced. Authorization is inherited from the parent
scan.

## Scan Progress Checklist

```
Framework Detect Progress:
- [ ] Step 0: Locate stress-recon outputs (tech_stack.txt, headers, URLs)
- [ ] Step 1: Run detect_framework.py
- [ ] Step 2: Verify frameworks.json + framework_playbooks.md were written
- [ ] Step 3: Stash file paths so downstream skills can include them as context
```

## Step 0 — Locate Inputs

stress-recon writes its outputs under `$OUTDIR/recon/` (the current scan's
`$OUTDIR` directory). The relevant files:

| Required? | Path |
|---|---|
| Strongly preferred | `$OUTDIR/recon/tech_stack.txt` |
| If present | `$OUTDIR/cloud/all_headers.txt` |
| If present | `$OUTDIR/patterns/ranked_urls.txt` (or `$OUTDIR/all_urls_final.txt`) |

If none exist (e.g., the user is running framework-detect standalone before
stress-recon), continue — the detector returns an empty result, which is not
an error.

## Step 1 — Run the Detector

```bash
python3 skills/framework-detect/script/detect_framework.py \
  --tech-stack "$OUTDIR/recon/tech_stack.txt" \
  --headers    "$OUTDIR/cloud/all_headers.txt" \
  --urls       "$OUTDIR/patterns/ranked_urls.txt" \
  --out-json   "$OUTDIR/recon/frameworks.json" \
  --out-playbooks "$OUTDIR/recon/framework_playbooks.md"
```

The detector is pure-Python stdlib (no external deps). Missing input files are
silently skipped. The exit code is `0` even when nothing is detected — that's a
valid result.

## Step 2 — Verify Outputs

After the run, both files should exist:

- `$OUTDIR/recon/frameworks.json` — structured:
  ```json
  {
    "detected": [
      {"id": "fastapi", "name": "FastAPI", "confidence": "high",
       "score": 5, "evidence": ["Server: uvicorn header", "..."]}
    ],
    "scan_hints": ["fastapi"]
  }
  ```
- `$OUTDIR/recon/framework_playbooks.md` — concatenation of the matching
  per-framework markdown playbooks from `skills/framework-detect/playbooks/`,
  with each section preceded by the confidence + evidence summary.

If `detected` is empty, the bundle file just contains a "no frameworks
detected" note. That's fine; the downstream skills fall back to generic
coverage.

## Step 3 — Notify Downstream Skills

Tell the orchestrator (the next scan step) the paths of the produced files:

```
Framework playbooks ready at $OUTDIR/recon/framework_playbooks.md
Detected: <list of names>
```

The orchestrator should include the playbook bundle as additional context for
stress-scan, front-end-scan, and browser-scan. The relevant agents within each
of those skills will then apply framework-specific test cases.

## Supported Frameworks (Current Coverage)

| ID | Name | Playbook |
|---|---|---|
| `fastapi`     | FastAPI         | Deep — `/openapi.json`, Pydantic, OAuth2PasswordBearer, BackgroundTasks |
| `nextjs`      | Next.js         | Deep — `/_next/image` SSRF, `__NEXT_DATA__` leak, server actions, middleware bypass |
| `express`     | Express         | Solid — NoSQL operator injection, prototype pollution, CORS, ReDoS |
| `django`      | Django          | Solid — DEBUG=True, mass assignment, `.extra()` SQLi, pickle sessions |
| `spring-boot` | Spring Boot     | Outline — Actuator endpoints, Spring4Shell, SpEL, heapdump |
| `keycloak`    | Keycloak        | Outline — realm enumeration, `redirect_uri` bypass, admin REST exposure |

Adding more is a one-file change: add an entry to `SIGNALS` in
`detect_framework.py` and drop a markdown playbook with the matching `id` into
`playbooks/`. The bundler picks it up automatically.

## Do Not

- Do **not** issue live HTTP requests from this skill. All evidence comes from
  files stress-recon already produced. Live probing is the next step's job.
- Do **not** flag detection as a "finding". framework-detect emits *meta*
  output that informs scanning; it does not by itself produce report findings.
- Do **not** invent frameworks not in the SIGNALS dict. If a target uses
  something exotic (Phoenix, Rocket, FastAPI variants), note it as a comment
  in the orchestrator log — but the bundle stays restricted to playbooks we
  actually ship.

## See Also

- `references/` directory under each individual skill (front-end-scan,
  browser-scan, stress-scan) — they have their own internal references that
  layer on top of framework-detect's output
- `tests/framework-detect/` — pure-Python unit tests covering 26 cases
