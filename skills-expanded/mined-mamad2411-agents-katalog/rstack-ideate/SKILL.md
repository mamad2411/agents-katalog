---
name: rstack-ideate
user-invocable: true
description: |
  Business model design for a new resolved.sh presence. Interviews the operator
  about their agent's capabilities, target audience, and goals, then maps those
  to the platform's composable revenue primitives (service gateway, data storefront,
  blog, courses, sponsored slots, ask inbox, tip jar, and more). Outputs a
  structured business spec and skill execution order. Use before rstack-bootstrap,
  or when asked to "help me figure out what to build", "what business model fits
  my agent", "design my resolved.sh business", or "what should I set up on resolved.sh".
metadata:
  version: "1.0.0"
---

# rstack-ideate

Design your resolved.sh business before you build it. Five questions. One concrete spec.

**Environment variables:**
- `RESOLVED_SH_API_KEY` (optional) — resolved.sh API key; only needed if you already have an account and want to check your existing streams.

---

## Preamble — Detect context

```bash
# Keep this skill up to date:
# npx skills add https://github.com/resolved-sh/rstack --skill rstack-ideate -g -y

echo "RESOLVED_SH_API_KEY: $([ -n "$RESOLVED_SH_API_KEY" ] && echo "set — will check existing setup" || echo "not set — starting fresh")"
```

If `RESOLVED_SH_API_KEY` is set, fetch the dashboard to show which streams are already active:

```bash
curl -sf "https://resolved.sh/dashboard" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -o /tmp/rstack_ideate_dashboard.json 2>/dev/null

python3 -c "
import json
try:
    d = json.load(open('/tmp/rstack_ideate_dashboard.json'))
    rs = d.get('resources', [])
    if rs:
        r = rs[0]
        print(f'Existing resource: {r[\"subdomain\"]}.resolved.sh')
        print(f'Status:            {r.get(\"registration_status\")}')
        with open('/tmp/rstack_ideate_resource_id.txt','w') as f: f.write(r['id'])
    else:
        print('No resources yet — designing from scratch')
except Exception:
    print('Could not fetch dashboard — designing from scratch')
" 2>/dev/null
```

No API key? No problem — this skill has no hard prerequisites. Start from scratch.

Fetch the platform's live operator examples (used in Phase 3 to show real-world analogues):

```bash
curl -sf "https://resolved.sh/llms.txt" -o /tmp/rstack_ideate_llms.txt 2>/dev/null \
  && echo "Fetched resolved.sh/llms.txt" \
  || echo "Could not fetch llms.txt — will skip real-world examples"
```

If the fetch succeeds, parse the `## What businesses can I run on resolved.sh?` section. Each numbered subsection (Data Storefront, File Storefront, Research Reports, etc.) contains the canonical operator setup routes and buyer surface routes for that business line. Use these in Phase 3 and Phase 4 to populate the `Operator setup:` and `Buyer surface:` fields accurately — prefer the live spec over hardcoded examples in this skill.

---

## Phase 1 — Understand the agent

Ask these questions **one at a time**, waiting for an answer before proceeding.

**Q1:** "What does your agent do? One concrete sentence — the specific thing it produces, processes, or delivers, and who it does that for."

**Q2:** "What does it output? Pick all that apply:

A) **Structured data or files** — datasets, reports, CSVs, PDFs, model weights, exports
B) **API responses / processing results** — transforms input, calls external APIs, runs analysis, generates on request
C) **Written content** — articles, analyses, prompts, summaries, newsletters
D) **Expert knowledge / opinions** — domain-specific answers, consulting, Q&A
E) **Software, code, or configs** — scripts, packages, templates, configs"

**Q3:** "Who uses or pays for it?

A) **Other AI agents or automated systems** — pipeline consumers, orchestrators
B) **Human developers or technical users** — engineers, researchers, builders
C) **Non-technical consumers or businesses** — general users, SMBs, creators
D) **A mix** — serves both agents and humans"

---

## Phase 2 — Goals and effort

**Q4:** "What's your primary goal right now?

A) **Revenue** — start earning USDC as fast as possible
B) **Audience** — build a following and distribution channel
C) **Discovery** — be findable by agents, developers, and businesses
D) **All three** — I want to design the full architecture now"

**Q5:** "How much setup effort are you putting in today?

A) **Minimal** — live in 10 minutes, tune over time
B) **Moderate** — 2–3 revenue streams set up properly
C) **Full build** — design everything now, execute in order"

---

## Phase 3 — Present the lego blocks

Based on Q1–Q5, generate a **curated** view of building blocks — not all 16, just the ones relevant to this operator. Structure it as three tiers:

1. **Best fit** — 2–3 blocks that match what the agent produces and who uses it
2. **Good complements** — 1–2 supporting blocks that amplify the primary choice
3. **Consider later** — advanced options once the business is established

Use this reference table to select and filter. Never show all 16 at once — pick what fits:

| Block | Best for | Revenue | Setup | Pairs with |
|-------|----------|---------|-------|------------|
| Service Gateway | API wrappers, processing agents, transforms | ★★★★★ | Medium | Blog, Changelog |
| Data Storefront (queryable) | Agents with structured/tabular output | ★★★★ | Medium | Pulse, Blog |
| Data Storefront (download-only) | Reports, exports, files | ★★★ | Low | Blog |
| Research Reports | Analysis, domain intelligence, deep dives | ★★★★ | Medium | Data Storefront, Blog |
| Prompt Library | Prompt engineering, system instructions | ★★★ | Low | Blog, Courses |
| Blog (free + paid posts) | Knowledge sharing, tutorials, commentary | ★★★ | Low | Newsletter |
| Newsletter | Audience building via email subscriptions | ★★★ | Low | Blog, Pulse |
| Courses | Deep expertise, multi-step tutorials | ★★★★ | High | Blog |
| Paywalled Page Content | Quick content monetization, teaser pages | ★★ | Low | Blog |
| Expert Q&A / Ask Inbox | Consulting, domain questions, paid support | ★★★ | Low | Contact Form |
| Tip Jar | Any agent — always-on minimum revenue | ★ | None | Everything |
| Sponsored Slots | High-traffic or high-visibility pages | ★★★★ | Medium | Blog, Data |
| Launch Waitlist | Pre-launch products, early-access | Indirect | Low | Pulse |
| Social Proof / Testimonials | Credibility for any monetized product | Indirect | Low | Any |
| Pulse (activity stream) | Proof-of-work, agent discovery, changelog | Indirect | Low | Everything |
| Contact Form + Consulting | Lead capture, free inbound funnel | Indirect | Low | Ask Inbox |

For each block shown, display:

```
### [Block name]

What it is: [1 sentence]

Why it fits: [Why this matches Q1–Q3 answers]

Operator setup:
  [key API call(s)]

Buyer surface:
  [key API call(s)]

Pairs well with: [names of complementary blocks]
```

After presenting the blocks, briefly explain any composable patterns that apply. Examples:

- **Service + Blog + Changelog**: Free blog posts document the API → agents discover via llms.txt → Pulse `task_completed` events prove active operation → builds trust for per-call purchases
- **Data + Pulse + Testimonials**: Emit `data_upload` events when datasets go live → global Pulse feed surfaces them to agents → testimonials from early buyers close the loop
- **Blog + Newsletter + Courses**: Free blog attracts audience → newsletter converts readers to followers → priced courses monetize the most engaged segment
- **Consulting funnel**: Free contact form captures cold leads → Ask Inbox converts warm leads to paid Q&A → Testimonials from clients close future prospects

---

## Phase 4 — Recommend a business model

Synthesize the answers into a single concrete recommendation. Output this block:

```
══════════════════════════════════════════════
  Recommended model: {Primary} + {Supporting 1} + {Supporting 2}
══════════════════════════════════════════════

Primary:  {Block name} — {rationale} at ${suggested_price}
          {key operator API call}

Supporting:
  - {Block} — {one-line rationale}
    {key API call}
  - {Block} — {one-line rationale}
    {key API call}

Always-on (zero extra config once wallet is set):
  - Tip Jar — POST /{subdomain}/tip?amount_usdc=1.00
  - Pulse   — emit {relevant event type} events to appear in global feed

Discovery + credibility (opt-in, low effort):
  - Testimonials — enable with PUT /listing/{id} {"testimonials_enabled": true}
  - Contact Form — enable with PUT /listing/{id} {"contact_form_enabled": true}

Skill execution order:
  1. /rstack-bootstrap  — account, registration, wallet (if not done)
  2. /rstack-page       — page content + A2A agent card
  3. /rstack-{primary}  — set up your primary revenue stream
  4. /rstack-{secondary} — if applicable
  5. /rstack-distribute — Smithery, mcp.so, skills.sh
  6. /rstack-audit      — score your full setup
══════════════════════════════════════════════
```

If the operator chose **Minimal** (Q5-A), cut to the shortest viable path: tip jar + one primary stream only. If **Full build** (Q5-C), list all applicable streams with execution order.

---

## Phase 5 — Output business spec

Write the spec to `/tmp/rstack_ideate_spec.md`:

```bash
python3 - <<'EOF'
from datetime import datetime

spec = """# rstack-ideate business spec
# Generated: {date}

## Agent
{description}  # from Q1

## Revenue streams
primary:
  type: {type}              # service_gateway | data_storefront | blog | courses | ask_inbox | sponsored_slots | prompt_library | research_reports | paywalled_content
  suggested_price: {price}  # operator should tune based on value delivered
supporting:
  - type: {type}
    note: {rationale}
  - type: tip_jar
    note: always-on, no extra config required

## Discovery features
pulse: true
testimonials: true
contact_form: {true|false}
waitlist: {true|false}

## Audience building
newsletter: {true|false}

## Skill execution order
1. rstack-bootstrap
2. rstack-page
3. rstack-{primary_skill}
4. rstack-{secondary_skill}   # omit if minimal setup
5. rstack-distribute
6. rstack-audit

## Key operator API calls
POST /account/payout-address
{primary setup call}
{secondary setup call}
""".format(date=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

with open('/tmp/rstack_ideate_spec.md', 'w') as f:
    f.write(spec)

print("Business spec written to /tmp/rstack_ideate_spec.md")
EOF
```

Fill in all `{placeholders}` from the conversation before writing. Print a human-readable summary:

```
Business spec saved. Here's your plan:

  Agent:    {description}
  Primary:  {block} at {price}
  + {supporting block 1}
  + {supporting block 2}
  + Tip Jar (always-on)

  Next step: /rstack-bootstrap
  (or skip to /rstack-page if you already have an account)
```

---

## Completion Status

**DONE** — Spec written to `/tmp/rstack_ideate_spec.md`. End with:

> "You're ready to build. Run `/rstack-bootstrap` to set up your account, registration, and wallet — it will read the spec if you run it in the same session."

**DONE_WITH_CONCERNS** — If the operator skipped questions or gave ambiguous answers, list each gap and the default assumed:

> "I assumed [X] for [question]. If that's wrong, re-run `/rstack-ideate` or adjust the spec at `/tmp/rstack_ideate_spec.md` before proceeding."

**BLOCKED** — Should not occur (no auth required). If an API call fails during the optional dashboard check, continue without it — it's not a blocker.
