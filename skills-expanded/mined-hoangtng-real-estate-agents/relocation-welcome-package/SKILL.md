---
name: relocation-welcome-package
description: Create a personalized relocation welcome package for clients moving into a new city or neighborhood. Use this skill whenever a user asks to create a welcome guide, neighborhood orientation, relocation packet, newcomer guide, or "what to tell a client who's moving here." Also use when a buyer is relocating from out of state and needs community context, school information, vendor referrals, or a first-week logistics checklist. Produces a hyper-specific, locally-grounded welcome package — not a generic city overview.
---

# Relocation Welcome Package

Produces a personalized, locally-specific welcome package for relocating clients. This is Claire's work: specificity is the service. "Great restaurants nearby" is not a deliverable — naming the chef and what to order is.

## What You Need From the User

- **Client profile:** name(s), family composition (kids' ages, pets), lifestyle interests, where they're coming from
- **Destination:** city, neighborhood, specific address if known
- **Motivation:** job transfer / lifestyle / family / retirement / investment
- **Timeline:** move-in date or target range
- **Priorities:** schools / commute / walkability / social scene / specific needs

The more detail provided, the more personalized the package. If details are sparse, generate a strong template with `[PERSONALIZE: ...]` callouts.

## Output Format

```markdown
# Welcome to [Neighborhood], [City] 🏡
*A personal guide prepared for [Client Name(s)] by Claire, Concierge & Relocation Specialist*
*Prepared: [Date] | Move-in target: [Date]*

---

## Your New Neighborhood: [Name]

**The character in a few sentences:**
[Authentic 3–4 sentence description — NOT from a website. The feel of the street, the kind of people who live here, what makes it distinct from neighboring areas. If you don't have this information, write: "PERSONALIZE: Add authentic neighborhood character description here — walk the street, talk to the listing agent."]

**Walkability:** [Score if known] — You can walk to: [list actual walkable destinations]
**Best time to be outside:** [Specific: farmers market on Saturday morning, sunset walks along X, etc.]
**The insider thing:** [One local thing that isn't on any list — a specific park bench, a back-door coffee situation, a neighborhood tradition]

---

## Schools
*[If no children: skip this section or note "Available on request"]*

### Elementary
**[School Name]**
- Enrollment: [X] students | Type: [Public / Magnet / Charter]
- What parents love: [specific — the principal is exceptional, strong arts program, etc.]
- One honest note: [any caveat worth knowing]
- Registration: [district website + what documents to bring]

**[Alternative Option]**
- [Same format]

### Middle School
**[School Name]**
- [Highlights: sports / STEM / arts — what this school is known for]
- [College placement or notable outcomes if relevant]

### High School
**[School Name]**
- [AP offerings, sports, graduation rate, notable programs]

### Private Options (if applicable)
- **[School Name]:** [Philosophy, tuition range, waitlist reality]

---

## Healthcare

| Type | Provider | Practice | Phone | Notes |
|------|----------|----------|-------|-------|
| Family / Primary Care | [Name] | [Practice] | [Phone] | Accepting new patients ✅ |
| Pediatrics | [Name] | [Practice] | [Phone] | [Note] |
| Urgent Care (closest) | [Name] | [Address] | [Phone] | Walk-in hours: [X] |
| Hospital (best for emergencies) | [Name] | | [Phone] | [Specialty strength] |
| Dentist | [Name] | [Practice] | [Phone] | Family-friendly |

*[Note: Always confirm "accepting new patients" status before including — this changes frequently. Mark unconfirmed entries with ⚠️]*

---

## Everyday Logistics

| Category | Name | Distance | Notes |
|----------|------|----------|-------|
| Grocery (everyday) | [Name] | [X] min | Best for: [items] |
| Grocery (specialty/organic) | [Name] | [X] min | [What makes it worth the trip] |
| Pharmacy | [Name] | [X] min | Drive-through: Y/N |
| Hardware / Home | [Name] | [X] min | |
| Dry Cleaning | [Name] | [X] min | Fast turnaround |
| Post Office | [Address] | [X] min | Hours: [X] |
| Library | [Name] | [X] min | [Notable programs] |

---

## Dining & Gathering

*Not a Yelp list — places worth your time*

**Weekend breakfast / brunch:**
[Name] — [2 sentences: why, what to order, any logistics like "cash only" or "arrive before 10am"]

**Date night:**
[Name] — [why, make a reservation, price range]

**Casual weeknight:**
[Name] — [why, kid-friendly Y/N, parking situation]

**Best coffee + work:**
[Name] — [wifi quality, outlet availability, vibe, best seat in the house]

**Neighborhood bar / gathering spot:**
[Name] — [the vibe, who goes there, best night to go]

**The place locals take out-of-towners:**
[Name] — [brief explanation]

---

## Getting Around

**Daily commute to [employer/destination]:**
- By car: [X] min at [peak time] via [route] | Parking at destination: [notes]
- By transit: [option, line, duration, cost]
- By bike: [X] min — [route quality note]

**Airport:**
- [Airport name]: [X] min | Best terminal for [airline]: [X]
- Parking: [Lot / App recommendation]
- Rideshare pickup: [Terminal / location note]

**Parking in your area:**
[Street parking rules, permit zones, garage options — anything non-obvious]

---

## Community & Social

**[Interest-specific — PERSONALIZE based on client profile]**

- Neighborhood association: [Name] | Meets: [frequency] | How to join: [link/contact]
- [Sports league / fitness class / running club relevant to client]: [Name + contact]
- [Kids activity / parent group if applicable]: [Name + contact]
- [Cultural / arts / hobby group if relevant]: [Name + contact]
- Farmers market: [Day, location, hours] — go early for [specific item]

---

## First-Week Logistics Checklist

### Must-Do in Week 1
- [ ] **Driver's license:** [State DMV location] | Hours: [X] | Bring: [list]
- [ ] **Vehicle registration:** Due within [X] days | [Process + link]
- [ ] **Voter registration:** [Online link — takes 5 minutes]
- [ ] **Utilities:** Electric: [Provider + signup link] | Gas: [Provider] | Water: [note if included]
- [ ] **Internet:** [Provider options for this address] — [who installs fastest]
- [ ] **USPS change of address:** [usps.com/move — do this before you move if possible]
- [ ] **Schools enrollment:** [District portal link + what to bring]
- [ ] **Pet registration** (if applicable): [City/county requirement + link]

### Nice to Do in Month 1
- [ ] Explore [specific neighborhood feature — trail, market, district]
- [ ] Introduce yourself to [neighbor context — block association, building, etc.]
- [ ] Find your [gym / yoga studio / running route]
- [ ] [PERSONALIZE: one specific thing based on their stated interests]

---

## Your Concierge Contact

**Claire** — Concierge & Relocation Specialist
[Phone] | [Email]

*I'll check in with you one week after move-in. Text me anytime before then — no question is too small. If something on this list is wrong or outdated, I want to know.*

*And if you know anyone else who might be making a move — to or from this area — I'd be honored to help them too.*
```

## Behavior Notes

- **Specificity over completeness.** A package with 5 specific, accurate, locally-grounded recommendations is worth more than 20 generic ones.
- **Always personalize to the client's stated interests.** A couple with a toddler gets a different package than a retiring couple. A remote worker cares about the coffee shop wifi. A runner wants the trail.
- **Mark anything unverifiable.** Use `⚠️ [Verify before sending]` for anything like "accepting new patients" or hours that may have changed.
- **The "insider thing" is the most valuable line in the package.** Push yourself to find it — or if you can't, use `[PERSONALIZE: Ask the listing agent or a local — this is the line that makes the package feel real]`.
- If user says "make it shorter": cut the dining section in half and collapse logistics into a bulleted checklist. Keep the neighborhood character paragraph and the first-week checklist.
- Always close with Claire's contact note — the package is a relationship tool, not just an information dump.
