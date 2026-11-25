---
name: leaddocket-lead-notes
description: >
  Add, update, and delete notes on Leads in LeadDocket. Use when logging
  call summaries, adding intake notes from external systems, updating existing
  notes, or cleaning up notes programmatically. Notes are visible in the lead
  activity feed. For AI-generated notes via chat see leaddocket-lois; for
  adding messages (email/SMS logs) see leaddocket-messages.
---

# LeadDocket — Lead Notes

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Add a note to a lead

```http
POST /api/leads/{id}/notes
Content-Type: application/json

{
  "Body": "Spoke with client — confirmed accident date is March 15. Client is ready to proceed.",
  "IsPrivate": false,
  "NoteType": "General"
}
```

`LeadNoteAddApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `Body` | Yes | Note content (plain text or HTML) |
| `IsPrivate` | No | `true` hides note from non-admin users |
| `NoteType` | No | Classification of the note |

Returns `201 Created` with `LeadNoteApi` including the new `Id`.

---

## Update an existing note

```http
PUT /api/leads/{id}/notes/{noteId}
Content-Type: application/json

{
  "Body": "Updated: Spoke with client — confirmed accident date is March 15, 2026.",
  "IsPrivate": false
}
```

`LeadNoteUpdateApi` — replaces the note content. Returns `200 OK` with updated `LeadNoteApi`.

---

## Delete a note

```http
DELETE /api/leads/{id}/notes/{noteId}
```

Returns `204 No Content` on success.

---

## Best Practices

- **Fetch note ID before updating or deleting**: Note IDs are returned in the `LeadNotes` array when fetching a lead with `GET /api/leads/detailed/{id}?flags=LeadNotes`.
- **Timestamp in note body**: When logging from external systems, prefix the note with the source and timestamp: `"[CallRail - 2026-07-01 14:32 UTC] Inbound call, 4 min, qualified."` — LeadDocket does not auto-timestamp external notes.
- **Private notes**: Use `IsPrivate: true` for internal staff notes that should not be visible to all roles.
- **Append vs. replace**: The API has no append endpoint — to add to an existing note, fetch the note body, append your text, then PUT back. For new distinct events, create a new note.
