---
name: compliance-handling
description: When the user wants to build or improve a sales bot's ability to respect opt-outs, DNC lists, and regulatory requirements like TCPA and ACMA. Also use when the user mentions "compliance," "opt-out handling," "TCPA," "ACMA," "DNC lists," "unsubscribe," or "regulatory requirements."
---

# Compliance Handling for Sales Bots

You are an expert in building compliance systems for automated sales bots. Your goal is to help design systems that respect opt-outs, DNC lists, and regulatory requirements across channels.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels does your bot operate on?
   - What regions do you operate in?
   - What regulations apply to your business?

2. **Current State**
   - How do you handle opt-outs today?
   - Do you have a DNC list process?
   - Have you had any compliance issues?

3. **Goals**
   - What compliance capabilities do you need?
   - What risks are you trying to mitigate?

---

## Core Principles

### 1. Compliance is Non-Negotiable
- This isn't about conversion optimization
- Violations have real consequences
- When in doubt, don't contact

### 2. Opt-Out Must Be Instant
- Process immediately
- No exceptions
- No "one more message"

### 3. Documentation is Critical
- Record everything
- Timestamps matter
- Audit trail required

### 4. Stay Current
- Regulations change
- New channels, new rules
- Regular review required

---

## Regulatory Framework

### TCPA (US - SMS/Voice)

**Key requirements:**
- Prior express written consent for marketing
- Honor opt-out requests immediately
- No calls/texts to numbers on DNC list
- Calling hours: 8am-9pm local time
- Must identify sender

**Opt-out keywords:**
- STOP
- UNSUBSCRIBE
- CANCEL
- END
- QUIT

**Penalties:**
- $500-$1,500 per violation
- Class action potential
- Private right of action

### ACMA (Australia - SMS/Voice)

**Key requirements:**
- Consent required (express or inferred)
- Must include opt-out mechanism
- Honor opt-out within 5 business days
- Calling hours: 9am-8pm weekdays, 9am-5pm Saturday
- No Sunday/public holiday calls

**Do Not Call Register:**
- Check before calling
- Re-check every 30 days
- Maintain wash records

### CAN-SPAM (US - Email)

**Key requirements:**
- Identify as advertisement
- Include physical address
- Clear opt-out mechanism
- Honor opt-out within 10 days
- Accurate header information

### GDPR (EU/UK)

**Key requirements:**
- Lawful basis for processing
- Purpose limitation
- Right to access, correct, delete
- Data minimization
- Privacy by design

### CASL (Canada)

**Key requirements:**
- Express or implied consent
- Identify sender clearly
- Include unsubscribe mechanism
- Honor unsubscribe promptly
- Record keeping

---

## Opt-Out Implementation

### Detection Priority

**Immediate detection (before any other processing):**
```
function processMessage(message, contact) {
  // FIRST: Check for opt-out
  if (isOptOut(message.content)) {
    processOptOut(contact, message.channel)
    return sendOptOutConfirmation(contact)
  }

  // THEN: Normal processing
  return normalProcessing(message, contact)
}
```

### Opt-Out Keywords

**SMS (TCPA compliant):**
```
OPT_OUT_KEYWORDS = [
  "STOP",
  "UNSUBSCRIBE",
  "CANCEL",
  "END",
  "QUIT",
  "STOPALL",
  "STOP ALL"
]

function isOptOut(message) {
  normalized = message.toUpperCase().trim()
  return OPT_OUT_KEYWORDS.includes(normalized) ||
         containsOptOutPhrase(message)
}

function containsOptOutPhrase(message) {
  phrases = [
    "stop texting",
    "stop messaging",
    "remove me",
    "take me off",
    "opt out",
    "opt-out"
  ]
  lower = message.toLowerCase()
  return phrases.some(p => lower.includes(p))
}
```

### Opt-Out Processing

```
function processOptOut(contact, channel) {
  // Record the opt-out
  optOutRecord = {
    contact_id: contact.id,
    channel: channel,
    timestamp: now(),
    source: "message",
    original_message: message.content
  }
  saveOptOut(optOutRecord)

  // Update contact record
  contact.opt_out_status[channel] = true
  contact.opt_out_date[channel] = now()
  saveContact(contact)

  // Add to suppression list
  addToSuppressionList(contact.phone || contact.email, channel)

  // Cancel any scheduled messages
  cancelScheduledMessages(contact.id, channel)

  // Log for audit
  auditLog("OPT_OUT", contact.id, channel, now())
}
```

### Confirmation Messages

**SMS:**
"You've been unsubscribed and will no longer receive messages from [Company]. Reply HELP for help."

**Email:**
Subject: "You've been unsubscribed"
"You have been successfully removed from our mailing list. You will no longer receive marketing emails from [Company]."

---

## Do Not Call/Contact Lists

### DNC List Management

**Internal DNC:**
- Customer opt-outs
- Complaint-generated entries
- Manual additions

**External DNC:**
- National registries (FTC, ACMA)
- State registries
- Industry-specific lists

### List Checking

```
function canContact(contact, channel) {
  // Check internal suppression
  if (isOnInternalDNC(contact, channel)) {
    return { allowed: false, reason: "internal_opt_out" }
  }

  // Check external registries
  if (channel == "phone" || channel == "sms") {
    if (isOnNationalDNC(contact.phone)) {
      return { allowed: false, reason: "national_dnc" }
    }
  }

  // Check consent status
  if (!hasValidConsent(contact, channel)) {
    return { allowed: false, reason: "no_consent" }
  }

  // Check contact frequency limits
  if (exceedsFrequencyLimit(contact, channel)) {
    return { allowed: false, reason: "frequency_limit" }
  }

  return { allowed: true }
}
```

### List Updates

**Frequency:**
- National DNC: Check before each campaign, refresh every 31 days
- Internal lists: Real-time updates
- Consent records: Update on every interaction

---

## Consent Management

### Consent Types

**Express consent:**
- Written or digital agreement
- Clear affirmative action
- Documented and timestamped

**Implied consent:**
- Existing business relationship
- Inquiry (limited time)
- Published contact (limited scope)

### Consent Recording

```
ConsentRecord = {
  contact_id: string,
  consent_type: "express" | "implied",
  channel: "email" | "sms" | "phone",
  granted_at: timestamp,
  source: string,  // "web_form", "verbal", "business_relationship"
  proof: string,   // Form submission ID, recording ID, etc.
  scope: string,   // What they consented to
  expires: timestamp | null
}
```

### Consent Verification

```
function hasValidConsent(contact, channel, purpose) {
  consent = getConsentRecord(contact.id, channel)

  if (!consent) return false
  if (consent.expires && consent.expires < now()) return false
  if (!scopeCovers(consent.scope, purpose)) return false

  return true
}
```

---

## Time-of-Day Compliance

### Quiet Hours

```
QUIET_HOURS = {
  "US": { start: 21, end: 8 },      // 9pm-8am
  "AU": {
    weekday: { start: 20, end: 9 },  // 8pm-9am
    saturday: { start: 17, end: 9 }, // 5pm-9am
    sunday: "no_contact"
  },
  "UK": { start: 21, end: 8 }
}

function isContactAllowed(contact, channel) {
  if (channel != "phone" && channel != "sms") return true

  local_time = getLocalTime(contact.timezone)
  region = contact.region

  hours = QUIET_HOURS[region]
  // ... check against current time
}
```

### Scheduling Around Quiet Hours

```
function scheduleMessage(contact, message, preferred_time) {
  if (isContactAllowed(contact, message.channel, preferred_time)) {
    return schedule(message, preferred_time)
  }

  // Find next allowed time
  next_allowed = getNextAllowedTime(contact, message.channel)
  return schedule(message, next_allowed)
}
```

---

## Message Requirements

### Required Disclosures

**SMS:**
- Sender identification
- Opt-out instructions
- Message frequency disclosure (at opt-in)

**Email:**
- Physical postal address
- Unsubscribe mechanism
- Clear identification as marketing (if applicable)

**Voice:**
- Identify caller and company
- Purpose of call
- Bot disclosure (in some jurisdictions)

### Message Templates

**SMS with required elements:**
```
[Company Name]: [Message content]

Reply STOP to unsubscribe
```

**Email footer:**
```
[Company Name]
[Physical Address]

You're receiving this because [reason].
Unsubscribe: [link]
```

---

## Audit and Documentation

### What to Log

**For every contact attempt:**
- Contact ID
- Channel
- Timestamp
- Message content
- Consent verification result
- DNC check result
- Outcome

**For every opt-out:**
- Contact ID
- Channel
- Timestamp
- Source (keyword, link, request)
- Original message
- Processing time

### Retention Requirements

**Keep records for:**
- 4 years (TCPA safe harbor)
- 3 years (CAN-SPAM)
- As required by GDPR
- Check jurisdiction-specific requirements

### Audit Trail

```
AuditRecord = {
  timestamp: datetime,
  action_type: "contact_attempt" | "opt_out" | "consent_change",
  contact_id: string,
  channel: string,
  details: object,
  compliance_checks: [
    { check: "dnc_list", result: "pass", timestamp: datetime },
    { check: "consent", result: "pass", timestamp: datetime },
    { check: "quiet_hours", result: "pass", timestamp: datetime }
  ]
}
```

---

## Error Handling

### When Compliance Fails

**Failed DNC check:**
- Do not send
- Log the block
- Alert if unexpected

**No consent found:**
- Do not send
- Flag for consent capture
- Consider alternative channel

**Quiet hours violation:**
- Reschedule, don't send
- Log the reschedule
- Ensure future delivery

### Edge Cases

**Consent expired:**
- Treat as no consent
- Attempt re-consent if appropriate

**Contact in multiple regions:**
- Apply strictest rules
- Document decision logic

**Unclear opt-out:**
- Err on side of caution
- May ask for clarification (once)

---

## Questions to Ask

If you need more context:
1. What channels do you use for outreach?
2. What regions/countries do you operate in?
3. How do you currently capture consent?
4. Have you had any compliance issues?
5. What systems store your contact/consent data?

---

## Related Skills

- **intent-detection**: Detecting opt-out intent
- **multi-channel-coordination**: Compliance across channels
- **conversation-memory**: Storing consent records
- **timing-optimization**: Quiet hours compliance
