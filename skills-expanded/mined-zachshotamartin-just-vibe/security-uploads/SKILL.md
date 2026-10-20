---
name: security-uploads
description: "Review file validation, storage, processing, and download access. Use for file receipt, processing and download safety; backend-permissions handles general resource access, and security-fix repairs a confirmed upload flaw."
---

# security-uploads

Review file validation, storage, processing, and download access.

## Choose this workflow

Use for file receipt, processing and download safety; backend-permissions handles general resource access, and security-fix repairs a confirmed upload flaw.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Security methods](../../references/packs/security.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; upload/download/processing paths, storage policy, file types, and access rules.

**Pack prerequisites:** Defined application boundary, authorized code/environment, relevant trust/access rules, and evidence sources. Default to defensive inspection; active tests use owned or explicitly authorized isolated targets. Minimize sensitive evidence and never print usable credentials.

- **Infer from evidence:** Resolve the requested surface, source/runtime version, reachable callers and actual trust/access boundaries.
- **Reasonable default:** Start with source analysis and bounded owned fixtures; treat scanner output as leads and preserve legitimate controls.
- **Ask only when needed:** Ask when target authorization or necessary trust semantics are unresolved before active probing; source inspection need not wait for production access.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

File validation, size limits, names/paths, processing isolation, storage exposure, and download authorization.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Follow the complete file lifecycle: filename, content and type trust, storage ownership, parser invocation, resource limits and download authorization.
2. Define safe malicious and invalid-file fixtures covering path, size, type, processing and access.

## Technical method

- **Inspect:** Trace receipt, content validation, parser, quarantine, extraction, storage and download authorization.
- **Method:** Apply file and resource limits at each stage, use server-owned names and verify private storage/scan state before processing or serving.
- **Avoid misdiagnosis:** Filename extension and client MIME type do not establish content; archive members and symlinks can escape a checked top-level path.
- **Check the result:** Use small inert invalid files, bounded archive/path fixtures and a valid upload; verify no pre-scan download or cross-tenant access.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Security worked example](../../references/examples/security.md).
- Uploads, filesystem paths, extraction or artifact loading are in scope: [Files and resource limits](../../references/security/files.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves bug bounty, authorized pentest, security proof; load only the matching method: [Authorized vulnerability research](../../references/methods/authorized-security-research.md).

## Decision branches

- **When scanning occurs asynchronously after upload:** Define quarantine/access state so unverified files cannot be consumed through another route.

## Deliver and verify

- Upload lifecycle/trust map with threat findings, remediation priorities and isolated path, size, type, processing and access test scenarios.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- User-supplied filenames cannot escape storage boundaries; private files require authorization at download as well as upload.

## Stop and recover

- Do not execute hostile files or upload dangerous content to public services. Missing processor configuration limits assurance.

## Example requests

- **Normal (inspect):** Audit file validation, processing, private storage, and download access.
- **Edge (inspect):** Audit private uploads with user filenames and an asynchronous processor.
- **Blocked (inspect):** Review upload source without executing hostile files or publishing dangerous test content.
