---
name: android-photo-picker
description: >
  Android Photo Picker for owned apps: least-privilege media access without broad
  storage permissions, single/multiple select, and migration off READ_EXTERNAL_STORAGE
  where possible. Use when implementing image/video selection with modern privacy —
  not for bypassing user consent to read the entire gallery.
---

# Android Photo Picker

## Scope And Authorization

- **In scope:** Apps you own that need user-selected photos/videos.
- **Out of scope:** Covert gallery exfiltration; exploiting picker bugs on third-party apps without authorization.
- Treat selected media as user-sensitive; upload over TLS with authz.
- Pair with `code-quality-standards`.

## When To Use

- Letting users choose images/videos for avatar, attachments, posts.
- Removing broad storage permissions on modern Android.
- Replacing `ACTION_GET_CONTENT` / Storage Access Framework patterns with Photo Picker UX when appropriate.
- Privacy review of media access.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Health data permissions | `android-health-connect` |
| General intent security | `android-intent-security` |
| WebView file upload hardening | `android-webview-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Approach | Permission posture |
| --- | --- |
| Android Photo Picker | No broad storage read for simple picks |
| SAF `OpenDocument` | User-granted URI per file |
| `READ_MEDIA_IMAGES` etc. | Broader access — justify strongly |
| Legacy `READ_EXTERNAL_STORAGE` | Avoid on new targets |

## Workflow

### 1. Confirm scope and success criteria

1. Record media types (image/video), multi-select needs, max count, upload destinations.
2. Success: picker works without broad storage permission; app only accesses returned URIs; revoke/unload handled.
3. Privacy policy mentions media uploads.

### 2. Prefer Photo Picker APIs

```kotlin
// Activity Result API — PickVisualMedia
val pickMedia = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
    if (uri != null) handleUri(uri) else /* canceled */
}
pickMedia.launch(
    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
)

// Multi-select
val pickMultiple = registerForActivityResult(
    ActivityResultContracts.PickMultipleVisualMedia(maxItems = 5)
) { uris -> handleUris(uris) }
```

1. Use `ImageOnly` / `VideoOnly` / `ImageAndVideo` intentionally.
2. Cap `maxItems` for multi-select.

### 3. Handle URIs safely

```kotlin
// Persist permission only if you must re-read later and API grants it
contentResolver.takePersistableUriPermission(
    uri, Intent.FLAG_GRANT_READ_URI_PERMISSION
)
// Read via ContentResolver.openInputStream(uri) — not raw paths
// Never log full content; scrub EXIF if product requires (location)
```

| Risk | Mitigation |
| --- | --- |
| Path traversal assumptions | Use ContentResolver only |
| EXIF GPS | Strip before upload if policy requires |
| Huge files | Size limits + streaming upload |
| Malicious image codecs | Server-side re-encode; updated image libs |

### 4. Permissions cleanup

```xml
<!-- Remove unnecessary -->
<!-- <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" /> -->
<!-- Add only if true need for broad library access beyond picker -->
```

1. Audit merged manifest for SDK-added permissions.
2. Document any remaining `READ_MEDIA_*` with product justification.

### 5. WebView / hybrid note

1. File chooser callbacks should also launch Photo Picker / SAF — not grant full storage.
2. See `android-webview-security` for JS bridges.

### 6. Verify

```bash
adb shell dumpsys package com.example.app | rg -i 'READ_MEDIA|READ_EXTERNAL|WRITE_EXTERNAL'
# Manual: deny storage; picker still works
# Manual: select image; upload succeeds; app cannot list other photos
```

### 7. Hand off

1. UX copy for permission-less picker.
2. Server virus/malware scanning for uploads if threat model requires.
3. Retention/deletion for uploaded media.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Access | User-selected URIs only | Request all photos for one avatar |
| EXIF | Strip location when needed | Upload raw GPS to public CDN |
| Size | Client + server limits | Decode unbounded bitmaps on main thread |
| Permissions | Minimal | Legacy storage “for convenience” |

## Output Checklist

- [ ] Media types and limits defined
- [ ] Photo Picker / SAF implemented
- [ ] Broad storage permissions removed or justified
- [ ] URI handling + EXIF policy done
- [ ] Upload security (TLS, authz, size) reviewed
- [ ] Manual tests without storage permission
- [ ] Privacy policy updated
- [ ] `code-quality-standards` applied

## Rules

- User selection is the privacy boundary — honor it.
- Prefer Photo Picker over broad media permissions.
- Do not attempt to read gallery without consent.
- Treat uploaded media as sensitive user content.
- Owned apps only.
