---
name: leaddocket-templates
description: >
  Create and manage Custom Templates in LeadDocket — reusable email and
  document templates with merge fields that auto-populate from lead and contact
  data. Covers creating templates, inserting merge fields, associating templates
  with statuses or triggers, and using templates in manual or automated sends.
  Use when standardizing firm communications or automating outreach.
---

# LeadDocket — Custom Templates

LeadDocket's template system lets you build reusable email and document
templates that automatically merge lead and contact data.

> Support section: [Custom Templates](https://support.leaddocket.com/hc/en-us/sections/360009506931-Custom-Templates)

---

## Template Types

| Type | Use case |
|------|---------|
| **Email Template** | Standardized client emails, follow-ups, intake confirmations |
| **Document Template** | Engagement letters, retainer agreements, intake packets |

---

## Creating a Template (in the LeadDocket UI)

1. Navigate to **Settings → Templates**
2. Click **New Template**
3. Select the template type (Email or Document)
4. Add a name and subject (for email templates)
5. Build the body in the rich text editor
6. Insert merge fields using the **Insert Field** button
7. Save the template

---

## Available Merge Fields

Merge fields auto-populate from the lead and contact data when the template is used.

| Category | Example merge fields |
|----------|----------------------|
| **Contact** | `{{Contact.FirstName}}`, `{{Contact.LastName}}`, `{{Contact.Email}}`, `{{Contact.Phone}}` |
| **Lead** | `{{Lead.CaseType}}`, `{{Lead.Status}}`, `{{Lead.CreatedDate}}` |
| **Firm/User** | `{{User.FirstName}}`, `{{Firm.Name}}`, `{{Firm.Phone}}` |
| **Custom Fields** | `{{CustomField.DateOfIncident}}`, `{{CustomField.InsuranceCarrier}}` |

---

## Using Templates

### Manual send (UI)

1. Open a lead
2. Click **New Message** or **Send Email**
3. Click **Use Template**
4. Select a template — fields are auto-merged
5. Review and send

### Status-triggered automatic sends

Templates can be attached to status changes to fire automatically:

1. Navigate to **Settings → Statuses**
2. Edit a status
3. Under **Automation**, attach an email template
4. The template fires when a lead moves to that status

---

## Best Practices

- **Use merge fields instead of hardcoded names**: Never type "Dear John" — always use `Dear {{Contact.FirstName}}` so the template works for any client.
- **Test before activating triggers**: Use the manual send flow to preview a merge with a real lead before attaching to a status automation.
- **Consistent naming convention**: Name templates descriptively: `"Intake Confirmation - PI"`, `"Retainer - Auto Accident"`, `"90-Day Follow-Up"`. Avoid generic names like `"Template 1"`.
- **Custom field merge fields**: Ensure the custom field exists and has data on the lead before automating sends that use it — empty merge fields produce awkward emails.
