---
name: leaddocket-docusign
description: >
  Send and track e-sign documents using the DocuSign integration built into
  LeadDocket. Covers the workflow for sending documents to leads for electronic
  signature, tracking signature status, and handling completed documents. Use
  when automating retainer agreements, engagement letters, or any document
  requiring client signature. Configured through the LeadDocket UI and managed
  through the Filevine/DocuSign integration layer.
---

# LeadDocket — DocuSign E-Sign Integration

LeadDocket has a native **DocuSign** integration for sending documents to leads for electronic signature directly from a lead record.

> Support section: [Docusign](https://support.leaddocket.com/hc/en-us/sections/360009497071-Docusign)

---

## Integration Setup (Admin, in LeadDocket UI)

1. Navigate to **Settings → Integrations → DocuSign**
2. Connect your DocuSign account (OAuth flow)
3. Configure document templates in DocuSign
4. Map DocuSign template fields to LeadDocket lead fields for auto-population
5. Enable the integration

---

## Sending a Document for Signature (in the LeadDocket UI)

1. Open a lead
2. Click **Send Document** (or the DocuSign icon)
3. Select a document template
4. Review the pre-populated fields (mapped from lead data)
5. Add or modify recipients (defaults to lead's primary contact)
6. Click **Send**

LeadDocket sends the DocuSign envelope and records it in the lead's activity.

---

## Tracking Signature Status

Signed documents are visible in the lead's **E-Sign Documents** section.

Via the API, fetch e-sign document status using the detailed lead endpoint:

```http
GET /api/leads/detailed/{leadId}?flags=EsignDocuments
```

Returns the lead with an `EsignDocuments` array:

```json
{
  "EsignDocuments": [
    {
      "Id": 99,
      "TemplateId": "docusign-template-uuid",
      "Status": "Completed",
      "SentDate": "2026-06-20T10:00:00Z",
      "CompletedDate": "2026-06-20T14:22:00Z",
      "RecipientEmail": "client@example.com"
    }
  ]
}
```

---

## Document Status Values

| Status | Meaning |
|--------|---------|
| `Sent` | Envelope sent, awaiting client action |
| `Delivered` | Client has opened the document |
| `Completed` | All signatures collected |
| `Declined` | Client declined to sign |
| `Voided` | Envelope was cancelled |
| `Expired` | Envelope expired before signing |

---

## Best Practices

- **Map lead fields to DocuSign templates**: Spend time mapping LeadDocket custom fields to DocuSign template fields upfront to avoid manual data entry.
- **Use templates**: Create DocuSign templates for retainer agreements, fee agreements, and intake authorizations — don't upload ad-hoc PDFs each time.
- **Poll for completion**: Use `GET /api/leads/detailed/{leadId}?flags=EsignDocuments` in your integration to detect when documents are completed and trigger downstream actions (e.g., status change, Filevine file creation).
- **Check `Settings` first**: Verify DocuSign is enabled on the account via `GET /api/settings/get-options` before attempting to trigger e-sign workflows programmatically.
