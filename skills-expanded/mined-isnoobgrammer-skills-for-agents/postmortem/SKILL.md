---
name: postmortem
description: >-
  Runs the full postmortem workflow: gathers incident context, writes a blameless report to a
  gitignored `postmortem/` folder, and creates action items. Use whenever the user wants to review
  or document any production incident or outage. Triggers on: '/postmortem', 'write a postmortem',
  'incident review', 'post-incident', 'blameless review', 'what broke and why', 'SEV1/SEV2
  report', or 'help me write up what happened'.
domain: process
composable: true
yields_to: []
---

# Postmortem Skill

No blame. No drama. Just: what broke, why, what we do next.

Real postmortems are hard to write coz engineers are tired after incidents and want to move on.
This skill forces the structure so your 3am brain doesn't skip the root cause and call it done.

---

## When to Use

- `/postmortem`
- "write a postmortem"
- "incident review" / "post-incident"
- SEV1 / SEV2 / SEV3 — any severity label near "report" or "review"
- "what broke and why"
- "we had an outage"
- "production incident"
- "blameless review"
- "help me document the incident"

---

## STEP 0: Before Anything

**Do this first. Always.**

```bash
# Create postmortem root folder if not exists
mkdir -p postmortem

# Add to .gitignore (postmortems can have sensitive blast radius / customer impact data)
if ! grep -qxF 'postmortem/' .gitignore 2>/dev/null; then
  echo 'postmortem/' >> .gitignore
  echo "added postmortem/ to .gitignore"
fi
```

If no `.gitignore` exists, create one with `postmortem/` as first entry.

Each incident gets its own subfolder inside `postmortem/`:
```
postmortem/
└── YYYY-MM-DD-<slug>/
    ├── index.html          # Main report (entry point)
    ├── timeline.html       # Detailed timeline with visualizations
    ├── root-cause.html     # 5 Whys deep dive + system diagrams
    ├── action-items.html   # Action item tracker with status
    ├── assets/
    │   ├── style.css       # Shared dark-theme stylesheet
    │   └── charts.js       # Chart.js config
    └── data/
        └── incident.json   # Raw structured data (machine-readable backup)
```

---

## STEP 1: Gather Context

Ask user for these. Be direct, not a form. One shot:

**Required:**
- Incident title (short, descriptive — not "Production Issue")
- Severity (SEV1 / SEV2 / SEV3 / SEV4)
- Date + time of incident (UTC preferred)
- Duration
- What broke (user-facing impact, one sentence)
- Root cause (even rough — will refine)
- Who was on-call / who responded

**Optional but valuable:**
- Timeline (can be rough, will format it)
- Metrics (error rate, affected users, revenue loss)
- Action items already identified
- Related past incidents

If user gives a wall of text / Slack dump / runbook notes — parse it. Extract the structure. Don't make them re-type.

---

## STEP 2: Generate the Report

Folder: `postmortem/YYYY-MM-DD-<slug>/`

Slug = lowercase kebab-case of incident title.
Example: `postmortem/2024-01-15-payment-service-db-pool-exhaustion/index.html`

### HTML Report Requirements

Every postmortem report MUST be a **visually polished, self-contained HTML document**. The goal: a report that looks like a professional incident dashboard — scannable, visual, not a text wall.

#### Design Rules

1. **Dark theme** — dark background (#0d1117), light text (#e6edf3), severity accent colors: red=SEV1, orange=SEV2, yellow=SEV3, blue=SEV4.
2. **Impact stat cards at top** — severity badge, duration, users affected, revenue impact, time to detect, time to resolve — in a prominent card row.
3. **No walls of text** — use tables, badges, cards, collapsible sections (`<details>`), and visual hierarchy. Every section should scan in <5 seconds.
4. **Charts for data** — use Chart.js (CDN: `https://cdn.jsdelivr.net/npm/chart.js`) for: incident timeline (line chart with annotated events), error rate over time (area chart), impact breakdown (doughnut). Inline the config in a `<script>` tag.
5. **Severity badges** — color-coded: `SEV1` (red), `SEV2` (orange), `SEV3` (yellow), `SEV4` (blue). Prominent in header.
6. **Visual timeline** — the timeline is NOT just a table. Use a vertical timeline component with colored dots (red=detection, yellow=mitigation, green=resolution), timestamps, and event descriptions. CSS-based, no external deps.
7. **5 Whys visualization** — render as a cascading card chain, not a table. Each "Why" card connects to the next with an arrow/line. Color deepens as you go deeper (light yellow -> dark orange -> red for root cause).
8. **System diagram** — use CSS/SVG to show the affected system flow. Boxes for services, arrows for data flow, red highlight on the failure point. Replace ASCII art with actual visual diagrams.
9. **Action item cards** — each action item gets its own card with priority badge (P0=red, P1=orange, P2=yellow), owner avatar placeholder, due date, and status indicator.
10. **Responsive** — works on desktop and mobile.
11. **Self-contained** — all CSS inline or in `assets/style.css`. System fonts stack. Chart.js is the only allowed CDN dependency.
12. **Print-friendly** — include `@media print` rules.

#### CSS Theme (assets/style.css)

```css
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-card: #21262d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --border: #30363d;
  --accent-green: #3fb950;
  --accent-yellow: #d29922;
  --accent-red: #f85149;
  --accent-orange: #db6d28;
  --accent-blue: #58a6ff;
  --accent-purple: #bc8cff;
}
```

#### index.html Structure

- **Header**: incident title, severity badge, status badge (Draft/Reviewed/Actioned), report date
- **Impact stat cards row**: severity | duration | users affected | revenue impact | TTD | TTR
- **TL;DR card**: one-paragraph summary in a highlighted box with severity-colored left border
- **Visual timeline**: vertical timeline with colored event markers
- **System diagram**: CSS/SVG diagram of affected flow with failure point highlighted
- **Key findings**: root cause summary in a cascading card chain
- **Action items preview**: top 3 P0 items as cards, link to full list
- **Navigation**: links to `timeline.html`, `root-cause.html`, `action-items.html`

#### Supporting Pages

- **timeline.html**: Full detailed timeline with every event. Chart.js line chart showing error rate over time with annotated incident milestones. Expandable event details.
- **root-cause.html**: Full 5 Whys as cascading cards. System context diagram (detailed). Detection and response analysis. Lessons learned cards (went well / went wrong / got lucky).
- **action-items.html**: Complete action item tracker. Sortable table with priority, owner, due date, status, ticket link. Priority breakdown chart (doughnut).

#### Data Backup (data/incident.json)

```json
{
  "title": "incident title",
  "severity": "SEV1|SEV2|SEV3|SEV4",
  "date": "YYYY-MM-DD",
  "duration": "duration",
  "impact": {"users_affected": 0, "revenue_impact": "", "data_loss": false, "security_implications": false},
  "timeline": [{"time": "HH:MM", "event": "...", "type": "detection|mitigation|resolution|other"}],
  "root_cause": {"primary": "", "contributing": []},
  "five_whys": [{"question": "", "answer": "", "evidence": ""}],
  "detection": {"time_to_detect_min": 0, "detected_by": "", "worked": [], "failed": []},
  "response": {"time_to_resolve_min": 0, "responders": [], "worked": [], "could_be_faster": []},
  "lessons": {"went_well": [], "went_wrong": [], "got_lucky": []},
  "action_items": [{"priority": "P0|P1|P2", "action": "", "owner": "", "due": "", "ticket": ""}]
}
```

Use this JSON as the data backbone. Every HTML page reads from this structure. If the HTML ever needs regeneration, the JSON has everything.

---

## STEP 3: Review Pass

Before saving, check:

- [ ] No person blamed. System blamed. Always system.
- [ ] Timeline has no gaps > 10 min without explanation — because gaps hide decision points and make the timeline unreliable for root cause analysis
- [ ] 5 Whys went deep enough (if Why 3 is still a person's mistake, go deeper)
- [ ] Every action item has an owner. No orphan actions.
- [ ] "Got lucky" section is honest. If you didn't get lucky, say so.
- [ ] TL;DR is actually a TL;DR (< 100 words) — because a TL;DR longer than that is a summary, not a TL;DR — executives won't read it

---

## STEP 4: Save and Confirm

Create the full folder structure:

```bash
SLUG="YYYY-MM-DD-incident-slug"
mkdir -p "postmortem/$SLUG/assets"
mkdir -p "postmortem/$SLUG/data"

# Write all HTML files (index.html, timeline.html, root-cause.html, action-items.html)
# Write assets/style.css and assets/charts.js
# Write data/incident.json

echo "postmortem saved: postmortem/$SLUG/"
echo "entry point: postmortem/$SLUG/index.html"
echo "gitignored: yes"
```

Tell user:
1. Folder location and that `index.html` is the entry point
2. That it's gitignored (so sensitive impact data stays local)
3. Suggest next: share in incident channel, create tickets for P0s
4. All supporting pages (timeline, root-cause, action-items) are linked from index.html

---

## Blameless Culture — the 30 second version

Blame shuts down learning. When someone makes a mistake in a system, the question is never *who* — it's *what conditions let this happen*. Fix the conditions.

| Don't say | Say instead |
|-----------|-------------|
| "Alice pushed broken code" | "The deploy lacked a canary stage" |
| "Bob missed it in review" | "The review checklist didn't cover infra changes" |
| "On-call was slow" | "Alert threshold was too high to fire early" |

The goal: next engineer in same situation succeeds. Not: next engineer is scared.

---

## Triggers Reference

See the "When to Use" section above for the full list of trigger phrases.

---

## Edge Cases

**"It was a minor incident"** — still write it. SEV3s reveal patterns SEV1s don't.

**"I don't know the root cause yet"** — write what you know. Mark root cause section as `[INVESTIGATION IN PROGRESS]`. Revisit.

**"It was a third-party issue"** — still write it. Root cause = vendor. Action items = better circuit breakers, fallbacks, SLA review.

**"We fixed it, no action items needed"** — wrong. There's always at least one. "Monitor X metric" counts.

**"I just want the template"** — skip to Step 2, dump the template, let them fill it. Still do Step 0 (mkdir + gitignore).

---

## Files Created by This Skill

```
postmortem/                           # gitignored, auto-created
└── YYYY-MM-DD-<slug>/               # per-incident folder
    ├── index.html                    # main report (entry point)
    ├── timeline.html                 # detailed timeline + charts
    ├── root-cause.html               # 5 whys + system diagrams
    ├── action-items.html             # action item tracker
    ├── assets/
    │   ├── style.css                 # dark theme stylesheet
    │   └── charts.js                 # Chart.js configurations
    └── data/
        └── incident.json             # raw structured data backup
.gitignore                            # updated with postmortem/ entry
```

That's it. No extra config. No setup. Just: incident happens -> run skill -> folder exists with visual HTML report -> tickets exist -> done.

---

## Boundaries

- Does not track action items after creation (defers to project management tools)
- Does not replace incident response or on-call tooling
- Does not handle legal, compliance, or regulatory reviews
- Does not assign blame or evaluate individual performance

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []  # process owns structure — nobody overrides it
```

Postmortem owns **process** — the workflow, template, required sections, review checklist, file structure. The skeleton is sacred.

### When Postmortem Leads

- Any incident documentation request
- When structured blameless analysis is needed
- SEV reports, outage reviews, failure documentation

### When Postmortem Defers

| Other Skill's Domain | What Postmortem Does |
|---------------------|-------------------|
| **Voice** (e.g. personality/tone) | Postmortem provides the structure and required content. Voice skills fill it with personality. The timeline table still has precise times. The 5 Whys still go 5 deep. But the prose in "What happened" and "Lessons" sections can carry voice. |
| **Density** (e.g. compression) | After the report is generated, density skills can compress it. Postmortem generates the full report first — never skip sections for brevity. Compression is a post-processing step. |
| **Craft** (e.g. design/UI expertise) | If the incident involved UI/UX issues, invite craft skills to fill the technical analysis sections. Postmortem provides the section header and context; the craft skill provides the design-specific diagnosis. |

### Layered Composition Rules

1. **Process + Voice**: Structure first, voice second. Every required section exists. Every required field is filled. Voice applies WITHIN sections, never restructures them. The "Got lucky" section written in a casual voice is still a "Got lucky" section with honest content.

2. **Process + Density**: Pipeline pattern. Postmortem generates full report → density skill compresses it. The density skill must preserve: all section headers, table structures, required fields, timeline entries. Compress only the prose in description paragraphs.

3. **Process + Craft**: If the incident was UI-related, the "Root Cause" and "System context" sections benefit from craft skill analysis. Postmortem provides the section; craft fills the technical details (what broke visually, what heuristic was violated, what the fix should be).

4. **Process + Voice + Density (triple layer)**: Postmortem provides structure → voice fills sections with personality → density compresses the result. This is the full pipeline. Output: a postmortem report that sounds like the author, is compressed for storage, but has every required section.

### Pipeline Behavior

- **Upstream** (receives content from another skill): Rare. Postmortem usually starts from raw user input. But if another skill pre-processed incident data (e.g., a craft skill already diagnosed a UI regression), incorporate that analysis into the appropriate section.
- **Downstream** (postmortem output goes to another skill): Common. Report → compress (density), report → blog post (voice + content), report → UI audit (craft). Postmortem's structured output is designed to be machine-readable and skill-parseable.

### Handoff Patterns

Postmortem naturally leads to other skills:

```
postmortem → blogger
  "Write a blog post about what we learned from this incident"
  Postmortem provides the facts. Blogger provides the voice.
  
postmortem → compress
  "Compress the postmortem for the knowledge base"
  Full report → compressed version. Structure preserved.

postmortem → painter (advisory)
  "The incident was a CSS regression — what exactly broke?"
  Painter fills the technical analysis. Postmortem owns the structure.
```

### Conflict Signal

If another skill tries to modify postmortem's structure:

> `⚠️ Process conflict: postmortem structure is fixed. [Skill X] attempting to [merge sections / skip required fields / restructure template]. Preserving structure, applying [Skill X] within sections only.`