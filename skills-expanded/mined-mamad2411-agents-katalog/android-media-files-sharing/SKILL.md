---
name: "android-media-files-sharing"
description: "Use modern Android file, media, picker, FileProvider, and share-sheet APIs with minimal permissions."
metadata:
  version: "0.1.0"
  category: "data-platform"
  tags: ["android", "media", "files", "sharing"]
  triggers:
    include: ["android file sharing", "photo picker android app", "fileprovider setup android", "share pdf image android", "media attachment android flow", "android-media-files-sharing skill", "content uri sharing android", "share sheet android fileprovider", "share-sheet apis with minimal permissions"]
    exclude: ["room dao change", "compose performance", "gradle plugin error", "runtime permission request only", "request notification permission"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Media Files Sharing

## When To Use
- Use this skill when the request is about: android file sharing, photo picker android app, fileprovider setup android.
- Primary outcome: Use modern Android file, media, picker, FileProvider, and share-sheet APIs with minimal permissions.
- Reach for this skill when the core problem is content URIs, share-sheet flows, picker choice, or app-to-app file exchange. Use `android-permissions-activity-results` only when the hard part is the runtime permission flow itself.
- Handoff skills when the scope expands:
- `android-permissions-activity-results`
- `android-security-best-practices`

## Workflow
1. Start with the asset movement path: pick existing media, open a document, create/export a file, capture new content, or share app-owned content to another app.
2. Choose the narrowest platform surface first: Photo Picker, SAF contracts, `FileProvider`, or chooser-based sharing before considering broad storage permissions.
3. Keep file ownership and URI grants explicit with app-private storage, MIME types, temporary grants, and stable authorities.
4. Validate return flows, absent-capability fallbacks, and recipient-app interoperability instead of testing only the happy path.
5. Hand off runtime permission complexity or deeper hardening only after the URI and sharing contract is correct.

## Guardrails
- Prefer Photo Picker, SAF, and chooser APIs over broad media or storage permissions where possible.
- Share content with `content://` URIs and temporary grants, never raw file paths.
- Keep exported authorities, MIME types, and cache cleanup explicit.
- Treat recipients outside your app as untrusted; validate what leaves the app and what comes back.

## Anti-Patterns
- Requesting broad media or storage access when Photo Picker or SAF is enough.
- Sharing `file://` paths or world-readable files instead of `FileProvider` URIs.
- Assuming every recipient app handles every MIME type or URI permission correctly.
- Mixing permission-flow design with file-sharing contract design until both become unclear.

## Review Focus
- Picker/SAF/FileProvider/chooser selection.
- MIME type, URI authority, and grant lifecycle correctness.
- Minimal-permission media access.
- Recipient-app interoperability and cleanup of temporary files.

## Examples
### Happy path
- Scenario: Attach and share a task snapshot using the least-privilege API.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:testDebugUnitTest`

### Edge case
- Scenario: Handle absent picker support or denied media capabilities in the XML fixture.
- Command: `cd examples/orbittasks-xml && ./gradlew :app:testDebugUnitTest`

### Failure recovery
- Scenario: Separate media/file flows from permission-only or networking-only requests.
- Command: `python3 scripts/eval_triggers.py --skill android-media-files-sharing`

## Done Checklist
- The platform surface is narrower than a broad storage permission where possible.
- URI authorities, MIME types, and temporary grants are explicit.
- Picker and share-sheet fallbacks are covered.
- Permission-only work is handed off instead of conflated with the sharing contract.

## Official References
- [https://developer.android.com/training/data-storage/shared/photopicker](https://developer.android.com/training/data-storage/shared/photopicker)
- [https://developer.android.com/training/data-storage/shared/documents-files](https://developer.android.com/training/data-storage/shared/documents-files)
- [https://developer.android.com/training/secure-file-sharing/setup-sharing](https://developer.android.com/training/secure-file-sharing/setup-sharing)
- [https://developer.android.com/training/sharing/send](https://developer.android.com/training/sharing/send)
- [https://developer.android.com/topic/performance/graphics/picker](https://developer.android.com/topic/performance/graphics/picker)
