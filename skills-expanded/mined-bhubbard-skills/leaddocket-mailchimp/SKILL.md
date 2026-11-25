---
name: leaddocket-mailchimp
description: >
  Sync Contacts and Leads from LeadDocket to MailChimp for email marketing
  campaigns. Covers configuring the MailChimp integration, mapping LeadDocket
  contacts to MailChimp audiences, triggering list syncs based on status
  changes, and tagging contacts in MailChimp based on case type. Use when
  automating law firm newsletter or drip campaign enrollment from intake data.
---

# LeadDocket — MailChimp Integration

LeadDocket integrates with **MailChimp** to sync contacts for email marketing campaigns. When leads move through the pipeline, their contacts can be automatically added to MailChimp audiences/lists.

> Support section: [MailChimp](https://support.leaddocket.com/hc/en-us/sections/360009496871-MailChimp)

---

## Integration Setup (Admin, in the LeadDocket UI)

1. Navigate to **Settings → Integrations → MailChimp**
2. Click **Connect MailChimp Account**
3. Authenticate with your MailChimp credentials (OAuth)
4. Select the MailChimp audience (list) to sync to
5. Configure field mapping:
   - `Contact.FirstName` → `FNAME`
   - `Contact.LastName` → `LNAME`
   - `Contact.Email` → `EMAIL`
   - Custom fields → MailChimp merge tags
6. Save

---

## Sync Triggers

| Trigger | Behavior |
|---------|----------|
| **Lead status change** | When a lead moves to a configured status, the contact is added to MailChimp |
| **Opportunity created** | New opportunity contact optionally added to intake list |
| **Manual sync** | Bulk sync contacts from the admin panel |

### Configuring status-based sync

1. Navigate to **Settings → Statuses**
2. Edit a status
3. Under **MailChimp**, select the audience and enable sync
4. Save

---

## Field Mapping

| LeadDocket field | MailChimp tag |
|-----------------|--------------|
| `Contact.FirstName` | `FNAME` |
| `Contact.LastName` | `LNAME` |
| `Contact.Email` | `EMAIL` |
| `Contact.Phone` | `PHONE` |
| `Lead.CaseType` | `CASETYPE` (custom merge tag) |
| `Lead.Status` | `STATUS` (custom merge tag) |
| Custom fields | Map to MailChimp merge tags |

---

## Tagging Contacts in MailChimp

Configure LeadDocket to apply MailChimp tags based on lead properties:

- Case type: tag as "Personal Injury", "Auto Accident", "Slip and Fall"
- Lead status: tag as "Prospect", "Active Client", "Settled"
- Lead source: tag as "Google", "Referral", "Billboard"

Tags allow targeted campaigns to segments of your list.

---

## Best Practices

- **Only sync opted-in contacts**: Confirm email marketing consent at intake before syncing. LeadDocket can capture consent in a custom field; only sync contacts where that field is `true`.
- **Map case type as a tag**: Tag by case type in MailChimp to send relevant newsletters (PI newsletter to PI clients, not DUI clients).
- **Use double opt-in in MailChimp**: Enable double opt-in in your MailChimp audience settings to prevent deliverability issues from incorrect email addresses.
- **Sync on acceptance, not inquiry**: Only sync contacts who have been accepted as clients, not raw opportunity inquiries — not all inquiries consent to marketing.
- **Monitor unsubscribes**: MailChimp unsubscribes should be reflected back to LeadDocket — tag or note the contact as unsubscribed to prevent accidental re-syncing.
