---
name: schedule-audit
description: >-
  Audit an instructor's upcoming training schedule from Airtable. Use when the user asks to
  "audit schedule", "check instructor schedule", "review upcoming classes for [name]",
  "find schedule conflicts", "check teaching assignments", or mentions instructor schedule
  validation.
disabled-model-invocation: true
argument-hint: "[instructor name]"
---

# Schedule Audit

Audit an instructor's upcoming ILT training schedule for collisions, skills gaps, travel needs, and timezone edge cases. Data is sourced from the Airtable Training Operations base via MCP.

## Constants

| Constant | Value |
|----------|-------|
| Base ID | `appNCMjJ2yMKUrTbo` |
| ILT Schedule Table | `tblU6ek43LMSNgFj8` |
| Instructors Table | `tblIG4Y3lyz33rdh0` |
| Instructor Skills Table | `tblaVtSE8BjLH0x7b` |
| Audit Window | 4 weeks from today |

## CRITICAL: Airtable Date Handling

Airtable `Start Date` and `End Date` values are stored as the **delivery-timezone local time with a fake Z (UTC) suffix**. They are NOT true UTC.

Example: A session in CET with `Start Date: 2026-03-02T09:00:00.000Z` actually means **09:00 CET**, not 09:00 UTC. The true UTC would be 08:00.

**To get true UTC for collision detection**, you must:
1. Parse the date string, stripping the Z
2. Attach the session's delivery timezone (from the `Timezone` field)
3. Convert to UTC

```python
from zoneinfo import ZoneInfo
from datetime import datetime
# CORRECT: treat stored time as delivery-local
local_dt = datetime.fromisoformat("2026-03-02T09:00:00").replace(tzinfo=ZoneInfo("Europe/Paris"))
utc_dt = local_dt.astimezone(ZoneInfo("UTC"))  # 08:00 UTC
```

For sessions without a `Timezone` field (Travel, Internal Work blocks), treat the stored time as-is.

## Timezone Mapping

The ILT Schedule `Timezone` field and the Instructor `Home Timezone` field use **different naming conventions**. Both must map to IANA identifiers.

### ILT Schedule Timezone Values (region-code style)

| Airtable Value | IANA Timezone |
|----------------|---------------|
| ET - NEW YORK | America/New_York |
| CT - CHICAGO | America/Chicago |
| MT - DENVER | America/Denver |
| PT - LOS ANGELES | America/Los_Angeles |
| UK - LONDON | Europe/London |
| GMT - LONDON | Europe/London |
| CET - PARIS | Europe/Paris |
| CET - BERLIN | Europe/Berlin |
| EEST | Europe/Athens |
| IST - MUMBAI | Asia/Kolkata |
| IST - TEL AVIV | Asia/Jerusalem |
| SGT - SINGAPORE | Asia/Singapore |
| HKT - HONG KONG | Asia/Hong_Kong |
| JST - TOKYO | Asia/Tokyo |
| KST - SEOUL | Asia/Seoul |
| AET - SYDNEY | Australia/Sydney |
| AEST - SYDNEY | Australia/Sydney |
| BRT - SAO PAULO | America/Sao_Paulo |
| CST - SHANGHAI | Asia/Shanghai |
| VNT - HO CHI MINH | Asia/Ho_Chi_Minh |
| ICT - BANGKOK | Asia/Bangkok |

### Instructor Home Timezone Values (Windows-style names)

| Airtable Value | IANA Timezone |
|----------------|---------------|
| Eastern Time | America/New_York |
| Central Time | America/Chicago |
| Mountain Time | America/Denver |
| Pacific Time | America/Los_Angeles |
| Greenwich Mean Time | Europe/London |
| Central European Standard Time | Europe/Berlin |
| Eastern European Summer Time | Europe/Athens |
| India Standard Time | Asia/Kolkata |
| IST | Asia/Kolkata |
| Singapore Standard Time | Asia/Singapore |
| Japan Standard Time | Asia/Tokyo |
| Korea Standard Time | Asia/Seoul |
| Australian Eastern Standard Time | Australia/Sydney |
| Australian Eastern Time | Australia/Sydney |
| Brasilia Standard Time | America/Sao_Paulo |
| Gulf Standard Time | Asia/Dubai |

If a value does not match either table, log it as an unknown timezone in the output footer and fall back to UTC.

---

## Step 1: Input & Date Setup

The instructor name is `$ARGUMENTS`. If blank, ask the user for a name before proceeding.

Get today's date and 4-week window end:

```bash
python3 -c "
from datetime import datetime, timedelta, timezone
today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
end = today + timedelta(days=28)
print(f'TODAY={today.strftime(\"%Y-%m-%dT%H:%M:%S.000Z\")}')
print(f'END={end.strftime(\"%Y-%m-%dT%H:%M:%S.000Z\")}')
"
```

Store both dates for use in later steps.

---

## Step 2: Instructor Lookup

Search the Instructors table for the given name:

- **Tool**: `mcp__airtable__search_records`
- **baseId**: `appNCMjJ2yMKUrTbo`
- **tableId**: `tblIG4Y3lyz33rdh0`
- **searchTerm**: the instructor name from $ARGUMENTS

### Handle Results

1. **No results** — Report "No instructor found matching '[name]'" and stop.
2. **One result** — Use that record.
3. **Multiple results** — Filter for records where `Status` is `"Approved"` or `"Brickster - Approved"`. Ignore records with Status = "Moved to Super ATP", "Deactivated", "Inactive", "Candidate". If multiple "Approved" records remain, present them to the user and ask which to use.

### Extract Instructor Profile

From the matched record, capture:

| Field | Use |
|-------|-----|
| `Instructor Name` | Display name |
| `Instructor Email` | Contact reference |
| `Home Timezone` | Primary display TZ — map to IANA using the table above |
| `Teaching Timezones` | Approved delivery TZs |
| `Approved Courses` | Linked record IDs — resolve via Instructor Skills table in Step 5 |
| `Instructor Skills` | Linked record IDs to Instructor Skills & Credentials table |
| `Certifications` | Additional qualifications |
| `On-Site Approved` | "Yes" or "No" — onsite eligibility |
| `Location` | Home base city |
| `ILT (Instructor+TA) Schedule` | Array of linked record IDs — these are the session references |
| Record ID | For cross-referencing |

---

## Step 3: Fetch Future Sessions

The `ILT (Instructor+TA) Schedule` field contains record IDs linking to the ILT Schedule table. These include ALL historical sessions (some instructors have 500+). Do NOT fetch all of them.

### Fetching Strategy

**For instructors with <= 40 linked sessions**: Fetch all by ID.

**For instructors with > 40 linked sessions**: Linked IDs are appended chronologically, so the most recent sessions are at the END of the array. Take the **last 40 IDs** from the array — this covers recent and upcoming sessions while avoiding hundreds of unnecessary API calls.

For each record ID in the set, call:

- **Tool**: `mcp__airtable__get_record`
- **baseId**: `appNCMjJ2yMKUrTbo`
- **tableId**: `tblU6ek43LMSNgFj8`
- **recordId**: the linked ID

Fetch in parallel batches of up to 10 to balance speed and API load.

### Client-Side Filtering

**Include** a session if ALL are true:
- `Start Date` >= today (UTC)
- `Start Date` <= today + 28 days
- `Status` is NOT one of: Cancelled, Completed, Cancelled - Need to postpone, Cancellation - Fee, Penalty Fee
- `Provider` is NOT one of: Holiday, Instructor Not Available, Schedule Hold

**Exclude** anything that doesn't meet all inclusion criteria.

### Fields to Capture Per Session

| Field | Notes |
|-------|-------|
| `Start Date` | Delivery-local datetime (see "CRITICAL: Airtable Date Handling" above) |
| `End Date` | Delivery-local datetime (same caveat) |
| `Timezone` | Delivery timezone (map to IANA — required to interpret Start/End Date correctly) |
| `Modality` | Virtual / Onsite / Hybrid / Customer |
| `Status` | Current session status |
| `Projects` | Course name |
| `Training Type` | Private / Public / Conference / etc. |
| `Company Name` | Customer name |
| `Onsite Location` | Physical location (lookupValues) |
| `Location Address` | Full address for onsite |
| `ILT Duration (Days)` | Number of days |
| `Instructor Led Training / Project Name` | Full display name |
| `Instructor + TA Assignments` | Co-instructor references |

### No Sessions Found

If no sessions match the filter:
> "No upcoming sessions found for [name] in the next 4 weeks."

Still display the instructor profile summary — it may be useful on its own.

---

## Step 4: Collision Detection

Compare every pair of sessions (i, j) where i != j. Use `python3 -c` for date arithmetic.

**First, convert all session times to true UTC** by parsing each Start/End Date as delivery-local and converting. See "CRITICAL: Airtable Date Handling" section. For sessions without a Timezone field (Travel, Internal Work blocks), treat the stored time as UTC.

### 4a: Direct Time Overlap

Two sessions overlap when:
```
session_i.start_utc < session_j.end_utc AND session_j.start_utc < session_i.end_utc
```

This naturally handles multi-day sessions since we compare the full start-to-end range.

**Severity:**
- **CRITICAL** — Both sessions have Status = Confirmed (or Confirmed - FULL, Confirmed - DAR, Confirmed - Lab Extension)
- **WARNING** — One or both are Tentative, Proposed, NEW, or Create/Update Session
- **INFO** — One or both are Waiting for roster

### 4b: Same-Day Insufficient Gap

If two sessions fall on the same calendar day in the **instructor's home timezone** but don't technically overlap in UTC:
- Flag if the gap between `session_i.end` and `session_j.start` (or vice versa) is less than 2 hours
- Extra note if the two sessions have different delivery timezones

### 4c: Adjacent-Day Travel Conflict

If two sessions are on consecutive calendar days (in home TZ) AND:
- Both have `Modality` = "Onsite" or "Hybrid"
- They have DIFFERENT `Onsite Location` values

Flag as a travel conflict — the instructor would need to travel between locations overnight.

**Severity:** CRITICAL if both Confirmed, WARNING otherwise.

---

## Step 5: Skills Validation

The instructor's `Approved Courses` field contains **linked record IDs** from the Instructor Skills & Credentials table (`tblaVtSE8BjLH0x7b`), not course names. You must resolve these to get matchable course names.

### 5a: Resolve Approved Course Names

Fetch the instructor's skill records from the Instructor Skills table. Use `mcp__airtable__list_records` with a filter for this instructor:

- **Tool**: `mcp__airtable__list_records`
- **baseId**: `appNCMjJ2yMKUrTbo`
- **tableId**: `tblaVtSE8BjLH0x7b`
- **filterByFormula**: `{Instructor Email} = 'INSTRUCTOR_EMAIL_HERE'`

If the result set is too large or the filter fails, fall back to fetching individual records by ID from the `Approved Courses` array (batch of 10 at a time), but only fetch enough to cover the courses needed for matching (deduplicate against the session `Projects` values first).

### 5b: Extract Course Names

From each resolved skill record, capture:

| Field | Use |
|-------|-----|
| `Session Mapping (from Course Name)` | **Primary match field** — maps to the parent training stream (e.g., "Data Engineering with Databricks") which aligns with the ILT Schedule `Projects` field |
| `Course Name` | Linked record — the specific course variant |
| `Status` | Only count skills where Status is "Approved", "Approved - FULL COURSE", "Approved - HALF-DAY COURSE", or "Achieved Certification" |
| `Active? (from Instructor)` | Verify instructor is still active for this skill |

Build a set of approved course names from the `Session Mapping (from Course Name)` values.

### 5c: Match Sessions Against Approved Courses

For each teaching session, compare its `Projects` field against the resolved set of `Session Mapping` values:

1. Normalize both values: lowercase, strip leading/trailing whitespace
2. Check for exact match first, then substring containment in both directions
3. **Skip** validation for sessions where `Projects` is one of: "Field Enablement", "Internal Work", "Travel", "HOLD", "DAIS", "Holiday", "Instructor Not Available", "Schedule Hold" — these are blocks/events, not courses requiring certification
4. **Skip** validation if no skill records were resolved — note this in the output instead of flagging every session

### 5d: Onsite Approval Check

If a session has `Modality` = "Onsite" or "Hybrid" AND the instructor's `On-Site Approved` is "No" or empty/null:
- Flag: "Instructor is not approved for onsite delivery but is assigned to onsite session [session name]"

### Output for Gaps

For each unmatched session, flag:
> **SKILLS GAP**: "[Course Name]" not found in Approved Courses

List the instructor's resolved approved course names (from Session Mapping) for reference so the user can verify naming mismatches vs. genuine gaps.

---

## Step 6: Travel Identification

### Flag Onsite/Hybrid Sessions

For every session where `Modality` is "Onsite", "Hybrid", or "Customer":
1. Flag as needing travel booking
2. Include `Onsite Location` and `Location Address`
3. If the session's timezone differs from instructor's `Home Timezone`, add:
   > "Travel required: Instructor based in [home TZ/location] — session at [session location/TZ]"

### Consecutive Onsite at Different Locations

If two onsite/hybrid sessions are within 2 calendar days of each other at different `Onsite Location` values, flag the logistics concern.

---

## Step 7: Timezone Analysis

### Convert All Times

For each session, compute start and end times in:
1. **Instructor's home timezone** (primary display)
2. **Session delivery timezone** (secondary display)

Remember: Airtable dates are delivery-local, NOT UTC. Parse accordingly:

```bash
python3 -c "
from datetime import datetime
from zoneinfo import ZoneInfo
# Step 1: Parse as delivery-local (strip the fake Z)
delivery_tz = ZoneInfo('SESSION_IANA_TZ')
local_dt = datetime.fromisoformat('SESSION_START_HERE'.replace('Z','')).replace(tzinfo=delivery_tz)
# Step 2: Convert to home TZ
home_dt = local_dt.astimezone(ZoneInfo('INSTRUCTOR_IANA_TZ'))
print(f'Home: {home_dt.strftime(\"%a %b %d %I:%M %p %Z\")}')
print(f'Delivery: {local_dt.strftime(\"%a %b %d %I:%M %p %Z\")}')
"
```

### Onsite Sessions: Instructor IS in the Delivery Timezone

For sessions where `Modality` is "Onsite" or "Hybrid", the instructor travels to the delivery location. In this case:
- The instructor's home timezone is **irrelevant** for that session — they are physically in the delivery timezone
- Display the delivery timezone as the primary time (not home TZ)
- In the calendar, show the delivery timezone for both columns and note "(onsite — instructor is local)"
- The unusual-hours check should compare against the **delivery** timezone, not home TZ, for onsite sessions
- Collision detection between an onsite session and a virtual session should still use true UTC for overlap comparison

### DST Transition Check

Check if any session date falls within 7 days of a DST transition for either the instructor's home TZ or the delivery TZ. Use python3:

```bash
python3 -c "
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
tz = ZoneInfo('America/New_York')
session_date = datetime.fromisoformat('SESSION_DATE_HERE').replace(tzinfo=tz)
for delta in range(-7, 8):
    check = session_date + timedelta(days=delta)
    offset_before = check.utcoffset()
    offset_after = (check + timedelta(days=1)).utcoffset()
    if offset_before != offset_after:
        print(f'DST transition on {check.date()} in {tz}')
"
```

If found, flag:
> "DST transition on [date] affects [timezone]. Verify session start times are correct."

### Unusual Hours Check

**Virtual sessions** — the instructor delivers from their home timezone. Check both perspectives:

1. **Instructor perspective**: If the session's start or end time in the instructor's **home timezone** falls between 10:00 PM and 6:00 AM, flag:
   > "Session [name] runs [time range] in your home timezone ([home TZ]) — very early/late for you."

2. **Delivery perspective**: If the session's start or end time in the **delivery timezone** falls outside normal business hours (before 7:00 AM or after 7:00 PM delivery-local), flag:
   > "Session [name] runs [time range] in delivery timezone ([delivery TZ]) — unusual hours for attendees."

3. **Cross-timezone stretch**: If the offset between home TZ and delivery TZ is >= 5 hours, flag as informational:
   > "Session [name] spans a [X]hr timezone gap ([home TZ] → [delivery TZ])."

**Onsite sessions** — the instructor is physically in the delivery timezone. Only check delivery-local hours (item 2 above). Home TZ is irrelevant.

---

## Output Format

Present the output in this exact order. Use the instructor's home timezone for all displayed times.

### 1. Header

```
# Schedule Audit: [Instructor Name]
**Generated**: [current date/time in home TZ]
**Home Timezone**: [Airtable value] ([IANA ID])
**Audit Window**: [start] — [end] (4 weeks)
**Sessions Found**: [count]
```

### 2. Instructor Profile

| Field | Value |
|-------|-------|
| Email | [email] |
| Home Timezone | [value] |
| Home Location | [Location field value] |
| On-Site Approved | Yes/No |
| Teaching Timezones | [comma list] |
| Certifications | [comma list] |
| Approved Courses | [resolved course names from Step 5, comma-separated] |

### 3. Flags Summary

Show this section BEFORE the calendar so issues are immediately visible.

#### Collisions

| Severity | Type | Session A | Session B | Details |
|----------|------|-----------|-----------|---------|
| CRITICAL | OVERLAP | [name, date] | [name, date] | Both confirmed, [overlap window] |
| WARNING | GAP | [name, date] | [name, date] | Only [X]hr gap between sessions |

If none: "No scheduling collisions found."

#### Skills Gaps

| Session | Date | Course | Issue |
|---------|------|--------|-------|
| [name] | [date] | [Projects value] | Not in Approved Courses |

If none: "All sessions match approved courses."

#### Travel Needs

| Session | Date(s) | Location | Notes |
|---------|---------|----------|-------|
| [name] | [dates] | [location] | Different from home base / Consecutive onsite |

If none: "No onsite sessions requiring travel."

#### Timezone Alerts

| Session | Date | Alert |
|---------|------|-------|
| [name] | [date] | DST transition on [date] in [TZ] |
| [name] | [date] | Runs 5:00 AM - 1:00 PM in home TZ |

If none: "No timezone concerns."

### 4. Four-Week Calendar

For each week, show:

```
## Week of [Mon date] — [Sun date]
```

| Day | Time (Home TZ) | Time (Delivery TZ) | Course | Customer | Modality | Status | Flags |
|-----|----------------|---------------------|--------|----------|----------|--------|-------|
| Mon Mar 2 | 9:00 AM - 5:00 PM EST | 9:00 AM - 5:00 PM EST | DE Associate | Acme Corp | Virtual | Confirmed | |
| Tue Mar 3 | 8:00 AM - 4:00 PM EST | 7:00 AM - 3:00 PM CST | ML Prof | Beta Inc | Onsite | Tentative | TRAVEL, SKILLS |

If a week has no sessions: "No sessions this week."

For multi-day sessions, show a row for EACH day of the session with the same course/customer info.

### 5. Footer

```
---
*Source: Airtable Training Operations base (real-time).*
*Virtual sessions: times shown in instructor home TZ with delivery TZ noted.*
*Onsite sessions: times shown in delivery TZ (instructor travels to location).*
*Airtable dates are delivery-local (NOT true UTC despite the Z suffix). All conversions account for this.*
*Included statuses: Confirmed, Tentative, Waiting for roster, Create/Update Session, NEW, Proposed*
*Excluded: Cancelled, Completed, Holiday, Instructor Not Available, Schedule Hold*
```

---

## Error Handling

- **Airtable API errors**: Report the error, continue with available data. Do not abort the full audit for one failed fetch.
- **Missing fields**: Include the session in the calendar but note missing data (e.g. "TZ: unknown").
- **Unknown timezone values**: Log in footer, use UTC as fallback, and still show the raw Airtable value.
- **Rate limiting**: If Airtable returns errors on batch fetches, reduce batch size and retry.
