---

name: sarah-outbound-caller
description: sarah-outbound-caller lets the user deploy and manage Sarah, a VAPI-powered AI voice assistant that runs four distinct outbound call types — REI property acquisition, event reminders, community engagement, and agency outreach — with strict script isolation per campaign, which is useful when they want to automate calling campaigns, set up new call flows, or manage multi-vertical outreach without manual dialing.

---
Sarah is a VAPI-powered AI voice assistant that handles outbound calls for four business verticals with strict script isolation. This skill packages the complete system: Vercel dashboard, VAPI integration, call routing logic, and conversation prompts.

## What This Skill Does

This skill sarah-outbound-caller lets the user deploy and manage Sarah, a VAPI-powered AI voice assistant that runs four distinct outbound call types — REI property acquisition, event reminders, community engagement, and agency outreach — with strict script isolation per campaign, which is useful when they want to automate calling campaigns, set up new call flows, or manage multi-vertical outreach without manual dialing.

## System Overview

**Components:**
- **Vercel Dashboard** (`index.html`) - Web interface for triggering calls (single/batch CSV)
- **API Handler** (`api/call.js`) - Serverless function routing calls to VAPI
- **VAPI Assistant** - Sarah's voice AI (ID: `2e7609a1-dcfd-430e-9111-1426cb3cb38e`)
- **System Prompt** - Unified conversation logic with context-based routing

## Four Call Types

| Type | Business | Purpose | Key Info |
|------|----------|---------|----------|
| **Acquisition** | Chucky Buys Lucky Houses | Property cash offers | `name`, `phone`, `address` |
| **RDM** | Real Deal Meetup | Event reminders/invites | `name`, `phone`, `message`, `type: rdm` |
| **Skool** | REI AI Skool Community | Community engagement | `name`, `phone`, `message`, `type: skool` |
| **MMS** | Mad Marketing Success | AI/GHL agency outreach | `name`, `phone`, `message`, `type: mms` |

**Critical Rule:** Sarah NEVER cross-contaminates scripts. Each call type stays 100% isolated.

## Quick Start

### Deploy Dashboard

```bash
# Clone repo (if not exists)
gh repo clone jamesclawbot-pixel/sarah-caller-app

# Deploy to Vercel
cd sarah-caller-app
vercel deploy --prod
```

**After deployment, Vercel will output the live URL. If the command center is not already open, always provide this URL to the user so they can access the dashboard.**

Example:
```
✅ Deployed to: https://company-dashboard-beta-one.vercel.app/
```

**Always share the Vercel URL immediately after successful deployment (unless already open in user's browser).**

### Update Sarah's Prompt

1. Go to https://vapi.ai/dashboard
2. Find assistant `2e7609a1-dcfd-430e-9111-1426cb3cb38e`
3. Copy `references/SARAH-UNIFIED-PROMPT.md`
4. Paste into **System Prompt** field
5. Save

### Test Single Call

Dashboard: https://company-dashboard-beta-one.vercel.app/

**Acquisition Test:**
- Name: `John Smith`
- Phone: `+1234567890`
- Address: `1234 Main St NW, Washington DC`
- Click **"Trigger Outreach Call"**

**RDM/Skool/MMS Test:**
- Name: `Jane Doe`
- Phone: `+1234567890`
- Message: `Custom message here`
- Click corresponding business button

## Modifying Call Scripts

### Update Opening Script

Edit `api/call.js`:

```javascript
if (spokenAddress) {
    firstMessage = `Hi can I speak with ${firstName}, this is Sarah... at ${spokenAddress}.`;
}
```

Push to GitHub → Vercel auto-deploys.

### Update Conversation Logic

Edit `references/SARAH-UNIFIED-PROMPT.md`, then:
1. Copy updated prompt
2. Paste into VAPI dashboard
3. Test calls to verify

### Add New Call Type

**1. Update `api/call.js`:**

```javascript
if (type === 'new-type') {
    firstMessage = `Hi ${firstName}, this is Sarah... [custom message]`;
}
```

**2. Update VAPI prompt:**
Add new call flow section to `SARAH-UNIFIED-PROMPT.md`.

**3. Update dashboard:**
Add new card to `index.html` with form and trigger button.

**4. Deploy:**
```bash
git add -A
git commit -m "Add new call type: [type]"
git push
```

## Address Formatting

Sarah speaks addresses naturally (e.g., "Main Street Northwest" not "Main St NW").

**Function:** `formatAddressForSpeech(address)` in `api/call.js`

**Expansions:**
- `St` → `Street`
- `NW` → `Northwest`
- `Ave` → `Avenue`
- etc.

**Test:**
```bash
cd /data/.openclaw/workspace
node test-sarah-address.js
```

## Script Isolation Rules

See `references/SARAH-SCRIPT-ISOLATION-RULES.md` for complete boundaries.

**Key Rule:** Sarah NEVER mentions other businesses unless explicitly asked, and even then defers to Charles:

> "I'm specifically calling about [current business]. If you're interested in other services, I can have Charles reach out separately."

## Batch CSV Processing

Dashboard supports CSV uploads for batch calling.

**CSV Format:**
```csv
Name,Phone,Address
John Smith,+1234567890,1234 Main St NW
Jane Doe,+1987654321,567 Oak Ave SE
```

**Note:** Address column optional for RDM/Skool/MMS types.

## Environment Variables

Vercel env vars (set in dashboard):
- `VAPI_API_KEY` - VAPI API key

## Files Reference

### Core Files
- `references/index.html` - Dashboard UI
- `references/api/call.js` - API handler with address formatting
- `references/SARAH-UNIFIED-PROMPT.md` - VAPI system prompt
- `references/test-sarah-address.js` - Address formatter test suite

### Documentation
- `references/SARAH-CALL-TYPES.md` - Four call type specifications
- `references/SARAH-SCRIPT-ISOLATION-RULES.md` - Script boundaries and rules
- `references/SARAH-ADDRESS-FIX.md` - Address pronunciation implementation

### Prompt Variants (reference only)
- `references/sarah-prompts/SARAH-ACQUISITION-PROMPT.md`
- `references/sarah-prompts/SARAH-RDM-PROMPT.md`
- `references/sarah-prompts/SARAH-SKOOL-PROMPT.md`
- `references/sarah-prompts/SARAH-MMS-PROMPT.md`

(These are isolated prompt variants if you ever want to split Sarah into 4 separate assistant IDs. Current system uses unified prompt.)

## Troubleshooting

**Sarah reads "property address" literally:**
- Check VAPI prompt has no `{{property_address}}` placeholders
- Use `references/SARAH-UNIFIED-PROMPT.md` (no variable placeholders)

**Sarah mentions wrong business:**
- Verify `type` parameter is set correctly in dashboard
- Check `firstMessage` logic in `api/call.js`
- Review VAPI prompt boundaries

**Address pronunciation wrong:**
- Run `node test-sarah-address.js` to verify formatting
- Check `formatAddressForSpeech()` expansions in `api/call.js`

**Call not triggering:**
- Verify VAPI API key in Vercel env vars
- Check browser console for API errors
- Confirm phone number format (`+1...`)

## GitHub Repository

Repo: `jamesclawbot-pixel/sarah-caller-app`  
Live URL: https://company-dashboard-beta-one.vercel.app/  
VAPI Dashboard: https://vapi.ai/dashboard

## Next Steps

After deployment:
1. Test each call type independently
2. Verify script isolation (ask off-topic questions)
3. Confirm address pronunciation
4. Review call logs in VAPI dashboard
5. Iterate on prompts based on real call performance
