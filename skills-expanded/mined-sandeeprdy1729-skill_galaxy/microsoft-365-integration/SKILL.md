---
name: microsoft-365-integration
description: "Integrate with Microsoft 365 using the Microsoft Graph API. Covers Outlook mail, calendar, Teams, OneDrive, SharePoint, and Excel automation for building AI-powered productivity workflows."
license: Apache 2.0
tags: ["microsoft-365", "graph-api", "outlook", "teams", "sharepoint", "onedrive", "office", "enterprise"]
difficulty: intermediate
time_to_master: "8-14 weeks"
version: "1.0.0"
---

# Microsoft 365 Integration

## Overview

Microsoft 365 powers 400M+ paid seats globally. The Microsoft Graph API provides unified access to Outlook mail, Calendar, Teams, OneDrive, SharePoint, Excel, and more — all through a single REST endpoint. AI agents with Graph API access can manage email, schedule meetings, search documents, post to Teams channels, and automate office workflows.

## When to Use This Skill

- Building MCP servers that manage Outlook email and calendar
- Automating Teams messages, channel management, and meeting scheduling
- Implementing document management with OneDrive and SharePoint
- Creating AI-powered email triage and response workflows
- Building enterprise search across Microsoft 365 content

## Core Concepts

### Microsoft Graph API Structure

```
https://graph.microsoft.com/v1.0/
  ├── /me/                    (Current user)
  │   ├── /messages           (Outlook mail)
  │   ├── /calendar/events    (Calendar)
  │   ├── /drive/root         (OneDrive files)
  │   ├── /joinedTeams        (Teams)
  │   └── /contacts           (People)
  ├── /users/{id}/            (Specific user)
  ├── /groups/{id}/           (Groups/Teams)
  ├── /sites/{id}/            (SharePoint)
  └── /teams/{id}/channels    (Teams channels)
```

### Authentication: Azure AD OAuth 2.0

| Flow | Use Case | Scopes |
|------|----------|--------|
| Authorization Code | User-interactive apps | Delegated permissions |
| Client Credentials | Daemon/service apps | Application permissions |
| On-Behalf-Of | API-to-API delegation | Delegated via middleware |

### Common Permissions

| Operation | Permission (Delegated) | Permission (Application) |
|-----------|----------------------|-------------------------|
| Read mail | Mail.Read | Mail.Read |
| Send mail | Mail.Send | Mail.Send |
| Read calendar | Calendars.Read | Calendars.Read |
| Create events | Calendars.ReadWrite | Calendars.ReadWrite |
| Read files | Files.Read | Files.Read.All |
| Post to Teams | ChannelMessage.Send | ChannelMessage.Send |

## Implementation Guide

### Email Management

```typescript
import { Client } from "@microsoft/microsoft-graph-client";

const graphClient = Client.init({
  authProvider: (done) => done(null, accessToken),
});

// Get recent emails
const messages = await graphClient
  .api("/me/messages")
  .select("subject,from,receivedDateTime,bodyPreview,isRead")
  .filter("isRead eq false")
  .orderby("receivedDateTime desc")
  .top(20)
  .get();

// Send an email
await graphClient
  .api("/me/sendMail")
  .post({
    message: {
      subject: "Q2 Pipeline Review",
      body: {
        contentType: "HTML",
        content: "<p>Please review the attached pipeline summary.</p>",
      },
      toRecipients: [
        { emailAddress: { address: "manager@company.com" } },
      ],
    },
  });

// Search emails
const searchResults = await graphClient
  .api("/me/messages")
  .filter(`contains(subject, 'contract') and receivedDateTime ge ${thirtyDaysAgo}`)
  .select("subject,from,receivedDateTime,bodyPreview")
  .top(10)
  .get();
```

### Calendar Operations

```typescript
// Get upcoming meetings
const events = await graphClient
  .api("/me/calendarView")
  .query({
    startDateTime: new Date().toISOString(),
    endDateTime: new Date(Date.now() + 7 * 86400000).toISOString(),
  })
  .select("subject,start,end,location,attendees,isOnlineMeeting")
  .orderby("start/dateTime")
  .get();

// Schedule a meeting
const newEvent = await graphClient
  .api("/me/events")
  .post({
    subject: "Design Review",
    start: { dateTime: "2026-04-01T14:00:00", timeZone: "America/New_York" },
    end: { dateTime: "2026-04-01T15:00:00", timeZone: "America/New_York" },
    attendees: [
      {
        emailAddress: { address: "colleague@company.com", name: "Jane Doe" },
        type: "required",
      },
    ],
    isOnlineMeeting: true,
    onlineMeetingProvider: "teamsForBusiness",
  });

// Find available meeting times
const availability = await graphClient
  .api("/me/findMeetingTimes")
  .post({
    attendees: [
      { emailAddress: { address: "colleague@company.com" }, type: "required" },
    ],
    timeConstraint: {
      timeslots: [{
        start: { dateTime: "2026-04-01T09:00:00", timeZone: "America/New_York" },
        end: { dateTime: "2026-04-03T17:00:00", timeZone: "America/New_York" },
      }],
    },
    meetingDuration: "PT1H",
  });
```

### Teams Integration

```typescript
// Post a message to a Teams channel
await graphClient
  .api(`/teams/${teamId}/channels/${channelId}/messages`)
  .post({
    body: {
      contentType: "html",
      content: "<h3>Daily Pipeline Update</h3><p>3 deals moved to negotiation stage today.</p>",
    },
  });

// Get chat messages
const messages = await graphClient
  .api(`/me/chats/${chatId}/messages`)
  .top(50)
  .get();
```

### Microsoft 365 MCP Server

```typescript
server.tool(
  "search_emails",
  "Search Outlook emails by subject, sender, or content",
  {
    query: z.string().describe("Search terms"),
    folder: z.enum(["inbox", "sent", "drafts", "all"]).default("inbox"),
    unreadOnly: z.boolean().default(false),
    days: z.number().default(7),
  },
  async ({ query, folder, unreadOnly, days }) => {
    let filter = `receivedDateTime ge ${daysAgo(days)}`;
    if (unreadOnly) filter += " and isRead eq false";

    const messages = await graphClient
      .api("/me/messages")
      .search(`"${query}"`)
      .filter(filter)
      .select("subject,from,receivedDateTime,bodyPreview,isRead")
      .top(15)
      .get();

    return {
      content: [{
        type: "text",
        text: messages.value.map(m =>
          `${m.isRead ? "📭" : "📬"} ${m.from.emailAddress.name}: ${m.subject}\n` +
          `  ${m.receivedDateTime} | ${m.bodyPreview.slice(0, 100)}...`
        ).join("\n\n"),
      }],
    };
  }
);

server.tool(
  "get_upcoming_meetings",
  "Get upcoming calendar events for the next N days",
  {
    days: z.number().default(3),
  },
  async ({ days }) => {
    const events = await graphClient
      .api("/me/calendarView")
      .query({
        startDateTime: new Date().toISOString(),
        endDateTime: new Date(Date.now() + days * 86400000).toISOString(),
      })
      .select("subject,start,end,attendees,isOnlineMeeting,onlineMeetingUrl")
      .orderby("start/dateTime")
      .get();

    return {
      content: [{
        type: "text",
        text: events.value.map(e =>
          `📅 ${e.subject}\n` +
          `  ${formatDateTime(e.start)} - ${formatDateTime(e.end)}\n` +
          `  Attendees: ${e.attendees.map(a => a.emailAddress.name).join(", ")}\n` +
          (e.isOnlineMeeting ? `  Teams: ${e.onlineMeetingUrl}` : "  In-person")
        ).join("\n\n"),
      }],
    };
  }
);
```

## Best Practices

1. **Use delegated permissions** when acting on behalf of a user; application permissions for daemons
2. **Request minimal scopes** — only ask for permissions the app actually needs
3. **Use $select to limit fields** — reduces payload size and improves performance
4. **Implement delta queries** for incremental sync instead of full re-fetch
5. **Handle throttling** — respect `Retry-After` headers on 429 responses
6. **Use batch requests** — combine up to 20 requests in a single batch call

## Resources

- [Microsoft Graph Documentation](https://learn.microsoft.com/en-us/graph/)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Microsoft Graph JS SDK](https://github.com/microsoftgraph/msgraph-sdk-javascript)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
