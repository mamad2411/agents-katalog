---
name: recording-studio-saving
description: Create, revise, or log Recording Studio content through public helpers. Use when writing tree content, appending history, or when tempted to insert Recording or Event rows directly. For webhook deliveries and similar exhaust, use recording-studio-data-shape instead.
---

# Saving

Owned content goes through the public write path. Do not insert `Recording` or `Event` rows by hand, and do not `save!` a recordable to “update” it in place.

If the data is caused activity that does not belong in the tree (deliveries, request traces), it is a **log** or a plain table — not `record` / `revise`. Layers: `recording-studio-data-shape`.

## Checklist

1. Normalize the type with `RecordingStudio.recordable_type_name(...)` and `RecordingStudio.recordable_declaration_for(...)`.
2. If the write is for a top-level object, confirm `RecordingStudio.root_allowed?(type)` and call `RecordingStudio.root_recording_for(persisted_recordable)`.
3. If the write is for a child, resolve `parent_recording` first and verify `RecordingStudio.parent_allowed?(child_type:, parent_recording:)`.
4. If the child is capability-owned, inspect `RecordingStudio.recordable_parent_allowances_for(...)` and `RecordingStudio.parent_capabilities_for(child_type:, parent_recording:)` to explain why the parent is valid.
5. Write with the `Recording` helpers `recording.record` / `#revise` / `#log_event!`; they wrap the low-level `RecordingStudio.record!`, which you use directly only when you need the returned event or lower-level control.
6. For retriable jobs (webhooks, imports), pass an `idempotency_key` so a retry does not create a second recording or event.

## Tests

- Assert a new recordable row on `revise`, not in-place mutation.
- Assert event action and count.
- Cover the idempotent retry when you use `idempotency_key`.

For the full method surface, read `docs/API_REFERENCE.md` in the Recording Studio gem.
