---

name: owner-skip-trace
description: owner-skip-trace lets the user start from a property or owner name and identify the most likely current owner contact details, including phones, emails, mailing addresses, and related people or entity clues, so they can go from raw property lead to direct-owner outreach with less guesswork and fewer dead ends.
category: openclaw-imports

---
**Find phone numbers, emails, social media profiles, and business records for property owners using only free public web sources. No paid databases (TLO, LexisNexis) required.**

## What This Skill Does

This skill owner-skip-trace lets the user start from a property or owner name and identify the most likely current owner contact details, including phones, emails, mailing addresses, and related people or entity clues, so they can go from raw property lead to direct-owner outreach with less guesswork and fewer dead ends.

## When to Use
- After you have an owner's name from LandGlide, SDAT, Rentcast, or public records
- User wants contact info for a property owner
- User says "skip trace" or "find their phone number"

## Workflow

### Step 1: Normalize the Owner Name
LandGlide returns names like "STATON DERRELL" — convert to "Derrell Staton" for better search results. If you have a middle name/initial from other sources, use it too (e.g., "Derrell A Staton").

### Step 2: Run 3 Parallel Web Searches
Run these simultaneously for best coverage:

```
Search 1 (Contact): "OWNER_NAME" CITY STATE phone email
Search 2 (Social):  "OWNER_NAME" ADDRESS STREET_NAME CITY social media
Search 3 (Records): "OWNER_NAME" CITY STATE property records contact
```

**Pro tip:** If the owner has an uncommon last name, you'll get clean results. If it's "Smith" or "Johnson," add more specificity like street name or business name.

### Step 3: Extract Details from Promising Results
For each URL that looks like it has contact data, run web_extract:

```
web_extract(urls: [promising_url_1, promising_url_2, ...])
```

**Best sources (in order of usefulness):**
1. **RocketReach.com** — Phone numbers + emails. Snippet often shows partial numbers. Full details need login but the search hit confirms the person exists.
2. **FMCSA / DOT carrier records** (e.g., newbizbot.ai) — If the owner has a trucking/logistics business, phone numbers and emails are FULLY visible. This is a goldmine.
3. **LinkedIn** — Professional profile with work history, sometimes email visible. URL format: linkedin.com/in/[slug]
4. **Facebook** — Personal profile or business page. Sometimes phone/email listed.
5. **State business registry** — If they own an LLC/Corp, officer name and registered agent address are public.
6. **CyberBackgroundChecks / Spokeo / TruePeopleSearch** — Confirm name/phone/address match. Free tier shows partial data but enough to confirm.
7. **Voter records** — Some states publish voter registration with address and sometimes DOB.
8. **Court records** — County clerk searches show lawsuits, liens, evictions — all public and often include phone numbers.

### Step 4: Cross-Reference and Verify
- If multiple sources show the same phone number (e.g., RocketReach partial + FMCSA full = match), mark it as **confirmed**.
- If a source contradicts another (different phone for same person), flag as **unconfirmed**.
- If the owner has a business at a different address than the property, note both.

### Step 5: Compile the Contact Card
Format the output as:

```
OWNER FULL NAME, Age [if found]
Property: [address from records]

PHONE NUMBERS:
- (XXX) XXX-XXXX — confirmed active [source]
- (XXX) XXX-XXXX — unconfirmed [source]

EMAIL:
- name@domain.com — business [source]
- name@gmail.com — personal [source]

SOCIAL MEDIA:
- LinkedIn: linkedin.com/in/[profile]
- Facebook: facebook.com/[profile]
- [any others]

BUSINESS AFFILIATIONS:
- Company name, role, status (Active/Dissolved)
- DOT/EIN if applicable

ASSESSMENT:
[1-3 sentences: owner-occupied vs investor, purchase date vs current value, equity position, any red flags or motivators]
```

## Important Notes
- This method is **FREE** — no paid database subscriptions needed
- It won't always find everything — common names or very private individuals may have limited results
- FMCSA/DOT business records are the single best free source when the owner has a trucking or logistics business
- Always verify that the person found actually matches the property owner (same city, similar address pattern, matching business records)
- Do NOT fabricate phone numbers or emails — if you can't find it, say so
- This is public data only — all info is from publicly accessible records and profiles

## Example: Derrell Staton — 944 N Hill Rd, Baltimore MD

**Owner from LandGlide:** STATON DERRELL

**Search 1:** "Derrell Staton Baltimore MD phone email"
→ RocketReach match: Director at Military Prep Center
→ FMCSA match: DOT #3336094, phone (443) 418-8929

**Search 2:** "Derrell Staton Hill Road Baltimore social media"
→ LinkedIn: linkedin.com/in/derrell-staton-8596b8a1
→ Facebook: facebook.com/militaryprepcenter

**Search 3:** "Derrell Staton Baltimore property records contact"
→ CyberBackgroundChecks: Derrell A Staton, Age 45, Baltimore MD

**Result compiled into contact card with confirmed phone, email, LinkedIn, business info, and assessment.**
