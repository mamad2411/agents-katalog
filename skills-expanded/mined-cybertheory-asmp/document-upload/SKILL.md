---
name: document-upload-skill
description: Submit a document URL for processing
version: "1.0"
---

# Document Upload Skill

Use this skill when the workflow state is **UPLOAD** or **INITIAL**.

## Instructions

1. Obtain a URL to the document (PDF, DOCX, or similar). The URL must be accessible to the server.
2. Call the **submit_doc** action with a JSON body:
   - `file_url` (string, required): The full URL of the document.

## Example

```json
{
  "file_url": "https://storage.example.com/contracts/doc.pdf"
}
```

Do not proceed to audit until the server confirms the document was received (next state will be ANALYZING or AUDIT).
