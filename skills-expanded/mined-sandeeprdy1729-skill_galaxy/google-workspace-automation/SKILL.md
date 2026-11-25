---
name: google-workspace-automation
description: "Automate Google Workspace using Gmail, Calendar, Drive, Sheets, and Docs APIs. Covers authentication, email management, document generation, spreadsheet operations, and AI-powered workspace workflows."
license: Apache 2.0
tags: ["google-workspace", "gmail", "google-drive", "google-sheets", "google-docs", "gsuite", "automation"]
difficulty: intermediate
time_to_master: "8-12 weeks"
version: "1.0.0"
---

# Google Workspace Automation

## Overview

Google Workspace (formerly G Suite) serves 3B+ Gmail users and 10M+ paying organizations. Its APIs provide programmatic access to Gmail, Calendar, Drive, Sheets, Docs, and Meet. AI agents with Workspace access can manage email, generate documents, update spreadsheets, and orchestrate office workflows at scale.

## When to Use This Skill

- Building MCP servers for Gmail management and email triage
- Automating Google Sheets for reporting and data pipelines
- Generating Google Docs from templates or AI content
- Implementing Google Calendar scheduling and availability checking
- Creating file management workflows with Google Drive

## Core Concepts

### Google Workspace API Landscape

| API | Purpose | Key Operations |
|-----|---------|---------------|
| Gmail API | Email management | Send, search, labels, threads |
| Calendar API | Scheduling | Events, availability, reminders |
| Drive API | File management | Upload, share, organize, search |
| Sheets API | Spreadsheet ops | Read, write, format, formulas |
| Docs API | Document generation | Create, insert, format |
| Admin SDK | Org management | Users, groups, audit |

### Authentication

```typescript
import { google } from "googleapis";

// Service Account (server-to-server)
const auth = new google.auth.GoogleAuth({
  keyFile: "service-account-key.json",
  scopes: [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
  ],
  subject: "user@company.com",  // Impersonate user (domain-wide delegation)
});

// OAuth 2.0 (user-interactive)
const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);
```

## Implementation Guide

### Gmail Operations

```typescript
const gmail = google.gmail({ version: "v1", auth });

// Search emails
const searchResults = await gmail.users.messages.list({
  userId: "me",
  q: "is:unread from:client@acme.com after:2026/03/01",
  maxResults: 20,
});

// Get message details
const message = await gmail.users.messages.get({
  userId: "me",
  id: messageId,
  format: "full",
});

// Send email
const encodedMessage = Buffer.from(
  `To: recipient@example.com\r\n` +
  `Subject: Weekly Report\r\n` +
  `Content-Type: text/html; charset=utf-8\r\n\r\n` +
  `<h2>Weekly Summary</h2><p>Key metrics attached.</p>`
).toString("base64url");

await gmail.users.messages.send({
  userId: "me",
  requestBody: { raw: encodedMessage },
});

// Apply labels for organization
await gmail.users.messages.modify({
  userId: "me",
  id: messageId,
  requestBody: {
    addLabelIds: ["Label_Reviewed"],
    removeLabelIds: ["UNREAD"],
  },
});
```

### Google Sheets Operations

```typescript
const sheets = google.sheets({ version: "v4", auth });

// Read data
const data = await sheets.spreadsheets.values.get({
  spreadsheetId: SHEET_ID,
  range: "Pipeline!A1:F100",
});

// Write data
await sheets.spreadsheets.values.update({
  spreadsheetId: SHEET_ID,
  range: "Pipeline!A1",
  valueInputOption: "USER_ENTERED",
  requestBody: {
    values: [
      ["Deal Name", "Stage", "Amount", "Close Date", "Owner", "Probability"],
      ["Acme Corp", "Negotiation", "$150,000", "2026-04-30", "Jane", "75%"],
      ["Beta Inc", "Proposal", "$80,000", "2026-05-15", "John", "50%"],
    ],
  },
});

// Append rows (add to end)
await sheets.spreadsheets.values.append({
  spreadsheetId: SHEET_ID,
  range: "Leads!A:D",
  valueInputOption: "USER_ENTERED",
  requestBody: {
    values: [["New Lead", "lead@example.com", "Technology", new Date().toISOString()]],
  },
});
```

### Google Drive Operations

```typescript
const drive = google.drive({ version: "v3", auth });

// Search files
const files = await drive.files.list({
  q: "name contains 'Q2 Report' and mimeType = 'application/pdf' and trashed = false",
  fields: "files(id, name, modifiedTime, webViewLink, size)",
  orderBy: "modifiedTime desc",
  pageSize: 10,
});

// Upload a file
const uploadedFile = await drive.files.create({
  requestBody: {
    name: "Monthly-Report-March-2026.pdf",
    parents: [folderId],
  },
  media: {
    mimeType: "application/pdf",
    body: fs.createReadStream("report.pdf"),
  },
});

// Share with specific users
await drive.permissions.create({
  fileId: uploadedFile.data.id,
  requestBody: {
    role: "reader",
    type: "user",
    emailAddress: "manager@company.com",
  },
});
```

### Workspace MCP Server

```typescript
server.tool(
  "search_gmail",
  "Search Gmail messages using Gmail search syntax",
  {
    query: z.string().describe("Gmail search query (e.g., 'from:boss is:unread')"),
    maxResults: z.number().default(10),
  },
  async ({ query, maxResults }) => {
    const results = await gmail.users.messages.list({
      userId: "me",
      q: query,
      maxResults,
    });

    if (!results.data.messages?.length) {
      return { content: [{ type: "text", text: "No messages found." }] };
    }

    const messages = await Promise.all(
      results.data.messages.map(async (m) => {
        const full = await gmail.users.messages.get({
          userId: "me", id: m.id, format: "metadata",
          metadataHeaders: ["Subject", "From", "Date"],
        });
        const headers = Object.fromEntries(
          full.data.payload.headers.map(h => [h.name, h.value])
        );
        return { subject: headers.Subject, from: headers.From, date: headers.Date, snippet: full.data.snippet };
      })
    );

    return {
      content: [{
        type: "text",
        text: messages.map(m =>
          `From: ${m.from}\nSubject: ${m.subject}\nDate: ${m.date}\n${m.snippet}\n`
        ).join("\n---\n"),
      }],
    };
  }
);

server.tool(
  "update_spreadsheet",
  "Read from or write to a Google Sheets spreadsheet",
  {
    spreadsheetId: z.string(),
    range: z.string().describe("Cell range (e.g., 'Sheet1!A1:D10')"),
    action: z.enum(["read", "write", "append"]),
    data: z.array(z.array(z.string())).optional().describe("Rows of data for write/append"),
  },
  async ({ spreadsheetId, range, action, data }) => {
    if (action === "read") {
      const result = await sheets.spreadsheets.values.get({ spreadsheetId, range });
      return {
        content: [{
          type: "text",
          text: result.data.values?.map(row => row.join(" | ")).join("\n") || "Empty range",
        }],
      };
    }
    // write or append
    const method = action === "append" ? "append" : "update";
    await sheets.spreadsheets.values[method]({
      spreadsheetId, range,
      valueInputOption: "USER_ENTERED",
      requestBody: { values: data },
    });
    return { content: [{ type: "text", text: `${data.length} rows ${action === "append" ? "appended" : "written"} to ${range}` }] };
  }
);
```

## Best Practices

1. **Use service accounts with domain-wide delegation** for server-side automation
2. **Batch API calls** — Google APIs support batch requests (up to 100 per batch)
3. **Respect quotas** — Gmail: 250 messages/day (free), Drive: 1000 queries/100s
4. **Use push notifications** over polling for real-time updates (Drive, Gmail watch)
5. **Paginate with nextPageToken** — never assume complete results
6. **Scope permissions minimally** — only request OAuth scopes you actually need

## Resources

- [Google Workspace API Documentation](https://developers.google.com/workspace)
- [Gmail API Reference](https://developers.google.com/gmail/api)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [googleapis Node.js Client](https://github.com/googleapis/google-api-nodejs-client)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
