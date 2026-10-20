---
name: launch-initiative
description: Use when the user wants to launch, start, or set up a NEW initiative on Boom, an AI conversation with a group of customers over WhatsApp, for any job: winning back customers who dropped off, qualifying leads, onboarding, collecting documents or data, NPS follow-up, product research. Covers the objective, context and guiding questions, the opening template, enrolling participants, and launching. For an initiative that already exists, use manage-participants or analyze-results.
---

# Launch an Initiative

An initiative is one mission: an audience, a goal, and the flow that carries it out. Its quality is decided by three text fields — `objective`, `context`, and the guiding questions — because they go straight into the agent's prompt. This skill encodes how Boom's highest-performing production initiatives write them, and the formulas hold whatever the job is.

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `initiatives_create` / `initiatives_update` | Create/edit the initiative (DRAFT only is editable) | write |
| `initiatives_get` | Verify configuration before launch | read |
| `whatsapp_numbers_list` | Discover the org's WhatsApp sender numbers | read |
| `templates_list` / `templates_create` | Pick or create the opening template — see `whatsapp-templates` | read / write |
| `initiatives_templates_get` / `initiatives_templates_set` | Attach opener + follow-up templates to the initiative | read / write |
| `extraction_schema_get` / `extraction_schema_set` | Read/declare the typed fields to pull from every conversation, set before launch | read / write |
| `initiatives_participants_add` | Enroll people | **admin** |
| `initiatives_launch` | Start outreach | **admin** |
| `drafts_list` / `drafts_count` / `drafts_decide` | Review, count and approve sends held as drafts (optional step 9) | read / write |

> Tool names may drift while Boom's MCP is in beta. On `tool_not_found`, list tools and match the `domain_action` pattern.

## When to use / when not to

- Use whenever a group of customers needs a real conversation with a goal: win back the ones who dropped off, qualify inbound leads, walk someone through onboarding, collect a missing document, follow up an NPS score, understand why people churn.
- NOT for a one-off blast. An initiative holds a multi-turn conversation and pursues an objective; if you only need to push a message, that's a flow with a send step (see `design-journey`).
- Only reading existing results → `analyze-results`. Audience building → `cdp-and-segments`.

## Workflow

1. **Clarify the goal.** One sentence: what should be true when this initiative has run? A decision to inform, a customer recovered, a document collected, a lead qualified. Push back on survey-shaped asks: the agent holds a real conversation and follows up, so use that.
2. **Draft the three core fields** using the formulas below. Show them to the user before creating anything.
3. **Create** with `initiatives_create` — only `name` is required, but always send: `objective`, `context`, `guidingQuestions[]`, `language` (default `es`), `identityDeflection`, `flagCondition`, `maxAttempts`. It's created as **DRAFT** with **no journey**: nothing is scaffolded for you.
   - **Guiding questions are write-once.** `initiatives_update` cannot change them and there is no delete capability, so a wrong question list means cancelling the initiative and rebuilding it. Settle the questions with the user *before* this call.
   - **The name must be unique in the org.** A duplicate currently fails as a bare `Internal error`, not a clean conflict, so check `initiatives_list` first.
4. **Build the journey** — `journeys_create_draft`, then `journeys_validate` (see `design-journey`). An initiative created over MCP or REST has no journey until you make one, and it cannot launch without one.
5. **Attach the opener**: `whatsapp_numbers_list` → pick/create the template (see `whatsapp-templates`) → `initiatives_templates_set`. New templates take ~24–48h for Meta approval — create them early. On an email initiative the first send is a `SEND_EMAIL` node with a published email template instead, see `email-templates`; there's no approval wait.
6. **Set the extraction schema before launching**, if the mission needs structured fields back (`extraction_schema_set`). A conversation is extracted against whichever schema was current when it ran, and a closed conversation can't be re-extracted under new fields via the API, so declare it now rather than after the first results come in. Six field types (`bool`, `int`, `enum`, `enum[]`, `string`, `string[]`); `topic`, `problem`, and `competitor` are reserved slugs that get rejected. Each field's `description` is the instruction the model reads to fill it, not a label, so write it like a briefing. Extraction only runs on conversations with at least 3 messages and 1 inbound reply: a cold audience that stays silent yields no fields for whoever never answers.
7. **Verify** with `initiatives_get`; read back name/objective/template/journey. **Launching and enrolling message real customers, get explicit confirmation.**
8. **Launch** with `initiatives_launch` (requires org admin). This flips DRAFT → ACTIVE and publishes the journey for you, on the WhatsApp or the email channel, so no separate `journeys_publish` is needed. Launching with nobody enrolled sends nothing, which is what makes the next step safe to stage.
9. **(Optional) review the first sends as drafts.** For a first run to a new audience, set `delivery: "draft"` on the journey's send nodes (template WhatsApp or email) before launching. Each send is then held on the initiative's **Drafts** tab until someone approves it, so the user can read real, personalized messages before anyone receives them. Approve with `drafts_decide` only after the user has seen the content and said yes. Switch back to immediate delivery in a new journey version once they trust it. Not available on Transactional initiatives. See `design-journey`, "Hold sends for approval".
10. **Enroll participants** (`initiatives_participants_add`, with `phoneNumber` on WhatsApp or `email` on email, see `manage-participants`) — **after launch, not before.** Enrollment requires an ACTIVE initiative and a published journey; on a DRAFT it fails with `initiative_not_active`. Each person added **receives a real message immediately**, so enroll one test contact first, confirm it arrives and reads correctly, then add the rest.

## Enrolling people

**Phone format differs by surface, and each one rejects the other's.** `initiatives_participants_add` wants E.164 **with** the leading `+` (`+573001234567`). The CSV upload in the app wants **bare digits, no `+`**, 10 to 15 of them. Same number, two spellings — format for the door you're walking through.

**To enroll a list in bulk, use `initiatives_participants_add`** (up to 500 people per call). It works even when the journey's `ENTRY` is event-triggered, because enrollment doesn't check what the trigger declares. Do **not** reach for `cdp_events_batch_record` to start people in bulk: the batch endpoint deliberately does not fire journey enrollment, so you would load hundreds of events and enroll nobody, with no error to tell you. Only the single-event endpoint enrolls.

**DNC is enforced server-side.** A lower participant count than the list you sent means suppression. Report the delta and never retry those entries.

## Giving the agent per-participant data

The initiative `context` is a **static briefing, not a template** — nothing in it is interpolated, so writing "adapt to `{{plan}}`" there gets you literal text and no value. Per-participant data reaches the conversation through two places instead:

| Where you put it | How it arrives | Reliability |
|---|---|---|
| Participant `context` at enrollment (CSV columns, `participants_add`) | Pushed into every turn as that person's own data, labelled with your `contextSchema` descriptions | **Unconditional.** The default, and what to use whenever the audience arrives as a list |
| The triggering event's `properties` | Frozen at enrollment, pushed in as workflow state | **Unconditional.** For event-triggered flows, where your system already knows the values |
| A CDP person attribute, fetched with `read_person` | The agent calls the tool mid-conversation and reads the attributes back | **Conditional** — see below |

Then **reference those field names in the `context` briefing** so the agent knows what to do with them — the values arrive as data, the instruction for using them is yours to write. Say what to do with each value, and say what not to do with it: "use it to calibrate the question, never quote the number back to them" is the kind of line that keeps a personalized opener from reading like surveillance.

### The CDP path, and why it is not the default

The agent *can* reach live CDP data: `read_person` returns a person's full `attributes`, the prompt hands it that person's id for free whenever the WhatsApp sender resolves unambiguously, and a data catalogue lists the attribute keys the organization has. That makes it genuinely useful for something the agent should look up *because the conversation went there*.

It is the wrong tool for personalizing an opener, for three reasons worth knowing before you design around it:

- **The tool is entitled per organization, and nothing is on by default.** If the org has no access row for `read_person`, the agent simply does not have it that turn, and there is no error to notice.
- **The catalogue only lists the first few attribute keys inline** (alphabetically). Past that it tells the agent to ask for the full list, which is one more call the agent has to decide to make.
- **Nothing forces the call.** Naming an attribute in the briefing does not make the model go fetch it. Models reliably call a tool they were told to call, and unreliably fetch a number nobody asked them for.

So: if a value matters to **every** conversation, push it in at enrollment where it arrives unconditionally. If you do want a lookup, write the instruction as an imperative that names the tool — "before your opening line, call `read_person` for this customer and check `transaction_days_30d`" — rather than mentioning the field and hoping.

## Writing the `objective` (≤2000 chars; aim for 1–3 sentences)

This becomes the agent's *entire purpose*. State **what to understand, about whom, at which moment**:

> "Entender por qué los usuarios que mostraron interés en un financiamiento recibieron el mensaje con éxito pero no abrieron el link para completar su onboarding digital."

Not a topic ("churn feedback"), not a question list — one understanding-goal.

## Writing the `context` (≤5000 chars Markdown) — the formula

Production initiatives with the best interview quality all include these six blocks:

1. **Business flow** — how the product/process works, step by step, so the agent never guesses. Name internal projects, partners, plans.
2. **What the participant already experienced** — quote verbatim any prior messages they got, the screen they abandoned, the plan they canceled. The agent can then reference reality: "el mensaje donde te compartimos el link…"
3. **Who the participants are** — customers? churned? leads who never converted? their relationship to the brand ("no son clientes de Nexu, solo leads que iniciaron con otra financiera").
4. **Brand presentation rules** — what name to present as (sub-brands per partner: "preséntate como KIA Trust, nunca como Nexu"), tone constraints, language/formality.
5. **No-go topics** — words and topics to avoid ("no destaques la palabra 'rechazo'", "nada que deje mal a Inbursa"), plus what to do when asked something off-script.
6. **How much to say per turn** — the five blocks above are the agent's *reference material*; this one is the only thing that stops it reading them aloud. One short message per turn, one question per turn and put it last, never restate what the opening template already said, and mark which blocks are for later ("the account portal is for someone who already subscribed — don't raise it yourself"). Include one worked example of a good turn: showing the target length lands far better than describing it.

**A context that reads like documentation gets recited like documentation.** A
well-grounded agent with no turn budget will cover every block you gave it, in one
go. This is easy to wave through in review because nothing in the reply is *wrong*:
the facts check out, the links work, the tone is right — it is simply all of it, at
once, including the offer the template just made and the instructions for a state the
customer is not in yet. Formatting rules ("don't paste a numbered list") do not fix
it; they change how the answer looks, not how much it says. Budget the turn, and mark
the blocks that are for later.

Optionally: behavioral-science framing ("sé respetuoso y no invasivo al explorar el porqué de su inacción"). Files can be referenced with `[name](asset:<id>)` mentions if uploaded in the app.

## Guiding questions — use the whole schema

4–8 questions is the production sweet spot (≤50 allowed). Each supports:

| Field | Values | Use |
|---|---|---|
| `questionText` | ≤280 chars | The question, in the initiative's language |
| `answerType` | `OPEN` \| `MULTIPLE_CHOICE` \| `BOOLEAN` \| `SCALE` | `OPEN` for research; `SCALE` needs `scaleMin`/`scaleMax`; `MULTIPLE_CHOICE` takes `options[]` (≤20) |
| `priority` | 1–5 | Interview order/importance — the agent covers high-priority first |
| `followUpDepth` | `NONE` \| `LIGHT` \| `STANDARD` \| `DEEP` | How hard the AI digs. `DEEP` on the 1–2 questions the decision hinges on; `LIGHT` elsewhere keeps interviews short |
| `evaluationCriterion` | free text | What counts as a *complete* answer — drives the analyzer ("respuesta completa = causa concreta + si volvería a intentarlo") |

Pattern from winners: Q1 = the core "why" (DEEP), Q2 = reaction to the concrete artifact they saw (quote it in context), Q3 = what would have changed their behavior, Q4 = situational factors (timing, alternatives).

## The supporting fields

- **`identityDeflection`** — how the agent answers "are you a bot?". Honest + warm + human-oversight works best in production: *"Sí, soy un bot pero del bueno 😊 — todas las respuestas las lee una persona del equipo, y tu opinión de verdad nos ayuda a mejorar."* Never instruct it to deny being an AI.
- **`flagCondition`** — natural-language condition that flags a conversation for human review. Flag *actionable* moments, not sentiment: "el usuario expresa que aún le interesa obtener su préstamo", "menciona una mala práctica del asesor". One condition, concrete and observable.
- **`maxAttempts`** (1–5, default 3) — how many outreach rounds this mission gets. It sizes nothing on its own: you build the journey to match, with one approved follow-up template per extra round.
- **`contextSchema`** — declares the per-participant variables you pass at enrollment (e.g. `{"credit_line": "monto de línea aprobada"}`). **Not settable over MCP or REST**: it is written by the CSV-upload flow in the Boom app, or derived automatically from the first enrolled participant's attributes if it was never set. It *is* enforced either way — `initiatives_participants_add` rejects any `context` key that isn't in it. Two consequences worth planning around: if you enroll over the API into an initiative with no schema, whoever lands first silently defines the allowed keys for everyone after them (capped at 50), and any key you forgot is rejected rather than ignored. Keep keys snake_case and short.
- **End conditions** — `endConditionType`: `MANUAL` (default), `DATE` (+`endDate`), or `RESPONSE_COUNT` (+`endResponseTarget`). `isRecurring` + `reportCadence` (`WEEKLY`/`BIWEEKLY`/`MONTHLY`) for always-on programs.

## Boom best practices

- 50–300 participants per batch. WhatsApp response rates far exceed email, but **what actually moves the rate is who the audience is, not how many** — set the expectation from the relationship, not the list size. An active customer answers far more than someone who churned; someone who churned two days ago answers far more than someone who churned two months ago. Production spans roughly 70–90% on warm, current audiences down to the mid-20s on people who left a while back, and a cold cohort landing at 25% is the normal result, not a failure. Say the number out loud before launch so nobody reads a healthy run as a bad one.
- Spanish (`es`) is the default and >98% of production volume; write all agent-facing text in the participant's language.
- DNC is enforced server-side — a lower participant count than the list you sent means suppression; report the delta, never retry those entries.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `forbidden` on participants/launch | The signed-in user isn't an org admin | An org admin runs it, or launch from the Boom app |
| `initiative_not_active` on `participants_add` | You enrolled before launching | Launch first, then enroll — see step 10 |
| Bare `Internal error` on `initiatives_create` | Almost always a duplicate initiative name in the org | Check `initiatives_list` and pick another name. The underlying uniqueness conflict isn't mapped to a clean error yet |
| `initiatives_update` rejected | Initiative left DRAFT | Only DRAFT is editable; changes after activation go through the app |
| `guidingQuestions` ignored on update | They can only be set at creation | No public edit path — cancel and recreate, or fix it in the app |
| Launched and enrolled, but nothing sent | A send node has `delivery: "draft"`, so the messages are waiting for approval | Check the initiative's **Drafts** tab or `drafts_list` for PENDING drafts; approve them once the user has reviewed the content |
| Launch succeeds, then no message arrives | A round's template was still `PENDING` when that round fired | **Nothing checks template approval before sending.** `journeys_validate`, publish and launch all pass with unapproved templates; the failure only appears per-send, as free text on the step, with no error code. Confirm every round is `APPROVED` with `templates_list` before you enroll anyone |
| `409 initiative_not_draft` on launch | Already launched, or cancelled/archived | Only a DRAFT launches |
| `422 no_outreach_template` on launch | Round one has no approved, active WhatsApp template linked | Approve/attach one first, see `whatsapp-templates` |
| `422 journey_not_ready` on launch | The journey behind it failed validation at publish, or there is no journey at all (WhatsApp and email alike) | The response lists the issues; fix them with `design-journey`'s tools and launch again |
| `422 initiative_not_ready` on launch | A required field is missing, or rewards aren't set up | The message names what's missing; check `initiatives_get` |
| Template stuck in PENDING | Meta review (~24–48h) | Create templates first; check back with `templates_list` |
| Participant `context` rejected | Keys don't match `contextSchema` | Align keys exactly (case-sensitive) |
| Interviews feel generic | `context` missing blocks 2/4/5 of the formula | Rewrite context; quote the actual artifacts participants saw |

See [`CONTEXT.md`](../../CONTEXT.md) for the domain model.
